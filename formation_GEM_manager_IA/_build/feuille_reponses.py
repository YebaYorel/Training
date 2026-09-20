# -*- coding: utf-8 -*-
"""Feuille de reponses remplissable a l'ecran (champs de formulaire PDF).
Indispensable a distance : le stagiaire remplit, enregistre et renvoie."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas as cv
from charte import charger
_C = charger()
NUIT  = colors.HexColor(_C["nuit"]);  GRIS = colors.HexColor(_C["gris"])
CLAIR = colors.HexColor(_C["clair"]); TXT  = colors.HexColor(_C["txt"])
ORG   = _C["organisme"]

def feuille(chemin, numero, titre):
    L, H = A4
    c = cv.Canvas(chemin, pagesize=A4)
    c.setTitle("Feuille de réponses — Quiz n°%d" % numero)
    c.setAuthor(ORG)
    c.setFillColor(NUIT); c.rect(0, H - 26*mm, L, 26*mm, stroke=0, fill=1)
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 15)
    c.drawString(18*mm, H - 14*mm, "Feuille de réponses — Quiz n°%d" % numero)
    c.setFont("Helvetica", 10.5); c.setFillColor(colors.HexColor("#D8E0EA"))
    c.drawString(18*mm, H - 20.5*mm, titre)

    c.setFillColor(TXT); c.setFont("Helvetica", 12)
    y = H - 38*mm
    for lib, larg in (("Nom et prénom", 85*mm), ("Date", 45*mm)):
        c.drawString(18*mm, y + 1.5*mm, lib + " :")
        c.acroForm.textfield(name=lib.replace(" ", "_") + "_q%d" % numero,
            tooltip=lib, x=18*mm + 34*mm, y=y - 2*mm, width=larg, height=8*mm,
            borderColor=GRIS, fillColor=colors.white, textColor=TXT,
            forceBorder=True, fontSize=12)
        y -= 13*mm

    c.setFont("Helvetica", 11); c.setFillColor(GRIS)
    c.drawString(18*mm, y, "Questions 1 à 9 : écrivez la lettre (A, B, C ou D), "
                           "ou VRAI / FAUX pour les questions vrai-faux.")
    y -= 10*mm

    c.setFont("Helvetica-Bold", 12); c.setFillColor(TXT)
    x0 = 18*mm
    for i in range(1, 10):
        col, lig = (i - 1) % 3, (i - 1) // 3
        x = x0 + col * 58*mm
        yy = y - lig * 16*mm
        c.setFillColor(TXT); c.setFont("Helvetica-Bold", 12)
        c.drawString(x, yy + 2*mm, "Q%d" % i)
        c.acroForm.textfield(name="Q%d_quiz%d" % (i, numero), tooltip="Question %d" % i,
            x=x + 11*mm, y=yy - 1.5*mm, width=34*mm, height=9*mm,
            borderColor=GRIS, fillColor=colors.white, textColor=TXT,
            forceBorder=True, fontSize=12)
    y -= 3 * 16*mm + 6*mm

    c.setFillColor(TXT); c.setFont("Helvetica-Bold", 12)
    c.drawString(18*mm, y, "Question 10 — réponse rédigée")
    y -= 4*mm
    c.acroForm.textfield(name="Q10_quiz%d" % numero, tooltip="Question 10",
        x=18*mm, y=y - 62*mm, width=L - 36*mm, height=62*mm,
        borderColor=GRIS, fillColor=colors.white, textColor=TXT,
        forceBorder=True, fontSize=11, fieldFlags="multiline")
    y -= 70*mm

    c.setFillColor(CLAIR); c.rect(18*mm, y - 20*mm, L - 36*mm, 18*mm, stroke=0, fill=1)
    c.setFillColor(NUIT); c.setFont("Helvetica-Bold", 10.5)
    c.drawString(21*mm, y - 7*mm, "Comment rendre cette feuille")
    c.setFont("Helvetica", 10.5); c.setFillColor(TXT)
    c.drawString(21*mm, y - 13*mm, "Remplissez les champs, enregistrez le fichier sous votre nom, "
                                   "puis renvoyez-le au formateur.")
    c.drawString(21*mm, y - 18*mm, "Si vous ne pouvez pas l'enregistrer : imprimez, complétez "
                                   "à la main et envoyez une photo.")

    c.setStrokeColor(colors.HexColor("#C3CBD6")); c.setLineWidth(0.7)
    c.line(18*mm, 14*mm, L - 18*mm, 14*mm)
    c.setFont("Helvetica", 9); c.setFillColor(GRIS)
    c.drawString(18*mm, 9*mm, ORG + "  –  " + _C["titre_jour"])
    c.drawRightString(L - 18*mm, 9*mm, "Barème : 9 x 1 pt + 3 pts — seuil 8 / 12")
    c.save()
    print("Feuille de réponses quiz %d : OK" % numero)

feuille("../05_quiz_stagiaires/Feuille_reponses_Quiz_1.pdf", 1, "La psychologie du dirigeant")
feuille("../05_quiz_stagiaires/Feuille_reponses_Quiz_2.pdf", 2, "IA, RGPD et IA Act")
