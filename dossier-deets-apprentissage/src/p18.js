const rdv = require('./rdv');
const cal = require('./cal');
const h = cal.heures;
const hdr = ['Jour', '8 h 00 – 12 h 00', '13 h 00 – 16 h 00'];
const lignes = cal.mois.map((m) => {
  const an = m.mois.split(' ')[1];
  const mo = m.mois.split(' ')[0].toLowerCase();
  const cours = m.cours.map((d) => (d === '1' ? '1er' : d)).join(', ') + ` ${mo}`;
  return [m.mois, cours + (m.intensive ? ` ; ${m.intensive} (semaine intensive)` : ''), `${m.rdv === '1' ? '1er' : m.rdv} ${mo}`, m.dominante];
});
module.exports = {
  num: '18',
  slug: '18_Emplois_du_temps_previsionnels',
  title: 'Emplois du temps prévisionnels — Titre professionnel Manager d’établissement marchand',
  objet: 'Rythme d’alternance, calendrier de la promotion MEM 2027-2028 (mars 2027 – février 2028), répartition des heures et journées types.',
  blocks: [
    ['h1', '1. Certification préparée'],
    ['table', ['Certification', 'Code', 'Niveau', 'Certificateur', 'Modalité de certification'], [
      ['Titre professionnel Manager d’établissement marchand (MEM)', 'RNCP 41853', '5', 'Ministère du Travail', 'Session de validation organisée par YEBA FORMATIONS après agrément de la DEETS La Réunion'],
    ], [2500, 1300, 1150, 2050, 2638]],
    ['h1', '2. Un rythme hebdomadaire : le mardi au CFA'],
    ['p', `Les apprentis viennent au CFA **chaque mardi** et passent les quatre autres jours de la semaine en entreprise. Chaque mois comprend **trois ou quatre mardis de cours** et **un mardi consacré au Rendez-vous du mois** (rencontre, visite, activité culturelle, sportive ou solidaire, pièce n° 19). Deux **semaines intensives** au CFA, en janvier et en février 2028, préparent les dernières évaluations et la session de validation du titre.`],
    ['p', 'Ce rythme a été choisi pour quatre raisons :'],
    ['ul', [
      '**Un aller-retour permanent entre théorie et pratique** : ce qui est vu le mardi est appliqué en magasin dès le mercredi, et les situations vécues en entreprise nourrissent le cours suivant.',
      '**Un lien hebdomadaire avec chaque apprenti** : le formateur voit la promotion chaque semaine, ce qui permet de repérer très tôt une difficulté, une absence ou une démotivation (pièce n° 11).',
      '**Une organisation adaptée aux TPE-PME** : l’employeur ne se prive de son apprenti qu’une journée par semaine, toujours la même, ce qui facilite les plannings du point de vente.',
      '**Un rythme régulier et prévisible** pour l’apprenti, son employeur et sa famille.',
    ]],
    ['h1', '3. Respect de la durée minimale de formation'],
    ['p', 'L’article L.6211-2 du Code du travail dispose que la durée de formation en CFA ne peut être inférieure à **25 % de la durée totale du contrat**. Sur un contrat de 12 mois à temps plein (1 607 heures), ce minimum est d’environ **402 heures**.'],
    ['table', ['Composante', 'Calcul', 'Heures'], [
      ['Mardis de cours', `${cal.nbCours} mardis × 7 heures`, String(h.mardis)],
      ['Semaines intensives', '2 semaines × 35 heures', String(h.intensives)],
      ['**Sous-total : enseignements en face à face**', '', `**${h.enseignement}**`],
      ['Rendez-vous du mois (journées pédagogiques hors les murs)', '12 mardis × 7 heures', String(h.rdv)],
      ['**Total de la formation au CFA**', `soit ${(h.total / 1607 * 100).toFixed(1).replace('.', ',')} % de la durée du contrat`, `**${h.total}**`],
    ], [4600, 3400, 1638]],
    ['p', 'Les Rendez-vous du mois sont des **journées pédagogiques à part entière** : chacune poursuit des objectifs rattachés aux compétences du titre (pièce n° 19), comporte un atelier le matin et une rencontre ou une mise en situation l’après-midi, donne lieu à un émargement et à une production écrite de l’apprenti dans son livret, réutilisée dans le dossier professionnel. Elles figurent au calendrier annexé à la convention de formation.'],
    ['h1', '4. Règles communes'],
    ['ul', [
      'Promotion unique de **8 à 10 apprentis** ; contrats de **12 mois**, du **1er mars 2027 au 29 février 2028**.',
      'Horaires : **8 h 00 – 12 h 00 et 13 h 00 – 16 h 00**, soit 7 heures par jour, avec une **pause de 15 minutes à 10 h et à 15 h** (mardis de cours, Rendez-vous du mois et semaines intensives).',
      'Lieu : **7 rue Henri Cornu, Immeuble Rodrigue 2, Technopole Réunion / Technor, 97490 Sainte-Clotilde**. Locaux accessibles aux personnes à mobilité réduite. Les Rendez-vous peuvent se dérouler à l’extérieur (visites, tournoi).',
      'Aucun mardi n’est férié entre mars 2027 et février 2028 ; les semaines intensives ne comprennent aucun jour férié.',
      'Les employeurs fixent les congés payés des apprentis en dehors des mardis et des deux semaines intensives.',
    ]],
    ['h1', '5. Calendrier de la promotion'],
    ['table', ['Mois', 'Mardis de cours et semaines intensives', 'Rendez-vous du mois (mardi)', 'Dominante pédagogique et temps forts'], lignes, [1500, 2900, 1600, 3638]],
    ['p', 'La **session de validation** du titre a lieu la semaine du 21 février 2028 [[date fixée après agrément de la DEETS]]. Le mardi 29 février 2028, dernier jour des contrats, est consacré à la cérémonie de clôture.'],
    ['h1', '6. Calendrier des Rendez-vous du mois'],
    ['table', ['Date (8 h – 12 h, 13 h – 16 h)', 'Rendez-vous', 'Nature'], rdv.map((r) => [r.date, r.titre, r.type]), [3400, 3800, 2438]],
    ['h1', '7. Répartition des heures d’enseignement'],
    ['table', ['Module', 'Heures'], [
      ['Intégration : statut d’apprenti, droits, santé-sécurité, égalité, positionnement', '14'],
      ['CCP 1 — Manager l’équipe de son périmètre au sein de l’établissement marchand', '91'],
      ['CCP 2 — Développer la dynamique commerciale de son périmètre au sein de l’établissement marchand', '91'],
      ['CCP 3 — Contribuer à la performance commerciale et à la rentabilité de son périmètre au sein de l’établissement marchand', '70'],
      ['Numérique, outils d’IA et protection des données', '14'],
      ['Esprit d’entreprendre', '7'],
      ['Techniques de recherche d’emploi et insertion', '14'],
      ['Évaluations passées en cours de formation (3 ECF) et examen blanc', '28'],
      ['Accompagnement individualisé : dossier professionnel, remédiation', '14'],
      [`**Sous-total : enseignements en face à face**`, `**${h.enseignement}**`],
      ['Rendez-vous du mois (12 journées pédagogiques hors les murs)', String(h.rdv)],
      ['**Total de la formation**', `**${h.total}**`],
    ], [7800, 1838]],
    ['h1', '8. Journées types'],
    ['h2', 'Mardi de cours — exemple du 6 avril 2027 (CCP 1)'],
    ['table', hdr, [
      ['8 h – 10 h', 'Retour sur la semaine en magasin : situations vécues par chacun', ''],
      ['10 h 15 – 12 h', 'CCP 1 : planifier l’activité et les horaires d’une équipe', ''],
      ['13 h – 15 h', '', 'CCP 1 : conduire un brief d’équipe (jeux de rôle filmés)'],
      ['15 h 15 – 16 h', '', 'Dossier professionnel : attendus et choix des situations ; mission de la semaine pour l’entreprise'],
    ], [1600, 4000, 4038]],
    ['h2', 'Semaine intensive n° 1 — du 24 au 28 janvier 2028 (CCP 3)'],
    ['table', hdr, [
      ['Lundi 24', 'CCP 3 : lire un compte d’exploitation', 'CCP 3 : tableau de bord et indicateurs'],
      ['Mardi 25', 'CCP 3 : gérer les stocks et la démarque', 'CCP 3 : proposer des actions d’amélioration'],
      ['Mercredi 26', 'Révision des trois CCP', 'Accompagnement individualisé : dossier professionnel'],
      ['Jeudi 27', '**ECF du CCP 3**', 'Correction et retours individuels'],
      ['Vendredi 28', '**Examen blanc** dans les conditions de la session', 'Retours individuels et plan de révision'],
    ], [1600, 4000, 4038]],
    ['h2', 'Semaine intensive n° 2 — du 7 au 11 février 2028'],
    ['table', hdr, [
      ['Lundi 7', 'Révisions ciblées selon l’examen blanc', 'Révisions ciblées selon l’examen blanc'],
      ['Mardi 8', 'Dossier professionnel : relecture finale', 'Oral blanc n° 1 : présentation du dossier professionnel'],
      ['Mercredi 9', 'Mise en situation professionnelle d’entraînement', 'Retours individuels'],
      ['Jeudi 10', 'Insertion : CV de manager, entretien d’embauche', 'Oral blanc n° 2 : entretien avec le jury'],
      ['Vendredi 11', '**Remise des dossiers professionnels**', 'Bilan et organisation de la session'],
    ], [1600, 4000, 4038]],
    ['rgpd', [
      '**IA Act** — Le module « Numérique, outils d’IA et protection des données » et le Rendez-vous du 20 avril 2027 contribuent à l’obligation de **maîtrise de l’IA** (article 4 du règlement européen sur l’IA, applicable depuis le 2 février 2025) chez les futurs managers.',
      '**RGPD** — Les exercices utilisent des données fictives ; aucune donnée réelle de salariés ou de clients des entreprises d’accueil n’est importée dans les outils de formation.',
    ]],
  ],
};
