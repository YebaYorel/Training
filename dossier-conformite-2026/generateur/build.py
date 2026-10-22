"""Génère tout le dossier (DOCX + XLSX), contrôle la mise en page, puis exporte chaque DOCX en PDF.

Usage : python3 build.py   (LibreOffice requis pour l'export PDF)
"""
import shutil
import subprocess
import sys

import gen_deets
import gen_html
import gen_note
import gen_organisme
import gen_pilotage
import gen_rgpd
import gen_stagiaires
import gen_tarifs
import gen_titres
from lib import ERREURS_MISE_EN_PAGE, SORTIE

if __name__ == "__main__":
    if SORTIE.exists():
        shutil.rmtree(SORTIE)
    fichiers = [gen_note.note()]
    for module in (gen_deets, gen_titres, gen_stagiaires, gen_rgpd, gen_pilotage, gen_tarifs, gen_organisme, gen_html):
        fichiers += module.tout()
    if ERREURS_MISE_EN_PAGE:
        print("Mots coupés ou largeurs incorrectes :\n" + "\n".join(ERREURS_MISE_EN_PAGE))
        sys.exit(1)
    for f in fichiers:
        if f.suffix == ".docx":
            subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(f.parent), str(f)],
                           check=True, capture_output=True)
    print(f"{len(fichiers)} documents générés dans {SORTIE} — aucun mot coupé")
