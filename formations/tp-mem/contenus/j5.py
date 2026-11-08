from aides import cartes, encadre, flux, matrice, tableau

J = {
    "num": 5,
    "date": "Lundi 7 décembre 2026",
    "date_court": "2026-12-07",
    "titre": "S’organiser et résoudre les problèmes du magasin : méthodes du manager et carnet de bord",
    "objectif_general": "Organiser son temps et celui de l’équipe, et résoudre méthodiquement un problème de terrain (rupture, démarque, "
                        "réclamation), tout en préparant la collecte de preuves pour les dossiers AT1 et AT3.",
    "objectifs": [
        ("Comprendre (Bloom 2)", "expliquer la différence entre urgent et important, et les principaux « voleurs de temps »"),
        ("Appliquer (Bloom 3)", "prioriser une liste de tâches réelles avec la matrice d’Eisenhower et bâtir un rétroplanning"),
        ("Analyser (Bloom 4)", "rechercher les causes d’un problème avec le QQOQCP, les 5 pourquoi et le diagramme d’Ishikawa"),
        ("Évaluer (Bloom 5)", "choisir une solution avec une matrice de décision et planifier son suivi (PDCA)"),
        ("Créer (Bloom 6)", "concevoir son carnet de bord de période en entreprise et la fiche d’identité de son établissement"),
    ],
    "lien_reac": "Compétences transversales « Organiser ses actions » et « Mettre en œuvre une démarche de résolution de problème ». "
                 "AT1 : Planifier et coordonner l’activité (déléguer, prioriser, imprévus). AT3 : Proposer des actions correctives et assurer "
                 "le suivi du plan d’actions (étapes, échéances, responsables, indicateurs, preuves). RC/RE : documents et preuves des dossiers.",
    "prerequis": "J3 (indicateurs) et J4 (consignes, faits / opinions).",
    "materiel": "Vidéoprojecteur ; paperboard ; post-it de 4 couleurs ; 12 cartes « tâches du lundi matin » ; enveloppes de l’escape game "
                "(4 énigmes) ; minuteur ; modèle de carnet de bord imprimé (annexe de la ressource).",
    "progression": "Enactif : « Lundi matin chaotique » (on trie de vraies tâches sous pression) et escape game → Iconique : matrice "
                   "d’Eisenhower, arête de poisson, roue PDCA → Symbolique : vocabulaire des méthodes, plan d’actions → retour enactif : "
                   "cas complet « ruptures au rayon boissons » et carnet de bord personnel. Spirale : chiffres (J3) + communication (J4).",
    "slides": [
        {"type": "couverture", "titre": "S’organiser, résoudre", "sous_titre": "Méthodes du manager · Carnet de bord", "date": "Lundi 7 décembre 2026",
         "notes": "Retour sur le briefing observé en entreprise : quels temps étaient présents ? Qu’est-ce qui manquait ?"},
        {"type": "activite", "titre": "Jeu : lundi matin chaotique", "genre": "Individuel puis binôme", "duree": "20 min",
         "items": ["12 tâches, 8 h 30", "J’ordonne, je délègue", "Je justifie"], "notes":
         "Chaque apprenant reçoit 12 cartes : livraison qui arrive à 8 h 45 ; un collaborateur absent ; mail du directeur à rendre pour "
         "midi (chiffres de la semaine) ; client mécontent à l’accueil ; flaque d’eau devant le rayon boissons ; promo de demain à "
         "étiqueter ; planning de la semaine prochaine ; appel d’un fournisseur ; formation e-learning obligatoire ; café avec un "
         "collègue ; entretien d’un nouveau à 11 h ; ruptures sur 6 produits. Consigne : les classer dans l’ordre de traitement et dire "
         "ce qu’on délègue. Comparaison en binôme. Réponse attendue en tête : la flaque (sécurité, immédiat), puis le client, la "
         "livraison… Le débriefing amène la matrice d’Eisenhower."},
        {"type": "cartes", "titre": "Le programme du jour", "items": [
            ("1 · Mon temps", "priorités"), ("2 · Les causes", "méthodes"), ("3 · Les solutions", "plan d’actions"), ("4 · Mes preuves", "carnet de bord")], "notes": ""},
        {"type": "section", "num": "01", "titre": "Organiser son temps", "sous_titre": "Urgent n’est pas important", "notes": ""},
        {"type": "cartes", "titre": "La matrice d’Eisenhower", "items": [
            ("Urgent + important", "je fais"), ("Important", "je planifie"), ("Urgent", "je délègue"), ("Ni l’un ni l’autre", "j’élimine")],
         "notes": "Important = lié à mes objectifs, à la sécurité, au client. Urgent = qui ne peut pas attendre. Le piège du manager de "
                  "proximité : passer toute sa journée dans l’urgent (les « pompiers ») et ne jamais traiter l’important non urgent "
                  "(planning, formation de l’équipe, analyse des chiffres), qui évite pourtant les urgences de demain."},
        {"type": "chiffre", "titre": "La loi de Pareto", "valeur": "20 / 80", "legende": "20 % des causes font souvent 80 % des effets",
         "notes": "Ordre de grandeur, pas une loi exacte. Exemples : une poignée de produits fait l’essentiel du CA d’un rayon ; quelques "
                  "références font l’essentiel de la démarque. Le manager concentre son énergie sur ces 20 %."},
        {"type": "cartes", "titre": "Les voleurs de temps", "items": [
            ("Interruptions", "regrouper"), ("Tout faire", "déléguer"), ("Pas de plan", "to-do du jour"), ("Réunions", "courtes, utiles")],
         "notes": "Solutions : plages de travail protégées (ex. 14 h – 14 h 30 : chiffres, porte fermée ou réserve), to-do list priorisée "
                  "la veille au soir, délégation avec consigne QQOQCP (J4), réunions debout avec un objectif. Lien REAC : « anticiper "
                  "l’activité », « gérer les imprévus », « se joindre aux collaborateurs le cas échéant » sans s’y enfermer."},
        {"type": "etapes", "titre": "Le rétroplanning", "items": [("Date finale", "je pars de la fin"), ("Étapes", "je remonte"), ("Jalons", "je contrôle")],
         "notes": "Exemple : implantation de Noël prête le 1er décembre. On remonte : commande des produits (−4 semaines, fret maritime "
                  "depuis la métropole ou l’Asie), réception (−10 jours), préparation du mobilier (−5 jours), implantation la nuit du "
                  "30 novembre. À La Réunion, les délais d’approvisionnement par bateau imposent d’anticiper plus qu’en métropole."},
        {"type": "section", "num": "02", "titre": "Trouver les vraies causes", "sous_titre": "Ne pas soigner le symptôme", "notes": "Pause de 10 minutes vers 10 h."},
        {"type": "etapes", "titre": "La résolution de problème", "items": [("Poser", "le problème"), ("Chercher", "les causes"), ("Choisir", "la solution"), ("Suivre", "les résultats")],
         "notes": "Le réflexe naturel est de sauter directement à la solution. Résultat : on traite le symptôme et le problème revient. "
                  "Exemple : « ruptures sur l’eau » → on commande plus… mais la vraie cause était un réassort en réserve non fait le "
                  "dimanche faute de personnel."},
        {"type": "cartes", "titre": "Poser le problème : QQOQCP", "items": [
            ("Quoi ?", "le constat"), ("Qui ?", "concerné"), ("Où ?", "rayon, zone"), ("Quand ?", "depuis quand"), ("Comment ?", "combien"), ("Pourquoi ?", "enjeu")],
         "notes": "Le même outil que pour la consigne (J4), utilisé cette fois pour décrire un problème de façon factuelle. Exemple : "
                  "« Depuis 3 semaines (quand), le rayon boissons (où) présente en moyenne 7 ruptures par jour (combien), surtout le "
                  "lundi matin (quand), ce qui génère des réclamations et une perte estimée de 400 € de CA par semaine (pourquoi c’est important). »"},
        {"type": "etapes", "titre": "Les 5 pourquoi", "items": [("Pourquoi ?", "rupture"), ("Pourquoi ?", "pas de réassort"), ("Pourquoi ?", "personne dimanche"), ("Cause", "planning")],
         "notes": "On demande « pourquoi ? » jusqu’à trouver une cause sur laquelle on peut agir (souvent 3 à 5 fois). Ruptures le lundi → "
                  "parce que les rayons ne sont pas réassortis le dimanche après-midi → parce qu’il n’y a personne en réserve le dimanche "
                  "→ parce que le planning du dimanche ne prévoit que des hôtesses de caisse → parce que le planning a été copié de "
                  "l’ancien horaire d’ouverture. Cause racine : planning du dimanche inadapté. Action : prévoir une heure de réassort."},
        {"type": "cartes", "titre": "Ishikawa : les 5 M", "items": [
            ("Main-d’œuvre", "les personnes"), ("Méthodes", "les procédures"), ("Matériel", "les outils"), ("Matières", "les produits"), ("Milieu", "l’environnement")],
         "notes": "Le diagramme en arête de poisson : le problème est la tête, chaque arête est une famille de causes. On fait un "
                  "remue-méninges (brainstorming) avec l’équipe, une idée par post-it, rangée dans un M. Associer l’équipe, c’est aussi "
                  "l’engager dans la solution (REAC : écouter les propositions d’amélioration des collaborateurs)."},
        {"type": "activite", "titre": "Escape game du magasin", "genre": "4 équipes · 4 énigmes", "duree": "45 min",
         "items": ["Énigme = un problème", "Méthode imposée", "Code = la cause"], "notes":
         "4 enveloppes, chacune avec un mini-dossier (chiffres, témoignages, photos décrites) et une méthode imposée. 1) Hausse de la "
         "démarque sur les yaourts → Ishikawa (cause : chambre froide mal fermée, matériel). 2) Réclamations en caisse le samedi → 5 "
         "pourquoi (cause : ouverture d’une seule caisse rapide, planning). 3) Baisse du panier moyen au rayon jouets → QQOQCP + "
         "chiffres du J3 (cause : rupture des piles, produits complémentaires absents). 4) Accident évité de justesse en réserve → "
         "5M (cause : cartons stockés en hauteur, méthode). Chaque bonne cause donne une lettre du code final « PDCA ». "
         "Accessibilité : dossiers en gros caractères, lecture possible à voix haute dans l’équipe."},
        {"type": "section", "num": "03", "titre": "Choisir et suivre", "sous_titre": "Le plan d’actions", "notes": "Après le déjeuner."},
        {"type": "cartes", "titre": "Choisir une solution", "items": [("Efficacité", "règle la cause ?"), ("Coût", "budget"), ("Délai", "rapidité"), ("Faisabilité", "mes moyens")],
         "notes": "Matrice de décision : chaque solution est notée de 1 à 5 sur chaque critère ; on additionne. Le MEM choisit dans les "
                  "limites de son périmètre et propose à sa hiérarchie ce qui le dépasse (budget, recrutement). Lien AT3 : « prise en "
                  "compte des moyens humains, matériels et financiers disponibles »."},
        {"type": "etapes", "titre": "La roue PDCA", "items": [("Plan", "je prévois"), ("Do", "je fais"), ("Check", "je mesure"), ("Act", "j’ajuste")],
         "notes": "Roue de Deming : on prévoit (objectif, actions, indicateur), on fait, on vérifie avec l’indicateur, on ajuste et on "
                  "recommence. C’est exactement la troisième partie du dossier AT3 : plan d’actions, mise en œuvre, évaluation des "
                  "résultats, ajustements."},
        {"type": "cartes", "titre": "Un plan d’actions complet", "items": [
            ("Action", "quoi"), ("Responsable", "qui"), ("Échéance", "quand"), ("Moyens", "avec quoi"), ("Indicateur", "comment je mesure"), ("Preuve", "ce que je garde")],
         "notes": "Le RC/RE demande un plan d’actions « détaillé, avec les étapes, les échéances, les responsables, les moyens mobilisés et "
                  "les indicateurs de suivi », documenté par des preuves (plannings, comptes rendus, reporting, photos terrain, extraits de "
                  "mails). Le tableau modèle est dans la ressource."},
        {"type": "activite", "titre": "Cas : ruptures boissons", "genre": "Équipes · paperboard", "duree": "45 min",
         "items": ["QQOQCP + 5 pourquoi", "Matrice de décision", "Plan d’actions PDCA"], "notes":
         "Cas complet (données dans la ressource) : supermarché de Saint-Benoît, 7 ruptures par jour au rayon boissons, pic le lundi. "
         "Les équipes enchaînent : poser le problème, trouver la cause racine, comparer 3 solutions, construire le plan d’actions avec "
         "indicateur (nombre de ruptures relevées à 10 h) et preuve (relevé photo daté). Restitution : 3 minutes par équipe, comme "
         "devant un responsable."},
        {"type": "section", "num": "04", "titre": "Mes preuves", "sous_titre": "Le carnet de bord", "notes": "Pause de 10 minutes vers 14 h 30."},
        {"type": "puces", "titre": "Le carnet de bord", "items": ["1 page par semaine", "Observé, fait, appris", "Chiffres du périmètre", "Preuves anonymisées"],
         "notes": "Les dossiers AT1 et AT3 se construisent à partir de vos observations et actions réelles (280 h). Sans traces écrites "
                  "au fil de l’eau, impossible de retrouver en avril ce que vous avez fait en décembre. Modèle de page dans la ressource."},
        {"type": "cartes", "titre": "Fiche d’identité", "items": [("Enseigne", "format, statut"), ("Lieu", "zone, concurrence"), ("Équipe", "effectif, organigramme"), ("Chiffres", "CA, surface")],
         "notes": "Page obligatoire en introduction de chaque document (RC/RE). Elle se prépare maintenant, avec l’accord du tuteur pour "
                  "les chiffres internes. Reprendre les 5 diapositives du J2."},
        {"type": "activite", "titre": "Atelier : mon carnet", "genre": "Individuel", "duree": "30 min",
         "items": ["Fiche d’identité", "Page de la semaine", "3 preuves à collecter"], "notes":
         "Chacun remplit la fiche d’identité de son établissement (ou la liste de ce qu’il doit demander à son tuteur) et la première "
         "page du carnet. RGPD : pas de nom de collègue ni de client ; photos sans personnes identifiables ; documents internes avec "
         "l’accord du tuteur."},
        {"type": "activite", "titre": "Quiz : 10 questions", "genre": "Individuel", "duree": "15 min", "items": ["10 questions", "Correction ensemble", "Objectif : 7 / 10"], "notes": ""},
        {"type": "puces", "titre": "À retenir", "items": ["Important avant urgent", "5 pourquoi : la vraie cause", "Plan : qui, quoi, quand", "Je garde des preuves"],
         "notes": "Annonce du 14/12 : les règles du manager (droit du travail, sécurité, RSE, RGPD, IA) et préparation de l’AT1 en janvier."},
        {"type": "question", "titre": "Mon engagement", "texte": "Cette semaine, je remplis\nma première page de carnet", "notes": ""},
    ],
    "ressource": [
        ("Pourquoi s’organiser et résoudre sont des compétences",
         "<p>Deux des quatre compétences transversales du REAC sont au cœur de cette journée : <b>Organiser ses actions</b> (anticiper, "
         "planifier, répartir la charge, gérer les imprévus, prévenir les risques) et <b>Mettre en œuvre une démarche de résolution de "
         "problème</b>. Elles nourrissent l’AT1 (planifier et coordonner) et l’AT3 (actions correctives et suivi).</p>"),
        ("Organiser son temps",
         matrice("Urgence →", "Importance →", [
             ("Important, pas urgent → je PLANIFIE", "Planning, formation de l’équipe, analyse des chiffres, entretiens"),
             ("Urgent ET important → je FAIS", "Sécurité (flaque, chute), client mécontent, livraison qui arrive"),
             ("Ni urgent ni important → j’ÉLIMINE", "Certaines sollicitations, tâches sans valeur"),
             ("Urgent, pas important → je DÉLÈGUE", "Étiquetage de la promo, appel fournisseur courant")], "La matrice d’Eisenhower")
         + tableau(["Voleur de temps", "Parade"], [["Interruptions permanentes", "Plages protégées, regrouper les questions au briefing"],
                                                 ["Vouloir tout faire soi-même", "Déléguer avec QQOQCP et contrôle"], ["Pas de plan de journée", "To-do priorisée la veille au soir"],
                                                 ["Réunions longues", "Debout, ordre du jour, décision écrite"], ["Perfectionnisme", "« Bien fait » plutôt que « parfait » quand l’enjeu est faible"]])
         + encadre("ex", "<p><b>Rétroplanning de l’implantation de Noël</b> (prête le 1er décembre) : commande au fournisseur 4 à 6 semaines "
                   "avant (fret maritime), réception 10 jours avant, préparation du mobilier 5 jours avant, implantation la nuit du 30 "
                   "novembre, briefing de l’équipe le 1er au matin.</p>")
         + encadre("retenir", "<p>Le temps passé sur l’<b>important non urgent</b> est ce qui fait disparaître les urgences de demain.</p>")),
        ("Résoudre un problème en 4 étapes",
         flux([("Poser", "QQOQCP, faits chiffrés"), ("Chercher", "5 pourquoi, Ishikawa, avec l’équipe"), ("Choisir", "matrice de décision"),
               ("Suivre", "plan d’actions et PDCA")], "La démarche de résolution de problème")
         + "<h3>Les 5 pourquoi (exemple)</h3>"
         + tableau(["Question", "Réponse"], [["Pourquoi des ruptures le lundi ?", "Les rayons ne sont pas réassortis le dimanche après-midi"],
                                           ["Pourquoi ?", "Personne n’est en réserve le dimanche"], ["Pourquoi ?", "Le planning du dimanche ne prévoit que des hôtesses de caisse"],
                                           ["Pourquoi ?", "Il a été copié de l’ancien horaire, quand le magasin fermait à 12 h"],
                                           ["Cause racine", "<b>Planning du dimanche inadapté</b> → action : 1 h de réassort à 15 h"]])
         + "<h3>Le diagramme d’Ishikawa (5 M)</h3>"
         + cartes([("Main-d’œuvre", "formation, effectif, motivation"), ("Méthodes", "procédures, organisation"), ("Matériel", "meubles, froid, caisses, outils"),
                   ("Matières", "produits, emballages, livraisons"), ("Milieu", "météo, travaux, concurrence, chaleur")], "Les 5 familles de causes, autour du problème", cols=3)
         + encadre("astuce", "<p>Faites le remue-méninges avec l’équipe : une idée par post-it, sans critique, puis on range dans les 5 M. "
                   "Ceux qui ont trouvé la cause appliquent plus volontiers la solution.</p>")),
        ("Choisir une solution et la suivre",
         tableau(["Solution", "Efficacité", "Coût", "Délai", "Faisabilité", "Total / 20"], [
             ["Commander 30 % d’eau en plus", "2", "2", "5", "4", "13"], ["1 h de réassort le dimanche à 15 h", "5", "4", "4", "4", "<b>17</b>"],
             ["Nouvelle étagère en réserve", "3", "1", "2", "2", "8"]], )
         + flux([("Plan", "objectif, actions, indicateur"), ("Do", "mise en œuvre avec l’équipe"), ("Check", "mesure avec l’indicateur"),
                 ("Act", "ajustement, on généralise ou on corrige")], "La roue PDCA (Deming)")
         + "<h3>Modèle de plan d’actions</h3>"
         + tableau(["Action", "Responsable", "Échéance", "Moyens", "Indicateur", "Preuve"], [
             ["Ajouter 1 h de réassort le dimanche 15 h – 16 h", "Manager (planning) + 1 employé libre-service", "Dès le 13/12", "1 h de travail / semaine",
              "Ruptures relevées le lundi à 10 h (objectif : ≤ 2)", "Relevé photo daté, planning anonymisé"],
             ["Check-list de réassort affichée en réserve", "Employé référent", "11/12", "Impression, plastification", "Check-list remplie chaque dimanche", "Photo de la check-list"]])
         + encadre("jury", "<p>Au dossier AT3 (partie 3), le jury attend : un plan d’actions détaillé, des preuves de mise en œuvre, un "
                   "suivi des résultats (tableau, graphique), l’analyse des écarts persistants et des ajustements réalistes.</p>")),
        ("Cas « ruptures au rayon boissons » (données de l’atelier)",
         "<p>Supermarché fictif de Saint-Benoît, rayon boissons, 3 semaines d’observation.</p>"
         + tableau(["Jour", "Ruptures relevées à 10 h (moyenne)", "Réclamations"], [["Lundi", "12", "5"], ["Mardi", "6", "2"], ["Mercredi", "5", "1"],
                                                                                   ["Jeudi", "5", "1"], ["Vendredi", "6", "2"], ["Samedi", "8", "3"], ["Dimanche", "7", "2"]])
         + "<p>Témoignages : « Le dimanche, on n’est que trois en caisse » (hôtesse) ; « Les palettes d’eau arrivent le mardi » (réceptionnaire) ; "
           "« Il fait 34 °C, les clients prennent des packs entiers » (vendeur). Perte estimée : 400 € de CA par semaine.</p>"
         + encadre("ex", "<p>Pistes attendues : cause racine liée à l’organisation du dimanche (méthode, main-d’œuvre) aggravée par la "
                   "chaleur (milieu) ; solution prioritaire : réassort le dimanche après-midi ; indicateur : ruptures du lundi à 10 h.</p>")),
        ("Le carnet de bord et la fiche d’identité",
         "<h3>Fiche d’identité de l’établissement (page 1 de chaque dossier)</h3>"
         + tableau(["Rubrique", "À renseigner"], [["Enseigne et format", "Nom, type (hyper, supermarché, spécialisé, franchise, indépendant)"],
                                                 ["Localisation", "Commune, zone (centre-ville, zone commerciale), concurrence proche"],
                                                 ["Organisation", "Effectif, organigramme simplifié (fonctions, pas de noms), horaires d’ouverture"],
                                                 ["Chiffres clés", "Surface de vente, CA annuel ou du périmètre (avec l’accord du tuteur)"],
                                                 ["Mon périmètre", "Rayon / secteur, mon rôle, mon tuteur (fonction)"]])
         + "<h3>Modèle de page hebdomadaire</h3>"
         + tableau(["Semaine du … au …", ""], [["Ce que j’ai observé", "Organisation, briefing, réassort, clients…"],
                                             ["Ce que j’ai fait moi-même", "Tâches, initiatives, actions (« je »)"],
                                             ["Les chiffres de mon périmètre", "CA, panier, ruptures, démarque…"],
                                             ["Les preuves collectées", "Photo datée, planning anonymisé, compte rendu…"],
                                             ["Lien avec le REAC", "AT1 / AT2 / AT3 — compétence n° …"],
                                             ["Ce que j’ai appris / ma question au tuteur", ""]])
         + encadre("loi", "<p><b>RGPD</b> : plannings, comptes rendus d’entretien, réclamations clients contiennent des données "
                   "personnelles. Dans vos preuves : anonymiser (« Collaborateur A »), flouter les visages et les plaques, ne garder que "
                   "le nécessaire (minimisation, art. 5), et obtenir l’accord du tuteur. <b>Secret des affaires</b> : les chiffres internes "
                   "ne sortent pas du cadre de l’examen. <b>IA Act</b> : si vous utilisez une IA pour reformuler vos notes, n’y collez "
                   "aucune donnée personnelle ni chiffre confidentiel.</p>")),
    ],
    "sources": [
        "REAC MEM v09 : compétences transversales « Organiser ses actions » et « Résolution de problème » ; RC/RE : dossier AT3, partie 3 (pièces jointes).",
        "Méthodes classiques de management de la qualité : roue PDCA (W. E. Deming), diagramme causes-effets (K. Ishikawa), matrice d’Eisenhower.",
        "Règlement (UE) 2016/679 (RGPD), article 5 (minimisation) — eur-lex.europa.eu.",
        "Cas Saint-Benoît : données fictives créées pour l’exercice.",
    ],
    "grille": {
        "situation": "Cas « ruptures au rayon boissons » en équipe, puis carnet de bord individuel.",
        "criteres": [
            {"critere": "Priorisation", "indicateurs": ["Classe correctement les tâches (sécurité d’abord)", "Identifie ce qui se délègue"],
             "niveaux": ["Ordre aléatoire", "Sécurité oubliée ou délégation absente", "Priorités justes, délégation pertinente", "Priorités justifiées avec la matrice, consignes de délégation"]},
            {"critere": "Énoncé du problème", "indicateurs": ["QQOQCP complet", "Faits chiffrés, sans jugement"],
             "niveaux": ["Problème flou", "Partiel", "Complet et factuel", "Complet, chiffré, enjeu explicité"]},
            {"critere": "Recherche des causes", "indicateurs": ["5 pourquoi jusqu’à une cause actionnable", "Classement en 5 M"],
             "niveaux": ["Saute à la solution", "Cause superficielle", "Cause racine trouvée", "Cause racine + causes secondaires hiérarchisées"]},
            {"critere": "Plan d’actions", "indicateurs": ["Action, responsable, échéance, moyens, indicateur, preuve", "Logique PDCA"],
             "niveaux": ["Absent", "Incomplet", "Complet", "Complet, réaliste, chiffré, suivi prévu"]},
            {"critere": "Carnet de bord et fiche d’identité", "indicateurs": ["Fiche d’identité renseignée", "Règles RGPD appliquées aux preuves"],
             "niveaux": ["Non commencé", "Ébauche", "Fiche + 1re page complètes", "Complet, preuves listées, anonymisation maîtrisée"]},
        ]},
    "quiz": [
        {"q": "Dans la matrice d’Eisenhower, une tâche importante mais non urgente :", "choix": ["se fait tout de suite", "se planifie", "se délègue", "s’élimine"], "rep": 1,
         "explication": "Elle se planifie : c’est elle qui évite les urgences de demain."},
        {"q": "Une flaque d’eau devant le rayon à l’ouverture est :", "choix": ["urgente et importante", "importante, pas urgente", "urgente, pas importante", "ni l’un ni l’autre"], "rep": 0,
         "explication": "Risque de chute : sécurité des clients et salariés, on agit immédiatement."},
        {"q": "La loi de Pareto dit qu’en général :", "choix": ["50 % des causes font 50 % des effets", "20 % des causes font 80 % des effets",
                                                                 "80 % des causes font 20 % des effets", "tout se vaut"], "rep": 1, "explication": "C’est un ordre de grandeur qui aide à prioriser."},
        {"q": "Un rétroplanning se construit :", "choix": ["à partir d’aujourd’hui", "en partant de la date finale", "au hasard", "après l’événement"], "rep": 1,
         "explication": "On part de l’échéance et on remonte les étapes."},
        {"q": "Les 5 pourquoi servent à :", "choix": ["trouver la cause racine", "choisir une solution", "faire un planning", "motiver l’équipe"], "rep": 0,
         "explication": "On demande « pourquoi » jusqu’à une cause sur laquelle on peut agir."},
        {"q": "Lequel n’est PAS un des 5 M d’Ishikawa ?", "choix": ["Méthodes", "Milieu", "Marketing", "Matériel"], "rep": 2,
         "explication": "Main-d’œuvre, Méthodes, Matériel, Matières, Milieu."},
        {"q": "Dans PDCA, le C (Check) correspond à :", "choix": ["commander", "mesurer les résultats", "communiquer", "corriger"], "rep": 1,
         "explication": "Plan, Do, Check (vérifier avec l’indicateur), Act (ajuster)."},
        {"q": "Un plan d’actions complet comporte notamment :", "choix": ["action, responsable, échéance, indicateur", "seulement l’action", "le nom des clients", "le budget de l’enseigne"], "rep": 0,
         "explication": "Plus les moyens et les preuves, comme le demande le RC/RE."},
        {"q": "Dans une preuve pour le dossier, un planning doit être :", "choix": ["recopié tel quel", "anonymisé", "envoyé à une IA", "affiché sur les réseaux"], "rep": 1,
         "explication": "RGPD : minimisation et anonymisation des données des collègues."},
        {"q": "La fiche d’identité de l’établissement se place :", "choix": ["en annexe", "en introduction de chaque document", "dans le diaporama seulement", "nulle part"], "rep": 1,
         "explication": "Le RC/RE l’impose sur une page en introduction de chaque document."},
    ],
    "deroule": [
        ("8 h 00 – 8 h 15", "Accueil : le briefing observé", "Analyser une pratique (Bloom 4)", "Retour sur les briefings observés, comparaison aux 4 temps",
         "Interrogative · symbolique", "Diapo 1", "Oral"),
        ("8 h 15 – 8 h 40", "Jeu « lundi matin chaotique »", "Prioriser sous pression (Bloom 3)", "12 cartes à ordonner, délégation, comparaison en binôme",
         "Ludique · enactif", "Diapos 2-3, cartes", "Grille critère 1"),
        ("8 h 40 – 10 h 00", "S1 · Organiser son temps", "Expliquer et appliquer Eisenhower, Pareto, rétroplanning (Bloom 2-3)",
         "Matrice (retour sur les cartes) ; Pareto ; voleurs de temps ; rétroplanning de Noël (exercice)", "Expositive participative · iconique",
         "Diapos 4-8, ressource §2", "Exercice de rétroplanning"),
        ("10 h 00 – 10 h 10", "Pause", "", "", "", "", ""),
        ("10 h 10 – 11 h 00", "S2 · Trouver les vraies causes", "Analyser un problème (Bloom 4)", "4 étapes ; QQOQCP ; 5 pourquoi ; Ishikawa avec post-it",
         "Démonstrative · iconique → symbolique", "Diapos 9-13", "Questions"),
        ("11 h 00 – 12 h 00", "S2 · Escape game du magasin", "Appliquer les méthodes (Bloom 3-4)", "4 équipes, 4 énigmes, code final PDCA ; débriefing",
         "Ludique · enactif", "Diapo 14, enveloppes", "Grille critères 2-3"),
        ("12 h 00 – 13 h 00", "Pause déjeuner", "", "", "", "", ""),
        ("13 h 00 – 13 h 30", "S3 · Choisir et suivre", "Évaluer des solutions (Bloom 5)", "Matrice de décision ; PDCA ; plan d’actions modèle",
         "Expositive · iconique", "Diapos 15-18, ressource §4", "Questions"),
        ("13 h 30 – 14 h 30", "S3 · Cas « ruptures boissons »", "Construire un plan d’actions (Bloom 5-6)", "Enchaînement complet sur paperboard ; restitutions de 3 min",
         "Active · enactif + symbolique", "Diapo 19, ressource §5", "Grille critère 4"),
        ("14 h 30 – 14 h 40", "Pause", "", "", "", "", ""),
        ("14 h 40 – 15 h 35", "S4 · Carnet de bord et fiche d’identité", "Créer ses outils de preuve (Bloom 6)",
         "Pourquoi un carnet ; fiche d’identité ; atelier individuel ; règles RGPD des preuves", "Active · enactif", "Diapos 20-23, modèle imprimé", "Grille critère 5"),
        ("15 h 35 – 15 h 55", "Quiz 10 questions", "Évaluer (Bloom 1-2)", "Quiz puis correction", "Évaluative", "Quiz", "Sommative 7/10"),
        ("15 h 55 – 16 h 00", "Bilan et engagement", "S’engager (Bloom 3)", "À retenir ; première page du carnet", "Réflexive", "Diapos 25-26", "Engagement"),
    ],
}
