"""Assemble l'Atelier de décorticage en un seul fichier HTML.

    python web/construire.py

Produit dans web/dist/ :
* atelier_decorticage_artifact.html : version publiée sur claude.ai (sans squelette, ajouté à la publication)
* Atelier_decorticage.html          : version autonome à ouvrir dans n'importe quel navigateur
Les bibliothèques (versions figées) sont chargées depuis cdn.jsdelivr.net ; tout le reste est intégré.
"""
import re
from pathlib import Path

ICI = Path(__file__).resolve().parent
SRC = ICI / "src"
LIBS = [
    "https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.min.js",
    "https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js",
    "https://cdn.jsdelivr.net/npm/exceljs@4.4.0/dist/exceljs.min.js",
    "https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js",
    "https://cdn.jsdelivr.net/npm/docx@8.5.0/build/index.umd.js",
]
MODULES = ["referentiels", "extraction", "pedagogie", "planification", "programme", "exports", "moteur", "app"]


def inline(js: str) -> str:
    # aucun « </script> » ne peut fermer la balise par erreur ; les autres « </ » (regex) restent intacts
    return re.sub(r"</(script)", r"<\\/\1", js, flags=re.IGNORECASE)


def construire() -> tuple[Path, Path]:
    page = (SRC / "page.html").read_text(encoding="utf-8")
    exemple = (SRC / "exemple_mem.json").read_text(encoding="utf-8")
    scripts = [f'<script src="{u}"></script>' for u in LIBS]
    scripts.append(f"<script>window.EXEMPLE_MEM = {inline(exemple)};</script>")
    code = "\n".join(inline((SRC / f"{m}.js").read_text(encoding="utf-8")) for m in MODULES)
    scripts.append(f"<script>\n{code}\n</script>")
    contenu = page.replace("{{SCRIPTS}}", "\n".join(scripts))
    dist = ICI / "dist"
    dist.mkdir(exist_ok=True)
    artefact = dist / "atelier_decorticage_artifact.html"
    artefact.write_text(contenu, encoding="utf-8")
    autonome = dist / "Atelier_decorticage.html"
    autonome.write_text('<!doctype html>\n<html lang="fr"><head><meta charset="utf-8">'
                        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
                        "</head><body>\n" + contenu + "\n</body></html>\n", encoding="utf-8")
    return artefact, autonome


if __name__ == "__main__":
    for p in construire():
        print(f"{p.stat().st_size / 1e3:8.0f} Ko  {p}")
