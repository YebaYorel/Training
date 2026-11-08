from aides import cartes, encadre, flux, matrice, tableau

J = {
    "num": 4,
    "date": "Lundi 30 novembre 2026",
    "date_court": "2026-11-30",
    "titre": "Communiquer en manager : consignes, briefing, écoute et feedback",
    "objectif_general": "Communiquer avec clarté et justesse auprès de l’équipe et de la hiérarchie : transmettre une consigne qui a du sens, "
                        "animer un briefing, écouter activement, donner un feedback constructif et rester assertif.",
    "objectifs": [
        ("Comprendre (Bloom 2)", "expliquer le schéma de la communication et les causes de déformation d’un message"),
        ("Appliquer (Bloom 3)", "formuler une consigne complète (QQOQCP + le sens) et vérifier sa compréhension par la reformulation"),
        ("Appliquer (Bloom 3)", "animer un briefing de 5 minutes structuré en 4 temps"),
        ("Analyser (Bloom 4)", "distinguer faits, opinions et sentiments dans une situation de tension"),
        ("Créer (Bloom 6)", "construire et délivrer un feedback avec la méthode DESC, de façon assertive"),
    ],
    "lien_reac": "Compétence transversale « Communiquer » (consignes claires, distinguer faits et opinions, vérifier la compréhension, "
                 "confidentialité, écrits clairs et factuels pour la hiérarchie). AT1 : Animer l’équipe (transmission des consignes, "
                 "briefings et débriefings, motivation) ; Accompagner la performance individuelle (feedback, entretiens). RC/RE : dossier AT1 partie 1.",
    "prerequis": "J1 : les 4 piliers de la posture managériale.",
    "materiel": "Vidéoprojecteur ; feuilles blanches et crayons ; 2 figures géométriques imprimées (jeu du dessin dicté) ; cartes « situations » "
                "pour les jeux de rôle ; minuteur ; paperboard.",
    "progression": "Enactif : jeu du dessin dicté (on vit la perte d’information) → Iconique : schéma émetteur / récepteur / bruits, matrice "
                   "des comportements → Symbolique : QQOQCP, DESC, assertivité → retour enactif : briefings filmés ou observés et feedbacks "
                   "en jeu de rôle. Spirale : on réinvestit la posture du J1 et les chiffres du J3 dans un vrai briefing.",
    "slides": [
        {"type": "couverture", "titre": "Communiquer en manager", "sous_titre": "Consignes · Briefing · Écoute · Feedback",
         "date": "Lundi 30 novembre 2026", "notes": "Retour sur les 3 chiffres relevés en magasin (J3) : chacun les présente en 30 secondes "
                                                    "et dit ce qu’ils lui apprennent. C’est déjà un exercice de communication."},
        {"type": "question", "titre": "Pour commencer", "texte": "« Range la réserve. »\nC’est clair ?", "notes":
         "Demander à 4 personnes ce qu’elles feraient exactement. Les réponses divergent : par quoi commencer, jusqu’à quand, avec quel "
         "matériel, pourquoi ? Message : une consigne qui paraît claire pour celui qui la donne ne l’est pas forcément pour celui qui la reçoit."},
        {"type": "cartes", "titre": "Le programme du jour", "items": [
            ("1 · Le message", "qui se perd"), ("2 · La consigne", "et le briefing"), ("3 · L’écoute", "faits / opinions"), ("4 · Le feedback", "assertif")],
         "notes": "Journée très active : beaucoup de mises en situation. Rappeler la bienveillance : on a le droit de se tromper."},
        {"type": "section", "num": "01", "titre": "Le message qui se perd", "sous_titre": "Ce que je dis ≠ ce qui est compris", "notes": ""},
        {"type": "activite", "titre": "Jeu : le dessin dicté", "genre": "Tout le groupe · 2 manches", "duree": "25 min",
         "items": ["Manche 1 : dos tourné", "Manche 2 : questions OK", "On compare"], "notes":
         "Un volontaire décrit une figure (carrés, triangles, cercle) dos au groupe, sans geste, sans répondre aux questions. Les autres "
         "dessinent. Manche 2 : nouvelle figure, face au groupe, questions autorisées. On compare les dessins et le temps passé. Résultat "
         "habituel : la manche 2 est plus longue mais beaucoup plus juste. Leçon : la communication à sens unique est rapide mais "
         "inefficace ; le retour (feedback) et la reformulation font la qualité. Accessibilité : prévoir une version tactile (formes "
         "découpées) pour une personne malvoyante, ou un rôle de descripteur."},
        {"type": "etapes", "titre": "Le schéma de la communication", "items": [("Émetteur", "je code"), ("Message", "canal"), ("Récepteur", "il décode")],
         "notes": "Entre les deux : des « bruits » (bruit réel du magasin, fatigue, stress, vocabulaire technique, langue, préjugés). Le "
                  "retour du récepteur (questions, reformulation) permet de vérifier. Au magasin : briefing au milieu des transpalettes, "
                  "consigne donnée en passant, message transmis par un tiers… autant de bruits."},
        {"type": "cartes", "titre": "3 canaux à la fois", "items": [("Verbal", "les mots"), ("Paraverbal", "la voix, le débit"), ("Non verbal", "corps, regard")],
         "notes": "Le REAC le dit : « être conscient du langage non verbal, du débit et du registre de langage ». Attention à un mythe "
                  "répandu : les « 7 % de mots, 38 % de voix, 55 % de corps » (Mehrabian) ne valent que pour l’expression d’émotions dans "
                  "une expérience de laboratoire, pas pour toute communication. Ce qui est vrai : si les mots et le corps se contredisent, "
                  "c’est le corps qu’on croit."},
        {"type": "exemple", "titre": "Le créole au magasin", "lieu": "La Réunion", "lieu_detail": ["Équipe bilingue", "français · créole"],
         "items": ["Une richesse", "Un registre adapté", "Personne n’est exclu"], "notes":
         "À La Réunion, le créole est souvent la langue du quotidien de l’équipe et de nombreux clients. Le manager peut s’en servir pour "
         "créer du lien et se faire comprendre, mais veille à ce qu’aucun collaborateur (arrivé de métropole, de Mayotte, de Madagascar…) "
         "ne soit exclu des informations importantes. Les consignes de sécurité et les écrits restent en français, et on vérifie que "
         "tout le monde a compris. Le registre (familier, courant, soutenu) s’adapte à l’interlocuteur : un client, un collègue, la direction."},
        {"type": "section", "num": "02", "titre": "La consigne et le briefing", "sous_titre": "Clair, complet, qui a du sens", "notes": "Pause de 10 minutes vers 10 h."},
        {"type": "cartes", "titre": "Une consigne : QQOQCP", "items": [
            ("Quoi ?", "la tâche"), ("Qui ?", "la personne"), ("Où ?", "le lieu"), ("Quand ?", "le délai"), ("Comment ?", "la méthode"), ("Pourquoi ?", "le sens")],
         "notes": "Le « pourquoi » est ce qui distingue un manager d’un donneur d’ordres (REAC : « donner du sens aux actions demandées », "
                  "dossier AT1). Exemple : « Kévin, avant 10 h, refais le facing du rayon boissons fraîches avec les packs d’eau en bas "
                  "(sécurité), parce que la chaleur annoncée va doubler les ventes cet après-midi et qu’on veut zéro rupture. »"},
        {"type": "etapes", "titre": "Vérifier la compréhension", "items": [("Je dis", "consigne"), ("Il reformule", "avec ses mots"), ("J’ajuste", "si besoin")],
         "notes": "Ne pas demander « C’est compris ? » (on répond toujours oui). Demander : « Tu peux me dire comment tu vas t’y prendre ? » "
                  "C’est la reformulation par le collaborateur. Elle évite la majorité des erreurs."},
        {"type": "etapes", "titre": "Le briefing en 4 temps", "items": [("Hier", "résultats"), ("Ce jour", "objectif"), ("Comment", "qui fait quoi"), ("Énergie", "on y va")],
         "notes": "Briefing debout, 5 à 10 minutes, même heure chaque jour. 1) Hier : un chiffre, une réussite à féliciter (nommer la "
                  "personne). 2) Aujourd’hui : un objectif chiffré et un seul message prioritaire. 3) Organisation : qui fait quoi, "
                  "les pauses, les points de vigilance (sécurité, livraison). 4) Énergie : une phrase positive, une question « des "
                  "questions ? ». Le débriefing du soir fait le bilan."},
        {"type": "activite", "titre": "Atelier : mon briefing de 5 min", "genre": "Préparation puis passage", "duree": "60 min",
         "items": ["Fiche situation tirée", "15 min de préparation", "5 min devant le groupe"], "notes":
         "Situations (cartes) : 1) Lancement de l’opération rentrée scolaire, papeterie d’un hyper de Sainte-Clotilde. 2) Alerte "
         "cyclonique orange annoncée : le magasin va être pris d’assaut (eau, bougies, piles). 3) Lundi après un week-end raté (−8 % de CA, "
         "réutiliser un chiffre du J3). 4) Arrivée de deux nouveaux saisonniers pour les fêtes. Chacun prépare avec la trame en 4 temps, "
         "le groupe joue l’équipe. Observateurs : grille critères 2 et 3. Passages de 5 minutes + 3 minutes de retours."},
        {"type": "section", "num": "03", "titre": "Écouter vraiment", "sous_titre": "Faits, opinions, sentiments", "notes": "Après le déjeuner."},
        {"type": "cartes", "titre": "L’écoute active", "items": [("Se taire", "laisser finir"), ("Questionner", "questions ouvertes"), ("Reformuler", "« si je comprends bien… »")],
         "notes": "Questions ouvertes (« Comment ça s’est passé ? ») pour faire parler ; questions fermées (« Tu as prévenu la caisse ? ») "
                  "pour vérifier un fait. La reformulation montre qu’on a compris ET permet à l’autre de corriger. Le silence est un "
                  "outil : compter mentalement jusqu’à 3 avant de répondre."},
        {"type": "cartes", "titre": "Fait, opinion, sentiment", "items": [
            ("Fait", "« 3 retards ce mois »"), ("Opinion", "« Tu t’en fiches »"), ("Sentiment", "« Je suis inquiet »")],
         "notes": "Un fait est vérifiable, daté, chiffré. Une opinion est un jugement, contestable. Un sentiment est personnel et ne se "
                  "discute pas. Le manager s’appuie sur les faits (REAC : « distinguer faits et opinions ») et peut exprimer ses "
                  "sentiments, jamais juger la personne."},
        {"type": "activite", "titre": "Jeu : fait ou opinion ?", "genre": "Cartons F / O / S", "duree": "15 min",
         "items": ["J’entends une phrase", "Je lève F, O ou S", "On reformule en fait"], "notes":
         "Phrases : « Le rayon est toujours en désordre » (O → « 4 ruptures relevées à 11 h ») ; « Tu es arrivé à 9 h 20 au lieu de 9 h » "
         "(F) ; « Les jeunes ne veulent plus travailler » (O, et préjugé) ; « Je suis déçu du résultat » (S) ; « Le CA du samedi est de "
         "8 950 € » (F) ; « Les clients sont mécontents » (O → « 3 réclamations écrites cette semaine »)."},
        {"type": "section", "num": "04", "titre": "Le feedback", "sous_titre": "Dire les choses, sans casser", "notes": "Pause de 10 minutes vers 14 h 30."},
        {"type": "cartes", "titre": "4 attitudes face à l’autre", "items": [
            ("Passif", "je subis"), ("Agressif", "j’attaque"), ("Manipulateur", "je contourne"), ("Assertif", "je dis, je respecte")],
         "notes": "L’assertivité : exprimer clairement ce que l’on pense et ce que l’on attend, en respectant l’autre. Ni paillasson, ni "
                  "hérisson, ni renard. Exemple face à un refus de faire une tâche : passif (« bon, je le fais moi-même »), agressif "
                  "(« tu fais ce que je dis »), manipulateur (« ça serait dommage pour ton entretien annuel… »), assertif (« J’entends que "
                  "ça te pèse ; cette tâche doit être faite avant 14 h ; comment t’organises-tu ? »)."},
        {"type": "cartes", "titre": "La méthode DESC", "items": [
            ("D · Décrire", "les faits"), ("E · Exprimer", "mon ressenti"), ("S · Spécifier", "ce que j’attends"), ("C · Conséquences", "positives")],
         "notes": "Exemple : « Cette semaine, tu es arrivé 3 fois après 9 h 15 (D). Je suis embêté, car l’ouverture du rayon frais se fait "
                  "à deux et ta collègue se retrouve seule (E). J’ai besoin que tu sois là à 9 h, et si tu as une difficulté, préviens-moi "
                  "avant (S). Comme ça, on ouvre à l’heure et l’équipe est soulagée (C). » DESC sert aussi pour féliciter : décrire "
                  "précisément ce qui a été bien fait motive plus qu’un « bravo » général."},
        {"type": "comparer", "titre": "Feedback : à faire / à éviter", "gauche": ("À faire", ["En privé", "Vite après le fait", "Sur un fait"]),
         "droite": ("À éviter", ["Devant l’équipe", "Des mois après", "Sur la personne"]), "notes":
         "Règle d’or : on félicite en public, on recadre en privé. Confidentialité (REAC). Le feedback positif doit être bien plus "
         "fréquent que le négatif. Ne jamais commenter la santé, la vie privée ou l’origine d’une personne (discrimination, Code du "
         "travail art. L1132-1)."},
        {"type": "activite", "titre": "Jeu de rôle : le feedback DESC", "genre": "Trios · rotation", "duree": "40 min",
         "items": ["1 manager, 1 collaborateur", "1 observateur", "3 situations"], "notes":
         "Situations : 1) Une collaboratrice très efficace qui a sauvé l’inventaire (feedback positif). 2) Un collaborateur qui ne "
         "respecte pas le port des chaussures de sécurité en réserve. 3) Une collaboratrice qui parle mal à un client devant les autres. "
         "Le collaborateur réagit de façon réaliste (justification, émotion). L’observateur coche D, E, S, C et l’attitude (passif / "
         "agressif / manipulateur / assertif). Rotation des rôles."},
        {"type": "puces", "titre": "Écrire à sa hiérarchie", "items": ["Objet précis", "Les faits, les chiffres", "Ma proposition", "Court, poli"],
         "notes": "Compétence transversale : « rédiger des analyses, des bilans, des propositions à destination de la hiérarchie dans un "
                  "langage clair et factuel ». Exemple d’objet : « Rayon frais — démarque en hausse de 1,2 point en novembre : 2 "
                  "propositions ». Le mail tient en 10 lignes : constat chiffré, cause probable, proposition, demande de validation."},
        {"type": "activite", "titre": "Quiz : 10 questions", "genre": "Individuel", "duree": "15 min", "items": ["10 questions", "Correction ensemble", "Objectif : 7 / 10"],
         "notes": "Lecture à voix haute possible."},
        {"type": "puces", "titre": "À retenir", "items": ["Consigne : QQOQCP + pourquoi", "Il reformule, j’ajuste", "Briefing : 4 temps", "DESC, en privé"],
         "notes": "Annonce du 7/12 : s’organiser et résoudre les problèmes du magasin."},
        {"type": "question", "titre": "Mon engagement", "texte": "Cette semaine, j’observe\nun briefing en entreprise", "notes":
         "Noter la structure observée (sans juger les personnes, sans nom) et la comparer aux 4 temps. Matière pour le dossier AT1."},
    ],
    "ressource": [
        ("Pourquoi la communication est une compétence clé",
         "<p>Le REAC fait de « Communiquer » une compétence transversale : on la retrouve dans les trois activités-types. Le jury de l’AT1 "
         "vous interrogera sur vos consignes, vos briefings et la façon dont vous motivez et recadrez (dossier AT1, partie 1).</p>"
         + encadre("retenir", "<p>Ce qui compte n’est pas ce que je dis, mais ce que l’autre comprend… et ce qu’il en fait.</p>")),
        ("Le schéma de la communication",
         flux([("Émetteur", "a une idée, la code en mots, ton, gestes"), ("Message", "passe par un canal : oral, écrit, affichage"),
               ("Récepteur", "décode avec son vécu, son vocabulaire"), ("Retour", "questions, reformulation : on vérifie")], "Émetteur, message, récepteur… et retour")
         + "<p><b>Les bruits</b> qui déforment : bruit réel du magasin, stress du rush, vocabulaire technique (« facing », « DLC »), langue, "
           "fatigue, préjugés, message transmis par un tiers.</p>"
         + cartes([("Verbal", "Les mots choisis : précis, adaptés à la personne."), ("Paraverbal", "Le ton, le volume, le débit, les silences."),
                   ("Non verbal", "La posture, le regard, les gestes, la distance.")], cols=3)
         + encadre("piege", "<p>Le fameux « 7 % – 38 % – 55 % » (Mehrabian) est souvent mal utilisé : il ne concerne que l’expression "
                   "d’émotions dans une expérience précise. Retenez simplement : quand les mots et le corps se contredisent, on croit le corps.</p>")
         + encadre("ex", "<p><b>Le créole au magasin :</b> une richesse pour créer du lien et se faire comprendre. Le manager veille à ce "
                   "que personne ne soit exclu des informations importantes ; consignes de sécurité et écrits en français, avec "
                   "vérification de la compréhension.</p>")),
        ("La consigne qui a du sens",
         cartes([("Quoi ?", "La tâche précise"), ("Qui ?", "La personne nommée"), ("Où ?", "Le lieu exact"), ("Quand ?", "Le délai, l’heure"),
                 ("Comment ?", "La méthode, le matériel, la sécurité"), ("Pourquoi ?", "Le sens : lien avec l’objectif ou le client")], "QQOQCP", cols=3)
         + tableau(["Consigne floue", "Consigne de manager"], [
             ["« Range la réserve. »", "« Inès, d’ici 15 h, range l’allée B de la réserve : les cartons lourds en bas, les allées dégagées "
              "(sécurité incendie). Demain matin on reçoit 3 palettes et il faut pouvoir les stocker. Tu me dis comment tu t’y prends ? »"],
             ["« Fais attention aux prix. »", "« Avant l’ouverture, vérifie les 20 étiquettes de la promo letchis avec le listing : un prix "
              "faux en caisse, c’est un client mécontent et une perte de marge. »"]])
         + flux([("Je donne la consigne", "QQOQCP + pourquoi"), ("Il reformule", "« Comment vas-tu t’y prendre ? »"), ("J’ajuste", "je complète, je remercie"),
                 ("Je contrôle", "au moment prévu, et je félicite")], "La boucle de la consigne")
         + encadre("astuce", "<p>Ne demandez jamais « C’est compris ? » : la réponse est toujours oui. Demandez à la personne de reformuler.</p>")),
        ("Le briefing et le débriefing",
         flux([("Hier", "1 chiffre, 1 réussite à féliciter"), ("Aujourd’hui", "1 objectif chiffré, 1 message prioritaire"),
               ("Comment", "qui fait quoi, pauses, sécurité, livraisons"), ("Énergie", "phrase positive, « des questions ? »")], "Le briefing en 4 temps (5 à 10 min, debout)")
         + tableau(["", "Briefing", "Débriefing"], [["Quand", "Début de journée ou de service", "Fin de journée ou d’opération"],
                                                  ["Durée", "5 à 10 minutes", "10 à 15 minutes"],
                                                  ["But", "Lancer, donner le cap, organiser", "Faire le bilan, apprendre, remercier"],
                                                  ["Question clé", "« Que va-t-on réussir aujourd’hui ? »", "« Qu’a-t-on appris ? Que garde-t-on ? »"]])
         + encadre("ex", "<p><b>Alerte cyclonique orange à Saint-André :</b> « Hier, 41 000 € de CA, merci à l’équipe caisse pour la "
                   "fluidité (Hier). Aujourd’hui, la préfecture annonce l’alerte orange : on attend deux fois plus de monde sur l’eau, les "
                   "piles et les bougies, objectif zéro rupture (Aujourd’hui). Marc et Sandy, réassort eau toutes les heures ; Julie, "
                   "renfort caisse de 11 h à 14 h ; personne ne monte sur un escabeau seul (Comment). On sait faire, on l’a déjà fait "
                   "l’an dernier. Des questions ? (Énergie) »</p>")
         + encadre("jury", "<p>Au dossier AT1, décrivez fréquence, durée, contenu, supports de vos briefings et comment vous les adaptez "
                   "aux profils (nouveaux, expérimentés). Joignez une trame de briefing en annexe.</p>")),
        ("L’écoute active et les faits",
         cartes([("Se taire", "Laisser finir, ne pas préparer sa réponse pendant que l’autre parle."),
                 ("Questionner", "Questions ouvertes pour comprendre, fermées pour vérifier un fait."),
                 ("Reformuler", "« Si je comprends bien, tu… » : l’autre se sent entendu et peut corriger.")], cols=3)
         + tableau(["Type", "Définition", "Exemple", "Reformulation en fait"], [
             ["Fait", "Vérifiable, daté, chiffré", "« 3 retards ce mois-ci »", "—"],
             ["Opinion", "Jugement, contestable", "« Le rayon est toujours en désordre »", "« À 11 h, j’ai relevé 4 ruptures et 2 produits mal rangés »"],
             ["Sentiment", "Ressenti personnel", "« Je suis inquiet pour le week-end »", "On l’exprime, on ne le discute pas"]])),
        ("Assertivité et feedback DESC",
         matrice("Respect de l’autre →", "Expression de soi →", [
             ("Agressif", "Je m’exprime, mais j’écrase l’autre"), ("Assertif", "Je m’exprime ET je respecte l’autre"),
             ("Manipulateur", "Je contourne, j’obtiens sans le dire"), ("Passif", "Je me tais, je subis, je m’efface")], "Les 4 attitudes")
         + flux([("D · Décrire", "les faits, sans jugement"), ("E · Exprimer", "mon ressenti, l’impact"), ("S · Spécifier", "ce que j’attends, concrètement"),
                 ("C · Conséquences", "ce que ça va apporter")], "La méthode DESC")
         + encadre("ex", "<p>« Cette semaine, tu es arrivé 3 fois après 9 h 15 (D). Je suis embêté, car ta collègue ouvre seule le rayon "
                   "frais (E). J’ai besoin que tu sois là à 9 h, et si tu as une difficulté, préviens-moi avant (S). Ainsi, on ouvre à "
                   "l’heure et l’équipe est soulagée (C). »</p>")
         + tableau(["À faire", "À éviter"], [["Féliciter en public, recadrer en privé", "Recadrer devant l’équipe ou un client"],
                                            ["Juste après les faits", "Attendre l’entretien annuel"], ["Parler du comportement", "Juger la personne"],
                                            ["Beaucoup de feedbacks positifs précis", "Seulement des reproches"]])
         + encadre("loi", "<p><b>Droit du travail</b> : ne jamais faire de remarque sur l’origine, la santé, l’âge, la religion, la "
                   "situation de famille… (discrimination, Code du travail art. L1132-1). <b>RGPD</b> : ce qui se dit en entretien "
                   "individuel reste confidentiel ; les notes écrites sur un collaborateur sont des données personnelles qu’il peut "
                   "demander à consulter (droit d’accès, art. 15).</p>")),
        ("Écrire à sa hiérarchie",
         tableau(["Partie du mail", "Contenu", "Exemple"], [
             ["Objet", "Sujet + enjeu", "Rayon frais — démarque +1,2 point en novembre : 2 propositions"],
             ["Constat", "Faits chiffrés, période, référence", "La démarque atteint 3,4 % du CA contre 2,2 % en octobre"],
             ["Cause probable", "Interne / externe, vérifiée", "Produits à DLC courte reçus en trop grande quantité les lundis"],
             ["Proposition", "Action, coût, délai", "Réduire la commande du lundi de 15 % et créer un bac « anti-gaspi » à −30 %"],
             ["Demande", "Ce que j’attends", "Pouvez-vous valider ces deux actions pour lundi prochain ?"]])
         + encadre("astuce", "<p>Relisez-vous en vous mettant à la place du lecteur : peut-il décider en 1 minute ?</p>")),
    ],
    "sources": [
        "REAC MEM v09 : fiche des compétences transversales (« Communiquer ») et AT1 ; RC/RE : dossier AT1, partie 1 (pièces jointes).",
        "Mehrabian A., Silent Messages, 1971 : portée limitée de la règle 7-38-55 (communication des émotions).",
        "Code du travail, article L1132-1 (principe de non-discrimination) — legifrance.gouv.fr.",
        "Règlement (UE) 2016/679 (RGPD), article 15 (droit d’accès) — eur-lex.europa.eu.",
    ],
    "grille": {
        "situation": "Briefing de 5 minutes à partir d’une situation tirée au sort, puis feedback DESC en jeu de rôle.",
        "criteres": [
            {"critere": "Clarté de la consigne", "indicateurs": ["QQOQCP complet, dont le « pourquoi »", "Fait reformuler le collaborateur"],
             "niveaux": ["Consigne floue", "Incomplète, sans sens", "Complète et sensée", "Complète, sensée, compréhension vérifiée"]},
            {"critere": "Structure du briefing", "indicateurs": ["4 temps : hier, aujourd’hui, comment, énergie", "Durée respectée (5 min)"],
             "niveaux": ["Pas de structure", "2 temps présents", "4 temps, durée respectée", "4 temps, chiffres, félicitations nominatives, dynamique"]},
            {"critere": "Communication non verbale et paraverbale", "indicateurs": ["Regard, posture, voix audible", "Registre adapté à l’équipe"],
             "niveaux": ["Lecture, regard fuyant", "Hésitant", "Posture et voix adaptées", "Aisance, adapte son registre et son rythme"]},
            {"critere": "Écoute et faits", "indicateurs": ["Questions ouvertes, reformulation", "S’appuie sur des faits, pas sur des opinions"],
             "niveaux": ["Coupe la parole, juge", "Écoute partielle", "Écoute et faits", "Écoute active fine, reformulations précises"]},
            {"critere": "Feedback DESC assertif", "indicateurs": ["D, E, S, C présents", "Attitude assertive, en privé, sans jugement de la personne"],
             "niveaux": ["Agressif ou passif", "DESC incomplet", "DESC complet, assertif", "DESC complet, adapté aux réactions, engagement obtenu"]},
        ]},
    "quiz": [
        {"q": "Dans le schéma de la communication, ce qui déforme le message s’appelle :", "choix": ["le canal", "les bruits", "le code", "le retour"], "rep": 1,
         "explication": "Les bruits : bruit réel, stress, vocabulaire, préjugés, intermédiaires…"},
        {"q": "Que signifie le dernier P de QQOQCP ?", "choix": ["Planning", "Pourquoi", "Priorité", "Procédure"], "rep": 1,
         "explication": "Pourquoi : le sens de la consigne, attendu par le REAC (« donner du sens aux actions demandées »)."},
        {"q": "Pour vérifier qu’une consigne est comprise, le mieux est de :", "choix": ["demander « c’est compris ? »", "la répéter deux fois",
                                                                                     "demander au collaborateur de reformuler", "l’afficher"], "rep": 2,
         "explication": "La reformulation par le collaborateur révèle les malentendus ; « c’est compris ? » obtient toujours « oui »."},
        {"q": "Quel est l’ordre du briefing en 4 temps ?", "choix": ["Énergie, hier, comment, aujourd’hui", "Hier, aujourd’hui, comment, énergie",
                                                                    "Aujourd’hui, hier, énergie, comment", "Comment, énergie, hier, aujourd’hui"], "rep": 1,
         "explication": "Hier (résultats), aujourd’hui (objectif), comment (organisation), énergie (mobilisation)."},
        {"q": "« Le rayon est toujours en désordre » est :", "choix": ["un fait", "une opinion", "un sentiment", "une consigne"], "rep": 1,
         "explication": "C’est un jugement. Le fait serait : « À 11 h, 4 ruptures et 2 produits mal rangés »."},
        {"q": "Une question ouverte :", "choix": ["appelle oui ou non", "permet à l’autre de s’exprimer librement", "est interdite en entretien", "est toujours agressive"], "rep": 1,
         "explication": "Exemple : « Comment s’est passée ta matinée ? »"},
        {"q": "L’attitude qui consiste à s’exprimer clairement en respectant l’autre est :", "choix": ["passive", "agressive", "manipulatrice", "assertive"], "rep": 3,
         "explication": "L’assertivité : ni paillasson, ni hérisson, ni renard."},
        {"q": "Dans la méthode DESC, le S signifie :", "choix": ["Sanctionner", "Spécifier ce que j’attends", "Synthétiser", "Souligner l’erreur"], "rep": 1,
         "explication": "Décrire, Exprimer, Spécifier, Conséquences."},
        {"q": "La règle d’or du feedback est :", "choix": ["féliciter en privé, recadrer en public", "féliciter en public, recadrer en privé",
                                                           "tout faire par mail", "attendre l’entretien annuel"], "rep": 1,
         "explication": "Le recadrage en public humilie et casse la confiance ; la confidentialité est attendue par le REAC."},
        {"q": "Un mail à sa hiérarchie doit avant tout être :", "choix": ["long et détaillé", "clair, factuel et proposer une action", "émotionnel", "informel"], "rep": 1,
         "explication": "Compétence transversale « Communiquer » : écrits clairs et factuels, avec des propositions."},
    ],
    "deroule": [
        ("8 h 00 – 8 h 20", "Accueil : mes 3 chiffres", "Restituer (Bloom 2)", "Chaque apprenant présente ses 3 chiffres en 30 s ; question « Range la réserve »",
         "Interrogative · enactif", "Diapos 1-3", "Oral"),
        ("8 h 20 – 8 h 45", "S1 · Jeu du dessin dicté", "Vivre la perte d’information (Bloom 2)", "2 manches, comparaison des dessins et des temps",
         "Ludique · enactif", "Diapos 4-5, figures, feuilles", "Observation"),
        ("8 h 45 – 10 h 00", "S1 · Schéma, canaux, registre", "Expliquer la communication (Bloom 2)",
         "Émetteur / récepteur / bruits ; verbal, paraverbal, non verbal ; mythe Mehrabian ; le créole au magasin (échange)",
         "Expositive participative · iconique", "Diapos 6-8, ressource §2", "Questions"),
        ("10 h 00 – 10 h 10", "Pause", "", "", "", "", ""),
        ("10 h 10 – 10 h 50", "S2 · Consigne et briefing", "Formuler une consigne complète (Bloom 3)",
         "QQOQCP ; reformulation ; briefing en 4 temps ; exemple alerte cyclonique", "Démonstrative · symbolique", "Diapos 9-12, ressource §3-4", "Consignes réécrites"),
        ("10 h 50 – 12 h 00", "S2 · Atelier « mon briefing »", "Animer un briefing (Bloom 3)", "Tirage de situations, 15 min de préparation, passages de 5 min + retours",
         "Simulation · enactif", "Diapo 13, cartes situations", "Grille critères 1-3"),
        ("12 h 00 – 13 h 00", "Pause déjeuner", "", "", "", "", ""),
        ("13 h 00 – 13 h 20", "Suite des passages briefing", "Animer (Bloom 3)", "Derniers passages et synthèse des bonnes pratiques",
         "Simulation · enactif", "Cartes situations", "Grille critères 1-3"),
        ("13 h 20 – 14 h 30", "S3 · Écoute active, faits / opinions", "Distinguer faits et opinions (Bloom 4)",
         "Écoute active ; fait / opinion / sentiment ; jeu des cartons F / O / S ; reformulation en faits", "Ludique + interrogative · iconique",
         "Diapos 14-17, cartons", "Grille critère 4"),
        ("14 h 30 – 14 h 40", "Pause", "", "", "", "", ""),
        ("14 h 40 – 15 h 00", "S4 · Assertivité et DESC", "Expliquer les attitudes et la méthode (Bloom 2)", "Matrice des 4 attitudes ; DESC ; à faire / à éviter",
         "Expositive · iconique → symbolique", "Diapos 18-21", "Questions"),
        ("15 h 00 – 15 h 35", "S4 · Jeu de rôle feedback DESC", "Créer un feedback (Bloom 6)", "Trios, 3 situations, rotation ; mail à la hiérarchie (rappel)",
         "Simulation · enactif", "Diapos 22-23", "Grille critère 5"),
        ("15 h 35 – 15 h 55", "Quiz 10 questions", "Évaluer (Bloom 1-2)", "Quiz puis correction", "Évaluative", "Quiz", "Sommative 7/10"),
        ("15 h 55 – 16 h 00", "Bilan et engagement", "S’engager (Bloom 3)", "À retenir ; observer un briefing en entreprise", "Réflexive", "Diapos 25-27", "Engagement"),
    ],
}
