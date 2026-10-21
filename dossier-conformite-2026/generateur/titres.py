"""Référentiel pédagogique YEBA FORMATIONS pour les deux titres professionnels.

Sources : fiches France Compétences RNCP41853 (MEM) et RNCP38575 (RPMS),
consultées le 21/10/2026. La découpe en modules et le volume horaire en centre
sont des choix pédagogiques de l'organisme (le RNCP ne fixe pas de durée).
"""

# Chaque module : code, intitulé, heures, CCP rattaché, objectif opérationnel,
# contenus, méthodes / exemples, évaluation formative.
MEM = {
    "code": "MEM",
    "rncp": "RNCP41853",
    "intitule": "Titre professionnel Manager d'établissement marchand",
    "niveau": "Niveau 5 (cadre national des certifications)",
    "arrete": "Arrêté du 4 décembre 2025 (JO) — parcours certifiants à partir du 03/03/2026, échéance 02/03/2031",
    "rome": "D1502, D1503, D1508, D1509",
    "certificateur": "Ministère du Travail, du Plein Emploi et de l'Insertion",
    "pae": 280,
    "pae_source": "280 h minimum — article 6 de l'arrêté du 4 décembre 2025 (cité sur la fiche RNCP41853)",
    "session": "7 h 55 par candidat (mise en situation professionnelle 4 h + entretien technique 1 h 30 + questionnement à partir de productions 2 h 10 + entretien final 15 min)",
    "blocs": [
        ("CCP1 — RNCP41853BC01", "Manager l'équipe de son périmètre au sein de l'établissement marchand"),
        ("CCP2 — RNCP41853BC02", "Développer la dynamique commerciale de son périmètre au sein de l'établissement marchand"),
        ("CCP3 — RNCP41853BC03", "Contribuer à la performance commerciale et à la rentabilité de son périmètre au sein de l'établissement marchand"),
    ],
    "emplois": "Manager de rayon, chef de rayon, responsable de boutique / de magasin / de point de vente, manager de surface de vente, gérant de magasin, responsable de département",
    "insertion": "Taux d'insertion global à 6 mois : 76 % (2024) — 78 % (2023) ; dans le métier visé à 6 mois : 65 % (2024) — source : fiche RNCP41853, statistiques de l'ancienne version RNCP38676",
    "public": "Demandeurs d'emploi (orientés par France Travail ou les Missions Locales), salariés en reconversion ou en évolution (CPF, projet de transition professionnelle, plan de développement des compétences), personnes en situation de handicap (parcours adapté).",
    "prerequis": [
        "Aucun prérequis réglementaire fixé par le titre.",
        "Critères d'admission YEBA FORMATIONS : expérience dans la vente, le commerce ou l'encadrement (même courte, y compris job étudiant) OU niveau 4 (bac) ; maîtrise du français écrit et oral ; bases de l'outil informatique.",
        "Validation par : information collective + test de positionnement + entretien individuel de motivation (projet professionnel).",
    ],
    "modules": [
        ("M0", "Accueil, intégration et positionnement", 14, "Transversal",
         "Situer son parcours, ses droits et devoirs, et ses acquis de départ.",
         ["Présentation du titre, des 3 CCP, des épreuves et de la période en entreprise", "Règlement intérieur, livret d'accueil, contrat d'engagement", "Test de positionnement et parcours individualisé", "Sensibilisation santé-sécurité au travail, droits du stagiaire", "Information RGPD : quelles données, pourquoi, combien de temps"],
         "Jeu « Le magasin idéal » en équipes ; visite virtuelle d'un hypermarché réunionnais ; photo-langage « mon meilleur et mon pire manager »",
         "Test de positionnement (non noté) + entretien individuel"),
        ("M1.1", "Animer l'équipe de son périmètre", 35, "CCP1",
         "Conduire un briefing, un débriefing et une réunion d'équipe qui mobilisent.",
         ["Styles de management et leadership situationnel", "Briefing de 5 minutes / débriefing de fin de journée", "Communication assertive, écoute active, feed-back", "Prévention et gestion des tensions et conflits", "Démarche de maîtrise des risques professionnels (DUERP, gestes et postures, EPI)"],
         "Jeu de rôle « Le lundi après le cyclone » : briefing d'une équipe démotivée après 3 jours de fermeture ; vidéo-analyse des briefings filmés (avec accord écrit)",
         "Mise en situation filmée + grille d'observation"),
        ("M1.2", "Planifier et coordonner l'activité de l'équipe", 35, "CCP1",
         "Construire un planning conforme au droit du travail et aux flux clients.",
         ["Bases du droit du travail : durée, repos, dimanches et jours fériés, temps partiel", "Planning hebdomadaire selon les flux (rentrée scolaire, fêtes de fin d'année, cyclone)", "Prise en compte des besoins spécifiques des collaborateurs en situation de handicap", "Délégation, suivi et contrôle des tâches", "Outils numériques de planification (tableur ; IA d'aide à la planification — décision humaine finale)"],
         "Cas « La veille de Noël à la zone commerciale » : 12 personnes, 2 absents, 1 salarié avec aménagement de poste",
         "Production d'un planning commenté (tableur)"),
        ("M1.3", "Accompagner la performance individuelle des collaborateurs", 35, "CCP1",
         "Fixer des objectifs, conduire un entretien et organiser une montée en compétences.",
         ["Objectifs SMART et indicateurs individuels", "Entretien de recadrage, entretien de félicitations, entretien annuel/professionnel", "Repérer les besoins en compétences ; animer une action de professionnalisation courte", "Motivation et reconnaissance (sans surveillance automatisée des salariés)"],
         "Duo filmé « Le vendeur star qui arrive toujours en retard » ; atelier « former un nouveau en 15 minutes au rayon »",
         "Jeu de rôle évalué par grille critériée"),
        ("M1.4", "Contribuer au recrutement et à l'intégration", 35, "CCP1",
         "Définir un besoin, sélectionner sans discriminer et réussir une intégration.",
         ["Analyse du besoin et fiche de poste", "Annonce, tri des candidatures sans discrimination (25 critères légaux)", "RGPD du recrutement : données collectées, durée de conservation, information du candidat", "IA Act : un outil d'IA qui trie ou classe des candidats est un système à haut risque — usage interdit en formation sans encadrement", "Conduite d'entretien, période d'essai, parcours d'intégration (onboarding), adaptation du poste de travail"],
         "Jeu « Le CV mystère » (CV anonymisés fictifs) ; débat : « l'IA peut-elle choisir mon prochain vendeur ? »",
         "Quiz + simulation d'entretien de recrutement"),
        ("M2.1", "Gérer l'approvisionnement de son périmètre", 49, "CCP2",
         "Anticiper les besoins, commander, réceptionner et stocker en limitant le gaspillage.",
         ["Analyse des stocks, prévisions de ventes, tendances, capacités de stockage", "Spécificités réunionnaises : délais maritimes, conteneurs, octroi de mer, ruptures", "Réception, contrôle, stockage, inventaire, démarque connue/inconnue", "Démarche RSE : déchets, anti-gaspillage (loi AGEC), dons alimentaires", "Prévisions assistées par IA : intérêt et limites (biais, données manquantes)"],
         "Simulation « Le conteneur bloqué au Port » : recalculer les commandes avec 3 semaines de retard ; défi anti-gaspi sur un rayon frais",
         "Étude de cas chiffrée sur tableur"),
        ("M2.2", "Organiser et mettre en œuvre le merchandising", 56, "CCP2",
         "Implanter l'offre et conduire une opération commerciale rentable.",
         ["Règles de merchandising : zones chaudes/froides, facing, planogramme", "Calendrier commercial réunionnais (rentrée de janvier, fête Dipavali, Nouvel an chinois, fêtes de fin d'année)", "Opérations commerciales, promotions, signalétique, PLV", "Analyse des résultats commerciaux et budgétaires d'une implantation", "Omnicanal : click & collect, réseaux sociaux, avis clients"],
         "Atelier maquette : réimplanter un rayon en carton à l'échelle ; « avant/après » photographiés",
         "Projet d'implantation présenté à l'oral"),
        ("M2.3", "Participer à l'amélioration de l'expérience client", 49, "CCP2",
         "Mesurer et améliorer la satisfaction client, y compris pour les clients en situation de handicap.",
         ["Parcours client, moments de vérité, accueil", "Accueil des clients en situation de handicap (visible ou non)", "Argumentaires adaptés, traitement des objections et réclamations", "Mesure de la satisfaction ; analyse des avis clients (IA possible sur données anonymisées)", "Plan d'amélioration et sensibilisation de l'équipe"],
         "Client mystère en binôme dans des enseignes locales (grille fournie, aucune photo de personnes) ; jeu « réclamation explosive »",
         "Rapport client mystère + plan d'action"),
        ("M3.1", "Analyser la performance commerciale de son périmètre", 42, "CCP3",
         "Lire et commenter un tableau de bord commercial.",
         ["Indicateurs : CA, panier moyen, indice de vente, taux de transformation, fréquentation, démarque", "Comparaisons N/N-1, objectifs, écarts", "Construction d'un tableau de bord sur tableur", "Visualisation et commentaire des résultats ; IA pour reformuler, jamais pour inventer un chiffre"],
         "Enquête « Qui a volé la marge ? » : retrouver dans les chiffres l'origine d'une baisse de résultat",
         "Tableau de bord commenté"),
        ("M3.2", "Analyser la rentabilité de son périmètre", 42, "CCP3",
         "Calculer et interpréter marge, frais et contribution du rayon.",
         ["Marge brute, taux de marque, coefficient multiplicateur", "Compte d'exploitation du rayon, frais de personnel, ratios de productivité", "Budget prévisionnel et suivi", "Seuil de rentabilité appliqué au point de vente"],
         "Jeu « Le juste prix péi » : fixer un prix de vente avec octroi de mer et transport",
         "Exercices chiffrés corrigés"),
        ("M3.3", "Proposer des actions correctives et suivre le plan d'actions", 42, "CCP3",
         "Présenter à sa hiérarchie un plan d'actions argumenté et en assurer le suivi.",
         ["Diagnostic, causes racines (5 pourquoi, Ishikawa)", "Plan d'actions : qui, quoi, quand, combien, indicateurs", "Présentation orale à la hiérarchie, diaporama efficace", "Suivi, ajustements, retour d'expérience"],
         "« Pitch au directeur régional » : 10 minutes pour convaincre, jury de pairs",
         "Présentation orale évaluée par grille critériée"),
        ("T1", "IA appliquée au management et au commerce (module distinctif YEBA)", 42, "Transversal",
         "Utiliser l'IA générative de façon productive, éthique et conforme (RGPD / IA Act).",
         ["Notions d'IA, IA générative, limites (hallucinations, biais)", "Rédiger des consignes (prompts) efficaces : annonces, argumentaires, plannings, synthèses", "Outils respectant la souveraineté européenne des données (ex. solutions hébergées dans l'UE)", "RGPD : jamais de données personnelles de clients ou salariés dans un outil non validé", "IA Act : obligation de maîtrise de l'IA (art. 4), pratiques interdites (art. 5), systèmes à haut risque (RH)", "Vérifier, citer, garder la décision humaine"],
         "Duel « Humain contre IA » sur un argumentaire produit ; chasse aux hallucinations",
         "Production guidée + quiz IA Act"),
        ("T2", "Bureautique et tableur pour les épreuves", 21, "Transversal",
         "Maîtriser traitement de texte et tableur au niveau exigé par la mise en situation professionnelle.",
         ["Mise en forme de documents, impression", "Tableur : formules, pourcentages, graphiques, tableaux croisés simples", "Gestion des fichiers et maquettes fournies"],
         "Escape game tableur « Le coffre du magasin »",
         "Exercices chronométrés"),
        ("T3", "Dossier professionnel et productions pour l'examen", 21, "Transversal",
         "Rédiger le dossier professionnel et les deux productions + diaporamas exigés.",
         ["Dossier professionnel (DP) : choix des exemples issus de la période en entreprise", "Production CCP3 « performance et rentabilité » + diaporama (20 min)", "Production CCP1 « management » + diaporama (25 min)", "Relecture, accessibilité et lisibilité des supports"],
         "Atelier « relecture croisée » entre stagiaires",
         "Relecture formateur + grille de conformité"),
        ("T4", "Préparation de la période en entreprise et recherche d'emploi", 14, "Transversal",
         "Trouver la structure d'accueil, préparer les objectifs de la période en entreprise et son insertion.",
         ["Prospection d'entreprises d'accueil, CV, lettre, réseaux professionnels", "Convention de stage tripartite et objectifs de la période", "Préparation à l'entretien d'embauche", "Sensibilisation à la création / reprise d'entreprise"],
         "Job dating simulé avec des managers locaux invités",
         "Convention signée + plan de prospection"),
        ("T5", "Entraînement aux épreuves du titre", 21, "Transversal",
         "Se présenter à la session de validation en confiance.",
         ["Mise en situation professionnelle blanche (4 h, conditions réelles)", "Entretiens techniques blancs face à un jury de professionnels", "Gestion du stress et de la prise de parole", "Entretien final : comprendre les attentes du jury"],
         "Session blanche complète avec jury invité",
         "Résultats des épreuves blanches + plan de révision individuel"),
        ("T6", "Suivi individuel et prévention du décrochage", 7, "Transversal",
         "Repérer et lever tôt les freins à la poursuite du parcours.",
         ["Entretiens individuels de suivi (J+15, mi-parcours, avant session)", "Point sur les freins périphériques : mobilité, garde d'enfants, santé, logement", "Orientation vers les partenaires (Mission Locale, France Travail, CAF, MDPH)"],
         "Météo émotionnelle hebdomadaire ; tableau de progression visuel",
         "Fiche de suivi individuel"),
    ],
    # ordre de déroulement et alternance centre / entreprise (semaines de 35 h)
    "ordre": ["M0", "T2", "M1.1", "M1.2", "T4", "M1.3", "M1.4", "M2.1", "M2.2", "M2.3",
              "|PAE:140", "T1", "M3.1", "M3.2", "M3.3", "|PAE:140", "T3", "T5", "T6"],
}

RPMS = {
    "code": "RPMS",
    "rncp": "RNCP38575",
    "intitule": "Titre professionnel Responsable de petite ou moyenne structure",
    "niveau": "Niveau 5 (cadre national des certifications)",
    "arrete": "Arrêté du 5 décembre 2023 (JO du 20/12/2023) — parcours certifiants du 08/02/2024, échéance 08/02/2029",
    "rome": "M1302 — Direction de petite ou moyenne entreprise",
    "certificateur": "Ministère du Travail, du Plein Emploi et de l'Insertion",
    "pae": 210,
    "pae_source": "[À VÉRIFIER : 210 h minimum selon plusieurs organismes (icademie.com, etudis.net) — à confirmer dans l'arrêté du 5 décembre 2023 / référentiel de certification avant diffusion]",
    "session": "1 h 35 par candidat (présentation d'un projet réalisé en amont 45 min + entretien technique 30 min + entretien final 20 min)",
    "blocs": [
        ("CCP1 — RNCP38575BC01", "Diriger une structure avec une équipe"),
        ("CCP2 — RNCP38575BC02", "Mettre en œuvre l'objet social de la structure"),
        ("CCP3 — RNCP38575BC03", "Établir et présenter un rapport d'activité de la structure"),
    ],
    "emplois": "Manager, chef, responsable, directeur adjoint, directeur, délégué … de proximité, d'agence, d'unité, de centre de profit, de site, d'établissement, d'entreprise ou d'association (moins de 50 salariés)",
    "insertion": "Taux d'insertion global à 6 mois : 69 % ; dans le métier visé à 6 mois : 66 % ; à 2 ans : 78 % (440 certifiés en 2022) — source : fiche RNCP38575",
    "public": "Salariés en évolution vers une fonction de direction, créateurs et repreneurs d'entreprise, responsables associatifs, demandeurs d'emploi expérimentés (orientation France Travail), personnes en situation de handicap (parcours adapté).",
    "prerequis": [
        "Aucun prérequis réglementaire fixé par le titre.",
        "Critères d'admission YEBA FORMATIONS : expérience professionnelle d'au moins 2 ans (encadrement, gestion, commerce ou responsabilité associative) OU projet de création / reprise étayé ; niveau 4 recommandé.",
        "Validation par : information collective + test de positionnement (expression écrite, calculs de gestion) + entretien individuel de motivation.",
    ],
    "modules": [
        ("M0", "Accueil, intégration et positionnement", 14, "Transversal",
         "Situer son parcours, ses droits et devoirs, et ses acquis de départ.",
         ["Présentation du titre, des 3 CCP, du dossier de projet et de l'épreuve", "Règlement intérieur, livret d'accueil, contrat d'engagement", "Test de positionnement et parcours individualisé", "Choix du « projet fil rouge » (structure réelle ou de création)", "Information RGPD des stagiaires"],
         "Jeu « Pitch ta boîte en 60 secondes » ; carte d'identité des TPE-PME réunionnaises",
         "Test de positionnement + entretien individuel"),
        ("M1.1", "Développer une vision systémique de la structure", 49, "CCP1",
         "Analyser une structure dans son environnement et ses interactions.",
         ["Formes juridiques, gouvernance, statut du dirigeant", "Responsabilité civile et pénale du dirigeant, délégation de pouvoirs", "Diagnostics PESTEL, SWOT, chaîne de valeur", "Veille réglementaire, économique et technologique (dont IA)", "Conformité : RGPD, IA Act, cybersécurité (recommandations ANSSI)"],
         "Enquête « Autopsie d'une faillite » sur un cas réunionnais fictif ; carte mentale géante de la structure",
         "Diagnostic écrit du projet fil rouge"),
        ("M1.2", "Inscrire la structure dans son territoire", 35, "CCP1",
         "Positionner la structure dans l'écosystème local et ses réseaux.",
         ["Acteurs du territoire : Région Réunion, CCI, CMA, réseaux d'entreprises, collectivités", "Démarche RSE et développement durable", "Partenariats, marchés publics, économie sociale et solidaire", "Représenter la structure : négociation, prise de parole"],
         "Rallye « Qui fait quoi à La Réunion ? » ; intervention d'un chef d'entreprise local",
         "Cartographie des parties prenantes"),
        ("M1.3", "Manager et animer une équipe", 70, "CCP1",
         "Diriger au quotidien une équipe en respectant le droit du travail et la QVCT.",
         ["Droit du travail essentiel : contrats, durée, représentation du personnel, discipline", "Santé-sécurité : DUERP, prévention, QVCT", "Recrutement non discriminant, intégration, handicap (obligation d'emploi, aménagements)", "Entretiens, délégation, motivation, gestion des conflits", "Gestion des aléas et priorités (matrice d'Eisenhower, plan de continuité cyclonique)", "RGPD des données RH ; IA Act : outils RH à haut risque"],
         "Simulation « Alerte rouge cyclonique : que fait le dirigeant ? » ; jeux de rôle d'entretiens",
         "Jeu de rôle évalué par grille critériée"),
        ("M2.1", "Adapter l'offre de la structure à la demande", 63, "CCP2",
         "Analyser le marché et faire évoluer l'offre de biens et services.",
         ["Étude de marché (sources : INSEE Réunion, CCI, enquêtes terrain)", "Segmentation, ciblage, positionnement", "Construction de l'offre et du prix", "Innovation, IA et nouveaux services"],
         "Défi « Lancer un nouveau produit péi en 3 heures »",
         "Étude de marché du projet fil rouge"),
        ("M2.2", "Organiser et développer la diffusion de l'offre", 56, "CCP2",
         "Construire et piloter un plan d'action commercial.",
         ["Plan d'action commercial, canaux de distribution", "Marketing digital, réseaux sociaux, site internet (mentions légales, cookies : RGPD)", "Prospection, négociation, fidélisation", "Réponse simple à un interlocuteur anglophone"],
         "Négociation chronométrée « Le client de Maurice » (en partie en anglais)",
         "Plan d'action commercial présenté"),
        ("M2.3", "Organiser la production", 56, "CCP2",
         "Organiser la production de biens ou de services avec qualité et efficience.",
         ["Processus, cartographie, qualité, amélioration continue", "Achats, fournisseurs, stocks, logistique insulaire", "Planification de la production, gestion des aléas", "Automatisation et workflows (outils souverains)"],
         "Jeu « L'usine à samoussas » : optimiser une ligne de production en 3 tours",
         "Cartographie de processus"),
        ("M3.1", "Analyser le bilan de la structure", 49, "CCP3",
         "Lire et interpréter un bilan.",
         ["Actif, passif, fonds de roulement, BFR, trésorerie", "Ratios de structure et de solvabilité", "Lecture de liasses fiscales réelles anonymisées"],
         "« Le bilan raconte une histoire » : deviner le métier d'une entreprise à partir de son bilan",
         "Exercices corrigés"),
        ("M3.2", "Analyser le compte de résultat de la structure", 49, "CCP3",
         "Interpréter le compte de résultat et piloter la rentabilité.",
         ["Soldes intermédiaires de gestion, capacité d'autofinancement", "Seuil de rentabilité, point mort", "Budget, plan de trésorerie, tableau de bord", "Aides et financements des entreprises à La Réunion"],
         "Simulation « Trésorerie en eaux troubles » : passer un trimestre sans découvert",
         "Tableau de bord du projet fil rouge"),
        ("M3.3", "Rédiger le rapport d'activité de la structure", 42, "CCP3",
         "Produire et présenter un rapport d'activité clair à la gouvernance.",
         ["Structure d'un rapport d'activité", "Indicateurs extra-financiers (RSE, social)", "Rédaction claire, accessibilité des documents", "Présentation orale à la gouvernance"],
         "« Assemblée générale simulée » avec questions pièges",
         "Rapport d'activité rédigé"),
        ("T1", "IA, données et gouvernance du dirigeant (module distinctif YEBA)", 42, "Transversal",
         "Piloter l'usage de l'IA dans une petite structure de façon rentable et conforme.",
         ["IA générative : usages de direction (synthèses, veille, rédaction, analyse)", "Workflows et automatisations simples, choix d'outils souverains", "RGPD du dirigeant : registre, base légale, sous-traitants, violations", "IA Act : maîtrise de l'IA (art. 4), pratiques interdites, haut risque, transparence (art. 50)", "Cybersécurité de base (guide ANSSI des TPE-PME)", "Charte d'usage de l'IA pour son équipe"],
         "Atelier « Ma charte IA en 2 heures » ; chasse aux hallucinations",
         "Charte IA rédigée pour le projet fil rouge"),
        ("T2", "Anglais professionnel de base", 14, "Transversal",
         "Répondre à des demandes simples d'un interlocuteur anglophone.",
         ["Accueil, téléphone, e-mail simple", "Vocabulaire commercial et de gestion"],
         "Jeux de rôle avec un client touriste",
         "Mise en situation orale"),
        ("T3", "Dossier de projet, dossier professionnel et diaporama", 21, "Transversal",
         "Finaliser le dossier de projet, le dossier professionnel et le diaporama de l'épreuve.",
         ["Dossier de projet couvrant les 3 CCP", "Dossier professionnel (DP)", "Diaporama de présentation (45 min)"],
         "Relecture croisée entre stagiaires",
         "Grille de conformité du dossier"),
        ("T4", "Préparation de la période en entreprise et insertion", 14, "Transversal",
         "Préparer la période en entreprise et son projet professionnel ou entrepreneurial.",
         ["Recherche de la structure d'accueil, convention", "Objectifs de la période liés au projet fil rouge", "Sensibilisation à la création et reprise d'entreprise (accompagnement local)"],
         "Speed-meeting avec des dirigeants locaux",
         "Convention signée + objectifs écrits"),
        ("T5", "Entraînement à l'épreuve du titre", 14, "Transversal",
         "Présenter son projet et répondre au jury avec aisance.",
         ["Présentations blanches chronométrées (45 min)", "Entretiens techniques et finaux blancs"],
         "Jury blanc composé de dirigeants invités",
         "Résultats de l'épreuve blanche"),
        ("T6", "Suivi individuel et prévention du décrochage", 7, "Transversal",
         "Repérer et lever tôt les freins à la poursuite du parcours.",
         ["Entretiens individuels (J+15, mi-parcours, avant session)", "Freins périphériques et orientation vers les partenaires"],
         "Tableau de progression visuel",
         "Fiche de suivi individuel"),
    ],
    "ordre": ["M0", "M1.1", "M1.2", "M1.3", "T4", "M2.1", "M2.2", "T2",
              "|PAE:105", "M2.3", "T1", "M3.1", "M3.2", "M3.3", "|PAE:105", "T3", "T5", "T6"],
}

HEURES_SEMAINE = 35


def heures_centre(titre):
    return sum(m[2] for m in titre["modules"])


def planning(titre):
    """Découpe le parcours en semaines de 35 h ; renvoie [(n°, type, [(code, h)])]."""
    mods = {m[0]: m for m in titre["modules"]}
    semaines, courant, reste = [], [], HEURES_SEMAINE
    for etape in titre["ordre"]:
        if etape.startswith("|PAE:"):
            if courant:
                semaines.append(("Centre", courant))
                courant, reste = [], HEURES_SEMAINE
            h = int(etape.split(":")[1])
            while h > 0:
                semaines.append(("Entreprise", [("PAE", min(h, HEURES_SEMAINE))]))
                h -= HEURES_SEMAINE
            continue
        h = mods[etape][2]
        while h > 0:
            prise = min(h, reste)
            courant.append((etape, prise))
            h -= prise
            reste -= prise
            if reste == 0:
                semaines.append(("Centre", courant))
                courant, reste = [], HEURES_SEMAINE
    if courant:
        semaines.append(("Centre", courant))
    return [(i + 1, t, c) for i, (t, c) in enumerate(semaines)]


if __name__ == "__main__":
    for t in (MEM, RPMS):
        pl = planning(t)
        pae = sum(h for _, ty, c in pl if ty == "Entreprise" for _, h in c)
        print(t["code"], "centre", heures_centre(t), "PAE", pae, "semaines", len(pl))
        assert pae == t["pae"], (pae, t["pae"])
