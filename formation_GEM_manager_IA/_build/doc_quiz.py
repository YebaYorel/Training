# -*- coding: utf-8 -*-
from docs_engine import *
from quiz_data import QUIZ1, QUIZ2
from reportlab.platypus import Paragraph, Table, TableStyle

LETTRES = "ABCD"

def bloc_identite():
    t = tableau([["Nom et prénom :", "", "Date :", ""]],
                [34*mm, None, 20*mm, 34*mm], entete=False)
    t.setStyle(TableStyle([("TOPPADDING", (0,0), (-1,-1), 9),
                           ("BOTTOMPADDING", (0,0), (-1,-1), 9)]))
    return t

def feuille_quiz(chemin, numero, titre_partie, questions, consigne):
    f = [H1("Quiz n°%d — %s" % (numero, titre_partie))]
    f += [bloc_identite(), E(4)]
    f += [encadre("Consigne", consigne)]
    f += [E(5)]
    for i, q in enumerate(questions, 1):
        bloc = [Paragraph("<b>Question %d.</b> %s" % (i, q[1]), ST["p"])]
        if q[0] == "QCM":
            for j, op in enumerate(q[2]):
                bloc.append(Paragraph("%s.  %s" % (LETTRES[j], op), ST["puce"], bulletText="❑"))
        elif q[0] == "VF":
            bloc.append(Paragraph("❑&nbsp;&nbsp;VRAI&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;❑&nbsp;&nbsp;FAUX", ST["puce"]))
        else:
            t = Table([[""], [""], [""], [""], [""]], colWidths=[174*mm], rowHeights=[8*mm]*5)
            t.setStyle(TableStyle([("LINEBELOW", (0,0), (-1,-1), 0.5, colors.HexColor("#9AA5B4"))]))
            bloc.append(E(2)); bloc.append(t)
        bloc.append(E(3))
        f.append(KeepTogether(bloc))
    f += [E(4), P("<b>Barème :</b> 9 questions fermées à 1 point + 1 question ouverte "
                  "sur 3 points. Total : 12 points. Seuil d'acquisition : 8 / 12.", "petit")]
    doc = document(chemin, "Quiz n°%d — %s" % (numero, titre_partie),
                   "Feuille stagiaire — à rendre au formateur")
    doc.build(f)
    print("Quiz %d : OK" % numero)

def feuille_corrige(chemin, numero, titre_partie, questions):
    f = [H1("CORRIGÉ — Quiz n°%d : %s" % (numero, titre_partie))]
    f += [encadre("Document formateur", [
        "Feuille distincte de la feuille stagiaire. À ne pas distribuer avant la correction.",
        "Barème : 9 questions fermées à 1 point, 1 question ouverte sur 3 points — total 12 points.",
        "Seuil d'acquisition : 8 / 12. En dessous, reprendre en priorité les items ratés."],
        coul=ROUGE, fond=PALE_ROUGE)]
    f += [E(5)]
    lignes = [["N°", "Réponse attendue", "Justification à donner au groupe"]]
    for i, q in enumerate(questions, 1):
        if q[0] == "QCM":
            rep = "<b>%s</b> — %s" % (LETTRES[q[3]], q[2][q[3]])
        elif q[0] == "VF":
            rep = "<b>%s</b>" % ("VRAI" if q[3] else "FAUX")
        else:
            rep = "<b>Question ouverte</b><br/>(3 points)"
        lignes.append([str(i), rep, q[4]])
    f += [tableau(lignes, [10*mm, 52*mm, None])]
    f += [E(5), H2("Points de vigilance à l'oral")]
    if numero == 1:
        f += puces([
            "Question 2 : insister sur le fait que « directif » n'est ni brutal ni définitif.",
            "Question 6 : c'est souvent la question la plus ratée. Prendre le temps.",
            "Question 10 : accepter toute formulation équivalente. On évalue le raisonnement, "
            "pas le vocabulaire technique."])
    else:
        f += puces([
            "Question 4 : la confusion « interdit » / « haut risque » est la plus fréquente. "
            "Rappeler qu'un accord ne rend jamais licite une pratique interdite.",
            "Question 8 : le mot « exclusivement » est le cœur de la réponse.",
            "Question 10 : valoriser la réponse qui pose la question avant de décider, "
            "même si la décision finale diffère de la nôtre."])
    f += [E(4), P("Rappel : ce corrigé renvoie à des textes qui évoluent. Vérifier les "
                  "références à la date de la session (Légifrance, Journal officiel de l'UE, CNIL).",
                  "petit")]
    doc = document(chemin, "CORRIGÉ — Quiz n°%d" % numero,
                   "Document formateur — feuille distincte, ne pas distribuer")
    doc.build(f)
    print("Corrige %d : OK" % numero)

feuille_quiz("../05_quiz_stagiaires/Quiz_1_Psychologie_du_dirigeant.pdf", 1,
             "La psychologie du dirigeant", QUIZ1,
             ["Durée : 10 minutes. Documents fermés.",
              "Une seule réponse par question fermée. Cochez la case correspondante.",
              "La dernière question est ouverte : répondez avec vos mots, en 4 lignes maximum."])
feuille_quiz("../05_quiz_stagiaires/Quiz_2_IA_RGPD_IA_Act.pdf", 2,
             "IA, RGPD et IA Act", QUIZ2,
             ["Durée : 10 minutes. Documents fermés.",
              "Une seule réponse par question fermée. Cochez la case correspondante.",
              "La dernière question est une mise en situation : raisonnez à voix écrite."])
feuille_corrige("../06_corriges/CORRIGE_Quiz_1_Psychologie_du_dirigeant.pdf", 1,
                "La psychologie du dirigeant", QUIZ1)
feuille_corrige("../06_corriges/CORRIGE_Quiz_2_IA_RGPD_IA_Act.pdf", 2,
                "IA, RGPD et IA Act", QUIZ2)
