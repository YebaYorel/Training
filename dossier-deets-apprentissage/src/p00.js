// Bordereau d'envoi + liste de contrôle des éléments à compléter (générée automatiquement).
const fs = require('fs');
const { placeholders } = require('./lib');
const pieces = fs.readdirSync(__dirname).filter((f) => /^p\d+\.js$/.test(f) && f !== 'p00.js').sort().map((f) => require('./' + f)).filter((d) => d.num !== 'NI');
const byNum = Object.fromEntries(pieces.map((d) => [d.num, d]));
const ref = (n) => (byNum[n] ? 'Fichier Word fourni' : 'À joindre');

const liste = [
  ['01', 'Statuts faisant mention de l’apprentissage', 'Aurélien LUMEKA', ''],
  ['02', 'Bulletin n° 3 du casier judiciaire de la personne exerçant la direction', 'Aurélien LUMEKA', ''],
  ['03', 'Justificatifs des locaux et de leur aménagement (bail, photos, sanitaires, salle de pause / restauration)', 'Aurélien LUMEKA', ''],
  ['04', 'Titres et qualités des formateurs (diplômes, CV)', 'Tableau rédigé + justificatifs à joindre', ref('04')],
  ['05', 'Notice recherche d’employeur et rupture du contrat', 'Rédigée — à compléter', ref('05')],
  ['06', 'Notice évaluation des compétences', 'Rédigée — à compléter', ref('06')],
  ['07', 'Notice suivi en entreprise et adéquation CFA / entreprise', 'Rédigée — à compléter', ref('07')],
  ['08', 'Notice mixité et égalité femmes-hommes', 'Rédigée — à compléter', ref('08')],
  ['09', 'Mobilité internationale', 'Rédigée — à compléter', ref('09')],
  ['10', 'Notice handicap et justificatifs', 'Rédigée — justificatifs à joindre', ref('10')],
  ['11', 'Notice prévention du décrochage', 'Rédigée — à compléter', ref('11')],
  ['12', 'Notice santé, sécurité, prévention des risques et documents remis', 'Rédigée — documents à joindre', ref('12')],
  ['13', 'Insertion professionnelle après la certification', 'Rédigée — à compléter', ref('13')],
  ['14', 'Suivi des anciens apprentis', 'Rédigée — à compléter', ref('14')],
  ['15', 'Sensibilisation à la création / reprise d’entreprise', 'Rédigée — à compléter', ref('15')],
  ['16', 'Activités culturelles et sportives', 'Rédigée — à compléter', ref('16')],
  ['17', 'Compétences des maîtres d’apprentissage et récapitulatif des actions', 'Rédigée — récapitulatif à compléter', ref('17')],
  ['18', 'Emplois du temps prévisionnels', 'Rédigée sur hypothèses — à valider', ref('18')],
];

const blocks = [
  ['h1', '1. Calendrier'],
  ['p', 'Courriel de la DEETS reçu le **20 octobre 2026** ; délai de réponse de 12 jours, soit le **1er novembre 2026** (dimanche, Toussaint). Envoi recommandé **au plus tard le vendredi 30 octobre 2026**. Si certaines pièces ne peuvent pas être finalisées, adresser les pièces prêtes dans le délai et indiquer par écrit la date de transmission des compléments.'],
  ['h1', '2. Bordereau des pièces'],
  ['table', ['N°', 'Pièce demandée', 'État / responsable', 'Document'], liste, [700, 4300, 2600, 2038]],
  ['h1', '3. Points stratégiques à sécuriser'],
  ['ul', [
    '**Qualiopi** : l’audit d’extension « apprentissage » ne peut avoir lieu qu’après l’entrée en formation d’un premier apprenti (courriel du certificateur du 14/10/2026). Demander **par écrit à chaque OPCO** comment sont financés les premiers contrats pendant cette période, avant de signer avec les employeurs.',
    '**MEM (RNCP 41853)** : déposer la demande d’agrément auprès de la DEETS La Réunion (démarche en ligne « DEETS 974 — demande d’agrément pour organiser des sessions ») au moins 6 mois avant la session de février 2028, soit **avant fin juillet 2027** ; dépôt conseillé dès le premier trimestre 2027.',
    '**Product Builder (RNCP 39108)** : enregistrement valable jusqu’au **31/05/2027**, soit avant la fin des contrats. Obtenir de l’École Cube l’assurance écrite du renouvellement avant de signer des contrats.',
    '**Responsable RH (RNCP 38442, Cnam)** : vérifier auprès du Cnam qu’un organisme extérieur à son réseau peut préparer cette certification (contact : Cnam La Réunion) ; sinon, choisir une autre fiche « Responsable RH ».',
    '**Capacité** : trois groupes et un seul formateur permanent. Les intervenants experts (RH, no-code) et le sous-traitant chargé du placement doivent être identifiés avant mars 2027. Ouvrir d’abord le MEM, puis les autres titres une fois les partenariats signés, réduirait le risque.',
    '**Sincérité** : ne présenter comme réalisés que les actions et partenariats effectivement engagés. Les surlignages jaunes signalent les points à compléter ou à vérifier.',
  ]],
  ['h1', '4. Proposition de courriel d’accompagnement'],
  ['p', 'Objet : Extension de la déclaration d’activité à l’apprentissage — YEBA FORMATIONS (NDA 04973676397) — transmission des pièces'],
  ['p', 'Madame, Monsieur,'],
  ['p', 'Suite à notre entretien téléphonique et à votre courriel du 20 octobre 2026, je vous prie de trouver ci-joint les pièces demandées dans le cadre de l’instruction de la modification de notre déclaration d’activité, en application de l’article L.6351-5 du Code du travail. Le bordereau joint récapitule les 18 pièces transmises. [[Le cas échéant : les pièces n° … vous seront adressées au plus tard le …]]'],
  ['p', 'Je reste à votre disposition pour tout complément d’information.'],
  ['p', 'Veuillez agréer, Madame, Monsieur, mes salutations distinguées.'],
  ['p', 'Aurélien LUMEKA — Directeur de YEBA FORMATIONS — [[téléphone]]'],
  ['pb'],
  ['h1', '5. Liste de contrôle des éléments à compléter (usage interne — ne pas transmettre)'],
  ...pieces.flatMap((d) => {
    const ph = placeholders(d.blocks);
    return ph.length ? [['h2', `Pièce ${d.num} — ${ph.length} élément(s)`], ['ul', ph.map((x) => x)]] : [];
  }),
];

module.exports = {
  num: '00',
  slug: '00_Bordereau_et_liste_de_controle',
  title: 'Bordereau d’envoi et liste de contrôle du dossier',
  objet: 'Récapitulatif des pièces transmises en réponse au courriel de la DEETS du 20 octobre 2026.',
  blocks,
};
