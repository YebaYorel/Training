"""Assemble le Pilotage YEBA FORMATIONS en un seul fichier HTML.

    python web/pilotage/construire.py

Produit dans web/pilotage/dist/ :
* pilotage_artifact.html : version publiée sur claude.ai (squelette ajouté à la publication)
* Pilotage.html          : version autonome à ouvrir dans n'importe quel navigateur
Le moteur de décorticage (web/src) est réutilisé tel quel ; seules les bibliothèques
(versions figées) viennent de cdn.jsdelivr.net.
"""
import re
from pathlib import Path

ICI = Path(__file__).resolve().parent
SRC = ICI / "src"
MOTEUR = ICI.parent / "src"
LIBS = [
    "https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.min.js",
    "https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js",
    "https://cdn.jsdelivr.net/npm/exceljs@4.4.0/dist/exceljs.min.js",
    "https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js",
    "https://cdn.jsdelivr.net/npm/docx@8.5.0/build/index.umd.js",
    "https://cdn.jsdelivr.net/npm/pptxgenjs@3.12.0/dist/pptxgen.bundle.js",
]
MODULES_MOTEUR = ["referentiels", "extraction", "pedagogie", "planification", "programme", "exports", "moteur"]
MODULES = ["coffre", "donnees", "suivi", "generateur", "documents", "finances", "ui"]


def inline(js: str) -> str:
    return re.sub(r"</(script)", r"<\\/\1", js, flags=re.IGNORECASE)


def construire() -> tuple[Path, Path]:
    page = (SRC / "page.html").read_text(encoding="utf-8")
    scripts = [f'<script src="{u}"></script>' for u in LIBS]
    code = [inline((MOTEUR / f"{m}.js").read_text(encoding="utf-8")) for m in MODULES_MOTEUR]
    code += [inline((SRC / f"{m}.js").read_text(encoding="utf-8")) for m in MODULES]
    scripts.append("<script>\n" + "\n".join(code) + "\n</script>")
    contenu = page.replace("{{SCRIPTS}}", "\n".join(scripts))
    dist = ICI / "dist"
    dist.mkdir(exist_ok=True)
    artefact = dist / "pilotage_artifact.html"
    artefact.write_text(contenu, encoding="utf-8")
    autonome = dist / "Pilotage.html"
    autonome.write_text('<!doctype html>\n<html lang="fr"><head><meta charset="utf-8">'
                        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
                        "</head><body>\n" + contenu + "\n</body></html>\n", encoding="utf-8")
    return artefact, autonome


if __name__ == "__main__":
    for p in construire():
        print(f"{p.stat().st_size / 1e3:8.0f} Ko  {p}")
