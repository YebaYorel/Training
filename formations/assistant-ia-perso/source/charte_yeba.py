"""Charte YEBA FORMATIONS pour les documents PDF (reportlab).

Couleurs et règles reprises de la table CONFIG SYSTEME (Airtable) :
- bleu #1B3A6B, or #C9A84C, noir #121212 ;
- l'or ne touche JAMAIS le blanc en texte (contraste 2,29:1) : réservé aux
  surfaces, filets et au texte sur fond bleu ou noir.
- bloc-marque normalisé obligatoire en pied de tout document sortant.
"""
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether)

BLEU = colors.HexColor("#1B3A6B")
OR = colors.HexColor("#C9A84C")
NOIR = colors.HexColor("#121212")
BLEU_PALE = colors.HexColor("#E8EDF5")
OR_PALE = colors.HexColor("#F6F0DF")
GRIS = colors.HexColor("#4A4A4A")

_F = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("Corps", _F + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Corps-Gras", _F + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Corps-Ital", _F + "LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Corps-GrasItal", _F + "LiberationSans-BoldItalic.ttf"))
pdfmetrics.registerFontFamily("Corps", normal="Corps", bold="Corps-Gras",
                              italic="Corps-Ital", boldItalic="Corps-GrasItal")

TITRE_FORMATION = "Assistant IA perso : Piloter son activité en parlant à son téléphone"

BLOC_MARQUE = (
    "YEBA FORMATIONS — Aurélien LUMEKA, directeur — 9 rue Françoise Châtelain, 97490 Sainte-Clotilde, "
    "La Réunion — Tél. 0693 32 24 45 — yebaformations@gmail.com — SIRET 814 622 262 00032 — "
    "Déclaration d'activité n° 04973676397 auprès du Préfet de La Réunion. Cet enregistrement ne vaut pas "
    "agrément de l'État. — Certification Qualiopi n° 25FOR02027.1 délivrée au titre de la catégorie actions "
    "de formation — organisme certificateur Qualitia (accrédité COFRAC). — Référent handicap : "
    "Aurélien LUMEKA — yebaformations@gmail.com"
)


def styles(base=11.5):
    """Feuille de styles. `base` = corps du texte (11,5 standard, 16 gros caractères)."""
    k = base / 11.5
    s = {}
    s["corps"] = ParagraphStyle("corps", fontName="Corps", fontSize=base, leading=base * 1.45,
                                textColor=NOIR, spaceAfter=base * 0.5, alignment=TA_LEFT)
    s["petit"] = ParagraphStyle("petit", parent=s["corps"], fontSize=base * 0.85, leading=base * 1.2)
    s["puce"] = ParagraphStyle("puce", parent=s["corps"], leftIndent=14 * k, bulletIndent=3 * k,
                               spaceAfter=base * 0.25)
    s["h1"] = ParagraphStyle("h1", fontName="Corps-Gras", fontSize=base * 1.9, leading=base * 2.3,
                             textColor=BLEU, spaceBefore=base * 0.6, spaceAfter=base * 0.7)
    s["h2"] = ParagraphStyle("h2", fontName="Corps-Gras", fontSize=base * 1.35, leading=base * 1.7,
                             textColor=BLEU, spaceBefore=base * 0.9, spaceAfter=base * 0.4)
    s["h3"] = ParagraphStyle("h3", fontName="Corps-Gras", fontSize=base * 1.1, leading=base * 1.45,
                             textColor=NOIR, spaceBefore=base * 0.5, spaceAfter=base * 0.25)
    s["cell"] = ParagraphStyle("cell", fontName="Corps", fontSize=base * 0.88, leading=base * 1.18,
                               textColor=NOIR)
    s["cell_b"] = ParagraphStyle("cell_b", parent=s["cell"], fontName="Corps-Gras")
    s["cell_entete"] = ParagraphStyle("cell_entete", parent=s["cell"], fontName="Corps-Gras",
                                      textColor=colors.white)
    s["couv_titre"] = ParagraphStyle("couv_titre", fontName="Corps-Gras", fontSize=base * 2.5,
                                     leading=base * 3.0, textColor=colors.white)
    s["couv_sous"] = ParagraphStyle("couv_sous", fontName="Corps", fontSize=base * 1.3,
                                    leading=base * 1.7, textColor=OR)
    s["encadre"] = ParagraphStyle("encadre", parent=s["corps"], spaceAfter=base * 0.2)
    s["centre"] = ParagraphStyle("centre", parent=s["corps"], alignment=TA_CENTER)
    return s


def puces(items, s):
    return [Paragraph(t, s["puce"], bulletText="•") for t in items]


def encadre(contenu, s, fond=BLEU_PALE, titre=None):
    """Encadré teinté (pas de bandeau latéral) : liste de flowables ou de chaînes."""
    rows = []
    if titre:
        rows.append([Paragraph(f"<b>{titre}</b>", s["encadre"])])
    for c in contenu:
        rows.append([Paragraph(c, s["encadre"]) if isinstance(c, str) else c])
    t = Table(rows, colWidths=["100%"])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fond),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (0, 0), 8), ("BOTTOMPADDING", (0, -1), (-1, -1), 8),
    ]))
    return KeepTogether([t, Spacer(1, 8)])


def tableau(lignes, s, largeurs, entete=True, zebre=True):
    """Tableau : la 1re ligne est l'en-tête (fond bleu, texte blanc)."""
    data = []
    for i, ligne in enumerate(lignes):
        st = s["cell_entete"] if (entete and i == 0) else s["cell"]
        data.append([Paragraph(str(c), st) if not hasattr(c, "wrap") else c for c in ligne])
    t = Table(data, colWidths=largeurs, repeatRows=1 if entete else 0)
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#B8C2D3")),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if entete:
        style.append(("BACKGROUND", (0, 0), (-1, 0), BLEU))
    if zebre:
        for r in range(1 if entete else 0, len(data)):
            if r % 2 == 0:
                style.append(("BACKGROUND", (0, r), (-1, r), BLEU_PALE))
    t.setStyle(TableStyle(style))
    return t


class DocYeba(BaseDocTemplate):
    """Document A4 avec en-tête (nom du document) et bloc-marque en pied."""

    def __init__(self, chemin, titre_doc, paysage=False, base=11.5, **kw):
        self.taille = landscape(A4) if paysage else A4
        super().__init__(chemin, pagesize=self.taille, title=titre_doc, author="YEBA FORMATIONS",
                         subject=TITRE_FORMATION, lang="fr-FR",
                         leftMargin=18 * mm, rightMargin=18 * mm, topMargin=24 * mm,
                         bottomMargin=30 * mm, **kw)
        self.titre_doc = titre_doc
        self.base = base
        w, h = self.taille
        cadre = Frame(self.leftMargin, self.bottomMargin, w - self.leftMargin - self.rightMargin,
                      h - self.topMargin - self.bottomMargin, id="f")
        self.addPageTemplates([PageTemplate(id="p", frames=[cadre], onPage=self._decor)])

    def _decor(self, c, doc):
        w, h = self.taille
        c.saveState()
        # En-tête : pastille bleue + libellés (texte bleu/noir sur blanc, jamais or)
        c.setFillColor(BLEU)
        c.circle(self.leftMargin + 4, h - 14 * mm, 4, stroke=0, fill=1)
        c.setFillColor(OR)
        c.circle(self.leftMargin + 4, h - 14 * mm, 1.6, stroke=0, fill=1)
        c.setFont("Corps-Gras", 9)
        c.setFillColor(BLEU)
        c.drawString(self.leftMargin + 14, h - 15.2 * mm, "YEBA FORMATIONS")
        c.setFont("Corps", 9)
        c.setFillColor(GRIS)
        c.drawRightString(w - self.rightMargin, h - 15.2 * mm, self.titre_doc)
        # Pied : bloc-marque normalisé (obligatoire) + pagination
        st = ParagraphStyle("pied", fontName="Corps", fontSize=6.6, leading=8, textColor=GRIS)
        p = Paragraph(BLOC_MARQUE, st)
        larg = w - self.leftMargin - self.rightMargin - 40
        _, ph = p.wrap(larg, 30 * mm)
        p.drawOn(c, self.leftMargin, 8 * mm + (18 * mm - ph) / 2)
        c.setFont("Corps-Gras", 9)
        c.setFillColor(BLEU)
        c.drawRightString(w - self.rightMargin, 13 * mm, f"{doc.page}")
        c.restoreState()


def couverture(s, titre, sous_titre, mentions, largeur):
    """Bloc de couverture : aplat bleu, titre blanc, sous-titre or (or sur bleu = AA)."""
    rows = [[Paragraph(titre, s["couv_titre"])],
            [Spacer(1, 6)],
            [Paragraph(sous_titre, s["couv_sous"])]]
    for m in mentions:
        rows.append([Paragraph(m, ParagraphStyle("m", parent=s["corps"], textColor=colors.white))])
    t = Table(rows, colWidths=[largeur])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BLEU),
        ("LEFTPADDING", (0, 0), (-1, -1), 18), ("RIGHTPADDING", (0, 0), (-1, -1), 18),
        ("TOPPADDING", (0, 0), (0, 0), 22), ("BOTTOMPADDING", (0, -1), (-1, -1), 22),
    ]))
    return t
