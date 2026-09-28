"""Génère les illustrations vectorielles « maison » de la soirée (aucune photo tierce).

Sorties (PNG transparents, aux couleurs YEBA) :
  - illustrations/baobab-or.png   : silhouette de baobab stylisée
  - illustrations/jauge-or.png    : compte-tours (métaphore « moteur » des formations)
  - illustrations/etoiles-ue.png  : cercle de 12 points (souveraineté européenne)

Usage : python assets/generer_illustrations.py
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

OR = (201, 168, 76, 255)
OR_DOUX = (201, 168, 76, 90)
BLANC = (255, 255, 255, 255)
SS = 4  # suréchantillonnage pour l'anticrénelage

SORTIE = Path(__file__).parent / "illustrations"


def _fin(img, taille):
    return img.resize(taille, Image.LANCZOS)


def baobab():
    w, h = 1200 * SS, 1300 * SS
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, sol = w // 2, int(h * 0.93)

    # Tronc en forme de bouteille, caractéristique du baobab
    pts = []
    for i in range(0, 101):
        t = i / 100
        y = sol - t * h * 0.46
        largeur = (0.30 - 0.10 * t + 0.05 * math.sin(t * math.pi)) * w
        pts.append((cx - largeur / 2, y))
    droite = [(2 * cx - x, y) for x, y in reversed(pts)]
    d.polygon(pts + droite, fill=OR)
    # Racines
    for dx in (-0.16, -0.09, 0.09, 0.16):
        d.polygon([(cx + dx * w * 0.6, sol - 30 * SS), (cx + dx * w * 1.25, sol + 10 * SS),
                   (cx + dx * w * 0.8, sol + 10 * SS)], fill=OR)
    d.rectangle([cx - 0.36 * w, sol, cx + 0.36 * w, sol + 14 * SS], fill=OR)

    # Branches : courtes, épaisses, étalées (silhouette « arbre à l'envers »)
    haut = sol - h * 0.46
    branches = [(-0.40, -0.10), (-0.28, -0.26), (-0.12, -0.34), (0.02, -0.38),
                (0.15, -0.33), (0.29, -0.25), (0.41, -0.09)]
    for bx, by in branches:
        x2, y2 = cx + bx * w, haut + by * h * 0.9
        x1 = cx + bx * w * 0.25
        ep = 55 * SS
        d.polygon([(x1 - ep, haut + 20 * SS), (x1 + ep, haut + 20 * SS), (x2 + ep / 2.2, y2), (x2 - ep / 2.2, y2)], fill=OR)
        # Rameaux + feuillage clairsemé
        for k in (-1, 0, 1):
            x3, y3 = x2 + k * 55 * SS, y2 - 70 * SS + abs(k) * 25 * SS
            d.line([(x2, y2), (x3, y3)], fill=OR, width=12 * SS)
            r = 52 * SS
            d.ellipse([x3 - r, y3 - r * 0.7, x3 + r, y3 + r * 0.7], fill=OR)
    img = img.filter(ImageFilter.GaussianBlur(SS / 2))
    _fin(img, (1200, 1300)).save(SORTIE / "baobab-or.png")


def jauge():
    t = 1000 * SS
    img = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c, r = t / 2, t * 0.44
    d.arc([c - r, c - r, c + r, c + r], start=135, end=405, fill=OR_DOUX, width=26 * SS)
    d.arc([c - r, c - r, c + r, c + r], start=135, end=330, fill=OR, width=26 * SS)
    for i in range(0, 11):
        a = math.radians(135 + i * 27)
        r1, r2 = r * 0.80, r * (0.92 if i % 2 == 0 else 0.87)
        d.line([(c + r1 * math.cos(a), c + r1 * math.sin(a)), (c + r2 * math.cos(a), c + r2 * math.sin(a))],
               fill=OR, width=10 * SS)
    a = math.radians(300)
    d.line([(c, c), (c + r * 0.72 * math.cos(a), c + r * 0.72 * math.sin(a))], fill=BLANC, width=16 * SS)
    d.ellipse([c - 30 * SS, c - 30 * SS, c + 30 * SS, c + 30 * SS], fill=OR)
    _fin(img, (1000, 1000)).save(SORTIE / "jauge-or.png")


def etoiles_ue():
    t = 600 * SS
    img = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c, r, p = t / 2, t * 0.38, t * 0.05
    for i in range(12):
        a = math.radians(i * 30 - 90)
        x, y = c + r * math.cos(a), c + r * math.sin(a)
        d.ellipse([x - p, y - p, x + p, y + p], fill=OR)
    _fin(img, (600, 600)).save(SORTIE / "etoiles-ue.png")


if __name__ == "__main__":
    SORTIE.mkdir(exist_ok=True)
    baobab()
    jauge()
    etoiles_ue()
    print("Illustrations générées dans", SORTIE)
