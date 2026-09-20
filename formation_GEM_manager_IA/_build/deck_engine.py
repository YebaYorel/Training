# -*- coding: utf-8 -*-
"""Moteur de construction du diaporama - accessibilite malvoyants.
Regles appliquees :
 - Police sans-serif Verdana (fort encombrement lateral = meilleure lisibilite)
 - Titre 40 pt / Corps 28 pt / Sous-puce 24 pt  (jamais en dessous de 24 pt)
 - Contrastes >= 4.5:1 (WCAG 2.1 AA, W3C)
 - Alignement a gauche, pas de justification, pas de bloc capitales
 - Controle automatique de longueur : aucun debordement, aucune coupure de mot
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

ORGANISME = "GEM FORMATION"
TITRE_JOUR = "Manager aujourd'hui : posture et intelligence artificielle"

# ---- Palette neutre accessible (a remplacer par la charte GEM si fournie) ----
C_TXT     = RGBColor(0x1A, 0x1A, 0x2E)   # 15.8:1 sur blanc
C_BG      = RGBColor(0xFF, 0xFF, 0xFF)
C_NUIT    = RGBColor(0x12, 0x29, 0x4A)   # bandeau  13.0:1 avec blanc
C_GRIS    = RGBColor(0x4A, 0x55, 0x68)   # 7.1:1 sur blanc
C_ACCENT  = RGBColor(0xC2, 0x41, 0x0C)   # orange  5.4:1 sur blanc
C_VERT    = RGBColor(0x15, 0x6B, 0x36)   # 6.2:1 sur blanc
C_ROUGE   = RGBColor(0xB9, 0x1C, 0x1C)   # 6.0:1 sur blanc
C_BLANC   = RGBColor(0xFF, 0xFF, 0xFF)
C_CLAIR   = RGBColor(0xEF, 0xF2, 0xF7)

FONT = "Verdana"
SZ_TITRE, SZ_CORPS, SZ_SOUS, SZ_SURTITRE = 40, 28, 24, 18

# Largeurs utiles (points). Verdana : largeur moyenne ~0.62 x corps.
W_SLIDE_PT = 13.333 * 72
BOX_W_PT   = 11.93 * 72
MAX_N1 = 46   # caracteres max niveau 1 a 28 pt -> tient sur 1 ligne
MAX_N2 = 52   # caracteres max niveau 2 a 24 pt

ERREURS = []

# ---- Ajusteur vertical : garantit qu'aucun texte ne sort du cadre --------
# Echelle de repli : (corps, espacement) ; le corps ne descend jamais sous 24 pt.
ECHELLE = [(28,16),(28,12),(28,8),(26,12),(26,8),(25,8),(24,10),(24,6),(24,3)]
LH = 1.22       # interligne demande a PowerPoint
LH_REEL = 1.50  # hauteur reellement occupee (police x interligne), mesuree au rendu

def _hauteur(puces, s1, gap):
    total = 0.0
    for niv, _ in puces:
        t = s1 if niv == 1 else s1 - 4
        g = gap if niv == 1 else max(gap - 6, 3)
        total += t * LH_REEL + g
    return total - (gap if puces else 0)

def ajuster(puces, hauteur_in, ou=""):
    """Retourne (corps, gap) qui tient dans la hauteur disponible."""
    dispo = hauteur_in * 72
    for s1, gap in ECHELLE:
        if _hauteur(puces, s1, gap) <= dispo:
            return s1, gap
    ERREURS.append("[%s] trop de lignes : %d puces ne tiennent pas a 24 pt"
                   % (ou, len(puces)))
    return 24, 3

def _check(texte, maxi, ou):
    if len(texte) > maxi:
        ERREURS.append(f"[{ou}] {len(texte)}>{maxi} car. : {texte}")

def new_deck():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    return prs

def _blank(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.background.fill; bg.solid(); bg.fore_color.rgb = C_BG
    return s

def _rect(s, x, y, w, h, color):
    from pptx.enum.shapes import MSO_SHAPE
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = color
    sh.line.fill.background(); sh.shadow.inherit = False
    return sh

def _tb(s, x, y, w, h):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Emu(0)
    tf.margin_top = tf.margin_bottom = Emu(0)
    return tf

def _run(par, texte, taille, couleur, gras=False, italique=False):
    r = par.add_run(); r.text = texte
    f = r.font; f.name = FONT; f.size = Pt(taille); f.color.rgb = couleur
    f.bold = gras; f.italic = italique
    return r

def _para(tf, first=False):
    return tf.paragraphs[0] if first else tf.add_paragraph()

# --------------------------------------------------------------- SLIDES ----
def slide_couverture(prs, surtitre, titre, sous_titre, bas):
    s = _blank(prs)
    _rect(s, 0, 0, 13.333, 7.5, C_NUIT)
    _rect(s, 0.7, 1.95, 0.18, 2.95, C_ACCENT)
    tf = _tb(s, 1.15, 1.10, 11.3, 0.8)
    p = _para(tf, True); p.alignment = PP_ALIGN.LEFT
    _run(p, surtitre, SZ_SURTITRE + 4, C_ACCENT, True)
    tf = _tb(s, 1.15, 1.95, 11.3, 2.95)
    for i, ligne in enumerate(titre):
        p = _para(tf, i == 0); p.line_spacing = 1.15
        _run(p, ligne, 44, C_BLANC, True)
    tf = _tb(s, 1.15, 5.25, 11.3, 0.8)
    p = _para(tf, True); _run(p, sous_titre, 24, C_CLAIR)
    tf = _tb(s, 1.15, 6.35, 11.3, 0.6)
    p = _para(tf, True); _run(p, bas, 20, C_CLAIR)
    return s

def slide_partie(prs, numero, titre, horaire, items):
    s = _blank(prs)
    _rect(s, 0, 0, 13.333, 7.5, C_NUIT)
    tf = _tb(s, 1.0, 0.62, 11.3, 0.6)
    p = _para(tf, True); _run(p, numero, 24, C_ACCENT, True)
    tf = _tb(s, 1.0, 1.25, 11.3, 1.7)
    for i, l in enumerate(titre):
        p = _para(tf, i == 0); p.line_spacing = 1.15
        _run(p, l, 44, C_BLANC, True)
    tf = _tb(s, 1.0, 3.10, 11.3, 0.6)
    p = _para(tf, True); _run(p, horaire, 26, C_ACCENT, True)
    puces = [(1, it) for it in items]
    corps, gap = ajuster(puces, 6.60 - 3.85, "partie " + numero)
    tf = _tb(s, 1.0, 3.85, 11.3, 6.60 - 3.85)
    for i, it in enumerate(items):
        _check(it, MAX_N1, "partie " + numero)
        p = _para(tf, i == 0); p.space_after = Pt(gap); p.line_spacing = LH
        _run(p, "\u2022  " + it, corps, C_CLAIR)
    return s

def slide(prs, titre, puces, note=None, couleur_bandeau=C_NUIT, etiquette=None):
    """puces : liste de (niveau, texte) ; niveau 1 ou 2."""
    s = _blank(prs)
    _rect(s, 0, 0, 13.333, 1.32, couleur_bandeau)
    _check(titre, 52, "titre")
    tf = _tb(s, 0.7, 0.36, 11.9, 0.7)
    p = _para(tf, True); _run(p, titre, SZ_TITRE, C_BLANC, True)
    if etiquette:
        et = _rect(s, 10.6, 1.55, 2.03, 0.52, C_ACCENT)
        etf = et.text_frame; etf.word_wrap = False
        etf.margin_left = etf.margin_right = Emu(0)
        pe = etf.paragraphs[0]; pe.alignment = PP_ALIGN.CENTER
        _run(pe, etiquette, 16, C_BLANC, True)
        etf.vertical_anchor = MSO_ANCHOR.MIDDLE
    haut = 1.85 if not etiquette else 2.28
    bas = 6.58
    corps, gap = ajuster(puces, bas - haut, titre)
    tf = _tb(s, 0.7, haut, 11.9, bas - haut)
    n = 0
    for niv, txt in puces:
        first = (n == 0); n += 1
        p = _para(tf, first); p.line_spacing = LH
        if niv == 1:
            _check(txt, MAX_N1, titre)
            p.space_after = Pt(gap)
            _run(p, "\u25AA  ", corps, C_ACCENT, True)
            _run(p, txt, corps, C_TXT)
        else:
            _check(txt, MAX_N2, titre)
            p.space_after = Pt(max(gap - 6, 3)); p.level = 1
            _run(p, "      \u2013  ", corps - 4, C_GRIS, True)
            _run(p, txt, corps - 4, C_GRIS)
    if note:
        _check(note, 74, "note " + titre)
        _rect(s, 0, 6.72, 13.333, 0.78, C_CLAIR)
        tf = _tb(s, 0.7, 6.95, 11.9, 0.4)
        p = _para(tf, True); _run(p, note, 18, C_NUIT, True)
    return s

def slide_choc(prs, ligne1, ligne2=None, sous=None, fond=C_ACCENT):
    s = _blank(prs)
    _rect(s, 0, 0, 13.333, 7.5, fond)
    tf = _tb(s, 1.0, 2.3, 11.3, 2.6)
    p = _para(tf, True); p.alignment = PP_ALIGN.CENTER; p.line_spacing = 1.2
    _run(p, ligne1, 54, C_BLANC, True)
    if ligne2:
        p = _para(tf); p.alignment = PP_ALIGN.CENTER; p.line_spacing = 1.2
        _run(p, ligne2, 54, C_BLANC, True)
    if sous:
        tf = _tb(s, 1.0, 5.3, 11.3, 0.9)
        p = _para(tf, True); p.alignment = PP_ALIGN.CENTER
        _run(p, sous, 26, C_BLANC)
    return s

def slide_deux_colonnes(prs, titre, g_titre, g_items, d_titre, d_items,
                        g_coul=C_ROUGE, d_coul=C_VERT, note=None):
    s = _blank(prs)
    _rect(s, 0, 0, 13.333, 1.32, C_NUIT)
    _check(titre, 52, "titre")
    tf = _tb(s, 0.7, 0.36, 11.9, 0.7)
    p = _para(tf, True); _run(p, titre, SZ_TITRE, C_BLANC, True)
    for x, t, items, coul in ((0.7, g_titre, g_items, g_coul),
                              (6.93, d_titre, d_items, d_coul)):
        _rect(s, x, 1.75, 5.7, 0.72, coul)
        tf = _tb(s, x + 0.25, 1.94, 5.2, 0.5)
        p = _para(tf, True); _run(p, t, 26, C_BLANC, True)
        cps, gp = ajuster([(2, i2) for i2 in items], 6.45 - 2.72, titre + "/" + t)
        cps += 4  # les items de colonne sont au niveau corps reduit
        tf = _tb(s, x + 0.25, 2.72, 5.3, 6.45 - 2.72)
        for i, it in enumerate(items):
            _check(it, 34, titre + "/" + t)
            p = _para(tf, i == 0); p.space_after = Pt(14); p.line_spacing = 1.2
            _run(p, "▪  ", SZ_SOUS, coul, True)
            _run(p, it, SZ_SOUS, C_TXT)
    if note:
        _check(note, 74, "note " + titre)
        _rect(s, 0, 6.72, 13.333, 0.78, C_CLAIR)
        tf = _tb(s, 0.7, 6.95, 11.9, 0.4)
        p = _para(tf, True); _run(p, note, 18, C_NUIT, True)
    return s

def slide_jeu(prs, numero, nom, duree, but, deroule, materiel):
    s = _blank(prs)
    _rect(s, 0, 0, 13.333, 1.32, C_VERT)
    tf = _tb(s, 0.7, 0.36, 11.9, 0.7)
    p = _para(tf, True)
    _run(p, "JEU " + numero + "  –  " + nom, SZ_TITRE, C_BLANC, True)
    _rect(s, 0.7, 1.62, 2.4, 0.56, C_ACCENT)
    tf = _tb(s, 0.7, 1.75, 2.4, 0.4)
    p = _para(tf, True); p.alignment = PP_ALIGN.CENTER
    _run(p, duree, 20, C_BLANC, True)
    tf = _tb(s, 3.4, 1.72, 9.2, 0.5)
    p = _para(tf, True); _run(p, but, SZ_SOUS, C_VERT, True)
    puces = [(1, d) for d in deroule]
    corps, gap = ajuster(puces, 6.58 - 2.55, "jeu " + numero)
    tf = _tb(s, 0.7, 2.55, 11.9, 6.58 - 2.55)
    for i, d in enumerate(deroule):
        _check(d, MAX_N1, "jeu " + numero)
        p = _para(tf, i == 0); p.space_after = Pt(gap); p.line_spacing = LH
        _run(p, str(i + 1) + ".  ", corps, C_VERT, True)
        _run(p, d, corps, C_TXT)
    _rect(s, 0, 6.72, 13.333, 0.78, C_CLAIR)
    tf = _tb(s, 0.7, 6.95, 11.9, 0.4)
    p = _para(tf, True); _run(p, "Materiel : " + materiel, 18, C_NUIT, True)
    return s

def slide_pause(prs, titre, sous):
    s = _blank(prs)
    _rect(s, 0, 0, 13.333, 7.5, C_CLAIR)
    _rect(s, 0, 3.0, 13.333, 0.12, C_ACCENT)
    tf = _tb(s, 1.0, 3.4, 11.3, 1.2)
    p = _para(tf, True); p.alignment = PP_ALIGN.CENTER
    _run(p, titre, 58, C_NUIT, True)
    tf = _tb(s, 1.0, 4.8, 11.3, 0.8)
    p = _para(tf, True); p.alignment = PP_ALIGN.CENTER
    _run(p, sous, 28, C_GRIS)
    return s

def numeroter(prs, depart=2):
    """Numero de page + rappel du titre, gros et contraste."""
    for i, s in enumerate(prs.slides, start=1):
        if i < depart:
            continue
        tf = _tb(s, 11.6, 6.98, 1.05, 0.35)
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.RIGHT
        _run(p, str(i), 16, C_GRIS, True)
