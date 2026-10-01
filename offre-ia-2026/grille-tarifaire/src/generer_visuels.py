"""Visuels de la grille tarifaire (bandeau « circuit » + QR) pour les 3 versions de charte.

Réutilise les couleurs, le logo sans l'œil et le motif circuit des cartes de visite.
Sortie : visuels/bandeau_V1.png … et visuels/qr_V1.png …
"""
import pathlib
import subprocess
import sys

ICI = pathlib.Path(__file__).resolve().parent
CARTES = ICI.parent.parent / "cartes-de-visite" / "src"
sys.path.insert(0, str(CARTES))
import generer_cartes as gc  # noqa: E402

VISUELS = ICI / "visuels"
VISUELS.mkdir(exist_ok=True)


def circuit_large() -> str:
    """Chevrons en pistes de circuit, à gauche et à droite du bandeau (zone centrale libre pour le texte)."""
    traits, noeuds = [], []
    for k in range(9):
        d = 40 + k * 46
        a = 330 - k * 34
        traits.append(f"M-40,{280-d} L{a},280 L-40,{280+d}")
        traits.append(f"M2520,{280-d} L{2480-a},280 L2520,{280+d}")
        noeuds += [(a, 280), (2480 - a, 280)]
    chemins = "".join(f'<path d="{t}"/>' for t in traits)
    points = "".join(f'<circle cx="{x}" cy="{y}" r="9"/>' for x, y in noeuds)
    return (f'<svg style="position:absolute;inset:0" viewBox="0 0 2480 560"><defs><linearGradient id="gr" x1="0" x2="1">'
            f'<stop offset="0" stop-color="var(--or)"/><stop offset=".5" stop-color="var(--or2)" stop-opacity=".3"/>'
            f'<stop offset="1" stop-color="var(--or)"/></linearGradient></defs>'
            f'<g fill="none" stroke="url(#gr)" stroke-width="3.2" stroke-linejoin="round">{chemins}</g>'
            f'<g fill="var(--or2)">{points}</g></svg>')


def bandeau(v: dict) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{CARTES}/fonts-local.css">
<style>
@font-face{{font-family:'Playfair Display';font-weight:900;src:url({CARTES}/fonts/playfair-display-latin-900-normal.woff2)}}
@font-face{{font-family:'JetBrains Mono';font-weight:400;src:url({CARTES}/fonts/jetbrains-mono-latin-400-normal.woff2)}}
:root{{--or:{v['or']};--or2:{v['or2']}}}
*{{margin:0;padding:0}} body{{width:2480px;height:560px;overflow:hidden}}
.b{{position:relative;width:2480px;height:560px;background:radial-gradient(70% 140% at 50% 50%,{v['sombre1']} 0%,{v['sombre2']} 100%)}}
.c{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.or-feuille{{background:linear-gradient(115deg,#8A6A2A 0%,{v['or2']} 28%,{v['or']} 45%,#F6E4AE 58%,#A7832F 78%,{v['or2']} 100%);-webkit-background-clip:text;background-clip:text;color:transparent}}
.sym{{width:240px;margin-bottom:14px}}
.y{{font:{v['poids_marque']} 170px/0.95 '{v['police_marque']}';letter-spacing:10px}}
.f{{font:600 46px Inter;color:{v['or']};letter-spacing:.55em;margin:14px 0 0 .55em}}
.p{{font:400 30px 'JetBrains Mono';color:{v['doux']};margin-top:18px;letter-spacing:2px}}
.p b{{color:{v['or']};font-weight:400}}
</style></head><body><div class="b">{circuit_large()}
<div class="c"><img class="sym" src="{CARTES}/sym_{v['code']}_sombre.svg"><div class="y or-feuille">YEBA</div><div class="f">FORMATIONS</div>
<div class="p"><b>&gt;</b> grille_tarifaire --annee 2026 --ia</div></div></div></body></html>"""


def main() -> None:
    for v in gc.VERSIONS:
        gc.preparer_fichiers(v)
        html = VISUELS / f"bandeau_{v['code']}.html"
        html.write_text(bandeau(v))
        subprocess.run(["node", str(ICI / "capture.js"), str(html), str(VISUELS / f"bandeau_{v['code']}.png"), "2480", "560"], check=True)
        html.unlink()
        # QR : couleur « encre » sur fond clair, marge de silence intégrée (4 modules)
        import qrcode
        q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q, box_size=24, border=4)
        q.add_data(gc.URL_QR)
        q.make(fit=True)
        q.make_image(fill_color=v["encre"], back_color="white").save(VISUELS / f"qr_{v['code']}.png")
        print("visuels", v["code"], "ok")


if __name__ == "__main__":
    main()
