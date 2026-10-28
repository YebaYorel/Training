"""Sécurité du logiciel de décorticage — YEBA FORMATIONS.

Ce module regroupe toutes les protections contre les fichiers piégés et les
accès non autorisés :

* contrôle des fichiers reçus (extension + signature réelle du fichier,
  taille, bombes ZIP, macros VBA, chemins piégés dans les archives) ;
* nettoyage des noms de fichiers (anti « path traversal ») ;
* neutralisation des formules dans les cellules Excel (anti « injection de
  formule » / CSV injection) ;
* mot de passe local haché (PBKDF2-SHA256, 600 000 itérations, sel aléatoire)
  avec blocage progressif après plusieurs échecs.

Aucune donnée ne quitte l'ordinateur : pas d'appel réseau dans ce module.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import secrets
import stat
import time
import unicodedata
import zipfile
from pathlib import Path
from typing import Optional

# --------------------------------------------------------------------------
# Limites (volontairement strictes : un REAC fait ~1 Mo)
# --------------------------------------------------------------------------
TAILLE_MAX_FICHIER = 50 * 1024 * 1024          # 50 Mo par fichier reçu
TAILLE_MAX_DECOMPRESSEE = 250 * 1024 * 1024    # 250 Mo une fois décompressé
RATIO_MAX_COMPRESSION = 120                    # au-delà : bombe ZIP probable
NB_MAX_ENTREES_ZIP = 5000
NB_MAX_PAGES_PDF = 400

EXTENSIONS_DOCUMENTS = {".pdf", ".docx", ".xlsx", ".txt", ".csv"}
EXTENSIONS_IMAGES = {".png", ".jpg", ".jpeg"}

# Formats refusés avec une explication claire (macros ou formats binaires
# anciens, vecteurs classiques d'attaques).
EXTENSIONS_REFUSEES = {
    ".docm": "Word avec macros : enregistrez-le en .docx (sans macros).",
    ".xlsm": "Excel avec macros : enregistrez-le en .xlsx (sans macros).",
    ".doc": "ancien format Word : ouvrez-le puis « Enregistrer sous » .docx.",
    ".xls": "ancien format Excel : ouvrez-le puis « Enregistrer sous » .xlsx.",
    ".odt": "format LibreOffice : exportez-le en .docx ou .pdf.",
    ".ods": "format LibreOffice : exportez-le en .xlsx.",
}


class FichierRefuse(ValueError):
    """Le fichier reçu ne passe pas les contrôles de sécurité."""


# --------------------------------------------------------------------------
# Noms de fichiers
# --------------------------------------------------------------------------
def nom_fichier_sur(nom: str, defaut: str = "fichier") -> str:
    """Retourne un nom de fichier sans chemin, sans caractère dangereux.

    >>> nom_fichier_sur("../../etc/passwd")
    'passwd'
    >>> nom_fichier_sur("REAC MEM (v09).pdf")
    'REAC_MEM_v09.pdf'
    """
    nom = (nom or "").replace("\\", "/").split("/")[-1]
    nom = unicodedata.normalize("NFKD", nom).encode("ascii", "ignore").decode()
    nom = re.sub(r"[^A-Za-z0-9._-]+", "_", nom).strip("._")
    nom = re.sub(r"_+", "_", nom)
    if not nom or nom in {".", ".."}:
        nom = defaut
    racine, ext = os.path.splitext(nom)
    return racine[:80] + ext[:10].lower()


def chemin_dans(base: Path, *morceaux: str) -> Path:
    """Construit un chemin et vérifie qu'il reste DANS `base`.

    Lève FichierRefuse si quelqu'un tente de sortir du dossier
    (ex. « ../../ »), y compris via un lien symbolique.
    """
    base_res = base.resolve()
    cible = base_res.joinpath(*morceaux).resolve()
    if cible != base_res and base_res not in cible.parents:
        raise FichierRefuse("Chemin interdit (tentative de sortie du dossier).")
    return cible


# --------------------------------------------------------------------------
# Contrôle des fichiers reçus
# --------------------------------------------------------------------------
def _verifier_zip(contenu_chemin: Path, attendu: str) -> None:
    """Contrôles anti-bombe ZIP, anti-macro et anti-chemin pour docx/xlsx."""
    try:
        with zipfile.ZipFile(contenu_chemin) as zf:
            infos = zf.infolist()
            if len(infos) > NB_MAX_ENTREES_ZIP:
                raise FichierRefuse("Archive anormale (trop d'éléments).")
            total = 0
            noms = set()
            for info in infos:
                n = info.filename
                if n.startswith("/") or ".." in n.split("/") or "\\" in n:
                    raise FichierRefuse("Archive piégée (chemin interdit).")
                total += info.file_size
                if info.compress_size and info.file_size / max(info.compress_size, 1) > RATIO_MAX_COMPRESSION:
                    raise FichierRefuse("Archive suspecte (bombe de décompression).")
                noms.add(n.lower())
            if total > TAILLE_MAX_DECOMPRESSEE:
                raise FichierRefuse("Fichier trop volumineux une fois décompressé.")
            if any(n.endswith("vbaproject.bin") for n in noms):
                raise FichierRefuse("Le fichier contient des macros : refusé.")
            if attendu not in noms:
                raise FichierRefuse("Le contenu ne correspond pas à l'extension annoncée.")
    except zipfile.BadZipFile as exc:
        raise FichierRefuse("Fichier corrompu ou déguisé.") from exc


def verifier_fichier(chemin: Path, extensions: Optional[set] = None) -> str:
    """Vérifie un fichier reçu. Retourne son extension normalisée.

    Le type est vérifié par la *signature* du fichier, pas seulement par son
    nom : un .exe renommé en .pdf est refusé.
    """
    extensions = extensions or EXTENSIONS_DOCUMENTS
    ext = chemin.suffix.lower()
    if ext in EXTENSIONS_REFUSEES:
        raise FichierRefuse(f"Format refusé — {EXTENSIONS_REFUSEES[ext]}")
    if ext not in extensions:
        raise FichierRefuse(
            f"Extension « {ext or '(aucune)'} » non acceptée. "
            f"Formats acceptés : {', '.join(sorted(extensions))}."
        )
    taille = chemin.stat().st_size
    if taille == 0:
        raise FichierRefuse("Fichier vide.")
    if taille > TAILLE_MAX_FICHIER:
        raise FichierRefuse("Fichier trop volumineux (50 Mo maximum).")

    with open(chemin, "rb") as fh:
        entete = fh.read(16)

    if ext == ".pdf":
        if b"%PDF-" not in entete[:8]:
            raise FichierRefuse("Ce fichier n'est pas un vrai PDF.")
    elif ext == ".docx":
        if not entete.startswith(b"PK\x03\x04"):
            raise FichierRefuse("Ce fichier n'est pas un vrai document Word (.docx).")
        _verifier_zip(chemin, "word/document.xml")
    elif ext == ".xlsx":
        if not entete.startswith(b"PK\x03\x04"):
            raise FichierRefuse("Ce fichier n'est pas un vrai classeur Excel (.xlsx).")
        _verifier_zip(chemin, "xl/workbook.xml")
    elif ext in {".txt", ".csv"}:
        with open(chemin, "rb") as fh:
            echantillon = fh.read(65536)
        if b"\x00" in echantillon:
            raise FichierRefuse("Fichier texte invalide (contenu binaire).")
    elif ext == ".png":
        if not entete.startswith(b"\x89PNG\r\n\x1a\n"):
            raise FichierRefuse("Ce fichier n'est pas une vraie image PNG.")
    elif ext in {".jpg", ".jpeg"}:
        if not entete.startswith(b"\xff\xd8\xff"):
            raise FichierRefuse("Ce fichier n'est pas une vraie image JPEG.")
    return ext


# --------------------------------------------------------------------------
# Excel : neutralisation des formules et caractères interdits
# --------------------------------------------------------------------------
_CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
DEBUTS_FORMULE = ("=", "+", "-", "@", "\t", "\r")


def texte_cellule(valeur):
    """Nettoie une valeur avant écriture dans Excel.

    * supprime les caractères de contrôle (sinon fichier corrompu) ;
    * une chaîne qui commence par « = » ne doit JAMAIS devenir une formule :
      l'appelant force le type texte via `ecrire_cellule`.
    """
    if isinstance(valeur, str):
        return _CTRL.sub("", valeur)
    return valeur


def ecrire_cellule(cellule, valeur) -> None:
    """Écrit une valeur dans une cellule openpyxl sans risque de formule."""
    valeur = texte_cellule(valeur)
    cellule.value = valeur
    if isinstance(valeur, str) and valeur.startswith(DEBUTS_FORMULE):
        cellule.data_type = "s"  # force le texte : pas d'exécution de formule


def texte_csv(valeur) -> str:
    """Neutralise l'injection de formule pour un export CSV."""
    v = "" if valeur is None else str(texte_cellule(valeur))
    if v.startswith(DEBUTS_FORMULE):
        v = "'" + v
    return v


# --------------------------------------------------------------------------
# Mot de passe local (logiciel mono-utilisateur)
# --------------------------------------------------------------------------
ITERATIONS = 600_000
LONGUEUR_MIN_MDP = 12
ECHECS_AVANT_BLOCAGE = 5


def _hacher(mdp: str, sel: bytes, iterations: Optional[int] = None) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", mdp.encode("utf-8"), sel, iterations or ITERATIONS)


class CoffreAcces:
    """Gère le mot de passe d'accès au logiciel (fichier acces.json local)."""

    def __init__(self, dossier: Path) -> None:
        self.fichier = dossier / "acces.json"

    def existe(self) -> bool:
        return self.fichier.exists()

    def _lire(self) -> dict:
        return json.loads(self.fichier.read_text(encoding="utf-8"))

    def _ecrire(self, donnees: dict) -> None:
        tmp = self.fichier.with_suffix(".tmp")
        tmp.write_text(json.dumps(donnees), encoding="utf-8")
        os.replace(tmp, self.fichier)
        restreindre_droits(self.fichier)

    @staticmethod
    def valider_robustesse(mdp: str) -> Optional[str]:
        """Retourne un message d'erreur si le mot de passe est trop faible."""
        if len(mdp) < LONGUEUR_MIN_MDP:
            return f"Au moins {LONGUEUR_MIN_MDP} caractères."
        familles = sum(bool(re.search(p, mdp)) for p in (r"[a-z]", r"[A-Z]", r"\d", r"[^A-Za-z0-9]"))
        if familles < 3:
            return "Mélangez au moins 3 familles : minuscules, majuscules, chiffres, symboles."
        return None

    def definir(self, mdp: str) -> None:
        erreur = self.valider_robustesse(mdp)
        if erreur:
            raise ValueError(erreur)
        sel = secrets.token_bytes(16)
        self._ecrire({
            "algo": "pbkdf2_sha256",
            "iterations": ITERATIONS,  # mémorisé : permet d'augmenter plus tard sans casser l'accès
            "sel": sel.hex(),
            "empreinte": _hacher(mdp, sel).hex(),
            "echecs": 0,
            "bloque_jusqua": 0,
        })

    def attente_restante(self) -> int:
        """Secondes à attendre avant un nouvel essai (0 si aucune)."""
        if not self.existe():
            return 0
        return max(0, int(self._lire().get("bloque_jusqua", 0) - time.time()))

    def verifier(self, mdp: str) -> bool:
        if not self.existe():
            return False
        d = self._lire()
        if time.time() < d.get("bloque_jusqua", 0):
            return False
        calcule = _hacher(mdp, bytes.fromhex(d["sel"]), int(d.get("iterations", ITERATIONS)))
        ok = hmac.compare_digest(calcule, bytes.fromhex(d["empreinte"]))
        if ok:
            d["echecs"] = 0
            d["bloque_jusqua"] = 0
        else:
            d["echecs"] = int(d.get("echecs", 0)) + 1
            if d["echecs"] >= ECHECS_AVANT_BLOCAGE:
                # Blocage exponentiel : 30 s, 60 s, 120 s… plafonné à 1 h.
                palier = d["echecs"] - ECHECS_AVANT_BLOCAGE
                d["bloque_jusqua"] = time.time() + min(30 * (2 ** palier), 3600)
        self._ecrire(d)
        return ok


# --------------------------------------------------------------------------
# Droits sur les fichiers (dossier de données lisible par vous seul)
# --------------------------------------------------------------------------
def restreindre_droits(chemin: Path) -> None:
    """Rend un fichier/dossier accessible au seul utilisateur courant.

    Sous Windows, chmod a un effet limité : le dossier hérite des droits du
    profil utilisateur, ce qui est acceptable ; on recommande BitLocker.
    """
    try:
        if chemin.is_dir():
            os.chmod(chemin, stat.S_IRWXU)
        else:
            os.chmod(chemin, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass


def jeton_aleatoire(n: int = 32) -> str:
    return secrets.token_urlsafe(n)
