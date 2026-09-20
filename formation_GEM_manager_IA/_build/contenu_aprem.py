# -*- coding: utf-8 -*-
from deck_engine import *

def construire(prs):
    slide_partie(prs, "PARTIE 2", ["IA et responsabilité", "en entreprise"], "13h30 – 17h00",
        ["Ce qu'est vraiment une IA générative",
         "RGPD : l'essentiel pour un responsable",
         "IA Act : les 4 niveaux de risque",
         "Ce que vous n'avez pas le droit de faire",
         "L'IA qui vous rend du temps"])

    slide_jeu(prs, "5", "Vrai ou faux", "15 min",
        "Réveiller le groupe et mesurer les idées reçues",
        ["Debout, et caméra si vous le pouvez",
         "Vrai : pouce levé. Faux : pouce baissé",
         "Interdit de ne pas répondre",
         "Deux personnes justifient à chaque fois",
         "Je donne la réponse et la source",
         "6 affirmations, rythme rapide"],
        "Aucun. 6 affirmations (kit jeux, fiche J5)")

    # --- A1
    slide_choc(prs, "Une IA générative", "ne sait rien.",
        "Elle calcule ce qui est probable après vos mots.", C_NUIT)

    slide(prs, "Comment ça marche, vraiment",
        [(1, "Elle a lu des milliards de textes"),
         (1, "Elle prédit le mot suivant le plus probable"),
         (1, "Elle n'a ni intention, ni conscience"),
         (1, "Elle n'a aucune idée du vrai et du faux"),
         (2, "Image : un correcteur prédictif très, très entraîné")],
        note="Conséquence directe : elle a toujours l'air sûre d'elle.")

    slide(prs, "Les trois pièges à connaître",
        [(1, "L'hallucination : elle invente, avec aplomb"),
         (2, "Chiffres, articles de loi, noms, citations"),
         (1, "Le biais : elle reproduit ses données"),
         (2, "Un historique d'embauche biaisé se rejoue"),
         (1, "La fuite : ce que vous saisissez peut sortir"),
         (2, "Selon l'outil et son hébergement")],
        note="Règle d'or : aucune donnée que vous n'afficheriez pas en salle de pause.")

    slide(prs, "Le biais, en magasin",
        [(1, "Vous triez 300 CV de saisonniers"),
         (1, "L'outil apprend sur vos embauches passées"),
         (1, "Il reproduit vos préférences d'hier"),
         (2, "Âge, quartier, prénom, durée d'inactivité"),
         (1, "Résultat : une discrimination automatisée")],
        note="Bloc 1 du titre : lutter contre les discriminations. C'est exactement ça.",
        couleur_bandeau=C_ROUGE, etiquette="TP MEM")

    slide_deux_colonnes(prs, "Ce qu'elle fait bien / mal",
        "Confiez-lui", ["Reformuler, résumer", "Structurer un brief",
                        "Traduire, corriger", "Faire 20 variantes",
                        "Préparer un questionnement"],
        "Ne lui confiez pas", ["Un chiffre à vérifier", "Une référence juridique",
                               "Une décision sur une personne", "Un diagnostic humain",
                               "Le dernier mot"],
        g_coul=C_VERT, d_coul=C_ROUGE,
        note="Elle est un stagiaire brillant et amnésique : on relit toujours.")

    # --- A2
    slide_choc(prs, "Vos équipes", "sont des personnes.",
        "Leurs données leur appartiennent. Toujours.", C_ACCENT)

    slide(prs, "RGPD : le minimum vital",
        [(1, "Une finalité précise, dite à l'avance"),
         (1, "Une base légale, pas « j'en ai besoin »"),
         (1, "Le strict nécessaire, rien de plus"),
         (1, "Une durée de conservation décidée"),
         (1, "Des personnes informées, en clair"),
         (2, "Source : Règlement (UE) 2016/679, articles 5 et 6")],
        note="Le consentement du salarié est rarement valable : lien de subordination.")

    slide(prs, "Le réflexe des 4 questions",
        [(1, "Pourquoi je collecte cette donnée ?"),
         (1, "En ai-je vraiment besoin pour ça ?"),
         (1, "Qui y accède, et pourquoi lui ?"),
         (1, "Quand est-ce que je l'efface ?"),
         (2, "Une seule réponse floue = on ne collecte pas")],
        note="30 secondes de réflexe vous évitent 3 mois de contentieux.")

    slide(prs, "Surveiller son équipe : les limites",
        [(1, "Pas de collecte à l'insu des salariés"),
         (2, "Code du travail, article L.1222-4"),
         (1, "Information et consultation du CSE"),
         (2, "Code du travail, article L.2312-38"),
         (1, "Contrôle proportionné au but poursuivi"),
         (2, "Pas de caméra braquée en continu sur une caisse")],
        note="Sources : Légifrance et CNIL, fiches « travail et données » (cnil.fr).",
        couleur_bandeau=C_ROUGE)

    slide(prs, "L'article 22, celui qui piège",
        [(1, "Une décision 100 % automatisée est interdite"),
         (2, "Si l'effet sur la personne est significatif"),
         (1, "Exemples : tri de CV, refus, sanction"),
         (1, "Il faut un humain qui peut dire non"),
         (2, "Un humain qui valide tout n'est pas un humain")],
        note="Source : RGPD, article 22. C'est le pont direct vers l'IA Act.",
        couleur_bandeau=C_ROUGE)

    # --- A3
    slide_choc(prs, "L'IA Act", "ne classe pas les outils.",
        "Il classe les usages que vous en faites.", C_NUIT)

    slide(prs, "IA Act : de quoi parle-t-on",
        [(1, "Règlement (UE) 2024/1689"),
         (1, "En vigueur depuis le 1er août 2024"),
         (1, "Il s'applique par étapes jusqu'en 2027"),
         (1, "Deux rôles : fournisseur et déployeur"),
         (2, "Vous serez presque toujours déployeur")],
        note="Source : Journal officiel de l'UE. Calendrier à revalider régulièrement.")

    slide(prs, "Les quatre niveaux de risque",
        [(1, "Inacceptable : interdit, sans exception"),
         (2, "Émotions au travail, notation sociale"),
         (1, "Haut risque : autorisé, très encadré"),
         (2, "Embauche, promotion, planning, suivi"),
         (1, "Risque limité : obligation de transparence"),
         (2, "Dire que c'est une IA, marquer les contenus"),
         (1, "Risque minimal : usage libre")],
        note="VIDÉO 2 – « La pyramide des risques de l'IA Act » (2 min 55).")

    slide(prs, "Interdit : ce qui vous concerne",
        [(1, "Détecter les émotions des salariés"),
         (2, "Sauf raison médicale ou de sécurité"),
         (1, "Noter socialement les personnes"),
         (1, "Exploiter une vulnérabilité pour influencer"),
         (2, "Source : IA Act, article 5, applicable depuis 2025")],
        note="Une caméra qui mesure le sourire des hôtesses de caisse : interdite.",
        couleur_bandeau=C_ROUGE)

    slide(prs, "Haut risque : le quotidien du MEM",
        [(1, "Trier, filtrer, classer des candidatures"),
         (1, "Évaluer, promouvoir, mettre fin à un contrat"),
         (1, "Bâtir le planning automatiquement"),
         (1, "Suivre et noter la performance vendeur"),
         (2, "Source : IA Act, annexe III, point 4")],
        note="Obligation clé : informer les représentants du personnel avant usage.",
        couleur_bandeau=C_ROUGE)

    slide(prs, "Article 4 : votre obligation",
        [(1, "Former votre personnel à l'IA qu'il utilise"),
         (1, "Niveau adapté au rôle et au risque"),
         (1, "Applicable depuis le 2 février 2025"),
         (1, "Aucune taille d'entreprise exemptée"),
         (2, "Cette journée y contribue : gardez la preuve")],
        note="Source : IA Act, article 4 (littératie en matière d'IA).",
        etiquette="ESSENTIEL")

    slide(prs, "Ce que ça coûte si on ignore",
        [(1, "Pratique interdite : jusqu'à 35 M€"),
         (2, "Ou 7 % du chiffre d'affaires mondial"),
         (1, "Autres manquements : jusqu'à 15 M€"),
         (2, "Ou 3 % du chiffre d'affaires mondial"),
         (1, "RGPD : jusqu'à 20 M€ ou 4 %"),
         (2, "Le plus élevé des deux montants s'applique")],
        note="Le risque réel pour une enseigne : l'image, le contentieux, le CSE.",
        couleur_bandeau=C_ROUGE)

    slide_pause(prs, "Pause", "15 minutes – reprise à 15h30, caméra allumée")

    slide_jeu(prs, "6", "Le tri des risques", "20 min",
        "Savoir classer un usage avant de l'autoriser",
        ["Sous-groupes de 4 en salles séparées",
         "12 usages réels d'un établissement marchand",
         "Classez chacun dans l'un des 4 niveaux",
         "8 minutes, puis retour en plénière",
         "Un groupe défend, un autre conteste",
         "Correction avec l'article applicable"],
        "Salles séparées + fiche J6 (tableau à compléter)")

    # --- A4
    slide_choc(prs, "L'outil n'est jamais", "responsable.",
        "Celui qui l'a mis en service, oui.", C_ACCENT)

    slide(prs, "Vos cinq devoirs de déployeur",
        [(1, "Savoir quel outil fait quoi, chez vous"),
         (1, "Garder un humain qui peut trancher"),
         (1, "Informer les personnes concernées"),
         (1, "Consulter les représentants du personnel"),
         (1, "Tracer : qui a décidé quoi, et quand")],
        note="Source : IA Act, article 26 (obligations des déployeurs).")

    slide(prs, "La supervision humaine réelle",
        [(1, "Avoir le temps de vérifier"),
         (1, "Avoir la compétence pour contredire"),
         (1, "Avoir le droit de ne pas suivre l'IA"),
         (1, "Et que ça n'ait aucune conséquence"),
         (2, "Sinon : supervision de façade, risque maximal")],
        note="Question test : quand avez-vous dit non à l'outil pour la dernière fois ?")

    slide(prs, "Trois réflexes avant de lancer",
        [(1, "Y a-t-il des données personnelles dedans ?"),
         (2, "Si oui : finalité, base légale, durée, information"),
         (1, "L'usage touche-t-il une décision RH ?"),
         (2, "Si oui : haut risque, humain obligatoire, CSE"),
         (1, "Où sont hébergées les données ?"),
         (2, "Hors UE : encadrement du transfert à vérifier")],
        note="Ces 3 questions tiennent sur une carte. Elle est dans vos ressources.",
        etiquette="À GARDER")

    slide_jeu(prs, "7", "Le prompt qui fuit", "20 min",
        "Transformer un usage risqué en usage conforme",
        ["Je partage un prompt réel et dangereux",
         "Il contient nom, santé, avis sur une vendeuse",
         "Par deux, en salle séparée : ce qui cloche",
         "Réécrivez-le en version conforme",
         "Deux binômes lisent leur version",
         "On compare avec la version de référence"],
        "Partage d'écran + fiche J7 envoyée avant la session")

    # --- A5
    slide_choc(prs, "L'IA ne remplace pas", "le manager.",
        "Elle lui rend les heures qu'il n'a plus.", C_NUIT)

    slide(prs, "Où vous gagnez du temps",
        [(1, "Comptes rendus de brief structurés"),
         (1, "Préparation d'un entretien difficile"),
         (1, "Trames, procédures, modes opératoires"),
         (1, "Argumentaires et objections produits"),
         (1, "Analyse d'un texte long, en questions")],
        note="Aucun de ces usages n'est à haut risque, s'il reste anonymisé.")

    slide(prs, "Un bon prompt en 4 blocs",
        [(1, "Rôle : « Tu es chef de rayon… »"),
         (1, "Contexte : enseigne, taille, contrainte"),
         (1, "Tâche : un seul verbe, très précis"),
         (1, "Format : longueur, plan, ton attendu"),
         (2, "Et toujours : « dis-moi ce qu'il te manque »")],
        note="Le prompt est un brief. Un mauvais brief donne un mauvais stagiaire.")

    slide(prs, "Souveraineté : la question qui fâche",
        [(1, "Où sont stockées vos données ?"),
         (1, "Qui peut y accéder, sous quelle loi ?"),
         (1, "Sont-elles utilisées pour l'entraînement ?"),
         (1, "Pouvez-vous tout récupérer et partir ?"),
         (2, "Exigez ces 4 réponses par écrit au fournisseur")],
        note="Un hébergement UE ne suffit pas : regardez le droit applicable.",
        etiquette="À GARDER")

    slide_jeu(prs, "8", "Mon chantier IA", "15 min",
        "Repartir avec un plan applicable dès lundi",
        ["Listez vos tâches répétitives de la semaine",
         "Entourez celle qui vous coûte le plus",
         "Vérifiez-la avec les 3 réflexes",
         "Rédigez le prompt en 4 blocs",
         "Trois volontaires présentent en 60 secondes"],
        "Fiche J8 « Mon plan 30 jours » + grille d'évaluation n°2")

    slide(prs, "Ce qu'on retient de l'après-midi",
        [(1, "L'IA prédit, elle ne sait pas"),
         (1, "Données : finalité, minimum, durée, info"),
         (1, "L'IA Act classe les usages, pas les outils"),
         (1, "Embauche et planning = haut risque"),
         (1, "Article 4 : former, c'est obligatoire")],
        note="À vous : QUIZ n°2, 10 questions, 10 minutes, sans document.")

    slide_choc(prs, "Vous ne serez pas", "des chefs parfaits.",
        "Vous serez des chefs prévisibles. C'est mieux.", C_ACCENT)

    slide(prs, "Avant de vous déconnecter",
        [(1, "Votre plan 30 jours est écrit"),
         (1, "Une action, une date, une personne"),
         (1, "Les fiches ressources restent à vous"),
         (1, "L'évaluation à chaud : 3 minutes"),
         (2, "Merci pour votre énergie et votre franchise")],
        note="Une question après la formation ? Elle mérite quand même une réponse.")
