"""Calques graphiques du PowerPoint (PNG transparents, aux couleurs YEBA) — aucun trait ne traverse un texte.

  calques/etoiles.png      : champ d'étoiles dorées (parallaxe par Morphose), points uniquement
  calques/halo-*.png       : halos de lumière doux (or, bleu, terre) que la Morphose fait glisser
  calques/vignette.png     : assombrissement des bords (lisibilité, effet cinéma)
  pictos/*.png             : pictogrammes au trait or (avantages)

Usage : python3 assets/generer_calques.py
"""
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ICI = Path(__file__).resolve().parent
CALQUES = ICI / "calques"
PICTOS = ICI / "pictos"
OR = (201, 168, 76)
OR_CLAIR = (233, 215, 160)
SS = 4


def etoiles():
    w, h = 2400, 1350  # affiché à 16,67 × 9,375 pouces (plus grand que la slide : marge de dérive)
    rng = np.random.default_rng(974)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for _ in range(170):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        r = rng.choice([1.2, 1.6, 2.2, 3.0, 4.2], p=[0.35, 0.3, 0.2, 0.1, 0.05])
        a = int(rng.uniform(40, 150))
        coul = OR_CLAIR if rng.random() < 0.3 else OR
        d.ellipse([x - r, y - r, x + r, y + r], fill=coul + (a,))
    lueur = img.filter(ImageFilter.GaussianBlur(4))
    lueur = Image.eval(lueur, lambda v: v)  # halo doux autour des étoiles
    base = Image.alpha_composite(lueur, img)
    base.save(CALQUES / "etoiles.png", optimize=True)


def halo(nom, couleur, force=0.30):
    t = 900
    y, x = np.mgrid[0:t, 0:t]
    r = np.hypot(x - t / 2, y - t / 2) / (t / 2)
    alpha = np.clip(1 - r, 0, 1) ** 2.2 * 255 * force
    rgba = np.zeros((t, t, 4), dtype=np.uint8)
    rgba[..., 0], rgba[..., 1], rgba[..., 2] = couleur
    rgba[..., 3] = alpha.astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(CALQUES / f"halo-{nom}.png", optimize=True)


def vignette():
    w, h = 1920, 1080
    y, x = np.mgrid[0:h, 0:w]
    r = np.hypot((x - w / 2) / (w * 0.62), (y - h / 2) / (h * 0.66))
    alpha = np.clip((r - 0.55) / 0.5, 0, 1) ** 1.6 * 255 * 0.62
    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    rgba[..., 3] = alpha.astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(CALQUES / "vignette.png", optimize=True)


# ───────────────────────────── pictogrammes au trait ─────────────────────────────

def _picto(nom, dessin):
    t = 256 * SS
    img = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    e = 9 * SS
    dessin(d, lambda v: v * SS, e)
    img = img.resize((256, 256), Image.LANCZOS)
    img.save(PICTOS / f"{nom}.png", optimize=True)


def _rect(d, k, e, x0, y0, x1, y1, r=14):
    d.rounded_rectangle([k(x0), k(y0), k(x1), k(y1)], radius=k(r), outline=OR, width=e)


def dossier(d, k, e):
    d.line([k(30), k(70), k(100), k(70), k(118), k(52), k(226), k(52), k(226), k(206), k(30), k(206), k(30), k(70)], fill=OR, width=e, joint="curve")
    d.line([k(84), k(132), k(116), k(164), k(176), k(104)], fill=OR_CLAIR, width=e, joint="curve")


def devis(d, k, e):
    _rect(d, k, e, 50, 26, 180, 226)
    for y in (76, 112, 148):
        d.line([k(78), k(y), k(152), k(y)], fill=OR, width=e - SS * 2)
    d.ellipse([k(150), k(150), k(226), k(226)], fill=(0, 0, 0, 0), outline=OR_CLAIR, width=e)
    d.line([k(188), k(166), k(188), k(190), k(204), k(200)], fill=OR_CLAIR, width=e - SS * 2, joint="curve")


def paiement(d, k, e):
    _rect(d, k, e, 26, 66, 230, 196, 18)
    d.line([k(26), k(104), k(230), k(104)], fill=OR, width=e)
    d.line([k(58), k(156), k(118), k(156)], fill=OR_CLAIR, width=e)
    d.line([k(150), k(156), k(198), k(156), k(182), k(140)], fill=OR_CLAIR, width=e - SS * 2, joint="curve")
    d.line([k(198), k(156), k(182), k(172)], fill=OR_CLAIR, width=e - SS * 2)


def groupe(d, k, e):
    for cx, cy, r in ((128, 82, 30), (60, 104, 22), (196, 104, 22)):
        d.ellipse([k(cx - r), k(cy - r), k(cx + r), k(cy + r)], outline=OR if cx == 128 else OR_CLAIR, width=e)
    d.arc([k(70), k(122), k(186), k(238)], 200, 340, fill=OR, width=e)
    d.arc([k(18), k(132), k(102), k(216)], 205, 335, fill=OR_CLAIR, width=e - SS * 2)
    d.arc([k(154), k(132), k(238), k(216)], 205, 335, fill=OR_CLAIR, width=e - SS * 2)


def attestation(d, k, e):
    _rect(d, k, e, 40, 22, 176, 210)
    for y in (64, 96):
        d.line([k(66), k(y), k(150), k(y)], fill=OR, width=e - SS * 2)
    d.ellipse([k(150), k(130), k(222), k(202)], outline=OR_CLAIR, width=e)
    d.line([k(166), k(196), k(158), k(240), k(186), k(226), k(214), k(240), k(206), k(196)], fill=OR_CLAIR, width=e - SS * 2, joint="curve")


def accessibilite(d, k, e):
    d.ellipse([k(24), k(24), k(232), k(232)], outline=OR, width=e)
    d.ellipse([k(114), k(52), k(142), k(80)], fill=OR_CLAIR)
    d.line([k(70), k(104), k(128), k(114), k(186), k(104)], fill=OR_CLAIR, width=e, joint="curve")
    d.line([k(128), k(114), k(128), k(152)], fill=OR_CLAIR, width=e)
    d.line([k(98), k(204), k(128), k(152), k(158), k(204)], fill=OR_CLAIR, width=e, joint="curve")


if __name__ == "__main__":
    CALQUES.mkdir(exist_ok=True)
    PICTOS.mkdir(exist_ok=True)
    etoiles()
    halo("or", OR, 0.32)
    halo("bleu", (110, 150, 220), 0.30)
    halo("terre", (205, 118, 58), 0.34)
    vignette()
    for nom, f in (("dossier", dossier), ("devis", devis), ("paiement", paiement), ("groupe", groupe), ("attestation", attestation), ("accessibilite", accessibilite)):
        _picto(nom, f)
    print("Calques :", sorted(p.name for p in CALQUES.iterdir()), "| Pictos :", sorted(p.name for p in PICTOS.iterdir()))
