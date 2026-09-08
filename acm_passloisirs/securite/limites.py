"""Limitation de débit, anti-rejeu et validation des entrées.

Vecteurs d'attaque couverts :
  A8 — formulaire public noyé sous des milliers de soumissions. Sur une base à
       quota d'enregistrements, l'attaquant ne vole rien : il sature, et le
       service s'arrête. Déni de service « par le bas », très peu coûteux.
  Rejeu — une même soumission renvoyée n fois crée n enregistrements.
  A9 — injection indirecte : neutraliser le contenu hostile AVANT stockage,
       pour qu'il ne soit pas rejoué plus tard à une IA ou dans un e-mail.

Audit S05 : « protection anti-rejeu et contre les doublons ; limites d'usage »
et contrôle C07 : « Fichier interdit, formulaire répété, événement doublonné :
refus/traitement contrôlé, sans altération des données ».
"""

from __future__ import annotations

import hashlib
import re
import time
import unicodedata
from collections import deque
from dataclasses import dataclass, field


class TropDeRequetes(Exception):
    """Levée quand un appelant dépasse son quota."""


class EntreeInvalide(ValueError):
    """Levée quand une entrée ne respecte pas le format attendu."""


@dataclass
class LimiteurDebit:
    """Fenêtre glissante en mémoire.

    LIMITE ASSUMÉE : l'état vit dans le processus. Avec plusieurs instances
    derrière un répartiteur de charge, il faut le déporter (Redis, ou la
    limitation de l'hébergeur). Le noter plutôt que de croire le problème
    résolu : un limiteur qui ne compte qu'un serveur sur trois protège trois
    fois moins qu'annoncé.
    """

    max_requetes: int = 5
    fenetre_secondes: float = 60.0
    _historique: dict[str, deque[float]] = field(default_factory=dict)

    def verifier(self, cle: str, maintenant: float | None = None) -> None:
        """Enregistre un appel et lève TropDeRequetes si le quota est dépassé."""
        instant = maintenant if maintenant is not None else time.monotonic()
        journal = self._historique.setdefault(cle, deque())

        limite_basse = instant - self.fenetre_secondes
        while journal and journal[0] <= limite_basse:
            journal.popleft()

        if len(journal) >= self.max_requetes:
            raise TropDeRequetes(
                f"Quota dépassé : {self.max_requetes} requêtes "
                f"par {int(self.fenetre_secondes)} s."
            )
        journal.append(instant)


@dataclass
class GardeAntiRejeu:
    """Empêche qu'une même soumission soit comptée deux fois.

    On stocke une EMPREINTE du contenu, jamais le contenu : le garde ne doit
    pas devenir lui-même un entrepôt de données personnelles.
    """

    fenetre_secondes: float = 3600.0
    _vues: dict[str, float] = field(default_factory=dict)

    @staticmethod
    def empreinte(*parties: str) -> str:
        brut = "\x1f".join(parties)
        return hashlib.sha256(brut.encode("utf-8")).hexdigest()

    def est_rejeu(self, empreinte: str, maintenant: float | None = None) -> bool:
        instant = maintenant if maintenant is not None else time.monotonic()
        self._purger(instant)
        if empreinte in self._vues:
            return True
        self._vues[empreinte] = instant
        return False

    def _purger(self, instant: float) -> None:
        limite = instant - self.fenetre_secondes
        for cle in [c for c, t in self._vues.items() if t <= limite]:
            del self._vues[cle]


# --- Validation des entrées ------------------------------------------------

#: Champs acceptés par le formulaire public de préinscription.
#: Liste blanche stricte : aucun champ de santé, conformément à S02.
CHAMPS_PREINSCRIPTION_AUTORISES = frozenset(
    {"nom", "prenom", "telephone", "email", "formule_reperee",
     "debut_repere", "besoin_particulier", "note"}
)

_MOTIF_TELEPHONE = re.compile(r"^\+?[0-9 .\-]{6,20}$")
_MOTIF_EMAIL = re.compile(r"^[^@\s]+@[^@\s.]+\.[^@\s]{2,}$")

#: Caractères de contrôle et marques de direction : vecteurs classiques de
#: dissimulation de texte (une instruction peut être rendue invisible à
#: l'œil tout en restant lue par un automate).
_CARACTERES_INVISIBLES = re.compile(
    "["
    "\u0000-\u0008\u000b-\u001f\u007f"   # caracteres de controle
    "\u200b-\u200f"                        # espaces de largeur nulle, marques de direction
    "\u2028\u2029"                          # separateurs de ligne et de paragraphe
    "\u202a-\u202e"                        # forcage de direction (texte affiche a l envers)
    "\u2066-\u2069"                        # isolats de direction
    "\ufeff"                                # marque d ordre des octets
    "]"
)


def nettoyer_texte(valeur: str, longueur_max: int = 500) -> str:
    """Normalise et neutralise un texte libre avant stockage.

    Ne « désinfecte » pas une injection — on ne peut pas deviner toutes les
    formulations hostiles. On supprime ce qui sert à la DISSIMULER, et on
    borne la longueur. La vraie protection contre A9 reste de ne jamais
    traiter un contenu stocké comme une instruction.
    """
    if not isinstance(valeur, str):
        raise EntreeInvalide("Valeur textuelle attendue.")
    texte = unicodedata.normalize("NFKC", valeur)
    texte = _CARACTERES_INVISIBLES.sub("", texte)
    texte = texte.strip()
    if len(texte) > longueur_max:
        raise EntreeInvalide(f"Texte trop long ({len(texte)} > {longueur_max}).")
    return texte


def valider_preinscription(charge_utile: dict[str, object]) -> dict[str, str]:
    """Valide une soumission publique. Rejette tout champ non prévu.

    Rejeter explicitement au lieu d'ignorer : un champ inattendu est soit une
    erreur d'intégration, soit une tentative de forcer une valeur (par
    pré-remplissage d'URL, par exemple). Dans les deux cas, il faut le savoir.
    """
    inconnus = set(charge_utile) - CHAMPS_PREINSCRIPTION_AUTORISES
    if inconnus:
        raise EntreeInvalide(
            "Champs non autorisés : " + ", ".join(sorted(inconnus))
        )

    for obligatoire in ("nom", "prenom"):
        if not str(charge_utile.get(obligatoire, "")).strip():
            raise EntreeInvalide(f"Champ obligatoire manquant : {obligatoire}.")

    propre: dict[str, str] = {}
    for cle, valeur in charge_utile.items():
        texte = nettoyer_texte(str(valeur), longueur_max=1000 if cle == "note" else 200)
        if cle == "telephone" and texte and not _MOTIF_TELEPHONE.match(texte):
            raise EntreeInvalide("Numéro de téléphone invalide.")
        if cle == "email" and texte and not _MOTIF_EMAIL.match(texte):
            raise EntreeInvalide("Adresse électronique invalide.")
        if cle == "besoin_particulier" and texte not in {"", "Oui", "Non"}:
            # Booléen strict : aucun détail médical ne doit transiter ici.
            raise EntreeInvalide(
                "« besoin_particulier » n'accepte que Oui ou Non : le "
                "formulaire public ne collecte aucun détail de santé."
            )
        propre[cle] = texte
    return propre


#: Types de fichiers acceptés en dépôt. Liste blanche.
TYPES_FICHIERS_AUTORISES = frozenset({"application/pdf", "image/jpeg", "image/png"})
TAILLE_MAX_FICHIER = 10 * 1024 * 1024  # 10 Mo


def valider_fichier(nom: str, type_mime: str, taille_octets: int) -> str:
    """Valide un dépôt de fichier et renvoie un nom de stockage neutralisé."""
    if type_mime not in TYPES_FICHIERS_AUTORISES:
        raise EntreeInvalide(f"Type de fichier refusé : {type_mime}.")
    if taille_octets <= 0 or taille_octets > TAILLE_MAX_FICHIER:
        raise EntreeInvalide("Taille de fichier hors limites.")

    # Le nom fourni par le client n'est jamais réutilisé tel quel :
    # il peut contenir des séquences de remontée de répertoire (« ../ »).
    base = nom.replace("\\", "/").split("/")[-1]
    base = _CARACTERES_INVISIBLES.sub("", base)
    base = re.sub(r"[^A-Za-z0-9._-]", "_", base)[-100:]
    if not base or base.startswith("."):
        raise EntreeInvalide("Nom de fichier invalide.")
    return base
