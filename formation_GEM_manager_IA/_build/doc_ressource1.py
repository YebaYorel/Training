# -*- coding: utf-8 -*-
from docs_engine import *

f = []
f += [H1("Fiche ressource n°1 — La psychologie du dirigeant et la posture managériale"),
      P("Document remis aux stagiaires du titre professionnel Manager d'Établissement Marchand. À conserver et à relire 30 jours après la formation."), E(3)]

f += [H2("1. Ce que porte un dirigeant (et que l'équipe ne voit pas)")]
f += [P("Le dirigeant n'a ni les mêmes informations, ni les mêmes échéances, ni les mêmes "
        "contraintes que son équipe. Comprendre cet écart ne sert pas à l'excuser : cela sert "
        "à mieux dialoguer avec lui, et à se préparer à occuper sa place.")]
f += puces([
    "<b>La charge économique</b> : le chiffre, la marge, la démarque, la paie du mois prochain.",
    "<b>La confidentialité subie</b> : il détient des informations qu'il n'a pas le droit de partager.",
    "<b>La décision en information incomplète</b> : il tranche rarement avec toutes les données.",
    "<b>La double loyauté</b> : vers le haut (siège, objectifs, marge) et vers le bas "
    "(conditions de travail, équité, moyens). Les deux tirent en sens inverse.",
    "<b>L'exposition permanente</b> : son humeur du matin est lue, interprétée et commentée."])
f += [E(2), encadre("Ce qu'il faut retenir", [
    "Un dirigeant distant n'est pas forcément méprisant : il est souvent saturé.",
    "Un manager de proximité vit le même grand écart, à une échelle plus petite.",
    "Comprendre la contrainte de l'autre, c'est augmenter son pouvoir de négociation."])]
f += [E(2), source("H. Mintzberg, <i>Le manager au quotidien : les dix rôles du cadre</i> "
                   "(rôles interpersonnels, informationnels et décisionnels).")]

f += [E(4), H2("2. Ni ami, ni ennemi : la troisième position")]
f += [tableau([
    ["Position", "Ce que je cherche", "Ce que ça produit"],
    ["L'ami", "Être apprécié, éviter le conflit",
     "Je n'ose plus recadrer. Les règles deviennent négociables. Les plus discrets se sentent lésés."],
    ["L'ennemi", "Être craint, garder le contrôle",
     "On me cache les erreurs. L'information remonte fausse. Je décide sur du vide."],
    ["Le garant du cadre", "Que la règle tienne pour tous",
     "On sait à quoi s'attendre. Le désaccord devient possible. La confiance se construit."]],
    [34*mm, 48*mm, None])]
f += [E(3), P("<b>La formule à retenir :</b> chaleureux sur la relation, ferme sur le cadre. "
              "Ce n'est pas contradictoire, c'est la définition même de la posture managériale.")]
f += [E(3), H3("Le pi\u00e8ge du chef sorti du rang"),
      P("C'est la situation la plus fr\u00e9quente en \u00e9tablissement marchand : hier vendeur, "
        "aujourd'hui responsable, avec la m\u00eame \u00e9quipe, la m\u00eame pause et les m\u00eames blagues. "
        "Puis arrive le premier samedi de repos \u00e0 refuser, et l'amiti\u00e9 se transforme en dette."),
      *puces([
        "Posez la r\u00e8gle <b>avant</b> d'en avoir besoin, d\u00e8s les premiers jours.",
        "Dites explicitement ce qui change et ce qui ne change pas dans la relation.",
        "N'annulez pas les liens : rendez-les visibles et \u00e9quitables pour tous.",
        "Acceptez de perdre un peu de popularit\u00e9 : c'est le prix de la pr\u00e9visibilit\u00e9."])]
f += [E(2), H3("Le test des trois questions avant d'agir"),
      *numerote([
        "Est-ce que j'appliquerais la même règle à quelqu'un que j'apprécie moins ?",
        "Est-ce que je pourrais dire cette phrase devant toute l'équipe ?",
        "Est-ce que je défends la règle, ou est-ce que je défends mon ego ?"])]
f += [E(2), encadre("Trois phrases à bannir", [
    "« Entre nous, la direction se trompe » → vous détruisez votre propre légitimité.",
    "« Je te le dis, mais garde-le pour toi » → vous créez un cercle, donc des exclus.",
    "« De toute façon, on n'y peut rien » → vous validez l'impuissance de l'équipe."],
    coul=ROUGE, fond=PALE_ROUGE)]

f += [SAUT(), H2("3. Les quatre styles de management, et quand les utiliser")]
f += [P("Il n'existe pas de bon style en soi. Il existe un style adapté à une personne, "
        "sur une tâche donnée, à un moment donné. Le même collaborateur peut appeler "
        "deux styles différents dans la même journée.")]
f += [tableau([
    ["Style", "Je fais quoi", "Quand c'est le bon choix", "Le risque si j'insiste"],
    ["Directif", "Je dis quoi faire et comment, je contrôle serré",
     "Urgence, sécurité, personne débutante, cadre non négociable", "Infantilisation, désengagement"],
    ["Persuasif", "J'explique le pourquoi, je convaincs, je mobilise",
     "Changement, résistance, besoin de sens", "Épuisement à argumenter, débat sans fin"],
    ["Participatif", "Je décide avec, je fais émerger les solutions",
     "Équipe compétente mais hésitante ou démotivée", "Lenteur, flou sur qui décide"],
    ["Délégatif", "Je confie l'objectif et les moyens, je suis les jalons",
     "Personne autonome et fiable sur cette tâche", "Abandon perçu, dérive non vue à temps"]],
    [26*mm, 42*mm, None, 40*mm])]
f += [E(2), source("P. Hersey et K. Blanchard, leadership situationnel — le style se choisit "
                   "selon la compétence et la motivation, tâche par tâche.")]
f += [E(3), encadre("L'erreur n°1 du manager débutant", [
    "Appliquer à tout le monde le style dans lequel il est le plus à l'aise.",
    "Directif avec un expert : il se ferme. Délégatif avec un débutant : il coule.",
    "Réflexe : avant d'entrer dans l'échange, se demander « où en est cette personne, sur CETTE tâche ? »"])]

f += [E(4), H2("4. Rigueur, ténacité : l'exigence qui fait grandir")]
f += puces([
    "<b>Une attente claire, formulée avant</b> : on ne sanctionne jamais une règle non dite.",
    "<b>La même règle pour tous</b> : l'exception non expliquée détruit plus qu'une sanction.",
    "<b>Les moyens avant le résultat</b> : exiger sans donner les moyens s'appelle une injonction paradoxale.",
    "<b>Un retour rapide</b> : dans les 48 heures, sinon le fait devient une rumeur.",
    "<b>La ténacité</b> : tenir la règle le 40<super>e</super> jour comme le premier. "
    "C'est là que se gagne la crédibilité, pas dans le discours de lancement."])

f += [E(3), H2("5. La frontière entre exigence et toxicité")]
f += [tableau([
    ["Critère", "Manager exigeant", "Manager toxique"],
    ["Objet de la critique", "Le résultat, le comportement, le fait", "La personne, son caractère, son intelligence"],
    ["Lieu du recadrage", "En privé, systématiquement", "En public, devant l'équipe ou en réunion"],
    ["Stabilité des règles", "Stables, écrites, connues à l'avance", "Changeantes, implicites, rétroactives"],
    ["Nature du contrôle", "Sur des jalons définis ensemble", "Sur chaque geste, en continu"],
    ["Gestion du silence", "Dit les choses vite et clairement", "Silence punitif, mise à l'écart"],
    ["Issue proposée", "Un chemin de progression, daté", "Aucune porte de sortie"]],
    [38*mm, None, None])]
f += [E(3), encadre("Les conséquences, côté équipe", [
    "Hypervigilance, troubles du sommeil, fatigue chronique.",
    "Disparition du signalement d'erreur : les problèmes remontent trop tard.",
    "Absentéisme, puis départs en série — les plus employables partent les premiers.",
    "Cadre de lecture : les 6 familles de facteurs de risques psychosociaux, dont les "
    "« rapports sociaux au travail dégradés »."], coul=ROUGE, fond=PALE_ROUGE)]
f += [E(2), source("INRS, dossier « Risques psychosociaux », six familles de facteurs de RPS (inrs.fr).")]

f += [E(3), H3("Le rappel juridique"),
      *puces([
        "<b>Obligation de sécurité de l'employeur</b> — Code du travail, article L.4121-1 : "
        "l'employeur prend les mesures nécessaires pour assurer la sécurité et protéger la "
        "santé physique et mentale des travailleurs.",
        "<b>Harcèlement moral</b> — Code du travail, article L.1152-1 : agissements répétés "
        "ayant pour objet ou pour effet une dégradation des conditions de travail.",
        "<b>Le manager est concerné</b> : une délégation de pouvoir s'accompagne d'une "
        "délégation de responsabilité."])]
f += [E(2), source("Légifrance, Code du travail. Vérifier la version en vigueur à la date de la formation.")]

f += [SAUT(), H2("6. Langage, voix et posture")]
f += [P("Trois canaux transmettent simultanément votre message. Lorsqu'ils se contredisent, "
        "l'interlocuteur accorde le plus de poids au canal non verbal pour juger de votre "
        "attitude et de votre sincérité — pas pour comprendre le contenu.")]
f += [tableau([
    ["Canal", "Ce que ça déclenche", "Le réglage utile"],
    ["Les mots", "La compréhension du contenu", "Des faits, des verbes d'action, pas d'adjectif sur la personne"],
    ["La voix", "La perception de l'assurance", "Débit ralenti, volume stable, silences de 2 secondes"],
    ["Le corps", "Le jugement sur la sincérité", "Appuis stables, mains visibles, regard balayé"]],
    [28*mm, 56*mm, None])]
f += [E(2), P("<b>Attention aux idées reçues :</b> le fameux « 7 % / 38 % / 55 % » "
              "(Mehrabian) ne concerne que la perception d'une attitude émotionnelle en cas de "
              "message contradictoire. Il ne signifie pas que les mots ne comptent que pour 7 %.")]
f += [E(2), H3("La posture en 5 points, applicable immédiatement"),
      *numerote([
        "Deux pieds au sol, poids réparti également : vous cessez de vous balancer.",
        "Épaules basses, menton horizontal : la voix descend et porte davantage.",
        "Mains visibles, au-dessus de la ceinture : elles rassurent.",
        "Regard balayé, environ 3 secondes par personne : chacun se sent adressé.",
        "Un silence de 2 secondes juste avant le message essentiel : il crée l'attention."])]

f += [E(3), H2("7. Dire ce qui ne va pas : la méthode DESC")]
f += [tableau([
    ["Étape", "Ce que je fais", "Exemple"],
    ["D — Décrire", "Les faits seuls, datés, sans adjectif",
     "« La caisse a ouvert à 9h12, l'ouverture était à 9h00. »"],
    ["E — Exprimer", "L'effet, en parlant de soi",
     "« J'ai eu six clients en attente devant une grille fermée. »"],
    ["S — Suggérer", "Une solution précise, pas un reproche",
     "« Je te propose de m'appeler dès que tu vois que tu seras en retard. »"],
    ["C — Conclure", "Un accord daté et vérifiable",
     "« On se refait un point vendredi 10h pour valider. »"]],
    [30*mm, 54*mm, None])]
f += [E(2), encadre("Les trois règles non négociables du feedback", [
    "Jamais devant les autres. Toujours en face à face.",
    "Dans les 48 heures après le fait. Au-delà, c'est du ressentiment.",
    "Un seul sujet par entretien. Deux reproches simultanés = zéro message reçu."])]

f += [E(4), H2("8. Conduire un brief d'équipe qui sert à quelque chose")]
f += [H3("Avant — c'est là que le brief se gagne"),
      *puces([
        "Un objectif écrit en une phrase : « À la fin, nous aurons décidé que… »",
        "Trois points maximum à l'ordre du jour, avec une durée par point.",
        "Les bonnes personnes, pas toutes les personnes.",
        "Une durée annoncée — et tenue, même si tout n'est pas traité.",
        "<b>Règle simple :</b> pas d'ordre du jour écrit, pas de brief."])]
f += [E(2), H3("Pendant"),
      *puces([
        "Rappeler l'objectif en 30 secondes, debout si possible.",
        "Donner la parole avant de donner son avis : sinon plus personne ne contredit.",
        "Aller chercher les silencieux nommément, en premier.",
        "Couper le hors-sujet avec respect : « Sujet important, je le note, on le traite à part. »",
        "Conclure par qui fait quoi, pour quand — à voix haute, devant tous.",
        "<b>Indicateur :</b> si vous parlez plus de 40 % du temps, ce n'est plus un brief."])]
f += [E(2), H3("Les quatre profils difficiles"),
      tableau([
        ["Profil", "Ce qu'il fait", "Ce que vous faites"],
        ["Le bavard", "Occupe l'espace, déroule", "Cadrez le temps : « deux minutes chacun », puis tenez-le"],
        ["Le sceptique", "Objecte sur tout", "Demandez sa condition : « qu'est-ce qu'il te faudrait pour y croire ? »"],
        ["Le silencieux", "Ne dit rien, désapprouve après", "Interrogez-le en premier, sur un point précis"],
        ["Le démotivé", "Soupire, ironise, décourage", "Ne traitez jamais en public : rendez-vous en privé sous 48h"]],
        [28*mm, 52*mm, None])]

f += [E(4), H2("9. Votre plan d'action à 30 jours")]
f += [P("Choisissez <b>trois</b> actions maximum. Une action sans date n'est pas une action.")]
f += [tableau([
    ["Ce que je change", "Avec qui", "Avant le", "Comment je saurai que c'est fait"],
    [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]],
    [None, 34*mm, 26*mm, 58*mm])]

f += [E(4), H2("Sources et pour aller plus loin")]
f += puces([
    "H. Mintzberg, <i>Le manager au quotidien</i> — les dix rôles du cadre.",
    "P. Hersey et K. Blanchard — leadership situationnel (quatre styles).",
    "R. Blake et J. Mouton — grille managériale (souci des résultats / souci des personnes).",
    "D. Goleman, <i>Leadership that gets results</i> — six styles de leadership.",
    "INRS — dossier « Risques psychosociaux », six familles de facteurs (inrs.fr).",
    "ANACT — ressources sur la qualité de vie et des conditions de travail (anact.fr).",
    "Légifrance — Code du travail, articles L.4121-1 et L.1152-1 (legifrance.gouv.fr)."], st="petit")
f += [E(2), P("<i>Les références juridiques doivent être vérifiées dans leur version en vigueur "
              "à la date de consultation.</i>", "petit")]

doc = document("../07_fiches_ressources/Fiche_ressource_1_Psychologie_du_dirigeant.pdf",
               "Fiche ressource n°1 — Psychologie du dirigeant",
               "Posture managériale, styles, exigence et toxicité, langage, réunions")
doc.build(f)
print("Fiche ressource 1 : OK")
