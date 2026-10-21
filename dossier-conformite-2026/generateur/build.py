"""Génère tout le dossier (DOCX + XLSX) puis exporte chaque DOCX en PDF.

Usage : python3 build.py   (LibreOffice requis pour l'export PDF)
"""
import shutil
import subprocess

import gen_deets
import gen_note
import gen_pilotage
import gen_rgpd
import gen_stagiaires
import gen_titres
from lib import SORTIE

if __name__ == "__main__":
    if SORTIE.exists():
        shutil.rmtree(SORTIE)
    fichiers = [gen_note.note()]
    for module in (gen_deets, gen_titres, gen_stagiaires, gen_rgpd, gen_pilotage):
        fichiers += module.tout()
    for f in fichiers:
        if f.suffix == ".docx":
            subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(f.parent), str(f)],
                           check=True, capture_output=True)
    print(f"{len(fichiers)} documents générés dans {SORTIE}")
