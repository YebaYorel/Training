"""Audit des 32 indicateurs Qualiopi pour l'action Marilyn Institut + fiches manquantes créées.

Référentiel : décret n° 2019-564 du 6 juin 2019 relatif à la qualité des actions de la formation professionnelle,
et guide de lecture du Référentiel national qualité (ministère du Travail). Organisme certifié « actions de formation »
uniquement : les indicateurs propres aux CFA, bilans de compétences, VAE et certifications ne s'appliquent pas.
"""
import donnees as D
from docx_lib import Doc, BLEU, ROUGE

OUT = D.SORTIE / "06_QUALIOPI_ET_OPCO"
OK, AF, MQ, NA = "✔ Réalisé", "⚠ À compléter", "✘ Créé ce jour", "— Non applicable"

INDICATEURS = [
    (1, "Information du public (prérequis, objectifs, durée, tarifs, contacts, accessibilité)", OK,
     "Programme FOR-0007, devis, livret d'accueil.", "Vérifier que la fiche publique est en ligne et à jour sur www.yebaformations.re (ou retirer la mention « sous-traitance » d'Airtable si l'action est bien en direct)."),
    (2, "Indicateurs de résultats publiés", MQ, "Première action : aucun résultat à publier encore.",
     "Remplir le « Tableau des indicateurs de résultats » après les sessions et le publier sur le site."),
    (3, "Taux d'obtention des certifications", NA, "Action non certifiante.", ""),
    (4, "Analyse du besoin avec l'entreprise et le financeur", AF, "Devis, convention, échanges avec Sarah MACHON (courriels du 17 et 23/09).",
     "Compléter et faire signer la « Fiche d'analyse du besoin » créée ce jour."),
    (5, "Objectifs opérationnels et évaluables", OK, "10 objectifs de la fiche FOR-0007 (annexe 1 de la convention), repris sur l'attestation.", ""),
    (6, "Contenus et modalités de mise en œuvre adaptés", OK, "Programme, diaporama, conducteur, kit, ressource.", ""),
    (7, "Adéquation contenus / exigences d'une certification", NA, "Action non certifiante.", ""),
    (8, "Positionnement et évaluation des acquis à l'entrée", OK, "Questionnaire Drag'n Survey (5/8), fiche Indicateur 8, positionnement express.",
     D.vigilance("ind8")),
    (9, "Information sur les conditions de déroulement", AF, "Convocations, livret, règlement, notice RGPD.",
     D.vigilance("ind9")),
    (10, "Adaptation de la prestation et de l'accompagnement", OK, "Fiche Indicateur 8, section 3 : 11 adaptations tracées.", ""),
    (11, "Évaluation de l'atteinte des objectifs", OK, "Grille critériée, quiz, positionnement matin/soir, attestation avec résultats.", ""),
    (12, "Engagement des bénéficiaires et prévention des abandons", OK, "Pédagogie active (71 % de pratique), relance des non-répondantes, procédure retard/absence.", ""),
    (13, "Coordination des acteurs de l'alternance", NA, "Pas d'action en alternance.", ""),
    (14, "Accompagnement socio-professionnel des apprentis", NA, "Réservé aux CFA.", ""),
    (15, "Information des apprentis sur leurs droits", NA, "Réservé aux CFA.", ""),
    (16, "Conditions de présentation à la certification", NA, "Action non certifiante.", ""),
    (17, "Moyens humains, techniques et locaux adaptés", AF, "Salle « SEYCHELLES » du C.R.E.P.S (convention, art. 2 et 4).",
     "Conserver la preuve de réservation de la salle (à la charge du client selon le devis) et vérifier l'accessibilité PMR."),
    (18, "Coordination des intervenants", OK, "Formateur unique, référent pédagogique et handicap identifiés.", ""),
    (19, "Ressources pédagogiques mises à disposition", OK, "Ressource stagiaire, kit, phrases d'appui, livrables co-construits.", ""),
    (20, "Référents (pédagogique, handicap, administratif) et ressources", OK, "Livret d'accueil, rubrique 2.", ""),
    (21, "Compétences des intervenants", AF, "Titre professionnel FPA (2021), expérience vente et management.",
     "Tenir au dossier le CV et les justificatifs à jour du formateur (la convention dit « communiqués sur demande »)."),
    (22, "Développement des compétences des salariés de l'organisme", OK, "Plan de formation et entretien annuel (Drive, août 2025).", "Mettre à jour pour 2026."),
    (23, "Veille légale et réglementaire", AF, "Sources citées dans la ressource (RGPD, CPCE, règlement cosmétique, IA Act).",
     "Formaliser un registre de veille daté (une ligne par texte suivi)."),
    (24, "Veille sur les compétences, métiers et emplois", AF, "Aucune trace formalisée pour le secteur esthétique.",
     "Ajouter au registre de veille 2 ou 3 sources du secteur (branche esthétique, OPCO EP)."),
    (25, "Veille sur les innovations pédagogiques et technologiques", OK, "Quiz interactif hors ligne, jeux de cartes, pédagogie inversée du positionnement.", ""),
    (26, "Accueil des personnes en situation de handicap", AF, "Référent handicap, mesures universelles, fiche Indicateur 8 section 5.",
     "Tenir le « Registre des aménagements » créé ce jour (sans aucune donnée de santé)."),
    (27, "Sous-traitance : respect du référentiel", NA, "Action réalisée en direct (convention YEBA / MARILYN INSTITUT).",
     "Airtable classe encore FOR-0007 en « sous-traitance — marque blanche » : à corriger."),
    (28, "Formation en situation de travail / alternance : ressources du milieu pro", NA, "Formation en salle.", ""),
    (29, "Insertion professionnelle", NA, "Concerne les actions d'insertion.", ""),
    (30, "Recueil des appréciations", OK, "Évaluation à chaud, à froid (3 mois), commanditaire (30 jours).", ""),
    (31, "Traitement des difficultés et réclamations", MQ, "Procédure décrite (livret, règlement, convention art. 12).",
     "Utiliser la « Fiche de réclamation » et le registre créés ce jour."),
    (32, "Amélioration continue", MQ, "Rien encore : première action.", "Remplir la « Fiche bilan de session et plan d'amélioration » après chaque session."),
]


def audit():
    doc = Doc("Audit des 32 indicateurs Qualiopi", "Action Marilyn Institut — état au 27/09/2026",
              f"{D.ORG['qualiopi']} — action {D.ACTION['reference']}", corps=10, paysage=True, compact=True)
    ok = sum(1 for i in INDICATEURS if i[2] == OK)
    na = sum(1 for i in INDICATEURS if i[2] == NA)
    af = sum(1 for i in INDICATEURS if i[2] == AF)
    mq = sum(1 for i in INDICATEURS if i[2] == MQ)
    doc.p((f"Bilan : {ok} réalisés · {af} à compléter · {mq} fiches créées ce jour · {na} non applicables. ", {"b": True}),
          "Aucun indicateur applicable n'est laissé sans réponse.", taille=11)
    lignes = [["Ind.", "Exigence", "Statut", "Preuve pour cette action", "Action à mener"]]
    for n, e, st, pr, ac in INDICATEURS:
        lignes.append([str(n), e, st, pr, ac or "—"])
    doc.table(lignes, [1.1, 6.6, 3.2, 7.2, 7.7], taille=8.5, centre_cols=(0,))
    doc.h2("Contrôles spécifiques de l'OPCO EP")
    doc.table([["Point de contrôle", "État", "À faire"],
               ["Accord de prise en charge obtenu AVANT le début de chaque session", "Inconnu", D.A_COMPLETER + " — demander la copie de l'accord à Sarah MACHON (convention, art. 7)."],
               ["Cohérence convention / émargement / certificat (noms, dates, durée)", "⚠ Écart",
                D.vigilance("opco_ecart")],
               ["Orthographe des noms identique partout", "⚠ À vérifier", D.vigilance("opco_orthographe")],
               ["Durée attestée = durée financée", "⚠ Point de vigilance",
                "8h00-17h00 moins 1 h de déjeuner = 8 h de présence (pauses comprises), pour 7 h conventionnelles. Le certificat indique 7 h (durée financée). "
                "Recommandation : garder 7 h sur le certificat et l'attestation, les horaires réels sur l'émargement."],
               ["Émargement par demi-journée, signé par stagiaire et formateur", "✔", "Feuilles générées par session."],
               ["Certificat de réalisation au modèle attendu", "✔ / à vérifier", "Vérifier si l'OPCO EP impose son modèle sur son espace en ligne."],
               ["Une facture par session", "✔", "Convention art. 7 : factures F-MAR-2026-01 et -02 déjà préparées (Drive)."],
               ["Convention collective (IDCC)", D.A_COMPLETER, "Champ « à compléter » dans la convention : à relever sur un bulletin de paie."]],
              [7.2, 3, 15.6], taille=9)
    return doc.enregistrer(OUT / "01_Audit_32_indicateurs_Qualiopi_et_controles_OPCO.docx")


def analyse_besoin():
    doc = Doc("Fiche d'analyse du besoin", "Qualiopi — indicateur 4 — à faire signer par le commanditaire",
              f"Convention {D.ACTION['convention']}", corps=11)
    doc.encadre("À quoi sert cette fiche", ["Elle prouve que le besoin a été analysé AVEC l'entreprise et le financeur avant la formation (indicateur 4). "
                                            "Les informations connues sont pré-remplies ; les autres sont à compléter avec Sarah MACHON, pas à deviner."])
    doc.table([["Rubrique", "Information"],
               ["Entreprise", f"{D.CLIENT['raison_sociale']} ({D.CLIENT['forme']}) — SIREN {D.CLIENT['siren']} — 2 établissements : MARILYN INSTITUT (Saint-Denis), L'OR DES ÎLES (Bras-Panon)"],
               ["Interlocutrice", f"{D.CLIENT['representant']}, {D.CLIENT['qualite']}"],
               ["Financeur", D.CLIENT["opco"] + " — plan de développement des compétences"],
               ["Public", "8 salariées : esthéticiennes, prothésistes ongulaires, apprentie"],
               ["Contrainte d'organisation", "Deux groupes de 4 sur deux jours, pour maintenir l'activité des deux instituts (programme FOR-0007)"],
               ["Besoin exprimé par la direction", D.A_COMPLETER],
               ["Situations problématiques observées par la direction", D.A_COMPLETER],
               ["Résultat attendu à 3 mois (indicateur suivi)", D.A_COMPLETER + " (ex. : taux de reprise de RDV, ventes produits)"],
               ["Besoins exprimés par les salariées (positionnement)", "Objections et recommandation, parler chiffres, recevoir une remarque, aisance orale, communication d'équipe"],
               ["Réponse proposée", f"« {D.ACTION['intitule']} » — 7 h par groupe — 10 objectifs — protocole M.A.R.I.L.Y.N."],
               ["Date de l'échange d'analyse", D.A_COMPLETER]],
              [6, 11.4], taille=10)
    doc.signatures(["Pour MARILYN INSTITUT", f"{D.CLIENT['representant']}, {D.CLIENT['qualite']}", "Date et signature"],
                   ["Pour YEBA FORMATIONS", "Aurélien LUMEKA, directeur", "Date et signature"])
    return doc.enregistrer(OUT / "02_Fiche_analyse_du_besoin_Indicateur_4.docx")


def registre_amenagements():
    doc = Doc("Registre des aménagements", "Qualiopi — indicateur 26 — accessibilité", f"Action {D.ACTION['reference']}", corps=11)
    doc.encadre("Règle absolue", ["On note UNIQUEMENT l'aménagement mis en œuvre, jamais sa raison. Aucune pathologie, aucun état de santé, "
                                  "aucune grossesse, aucun traitement : ce sont des données de santé (RGPD, art. 9) que YEBA FORMATIONS n'enregistre pas "
                                  "(convention, art. 6)."])
    doc.table([["Date", "Session", "Aménagement demandé", "Aménagement mis en œuvre", "Vérifié par / le"],
               ["27/09/2026", "1 et 2", "Confort pendant la journée (mesure collective)", "Chaises à dossier, activités assises ou debout au choix, pauses libres, eau, supports 28 pt", "A. LUMEKA"],
               ["27/09/2026", "1 et 2", "Poste de travail à l'institut (3 demandes, hors formation)", "Remontée collective anonyme à l'employeur, avec l'accord des intéressées", "A. LUMEKA"],
               ["", "", "", "", ""], ["", "", "", "", ""], ["", "", "", "", ""]],
              [2.4, 1.8, 4.6, 5.8, 2.8], taille=10, hauteur_cm=1.2)
    return doc.enregistrer(OUT / "03_Registre_des_amenagements_Indicateur_26.docx")


def reclamation():
    doc = Doc("Fiche de réclamation", "Qualiopi — indicateur 31", f"Action {D.ACTION['reference']}", corps=11)
    doc.table([["Rubrique", "À remplir"],
               ["Date de réception", ""], ["Émetteur (stagiaire, entreprise, financeur, autre)", ""], ["Canal (oral, e-mail, courrier)", ""],
               ["Objet de la réclamation", ""], ["Accusé de réception envoyé le (sous 5 jours ouvrés)", ""],
               ["Analyse de la cause", ""], ["Réponse apportée le (sous 15 jours ouvrés)", ""], ["Action corrective", ""],
               ["Clôture (date, satisfaction de l'émetteur)", ""]], [7.4, 10], taille=11, hauteur_cm=1.35)
    doc.h2("Registre des réclamations")
    doc.table([["N°", "Date", "Émetteur", "Objet", "Réponse le", "Action", "Clos"]] + [["", "", "", "", "", "", ""] for _ in range(6)],
              [1, 2.2, 3, 4.6, 2.2, 3.2, 1.2], taille=10, hauteur_cm=1.0)
    doc.p(f"Réclamation : {D.ORG['email']} — délais alignés sur la convention (art. 12).", taille=10)
    return doc.enregistrer(OUT / "04_Fiche_et_registre_reclamations_Indicateur_31.docx")


def bilan_session():
    doc = Doc("Bilan de session et plan d'amélioration", "Qualiopi — indicateurs 2, 30 et 32 — à remplir après chaque session",
              f"Action {D.ACTION['reference']}", corps=11)
    doc.table([["Indicateur", "Session 1 (28/09)", "Session 2 (29/09)", "Total"],
               ["Stagiaires prévues / présentes", " / ", " / ", " / "], ["Heures réalisées / prévues", " / 28 h", " / 28 h", " / 56 h"],
               ["Taux d'assiduité", " %", " %", " %"], ["Quiz : moyenne / 10", "", "", ""], ["Grille : moyenne / 39", "", "", ""],
               ["Stagiaires ayant atteint les objectifs", " / ", " / ", " / "], ["Satisfaction à chaud (très satisfaites + satisfaites)", " %", " %", " %"],
               ["Recommanderaient la formation", " %", " %", " %"], ["Progression moyenne au positionnement express", "", "", ""],
               ["Réclamations", "", "", ""]], [7.2, 3.4, 3.4, 3.4], taille=10, hauteur_cm=0.9)
    doc.h2("Ce qui a bien marché / ce qui doit changer")
    doc.table([["Constat", "Source (quiz, grille, satisfaction, observation)", "Action d'amélioration", "Pour quand"]] + [["", "", "", ""] for _ in range(5)],
              [5, 4.4, 5, 3], taille=10, hauteur_cm=1.3)
    doc.p("Les indicateurs de résultats (assiduité, satisfaction, atteinte des objectifs) sont publiés sur le site de l'organisme (indicateur 2), "
          "sans aucune donnée nominative.", taille=10)
    return doc.enregistrer(OUT / "05_Bilan_session_et_amelioration_Indicateurs_2_30_32.docx")


def construire():
    return [audit(), analyse_besoin(), registre_amenagements(), reclamation(), bilan_session()]


if __name__ == "__main__":
    for f in construire():
        print(f.relative_to(D.SORTIE))
