# -*- coding: utf-8 -*-
from docs_engine import *
from reportlab.platypus import Table, TableStyle, Paragraph

def fiche(num, nom, duree, moment, objectif, materiel, deroule, debrief, extra=None):
    b = [H1("Jeu n°%d — %s" % (num, nom))]
    b += [tableau([["Durée", "Moment", "Objectif pédagogique"],
                   [duree, moment, objectif]], [22*mm, 34*mm, None])]
    b += [E(3), H2("Matériel"), *puces(materiel)]
    b += [E(2), H2("Déroulé"), *numerote(deroule)]
    if extra:
        b += extra
    b += [E(2), H2("Débrief — les questions à poser"), *puces(debrief)]
    return b

f = [H1("Kit de jeux et d'exercices — mode d'emploi de l'animateur"),
     P("Huit séquences actives réparties sur la journée. Chaque fiche est autonome : "
       "matériel, déroulé minuté, corrigé et questions de débrief."),
     E(3),
     encadre("Règles d'animation communes", [
        "Annoncer systématiquement la durée et la faire respecter : le chrono crée l'énergie.",
        "Ne jamais corriger avant d'avoir fait justifier : l'erreur expliquée vaut le cours.",
        "Accessibilité : proposer toujours une alternative assise aux jeux en déplacement, "
        "et lire à voix haute toute carte distribuée.",
        "Aucune situation ne doit désigner un participant ou son entreprise réelle."]),
     SAUT()]

# ------------------------------------------------------------------ J1 ----
f += fiche(1, "Le thermomètre", "15 min", "8h05 — ouverture",
  "Faire émerger les représentations du groupe sur la place du dirigeant, sans débat.",
  ["Ruban adhésif ou corde pour tracer une ligne de 6 mètres au sol",
   "Deux feuilles A3 : « MON CHEF EST UN AMI » / « MON CHEF EST UN ADVERSAIRE »"],
  ["Tracer la ligne, poser les deux affiches aux extrémités.",
   "Annoncer : « Placez-vous où vous vous sentez juste. Il n'y a pas de bonne place. »",
   "Laisser 60 secondes de placement, sans commentaire.",
   "Interroger trois volontaires : « pourquoi ici et pas 2 mètres plus loin ? »",
   "Interdire tout débat ou contradiction : on écoute, on ne répond pas.",
   "Conclure : « Gardez votre place en tête. On y revient à 11h45. »"],
  ["Qu'est-ce qui vous a fait hésiter au moment de vous placer ?",
   "Qui a changé de place en voyant les autres ? Qu'est-ce que ça dit d'une équipe ?",
   "Est-ce que votre place décrit votre chef actuel, ou le chef que vous voudriez être ?"],
  extra=[E(2), encadre("Variante assise (accessibilité)", [
     "Distribuer une réglette de 0 à 10 ; chacun entoure un chiffre et l'annonce à voix haute.",
     "L'effet de groupe est conservé, le déplacement n'est plus nécessaire."])])

f += [SAUT()]
# ------------------------------------------------------------------ J2 ----
f += fiche(2, "Les quatre coins", "20 min", "10h15 — après la pause",
  "Choisir le style managérial adapté à une situation, sous contrainte de temps.",
  ["4 affiches A3 : DIRECTIF / PERSUASIF / PARTICIPATIF / DÉLÉGATIF, une par coin",
   "La liste des 8 situations ci-dessous (animateur uniquement)"],
  ["Afficher un style dans chaque coin de la salle.",
   "Lire une situation à voix haute, deux fois, lentement.",
   "Annoncer : « 10 secondes pour rejoindre un coin. »",
   "Choisir un porte-parole par coin : 20 secondes de justification.",
   "Révéler le style attendu et, surtout, le critère qui tranche.",
   "Enchaîner les 8 situations sans commenter longuement."],
  ["Sur quelle situation le groupe s'est-il le plus divisé ? Pourquoi ?",
   "Quel style avez-vous choisi le plus souvent ? C'est votre style par défaut.",
   "Quel style n'avez-vous jamais choisi ? C'est votre angle mort."])
f += [E(3), H2("Les 8 situations et le style attendu — document animateur"),
  tableau([
    ["N°", "Situation lue à voix haute", "Attendu", "Critère qui tranche"],
    ["1", "Un client menace de rompre le contrat aujourd'hui. L'équipe attend une consigne.",
     "Directif", "Urgence + enjeu immédiat"],
    ["2", "Une nouvelle recrue, troisième jour, doit utiliser une machine dangereuse.",
     "Directif", "Sécurité + compétence faible"],
    ["3", "La direction impose un changement d'horaires. L'équipe est en colère.",
     "Persuasif", "Décision non négociable mais besoin de sens"],
    ["4", "Il faut installer un nouveau logiciel. Personne n'en voit l'intérêt.",
     "Persuasif", "Résistance + adhésion à construire"],
    ["5", "L'équipe expérimentée doit réorganiser le planning des congés d'été.",
     "Participatif", "Compétence présente + acceptabilité déterminante"],
    ["6", "Deux techniciens compétents sont démotivés depuis le départ de leur collègue.",
     "Participatif", "Compétence haute, motivation basse"],
    ["7", "Un chef d'équipe autonome depuis quatre ans prend un chantier qu'il connaît.",
     "Délégatif", "Autonomie avérée sur cette tâche"],
    ["8", "Un collaborateur senior demande à gérer seul un dossier qu'il a déjà mené trois fois.",
     "Délégatif", "Demande + historique de réussite"]],
    [8*mm, None, 24*mm, 44*mm])]
f += [E(2), P("<b>Message de synthèse à faire émerger :</b> ce n'est jamais la personne "
              "qui détermine le style, c'est le couple personne + tâche + urgence.", "petit")]

f += [SAUT()]
# ------------------------------------------------------------------ J3 ----
f += fiche(3, "Exigeant ou toxique ?", "20 min", "10h40",
  "Construire collectivement le critère qui sépare l'exigence de la toxicité.",
  ["12 cartes A5 par équipe (à photocopier et découper, page suivante)",
   "3 feuilles A3 par équipe : EXIGEANT / LIMITE / TOXIQUE"],
  ["Constituer des équipes de 4 personnes maximum.",
   "Distribuer les 12 cartes et les trois zones.",
   "10 minutes pour classer les 12 cartes. Consensus obligatoire.",
   "Chaque équipe présente uniquement sa carte classée en « LIMITE ».",
   "Noter au tableau les critères invoqués par les équipes.",
   "Retenir collectivement trois critères et les afficher pour la journée."],
  ["Quelle carte a provoqué le plus de désaccord dans votre équipe ?",
   "Un même comportement peut-il être exigeant avec l'un et toxique avec l'autre ?",
   "Qu'est-ce qui change tout : l'intention du manager, ou l'effet sur la personne ?"])
f += [E(3), H2("Les 12 cartes et leur classement — document animateur"),
  tableau([
    ["N°", "Texte de la carte", "Classement"],
    ["1", "Le manager reprend un collaborateur en privé, 24 heures après l'erreur, en décrivant les faits.", "Exigeant"],
    ["2", "En réunion, le manager dit : « Encore une fois, le rapport n'est pas arrivé. » en regardant une personne.", "Toxique"],
    ["3", "Le manager demande un point d'avancement chaque vendredi, fixé dès le lancement du projet.", "Exigeant"],
    ["4", "Le manager demande un point d'avancement quatre fois par jour, sans l'avoir annoncé.", "Toxique"],
    ["5", "Le manager refuse une demande de congés en expliquant la règle, la même pour tous.", "Exigeant"],
    ["6", "Depuis un désaccord, le manager ne répond plus aux messages d'un collaborateur, depuis trois jours.", "Toxique"],
    ["7", "Le manager fixe un objectif ambitieux puis demande : « qu'est-ce qu'il te manque ? »", "Exigeant"],
    ["8", "Le manager change la priorité du dossier tous les deux jours, sans jamais expliquer pourquoi.", "Toxique"],
    ["9", "Le manager dit : « Je sais que tu peux faire mieux, montre-moi une version 2 pour jeudi. »", "Exigeant"],
    ["10", "Le manager plaisante sur la façon de parler d'un collaborateur, devant l'équipe.", "Toxique"],
    ["11", "Le manager envoie des messages professionnels à 23 heures. Il n'attend pas de réponse, mais ne l'a jamais dit.", "<b>Limite</b>"],
    ["12", "En réunion, le manager félicite systématiquement la même personne.", "<b>Limite</b>"]],
    [8*mm, None, 26*mm])]
f += [E(2), encadre("Clé de lecture à donner après le débat", [
   "Carte 11 : ce n'est pas l'horaire qui pose problème, c'est le non-dit. Une règle explicite "
   "(« je travaille tard, personne ne répond avant 8h ») fait basculer la carte côté exigeant.",
   "Carte 12 : l'intention est bonne, l'effet est un favoritisme perçu. C'est l'effet qui compte.",
   "Les trois critères à faire émerger : l'objet de la critique (fait ou personne), "
   "le lieu (privé ou public), l'existence d'une issue (chemin de progression ou impasse)."])]

f += [SAUT()]
# ------------------------------------------------------------------ J4 ----
f += fiche(4, "La réunion de 9h", "30 min", "11h20 — évaluation",
  "Se mettre en situation réelle d'animation sous tension et se voir évaluer sur des faits.",
  ["4 cartes rôles à découper (ci-dessous), remises pliées",
   "Un chronomètre visible de tous",
   "Une grille d'évaluation n°1 par observateur"],
  ["Désigner un manager volontaire et quatre joueurs de rôle. Les autres observent.",
   "Remettre les cartes rôles pliées : personne ne connaît le rôle des autres.",
   "Briefer le manager à voix haute (encadré ci-dessous), devant tout le monde.",
   "Lancer 8 minutes de réunion, chrono visible. Ne jamais interrompre.",
   "Stopper net à 8 minutes, même si la réunion n'est pas conclue.",
   "Débrief de 10 minutes : le manager d'abord, les rôles ensuite, les observateurs en dernier.",
   "Si le temps le permet, refaire un passage avec un autre manager."],
  ["Manager : à quel moment avez-vous senti que vous perdiez la salle ?",
   "Joueurs : à quel moment précis vous êtes-vous senti écouté ? Et ignoré ?",
   "Observateurs : citez un fait, jamais une impression.",
   "Que feriez-vous différemment dans les 60 premières secondes ?"])
f += [E(3), encadre("Brief du manager — à lire à voix haute", [
   "Vous êtes responsable d'une équipe de quatre personnes.",
   "La direction impose un nouveau planning à partir du mois prochain : les horaires "
   "changent, les jours de repos aussi. Ce n'est pas négociable.",
   "Vous n'avez pas choisi cette décision et vous n'êtes pas d'accord avec la méthode.",
   "Vous avez 8 minutes pour annoncer, entendre l'équipe et repartir avec des engagements."])]
f += [E(3), H2("Les quatre cartes rôles — à découper et à plier")]
for titre_r, texte_r in [
  ("RÔLE 1 — LE BAVARD",
   "Vous parlez beaucoup et vous partez souvent du sujet. Vous racontez une anecdote dès "
   "que vous le pouvez. Vous n'êtes pas de mauvaise foi : vous aimez sincèrement échanger. "
   "Si le manager vous cadre avec respect, vous acceptez volontiers."),
  ("RÔLE 2 — LE SCEPTIQUE",
   "Vous objectez sur chaque point : « ça ne marchera pas », « on a déjà essayé ». "
   "Vous avez de vraies raisons : le dernier changement s'est mal passé. Si le manager "
   "vous demande ce qu'il vous faudrait pour y croire, vous donnez une condition précise."),
  ("RÔLE 3 — LE SILENCIEUX",
   "Vous ne dites rien, sauf si on vous interroge nommément et sur un point précis. "
   "Vous êtes en réalité le plus impacté : le nouveau planning est incompatible avec "
   "votre mode de garde. Vous ne le direz que si on vous met en confiance."),
  ("RÔLE 4 — LE DÉMOTIVÉ",
   "Vous soupirez, vous consultez votre téléphone, vous lancez des piques : « de toute "
   "façon… ». Si le manager vous prend à partie en public, vous vous braquez. S'il vous "
   "propose un point en privé après la réunion, vous acceptez.")]:
    f += [encadre(titre_r, [texte_r], coul=ACCENT, fond=colors.HexColor("#FCEFE7")), E(2)]

f += [SAUT()]
# ------------------------------------------------------------------ J5 ----
f += fiche(5, "Vrai ou faux, debout", "15 min", "13h00 — reprise",
  "Relancer l'énergie après le déjeuner et mesurer les idées reçues sur l'IA.",
  ["Deux affiches A3 : VRAI / FAUX, posées de part et d'autre de la salle",
   "Les 6 affirmations ci-dessous"],
  ["Faire lever tout le monde et se regrouper au centre.",
   "Lire l'affirmation, deux fois. Annoncer : « 5 secondes, on choisit un côté. »",
   "Interdire de rester au milieu : trancher fait partie de l'exercice.",
   "Interroger une personne de chaque côté, 15 secondes chacune.",
   "Donner la réponse ET la source. Enchaîner immédiatement.",
   "Rester debout jusqu'à la fin des 6 affirmations."],
  ["Quelle réponse vous a le plus surpris ?",
   "Laquelle de ces croyances circule dans votre entreprise ?",
   "Qui, chez vous, devrait entendre ces six réponses ?"])
f += [E(3), tableau([
    ["Affirmation lue", "Réponse", "À dire immédiatement après"],
    ["« L'IA Act interdit d'utiliser l'IA générative en entreprise. »", "FAUX",
     "Il encadre les usages selon leur risque. La plupart des usages de bureau sont à risque minimal."],
    ["« Une IA peut inventer un article de loi qui n'existe pas. »", "VRAI",
     "C'est l'hallucination : une référence plausible et fausse. Toujours vérifier à la source."],
    ["« Trier des CV avec une IA est un usage à haut risque. »", "VRAI",
     "Emploi et gestion de la main-d'œuvre : annexe III de l'IA Act."],
    ["« Si mes données sont hébergées en France, la souveraineté est assurée. »", "FAUX",
     "Le lieu ne suffit pas : il faut regarder le droit auquel l'éditeur est soumis."],
    ["« Je suis obligé de former mon personnel à l'IA qu'il utilise. »", "VRAI",
     "IA Act, article 4, applicable depuis le 2 février 2025. Aucune exemption de taille."],
    ["« Analyser l'humeur des salariés en réunion est permis si on les prévient. »", "FAUX",
     "Pratique interdite (art. 5). Aucune information ni aucun accord ne la rend licite."]],
    [None, 20*mm, 62*mm])]

f += [SAUT()]
# ------------------------------------------------------------------ J6 ----
f += fiche(6, "Le tri des risques", "20 min", "14h30",
  "Savoir classer un usage d'IA avant de l'autoriser, en justifiant par l'usage.",
  ["4 affiches A3 : INTERDIT / HAUT RISQUE / RISQUE LIMITÉ / RISQUE MINIMAL",
   "12 cartes usages par équipe (ci-dessous)"],
  ["Poser les 4 zones au sol ou au mur, dans l'ordre décroissant.",
   "Équipes de 4. Distribuer les 12 cartes mélangées.",
   "8 minutes pour placer les 12 cartes. Consensus obligatoire.",
   "Une équipe défend trois cartes de son choix ; une autre équipe peut contester.",
   "Corriger en citant l'article applicable, pas en donnant un avis.",
   "Identifier les trois cartes qui ont le plus divisé et y revenir."],
  ["Qu'est-ce qui vous a fait hésiter : l'outil ou l'usage ?",
   "Combien de ces usages existent déjà chez vous, sans avoir été qualifiés ?",
   "Qui, dans votre entreprise, devrait faire ce tri avant l'achat d'un outil ?"])
f += [E(3), H2("Les 12 cartes usages et leur classement — document animateur"),
  tableau([
    ["N°", "Usage décrit sur la carte", "Niveau", "Fondement"],
    ["1", "Analyser les expressions du visage des salariés en réunion pour mesurer l'engagement.", "<b>Interdit</b>", "IA Act art. 5 — émotions au travail"],
    ["2", "Classer automatiquement les candidatures reçues pour un poste.", "Haut risque", "Annexe III, pt 4"],
    ["3", "Rédiger un compte rendu à partir de notes anonymisées.", "Minimal", "Aucun traitement à enjeu"],
    ["4", "Un agent conversationnel répond aux clients sur le site internet.", "Limité", "IA Act art. 50 — transparence"],
    ["5", "Noter les salariés à partir de leurs publications sur les réseaux sociaux.", "<b>Interdit</b>", "IA Act art. 5 — notation sociale"],
    ["6", "Attribuer automatiquement les tâches et les tournées de chaque salarié.", "Haut risque", "Annexe III — répartition des tâches"],
    ["7", "Le correcteur orthographique intégré au traitement de texte.", "Minimal", "Usage libre"],
    ["8", "Générer une image d'équipe pour la plaquette commerciale.", "Limité", "Art. 50 — marquage du contenu généré"],
    ["9", "Présélectionner les salariés à promouvoir cette année.", "Haut risque", "Annexe III + RGPD art. 22"],
    ["10", "Traduire les consignes de sécurité en trois langues.", "Minimal", "Relecture humaine indispensable"],
    ["11", "Surveiller en continu la productivité individuelle et déclencher des alertes.", "Haut risque", "Annexe III + proportionnalité (CNIL)"],
    ["12", "Imiter la voix du dirigeant pour un message vidéo interne, sans le préciser.", "Limité", "Art. 50 — obligation de révéler"]],
    [8*mm, None, 22*mm, 40*mm])]
f += [E(2), encadre("Les trois cartes qui divisent toujours", [
   "Carte 10 : « minimal » ne veut pas dire « sans relecture ». Une consigne de sécurité "
   "mal traduite engage l'obligation de sécurité de l'employeur (C. trav., art. L.4121-1).",
   "Carte 11 : beaucoup la classent « limité ». C'est du suivi de performance : haut risque, "
   "avec en plus la question de la proportionnalité du contrôle et la consultation du CSE.",
   "Carte 12 : techniquement « risque limité », mais le non-dit crée un risque social majeur. "
   "Rappeler que conformité minimale et bonne décision managériale ne se confondent pas."])]

f += [SAUT()]
# ------------------------------------------------------------------ J7 ----
f += fiche(7, "Le prompt qui fuit", "20 min", "15h25",
  "Transformer un usage risqué en usage conforme, et repérer ce qui ne doit jamais être saisi.",
  ["Le prompt « dangereux » projeté ou photocopié (ci-dessous)",
   "Un stylo par personne ; travail par binôme"],
  ["Projeter le prompt dangereux. Le lire à voix haute, sans commentaire.",
   "Consigne : « Par deux, entourez tout ce qui vous dérange. 5 minutes. »",
   "Recenser au tableau tout ce qui a été repéré, sans trier.",
   "Consigne : « Réécrivez-le en version conforme et utile. 7 minutes. »",
   "Deux binômes lisent leur version à voix haute.",
   "Projeter la version de référence et comparer, sans hiérarchiser."],
  ["Qu'est-ce qui rendait ce prompt dangereux : les données, ou la demande elle-même ?",
   "Auriez-vous écrit ce prompt un vendredi à 18 heures, sous pression ?",
   "Que faudrait-il mettre en place chez vous pour que personne ne l'écrive ?"])
f += [E(3), encadre("Le prompt dangereux — à projeter tel quel", [
   "« Voici mes notes sur Sandrine, 42 ans, technicienne, en arrêt maladie depuis trois "
   "semaines pour dépression. Elle est en conflit ouvert avec son chef d'équipe et son "
   "conjoint vient de perdre son emploi. Rédige-moi un argumentaire pour justifier de ne "
   "pas la reconduire sur le poste, et dis-moi si je peux la licencier. »"],
   coul=ROUGE, fond=colors.HexColor("#FBEAEA"))]
f += [E(3), H2("Corrigé — ce qui doit être repéré"),
  tableau([
    ["Ce qui cloche", "Pourquoi"],
    ["Identité et âge", "Données personnelles directement identifiantes, sans nécessité pour la tâche."],
    ["Arrêt maladie et dépression", "Donnée de santé : catégorie particulière, protégée par l'article 9 du RGPD."],
    ["Situation du conjoint", "Vie privée d'un tiers qui n'a rien demandé. Aucune finalité légitime."],
    ["« Justifier de ne pas la reconduire »", "La décision est déjà prise : on demande à l'outil de fabriquer une justification."],
    ["Lien avec l'état de santé", "Risque de discrimination : l'état de santé est un critère prohibé (C. trav., art. L.1132-1)."],
    ["« Dis-moi si je peux la licencier »", "Conseil juridique individualisé demandé à un outil qui peut halluciner."],
    ["L'usage lui-même", "Décision concernant une personne : haut risque (annexe III) + RGPD art. 22."]],
    [56*mm, None])]
f += [E(3), encadre("Version de référence — conforme et réellement utile", [
   "« Tu es responsable des ressources humaines dans une PME de 40 personnes.",
   "Contexte : un poste de technicien arrive au terme d'une mission de remplacement. "
   "Aucune décision n'est prise à ce stade.",
   "Tâche : liste les étapes légales et les points de vigilance d'un entretien de fin de "
   "mission, ainsi que les éléments objectifs qu'il est licite de prendre en compte.",
   "Format : 8 points maximum, ton factuel, sans jargon.",
   "Contrainte : je ne te transmets aucune donnée nominative ni aucune information de santé.",
   "Si une information te manque, pose-moi la question au lieu de l'inventer. »"],
   coul=VERT, fond=colors.HexColor("#E8F3EC"))]
f += [E(2), P("<b>Le message central :</b> on ne demande jamais à une IA de justifier une "
              "décision déjà prise sur une personne. On lui demande de préparer un "
              "raisonnement que l'on vérifiera soi-même.", "petit")]

f += [SAUT()]
# ------------------------------------------------------------------ J8 ----
f += fiche(8, "Mon chantier IA", "20 min", "16h20 — évaluation",
  "Repartir avec un usage conforme, testé, et un plan applicable dès la semaine suivante.",
  ["La fiche « Mon chantier IA » ci-dessous, une par stagiaire",
   "Un téléphone ou un ordinateur par binôme (facultatif)",
   "La grille d'évaluation n°2 pour le formateur"],
  ["Consigne : « Listez vos tâches répétitives de la semaine dernière. 3 minutes. »",
   "Entourer celle qui coûte le plus de temps pour le moins de valeur.",
   "Passer les trois réflexes (données / décision sur une personne / hébergement).",
   "Rédiger le prompt en quatre blocs sur la fiche.",
   "Tester si possible, puis améliorer une fois.",
   "Présentation de 60 secondes devant le groupe, évaluée avec la grille n°2."],
  ["Qu'est-ce qui vous a fait renoncer à un usage ? C'est une bonne nouvelle : dites pourquoi.",
   "Combien de temps par semaine ce chantier vous fait-il gagner, vérification comprise ?",
   "Qui doit être informé avant que vous ne lanciez ce chantier lundi ?"])
f += [E(3), H2("Fiche « Mon chantier IA » — à photocopier"),
  tableau([
    ["La tâche que je veux alléger", ""],
    ["Temps qu'elle me coûte par semaine", ""],
    ["Réflexe 1 — Données personnelles en jeu ?", ""],
    ["Réflexe 2 — Décision concernant une personne ?", ""],
    ["Réflexe 3 — Où sont traitées les données ?", ""],
    ["Niveau de risque retenu (IA Act)", ""],
    ["Mon prompt — Rôle", ""],
    ["Mon prompt — Contexte", ""],
    ["Mon prompt — Tâche", ""],
    ["Mon prompt — Format", ""],
    ["Ce que je vérifierai systématiquement", ""],
    ["Qui j'informe avant de lancer", ""],
    ["Je commence le (date)", ""]],
    [72*mm, None], entete=False)]
f += [E(3), P("Conserver les fiches renseignées : elles constituent, avec l'émargement et le "
              "programme, un commencement de preuve utile au titre de l'article 4 de l'IA Act.", "petit")]

doc = document("../03_jeux/Kit_jeux_et_exercices.pdf",
               "Kit de jeux et d'exercices — document animateur",
               "8 séquences actives, cartes à découper, corrigés et débriefs")
doc.build(f)
print("Kit jeux : OK")
