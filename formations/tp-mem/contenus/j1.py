from aides import cartes, encadre, flux, pyramide, tableau

J = {
    "num": 1,
    "date": "Lundi 9 novembre 2026",
    "date_court": "2026-11-09",
    "titre": "Le métier de manager d’établissement marchand : comprendre, se positionner, trouver sa place",
    "objectif_general": "Se représenter concrètement le métier de MEM, ses enjeux, la posture attendue et l’examen, "
                        "puis engager une recherche de poste ou d’entreprise d’accueil efficace en 2026, avec l’IA comme assistant.",
    "objectifs": [
        ("Se rappeler (Bloom 1)", "citer les 3 activités-types et les 10 compétences du titre MEM"),
        ("Comprendre (Bloom 2)", "expliquer la différence entre manager de proximité (MEM, niveau 5) et responsable d’établissement (REM, niveau 6)"),
        ("Appliquer (Bloom 3)", "adopter une posture managériale adaptée dans une situation de prise de poste (jeu de rôle)"),
        ("Analyser (Bloom 4)", "décoder une offre d’emploi de manager et la relier aux compétences du REAC"),
        ("Créer (Bloom 6)", "produire son pitch de 60 secondes et un CV ciblé à l’aide d’une IA, en vérifiant et en protégeant ses données"),
    ],
    "lien_reac": "Vue synoptique de l’emploi-type ; fiche emploi-type ; compétences transversales (Communiquer, Organiser ses actions, "
                 "Respecter des règles et des procédures, Résolution de problème) ; RC/RE : modalités d’évaluation et période en entreprise de 280 h.",
    "prerequis": "Aucun : journée d’ouverture. Avoir un CV, même ancien, sur clé USB ou téléphone (facultatif).",
    "materiel": "Vidéoprojecteur ; postes informatiques avec navigateur ; cartons VERT / ROUGE (un jeu par apprenant) ; 3 offres d’emploi "
                "de manager imprimées (relevées par le formateur sur France Travail la semaine même) ; post-it ; minuteur visible.",
    "progression": "Enactif : brise-glace et jeu « Vrai / Faux » (on vit le métier avant de le nommer) → Iconique : schémas des 3 blocs, "
                   "journée type, pyramide de posture → Symbolique : vocabulaire du REAC, modalités d’examen → retour enactif : jeu de rôle, "
                   "atelier IA, pitch. Le même trio (équipe / commerce / chiffres) reviendra à chaque lundi, à un niveau plus élevé (spirale).",
    "slides": [
        {"type": "couverture", "titre": "Le métier de manager", "sous_titre": "Comprendre · Se positionner · Trouver sa place",
         "date": "Lundi 9 novembre 2026", "notes":
         "Accueil. Se présenter brièvement. Annoncer : aujourd’hui, on ne fait pas encore les activités-types, on construit la carte "
         "du voyage jusqu’à l’examen. Vérifier le placement (malvoyance : près de l’écran ; lecture labiale : face au formateur). "
         "Rappeler les horaires : 8 h – 12 h / 13 h – 16 h, pauses de 10 min vers 10 h et 14 h 30."},
        {"type": "question", "titre": "Pour commencer", "texte": "Un bon manager…\nc’est qui pour vous ?", "notes":
         "Tour de table rapide : chacun cite UN manager qui l’a marqué (en bien ou en mal) et UN mot pour le décrire. "
         "Écrire les mots au tableau en deux colonnes : « ce qui motive » / « ce qui démotive ». On réutilisera ce tableau dans la séquence 2 "
         "(posture). Ne pas citer de noms de personnes réelles : prénoms ou fonctions seulement."},
        {"type": "activite", "titre": "Brise-glace : mon ticket de caisse", "duree": "15 min",
         "items": ["3 articles : mes qualités", "1 remise : mon expérience", "Total : mon objectif MEM"], "notes":
         "Chaque apprenant dessine un ticket de caisse sur une feuille : 3 « articles » = 3 qualités ; 1 « remise » = une expérience "
         "dont il est fier (job, bénévolat, sport, famille) ; « Total à payer » = ce qu’il veut obtenir avec ce titre. Présentation en "
         "30 secondes chacun. Le formateur montre l’exemple. Intérêt : on parle déjà le langage du commerce et on ose prendre la parole."},
        {"type": "cartes", "titre": "Le programme du jour", "items": [
            ("1 · Le métier", "en vrai"), ("2 · La posture", "du manager"), ("3 · L’examen", "décodé"), ("4 · Mon poste", "avec l’IA")],
         "notes": "Séquence 1 jusqu’à 10 h ; séquence 2 jusqu’à midi ; séquence 3 de 13 h à 14 h 30 ; séquence 4 jusqu’à 15 h 40 ; "
                  "quiz et bilan pour finir. Chaque séquence se termine par une activité : on apprend en faisant."},
        {"type": "section", "num": "01", "titre": "Le métier en vrai", "sous_titre": "Manager de proximité", "notes":
         "Transition : on part de ce que dit le référentiel officiel (REAC TP-00136, version 09 du 10/12/2025), mais traduit en langage terrain."},
        {"type": "puces", "titre": "MEM : le manager de proximité", "items": [
            "Un périmètre : rayon, magasin, e-commerce", "Une équipe à animer", "Des objectifs : ventes, marge",
            "Un client à satisfaire"], "notes":
         "Définition du REAC : « Le MEM est un manager de proximité. Il assure au quotidien l’organisation opérationnelle et la performance "
         "d’un périmètre commercial : rayon, magasin, point de vente spécialisé ou périmètre e-commerce rattaché. » "
         "Exemples péi : chef de rayon frais dans un hyper de Saint-Pierre, responsable d’une boutique de prêt-à-porter au centre-ville "
         "de Saint-Denis, adjoint dans une jardinerie de Saint-Paul, manager du drive d’une enseigne alimentaire."},
        {"type": "chiffre", "titre": "Un métier qui recrute", "valeur": "× 3,7",
         "legende": "offres pour 1 candidat (managers de proximité)", "source": "Source : REAC MEM v09, données début 2025",
         "notes": "Chiffre du REAC : 124 930 offres pour 33 766 demandes, soit un taux de tension de 3,7 pour les postes de manager de "
                  "proximité, contre 1,0 pour l’ensemble de la distribution. Message : vous visez un métier où l’on manque de candidats "
                  "qualifiés. Attention : chiffres nationaux, pas spécifiques à La Réunion. Ne pas inventer de chiffre local."},
        {"type": "cartes", "titre": "3 blocs = 3 activités-types", "items": [
            ("AT1", ["Manager", "l’équipe"]), ("AT2", ["Dynamiser", "le commerce"]), ("AT3", ["Piloter", "les chiffres"])],
         "t_titre": 40, "t_texte": 30, "notes":
         "AT1 : Manager l’équipe de son périmètre. AT2 : Développer la dynamique commerciale de son périmètre. AT3 : Contribuer à la "
         "performance commerciale et à la rentabilité de son périmètre. Image à donner : un tabouret à trois pieds. S’il manque un pied, "
         "le manager tombe. Chaque bloc peut être validé séparément (certificat de compétences professionnelles, CCP)."},
        {"type": "cartes", "titre": "AT1 · Manager l’équipe", "items": [
            ("Animer", "l’équipe"), ("Planifier", "l’activité"), ("Accompagner", "chacun"), ("Recruter", "et intégrer")], "notes":
         "Les 4 compétences de l’AT1, du collectif vers l’individuel : 1. Animer l’équipe ; 2. Planifier et coordonner l’activité ; "
         "3. Accompagner la performance individuelle ; 4. Contribuer au recrutement et à l’intégration. C’est le bloc placé en premier "
         "dans le référentiel car c’est le cœur du métier."},
        {"type": "cartes", "titre": "AT2 · Dynamiser le commerce", "items": [
            ("Stocks", "approvisionner"), ("Merchandiser", "valoriser l’offre"), ("Expérience client", "accueil, omnicanal")],
         "notes": "AT2 : 1. Gérer l’approvisionnement ; 2. Organiser et mettre en œuvre le merchandising de l’offre de produits et de "
                  "services ; 3. Participer à l’amélioration de l’expérience client. Nouveauté 2025 : la « vente » devient "
                  "« expérience client » (accueil, personnalisation, accessibilité, omnicanal) ; prise en compte du vrac et du réemploi."},
        {"type": "cartes", "titre": "AT3 · Piloter les chiffres", "items": [
            ("Analyser", "les ventes"), ("Analyser", "la rentabilité"), ("Corriger", "plan d’actions")], "notes":
         "AT3 : 1. Analyser la performance commerciale ; 2. Analyser la rentabilité ; 3. Proposer des actions correctives à sa hiérarchie "
         "et assurer le suivi du plan d’actions. Le MEM ne fait plus les prévisions financières (c’est le REM, niveau 6) : il collecte, "
         "analyse, alerte et propose."},
        {"type": "comparer", "titre": "MEM ou REM ?", "gauche": ("MEM · niveau 5", ["Terrain, quotidien", "Son périmètre", "Analyse, propose", "Rend compte"]),
         "droite": ("REM · niveau 6", ["Stratégie", "Tout l’établissement", "Prévoit, décide", "Pilote les projets"]),
         "notes": "Différence clé pour l’examen : le jury attend un manager OPÉRATIONNEL qui connaît les limites de sa responsabilité "
                  "(compétence transversale « Respecter des règles et des procédures »). Exemple : face à une baisse de marge, le MEM "
                  "analyse, alerte son N+1 et propose 2 ou 3 actions chiffrées ; il ne décide pas seul de baisser les prix de tout le magasin."},
        {"type": "exemple", "titre": "Une journée de Nadia", "lieu": "Saint-Louis", "lieu_detail": ["Manager rayon frais", "Hypermarché", "8 personnes"],
         "items": ["5 h 45 : réception, contrôle", "7 h : briefing équipe", "9 h : ruptures, prix", "14 h : planning semaine", "16 h : chiffres du jour"],
         "notes": "Personnage fictif. Raconter la journée comme une histoire : 5 h 45, réception d’une palette de letchis dont 2 cagettes "
                  "sont abîmées (approvisionnement, AT2) ; 7 h, briefing de 10 minutes debout : objectif du jour, mise en avant des "
                  "letchis, rappel sécurité transpalette (AT1) ; 9 h, ruptures en yaourts, elle relance la commande (AT2) ; 11 h, "
                  "entretien de suivi avec une nouvelle recrue (AT1) ; 14 h, planning de la semaine avec un congé imprévu (AT1) ; 16 h, "
                  "chiffre d’affaires du jour comparé à N-1, la démarque est en hausse, elle alerte son responsable (AT3). "
                  "Faire repérer par le groupe à quel bloc appartient chaque moment."},
        {"type": "activite", "titre": "Jeu : Vrai ou Faux ?", "genre": "Cartons vert / rouge", "duree": "20 min",
         "items": ["J’écoute l’affirmation", "Je lève mon carton", "Je justifie en 1 phrase"], "notes":
         "Lire une affirmation, tout le monde lève un carton en même temps (vert = vrai, rouge = faux), puis un volontaire justifie. "
         "Affirmations : 1) Le MEM fixe seul les prix de son rayon (FAUX : il applique la politique de l’enseigne et propose). "
         "2) Le MEM peut participer à la mise en rayon (VRAI : « le cas échéant, se joindre aux collaborateurs », REAC). "
         "3) Le MEM réalise les prévisions financières de l’établissement (FAUX : c’est le REM). 4) L’expérience client inclut "
         "l’accessibilité aux personnes en situation de handicap (VRAI). 5) Un manager n’a pas à se soucier de la sécurité, c’est le rôle "
         "des RH (FAUX : prévention des risques = compétence transversale). 6) Pour l’examen, il faut 280 h en entreprise (VRAI). "
         "7) Le MEM participe au recrutement (VRAI : il « contribue »). 8) Le dossier se rédige en police libre (FAUX : Arial 11, interligne 1,15). "
         "Accessibilité : lire chaque affirmation à voix haute ET l’afficher ; les cartons ont aussi un symbole (✔ / ✖) pour les daltoniens."},
        {"type": "section", "num": "02", "titre": "Enjeux et posture", "sous_titre": "Devenir manager, pas « super vendeur »", "notes":
         "Pause de 10 minutes juste avant ou juste après selon l’horaire (10 h 00 – 10 h 10)."},
        {"type": "cartes", "titre": "Les enjeux du métier en 2026", "items": [
            ("Omnicanal", "magasin + web"), ("RSE", "vrac, anti-gaspi"), ("Sécurité", "prévenir les risques"),
            ("Data", "indicateurs, outils"), ("Équipes", "tous âges"), ("Inclusion", "handicap, accueil")], "notes":
         "Ces enjeux viennent directement du REAC (« Enjeux, problématique et questionnement »). Exemples péi : click & collect d’une "
         "enseigne de bricolage au Port ; rayon vrac et consigne dans une épicerie de Saint-Leu ; chaleur en réserve l’été austral "
         "(prévention) ; équipe avec un étudiant de 19 ans et une collaboratrice de 58 ans qui n’ont pas les mêmes attentes."},
        {"type": "etapes", "titre": "Du vendeur au manager", "items": [
            ("Faire", "je fais moi-même"), ("Faire faire", "je délègue, je contrôle"), ("Faire grandir", "je développe l’équipe")],
         "notes":
         "Le piège n° 1 du nouveau manager : rester le meilleur vendeur et tout faire soi-même. Résultat : il s’épuise et l’équipe ne "
         "progresse pas. La progression attendue : faire (montrer l’exemple), faire faire (déléguer avec des consignes claires et un "
         "contrôle), faire grandir (former, faire monter en compétences, préparer un remplaçant). Lien AT1 : déléguer des responsabilités "
         "(REAC, compétence « Planifier et coordonner »)."},
        {"type": "cartes", "titre": "4 piliers de la posture", "items": [
            ("Exemplaire", "je fais ce que je dis"), ("Clair", "consignes, objectifs"), ("À l’écoute", "je reformule"), ("Juste", "même règle pour tous")],
         "notes": "Relier au tableau du brise-glace : les mots « ce qui motive » se rangent presque toujours dans ces 4 piliers. "
                  "Le REAC insiste sur : distinguer faits et opinions, vérifier la bonne compréhension, tenir compte de la confidentialité."},
        {"type": "comparer", "titre": "Ni copain, ni petit chef", "gauche": ("Trop copain", ["Pas de cadre", "Favoritisme", "Perte d’autorité"]),
         "droite": ("Petit chef", ["Ordres sans sens", "Peur, turnover", "Zéro initiative"]),
         "notes": "Le juste milieu : proche ET exigeant. Phrase à retenir : « Je suis proche des personnes et exigeant sur les règles. » "
                  "Cas fréquent en titre pro : l’apprenant devient manager de ses anciens collègues. Conseil : un entretien individuel "
                  "avec chacun dans la première semaine, poser le cadre, ne pas changer tout d’un coup."},
        {"type": "activite", "titre": "Jeu de rôle : promu demain", "genre": "Par trois · 3 rôles", "duree": "35 min",
         "items": ["Manager : premier briefing", "Collègue vexé·e", "Observateur : la grille"], "notes":
         "Situation : Kévin, vendeur depuis 4 ans dans une enseigne de sport de Saint-Pierre, est promu responsable de rayon. Demain, il "
         "fait son premier briefing devant ses anciens collègues, dont Sabrina qui visait aussi le poste. Rôles : le manager (5 min de "
         "briefing), la collègue vexée (objections réalistes, sans agressivité), l’observateur (note les 4 piliers : exemplaire, clair, "
         "à l’écoute, juste). Rotation des rôles : 3 passages de 10 minutes. Débriefing collectif de 5 minutes : qu’est-ce qui a "
         "fonctionné ? Variante accessibilité : rôle d’observateur possible à l’oral, sans écrire."},
        {"type": "section", "num": "03", "titre": "L’examen décodé", "sous_titre": "Savoir où l’on va", "notes":
         "Après la pause déjeuner (13 h). Énergie basse : on démarre par une question au groupe : « Selon vous, combien de temps dure "
         "l’examen ? » Réponse : 7 h 55 pour le candidat."},
        {"type": "cartes", "titre": "Les épreuves du titre", "items": [
            ("Étude de cas", ["4 h · AT2", "Word + Excel"]), ("Entretien technique", ["1 h 30", "sur l’étude de cas"]),
            ("Vos dossiers", ["2 h 10", "AT3 + AT1"]), ("Entretien final", ["15 min", "le projet"])], "notes":
         "Source : RC/RE MEM v09. 1) Mise en situation professionnelle : étude de cas de 4 h dans un établissement fictif, sur l’AT2, avec "
         "un dossier papier et des maquettes numériques, sur traitement de texte et tableur ; on imprime ses travaux. 2) Entretien technique "
         "de 1 h 30 : 30 min de préparation, 10 min de présentation, 50 min d’échange. 3) Questionnement à partir de productions de 2 h 10 : "
         "20 min de présentation du diaporama AT3 + 40 min de questions ; 25 min de présentation du diaporama AT1 + 45 min de questions. "
         "4) Entretien final de 15 min, y compris le dossier professionnel. Total : 7 h 55."},
        {"type": "cartes", "titre": "Vos 2 productions à préparer", "items": [
            ("Dossier AT3", ["12 à 18 pages", "+ 12 à 18 diapos"]), ("Dossier AT1", ["16 à 24 pages", "+ 18 à 24 diapos"])],
         "t_titre": 36, "t_texte": 30, "notes":
         "Règles de forme : police Arial 11, interligne 1,15, pages hors garde, sommaire et annexes. Chaque document commence par une page "
         "de présentation de l’établissement. Le dossier AT3 est écrit comme un document adressé à un supérieur hiérarchique. "
         "Les diaporamas : hors page de garde et sommaire. D’où le lundi 16/11 consacré à Word, Excel et PowerPoint."},
        {"type": "chiffre", "titre": "La clé : l’entreprise", "valeur": "280 h", "legende": "en entreprise, obligatoires",
         "source": "Source : RC/RE MEM v09", "notes":
         "Sans période en entreprise, pas d’examen : les dossiers se construisent à partir de VOS observations et actions réelles. "
         "Les apprenants qui n’ont pas encore d’entreprise d’accueil : c’est la priorité de la séquence 4. Preuve de la période à "
         "remettre au responsable de session."},
        {"type": "puces", "titre": "Ce que le jury regarde", "items": [
            "Des faits, des chiffres", "Vos actions à vous", "Les limites de votre rôle", "Clarté, posture"], "notes":
         "Le jury évalue un professionnel, pas un élève qui récite. Il cherche : des preuves (plannings, comptes rendus, tableaux, photos "
         "terrain), le « je » plutôt que le « on », la conscience de son périmètre, et une communication claire. Conseil : commencez dès "
         "maintenant un carnet de bord de vos observations en entreprise (sans données personnelles de clients ou de collègues)."},
        {"type": "section", "num": "04", "titre": "Trouver mon poste en 2026", "sous_titre": "Méthode + IA = efficacité", "notes":
         "Pour les apprenants déjà en entreprise : la séquence sert à préparer la suite (poste après le titre, évolution interne)."},
        {"type": "etapes", "titre": "La méthode en 5 étapes", "items": [
            ("Cibler", "enseignes, secteur"), ("Préparer", "CV, pitch"), ("Diffuser", "canaux"), ("Relancer", "J+7"), ("Convaincre", "entretien")],
         "notes":
         "Cibler : 15 entreprises maximum, classées par secteur (alimentaire, sport, bricolage, mode, jardinerie…) et par zone (Sud, Ouest, "
         "Nord, Est). Préparer : un CV adapté à chaque offre. Diffuser : plusieurs canaux. Relancer : un appel ou un passage en magasin "
         "une semaine après. Convaincre : préparer des exemples concrets (méthode STAR, voir la ressource)."},
        {"type": "cartes", "titre": "Où chercher ?", "items": [
            ("France Travail", "offres, alternance"), ("LinkedIn", "réseau, managers"), ("Job boards", "Indeed, HelloWork"),
            ("Sur place", "CV en main"), ("Réseau", "forums, anciens"), ("Intérim", "agences")], "notes":
         "Spécificité réunionnaise : le réseau et la démarche en personne restent très efficaces. Se présenter en magasin en dehors des "
         "heures de pointe (pas le samedi après-midi !), demander le responsable, CV en main, tenue soignée. Les forums emploi et les "
         "salons de l’alternance organisés sur l’île sont aussi des occasions directes. Le formateur vérifie les dates des prochains "
         "forums avant la séance (ne pas annoncer une date non vérifiée)."},
        {"type": "cartes", "titre": "L’IA : mon assistant", "items": [
            ("Analyser", "une offre d’emploi"), ("Adapter", "mon CV, ma lettre"), ("M’entraîner", "simulation d’entretien")],
         "notes": "Outils : Le Chat (Mistral AI, entreprise française, hébergement en Europe), Microsoft Copilot, ChatGPT, Gemini. "
                  "Préférer un outil européen quand c’est possible (souveraineté des données). L’IA ne remplace pas votre expérience : elle "
                  "vous aide à la formuler. RGPD : ne jamais coller son numéro de sécurité sociale, son adresse complète ou des informations "
                  "de santé ; anonymiser le CV avant de le soumettre (remplacer nom et coordonnées par [NOM], [TEL])."},
        {"type": "comparer", "titre": "IA : bon ou mauvais usage ?", "gauche": ("Oui", ["Je vérifie tout", "Je garde mon style", "J’anonymise"]),
         "droite": ("Non", ["Je copie-colle", "J’invente", "Je donne tout"]), "notes":
         "Un recruteur repère en 10 secondes une lettre générée et copiée telle quelle (« passionné par le dynamisme de votre enseigne… »). "
         "Une IA peut inventer des diplômes ou des expériences : tout relire. IA Act : quand un employeur utilise une IA pour trier les CV, "
         "c’est un système « à haut risque » (règlement UE 2024/1689, annexe III, point 4) : il doit garder un contrôle humain et informer. "
         "RGPD article 22 : le candidat peut refuser une décision prise uniquement par une machine."},
        {"type": "puces", "titre": "Un bon prompt : R-C-T-F", "items": [
            "Rôle : qui parle ?", "Contexte : poste, enseigne", "Tâche : je veux…", "Format : liste, longueur"], "notes":
         "Exemple complet à afficher dans la ressource : « Tu es recruteur pour une enseigne de bricolage à La Réunion (Rôle). Je postule "
         "à un poste de manager de rayon en alternance, j’ai 3 ans d’expérience de vendeur (Contexte). Pose-moi 8 questions d’entretien, "
         "une par une, attends ma réponse et donne-moi un conseil après chaque réponse (Tâche). Réponses courtes, en français simple "
         "(Format). » Les apprenants le testent en séquence suivante."},
        {"type": "activite", "titre": "Atelier : mon pitch de 60 s", "genre": "Individuel puis en binôme", "duree": "40 min",
         "items": ["Décoder une offre", "Pitch avec l’IA", "Je le dis"], "notes":
         "1) Chaque apprenant choisit une des 3 offres imprimées et surligne : missions, compétences, savoir-être. Il relie chaque élément "
         "à une compétence du REAC (10 min). 2) Avec l’IA et le prompt R-C-T-F, il construit un pitch de 60 secondes : qui je suis, ce que "
         "j’ai fait, ce que je veux (15 min). Il réécrit ensuite le pitch avec ses propres mots. 3) Binôme : chacun dit son pitch, "
         "l’autre chronomètre et donne 1 point fort + 1 conseil (15 min). Évaluation formative avec la grille critériée du jour."},
        {"type": "activite", "titre": "Quiz : 10 questions", "genre": "Individuel", "duree": "15 min",
         "items": ["10 questions", "Correction ensemble", "Objectif : 7 / 10"], "notes":
         "Distribuer la version apprenant. Lire les questions à voix haute pour les personnes qui en ont besoin ; temps majoré si "
         "aménagement. Correction collective immédiate : on explique chaque réponse."},
        {"type": "puces", "titre": "À retenir", "items": [
            "Équipe · commerce · chiffres", "Manager = faire grandir", "Examen : 7 h 55", "280 h en entreprise", "IA : je vérifie"],
         "notes": "Faire reformuler par 2 apprenants. Annoncer lundi prochain : Word, Excel, PowerPoint pour l’examen."},
        {"type": "question", "titre": "Mon engagement", "texte": "D’ici lundi prochain,\nje fais…", "notes":
         "Chacun écrit sur un post-it UNE action concrète (envoyer 3 candidatures, appeler mon tuteur, ouvrir mon carnet de bord…). "
         "Le post-it est repris lundi prochain en ouverture. Fin de journée 16 h."},
    ],
    "ressource": [
        ("Le MEM en une phrase",
         "<p>Le manager d’établissement marchand (MEM) est un <b>manager de proximité</b>. Il organise le quotidien et fait progresser "
         "les résultats d’un <b>périmètre commercial</b> : un rayon, un magasin, un point de vente spécialisé ou un périmètre "
         "e-commerce rattaché (drive, retrait en magasin, préparation de commandes).</p>"
         + encadre("def", "<p><b>Périmètre</b> : la partie de l’établissement dont vous êtes responsable (exemple : le rayon frais, "
                   "ou toute la boutique si c’est un petit commerce). Le mot revient dans chaque bloc du titre : vous êtes jugé sur "
                   "VOTRE périmètre, pas sur tout l’établissement.</p>")
         + "<p>Ses 4 missions, en langage simple :</p>"
         + cartes([("Une équipe", "à animer, organiser, faire progresser"), ("Un commerce", "à approvisionner et rendre attractif"),
                   ("Des clients", "à accueillir et satisfaire, en magasin et en ligne"), ("Des chiffres", "ventes et marge à suivre et améliorer")], cols=4)
         + "<h3>MEM (niveau 5) ou REM (niveau 6) ?</h3>"
         + tableau(["", "MEM — Manager d’établissement marchand", "REM — Responsable d’établissement marchand"], [
             ["Niveau", "5 (équivalent bac + 2)", "6 (équivalent bac + 3/4)"],
             ["Horizon", "Le jour, la semaine, le mois", "Le trimestre, l’année, la stratégie"],
             ["Champ", "Son périmètre (rayon, secteur, boutique)", "Tout l’établissement"],
             ["Chiffres", "Collecte, analyse, alerte, propose des actions", "Prévisions économiques et financières, décisions"],
             ["Projets", "Y associe son équipe, les met en œuvre", "Conduit et pilote les projets"]])
         + encadre("jury", "<p>Le jury attend un manager <b>opérationnel</b> qui connaît les limites de sa responsabilité. Exemple de "
                   "bonne réponse : « J’ai constaté une baisse de 6 % du chiffre d’affaires du rayon par rapport à l’an dernier, j’en ai "
                   "analysé les causes et j’ai proposé trois actions à mon responsable, qui en a validé deux. »</p>")),
        ("Les 3 activités-types et les 10 compétences",
         "<p>Le titre est construit en <b>3 blocs</b> (activités-types). Chaque bloc peut être validé séparément sous forme de "
         "certificat de compétences professionnelles (CCP). Imaginez un <b>tabouret à trois pieds</b> : sans l’un d’eux, le manager tombe.</p>"
         + tableau(["Activité-type", "Compétences professionnelles", "En clair"], [
             ["<b>AT1</b> Manager l’équipe de son périmètre", "1. Animer l’équipe<br>2. Planifier et coordonner l’activité<br>"
              "3. Accompagner la performance individuelle<br>4. Contribuer au recrutement et à l’intégration",
              "Briefings, motivation, plannings, entretiens, recrutement, accueil des nouveaux"],
             ["<b>AT2</b> Développer la dynamique commerciale", "5. Gérer l’approvisionnement<br>6. Organiser et mettre en œuvre le "
              "merchandising<br>7. Participer à l’amélioration de l’expérience client",
              "Commandes, stocks, ruptures, mise en rayon, implantation, accueil, omnicanal"],
             ["<b>AT3</b> Contribuer à la performance et à la rentabilité", "8. Analyser la performance commerciale<br>9. Analyser la "
              "rentabilité<br>10. Proposer des actions correctives et suivre le plan d’actions",
              "Indicateurs, écarts, marge, démarque, plan d’actions, reporting"]])
         + "<h3>Les 4 compétences transversales (présentes partout)</h3>"
         + cartes([("Communiquer", "consignes claires, écrits factuels pour la hiérarchie, écoute"),
                   ("Organiser ses actions", "anticiper, planifier, gérer les imprévus, prévenir les risques"),
                   ("Respecter règles et procédures", "limites de son rôle, politique RH, RSE, sécurité"),
                   ("Résoudre des problèmes", "analyser une situation, trouver des solutions, suivre")], cols=4)
         + encadre("retenir", "<p><b>Équipe – Commerce – Chiffres.</b> Ces trois mots résument le métier. Vous les retrouverez à chaque "
                   "lundi, de plus en plus en profondeur.</p>")),
        ("Une journée type (personnage fictif)",
         "<p>Nadia est manager du rayon frais d’un hypermarché de Saint-Louis. Elle encadre 8 personnes.</p>"
         + tableau(["Heure", "Ce que fait Nadia", "Bloc"], [
             ["5 h 45", "Réception d’une livraison : 2 cagettes de letchis abîmées, elle émet une réserve sur le bon de livraison", "AT2"],
             ["7 h 00", "Briefing debout de 10 minutes : objectif du jour, mise en avant des letchis, rappel sécurité transpalette", "AT1"],
             ["9 h 00", "Tour du rayon : 3 ruptures en yaourts, elle relance la commande et ajuste l’implantation", "AT2"],
             ["11 h 00", "Entretien de suivi avec une nouvelle recrue arrivée il y a 2 semaines", "AT1"],
             ["14 h 00", "Planning de la semaine : un congé imprévu, elle réorganise en respectant les temps de repos", "AT1"],
             ["15 h 30", "Une cliente en fauteuil ne peut pas atteindre un produit : elle fait revoir l’emplacement", "AT2"],
             ["16 h 00", "Chiffre du jour comparé à l’an dernier ; la démarque augmente, elle alerte son responsable", "AT3"]])
         + encadre("ex", "<p>Le même métier change selon l’établissement : dans une petite boutique de Saint-Denis, le manager fait "
                   "presque tout lui-même ; dans un grand hypermarché, ses missions sont plus ciblées et encadrées (REAC, « structure "
                   "du tissu économique »).</p>")),
        ("Les enjeux du métier en 2026",
         "<p>Le référentiel (rédigé à partir de 64 entretiens de managers et responsables entre 2023 et 2025) met en avant ces enjeux :</p>"
         + cartes([("Omnicanalité", "le client passe du site au magasin : click & collect, drive, réseaux sociaux"),
                   ("RSE", "vrac, réemploi, seconde main, lutte contre le gaspillage, circuits courts"),
                   ("Santé-sécurité", "prévenir les risques : port de charges, chaleur, agressions, chutes"),
                   ("Données", "suivre des indicateurs, utiliser les outils numériques pour décider"),
                   ("Équipes variées", "plusieurs générations, plusieurs cultures, attentes différentes"),
                   ("Inclusion", "accueil des clients et collaborateurs en situation de handicap")], cols=3)
         + encadre("ex", "<p>Exemples péi : le rayon vrac d’une épicerie de Saint-Leu demande des règles d’hygiène et de traçabilité "
                   "renforcées ; en été austral, la chaleur dans une réserve non climatisée devient un risque à prévenir ; une "
                   "équipe peut réunir un étudiant de 19 ans et une collaboratrice de 58 ans qui n’attendent pas la même chose de leur "
                   "manager.</p>")),
        ("La posture du manager",
         "<h3>Du vendeur au manager</h3>"
         + flux([("Faire", "Je montre l’exemple, je sais faire le métier"), ("Faire faire", "Je délègue avec des consignes claires et je contrôle"),
                 ("Faire grandir", "Je forme, je fais progresser, je prépare la relève")], "La progression du manager de proximité")
         + "<p>Le piège n° 1 : rester « le meilleur vendeur » et tout faire soi-même. Le manager s’épuise et l’équipe ne progresse pas.</p>"
         + "<h3>Les 4 piliers</h3>"
         + cartes([("Exemplaire", "Je respecte moi-même les règles que je demande (horaires, sécurité, tenue)."),
                   ("Clair", "Mes consignes disent quoi, qui, quand, comment, et pourquoi (le sens)."),
                   ("À l’écoute", "Je laisse parler, je reformule, je distingue faits et opinions."),
                   ("Juste", "La même règle pour tous, pas de favoritisme, confidentialité respectée.")], cols=4)
         + "<h3>Ni copain, ni petit chef</h3>"
         + tableau(["Trop copain", "Juste milieu", "Petit chef"], [
             ["Pas de cadre, règles floues", "Proche des personnes, exigeant sur les règles", "Ordres sans explication"],
             ["Favoritisme ressenti", "Équité, explications, écoute", "Peur, départs, absentéisme"],
             ["Perte d’autorité", "Autorité reconnue", "Plus aucune initiative"]])
         + encadre("astuce", "<p><b>Promu parmi ses anciens collègues ?</b> Dans la première semaine : un entretien individuel avec "
                   "chacun, poser le cadre calmement, reconnaître ce qui fonctionne déjà, ne pas tout changer d’un coup, et rester "
                   "constant. La légitimité se gagne par les actes.</p>")),
        ("L’examen décodé",
         tableau(["Épreuve", "Durée", "Ce qui se passe", "Compétences"], [
             ["Mise en situation professionnelle (étude de cas)", "4 h", "Établissement fictif ; dossier papier + maquettes numériques ; "
              "travail sur traitement de texte et tableur ; impression des travaux", "AT2 : approvisionnement, merchandising, expérience client"],
             ["Entretien technique", "1 h 30", "30 min de préparation, 10 min de présentation, 50 min d’échange avec simulations possibles", "AT2"],
             ["Questionnement à partir de productions", "2 h 10", "Diaporama AT3 : 20 min + 40 min de questions ; diaporama AT1 : 25 min + "
              "45 min de questions", "AT3 et AT1"],
             ["Entretien final", "15 min", "Échange avec le jury, y compris sur le dossier professionnel", "Ensemble du titre"]])
         + "<p><b>Durée totale pour le candidat : 7 h 55.</b></p>"
         + "<h3>Les deux productions à rédiger en amont</h3>"
         + tableau(["Production", "Document", "Diaporama", "Contenu"], [
             ["AT3 — Performance et rentabilité", "12 à 18 pages", "12 à 18 diapositives", "Synthèse, contexte ; performance commerciale ; "
              "rentabilité ; actions correctives et suivi (rédigé pour un supérieur hiérarchique)"],
             ["AT1 — Manager l’équipe", "16 à 24 pages", "18 à 24 diapositives", "Animer ; planifier et coordonner ; accompagner la "
              "performance ; recrutement et intégration"]])
         + "<p>Forme obligatoire : <b>Arial 11, interligne 1,15</b> ; pages comptées hors page de garde, sommaire et annexes ; une page de "
           "présentation de l’établissement en introduction de chaque document.</p>"
         + encadre("retenir", "<p><b>280 heures en entreprise sont obligatoires</b> pour se présenter au titre complet (140 h pour un seul "
                   "CCP). Vos dossiers se construisent à partir de vos observations et de vos actions réelles.</p>")
         + encadre("jury", "<p>Le jury veut : des <b>faits et des chiffres</b> ; <b>vos</b> actions (« je » plutôt que « on ») ; des "
                   "<b>preuves</b> (plannings, comptes rendus, tableaux de suivi, photos du rayon) ; la conscience des <b>limites de "
                   "votre rôle</b> ; une communication claire.</p>")
         + encadre("loi", "<p><b>RGPD dans vos dossiers :</b> les plannings, comptes rendus d’entretien ou captures d’écran contiennent des "
                   "données personnelles de collègues ou de clients. Anonymisez-les toujours (« Collaborateur A », initiales) et demandez "
                   "l’accord de votre tuteur avant d’utiliser un document interne.</p>")),
        ("Trouver mon poste ou mon entreprise d’accueil en 2026",
         flux([("Cibler", "15 entreprises max, par secteur et par zone"), ("Préparer", "CV adapté à chaque offre, pitch de 60 s"),
               ("Diffuser", "plusieurs canaux en parallèle"), ("Relancer", "appel ou visite 7 jours après"),
               ("Convaincre", "entretien préparé avec la méthode STAR")], "La méthode en 5 étapes")
         + "<h3>Les canaux</h3>"
         + tableau(["Canal", "Pour quoi faire", "Conseil"], [
             ["France Travail (site et application)", "Offres d’emploi et d’alternance, simulateurs, ateliers", "Activer les alertes avec les mots "
              "« manager », « responsable de rayon », « adjoint »"],
             ["LinkedIn", "Être trouvé, contacter des managers de magasin", "Photo professionnelle, titre clair : « Futur manager "
              "d’établissement marchand — en alternance »"],
             ["Job boards (Indeed, HelloWork…)", "Volume d’offres", "Lire l’offre en entier, adapter le CV à chaque fois"],
             ["En personne, au magasin", "Très efficace à La Réunion", "Venir hors heures de pointe, demander le responsable, CV en main"],
             ["Réseau, forums, salons", "Rencontrer directement les recruteurs", "Préparer son pitch et 5 CV imprimés"],
             ["Agences d’intérim", "Missions dans le commerce", "Une première mission peut ouvrir un poste"]])
         + "<h3>Le pitch de 60 secondes</h3>"
         + flux([("Qui je suis", "prénom, situation, formation MEM"), ("Ce que j’ai fait", "1 ou 2 réussites concrètes et chiffrées"),
                 ("Ce que je veux", "le poste visé, ce que j’apporte")])
         + "<h3>La méthode STAR pour répondre en entretien</h3>"
         + cartes([("S — Situation", "Le contexte : où, quand"), ("T — Tâche", "Ce qu’on attendait de moi"),
                   ("A — Action", "Ce que J’AI fait, concrètement"), ("R — Résultat", "Ce que ça a donné, en chiffres si possible")], cols=4)
         + encadre("ex", "<p>« Pendant les fêtes de fin d’année (S), je devais gérer seul le rayon jouets un samedi (T). J’ai réorganisé la "
                   "réserve pour réapprovisionner plus vite et j’ai mis en avant les produits les plus demandés à l’entrée (A). Nous "
                   "n’avons eu aucune rupture sur les 10 meilleures ventes ce jour-là (R). »</p>")),
        ("L’IA au service de ma recherche",
         "<p>L’IA générative (Le Chat de Mistral AI, Microsoft Copilot, ChatGPT, Gemini…) est un <b>assistant</b> : elle aide à formuler, "
         "pas à inventer votre parcours. Quand c’est possible, préférez un outil européen (Le Chat, entreprise française) pour la "
         "protection de vos données.</p>"
         + "<h3>La formule R-C-T-F</h3>"
         + cartes([("Rôle", "« Tu es recruteur dans le commerce à La Réunion… »"), ("Contexte", "le poste, l’enseigne, votre profil"),
                   ("Tâche", "ce que vous attendez exactement"), ("Format", "longueur, style, liste ou tableau")], cols=4)
         + "<h3>3 prompts prêts à l’emploi</h3>"
         + tableau(["Objectif", "Prompt (à adapter)"], [
             ["Décoder une offre", "« Tu es conseiller en recrutement. Voici une offre de manager de rayon : [coller l’offre sans le nom du "
              "recruteur]. Liste les 5 compétences les plus importantes et, pour chacune, une question qu’on pourrait me poser. Réponds "
              "en liste courte. »"],
             ["Adapter mon CV", "« Voici mon CV anonymisé : [coller le CV en remplaçant nom, adresse, téléphone par des crochets]. Propose "
              "3 améliorations pour le rendre adapté à cette offre : [offre]. N’invente aucune expérience. »"],
             ["Simuler un entretien", "« Tu es recruteur pour une enseigne de bricolage à La Réunion. Je postule à un poste de manager de "
              "rayon en alternance. Pose-moi 8 questions, une par une, attends ma réponse et donne un conseil après chacune. Français simple. »"]])
         + tableau(["Bon usage", "Mauvais usage"], [
             ["Je relis et je vérifie chaque information", "Je copie-colle sans relire"],
             ["Je réécris avec mes mots", "Je laisse l’IA inventer des expériences"],
             ["J’anonymise mon CV avant de le coller", "Je donne mon adresse, mon numéro de sécurité sociale, ma santé"]])
         + encadre("loi", "<p><b>RGPD</b> (règlement UE 2016/679) : vos données vous appartiennent ; ne transmettez à une IA que le "
                   "nécessaire (principe de minimisation, art. 5). Certains outils réutilisent les conversations pour s’entraîner : "
                   "désactivez cette option dans les paramètres quand elle existe.<br><b>IA Act</b> (règlement UE 2024/1689) : un "
                   "logiciel d’IA utilisé par un employeur pour trier des candidatures est classé <b>« à haut risque »</b> (annexe III, "
                   "point 4) ; il doit rester sous contrôle humain. Et le RGPD (art. 22) vous protège contre une décision prise "
                   "uniquement par une machine : vous pouvez demander l’intervention d’une personne.</p>")),
        ("Lexique",
         tableau(["Mot", "Définition simple"], [
             ["REAC", "Référentiel emploi activités compétences : décrit le métier et les compétences du titre"],
             ["RC / RE", "Référentiel de certification / d’évaluation : décrit comment se passe l’examen"],
             ["Activité-type (AT)", "Un grand bloc du métier ; le titre MEM en compte 3"],
             ["CCP", "Certificat de compétences professionnelles : validation d’une seule activité-type"],
             ["Périmètre", "La partie de l’établissement dont le manager est responsable"],
             ["Omnicanal", "Le client utilise plusieurs canaux (magasin, site, application, réseaux) pour un même achat"],
             ["RSE", "Responsabilité sociétale des entreprises : impact social et environnemental de l’activité"],
             ["Démarque", "Perte de marchandise : vol, casse, produits périmés, erreurs"],
             ["Prompt", "La consigne écrite que l’on donne à une IA"]])),
        ("Pour aller plus loin",
         "<ul><li>Relire la « Vue synoptique » du REAC (page 10) : elle tient sur une page et résume tout le titre.</li>"
         "<li>Ouvrir un <b>carnet de bord</b> de la période en entreprise : une page par semaine, ce que j’ai observé, ce que j’ai fait, "
         "les chiffres du rayon (sans données personnelles).</li>"
         "<li>Créer une alerte France Travail sur « manager » + votre zone.</li>"
         "<li>Préparer pour lundi prochain : un document Word avec votre CV et une offre que vous aimeriez décrocher.</li></ul>"),
    ],
    "sources": [
        "Référentiel emploi activités compétences (REAC) — Titre professionnel Manager d’établissement marchand, TP-00136, version 09 du 10/12/2025 (pièce jointe fournie).",
        "Référentiel de certification et d’évaluation (RC/RE) — MEM, version 09 du 10/12/2025 (pièce jointe fournie).",
        "Règlement (UE) 2016/679 (RGPD), articles 5 et 22 — eur-lex.europa.eu.",
        "Règlement (UE) 2024/1689 (IA Act), annexe III point 4 — eur-lex.europa.eu.",
    ],
    "grille": {
        "situation": "Atelier « Mon pitch de 60 s » : décodage d’une offre réelle, pitch oral construit avec l’aide d’une IA, présenté en binôme.",
        "criteres": [
            {"critere": "Compréhension du métier", "indicateurs": ["Définit le périmètre et les missions du MEM", "Distingue MEM et REM"],
             "niveaux": ["Définition confuse ou fausse", "Définition partielle", "Définition juste, avec un exemple", "Définition juste, exemples variés, limites du rôle claires"]},
            {"critere": "Repérage des 3 activités-types", "indicateurs": ["Relie les éléments de l’offre aux AT du REAC", "Cite les épreuves de l’examen"],
             "niveaux": ["Aucun lien fait", "1 AT reliée", "3 AT reliées correctement", "3 AT reliées et justifiées, examen expliqué"]},
            {"critere": "Posture managériale", "indicateurs": ["Applique les 4 piliers en jeu de rôle", "Évite les postures « copain » et « petit chef »"],
             "niveaux": ["Posture inadaptée", "1 ou 2 piliers visibles", "3 piliers visibles", "4 piliers, adaptation à l’interlocuteur"]},
            {"critere": "Communication orale du pitch", "indicateurs": ["Respecte 60 s ± 10 s", "Structure : qui je suis / ce que j’ai fait / ce que je veux"],
             "niveaux": ["Non structuré, hors temps", "Structure incomplète", "Structuré, dans le temps", "Structuré, chiffré, convaincant, regard et voix maîtrisés"]},
            {"critere": "Usage raisonné de l’IA", "indicateurs": ["Prompt R-C-T-F complet", "Vérifie, réécrit, anonymise ses données"],
             "niveaux": ["Copie sans vérifier ou données exposées", "Prompt incomplet", "Prompt complet, texte vérifié", "Prompt complet, texte personnalisé, RGPD respecté et expliqué"]},
        ]},
    "quiz": [
        {"q": "Combien d’activités-types compte le titre professionnel MEM ?", "choix": ["2", "3", "4", "10"], "rep": 1,
         "explication": "3 activités-types : manager l’équipe (AT1), développer la dynamique commerciale (AT2), contribuer à la performance et à la rentabilité (AT3). 10 est le nombre de compétences."},
        {"q": "Quelle mission relève du REM (niveau 6) et non du MEM ?", "choix": ["Animer un briefing", "Réaliser les prévisions économiques et financières de l’établissement",
                                                                                  "Analyser la démarque du rayon", "Participer au recrutement"], "rep": 1,
         "explication": "Depuis la révision de 2025, les prévisions économiques et financières relèvent du REM. Le MEM analyse, alerte et propose."},
        {"q": "Dans le titre MEM, la notion de « vente » a été remplacée par :", "choix": ["la prospection", "l’expérience client", "la négociation", "le merchandising"], "rep": 1,
         "explication": "L’expérience client inclut l’accueil, la personnalisation, l’accessibilité et la relation omnicanale."},
        {"q": "Quelle est la durée de l’étude de cas (mise en situation professionnelle) ?", "choix": ["1 h 30", "2 h 10", "4 h", "7 h 55"], "rep": 2,
         "explication": "4 h sur poste informatique (traitement de texte et tableur). 7 h 55 est la durée totale de l’examen pour le candidat."},
        {"q": "Combien d’heures en entreprise sont obligatoires pour présenter le titre complet ?", "choix": ["140 h", "210 h", "280 h", "400 h"], "rep": 2,
         "explication": "280 h pour le titre complet ; 140 h pour un seul certificat de compétences professionnelles."},
        {"q": "Quelle police et quel interligne sont imposés pour les dossiers ?", "choix": ["Times 12, interligne 1,5", "Arial 11, interligne 1,15",
                                                                                           "Calibri 11, interligne simple", "Libre"], "rep": 1,
         "explication": "Le RC/RE impose Arial 11 et un interligne de 1,15."},
        {"q": "La progression du manager de proximité, c’est :", "choix": ["Faire → Faire faire → Faire grandir", "Contrôler → Sanctionner → Récompenser",
                                                                         "Vendre → Vendre plus → Vendre mieux", "Commander → Ranger → Compter"], "rep": 0,
         "explication": "Le manager passe de l’exemple (faire) à la délégation contrôlée (faire faire) puis au développement de l’équipe (faire grandir)."},
        {"q": "Dans la méthode STAR, le « A » signifie :", "choix": ["Analyse", "Action : ce que j’ai fait moi-même", "Avis du manager", "Atout"], "rep": 1,
         "explication": "Situation, Tâche, Action, Résultat. Le jury et les recruteurs veulent VOS actions concrètes."},
        {"q": "Avant de soumettre son CV à une IA, il faut :", "choix": ["Ajouter son numéro de sécurité sociale", "L’anonymiser (nom, adresse, téléphone)",
                                                                       "Le traduire en anglais", "Rien de particulier"], "rep": 1,
         "explication": "Principe de minimisation du RGPD (art. 5) : ne transmettre que le nécessaire."},
        {"q": "Un logiciel d’IA qui trie automatiquement les CV d’un employeur est classé par l’IA Act comme :", "choix": ["à risque minimal", "interdit",
                                                                                                                          "à haut risque", "non concerné"], "rep": 2,
         "explication": "Règlement (UE) 2024/1689, annexe III, point 4 : le recrutement est un domaine « à haut risque », avec contrôle humain obligatoire."},
    ],
    "deroule": [
        ("8 h 00 – 8 h 20", "Accueil et brise-glace", "Se présenter dans le langage du commerce (Bloom 1)",
         "Accueil, règles du groupe, horaires et pauses ; tour de table « un bon manager, c’est… » ; tableau motive / démotive",
         "Interrogative · enactif", "Diapos 1-2, tableau", "Participation orale"),
        ("8 h 20 – 8 h 40", "Brise-glace « mon ticket de caisse »", "Valoriser son expérience (Bloom 2)",
         "Chacun dessine son ticket : 3 qualités, 1 expérience, 1 objectif ; présentation 30 s", "Active · enactif", "Diapo 3, feuilles A4", "Observation"),
        ("8 h 40 – 9 h 25", "S1 · Le métier en vrai", "Citer les 3 AT et 10 compétences ; distinguer MEM / REM (Bloom 1-2)",
         "Définition, tension du marché, 3 blocs, AT1-AT2-AT3, MEM vs REM ; journée de Nadia : les apprenants classent chaque moment par AT",
         "Expositive participative · iconique", "Diapos 4-13, ressource §1-3", "Questions orales"),
        ("9 h 25 – 10 h 00", "S1 · Jeu « Vrai ou Faux »", "Vérifier la compréhension (Bloom 2)",
         "8 affirmations, cartons vert/rouge (✔ / ✖), justification en 1 phrase", "Ludique · enactif", "Diapo 14, cartons", "Formative : taux de bonnes réponses"),
        ("10 h 00 – 10 h 10", "Pause", "", "", "", "", ""),
        ("10 h 10 – 10 h 50", "S2 · Enjeux et posture", "Expliquer les enjeux 2026 et la posture attendue (Bloom 2)",
         "6 enjeux du REAC avec exemples péi ; faire / faire faire / faire grandir ; 4 piliers (retour sur le tableau du brise-glace) ; ni copain ni petit chef",
         "Expositive + interrogative · iconique", "Diapos 15-19, ressource §4-5", "Questions orales"),
        ("10 h 50 – 11 h 35", "S2 · Jeu de rôle « promu demain »", "Adopter une posture adaptée (Bloom 3)",
         "Trios : manager / collègue vexée / observateur ; 3 rotations de 10 min + 5 min de débriefing", "Simulation · enactif", "Diapo 20, fiche observateur (4 piliers)",
         "Grille critère 3 (formative)"),
        ("11 h 35 – 12 h 00", "S2 · Synthèse matinée", "Reformuler (Bloom 2)", "Chaque trio partage une bonne pratique ; le formateur complète",
         "Interrogative · symbolique", "Tableau", "Reformulation"),
        ("12 h 00 – 13 h 00", "Pause déjeuner", "", "", "", "", ""),
        ("13 h 00 – 14 h 00", "S3 · L’examen décodé", "Décrire les épreuves et les productions (Bloom 1-2)",
         "Devinette « combien dure l’examen ? » ; 4 épreuves ; 2 dossiers et diaporamas ; 280 h ; ce que regarde le jury ; RGPD des dossiers",
         "Expositive participative · symbolique", "Diapos 21-25, ressource §6", "Questions flash"),
        ("14 h 00 – 14 h 30", "S4 · Méthode de recherche", "Planifier sa recherche (Bloom 3)",
         "5 étapes ; canaux ; spécificité locale (démarche en personne) ; pitch ; STAR ; chacun liste 5 entreprises cibles",
         "Démonstrative · iconique", "Diapos 26-28, ressource §7", "Liste de cibles produite"),
        ("14 h 30 – 14 h 40", "Pause", "", "", "", "", ""),
        ("14 h 40 – 15 h 40", "S4 · Atelier IA « mon pitch de 60 s »", "Analyser une offre ; créer son pitch avec l’IA (Bloom 4-6)",
         "Bons usages de l’IA, R-C-T-F, RGPD et IA Act (10 min) ; décodage d’une offre (10 min) ; pitch avec l’IA puis réécriture (20 min) ; "
         "passage en binôme chronométré (20 min)", "Active · enactif + symbolique", "Diapos 29-32, postes, offres imprimées, ressource §8",
         "Grille critériée complète (formative)"),
        ("15 h 40 – 15 h 55", "Quiz 10 questions", "Évaluer les acquis (Bloom 1-2)", "Quiz individuel puis correction collective",
         "Évaluative", "Quiz apprenant, corrigé", "Sommative : objectif 7/10"),
        ("15 h 55 – 16 h 00", "Bilan et engagement", "S’engager dans une action (Bloom 3)", "À retenir ; post-it « d’ici lundi, je fais… » ; annonce du 16/11",
         "Réflexive", "Diapos 34-35, post-it", "Engagement écrit"),
    ],
}
