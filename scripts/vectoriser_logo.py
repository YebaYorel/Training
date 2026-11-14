"""Vectorisation FIDÈLE du logo officiel YEBA FORMATIONS (fichier fourni, jamais redessiné).

    python scripts/vectoriser_logo.py site/scripts/documents-pdf/logo-yeba.png dossier_sortie/

Méthode (numpy + PIL uniquement) : agrandissement de la couche alpha (Lanczos), extraction des contours
au sous-pixel (« marching squares », seuil 50 %), simplification de Ramer-Douglas-Peucker, puis remplissage
avec les couleurs relevées sur l'original : aplat pour « YEBA » et « FORMATIONS », dégradé horizontal
relevé colonne par colonne pour les montagnes. Le résultat est à comparer à l'original avant tout usage.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ECHELLE = 3          # suréchantillonnage avant extraction des contours
TOLERANCE = 0.18     # tolérance de simplification, en pixels de l'original


def contours(champ, seuil=0.5):
    """Iso-contours fermés d'un champ 2D (bords mis à zéro) : liste de polylignes [(x, y), ...]."""
    f = np.pad(champ, 1)
    h, w = f.shape
    tl, tr, br, bl = f[:-1, :-1], f[:-1, 1:], f[1:, 1:], f[1:, :-1]
    cas = (tl > seuil) * 8 + (tr > seuil) * 4 + (br > seuil) * 2 + (bl > seuil) * 1
    ii, jj = np.nonzero((cas > 0) & (cas < 15))

    def pt(cle):
        sens, i, j = cle
        if sens == 'h':   # arête horizontale à la ligne i, entre les colonnes j et j+1
            a, b = f[i, j], f[i, j + 1]
            return (j + (seuil - a) / (b - a) - 1, i - 1)
        a, b = f[i, j], f[i + 1, j]   # arête verticale à la colonne j, entre les lignes i et i+1
        return (j - 1, i + (seuil - a) / (b - a) - 1)

    voisins = {}

    def lier(a, b):
        voisins.setdefault(a, []).append(b)
        voisins.setdefault(b, []).append(a)

    for i, j in zip(ii.tolist(), jj.tolist()):
        c = int(cas[i, j])
        haut, droite, bas, gauche = ('h', i, j), ('v', i, j + 1), ('h', i + 1, j), ('v', i, j)
        centre = (f[i, j] + f[i, j + 1] + f[i + 1, j + 1] + f[i + 1, j]) / 4 > seuil
        table = {1: [(gauche, bas)], 2: [(bas, droite)], 3: [(gauche, droite)], 4: [(haut, droite)],
                 5: [(gauche, haut), (bas, droite)] if centre else [(gauche, bas), (haut, droite)],
                 6: [(haut, bas)], 7: [(gauche, haut)], 8: [(gauche, haut)], 9: [(haut, bas)],
                 10: [(haut, droite), (gauche, bas)] if centre else [(gauche, haut), (bas, droite)],
                 11: [(haut, droite)], 12: [(gauche, droite)], 13: [(bas, droite)], 14: [(gauche, bas)]}
        for a, b in table[c]:
            lier(a, b)
    vus, lignes = set(), []
    for depart in voisins:
        if depart in vus:
            continue
        chemin, precedent, courant = [depart], None, depart
        vus.add(depart)
        while True:
            suivants = [n for n in voisins[courant] if n != precedent and n not in vus]
            if not suivants:
                break
            precedent, courant = courant, suivants[0]
            vus.add(courant)
            chemin.append(courant)
        if len(chemin) > 4:
            lignes.append([pt(k) for k in chemin])
    return lignes


def rdp(points, tol):
    """Simplification de Ramer-Douglas-Peucker (itérative)."""
    p = np.asarray(points, float)
    if len(p) < 4:
        return p
    garder = np.zeros(len(p), bool)
    garder[0] = garder[-1] = True
    pile = [(0, len(p) - 1)]
    while pile:
        a, b = pile.pop()
        if b <= a + 1:
            continue
        seg = p[b] - p[a]
        n = np.hypot(*seg) or 1e-9
        v = p[a + 1:b] - p[a]
        d = np.abs(seg[0] * v[:, 1] - seg[1] * v[:, 0]) / n
        k = int(np.argmax(d))
        if d[k] > tol:
            garder[a + 1 + k] = True
            pile += [(a, a + 1 + k), (a + 1 + k, b)]
    return p[garder]


def chemin_svg(lignes, decalage, tolerance=TOLERANCE, angle_coin=32):
    """Polygones simplifiés → tracé SVG lissé : angles nets conservés, courbes en Bézier quadratiques."""
    ox, oy = decalage
    morceaux = []
    for l in lignes:
        p = np.vstack([l, l[:1]])
        k = int(np.argmax(np.hypot(*(p - p[0]).T)))   # courbe fermée : on la coupe au point le plus éloigné du départ
        q = np.vstack([rdp(p[:k + 1], tolerance * ECHELLE)[:-1], rdp(p[k:], tolerance * ECHELLE)])[:-1] / ECHELLE
        q = q - (ox, oy)
        n = len(q)
        if n < 3:
            continue
        av, ap = np.roll(q, 1, axis=0), np.roll(q, -1, axis=0)
        u, v = q - av, ap - q
        cosang = (u * v).sum(1) / (np.hypot(*u.T) * np.hypot(*v.T) + 1e-9)
        coin = np.degrees(np.arccos(np.clip(cosang, -1, 1))) > angle_coin
        mil = (q + ap) / 2
        f = lambda pt: f'{pt[0]:.2f} {pt[1]:.2f}'
        d = ['M' + f(mil[-1])]
        for i in range(n):
            if coin[i]:
                d.append('L' + f(q[i]) + ' L' + f(mil[i]))
            else:
                d.append('Q' + f(q[i]) + ' ' + f(mil[i]))
        morceaux.append(' '.join(d) + ' Z')
    return ' '.join(morceaux)


def couleur(rgba, masque):
    px = rgba[masque & (rgba[..., 3] > 220)][:, :3]
    return '#%02X%02X%02X' % tuple(int(v) for v in np.median(px, axis=0))


def main(source, sortie):
    sortie = Path(sortie)
    sortie.mkdir(parents=True, exist_ok=True)
    im = Image.open(source).convert('RGBA')
    rgba = np.asarray(im).astype(float)
    alpha = rgba[..., 3]
    # 1. Trois zones séparées par des lignes vides : montagnes, « YEBA », « FORMATIONS »
    lignes_pleines = np.nonzero((alpha > 30).any(axis=1))[0]
    coupures = np.nonzero(np.diff(lignes_pleines) > 1)[0]
    bornes = np.split(lignes_pleines, coupures + 1)
    assert len(bornes) == 3, f'{len(bornes)} zones trouvées (3 attendues)'
    # 2. Contours au sous-pixel sur l'alpha agrandi
    grand = np.asarray(Image.fromarray(alpha.astype(np.uint8)).resize((im.width * ECHELLE, im.height * ECHELLE), Image.LANCZOS)).astype(float) / 255
    ys, xs = np.nonzero(alpha > 30)
    x0, y0, x1, y1 = xs.min() - 4, ys.min() - 4, xs.max() + 5, ys.max() + 5
    zones = []
    for b in bornes:
        z = np.zeros_like(grand)
        haut, bas = b[0] * ECHELLE - 2, (b[-1] + 1) * ECHELLE + 2
        z[haut:bas] = grand[haut:bas]
        m = np.zeros(alpha.shape, bool)
        m[b[0]:b[-1] + 1] = True
        tol = 0.4 if not zones else 0.7          # montagnes : traits fins ; lettres : bords droits redressés
        zones.append((chemin_svg(contours(z), (x0, y0), tol), m))
    # 3. Couleurs relevées sur l'original
    mont = zones[0][1] & (alpha > 220)
    cols = np.nonzero(mont.any(axis=0))[0]
    gx0, gx1 = cols.min(), cols.max()
    arrets = []
    for t in np.linspace(0, 1, 13):
        cx = gx0 + t * (gx1 - gx0)
        bande = mont & (np.abs(np.arange(alpha.shape[1]) - cx) < 14)[None, :]
        if bande.sum() > 20:
            r, g, b = np.median(rgba[bande][:, :3], axis=0)
            arrets.append(f'<stop offset="{t:.3f}" stop-color="#{int(r):02X}{int(g):02X}{int(b):02X}"/>')
    c_yeba, c_form = couleur(rgba, zones[1][1]), couleur(rgba, zones[2][1])
    w, h = x1 - x0, y1 - y0

    def svg(remplissages, titre):
        defs = (f'<defs><linearGradient id="montagnes" gradientUnits="userSpaceOnUse" x1="{gx0 - x0}" y1="0" x2="{gx1 - x0}" y2="0">'
                + ''.join(arrets) + '</linearGradient></defs>') if remplissages[0] == 'url(#montagnes)' else ''
        corps = ''.join(f'<path fill="{f}" fill-rule="evenodd" d="{d}"/>' for f, (d, _) in zip(remplissages, zones))
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{titre}">'
                f'<title>{titre}</title>{defs}{corps}</svg>\n')

    (sortie / 'YEBA-logo-couleur.svg').write_text(svg(['url(#montagnes)', c_yeba, c_form], 'YEBA FORMATIONS'), encoding='utf-8')
    (sortie / 'YEBA-logo-blanc.svg').write_text(svg(['#FFFFFF'] * 3, 'YEBA FORMATIONS'), encoding='utf-8')
    (sortie / 'YEBA-logo-bleu.svg').write_text(svg(['#1B3A6B'] * 3, 'YEBA FORMATIONS'), encoding='utf-8')
    print(f'zones : {[len(b) for b in bornes]} lignes ; couleurs YEBA {c_yeba}, FORMATIONS {c_form} ; {len(arrets)} arrêts de dégradé ; '
          f'taille {w} × {h}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
