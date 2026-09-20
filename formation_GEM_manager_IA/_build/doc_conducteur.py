# -*- coding: utf-8 -*-
from docs_engine import *

f = [H1("Conducteur d'animation — journée complète à distance"),
     P("Document formateur. Horaires, diapositives, dispositif technique et points de vigilance."),
     E(3)]
f += [encadre("Cadre de la journée", [
    "Modalité : <b>formation à distance</b>, en classe virtuelle synchrone.",
    "Horaires : 9h00 → 17h00. Déjeuner 12h30 → 13h30.",
    "Pauses de 15 minutes à 10h30 et à 15h15.",
    "<b>Durée de formation : 7 h 00</b> (9h-17h moins l'heure de déjeuner), pauses incluses.",
    "Public : stagiaires du titre professionnel Manager d'Établissement Marchand (MEM).",
    "Matin : la psychologie du dirigeant. Après-midi : IA et responsabilité en entreprise."])]
f += [E(3), encadre("Ce qui a changé avec le passage à distance", [
    "Tous les jeux en déplacement ont été reconçus : tchat, pouces face caméra, salles séparées.",
    "Les séquences d'apport ne dépassent jamais 15 minutes sans interaction.",
    "Les cartes à découper sont devenues des fiches PDF envoyées la veille.",
    "Une variante de repli est prévue pour chaque jeu si les salles séparées échouent.",
    "Le diaporama doit être <b>envoyé avant</b> : le partage d'écran dégrade la lisibilité."],
    coul=ACCENT, fond=PALE_ACCENT)]

def seq(donnees, titre):
    return [E(4), H2(titre),
            tableau([["Horaire", "Séquence", "Ce que fait le formateur", "Support"]] + donnees,
                    [22*mm, 34*mm, None, 26*mm])]

f += seq([
 ["8h30", "Ouverture de la salle",
  "Se connecte 30 minutes avant. Teste son, partage d'écran, salles séparées et lecture de la vidéo 1. "
  "Accueille les premiers arrivés.", "—"],
 ["9h00\n9h20", "Accueil, cadre, objectifs",
  "Tour de table éclair (prénom + une attente, 10 secondes chacun). Pose les règles à distance. "
  "Demande explicitement les besoins d'adaptation. Lance le jeu n°1.", "Diapos 1 à 6"],
 ["9h20\n9h55", "Dans la tête du dirigeant",
  "Apport : charge, confidentialité, décision en information incomplète, double loyauté. "
  "Fait réagir sur la colonne « on croit / réalité ».", "Diapos 7 à 12"],
 ["9h55\n10h30", "Ni ami, ni ennemi",
  "Diffuse la vidéo n°1 (2 min 30) puis développe les trois positions et le piège du chef sorti "
  "du rang. Exercice éclair dans le tchat.", "Diapos 13 à 18 + vidéo 1"],
 ["10h30\n10h45", "PAUSE", "Laisse la salle ouverte. Reste connecté : c'est là que viennent les questions gênantes.", "—"],
 ["10h45\n11h10", "Les styles + jeu n°2",
  "Pose les quatre styles, puis enchaîne les 8 situations de magasin au rythme soutenu.",
  "Diapos 19 à 22 + fiche J2"],
 ["11h10\n11h35", "Exigence et toxicité + jeu n°3",
  "Apport puis salles séparées (10 min). Fait émerger trois critères et les laisse affichés. "
  "Traite le volet juridique sans dramatiser.", "Diapos 23 à 28 + fiche J3"],
 ["11h35\n11h50", "Langage, posture, brief",
  "Trois canaux, posture en 5 points, la même en visio, DESC, brief avant/pendant, profils "
  "difficiles. Fait tester la posture debout, 60 secondes.", "Diapos 29 à 36"],
 ["11h50\n12h20", "Jeu n°4 — Le brief de 8h",
  "Envoie les rôles en message privé, lance 8 minutes, débrief avec la grille n°1. "
  "Deux passages si l'effectif le permet.", "Fiche J4 + grille n°1"],
 ["12h20\n12h30", "Quiz n°1",
  "Diffuse le quiz n°1 (PDF à remplir ou réponses dans le tchat privé). 10 minutes, documents fermés. "
  "Correction reportée à 13h30.", "Quiz n°1"]], "Matin — 9h00 à 12h30")

f += [SAUT()]
f += seq([
 ["13h30\n13h45", "Reprise et correction",
  "Corrige le quiz n°1 (5 min), puis lance le jeu n°5 debout : c'est le créneau le plus difficile "
  "de la journée, il ne se négocie pas.", "Corrigé quiz 1 + fiche J5"],
 ["13h45\n14h15", "Comprendre l'IA sans jargon",
  "Explique la prédiction du mot suivant. Montre une hallucination en direct si possible. "
  "Les trois pièges, puis le biais appliqué au tri des saisonniers.", "Diapos 40 à 45"],
 ["14h15\n14h45", "RGPD pour responsables",
  "Les six réflexes, le piège du consentement, les limites de la surveillance, l'article 22. "
  "Rythme soutenu : c'est un passage, pas un cours de droit.", "Diapos 46 à 51"],
 ["14h45\n15h15", "IA Act",
  "Diffuse la vidéo n°2 (2 min 55), pose les quatre niveaux, les interdits, le haut risque "
  "et l'article 4. Mentionne les sanctions sans en faire le sujet.", "Diapos 52 à 58 + vidéo 2"],
 ["15h15\n15h30", "PAUSE", "Prépare les salles séparées du jeu n°6 pendant la pause.", "—"],
 ["15h30\n15h50", "Jeu n°6 — Le tri des risques",
  "12 usages, 4 niveaux, salles séparées. Corrige en citant l'article, jamais un avis personnel.",
  "Fiche J6"],
 ["15h50\n16h15", "Responsabilité du déployeur + jeu n°7",
  "Les cinq devoirs, la supervision humaine réelle, les trois réflexes. Puis le prompt qui fuit.",
  "Diapos 60 à 63 + fiche J7"],
 ["16h15\n16h35", "L'IA qui rend du temps",
  "Usages concrets, prompt en 4 blocs, souveraineté. Laisse les stagiaires citer leurs propres tâches.",
  "Diapos 64 à 68"],
 ["16h35\n16h45", "Jeu n°8 — Mon chantier IA",
  "Atelier individuel, trois présentations de 60 secondes évaluées avec la grille n°2. "
  "Les autres fiches sont déposées après la session.", "Fiche J8 + grille n°2"],
 ["16h45\n16h55", "Quiz n°2", "Diffuse, 10 minutes, documents fermés.", "Quiz n°2"],
 ["16h55\n17h00", "Correction, plan, clôture",
  "Corrige en 3 minutes. Chacun énonce une action à voix haute, caméra allumée. "
  "Évaluation à chaud et émargement de fin.", "Corrigé quiz 2 + diapos 69 à 73"]],
 "Après-midi — 13h30 à 17h00")

f += [SAUT(), H2("Checklist technique")]
f += [H3("J–7 — une semaine avant"),
      *puces([
        "Envoyer le lien de connexion, les horaires et le programme détaillé.",
        "Envoyer le <b>diaporama en PDF</b> : chacun suivra sur son écran, à son propre zoom.",
        "Envoyer les fiches J2, J3, J6, J7, J8 et les deux grilles d'évaluation.",
        "Demander par retour : besoins d'adaptation, contraintes de connexion, effectif définitif.",
        "Indiquer le numéro ou l'adresse de l'<b>assistance technique</b> joignable le jour J."])]
f += [E(2), H3("J–1 — la veille"),
      *puces([
        "Relancer les stagiaires n'ayant pas confirmé leur connexion.",
        "Tester le partage d'une vidéo HTML avec le son : c'est le point qui casse le plus souvent.",
        "Vérifier la création et le retour automatique des salles séparées.",
        "Préparer les quatre messages privés du jeu n°4, prêts à coller.",
        "Préparer un partage de connexion mobile en secours."])]
f += [E(2), H3("Jour J — 30 minutes avant"),
      *puces([
        "Ouvrir la salle à 8h30. Tester micro, caméra, partage, son de la vidéo.",
        "Ouvrir déjà les deux vidéos dans des onglets séparés, prêtes à lancer.",
        "Afficher une diapositive d'accueil : horaires, règles, contact assistance.",
        "Vérifier que le tchat est ouvert à tous, y compris en message privé."])]

f += [E(3), encadre("Plan B — quand la technique lâche", [
    "<b>Un stagiaire ne se connecte pas</b> : l'assistance technique prend le relais pendant que "
    "vous continuez. Vous ne suspendez jamais le groupe pour une personne.",
    "<b>Les salles séparées échouent</b> : tout jeu se rabat sur le tchat en plénière. "
    "Les variantes sont écrites fiche par fiche dans le kit jeux.",
    "<b>La vidéo ne se partage pas avec le son</b> : vous la laissez défiler en muet et vous lisez "
    "le script voix off. C'est prévu, c'est même la modalité recommandée.",
    "<b>Votre connexion tombe</b> : les stagiaires restent en salle, vous revenez. "
    "Annoncez cette consigne dès 9h00 pour éviter la débandade.",
    "<b>Rupture longue</b> : basculer sur un rattrapage convenu avec le centre. "
    "Tracer l'incident et la mesure prise."], coul=ROUGE, fond=PALE_ROUGE)]

f += [SAUT(), H2("Accessibilité — vérifications spécifiques au distanciel")]
f += puces([
 "Demander en ouverture, devant tout le groupe, si quelqu'un a un besoin particulier.",
 "<b>Le point le plus important</b> : le diaporama a été envoyé avant. Le partage d'écran "
 "compresse l'image et ruine le travail fait sur la taille des caractères.",
 "Annoncer le numéro de chaque diapositive à voix haute : « diapositive 24, les dégâts côté équipe ».",
 "Lire à voix haute tout ce qui est écrit à l'écran, y compris le tchat et les consignes de jeu.",
 "Ne jamais désigner un élément par sa seule couleur : dire « la colonne de droite, exigeant ».",
 "Proposer la transcription automatique si l'outil en dispose, et vérifier qu'elle est activable.",
 "Vérifier que personne n'est contraint de suivre sur un téléphone : le proposer autrement si c'est le cas."])

f += [E(4), H2("Points de vigilance d'animation")]
f += puces([
 "<b>9h00</b> : ne pas commencer par le contenu. Le cadre et le jeu n°1 conditionnent toute la journée.",
 "<b>À distance, le silence n'est pas un accord.</b> Nommez, relancez, comptez jusqu'à cinq.",
 "<b>Matin</b> : le sujet touche des vécus. Si un stagiaire raconte une situation personnelle "
 "difficile, accueillir brièvement, ne pas instruire le cas, proposer un temps à la pause.",
 "<b>Public MEM</b> : ce sont de futurs responsables, souvent en alternance en magasin. Partez "
 "toujours d'une situation de rayon, de caisse ou de planning, jamais d'un exemple de bureau.",
 "<b>Jeu n°4</b> : ne jamais laisser les observateurs commenter la personnalité. Recentrer sur "
 "un fait observé dès la première dérive.",
 "<b>Après-midi</b> : résister à la tentation du cours de droit. Une référence par notion, pas plus.",
 "<b>Questions juridiques individuelles</b> : rappeler que la formation n'est pas un conseil "
 "juridique personnalisé et renvoyer vers un conseil compétent.",
 "<b>16h55</b> : faire énoncer chaque plan d'action à voix haute. L'engagement public triple le "
 "passage à l'acte — et à distance, il réveille le groupe une dernière fois."])

f += [E(4), H2("Après la session")]
f += puces([
 "Conserver : émargements, programme, quiz renseignés, grilles, fiches « Mon chantier IA », "
 "traces de connexion.",
 "Transmettre au centre une synthèse <b>anonymisée</b> des résultats aux deux quiz.",
 "Signaler tout incident technique et la mesure de rattrapage retenue : c'est attendu au titre "
 "de l'assistance technique en formation à distance.",
 "<b>Point de vigilance RGPD</b> : les copies de quiz et les grilles nominatives sont des données "
 "personnelles. Définir une durée de conservation, l'annoncer aux stagiaires, et ne transmettre "
 "au centre que ce qui lui est nécessaire.",
 "Voir le document « Dispositif à distance et conformité » pour le détail des obligations."])

doc = document("../08_conducteur/Conducteur_animation_journee.pdf",
               "Conducteur d'animation — journée à distance",
               "9h00-17h00 — minutage, dispositif technique, plan B, vigilances")
doc.build(f)
print("Conducteur (distanciel 9h-17h) : OK")
