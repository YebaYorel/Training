"""Contrôle d'accessibilité d'un .pptx pour un public malvoyant / en situation de handicap.

  python verifier_accessibilite.py presentation.pptx [--charte ../charte.json]

Vérifie, diapo par diapo :
  - tailles de police (minimum absolu, texte, titres) ;
  - nombre de mots (des mots-clés, pas des phrases) ;
  - mot trop long pour sa zone (risque de mot coupé en deux) ;
  - ligne / connecteur qui traverse une zone de texte ;
  - contraste texte / fond quand les couleurs sont explicites (WCAG 2.1 AA = 4,5:1) ;
  - texte alternatif des images.
Précision (v2, 12/11/2026) :
  - fond réel d'un texte = fond de la diapo + formes pleines situées DESSOUS (transparence comprise) ;
  - éléments marqués « décoratif » (PowerPoint : Marquer comme décoratif) : ni texte alternatif ni contraste exigés ;
  - largeur des mots mesurée sur les vraies polices quand elles sont disponibles (YEBA_POLICES ou assets/fonts),
    groupes insécables (espaces insécables) compris.
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


DECORATIF_URI = "{C183D7F6-B498-43B3-948B-1728B52AA6E4}"
NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"


def est_decoratif(sh) -> bool:
    """Forme ou image marquée « décorative » (extension Office adec:decorative val=1)."""
    return any(v in ("1", "true") for v in sh._element.xpath(
        f'./*[1]/p:cNvPr/a:extLst/a:ext[@uri="{DECORATIF_URI}"]/*[local-name()="decorative"]/@val'))


def alpha_remplissage(sh) -> float:
    vals = sh._element.xpath("./p:spPr/a:solidFill/a:srgbClr/a:alpha/@val")
    return int(vals[0]) / 100000 if vals else 1.0


def melanger(dessus: str, dessous: str, alpha: float) -> str:
    a = [int(dessus[i:i + 2], 16) for i in (0, 2, 4)]
    b = [int(dessous[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join(f"{round(alpha * x + (1 - alpha) * y):02X}" for x, y in zip(a, b))


def fond_reel(sh, toutes, fond):
    """Couleur réellement derrière le texte : fond de diapo, puis chaque forme pleine placée dessous (ordre
    d'empilement) qui contient le centre du texte, transparence comprise, puis le remplissage du texte lui-même."""
    b = boite(sh)
    if not b:
        return remplissage(sh) or fond
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    couleur = fond
    for autre in toutes:
        if autre is sh:
            break
        bb = boite(autre)
        rem = remplissage(autre) if autre.shape_type != MSO_SHAPE_TYPE.PICTURE else None
        if rem and bb and bb[0] <= cx <= bb[2] and bb[1] <= cy <= bb[3]:
            couleur = melanger(rem, couleur, alpha_remplissage(autre))
    propre = remplissage(sh)
    if propre:
        couleur = melanger(propre, couleur, alpha_remplissage(sh))
    return couleur


_POLICES = {"montserrat extrabold": "Montserrat-800.ttf", "montserrat black": "Montserrat-900.ttf",
            "montserrat bold": "Montserrat-700.ttf", "montserrat semibold": "Montserrat-600.ttf",
            "montserrat": "Montserrat-400.ttf", "inter semibold": "Inter-600.otf", "inter": "Inter-400.otf"}
_CACHE_POLICES = {}


def _dossiers_polices():
    racine = os.path.abspath(os.path.join(ICI, "..", "..", "..", ".."))
    return [d for d in (os.environ.get("YEBA_POLICES"), os.path.join(ICI, "..", "assets", "fonts"),
                        os.path.join(racine, "soiree-lancement", "assets", "fonts")) if d and os.path.isdir(d)]


def largeur_pt(txt: str, taille: float, police) -> float:
    """Largeur d'un texte en points : glyphes réels si la police est disponible, sinon moyenne 0,62 em."""
    fichier = _POLICES.get((police or "").lower())
    if fichier:
        cle = (fichier, taille)
        if cle not in _CACHE_POLICES:
            _CACHE_POLICES[cle] = None
            try:
                from PIL import ImageFont
                for d in _dossiers_polices():
                    if os.path.exists(os.path.join(d, fichier)):
                        _CACHE_POLICES[cle] = ImageFont.truetype(os.path.join(d, fichier), size=int(taille * 10))
                        break
            except ImportError:
                pass
        f = _CACHE_POLICES[cle]
        if f is not None:
            return f.getlength(txt) / 10
    return len(txt) * taille * LARGEUR_CAR


def marges_pt(sh) -> float:
    vals = sh._element.xpath("./p:txBody/a:bodyPr/@lIns | ./p:txBody/a:bodyPr/@rIns")
    if len(vals) == 2:
        return sum(int(v) for v in vals) / EMU_PAR_PT
    return 14.4  # 0,1 in de chaque côté (valeur par défaut de PowerPoint)


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
    erreurs, alertes, decoratifs = [], [], []
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
            deco = est_decoratif(sh)
            if sh.shape_type == MSO_SHAPE_TYPE.PICTURE and not deco:
                descr = sh._element.xpath("./p:nvPicPr/p:cNvPr/@descr")
                if not descr or not descr[0].strip():
                    erreurs.append(f"diapo {n} : image « {sh.name} » sans texte alternatif (ni marquée décorative)")
            if not sh.has_text_frame or not sh.text_frame.text.strip():
                continue
            if deco:
                decoratifs.append(f"diapo {n} : « {sh.text_frame.text[:20]} » ({sh.name})")
                continue
            titre = est_titre(sh)
            mini = regles["taille_min_titre_pt"] if titre else regles["taille_min_texte_pt"]
            fond_forme = fond_reel(sh, toutes, fond)
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
                    if sh.width and sh.text_frame.word_wrap is not False:
                        dispo = Emu(sh.width).pt - marges_pt(sh)
                        # unités insécables : on ne coupe qu'aux espaces ordinaires (pas aux espaces insécables)
                        blocs = [m for m in run.text.replace("\n", " ").replace("\v", " ").replace("\t", " ").split(" ") if m]
                        if blocs:
                            plus_long = max(blocs, key=lambda m: largeur_pt(m, taille, run.font.name))
                            if largeur_pt(plus_long, taille, run.font.name) > dispo:
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
    return erreurs, sorted(set(alertes), key=alertes.index), decoratifs


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pptx")
    ap.add_argument("--charte", default=CHARTE)
    a = ap.parse_args(argv)
    with open(a.charte, encoding="utf-8") as f:
        regles = json.load(f)["accessibilite"]
    erreurs, alertes, decoratifs = analyser(a.pptx, regles)
    for e in erreurs:
        print("ERREUR  ", e)
    for w in alertes:
        print("ALERTE  ", w)
    if decoratifs:
        print(f"\nInfo : {len(decoratifs)} texte(s) marqué(s) décoratif(s), exemptés (ignorés par les lecteurs d'écran) :")
        for d in decoratifs[:12]:
            print("  -", d)
    print(f"\nBilan : {len(erreurs)} erreur(s), {len(alertes)} alerte(s)")
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
