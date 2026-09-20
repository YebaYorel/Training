# -*- coding: utf-8 -*-
"""Generateur de documents PDF accessibles (corps 13 pt minimum)."""
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, KeepTogether)

from charte import charger, verifier
_C = charger(); verifier(_C)

ORGANISME  = _C["organisme"]
TITRE_JOUR = _C["titre_jour"]

NUIT   = colors.HexColor(_C["nuit"])
ACCENT = colors.HexColor(_C["accent"])
VERT   = colors.HexColor(_C["vert"])
ROUGE  = colors.HexColor(_C["rouge"])
GRIS   = colors.HexColor(_C["gris"])
CLAIR  = colors.HexColor(_C["clair"])
TXT    = colors.HexColor(_C["txt"])

def _pale(hexa, f=0.88):
    """Fond tres clair derive d'une couleur, pour les encadres."""
    c = colors.HexColor(hexa)
    return colors.Color(c.red + (1 - c.red) * f,
                        c.green + (1 - c.green) * f,
                        c.blue + (1 - c.blue) * f)

PALE_ROUGE  = _pale(_C["rouge"])
PALE_VERT   = _pale(_C["vert"])
PALE_ACCENT = _pale(_C["accent"])

def S(nom, taille, **kw):
    base = dict(fontName="Helvetica", fontSize=taille, leading=taille * 1.45,
                textColor=TXT, alignment=TA_LEFT, spaceAfter=taille * 0.45)
    base.update(kw)
    return ParagraphStyle(nom, **base)

ST = {
    "h1":    S("h1", 19, fontName="Helvetica-Bold", textColor=NUIT, spaceAfter=10, spaceBefore=2),
    "h2":    S("h2", 15, fontName="Helvetica-Bold", textColor=ACCENT, spaceBefore=12, spaceAfter=6),
    "h3":    S("h3", 13, fontName="Helvetica-Bold", textColor=NUIT, spaceBefore=8, spaceAfter=4),
    "p":     S("p", 13),
    "pc":    S("pc", 13, alignment=TA_CENTER),
    "puce":  S("puce", 13, leftIndent=12, bulletIndent=2, spaceAfter=4),
    "petit": S("petit", 11, textColor=GRIS),
    "cell":  S("cell", 11.5),
    "cellb": S("cellb", 11.5, fontName="Helvetica-Bold"),
    "cellc": S("cellc", 11.5, alignment=TA_CENTER),
    "enc":   S("enc", 12.5),
}

def _entete(titre, sous):
    def dessiner(canv, doc):
        L, H = doc.pagesize
        canv.saveState()
        canv.setFillColor(NUIT); canv.rect(0, H - 26 * mm, L, 26 * mm, stroke=0, fill=1)
        canv.setFillColor(colors.white); canv.setFont("Helvetica-Bold", 15)
        canv.drawString(18 * mm, H - 14 * mm, titre[:78])
        canv.setFont("Helvetica", 10.5); canv.setFillColor(_pale(_C["nuit"], 0.72))
        canv.drawString(18 * mm, H - 20.5 * mm, sous[:110])
        canv.setStrokeColor(colors.HexColor("#D5DCE6")); canv.setLineWidth(0.7)
        canv.line(18 * mm, 14 * mm, L - 18 * mm, 14 * mm)
        canv.setFont("Helvetica", 9); canv.setFillColor(GRIS)
        canv.drawString(18 * mm, 9 * mm, ORGANISME + "  –  Manager aujourd'hui : posture et intelligence artificielle")
        canv.drawRightString(L - 18 * mm, 9 * mm, "Page %d" % doc.page)
        canv.restoreState()
    return dessiner

def document(chemin, titre, sous, paysage=False):
    fmt = landscape(A4) if paysage else A4
    doc = BaseDocTemplate(chemin, pagesize=fmt,
                          leftMargin=18 * mm, rightMargin=18 * mm,
                          topMargin=32 * mm, bottomMargin=19 * mm,
                          title=titre, author=ORGANISME, subject=sous)
    cadre = Frame(doc.leftMargin, doc.bottomMargin,
                  fmt[0] - 36 * mm, fmt[1] - 51 * mm, id="c",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="p", frames=[cadre], onPage=_entete(titre, sous))])
    return doc

# ------------------------------------------------------------- briques ----
def P(t, st="p"):      return Paragraph(t, ST[st])
def H1(t):             return Paragraph(t, ST["h1"])
def H2(t):             return Paragraph(t, ST["h2"])
def H3(t):             return Paragraph(t, ST["h3"])
def E(h=5):            return Spacer(1, h * mm)
def SAUT():            return PageBreak()

def puces(liste, st="puce", symbole="▪"):
    return [Paragraph(x, ST[st], bulletText=symbole) for x in liste]

def numerote(liste, st="puce"):
    return [Paragraph(x, ST[st], bulletText="%d." % (i + 1)) for i, x in enumerate(liste)]

def encadre(titre, lignes, coul=NUIT, fond=CLAIR):
    corps = [[Paragraph("<b>%s</b>" % titre, S("t", 12.5, fontName="Helvetica-Bold", textColor=coul))]]
    for l in lignes:
        corps.append([Paragraph(l, ST["enc"])])
    t = Table(corps, colWidths=[None])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fond),
        ("LINEBEFORE", (0, 0), (0, -1), 3, coul),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t

def tableau(donnees, largeurs, entete=True, aligns=None, coul=NUIT):
    lignes = []
    for i, rang in enumerate(donnees):
        l = []
        for j, c in enumerate(rang):
            if isinstance(c, str):
                st = "cellb" if (entete and i == 0) else "cell"
                if aligns and aligns[j] == "c" and not (entete and i == 0):
                    st = "cellc"
                para = Paragraph(c, ST[st])
                if entete and i == 0:
                    para = Paragraph('<font color="#FFFFFF"><b>%s</b></font>' % c, ST["cell"])
                l.append(para)
            else:
                l.append(c)
        lignes.append(l)
    t = Table(lignes, colWidths=largeurs, repeatRows=1 if entete else 0)
    style = [
        ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#9AA5B4")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if entete:
        style += [("BACKGROUND", (0, 0), (-1, 0), coul),
                  ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F6F8FB")])]
    t.setStyle(TableStyle(style))
    return t

def source(txt):
    return Paragraph("<i>Source : %s</i>" % txt, ST["petit"])
