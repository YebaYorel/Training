"""Génère le PowerPoint « YEBA — Saison 1 » (python-pptx), motion design natif.

Source unique : ../contenu/slides.json — modifier le JSON puis relancer :
    python3 pptx/build_pptx.py            → dist/YEBA_Soiree_Lancement.pptx (version « cinéma »)
    python3 pptx/build_pptx.py --sobre    → dist/YEBA_Soiree_Lancement_SOBRE.pptx (fonds en images fixes : aucune vidéo de fond à lire)
    python3 pptx/build_pptx.py --images   → dist/YEBA_Soiree_Lancement_IMAGES.pptx (source du PDF, toutes vidéos en images)

Ce que fait le script, sans macro :
  - Chronologie native : animations d'entrée (fondu montant, zoom, balayage, avec décélération)
    et lecture AUTOMATIQUE des vidéos (en boucle et muettes pour les fonds) ;
  - Transition Morphose sur chaque slide (repli Fondu), avance automatique à la fin des vidéos ;
  - Calques de mouvement : champ d'étoiles en parallaxe et halo de lumière que la Morphose fait
    glisser d'une slide à l'autre, vignettage cinéma ;
  - Fonds vidéo vivants (Remotion) sous le texte, qui reste éditable ;
  - Carrousels : objets hors champ nommés !!xxx pour faire glisser des groupes entiers ;
  - Accessibilité : titres structurés, texte alternatif, langue fr-FR, corps de texte >= 24 pt,
    aucun trait ne traverse un mot, espaces insécables (pas de mot orphelin coupé).
"""
import json
import math
import re
import sys
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

RACINE = Path(__file__).resolve().parent.parent
ASSETS = RACINE / "assets"
DIST = RACINE / "dist"
C = json.loads((RACINE / "contenu" / "slides.json").read_text(encoding="utf-8"))
PAL = {k: RGBColor.from_string(v) for k, v in C["palette"].items()}
GRIS2 = RGBColor.from_string("8C93A0")
ROUGE_LIVE = RGBColor.from_string("E53935")
NOIR_PUR = RGBColor.from_string("000000")
IMAGES = "--images" in sys.argv  # source du PDF : chaque vidéo devient son image fixe (sinon le PDF embarque les MP4)
SOBRE = "--sobre" in sys.argv or IMAGES

W, H = 13.333, 7.5
M = 0.8
PX = W / 1920  # pouces par pixel du repère 1920 × 1080 des vidéos
F_TEXTE = "Montserrat"
F_GRAS = "Montserrat ExtraBold"
F_NOIR = "Montserrat Black"
NB = " "

FONDS_TEINTE = {"noir": "noir", "terre": "terre", "bleu": "bleu", "bleu_nuit": "bleu_nuit"}


# ───────────────────────────────────────── typographie ─────────────────────────────────────────

_MOT_COURT = re.compile(r"(?<![\w'’])([A-Za-zÀ-ÖØ-öø-ÿ]{1,2}) (?=[\w«“(\d])")


def typo(t: str) -> str:
    """Typographie française : espaces insécables (avant : ; ? ! », après «, nombre + unité),
    « · » et « → » jamais en début de ligne, mots de 1-2 lettres jamais seuls en fin de ligne."""
    for signe in (" :", " ;", " ?", " !", " »"):
        t = t.replace(signe, NB + signe[1])
    t = t.replace("« ", "«" + NB)
    for unite in (" h", " j", " %", " €", " jours", " jour", " pers.", " stagiaires"):
        for chiffre in "0123456789":
            t = t.replace(chiffre + unite, chiffre + NB + unite[1:])
    t = t.replace("N° ", "N°" + NB).replace("n° ", "n°" + NB).replace("IA Act", "IA" + NB + "Act")
    t = t.replace(" · ", NB + "· ").replace(" → ", NB + "→" + NB).replace(" & ", " &" + NB)
    return _MOT_COURT.sub(lambda m: m.group(1) + NB, t)


_POLICES = {}
LH = 1.22  # hauteur de ligne réelle de Montserrat (ascendante + descendante) en « simple »
AVERTISSEMENTS = []  # textes qui ne tiennent pas : affichés en fin de construction


def largeur_texte(txt, pt, gras=True):
    """Largeur réelle (pouces) d'un texte, mesurée sur les glyphes Montserrat (+6 % de marge).
    gras : True = ExtraBold (800), False = Regular (400), "noir" = Black (900)."""
    from PIL import ImageFont

    poids = {True: 800, False: 400, "noir": 900}[gras]
    fichier = ASSETS / "fonts" / f"Montserrat-{poids}.ttf"
    cle = (fichier, pt)
    if cle not in _POLICES:
        _POLICES[cle] = ImageFont.truetype(str(fichier), size=int(pt * 10))
    return _POLICES[cle].getlength(txt) / 10 / 72 * 1.06


def nb_lignes(txt, pt, largeur, gras=True):
    lignes, courant = 1, 0.0
    esp = largeur_texte(" ", pt, gras)
    for mot in typo(txt).split(" "):
        l = largeur_texte(mot, pt, gras)
        if l > largeur:
            return 99  # un mot seul ne tient pas : interdit (aucune césure)
        if courant == 0:
            courant = l
        elif courant + esp + l <= largeur:
            courant += esp + l
        else:
            lignes += 1
            courant = l
    return lignes


def _hauteur(paras, pt, largeur, interligne, gras):
    return sum(nb_lignes(p, pt, largeur - 0.2, gras) * pt * LH * interligne / 72 for p in paras)


def taille_qui_tient(paras, largeur, hauteur, pt_max, pt_min=24, interligne=1.0, gras=True):
    """Plus grand corps (pas de 2 pt) qui tient dans la boîte, sans couper un mot ; sinon alerte."""
    pt = pt_max
    while pt >= pt_min:
        if _hauteur(paras, pt, largeur, interligne, gras) <= hauteur - 0.1:
            return pt
        pt -= 2
    AVERTISSEMENTS.append(f"ne tient pas à {pt_min} pt dans {largeur:.2f} × {hauteur:.2f} in : {' / '.join(paras)}")
    return pt_min


def hauteur_texte(txt, pt, largeur, interligne=1.0, gras=True):
    return _hauteur([txt], pt, largeur, interligne, gras) + 0.1


# ───────────────────────────────────────── formes de base ─────────────────────────────────────────

def nommer(shape, nom):
    shape.name = nom
    return shape


def _run(p, texte, pt, couleur, police=F_GRAS, espacement=None):
    r = p.add_run()
    r.text = typo(texte)
    f = r.font
    f.size = Pt(pt)
    f.name = police
    f.color.rgb = couleur
    rpr = r._r.get_or_add_rPr()
    rpr.set("lang", "fr-FR")
    if espacement:
        rpr.set("spc", str(espacement))
    return r


def _prep_tf(tf, ancre, marge=0.05, retour=True):
    tf.word_wrap = retour
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = ancre
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, Inches(marge))


def _remplir(tf, paras, align, interligne):
    for i, runs in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = interligne
        for run in runs:
            _run(p, *run)


def texte(sl, nom, x, y, w, h, paras, align=PP_ALIGN.LEFT, ancre=MSO_ANCHOR.TOP, interligne=1.0, retour=True):
    """Zone de texte. retour=False : jamais de retour à la ligne (étiquettes courtes : heures, chiffres)."""
    tb = sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    nommer(tb, nom)
    _prep_tf(tb.text_frame, ancre, retour=retour)
    _remplir(tb.text_frame, paras, align, interligne)
    return tb


def titre(sl, x, y, w, h, paras, align=PP_ALIGN.LEFT, ancre=MSO_ANCHOR.TOP, interligne=1.0, nom="titre"):
    """Espace réservé « Titre » (structure lue par les lecteurs d'écran)."""
    ph = sl.shapes.title
    nommer(ph, nom)
    ph.left, ph.top, ph.width, ph.height = Inches(x), Inches(y), Inches(w), Inches(h)
    tf = ph.text_frame
    _prep_tf(tf, ancre)
    tf.text = ""
    _remplir(tf, paras, align, interligne)
    return ph


def titre_cache(sl, txt):
    """Titre hors champ (slides vidéo) : lu par les lecteurs d'écran, invisible à l'écran."""
    ph = sl.shapes.title
    nommer(ph, "titre")
    ph.text = typo(txt)
    ph.left, ph.top, ph.width, ph.height = Inches(-4), Inches(0), Inches(3), Inches(1)


def _alpha(el_couleur, pct):
    a = etree.SubElement(el_couleur, qn("a:alpha"))
    a.set("val", str(int(pct * 1000)))


def rect(sl, nom, x, y, w, h, couleur=None, contour=None, ep=2.0, forme=MSO_SHAPE.RECTANGLE, arrondi=None,
         opacite=100, opacite_contour=100, tirets=False):
    s = sl.shapes.add_shape(forme, Inches(x), Inches(y), Inches(w), Inches(h))
    nommer(s, nom)
    if couleur is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = couleur
        if opacite < 100:
            _alpha(s.fill._xPr.find(qn("a:solidFill")).find(qn("a:srgbClr")), opacite)
    if contour is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = contour
        s.line.width = Pt(ep)
        ln = s._element.spPr.find(qn("a:ln"))
        if opacite_contour < 100:
            _alpha(ln.find(qn("a:solidFill")).find(qn("a:srgbClr")), opacite_contour)
        if tirets:
            d = etree.SubElement(ln, qn("a:prstDash"))
            d.set("val", "dash")
    s.shadow.inherit = False
    if arrondi is not None and forme == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = arrondi
    return s


def image(sl, nom, chemin, x, y, w=None, h=None, alt=""):
    pic = sl.shapes.add_picture(str(chemin), Inches(x), Inches(y), Inches(w) if w else None, Inches(h) if h else None)
    nommer(pic, nom)
    pic._element.nvPicPr.cNvPr.set("descr", alt)
    return pic


def texte_forme(forme, paras, align=PP_ALIGN.CENTER, ancre=MSO_ANCHOR.MIDDLE, marge=0.08):
    tf = forme.text_frame
    _prep_tf(tf, ancre, marge)
    _remplir(tf, paras, align, 1.0)


def film(sl, nom, chemin, apercu, x=0, y=0, w=W, h=H, alt=""):
    """Vidéo intégrée, SANS le « clic = lecture/pause » que python-pptx ajoute par défaut.
    En mode --images (source du PDF), l'image fixe de la vidéo la remplace."""
    if IMAGES:
        return image(sl, nom, RACINE / apercu, x, y, w, h, alt=alt)
    mv = sl.shapes.add_movie(str(RACINE / chemin), Inches(x), Inches(y), Inches(w), Inches(h),
                             poster_frame_image=str(RACINE / apercu), mime_type="video/mp4")
    nommer(mv, nom)
    cnv = mv._element.nvPicPr.cNvPr
    cnv.set("descr", alt)
    for lien in cnv.findall(qn("a:hlinkClick")):
        cnv.remove(lien)
    timing = sl._element.find(qn("p:timing"))
    if timing is not None:
        sl._element.remove(timing)
    return mv


def note_hors_champ(sl, txt):
    """Post-it rouge À DROITE de la slide : visible en mode édition, jamais projeté."""
    r = rect(sl, "a-confirmer", W + 0.25, 0.3, 3.2, 1.6, couleur=RGBColor.from_string("C62828"))
    texte_forme(r, [[(txt, 16, PAL["blanc"], F_GRAS)]], align=PP_ALIGN.LEFT, ancre=MSO_ANCHOR.TOP, marge=0.12)


# ───────────────────────────────────────── chronologie native ─────────────────────────────────────────

P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"
P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"
P159 = "http://schemas.microsoft.com/office/powerpoint/2015/09/main"


class Chrono:
    """Construit <p:timing> : groupe 0 automatique, groupes suivants au clic, médias en lecture auto."""

    PRESETS = {"fondu": (10, 0), "fondu_montant": (42, 0), "zoom": (53, 16), "balayage": (22, 8)}

    def __init__(self, sl):
        self.sl = sl
        self.groupes = {0: []}
        self.medias = []

    def entree(self, shape, effet="fondu_montant", debut=0, duree=600, clic=None):
        g = 0 if clic is None else clic
        self.groupes.setdefault(g, []).append((shape, effet, int(debut), int(duree)))

    def media(self, shape, duree_s, boucle=False, muet=False):
        if IMAGES:
            return  # image fixe à la place de la vidéo : rien à lire
        self.medias.append((shape, int(duree_s * 1000), boucle, muet))

    def _bhvr(self, ident, spid, dur, attr=None, fill=True, decel=False):
        a = f' fill="hold"' if fill else ""
        d = ' decel="100000"' if decel else ""
        noms = f"<p:attrNameLst><p:attrName>{attr}</p:attrName></p:attrNameLst>" if attr else ""
        return f'<p:cBhvr><p:cTn id="{ident()}" dur="{dur}"{d}{a}/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>{noms}</p:cBhvr>'

    def _anim(self, ident, spid, dur, attr, de, a):
        return (f'<p:anim calcmode="lin" valueType="num">{self._bhvr(ident, spid, dur, attr, decel=True)}'
                f'<p:tavLst><p:tav tm="0"><p:val><p:strVal val="{de}"/></p:val></p:tav>'
                f'<p:tav tm="100000"><p:val><p:strVal val="{a}"/></p:val></p:tav></p:tavLst></p:anim>')

    def _effet(self, ident, shape, effet, debut, duree, type_noeud):
        spid = shape.shape_id
        pid, sous = self.PRESETS[effet]
        grp = ' grpId="0"'
        visible = (f'<p:set><p:cBhvr><p:cTn id="{ident()}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
                   f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr>'
                   f'<p:to><p:strVal val="visible"/></p:to></p:set>')
        if effet == "balayage":
            corps = f'<p:animEffect transition="in" filter="wipe(right)">{self._bhvr(ident, spid, duree, fill=False)}</p:animEffect>'
        else:
            corps = f'<p:animEffect transition="in" filter="fade">{self._bhvr(ident, spid, duree, fill=False)}</p:animEffect>'
        if effet == "fondu_montant":
            corps += self._anim(ident, spid, duree, "ppt_x", "#ppt_x", "#ppt_x")
            corps += self._anim(ident, spid, duree, "ppt_y", "#ppt_y+.06", "#ppt_y")
        elif effet == "zoom":
            corps += self._anim(ident, spid, duree, "ppt_w", "#ppt_w*0.82", "#ppt_w")
            corps += self._anim(ident, spid, duree, "ppt_h", "#ppt_h*0.82", "#ppt_h")
        return (f'<p:par><p:cTn id="{ident()}" presetID="{pid}" presetClass="entr" presetSubtype="{sous}" fill="hold"{grp} nodeType="{type_noeud}">'
                f'<p:stCondLst><p:cond delay="{debut}"/></p:stCondLst><p:childTnLst>{visible}{corps}</p:childTnLst></p:cTn></p:par>')

    def _lecture(self, ident, shape, dur, type_noeud):
        return (f'<p:par><p:cTn id="{ident()}" presetID="1" presetClass="mediacall" presetSubtype="0" fill="hold" nodeType="{type_noeud}">'
                f'<p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
                f'<p:cmd type="call" cmd="playFrom(0.0)"><p:cBhvr><p:cTn id="{ident()}" dur="{dur}" fill="hold"/>'
                f'<p:tgtEl><p:spTgt spid="{shape.shape_id}"/></p:tgtEl></p:cBhvr></p:cmd></p:childTnLst></p:cTn></p:par>')

    def ecrire(self):
        if not self.medias and not any(self.groupes.values()):
            return
        compteur = iter(range(3, 100000))
        ident = lambda: next(compteur)  # noqa: E731
        groupes_xml = []
        for g in sorted(self.groupes):
            effets = self.groupes[g]
            if g == 0 and not effets and not self.medias:
                continue
            if g > 0 and not effets:
                continue
            id_groupe = ident()
            id_creneau = ident()
            enfants = []
            premier = True
            if g == 0:
                for shape, dur, _b, _m in self.medias:
                    enfants.append(self._lecture(ident, shape, dur, "afterEffect" if premier else "withEffect"))
                    premier = False
            for shape, effet, debut, duree in sorted(effets, key=lambda e: e[2]):
                noeud = ("afterEffect" if g == 0 else "clickEffect") if premier else "withEffect"
                enfants.append(self._effet(ident, shape, effet, debut, duree, noeud))
                premier = False
            demarrage = '<p:cond delay="indefinite"/>' + ('<p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond>' if g == 0 else "")
            groupes_xml.append(
                f'<p:par><p:cTn id="{id_groupe}" fill="hold"><p:stCondLst>{demarrage}</p:stCondLst><p:childTnLst>'
                f'<p:par><p:cTn id="{id_creneau}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
                + "".join(enfants) + "</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>"
            )
        medias_xml = ""
        for shape, _dur, boucle, muet in self.medias:
            rep = ' repeatCount="indefinite"' if boucle else ""
            mute = ' mute="1"' if muet else ""
            medias_xml += (f'<p:video><p:cMediaNode vol="80000"{mute}><p:cTn id="{ident()}"{rep} fill="hold" display="0">'
                           f'<p:stCondLst><p:cond delay="indefinite"/></p:stCondLst></p:cTn>'
                           f'<p:tgtEl><p:spTgt spid="{shape.shape_id}"/></p:tgtEl></p:cMediaNode></p:video>')
        construits = []
        for g in self.groupes.values():
            for shape, *_ in g:
                if shape.shape_id not in construits and shape._element.tag == qn("p:sp"):
                    construits.append(shape.shape_id)
        bld = "".join(f'<p:bldP spid="{i}" grpId="0" animBg="1"/>' for i in construits)
        xml = (f'<p:timing xmlns:p="{P_NS}"><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
               f'<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
               + "".join(groupes_xml) +
               '</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
               '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
               + medias_xml + "</p:childTnLst></p:cTn></p:par></p:tnLst>"
               + (f"<p:bldLst>{bld}</p:bldLst>" if bld else "") + "</p:timing>")
        self.sl._element.append(etree.fromstring(xml))


def transition(sl, option="byObject", duree_ms=1400, avance_ms=None):
    """Morphose (repli Fondu), insérée juste après clrMapOvr ; avance automatique facultative."""
    av = f' advTm="{avance_ms}"' if avance_ms else ""
    xml = (f'<mc:AlternateContent xmlns:mc="{MC}" xmlns:p="{P_NS}">'
           f'<mc:Choice xmlns:p159="{P159}" Requires="p159"><p:transition xmlns:p14="{P14}" spd="slow" p14:dur="{duree_ms}"{av}>'
           f'<p159:morph option="{option}"/></p:transition></mc:Choice>'
           f'<mc:Fallback><p:transition spd="slow"{av}><p:fade/></p:transition></mc:Fallback></mc:AlternateContent>')
    el = etree.fromstring(xml)
    ancre = sl._element.find(qn("p:clrMapOvr"))
    if ancre is None:
        ancre = sl._element.find(qn("p:cSld"))
    ancre.addnext(el)


def notes(sl, s):
    tf = sl.notes_slide.notes_text_frame
    fond = f"\nFOND : {s['fond']}" if s.get("fond") else ""
    tf.text = (f"[{s['id']}] ÉPISODE {s.get('episode', 0)} · {s['partie'].upper()} — durée ≈ {s['duree_s']} s\n\n"
               f"CE QUE VOUS DITES / À SAVOIR :\n{s['notes']}\n\nVISUEL : {s['visuel']}\n\nANIMATION : {s['animation']}{fond}")


# ───────────────────────────────────────── calques de mouvement ─────────────────────────────────────────

COULEUR_FOND = {"noir": "noir", "terre": "terre", "bleu": "bleu", "bleu_nuit": "bleu_nuit"}
HALO_TEINTE = {"noir": "or", "terre": "terre", "bleu": "bleu", "bleu_nuit": "bleu"}


def calques(sl, s, idx, ch, halo_xy=(6.67, 3.75), halo_taille=9.0):
    teinte = s.get("teinte", "noir")
    f = sl.background.fill
    f.solid()
    f.fore_color.rgb = PAL[COULEUR_FOND.get(teinte, "noir")]
    couches = []
    if s.get("fond"):
        spec = C["fonds"][s["fond"]]
        if SOBRE:  # même décor, en image fixe : aucune vidéo à lire (PC modeste, public sensible au mouvement)
            couches.append(image(sl, "fond-image", RACINE / spec["apercu"], 0, 0, w=W, h=H, alt=""))
        else:
            mv = film(sl, "fond-video", spec["fichier"], spec["apercu"], alt="Fond animé décoratif")
            ch.media(mv, spec["duree_s"], boucle=spec["boucle"], muet=True)
            couches.append(mv)
    # Champ d'étoiles : la Morphose le déplace légèrement d'une slide à l'autre (parallaxe lente)
    dx = -1.6 + 0.55 * math.sin(idx * 0.55)
    dy = -0.95 + 0.4 * math.cos(idx * 0.42)
    couches.append(image(sl, "!!etoiles", ASSETS / "calques" / "etoiles.png", dx, dy, w=16.67, alt=""))
    hx, hy = halo_xy
    couches.append(image(sl, "!!halo", ASSETS / "calques" / f"halo-{HALO_TEINTE.get(teinte, 'or')}.png", hx - halo_taille / 2,
                         hy - halo_taille / 2, w=halo_taille, alt=""))
    couches.append(image(sl, "vignette", ASSETS / "calques" / "vignette.png", 0, 0, w=W, h=H, alt=""))
    au_fond(sl, couches)


def au_fond(sl, formes):
    """Place ces formes tout en bas de la pile (dans cet ordre) : le titre, créé en premier par la disposition,
    doit rester AU-DESSUS du fond vidéo, des étoiles, du halo et du vignettage."""
    arbre = sl.shapes._spTree
    for k, forme in enumerate(formes):
        arbre.remove(forme._element)
        arbre.insert(2 + k, forme._element)  # 0 = nvGrpSpPr, 1 = grpSpPr


_POIDS = {F_GRAS: True, F_TEXTE: False, F_NOIR: "noir"}


def verifier_slide(sl, ident):
    """Garde-fou : aucun groupe insécable (mot + espaces insécables) ne doit dépasser la largeur de sa zone,
    sinon PowerPoint couperait le mot en plein milieu ; aucune étiquette sans retour ne doit déborder."""
    emu = 914400
    for forme in sl.shapes:
        if not forme.has_text_frame or forme.width is None or forme.left is None:
            continue
        tf = forme.text_frame
        dispo = (forme.width - (tf.margin_left or 0) - (tf.margin_right or 0)) / emu
        if forme.left / emu > W or (forme.left + forme.width) / emu < 0:
            continue  # objet hors champ (carrousel, post-it) : non projeté tel quel
        for para in tf.paragraphs:
            ligne = 0.0
            for run in para.runs:
                if run.font.size is None:
                    continue
                pt, gras = run.font.size.pt, _POIDS.get(run.font.name, True)
                ligne += largeur_texte(run.text, pt, gras) / 1.06
                for bloc in run.text.split(" "):
                    if bloc and largeur_texte(bloc, pt, gras) / 1.06 * 1.02 > dispo:
                        AVERTISSEMENTS.append(f"[{ident}] « {bloc} » ({pt:.0f} pt) dépasse sa zone « {forme.name} » ({dispo:.2f} in)")
            if tf.word_wrap is False and ligne > dispo + 0.3:
                AVERTISSEMENTS.append(f"[{ident}] étiquette « {para.text} » plus large que « {forme.name} »")


def petit_logo(sl):
    image(sl, "!!logo", ASSETS / "embleme-fond-sombre.png", W - 1.35, H - 0.68, w=0.95,
          alt="Emblème YEBA FORMATIONS : trois pitons reliés en réseau")


def lignes(s, pt_max, largeur, hauteur):
    """Titre blanc + titre or : même corps, le plus grand possible sans jamais couper un mot."""
    lg = [s["titre"]] + ([s["titre_or"]] if s.get("titre_or") else [])
    return taille_qui_tient(lg, largeur, hauteur, pt_max, 40)


def titre_deux_tons(sl, ch, s, x, y, w, h, pt_max, align=PP_ALIGN.LEFT, debut=250, clic_or=None, ancre_bas=False):
    """Ligne blanche (espace réservé Titre) puis ligne or (zone séparée, animée après)."""
    pt = lignes(s, pt_max, w, h)
    h1 = hauteur_texte(s["titre"], pt, w)
    h2 = hauteur_texte(s["titre_or"], pt, w) if s.get("titre_or") else 0
    y0 = y + (h - h1 - h2) if ancre_bas else y + max(0, (h - h1 - h2) / 2)
    t1 = titre(sl, x, y0, w, h1, [[(s["titre"], pt, PAL["blanc"], F_GRAS)]], align=align, ancre=MSO_ANCHOR.BOTTOM)
    ch.entree(t1, "fondu_montant", debut, 700)
    if s.get("titre_or"):
        t2 = texte(sl, "titre-or", x, y0 + h1 - 0.06, w, h2, [[(s["titre_or"], pt, PAL["or"], F_GRAS)]], align=align)
        ch.entree(t2, "fondu_montant", 0 if clic_or else debut + 420, 700, clic=clic_or)
    return pt, y0 + h1 + h2


def titre_ligne(sl, ch, s, x, y, w, pt_max=54, debut=200):
    """Titre blanc + or sur UNE ligne (corps réduit jusqu'à tenir)."""
    txt = s["titre"] + " " + s.get("titre_or", "")
    pt = pt_max
    while pt > 36 and largeur_texte(typo(txt), pt) > w - 0.3:
        pt -= 2
    t = titre(sl, x, y, w, pt / 72 * 1.3, [[(s["titre"] + " ", pt, PAL["blanc"], F_GRAS), (s.get("titre_or", ""), pt, PAL["or"], F_GRAS)]])
    ch.entree(t, "fondu_montant", debut, 700)
    return pt


# ───────────────────────────────────────── gabarits ─────────────────────────────────────────

def g_video(sl, s, idx, ch):
    sl.background.fill.solid()
    sl.background.fill.fore_color.rgb = NOIR_PUR
    titre_cache(sl, s["titre"])
    spec = C["videos"][s["video"]]
    mv = film(sl, f"!!video-{s['id']}", spec["fichier"], spec["apercu"], alt=s["visuel"])
    ch.media(mv, spec["duree_s"], boucle=spec["boucle"], muet=False)


def g_cover(sl, s, idx, ch):
    calques(sl, s, idx, ch, (6.67, 1.9), 8.5)
    lw = 3.6
    logo = image(sl, "!!logo", ASSETS / "logo-yeba-fond-sombre.png", (W - lw) / 2, 0.3, w=lw,
                 alt="Logo YEBA FORMATIONS : trois pitons reliés en réseau, au-dessus du nom YEBA FORMATIONS")
    ch.entree(logo, "zoom", 0, 1100)
    k = texte(sl, "kicker", 0, 3.72, W, 0.5, [[(s["kicker"], 24, PAL["or"], F_GRAS, 500)]], align=PP_ALIGN.CENTER)
    ch.entree(k, "fondu", 700, 700)
    titre_deux_tons(sl, ch, s, 0.8, 4.2, W - 1.6, 1.85, 44, align=PP_ALIGN.CENTER, debut=1000)
    meta = f"{C['meta']['date']} · {C['meta']['lieu']} · La Réunion"
    m = texte(sl, "meta", 0, 6.3, W, 0.55, [[(meta, 24, PAL["gris"], F_TEXTE)]], align=PP_ALIGN.CENTER)
    ch.entree(m, "fondu", 1900, 800)


def g_statement(sl, s, idx, ch):
    calques(sl, s, idx, ch, (3.2, 3.9), 9.5)
    largeur = 10.8
    if s["id"] == "S22":
        ill = image(sl, "illustration", ASSETS / "illustrations" / "etoiles-ue.png", 10.4, 0.75, w=2.2,
                    alt="Cercle de douze points dorés évoquant le drapeau européen")
        ch.entree(ill, "zoom", 1300, 900)
        largeur = 9.3
    rect(sl, "!!barre", 0.45, 1.75, 0.12, 4.3, couleur=PAL["or"])
    k = texte(sl, "kicker", 0.95, 1.18, 8, 0.5, [[(s["kicker"], 24, PAL["or"], F_GRAS, 500)]])
    ch.entree(k, "fondu", 100, 600)
    clic = 1 if s.get("kicker") == "QUESTION" else None
    titre_deux_tons(sl, ch, s, 0.95, 1.85, largeur, 4.3, 64, debut=300, clic_or=clic)
    petit_logo(sl)


def g_agenda(sl, s, idx, ch):
    calques(sl, s, idx, ch, (10.6, 3.7), 8.0)
    a = s["agenda_actif"]
    titre(sl, M, 0.42, 8, 0.75, [[(s["titre"], 34, PAL["blanc"], F_GRAS)]], nom="!!titre")
    y0, pas = 1.38, 0.79
    for i, ep in enumerate(C["episodes"]):
        y = y0 + i * pas
        actif = i == a
        texte(sl, f"!!agn{i}", M + 0.35, y, 0.9, 0.7, [[(f"{i + 1:02d}", 28, PAL["or"] if actif else GRIS2, F_GRAS)]], ancre=MSO_ANCHOR.MIDDLE, retour=False)
        texte(sl, f"!!ag{i}", M + 1.25, y, 3.55, 0.7, [[(ep["titre"], 32 if actif else 28, PAL["blanc"] if actif else GRIS2, F_GRAS if actif else F_TEXTE)]],
              ancre=MSO_ANCHOR.MIDDLE, retour=False)
        texte(sl, f"!!ags{i}", M + 4.85, y, 4.45, 0.7, [[(ep["sujet"], 24, PAL["or"] if actif else GRIS2, F_TEXTE)]], ancre=MSO_ANCHOR.MIDDLE, retour=False)
        if largeur_texte(typo(ep["sujet"]), 24, False) > 4.35 or largeur_texte(typo(ep["titre"]), 32) > 3.45:
            AVERTISSEMENTS.append(f"agenda : « {ep['titre']} / {ep['sujet']} » trop long pour une ligne")
    rect(sl, "!!marqueur", M, y0 + a * pas + 0.08, 0.13, 0.54, couleur=PAL["or"])
    texte(sl, "!!agbig", 9.75, 1.35, 3.3, 4.2, [[(f"{a + 1:02d}", 150, PAL["or"], F_NOIR)]], align=PP_ALIGN.RIGHT, ancre=MSO_ANCHOR.MIDDLE, retour=False)
    petit_logo(sl)


def g_team(sl, s, idx, ch):
    calques(sl, s, idx, ch, (6.67, 4.2), 10)
    titre_ligne(sl, ch, s, M, 0.45, W - 2 * M)
    cw, gap, y = 3.85, 0.3, 1.7
    x0 = (W - (3 * cw + 2 * gap)) / 2
    pt = min(taille_qui_tient([c["nom"]], cw - 0.3, 1.1, 30, 24) for c in s["cartes"])
    for i, c in enumerate(s["cartes"]):
        x = x0 + i * (cw + gap)
        t0 = 600 + i * 180
        carte = rect(sl, f"carte{i}", x, y, cw, 4.85, couleur=PAL["blanc"], opacite=6, contour=PAL["or"], opacite_contour=55, ep=1.25,
                     forme=MSO_SHAPE.ROUNDED_RECTANGLE, arrondi=0.07)
        d = 1.8
        cercle = rect(sl, f"photo{i}", x + (cw - d) / 2, y + 0.35, d, d, couleur=PAL["bleu"], contour=PAL["or"], ep=3, forme=MSO_SHAPE.OVAL)
        texte_forme(cercle, [[(c["initiales"], 44, PAL["blanc"], F_GRAS)]])
        nom = texte(sl, f"nom{i}", x + 0.15, y + 2.25, cw - 0.3, 1.1, [[(c["nom"], pt, PAL["blanc"], F_GRAS)]], align=PP_ALIGN.CENTER, ancre=MSO_ANCHOR.MIDDLE)
        pt_r = taille_qui_tient([c["role"]], cw - 0.3, 1.3, 26, 24, gras=False)
        role = texte(sl, f"role{i}", x + 0.15, y + 3.4, cw - 0.3, 1.3, [[(c["role"], pt_r, PAL["gris"], F_TEXTE)]], align=PP_ALIGN.CENTER)
        for forme in (carte, cercle, nom, role):
            ch.entree(forme, "fondu_montant", t0, 750)
    petit_logo(sl)


def g_badges(sl, s, idx, ch):
    calques(sl, s, idx, ch, (6.67, 4.3), 10)
    titre_ligne(sl, ch, s, M, 0.45, W - 2 * M)
    bw, bh, gx, gy = 3.7, 1.75, 0.32, 0.42
    for i, item in enumerate(s["items"]):
        rang = i // 3
        n_rang = 3 if rang == 0 else len(s["items"]) - 3
        x0 = (W - (n_rang * bw + (n_rang - 1) * gx)) / 2
        x = x0 + (i % 3) * (bw + gx)
        y = 2.0 + rang * (bh + gy)
        b = rect(sl, f"badge{i}", x, y, bw, bh, couleur=PAL["blanc"], opacite=6, contour=PAL["or"], ep=2.25, forme=MSO_SHAPE.ROUNDED_RECTANGLE, arrondi=0.2)
        pt = taille_qui_tient([item], bw, bh - 0.1, 30, 24)
        texte_forme(b, [[(item, pt, PAL["blanc"], F_GRAS)]])
        ch.entree(b, "zoom", 500 + i * 140, 650)
    petit_logo(sl)


def g_word(sl, s, idx, ch):
    calques(sl, s, idx, ch, (6.67, 3.0), 10)
    titre(sl, 0.3, 0.7, W - 0.6, 4.3, [[(s["titre"], 250, PAL["or"], F_NOIR)]], align=PP_ALIGN.CENTER, ancre=MSO_ANCHOR.MIDDLE, nom="!!yeba")
    t = texte(sl, "traduction", 0.5, 5.15, W - 1, 0.9, [[(s["texte"], 36, PAL["blanc"], F_GRAS)]], align=PP_ALIGN.CENTER)
    ch.entree(t, "fondu_montant", 500, 800)
    petit_logo(sl)


def g_quote(sl, s, idx, ch):
    calques(sl, s, idx, ch, (2.2, 2.2), 8)
    g = texte(sl, "guillemets", 0.3, 0.2, 2.2, 2.2, [[("«", 200, RGBColor.from_string("5A4A22"), F_NOIR)]])
    ch.entree(g, "fondu", 0, 900)
    titre_deux_tons(sl, ch, s, 2.4, 1.85, 10.2, 4.4, 54, debut=400)
    petit_logo(sl)


def g_tree(sl, s, idx, ch):
    calques(sl, s, idx, ch, (6.67, 3.6), 9)
    # Le « Y » géant (340 pt) laisse 0,3 in de part et d'autre : les branches n'y touchent jamais.
    titre(sl, (W - 5) / 2, 0.5, 5, 6.3, [[(s["titre"], 340, PAL["or"], F_NOIR)]], align=PP_ALIGN.CENTER, ancre=MSO_ANCHOR.MIDDLE, nom="!!yeba")
    g, d = s["branches"]
    bw = 4.45
    xg, xd = 0.3, W - 0.3 - bw
    pt = min(taille_qui_tient([b_], bw, 1.9, 34, 26) for b_ in (g, d))
    bg = texte(sl, "branche-gauche", xg, 1.1, bw, 1.9, [[(g, pt, PAL["blanc"], F_GRAS)]], align=PP_ALIGN.RIGHT, ancre=MSO_ANCHOR.MIDDLE)
    bd = texte(sl, "branche-droite", xd, 1.1, bw, 1.9, [[(d, pt, PAL["blanc"], F_GRAS)]], align=PP_ALIGN.LEFT, ancre=MSO_ANCHOR.MIDDLE)
    sg = texte(sl, "sous-gauche", xg, 3.05, bw, 1.0, [[("Genèse · Savoir", 26, PAL["gris"], F_TEXTE)]], align=PP_ALIGN.RIGHT)
    sd = texte(sl, "sous-droite", xd, 3.05, bw, 1.0, [[("Afrique · Transmission", 26, PAL["gris"], F_TEXTE)]])
    for forme, t0 in ((bg, 500), (sg, 800), (bd, 1100), (sd, 1400)):
        ch.entree(forme, "fondu_montant", t0, 700)
    petit_logo(sl)


def g_baobab(sl, s, idx, ch):
    calques(sl, s, idx, ch, (3.3, 3.6), 8.5)
    titre_deux_tons(sl, ch, s, M, 1.6, 6.2, 3.0, 60, debut=1300, ancre_bas=True)
    mts = texte(sl, "mots", M, 4.85, 6.4, 0.8, [[(s["texte"], 28, PAL["gris"], F_TEXTE)]])
    ch.entree(mts, "fondu", 2500, 900)
    if not s.get("fond"):
        b = image(sl, "baobab", ASSETS / "illustrations" / "baobab-or.png", 7.6, 0.6, h=6.0, alt="Silhouette dorée d'un baobab")
        ch.entree(b, "balayage", 400, 1600)
    petit_logo(sl)


def g_split(sl, s, idx, ch):
    calques(sl, s, idx, ch, (3.3, 6.2), 8)
    rect(sl, "!!droite", W / 2, 0, W / 2, H, couleur=PAL["bleu"], opacite=88)
    t = titre(sl, 0, 0.45, W / 2, 1.0, [[(s["titre"], 50, PAL["blanc"], F_GRAS)]], align=PP_ALIGN.CENTER)
    ch.entree(t, "fondu_montant", 200, 700)
    t2 = texte(sl, "titre-droite", W / 2, 0.45, W / 2, 1.0, [[(s["titre_or"], 50, PAL["or"], F_GRAS)]], align=PP_ALIGN.CENTER)
    ch.entree(t2, "fondu_montant", 500, 700)
    for k, (cote, x) in enumerate((("gauche", 0), ("droite", W / 2))):
        bloc = s[cote]
        paras = [[(bloc["label"], 24, PAL["or"], F_GRAS, 600)]] + [[(m, 36, PAL["blanc"], F_GRAS)] for m in bloc["mots"]]
        col = texte(sl, f"mots-{cote}", x + 0.5, 1.75, W / 2 - 1, 3.3, paras, align=PP_ALIGN.CENTER, interligne=1.15)
        ch.entree(col, "fondu_montant", 900 + k * 350, 750)
    em = image(sl, "embleme", ASSETS / "embleme-fond-sombre.png", (W - 3.6) / 2, 5.35, w=3.6,
               alt="Emblème YEBA : trois pitons en réseau, à cheval entre héritage et modernité")
    ch.entree(em, "zoom", 1700, 900)


def g_values(sl, s, idx, ch):
    calques(sl, s, idx, ch, (1.6, 4.0), 8)
    t = titre(sl, M, 0.4, 8, 0.9, [[(s["titre"], 44, PAL["blanc"], F_GRAS)]])
    ch.entree(t, "fondu_montant", 150, 650)
    for i, v in enumerate(s["items"]):
        y = 1.45 + i * 1.08
        n = texte(sl, f"num{i}", M, y, 1.5, 0.95, [[(f"{i + 1:02d}", 48, PAL["or"], F_NOIR)]], ancre=MSO_ANCHOR.MIDDLE)
        val = texte(sl, f"val{i}", M + 1.7, y, 9.4, 0.95, [[(v, 40, PAL["blanc"], F_GRAS)]], ancre=MSO_ANCHOR.MIDDLE)
        ch.entree(n, "zoom", 0, 450, clic=i + 1)
        ch.entree(val, "fondu_montant", 120, 650, clic=i + 1)
    petit_logo(sl)


def g_timeline(sl, s, idx, ch):
    calques(sl, s, idx, ch, (6.67, 4.1), 10)
    t = titre(sl, M, 0.45, 8, 0.9, [[(s["titre"], 44, PAL["blanc"], F_GRAS)]])
    ch.entree(t, "fondu_montant", 150, 650)
    ly, bord = 3.9, 0.35
    ligne = rect(sl, "ligne", bord, ly, W - 2 * bord, 0.06, couleur=PAL["or"])
    ch.entree(ligne, "balayage", 500, 1500)
    n = len(s["etapes"])
    pas = (W - 2 * bord) / n
    # Même corps pour toutes les étapes ; « a · b · c » devient une petite liste verticale.
    listes = [[m.strip() for m in e["texte"].split("·")] for e in s["etapes"]]
    pt_e = min(taille_qui_tient(l_, pas - 0.1, 1.95, 28, 24, gras=False) for l_ in listes)
    pt_d = min(taille_qui_tient([e["date"]], pas - 0.1, 0.95, 36, 26) for e in s["etapes"])
    for i, e in enumerate(s["etapes"]):
        cx = bord + pas * (i + 0.5)
        dmt = 0.5 if i == n - 1 else 0.34
        t0 = 900 + i * 380
        j = rect(sl, f"jalon{i}", cx - dmt / 2, ly + 0.03 - dmt / 2, dmt, dmt, couleur=PAL["or"] if i < n - 1 else PAL["blanc"], forme=MSO_SHAPE.OVAL)
        dt = texte(sl, f"date{i}", cx - pas / 2 + 0.05, 2.5, pas - 0.1, 0.95, [[(e["date"], pt_d, PAL["or"], F_GRAS)]], align=PP_ALIGN.CENTER, ancre=MSO_ANCHOR.BOTTOM)
        et = texte(sl, f"etape{i}", cx - pas / 2 + 0.05, 4.45, pas - 0.1, 1.95, [[(m, pt_e, PAL["blanc"], F_TEXTE)] for m in listes[i]], align=PP_ALIGN.CENTER)
        ch.entree(j, "zoom", t0, 450)
        ch.entree(dt, "fondu_montant", t0 + 80, 600)
        ch.entree(et, "fondu", t0 + 200, 600)
    petit_logo(sl)


def g_pillars(sl, s, idx, ch):
    calques(sl, s, idx, ch, (6.67, 4.6), 10)
    titre_ligne(sl, ch, s, M, 0.45, W - 2 * M, 50)
    cw, gap, y = 3.7, 0.45, 2.0
    x0 = (W - (3 * cw + 2 * gap)) / 2
    pt = min(taille_qui_tient([it["titre"]], cw, 0.95, 44, 30) for it in s["items"])
    for i, it in enumerate(s["items"]):
        x = x0 + i * (cw + gap)
        t0 = 600 + i * 260
        fil = texte(sl, f"filigrane{i}", x, y - 0.3, cw, 1.8, [[(f"0{i + 1}", 110, RGBColor.from_string("2E2A20"), F_NOIR)]])
        vb = texte(sl, f"pilier{i}", x, y + 1.7, cw, 1.0, [[(it["titre"], pt, PAL["blanc"], F_GRAS)]])
        tr = rect(sl, f"trait{i}", x + 0.05, y + 2.82, 1.0, 0.08, couleur=PAL["or"])
        dt = texte(sl, f"detail{i}", x, y + 3.05, cw, 1.4, [[(it["texte"], taille_qui_tient([it["texte"]], cw, 1.4, 28, 24), PAL["or"], F_GRAS)]])
        ch.entree(fil, "fondu", t0, 700)
        ch.entree(vb, "fondu_montant", t0 + 100, 700)
        ch.entree(tr, "balayage", t0 + 300, 500)
        ch.entree(dt, "fondu", t0 + 400, 600)
    petit_logo(sl)


def g_offres(sl, s, idx, ch):
    calques(sl, s, idx, ch, (9.4, 2.4), 9)
    titre_ligne(sl, ch, s, M, 0.45, W - 2 * M, 54)
    items = s["items"]
    ligne1 = [(M, 1.85, 3.55), (M + 3.55 + 0.22, 1.85, 3.55), (M + 2 * (3.55 + 0.22), 1.85, W - 2 * M - 2 * (3.55 + 0.22))]
    l2 = (W - 2 * M - 0.22) / 2
    ligne2 = [(M, 4.3, l2), (M + l2 + 0.22, 4.3, l2)]
    for i, ((x, y, w), it) in enumerate(zip(ligne1 + ligne2, items)):
        phare = it.get("phare")
        tuile = rect(sl, f"offre{i}", x, y, w, 2.2, couleur=PAL["or"] if phare else PAL["blanc"], opacite=100 if phare else 7,
                     contour=None if phare else PAL["or"], opacite_contour=50, ep=1.25, forme=MSO_SHAPE.ROUNDED_RECTANGLE, arrondi=0.08)
        coul_t = PAL["noir"] if phare else PAL["blanc"]
        coul_s = PAL["noir"] if phare else PAL["or"]
        pt = taille_qui_tient([it["titre"]], w - 0.7, 1.1, 40, 28)
        texte_forme(tuile, [[(it["titre"], pt, coul_t, F_GRAS)], [(it["texte"], 26, coul_s, F_GRAS)]], align=PP_ALIGN.LEFT, marge=0.4)
        ch.entree(tuile, "fondu_montant", 600 + i * 140, 700)
    petit_logo(sl)


def _heure(h):
    hh, mm = h.split("h")
    return int(hh) + (int(mm) if mm else 0) / 60


def g_journee(sl, s, idx, ch):
    calques(sl, s, idx, ch, (2.0, 1.6), 7)
    hor = C["meta"]["horaires"]
    h0, h1 = _heure(hor["debut"]), _heure(hor["fin"])
    xh = lambda h: (260 + (h - h0) / (h1 - h0) * 1400) * PX  # noqa: E731  (même repère que la vidéo)
    ms = lambda h: int((16 + 140 * (h - h0) / (h1 - h0)) / 30 * 1000)  # noqa: E731  (passage du soleil)
    k = texte(sl, "kicker", M, 0.42, 7, 0.5, [[(s["kicker"], 24, PAL["or"], F_GRAS, 500)]])
    ch.entree(k, "fondu", 100, 600)
    lt = largeur_texte(typo(s["titre"]), 120, "noir") + 0.25
    t = titre(sl, 0.7, 0.72, lt, 1.65, [[(s["titre"], 120, PAL["or"], F_NOIR)]], ancre=MSO_ANCHOR.MIDDLE)
    t.text_frame.word_wrap = False
    ch.entree(t, "zoom", 300, 900)
    sous = texte(sl, "sous-titre", 0.75 + lt, 1.2, 5.4, 0.75, [[(s["texte"], 30, PAL["blanc"], F_GRAS)]], ancre=MSO_ANCHOR.MIDDLE, retour=False)
    ch.entree(sous, "fondu_montant", 700, 700)
    yb = 860 * PX
    hp0, hp1 = _heure(hor["pause_debut"]), _heure(hor["pause_fin"])
    if not s.get("fond"):
        # Sans fond : la frise de la vidéo, en formes (formation en or, pause en gris)
        rect(sl, "frise-matin", xh(h0), yb - 0.03, xh(hp0) - xh(h0), 0.06, couleur=PAL["or"])
        rect(sl, "frise-pause", xh(hp0) + 0.06, yb - 0.02, xh(hp1) - xh(hp0) - 0.12, 0.04, couleur=GRIS2)
        rect(sl, "frise-apres-midi", xh(hp1), yb - 0.03, xh(h1) - xh(hp1), 0.06, couleur=PAL["or"])
    for h in (hor["debut"], hor["pause_debut"], hor["pause_fin"], hor["fin"]):
        x = xh(_heure(h))
        # Les deux heures de la pause s'écartent de part et d'autre de leur repère (jamais collées).
        if h == hor["pause_debut"]:
            boite, al = (x - 1.6 + 0.3, 1.6), PP_ALIGN.RIGHT
        elif h == hor["pause_fin"]:
            boite, al = (x - 0.3, 1.6), PP_ALIGN.LEFT
        else:
            boite, al = (x - 0.8, 1.6), PP_ALIGN.CENTER
        lab = texte(sl, f"heure-{h}", boite[0], yb + 0.14, boite[1], 0.5, [[(h, 24, PAL["blanc"], F_GRAS)]], align=al, retour=False)
        ch.entree(lab, "fondu", ms(_heure(h)), 500)
    for seg in s["segments"]:
        a, b = _heure(seg["de"]), _heure(seg["a"])
        cx = (xh(a) + xh(b)) / 2
        lab = texte(sl, f"segment-{seg['de']}", cx - 1.3, yb - 0.72, 2.6, 0.5,
                    [[(seg["label"], 24, PAL["gris"] if seg.get("pause") else PAL["or"], F_GRAS)]], align=PP_ALIGN.CENTER, retour=False)
        ch.entree(lab, "fondu", ms((a + b) / 2), 600)
    men = texte(sl, "mention", M, 6.72, 9, 0.5, [[(s["mention"], 24, PAL["gris"], F_TEXTE)]])
    ch.entree(men, "fondu", 5200, 800)
    petit_logo(sl)


def g_confiance(sl, s, idx, ch):
    calques(sl, s, idx, ch, (9.7, 3.9), 9)
    titre_ligne(sl, ch, s, M, 0.45, W - 2 * M, 54)
    q, n = s["qualiopi"], s["nda"]
    pw, py, ph = 5.75, 1.9, 3.55
    panneaux = []
    for i, (bloc, lignes_bloc) in enumerate(((q, [(q["ligne1"], 30, PAL["blanc"], F_GRAS), (q["ligne2"], 24, PAL["gris"], F_TEXTE)]),
                                             (n, [(n["ligne1"], 26, PAL["blanc"], F_GRAS), (n["ligne2"], 24, PAL["gris"], F_TEXTE)]))):
        x = M if i == 0 else W - M - pw
        p = rect(sl, f"panneau{i}", x, py, pw, ph, couleur=PAL["bleu_nuit"], contour=PAL["or"], opacite_contour=60, ep=1.5,
                 forme=MSO_SHAPE.ROUNDED_RECTANGLE, arrondi=0.06)
        paras = [[(bloc["titre"], 60, PAL["or"], F_NOIR)]] + [[(t_, pt_, c_, f_)] for (t_, pt_, c_, f_) in lignes_bloc]
        texte_forme(p, paras, align=PP_ALIGN.LEFT, ancre=MSO_ANCHOR.MIDDLE, marge=0.45)
        ch.entree(p, "fondu_montant", 700 + i * 350, 800)
        panneaux.append(p)
    ban = rect(sl, "bandeau", M, 5.72, W - 2 * M, 0.85, couleur=PAL["bleu_nuit"], contour=PAL["or"], ep=1.5,
               forme=MSO_SHAPE.ROUNDED_RECTANGLE, arrondi=0.5)
    texte_forme(ban, [[("✓  ", 28, PAL["or"], F_GRAS), (s["texte"], 28, PAL["blanc"], F_GRAS)]])
    ch.entree(ban, "fondu_montant", 1600, 800)
    petit_logo(sl)


AVANTAGES = [s for s in C["slides"] if s["layout"] == "avantages"]


def corps_titre_texte(titre_txt, sous_txt, largeur, hauteur, titre_max=32, titre_min=26, sous_max=26, sous_min=24):
    """Corps (titre, sous-texte) les plus grands qui tiennent ENSEMBLE dans la zone (une seule zone de texte :
    le sous-texte suit le titre, ils ne peuvent pas se chevaucher)."""
    for pt1 in range(titre_max, titre_min - 1, -2):
        for pt2 in range(min(sous_max, pt1), sous_min - 1, -2):
            if _hauteur([titre_txt], pt1, largeur, 1.0, True) + _hauteur([sous_txt], pt2, largeur, 1.0, True) <= hauteur - 0.1:
                return pt1, pt2
    AVERTISSEMENTS.append(f"tuile trop pleine : {titre_txt} / {sous_txt}")
    return titre_min, sous_min


def _tuiles_avantages(sl, page, dx, ch=None):
    s = AVANTAGES[page]
    tw, th, gx, y = 3.7, 3.4, 0.32, 3.1
    x0 = (W - (3 * tw + 2 * gx)) / 2 + dx
    for i, it in enumerate(s["items"]):
        x = x0 + i * (tw + gx)
        base = f"!!av{page}-{i}"
        r = rect(sl, f"{base}-tuile", x, y, tw, th, couleur=PAL["blanc"], opacite=6, contour=PAL["or"], opacite_contour=55, ep=1.25,
                 forme=MSO_SHAPE.ROUNDED_RECTANGLE, arrondi=0.07)
        ic = image(sl, f"{base}-picto", ASSETS / "pictos" / f"{it['icone']}.png", x + 0.32, y + 0.28, w=0.95, alt="")
        zone_w, zone_h = tw - 0.5, th - 1.35 - 0.15
        pt1, pt2 = corps_titre_texte(it["titre"], it["texte"], zone_w, zone_h)
        t = texte(sl, f"{base}-texte", x + 0.25, y + 1.35, zone_w, zone_h,
                  [[(it["titre"], pt1, PAL["blanc"], F_GRAS)], [(it["texte"], pt2, PAL["or"], F_GRAS)]])
        if ch is not None:
            for forme in (r, ic, t):
                ch.entree(forme, "fondu_montant", 600 + i * 180, 700)


def g_avantages(sl, s, idx, ch):
    calques(sl, s, idx, ch, (6.67, 4.6), 10)
    page = AVANTAGES.index(s)
    if s.get("kicker"):
        k = texte(sl, "kicker", M, 0.42, 8, 0.5, [[(s["kicker"], 24, PAL["or"], F_GRAS, 500)]])
        if page == 0:
            ch.entree(k, "fondu", 100, 600)
    titre_deux_tons(sl, ch, s, M, 0.6, 11.5, 2.4, min(lignes(a_, 54, 11.5, 2.4) for a_ in AVANTAGES), debut=250)
    # Carrousel : la page voisine attend hors champ ; la Morphose fait glisser toute la rangée.
    _tuiles_avantages(sl, page, 0, ch if page == 0 else None)
    if page + 1 < len(AVANTAGES):
        _tuiles_avantages(sl, page + 1, W)
    if page > 0:
        _tuiles_avantages(sl, page - 1, -W)
    petit_logo(sl)


ATELIER = next(s for s in C["slides"] if s["layout"] == "atelier")
COUL_FAMILLE = {f: RGBColor.from_string(c) for f, c in ATELIER["familles"].items()}


def _tuiles_atelier(sl, ch=None):
    tw, th, gx, gy = 2.95, 1.3, 0.17, 0.12
    x0, y0 = (W - (4 * tw + 3 * gx)) / 2, 1.5
    for i, it in enumerate(ATELIER["items"]):
        x, y = x0 + (i % 4) * (tw + gx), y0 + (i // 4) * (th + gy)
        coul = COUL_FAMILLE[it["famille"]]
        r = rect(sl, f"!!tuile-{it['ref']}", x, y, tw, th, couleur=PAL["blanc"], opacite=6, contour=coul, ep=2.25, tirets=bool(it.get("bientot")))
        haut = th - 0.42 if it.get("bientot") else th
        paras = [[(it["nom"], taille_qui_tient([it["nom"]], tw, haut, 24, 22), PAL["blanc"], F_GRAS)]]
        if it.get("bientot"):
            paras.append([("bientôt", 24, PAL["or"], F_GRAS)])
        t = texte(sl, f"!!nom-{it['ref']}", x, y, tw, th, paras, align=PP_ALIGN.CENTER, ancre=MSO_ANCHOR.MIDDLE)
        if ch is not None:
            ch.entree(r, "fondu", 500 + i * 70, 500)
            ch.entree(t, "fondu_montant", 540 + i * 70, 600)
    # Légende sur deux rangées (24 pt minimum : une rangée unique déborderait de la slide)
    familles = list(COUL_FAMILLE.items())
    for rang, groupe in enumerate((familles[:3], familles[3:])):
        x, y = x0, 5.72 + rang * 0.56
        for fam, coul in groupe:
            rect(sl, f"legende-{fam}", x, y + 0.13, 0.28, 0.28, couleur=coul)
            lw = largeur_texte(typo(fam), 24, False) + 0.15
            texte(sl, f"legende-txt-{fam}", x + 0.36, y, lw, 0.54, [[(fam, 24, PAL["blanc"], F_TEXTE)]], ancre=MSO_ANCHOR.MIDDLE, retour=False)
            x += 0.36 + lw + 0.4
        if x > W - 1.5:
            AVERTISSEMENTS.append("légende du catalogue trop large")


def g_atelier(sl, s, idx, ch, retour=False):
    calques(sl, s, idx, ch, (6.67, 4.0), 10)
    if retour:
        titre(sl, M, 0.4, W - 2 * M, 0.9, [[(s["titre"] + " ", 48, PAL["blanc"], F_GRAS), (s["titre_or"], 48, PAL["or"], F_GRAS)]], nom="!!titre-atelier")
    else:
        t = titre(sl, M, 0.4, W - 2 * M, 0.9, [[(s["titre"] + " ", 48, PAL["blanc"], F_GRAS), (s["titre_or"], 48, PAL["or"], F_GRAS)]], nom="!!titre-atelier")
        ch.entree(t, "fondu_montant", 150, 700)
    _tuiles_atelier(sl, None if retour else ch)
    petit_logo(sl)


FOCUS_PT = min(lignes(s_, 60, W - 4.1 - 1.3, 3.3) for s_ in C["slides"] if s_["layout"] == "focus")


def g_focus(sl, s, idx, ch):
    calques(sl, s, idx, ch, (2.05, 3.75), 8)
    item = next(i for i in ATELIER["items"] if i["ref"] == s["ref"])
    coul = COUL_FAMILLE[item["famille"]]
    bw = 4.1
    rect(sl, f"!!tuile-{s['ref']}", 0, 0, bw, H, couleur=coul)
    pt = taille_qui_tient([s["nom"]], 6.9, 1.7, 44, 28, gras="noir")
    code = texte(sl, f"!!nom-{s['ref']}", bw / 2 - 3.5, H / 2 - 0.85, 7.0, 1.7, [[(s["nom"], pt, PAL["noir"], F_NOIR)]], align=PP_ALIGN.CENTER, ancre=MSO_ANCHOR.MIDDLE)
    code.rotation = 270
    xc, wc = bw + 0.7, W - bw - 1.3
    # La famille est portée par la couleur de la bande (règle des 20 mots : pas de surtitre ici).
    titre_deux_tons(sl, ch, s, xc, 0.55, wc, 3.3, FOCUS_PT, debut=300)
    for i, p_ in enumerate(s["puces"]):
        pc = texte(sl, f"puce{i}", xc, 4.0 + i * 0.66, wc, 0.66, [[("— ", 32, PAL["or"], F_GRAS), (p_, 32, PAL["blanc"], F_GRAS)]], ancre=MSO_ANCHOR.MIDDLE)
        ch.entree(pc, "fondu_montant", 1150 + i * 200, 650)
    x = xc
    for i, c in enumerate(s["chips"]):
        cw = largeur_texte(typo(c), 24) + 0.5
        chip = rect(sl, f"pastille{i}", x, 6.05, cw, 0.68, contour=PAL["or"], ep=2, forme=MSO_SHAPE.ROUNDED_RECTANGLE, arrondi=0.5)
        texte_forme(chip, [[(c, 24, PAL["blanc"], F_GRAS)]])
        ch.entree(chip, "zoom", 1900 + i * 130, 500)
        x += cw + 0.25
    petit_logo(sl)


def g_demo(sl, s, idx, ch):
    calques(sl, s, idx, ch, (2.0, 1.6), 8)
    live = rect(sl, "live", M, 1.0, 3.6, 0.75, couleur=ROUGE_LIVE, forme=MSO_SHAPE.ROUNDED_RECTANGLE, arrondi=0.5)
    texte_forme(live, [[("●  " + s["kicker"], 26, PAL["blanc"], F_GRAS, 300)]])
    ch.entree(live, "zoom", 150, 600)
    titre_deux_tons(sl, ch, s, M, 2.1, W - 2 * M, 4.2, 72, debut=500)
    petit_logo(sl)


def g_bientot(sl, s, idx, ch):
    calques(sl, s, idx, ch, (10.6, 3.0), 9)
    k = texte(sl, "kicker", M, 0.5, 8, 0.5, [[(s["kicker"], 24, PAL["or"], F_GRAS, 600)]])
    ch.entree(k, "fondu", 100, 600)
    t = titre(sl, M, 0.95, 9, 1.6, [[(s["titre"], 88, PAL["blanc"], F_GRAS)]], ancre=MSO_ANCHOR.MIDDLE)
    ch.entree(t, "fondu_montant", 400, 900)
    n = len(s["items"])
    seule = n == 1  # une seule annonce confirmée : grande carte alignée sur le titre
    cw, gap, y, ch_ = (6.4, 0, 3.2, 2.6) if seule else (3.7, 0.32, 3.2, 2.5)
    x0 = M if seule else (W - (n * cw + (n - 1) * gap)) / 2
    a_confirmer = []
    for i, it in enumerate(s["items"]):
        x = x0 + i * (cw + gap)
        carte = rect(sl, f"carte{i}", x, y, cw, ch_, couleur=PAL["blanc"], opacite=6, contour=PAL["or"], opacite_contour=55, ep=1.25,
                     forme=MSO_SHAPE.ROUNDED_RECTANGLE, arrondi=0.08)
        pt1, pt2 = corps_titre_texte(it["titre"], it["texte"], cw - 0.7, ch_ - 0.6, 48 if seule else 32, 26, 30 if seule else 24, 24)
        texte_forme(carte, [[(it["titre"], pt1, PAL["blanc"], F_GRAS)], [(it["texte"], pt2, PAL["or"], F_GRAS)]],
                    align=PP_ALIGN.LEFT, marge=0.35)
        ch.entree(carte, "fondu_montant", 900 + i * 220, 700)
        if it.get("statut") == "a_confirmer":
            a_confirmer.append(it["titre"])
    if a_confirmer:
        note_hors_champ(sl, "À CONFIRMER AVANT PROJECTION :\n" + "\n".join(f"• {t_}" for t_ in a_confirmer) + "\n(feuille de route « Prévu »)")
    petit_logo(sl)


GABARITS = {
    "video": g_video, "cover": g_cover, "statement": g_statement, "agenda": g_agenda, "team": g_team, "badges": g_badges,
    "word": g_word, "quote": g_quote, "tree": g_tree, "baobab": g_baobab, "split": g_split, "values": g_values,
    "timeline": g_timeline, "pillars": g_pillars, "offres": g_offres, "journee": g_journee, "confiance": g_confiance,
    "avantages": g_avantages, "atelier": g_atelier, "focus": g_focus, "demo": g_demo, "bientot": g_bientot,
}


def sequence():
    """Liste ordonnée des slides : un « retour à la carte » est inséré entre deux fiches formation (zoom arrière / zoom avant)."""
    sortie = []
    slides = C["slides"]
    for i, s in enumerate(slides):
        sortie.append((s, False))
        suivant = slides[i + 1] if i + 1 < len(slides) else None
        if s["layout"] == "focus" and suivant and suivant["layout"] == "focus":
            retour = dict(ATELIER)
            retour.update({"id": s["id"] + "-carte", "duree_s": 3, "fond": ATELIER.get("fond"),
                           "notes": "Retour à la carte du catalogue : zoom arrière, puis zoom avant sur la formation suivante.",
                           "visuel": "La fiche se replie dans sa tuile.", "animation": "Morphose (zoom arrière)."})
            sortie.append((retour, True))
    return sortie


def construire(sortie):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    prs.core_properties.title = C["meta"]["titre"]
    prs.core_properties.author = "YEBA FORMATIONS"
    prs.core_properties.language = "fr-FR"
    prs.core_properties.subject = "Saison 1 — épisodes 1 à 4 (présentation, histoire, offre, formations) + générique"
    precedent = None
    for idx, (s, retour) in enumerate(sequence()):
        sl = prs.slides.add_slide(prs.slide_layouts[5])  # « Titre seul » : un vrai titre par slide
        ch = Chrono(sl)
        if retour:
            g_atelier(sl, s, idx, ch, retour=True)
        else:
            GABARITS[s["layout"]](sl, s, idx, ch)
        ch.ecrire()
        verifier_slide(sl, s["id"])
        if s["layout"] == "video":
            spec = C["videos"][s["video"]]
            avance = int(spec["duree_s"] * 1000) + 150 if s.get("avance") else None
            transition(sl, "byObject", 900, avance)
        else:
            option = "byChar" if (precedent == "word" and s["layout"] == "tree") else "byObject"
            transition(sl, option, 1200 if s["layout"] in ("agenda", "atelier") else 1500)
        notes(sl, s)
        if s.get("cache"):
            sl._element.set("show", "0")
        precedent = s["layout"]
    prs.save(sortie)
    return len(prs.slides)


if __name__ == "__main__":
    DIST.mkdir(exist_ok=True)
    nom = ("YEBA_Soiree_Lancement_IMAGES.pptx" if IMAGES else
           "YEBA_Soiree_Lancement_SOBRE.pptx" if SOBRE else "YEBA_Soiree_Lancement.pptx")
    out = DIST / nom
    n = construire(out)
    print(f"OK : {out} ({n} slides, {out.stat().st_size / 1e6:.1f} Mo)")
    for a in dict.fromkeys(AVERTISSEMENTS):
        print("  ⚠", a)
    if AVERTISSEMENTS:
        sys.exit(2)
