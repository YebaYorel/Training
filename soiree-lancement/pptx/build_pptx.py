"""Génère le PowerPoint de la soirée de lancement YEBA FORMATIONS (python-pptx).

Source unique : ../contenu/slides.json — modifier le JSON puis relancer :
    python pptx/build_pptx.py

Ce que fait le script :
  - 16:9, fond sombre, texte blanc, accent or (charte YEBA, contrastes WCAG vérifiés)
  - Montserrat (police du logo) ; tailles de texte auto-ajustées pour ne jamais déborder
  - Transition « Morphose » injectée directement dans le XML de chaque slide
    (repli automatique en « Fondu » sur les versions de PowerPoint sans Morphose)
  - Objets persistants nommés « !!xxx » : PowerPoint les apparie d'une slide à l'autre
  - Notes de l'orateur : durée, visuel, animation, texte à dire, alertes RGPD / IA Act
  - Texte alternatif sur les images et langue fr-FR (lecteurs d'écran, accessibilité)
  - Slides des parties « à construire » masquées
"""
import json
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
CONTENU = json.loads((RACINE / "contenu" / "slides.json").read_text(encoding="utf-8"))
PAL = {k: RGBColor.from_string(v) for k, v in CONTENU["palette"].items()}
GRIS_FONCE = RGBColor.from_string("8C93A0")  # étapes inactives de l'agenda (contraste 5,9:1 sur noir)
CARTE = RGBColor.from_string("1C1C1C")
FILIGRANE = RGBColor.from_string("2A2A2A")
ROUGE_LIVE = RGBColor.from_string("E53935")

W, H = 13.333, 7.5
M = 0.8
F_TEXTE = "Montserrat"
F_GRAS = "Montserrat ExtraBold"
F_NOIR = "Montserrat Black"

# ---------------------------------------------------------------- utilitaires


_POLICES = {}


def largeur_texte(txt, pt, gras=True):
    """Largeur réelle (pouces) d'un texte, mesurée sur les glyphes Montserrat (+6 % de marge)."""
    from PIL import ImageFont
    fichier = ASSETS / "fonts" / ("Montserrat-800.ttf" if gras else "Montserrat-400.ttf")
    cle = (fichier, pt)
    if cle not in _POLICES:
        _POLICES[cle] = ImageFont.truetype(str(fichier), size=int(pt * 10))
    return _POLICES[cle].getlength(txt) / 10 / 72 * 1.06


def nb_lignes(txt, pt, largeur, gras=True):
    lignes, courant = 1, 0.0
    esp = largeur_texte(" ", pt, gras)
    for mot in txt.split(" "):
        l = largeur_texte(mot, pt, gras)
        if l > largeur:  # un mot seul ne tient pas : interdit (pas de césure)
            return 99
        if courant == 0:
            courant = l
        elif courant + esp + l <= largeur:
            courant += esp + l
        else:
            lignes += 1
            courant = l
    return lignes


def taille_qui_tient(paras, largeur, hauteur, pt_max, pt_min=28, interligne=1.12):
    """Plus grande taille (pt) pour que tous les paragraphes tiennent dans la boîte."""
    pt = pt_max
    while pt > pt_min:
        h = sum(nb_lignes(p, pt, largeur - 0.2) * pt * interligne / 72 for p in paras)
        if h <= hauteur - 0.15:
            return pt
        pt -= 2
    return pt_min


def fond(slide, couleur):
    f = slide.background.fill
    f.solid()
    f.fore_color.rgb = PAL[couleur] if isinstance(couleur, str) else couleur


def nommer(shape, nom):
    shape.name = nom
    return shape


def _run(p, texte, pt, couleur, police=F_GRAS, espacement=None):
    r = p.add_run()
    r.text = texte
    f = r.font
    f.size = Pt(pt)
    f.name = police
    f.color.rgb = couleur
    rpr = r._r.get_or_add_rPr()
    rpr.set("lang", "fr-FR")
    if espacement:
        rpr.set("spc", str(espacement))
    return r


def _prep_tf(tf, ancre):
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = ancre
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, Inches(0.05))


def texte(slide, nom, x, y, w, h, paras, align=PP_ALIGN.LEFT, ancre=MSO_ANCHOR.TOP, interligne=1.0):
    """paras : liste de paragraphes ; chaque paragraphe = liste de runs (texte, pt, couleur, police[, spc])."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    nommer(tb, nom)
    tf = tb.text_frame
    _prep_tf(tf, ancre)
    for i, runs in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = interligne
        for run in runs:
            _run(p, *run)
    return tb


def titre(slide, x, y, w, h, paras, align=PP_ALIGN.LEFT, ancre=MSO_ANCHOR.TOP, interligne=1.0):
    """Remplit l'espace réservé « Titre » (structure lue par les lecteurs d'écran)."""
    ph = slide.shapes.title
    nommer(ph, "!!titre")
    ph.left, ph.top, ph.width, ph.height = Inches(x), Inches(y), Inches(w), Inches(h)
    tf = ph.text_frame
    _prep_tf(tf, ancre)
    tf.text = ""
    for i, runs in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = interligne
        for run in runs:
            _run(p, *run)
    return ph


def rect(slide, nom, x, y, w, h, couleur=None, contour=None, ep=2.0, forme=MSO_SHAPE.RECTANGLE, arrondi=None):
    s = slide.shapes.add_shape(forme, Inches(x), Inches(y), Inches(w), Inches(h))
    nommer(s, nom)
    if couleur is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = couleur
    if contour is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = contour
        s.line.width = Pt(ep)
    s.shadow.inherit = False
    if arrondi is not None and forme == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = arrondi
    return s


def image(slide, nom, chemin, x, y, w=None, h=None, alt=""):
    pic = slide.shapes.add_picture(str(chemin), Inches(x), Inches(y),
                                   Inches(w) if w else None, Inches(h) if h else None)
    nommer(pic, nom)
    pic._element.nvPicPr.cNvPr.set("descr", alt)
    return pic


def texte_forme(forme, paras, align=PP_ALIGN.CENTER, ancre=MSO_ANCHOR.MIDDLE):
    tf = forme.text_frame
    _prep_tf(tf, ancre)
    for i, runs in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        for run in runs:
            _run(p, *run)


MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"
P159 = "http://schemas.microsoft.com/office/powerpoint/2015/09/main"


def morphose(slide, option="byObject", duree_ms=1500):
    """Injecte une transition Morphose (repli Fondu) dans le XML de la slide."""
    xml = (
        f'<mc:AlternateContent xmlns:mc="{MC}" xmlns:p="{P}">'
        f'<mc:Choice xmlns:p159="{P159}" Requires="p159">'
        f'<p:transition xmlns:p14="{P14}" spd="slow" p14:dur="{duree_ms}">'
        f'<p159:morph option="{option}"/></p:transition></mc:Choice>'
        f'<mc:Fallback><p:transition spd="slow"><p:fade/></p:transition></mc:Fallback>'
        f"</mc:AlternateContent>"
    )
    el = etree.fromstring(xml)
    sld = slide._element
    ancre = sld.find(qn("p:clrMapOvr"))
    if ancre is None:
        ancre = sld.find(qn("p:cSld"))
    ancre.addnext(el)


def notes(slide, s):
    tf = slide.notes_slide.notes_text_frame
    tf.text = (
        f"[{s['id']}] {s['partie'].upper()} — durée ≈ {s['duree_s']} s\n\n"
        f"CE QUE VOUS DITES / À SAVOIR :\n{s['notes']}\n\n"
        f"VISUEL : {s['visuel']}\n\n"
        f"ANIMATION : {s['animation']}"
    )


def petit_logo(slide):
    image(slide, "!!logo", ASSETS / "embleme-fond-sombre.png", W - 1.35, H - 0.68, w=0.95,
          alt="Emblème YEBA FORMATIONS : trois pitons reliés en réseau")


def une_ligne(s, pt_max, largeur):
    """Titre + titre_or sur une seule ligne, taille réduite jusqu'à tenir."""
    txt = s["titre"] + " " + s.get("titre_or", "")
    pt = pt_max
    while pt > 32 and largeur_texte(txt, pt) > largeur - 0.3:
        pt -= 2
    return [[(s["titre"] + " ", pt, PAL["blanc"], F_GRAS), (s.get("titre_or", ""), pt, PAL["or"], F_GRAS)]]


def deux_lignes(s, pt_max, largeur, hauteur, couleur1="blanc"):
    lignes = [s["titre"]] + ([s["titre_or"]] if s.get("titre_or") else [])
    pt = taille_qui_tient(lignes, largeur, hauteur, pt_max)
    paras = [[(s["titre"], pt, PAL[couleur1], F_GRAS)]]
    if s.get("titre_or"):
        paras.append([(s["titre_or"], pt, PAL["or"], F_GRAS)])
    return paras, pt


# ------------------------------------------------------------------ gabarits


def g_cover(sl, s):
    fond(sl, "noir")
    lw = 3.6
    image(sl, "!!logo", ASSETS / "logo-yeba-fond-sombre.png", (W - lw) / 2, 0.35, w=lw,
          alt="Logo YEBA FORMATIONS : trois pitons reliés en réseau, au-dessus du nom YEBA FORMATIONS")
    texte(sl, "kicker", 0, 3.75, W, 0.55, [[(s["kicker"], 24, PAL["or"], F_GRAS, 600)]], align=PP_ALIGN.CENTER)
    paras, _ = deux_lignes(s, 44, W - 1.6, 1.75)
    titre(sl, 0.8, 4.3, W - 1.6, 1.75, paras, align=PP_ALIGN.CENTER, ancre=MSO_ANCHOR.MIDDLE)
    meta = f"{CONTENU['meta']['date']} · {CONTENU['meta']['lieu']} · La Réunion"
    texte(sl, "meta", 0, 6.35, W, 0.6, [[(meta, 24, PAL["gris"], F_TEXTE)]], align=PP_ALIGN.CENTER)


def g_statement(sl, s):
    couleur = {"QUESTION": "bleu", "L'IMAGE À RETENIR": "bleu_nuit", "ET MAINTENANT": "bleu"}.get(s.get("kicker"), "noir")
    fond(sl, couleur)
    largeur = 10.8
    if s["id"] == "S19":
        image(sl, "illustration", ASSETS / "illustrations" / "etoiles-ue.png", 10.4, 0.7, w=2.2,
              alt="Cercle de douze points dorés évoquant le drapeau européen")
        largeur = 9.4
    if s["id"] == "S22":
        image(sl, "illustration", ASSETS / "illustrations" / "jauge-or.png", 8.6, 1.3, w=4.4,
              alt="Compte-tours doré, aiguille dans la zone haute")
        largeur = 7.6
    rect(sl, "!!barre", 0.45, 1.75, 0.14, 4.3, couleur=PAL["or"])
    texte(sl, "kicker", 0.95, 1.2, 8, 0.55, [[(s["kicker"], 24, PAL["or"], F_GRAS, 600)]])
    paras, _ = deux_lignes(s, 64, largeur, 4.4)
    titre(sl, 0.95, 1.85, largeur, 4.4, paras, ancre=MSO_ANCHOR.MIDDLE, interligne=1.05)
    petit_logo(sl)


def g_agenda(sl, s):
    fond(sl, "noir")
    actif = s["agenda_actif"]
    titre(sl, M, 0.45, 8, 0.8, [[(s["titre"], 36, PAL["blanc"], F_GRAS)]])
    y0, pas = 1.45, 0.8
    for i, item in enumerate(CONTENU["agenda"]):
        y = y0 + i * pas
        est_actif = i == actif
        coul = PAL["blanc"] if est_actif else GRIS_FONCE
        texte(sl, f"!!agn{i}", M + 0.35, y, 0.9, 0.7, [[(f"{i + 1:02d}", 28, PAL["or"] if est_actif else GRIS_FONCE, F_GRAS)]],
              ancre=MSO_ANCHOR.MIDDLE)
        texte(sl, f"!!ag{i}", M + 1.3, y, 6.3, 0.7, [[(item, 32 if est_actif else 28, coul, F_GRAS if est_actif else F_TEXTE)]],
              ancre=MSO_ANCHOR.MIDDLE)
    rect(sl, "!!marqueur", M, y0 + actif * pas + 0.08, 0.14, 0.54, couleur=PAL["or"])
    texte(sl, "!!agbig", 7.9, 1.4, 5.1, 4.2, [[(f"{actif + 1:02d}", 210, PAL["or"], F_NOIR)]],
          align=PP_ALIGN.RIGHT, ancre=MSO_ANCHOR.MIDDLE)
    petit_logo(sl)


def g_team(sl, s):
    fond(sl, "noir")
    titre(sl, M, 0.45, W - 2 * M, 1.0, une_ligne(s, 54, W - 2 * M))
    cw, gap, y = 3.6, 0.45, 1.85
    x0 = (W - (3 * cw + 2 * gap)) / 2
    for i, c in enumerate(s["cartes"]):
        x = x0 + i * (cw + gap)
        rect(sl, f"!!carte{i}", x, y, cw, 4.6, couleur=CARTE, contour=PAL["or"], ep=1.5,
             forme=MSO_SHAPE.ROUNDED_RECTANGLE, arrondi=0.06)
        d = 1.9
        cercle = rect(sl, f"!!photo{i}", x + (cw - d) / 2, y + 0.35, d, d, couleur=PAL["bleu"], contour=PAL["or"], ep=3,
                      forme=MSO_SHAPE.OVAL)
        texte_forme(cercle, [[(c["initiales"], 44, PAL["blanc"], F_GRAS)]])
        pt = taille_qui_tient([c["nom"]], cw - 0.3, 0.75, 30, 24)
        texte(sl, f"nom{i}", x + 0.15, y + 2.4, cw - 0.3, 0.8, [[(c["nom"], pt, PAL["blanc"], F_GRAS)]],
              align=PP_ALIGN.CENTER, ancre=MSO_ANCHOR.MIDDLE)
        texte(sl, f"role{i}", x + 0.15, y + 3.3, cw - 0.3, 1.2, [[(c["role"], 24, PAL["gris"], F_TEXTE)]], align=PP_ALIGN.CENTER)
    petit_logo(sl)


def g_badges(sl, s):
    fond(sl, "noir")
    titre(sl, M, 0.45, W - 2 * M, 1.0, une_ligne(s, 54, W - 2 * M))
    bw, bh, gx, gy, y0 = 3.65, 1.75, 0.35, 0.4, 2.0
    x0 = (W - (3 * bw + 2 * gx)) / 2
    for i, item in enumerate(s["items"]):
        x, y = x0 + (i % 3) * (bw + gx), y0 + (i // 3) * (bh + gy)
        b = rect(sl, f"!!badge{i}", x, y, bw, bh, couleur=CARTE, contour=PAL["or"], ep=2.5,
                 forme=MSO_SHAPE.ROUNDED_RECTANGLE, arrondi=0.18)
        pt = taille_qui_tient([item], bw - 0.4, bh - 0.2, 30, 22)
        texte_forme(b, [[(item, pt, PAL["blanc"], F_GRAS)]])
    petit_logo(sl)


def g_word(sl, s):
    fond(sl, "noir")
    titre(sl, 0.3, 0.7, W - 0.6, 4.3, [[(s["titre"], 250, PAL["or"], F_NOIR)]], align=PP_ALIGN.CENTER, ancre=MSO_ANCHOR.MIDDLE)
    # Le Y sera réutilisé à la slide suivante : même nom pour la Morphose par caractère
    sl.shapes.title.name = "!!yeba"
    texte(sl, "traduction", 0.5, 5.2, W - 1, 0.9, [[(s["texte"], 36, PAL["blanc"], F_GRAS)]], align=PP_ALIGN.CENTER)
    petit_logo(sl)


def g_quote(sl, s):
    fond(sl, "noir")
    texte(sl, "guillemets", 0.3, 0.2, 2.2, 2.2, [[("«", 200, RGBColor.from_string("4A3F22"), F_NOIR)]])
    paras, _ = deux_lignes(s, 54, 10.2, 4.4)
    titre(sl, 2.4, 1.9, 10.2, 4.4, paras, ancre=MSO_ANCHOR.MIDDLE, interligne=1.05)
    petit_logo(sl)


def g_tree(sl, s):
    fond(sl, "noir")
    titre(sl, (W - 5) / 2, 0.5, 5, 6.3, [[(s["titre"], 380, PAL["or"], F_NOIR)]], align=PP_ALIGN.CENTER, ancre=MSO_ANCHOR.MIDDLE)
    sl.shapes.title.name = "!!yeba"
    g, d = s["branches"]
    texte(sl, "branche-gauche", 0.6, 1.1, 3.9, 1.9, [[(g, 34, PAL["blanc"], F_GRAS)]], align=PP_ALIGN.RIGHT, ancre=MSO_ANCHOR.MIDDLE)
    texte(sl, "branche-droite", W - 4.5, 1.1, 3.9, 1.9, [[(d, 34, PAL["blanc"], F_GRAS)]], align=PP_ALIGN.LEFT, ancre=MSO_ANCHOR.MIDDLE)
    texte(sl, "sous-gauche", 0.6, 3.05, 3.9, 0.6, [[("Genèse · Savoir", 26, PAL["gris"], F_TEXTE)]], align=PP_ALIGN.RIGHT)
    texte(sl, "sous-droite", W - 4.5, 3.05, 3.9, 0.6, [[("Afrique · Transmission", 26, PAL["gris"], F_TEXTE)]])
    petit_logo(sl)


def g_baobab(sl, s):
    fond(sl, "noir")
    image(sl, "!!baobab", ASSETS / "illustrations" / "baobab-or.png", 6.6, 0.35, h=6.2,
          alt="Silhouette dorée d'un baobab, l'arbre à palabres")
    paras, pt = deux_lignes(s, 60, 6.2, 3.0)
    titre(sl, M, 1.7, 6.2, 3.0, paras, ancre=MSO_ANCHOR.BOTTOM)
    texte(sl, "mots", M, 4.9, 6.2, 1.2, [[(s["texte"], 28, PAL["gris"], F_TEXTE)]])
    petit_logo(sl)


def g_split(sl, s):
    fond(sl, "noir")
    rect(sl, "!!droite", W / 2, 0, W / 2, H, couleur=PAL["bleu"])
    titre(sl, 0, 0.45, W / 2, 1.0, [[(s["titre"], 50, PAL["blanc"], F_GRAS)]], align=PP_ALIGN.CENTER)
    texte(sl, "titre-droite", W / 2, 0.45, W / 2, 1.0, [[(s["titre_or"], 50, PAL["or"], F_GRAS)]], align=PP_ALIGN.CENTER)
    for cote, x in (("gauche", 0), ("droite", W / 2)):
        bloc = s[cote]
        paras = [[(bloc["label"], 24, PAL["or"], F_GRAS, 600)]] + [[(m, 36, PAL["blanc"], F_GRAS)] for m in bloc["mots"]]
        texte(sl, f"mots-{cote}", x + 0.5, 1.8, W / 2 - 1, 3.2, paras, align=PP_ALIGN.CENTER, interligne=1.15)
    image(sl, "!!embleme", ASSETS / "embleme-fond-sombre.png", (W - 3.6) / 2, 5.35, w=3.6,
          alt="Emblème YEBA : trois pitons reliés par un réseau, à cheval entre héritage et modernité")


def g_values(sl, s):
    fond(sl, "noir")
    titre(sl, M, 0.4, 8, 0.9, [[(s["titre"], 44, PAL["blanc"], F_GRAS)]])
    for i, v in enumerate(s["items"]):
        y = 1.45 + i * 1.08
        texte(sl, f"!!num{i}", M, y, 1.5, 0.95, [[(f"{i + 1:02d}", 48, PAL["or"], F_NOIR)]], ancre=MSO_ANCHOR.MIDDLE)
        texte(sl, f"!!val{i}", M + 1.7, y, 9.2, 0.95, [[(v, 40, PAL["blanc"], F_GRAS)]], ancre=MSO_ANCHOR.MIDDLE)
    petit_logo(sl)


def g_timeline(sl, s):
    fond(sl, "noir")
    titre(sl, M, 0.45, 8, 0.9, [[(s["titre"], 44, PAL["blanc"], F_GRAS)]])
    ly = 3.9
    rect(sl, "!!ligne", 0.9, ly, W - 1.8, 0.07, couleur=PAL["or"])
    n = len(s["etapes"])
    pas = (W - 1.8) / n
    for i, e in enumerate(s["etapes"]):
        cx = 0.9 + pas * (i + 0.5)
        d = 0.5 if i == n - 1 else 0.34
        rect(sl, f"!!jalon{i}", cx - d / 2, ly + 0.035 - d / 2, d, d, couleur=PAL["or"] if i < n - 1 else PAL["blanc"],
             forme=MSO_SHAPE.OVAL)
        pt = taille_qui_tient([e["date"]], pas - 0.2, 0.9, 36, 28)
        texte(sl, f"date{i}", cx - pas / 2 + 0.1, 2.55, pas - 0.2, 0.95, [[(e["date"], pt, PAL["or"], F_GRAS)]],
              align=PP_ALIGN.CENTER, ancre=MSO_ANCHOR.BOTTOM)
        texte(sl, f"etape{i}", cx - pas / 2 + 0.1, 4.45, pas - 0.2, 1.9, [[(e["texte"], 26, PAL["blanc"], F_TEXTE)]],
              align=PP_ALIGN.CENTER)
    petit_logo(sl)


def g_bignumber(sl, s):
    fond(sl, "noir")
    titre(sl, 0.4, 0.5, 7.4, 6.0, [[(s["titre"], 300, PAL["or"], F_NOIR)]], align=PP_ALIGN.CENTER, ancre=MSO_ANCHOR.MIDDLE)
    texte(sl, "explication", 7.9, 2.0, 4.8, 3.6,
          [[(s["texte"], 36, PAL["blanc"], F_GRAS)], [(" ", 18, PAL["blanc"], F_TEXTE)], [(s["texte_or"], 32, PAL["or"], F_GRAS)]],
          ancre=MSO_ANCHOR.MIDDLE)
    petit_logo(sl)


def g_pillars(sl, s):
    fond(sl, "noir")
    titre(sl, M, 0.45, W - 2 * M, 1.0, une_ligne(s, 50, W - 2 * M))
    cw, gap, y = 3.7, 0.45, 2.1
    x0 = (W - (3 * cw + 2 * gap)) / 2
    for i, it in enumerate(s["items"]):
        x = x0 + i * (cw + gap)
        texte(sl, f"!!filigrane{i}", x, y - 0.3, cw, 1.8, [[(f"0{i + 1}", 110, FILIGRANE, F_NOIR)]])
        pt = min(taille_qui_tient([p["titre"]], cw, 0.9, 42, 30) for p in s["items"])
        texte(sl, f"!!pilier{i}", x, y + 1.75, cw, 0.95, [[(it["titre"], pt, PAL["blanc"], F_GRAS)]])
        rect(sl, f"!!trait{i}", x + 0.05, y + 2.85, 1.0, 0.09, couleur=PAL["or"])
        texte(sl, f"detail{i}", x, y + 3.1, cw, 1.4, [[(it["texte"], 26, PAL["or"], F_GRAS)]])
    petit_logo(sl)


def g_formats(sl, s):
    fond(sl, "noir")
    titre(sl, M, 0.45, W - 2 * M, 1.0, une_ligne(s, 50, W - 2 * M))
    tot = W - 2 * M
    a, b = 5.0, tot - 5.0 - 0.3
    cases = [(M, 1.85, a), (M + a + 0.3, 1.85, b), (M, 4.3, b), (M + b + 0.3, 4.3, a)]
    ordre = ["Intra", "Séminaire", "Inter", "Sur-mesure"]
    items = {it["titre"]: it for it in s["items"]}
    for (x, y, w), cle in zip(cases, ordre):
        it = items[cle]
        or_ = cle == "Séminaire"
        c = rect(sl, f"!!format-{cle}", x, y, w, 2.2, couleur=PAL["or"] if or_ else PAL["bleu_nuit"],
                 forme=MSO_SHAPE.ROUNDED_RECTANGLE, arrondi=0.08)
        coul_t = PAL["noir"] if or_ else PAL["blanc"]
        coul_s = PAL["noir"] if or_ else PAL["or"]
        texte_forme(c, [[(it["titre"], 44, coul_t, F_GRAS)], [(it["texte"], 26, coul_s, F_GRAS)]],
                    align=PP_ALIGN.LEFT, ancre=MSO_ANCHOR.MIDDLE)
        c.text_frame.margin_left = Inches(0.4)
    petit_logo(sl)


FAMILLES_TXT = {"IA": "IA", "Web & com": "Web & com", "Gouvernance": "Gouvernance", "Humain": "Humain"}


def g_garage(sl, s):
    fond(sl, "noir")
    titre(sl, M, 0.35, 8, 0.9, [[(s["titre"], 44, PAL["blanc"], F_GRAS)]])
    tw, th, gx, gy = 2.8, 1.3, 0.24, 0.24
    x0, y0 = (W - (4 * tw + 3 * gx)) / 2, 1.45
    for i, it in enumerate(s["items"]):
        x, y = x0 + (i % 4) * (tw + gx), y0 + (i // 4) * (th + gy)
        coul = RGBColor.from_string(s["familles"][it["famille"]])
        rect(sl, f"!!tuile-{it['code']}", x, y, tw, th, couleur=CARTE, contour=coul, ep=2.5)
        pt = taille_qui_tient([it["code"]], tw - 0.3, th - 0.1, 26, 22)
        texte(sl, f"!!code-{it['code']}", x + 0.1, y, tw - 0.2, th, [[(it["code"], pt, PAL["blanc"], F_GRAS)]],
              align=PP_ALIGN.CENTER, ancre=MSO_ANCHOR.MIDDLE)
    # Légende des familles
    x = x0
    for fam, hexa in s["familles"].items():
        rect(sl, f"legende-{fam}", x, 6.3, 0.32, 0.32, couleur=RGBColor.from_string(hexa))
        lw = largeur_texte(fam, 24, False) + 0.3
        texte(sl, f"legende-txt-{fam}", x + 0.42, 6.12, lw, 0.65, [[(fam, 24, PAL["blanc"], F_TEXTE)]], ancre=MSO_ANCHOR.MIDDLE)
        x += 0.42 + lw + 0.35
    petit_logo(sl)


def g_focus(sl, s):
    fond(sl, "noir")
    garage = next(x for x in CONTENU["slides"] if x["layout"] == "garage")
    fam = next(it["famille"] for it in garage["items"] if it["code"] == s["code"])
    coul = RGBColor.from_string(garage["familles"][fam])
    bw = 4.1
    rect(sl, f"!!tuile-{s['code']}", 0, 0, bw, H, couleur=coul)
    pt = taille_qui_tient([s["code"]], 6.9, 1.2, 48, 32)
    code = texte(sl, f"!!code-{s['code']}", bw / 2 - 3.5, H / 2 - 0.65, 7.0, 1.3, [[(s["code"], pt, PAL["noir"], F_NOIR)]],
                 align=PP_ALIGN.CENTER, ancre=MSO_ANCHOR.MIDDLE)
    code.rotation = 270
    xc, wc = bw + 0.7, W - bw - 1.3
    texte(sl, "famille", xc, 0.55, wc, 0.6, [[(s["famille"].upper(), 24, PAL["or"], F_GRAS, 500)]])
    paras, _ = deux_lignes(s, 54, wc, 2.5)
    titre(sl, xc, 1.15, wc, 2.5, paras, ancre=MSO_ANCHOR.MIDDLE)
    for i, p in enumerate(s["puces"]):
        texte(sl, f"puce{i}", xc, 3.85 + i * 0.72, wc, 0.7, [[("— ", 32, PAL["or"], F_GRAS), (p, 32, PAL["blanc"], F_GRAS)]],
              ancre=MSO_ANCHOR.MIDDLE)
    x = xc
    for i, c in enumerate(s["chips"]):
        cw = largeur_texte(c, 24) + 0.5
        ch = rect(sl, f"chip{i}", x, 6.05, cw, 0.68, contour=PAL["or"], ep=2, forme=MSO_SHAPE.ROUNDED_RECTANGLE, arrondi=0.5)
        texte_forme(ch, [[(c, 24, PAL["blanc"], F_GRAS)]])
        x += cw + 0.25
    petit_logo(sl)


def g_demo(sl, s):
    fond(sl, "noir")
    live = rect(sl, "!!live", M, 1.0, 3.6, 0.75, couleur=ROUGE_LIVE, forme=MSO_SHAPE.ROUNDED_RECTANGLE, arrondi=0.5)
    texte_forme(live, [[("●  " + s["kicker"], 26, PAL["blanc"], F_GRAS, 300)]])
    paras, _ = deux_lignes(s, 72, W - 2 * M, 4.2)
    titre(sl, M, 2.1, W - 2 * M, 4.2, paras, ancre=MSO_ANCHOR.MIDDLE)
    petit_logo(sl)


def g_video(sl, s):
    """Vidéo plein écran (clips fournis) : lecture automatique réglée par la macro VBA."""
    fond(sl, "noir")
    ph = sl.shapes.title  # titre hors champ : lu par les lecteurs d'écran, invisible à l'écran
    ph.text = s["titre"]
    ph.left = ph.top = Inches(-3)
    ph.width = ph.height = Inches(1)
    film = sl.shapes.add_movie(str(RACINE / s["fichier"]), 0, 0, Inches(W), Inches(H),
                               poster_frame_image=str(RACINE / s["apercu"]), mime_type="video/mp4")
    nommer(film, f"!!video-{s['id']}")
    film._element.nvPicPr.cNvPr.set("descr", s["visuel"])


GABARITS = {
    "cover": g_cover, "statement": g_statement, "agenda": g_agenda, "team": g_team, "badges": g_badges,
    "word": g_word, "quote": g_quote, "tree": g_tree, "baobab": g_baobab, "split": g_split, "values": g_values,
    "timeline": g_timeline, "bignumber": g_bignumber, "pillars": g_pillars, "formats": g_formats,
    "garage": g_garage, "focus": g_focus, "demo": g_demo, "video": g_video,
}


def slide_video(prs, video, poster):
    """Slide 0 : vidéo d'intro Remotion (lecture automatique réglée par la macro VBA)."""
    sl = prs.slides.add_slide(prs.slide_layouts[5])
    fond(sl, "noir")
    sl.shapes.title.text = "YEBA FORMATIONS — introduction vidéo"
    sl.shapes.title.left = sl.shapes.title.top = Inches(-3)
    sl.shapes.title.width = sl.shapes.title.height = Inches(1)
    film = sl.shapes.add_movie(str(video), 0, 0, prs.slide_width, prs.slide_height,
                               poster_frame_image=str(poster), mime_type="video/mp4")
    nommer(film, "!!video-intro")
    sl.notes_slide.notes_text_frame.text = (
        "[S00] Vidéo d'introduction (Remotion, 10 s). Lancer en boucle pendant l'installation du public. "
        "La macro VBA « YebaAppliquerAnimations » la règle en lecture automatique.")
    return sl


def construire(sortie):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    prs.core_properties.title = CONTENU["meta"]["titre"]
    prs.core_properties.author = "YEBA FORMATIONS"
    prs.core_properties.language = "fr-FR"
    prs.core_properties.subject = "Soirée de lancement — présentation, histoire, offre, formations"

    video = DIST / "yeba-intro.mp4"
    poster = DIST / "yeba-intro-poster.png"
    if video.exists() and poster.exists():
        slide_video(prs, video, poster)

    precedent = None
    for s in CONTENU["slides"]:
        sl = prs.slides.add_slide(prs.slide_layouts[5])  # « Titre seul » : un vrai titre par slide
        GABARITS[s["layout"]](sl, s)
        option = "byChar" if (precedent == "word" and s["layout"] == "tree") else "byObject"
        morphose(sl, option=option, duree_ms=1200 if s["layout"] == "agenda" else 1500)
        notes(sl, s)
        if s.get("cache"):
            sl._element.set("show", "0")
        precedent = s["layout"]
    prs.save(sortie)
    return len(prs.slides)


if __name__ == "__main__":
    DIST.mkdir(exist_ok=True)
    out = DIST / "YEBA_Soiree_Lancement.pptx"
    n = construire(out)
    print(f"OK : {out} ({n} slides)")
