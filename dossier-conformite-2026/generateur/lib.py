"""Mise en forme commune des documents YEBA FORMATIONS (DOCX accessibles).

Charte YEBA-IDENT-2026 : bleu #1B3A6B pour les titres, noir #121212 pour le texte,
or #C9A84C réservé aux filets et aplats (jamais de texte or sur fond blanc),
Arial 12 pt minimum, interligne 1,3, bloc-marque normalisé en fin de document. Chaque tableau est
contrôlé : si un mot ne tient pas dans sa colonne (mot coupé à l'affichage),
la génération s'arrête avec la liste des cellules fautives.
"""
import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from PIL import ImageFont

RACINE = Path(__file__).resolve().parents[1]
LOGO = RACINE / "assets" / "logo" / "logo_yeba_fond_clair_1000.png"
SORTIE = RACINE / "livrables"

BLEU = RGBColor(0x1B, 0x3A, 0x6B)
OR = RGBColor(0xC9, 0xA8, 0x4C)
NOIR = RGBColor(0x12, 0x12, 0x12)  # corps de texte (charte YEBA-IDENT-2026)
GRIS = RGBColor(0x5A, 0x5F, 0x6A)  # mentions secondaires
BLANC = RGBColor(0xFF, 0xFF, 0xFF)
BLEU_HEX, OR_HEX = "1B3A6B", "C9A84C"
FOND_BLEU, FOND_OR = "E8EEF7", "FBF6E9"

ORGANISME = {
    "nom": "YEBA FORMATIONS",
    "forme": "Entrepreneur individuel (EI)",
    "siret": "814 622 262 00032",
    "siren": "814 622 262",
    "nda": "04973676397",
    "nda_mention": ("Déclaration d'activité n° 04973676397 auprès du Préfet de La Réunion. "
                    "Cet enregistrement ne vaut pas agrément de l'État."),
    "qualiopi": "25FOR02027.1",
    "qualiopi_validite": "du 17/02/2026 au 16/02/2029, sous réserve de l'audit de surveillance",
    "qualiopi_categories": ("actions de formation, bilans de compétences, actions permettant de faire valider les acquis "
                            "de l'expérience, actions de formation par apprentissage"),
    "certificateur": "Qualitia (accrédité COFRAC)",
    "dirigeant": "Aurélien LUMEKA",
    "siege": "9 rue Françoise Châtelain, bâtiment A, entrée 1, porte 0042, 97490 Sainte-Clotilde (Saint-Denis)",
    "siege_court": "9 rue Françoise Châtelain, 97490 Sainte-Clotilde, La Réunion",
    "lieu": "Secrétariat Center — Immeuble Rodrigues 2 — 7 rue Henri Cornu — Parc Technor — 97490 Saint-Denis",
    "lieu_equipement": "entrée, parking, sièges et toilettes accessibles en fauteuil roulant, salle de pause, vidéoprojecteur et tableau",
    "tel": "0693 32 24 45",
    "mail": "yebaformations@gmail.com",
    "ref_handicap": "Aurélien LUMEKA, référent handicap certifié",
    "contact_rgpd": "yebaformations@gmail.com",
    "tva": "TVA non applicable — article 293 B du code général des impôts",
    "assurance": ("HISCOX SA (succursale France, 49 avenue de l'Opéra, 75002 Paris), par l'intermédiaire de Add Value Assurances — "
                  "police n° HRCP300980 — responsabilité civile professionnelle 100 000 € par année d'assurance ; responsabilité civile "
                  "exploitation 10 000 000 € par sinistre — validité du 10/09/2026 au 09/09/2027 — monde entier, sauf États-Unis et Canada"),
}

HORAIRES = {
    "journee": "8 h 00 – 16 h 00",
    "matin": "8 h 00 – 12 h 00 (4 h)",
    "apres_midi": "13 h 00 – 16 h 00 (3 h)",
    "pauses": "10 h 00 – 10 h 15 et 15 h 00 – 15 h 15",
    "dejeuner": "12 h 00 – 13 h 00 (non comptée dans la durée de formation)",
    "duree_jour": 7,
    "location_jour": 100,
}

PLACEHOLDER = re.compile(r"(\[À COMPLÉTER[^\]]*\]|\[À VÉRIFIER[^\]]*\]|_{6,})")

_POLICES = {
    False: ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 100),
    True: ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 100),
}
MARGE_CELLULE_CM = 0.45  # marges internes gauche + droite d'une cellule, avec sécurité
ERREURS_MISE_EN_PAGE = []


def largeur_mot_cm(mot, taille_pt, gras=False):
    """Largeur d'un mot en Arial (métrique identique à Liberation Sans)."""
    return _POLICES[gras].getlength(mot) / 100 * taille_pt * 0.03528


def _verifier_cellule(texte, largeur_cm, taille_pt, gras, ou):
    for mot in re.split(r"\s+", texte.replace("**", "")):
        if mot and largeur_mot_cm(mot, taille_pt, gras) > largeur_cm - MARGE_CELLULE_CM:
            ERREURS_MISE_EN_PAGE.append(f"{ou} : « {mot} » ne tient pas dans {largeur_cm} cm")


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


def _no_split(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:cantSplit")
    el.set(qn("w:val"), "true")
    trPr.append(el)


def _runs(par, texte, bold=False, color=None, size=None):
    """Ajoute du texte : **gras**, champs [À COMPLÉTER] en or foncé gras italique."""
    for morceau in re.split(r"(\*\*[^*]+\*\*)", texte):
        if not morceau:
            continue
        gras = bold or (morceau.startswith("**") and morceau.endswith("**"))
        morceau = morceau[2:-2] if morceau.startswith("**") else morceau
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
                r.bold, r.italic, r.underline = True, True, True
                r.font.color.rgb = BLEU


class Doc:
    def __init__(self, titre, sous_titre="", code="", paysage=False, couverture=False, version="2026-10-v3"):
        self.titre, self.code, self.version = titre, code, version
        self.paysage = paysage
        self.d = Document()
        sec = self.d.sections[0]
        if paysage:
            sec.orientation = WD_ORIENT.LANDSCAPE
            sec.page_width, sec.page_height = Cm(29.7), Cm(21)
        else:
            sec.page_width, sec.page_height = Cm(21), Cm(29.7)
        sec.left_margin = sec.right_margin = Cm(2)
        sec.top_margin, sec.bottom_margin = Cm(1.8), Cm(1.8)
        self.largeur_utile = (25.7 if paysage else 17.0)
        st = self.d.styles["Normal"]
        st.font.name = "Arial"
        st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
        st.font.size = Pt(12)
        st.font.color.rgb = NOIR
        st.paragraph_format.space_after = Pt(6)
        st.paragraph_format.line_spacing = 1.3
        for niv, taille, coul in ((1, 20, BLEU), (2, 16, BLEU), (3, 14, BLEU)):
            h = self.d.styles[f"Heading {niv}"]
            h.font.name, h.font.size, h.font.bold = "Arial", Pt(taille), True
            h.font.color.rgb = coul
            rpr = h.element.get_or_add_rPr()
            rpr.get_or_add_rFonts().set(qn("w:ascii"), "Arial")
            rpr.get_or_add_rFonts().set(qn("w:hAnsi"), "Arial")
            h.paragraph_format.keep_with_next = True
        for nom in ("List Bullet", "List Number"):
            self.d.styles[nom].font.name = "Arial"
            self.d.styles[nom].font.size = Pt(12)
        self.d.core_properties.title = titre
        self.d.core_properties.author = ORGANISME["nom"]
        self.d.core_properties.language = "fr-FR"
        self._entete_pied()
        if couverture:
            self._couverture(titre, sous_titre)
        else:
            self._page_titre(titre, sous_titre)

    def _entete_pied(self):
        sec = self.d.sections[0]
        hp = sec.header.paragraphs[0]
        hp.add_run().add_picture(str(LOGO), height=Cm(1.5))
        r = hp.add_run(f"     {ORGANISME['nom']}   |   NDA {ORGANISME['nda']}   |   Qualiopi {ORGANISME['qualiopi']}")
        r.font.size, r.font.color.rgb, r.bold = Pt(9), BLEU, True
        fp = sec.footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        txt = (f"{self.code}   |   {ORGANISME['nom']} — SIRET {ORGANISME['siret']} — "
               f"Version {self.version}   |   Page ")
        r = fp.add_run(txt)
        r.font.size, r.font.color.rgb = Pt(9), BLEU
        run = fp.add_run()
        for tag, val in (("begin", None), (None, "PAGE"), ("end", None)):
            if tag:
                el = OxmlElement("w:fldChar")
                el.set(qn("w:fldCharType"), tag)
            else:
                el = OxmlElement("w:instrText")
                el.text = val
            run._r.append(el)
        run.font.size, run.font.color.rgb = Pt(9), BLEU

    def _couverture(self, titre, sous_titre):
        p = self.d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(40)
        p.add_run().add_picture(str(LOGO), height=Cm(9 if not self.paysage else 6))
        p = self.d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(24)
        _runs(p, titre, bold=True, color=BLEU, size=26)
        if sous_titre:
            p = self.d.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            _runs(p, sous_titre, bold=True, color=BLEU, size=16)
        self.filet()
        for ligne in (ORGANISME["lieu"], f"SIRET {ORGANISME['siret']}  •  NDA {ORGANISME['nda']}  •  Qualiopi {ORGANISME['qualiopi']}"):
            p = self.d.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            _runs(p, ligne, color=BLEU, size=12)
        self.saut()

    def _page_titre(self, titre, sous_titre):
        p = self.d.add_paragraph()
        _runs(p, titre, bold=True, color=BLEU, size=22)
        if sous_titre:
            p = self.d.add_paragraph()
            _runs(p, sous_titre, color=BLEU, size=14, bold=True)
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

    def p(self, t, bold=False, italic=False, centre=False):
        par = self.d.add_paragraph()
        _runs(par, t, bold=bold)
        if italic:
            for r in par.runs:
                r.italic = True
        if centre:
            par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        return par

    def puces(self, items, style="List Bullet"):
        for it in items:
            _runs(self.d.add_paragraph(style=style), it)

    def numeros(self, items):
        """Liste numérotée en texte (évite la numérotation continue entre listes)."""
        for i, it in enumerate(items, 1):
            par = self.d.add_paragraph()
            par.paragraph_format.left_indent = Cm(0.8)
            par.paragraph_format.first_line_indent = Cm(-0.8)
            _runs(par, f"{i}.  ", bold=True, color=BLEU)
            _runs(par, it)

    def cases(self, items):
        for it in items:
            par = self.d.add_paragraph()
            par.paragraph_format.left_indent = Cm(0.8)
            par.paragraph_format.first_line_indent = Cm(-0.8)
            _runs(par, "☐   " + it)

    def tableau(self, entetes, lignes, largeurs=None, taille=11):
        n = len(entetes)
        largeurs = largeurs or [round(self.largeur_utile / n, 2)] * n
        if abs(sum(largeurs) - self.largeur_utile) > 0.15:
            ERREURS_MISE_EN_PAGE.append(f"{self.code} : largeurs {largeurs} ≠ {self.largeur_utile} cm")
        t = self.d.add_table(rows=1, cols=n)
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for i, e in enumerate(entetes):
            c = t.rows[0].cells[i]
            c.text = ""
            _runs(c.paragraphs[0], str(e), bold=True, color=BLANC, size=taille)
            _shade(c, BLEU_HEX)
            _verifier_cellule(str(e), largeurs[i], taille, True, f"{self.code} en-tête")
        trPr = t.rows[0]._tr.get_or_add_trPr()
        th = OxmlElement("w:tblHeader")
        th.set(qn("w:val"), "true")
        trPr.append(th)
        for k, ligne in enumerate(lignes):
            row = t.add_row()
            _no_split(row)
            for i, v in enumerate(ligne):
                c = row.cells[i]
                c.text = ""
                txt = str(v)
                _runs(c.paragraphs[0], txt, size=taille)
                if k % 2:
                    _shade(c, FOND_BLEU)
                _verifier_cellule(txt, largeurs[i], taille, "**" in txt, f"{self.code} ligne {k + 1}")
        _largeurs(t, largeurs)
        self.d.add_paragraph()
        return t

    def champs(self, libelles, largeurs=(6.5, 10.5)):
        """Formulaire : libellé + zone de saisie."""
        if self.paysage:
            largeurs = (8, 17.7)
        t = self.d.add_table(rows=0, cols=2)
        t.style = "Table Grid"
        for lib in libelles:
            row = t.add_row()
            _no_split(row)
            _runs(row.cells[0].paragraphs[0], lib, bold=True, size=11, color=BLEU)
            _shade(row.cells[0], FOND_BLEU)
            _verifier_cellule(lib, largeurs[0], 11, True, f"{self.code} champ")
        _largeurs(t, list(largeurs))
        self.d.add_paragraph()

    def encadre(self, titre, texte, fond=FOND_OR):
        t = self.d.add_table(rows=1, cols=1)
        t.style = "Table Grid"
        c = t.rows[0].cells[0]
        _shade(c, fond)
        c.text = ""
        _runs(c.paragraphs[0], titre, bold=True, color=BLEU, size=13)
        for ligne in texte if isinstance(texte, list) else [texte]:
            _runs(c.add_paragraph(), ligne, size=11)
        _largeurs(t, [self.largeur_utile])
        self.d.add_paragraph()

    def rgpd(self, lignes):
        self.encadre("RGPD et IA Act — points de conformité de ce document", lignes, fond=FOND_BLEU)

    def signatures(self, roles):
        t = self.d.add_table(rows=2, cols=len(roles))
        t.style = "Table Grid"
        w = round(self.largeur_utile / len(roles), 2)
        for i, r in enumerate(roles):
            _runs(t.rows[0].cells[i].paragraphs[0], r, bold=True, size=11, color=BLEU)
            _shade(t.rows[0].cells[i], FOND_BLEU)
            _verifier_cellule(r, w, 11, True, f"{self.code} signature")
            _runs(t.rows[1].cells[i].paragraphs[0], "Date :\n\nSignature :\n\n\n", size=11)
        _no_split(t.rows[1])
        _largeurs(t, [w] * len(roles))
        self.d.add_paragraph()

    def saut(self):
        self.d.add_page_break()

    def bloc_marque(self):
        """Bloc-marque normalisé (charte YEBA-IDENT-2026, § 4) et mention de transparence IA (§ 7)."""
        self.filet()
        o = ORGANISME
        for i, ligne in enumerate([
            f"{o['nom']} — {o['dirigeant']}, entrepreneur individuel (EI), directeur",
            o["siege_court"],
            f"Tél. {o['tel']} — {o['mail']}",
            f"SIRET {o['siret']}",
            o["nda_mention"],
            f"Certification Qualiopi n° {o['qualiopi']} délivrée au titre des catégories : {o['qualiopi_categories']} — "
            f"organisme certificateur {o['certificateur']}.",
            f"Référent handicap : {o['dirigeant']} — {o['mail']}. Document disponible en 16 points sur simple demande.",
        ]):
            par = self.d.add_paragraph()
            par.paragraph_format.space_after = Pt(0)
            par.paragraph_format.keep_with_next = True
            _runs(par, ligne, bold=(i == 0), color=BLEU if i == 0 else NOIR, size=10)
        par = self.d.add_paragraph()
        par.paragraph_format.space_before = Pt(6)
        _runs(par, "Ce document a été conçu par le formateur avec l'assistance d'un système d'IA générative (règlement (UE) 2024/1689, "
                   "art. 50). Son contenu a été vérifié et validé par un humain, qui en assume la responsabilité.", color=GRIS, size=9)

    def save(self, chemin_rel):
        self.bloc_marque()
        out = SORTIE / chemin_rel
        out.parent.mkdir(parents=True, exist_ok=True)
        self.d.save(out)
        return out
