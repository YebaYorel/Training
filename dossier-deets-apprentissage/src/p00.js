// Bordereau d'envoi + liste de contrôle des éléments à compléter (générée automatiquement).
const fs = require('fs');
const pieces = fs.readdirSync(__dirname).filter((f) => /^p\d+\.js$/.test(f) && f !== 'p00.js' && f !== 'p99.js').sort().map((f) => require('./' + f));
const byNum = Object.fromEntries(pieces.map((d) => [d.num, d]));
const ref = (n) => (byNum[n] ? 'Fichier joint' : 'À joindre');

const liste = [
  ['01', 'Statuts faisant mention de l’apprentissage', 'Joint', 'Fichier joint'],
  ['02', 'Bulletin n° 3 du casier judiciaire de la personne exerçant la direction', 'Joint', 'Fichier joint'],
  ['03', 'Justificatifs des locaux et de leur aménagement (bail, photos, sanitaires, salle de pause / restauration)', 'Joint', 'Fichier joint'],
  ['04', 'Titres et qualités des formateurs (diplômes, CV)', 'Tableau et justificatifs joints', ref('04')],
  ['05', 'Notice recherche d’employeur et rupture du contrat', 'Notice jointe', ref('05')],
  ['06', 'Notice évaluation des compétences', 'Notice jointe', ref('06')],
  ['07', 'Notice suivi en entreprise et adéquation CFA / entreprise', 'Notice jointe', ref('07')],
  ['08', 'Notice mixité et égalité femmes-hommes', 'Notice jointe', ref('08')],
  ['09', 'Mobilité internationale', 'Notice jointe', ref('09')],
  ['10', 'Notice handicap et justificatifs', 'Notice jointe', ref('10')],
  ['11', 'Notice prévention du décrochage', 'Notice jointe', ref('11')],
  ['12', 'Notice santé, sécurité, prévention des risques et documents remis', 'Notice jointe', ref('12')],
  ['13', 'Insertion professionnelle après la certification', 'Notice jointe', ref('13')],
  ['14', 'Suivi des anciens apprentis', 'Notice jointe', ref('14')],
  ['15', 'Sensibilisation à la création / reprise d’entreprise', 'Notice jointe', ref('15')],
  ['16', 'Activités culturelles et sportives', 'Notice jointe', ref('16')],
  ['17', 'Compétences des maîtres d’apprentissage et récapitulatif des actions', 'Notice jointe', ref('17')],
  ['18', 'Emplois du temps prévisionnels', 'Notice jointe', ref('18')],
  ['19', 'Complément : programme des Rendez-vous du mois (pièces 11, 15 et 16)', 'Notice jointe', ref('19')],
  ['20', 'Complément : planning annuel de la promotion MEM 2027-2028', 'Notice jointe', ref('20')],
];

const blocks = [
  ['p', 'En réponse à votre courriel du 20 octobre 2026, YEBA FORMATIONS vous adresse les pièces suivantes, à l’appui de sa demande de modification de sa déclaration d’activité pour l’extension à la formation par apprentissage (article L.6351-5 du Code du travail). La première promotion préparera le **titre professionnel Manager d’établissement marchand** (RNCP 41853, niveau 5) du 1er mars 2027 au 29 février 2028.'],
  ['table', ['N°', 'Pièce', 'Observations', 'Document'], liste, [700, 4300, 2600, 2038]],
];

module.exports = {
  num: '00',
  slug: '00_Bordereau_d_envoi',
  title: 'Bordereau d’envoi des pièces',
  objet: 'Récapitulatif des pièces transmises en réponse au courriel de la DEETS du 20 octobre 2026.',
  blocks,
};
