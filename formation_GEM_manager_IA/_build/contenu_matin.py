# -*- coding: utf-8 -*-
from deck_engine import *

def construire(prs):
    # ---------------------------------------------------------- OUVERTURE --
    slide_couverture(prs,
        "FORMATION – 1 JOUR",
        ["Manager aujourd'hui :", "posture et intelligence", "artificielle"],
        "Psychologie du dirigeant  •  IA et responsabilité en entreprise",
        ORGANISME + "   –   8h00 → 17h00")

    slide(prs, "Votre journée",
        [(1, "8h00  Ouverture et cadre commun"),
         (1, "8h20  La psychologie du dirigeant"),
         (1, "10h00  Pause – 15 minutes"),
         (1, "12h00  Déjeuner"),
         (1, "13h00  IA et responsabilité"),
         (1, "15h00  Pause – 15 minutes"),
         (1, "17h00  Clôture")],
        note="Deux univers, une seule question : quel responsable devenez-vous ?")

    slide(prs, "Ce soir, vous saurez…",
        [(1, "Nommer la place du dirigeant"),
         (1, "Choisir un style selon la situation"),
         (1, "Distinguer exigence et toxicité"),
         (1, "Tenir une réunion sous tension"),
         (1, "Situer une IA dans l'IA Act"),
         (1, "Protéger les données de vos équipes"),
         (1, "Lancer 3 usages IA dès lundi")],
        note="7 compétences. Toutes évaluées aujourd'hui.")

    slide(prs, "Notre cadre de travail",
        [(1, "On parle vrai, on ne cite personne"),
         (1, "Pas de question bête, jamais"),
         (1, "Le téléphone dort, sauf ateliers"),
         (1, "On essaie : l'erreur est la méthode"),
         (1, "Besoin spécifique ? Dites-le maintenant")],
        note="Accessibilité : signalez-moi tout besoin, j'adapte immédiatement.")

    slide_jeu(prs, "1", "Le thermomètre", "15 min",
        "Faire émerger les représentations du groupe",
        ["Une ligne imaginaire traverse la salle",
         "À gauche : « mon chef est un ami »",
         "À droite : « mon chef est un adversaire »",
         "Placez-vous où vous vous sentez juste",
         "3 volontaires expliquent leur place",
         "Personne ne débat : on écoute"],
        "Ruban adhésif au sol, espace libre de 6 mètres")

    # ------------------------------------------------------------ PARTIE 1 --
    slide_partie(prs, "PARTIE 1", ["La psychologie", "du dirigeant"], "8h20 – 12h00",
        ["Dans sa tête : ce qu'il porte vraiment",
         "Ni ami, ni ennemi : la juste place",
         "Quatre styles, quatre situations",
         "Exigeant ou toxique : la frontière",
         "Langage, posture, réunions"])

    # --- M1 : dans la tete du dirigeant
    slide_choc(prs, "Diriger,", "c'est arbitrer seul.",
        "Et assumer devant tout le monde.", C_NUIT)

    slide(prs, "Ce que le dirigeant porte",
        [(1, "La survie économique de la structure"),
         (1, "La paie de chacun, tous les mois"),
         (1, "Des informations qu'il ne peut dire"),
         (1, "Les décisions qu'il n'a pas choisies"),
         (1, "Le regard permanent de l'équipe")],
        note="Il ne voit pas la même carte que vous. Ni la même échéance.")

    slide(prs, "La solitude du décideur",
        [(1, "Il ne peut pas se plaindre en interne"),
         (1, "Il ne peut pas tout expliquer"),
         (1, "Il arbitre avec 60 % de l'information"),
         (1, "Il décide quand même : c'est le métier"),
         (2, "Conséquence : il paraît froid, fermé, pressé"),
         (2, "Ce n'est pas du mépris : c'est de la charge")],
        note="Source : H. Mintzberg, « Le manager au quotidien », rôles décisionnels.")

    slide(prs, "Sa double loyauté",
        [(1, "Vers le haut : actionnaires, résultats"),
         (1, "Vers le bas : équipes, conditions"),
         (1, "Les deux tirent en sens inverse"),
         (1, "Il devient un traducteur permanent"),
         (2, "Vous serez exactement à cette place demain")],
        note="Le manager de proximité vit ce grand écart chaque jour.")

    slide_deux_colonnes(prs, "Ce qu'on croit / ce qui est",
        "On croit", ["« Il s'en fiche »", "« Il décide seul »",
                      "« Il ne nous dit rien »", "« Il a tout le pouvoir »"],
        "Réalité fréquente", ["Il encaisse sans le montrer", "Il subit des contraintes",
                                    "Il est tenu à la confidentialité", "Il rend des comptes aussi"],
        note="Comprendre n'est pas excuser. Comprendre, c'est mieux négocier.")

    # --- M2 : ni ami ni ennemi
    slide_choc(prs, "Ni ami.", "Ni ennemi.", "Une troisième place existe.", C_ACCENT)

    slide(prs, "Les trois positions",
        [(1, "L'ami : je veux être aimé"),
         (2, "Résultat : je n'ose plus recadrer"),
         (1, "L'ennemi : je veux être craint"),
         (2, "Résultat : on me ment pour se protéger"),
         (1, "Le garant : je tiens le cadre"),
         (2, "Résultat : on sait à quoi s'attendre")],
        note="VIDÉO 1 – « Les trois positions du manager » (2 min 30).")

    slide(prs, "Le manager garant du cadre",
        [(1, "Il défend la règle, pas sa personne"),
         (1, "Il est prévisible : même règle pour tous"),
         (1, "Il sépare la personne du comportement"),
         (1, "Il peut être chaleureux ET ferme"),
         (2, "Chaleur sur la relation, fermeté sur le cadre")],
        note="C'est la posture « basse en forme, haute en fond ».")

    slide_deux_colonnes(prs, "Proximité : la bonne distance",
        "Trop près", ["Confidences réciproques", "Sorties en petit comité",
                        "Favoritisme perçu", "Recadrage impossible"],
        "Juste distance", ["Intérêt sincère pour l'autre", "Mêmes égards pour tous",
                           "Vie privée respectée", "Décision assumable"],
        note="Question test : « Pourrais-je dire cela à toute l'équipe ? »")

    slide(prs, "Trois phrases qui coûtent cher",
        [(1, "« Entre nous, la direction se trompe »"),
         (2, "Vous cassez votre propre autorité"),
         (1, "« Je te le dis, mais garde-le pour toi »"),
         (2, "Vous créez un cercle, donc des exclus"),
         (1, "« De toute façon, on n'y peut rien »"),
         (2, "Vous validez l'impuissance de l'équipe")],
        note="Exercice éclair : reformulez chaque phrase en version garante.")

    # --- M3 : les styles
    slide_choc(prs, "Il n'y a pas", "de bon style.",
        "Il y a le style que la situation réclame.", C_NUIT)

    slide(prs, "Quatre styles, quatre usages",
        [(1, "Directif : je dis quoi et comment"),
         (2, "Urgence, sécurité, personne débutante"),
         (1, "Persuasif : j'explique et j'embarque"),
         (2, "Changement, résistance, sens à donner"),
         (1, "Participatif : je décide avec"),
         (2, "Équipe compétente mais hésitante"),
         (1, "Délégatif : je confie et je suis")],
        note="Source : P. Hersey & K. Blanchard, leadership situationnel.")

    slide(prs, "L'erreur la plus fréquente",
        [(1, "Utiliser toujours le même style"),
         (1, "Directif avec un expert : il se ferme"),
         (1, "Délégatif avec un débutant : il coule"),
         (1, "Participatif en urgence : on perd"),
         (2, "Le style se choisit selon la personne ET la tâche")],
        note="Même collaborateur, deux tâches : deux styles différents.")

    slide_jeu(prs, "2", "Les quatre coins", "20 min",
        "Choisir le bon style sous contrainte de temps",
        ["Chaque coin de salle = un style",
         "Je lis une situation réelle à voix haute",
         "Vous avez 10 secondes pour vous placer",
         "Un porte-parole par coin justifie",
         "On révèle le style attendu et pourquoi",
         "8 situations s'enchaînent"],
        "4 affiches A3, jeu de 8 situations (kit jeux, fiche J2)")

    # --- M4 : exigence / toxicite
    slide_choc(prs, "Être exigeant", "n'est pas être dur.",
        "La différence tient en un mot : le cadre.", C_ACCENT)

    slide(prs, "La rigueur qui fait grandir",
        [(1, "Une attente claire, dite à l'avance"),
         (1, "La même règle appliquée à tous"),
         (1, "Un retour rapide, précis, privé"),
         (1, "Les moyens donnés avant le résultat"),
         (1, "L'engagement tenu, même petit")],
        note="La ténacité : tenir la règle le 40e jour comme le premier.")

    slide_deux_colonnes(prs, "Exigeant ou toxique ?",
        "Toxique", ["Critique la personne", "Humilie en public",
                    "Règles qui changent", "Contrôle chaque geste",
                    "Silence punitif"],
        "Exigeant", ["Critique le résultat", "Recadre en privé",
                     "Règles stables et dites", "Contrôle les jalons",
                     "Dit les choses vite"],
        note="Repère : l'exigence donne un chemin, la toxicité ferme les portes.")

    slide(prs, "Les dégâts, côté équipe",
        [(1, "Hypervigilance, fatigue, sommeil"),
         (1, "Plus personne n'ose signaler d'erreur"),
         (1, "Absentéisme, puis départs en série"),
         (1, "Les meilleurs partent les premiers"),
         (2, "Facteurs de RPS : rapports sociaux dégradés (INRS)")],
        note="Source : INRS, les 6 familles de facteurs de risques psychosociaux.")

    slide(prs, "Et côté juridique",
        [(1, "Obligation de sécurité de l'employeur"),
         (2, "Code du travail, article L.4121-1"),
         (1, "Interdiction du harcèlement moral"),
         (2, "Code du travail, article L.1152-1"),
         (1, "Le manager engage aussi sa responsabilité"),
         (2, "Délégation de pouvoir = délégation de risque")],
        note="Sources : Légifrance, Code du travail (à vérifier à la date du jour).",
        couleur_bandeau=C_ROUGE)

    slide_jeu(prs, "3", "Exigeant ou toxique ?", "20 min",
        "Tracer collectivement la frontière",
        ["Équipes de 4, 12 cartes situations",
         "Trois zones : exigeant / limite / toxique",
         "10 min pour classer les 12 cartes",
         "Chaque équipe défend sa carte « limite »",
         "On cherche le critère qui fait basculer",
         "Synthèse : 3 critères retenus au tableau"],
        "12 cartes A5 par équipe (kit jeux, fiche J3)")

    # --- M5 : langage, posture, reunion
    slide_choc(prs, "On ne retient pas", "ce que vous dites.",
        "On retient comment vous le dites.", C_NUIT)

    slide(prs, "Trois canaux, un seul message",
        [(1, "Les mots : précis, courts, concrets"),
         (1, "La voix : débit, volume, silences"),
         (1, "Le corps : appuis, mains, regard"),
         (2, "Si les trois se contredisent, on croit le corps"),
         (2, "C'est là que naît le « double message »")],
        note="Le non-verbal prime surtout sur l'émotion et l'attitude, pas le contenu.")

    slide(prs, "Votre posture en 5 points",
        [(1, "Deux pieds au sol, poids réparti"),
         (1, "Épaules basses, menton horizontal"),
         (1, "Mains visibles, au-dessus de la taille"),
         (1, "Regard balayé : 3 secondes par personne"),
         (1, "Silence de 2 secondes avant l'essentiel")],
        note="À tester dès le prochain atelier : effet immédiat sur l'écoute.")

    slide(prs, "Dire ce qui ne va pas : DESC",
        [(1, "Décrire les faits, sans adjectif"),
         (2, "« Le rapport est arrivé jeudi 17h »"),
         (1, "Exprimer l'effet, en « je »"),
         (2, "« J'ai dû décaler la réunion client »"),
         (1, "Suggérer une solution précise"),
         (1, "Conclure sur un accord daté")],
        note="Jamais devant les autres. Toujours dans les 48 heures.")

    slide(prs, "La réunion : avant",
        [(1, "Un objectif écrit en une phrase"),
         (1, "Trois points maximum à l'ordre du jour"),
         (1, "Les bonnes personnes, pas toutes"),
         (1, "Une durée annoncée et tenue"),
         (2, "Sans objectif écrit : annulez, vous gagnez 1 heure")],
        note="Règle simple : pas d'ordre du jour, pas de réunion.")

    slide(prs, "La réunion : pendant",
        [(1, "Vous rappelez l'objectif en 30 secondes"),
         (1, "Vous parlez en dernier sur les avis"),
         (1, "Vous faites parler les silencieux"),
         (1, "Vous coupez le hors-sujet avec respect"),
         (1, "Vous clarifiez : qui fait quoi pour quand")],
        note="Si vous parlez plus de 40 % du temps, ce n'est plus une réunion.")

    slide(prs, "Quatre profils difficiles",
        [(1, "Le bavard : cadrez le temps de parole"),
         (1, "Le sceptique : demandez sa condition"),
         (1, "Le silencieux : questionnez-le en premier"),
         (1, "Le démotivé : voyez-le après, en privé"),
         (2, "Jamais d'affrontement public : vous perdez deux fois")],
        note="Vous allez tous les rencontrer dans le jeu de rôle suivant.")

    slide_jeu(prs, "4", "La réunion de 9h", "30 min",
        "Se mettre dans la peau du manager, en direct",
        ["Un manager, quatre rôles secrets",
         "Sujet : un planning refusé par l'équipe",
         "8 minutes de réunion, chrono visible",
         "Les observateurs remplissent la grille 1",
         "Débrief : d'abord le manager parle",
         "Puis les rôles, puis les observateurs"],
        "Cartes rôles (kit jeux J4) + grille d'évaluation n°1")

    slide(prs, "Ce qu'on retient du matin",
        [(1, "Le dirigeant arbitre avec l'info qu'il a"),
         (1, "Ni ami, ni ennemi : garant du cadre"),
         (1, "Le style se choisit, il ne se subit pas"),
         (1, "L'exigence ouvre, la toxicité ferme"),
         (1, "La réunion se gagne avant d'entrer")],
        note="À vous : QUIZ n°1, 10 questions, 10 minutes, sans document.")

    slide_pause(prs, "Déjeuner", "Rendez-vous à 13h00 précises – salle identique")
