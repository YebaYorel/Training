"""Fabrique un PowerPoint accessible (malvoyance, dys, troubles de l'attention) à partir
d'une liste de diapositives décrites en données (voir contenus/jN.py).

Charte NEUTRE : ce TP MEM est animé pour un autre organisme de formation, donc
aucune mention de YEBA FORMATIONS (nom, logo, couleurs, métadonnées).
Les couleurs se changent en un seul endroit (PALETTE) si l'organisme fournit sa charte.
"""
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

PALETTE = {
    "fond": "102A33",      # pétrole très foncé
    "carte": "143640",     # pétrole moyen (cartes) : jaune 8,3:1, blanc 12,9:1
    "carte2": "22252E",    # ardoise (cartes alternées) : jaune 9,9:1
    "texte": "FFFFFF",     # blanc : contraste 14,6:1 sur fond
    "accent": "FFC845",    # jaune soleil : 10,9:1 sur fond, 7,6:1 sur carte
    "accent2": "7FE0D0",   # turquoise lagon : 9,9:1 sur fond
    "sombre": "102A33",
}
POLICE = "Arial"   # présente sur tous les postes ; lisible pour les publics dys
T_TITRE, T_TEXTE, T_PETIT = 44, 32, 26

W, H = Inches(13.333), Inches(7.5)
MARGE = Inches(0.6)


def rgb(h):
    return RGBColor.from_string(h)


def _fond(slide, couleur=None):
    f = slide.background.fill
    f.solid()
    f.fore_color.rgb = rgb(couleur or PALETTE["fond"])


def _style_runs(tf, taille, couleur, gras=False, align=PP_ALIGN.LEFT):
    for p in tf.paragraphs:
        p.alignment = align
        for r in p.runs:
            r.font.name = POLICE
            r.font.size = Pt(taille)
            r.font.bold = gras
            r.font.color.rgb = rgb(couleur)


def _puce(p):
    """Vraie puce PowerPoint (lue correctement par les lecteurs d'écran, non comptée comme un mot)."""
    from pptx.oxml.ns import qn
    pPr = p._p.get_or_add_pPr()
    pPr.set("marL", str(Inches(0.5)))
    pPr.set("indent", str(-Inches(0.45)))
    for tag in ("a:buClr", "a:buFont", "a:buChar"):
        el = pPr.find(qn(tag))
        if el is not None:
            pPr.remove(el)
    clr = pPr.makeelement(qn("a:buClr"), {})
    srgb = clr.makeelement(qn("a:srgbClr"), {"val": PALETTE["accent"]})
    clr.append(srgb)
    pPr.append(clr)
    pPr.append(pPr.makeelement(qn("a:buFont"), {"typeface": "Arial"}))
    pPr.append(pPr.makeelement(qn("a:buChar"), {"char": "•"}))


def boite_texte(slide, x, y, w, h, lignes, taille=T_TEXTE, couleur=None, gras=False,
                align=PP_ALIGN.LEFT, ancre=MSO_ANCHOR.TOP, puce=False, nom=None, interligne=1.15):
    tb = slide.shapes.add_textbox(x, y, w, h)
    if nom:
        tb.name = nom
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.vertical_anchor = ancre
    for m in ("margin_left", "margin_right"):
        setattr(tf, m, Inches(0.1))
    if isinstance(lignes, str):
        lignes = [lignes]
    for i, l in enumerate(lignes):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = interligne
        p.space_after = Pt(10)
        if puce:
            _puce(p)
        r = p.add_run()
        r.text = l
    _style_runs(tf, taille, couleur or PALETTE["texte"], gras, align)
    return tb


def carte(slide, x, y, w, h, titre, texte=None, fond=None, c_titre=None, t_titre=30, t_texte=28,
          nom=None):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    sh.adjustments[0] = 0.08
    sh.fill.solid()
    sh.fill.fore_color.rgb = rgb(fond or PALETTE["carte"])
    sh.line.fill.background()
    sh.shadow.inherit = False
    if nom:
        sh.name = nom
    tf = sh.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, Inches(0.15))
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = titre
    r.font.name, r.font.size, r.font.bold = POLICE, Pt(t_titre), True
    r.font.color.rgb = rgb(c_titre or PALETTE["accent"])
    if texte:
        for l in (texte if isinstance(texte, list) else [texte]):
            p2 = tf.add_paragraph()
            p2.alignment = PP_ALIGN.CENTER
            p2.space_before = Pt(6)
            r2 = p2.add_run()
            r2.text = l
            r2.font.name, r2.font.size = POLICE, Pt(t_texte)
            r2.font.color.rgb = rgb(PALETTE["texte"])
    return sh


def fleche(slide, x, y, w, h):
    sh = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x, y, w, h)
    sh.fill.solid()
    sh.fill.fore_color.rgb = rgb(PALETTE["accent2"])
    sh.line.fill.background()
    sh.name = "Flèche décorative"
    return sh


class Deck:
    def __init__(self, titre_doc, sujet):
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = W, H
        cp = self.prs.core_properties
        cp.title, cp.subject, cp.author, cp.last_modified_by = titre_doc, sujet, "Formateur TP MEM", "Formateur TP MEM"
        cp.keywords, cp.comments = "TP MEM, REAC TP-00136 v09", ""
        self.layout = self.prs.slide_layouts[5]  # « Titre seul » : le titre reste lisible par les lecteurs d'écran

    def _nouvelle(self, titre, fond=None, taille=T_TITRE, y=Inches(0.35), h=Inches(1.25), couleur=None):
        s = self.prs.slides.add_slide(self.layout)
        _fond(s, fond)
        t = s.shapes.title
        t.name = "!!titre"
        t.left, t.top, t.width, t.height = MARGE, y, W - 2 * MARGE, h
        t.text = titre
        tf = t.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        _style_runs(tf, taille, couleur or PALETTE["accent"], True, PP_ALIGN.LEFT)
        # bandeau d'accent SOUS le titre (ne traverse aucun texte)
        b = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, MARGE + Inches(0.1), y + h + Inches(0.05), Inches(1.6), Inches(0.09))
        b.fill.solid(); b.fill.fore_color.rgb = rgb(PALETTE["accent2"]); b.line.fill.background()
        b.name = "!!bandeau"
        return s

    def _notes(self, s, notes):
        if notes:
            s.notes_slide.notes_text_frame.text = notes

    # ---------- types de diapositives ----------
    def couverture(self, d):
        s = self._nouvelle(d["titre"], y=Inches(2.0), h=Inches(2.2), taille=54, couleur=PALETTE["texte"])
        boite_texte(s, MARGE, Inches(4.6), W - 2 * MARGE, Inches(1.0), d.get("sous_titre", ""), 34, PALETTE["accent"], True)
        boite_texte(s, MARGE, Inches(5.7), W - 2 * MARGE, Inches(0.9), d.get("date", ""), 28, PALETTE["accent2"])
        boite_texte(s, MARGE, Inches(0.5), W - 2 * MARGE, Inches(0.8), d.get("bandeau", "Titre professionnel MEM · Niveau 5"), 26, PALETTE["accent2"], True)
        self._notes(s, d.get("notes"))

    def section(self, d):
        s = self._nouvelle(d["titre"], y=Inches(2.8), h=Inches(1.6), taille=50, couleur=PALETTE["texte"])
        boite_texte(s, MARGE, Inches(1.2), Inches(5), Inches(1.4), d.get("num", ""), 66, PALETTE["accent"], True)
        if d.get("sous_titre"):
            boite_texte(s, MARGE, Inches(4.9), W - 2 * MARGE, Inches(1.2), d["sous_titre"], 32, PALETTE["accent2"])
        self._notes(s, d.get("notes"))

    def puces(self, d):
        s = self._nouvelle(d["titre"])
        boite_texte(s, MARGE + Inches(0.2), Inches(2.0), W - 2 * MARGE - Inches(0.4), Inches(5.0),
                    d["items"], d.get("taille", T_TEXTE), puce=True, interligne=1.2)
        self._notes(s, d.get("notes"))

    def chiffre(self, d):
        s = self._nouvelle(d["titre"])
        boite_texte(s, MARGE, Inches(2.0), W - 2 * MARGE, Inches(2.6), d["valeur"], 120, PALETTE["accent"], True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
        boite_texte(s, MARGE, Inches(4.7), W - 2 * MARGE, Inches(1.2), d["legende"], 34, PALETTE["texte"], True, PP_ALIGN.CENTER)
        if d.get("source"):
            boite_texte(s, MARGE, Inches(6.2), W - 2 * MARGE, Inches(0.8), d["source"], 24, PALETTE["accent2"], False, PP_ALIGN.CENTER)
        self._notes(s, d.get("notes"))

    def cartes(self, d):
        s = self._nouvelle(d["titre"])
        items = d["items"]
        n = len(items)
        cols = d.get("cols", 2 if n == 4 else (n if n <= 3 else (3 if n in (5, 6) else 4)))
        lignes = (n + cols - 1) // cols
        gx = Inches(0.3)
        zone_w = W - 2 * MARGE
        cw = (zone_w - gx * (cols - 1)) / cols
        top = Inches(2.05)
        zone_h = Inches(5.1)
        gy = Inches(0.3)
        ch = (zone_h - gy * (lignes - 1)) / lignes
        for i, it in enumerate(items):
            r, c = divmod(i, cols)
            x = MARGE + int((cw + gx) * c)
            y = top + int((ch + gy) * r)
            fond = PALETTE["carte"] if (r + c) % 2 == 0 else PALETTE["carte2"]
            carte(s, x, y, int(cw), int(ch), it[0], it[1] if len(it) > 1 else None, fond,
                  t_titre=d.get("t_titre", 32 if n <= 4 else 30), t_texte=d.get("t_texte", 28), nom=f"Carte {i+1}")
        self._notes(s, d.get("notes"))

    def etapes(self, d):
        items = d["items"]
        if len(items) > 4:  # trop étroit en ligne : bascule en cartes numérotées (aucun mot coupé)
            return self.cartes({**d, "items": [(f"{i+1} · {t[0]}",) + tuple(t[1:]) for i, t in enumerate(items)]})
        s = self._nouvelle(d["titre"])
        n = len(items)
        fw = Inches(0.45)
        zone_w = W - 2 * MARGE
        cw = (zone_w - fw * (n - 1) - Inches(0.2) * 2 * (n - 1)) / n
        y, h = Inches(2.4), Inches(4.0)
        x = MARGE
        for i, it in enumerate(items):
            carte(s, int(x), y, int(cw), h, it[0], it[1] if len(it) > 1 else None,
                  PALETTE["carte"] if i % 2 == 0 else PALETTE["carte2"], t_titre=d.get("t_titre", 30), t_texte=d.get("t_texte", 28),
                  nom=f"Étape {i+1}")
            x += cw
            if i < n - 1:
                fleche(s, int(x + Inches(0.2)), y + h // 2 - Inches(0.3), fw, Inches(0.6))
                x += fw + Inches(0.4)
        self._notes(s, d.get("notes"))

    def comparer(self, d):
        s = self._nouvelle(d["titre"])
        zone_w = W - 2 * MARGE
        cw = (zone_w - Inches(0.4)) / 2
        for k, (tete, items) in enumerate((d["gauche"], d["droite"])):
            x = MARGE + int((cw + Inches(0.4)) * k)
            carte(s, x, Inches(2.05), int(cw), Inches(1.0), tete, None, PALETTE["carte"] if k == 0 else PALETTE["carte2"], t_titre=32)
            boite_texte(s, x + Inches(0.1), Inches(3.25), int(cw) - Inches(0.2), Inches(3.9), items, 28, puce=True)
        self._notes(s, d.get("notes"))

    def exemple(self, d):
        s = self._nouvelle(d["titre"])
        carte(s, MARGE, Inches(2.05), Inches(4.3), Inches(4.9), d.get("lieu", "Exemple"), d.get("lieu_detail"),
              PALETTE["carte2"], c_titre=PALETTE["accent2"], t_titre=30, t_texte=26)
        boite_texte(s, MARGE + Inches(4.7), Inches(2.05), W - 2 * MARGE - Inches(4.7), Inches(4.9), d["items"], 30, puce=True)
        self._notes(s, d.get("notes"))

    def activite(self, d):
        s = self._nouvelle(d["titre"], fond=PALETTE["carte"])
        boite_texte(s, MARGE, Inches(1.95), Inches(5.5), Inches(0.8), d.get("genre", "À vous de jouer"), 30, PALETTE["accent2"], True)
        boite_texte(s, W - MARGE - Inches(4.5), Inches(1.95), Inches(4.5), Inches(0.8), d.get("duree", ""), 30, PALETTE["accent"], True, PP_ALIGN.RIGHT)
        boite_texte(s, MARGE + Inches(0.2), Inches(2.9), W - 2 * MARGE - Inches(0.4), Inches(4.2), d["items"], 30, puce=True)
        self._notes(s, d.get("notes"))

    def question(self, d):
        s = self._nouvelle(d.get("titre", "Question"))
        boite_texte(s, MARGE, Inches(2.2), W - 2 * MARGE, Inches(4.5), d["texte"].split("\n"), 40, PALETTE["texte"], True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
        self._notes(s, d.get("notes"))

    def ajouter(self, d):
        getattr(self, d["type"])(d)

    def enregistrer(self, chemin):
        self.prs.save(chemin)
