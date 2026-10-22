"""Référentiel pédagogique YEBA FORMATIONS pour les deux titres professionnels.

Sources :
- MEM : REAC MEM v09 du 10/12/2025 (TP-00136) et référentiel d'évaluation v09
  (critères, épreuves, période en entreprise) ; fiche RNCP41853.
- RPMS : fiche RNCP38575 (arrêté du 5 décembre 2023). Les REAC/RC transmis
  (RNCP35646, millésime 07 de 2016) correspondent à l'ancienne version et ne
  sont pas utilisés pour les compétences ; le REAC v08 reste à joindre.

Chaque module correspond à une compétence professionnelle (CP) du REAC ou à
un module transversal. Chaque module est découpé en journées de 7 h :
(titre de la séquence, objectif pédagogique opérationnel).
"""

DUREE_JOUR = 7

MEM = {
    "code": "MEM",
    "rncp": "RNCP41853",
    "intitule": "Titre professionnel Manager d'établissement marchand",
    "court": "Manager d'établissement marchand",
    "niveau": "Niveau 5 (cadre national des certifications 2019)",
    "arrete": "Arrêté du 4 décembre 2025 (JO du 07/12/2025) — effet au 03/03/2026, enregistrement jusqu'au 02/03/2031",
    "reac": "REAC MEM — TP-00136 — millésime 09 du 10/12/2025 ; référentiel d'évaluation millésime 09",
    "rome": "D1502, D1503, D1508, D1509, D1510",
    "nsf": "312m — Commerce, vente",
    "formacode": "34566, 34587, 34588, 34559, 34502",
    "certificateur": "Ministère du Travail, du Plein Emploi et de l'Insertion",
    "pae": 280,
    "pae_blocs": (140, 140),
    "pae_source": "280 h minimum pour le titre (140 h pour le CCP « Manager l'équipe », 140 h pour le CCP « Contribuer à la performance ») — référentiel d'évaluation MEM v09",
    "session": "7 h 55 par candidat : mise en situation professionnelle (étude de cas sur poste informatique) 4 h, entretien technique 1 h 30, questionnement à partir de productions 2 h 10, entretien final 15 min",
    "jury": "Présence du jury : 3 h 25 par candidat ; correction et lecture des dossiers : 1 h 30 minimum par candidat ; surveillance requise pendant l'étude de cas (4 h) et la préparation de l'entretien technique (30 min).",
    "productions": [
        "Document « Contribuer à la performance commerciale et à la rentabilité » : 12 à 18 pages (3 parties de 4 à 6 pages), Arial 11, interligne 1,15, avec une page de présentation de l'établissement — diaporama de 12 à 18 diapositives (présentation de 20 min).",
        "Document « Manager l'équipe de son périmètre » : 16 à 24 pages (4 parties de 4 à 6 pages), Arial 11, interligne 1,15, avec une page de présentation de l'établissement — diaporama de 18 à 24 diapositives (présentation de 25 min).",
        "Dossier professionnel (DP) et preuve de la période en entreprise, remis au responsable de session.",
    ],
    "emplois": "Manager de rayon, chef de rayon, manager de surface de vente, manager d'univers commercial, responsable de boutique, de magasin ou de point de vente, gérant de magasin, responsable de succursale, responsable de département",
    "insertion": "Insertion globale à 6 mois : 76 % (2024), 78 % (2023) ; dans le métier visé à 6 mois : 65 % (2024) — fiche RNCP41853. Tension nationale sur les postes de manager de proximité : 3,7 (REAC v09, début 2025).",
    "public": "Demandeurs d'emploi orientés par France Travail ou les Missions Locales, salariés du commerce en évolution vers l'encadrement, personnes en reconversion, personnes en situation de handicap (parcours adapté).",
    "prerequis": [
        "Aucun prérequis réglementaire n'est fixé par le titre.",
        "Critères d'admission YEBA FORMATIONS : une première expérience en vente, commerce ou relation client (y compris job étudiant ou stage), OU un niveau 4 (baccalauréat) ; maîtrise du français écrit et oral ; bases de l'outil informatique.",
        "Admission après : information collective, positionnement et entretien individuel de motivation.",
    ],
    "transversales": [
        ("Communiquer", "Consignes claires, synthèses écrites claires et factuelles à la hiérarchie, plannings communiqués de façon adaptée."),
        ("Organiser ses actions", "Anticiper les besoins humains, répartir la charge de travail, gérer les imprévus, intégrer la prévention des risques."),
        ("Respecter des règles et des procédures", "Limites de sa responsabilité, politique RH, démarche RSE, consignes de la hiérarchie, maîtrise des risques."),
        ("Mettre en œuvre une démarche de résolution de problème", "Identifier un dysfonctionnement, en analyser les causes, proposer et suivre des solutions."),
    ],
    "blocs": [
        ("CCP1", "RNCP41853BC01", "Manager l'équipe de son périmètre au sein de l'établissement marchand",
         "Questionnement à partir de productions : présentation du diaporama « Manager l'équipe » (25 min) puis questionnement du jury (45 min)"),
        ("CCP2", "RNCP41853BC02", "Développer la dynamique commerciale de son périmètre au sein de l'établissement marchand",
         "Mise en situation professionnelle : étude de cas sur poste informatique (4 h), puis entretien technique (1 h 30)"),
        ("CCP3", "RNCP41853BC03", "Contribuer à la performance commerciale et à la rentabilité de son périmètre au sein de l'établissement marchand",
         "Questionnement à partir de productions : présentation du diaporama « Performance et rentabilité » (20 min) puis questionnement du jury (40 min)"),
    ],
    "modules": [
        {"code": "M0", "cp": "—", "bloc": "Transversal", "intitule": "Accueil, intégration et positionnement",
         "objectif": "Comprendre le parcours, ses règles et ses exigences, et situer ses acquis de départ.",
         "jours": [
             ("Bienvenue et découverte du parcours", "Identifier les étapes du parcours, les 3 CCP, les épreuves du titre, les règles de vie et ses droits."),
             ("Positionnement et projet individuel", "Situer ses acquis par rapport au REAC et formaliser ses objectifs personnels de formation."),
         ],
         "methodes": "Jeu de découverte en équipes, présentation interactive, entretiens individuels",
         "evaluation": "Positionnement (non noté) et entretien individuel"},
        {"code": "T2", "cp": "Savoir-faire REAC", "bloc": "Transversal", "intitule": "Outils bureautiques et tableur",
         "objectif": "Utiliser le traitement de texte et le tableur au niveau exigé par les épreuves du titre.",
         "jours": [
             ("Traitement de texte professionnel", "Produire un document structuré (titres, tableaux, pagination) en Arial 11, interligne 1,15, et l'imprimer."),
             ("Tableur : formules et calculs commerciaux", "Calculer des pourcentages, évolutions, marges et totaux avec des formules fiables."),
             ("Tableur : graphiques et tableaux croisés", "Construire un graphique et un tableau croisé dynamique pour présenter des résultats."),
         ],
         "methodes": "Ateliers sur poste, exercices chronométrés, défis en binômes",
         "evaluation": "Exercices pratiques sur poste"},
        {"code": "M1.1", "cp": "CP1", "bloc": "CCP1", "intitule": "Animer l'équipe de son périmètre",
         "objectif": "Mobiliser l'équipe et favoriser sa cohésion autour des objectifs de l'établissement.",
         "jours": [
             ("Postures et styles de management", "Adapter son style de management aux collaborateurs et aux situations."),
             ("Transmettre des consignes qui ont du sens", "Formuler une consigne claire en expliquant sa finalité et vérifier sa compréhension."),
             ("Briefings, débriefings et réunions d'équipe", "Préparer et animer un briefing, un débriefing et une réunion adaptés aux enjeux et à l'équipe."),
             ("Motivation, cohésion et amélioration continue", "Utiliser des techniques de stimulation et impliquer l'équipe dans les actions d'amélioration (PDCA)."),
             ("Prévention des risques, QHSE et non-discrimination", "Appliquer et faire appliquer les règles de santé, sécurité et hygiène ; sensibiliser à la non-discrimination."),
         ],
         "methodes": "Jeux de rôle, mises en situation filmées avec accord écrit, études de cas réunionnais",
         "evaluation": "Mise en situation commentée en groupe"},
        {"code": "M1.2", "cp": "CP2", "bloc": "CCP1", "intitule": "Planifier et coordonner l'activité de l'équipe",
         "objectif": "Élaborer et ajuster des plannings conformes à la réglementation et à l'activité prévue.",
         "jours": [
             ("Cadre légal du temps de travail", "Appliquer les règles sur la durée du travail, les repos, les congés et les jours fériés."),
             ("Anticiper les besoins humains", "Évaluer la charge de travail à partir des prévisions d'activité, des flux clients et des opérations."),
             ("Construire et communiquer le planning", "Élaborer un planning, répartir les tâches, déléguer et le communiquer de façon adaptée."),
             ("Besoins spécifiques et prévention des risques", "Intégrer les besoins des collaborateurs en situation de handicap et la prévention (TMS, chutes, RPS)."),
             ("Gérer les imprévus et réguler l'activité", "Réajuster un planning face à une absence, un aléa ou un pic d'activité."),
         ],
         "methodes": "Cas pratiques sur tableur, simulation d'aléas, travail en sous-groupes",
         "evaluation": "Planning commenté produit en séance"},
        {"code": "M1.3", "cp": "CP3", "bloc": "CCP1", "intitule": "Accompagner la performance individuelle des collaborateurs",
         "objectif": "Évaluer les compétences et accompagner la progression de chaque collaborateur.",
         "jours": [
             ("Évaluer compétences, implication et potentiel", "Évaluer un collaborateur à partir de critères établis et d'observations factuelles."),
             ("Freins et leviers de motivation", "Identifier les freins et les leviers motivationnels d'un collaborateur."),
             ("Conduire les entretiens individuels", "Conduire un entretien de suivi, de recadrage, de félicitation et un entretien professionnel."),
             ("Plans d'accompagnement et de formation", "Construire un plan d'accompagnement individualisé et une formation en situation de travail."),
             ("Confidentialité, équité et handicap", "Appliquer les règles de confidentialité, de traitement équitable et d'aménagement raisonnable."),
         ],
         "methodes": "Entretiens simulés en trinômes (acteur, manager, observateur), études de cas",
         "evaluation": "Simulation d'entretien commentée"},
        {"code": "M1.4", "cp": "CP4", "bloc": "CCP1", "intitule": "Contribuer au recrutement et à l'intégration",
         "objectif": "Participer au recrutement et réussir l'intégration d'une nouvelle recrue.",
         "jours": [
             ("Identifier un besoin et analyser un poste", "Identifier un besoin en personnel et analyser une fiche de poste."),
             ("Sélectionner sans discriminer", "Sélectionner des candidatures selon des critères définis, dans le respect de la non-discrimination et du RGPD."),
             ("Conduire un entretien de recrutement", "Participer à un entretien et évaluer l'adéquation entre le profil et le poste."),
             ("Parcours d'intégration et tutorat", "Construire un parcours d'intégration individualisé et organiser le tutorat."),
             ("Suivre la période d'essai et adapter le poste", "Suivre la période d'essai, remonter les difficultés et contribuer à l'adaptation d'un poste."),
         ],
         "methodes": "Analyse de CV fictifs, simulations d'entretien, construction d'un parcours d'intégration",
         "evaluation": "Parcours d'intégration présenté à l'oral"},
        {"code": "T4", "cp": "—", "bloc": "Transversal", "intitule": "Préparer la période en entreprise",
         "objectif": "Trouver la structure d'accueil et préparer la collecte des éléments exigés par les productions d'examen.",
         "jours": [
             ("Trouver sa structure d'accueil", "Prospecter des entreprises d'accueil et préparer son argumentaire."),
             ("Objectifs de la période et collecte de preuves", "Fixer avec le tuteur les objectifs de la période et la liste des éléments à recueillir pour les productions."),
         ],
         "methodes": "Atelier de prospection, simulation d'appel, préparation de la convention",
         "evaluation": "Convention signée et objectifs écrits"},
        {"code": "M2.1", "cp": "CP5", "bloc": "CCP2", "intitule": "Gérer l'approvisionnement de son périmètre",
         "objectif": "Anticiper les besoins, commander, réceptionner et stocker en limitant le gaspillage.",
         "jours": [
             ("Circuits d'approvisionnement et de distribution", "Décrire les circuits d'approvisionnement, dont les spécificités insulaires de La Réunion."),
             ("Analyser stocks, ventes et tendances", "Analyser les données de stock, de ventes et de tendances pour anticiper les besoins."),
             ("Déterminer et passer les commandes", "Déterminer les quantités à commander selon stocks, ventes et réservations clients."),
             ("Réceptionner et contrôler les livraisons", "Contrôler une livraison, repérer et signaler les anomalies."),
             ("Stocker, inventorier et lutter contre la démarque", "Organiser le stockage, réaliser un inventaire et agir sur les causes de démarque."),
             ("Prévention des risques en réserve", "Appliquer et faire appliquer les gestes et postures, les EPI et les règles de manutention."),
             ("RSE : déchets, vrac et anti-gaspillage", "Appliquer les consignes RSE : valorisation des déchets, vrac, réemploi, lutte contre le gaspillage."),
         ],
         "methodes": "Études de cas chiffrées, simulation de commande, visite de réserve (si accord d'une enseigne)",
         "evaluation": "Étude de cas sur tableur"},
        {"code": "M2.2", "cp": "CP6", "bloc": "CCP2", "intitule": "Organiser et mettre en œuvre le merchandising",
         "objectif": "Implanter l'offre et conduire des opérations commerciales cohérentes avec les objectifs.",
         "jours": [
             ("Merchandising de gestion, d'organisation et de séduction", "Appliquer les règles de merchandising et les préconisations de l'enseigne."),
             ("Plan d'implantation et assortiment", "Élaborer et ajuster un plan d'implantation selon les stocks et les ventes."),
             ("Implanter l'offre permanente et saisonnière", "Implanter un assortiment en garantissant l'accessibilité des produits et des allées."),
             ("Calendrier commercial et réglementation", "Construire un calendrier d'opérations en respectant les règles d'affichage et de promotion."),
             ("Préparer une opération commerciale", "Préparer une opération commerciale à partir d'objectifs définis."),
             ("Mettre en œuvre avec l'équipe en sécurité", "Organiser la mise en place avec l'équipe et contrôler l'application des mesures de prévention."),
             ("Éco-merchandising, vrac et seconde main", "Agencer un espace vrac ou seconde main et installer une signalétique pédagogique."),
             ("Analyser les résultats d'une implantation", "Analyser les résultats commerciaux et budgétaires d'une implantation et proposer des actions."),
         ],
         "methodes": "Atelier maquette, analyse de photos de rayons, études de cas",
         "evaluation": "Projet d'implantation présenté à l'oral"},
        {"code": "M2.3", "cp": "CP7", "bloc": "CCP2", "intitule": "Participer à l'amélioration de l'expérience client",
         "objectif": "Identifier les attentes des clients et améliorer leur satisfaction sur tous les canaux.",
         "jours": [
             ("Attentes clients et tendances de consommation", "Identifier les attentes, le parcours d'achat et les tendances de consommation."),
             ("Parcours omnicanal et outils de relation client", "Utiliser les outils de gestion de la relation client et les solutions omnicanales."),
             ("Accueil des clients en situation de handicap", "Apporter une réponse adaptée aux besoins de tout type de clientèle."),
             ("Argumentaires et valorisation de l'offre", "Développer des argumentaires qui partent de la demande du client."),
             ("Réclamations, litiges et incivilités", "Adopter une posture de fidélisation et soutenir l'équipe dans les situations difficiles."),
             ("Valoriser l'offre sur les supports numériques", "Valoriser l'offre sur le site, les réseaux sociaux et les supports numériques."),
             ("Mesurer la satisfaction et proposer des améliorations", "Exploiter les retours clients et proposer des améliorations à la hiérarchie."),
         ],
         "methodes": "Client mystère en binôme, jeux de rôle, analyse d'avis clients anonymisés",
         "evaluation": "Plan d'amélioration présenté"},
        {"code": "T6", "cp": "—", "bloc": "Transversal", "intitule": "Bilan individuel de mi-parcours",
         "objectif": "Faire le point sur sa progression, ses freins et son projet avant la période en entreprise.",
         "jours": [
             ("Bilan de mi-parcours", "Faire le bilan de ses acquis, ajuster son parcours et préparer la période en entreprise."),
         ],
         "methodes": "Entretiens individuels, bilan collectif",
         "evaluation": "Fiche de suivi individuel"},
        {"code": "T1", "cp": "Savoir-faire REAC", "bloc": "Transversal", "intitule": "IA appliquée au management et au commerce",
         "objectif": "Utiliser l'IA générative de façon utile, vérifiée et conforme au RGPD et à l'IA Act.",
         "jours": [
             ("Comprendre l'IA générative", "Expliquer le fonctionnement, l'intérêt et les limites de l'IA générative (erreurs, biais)."),
             ("Rédiger des consignes efficaces", "Rédiger une consigne précise et vérifier le résultat produit."),
             ("L'IA au service du manager", "Utiliser l'IA pour préparer un briefing, un planning ou une synthèse, en gardant la décision."),
             ("L'IA au service du commerce", "Utiliser l'IA pour un argumentaire, une analyse d'avis anonymisés ou une communication."),
             ("RGPD et IA Act au quotidien", "Appliquer les règles : pas de données personnelles, transparence, usages interdits ou à haut risque."),
             ("Outils souverains et charte d'usage", "Choisir un outil hébergé dans l'Union européenne et appliquer une charte d'usage."),
         ],
         "methodes": "Ateliers pratiques, comparaison humain / IA, chasse aux erreurs",
         "evaluation": "Production guidée commentée"},
        {"code": "M3.1", "cp": "CP8", "bloc": "CCP3", "intitule": "Analyser la performance commerciale de son périmètre",
         "objectif": "Collecter, calculer et analyser les indicateurs commerciaux, puis alerter sa hiérarchie.",
         "jours": [
             ("Les indicateurs de performance commerciale", "Calculer CA, panier moyen, indice de vente, taux de transformation, fréquentation."),
             ("Collecter et fiabiliser les données", "Collecter les données et vérifier leur fiabilité en croisant les sources."),
             ("Construire et renseigner un tableau de bord", "Construire un tableau de bord avec graphiques et tableau croisé."),
             ("Détecter et analyser les écarts", "Comparer aux objectifs et au N-1, distinguer causes internes et externes."),
             ("Alerter et rendre compte dans les délais", "Choisir le bon canal et le bon moment pour alerter et respecter le rythme de reporting."),
             ("Rédiger une analyse claire pour la hiérarchie", "Rédiger une analyse structurée, claire et argumentée."),
         ],
         "methodes": "Études de cas chiffrées, enquête sur une baisse de résultat, ateliers tableur",
         "evaluation": "Analyse écrite commentée"},
        {"code": "M3.2", "cp": "CP9", "bloc": "CCP3", "intitule": "Analyser la rentabilité de son périmètre",
         "objectif": "Calculer et interpréter les indicateurs de rentabilité et formuler des pistes d'optimisation.",
         "jours": [
             ("Compte de résultat du périmètre", "Identifier les composantes du compte de résultat d'un périmètre."),
             ("Marge, prix et démarque", "Calculer taux de marge, taux de marque, démarque, en tenant compte des coûts locaux."),
             ("Frais de personnel et productivité", "Calculer la productivité horaire et le ratio frais de personnel sur chiffre d'affaires."),
             ("Rotation des stocks et coûts", "Calculer la rotation des stocks et identifier les postes de coûts."),
             ("Analyser les écarts de rentabilité", "Analyser les écarts entre prévisionnel et réalisé et en identifier les causes."),
             ("Simuler et proposer des pistes d'optimisation", "Réaliser des simulations simples (prix, effectif, stock) et proposer des pistes."),
         ],
         "methodes": "Exercices chiffrés, simulations sur tableur, jeu de fixation de prix",
         "evaluation": "Exercices corrigés"},
        {"code": "M3.3", "cp": "CP10", "bloc": "CCP3", "intitule": "Proposer des actions correctives et suivre le plan d'actions",
         "objectif": "Proposer à sa hiérarchie un plan d'actions réaliste et en assurer le suivi.",
         "jours": [
             ("Démarche de résolution de problème", "Utiliser les outils Ishikawa, Pareto et QQOQCP pour poser un diagnostic."),
             ("Construire un plan d'actions", "Formaliser un plan d'actions : objectifs, moyens, échéances, responsables, indicateurs."),
             ("Argumenter auprès de la hiérarchie", "Présenter des propositions argumentées et chiffrées, adaptées aux moyens disponibles."),
             ("Mettre en œuvre avec l'équipe", "Informer l'équipe, organiser et suivre la mise en œuvre des actions validées."),
             ("Mesurer les résultats et les écarts persistants", "Mesurer l'impact des actions et identifier les écarts persistants."),
             ("Ajuster et rendre compte", "Proposer des ajustements réalistes et rédiger un compte rendu d'avancement."),
         ],
         "methodes": "Pitch devant un jury de pairs, études de cas, retours d'expérience de la période en entreprise",
         "evaluation": "Présentation orale commentée"},
        {"code": "T3", "cp": "Épreuves", "bloc": "Transversal", "intitule": "Productions d'examen et dossier professionnel",
         "objectif": "Finaliser les deux documents, les deux diaporamas et le dossier professionnel exigés par le référentiel d'évaluation.",
         "jours": [
             ("Document et diaporama « Performance et rentabilité »", "Structurer et finaliser le document (12 à 18 pages) et le diaporama (12 à 18 diapositives)."),
             ("Document et diaporama « Manager l'équipe »", "Structurer et finaliser le document (16 à 24 pages) et le diaporama (18 à 24 diapositives)."),
             ("Dossier professionnel", "Rédiger et finaliser le dossier professionnel et rassembler la preuve de période en entreprise."),
         ],
         "methodes": "Ateliers de rédaction, relecture croisée, accompagnement individuel",
         "evaluation": "Vérification de conformité aux exigences du référentiel d'évaluation"},
        {"code": "T5", "cp": "Épreuves", "bloc": "Transversal", "intitule": "Entraînement aux épreuves du titre",
         "objectif": "Se présenter à la session de validation dans les conditions réelles.",
         "jours": [
             ("Mise en situation professionnelle blanche", "Réaliser une étude de cas de 4 h sur poste, en conditions d'examen."),
             ("Entretien technique et présentations blanches", "Présenter ses travaux et ses diaporamas devant un jury blanc."),
             ("Entretien final et préparation mentale", "Préparer l'entretien final et gérer son stress le jour de l'examen."),
         ],
         "methodes": "Session blanche avec professionnels invités",
         "evaluation": "Retour individualisé du jury blanc"},
    ],
    # Alternance centre / entreprise. « PAE:n » = n jours en entreprise.
    "ordre": ["M0", "T2", "M1.1", "M1.2", "M1.3", "M1.4", "T4", "M2.1", "M2.2", "M2.3", "T6",
              "PAE:20", "T1", "M3.1", "M3.2", "M3.3", "PAE:20", "T3", "T5"],
}

RPMS = {
    "code": "RPMS",
    "rncp": "RNCP38575",
    "intitule": "Titre professionnel Responsable de petite ou moyenne structure",
    "court": "Responsable de petite ou moyenne structure",
    "niveau": "Niveau 5 (cadre national des certifications 2019)",
    "arrete": "Arrêté du 5 décembre 2023 (JO du 20/12/2023) — parcours depuis le 08/02/2024, enregistrement jusqu'au 08/02/2029",
    "reac": "Compétences de la fiche RNCP38575 (version en vigueur). REAC et référentiel d'évaluation millésime 08 (2023) [À VÉRIFIER : documents à joindre — ceux transmis concernent l'ancienne version RNCP35646 de 2016]",
    "rome": "M1302 — Direction de petite ou moyenne entreprise",
    "nsf": "310p — Spécialités plurivalentes des échanges et de la gestion",
    "formacode": "32094, 13175, 32008, 32047, 32048",
    "certificateur": "Ministère du Travail, du Plein Emploi et de l'Insertion",
    "pae": 210,
    "pae_blocs": (105, 105),
    "pae_source": "210 h minimum — référentiel d'évaluation RPMS v08 (21/12/2023), cité par plusieurs organismes ; à confirmer sur le document officiel",
    "session": "1 h 35 par candidat : présentation d'un projet réalisé en amont 45 min, entretien technique 30 min, entretien final 20 min",
    "jury": "[À VÉRIFIER : conditions de présence du jury dans le référentiel d'évaluation v08]",
    "productions": [
        "Dossier de projet présentant un ou plusieurs projets réalisés en amont, couvrant les compétences des 3 CCP, et diaporama de présentation.",
        "Dossier professionnel (DP) et preuve de la période en entreprise.",
        "[À VÉRIFIER : nombre de pages et consignes de forme dans le référentiel d'évaluation v08]",
    ],
    "emplois": "Manager, chef, responsable, directeur adjoint, directeur ou délégué d'agence, d'unité, de centre de profit, de site, d'établissement, d'entreprise ou d'association (moins de 50 salariés)",
    "insertion": "Insertion globale à 6 mois : 69 % ; dans le métier visé à 6 mois : 66 % ; à 2 ans : 78 % (440 certifiés en 2022) — fiche RNCP38575",
    "public": "Salariés en évolution vers une fonction de direction, créateurs et repreneurs d'entreprise, responsables associatifs, demandeurs d'emploi expérimentés, personnes en situation de handicap (parcours adapté).",
    "prerequis": [
        "Aucun prérequis réglementaire n'est fixé par le titre.",
        "Critères d'admission YEBA FORMATIONS : au moins 2 ans d'expérience professionnelle (encadrement, gestion, commerce ou responsabilité associative) OU projet de création ou de reprise étayé ; niveau 4 conseillé.",
        "Admission après : information collective, positionnement et entretien individuel de motivation.",
    ],
    "transversales": [
        ("Sécurité, QVCT et non-discrimination", "Intégrer la sécurité, la qualité de vie et des conditions de travail et la non-discrimination dans toutes les activités (fiche RNCP38575)."),
        ("Handicap", "Prendre en compte les personnes en situation de handicap sur le plan social (fiche RNCP38575)."),
        ("Développement durable", "Être vigilant aux critères environnementaux et du développement durable (fiche RNCP38575)."),
        ("Veille et adaptation", "Exercer une veille permanente et adapter sa gestion aux évolutions (fiche RNCP38575)."),
        ("Anglais", "Répondre à des demandes simples d'un interlocuteur anglophone selon le contexte (fiche RNCP38575)."),
    ],
    "blocs": [
        ("CCP1", "RNCP38575BC01", "Diriger une structure avec une équipe",
         "Présentation d'un projet réalisé en amont (30 min) puis entretien technique (15 min)"),
        ("CCP2", "RNCP38575BC02", "Mettre en œuvre l'objet social de la structure",
         "Présentation d'un projet réalisé en amont (30 min) puis entretien technique (15 min)"),
        ("CCP3", "RNCP38575BC03", "Établir et présenter un rapport d'activité de la structure",
         "Présentation d'un projet réalisé en amont (30 min) puis entretien technique (15 min)"),
    ],
    "modules": [
        {"code": "M0", "cp": "—", "bloc": "Transversal", "intitule": "Accueil, intégration et positionnement",
         "objectif": "Comprendre le parcours, ses règles et ses exigences, et choisir son projet fil rouge.",
         "jours": [
             ("Bienvenue et découverte du parcours", "Identifier les étapes du parcours, les 3 CCP, le dossier de projet et l'épreuve."),
             ("Positionnement et projet fil rouge", "Situer ses acquis et choisir la structure réelle ou en création qui servira de projet fil rouge."),
         ],
         "methodes": "Présentation interactive, pitch de 60 secondes, entretiens individuels",
         "evaluation": "Positionnement (non noté) et entretien individuel"},
        {"code": "M1.1", "cp": "CP1", "bloc": "CCP1", "intitule": "Développer une vision systémique de la structure dans son environnement",
         "objectif": "Analyser la structure, sa gouvernance et ses interactions avec son environnement.",
         "jours": [
             ("Formes juridiques et gouvernance", "Identifier la forme juridique, la gouvernance et les instances d'une structure."),
             ("Responsabilités du dirigeant", "Mesurer la responsabilité civile et pénale du dirigeant et le principe de délégation."),
             ("Analyse de l'environnement externe", "Réaliser une analyse PESTEL de la structure."),
             ("Analyse interne et chaîne de valeur", "Analyser les ressources, les processus et la chaîne de valeur."),
             ("Diagnostic stratégique", "Réaliser une synthèse SWOT et en tirer les enjeux prioritaires."),
             ("Veille et conformité", "Organiser une veille ; identifier les obligations RGPD, IA Act et cybersécurité."),
             ("Traduire la stratégie en objectifs", "Traduire les orientations stratégiques en objectifs opérationnels."),
         ],
         "methodes": "Études de cas, carte mentale de la structure, analyse d'un cas réunionnais fictif",
         "evaluation": "Diagnostic écrit du projet fil rouge"},
        {"code": "M1.2", "cp": "CP2", "bloc": "CCP1", "intitule": "Inscrire la structure dans son territoire",
         "objectif": "Positionner la structure dans son écosystème et développer ses partenariats.",
         "jours": [
             ("L'écosystème économique réunionnais", "Identifier les acteurs du territoire : collectivités, chambres consulaires, réseaux."),
             ("Cartographier les parties prenantes", "Cartographier les parties prenantes et leurs attentes."),
             ("RSE et développement durable", "Intégrer une démarche RSE adaptée à une petite structure."),
             ("Partenariats et marchés publics", "Identifier des partenariats, l'économie sociale et solidaire et l'accès aux marchés publics."),
             ("Représenter la structure et négocier", "Représenter la structure et conduire une négociation simple."),
         ],
         "methodes": "Rallye des acteurs locaux, témoignage de dirigeant, jeux de négociation",
         "evaluation": "Cartographie des parties prenantes"},
        {"code": "M1.3", "cp": "CP3", "bloc": "CCP1", "intitule": "Manager et animer une équipe",
         "objectif": "Diriger une équipe au quotidien dans le respect du droit du travail et de la QVCT.",
         "jours": [
             ("Droit du travail essentiel", "Appliquer les règles essentielles : contrats, durée, discipline."),
             ("Dialogue social et représentation du personnel", "Identifier les obligations liées au CSE et au dialogue social."),
             ("Santé, sécurité et DUERP", "Évaluer les risques professionnels et tenir le document unique."),
             ("Qualité de vie et des conditions de travail", "Mettre en place des actions de QVCT adaptées à une petite structure."),
             ("Recruter et intégrer sans discriminer", "Conduire un recrutement non discriminant et organiser l'intégration."),
             ("Handicap et obligation d'emploi", "Appliquer l'obligation d'emploi et organiser les aménagements de poste."),
             ("Entretiens et développement des compétences", "Conduire les entretiens et construire un plan de développement des compétences."),
             ("Déléguer, animer et motiver", "Déléguer, animer des réunions et motiver l'équipe."),
             ("Prévenir et gérer les conflits", "Prévenir les tensions et gérer un conflit."),
             ("Priorités, aléas et continuité d'activité", "Hiérarchiser les priorités et gérer les aléas, dont le risque cyclonique."),
         ],
         "methodes": "Jeux de rôle, études de cas, simulation d'alerte cyclonique",
         "evaluation": "Mise en situation commentée"},
        {"code": "T4", "cp": "—", "bloc": "Transversal", "intitule": "Préparer la période en entreprise",
         "objectif": "Trouver la structure d'accueil et préparer la collecte des éléments du dossier de projet.",
         "jours": [
             ("Trouver sa structure d'accueil", "Prospecter une structure d'accueil compatible avec son projet fil rouge."),
             ("Objectifs de la période et dossier de projet", "Fixer avec le tuteur les objectifs de la période et les éléments à recueillir."),
         ],
         "methodes": "Atelier de prospection, préparation de la convention",
         "evaluation": "Convention signée et objectifs écrits"},
        {"code": "M2.1", "cp": "CP4", "bloc": "CCP2", "intitule": "Adapter l'offre de la structure à la demande",
         "objectif": "Analyser le marché et faire évoluer l'offre de biens et de services.",
         "jours": [
             ("Comprendre son marché", "Définir le marché, la demande et la concurrence de la structure."),
             ("Sources d'information", "Exploiter des sources fiables : INSEE, chambres consulaires, études."),
             ("Enquête de terrain", "Concevoir et conduire une enquête de terrain simple."),
             ("Segmenter et cibler", "Segmenter la clientèle et choisir ses cibles."),
             ("Positionner l'offre", "Définir le positionnement de l'offre face à la concurrence."),
             ("Construire l'offre", "Construire une offre de biens ou de services adaptée aux cibles."),
             ("Fixer le prix", "Fixer un prix en tenant compte des coûts, de la demande et de la concurrence."),
             ("Innover et faire évoluer l'offre", "Proposer une innovation d'offre, y compris par des outils numériques."),
             ("Présenter l'offre adaptée", "Présenter une offre adaptée de façon argumentée."),
         ],
         "methodes": "Défi de création d'offre, enquête en binômes, études de cas",
         "evaluation": "Étude de marché du projet fil rouge"},
        {"code": "M2.2", "cp": "CP5", "bloc": "CCP2", "intitule": "Organiser et développer la diffusion de l'offre",
         "objectif": "Construire et piloter un plan d'action commercial.",
         "jours": [
             ("Plan d'action commercial", "Construire un plan d'action commercial avec objectifs et budget."),
             ("Canaux de distribution", "Choisir les canaux de distribution adaptés."),
             ("Marketing digital", "Définir des actions de marketing digital adaptées à une petite structure."),
             ("Site et réseaux sociaux conformes", "Vérifier la conformité d'un site et de réseaux sociaux (mentions légales, cookies, RGPD)."),
             ("Prospecter", "Organiser une action de prospection."),
             ("Négocier", "Conduire une négociation commerciale."),
             ("Fidéliser", "Mettre en place des actions de fidélisation."),
             ("Piloter les actions commerciales", "Suivre les résultats des actions commerciales et les ajuster."),
         ],
         "methodes": "Négociations chronométrées, ateliers, études de cas",
         "evaluation": "Plan d'action commercial présenté"},
        {"code": "T2", "cp": "Fiche RNCP", "bloc": "Transversal", "intitule": "Anglais professionnel de base",
         "objectif": "Répondre à des demandes simples d'un interlocuteur anglophone.",
         "jours": [
             ("Accueil et téléphone en anglais", "Accueillir et répondre au téléphone en anglais simple."),
             ("Échanges écrits simples en anglais", "Rédiger et comprendre un e-mail professionnel simple."),
         ],
         "methodes": "Jeux de rôle, mises en situation",
         "evaluation": "Mise en situation orale"},
        {"code": "T6", "cp": "—", "bloc": "Transversal", "intitule": "Bilan individuel de mi-parcours",
         "objectif": "Faire le point sur sa progression, ses freins et son projet avant la période en entreprise.",
         "jours": [
             ("Bilan de mi-parcours", "Faire le bilan de ses acquis et ajuster son parcours."),
         ],
         "methodes": "Entretiens individuels",
         "evaluation": "Fiche de suivi individuel"},
        {"code": "M2.3", "cp": "CP6", "bloc": "CCP2", "intitule": "Organiser la production",
         "objectif": "Organiser la production de biens ou de services avec qualité et efficience.",
         "jours": [
             ("Processus et cartographie", "Cartographier les processus de production de la structure."),
             ("Qualité et amélioration continue", "Mettre en place une démarche qualité simple (PDCA)."),
             ("Achats et fournisseurs", "Organiser les achats et choisir des fournisseurs."),
             ("Stocks et logistique insulaire", "Gérer les stocks en tenant compte des contraintes insulaires."),
             ("Planifier la production", "Planifier la production selon la demande et les ressources."),
             ("Gérer les aléas de production", "Anticiper et gérer les aléas de production."),
             ("Automatiser et digitaliser simplement", "Identifier les tâches automatisables avec des outils souverains."),
             ("Indicateurs de production", "Suivre des indicateurs de production et de qualité."),
         ],
         "methodes": "Jeu de simulation de production, études de cas",
         "evaluation": "Cartographie de processus"},
        {"code": "T1", "cp": "Fiche RNCP", "bloc": "Transversal", "intitule": "IA, données et gouvernance du dirigeant",
         "objectif": "Piloter l'usage de l'IA dans une petite structure de façon rentable et conforme.",
         "jours": [
             ("Comprendre l'IA générative", "Expliquer le fonctionnement, l'intérêt et les limites de l'IA générative."),
             ("L'IA au service de la direction", "Utiliser l'IA pour la veille, les synthèses et la rédaction, en vérifiant les résultats."),
             ("Workflows et automatisations", "Concevoir un workflow simple avec des outils hébergés dans l'Union européenne."),
             ("RGPD du dirigeant", "Tenir un registre, choisir une base légale, encadrer les sous-traitants, gérer une violation."),
             ("IA Act et cybersécurité", "Appliquer l'IA Act (maîtrise de l'IA, usages interdits et à haut risque) et les règles de base de l'ANSSI."),
             ("Charte d'usage de l'IA", "Rédiger une charte d'usage de l'IA pour son équipe."),
         ],
         "methodes": "Ateliers pratiques, cas réels de TPE-PME",
         "evaluation": "Charte IA du projet fil rouge"},
        {"code": "M3.1", "cp": "CP7", "bloc": "CCP3", "intitule": "Analyser le bilan de la structure",
         "objectif": "Lire et interpréter le bilan d'une structure.",
         "jours": [
             ("Structure du bilan", "Identifier les grandes masses du bilan."),
             ("L'actif", "Analyser les postes de l'actif."),
             ("Le passif", "Analyser les capitaux propres et les dettes."),
             ("Fonds de roulement, BFR et trésorerie", "Calculer et interpréter le fonds de roulement, le BFR et la trésorerie."),
             ("Ratios de structure", "Calculer et interpréter les ratios de structure et de solvabilité."),
             ("Lire une liasse fiscale", "Lire une liasse fiscale anonymisée."),
             ("Diagnostic financier", "Rédiger un diagnostic financier à partir du bilan."),
         ],
         "methodes": "Exercices sur cas réels anonymisés, jeu de devinette du métier à partir du bilan",
         "evaluation": "Exercices corrigés"},
        {"code": "M3.2", "cp": "CP8", "bloc": "CCP3", "intitule": "Analyser le compte de résultat de la structure",
         "objectif": "Interpréter le compte de résultat et piloter la rentabilité.",
         "jours": [
             ("Lire le compte de résultat", "Identifier les charges et les produits."),
             ("Soldes intermédiaires de gestion", "Calculer et interpréter les soldes intermédiaires de gestion."),
             ("Capacité d'autofinancement", "Calculer et interpréter la capacité d'autofinancement."),
             ("Seuil de rentabilité", "Calculer le seuil de rentabilité et le point mort."),
             ("Budget prévisionnel", "Construire un budget prévisionnel simple."),
             ("Plan de trésorerie", "Construire et suivre un plan de trésorerie."),
             ("Tableau de bord du dirigeant", "Construire un tableau de bord de pilotage."),
         ],
         "methodes": "Simulations sur tableur, jeu de gestion de trésorerie",
         "evaluation": "Tableau de bord du projet fil rouge"},
        {"code": "M3.3", "cp": "CP9", "bloc": "CCP3", "intitule": "Rédiger le rapport d'activité de la structure",
         "objectif": "Produire et présenter un rapport d'activité clair à la gouvernance.",
         "jours": [
             ("Structure d'un rapport d'activité", "Construire le plan d'un rapport d'activité."),
             ("Indicateurs extra-financiers", "Intégrer des indicateurs sociaux et environnementaux."),
             ("Rédiger clairement", "Rédiger de façon claire, factuelle et synthétique."),
             ("Rendre le rapport accessible", "Rendre un document accessible (lisibilité, contrastes, structure)."),
             ("Présenter à la gouvernance", "Présenter le rapport à l'oral devant la gouvernance."),
             ("Répondre aux questions", "Répondre aux questions et objections de la gouvernance."),
         ],
         "methodes": "Assemblée générale simulée, ateliers de rédaction",
         "evaluation": "Rapport d'activité rédigé"},
        {"code": "T3", "cp": "Épreuves", "bloc": "Transversal", "intitule": "Dossier de projet, dossier professionnel et diaporama",
         "objectif": "Finaliser le dossier de projet, le diaporama et le dossier professionnel.",
         "jours": [
             ("Dossier de projet", "Structurer le dossier de projet couvrant les 3 CCP."),
             ("Diaporama de présentation", "Concevoir le diaporama de la présentation de 45 minutes."),
             ("Dossier professionnel", "Finaliser le dossier professionnel et la preuve de période en entreprise."),
         ],
         "methodes": "Ateliers de rédaction, relecture croisée",
         "evaluation": "Vérification de conformité aux exigences du référentiel d'évaluation"},
        {"code": "T5", "cp": "Épreuves", "bloc": "Transversal", "intitule": "Entraînement à l'épreuve du titre",
         "objectif": "Présenter son projet et répondre au jury avec aisance.",
         "jours": [
             ("Présentation blanche", "Présenter son projet en 45 minutes devant un jury blanc."),
             ("Entretiens technique et final blancs", "Répondre aux questions techniques et à l'entretien final."),
         ],
         "methodes": "Jury blanc composé de dirigeants invités",
         "evaluation": "Retour individualisé du jury blanc"},
    ],
    "ordre": ["M0", "M1.1", "M1.2", "M1.3", "T4", "M2.1", "M2.2", "T2", "T6",
              "PAE:15", "M2.3", "T1", "M3.1", "M3.2", "M3.3", "PAE:15", "T3", "T5"],
}

TITRES = (MEM, RPMS)


def heures(module):
    return len(module["jours"]) * DUREE_JOUR


def heures_centre(titre):
    return sum(heures(m) for m in titre["modules"])


def jours_centre(titre):
    return sum(len(m["jours"]) for m in titre["modules"])


def module(titre, code):
    return next(m for m in titre["modules"] if m["code"] == code)


def sequence(titre):
    """Liste ordonnée des journées : ('Centre', module, n°, titre, objectif) ou ('Entreprise', ...)."""
    out, pae = [], 0
    for etape in titre["ordre"]:
        if etape.startswith("PAE:"):
            pae += 1
            n = int(etape.split(":")[1])
            for k in range(n):
                out.append(("Entreprise", None, k + 1, f"Période en entreprise n° {pae} — jour {k + 1}/{n}",
                            "Mettre en œuvre les compétences en situation réelle et recueillir les éléments des productions."))
            continue
        m = module(titre, etape)
        for k, (t, o) in enumerate(m["jours"]):
            out.append(("Centre", m, k + 1, t, o))
    return out


if __name__ == "__main__":
    for t in TITRES:
        seq = sequence(t)
        pae_h = sum(DUREE_JOUR for s in seq if s[0] == "Entreprise")
        print(t["code"], "centre", heures_centre(t), "h /", jours_centre(t), "jours ; PAE", pae_h, "h")
        assert pae_h == t["pae"], (pae_h, t["pae"])
        assert set(t["ordre"]) - {e for e in t["ordre"] if e.startswith("PAE")} == {m["code"] for m in t["modules"]}
