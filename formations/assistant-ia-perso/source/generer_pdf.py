"""Génère les documents PDF de la formation dans le dossier parent.

Usage : python generer_pdf.py   (nécessite : pip install reportlab)
"""
from pathlib import Path

from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, Spacer, KeepTogether

import contenu as C
from charte_yeba import (DocYeba, styles, puces, encadre, tableau, couverture, OR_PALE,
                         BLEU_PALE, TITRE_FORMATION)
from ressource import R

SORTIE = Path(__file__).resolve().parent.parent


def _l(doc):
    return doc.width


def _cm(lst):
    return [x * cm for x in lst]


# ---------------------------------------------------------------- Programme
def programme():
    doc = DocYeba(str(SORTIE / "01_Programme_de_formation.pdf"), "Programme de formation")
    s = styles()
    E = [couverture(s, TITRE_FORMATION, "Programme de formation — 2 jours, 16 heures",
                    ["Présentiel — inter-entreprise ou intra-entreprise — 4 à 8 stagiaires"], _l(doc)),
         Spacer(1, 12)]
    E += [Paragraph("Public visé", s["h2"])] + [Paragraph(x, s["corps"]) for x in C.PUBLIC.split("\n") if x]
    E += [Paragraph("Prérequis", s["h2"]), Paragraph(C.PREREQUIS, s["corps"])]
    E += [Paragraph("Objectifs pédagogiques", s["h2"]),
          Paragraph("À l'issue de la formation, le stagiaire sera capable de :", s["corps"])]
    E.append(tableau([["", "Niveau", "Objectif", "Indicateur de réussite"]] +
                     [[f"<b>{c}</b>", n, o, sm] for c, n, o, sm in C.OBJECTIFS], s, _cm([1.2, 2.3, 6.8, 6.1])))
    E += [Paragraph("Durée et horaires", s["h2"]), Paragraph(C.HORAIRES, s["corps"])]
    E += [Paragraph("Contenu", s["h2"])]
    jour = None
    for j, h, titre, cont, *_ in C.DEROULE:
        if j != jour:
            jour = j
            E.append(Paragraph(f"Journée {j[1]}", s["h3"]))
        if not cont:
            continue
        E.append(KeepTogether([Paragraph(f"<b>{h} — {titre}</b>", s["corps"])] + puces(cont, s)))
    E += [Paragraph("Méthodes et moyens pédagogiques", s["h2"])]
    E += puces(["30 % d'apport, 70 % de pratique, sur le smartphone de chaque stagiaire.",
                "Comparaison systématique voie américaine (Claude) / voie européenne (Le Chat, Baserow).",
                "Environnement de démonstration fourni (entreprise fictive KAZ'MARKET) : aucune donnée réelle de "
                "client manipulée en séance.",
                "5 jeux pédagogiques, études de cas, ateliers individuels et en binôme.",
                "Support projeté accessible, livret ressource (standard et gros caractères), kit « assistant sous "
                "contrôle ».",
                "Formateur : Aurélien LUMEKA — Google AI Specialist, SecNumacadémie (ANSSI), MOOC RGPD de la CNIL, "
                "référent handicap."], s)
    E += [Paragraph("Modalités d'évaluation", s["h2"])]
    for bloc in C.EVALUATION.split("\n\n"):
        E.append(Paragraph(bloc.replace("\n", "<br/>"), s["corps"]))
    E += [Paragraph("Accessibilité et adaptations", s["h2"]), Paragraph(C.ADAPTATIONS, s["corps"])]
    E += [Paragraph("Délai et modalités d'accès", s["h2"]), Paragraph(C.DELAI_ACCES, s["corps"])]
    E += [Paragraph("Tarifs et financement", s["h2"]),
          Paragraph("<b>Inter-entreprise</b> : 1 780 € par personne pour le parcours complet de 16 heures "
                    "(890 € par jour et par personne).", s["corps"]),
          Paragraph("<b>Intra-entreprise</b> : 5 400 € pour le groupe, jusqu'à 8 stagiaires (2 700 € par jour).",
                    s["corps"]),
          Paragraph("Inclus : questionnaire de positionnement, environnement de démonstration, livret ressource, "
                    "kit « assistant sous contrôle » et classe virtuelle de suivi d'1 heure à J+30. Prix nets de "
                    "taxe — TVA non applicable, article 293 B du code général des impôts.", s["corps"]),
          Paragraph("Financements possibles selon votre situation : OPCO, plan de développement des compétences, "
                    "France Travail (AIF), Région. Cette formation ne porte pas de code RNCP ou RS : elle n'est "
                    "<b>pas</b> éligible au CPF.", s["corps"])]
    doc.build(E)


# ---------------------------------------------------------------- Déroulé
def deroule():
    doc = DocYeba(str(SORTIE / "02_Deroule_pedagogique.pdf"), "Déroulé pédagogique", paysage=True)
    s = styles(10.5)
    E = [Paragraph("Déroulé pédagogique", s["h1"]),
         Paragraph(f"<b>{TITRE_FORMATION}</b> — 2 jours, 16 heures — 4 à 8 stagiaires — présentiel", s["corps"]),
         Paragraph("Pauses de 15 minutes à 10h00 et 15h00 incluses dans le temps de formation ; pause méridienne "
                   "12h00–13h00 hors temps de formation.", s["corps"]), Spacer(1, 6)]
    for jour in ("J1", "J2"):
        E.append(Paragraph(f"Journée {jour[1]}", s["h2"]))
        lignes = [["Horaire", "Séquence et contenus", "Obj.", "Méthode", "Supports et outils", "Évaluation"]]
        for j, h, titre, cont, obj, meth, sup, ev in C.DEROULE:
            if j != jour:
                continue
            if not cont:
                lignes.append([h, f"<i>{titre}</i>", "", "", "", ""])
                continue
            txt = f"<b>{titre}</b><br/>" + "<br/>".join("• " + c for c in cont)
            lignes.append([h, txt, obj, meth, sup, ev])
        E.append(tableau(lignes, s, _cm([2.4, 11.6, 1.5, 3.6, 3.9, 3.5])))
    E += [Spacer(1, 8), Paragraph("Matériel à préparer", s["h2"])]
    E += puces(["Vidéoprojecteur, micro-cravate, enceinte (démonstrations vocales audibles de tous).",
                "Smartphone du formateur relié au vidéoprojecteur (recopie d'écran).",
                "Comptes de démonstration KAZ'MARKET : messagerie, agenda, base de données — créés et testés à J-3.",
                "Réseau Wi-Fi testé sur le lieu (prévoir un partage de connexion de secours).",
                "Jeux : 10 cartes A5 (jeu 1), cartes consignes (jeu 2), tâches chronométrées (jeu 3), grilles de bingo "
                "(jeu 4), dossier d'enquête et 5 enveloppes (jeu 5).",
                "Impressions : grille critériée (1 par stagiaire), quiz, plan d'action, livret en gros caractères "
                "si demandé.",
                "Feuilles d'émargement par demi-journée."], s)
    doc.build(E)


# ---------------------------------------------------------------- Ressource
def ressource(gros=False):
    nom = "04_Ressource_stagiaire_GROS_CARACTERES.pdf" if gros else "04_Ressource_stagiaire.pdf"
    base = 16 if gros else 11.5
    doc = DocYeba(str(SORTIE / nom), "Livret ressource stagiaire", base=base)
    s = styles(base)
    larg = doc.width
    E = [couverture(s, TITRE_FORMATION, "Livret ressource stagiaire",
                    ["Construire, utiliser et sécuriser son assistant IA personnel",
                     "Version du 02/10/2026" + (" — gros caractères (corps 16)" if gros else "")], larg),
         Spacer(1, 14)]
    premier = True
    for typ, val in R:
        if typ == "h1":
            if not premier:
                E.append(PageBreak())
            premier = False
            E.append(Paragraph(val, s["h1"]))
        elif typ == "h2":
            E.append(Paragraph(val, s["h2"]))
        elif typ == "h3":
            E.append(Paragraph(val, s["h3"]))
        elif typ == "p":
            E.append(Paragraph(val, s["corps"]))
        elif typ == "puces":
            E += puces(val, s)
        elif typ == "encadre":
            titre, lignes = val
            fond = OR_PALE if titre.lower().startswith("réflexe") else BLEU_PALE
            E.append(encadre(lignes, s, fond=fond, titre=titre))
        elif typ == "tableau":
            largeurs, lignes = val
            tot = sum(largeurs)
            E.append(tableau(lignes, s, [larg * x / tot for x in largeurs]))
            E.append(Spacer(1, 8))
    doc.build(E)


# ---------------------------------------------------------------- Grille
def grille():
    doc = DocYeba(str(SORTIE / "05_Grille_evaluation_criteriee.pdf"), "Grille d'évaluation critériée", paysage=True)
    s = styles(10.5)
    E = [Paragraph("Grille d'évaluation critériée — 5 critères", s["h1"]),
         Paragraph(f"<b>{TITRE_FORMATION}</b>", s["corps"]),
         Paragraph("Stagiaire : ........................................................   Session : "
                   "................................   Date : ...... / ...... / ............", s["corps"]),
         Spacer(1, 6)]
    lignes = [["Critère"] + C.NIVEAUX + ["Niveau atteint"]]
    for code, lib, bloquant, desc in C.GRILLE:
        lignes.append([f"<b>{code} — {lib}</b>"] + desc + ["☐ 0   ☐ 1<br/>☐ 2   ☐ 3"])
    E.append(tableau(lignes, s, _cm([5.2, 4.4, 4.4, 4.4, 4.4, 2.7])))
    E += [Spacer(1, 8), Paragraph("Règles de décision", s["h2"])]
    E += puces(["Total sur 15 points. <b>Acquis</b> : 10 points et plus, et aucun critère à 0.",
                "<b>Maîtrisé</b> : 13 points et plus, et C4 et C5 au niveau 3.",
                "<b>Critères bloquants C4 et C5</b> : un niveau « non acquis » (0) sur l'un d'eux empêche la mention "
                "« acquis », quel que soit le total. On ne compense pas un risque juridique ou de sécurité par de la "
                "performance technique.",
                "Le quiz (seuil 7/10) complète la grille ; il ne la remplace pas.",
                "Aucun système d'IA n'intervient dans la notation : la décision appartient au formateur "
                "(IA Act, annexe III, point 3)."], s)
    E += [Spacer(1, 6), Paragraph("Total : ........ / 15     Quiz : ........ / 10     Résultat : ☐ Non acquis   "
                                  "☐ Acquis   ☐ Maîtrisé", s["h3"]),
          Paragraph("Commentaire du formateur : ..........................................................................."
                    "..........................................................................................", s["corps"]),
          Paragraph("Signature du formateur :                                         Signature du stagiaire :",
                    s["corps"])]
    doc.build(E)


# ---------------------------------------------------------------- Quiz
def quiz(corrige=False):
    nom = "07_Quiz_CORRIGE.pdf" if corrige else "06_Quiz_evaluation_sommative.pdf"
    titre = "Quiz — corrigé (réservé au formateur)" if corrige else "Quiz — évaluation sommative"
    doc = DocYeba(str(SORTIE / nom), titre)
    s = styles(12)
    E = [Paragraph(titre, s["h1"]), Paragraph(f"<b>{TITRE_FORMATION}</b>", s["corps"])]
    if not corrige:
        E += [Paragraph("Nom et prénom : ..............................................   Date : ...... / ...... / "
                        "............", s["corps"]),
              encadre(["10 questions, une seule bonne réponse par question. Entourez la lettre choisie.",
                       "Durée : 20 minutes (temps majoré sur demande). Seuil de réussite : 7 bonnes réponses sur 10.",
                       "Le quiz est corrigé et commenté en groupe juste après."], s)]
    else:
        E.append(encadre(["Seuil de réussite : 7/10. Correction commentée en groupe : faire expliquer chaque bonne "
                          "réponse par un stagiaire avant de lire l'explication."], s, fond=OR_PALE))
        tab = [["Question"] + [str(i) for i in range(1, 11)], ["Réponse"] + [q[2] for q in C.QUIZ]]
        E.append(tableau(tab, s, [2.4 * cm] + [1.3 * cm] * 10))
        E.append(Spacer(1, 10))
    for i, (q, choix, bonne, expl) in enumerate(C.QUIZ, 1):
        bloc = [Paragraph(f"<b>Question {i}.</b> {q}", s["corps"])]
        for lettre, c in zip("ABCD", choix):
            if corrige and lettre == bonne:
                bloc.append(Paragraph(f"<b>{lettre}. {c}   ✔ BONNE RÉPONSE</b>", s["puce"]))
            else:
                bloc.append(Paragraph(f"{lettre}. {c}", s["puce"]))
        if corrige:
            bloc.append(Paragraph(f"<i>Explication : {expl}</i>", s["corps"]))
        bloc.append(Spacer(1, 6))
        E.append(KeepTogether(bloc))
    if not corrige:
        E.append(Paragraph("Score : ........ / 10", s["h2"]))
    doc.build(E)


# ---------------------------------------------------------------- Jeux
def jeux():
    doc = DocYeba(str(SORTIE / "08_Jeux_pedagogiques.pdf"), "Jeux pédagogiques — fiches formateur")
    s = styles(11.5)
    E = [Paragraph("Jeux pédagogiques — fiches formateur", s["h1"]),
         Paragraph(f"<b>{TITRE_FORMATION}</b>", s["corps"]),
         Paragraph("Cinq jeux pour apprendre en s'amusant : chacun est relié à un objectif pédagogique et se termine "
                   "par un débriefing qui ancre la règle. Tous ont une variante accessible.", s["corps"])]
    for i, j in enumerate(C.JEUX):
        if i:
            E.append(PageBreak())
        E.append(Paragraph(j["nom"], s["h2"]))
        E.append(tableau([["Moment", "Objectif", "Matériel"], [j["moment"], j["objectif"], j["materiel"]]], s,
                         _cm([4.2, 2.0, 10.2])))
        E.append(Paragraph("Déroulé", s["h3"]))
        E += puces(j["deroule"], s)
        if j["cartes"]:
            E.append(Paragraph("Contenu (cartes, cases, failles)", s["h3"]))
            E += puces(j["cartes"], s)
        E.append(encadre([j["debrief"]], s, titre="Débriefing — la règle à retenir"))
        E.append(encadre([j["adaptation"]], s, fond=OR_PALE, titre="Variante accessible"))
    doc.build(E)


if __name__ == "__main__":
    programme()
    deroule()
    ressource()
    ressource(gros=True)
    grille()
    quiz()
    quiz(corrige=True)
    jeux()
    print("PDF générés dans", SORTIE)
