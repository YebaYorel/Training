"""Moteur de documents Word conformes à la charte YEBA FORMATIONS (YEBA-IDENT-2026).

- Bleu #1B3A6B pour les titres, or #C9A84C seulement en surfaces et filets.
- Corps 12 pt minimum pour les documents stagiaires, 10 pt pour le contractuel.
- Aucun texte or sur fond blanc (contraste 2,29:1, échec WCAG).
- Tout champ inconnu s'imprime en rouge : on le voit, on ne l'oublie pas.
"""
import subprocess
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from donnees import ORG, A_COMPLETER, ICI

BLEU = RGBColor(0x1B, 0x3A, 0x6B)
OR = RGBColor(0xC9, 0xA8, 0x4C)
NOIR = RGBColor(0x12, 0x12, 0x12)
GRIS = RGBColor(0x5A, 0x5F, 0x6A)
ROUGE = RGBColor(0xC0, 0x00, 0x00)
HEX_BLEU, HEX_OR, HEX_CLAIR, HEX_OR_CLAIR = "1B3A6B", "C9A84C", "F7F7F5", "F4EDDA"
POLICE = "Arial"

MENTION_IA = ("Document conçu par le formateur avec l'assistance d'un système d'IA générative "
              "(règlement (UE) 2024/1689, art. 50). Contenu vérifié et validé par un humain, qui en assume la responsabilité.")
MENTION_EVAL = ("Aucun système d'IA n'est utilisé pour évaluer, noter, classer ou sélectionner les stagiaires : "
                "la correction est réalisée exclusivement par le formateur.")


NBSP = "\u00a0"


def typo(t):
    """Espaces insécables français : jamais de « » ? ! : isolé en début de ligne."""
    for a, b in (("« ", "«" + NBSP), (" »", NBSP + "»"), (" ?", NBSP + "?"), (" !", NBSP + "!"), (" :", NBSP + ":"),
                 (" €", NBSP + "€"), (" %", NBSP + "%")):
        t = t.replace(a, b)
    return t


def _shade(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def _borders(table, color="BFC5CF", size=6):
    tbl = table._tbl
    tblPr = tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), str(size))
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), color)
        b.append(e)
    tblPr.append(b)


def _no_borders(table):
    tblPr = table._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "nil")
        b.append(e)
    tblPr.append(b)


def fixer_largeurs(t, largeurs_cm):
    """Largeurs de colonnes réellement respectées par Word ET LibreOffice."""
    t.autofit = False
    tblPr = t._tbl.tblPr
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
    grid = t._tbl.tblGrid
    for j, gc in enumerate(grid.findall(qn("w:gridCol"))):
        if j < len(largeurs_cm):
            gc.set(qn("w:w"), str(int(largeurs_cm[j] * 567)))
    for row in t.rows:
        for j, w in enumerate(largeurs_cm):
            if j < len(row.cells):
                row.cells[j].width = Cm(w)


def _cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    e = OxmlElement("w:cantSplit")
    trPr.append(e)


def _repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    e = OxmlElement("w:tblHeader")
    trPr.append(e)


def _page_field(paragraph):
    for code in ("PAGE",):
        r = paragraph.add_run()
        f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
        it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = code
        f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "end")
        r._r.append(f1); r._r.append(it); r._r.append(f2)
        r.font.size = Pt(8); r.font.color.rgb = GRIS


class Doc:
    """Document YEBA : en-tête, pied de page normalisé, helpers de mise en forme."""

    def __init__(self, titre, sous_titre="", ref="", corps=12, paysage=False, marque=True,
                 mention_eval=False, entete=True, compact=False):
        self.compact = compact
        self.d = Document()
        self.corps = corps
        st = self.d.styles["Normal"]
        st.font.name = POLICE
        st.element.rPr.rFonts.set(qn("w:eastAsia"), POLICE)
        st.font.size = Pt(corps)
        st.font.color.rgb = NOIR
        st.paragraph_format.line_spacing = 1.3
        st.paragraph_format.space_after = Pt(4)
        sec = self.d.sections[0]
        if paysage:
            sec.orientation = WD_ORIENT.LANDSCAPE
            sec.page_width, sec.page_height = Cm(29.7), Cm(21.0)
        else:
            sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
        for side in ("left_margin", "right_margin"):
            setattr(sec, side, Cm(1.8))
        sec.top_margin, sec.bottom_margin = Cm(1.5), Cm(1.6)
        sec.header_distance, sec.footer_distance = Cm(0.8), Cm(0.6)
        self.largeur = (sec.page_width - sec.left_margin - sec.right_margin)
        if entete:
            self._entete(titre, sous_titre, ref)
        self._pied(marque, mention_eval)

    # ------------------------------------------------------------------ cadre
    def _entete(self, titre, sous_titre, ref):
        t = self.d.add_table(rows=1, cols=2)
        _no_borders(t)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        c0, c1 = t.rows[0].cells
        fixer_largeurs(t, [5.2, self.largeur / 360000 - 5.2])
        p = c0.paragraphs[0]
        p.add_run().add_picture(str(ICI / "logo_1200.png"), width=Cm(2.2 if self.compact else 3.6))
        if not self.compact:
            p2 = c0.add_paragraph()
            r = p2.add_run("YEBA FORMATIONS"); r.bold = True; r.font.size = Pt(11); r.font.color.rgb = BLEU
        c1.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        _shade(c1, HEX_BLEU)
        p = c1.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Cm(0.3)
        r = p.add_run(titre.upper()); r.bold = True; r.font.size = Pt(14 if self.compact else 17); r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        if sous_titre:
            p = c1.add_paragraph(); p.paragraph_format.left_indent = Cm(0.3)
            r = p.add_run(sous_titre); r.font.size = Pt(11); r.font.color.rgb = OR  # or sur bleu : 4,93:1 AA
        if ref:
            p = c1.add_paragraph(); p.paragraph_format.left_indent = Cm(0.3)
            r = p.add_run(ref); r.font.size = Pt(9); r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        self.filet()

    def _pied(self, marque, mention_eval):
        f = self.d.sections[0].footer
        p = f.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if marque:
            txt = (f"{ORG['nom']} — {ORG['dirigeant']}, {ORG['qualite']} — {ORG['adresse']}, {ORG['cp_ville']} — "
                   f"{ORG['tel']} — {ORG['email']} — SIRET {ORG['siret']} — {ORG['nda_mention']} "
                   f"{ORG['qualiopi']}. Référent handicap : {ORG['dirigeant']}.")
            r = p.add_run(txt); r.font.size = Pt(7); r.font.color.rgb = GRIS
        p2 = f.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p2.add_run(MENTION_IA + (" " + MENTION_EVAL if mention_eval else "")); r.italic = True
        r.font.size = Pt(6.5); r.font.color.rgb = GRIS
        p3 = f.add_paragraph(); p3.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r = p3.add_run("Page "); r.font.size = Pt(8); r.font.color.rgb = GRIS
        _page_field(p3)

    # ------------------------------------------------------------- éléments
    def filet(self, couleur=HEX_OR, epaisseur=12):
        p = self.d.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        pPr = p._p.get_or_add_pPr()
        bdr = OxmlElement("w:pBdr")
        b = OxmlElement("w:bottom")
        b.set(qn("w:val"), "single"); b.set(qn("w:sz"), str(epaisseur)); b.set(qn("w:space"), "1"); b.set(qn("w:color"), couleur)
        bdr.append(b); pPr.append(bdr)
        return p

    def h1(self, texte, nouvelle_page=False):
        p = self.d.add_paragraph()
        p.paragraph_format.page_break_before = nouvelle_page
        p.paragraph_format.space_before = Pt(10); p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(texte); r.bold = True; r.font.size = Pt(self.corps + 5); r.font.color.rgb = BLEU
        return p

    def h2(self, texte):
        p = self.d.add_paragraph()
        p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(texte); r.bold = True; r.font.size = Pt(self.corps + 2); r.font.color.rgb = BLEU
        return p

    def p(self, *morceaux, taille=None, align=None, gras=False, italique=False, couleur=None, apres=None):
        """Paragraphe. Chaque morceau est un str ou un tuple (texte, {'b':..,'i':..,'c':RGB}).
        La valeur A_COMPLETER est automatiquement mise en rouge gras."""
        para = self.d.add_paragraph()
        if align == "c":
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif align == "r":
            para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        if apres is not None:
            para.paragraph_format.space_after = Pt(apres)
        for m in morceaux:
            self._run(para, m, taille, gras, italique, couleur)
        return para

    def _run(self, para, m, taille=None, gras=False, italique=False, couleur=None):
        style = {}
        if isinstance(m, tuple):
            m, style = m
        m = typo("" if m is None else str(m))
        # découpe pour colorer les A_COMPLETER
        parts = m.split(A_COMPLETER)
        for i, part in enumerate(parts):
            if part:
                r = para.add_run(part)
                r.bold = style.get("b", gras); r.italic = style.get("i", italique)
                if taille or style.get("t"):
                    r.font.size = Pt(style.get("t", taille))
                c = style.get("c", couleur)
                if c is not None:
                    r.font.color.rgb = c
            if i < len(parts) - 1:
                r = para.add_run(A_COMPLETER); r.bold = True; r.font.color.rgb = ROUGE
                if taille:
                    r.font.size = Pt(taille)

    def puces(self, items, taille=None):
        for it in items:
            para = self.d.add_paragraph(style="List Bullet")
            para.paragraph_format.space_after = Pt(2)
            self._run(para, it, taille)

    def numeros(self, items, taille=None):
        for i, it in enumerate(items, 1):
            para = self.d.add_paragraph()
            para.paragraph_format.left_indent = Cm(0.8); para.paragraph_format.first_line_indent = Cm(-0.6)
            para.paragraph_format.space_after = Pt(2)
            r = para.add_run(f"{i}. "); r.bold = True; r.font.color.rgb = BLEU
            if taille:
                r.font.size = Pt(taille)
            self._run(para, it, taille)

    def table(self, lignes, largeurs_cm=None, entete=True, taille=None, zebre=True, couleur_entete=HEX_BLEU,
              hauteur_cm=None, centre_cols=()):
        nb_col = max(len(l) for l in lignes)
        t = self.d.add_table(rows=0, cols=nb_col)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        _borders(t)
        taille = taille or max(self.corps - 1, 9)
        for i, ligne in enumerate(lignes):
            row = t.add_row()
            _cant_split(row)
            if hauteur_cm:
                row.height = Cm(hauteur_cm)
            for j in range(nb_col):
                cell = row.cells[j]
                cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                val = ligne[j] if j < len(ligne) else ""
                para = cell.paragraphs[0]
                para.paragraph_format.space_after = Pt(1)
                para.paragraph_format.line_spacing = 1.15
                if j in centre_cols:
                    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                if i == 0 and entete:
                    _shade(cell, couleur_entete)
                    r = para.add_run(str(val)); r.bold = True; r.font.size = Pt(taille)
                    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if couleur_entete == HEX_BLEU else NOIR
                else:
                    if zebre and i % 2 == 0:
                        _shade(cell, HEX_CLAIR)
                    items = val if isinstance(val, list) else [val]
                    for k, it in enumerate(items):
                        if k:
                            para = cell.add_paragraph(); para.paragraph_format.space_after = Pt(1)
                        self._run(para, it, taille)
            if i == 0 and entete:
                _repeat_header(row)
        if largeurs_cm:
            fixer_largeurs(t, largeurs_cm)
        self.d.add_paragraph().paragraph_format.space_after = Pt(2)
        return t

    def encadre(self, titre, lignes, fond=HEX_OR_CLAIR, taille=None):
        t = self.d.add_table(rows=1, cols=1)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        _borders(t, color=HEX_OR, size=12)
        c = t.rows[0].cells[0]
        _cant_split(t.rows[0])
        _shade(c, fond)
        para = c.paragraphs[0]
        r = para.add_run(titre); r.bold = True; r.font.color.rgb = BLEU; r.font.size = Pt((taille or self.corps) + 1)
        for l in lignes:
            para = c.add_paragraph(); para.paragraph_format.space_after = Pt(2)
            self._run(para, l, taille)
        self.d.add_paragraph().paragraph_format.space_after = Pt(2)

    def cases(self, options, taille=None):
        para = self.d.add_paragraph()
        for o in options:
            self._run(para, "☐ " + o + "     ", taille)
        return para

    def signatures(self, gauche, droite, hauteur_cm=2.6):
        t = self.d.add_table(rows=1, cols=2)
        _borders(t)
        for cell, txt in zip(t.rows[0].cells, (gauche, droite)):
            lignes = txt if isinstance(txt, list) else [txt]
            para = cell.paragraphs[0]
            self._run(para, (lignes[0], {"b": True}), max(self.corps - 1, 9))
            for l in lignes[1:]:
                para = cell.add_paragraph(); self._run(para, l, max(self.corps - 2, 9))
            para = cell.add_paragraph(); para.paragraph_format.space_after = Pt(0)
            para.paragraph_format.space_before = Pt(0)
        t.rows[0].height = Cm(hauteur_cm)
        w = self.largeur / 360000 / 2
        fixer_largeurs(t, [w, w])
        self.d.add_paragraph().paragraph_format.space_after = Pt(2)

    def saut(self):
        self.d.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    def enregistrer(self, chemin):
        chemin = Path(chemin)
        chemin.parent.mkdir(parents=True, exist_ok=True)
        self.d.save(str(chemin))
        return chemin


def en_pdf(fichiers, dossier=None):
    """Convertit une liste de .docx/.pptx en PDF via LibreOffice (même dossier par défaut)."""
    fichiers = [Path(f) for f in fichiers]
    par_dossier = {}
    for f in fichiers:
        par_dossier.setdefault(dossier or f.parent, []).append(str(f))
    for out, lst in par_dossier.items():
        for i in range(0, len(lst), 25):
            subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(out), *lst[i:i + 25]],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
