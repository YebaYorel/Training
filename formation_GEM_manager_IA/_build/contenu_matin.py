# -*- coding: utf-8 -*-
from deck_engine import *

def construire(prs):
    # ---------------------------------------------------------- OUVERTURE --
    slide_couverture(prs, MODALITE,
        ["Manager aujourd'hui :", "posture et intelligence", "artificielle"],
        "Psychologie du dirigeant  •  IA et responsabilité en entreprise",
        ORGANISME + "   –   TP Manager d'Établissement Marchand   –   " + HORAIRES)

    slide(prs, "Votre journée",
        [(1, "9h00  Ouverture et cadre commun"),
         (1, "9h20  La psychologie du dirigeant"),
         (1, "10h30  Pause – 15 minutes"),
         (1, "12h30  Déjeuner"),
         (1, "13h30  IA et responsabilité"),
         (1, "15h15  Pause – 15 minutes"),
         (1, "17h00  Clôture")],
        note="7 heures. Deux univers. Une seule question : quel chef devenez-vous ?")

    slide(prs, "Nos règles à distance",
        [(1, "Caméra allumée si vous le pouvez"),
         (1, "Micro coupé hors prise de parole"),
         (1, "La main levée vaut la parole"),
         (1, "Le tchat sert aux questions, j'y réponds"),
         (1, "Un souci technique ? Écrivez tout de suite"),
         (1, "Besoin d'adaptation ? Dites-le maintenant")],
        note="Aucun enregistrement. Une gêne à montrer votre cadre ? Dites-le-moi.",
        etiquette="À LIRE")

    slide(prs, "Ce soir, vous saurez…",
        [(1, "Nommer la place du responsable"),
         (1, "Choisir un style selon la situation"),
         (1, "Distinguer exigence et toxicité"),
         (1, "Tenir un brief d'équipe sous tension"),
         (1, "Situer une IA dans l'IA Act"),
         (1, "Protéger les données de votre équipe"),
         (1, "Lancer 3 usages IA dès lundi")],
        note="Le matin nourrit directement le bloc 1 du titre : manager l'équipe.")

    slide(prs, "Ce que vous allez devenir",
        [(1, "Manager d'établissement marchand"),
         (2, "Rayon, magasin, point de vente, équipe"),
         (1, "Entre la direction et le terrain"),
         (1, "Comptable des résultats, garant du climat"),
         (2, "Deux missions qui se contredisent souvent"),
         (1, "Aujourd'hui, on travaille cette place")],
        note="Tout ce qu'on voit aujourd'hui se joue en magasin, pas dans un manuel.")

    slide_jeu(prs, "1", "Le thermomètre", "15 min",
        "Faire émerger les représentations du groupe",
        ["Une règle de 0 à 10 s'affiche à l'écran",
         "0 : « mon chef est un ami »",
         "10 : « mon chef est un adversaire »",
         "Écrivez votre chiffre dans le tchat",
         "Trois volontaires expliquent leur note",
         "Personne ne débat : on écoute"],
        "Tchat de la visioconférence. Aucun outil supplémentaire.")

    # ------------------------------------------------------------ PARTIE 1 --
    slide_partie(prs, "PARTIE 1", ["La psychologie", "du dirigeant"], "9h20 – 12h30",
        ["Dans sa tête : ce qu'il porte vraiment",
         "Ni ami, ni ennemi : la juste place",
         "Quatre styles, quatre situations",
         "Exigeant ou toxique : la frontière",
         "Langage, posture, brief d'équipe"])

    # --- M1
    slide_choc(prs, "Diriger,", "c'est arbitrer seul.",
        "Et assumer devant tout le magasin.", C_NUIT)

    slide(prs, "Ce que le dirigeant porte",
        [(1, "La survie économique de l'enseigne"),
         (1, "La paie de chacun, tous les mois"),
         (1, "Des informations qu'il ne peut dire"),
         (1, "Les décisions qu'il n'a pas choisies"),
         (1, "Le regard permanent de l'équipe")],
        note="Il ne voit pas le même tableau de bord que vous. Ni la même échéance.")

    slide(prs, "La solitude du décideur",
        [(1, "Il ne peut pas se plaindre en interne"),
         (1, "Il ne peut pas tout expliquer"),
         (1, "Il arbitre avec 60 % de l'information"),
         (1, "Il décide quand même : c'est le métier"),
         (2, "Conséquence : il paraît froid, fermé, pressé"),
         (2, "Ce n'est pas du mépris : c'est de la charge")],
        note="Source : H. Mintzberg, « Le manager au quotidien », rôles décisionnels.")

    slide(prs, "Sa double loyauté",
        [(1, "Vers le haut : siège, marge, objectifs"),
         (1, "Vers le bas : équipe, planning, conditions"),
         (1, "Les deux tirent en sens inverse"),
         (1, "Il devient un traducteur permanent"),
         (2, "Vous serez exactement à cette place demain")],
        note="Exemple : la direction impose − 2 heures de planning. Vous annoncez quoi ?")

    slide_deux_colonnes(prs, "Ce qu'on croit / ce qui est",
        "On croit", ["« Il s'en fiche »", "« Il décide seul »",
                      "« Il ne nous dit rien »", "« Il a tout le pouvoir »"],
        "Réalité fréquente", ["Il encaisse sans le montrer", "Il subit des contraintes",
                                    "Il est tenu à la confidentialité", "Il rend des comptes aussi"],
        note="Comprendre n'est pas excuser. Comprendre, c'est mieux négocier.")

    # --- M2
    slide_choc(prs, "Ni ami.", "Ni ennemi.", "Une troisième place existe.", C_ACCENT)

    slide(prs, "Les trois positions",
        [(1, "L'ami : je veux être aimé"),
         (2, "Résultat : je n'ose plus recadrer"),
         (1, "L'ennemi : je veux être craint"),
         (2, "Résultat : on me ment pour se protéger"),
         (1, "Le garant : je tiens le cadre"),
         (2, "Résultat : on sait à quoi s'attendre")],
        note="VIDÉO 1 – « Les trois positions du manager » (2 min 30).")

    slide(prs, "Le piège du chef sorti du rang",
        [(1, "Hier collègue, aujourd'hui responsable"),
         (1, "Même pause, même groupe, mêmes blagues"),
         (1, "Puis il faut refuser un samedi de repos"),
         (2, "Et là, l'amitié devient une dette"),
         (1, "La règle se pose avant d'en avoir besoin")],
        note="Situation n°1 en établissement marchand. À traiter dès le premier jour.")

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
        [(1, "« Entre nous, le siège se trompe »"),
         (2, "Vous cassez votre propre autorité"),
         (1, "« Je te le dis, mais garde-le pour toi »"),
         (2, "Vous créez un cercle, donc des exclus"),
         (1, "« De toute façon, on n'y peut rien »"),
         (2, "Vous validez l'impuissance de l'équipe")],
        note="Exercice éclair dans le tchat : reformulez la première en version garante.")

    # --- M3
    slide_choc(prs, "Il n'y a pas", "de bon style.",
        "Il y a le style que la situation réclame.", C_NUIT)

    slide(prs, "Quatre styles, quatre usages",
        [(1, "Directif : je dis quoi et comment"),
         (2, "Rush, sécurité, saisonnier de la veille"),
         (1, "Persuasif : j'explique et j'embarque"),
         (2, "Nouveau planning, nouvelle procédure"),
         (1, "Participatif : je décide avec"),
         (2, "Équipe compétente mais démotivée"),
         (1, "Délégatif : je confie et je suis")],
        note="Source : P. Hersey & K. Blanchard, leadership situationnel.")

    slide(prs, "L'erreur la plus fréquente",
        [(1, "Utiliser toujours le même style"),
         (1, "Directif avec un ancien : il se ferme"),
         (1, "Délégatif avec un saisonnier : il coule"),
         (1, "Participatif un samedi de soldes : on perd"),
         (2, "Le style se choisit selon la personne ET la tâche")],
        note="Même vendeur, deux tâches : deux styles différents.")

    slide_jeu(prs, "2", "Les quatre coins", "20 min",
        "Choisir le bon style sous contrainte de temps",
        ["Quatre styles, quatre numéros : 1 à 4",
         "Je lis une situation de magasin",
         "10 secondes : votre chiffre dans le tchat",
         "Je choisis deux personnes qui justifient",
         "On révèle le style attendu et pourquoi",
         "8 situations s'enchaînent"],
        "Tchat, ou sondage intégré à la visio si disponible (kit jeux, fiche J2)")

    # --- M4
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
        "Toxique", ["Critique la personne", "Humilie devant les clients",
                    "Règles qui changent", "Contrôle chaque geste",
                    "Silence punitif"],
        "Exigeant", ["Critique le résultat", "Recadre en réserve",
                     "Règles stables et dites", "Contrôle les jalons",
                     "Dit les choses vite"],
        note="Repère : l'exigence donne un chemin, la toxicité ferme les portes.")

    slide(prs, "Les dégâts, côté équipe",
        [(1, "Hypervigilance, fatigue, sommeil"),
         (1, "Plus personne n'ose signaler d'erreur"),
         (1, "Absentéisme, puis départs en série"),
         (1, "Les meilleurs vendeurs partent d'abord"),
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
        ["Sous-groupes de 4 en salles séparées",
         "12 situations dans un document partagé",
         "Trois colonnes : exigeant / limite / toxique",
         "10 minutes, puis retour en salle plénière",
         "Chaque groupe défend sa situation « limite »",
         "Synthèse : 3 critères retenus à l'écran"],
        "Salles séparées + fiche J3 envoyée en PDF avant la session")

    # --- M5
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
        note="Debout derrière votre écran pendant 60 secondes : on essaie tout de suite.")

    slide(prs, "La même posture, en visio",
        [(1, "Caméra à hauteur des yeux, pas plus bas"),
         (1, "Regardez l'objectif, pas votre image"),
         (1, "Buste visible : les mains doivent entrer"),
         (1, "Nommez les gens : « Karim, ton avis ? »"),
         (2, "À distance, le silence dure deux fois plus longtemps")],
        note="En visio, tout ce qui n'est pas nommé explicitement n'existe pas.")

    slide(prs, "Dire ce qui ne va pas : DESC",
        [(1, "Décrire les faits, sans adjectif"),
         (2, "« La caisse a ouvert à 9h12 au lieu de 9h »"),
         (1, "Exprimer l'effet, en « je »"),
         (2, "« J'ai eu six clients en attente à l'entrée »"),
         (1, "Suggérer une solution précise"),
         (1, "Conclure sur un accord daté")],
        note="Jamais devant un client ni devant l'équipe. Toujours dans les 48 heures.")

    slide(prs, "Le brief d'équipe : avant",
        [(1, "Un objectif écrit en une phrase"),
         (1, "Trois points maximum, pas un de plus"),
         (1, "Les bonnes personnes, pas toutes"),
         (1, "Une durée annoncée et tenue"),
         (2, "Sans objectif écrit : annulez, vous gagnez 1 heure")],
        note="Règle simple : pas d'ordre du jour, pas de réunion.")

    slide(prs, "Le brief d'équipe : pendant",
        [(1, "Vous rappelez l'objectif en 30 secondes"),
         (1, "Vous parlez en dernier sur les avis"),
         (1, "Vous faites parler les silencieux"),
         (1, "Vous coupez le hors-sujet avec respect"),
         (1, "Vous clarifiez : qui fait quoi pour quand")],
        note="Si vous parlez plus de 40 % du temps, ce n'est plus un brief.")

    slide(prs, "Quatre profils difficiles",
        [(1, "Le bavard : cadrez le temps de parole"),
         (1, "Le sceptique : demandez sa condition"),
         (1, "Le silencieux : questionnez-le en premier"),
         (1, "Le démotivé : voyez-le après, en privé"),
         (2, "Jamais d'affrontement public : vous perdez deux fois")],
        note="Vous allez tous les rencontrer dans le jeu de rôle suivant.")

    slide_jeu(prs, "4", "Le brief de 8h", "30 min",
        "Se mettre dans la peau du manager, en direct",
        ["Un manager, quatre rôles secrets",
         "Sujet : le planning des fêtes est refusé",
         "8 minutes de brief, chrono partagé à l'écran",
         "Les autres observent avec la grille n°1",
         "Débrief : d'abord le manager parle",
         "Puis les rôles, puis les observateurs"],
        "Rôles envoyés en message privé + grille d'évaluation n°1")

    slide(prs, "Ce qu'on retient du matin",
        [(1, "Le dirigeant arbitre avec l'info qu'il a"),
         (1, "Ni ami, ni ennemi : garant du cadre"),
         (1, "Le style se choisit, il ne se subit pas"),
         (1, "L'exigence ouvre, la toxicité ferme"),
         (1, "Le brief se gagne avant de le lancer")],
        note="À vous : QUIZ n°1, 10 questions, 10 minutes, sans document.")

    slide_pause(prs, "Déjeuner", "Reconnexion à 13h30 précises – même lien")
