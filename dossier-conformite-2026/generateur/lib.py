"""Mise en forme commune des documents YEBA FORMATIONS (DOCX accessibles).

Charte : bleu marine #1B3A6B, or #C9A94D, police Arial 12 pt minimum,
titres larges, fort contraste, aucun texte en image (lisible par lecteur d'écran).
"""
import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

RACINE = Path(__file__).resolve().parents[1]
LOGO = RACINE / "assets" / "logo_yeba_formations.png"
SORTIE = RACINE / "livrables"

BLEU = RGBColor(0x1B, 0x3A, 0x6B)
OR = RGBColor(0xC9, 0xA9, 0x4D)
BLEU_HEX, OR_HEX, GRIS_HEX = "1B3A6B", "C9A94D", "F2F2F2"

ORGANISME = {
    "nom": "YEBA FORMATIONS",
    "siret": "814 622 262 00032",
    "nda": "04973676397",
    "nda_mention": "Cet enregistrement ne vaut pas agrément de l'État",
    "qualiopi": "25FOR02027.1",
    "dirigeant": "Aurélien LUMEKA",
    "adresse": "[À COMPLÉTER : adresse du siège]",
    "tel": "[À COMPLÉTER : téléphone]",
    "mail": "[À COMPLÉTER : e-mail de contact]",
    "ref_handicap": "Aurélien LUMEKA (référent handicap certifié)",
    "contact_rgpd": "[À COMPLÉTER : adresse e-mail dédiée RGPD, ex. rgpd@…]",
}

PLACEHOLDER = re.compile(r"(\[À COMPLÉTER[^\]]*\]|\[À VÉRIFIER[^\]]*\]|_{6,})")


def _shade(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def _largeurs(table, largeurs_cm):
    """Fixe les largeurs (grille + cellules) pour Word et LibreOffice."""
    table.autofit = False
    grille = table._tbl.tblGrid
    for i, col in enumerate(grille.findall(qn("w:gridCol"))):
        col.set(qn("w:w"), str(int(largeurs_cm[i] * 567)))
    for row in table.rows:
        for i, w in enumerate(largeurs_cm):
            row.cells[i].width = Cm(w)


def _runs(par, texte, bold=False, color=None, size=None):
    """Ajoute du texte ; **gras** et champs à compléter surlignés en jaune."""
    for morceau in re.split(r"(\*\*[^*]+\*\*)", texte):
        if not morceau:
            continue
        gras = bold or (morceau.startswith("**") and morceau.endswith("**"))
        morceau = morceau.strip("*") if morceau.startswith("**") else morceau
        for sous in PLACEHOLDER.split(morceau):
            if not sous:
                continue
            r = par.add_run(sous)
            r.bold = gras
            if color is not None:
                r.font.color.rgb = color
            if size:
                r.font.size = Pt(size)
            if PLACEHOLDER.fullmatch(sous) and not sous.startswith("_"):
                r.font.highlight_color = WD_COLOR_INDEX.YELLOW


class Doc:
    def __init__(self, titre, sous_titre="", code="", marque=True, paysage=False):
        self.titre, self.code, self.marque = titre, code, marque
        self.d = Document()
        sec = self.d.sections[0]
        if paysage:
            sec.orientation = WD_ORIENT.LANDSCAPE
            sec.page_width, sec.page_height = Cm(29.7), Cm(21)
        else:
            sec.page_width, sec.page_height = Cm(21), Cm(29.7)
        sec.left_margin = sec.right_margin = Cm(2)
        sec.top_margin, sec.bottom_margin = Cm(1.8), Cm(1.8)
        st = self.d.styles["Normal"]
        st.font.name = "Arial"
        st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
        st.font.size = Pt(12)
        st.paragraph_format.space_after = Pt(6)
        st.paragraph_format.line_spacing = 1.15
        for niv, taille, coul in ((1, 20, BLEU), (2, 16, BLEU), (3, 13, OR)):
            h = self.d.styles[f"Heading {niv}"]
            h.font.name, h.font.size, h.font.bold = "Arial", Pt(taille), True
            h.font.color.rgb = coul
        self.d.core_properties.title = titre
        self.d.core_properties.author = ORGANISME["nom"] if marque else ""
        self.d.core_properties.language = "fr-FR"
        self._entete_pied()
        self._page_titre(titre, sous_titre)

    def _entete_pied(self):
        sec = self.d.sections[0]
        hp = sec.header.paragraphs[0]
        if self.marque:
            hp.add_run().add_picture(str(LOGO), height=Cm(1.6))
            r = hp.add_run(f"    {ORGANISME['nom']}  |  NDA {ORGANISME['nda']}  |  Qualiopi {ORGANISME['qualiopi']}")
            r.font.size, r.font.color.rgb = Pt(9), BLEU
        fp = sec.footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        txt = f"{self.code}  —  " if self.code else ""
        if self.marque:
            txt += f"{ORGANISME['nom']} — SIRET {ORGANISME['siret']} — Version 2026-10 — Page "
        else:
            txt += "Version 2026-10 — Page "
        r = fp.add_run(txt)
        r.font.size = Pt(9)
        for code in ("PAGE",):
            run = fp.add_run()
            for tag, val in (("begin", None), (None, code), ("end", None)):
                if tag:
                    el = OxmlElement("w:fldChar")
                    el.set(qn("w:fldCharType"), tag)
                else:
                    el = OxmlElement("w:instrText")
                    el.text = val
                run._r.append(el)
            run.font.size = Pt(9)

    def _page_titre(self, titre, sous_titre):
        p = self.d.add_paragraph()
        _runs(p, titre, bold=True, color=BLEU, size=22)
        if sous_titre:
            p = self.d.add_paragraph()
            _runs(p, sous_titre, color=OR, size=14, bold=True)
        self.filet()

    def filet(self):
        p = self.d.add_paragraph()
        pPr = p._p.get_or_add_pPr()
        b = OxmlElement("w:pBdr")
        bot = OxmlElement("w:bottom")
        for k, v in (("w:val", "single"), ("w:sz", "18"), ("w:space", "1"), ("w:color", OR_HEX)):
            bot.set(qn(k), v)
        b.append(bot)
        pPr.append(b)

    # --- blocs -----------------------------------------------------------
    def h1(self, t):
        self.d.add_heading(t, level=1)

    def h2(self, t):
        self.d.add_heading(t, level=2)

    def h3(self, t):
        self.d.add_heading(t, level=3)

    def p(self, t, bold=False, italic=False):
        par = self.d.add_paragraph()
        _runs(par, t, bold=bold)
        if italic:
            for r in par.runs:
                r.italic = True
        return par

    def puces(self, items, style="List Bullet"):
        for it in items:
            _runs(self.d.add_paragraph(style=style), it)

    def numeros(self, items):
        self.puces(items, "List Number")

    def cases(self, items):
        for it in items:
            _runs(self.d.add_paragraph(), "☐  " + it)

    def tableau(self, entetes, lignes, largeurs=None):
        t = self.d.add_table(rows=1, cols=len(entetes))
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for i, e in enumerate(entetes):
            c = t.rows[0].cells[i]
            c.text = ""
            _runs(c.paragraphs[0], str(e), bold=True, color=RGBColor(0xFF, 0xFF, 0xFF), size=11)
            _shade(c, BLEU_HEX)
        # ligne d'en-tête répétée à chaque page
        trPr = t.rows[0]._tr.get_or_add_trPr()
        th = OxmlElement("w:tblHeader")
        th.set(qn("w:val"), "true")
        trPr.append(th)
        for n, ligne in enumerate(lignes):
            cells = t.add_row().cells
            for i, v in enumerate(ligne):
                cells[i].text = ""
                _runs(cells[i].paragraphs[0], str(v), size=11)
                if n % 2:
                    _shade(cells[i], GRIS_HEX)
        if largeurs:
            _largeurs(t, largeurs)
        self.d.add_paragraph()
        return t

    def champs(self, libelles, largeur=2):
        """Formulaire : libellé + zone de saisie."""
        t = self.d.add_table(rows=0, cols=2)
        t.style = "Table Grid"
        for lib in libelles:
            cells = t.add_row().cells
            _runs(cells[0].paragraphs[0], lib, bold=True, size=11)
            _shade(cells[0], GRIS_HEX)
        _largeurs(t, [6.5, 10.5])
        self.d.add_paragraph()

    def encadre(self, titre, texte, couleur=OR_HEX):
        t = self.d.add_table(rows=1, cols=1)
        t.style = "Table Grid"
        c = t.rows[0].cells[0]
        _shade(c, "FBF6E9" if couleur == OR_HEX else "E8EEF7")
        c.text = ""
        _runs(c.paragraphs[0], titre, bold=True, color=BLEU, size=12)
        for ligne in texte if isinstance(texte, list) else [texte]:
            _runs(c.add_paragraph(), ligne, size=11)
        self.d.add_paragraph()

    def rgpd(self, lignes):
        self.encadre("🔒 RGPD / IA Act — points de conformité de ce document", lignes)

    def signatures(self, roles):
        t = self.d.add_table(rows=2, cols=len(roles))
        t.style = "Table Grid"
        for i, r in enumerate(roles):
            _runs(t.rows[0].cells[i].paragraphs[0], r, bold=True, size=11)
            _shade(t.rows[0].cells[i], GRIS_HEX)
            _runs(t.rows[1].cells[i].paragraphs[0], "Date :\n\nSignature :\n\n\n", size=11)
        self.d.add_paragraph()

    def saut(self):
        self.d.add_page_break()

    def save(self, chemin_rel):
        out = SORTIE / chemin_rel
        out.parent.mkdir(parents=True, exist_ok=True)
        self.d.save(out)
        return out
