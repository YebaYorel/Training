#!/usr/bin/env python3
"""Nuages de points du générique v3 « La graine » (plan-séquence de particules).

Chaque forme compte exactement N points. Ils sont ordonnés le long d'une courbe de Hilbert : lors d'une
morphose, le coin haut-gauche d'une forme devient le coin haut-gauche de la suivante (mouvement lisible,
sans croisements inutiles). Sortie : src/v3/formes.json (positions, couleurs, groupes, tailles, arêtes).

Données utilisées (aucune n'est inventée) :
- contour réel de La Réunion : donnees/reunion.json (Natural Earth 1:10m, domaine public) ;
- emblème YEBA : assets/embleme-transparent.png (fichier officiel, échantillonné, jamais redessiné) ;
- polices : Montserrat (licence OFL), assets/fonts.

    python3 scripts/formes_v3.py            → src/v3/formes.json
    python3 scripts/formes_v3.py --apercu   → + planche de contrôle (scratch, chemin affiché)
"""
from __future__ import annotations

import json
import math
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
from scipy.spatial import cKDTree

ICI = Path(__file__).resolve().parent
REMOTION = ICI.parent
RACINE = REMOTION.parent
SORTIE = REMOTION / "src" / "v3" / "formes.json"
N = 2000
rng = np.random.default_rng(974)

# Palette (indices stockés par point) — charte : or #C9AB4C, bleu #1B3A6B (éclairci pour rester visible sur fond noir).
PALETTE = ["C9AB4C", "E9D7A0", "FFFFFF", "7FA7E0", "B8BCC6", "4F7FC4", "8E7330", "F6E7B0"]
OR, OR_CLAIR, BLANC, BLEU_CLAIR, GRIS, BLEU, OR_PROFOND, OR_VIF = range(8)
POLICE_NOIRE = RACINE / "assets" / "fonts" / "Montserrat-900.ttf"


# ───────────────────────────── outils ─────────────────────────────

def hilbert(x: int, y: int, n: int = 1024) -> int:
    d, s = 0, n >> 1
    while s > 0:
        rx = 1 if x & s else 0
        ry = 1 if y & s else 0
        d += s * s * ((3 * rx) ^ ry)
        if ry == 0:
            if rx == 1:
                x, y = n - 1 - x, n - 1 - y
            x, y = y, x
        s >>= 1
    return d


def ordre_hilbert(p2: np.ndarray) -> np.ndarray:
    mn, mx = p2.min(0), p2.max(0)
    q = ((p2 - mn) / np.maximum(mx - mn, 1e-9) * 1023).astype(int)
    return np.argsort([hilbert(int(a), int(b)) for a, b in q], kind="stable")


def repartir(longueurs, total):
    """Répartit `total` points proportionnellement aux longueurs (somme exacte)."""
    l = np.asarray(longueurs, float)
    brut = l / l.sum() * total
    n = np.floor(brut).astype(int)
    for i in np.argsort(-(brut - n))[: total - n.sum()]:
        n[i] += 1
    return n


def echantillonner(poly: np.ndarray, n: int, bruit=0.0):
    """n points régulièrement espacés le long d'une polyligne (abscisse curviligne)."""
    if n <= 0:
        return np.zeros((0, 3))
    seg = np.linalg.norm(np.diff(poly, axis=0), axis=1)
    cum = np.concatenate([[0], np.cumsum(seg)])
    s = np.linspace(0, cum[-1], n) if n > 1 else np.array([cum[-1] / 2])
    out = np.stack([np.interp(s, cum, poly[:, k]) for k in range(3)], axis=1)
    if bruit:
        out += rng.normal(0, bruit, out.shape)
    return out


class Forme:
    def __init__(self, nom, pos, col, grp=None, taille=None, aretes=None, plan=(0, 1)):
        self.nom = nom
        self.pos = np.asarray(pos, float)
        assert self.pos.shape == (N, 3), (nom, self.pos.shape)
        self.col = np.asarray(col, int)
        self.grp = np.zeros(N, int) if grp is None else np.asarray(grp, int)
        self.taille = np.ones(N) if taille is None else np.asarray(taille, float)
        self.aretes = np.zeros((0, 2), int) if aretes is None or len(aretes) == 0 else np.asarray(aretes, int)
        self.plan = plan
        self.extra: dict[str, np.ndarray] = {}

    def ordonner(self):
        perm = ordre_hilbert(self.pos[:, list(self.plan)])
        inv = np.empty(N, int)
        inv[perm] = np.arange(N)
        self.pos, self.col, self.grp, self.taille = self.pos[perm], self.col[perm], self.grp[perm], self.taille[perm]
        self.extra = {k: v[perm] for k, v in self.extra.items()}
        if len(self.aretes):
            self.aretes = inv[self.aretes]
        return self

    def json(self):
        return {
            "p": [round(float(v), 3) for v in self.pos.ravel()],
            "c": self.col.tolist(),
            "g": self.grp.tolist(),
            "t": [round(float(v), 2) for v in self.taille],
            "a": self.aretes.ravel().tolist(),
            **{k: [round(float(x), 3) for x in v] for k, v in self.extra.items()},
        }


def polylignes_vers_forme(nom, polys, total, couleur, groupe, taille, bruit=0.0, plan=(0, 1), lien_max=0.4):
    """Échantillonne des polylignes ; relie les points consécutifs d'une même polyligne."""
    longueurs = [max(1e-6, float(np.sum(np.linalg.norm(np.diff(p, axis=0), axis=1)))) for p in polys]
    comptes = repartir(longueurs, total)
    pos, col, grp, tai, aretes = [], [], [], [], []
    for k, (poly, n) in enumerate(zip(polys, comptes)):
        pts = echantillonner(poly, int(n), bruit)
        debut = sum(len(x) for x in pos)
        for i in range(len(pts) - 1):
            if np.linalg.norm(pts[i + 1] - pts[i]) < lien_max:
                aretes.append((debut + i, debut + i + 1))
        pos.append(pts)
        col.append(np.full(len(pts), couleur(k) if callable(couleur) else couleur))
        grp.append(np.full(len(pts), groupe(k) if callable(groupe) else groupe))
        tai.append(np.full(len(pts), taille(k) if callable(taille) else taille))
    return Forme(nom, np.concatenate(pos), np.concatenate(col), np.concatenate(grp), np.concatenate(tai), aretes, plan)


def masque_texte(texte, taille=560, marge=30):
    font = ImageFont.truetype(str(POLICE_NOIRE), taille)
    g, h, d, b = font.getbbox(texte)
    im = Image.new("L", (d - g + 2 * marge, b - h + 2 * marge), 0)
    ImageDraw.Draw(im).text((marge - g, marge - h), texte, font=font, fill=255)
    # abscisses des lettres (pour grouper par lettre)
    bords = [marge + font.getlength(texte[:i]) for i in range(len(texte) + 1)]
    return np.array(im) > 127, bords


def points_dans_masque(m: np.ndarray, n_rempli, n_contour, largeur_monde, bruit_z=0.12):
    contour = m & ~ndimage.binary_erosion(m, iterations=3)
    ys, xs = np.nonzero(m)
    yc, xc = np.nonzero(contour)
    i1 = rng.choice(len(xs), n_rempli, replace=False)
    i2 = rng.choice(len(xc), n_contour, replace=False)
    px = np.concatenate([xs[i1], xc[i2]]).astype(float)
    py = np.concatenate([ys[i1], yc[i2]]).astype(float)
    h, w = m.shape
    k = largeur_monde / w
    x = (px - w / 2) * k
    y = -(py - h / 2) * k
    z = np.concatenate([rng.normal(0, bruit_z, n_rempli), np.zeros(n_contour)])
    est_contour = np.concatenate([np.zeros(n_rempli, bool), np.ones(n_contour, bool)])
    return np.stack([x, y, z], 1), px, est_contour


def aretes_proches(pos, masque_points, k=2, dmax=0.2):
    idx = np.nonzero(masque_points)[0]
    arbre = cKDTree(pos[idx])
    d, j = arbre.query(pos[idx], k=k + 1)
    out = set()
    for a in range(len(idx)):
        for b in range(1, k + 1):
            if d[a, b] < dmax:
                out.add(tuple(sorted((int(idx[a]), int(idx[j[a, b]])))))
    return sorted(out)


def dans_polygone(x, y, poly):
    """Test point-dans-polygone (lancer de rayon), vectorisé."""
    dedans = np.zeros(len(x), bool)
    px, py = poly[:, 0], poly[:, 1]
    j = len(poly) - 1
    for i in range(len(poly)):
        coupe = ((py[i] > y) != (py[j] > y)) & (x < (px[j] - px[i]) * (y - py[i]) / (py[j] - py[i] + 1e-12) + px[i])
        dedans ^= coupe
        j = i
    return dedans


# ───────────────────────────── formes ─────────────────────────────

def f_graine():
    return Forme("graine", rng.normal(0, 0.035, (N, 3)), np.full(N, OR_VIF), taille=np.full(N, 0.9))


def f_reseau():
    """Réseau de racines lumineuses en 3D, issu de la graine (racines + synapses)."""
    polys, niveaux = [], []

    def pousser(o, d, L, niv):
        d = d / np.linalg.norm(d)
        pts, p = [o.copy()], o.copy()
        n = max(6, int(L / 0.1))
        for i in range(n):
            d = d + rng.normal(0, 0.16, 3) * np.array([1, 1, 0.55])
            d /= np.linalg.norm(d)
            p = p + d * (L / n)
            pts.append(p.copy())
            if niv < 3 and i > 5 and rng.random() < 0.055 * (3 - niv):
                pousser(p.copy(), d + rng.normal(0, 0.95, 3), L * rng.uniform(0.32, 0.55), niv + 1)
        polys.append(np.array(pts))
        niveaux.append(niv)

    for k in range(9):
        a = 2 * math.pi * k / 9 + rng.uniform(-0.25, 0.25)
        pousser(np.zeros(3), np.array([math.cos(a), math.sin(a) * 0.8, rng.uniform(-0.4, 0.4)]), rng.uniform(4.2, 6.4), 0)
    couleur = lambda k: [OR, OR_CLAIR, BLEU_CLAIR, BLANC][niveaux[k]]
    taille = lambda k: [1.25, 1.0, 0.8, 0.7][niveaux[k]]
    f = polylignes_vers_forme("reseau", polys, N, couleur, lambda k: niveaux[k], taille, bruit=0.012)
    # synapses : quelques liaisons entre branches voisines
    arbre = cKDTree(f.pos)
    paires = arbre.query_pairs(0.55)
    paires = [p for p in paires if abs(p[0] - p[1]) > 12]
    rng.shuffle(paires)
    f.aretes = np.concatenate([f.aretes, np.array(paires[:140], int)]) if paires else f.aretes
    # nœuds : 6 % des points plus gros
    f.taille[rng.random(N) < 0.06] = 2.2
    return f


def f_yeba():
    m, bords = masque_texte("YEBA")
    pos, px, contour = points_dans_masque(m, 1380, 620, largeur_monde=13.0)
    grp = np.searchsorted(np.array(bords[1:-1]), px)
    col = np.where(contour, OR_VIF, np.where(rng.random(N) < 0.5, OR, OR_CLAIR))
    tai = np.where(contour, 1.15, 0.85)
    aretes = aretes_proches(pos, contour, k=2, dmax=0.16)
    return Forme("yeba", pos, col, grp, tai, aretes)


def f_baobab():
    """Baobab de lumière : tronc en bouteille (lignes d'écorce), couronne en racines, graines aux extrémités."""
    H0, H1 = -4.4, 0.4
    tronc, branches, racines, graines = [], [], [], []

    def rayon(y):
        u = (y - H0) / (H1 - H0)
        return 1.0 + 0.6 * math.sin(math.pi * min(1.0, u * 1.1)) - 0.45 * u

    for k in range(28):
        a = 2 * math.pi * k / 28
        ys = np.linspace(H0, H1, 50)
        tronc.append(np.array([[rayon(y) * math.cos(a + 0.1 * math.sin(1.4 * y + k)), y,
                                rayon(y) * math.sin(a + 0.1 * math.sin(1.4 * y + k))] for y in ys]))

    def branche(p, d, L, niv, cible):
        n = max(5, int(L / 0.08))
        pts, q = [p.copy()], p.copy()
        d = d / np.linalg.norm(d)
        for _ in range(n):
            d = d + rng.normal(0, 0.11, 3)
            d[1] = max(d[1], -0.1)
            d /= np.linalg.norm(d)
            q = q + d * (L / n)
            pts.append(q.copy())
        cible.append(np.array(pts))
        if niv < 2:
            for _ in range(int(rng.integers(2, 4))):
                nd = d + rng.normal(0, 0.55, 3)
                nd[1] = abs(nd[1]) * 0.5 + 0.25
                branche(q, nd, L * rng.uniform(0.42, 0.62), niv + 1, cible)
        else:
            graines.append(q.copy())

    for k in range(9):
        a = 2 * math.pi * k / 9 + rng.uniform(-0.2, 0.2)
        branche(np.array([0.55 * math.cos(a), H1 - 0.15, 0.55 * math.sin(a)]),
                np.array([math.cos(a), rng.uniform(0.55, 1.2), math.sin(a)]), rng.uniform(1.9, 2.7), 0, branches)
    for k in range(8):
        a = 2 * math.pi * k / 8 + rng.uniform(-0.25, 0.25)
        o = np.array([1.05 * math.cos(a), H0 + 0.05, 1.05 * math.sin(a)])
        pts, q, d = [o.copy()], o.copy(), np.array([math.cos(a), -0.12, math.sin(a)])
        for _ in range(24):
            d = d + rng.normal(0, 0.12, 3)
            d[1] = min(d[1], 0.0) * 0.3
            d /= np.linalg.norm(d)
            q = q + d * rng.uniform(0.08, 0.12)
            pts.append(q.copy())
        racines.append(np.array(pts))

    n_graines = 8 * len(graines)
    reste = N - n_graines
    n_tronc, n_branches, n_racines = repartir([0.36, 0.52, 0.12], reste)
    def assembler(listes):
        pos, col, grp, tai, ar = [], [], [], [], []
        for polys, n, c, g, t in listes:
            longueurs = [float(np.sum(np.linalg.norm(np.diff(p, axis=0), axis=1))) for p in polys]
            for poly, m in zip(polys, repartir(longueurs, n)):
                pts = echantillonner(poly, int(m), 0.008)
                d0 = sum(len(x) for x in pos)
                ar += [(d0 + i, d0 + i + 1) for i in range(len(pts) - 1)]
                pos.append(pts)
                col.append(np.full(len(pts), c))
                grp.append(np.full(len(pts), g))
                tai.append(np.full(len(pts), t))
        return pos, col, grp, tai, ar

    pos, col, grp, tai, ar = assembler([(tronc, n_tronc, OR_PROFOND, 0, 0.8), (branches, n_branches, OR, 1, 0.95),
                                        (racines, n_racines, OR_PROFOND, 3, 0.75)])
    for g in graines:   # graines : petites grappes scintillantes
        pts = g + rng.normal(0, 0.05, (8, 3))
        pos.append(pts)
        col.append(np.array([OR_VIF] * 6 + [BLANC] * 2))
        grp.append(np.full(8, 2))
        tai.append(np.array([2.4] + [1.2] * 7))
    f = Forme("baobab", np.concatenate(pos), np.concatenate(col), np.concatenate(grp), np.concatenate(tai), ar)
    f.pos[:, 1] += 0.2
    return f


def f_ile():
    """La Réunion à plat (x est, z sud) : semis de points + littoral ; variante en relief (pitons)."""
    d = json.loads((REMOTION / "donnees" / "reunion.json").read_text(encoding="utf-8"))
    S = 6.6
    poly = np.array(d["contour"]) * S                 # (x, z)
    n_cote = 520
    n_int = N - n_cote
    # semis hexagonal à l'intérieur, pas ajusté pour obtenir ~n_int points
    xmin, zmin = poly.min(0)
    xmax, zmax = poly.max(0)
    pas = 0.30
    for _ in range(30):
        xs, zs = [], []
        for j, z in enumerate(np.arange(zmin, zmax, pas * 0.866)):
            dec = (j % 2) * pas / 2
            for x in np.arange(xmin + dec, xmax, pas):
                xs.append(x)
                zs.append(z)
        xs, zs = np.array(xs), np.array(zs)
        ok = dans_polygone(xs, zs, poly)
        if abs(ok.sum() - n_int) < 25 or ok.sum() < n_int:
            break
        pas *= math.sqrt(ok.sum() / n_int)
    xi, zi = xs[ok], zs[ok]
    if len(xi) > n_int:
        garde = np.sort(rng.choice(len(xi), n_int, replace=False))
        xi, zi = xi[garde], zi[garde]
    elif len(xi) < n_int:
        k = n_int - len(xi)
        j = rng.choice(len(xi), k)
        xi = np.concatenate([xi, xi[j] + rng.normal(0, pas / 3, k)])
        zi = np.concatenate([zi, zi[j] + rng.normal(0, pas / 3, k)])
    xi += rng.normal(0, pas * 0.08, len(xi))
    zi += rng.normal(0, pas * 0.08, len(zi))
    anneau = np.vstack([poly, poly[:1]])
    cote = echantillonner(np.column_stack([anneau[:, 0], np.zeros(len(anneau)), anneau[:, 1]]), n_cote + 1)[:-1]
    pos = np.vstack([np.column_stack([xi, np.zeros(len(xi)), zi]), cote])
    grp = np.concatenate([np.zeros(n_int, int), np.ones(n_cote, int)])
    # arêtes : littoral fermé + réseau clairsemé à l'intérieur
    ar = [(n_int + i, n_int + (i + 1) % n_cote) for i in range(n_cote)]
    arbre = cKDTree(pos[:n_int, [0, 2]])
    dd, jj = arbre.query(pos[:n_int, [0, 2]], k=4)
    for a in range(n_int):
        if rng.random() < 0.42:
            kk = int(rng.integers(1, 4))
            if dd[a, kk] < pas * 1.7:
                ar.append(tuple(sorted((a, int(jj[a, kk])))))
    ar = sorted(set(ar))
    # relief : pitons (altitudes réelles → hauteur exagérée pour la lecture)
    sommets = d["sommets"]
    h = np.zeros(N)
    for nom, s in sommets.items():
        cx, cz = np.array(s["pos"]) * S
        sigma = (0.36 if "Neiges" in nom else 0.30) * S
        h += (s["alt_m"] / 3070) * 2.7 * np.exp(-((pos[:, 0] - cx) ** 2 + (pos[:, 2] - cz) ** 2) / (2 * sigma**2))
    h[grp == 1] = 0.0
    h[grp == 0] += 0.15
    plat = Forme("ile", pos, np.where(grp == 1, OR_VIF, np.where(rng.random(N) < 0.55, OR, OR_CLAIR)), grp,
                 np.where(grp == 1, 1.05, 0.85), ar, plan=(0, 2))
    plat.extra["h"] = h
    return plat


def f_chemin():
    """Chemin lumineux qui s'enfonce dans la profondeur ; 4 jalons (2021, 2025, 2026, ce soir)."""
    def c(s):
        return np.array([3.0 * math.sin(2 * math.pi * 0.7 * s), -0.4 + 1.0 * s + 0.35 * math.sin(4 * math.pi * s), -34.0 * s])

    ss = np.linspace(0, 1, 600)
    axe = np.array([c(s) for s in ss])
    brins = []
    for k in range(5):
        a = 2 * math.pi * k / 5
        dec = np.array([0.16 * math.cos(a), 0.16 * math.sin(a), 0.0])
        brins.append(axe + dec + np.column_stack([np.zeros(len(ss)), 0.05 * np.sin(ss * 40 + k), np.zeros(len(ss))]))
    jalons_s = [0.12, 0.37, 0.62, 0.87]
    n_jalon = 110
    longueurs = [float(np.sum(np.linalg.norm(np.diff(b, axis=0), axis=1))) for b in brins]
    pos, col, grp, tai, ar = [], [], [], [], []
    for b, m in zip(brins, repartir(longueurs, N - 4 * n_jalon)):
        pts = echantillonner(b, int(m), 0.01)
        d0 = sum(len(x) for x in pos)
        ar += [(d0 + i, d0 + i + 1) for i in range(len(pts) - 1)]
        pos.append(pts)
        col.append(np.where(rng.random(len(pts)) < 0.7, OR, OR_CLAIR))
        grp.append(np.zeros(len(pts), int))
        tai.append(np.full(len(pts), 0.85))
    for j, s in enumerate(jalons_s):
        centre = c(s)
        coeur = centre + rng.normal(0, 0.09, (50, 3))
        t = np.linspace(0, 2 * math.pi, 60, endpoint=False)
        anneau = centre + np.column_stack([0.75 * np.cos(t), 0.75 * np.sin(t), np.zeros(60)])
        d0 = sum(len(x) for x in pos) + 50
        ar += [(d0 + i, d0 + (i + 1) % 60) for i in range(60)]
        pos += [coeur, anneau]
        col += [np.full(50, OR_VIF), np.full(60, BLANC)]
        grp += [np.full(50, j + 1), np.full(60, j + 1)]
        tai += [np.full(50, 1.6), np.full(60, 0.8)]
    forme = Forme("chemin", np.concatenate(pos), np.concatenate(col), np.concatenate(grp), np.concatenate(tai), ar, plan=(0, 2))
    forme.jalons = [c(s).round(3).tolist() for s in jalons_s]
    return forme


def f_metiers():
    """Trois pictogrammes en traits de lumière : livre (Former), engrenage (Implémenter), bouclier (Sécuriser)."""
    def arc(cx, cy, r, a0, a1, n=80):
        t = np.linspace(a0, a1, n)
        return np.column_stack([cx + r * np.cos(t), cy + r * np.sin(t), np.zeros(n)])

    def seg(*pts):
        return np.array([[x, y, 0.0] for x, y in pts])

    livre = []
    for sgn in (-1, 1):
        haut = np.array([[sgn * 1.55 * u, 0.95 + 0.22 * math.sin(math.pi * u), 0] for u in np.linspace(0, 1, 40)])
        bas = np.array([[sgn * 1.55 * u, -1.05 + 0.22 * math.sin(math.pi * u), 0] for u in np.linspace(0, 1, 40)])
        livre += [haut, seg((sgn * 1.55, 0.95), (sgn * 1.55, -1.05)), bas]
        for y in (0.5, 0.12, -0.26, -0.64):
            livre.append(seg((sgn * 0.32, y + 0.12 * 0.7), (sgn * 1.25, y + 0.12 * 0.95)))
    livre.append(seg((0, 0.95), (0, -1.05)))

    roue = []
    dents = 10
    contour = []
    for i in range(dents):
        a = 2 * math.pi * i / dents
        da = 2 * math.pi / dents
        for (r, u) in ((1.18, 0.0), (1.18, 0.28), (1.55, 0.36), (1.55, 0.64), (1.18, 0.72), (1.18, 1.0)):
            contour.append((r * math.cos(a + u * da), r * math.sin(a + u * da)))
    contour.append(contour[0])
    roue.append(np.array([[x, y, 0] for x, y in contour]))
    roue.append(arc(0, 0, 0.5, 0, 2 * math.pi, 60))

    bouclier = []
    cote = [(0, 1.45), (1.25, 1.1), (1.25, 0.1)]
    courbe = [(1.25 * math.cos(t) * (1 - 0.0), 0.1 - 1.55 * math.sin(t)) for t in np.linspace(0, math.pi / 2, 30)]
    droite = cote + [(x, y) for x, y in courbe]
    gauche = [(-x, y) for x, y in droite[::-1]]
    bouclier.append(seg(*(gauche + droite[1:])))
    bouclier.append(seg((-0.55, 0.05), (-0.12, -0.42), (0.62, 0.48)))

    groupes = [(livre, -5.4), (roue, 0.0), (bouclier, 5.4)]
    pos, col, grp, tai, ar = [], [], [], [], []
    comptes = repartir([1, 1, 1], N)
    for g, ((polys, dx), n) in enumerate(zip(groupes, comptes)):
        longueurs = [float(np.sum(np.linalg.norm(np.diff(p, axis=0), axis=1))) for p in polys]
        for poly, m in zip(polys, repartir(longueurs, int(n))):
            pts = echantillonner(poly, int(m), 0.006) * 1.05 + np.array([dx, 0.55, 0])
            d0 = sum(len(x) for x in pos)
            ar += [(d0 + i, d0 + i + 1) for i in range(len(pts) - 1) if np.linalg.norm(pts[i + 1] - pts[i]) < 0.3]
            pos.append(pts)
            col.append(np.where(rng.random(len(pts)) < 0.75, OR, OR_VIF))
            grp.append(np.full(len(pts), g))
            tai.append(np.full(len(pts), 0.95))
    return Forme("metiers", np.concatenate(pos), np.concatenate(col), np.concatenate(grp), np.concatenate(tai), ar)


FAMILLES = {"IA au quotidien": OR, "IA avancée": OR_CLAIR, "Visibilité": BLANC, "Gouvernance": BLEU_CLAIR, "Humain": GRIS}
ETOILES = [  # (famille, x, y) — 11 formations + 1 « bientôt » (pâle)
    ("IA au quotidien", 0.9, 2.3), ("IA au quotidien", 2.1, 1.1),
    ("IA avancée", 3.5, 2.9), ("IA avancée", 4.8, 2.0), ("IA avancée", 4.0, 0.6),
    ("Visibilité", 6.3, 2.5), ("Visibilité", 6.8, 0.8),
    ("Gouvernance", 1.9, -1.5), ("Gouvernance", 3.3, -2.5),
    ("Humain", 5.1, -1.2), ("Humain", 6.4, -2.6),
    ("IA au quotidien", 0.5, 0.2),
]


def f_etoiles():
    """11 formations = 11 étoiles colorées par famille (+ 1 étoile pâle « bientôt »), reliées en constellation."""
    comptes = repartir([1.0] * 11 + [0.55], N)
    pos, col, grp, tai, ancres = [], [], [], [], []
    for k, ((fam, x, y), n) in enumerate(zip(ETOILES, comptes)):
        c = np.array([x, y, rng.uniform(-0.6, 0.6)])
        n = int(n)
        n_coeur, n_halo = int(n * 0.45), int(n * 0.2)
        n_rayons = n - n_coeur - n_halo
        coeur = c + rng.normal(0, 0.045, (n_coeur, 3))
        halo = c + rng.normal(0, 0.2, (n_halo, 3))
        rayons = []
        for r in range(n_rayons):
            a = (r % 4) * math.pi / 2 + math.pi / 4 * (r % 8 >= 4)
            longueur = 0.75 if r % 8 < 4 else 0.38
            u = rng.uniform(0.1, 1.0) ** 1.6
            rayons.append(c + np.array([math.cos(a) * longueur * u, math.sin(a) * longueur * u, 0]))
        ancres.append(sum(len(p) for p in pos))
        pos += [coeur, halo, np.array(rayons)]
        couleur = FAMILLES[fam]
        col += [np.full(len(coeur), couleur), np.full(len(halo), couleur), np.full(len(rayons), couleur)]
        grp += [np.full(n, k)]
        tai += [np.full(len(coeur), 1.5), np.full(len(halo), 0.6), np.full(len(rayons), 0.75)]
    # constellation : chaînes par famille + quelques liens entre familles
    liens = [(0, 1), (1, 11), (2, 3), (3, 4), (5, 6), (7, 8), (9, 10), (1, 4), (4, 6), (8, 9), (7, 1), (6, 10)]
    ar = [(ancres[a], ancres[b]) for a, b in liens]
    return Forme("etoiles", np.concatenate(pos), np.concatenate(col), np.concatenate(grp), np.concatenate(tai), ar)


def f_sceau():
    """Sceau de confiance : anneaux concentriques (rotation pilotée par groupe), graduations, centre vide."""
    rayons = [1.75, 2.35, 2.95, 3.55]
    poids = [0.9, 1.1, 1.0, 1.25]
    n_grad = 48 * 6
    comptes = repartir([r * w for r, w in zip(rayons, poids)], N - n_grad)
    pos, col, grp, tai, ar = [], [], [], [], []
    for g, (r, n) in enumerate(zip(rayons, comptes)):
        t = np.linspace(0, 2 * math.pi, int(n), endpoint=False)
        pts = np.column_stack([r * np.cos(t), r * np.sin(t), np.zeros(len(t))])
        d0 = sum(len(x) for x in pos)
        if g != 3:  # anneau extérieur en pointillés (pas de liens)
            ar += [(d0 + i, d0 + (i + 1) % len(t)) for i in range(len(t))]
        pos.append(pts)
        col.append(np.full(len(t), [OR_CLAIR, OR, OR_VIF, OR][g]))
        grp.append(np.full(len(t), g))
        tai.append(np.full(len(t), [0.8, 0.95, 0.9, 1.4][g]))
    for i in range(48):  # graduations entre les anneaux 2 et 3
        a = 2 * math.pi * i / 48
        long = 0.32 if i % 4 == 0 else 0.18
        pts = np.array([[(2.47 + u) * math.cos(a), (2.47 + u) * math.sin(a), 0] for u in np.linspace(0, long, 6)])
        d0 = sum(len(x) for x in pos)
        ar += [(d0 + j, d0 + j + 1) for j in range(5)]
        pos.append(pts)
        col.append(np.full(6, OR))
        grp.append(np.full(6, 1))
        tai.append(np.full(6, 0.8))
    return Forme("sceau", np.concatenate(pos), np.concatenate(col), np.concatenate(grp), np.concatenate(tai), ar)


def f_embleme():
    """Emblème officiel échantillonné (jamais redessiné) : les points se posent sur les traits du fichier."""
    im = Image.open(RACINE / "assets" / "embleme-transparent.png").convert("RGBA")
    a = np.array(im)
    alpha = a[:, :, 3] > 140
    ys, xs = np.nonzero(alpha)
    i = rng.choice(len(xs), N, replace=False)
    xs, ys = xs[i].astype(float), ys[i].astype(float)
    rgb = a[ys.astype(int), xs.astype(int), :3].astype(float)
    refs = {BLEU_CLAIR: (27, 58, 107), GRIS: (120, 122, 112), OR: (201, 171, 76)}
    cles = list(refs)
    dist = np.stack([np.linalg.norm(rgb - np.array(refs[k]), axis=1) for k in cles], 1)
    col = np.array(cles)[np.argmin(dist, 1)]
    h, w = alpha.shape
    L = 9.0
    k = L / w
    pos = np.column_stack([(xs - w / 2) * k, -(ys - h / 2) * k, rng.normal(0, 0.05, N)])
    return Forme("embleme", pos, col, taille=np.full(N, 0.9)), {"largeur_monde": L, "largeur_px": w, "hauteur_px": h}


def boite_embleme_dans_logo():
    """Position de l'emblème dans le logo complet (pour superposer exactement particules et fichier officiel)."""
    logo = np.array(Image.open(RACINE / "assets" / "logo-yeba-fond-sombre.png").convert("RGBA"))[:, :, 3] > 40
    lignes = np.nonzero(logo.any(1))[0]
    # l'emblème est le premier bloc opaque en partant du haut (séparé du mot YEBA par une bande vide)
    vides = np.nonzero(~logo.any(1))[0]
    fin_embleme = next((y for y in vides if y > lignes[0] + 20), lignes[-1])
    bloc = logo[: fin_embleme]
    cols = np.nonzero(bloc.any(0))[0]
    rows = np.nonzero(bloc.any(1))[0]
    return {"logo_w": int(logo.shape[1]), "logo_h": int(logo.shape[0]),
            "x0": int(cols[0]), "x1": int(cols[-1] + 1), "y0": int(rows[0]), "y1": int(rows[-1] + 1)}


# ───────────────────────────── assemblage ─────────────────────────────

def main():
    formes = [f_graine(), f_reseau(), f_yeba(), f_baobab()]
    ile = f_ile()
    formes.append(ile)
    chemin = f_chemin()
    formes += [chemin, f_metiers(), f_etoiles(), f_sceau()]
    embleme, meta_emb = f_embleme()
    formes.append(embleme)
    sortie = {"N": N, "palette": PALETTE, "formes": {}, "meta": {}}
    for f in formes:
        f.ordonner()
        sortie["formes"][f.nom] = f.json()
    sortie["meta"]["jalons"] = chemin.jalons
    sortie["meta"]["embleme"] = {**meta_emb, "dans_logo": boite_embleme_dans_logo()}
    sortie["meta"]["etoiles"] = [{"famille": fam, "x": x, "y": y} for fam, x, y in ETOILES]
    sortie["meta"]["source"] = "scripts/formes_v3.py — Natural Earth (domaine public), emblème officiel, Montserrat (OFL)"
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(json.dumps(sortie, separators=(",", ":")), encoding="utf-8")
    print(f"{SORTIE.relative_to(REMOTION)} : {len(formes)} formes × {N} points, {SORTIE.stat().st_size / 1e6:.2f} Mo")
    for f in formes:
        print(f"  {f.nom:8s} arêtes={len(f.aretes):5d}  étendue x={np.ptp(f.pos[:,0]):5.1f} y={np.ptp(f.pos[:,1]):5.1f} z={np.ptp(f.pos[:,2]):5.1f}")
    if "--apercu" in sys.argv:
        apercu(formes)


def apercu(formes):
    cases = []
    for f in formes:
        im = Image.new("RGB", (480, 300), (14, 14, 18))
        d = ImageDraw.Draw(im)
        a, b = f.plan if f.nom not in ("ile",) else (0, 2)
        p = f.pos[:, [a, b]].copy()
        if f.nom != "ile":
            p[:, 1] *= -1
        mn, mx = p.min(0), p.max(0)
        k = min(440 / max(mx[0] - mn[0], 1e-6), 260 / max(mx[1] - mn[1], 1e-6))
        q = (p - (mn + mx) / 2) * k + np.array([240, 150])
        for i, j in f.aretes:
            d.line([tuple(q[i]), tuple(q[j])], fill=(110, 92, 40))
        for (x, y), c in zip(q, f.col):
            col = tuple(int(PALETTE[c][k2:k2 + 2], 16) for k2 in (0, 2, 4))
            d.point((x, y), fill=col)
        d.text((8, 6), f.nom, fill=(255, 220, 120))
        cases.append(im)
    planche = Image.new("RGB", (480 * 4, 300 * ((len(cases) + 3) // 4)), (0, 0, 0))
    for i, c in enumerate(cases):
        planche.paste(c, ((i % 4) * 480, (i // 4) * 300))
    chemin = Path(tempfile.gettempdir()) / "formes_v3_apercu.png"
    planche.save(chemin)
    print("aperçu :", chemin)


if __name__ == "__main__":
    main()
