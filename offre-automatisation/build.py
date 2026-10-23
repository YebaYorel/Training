"""Assemble les documents autonomes : chaque image de src/ est intégrée en data URI.

Usage : python offre-automatisation/build.py
Résultat : offre-automatisation/catalogue-2026.html et offre-automatisation.html,
envoyables tels quels (un seul fichier, aucune ressource externe).
"""
import base64
import mimetypes
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
ASSETS = ROOT / "assets"


def data_uri(name: str) -> str:
    path = ASSETS / name
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def build(page: Path) -> Path:
    html = page.read_text(encoding="utf-8")
    html = re.sub(r"assets/([\w.-]+\.(?:png|jpe?g|webp))", lambda m: data_uri(m.group(1)), html)
    out = ROOT / page.name
    out.write_text(html, encoding="utf-8")
    return out


if __name__ == "__main__":
    for page in sorted(SRC.glob("*.html")):
        out = build(page)
        print(f"{out.relative_to(ROOT.parent)}  {out.stat().st_size / 1024:.0f} Ko")
