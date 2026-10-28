"""Configuration locale : dossier de données portable et charte graphique.

Le dossier de données est, par défaut, `donnees_yeba/` À CÔTÉ du logiciel :
copier le dossier complet sur une clé USB ou un autre PC/Mac suffit pour
tout déplacer (projets, charte, tarifs, décisions de publication).
Variable d'environnement possible : YEBA_DATA_DIR.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from .securite import restreindre_droits

RACINE_LOGICIEL = Path(__file__).resolve().parent.parent
NOM_YEBA = "YEBA FORMATIONS"


def dossier_donnees() -> Path:
    d = Path(os.environ.get("YEBA_DATA_DIR") or (RACINE_LOGICIEL / "donnees_yeba"))
    d.mkdir(parents=True, exist_ok=True)
    restreindre_droits(d)
    for sous in ("projets", "site_a_publier", "charte", "tarifs"):
        (d / sous).mkdir(exist_ok=True)
        restreindre_droits(d / sous)
    return d


_HEX = re.compile(r"^#?[0-9A-Fa-f]{6}$")


@dataclass
class Charte:
    """Charte graphique. Les couleurs par défaut sont NEUTRES et à remplacer
    par les codes exacts de la charte YEBA FORMATIONS (non fournis à ce jour)."""
    nom_organisme: str = NOM_YEBA
    couleur_primaire: str = "1F3A5F"     # titres, en-têtes (À REMPLACER)
    couleur_secondaire: str = "E07A1F"   # accents, verbes Bloom (À REMPLACER)
    couleur_claire: str = "EEF3F8"       # bandes alternées
    couleur_texte: str = "1A1A1A"
    police: str = "Arial"
    taille_texte: int = 14               # lisibilité malvoyants : 14 minimum
    taille_titre: int = 22
    logo: str = ""                       # chemin relatif dans charte/
    couleurs_validees: bool = False      # passe à True quand vous avez saisi vos codes

    def valider(self) -> list[str]:
        erreurs = []
        for nom in ("couleur_primaire", "couleur_secondaire", "couleur_claire", "couleur_texte"):
            v = getattr(self, nom).lstrip("#")
            if not _HEX.match(v):
                erreurs.append(f"{nom} : code couleur invalide (format attendu : #1F3A5F)")
            else:
                setattr(self, nom, v.upper())
        self.taille_texte = max(14, min(int(self.taille_texte), 28))
        self.taille_titre = max(self.taille_texte + 4, min(int(self.taille_titre), 40))
        self.police = re.sub(r"[^A-Za-z0-9 \-]", "", self.police)[:40] or "Arial"
        self.nom_organisme = self.nom_organisme.strip()[:120]
        return erreurs

    def chemin_logo(self, base: Path) -> Path | None:
        if not self.logo:
            return None
        p = (base / "charte" / Path(self.logo).name)
        return p if p.exists() else None


def charger_charte(base: Path | None = None) -> Charte:
    base = base or dossier_donnees()
    f = base / "charte" / "charte.json"
    if f.exists():
        donnees = json.loads(f.read_text(encoding="utf-8"))
        champs = {k: v for k, v in donnees.items() if k in Charte.__dataclass_fields__}
        c = Charte(**champs)
    else:
        c = Charte()
    c.valider()
    return c


def enregistrer_charte(c: Charte, base: Path | None = None) -> list[str]:
    base = base or dossier_donnees()
    erreurs = c.valider()
    if not erreurs:
        f = base / "charte" / "charte.json"
        f.write_text(json.dumps(asdict(c), ensure_ascii=False, indent=2), encoding="utf-8")
        restreindre_droits(f)
    return erreurs


@dataclass
class Identite:
    """Qui apparaît sur les documents d'un projet.

    Règle contractuelle : si la formation est réalisée POUR un autre centre
    (ICCI, TETRANERGY, PAM OI, GEM FORMATION…), YEBA FORMATIONS et son logo
    n'apparaissent JAMAIS ; on affiche le centre commanditaire (ou rien).
    """
    commanditaire: str = ""          # vide = formation YEBA FORMATIONS
    afficher_logo: bool = True
    afficher_nom: bool = True

    @property
    def est_yeba(self) -> bool:
        c = self.commanditaire.strip().upper()
        return not c or c == NOM_YEBA

    def nom_affiche(self, charte: Charte) -> str:
        if not self.afficher_nom:
            return ""
        return charte.nom_organisme if self.est_yeba else self.commanditaire.strip()

    def logo_autorise(self) -> bool:
        return self.afficher_logo and self.est_yeba


@dataclass
class Reglages:
    """Paramètres d'un projet saisis dans l'interface (sérialisables)."""
    titre_projet: str = ""
    heures_centre: float = 0
    heures_entreprise: float = 0
    date_debut: str = ""
    date_examen: str = ""
    creneaux: str = "08:30-12:00, 13:00-16:30"
    pauses: str = "10:15-10:30, 14:45-15:00"
    jours: str = "1,2,3,4,5"          # 1 = lundi
    rythme: str = ""
    fermetures: str = ""             # « 2027-02-15..2027-02-19 Vacances ; 2027-03-08 Alerte rouge »
    ordre_cp: str = ""
    poids_cp: str = ""               # « 1=40, 5=30 »
    commanditaire: str = ""
    afficher_logo: bool = True
    afficher_nom: bool = True
    h_accueil: float = 7
    h_ecf_par_at: float = 3.5
    h_dossier_pro: float = 14
    h_productions: float = 21
    h_examen_blanc: float = 0
    h_bilan: float = 3.5
    referent_handicap: str = ""
    delai_acces: str = ""
    modalites_pedagogiques: str = "Présentiel, pédagogie active : apports, études de cas, mises en situation, jeux de rôle"
    public: str = ""
    prerequis: str = ""
    lieu: str = ""

    @classmethod
    def depuis_dict(cls, d: dict) -> "Reglages":
        r = cls()
        for nom, champ in cls.__dataclass_fields__.items():
            if nom not in d:
                if champ.type == "bool" and d:
                    setattr(r, nom, False)   # case décochée = absente du formulaire
                continue
            v = d[nom]
            if champ.type == "bool":
                v = v in (True, "1", "on", "true", "oui")
            elif champ.type == "float":
                try:
                    v = max(0.0, float(str(v).replace(",", ".").strip() or 0))
                except ValueError:
                    v = 0.0
            else:
                v = str(v)[:2000]
            setattr(r, nom, v)
        return r

    def en_dict(self) -> dict:
        return asdict(self)


def identite_depuis(reglages: Reglages) -> Identite:
    return Identite(commanditaire=reglages.commanditaire, afficher_logo=reglages.afficher_logo,
                    afficher_nom=reglages.afficher_nom)


__all__ = ["Charte", "Identite", "Reglages", "charger_charte", "enregistrer_charte", "dossier_donnees",
           "identite_depuis", "NOM_YEBA", "RACINE_LOGICIEL"]
