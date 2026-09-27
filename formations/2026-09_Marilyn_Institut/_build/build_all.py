"""Régénère TOUS les livrables (Word + PDF + diaporama + quiz HTML) puis une archive ZIP.

    python build_all.py

Les données nominatives sont lues dans ../_donnees_personnelles/stagiaires.json (hors Git).
"""
import shutil
import zipfile
from pathlib import Path

import donnees as D
import build_positionnement, build_livret, build_admin, build_pedago, build_ppt, build_qualiopi, quiz_html
from docx_lib import en_pdf


def main():
    if D.SORTIE.exists():
        shutil.rmtree(D.SORTIE)
    fichiers = []
    for mod in (build_positionnement, build_livret, build_admin, build_pedago, build_qualiopi):
        fichiers += mod.construire()
    ppt = build_ppt.construire()
    quiz_html.construire()
    en_pdf([f for f in fichiers if str(f).endswith(".docx")] + [ppt])
    zip_path = D.SORTIE.parent / "YEBA_Marilyn_Institut_livrables_2026-09.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(D.SORTIE.rglob("*")):
            if f.is_file() and not f.name.startswith("_graphique"):
                z.write(f, Path("livrables") / f.relative_to(D.SORTIE))
    n = sum(1 for f in D.SORTIE.rglob("*") if f.is_file())
    print(f"{n} fichiers générés — archive : {zip_path}")


if __name__ == "__main__":
    main()
