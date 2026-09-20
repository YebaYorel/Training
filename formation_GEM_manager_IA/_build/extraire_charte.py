# -*- coding: utf-8 -*-
"""Extrait la charte couleur d'un logo et l'ecrit dans charte.json.

Usage :  python3 extraire_charte.py ../charte/logo_gem.png
         python3 extraire_charte.py --couleurs "#0B4F8A" "#E2001A"

Le script assombrit automatiquement une couleur de marque trop claire
jusqu'a obtenir un contraste conforme WCAG 2.1 AA, puis verifie l'ensemble.
Les couleurs semantiques (vert = validation, rouge = interdit) restent
inchangees : elles portent du sens pedagogique, pas de l'identite.
"""
import sys, json, colorsys, os
from charte import DEFAUT, contraste, verifier

def hexa(rgb):
    return "#%02X%02X%02X" % tuple(max(0, min(255, int(round(v)))) for v in rgb)

def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def satur(c):
    return colorsys.rgb_to_hsv(*[v / 255 for v in c])[1]

def clarte(c):
    return colorsys.rgb_to_hsv(*[v / 255 for v in c])[2]

def assombrir(h, cible, fond="#FFFFFF", pas=0.04):
    """Assombrit progressivement jusqu'au contraste cible avec le fond."""
    r, g, b = [v / 255 for v in rgb(h)]
    hh, ss, vv = colorsys.rgb_to_hsv(r, g, b)
    for _ in range(40):
        if contraste(hexa([x * 255 for x in colorsys.hsv_to_rgb(hh, ss, vv)]), fond) >= cible:
            break
        vv = max(0.05, vv - pas)
    return hexa([x * 255 for x in colorsys.hsv_to_rgb(hh, ss, vv)])

def depuis_logo(chemin, n=10):
    from PIL import Image
    im = Image.open(chemin)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        fond = Image.new("RGB", im.size, (255, 255, 255))
        fond.paste(im, mask=im.split()[-1])
        im = fond
    else:
        im = im.convert("RGB")
    im.thumbnail((240, 240))
    q = im.quantize(colors=n, method=Image.MEDIANCUT).convert("RGB")
    compte = {}
    for px in q.getdata():
        compte[px] = compte.get(px, 0) + 1
    # On ecarte les quasi-blancs, quasi-noirs et gris desatures
    cands = [(c, n_) for c, n_ in compte.items()
             if satur(c) > 0.20 and 0.12 < clarte(c) < 0.97]
    if not cands:
        raise SystemExit("Aucune couleur de marque exploitable dans ce logo. "
                         "Utilisez --couleurs \"#xxxxxx\" \"#yyyyyy\".")
    cands.sort(key=lambda x: -x[1])
    retenues = [hexa(c) for c, _ in cands[:4]]
    print("Couleurs dominantes detectees : " + "  ".join(retenues))
    return retenues

def construire(couleurs, origine):
    # La plus sombre devient le bandeau ; la plus saturee devient l'accent.
    tri_sombre = sorted(couleurs, key=lambda h: clarte(rgb(h)))
    tri_satur  = sorted(couleurs, key=lambda h: -satur(rgb(h)))
    nuit = tri_sombre[0]
    accent = next((c for c in tri_satur if c != nuit), tri_satur[0])

    c = dict(DEFAUT)
    c["charte_source"] = origine
    c["nuit"]   = assombrir(nuit,   4.5)          # fond, texte blanc dessus
    c["accent"] = assombrir(accent, 4.5)          # sert aussi en texte sur blanc
    # gris et clair derives du bandeau pour rester dans la famille chromatique
    hh, ss, vv = colorsys.rgb_to_hsv(*[v / 255 for v in rgb(c["nuit"])])
    c["gris"]  = assombrir(hexa([x*255 for x in colorsys.hsv_to_rgb(hh, ss*.55, .42)]), 4.5)
    c["clair"] = hexa([x*255 for x in colorsys.hsv_to_rgb(hh, min(ss*.18, .10), .96)])
    c["txt"]   = assombrir(hexa([x*255 for x in colorsys.hsv_to_rgb(hh, ss*.35, .18)]), 7.0)
    return c

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        raise SystemExit(__doc__)
    if args[0] == "--couleurs":
        couleurs = [a if a.startswith("#") else "#" + a for a in args[1:]]
        if len(couleurs) < 2:
            raise SystemExit("Donnez au moins deux couleurs.")
        c = construire(couleurs, "charte GEM Formation — couleurs fournies : " + " ".join(couleurs))
    else:
        if not os.path.exists(args[0]):
            raise SystemExit("Fichier introuvable : " + args[0])
        c = construire(depuis_logo(args[0]), "charte GEM Formation — extraite de " + os.path.basename(args[0]))

    ech = verifier(c, strict=False)
    if ech:
        print("ATTENTION — couples non conformes apres correction :")
        for e in ech:
            print("   " + e)
        print("La generation reste possible mais l'accessibilite n'est plus garantie.")
    else:
        print("Contrôle WCAG 2.1 AA : CONFORME")
    for k in ("nuit", "accent", "vert", "rouge", "gris", "clair", "txt"):
        print("  %-7s %s" % (k, c[k]))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "charte.json"),
              "w", encoding="utf-8") as fh:
        json.dump(c, fh, ensure_ascii=False, indent=2)
    print("\ncharte.json ecrit. Relancez les scripts de generation.")
