# -*- coding: utf-8 -*-
"""Source unique de vérité : identité visuelle et cadre de la session.

Modifier CE fichier (ou charte.json) suffit a rehabiller tous les supports.
Les couleurs sont validees automatiquement : contraste >= 4.5:1 (WCAG 2.1 AA).
"""
import json, os

DEFAUT = {
    "organisme": "GEM FORMATION",
    "titre_jour": "Manager aujourd'hui : posture et intelligence artificielle",
    "modalite": "FORMATION À DISTANCE — 1 JOUR",
    "public": "Titre professionnel Manager d'Établissement Marchand (MEM)",
    "horaires": "9h00 → 17h00",
    # --- Palette : REMPLACER par la charte GEM Formation quand elle sera fournie
    "charte_source": "palette neutre provisoire — charte GEM non fournie",
    "nuit":   "#12294A",   # bandeaux, fonds sombres
    "accent": "#C2410C",   # rappels, encadres
    "vert":   "#156B36",   # jeux, validations
    "rouge":  "#B91C1C",   # alertes, interdits
    "gris":   "#4A5568",
    "clair":  "#EFF2F7",
    "txt":    "#1A1A2E",
}

def _lum(hexa):
    h = hexa.lstrip("#")
    c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def contraste(a, b):
    l1, l2 = sorted([_lum(a), _lum(b)], reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)

def charger():
    c = dict(DEFAUT)
    chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charte.json")
    if os.path.exists(chemin):
        with open(chemin, encoding="utf-8") as fh:
            c.update(json.load(fh))
    return c

def verifier(c, strict=True):
    """Controle WCAG 2.1 AA. Retourne la liste des couples non conformes."""
    couples = [
        ("texte sur blanc",        c["txt"],   "#FFFFFF", 4.5),
        ("gris sur blanc",         c["gris"],  "#FFFFFF", 4.5),
        ("accent sur blanc",       c["accent"],"#FFFFFF", 4.5),
        ("vert sur blanc",         c["vert"],  "#FFFFFF", 4.5),
        ("rouge sur blanc",        c["rouge"], "#FFFFFF", 4.5),
        ("blanc sur bandeau nuit", "#FFFFFF",  c["nuit"],  4.5),
        ("blanc sur bandeau vert", "#FFFFFF",  c["vert"],  4.5),
        ("blanc sur bandeau rouge","#FFFFFF",  c["rouge"], 4.5),
        ("blanc sur accent",       "#FFFFFF",  c["accent"],4.5),
        ("texte sur fond clair",   c["txt"],   c["clair"], 4.5),
    ]
    echecs = []
    for nom, a, b, seuil in couples:
        r = contraste(a, b)
        if r < seuil:
            echecs.append("%s : %.2f:1 (minimum %.1f:1)" % (nom, r, seuil))
    if echecs and strict:
        raise SystemExit("CHARTE NON ACCESSIBLE — corriger avant de générer :\n  "
                         + "\n  ".join(echecs))
    return echecs

if __name__ == "__main__":
    c = charger()
    print("Charte : %s" % c["charte_source"])
    for nom in ("nuit", "accent", "vert", "rouge", "gris", "clair", "txt"):
        print("  %-7s %s" % (nom, c[nom]))
    ech = verifier(c, strict=False)
    print("\nContrôle WCAG 2.1 AA : %s" % ("CONFORME" if not ech else "\n  ".join(ech)))
