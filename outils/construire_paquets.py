"""Fabrique les paquets à distribuer / transférer (à lancer depuis la racine du dépôt).

    python outils/construire_paquets.py [--sans-hors-ligne]

Produit dans `distribution/` :
* Logiciel_Decorticage_vX.zip                 — léger, installe les bibliothèques par internet
* Logiciel_Decorticage_vX_Windows_hors_ligne.zip — avec les bibliothèques Windows (aucun internet requis)
* Logiciel_Decorticage_vX_Mac_hors_ligne.zip     — avec les bibliothèques Mac (Apple Silicon + Intel)
* SHA256SUMS.txt                               — empreintes pour vérifier l'intégrité après transfert

Les données personnelles (donnees_yeba/, .env, sauvegardes) ne sont JAMAIS incluses.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

VERSION = "1.0"
RACINE = Path(__file__).resolve().parent.parent
SORTIE = RACINE / "distribution"
FICHIERS = [
    "decorticage", "tests", "exemples_sorties", "requirements-decorticage.txt", "DECORTICAGE.md",
    "Lancer_Decorticage_Windows.bat", "Lancer_Decorticage_Mac.command", "Lancer_Decorticage_Linux.sh",
    "Sauvegarder_mes_donnees_Windows.bat", "Restaurer_mes_donnees_Windows.bat",
    "Sauvegarder_mes_donnees_Mac.command", "Restaurer_mes_donnees_Mac.command",
]
INTERDITS = ("donnees_yeba", ".env", "Sauvegarde_decorticage_", "__pycache__", ".pyc", ".venv")
PLATEFORMES = {
    "Windows": [("win_amd64", v) for v in ("3.12", "3.13", "3.14", "3.15")],
    "Mac": [(p, v) for v in ("3.12", "3.13", "3.14") for p in ("macosx_11_0_arm64", "macosx_10_13_x86_64")]
           + [("macosx_11_0_arm64", "3.15")],
}
DOSSIER_ZIP = "Logiciel_Decorticage"
EXECUTABLES = (".command", ".sh")


def _fichiers():
    for nom in FICHIERS:
        p = RACINE / nom
        candidats = [p] if p.is_file() else sorted(x for x in p.rglob("*") if x.is_file())
        for f in candidats:
            rel = f.relative_to(RACINE).as_posix()
            if not any(i in rel for i in INTERDITS):
                yield f, rel


def _ajouter(z: zipfile.ZipFile, f: Path, rel: str):
    info = zipfile.ZipInfo(f"{DOSSIER_ZIP}/{rel}", date_time=(2026, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    # droits Unix conservés : les .command restent exécutables par double-clic sur Mac
    info.external_attr = ((0o755 if rel.endswith(EXECUTABLES) else 0o644) | 0o100000) << 16
    z.writestr(info, f.read_bytes())


def _telecharger(dossier: Path, plateforme: str, version: str):
    subprocess.run([sys.executable, "-m", "pip", "download", "-q", "--only-binary=:all:",
                    "--platform", plateforme, "--python-version", version, "-d", str(dossier),
                    "-r", str(RACINE / "requirements-decorticage.txt")], check=True)


def construire(hors_ligne: bool = True) -> list[Path]:
    SORTIE.mkdir(exist_ok=True)
    paquets = []
    leger = SORTIE / f"Logiciel_Decorticage_v{VERSION}.zip"
    with zipfile.ZipFile(leger, "w") as z:
        for f, rel in _fichiers():
            _ajouter(z, f, rel)
    paquets.append(leger)
    if hors_ligne:
        for os_nom, cibles in PLATEFORMES.items():
            with tempfile.TemporaryDirectory() as tmp:
                for plateforme, version in cibles:
                    _telecharger(Path(tmp), plateforme, version)
                cible = SORTIE / f"Logiciel_Decorticage_v{VERSION}_{os_nom}_hors_ligne.zip"
                with zipfile.ZipFile(cible, "w") as z:
                    for f, rel in _fichiers():
                        _ajouter(z, f, rel)
                    for w in sorted(Path(tmp).glob("*.whl")):
                        _ajouter(z, w, f"paquets/{w.name}")
                paquets.append(cible)
    with open(SORTIE / "SHA256SUMS.txt", "w", encoding="utf-8") as fh:
        for p in paquets:
            fh.write(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n")
    return paquets


if __name__ == "__main__":
    for p in construire(hors_ligne="--sans-hors-ligne" not in sys.argv):
        print(f"{p.stat().st_size / 1e6:7.1f} Mo  {p}")
    print(f"Empreintes : {SORTIE / 'SHA256SUMS.txt'}")
