# -*- coding: utf-8 -*-
from docs_engine import *

f = [H1("Dispositif à distance et conformité"),
     P("Document formateur et centre. Ce que la réglementation exige d'une formation réalisée "
       "à distance, ce que cette journée met concrètement en place, et les points à arbitrer "
       "avant la session."), E(3)]
f += [encadre("Avertissement", [
    "Ce document est un support de travail. Il ne constitue pas un conseil juridique "
    "individualisé. Les références doivent être vérifiées dans leur version en vigueur "
    "à la date de la session."], coul=ACCENT, fond=PALE_ACCENT)]

f += [E(3), H2("1. Ce qu'exige une action réalisée à distance")]
f += [P("Le Code du travail prévoit qu'une action de formation peut être réalisée en tout ou "
        "partie à distance. Trois éléments sont alors expressément requis.")]
f += [tableau([
    ["Exigence", "Ce que cette journée prévoit"],
    ["<b>1. Une assistance technique et pédagogique appropriée</b> pour accompagner le "
     "bénéficiaire dans le déroulement de son parcours",
     "Contact d'assistance communiqué à J–7 et rappelé sur la diapositive d'accueil. "
     "Formateur connecté 30 minutes avant. Plan B écrit pour chaque incident (voir conducteur). "
     "Assistance pédagogique assurée en continu par le formateur en classe virtuelle synchrone."],
    ["<b>2. Une information du bénéficiaire</b> sur les activités pédagogiques à effectuer "
     "à distance et leur durée moyenne",
     "Programme détaillé envoyé à J–7 avec le minutage séquence par séquence. "
     "Diapositive « Votre journée » affichée en ouverture. Durée annoncée avant chaque jeu."],
    ["<b>3. Des évaluations</b> qui jalonnent ou concluent l'action",
     "Deux grilles d'évaluation critériées en cours de journée (11h50 et 16h35) et deux quiz "
     "de 10 questions (12h20 et 16h45). Évaluation à chaud en clôture."]],
    [62*mm, None])]
f += [E(2), source("Code du travail, articles L.6353-1 et D.6313-3-1 — legifrance.gouv.fr. "
                   "Vérifier la rédaction en vigueur.")]

f += [E(4), H2("2. Traçabilité : ce qu'il faut pouvoir produire")]
f += [P("Une formation à distance financée se prouve autrement qu'une feuille d'émargement "
        "papier. Rassemblez systématiquement :")]
f += puces([
    "Le <b>programme</b> envoyé en amont, avec la modalité à distance clairement indiquée.",
    "Les <b>émargements</b> de la journée (au minimum matin et après-midi), signés selon "
    "les modalités acceptées par le centre.",
    "Les <b>traces de connexion</b> produites par l'outil de classe virtuelle.",
    "Les <b>productions des stagiaires</b> : quiz renseignés, grilles, fiches « Mon chantier IA ».",
    "Le <b>relevé des incidents</b> techniques et des mesures de rattrapage retenues.",
    "L'<b>évaluation à chaud</b> et, si le centre la pratique, l'évaluation à froid."])
f += [E(2), encadre("Le point le plus souvent oublié", [
    "Une formation à distance qui n'a laissé aucune production de stagiaire est très difficile "
    "à justifier. Les huit jeux de cette journée produisent tous une trace écrite : "
    "c'est délibéré. Ramassez-les."])]

f += [SAUT(), H2("3. Ce que l'audit qualité regardera")]
f += [P("Le référentiel national qualité impose, pour une prestation à distance, de démontrer "
        "principalement les points suivants. Les numéros d'indicateurs évoluant d'une version "
        "à l'autre du référentiel, ils ne sont volontairement pas cités ici : reportez-vous "
        "à la version en vigueur, et au guide de lecture.")]
f += [tableau([
    ["Ce que l'audit cherche", "La pièce que ce kit fournit"],
    ["Information préalable du public sur les modalités, les prérequis techniques et la durée",
     "Programme détaillé + checklist J–7 du conducteur"],
    ["Objectifs opérationnels et évaluables",
     "Diapositive « Ce soir, vous saurez… » : 7 compétences, toutes évaluées le jour même"],
    ["Adaptation des moyens à la modalité à distance",
     "Kit jeux intégralement reconçu pour la visio, avec variante de repli par jeu"],
    ["Prise en compte des situations de handicap",
     "Protocole d'accessibilité du conducteur + diaporama conçu et contrôlé pour le public malvoyant"],
    ["Évaluation de l'atteinte des objectifs",
     "2 grilles critériées à 7 critères et 2 quiz notés, avec seuils d'acquisition définis"],
    ["Recueil des appréciations et traitement des difficultés",
     "Évaluation à chaud en clôture + relevé d'incidents techniques"],
    ["Compétence et actualisation des connaissances du formateur",
     "Sources datées et référencées dans les deux fiches ressources"]],
    [66*mm, None])]

f += [E(4), H2("4. RGPD : la classe virtuelle est un traitement de données")]
f += [P("Organiser une classe virtuelle, c'est traiter des données personnelles : nom, image, "
        "voix, adresse électronique, adresse IP, horodatage des connexions, contenu du tchat.")]
f += [tableau([
    ["Question", "Réponse de principe"],
    ["Qui est responsable de traitement ?",
     "Le centre de formation organisateur, qui détermine la finalité et les moyens. Le formateur "
     "intervenant agit dans ce cadre. À clarifier par écrit avant la session."],
    ["Quelle finalité ?",
     "Réalisation et justification de l'action de formation. Rien d'autre : pas de prospection, "
     "pas de réutilisation commerciale des échanges."],
    ["Quelle base légale ?",
     "En règle générale l'exécution du contrat de formation, ou l'obligation légale pour "
     "les pièces justificatives exigées par le financeur."],
    ["Combien de temps conserver ?",
     "Le temps nécessaire à la justification auprès du financeur et au contrôle. La durée "
     "doit être <b>définie et annoncée</b>, pas subie."],
    ["Que dire aux stagiaires ?",
     "En ouverture, à voix haute : ce qui est collecté, pourquoi, combien de temps, "
     "à qui s'adresser. Trente secondes suffisent."]],
    [56*mm, None])]

f += [E(3), H3("La question de la caméra"),
      encadre("À ne pas transformer en obligation absolue", [
        "Imposer l'activation permanente de la caméra, de manière générale et sans justification "
        "proportionnée, est contestable au regard du droit à la vie privée : l'image du stagiaire "
        "et son cadre de vie sont en jeu.",
        "La position retenue dans ce kit : la caméra est <b>vivement encouragée et expliquée</b> "
        "(l'exercice de posture n'a pas de sens sans visage), jamais imposée sous sanction.",
        "Un stagiaire qui ne peut pas l'activer participe autrement : rôle d'observateur au jeu n°4, "
        "réponse dans le tchat au jeu n°5.",
        "Proposez systématiquement l'arrière-plan flouté : la gêne vient plus souvent du logement "
        "que du visage."], coul=ROUGE, fond=PALE_ROUGE)]

f += [E(3), H3("L'enregistrement de la session"),
      *puces([
        "L'enregistrement est un <b>traitement distinct</b>, avec sa finalité propre. Il ne se "
        "déduit pas de l'organisation de la classe virtuelle.",
        "Il suppose une information préalable claire, avant le début, et une base légale examinée.",
        "Si l'enregistrement repose sur l'accord des stagiaires, cet accord doit être réellement "
        "libre : prévoir une alternative pour qui refuse (caméra et micro coupés, participation "
        "par le tchat), sans conséquence sur l'évaluation.",
        "Préciser la durée de conservation et qui aura accès à l'enregistrement.",
        "<b>Choix retenu par défaut pour cette journée : aucun enregistrement.</b> C'est le plus "
        "simple, et cela libère la parole sur un sujet où l'on parle de son chef."])]
f += [E(2), source("CNIL — publications sur la visioconférence et sur les données des salariés "
                   "et stagiaires (cnil.fr). RGPD, art. 5, 6, 12 à 14 et 32.")]

f += [SAUT(), H2("5. Souveraineté : quel outil de classe virtuelle ?")]
f += [P("Vous enseignez l'après-midi que la localisation des données et le droit applicable au "
        "fournisseur sont deux questions distinctes. Le matin, vous utilisez un outil de visio : "
        "la cohérence se vérifie là."), E(2)]
f += [encadre("Les quatre questions à poser sur votre outil de visio", [
    "Où sont hébergés les flux, les enregistrements éventuels et les journaux de connexion ?",
    "À quelle législation l'éditeur est-il soumis ? Un hébergement en Europe ne neutralise pas "
    "une législation extraterritoriale applicable à la maison mère.",
    "Les contenus (tchat, transcriptions) servent-ils à entraîner des modèles ?",
    "Le contrat de sous-traitance prévu à l'article 28 du RGPD est-il signé et disponible ?"])]
f += [E(3), P("<b>Pistes à instruire</b> si le centre souhaite une solution européenne. Cette liste "
              "est une base de travail, <b>pas une recommandation</b> : vérifiez l'état des "
              "certifications, l'hébergement réel et les conditions contractuelles avant tout choix.")]
f += [tableau([
    ["Solution", "Nature", "À vérifier avant de choisir"],
    ["BigBlueButton", "Logiciel libre, pensé pour la formation (salles séparées, sondages, tableau blanc)",
     "Nécessite un hébergeur : qui l'opère, où, sous quel contrat"],
    ["Jitsi Meet", "Logiciel libre, installation simple",
     "Fonctions d'animation plus limitées ; hébergement à qualifier"],
    ["Tixeo", "Éditeur français, positionné sur la sécurité",
     "Étendue exacte des qualifications et adéquation aux besoins pédagogiques"],
    ["Livestorm, Whereby", "Éditeurs européens",
     "Hébergement effectif, sous-traitants ultérieurs, clauses de l'article 28"],
    ["Teams, Zoom, Meet", "Éditeurs soumis à une législation extraterritoriale",
     "Très répandus et fonctionnellement complets ; documenter le transfert et l'encadrement"]],
    [34*mm, None, 60*mm])]
f += [E(2), encadre("La position honnête à tenir devant le groupe", [
    "Si le centre impose un outil non européen, ne le cachez pas : dites-le, expliquez pourquoi "
    "le sujet se pose, et montrez ce qui est documenté pour l'encadrer.",
    "C'est pédagogiquement bien plus fort qu'un discours parfait : les stagiaires vivront "
    "exactement ce compromis dans leur enseigne."], coul=VERT, fond=PALE_VERT)]

f += [E(4), H2("6. À arbitrer avant la session")]
f += [tableau([
    ["Point", "Décision à prendre", "Par qui"],
    ["Effectif", "Le kit fonctionne de 6 à 16 stagiaires. En dessous de 6 : supprimer les salles "
     "séparées. Au-dessus de 16 : un seul passage au jeu n°4 et co-animation conseillée.",
     "Centre"],
    ["Outil de visio", "Lequel, avec quelles fonctions (salles séparées, sondage, message privé) ?",
     "Centre"],
    ["Assistance technique", "Qui répond le jour J, sur quel numéro, à quelles heures ?", "Centre"],
    ["Enregistrement", "Enregistré ou non ? Par défaut : non.", "Centre + formateur"],
    ["Émargement", "Quelles modalités acceptées par le financeur ?", "Centre"],
    ["Envoi des supports à J–7", "Qui envoie, sur quelle liste, avec quel message ?", "Centre + formateur"],
    ["Conservation des copies", "Durée retenue, et qui détruit à l'échéance ?", "Centre"]],
    [36*mm, None, 26*mm])]

f += [E(4), H2("Sources")]
f += puces([
    "Code du travail, articles L.6353-1 et D.6313-3-1 — legifrance.gouv.fr",
    "Référentiel national qualité (RNQ) et son guide de lecture — travail-emploi.gouv.fr",
    "Règlement (UE) 2016/679 (RGPD), articles 5, 6, 12 à 14, 28 et 32 — Journal officiel de l'UE",
    "CNIL — publications sur la visioconférence, le télétravail et les données des stagiaires (cnil.fr)",
    "Règlement (UE) 2024/1689 (IA Act), article 4 — Journal officiel de l'UE"], st="petit")
f += [E(2), P("<i>Toute référence doit être vérifiée dans sa version en vigueur au jour de la "
              "consultation.</i>", "petit")]

doc = document("../09_dispositif_distance/Dispositif_a_distance_et_conformite.pdf",
               "Dispositif à distance et conformité",
               "FOAD, traçabilité, qualité, RGPD de la classe virtuelle, souveraineté")
doc.build(f)
print("Dispositif FOAD : OK")
