# -*- coding: utf-8 -*-
from docs_engine import *
from reportlab.platypus import Table, TableStyle, Paragraph

NIV = ["0 — Non observé", "1 — Amorcé", "2 — Acquis", "3 — Maîtrisé"]

def grille(chemin, numero, titre, contexte, critiques, seuil_note, critiques_bloquants, obs):
    f = [H1("Grille d'évaluation n°%d — %s" % (numero, titre))]
    t = tableau([["Évalué :", "", "Observateur :", "", "Date :", ""]],
                [22*mm, 48*mm, 28*mm, 48*mm, 16*mm, None], entete=False)
    t.setStyle(TableStyle([("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
    f += [t, E(4)]
    f += [encadre("Contexte de l'évaluation", contexte)]
    f += [E(4), H2("Échelle d'appréciation")]
    f += [tableau([["Niveau", "Signification"],
                   ["0 — Non observé", "Le comportement attendu n'apparaît pas, ou un comportement contraire apparaît."],
                   ["1 — Amorcé", "Le comportement apparaît une fois, de manière hésitante ou incomplète."],
                   ["2 — Acquis", "Le comportement est présent, correct, reproductible en situation simple."],
                   ["3 — Maîtrisé", "Le comportement est présent, ajusté à la situation, tenu même sous tension."]],
                  [34*mm, None])]
    f += [E(5), H2("Critères observables")]
    lignes = [["N°", "Critère évalué", "Indicateur observable — ce que je dois voir ou entendre", "0", "1", "2", "3"]]
    for i, (crit, ind) in enumerate(critiques, 1):
        etoile = " <font color='#B91C1C'><b>*</b></font>" if i in critiques_bloquants else ""
        lignes.append([str(i), crit + etoile, ind, "", "", "", ""])
    t = tableau(lignes, [9*mm, 40*mm, None, 9*mm, 9*mm, 9*mm, 9*mm])
    f += [t]
    f += [E(3), P("<font color='#B91C1C'><b>*</b></font> Critère bloquant : un niveau 0 sur "
                  "ce critère empêche la validation, quel que soit le total.", "petit")]
    f += [E(5), H2("Résultat")]
    f += [tableau([["Total obtenu", "Total possible", "Seuil d'acquisition", "Acquis ?"],
                   ["______ / %d" % (len(critiques)*3), "%d points" % (len(critiques)*3),
                    "%d points" % seuil_note, "❑&nbsp;&nbsp;Oui&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;❑&nbsp;&nbsp;À consolider"]],
                  [None, None, None, None], aligns=["c","c","c","c"])]
    f += [E(5), H2("Observations et axe de progrès")]
    f += [P("<b>Ce qui a bien fonctionné (au moins un point précis) :</b>")]
    t = Table([[""],[""]], colWidths=[174*mm], rowHeights=[8*mm]*2)
    t.setStyle(TableStyle([("LINEBELOW",(0,0),(-1,-1),0.5,colors.HexColor("#9AA5B4"))]))
    f += [t, E(3)]
    f += [P("<b>Un seul axe de progrès, formulé en comportement observable :</b>")]
    t2 = Table([[""],[""]], colWidths=[174*mm], rowHeights=[8*mm]*2)
    t2.setStyle(TableStyle([("LINEBELOW",(0,0),(-1,-1),0.5,colors.HexColor("#9AA5B4"))]))
    f += [t2, E(4)]
    f += [encadre("Consignes de débrief (formateur)", obs, coul=VERT, fond=PALE_VERT)]
    doc = document(chemin, "Grille d'évaluation n°%d" % numero, titre)
    doc.build(f)
    print("Grille %d : OK" % numero)

# ------------------------------------------------------------- GRILLE 1 ---
grille("../04_grilles_evaluation/Grille_evaluation_1_Posture_manageriale.pdf", 1,
  "Posture managériale en situation de brief d'équipe",
  ["Support : jeu n°4 « Le brief de 8h » — 8 minutes de mise en situation en classe virtuelle.",
   "Le stagiaire anime un brief avec quatre vendeurs jouant un rôle secret.",
   "Sujet imposé : le planning des fêtes, imposé par le siège et refusé par l'équipe.",
   "Compétences visées : bloc 1 du TP Manager d'Établissement Marchand — manager l'équipe.",
   "L'évaluation porte sur des comportements observés, jamais sur la personnalité.",
   "À distance : l'observateur note ce qu'il voit à l'écran et ce qu'il entend, rien d'autre."],
  [("Ouverture et cadrage",
    "Il rappelle l'objectif en une phrase et annonce la durée, dans les 60 premières secondes. À distance : il vérifie d'abord que tout le monde l'entend."),
   ("Choix du style managérial",
    "Il adapte son style au profil rencontré (directif, persuasif, participatif, délégatif) "
    "au lieu d'appliquer le même registre à tous."),
   ("Régulation de la parole",
    "Il donne la parole avant de donner son avis, relance <b>nommément</b> le silencieux, "
    "borne le bavard sans le disqualifier. À distance, l'appel par le prénom est décisif."),
   ("Posture et voix",
    "Buste et mains dans le cadre, regard vers l'objectif et non vers sa propre image, "
    "débit ralenti, usage d'au moins un silence assumé."),
   ("Traitement du désaccord",
    "Il accueille l'objection, la reformule et demande une condition de réussite. "
    "Il critique le fait, jamais la personne. Aucun recadrage devant le groupe."),
   ("Tenue du cadre",
    "Il rappelle la règle applicable à tous, ne crée pas d'exception non expliquée, "
    "et ne se désolidarise pas de la décision du siège."),
   ("Clôture opérationnelle",
    "Il conclut par qui fait quoi pour quand, à voix haute, et vérifie l'accord.")],
  14, [5, 6],
  ["Faire parler le stagiaire en premier : « qu'est-ce que tu referais pareil ? »",
   "Puis les joueurs de rôle : « à quel moment t'es-tu senti écouté ? »",
   "Puis les observateurs, avec la grille, sur des faits uniquement.",
   "Terminer par un seul axe de progrès. Deux axes = zéro axe retenu.",
   "Durée conseillée du débrief : 10 minutes maximum par passage.",
   "À distance : demandez aux observateurs de garder le micro coupé et d'écrire leurs "
   "observations au fil de l'eau. Ils oublient tout en huit minutes."])

# ------------------------------------------------------------- GRILLE 2 ---
grille("../04_grilles_evaluation/Grille_evaluation_2_Usage_responsable_IA.pdf", 2,
  "Usage responsable de l'IA dans une situation professionnelle",
  ["Support : jeu n°8 « Mon chantier IA » — présentation orale de 60 secondes en classe "
   "virtuelle, appuyée sur la fiche complétée.",
   "Le stagiaire choisit une tâche réelle de son magasin et construit un usage d'IA conforme.",
   "Apport transverse : se rattache notamment à la non-discrimination et à la sécurité "
   "au travail, attendues au bloc 1 du TP MEM.",
   "Tous les stagiaires sont évalués : trois à l'oral, les autres sur la fiche déposée.",
   "L'évaluation porte sur le raisonnement de conformité, pas sur la maîtrise technique de l'outil."],
  [("Identification des données personnelles",
    "Il repère les données personnelles en entrée et en sortie, y compris les données "
    "indirectement identifiantes, et cite la finalité et la durée de conservation."),
   ("Qualification du niveau de risque",
    "Il situe l'usage parmi les quatre niveaux de l'IA Act et justifie par l'usage, "
    "non par l'outil. Il détecte le cas échéant le caractère interdit ou à haut risque."),
   ("Obligations identifiées",
    "Il cite les obligations applicables : supervision humaine effective, information des "
    "personnes, information et consultation des représentants du personnel, traçabilité."),
   ("Question de l'hébergement",
    "Il pose la question du lieu de traitement, du droit applicable au prestataire et de "
    "la réutilisation éventuelle des données pour l'entraînement."),
   ("Qualité du prompt produit",
    "Le prompt comporte les quatre blocs (rôle, contexte, tâche, format) et ne contient "
    "aucune donnée personnelle inutile."),
   ("Réalisme du gain annoncé",
    "Le gain de temps est chiffré, plausible, et le temps de vérification humaine est intégré."),
   ("Plan d'action exploitable",
    "Une action, une date, une personne. Le critère de réussite est vérifiable.")],
  14, [2, 3],
  ["Valoriser le stagiaire qui renonce à un usage après analyse : c'est une réussite, pas un échec.",
   "Ne pas sanctionner la méconnaissance d'un numéro d'article : évaluer le raisonnement.",
   "Reprendre systématiquement tout usage à haut risque présenté sans supervision humaine.",
   "Conserver les fiches : elles constituent une trace utile au titre de l'article 4 de l'IA Act.",
   "Durée conseillée : 60 secondes de présentation, 60 secondes de retour."])
