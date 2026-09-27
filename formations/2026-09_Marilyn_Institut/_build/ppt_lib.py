"""Moteur de diaporama accessible — charte YEBA FORMATIONS.

Règles tenues par construction :
- police Verdana (présente sur tout PC Windows/Mac), titres 40 pt, corps 28 pt minimum ;
- aucun filet ne traverse un mot : les barres or sont placées hors des zones de texte ;
- or uniquement sur fond bleu (contraste 4,93:1) ou en surface, jamais en texte sur blanc ;
- chaque diapositive a un vrai titre (placeholder) lu par les lecteurs d'écran ;
- le script du formateur est dans les notes, jamais à l'écran.
"""
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt, Emu

BLEU = RGBColor(0x1B, 0x3A, 0x6B)
BLEU_F = RGBColor(0x12, 0x28, 0x4C)
OR = RGBColor(0xC9, 0xA8, 0x4C)
OR_CLAIR = RGBColor(0xF4, 0xED, 0xDA)
NOIR = RGBColor(0x12, 0x12, 0x12)
BLANC = RGBColor(0xFF, 0xFF, 0xFF)
CASSE = RGBColor(0xF7, 0xF7, 0xF5)
GRIS = RGBColor(0x5A, 0x5F, 0x6A)
VERT = RGBColor(0x1E, 0x6B, 0x3A)   # 6,6:1 sur blanc
ROUGE = RGBColor(0xA3, 0x1E, 0x1E)  # 7,4:1 sur blanc
POLICE = "Verdana"
W, H = Inches(13.333), Inches(7.5)
NBSP = "\u00a0"


def typo(t):
    """Espaces insécables français : un guillemet ou un « ? » ne se retrouve jamais seul en début de ligne."""
    for a, b in (("« ", "«" + NBSP), (" »", NBSP + "»"), (" ?", NBSP + "?"), (" !", NBSP + "!"), (" :", NBSP + ":"),
                 (" €", NBSP + "€"), (" %", NBSP + "%")):
        t = t.replace(a, b)
    return t


def _larg_car(c):
    if c == " ":
        return 0.33
    if c in "il.,;:'!|·":
        return 0.34
    if c in "fjrtI()«»-":
        return 0.45
    if c.isupper() or c in "mwMW%€@":
        return 0.78
    if c.isdigit():
        return 0.66
    return 0.62


def largeur_txt(txt, pt, gras=False):
    """Largeur estimée (pouces), calibrée sur Verdana / DejaVu Sans (police de repli) — volontairement pessimiste."""
    return sum(_larg_car(c) for c in txt) * pt / 72 * (1.15 if gras else 1.04)


def lignes_necessaires(txt, pt, largeur, gras=False):
    """Retour à la ligne glouton par mots ; None si un mot seul dépasse (il serait coupé : interdit)."""
    n, cour = 1, ""
    for mot in txt.replace(NBSP, "\u2060").split(" "):
        mot_r = mot.replace("\u2060", " ")
        if largeur_txt(mot_r, pt, gras) > largeur:
            return None
        essai = (cour + " " + mot_r).strip()
        if largeur_txt(essai, pt, gras) <= largeur:
            cour = essai
        else:
            n += 1
            cour = mot_r
    return n


def ajuster(txt, largeur, hauteur, pt_max, pt_min=24, gras=False, interligne=1.2):
    """Plus grande taille (pas de 1 pt) telle que le texte tienne dans la boîte sans couper de mot."""
    txt = typo(txt)
    for pt in range(int(pt_max), int(pt_min) - 1, -1):
        n = lignes_necessaires(txt, pt, largeur, gras)
        if n is not None and n * pt * interligne / 72 <= hauteur:
            return pt
    raise ValueError(f"Texte trop long pour sa boîte, même à {pt_min} pt : « {txt} » ({largeur:.2f} x {hauteur:.2f} in)")


def taille_commune(textes, largeur, hauteur, pt_max, pt_min=24, gras=False):
    """Une seule taille pour toutes les cartes d'une diapositive : la plus grande qui convient à toutes."""
    return min(ajuster(t if isinstance(t, str) else t[0], largeur - 0.2, hauteur - 0.1, pt_max, pt_min, gras) for t in textes)


class Deck:
    def __init__(self, logo, logo_blanc):
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = W, H
        self.logo, self.logo_blanc = logo, logo_blanc
        self.n = 0

    # ------------------------------------------------------------ primitives
    def _slide(self, fond=CASSE):
        s = self.prs.slides.add_slide(self.prs.slide_layouts[5])  # « Titre seul »
        bg = s.background.fill
        bg.solid(); bg.fore_color.rgb = fond
        self.n += 1
        return s

    def _titre(self, s, texte, couleur=BLEU, top=0.35, taille=40, gauche=0.9, largeur=None, align=PP_ALIGN.LEFT):
        t = s.shapes.title
        t.left, t.top = Inches(gauche), Inches(top)
        t.width = Inches(largeur or (13.333 - gauche - 0.6)); t.height = Inches(1.1)
        tf = t.text_frame; tf.clear(); tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]; p.alignment = align
        r = p.add_run(); r.text = typo(texte)
        if top >= 0 and taille <= 40:
            taille = ajuster(texte, (largeur or (13.333 - gauche - 0.6)) - 0.2, 1.0, taille, 32, True)
        f = r.font; f.name = POLICE; f.size = Pt(taille); f.bold = True; f.color.rgb = couleur
        return t

    def _barre(self, s, top=0.45, h=0.9):
        """Barre or verticale à gauche du titre : elle ne touche jamais le texte."""
        b = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.45), Inches(top), Inches(0.14), Inches(h))
        b.fill.solid(); b.fill.fore_color.rgb = OR; b.line.fill.background()

    def _texte(self, s, x, y, w, h, lignes, taille=30, couleur=NOIR, gras=False, align=PP_ALIGN.LEFT,
               anchor=MSO_ANCHOR.TOP, interligne=1.1, police=POLICE, fit=None):
        """fit=(pt_max, pt_min) : taille calculée pour qu'aucun mot ne soit coupé ni ne déborde."""
        if fit:
            lignes0 = lignes if isinstance(lignes, list) else [lignes]
            txt = " ".join(l[0] if isinstance(l, tuple) else l for l in lignes0)
            taille = ajuster(txt, w - 0.2, h - 0.1, fit[0], fit[1], gras)
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
        tf.margin_left = tf.margin_right = Inches(0.08)
        tf.margin_top = tf.margin_bottom = Inches(0.03)
        lignes = lignes if isinstance(lignes, list) else [lignes]
        for i, l in enumerate(lignes):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align; p.line_spacing = interligne
            st = {}
            if isinstance(l, tuple):
                l, st = l
            r = p.add_run(); r.text = typo(l)
            f = r.font; f.name = police; f.size = Pt(st.get("t", taille)); f.bold = st.get("b", gras)
            f.color.rgb = st.get("c", couleur); f.italic = st.get("i", False)
            p.space_after = Pt(st.get("apres", 6))
        return tb

    def _carte(self, s, x, y, w, h, fond=BLANC, bord=None, forme=MSO_SHAPE.ROUNDED_RECTANGLE):
        c = s.shapes.add_shape(forme, Inches(x), Inches(y), Inches(w), Inches(h))
        c.fill.solid(); c.fill.fore_color.rgb = fond
        if bord is None:
            c.line.fill.background()
        else:
            c.line.color.rgb = bord; c.line.width = Pt(2.5)
        if forme == MSO_SHAPE.ROUNDED_RECTANGLE:
            c.adjustments[0] = 0.12
        c.shadow.inherit = False
        return c

    def _pied(self, s, sombre=False):
        self._texte(s, 11.9, 6.95, 1.2, 0.45, str(self.n), taille=14, couleur=(BLANC if sombre else GRIS), align=PP_ALIGN.RIGHT)

    def notes(self, s, texte):
        s.notes_slide.notes_text_frame.text = texte

    # ------------------------------------------------------------- gabarits
    def couverture(self, titre, sous, bas, note=""):
        s = self._slide(BLEU)
        s.shapes.add_picture(self.logo_blanc, Inches(0.9), Inches(0.6), width=Inches(2.6))
        self._titre(s, titre, BLANC, top=1.75, taille=44, largeur=11.6)
        s.shapes.title.height = Inches(2.6)
        s.shapes.title.text_frame.vertical_anchor = MSO_ANCHOR.BOTTOM
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(4.62), Inches(2.2), Inches(0.1))
        bar.fill.solid(); bar.fill.fore_color.rgb = OR; bar.line.fill.background()
        self._texte(s, 0.9, 4.85, 11.5, 0.8, sous, taille=30, couleur=OR, gras=True)
        self._texte(s, 0.9, 5.75, 11.5, 1.2, bas, taille=24, couleur=BLANC)
        self.notes(s, note)
        return s

    def section(self, lettre, titre, sous="", horaire="", note=""):
        s = self._slide(BLEU)
        self._texte(s, 0.6, 0.6, 4.2, 5.6, lettre, taille=260, couleur=OR, gras=True, align=PP_ALIGN.CENTER,
                    anchor=MSO_ANCHOR.MIDDLE)
        self._titre(s, titre, BLANC, top=2.2, taille=48, gauche=5.2, largeur=7.6)
        s.shapes.title.height = Inches(1.6)
        if sous:
            self._texte(s, 5.2, 3.85, 7.6, 1.45, sous, couleur=OR, gras=True, fit=(32, 26))
        if horaire:
            self._texte(s, 5.2, 5.5, 7.6, 0.7, horaire, taille=26, couleur=BLANC)
        self._pied(s, True)
        self.notes(s, note)
        return s

    def mots(self, titre, mots, note="", taille=32, colonnes=1, pastilles=True):
        """Liste de mots-clés sous forme de cartes blanches — 5 par colonne au maximum."""
        s = self._slide()
        self._barre(s); self._titre(s, titre)
        n = len(mots)
        par_col = -(-n // colonnes)
        larg = (12.0 - 0.3 * (colonnes - 1)) / colonnes
        haut = min(1.0, 5.2 / par_col - 0.15)
        dx0 = 0.7 if pastilles else 0
        tc = taille_commune(mots, larg - 0.3 - dx0, haut, taille, 24)
        for i, m in enumerate(mots):
            col, row = divmod(i, par_col)
            x = 0.7 + col * (larg + 0.3); y = 1.75 + row * (haut + 0.15)
            self._carte(s, x, y, larg, haut)
            dx = 0
            if pastilles:
                p = self._carte(s, x + 0.18, y + haut / 2 - 0.2, 0.4, 0.4, fond=OR, forme=MSO_SHAPE.OVAL)
                dx = 0.7
            txt = m if isinstance(m, tuple) else (m, {})
            self._texte(s, x + 0.15 + dx, y, larg - 0.3 - dx, haut, [txt], anchor=MSO_ANCHOR.MIDDLE, taille=tc)
        self._pied(s); self.notes(s, note)
        return s

    def tuiles(self, titre, tuiles, note="", taille_grand=66, taille_petit=24, hauteur=4.3):
        """Tuiles horizontales : (grand, petit). Idéal pour les acronymes."""
        s = self._slide()
        self._barre(s); self._titre(s, titre)
        n = len(tuiles)
        esp = 0.25
        larg = (12.0 - esp * (n - 1)) / n
        tg = taille_commune([g for g, _ in tuiles], larg, 1.6, taille_grand, 28, True)
        tp = taille_commune([p for _, p in tuiles], larg - 0.16, hauteur - 1.9, taille_petit, 22, True)
        for i, (g, p) in enumerate(tuiles):
            x = 0.7 + i * (larg + esp)
            self._carte(s, x, 1.9, larg, hauteur, fond=BLEU)
            self._texte(s, x, 2.05, larg, 1.6, g, couleur=OR, gras=True, align=PP_ALIGN.CENTER,
                        anchor=MSO_ANCHOR.MIDDLE, taille=tg)
            self._texte(s, x + 0.08, 3.7, larg - 0.16, hauteur - 1.9, p, couleur=BLANC, gras=True,
                        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP, taille=tp)
        self._pied(s); self.notes(s, note)
        return s

    def acronyme(self, titre, items, note="", colonnes=1, taille=34):
        """Une ligne par lettre : carré bleu + lettre or, puis le mot en entier. Aucun mot n'est jamais coupé."""
        s = self._slide()
        self._barre(s); self._titre(s, titre)
        par_col = -(-len(items) // colonnes)
        haut = min(1.05, 5.3 / par_col - 0.12)
        larg = (12.0 - 0.4 * (colonnes - 1)) / colonnes
        tc = taille_commune([m for _, m in items], larg - haut - 0.45, haut, taille, 24)
        for i, (l, mot) in enumerate(items):
            c, r = divmod(i, par_col)
            x = 0.7 + c * (larg + 0.4); y = 1.75 + r * (haut + 0.12)
            self._carte(s, x, y, haut, haut, fond=BLEU)
            self._texte(s, x, y, haut, haut, l, couleur=OR, gras=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                        fit=(int(haut * 50), 28))
            self._carte(s, x + haut + 0.15, y, larg - haut - 0.15, haut)
            self._texte(s, x + haut + 0.3, y, larg - haut - 0.45, haut, mot, anchor=MSO_ANCHOR.MIDDLE, taille=tc)
        self._pied(s); self.notes(s, note)
        return s

    def consigne(self, titre, etapes, duree, materiel="", note=""):
        """Diapositive d'exercice : pastille chrono à gauche, étapes numérotées à droite."""
        s = self._slide()
        self._barre(s); self._titre(s, titre)
        c = self._carte(s, 0.7, 1.9, 3.0, 3.0, fond=BLEU, forme=MSO_SHAPE.OVAL)
        nb = duree.split()[0]
        self._texte(s, 0.85, 2.2, 2.7, 1.4, nb, taille=72, couleur=OR, gras=True, align=PP_ALIGN.CENTER,
                    anchor=MSO_ANCHOR.MIDDLE)
        self._texte(s, 0.7, 3.55, 3.0, 0.6, "minutes", taille=24, couleur=BLANC, gras=True, align=PP_ALIGN.CENTER)
        if materiel:
            self._texte(s, 0.4, 5.1, 3.6, 1.6, materiel, taille=22, couleur=GRIS, align=PP_ALIGN.CENTER)
        y = 1.85
        h = min(1.15, 5.1 / len(etapes) - 0.1)
        tc = taille_commune(etapes, 7.5, h, 30, 24)
        for i, e in enumerate(etapes, 1):
            self._carte(s, 4.2, y, 8.5, h)
            self._texte(s, 4.3, y, 0.8, h, str(i), taille=34, couleur=BLEU, gras=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            self._texte(s, 5.1, y, 7.5, h, e, anchor=MSO_ANCHOR.MIDDLE, taille=tc)
            y += h + 0.1
        self._pied(s); self.notes(s, note)
        return s

    def citation(self, phrase, sous="", note="", titre_access="Phrase clé", fond=BLEU, taille=54):
        s = self._slide(fond)
        self._titre(s, titre_access, fond, top=-2.0, taille=10)  # titre accessible, hors champ visible
        clair = fond in (BLEU, BLEU_F)
        txt = "«" + NBSP + phrase.replace(" ?", NBSP + "?").replace(" !", NBSP + "!") + NBSP + "»"
        self._texte(s, 1.0, 1.4, 11.3, 3.6, txt, couleur=(BLANC if clair else BLEU),
                    gras=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fit=(taille, 36))
        if sous:
            self._texte(s, 1.0, 5.1, 11.3, 1.4, sous, taille=30, couleur=(OR if clair else NOIR), gras=True, align=PP_ALIGN.CENTER)
        self._pied(s, clair); self.notes(s, note)
        return s

    def compare(self, titre, gauche, droite, note="", taille=28):
        """Deux colonnes : (titre, [items], couleur)."""
        s = self._slide()
        self._barre(s); self._titre(s, titre)
        hh = min(1.25, 4.3 / max(len(gauche[1]), len(droite[1])) - 0.1)
        tc = taille_commune(gauche[1] + droite[1], 4.95, hh, taille, 24)
        te = taille_commune([gauche[0], droite[0]], 5.85, 0.95, 30, 24, True)
        for k, (t, items, coul, signe) in enumerate((gauche, droite)):
            x = 0.7 + k * 6.15
            self._carte(s, x, 1.85, 5.85, 0.95, fond=coul)
            self._texte(s, x, 1.85, 5.85, 0.95, t, couleur=BLANC, gras=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                        taille=te)
            y = 2.95
            h = hh
            for it in items:
                self._carte(s, x, y, 5.85, h)
                self._texte(s, x + 0.1, y, 0.7, h, signe, taille=30, couleur=coul, gras=True, anchor=MSO_ANCHOR.MIDDLE)
                self._texte(s, x + 0.8, y, 4.95, h, it, anchor=MSO_ANCHOR.MIDDLE, taille=tc)
                y += h + 0.1
        self._pied(s); self.notes(s, note)
        return s

    def parcours(self, titre, etapes, note=""):
        """Frise en 2 rangées (6 + 6)."""
        s = self._slide()
        self._barre(s); self._titre(s, titre)
        par = 3
        larg = (12.0 - 0.2 * (par - 1)) / par
        tc = taille_commune(etapes, larg - 1.1, 1.2, 28, 22)
        for i, e in enumerate(etapes):
            r, c = divmod(i, par)
            x = 0.7 + c * (larg + 0.2); y = 1.75 + r * 1.32
            self._carte(s, x, y, larg, 1.2, fond=BLANC, bord=BLEU)
            self._texte(s, x + 0.05, y, 1.0, 1.2, str(i + 1), taille=30, couleur=BLEU, gras=True, align=PP_ALIGN.CENTER,
                        anchor=MSO_ANCHOR.MIDDLE)
            self._texte(s, x + 1.05, y, larg - 1.1, 1.2, e, anchor=MSO_ANCHOR.MIDDLE, taille=tc)
        self._pied(s); self.notes(s, note)
        return s

    def grand_nombre(self, nombre, texte, note="", titre_access="Chiffre clé"):
        s = self._slide()
        self._titre(s, titre_access, CASSE, top=-2.0, taille=10)
        self._carte(s, 0.9, 1.3, 4.6, 4.6, fond=BLEU, forme=MSO_SHAPE.OVAL)
        self._texte(s, 1.2, 1.6, 4.0, 4.0, nombre, couleur=OR, gras=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                    fit=(150, 60))
        self._texte(s, 6.0, 1.3, 6.7, 4.6, texte, taille=40, couleur=BLEU, gras=True, anchor=MSO_ANCHOR.MIDDLE)
        self._pied(s); self.notes(s, note)
        return s

    def image(self, titre, chemin, note="", largeur=11.5):
        s = self._slide()
        self._barre(s); self._titre(s, titre)
        s.shapes.add_picture(chemin, Inches((13.333 - largeur) / 2), Inches(1.7), width=Inches(largeur))
        self._pied(s); self.notes(s, note)
        return s

    def fin(self, titre, lignes, note=""):
        s = self._slide(BLEU)
        s.shapes.add_picture(self.logo_blanc, Inches(0.9), Inches(0.6), width=Inches(2.2))
        self._titre(s, titre, BLANC, top=2.0, taille=54, largeur=11.6)
        self._texte(s, 0.9, 3.4, 11.6, 3.6, lignes, taille=28, couleur=BLANC)
        self.notes(s, note)
        return s

    def enregistrer(self, chemin):
        self.prs.save(str(chemin))
        return chemin
