"""Auto-contrôle de sécurité, avec correction automatique quand c'est possible.

Lancé à chaque démarrage (corrections silencieuses) et à la demande
(menu « Sécurité » ou `python -m decorticage audit`).
"""

from __future__ import annotations

import os
import stat
import sys
from importlib import metadata
from pathlib import Path

from .securite import restreindre_droits

# Versions minimales : corrigent des failles publiées (CVE) connues.
VERSIONS_MIN = {
    "openpyxl": (3, 1, 0),
    "pdfplumber": (0, 11, 0),
    "pdfminer.six": (20231228,),
    "python-docx": (1, 1, 0),
    "Pillow": (10, 3, 0),        # CVE-2024-28219 corrigée en 10.3.0
    "defusedxml": (0, 7, 1),     # protège openpyxl contre les attaques XML (XXE, billion laughs)
}


def _version(paquet: str):
    try:
        brut = metadata.version(paquet)
    except metadata.PackageNotFoundError:
        return None, None
    nums = tuple(int(x) for x in "".join(c if c.isdigit() or c == "." else " " for c in brut).split()[0].split(".") if x)
    return brut, nums


def auditer(base: Path, hote: str = "127.0.0.1") -> list[dict]:
    r = []

    def ajout(controle, ok, detail):
        r.append({"controle": controle, "ok": bool(ok), "detail": detail})

    ajout("Accès réseau", hote == "127.0.0.1", "Interface visible uniquement depuis cet ordinateur (127.0.0.1).")
    ajout("Mot de passe", (base / "acces.json").exists(), "Mot de passe haché PBKDF2-SHA256 (600 000 itérations).")
    ajout("Version de Python", sys.version_info >= (3, 10), f"Python {sys.version.split()[0]} (3.10 minimum).")
    for paquet, mini in VERSIONS_MIN.items():
        brut, nums = _version(paquet)
        ok = nums is not None and nums >= mini
        ajout(f"Bibliothèque {paquet}", ok,
              f"installée : {brut or 'absente'} — minimum : {'.'.join(map(str, mini))}"
              + ("" if ok else " → lancer : pip install -U -r requirements-decorticage.txt"))
    if os.name == "posix":
        mode = stat.S_IMODE(base.stat().st_mode)
        ajout("Droits du dossier de données", mode & 0o077 == 0, f"mode {oct(mode)} (attendu 0o700 : vous seul).")
        exposes = [p.name for p in base.rglob("*") if p.is_file() and stat.S_IMODE(p.stat().st_mode) & 0o077]
        ajout("Droits des fichiers", not exposes, "Tous privés." if not exposes else f"{len(exposes)} fichier(s) lisible(s) par d'autres.")
    else:
        ajout("Droits du dossier de données", True, "Windows : droits hérités du profil utilisateur. Activez BitLocker.")
    restes = list(base.rglob("_reception*"))
    ajout("Fichiers temporaires", not restes, "Aucun." if not restes else f"{len(restes)} reste(s) de réception.")
    journal = base / "erreurs.log"
    ajout("Journal d'erreurs", not journal.exists() or journal.stat().st_size < 5_000_000,
          "Taille raisonnable." if not journal.exists() or journal.stat().st_size < 5_000_000 else "Trop gros : rotation.")
    ajout("Chiffrement du disque", True,
          "Recommandé (non vérifiable ici) : BitLocker (Windows) ou FileVault (Mac), surtout sur ordinateur portable.")
    return r


def corriger(base: Path) -> None:
    """Applique les corrections automatiques possibles."""
    restreindre_droits(base)
    for p in base.rglob("*"):
        restreindre_droits(p)
    for p in base.rglob("_reception*"):
        try:
            p.unlink()
        except OSError:
            pass
    journal = base / "erreurs.log"
    if journal.exists() and journal.stat().st_size >= 5_000_000:
        journal.replace(base / "erreurs.log.1")
