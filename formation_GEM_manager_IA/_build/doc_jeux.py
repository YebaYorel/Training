# -*- coding: utf-8 -*-
from docs_engine import *
from reportlab.platypus import Table, TableStyle, Paragraph

def fiche(num, nom, duree, moment, objectif, materiel, deroule, debrief, extra=None):
    b = [H1("Jeu n°%d — %s" % (num, nom))]
    b += [tableau([["Durée", "Moment", "Objectif pédagogique"],
                   [duree, moment, objectif]], [22*mm, 30*mm, None])]
    b += [E(3), H2("Matériel et dispositif à distance"), *puces(materiel)]
    b += [E(2), H2("Déroulé"), *numerote(deroule)]
    if extra:
        b += extra
    b += [E(2), H2("Débrief — les questions à poser"), *puces(debrief)]
    return b

f = [H1("Kit de jeux et d'exercices — document animateur"),
     P("Huit séquences actives, toutes conçues <b>pour la visioconférence</b>. "
       "Chaque fiche est autonome : dispositif technique, déroulé minuté, corrigé et débrief."),
     E(3),
     encadre("Les sept règles de l'animation à distance", [
        "<b>Jamais plus de 15 minutes sans interaction.</b> À distance, l'attention décroche "
        "deux fois plus vite qu'en présentiel.",
        "<b>Nommer les gens.</b> « Qui veut répondre ? » ne produit rien. « Karim, ton avis ? » produit une réponse.",
        "<b>Compter jusqu'à cinq</b> après chaque question : la latence technique et sociale s'additionnent.",
        "<b>Annoncer la durée ET le signal de retour</b> avant chaque envoi en salle séparée.",
        "<b>Passer dans les salles séparées</b> : un groupe non visité décroche en trois minutes.",
        "<b>Tout dire à voix haute.</b> Ce qui n'est écrit qu'à l'écran est perdu pour qui voit mal.",
        "<b>Prévoir le repli</b> : si les salles séparées échouent, tout jeu se rabat sur le tchat "
        "en plénière. Les variantes sont indiquées fiche par fiche."]),
     E(3),
     encadre("Accessibilité — public malvoyant à distance", [
        "Le partage d'écran dégrade la netteté : <b>envoyez le diaporama et les fiches en PDF "
        "la veille</b>, pour que chacun suive sur son propre écran, à son propre zoom.",
        "Annoncez toujours le numéro de la diapositive à voix haute.",
        "Aucun jeu ne repose sur une couleur seule : chaque élément porte aussi un mot ou un numéro.",
        "Aucun jeu n'exige de lire un document partagé en temps réel sans l'avoir reçu avant."],
        coul=VERT, fond=PALE_VERT),
     SAUT()]

# ------------------------------------------------------------------ J1 ----
f += fiche(1, "Le thermomètre", "15 min", "9h05",
  "Faire émerger les représentations du groupe sur la place du chef, sans débat.",
  ["Le tchat de la visioconférence, rien d'autre.",
   "Une diapositive affichant la règle de 0 à 10."],
  ["Afficher la règle : 0 = « mon chef est un ami », 10 = « mon chef est un adversaire ».",
   "Annoncer : « Un seul chiffre dans le tchat. Il n'y a pas de bonne réponse. »",
   "Attendre que tout le monde ait écrit. Relancer nommément les silencieux.",
   "Lire à voix haute la dispersion : « trois personnes à 2, une à 9… »",
   "Interroger trois volontaires : « pourquoi ce chiffre et pas deux de plus ? »",
   "Interdire tout débat. Conclure : « Retenez votre chiffre, on y revient à 12h20. »"],
  ["Qu'est-ce qui vous a fait hésiter entre deux chiffres ?",
   "Votre chiffre décrit-il votre chef actuel, ou le chef que vous voulez devenir ?",
   "Qui a vu les réponses des autres avant d'écrire la sienne ? Qu'est-ce que ça dit d'une équipe ?"],
  extra=[E(2), encadre("Variante si le tchat est indisponible", [
     "Chacun montre son chiffre avec les doigts face caméra (deux mains = jusqu'à 10).",
     "Effet de groupe conservé, et tout le monde se voit répondre en même temps."])])

f += [SAUT()]
# ------------------------------------------------------------------ J2 ----
f += fiche(2, "Les quatre numéros", "20 min", "10h45",
  "Choisir le style managérial adapté à une situation de magasin, sous contrainte de temps.",
  ["Diapositive rappelant en permanence : 1 Directif – 2 Persuasif – 3 Participatif – 4 Délégatif.",
   "Le tchat, ou la fonction sondage de la visio si elle existe.",
   "Les 8 situations ci-dessous (animateur uniquement)."],
  ["Afficher la légende des quatre numéros et la laisser à l'écran tout le jeu.",
   "Lire la situation à voix haute, deux fois, lentement.",
   "« 10 secondes : un chiffre dans le tchat, pas de phrase. »",
   "Choisir deux personnes ayant répondu différemment : 20 secondes de justification chacune.",
   "Révéler le style attendu et, surtout, le critère qui tranche.",
   "Enchaîner les 8 situations sans commenter longuement."],
  ["Sur quelle situation le groupe s'est-il le plus divisé ? Pourquoi ?",
   "Quel numéro avez-vous choisi le plus souvent ? C'est votre style par défaut.",
   "Quel numéro n'avez-vous jamais choisi ? C'est votre angle mort."])
f += [E(3), H2("Les 8 situations et le style attendu — document animateur"),
  tableau([
    ["N°", "Situation lue à voix haute", "Attendu", "Critère qui tranche"],
    ["1", "Samedi 11h. Deux caisses tombent en panne, vingt clients attendent.",
     "1 Directif", "Urgence + client en attente"],
    ["2", "Une saisonnière, deuxième jour, doit utiliser le transpalette électrique.",
     "1 Directif", "Sécurité + compétence faible"],
    ["3", "Le siège impose un nouveau plan de rayon. L'équipe est en colère.",
     "2 Persuasif", "Décision non négociable, sens à donner"],
    ["4", "Nouveau logiciel d'encaissement. Personne n'en voit l'intérêt.",
     "2 Persuasif", "Résistance + adhésion à construire"],
    ["5", "Il faut répartir les samedis de décembre entre six vendeurs.",
     "3 Participatif", "Compétence présente + acceptabilité déterminante"],
    ["6", "Deux vendeurs expérimentés sont démotivés depuis le départ du chef de rayon.",
     "3 Participatif", "Compétence haute, motivation basse"],
    ["7", "Votre adjoint, autonome depuis quatre ans, prépare l'inventaire annuel.",
     "4 Délégatif", "Autonomie avérée sur cette tâche"],
    ["8", "Un vendeur senior demande à piloter seul l'opération promo qu'il a déjà menée trois fois.",
     "4 Délégatif", "Demande + historique de réussite"]],
    [8*mm, None, 24*mm, 42*mm])]
f += [E(2), P("<b>Message de synthèse à faire émerger :</b> ce n'est jamais la personne qui "
              "détermine le style, c'est le couple personne + tâche + urgence.", "petit")]

f += [SAUT()]
# ------------------------------------------------------------------ J3 ----
f += fiche(3, "Exigeant ou toxique ?", "20 min", "11h15",
  "Construire collectivement le critère qui sépare l'exigence de la toxicité.",
  ["Salles séparées de 4 personnes maximum.",
   "La fiche des 12 situations, <b>envoyée en PDF la veille</b> (ne pas découvrir à l'écran).",
   "Un tableau à trois colonnes à remplir : EXIGEANT / LIMITE / TOXIQUE.",
   "Un rapporteur désigné par salle, annoncé avant l'envoi."],
  ["Annoncer : « 10 minutes, retour automatique, un rapporteur par groupe. »",
   "Envoyer en salles séparées. Passer dans chaque salle au moins une fois.",
   "À 8 minutes, diffuser le message : « Deux minutes, choisissez votre situation LIMITE. »",
   "Retour en plénière. Chaque rapporteur présente uniquement sa situation « limite ».",
   "Noter à l'écran les critères invoqués, sans trier.",
   "Retenir trois critères et les laisser affichés jusqu'à la fin de la journée."],
  ["Quelle situation a provoqué le plus de désaccord dans votre salle ?",
   "Un même comportement peut-il être exigeant avec l'un et toxique avec l'autre ?",
   "Qu'est-ce qui change tout : l'intention du manager, ou l'effet sur la personne ?"])
f += [E(3), H2("Les 12 situations et leur classement — document animateur"),
  tableau([
    ["N°", "Situation", "Classement"],
    ["1", "Le manager reprend une vendeuse en réserve, 24 heures après, en décrivant les faits.", "Exigeant"],
    ["2", "Devant deux clients, le manager lance : « Encore une fois, le rayon n'est pas fait. »", "Toxique"],
    ["3", "Un point d'avancement chaque vendredi, fixé dès le lancement de l'opération.", "Exigeant"],
    ["4", "Le manager vient vérifier le facing six fois dans la journée, sans l'avoir annoncé.", "Toxique"],
    ["5", "Il refuse un samedi de repos en expliquant la règle, la même pour toute l'équipe.", "Exigeant"],
    ["6", "Depuis un désaccord, il ne salue plus un vendeur : trois jours que ça dure.", "Toxique"],
    ["7", "Il fixe un objectif de chiffre ambitieux puis demande : « qu'est-ce qu'il te manque ? »", "Exigeant"],
    ["8", "Il change le plan de rayon tous les deux jours, sans jamais expliquer pourquoi.", "Toxique"],
    ["9", "« Je sais que tu peux faire mieux : refais-moi cette vitrine pour jeudi. »", "Exigeant"],
    ["10", "Il plaisante sur la façon de parler d'un vendeur, devant toute l'équipe.", "Toxique"],
    ["11", "Il écrit sur le groupe de l'équipe à 23 heures. Il n'attend pas de réponse, mais ne l'a jamais dit.", "<b>Limite</b>"],
    ["12", "Au brief du matin, il félicite systématiquement le même vendeur.", "<b>Limite</b>"]],
    [8*mm, None, 26*mm])]
f += [E(2), encadre("Clé de lecture à donner après le débat", [
   "Situation 11 : ce n'est pas l'horaire qui pose problème, c'est le non-dit. Une règle explicite "
   "(« j'écris tard, personne ne répond avant l'ouverture ») la fait basculer côté exigeant. "
   "À relier au droit à la déconnexion.",
   "Situation 12 : l'intention est bonne, l'effet est un favoritisme perçu. C'est l'effet qui compte.",
   "Les trois critères à faire émerger : l'objet de la critique (fait ou personne), le lieu "
   "(privé ou devant l'équipe et les clients), l'existence d'une issue."])]

f += [SAUT()]
# ------------------------------------------------------------------ J4 ----
f += fiche(4, "Le brief de 8h", "30 min", "11h50 — évaluation",
  "Se mettre en situation réelle d'animation sous tension, et se voir évaluer sur des faits.",
  ["Quatre rôles envoyés <b>en message privé</b> dans le tchat, juste avant de commencer.",
   "Un chronomètre visible : partagez une fenêtre de minuterie, ou annoncez les minutes à voix haute.",
   "La grille d'évaluation n°1, envoyée en PDF la veille à tous les observateurs.",
   "Caméras vivement encouragées : sans visage, l'exercice perd son sens. Un stagiaire qui refuse prend un rôle d'observateur, jamais une sanction."],
  ["Désigner un manager volontaire et quatre joueurs de rôle. Les autres observent.",
   "Envoyer les quatre rôles en message privé : personne ne connaît le rôle des autres.",
   "Briefer le manager à voix haute (encadré ci-dessous), devant tout le monde.",
   "Lancer 8 minutes. Ne jamais interrompre, même si ça dérape.",
   "Stopper net à 8 minutes, même si le brief n'est pas conclu.",
   "Débrief de 10 minutes : le manager d'abord, les rôles ensuite, les observateurs en dernier.",
   "Deuxième passage avec un autre manager si l'effectif et le temps le permettent."],
  ["Manager : à quel moment avez-vous senti que vous perdiez le groupe ?",
   "Joueurs : à quel moment précis vous êtes-vous senti écouté ? Et ignoré ?",
   "Observateurs : citez un fait, jamais une impression.",
   "Que feriez-vous différemment dans les 60 premières secondes ?"])
f += [E(3), encadre("Brief du manager — à lire à voix haute", [
   "Vous êtes responsable d'un rayon et de quatre vendeurs.",
   "Le siège impose le planning des fêtes : ouverture élargie, deux samedis supplémentaires, "
   "repos déplacés. Ce n'est pas négociable.",
   "Vous n'avez pas choisi cette décision et vous n'êtes pas d'accord avec la méthode.",
   "Vous avez 8 minutes pour annoncer, entendre l'équipe et repartir avec des engagements."])]
f += [E(3), H2("Les quatre rôles — à copier en message privé")]
for titre_r, texte_r in [
  ("RÔLE 1 — LE BAVARD",
   "Vous parlez beaucoup et vous partez souvent du sujet. Vous racontez une anecdote client dès "
   "que vous le pouvez. Vous n'êtes pas de mauvaise foi : vous aimez sincèrement échanger. "
   "Si le manager vous cadre avec respect, vous acceptez volontiers."),
  ("RÔLE 2 — LE SCEPTIQUE",
   "Vous objectez sur chaque point : « ça ne marchera pas », « on a déjà essayé l'an dernier ». "
   "Vous avez de vraies raisons : le dernier changement de planning s'est mal passé. Si le manager "
   "vous demande ce qu'il vous faudrait pour y croire, vous donnez une condition précise."),
  ("RÔLE 3 — LE SILENCIEUX",
   "Vous ne dites rien, sauf si on vous interroge nommément et sur un point précis. "
   "Vous êtes en réalité le plus impacté : les nouveaux horaires sont incompatibles avec "
   "votre mode de garde. Vous ne le direz que si on vous met en confiance."),
  ("RÔLE 4 — LE DÉMOTIVÉ",
   "Vous soupirez, vous coupez votre caméra un instant, vous lancez des piques : « de toute "
   "façon… ». Si le manager vous prend à partie devant les autres, vous vous braquez. S'il vous "
   "propose un point en privé après le brief, vous acceptez.")]:
    f += [encadre(titre_r, [texte_r], coul=ACCENT, fond=PALE_ACCENT), E(2)]
f += [E(1), encadre("Si l'exercice dérape", [
   "Un joueur qui sur-joue empêche l'évaluation : coupez et rappelez « jouez juste, pas fort ».",
   "Un manager en difficulté réelle : arrêtez à 5 minutes et débriefez sur ce qui a déjà marché. "
   "On n'humilie jamais un stagiaire pour tenir un minutage."], coul=ROUGE, fond=PALE_ROUGE)]

f += [SAUT()]
# ------------------------------------------------------------------ J5 ----
f += fiche(5, "Vrai ou faux", "15 min", "13h30 — reprise",
  "Relancer l'énergie après le déjeuner et mesurer les idées reçues sur l'IA.",
  ["Aucun matériel. Caméras encouragées ; réponse dans le tchat pour qui n'en a pas.",
   "Les 6 affirmations ci-dessous."],
  ["Faire lever tout le monde : « debout, on se met bien dans le cadre. »",
   "Lire l'affirmation, deux fois. « 5 secondes : pouce levé pour vrai, pouce baissé pour faux. »",
   "Interdire le pouce horizontal : trancher fait partie de l'exercice.",
   "Interroger une personne de chaque camp, 15 secondes chacune.",
   "Donner la réponse ET la source. Enchaîner immédiatement.",
   "Rester debout jusqu'à la fin des 6 affirmations."],
  ["Quelle réponse vous a le plus surpris ?",
   "Laquelle de ces croyances circule dans votre magasin ?",
   "Qui, chez vous, devrait entendre ces six réponses ?"])
f += [E(3), tableau([
    ["Affirmation lue", "Réponse", "À dire immédiatement après"],
    ["« L'IA Act interdit d'utiliser l'IA générative en magasin. »", "FAUX",
     "Il encadre les usages selon leur risque. La plupart des usages de bureau sont à risque minimal."],
    ["« Une IA peut inventer un article de loi qui n'existe pas. »", "VRAI",
     "C'est l'hallucination : une référence plausible et fausse. Toujours vérifier à la source."],
    ["« Trier des CV de saisonniers avec une IA est un usage à haut risque. »", "VRAI",
     "Emploi et gestion de la main-d'œuvre : annexe III de l'IA Act."],
    ["« Si mes données sont hébergées en France, la souveraineté est assurée. »", "FAUX",
     "Le lieu ne suffit pas : il faut regarder le droit auquel l'éditeur est soumis."],
    ["« Je suis obligé de former mon équipe à l'IA qu'elle utilise. »", "VRAI",
     "IA Act, article 4, applicable depuis le 2 février 2025. Aucune exemption de taille."],
    ["« Analyser le sourire des hôtesses de caisse est permis si on les prévient. »", "FAUX",
     "Pratique interdite (art. 5). Aucune information ni aucun accord ne la rend licite."]],
    [None, 20*mm, 60*mm])]

f += [SAUT()]
# ------------------------------------------------------------------ J6 ----
f += fiche(6, "Le tri des risques", "20 min", "15h30",
  "Savoir classer un usage d'IA avant de l'autoriser, en justifiant par l'usage.",
  ["Salles séparées de 4 personnes.",
   "La fiche des 12 usages, <b>envoyée en PDF la veille</b>, avec une colonne vide à remplir.",
   "Diapositive de rappel des 4 niveaux laissée affichée."],
  ["Rappeler les quatre niveaux et les laisser à l'écran.",
   "« 8 minutes en salles séparées, un rapporteur, une colonne remplie. »",
   "Passer dans chaque salle : la question « sur quoi bloquez-vous ? » suffit.",
   "Retour en plénière. Un groupe défend trois usages de son choix.",
   "Un autre groupe peut contester avant la correction.",
   "Corriger en citant l'article applicable, jamais en donnant un avis personnel."],
  ["Qu'est-ce qui vous a fait hésiter : l'outil ou l'usage ?",
   "Combien de ces usages existent déjà dans votre enseigne, sans avoir été qualifiés ?",
   "Qui, chez vous, devrait faire ce tri avant l'achat d'un outil ?"])
f += [E(3), H2("Les 12 usages et leur classement — document animateur"),
  tableau([
    ["N°", "Usage décrit sur la fiche", "Niveau", "Fondement"],
    ["1", "Une caméra analyse le sourire et l'humeur des hôtesses de caisse.", "<b>Interdit</b>", "IA Act art. 5 — émotions au travail"],
    ["2", "Trier automatiquement les 300 CV reçus pour les saisonniers.", "Haut risque", "Annexe III, pt 4"],
    ["3", "Résumer les notes du brief du matin, anonymisées.", "Minimal", "Aucun traitement à enjeu"],
    ["4", "Un agent conversationnel répond aux clients sur le site de l'enseigne.", "Limité", "IA Act art. 50 — transparence"],
    ["5", "Noter les vendeurs d'après leurs publications sur les réseaux sociaux.", "<b>Interdit</b>", "IA Act art. 5 — notation sociale"],
    ["6", "Générer automatiquement le planning hebdomadaire de l'équipe.", "Haut risque", "Annexe III — répartition des tâches"],
    ["7", "Le correcteur orthographique des étiquettes et affiches promo.", "Minimal", "Usage libre"],
    ["8", "Générer une photo d'équipe pour la page recrutement du site.", "Limité", "Art. 50 — marquage du contenu généré"],
    ["9", "Présélectionner les vendeurs à promouvoir chef de rayon.", "Haut risque", "Annexe III + RGPD art. 22"],
    ["10", "Traduire les consignes de sécurité incendie en trois langues.", "Minimal", "Relecture humaine indispensable"],
    ["11", "Mesurer le temps de présence de chaque vendeur en rayon et alerter.", "Haut risque", "Annexe III + proportionnalité (CNIL)"],
    ["12", "Cloner la voix du directeur pour un message vidéo interne, sans le dire.", "Limité", "Art. 50 — obligation de révéler"]],
    [8*mm, None, 22*mm, 40*mm])]
f += [E(2), encadre("Les trois usages qui divisent toujours", [
   "Usage 10 : « minimal » ne veut pas dire « sans relecture ». Une consigne de sécurité mal "
   "traduite engage l'obligation de sécurité de l'employeur (C. trav., art. L.4121-1).",
   "Usage 11 : beaucoup le classent « limité ». C'est du suivi de performance : haut risque, "
   "plus la proportionnalité du contrôle et la consultation du CSE.",
   "Usage 12 : techniquement « risque limité », mais le non-dit crée un risque social majeur. "
   "Conformité minimale et bonne décision managériale ne se confondent pas."])]
f += [E(2), encadre("Si un stagiaire pose la question des clients", [
   "L'interdiction de l'article 5 vise la reconnaissance des émotions <b>sur le lieu de travail</b> "
   "et dans l'enseignement. Elle ne couvre pas, au même titre, l'analyse des émotions des clients.",
   "Mais un tel dispositif reste un traitement de données biométriques : le RGPD s'applique "
   "pleinement (finalité, base légale, art. 9, information, analyse d'impact au titre de l'art. 35).",
   "Réponse honnête à donner : « ce n'est pas interdit au même titre, mais c'est très "
   "difficilement licite. Ne lancez pas ça sans conseil. »"], coul=ACCENT, fond=PALE_ACCENT)]

f += [SAUT()]
# ------------------------------------------------------------------ J7 ----
f += fiche(7, "Le prompt qui fuit", "20 min", "16h05",
  "Transformer un usage risqué en usage conforme, et repérer ce qui ne doit jamais être saisi.",
  ["Le prompt « dangereux » en partage d'écran <b>et</b> dans la fiche PDF envoyée la veille.",
   "Salles séparées de deux personnes.",
   "De quoi écrire : la réécriture se fait à la main ou dans un document, pas dans un outil d'IA."],
  ["Partager le prompt dangereux et le lire à voix haute, sans commentaire.",
   "« Par deux, 5 minutes : relevez tout ce qui vous dérange. »",
   "Retour : recenser à l'écran tout ce qui a été repéré, sans trier.",
   "« Repartez 7 minutes : réécrivez-le en version conforme et utile. »",
   "Deux binômes lisent leur version à voix haute.",
   "Afficher la version de référence et comparer, sans hiérarchiser."],
  ["Qu'est-ce qui rendait ce prompt dangereux : les données, ou la demande elle-même ?",
   "Auriez-vous écrit ce prompt un samedi à 19 heures, sous pression ?",
   "Que faudrait-il mettre en place chez vous pour que personne ne l'écrive ?"])
f += [E(3), encadre("Le prompt dangereux — à partager tel quel", [
   "« Voici mes notes sur Sandrine, 42 ans, hôtesse de caisse, en arrêt maladie depuis trois "
   "semaines pour dépression. Elle est en conflit ouvert avec sa chef de caisse et son conjoint "
   "vient de perdre son emploi. Rédige-moi un argumentaire pour justifier de ne pas renouveler "
   "son contrat, et dis-moi si je peux la licencier. »"], coul=ROUGE, fond=PALE_ROUGE)]
f += [E(3), H2("Corrigé — ce qui doit être repéré"),
  tableau([
    ["Ce qui cloche", "Pourquoi"],
    ["Identité, âge, poste", "Données personnelles directement identifiantes, sans nécessité pour la tâche."],
    ["Arrêt maladie et dépression", "Donnée de santé : catégorie particulière, protégée par l'article 9 du RGPD."],
    ["Situation du conjoint", "Vie privée d'un tiers qui n'a rien demandé. Aucune finalité légitime."],
    ["« Justifier de ne pas renouveler »", "La décision est déjà prise : on demande à l'outil de fabriquer une justification."],
    ["Lien avec l'état de santé", "Risque de discrimination : l'état de santé est un critère prohibé (C. trav., art. L.1132-1)."],
    ["« Dis-moi si je peux la licencier »", "Conseil juridique individualisé demandé à un outil qui peut halluciner."],
    ["L'usage lui-même", "Décision concernant une personne : haut risque (annexe III) + RGPD art. 22."]],
    [54*mm, None])]
f += [E(3), encadre("Version de référence — conforme et réellement utile", [
   "« Tu es responsable des ressources humaines dans une enseigne de 40 personnes.",
   "Contexte : un contrat à durée déterminée arrive à son terme sur un poste de caisse. "
   "Aucune décision n'est prise à ce stade.",
   "Tâche : liste les étapes légales et les points de vigilance d'un entretien de fin de contrat, "
   "ainsi que les éléments objectifs qu'il est licite de prendre en compte.",
   "Format : 8 points maximum, ton factuel, sans jargon.",
   "Contrainte : je ne te transmets aucune donnée nominative ni aucune information de santé.",
   "Si une information te manque, pose-moi la question au lieu de l'inventer. »"],
   coul=VERT, fond=PALE_VERT)]
f += [E(2), P("<b>Le message central :</b> on ne demande jamais à une IA de justifier une décision "
              "déjà prise sur une personne. On lui demande de préparer un raisonnement que l'on "
              "vérifiera soi-même.", "petit")]

f += [SAUT()]
# ------------------------------------------------------------------ J8 ----
f += fiche(8, "Mon chantier IA", "15 min", "16h35 — évaluation",
  "Repartir avec un usage conforme et un plan applicable dès la semaine suivante.",
  ["La fiche « Mon chantier IA », envoyée en PDF la veille.",
   "Travail individuel, caméra libre : c'est un temps de réflexion.",
   "La grille d'évaluation n°2 pour le formateur."],
  ["« Listez vos tâches répétitives de la semaine dernière. 3 minutes. »",
   "Entourer celle qui coûte le plus de temps pour le moins de valeur.",
   "Passer les trois réflexes (données / décision sur une personne / hébergement).",
   "Rédiger le prompt en quatre blocs sur la fiche.",
   "Trois volontaires présentent 60 secondes, évalués avec la grille n°2.",
   "Les autres déposent leur fiche complétée après la session : tous sont évalués."],
  ["Qu'est-ce qui vous a fait renoncer à un usage ? C'est une bonne nouvelle : dites pourquoi.",
   "Combien de temps par semaine ce chantier vous fait-il gagner, vérification comprise ?",
   "Qui doit être informé avant que vous ne lanciez ce chantier lundi ?"])
f += [E(3), H2("Fiche « Mon chantier IA » — à envoyer en PDF"),
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
f += [E(3), P("Conserver les fiches renseignées : avec l'émargement et le programme, elles "
              "constituent un commencement de preuve utile au titre de l'article 4 de l'IA Act.", "petit")]

doc = document("../03_jeux/Kit_jeux_et_exercices.pdf",
               "Kit de jeux et d'exercices — document animateur",
               "8 séquences actives en visioconférence — corrigés, débriefs et variantes de repli")
doc.build(f)
print("Kit jeux (version distancielle) : OK")
