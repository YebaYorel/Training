"""Construit le prototype « Accueil Saison 1 » : accueil/index.html → dist/accueil/
  - polices Montserrat (licence OFL, sans nom réservé) réduites au latin et embarquées en woff2 :
    la page n'appelle ni Google Fonts ni aucun autre service tiers ;
  - logo et emblème convertis en WebP légers ;
  - espaces insécables à la française dans le texte (hors CSS et JavaScript).
Publication : page privée (Artifact) avec dist/accueil/index.html + logo.webp + embleme.webp.
"""
import base64
import io
import re
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from PIL import Image

RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "accueil" / "index.html"
SORTIE = RACINE / "dist" / "accueil"
POLICES = {400: "Montserrat-400.ttf", 700: "Montserrat-700.ttf", 900: "Montserrat-900.ttf"}
LATIN = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,"
         "U+2000-206F,U+2074,U+20AC,U+2122,U+2190-2193,U+2212,U+2215")
IMAGES = {  # source (fond sombre), largeur en pixels (2× la taille affichée)
    "logo.webp": ("assets/logo-yeba-fond-sombre.png", 380),
    "embleme.webp": ("assets/embleme-fond-sombre.png", 184),
}


def police_woff2(fichier):
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.hinting = False
    opts.layout_features = ["kern", "liga", "calt", "ccmp", "locl", "mark", "mkmk", "tnum", "lnum", "case"]
    opts.name_IDs = [0, 1, 2, 3, 4, 5, 6, 13, 14]  # copyright et licence OFL conservés dans la police
    police = TTFont(RACINE / "assets" / "fonts" / fichier)
    sous = subset.Subsetter(opts)
    sous.populate(unicodes=subset.parse_unicodes(LATIN))
    sous.subset(police)
    police.flavor = "woff2"
    tampon = io.BytesIO()
    police.save(tampon)
    return tampon.getvalue()


def typo_francaise(html):
    """Espaces insécables avant : ; ! ? et dans les guillemets, uniquement dans le texte HTML."""
    morceaux = re.split(r"(<script\b.*?</script>|<style\b.*?</style>)", html, flags=re.S)
    for i in range(0, len(morceaux), 2):
        t = morceaux[i].replace(" :", " :")
        t = re.sub(r" ([;!?])", " \\1", t)
        morceaux[i] = t.replace("« ", "« ").replace(" »", " »")
    return "".join(morceaux)


def main():
    SORTIE.mkdir(parents=True, exist_ok=True)
    faces, poids_polices = [], 0
    for poids, fichier in POLICES.items():
        donnees = police_woff2(fichier)
        poids_polices += len(donnees)
        b64 = base64.b64encode(donnees).decode("ascii")
        faces.append(f'@font-face{{font-family:"Montserrat";font-style:normal;font-weight:{poids};'
                     f'font-display:swap;src:url(data:font/woff2;base64,{b64}) format("woff2")}}')
    html = SOURCE.read_text(encoding="utf-8")
    assert "/*@POLICES@*/" in html, "repère /*@POLICES@*/ absent de accueil/index.html"
    html = typo_francaise(html.replace("/*@POLICES@*/", "\n".join(faces)))
    (SORTIE / "index.html").write_text(html, encoding="utf-8")
    poids_images = 0
    for nom, (source, largeur) in IMAGES.items():
        im = Image.open(RACINE / source).convert("RGBA")
        im = im.resize((largeur, round(im.height * largeur / im.width)), Image.LANCZOS)
        im.save(SORTIE / nom, "WEBP", quality=88, method=6)
        poids_images += (SORTIE / nom).stat().st_size
    page = (SORTIE / "index.html").stat().st_size
    print(f"OK : dist/accueil/index.html ({page / 1024:.0f} Ko dont polices {poids_polices / 1024:.0f} Ko) "
          f"+ images WebP ({poids_images / 1024:.0f} Ko)")


if __name__ == "__main__":
    main()
