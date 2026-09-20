# -*- coding: utf-8 -*-
from docs_engine import *

f = [H1("Conducteur d'animation — journée complète"),
     P("Document formateur. Horaires, diapositives, matériel et points de vigilance."),
     E(3)]
f += [encadre("Cadre de la journée", [
    "Horaires : 8h00 → 17h00. Déjeuner 12h00 → 13h00.",
    "Pauses de 15 minutes à 10h00 et à 15h00.",
    "Temps de face-à-face pédagogique : 7 h 30 (8 h moins les deux pauses).",
    "Matin : la psychologie du dirigeant. Après-midi : IA et responsabilité en entreprise.",
    "Deux évaluations formatives (grilles n°1 et n°2) et deux quiz de 10 questions."])]
f += [E(3), encadre("Point à valider avec le commanditaire", [
    "La commande mentionne 7 heures de formation ; le créneau 8h00-17h00 avec une heure de "
    "déjeuner et deux pauses de 15 minutes représente 7 h 30 de face-à-face.",
    "Deux options : conserver 7 h 30 et le mentionner sur la convention, ou retirer 30 minutes "
    "(le plus simple : réduire le jeu n°4 à un seul passage et le jeu n°8 à 15 minutes).",
    "À trancher avant l'édition du programme et de la feuille d'émargement."],
    coul=ACCENT, fond=colors.HexColor("#FCEFE7"))]

def seq(donnees, titre):
    return [E(4), H2(titre),
            tableau([["Horaire", "Séquence", "Ce que fait le formateur", "Support"]] + donnees,
                    [22*mm, 38*mm, None, 28*mm])]

f += seq([
 ["8h00\n8h20", "Ouverture, cadre, objectifs",
  "Accueil, tour de table éclair (prénom + une attente en 10 secondes). Pose du cadre. "
  "Demande explicite des besoins d'accessibilité. Lance le jeu n°1.", "Diapos 1 à 5"],
 ["8h20\n9h00", "Dans la tête du dirigeant",
  "Apport : charge, confidentialité, décision en information incomplète, double loyauté. "
  "Fait réagir sur la colonne « on croit / réalité ».", "Diapos 6 à 11"],
 ["9h00\n9h45", "Ni ami, ni ennemi",
  "Diffuse la vidéo n°1 (2 min 30) puis développe les trois positions. Exercice éclair : "
  "reformuler les trois phrases qui coûtent cher.", "Diapos 12 à 16 + vidéo 1"],
 ["9h45\n10h00", "Les styles : introduction",
  "Pose les quatre styles et l'erreur la plus fréquente. Annonce le jeu de la reprise.", "Diapos 17 à 19"],
 ["10h00\n10h15", "PAUSE", "Prépare les 4 affiches styles dans les coins de la salle.", "—"],
 ["10h15\n10h35", "Jeu n°2 — Les quatre coins",
  "Anime les 8 situations au rythme soutenu. Ne commente pas longuement entre deux.", "Kit jeux, fiche J2"],
 ["10h35\n11h05", "Exigence et toxicité",
  "Apport puis jeu n°3 (cartes). Fait émerger trois critères et les affiche pour la journée. "
  "Traite le volet juridique sans dramatiser.", "Diapos 20 à 25 + fiche J3"],
 ["11h05\n11h20", "Langage, posture, réunion",
  "Trois canaux, posture en 5 points, DESC, réunion avant/pendant, profils difficiles. "
  "Fait tester la posture debout, 60 secondes.", "Diapos 26 à 32"],
 ["11h20\n11h50", "Jeu n°4 — La réunion de 9h",
  "Distribue les rôles, lance 8 minutes chrono, débrief avec la grille n°1. "
  "Deux passages si le groupe est nombreux.", "Fiche J4 + grille n°1"],
 ["11h50\n12h00", "Quiz n°1 et synthèse",
  "Distribue le quiz n°1 (10 min, documents fermés). Ramasse. La correction se fera à 13h.",
  "Quiz n°1"]], "Matin — la psychologie du dirigeant")

f += [SAUT()]
f += seq([
 ["13h00\n13h15", "Reprise et correction",
  "Corrige le quiz n°1 avec le corrigé (5 min), puis lance le jeu n°5 debout pour relancer "
  "l'énergie digestive.", "Corrigé quiz 1 + fiche J5"],
 ["13h15\n13h50", "Comprendre l'IA sans jargon",
  "Explique la prédiction du mot suivant. Fait vivre une hallucination en direct si un outil "
  "est disponible. Présente les trois pièges.", "Diapos 35 à 39"],
 ["13h50\n14h20", "RGPD pour responsables",
  "Les six réflexes, le piège du consentement, les limites de la surveillance, l'article 22. "
  "Rythme soutenu : c'est un passage, pas un cours de droit.", "Diapos 40 à 44"],
 ["14h20\n14h30", "IA Act : architecture",
  "Diffuse la vidéo n°2 (2 min 45) puis pose les quatre niveaux.", "Diapos 45 à 47 + vidéo 2"],
 ["14h30\n14h50", "Jeu n°6 — Le tri des risques",
  "12 cartes, 4 zones. Corrige en citant l'article, jamais un avis personnel.", "Fiche J6"],
 ["14h50\n15h00", "Interdits, haut risque, article 4",
  "Insiste sur l'article 4 : c'est l'argument qui justifie cette journée. "
  "Mentionne les sanctions sans en faire le sujet.", "Diapos 48 à 52"],
 ["15h00\n15h15", "PAUSE", "Vérifie le matériel du jeu n°7 et projette le prompt dangereux.", "—"],
 ["15h15\n15h45", "Responsabilité du déployeur",
  "Les cinq devoirs, la supervision humaine réelle, les trois réflexes. Puis jeu n°7.",
  "Diapos 54 à 57 + fiche J7"],
 ["15h45\n16h20", "L'IA qui rend du temps",
  "Usages concrets, prompt en 4 blocs, question de la souveraineté. Laisse les participants "
  "citer leurs propres tâches.", "Diapos 58 à 62"],
 ["16h20\n16h40", "Jeu n°8 — Mon chantier IA",
  "Atelier individuel puis présentations de 60 secondes, évaluées avec la grille n°2.",
  "Fiche J8 + grille n°2"],
 ["16h40\n16h50", "Quiz n°2", "Distribue, 10 minutes, documents fermés. Ramasse.", "Quiz n°2"],
 ["16h50\n17h00", "Correction, plan 30 jours, clôture",
  "Corrige le quiz n°2 en 4 minutes. Chacun énonce une action à voix haute. "
  "Évaluation à chaud et émargement.", "Corrigé quiz 2 + diapos 63 à 69"]],
 "Après-midi — IA et responsabilité en entreprise")

f += [SAUT(), H2("Matériel à préparer la veille")]
f += [tableau([
 ["Support", "Quantité", "Remarque"],
 ["Diaporama (69 diapositives)", "1", "Tester la projection et le contraste dans la salle réelle"],
 ["Vidéos 1 et 2 (fichiers HTML)", "2", "Lecture hors ligne dans un navigateur, plein écran"],
 ["Fiche ressource n°1 et n°2", "1 jeu par stagiaire", "Imprimer en recto simple, corps 13 pt"],
 ["Quiz n°1 et n°2", "1 par stagiaire", "Ne pas distribuer avec les corrigés"],
 ["Corrigés 1 et 2", "1 pour le formateur", "Feuilles distinctes, à garder"],
 ["Grilles n°1 et n°2", "1 par observateur", "Prévoir large pour le jeu n°4"],
 ["Kit jeux — cartes J3, J4, J6", "1 jeu pour 4 stagiaires", "À découper avant la session"],
 ["Affiches A3", "4 styles + 4 risques + VRAI/FAUX", "Gros caractères, noir sur blanc"],
 ["Ruban adhésif, chronomètre visible, marqueurs", "—", "Chronomètre projeté si possible"]],
 [56*mm, 42*mm, None])]

f += [E(4), H2("Accessibilité — vérifications avant l'ouverture")]
f += puces([
 "Demander en ouverture, devant tout le groupe, si quelqu'un a un besoin particulier.",
 "Lire à voix haute toute carte distribuée et tout élément projeté : personne ne doit "
 "dépendre de sa seule vue pour suivre.",
 "Proposer systématiquement une variante assise aux jeux en déplacement (jeux 1, 2, 5, 6).",
 "Vérifier l'éclairage : ne pas éteindre complètement, le contraste du diaporama le permet.",
 "Placer les personnes malvoyantes au premier rang, face à l'écran, avant qu'elles ne le demandent.",
 "Disposer des exemplaires papier des diapositives clés pour lecture de près."])

f += [E(4), H2("Points de vigilance d'animation")]
f += puces([
 "<b>8h00</b> : ne pas commencer par le contenu. Le cadre et le jeu n°1 conditionnent toute la journée.",
 "<b>Matin</b> : le sujet touche les vécus. Si un participant raconte une situation personnelle "
 "difficile, accueillir brièvement, ne pas instruire le cas, proposer un temps à la pause.",
 "<b>Jeu n°4</b> : ne jamais laisser les observateurs commenter la personnalité. "
 "Recentrer sur un fait observé dès la première dérive.",
 "<b>13h00</b> : le créneau digestif est le plus difficile. Le jeu n°5 debout n'est pas optionnel.",
 "<b>Après-midi</b> : résister à la tentation du cours de droit. Une référence par notion, pas plus.",
 "<b>Questions juridiques individuelles</b> : rappeler que la formation n'est pas un conseil "
 "juridique personnalisé et renvoyer vers un conseil compétent.",
 "<b>16h50</b> : faire énoncer chaque plan d'action à voix haute. L'engagement public triple le passage à l'acte."])

f += [E(4), H2("Après la session")]
f += puces([
 "Conserver : émargement, programme, quiz renseignés, grilles, fiches « Mon chantier IA ».",
 "Ces pièces documentent à la fois l'action de formation et, pour le commanditaire, "
 "l'effort de littératie en matière d'IA attendu par l'article 4 du règlement (UE) 2024/1689.",
 "Transmettre au commanditaire une synthèse anonymisée des résultats aux deux quiz.",
 "Point de vigilance RGPD : les copies de quiz comportent des données personnelles "
 "(nom, résultat). Définir une durée de conservation et l'annoncer aux stagiaires."])

doc = document("../08_conducteur/Conducteur_animation_journee.pdf",
               "Conducteur d'animation — journée complète",
               "8h00-17h00 — minutage, supports, matériel, vigilances")
doc.build(f)
print("Conducteur : OK")
