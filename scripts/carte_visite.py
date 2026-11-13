"""Carte de visite YEBA FORMATIONS — fichier d'impression (PDF).

Format fini 85 x 55 mm, fond perdu 3 mm, traits de coupe.
Pages : 1 recto · 2 verso · 3 masque relief recto · 4 masque relief verso.
Les masques sont en noir 100 % : tout ce qui est noir reçoit le vernis 3D
(ou la dorure à chaud) ; ils se superposent exactement aux pages 1 et 2.

Usage : python scripts/carte_visite.py [dossier_de_sortie]
"""
import sys
from pathlib import Path

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import CMYKColor
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

RACINE = Path(__file__).resolve().parent.parent
POLICES = RACINE / "site/scripts/documents-pdf/polices"
LOGO = RACINE / "site/scripts/documents-pdf/logo-yeba.png"

L, H, FP, MARGE = 85 * mm, 55 * mm, 3 * mm, 8 * mm  # fini, fond perdu, zone d'impression des traits
PAGE = (L + 2 * (FP + MARGE), H + 2 * (FP + MARGE))
X0 = Y0 = FP + MARGE  # coin bas-gauche du format fini

# Charte : bleu #1B3A6B, or #C9AB4C, noir #121212 (conversions CMJN à valider sur épreuve)
BLEU = CMYKColor(0.90, 0.72, 0.25, 0.30)
OR = CMYKColor(0.20, 0.30, 0.78, 0.05)
BLANC = CMYKColor(0, 0, 0, 0)
NOIR = CMYKColor(0, 0, 0, 1)

IDENTITE = {
    "nom": "Aurélien LUMEKA",
    "fonction": "Directeur · Formateur IA",
    "metiers": ["Formation IA", "Solutions & workflows IA", "Conseil RGPD & IA Act"],
    "tel": "0693 32 24 45",
    "mel": "yebaformations@gmail.com",
    "lieu": "Sainte-Clotilde · La Réunion (974)",
    "legal": "Aurélien LUMEKA EI · SIRET 814 622 262 00032 · NDA 04973676397",
    "qualiopi": "Certifié Qualiopi n° 25FOR02027.1 — actions de formation",
}
VCARD = (
    "BEGIN:VCARD\nVERSION:3.0\nN:LUMEKA;Aurélien\nFN:Aurélien LUMEKA\n"
    "ORG:YEBA FORMATIONS\nTITLE:Directeur - Formateur IA\n"
    "TEL;TYPE=CELL:+262693322445\nEMAIL:yebaformations@gmail.com\n"
    "ADR;TYPE=WORK:;;9 rue Françoise Châtelain;Sainte-Clotilde;;97490;La Réunion\nEND:VCARD"
)

for nom in ("Montserrat-Bold", "Montserrat-ExtraBold", "Montserrat-SemiBold"):
    pdfmetrics.registerFont(TTFont(nom, str(POLICES / f"{nom}.ttf")))


def traits_de_coupe(c):
    c.setStrokeColor(CMYKColor(1, 1, 1, 1))  # repérage
    c.setLineWidth(0.25)
    d, lg = FP + 1 * mm, 4 * mm
    for x in (X0, X0 + L):
        c.line(x, Y0 - d, x, Y0 - d - lg)
        c.line(x, Y0 + H + d, x, Y0 + H + d + lg)
    for y in (Y0, Y0 + H):
        c.line(X0 - d, y, X0 - d - lg, y)
        c.line(X0 + L + d, y, X0 + L + d + lg, y)


def legende(c, texte):
    c.setFillColor(NOIR)
    c.setFont("Montserrat-SemiBold", 5)
    c.drawString(X0 - FP, 2.2 * mm, texte)


def reseau(c, couleur, epaisseur=0.35):
    """Motif « réseau de points reliés » de la charte, dans l'angle bas-droit du verso."""
    pts = [(68, 3.5), (66, 14), (75, 5), (80, 17), (71, 24), (83, 30), (62, 22)]
    liens = [(0, 1), (1, 2), (1, 4), (2, 3), (3, 4), (3, 5), (4, 5), (1, 6), (4, 6)]
    c.setStrokeColor(couleur)
    c.setFillColor(couleur)
    c.setLineWidth(epaisseur)
    for a, b in liens:
        c.line(X0 + pts[a][0] * mm, Y0 + pts[a][1] * mm, X0 + pts[b][0] * mm, Y0 + pts[b][1] * mm)
    for x, y in pts:
        c.circle(X0 + x * mm, Y0 + y * mm, 0.75 * mm, stroke=0, fill=1)


def qr(c, x, y, cote, couleur):
    w = QrCodeWidget(VCARD, barLevel="M", barFillColor=couleur, barBorder=0)
    b = w.getBounds()
    ech = cote / (b[2] - b[0])
    d = Drawing(cote, cote, transform=[ech, 0, 0, ech, 0, 0])
    d.add(w)
    renderPDF.draw(d, c, x, y)


def recto(c, masque=False):
    if not masque:
        c.setFillColor(BLANC)
        c.rect(X0 - FP, Y0 - FP, L + 2 * FP, H + 2 * FP, stroke=0, fill=1)
        lw = 34 * mm
        lh = lw * 657 / 771
        c.drawImage(str(LOGO), X0 + (L - lw) / 2, Y0 + 15.5 * mm, lw, lh, mask="auto")
    # filet or + signature : zone en relief
    c.setFillColor(NOIR if masque else OR)
    c.rect(X0 + 27.5 * mm, Y0 + 11.6 * mm, 30 * mm, 0.5 * mm, stroke=0, fill=1)
    c.setFillColor(NOIR if masque else BLEU)
    c.setFont("Montserrat-SemiBold", 7)
    c.drawCentredString(X0 + L / 2, Y0 + 6.6 * mm, "FORMATION · SOLUTIONS IA · GOUVERNANCE")
    if masque:  # le logo reçoit le vernis en relief : pavé de la taille exacte du logo
        lw = 34 * mm
        c.rect(X0 + (L - lw) / 2, Y0 + 15.5 * mm, lw, lw * 657 / 771, stroke=0, fill=1)


def verso(c, masque=False):
    i = IDENTITE
    if not masque:
        c.setFillColor(BLEU)
        c.rect(X0 - FP, Y0 - FP, L + 2 * FP, H + 2 * FP, stroke=0, fill=1)
        reseau(c, CMYKColor(0.20, 0.30, 0.78, 0.05, alpha=0.55))
    gx = X0 + 6 * mm
    # Nom : relief
    c.setFillColor(NOIR if masque else BLANC)
    c.setFont("Montserrat-ExtraBold", 13)
    c.drawString(gx, Y0 + 44.5 * mm, i["nom"])
    c.setFillColor(NOIR if masque else OR)
    c.rect(gx, Y0 + 42.2 * mm, 14 * mm, 0.6 * mm, stroke=0, fill=1)
    if masque:
        return
    c.setFillColor(OR)
    c.setFont("Montserrat-Bold", 7.5)
    c.drawString(gx, Y0 + 38.2 * mm, i["fonction"])
    c.setFillColor(BLANC)
    c.setFont("Montserrat-SemiBold", 7)
    y = Y0 + 32.6 * mm
    for m in i["metiers"]:
        c.drawString(gx, y, m)
        y -= 3.5 * mm
    c.setFont("Montserrat-Bold", 9.5)
    c.drawString(gx, Y0 + 18.6 * mm, i["tel"])
    c.setFont("Montserrat-SemiBold", 7.5)
    c.drawString(gx, Y0 + 14.6 * mm, i["mel"])
    c.drawString(gx, Y0 + 11.2 * mm, i["lieu"])
    c.setFont("Montserrat-SemiBold", 4.6)
    c.drawString(gx, Y0 + 6.6 * mm, i["legal"])
    c.drawString(gx, Y0 + 4.5 * mm, i["qualiopi"])
    # QR vCard sur cartouche blanc (lecture fiable)
    cote = 17 * mm
    qx, qy = X0 + L - 6 * mm - cote, Y0 + H - 6 * mm - cote
    c.setFillColor(BLANC)
    c.roundRect(qx - 1.2 * mm, qy - 1.2 * mm, cote + 2.4 * mm, cote + 2.4 * mm, 1 * mm, stroke=0, fill=1)
    qr(c, qx, qy, cote, BLEU)


def main():
    sortie = Path(sys.argv[1]) if len(sys.argv) > 1 else RACINE / "livrables-prives/carte-visite"
    sortie.mkdir(parents=True, exist_ok=True)
    fichier = sortie / "YEBA-carte-de-visite-impression.pdf"
    c = canvas.Canvas(str(fichier), pagesize=PAGE)
    c.setTitle("YEBA FORMATIONS — carte de visite 85 x 55 mm")
    c.setAuthor("YEBA FORMATIONS")
    for dessin, masque, texte in (
        (recto, False, "1/4 RECTO — quadri — 85 x 55 mm fini, fond perdu 3 mm"),
        (verso, False, "2/4 VERSO — quadri — 85 x 55 mm fini, fond perdu 3 mm"),
        (recto, True, "3/4 MASQUE RELIEF RECTO — noir 100 % = vernis 3D (logo, filet, signature)"),
        (verso, True, "4/4 MASQUE RELIEF VERSO — noir 100 % = vernis 3D ou dorure à chaud (nom, filet)"),
    ):
        dessin(c, masque)
        traits_de_coupe(c)
        legende(c, texte)
        c.showPage()
    c.save()
    print(fichier)


if __name__ == "__main__":
    main()
