"""Contrôle d'accessibilité d'un .pptx pour un public malvoyant / en situation de handicap.

  python verifier_accessibilite.py presentation.pptx [--charte ../charte.json]

Vérifie, diapo par diapo :
  - tailles de police (minimum absolu, texte, titres) ;
  - nombre de mots (des mots-clés, pas des phrases) ;
  - mot trop long pour sa zone (risque de mot coupé en deux) ;
  - ligne / connecteur qui traverse une zone de texte ;
  - contraste texte / fond quand les couleurs sont explicites (WCAG 2.1 AA = 4,5:1) ;
  - texte alternatif des images.
Code de sortie 1 s'il reste au moins une ERREUR.
"""
import argparse
import json
import os
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Emu

ICI = os.path.dirname(os.path.abspath(__file__))
CHARTE = os.path.join(ICI, "..", "charte.json")
EMU_PAR_PT = 12700
LARGEUR_CAR = 0.62  # largeur moyenne d'un caractère en « em » (police sans empattement, gras inclus)


def luminance(hexa: str) -> float:
    r, g, b = (int(hexa[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contraste(a: str, b: str) -> float:
    l1, l2 = sorted((luminance(a), luminance(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def couleur_run(run):
    try:
        if run.font.color and run.font.color.type is not None and run.font.color.rgb is not None:
            return str(run.font.color.rgb)
    except (AttributeError, TypeError):
        pass
    return None


def remplissage(obj):
    try:
        if obj.fill.type == 1:  # MSO_FILL.SOLID
            return str(obj.fill.fore_color.rgb)
    except (AttributeError, TypeError, ValueError):
        pass
    return None


def boite(sh):
    if sh.left is None or sh.width is None:
        return None
    return (sh.left, sh.top, sh.left + sh.width, sh.top + sh.height)


def intersecte(a, b):
    return a and b and a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def est_titre(sh):
    try:
        return sh.is_placeholder and sh.placeholder_format.type in (1, 3)  # TITLE, CENTER_TITLE
    except (AttributeError, ValueError):
        return False


def formes(shapes):
    for sh in shapes:
        if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from formes(sh.shapes)
        else:
            yield sh


def analyser(chemin, regles):
    prs = Presentation(chemin)
    erreurs, alertes = [], []
    fond_defaut = "FFFFFF"
    for n, slide in enumerate(prs.slides, start=1):
        try:
            fond = remplissage(slide.background) or fond_defaut
        except (AttributeError, TypeError):
            fond = fond_defaut
        toutes = list(formes(slide.shapes))
        lignes = [s for s in toutes if s.shape_type == MSO_SHAPE_TYPE.LINE or getattr(s, "begin_x", None) is not None]
        mots_diapo = 0
        for sh in toutes:
            if sh.shape_type == MSO_SHAPE_TYPE.PICTURE:
                descr = sh._element.xpath("./p:nvPicPr/p:cNvPr/@descr")
                if not descr or not descr[0].strip():
                    erreurs.append(f"diapo {n} : image « {sh.name} » sans texte alternatif")
            if not sh.has_text_frame or not sh.text_frame.text.strip():
                continue
            titre = est_titre(sh)
            mini = regles["taille_min_titre_pt"] if titre else regles["taille_min_texte_pt"]
            fond_forme = remplissage(sh) or fond
            for ligne in lignes:
                if ligne is not sh and intersecte(boite(ligne), boite(sh)):
                    erreurs.append(f"diapo {n} : la ligne « {ligne.name} » traverse le texte « {sh.text_frame.text[:30]} »")
            for para in sh.text_frame.paragraphs:
                texte = "".join(r.text for r in para.runs).strip()
                if not texte:
                    continue
                mots = texte.split()
                mots_diapo += len(mots)
                if not titre and len(mots) > regles["mots_max_par_ligne"]:
                    alertes.append(f"diapo {n} : « {texte[:40]}… » = {len(mots)} mots → réduire à des mots-clés")
                for run in para.runs:
                    if not run.text.strip():
                        continue
                    taille = run.font.size.pt if run.font.size else None
                    if taille is None:
                        alertes.append(f"diapo {n} : taille héritée du modèle pour « {run.text[:25]} » → la fixer explicitement")
                        continue
                    if taille < regles["taille_min_absolue_pt"]:
                        erreurs.append(f"diapo {n} : « {run.text[:25]} » en {taille:g} pt (< {regles['taille_min_absolue_pt']} pt)")
                    elif taille < mini:
                        alertes.append(f"diapo {n} : « {run.text[:25]} » en {taille:g} pt (visé ≥ {mini} pt)")
                    if sh.width:
                        largeur_pt = Emu(sh.width).pt - 14  # marges internes par défaut
                        plus_long = max(run.text.split(), key=len)
                        if len(plus_long) * taille * LARGEUR_CAR > largeur_pt:
                            erreurs.append(f"diapo {n} : le mot « {plus_long} » risque d'être coupé (zone trop étroite)")
                    coul = couleur_run(run)
                    if coul:
                        c = contraste(coul, fond_forme)
                        if c < regles["contraste_min"]:
                            erreurs.append(f"diapo {n} : contraste {c:.1f}:1 pour « {run.text[:25]} » (min {regles['contraste_min']}:1)")
                        elif c < regles["contraste_vise"]:
                            alertes.append(f"diapo {n} : contraste {c:.1f}:1 pour « {run.text[:25]} » (visé {regles['contraste_vise']}:1)")
        if mots_diapo > regles["mots_max_par_diapo"]:
            alertes.append(f"diapo {n} : {mots_diapo} mots au total (max conseillé {regles['mots_max_par_diapo']})")
    return erreurs, sorted(set(alertes), key=alertes.index)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pptx")
    ap.add_argument("--charte", default=CHARTE)
    a = ap.parse_args(argv)
    with open(a.charte, encoding="utf-8") as f:
        regles = json.load(f)["accessibilite"]
    erreurs, alertes = analyser(a.pptx, regles)
    for e in erreurs:
        print("ERREUR  ", e)
    for w in alertes:
        print("ALERTE  ", w)
    print(f"\nBilan : {len(erreurs)} erreur(s), {len(alertes)} alerte(s)")
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
