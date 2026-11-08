from aides import cartes, encadre, flux, tableau

J = {
    "num": 6,
    "date": "Lundi 14 décembre 2026",
    "date_court": "2026-12-14",
    "titre": "Les règles du jeu du manager : droit du travail, sécurité, RSE, RGPD et IA — bilan et cap sur l’AT1",
    "objectif_general": "Connaître le cadre réglementaire que le manager de proximité applique au quotidien (temps de travail, santé-sécurité, "
                        "non-discrimination, RSE, données personnelles, IA), savoir où s’arrête sa responsabilité, et préparer le démarrage de l’AT1.",
    "objectifs": [
        ("Se rappeler (Bloom 1)", "citer les principales limites légales du temps de travail utiles pour bâtir un planning"),
        ("Comprendre (Bloom 2)", "expliquer l’obligation de sécurité, le DUERP et les principes de prévention"),
        ("Appliquer (Bloom 3)", "vérifier la conformité d’un planning hebdomadaire et corriger les anomalies"),
        ("Analyser (Bloom 4)", "identifier dans des situations de magasin ce qui relève du RGPD, de l’IA Act, de la RSE ou de la discrimination"),
        ("Évaluer (Bloom 5)", "faire le bilan de ses acquis des 6 lundis et fixer son plan de préparation de l’AT1"),
    ],
    "lien_reac": "Compétence transversale « Respecter des règles et des procédures » (limites de sa responsabilité, politique RH, RSE, "
                 "maîtrise des risques professionnels). AT1 : Planifier et coordonner l’activité (réglementation : temps de pause, repos, "
                 "durée maximale, travail de nuit — RC/RE dossier AT1). AT2 : expérience client accessible ; vrac, anti-gaspillage.",
    "prerequis": "J1 à J5. Apporter si possible un planning (anonymisé) de son magasin.",
    "materiel": "Vidéoprojecteur ; planning fictif imprimé (ressource §2) ; cartes « situations » du jeu « Qui est concerné ? » ; cartons "
                "RGPD / IA Act / RSE / Discrimination / Sécurité ; feuilles de bilan ; post-it.",
    "progression": "Enactif : chasse aux erreurs dans un planning et jeu « Qui est concerné ? » → Iconique : frise des repos, pyramide de la "
                   "prévention, carte des 5 cadres → Symbolique : articles de loi et vocabulaire → retour enactif : bilan personnel et "
                   "plan de préparation de l’AT1. Fin de la spirale de préparation : équipe, commerce, chiffres, communication, méthode, règles.",
    "slides": [
        {"type": "couverture", "titre": "Les règles du jeu", "sous_titre": "Droit · Sécurité · RSE · RGPD · IA", "date": "Lundi 14 décembre 2026",
         "notes": "Dernier lundi avant les fêtes. Retour sur la première page du carnet de bord. Annoncer : ce matin les règles, cet "
                  "après-midi le bilan et le cap sur l’AT1 en janvier."},
        {"type": "question", "titre": "Pour commencer", "texte": "Un manager peut-il\nrefuser une pause ?", "notes":
         "Vote, puis réponse : NON, si le salarié travaille 6 heures, il a droit à 20 minutes de pause au minimum (Code du travail, "
         "art. L3121-16), sauf dispositions conventionnelles plus favorables. Le manager organise les pauses, il ne les supprime pas. "
         "Message : le manager applique des règles qu’il ne fixe pas, et les connaître le protège autant qu’elles protègent l’équipe."},
        {"type": "cartes", "titre": "5 cadres à respecter", "items": [
            ("Travail", "temps, repos"), ("Sécurité", "prévention"), ("Égalité", "zéro discrimination"), ("RSE", "vrac, anti-gaspi"), ("Données", "RGPD, IA")],
         "notes": "Le REAC : « respecter les limites de sa responsabilité, la politique RH, la démarche RSE et les consignes de sa "
                  "hiérarchie ; mettre en œuvre une démarche de maîtrise des risques professionnels ». Le MEM n’est pas juriste : il "
                  "connaît l’essentiel, applique les procédures et alerte quand il a un doute (RH, direction)."},
        {"type": "section", "num": "01", "titre": "Le temps de travail", "sous_titre": "Ce qu’un planning doit respecter", "notes": ""},
        {"type": "cartes", "titre": "Les repères du planning", "items": [
            ("35 h", "durée légale / semaine"), ("10 h", "max par jour"), ("48 h", "max par semaine"), ("20 min", "pause dès 6 h")],
         "notes": "Code du travail : durée légale 35 h (L3121-27) — au-delà, heures supplémentaires ; durée quotidienne maximale 10 h "
                  "(L3121-18) ; durée hebdomadaire maximale 48 h (L3121-20) et 44 h en moyenne sur 12 semaines (L3121-22) ; pause de 20 "
                  "minutes dès 6 h de travail (L3121-16). La convention collective (pour l’alimentaire : IDCC 2216) et les accords "
                  "d’entreprise peuvent prévoir plus favorable : le manager suit les règles de SON entreprise."},
        {"type": "cartes", "titre": "Les repos obligatoires", "items": [("11 h", "entre 2 journées"), ("35 h", "repos hebdo d’affilée")], "t_titre": 44, "t_texte": 30,
         "notes": "Repos quotidien : 11 heures consécutives minimum (L3131-1). Repos hebdomadaire : 24 heures + les 11 heures de repos "
                  "quotidien, soit 35 heures consécutives (L3132-2). Piège classique : fermeture à 21 h le samedi, ouverture à 7 h le "
                  "dimanche = 10 h de repos seulement : interdit. Jeunes de moins de 18 ans : règles plus strictes (repos de 12 h, pas de "
                  "travail de nuit) : toujours vérifier avec les RH."},
        {"type": "activite", "titre": "Chasse aux erreurs : planning", "genre": "Binômes", "duree": "35 min",
         "items": ["Planning de 6 personnes", "5 erreurs cachées", "Je corrige, j’explique"], "notes":
         "Planning fictif de la ressource §2. Erreurs à trouver : 1) Collaborateur A : 21 h → 7 h le lendemain (repos 10 h < 11 h). "
         "2) Collaboratrice B : 8 h – 19 h sans pause notée (11 h > 10 h max et pause manquante). 3) Collaborateur C (apprenti de 17 ans) "
         "jusqu’à 22 h 30 (travail de nuit des mineurs interdit sauf dérogations). 4) Collaboratrice D : 50 h dans la semaine (> 48 h). "
         "5) Collaborateur E : pas de jour de repos sur 7 jours. Chaque correction doit être réaliste (qui remplace ?). C’est l’exercice "
         "type du dossier AT1 et des questions du jury."},
        {"type": "section", "num": "02", "titre": "Santé et sécurité", "sous_titre": "Prévenir plutôt que guérir", "notes": "Pause de 10 minutes vers 10 h."},
        {"type": "chiffre", "titre": "L’obligation de l’employeur", "valeur": "Sécurité", "legende": "physique et mentale des salariés",
         "source": "Code du travail, art. L4121-1", "notes":
         "L’employeur doit assurer la sécurité et protéger la santé physique et mentale des travailleurs. Le manager de proximité, par "
         "délégation, applique et fait appliquer les mesures : il est en première ligne. Le DUERP (document unique d’évaluation des "
         "risques professionnels, art. R4121-1) recense les risques de chaque unité de travail : le manager doit connaître ceux de son "
         "périmètre et faire remonter les nouveaux."},
        {"type": "cartes", "titre": "Les risques du magasin", "items": [
            ("Charges", "port, palettes"), ("Chutes", "sol, escabeau"), ("Chaleur", "réserve, quais"), ("Coupures", "cutter, verre"), ("Agressions", "incivilités"), ("Stress", "rush, pression")],
         "notes": "Exemples péi : réserve non climatisée à 38 °C en janvier ; sol mouillé après une averse tropicale à l’entrée ; afflux "
                  "massif avant un cyclone ; incivilités en caisse. Mesures : formation gestes et postures, transpalette électrique, "
                  "rotation des tâches, eau à disposition, procédure en cas d’agression, écoute de l’équipe."},
        {"type": "etapes", "titre": "Prévenir en 3 niveaux", "items": [("Supprimer", "le risque"), ("Protéger", "collectif d’abord"), ("Former", "informer")],
         "notes": "Simplification des 9 principes généraux de prévention (L4121-2) : éviter le risque, le combattre à la source, adapter "
                  "le travail à l’homme, privilégier la protection collective (rambarde, chariot) sur l’individuelle (gants, chaussures), "
                  "donner des instructions. Exemple : plutôt que de demander de « faire attention » en montant sur un escabeau, ranger les "
                  "produits lourds en bas."},
        {"type": "section", "num": "03", "titre": "Égalité et RSE", "sous_titre": "Un commerce juste et responsable", "notes": ""},
        {"type": "puces", "titre": "Non-discrimination", "items": ["Recrutement", "Planning, promotions", "Remarques, blagues", "Accueil des clients"],
         "notes": "Code du travail, art. L1132-1 : aucune décision fondée sur l’origine, le sexe, l’âge, la situation de famille, la "
                  "grossesse, l’état de santé, le handicap, les convictions religieuses, l’apparence physique, le lieu de résidence, la "
                  "domiciliation bancaire, la langue… (plus de 25 critères). Au magasin : pas de « pas de femme en réserve », pas de "
                  "planning défavorable à cause de la religion, pas de moqueries. Accueil des clients en situation de handicap : loi du "
                  "11 février 2005 (accessibilité des établissements recevant du public)."},
        {"type": "cartes", "titre": "La RSE au rayon", "items": [("Anti-gaspi", "dons, promos DLC"), ("Vrac", "20 % en 2030"), ("Réemploi", "consigne, occasion"), ("Local", "produits péi")],
         "notes": "Loi AGEC (n° 2020-105 du 10 février 2020) : lutte contre le gaspillage, interdiction de détruire les invendus non "
                  "alimentaires (dons, recyclage). Loi Climat et résilience (n° 2021-1104) : les commerces de plus de 400 m² devront "
                  "consacrer environ 20 % de leur surface de vente de produits de grande consommation au vrac d’ici 2030 (vérifier "
                  "les décrets d’application). Dons alimentaires aux associations (grandes surfaces > 400 m²). À La Réunion : mettre en "
                  "avant la production locale (circuits courts, moins de fret)."},
        {"type": "section", "num": "04", "titre": "Données et IA", "sous_titre": "RGPD et IA Act au magasin", "notes": "Après le déjeuner."},
        {"type": "cartes", "titre": "Le RGPD au magasin", "items": [("Fidélité", "fichier clients"), ("Caméras", "affichage, 30 j"), ("Salariés", "dossiers, plannings"), ("Mails", "confidentialité")],
         "notes": "Toute information qui identifie une personne est une donnée personnelle. Le manager : collecte le minimum (carte "
                  "fidélité : pas besoin de la profession), ne partage pas (pas de photo d’un client « voleur » sur WhatsApp), sécurise "
                  "(pas de mot de passe sur un post-it), respecte les durées. Vidéoprotection : information des personnes par panneau, "
                  "conservation limitée (en principe 1 mois maximum pour les images de lieux ouverts au public), accès réservé. En cas de "
                  "fuite (vol d’un ordinateur, mail envoyé au mauvais destinataire) : alerter immédiatement la hiérarchie (notification "
                  "à la CNIL sous 72 h, art. 33)."},
        {"type": "cartes", "titre": "L’IA Act au magasin", "items": [("Interdit", "émotions au travail"), ("Haut risque", "tri des CV"), ("Transparence", "chatbot signalé"), ("Former", "art. 4")],
         "notes": "Règlement (UE) 2024/1689. Interdit depuis le 2 février 2025 : la reconnaissance des émotions sur le lieu de travail "
                  "(caméra qui « mesure » le sourire des caissières), la notation sociale (art. 5). Haut risque : IA de recrutement, "
                  "d’évaluation ou de répartition des tâches des salariés (annexe III, point 4) : contrôle humain obligatoire ; le "
                  "calendrier de ces obligations est en cours de révision au niveau européen (proposition « omnibus numérique ») : "
                  "vérifier la date applicable. Transparence (art. 50) : un client doit savoir qu’il parle à un chatbot. Maîtrise de "
                  "l’IA (art. 4) : les équipes qui utilisent l’IA doivent y être formées. Le MEM : n’installe aucun outil d’IA sans "
                  "validation, signale les usages douteux."},
        {"type": "activite", "titre": "Jeu : qui est concerné ?", "genre": "Équipes · 5 cartons", "duree": "30 min",
         "items": ["J’écoute la situation", "Je lève le bon carton", "Je dis quoi faire"], "notes":
         "Cartons : DROIT DU TRAVAIL / SÉCURITÉ / DISCRIMINATION / RSE / RGPD-IA (plusieurs réponses possibles). Situations : 1) Un "
         "collègue publie la photo d’un client pris en train de voler (RGPD). 2) Un fournisseur propose une caméra qui note l’humeur des "
         "vendeurs (IA Act, interdit). 3) Un manager écarte une candidate « parce qu’elle a des enfants » (discrimination). 4) 200 "
         "yaourts arrivent à DLC demain (RSE : promo, don). 5) Un apprenti de 16 ans sur un escabeau à 2 m de haut (sécurité + règles "
         "jeunes travailleurs). 6) Le site du magasin propose un chat automatisé sans le dire (IA Act, transparence). 7) Le planning de "
         "Noël prévoit 11 h de travail le 24 décembre (droit du travail). 8) Une cliente en fauteuil ne peut pas accéder à la caisse "
         "rapide (accessibilité). Pour chaque situation : la bonne réaction du MEM et la limite de son rôle."},
        {"type": "section", "num": "05", "titre": "Bilan et cap sur l’AT1", "sous_titre": "Rendez-vous en janvier", "notes": "Pause de 10 minutes vers 14 h 30."},
        {"type": "cartes", "titre": "6 lundis, 6 piliers", "items": [
            ("Métier", "9/11"), ("Outils", "16/11"), ("Chiffres", "23/11"), ("Communiquer", "30/11"), ("Méthodes", "7/12"), ("Règles", "14/12")],
         "notes": "Retour sur la spirale : chaque lundi a posé une brique que l’on retrouve dans les trois activités-types. Faire dire à "
                  "chacun, pour chaque pilier, une chose retenue."},
        {"type": "activite", "titre": "Mon bilan personnel", "genre": "Individuel puis tour de table", "duree": "30 min",
         "items": ["Je me positionne de 1 à 4", "Mes 2 forces", "Mes 2 priorités"], "notes":
         "Feuille de bilan (ressource §6) : autopositionnement sur les 6 thèmes, deux forces, deux priorités de travail pendant les "
         "vacances. Le formateur recueille les feuilles pour adapter le démarrage de l’AT1 (données à conserver dans le dossier de "
         "formation, pas ailleurs : RGPD)."},
        {"type": "puces", "titre": "Pour janvier : AT1", "items": ["Organigramme de l’équipe", "Un planning anonymisé", "Un briefing observé", "Carnet de bord à jour"],
         "notes": "L’AT1 « Manager l’équipe de son périmètre » démarre le 4 ou le 11 janvier 2027. Documents à rapporter (avec l’accord "
                  "du tuteur, anonymisés) : organigramme (fonctions), planning d’une semaine, trame d’un briefing observé, fiche de poste "
                  "d’un collaborateur, procédure d’accueil d’un nouveau si elle existe. Ce sont les matériaux du dossier AT1 (16 à 24 pages)."},
        {"type": "activite", "titre": "Quiz : 10 questions", "genre": "Individuel", "duree": "15 min", "items": ["10 questions", "Correction ensemble", "Objectif : 7 / 10"], "notes": ""},
        {"type": "puces", "titre": "À retenir", "items": ["11 h de repos, 20 min de pause", "Prévenir avant tout", "Aucune discrimination", "Données : le minimum"],
         "notes": "Remercier le groupe. Bonnes fêtes. Rappeler la date de reprise."},
        {"type": "question", "titre": "Mon engagement", "texte": "Pendant les vacances,\nje prépare…", "notes":
         "Post-it final à conserver et relire à la reprise en janvier."},
    ],
    "ressource": [
        ("Le manager et les règles : où s’arrête ma responsabilité ?",
         "<p>Le MEM applique des règles qu’il ne fixe pas : la loi, la convention collective, les accords et procédures de l’entreprise, "
         "les consignes de sa hiérarchie. Il les fait respecter dans son périmètre et <b>alerte</b> dès qu’un doute ou une difficulté "
         "dépasse son rôle (RH, direction, service sécurité).</p>"
         + cartes([("Droit du travail", "temps de travail, repos, pauses"), ("Santé-sécurité", "prévention des risques"), ("Égalité", "non-discrimination, handicap"),
                   ("RSE", "anti-gaspillage, vrac, local"), ("Données", "RGPD et IA Act")], "Les 5 cadres du manager", cols=3)
         + encadre("jury", "<p>Au dossier AT1, le RC/RE demande de préciser comment vous prenez en compte la réglementation dans vos "
                   "plannings (temps de pause, repos, durée maximale, travail de nuit…).</p>")),
        ("Le temps de travail : les repères du planning",
         tableau(["Règle", "Repère", "Référence"], [
             ["Durée légale", "35 h par semaine (au-delà : heures supplémentaires)", "Code du travail L3121-27"],
             ["Durée maximale quotidienne", "10 h", "L3121-18"],
             ["Durée maximale hebdomadaire", "48 h sur une semaine ; 44 h en moyenne sur 12 semaines", "L3121-20 et L3121-22"],
             ["Pause", "20 minutes consécutives dès 6 h de travail", "L3121-16"],
             ["Repos quotidien", "11 h consécutives entre deux journées", "L3131-1"],
             ["Repos hebdomadaire", "24 h + 11 h = 35 h consécutives", "L3132-2"],
             ["Jeunes de moins de 18 ans", "Règles renforcées : durées plus courtes, repos plus longs, travail de nuit interdit sauf dérogations", "L3162-1 et suivants"]])
         + encadre("piege", "<p>Fermeture à 21 h, ouverture à 7 h le lendemain : seulement 10 h de repos. <b>Interdit.</b></p>")
         + "<h3>Planning d’exercice (5 erreurs à trouver)</h3>"
         + tableau(["Collaborateur", "Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"], [
             ["A", "13 h – 21 h", "7 h – 14 h", "Repos", "13 h – 20 h", "13 h – 20 h", "13 h – 21 h", "Repos"],
             ["B", "8 h – 19 h", "Repos", "8 h – 15 h", "8 h – 15 h", "Repos", "8 h – 15 h", "Repos"],
             ["C (apprenti, 17 ans)", "École", "École", "14 h – 19 h", "Repos", "15 h – 22 h 30", "9 h – 16 h", "Repos"],
             ["D", "7 h – 16 h", "7 h – 16 h", "7 h – 16 h", "7 h – 16 h", "7 h – 16 h", "7 h – 12 h", "Repos"],
             ["E", "9 h – 13 h", "9 h – 13 h", "9 h – 13 h", "9 h – 13 h", "9 h – 13 h", "9 h – 13 h", "9 h – 13 h"]])
         + "<p class='petit'>Lecture : les horaires indiqués correspondent au temps de travail effectif (pause déjeuner hors de ces plages). Solutions : A (lundi 21 h → mardi 7 h : 10 h de repos au lieu de 11 h) ; B (11 h de travail le lundi : au-delà de 10 h, et pause de 20 min non prévue) ; C (mineur jusqu’à 22 h 30 : travail de nuit interdit) ; D (5 × 9 h + 5 h = 50 h : au-delà de 48 h) ; E (aucun jour de repos sur 7 jours).</p>"
         + encadre("retenir", "<p>Votre convention collective et les accords d’entreprise peuvent être plus favorables : appliquez toujours "
                   "les règles de votre entreprise et demandez aux RH en cas de doute.</p>")),
        ("Santé et sécurité au travail",
         "<p>L’employeur doit assurer la sécurité et protéger la santé <b>physique et mentale</b> des salariés (Code du travail, art. "
         "L4121-1). Le manager de proximité applique et fait appliquer les mesures de prévention et fait remonter les risques nouveaux. "
         "Les risques sont recensés dans le <b>DUERP</b> (document unique d’évaluation des risques professionnels, art. R4121-1).</p>"
         + tableau(["Risque au magasin", "Exemple péi", "Mesures de prévention"], [
             ["Port de charges", "Packs d’eau avant un cyclone", "Transpalette, gestes et postures, rotation des tâches"],
             ["Chutes", "Sol mouillé après une averse à l’entrée", "Tapis, signalisation, nettoyage immédiat"],
             ["Chaleur", "Réserve à 38 °C en janvier", "Ventilation, eau, horaires adaptés, pauses"],
             ["Coupures", "Ouverture des cartons au cutter", "Cutters de sécurité, gants, formation"],
             ["Agressions, incivilités", "Tension en caisse un samedi", "Procédure, binôme, soutien après incident"],
             ["Risques psychosociaux", "Rush des fêtes, pression des objectifs", "Écoute, charge de travail réaliste, reconnaissance"]])
         + flux([("Supprimer", "éviter le risque à la source"), ("Protéger", "collectif avant individuel"), ("Former", "consignes, formation, affichage")],
                "Les principes de prévention (L4121-2), simplifiés")),
        ("Égalité, inclusion et RSE",
         "<h3>Non-discrimination</h3><p>Aucune décision (recrutement, planning, formation, promotion, sanction) ne peut se fonder sur l’un "
         "des critères interdits par l’article L1132-1 du Code du travail : origine, sexe, âge, situation de famille, grossesse, état de "
         "santé, handicap, convictions religieuses, apparence physique, lieu de résidence, langue, etc.</p>"
         + encadre("ex", "<p>« Je ne prends pas de jeunes de tel quartier » ou « Pas de femme en réserve » : discrimination. "
                   "Le manager juge les compétences et les comportements, jamais les personnes pour ce qu’elles sont.</p>")
         + "<h3>Accessibilité</h3><p>La loi n° 2005-102 du 11 février 2005 impose l’accessibilité des établissements recevant du public. "
           "Au rayon : allées dégagées, produits atteignables, caisse adaptée, accueil bienveillant. C’est aussi l’« expérience client » de l’AT2.</p>"
         + "<h3>RSE au quotidien</h3>"
         + tableau(["Thème", "Repère", "Action du MEM"], [
             ["Anti-gaspillage", "Loi AGEC n° 2020-105 ; dons alimentaires (surfaces > 400 m²)", "Promotions DLC courte, dons aux associations, commandes ajustées"],
             ["Vrac", "Loi Climat et résilience n° 2021-1104 : objectif d’environ 20 % de la surface en vrac en 2030 (> 400 m²)", "Hygiène, traçabilité, conseil client"],
             ["Réemploi", "Consigne, seconde main", "Mise en avant, information client"],
             ["Local", "Produits péi, circuits courts", "Implantation visible, partenariats producteurs"]])),
        ("Données personnelles et intelligence artificielle",
         tableau(["Situation", "Cadre", "Bon réflexe"], [
             ["Fichier fidélité", "RGPD : minimisation (art. 5), information (art. 13)", "Ne demander que l’utile ; ne jamais exporter sur une clé personnelle"],
             ["Vidéoprotection", "RGPD + Code de la sécurité intérieure", "Panneau d’information, accès réservé, conservation limitée (en principe 1 mois max)"],
             ["Photo d’un client « voleur » partagée", "RGPD, droit à l’image", "Interdit : on passe par la procédure (sécurité, direction, police)"],
             ["Fuite de données (mail au mauvais destinataire)", "RGPD art. 33 : notification à la CNIL sous 72 h", "Alerter immédiatement sa hiérarchie"],
             ["Caméra qui « mesure » les émotions des vendeurs", "IA Act art. 5 : interdit depuis le 2/02/2025", "Refuser, alerter"],
             ["IA qui trie les CV ou évalue les salariés", "IA Act annexe III, point 4 : haut risque", "Contrôle humain ; calendrier en révision, vérifier la date applicable"],
             ["Chatbot sur le site du magasin", "IA Act art. 50 : transparence", "Le client doit savoir qu’il parle à une machine"],
             ["Équipe qui utilise une IA", "IA Act art. 4 : maîtrise de l’IA", "Former, fixer des règles d’usage, jamais de données personnelles"]])
         + encadre("loi", "<p><b>RGPD</b> = règlement (UE) 2016/679, contrôlé en France par la CNIL. <b>IA Act</b> = règlement (UE) "
                   "2024/1689, appliqué par étapes depuis 2025. Le MEM n’est pas responsable juridique du traitement, mais il est le "
                   "premier à voir les mauvaises pratiques : il les signale.</p>")),
        ("Bilan des 6 lundis et préparation de l’AT1",
         tableau(["Lundi", "Thème", "Je me positionne (1 à 4)", "Ce que je retiens"], [
             ["9/11", "Le métier, la posture, l’examen, la recherche de poste", "", ""], ["16/11", "Word, Excel, PowerPoint", "", ""],
             ["23/11", "Prix, marges, indicateurs", "", ""], ["30/11", "Communication du manager", "", ""],
             ["7/12", "Organisation et résolution de problème", "", ""], ["14/12", "Règles : travail, sécurité, RSE, RGPD, IA", "", ""]])
         + "<p><b>Mes 2 forces :</b> ……………………………………………………… <br><b>Mes 2 priorités pendant les vacances :</b> ………………………………………</p>"
         + "<h3>À rapporter en janvier pour l’AT1 (avec l’accord du tuteur, anonymisé)</h3>"
         "<ul><li>Organigramme de l’équipe (fonctions, pas de noms)</li><li>Un planning d’une semaine</li><li>La trame d’un briefing observé</li>"
         "<li>Une fiche de poste</li><li>La procédure d’accueil d’un nouveau collaborateur, si elle existe</li><li>Le carnet de bord à jour</li></ul>"),
    ],
    "sources": [
        "Code du travail, articles L3121-16, L3121-18, L3121-20, L3121-22, L3121-27, L3131-1, L3132-2, L3162-1, L4121-1, L4121-2, R4121-1, L1132-1 — legifrance.gouv.fr.",
        "Loi n° 2005-102 du 11 février 2005 (handicap, accessibilité) ; loi n° 2020-105 du 10 février 2020 (AGEC) ; loi n° 2021-1104 du 22 août 2021 (Climat et résilience) — legifrance.gouv.fr.",
        "Règlement (UE) 2016/679 (RGPD), articles 5, 13 et 33 ; CNIL, fiches pratiques « vidéoprotection » — cnil.fr.",
        "Règlement (UE) 2024/1689 (IA Act), articles 4, 5, 50 et annexe III — eur-lex.europa.eu ; proposition « omnibus numérique » de la Commission européenne (novembre 2025) : état d’adoption à vérifier.",
        "REAC et RC/RE MEM v09 (pièces jointes). Convention collective du commerce de détail et de gros à prédominance alimentaire (IDCC 2216), à adapter selon l’entreprise.",
    ],
    "grille": {
        "situation": "Chasse aux erreurs dans un planning, jeu « Qui est concerné ? » et bilan personnel des 6 lundis.",
        "criteres": [
            {"critere": "Règles du temps de travail", "indicateurs": ["Repère les 5 erreurs du planning", "Cite la règle correspondante"],
             "niveaux": ["0 à 1 erreur trouvée", "2 à 3 erreurs", "5 erreurs, règles citées", "5 erreurs + corrections réalistes (remplacements)"]},
            {"critere": "Santé et sécurité", "indicateurs": ["Identifie les risques de son périmètre", "Propose une mesure de prévention adaptée"],
             "niveaux": ["Risques ignorés", "Risques cités sans mesure", "Risques et mesures adaptés", "Priorise la protection collective, connaît le DUERP"]},
            {"critere": "Égalité et RSE", "indicateurs": ["Repère une discrimination", "Propose une action RSE concrète"],
             "niveaux": ["Ne repère pas", "Repère sans réagir", "Repère et réagit", "Réagit et explique le cadre légal"]},
            {"critere": "RGPD et IA Act", "indicateurs": ["Classe correctement les situations", "Indique le bon réflexe et la limite de son rôle"],
             "niveaux": ["Confusions", "Classement partiel", "Classement et réflexes justes", "Justes, avec la référence et l’alerte à la hiérarchie"]},
            {"critere": "Bilan et projet", "indicateurs": ["Autopositionnement argumenté", "Plan de préparation de l’AT1"],
             "niveaux": ["Non fait", "Superficiel", "Argumenté, priorités claires", "Argumenté, plan daté, documents identifiés"]},
        ]},
    "quiz": [
        {"q": "Dès combien d’heures de travail un salarié a-t-il droit à 20 minutes de pause ?", "choix": ["4 h", "5 h", "6 h", "8 h"], "rep": 2,
         "explication": "Code du travail, art. L3121-16 : 20 minutes consécutives dès 6 heures."},
        {"q": "Le repos quotidien minimal entre deux journées de travail est de :", "choix": ["8 h", "10 h", "11 h", "12 h"], "rep": 2, "explication": "Art. L3131-1 : 11 heures consécutives."},
        {"q": "La durée maximale de travail sur une journée est en principe de :", "choix": ["8 h", "10 h", "12 h", "Pas de limite"], "rep": 1, "explication": "Art. L3121-18 : 10 heures."},
        {"q": "Le document qui recense les risques professionnels de l’entreprise s’appelle :", "choix": ["le DUERP", "le RGPD", "le REAC", "le PDCA"], "rep": 0,
         "explication": "Document unique d’évaluation des risques professionnels (art. R4121-1)."},
        {"q": "En prévention, on privilégie :", "choix": ["la protection individuelle", "la protection collective", "la sanction", "la chance"], "rep": 1,
         "explication": "Les principes généraux de prévention font passer la protection collective avant l’individuelle."},
        {"q": "Refuser une candidate parce qu’elle a des enfants, c’est :", "choix": ["un choix d’organisation", "une discrimination", "autorisé en commerce", "un critère de compétence"], "rep": 1,
         "explication": "La situation de famille est un critère interdit (art. L1132-1)."},
        {"q": "Quelle loi de 2020 lutte contre le gaspillage et la destruction des invendus ?", "choix": ["La loi AGEC", "La loi Evin", "La loi Hamon", "La loi Macron"], "rep": 0,
         "explication": "Loi anti-gaspillage pour une économie circulaire (AGEC), n° 2020-105."},
        {"q": "Un collègue publie sur un groupe WhatsApp la photo d’un client soupçonné de vol. C’est :", "choix": ["autorisé pour prévenir", "une atteinte au RGPD et au droit à l’image",
                                                                                                       "obligatoire", "sans conséquence"], "rep": 1,
         "explication": "On passe par la procédure interne (sécurité, direction, forces de l’ordre)."},
        {"q": "Une caméra qui « mesure » les émotions des vendeurs au travail est, selon l’IA Act :", "choix": ["autorisée", "à haut risque", "interdite", "à risque minimal"], "rep": 2,
         "explication": "Article 5 : la reconnaissance des émotions sur le lieu de travail est interdite depuis le 2 février 2025."},
        {"q": "En cas de fuite de données personnelles, le MEM doit d’abord :", "choix": ["ne rien dire", "alerter immédiatement sa hiérarchie", "supprimer les traces", "prévenir la presse"], "rep": 1,
         "explication": "L’entreprise doit notifier la CNIL sous 72 h (RGPD, art. 33) : chaque heure compte."},
    ],
    "deroule": [
        ("8 h 00 – 8 h 20", "Accueil et question d’ouverture", "Mobiliser (Bloom 1)", "Carnet de bord ; « peut-on refuser une pause ? » ; 5 cadres",
         "Interrogative · symbolique", "Diapos 1-3", "Vote"),
        ("8 h 20 – 8 h 50", "S1 · Le temps de travail", "Citer les repères (Bloom 1-2)", "Durées, pauses, repos, jeunes travailleurs, convention collective",
         "Expositive · iconique", "Diapos 4-6, ressource §2", "Questions"),
        ("8 h 50 – 10 h 00", "S1 · Chasse aux erreurs", "Vérifier un planning (Bloom 3)", "Binômes : 5 erreurs, corrections réalistes ; correction collective",
         "Active · enactif", "Diapo 7, planning imprimé", "Grille critère 1"),
        ("10 h 00 – 10 h 10", "Pause", "", "", "", "", ""),
        ("10 h 10 – 11 h 10", "S2 · Santé et sécurité", "Expliquer la prévention (Bloom 2)",
         "Obligation de sécurité, DUERP ; risques du magasin (exemples péi, échanges d’expériences) ; 3 niveaux de prévention ; chaque apprenant liste 3 risques de son périmètre",
         "Expositive participative · iconique", "Diapos 8-11, ressource §3", "Grille critère 2"),
        ("11 h 10 – 12 h 00", "S3 · Égalité, accessibilité, RSE", "Repérer et réagir (Bloom 3-4)", "Critères de discrimination ; accessibilité ; AGEC, vrac, local ; mini-débat",
         "Interrogative · symbolique", "Diapos 12-14, ressource §4", "Grille critère 3"),
        ("12 h 00 – 13 h 00", "Pause déjeuner", "", "", "", "", ""),
        ("13 h 00 – 13 h 40", "S4 · RGPD et IA Act au magasin", "Comprendre les obligations (Bloom 2)", "Fidélité, caméras, fuite, WhatsApp ; IA interdite, haut risque, transparence, formation",
         "Expositive · iconique", "Diapos 15-17, ressource §5", "Questions"),
        ("13 h 40 – 14 h 30", "S4 · Jeu « Qui est concerné ? »", "Analyser des situations (Bloom 4)", "8 situations, 5 cartons, bonne réaction et limite du rôle",
         "Ludique · enactif", "Diapo 18, cartons", "Grille critère 4"),
        ("14 h 30 – 14 h 40", "Pause", "", "", "", "", ""),
        ("14 h 40 – 15 h 35", "S5 · Bilan et cap sur l’AT1", "Évaluer ses acquis (Bloom 5)", "6 piliers ; bilan individuel ; tour de table ; documents à rapporter en janvier",
         "Réflexive · symbolique", "Diapos 19-22, feuille de bilan", "Grille critère 5"),
        ("15 h 35 – 15 h 55", "Quiz 10 questions", "Évaluer (Bloom 1-2)", "Quiz puis correction", "Évaluative", "Quiz", "Sommative 7/10"),
        ("15 h 55 – 16 h 00", "Clôture", "S’engager (Bloom 3)", "À retenir ; post-it vacances ; date de reprise", "Réflexive", "Diapos 24-25", "Engagement"),
    ],
}
