// Bordereau d'envoi + liste de contrôle des éléments à compléter (générée automatiquement).
const fs = require('fs');
const { placeholders } = require('./lib');
const pieces = fs.readdirSync(__dirname).filter((f) => /^p\d+\.js$/.test(f) && f !== 'p00.js').sort().map((f) => require('./' + f));
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
    '**Certification Qualiopi** : vérifier que le certificat n° 25FOR02027.1 couvre la catégorie « actions de formation par apprentissage » ; sinon, demander une extension de périmètre à l’organisme certificateur. Sans elle, les contrats ne peuvent pas être financés par les OPCO.',
    '**Certifications préparées** : seuls des diplômes ou titres inscrits au RNCP peuvent être préparés en apprentissage. Pour un titre du ministère du Travail, prévoir l’agrément pour organiser les sessions ou un partenariat avec un centre agréé ; pour un autre certificateur, une convention de partenariat.',
    '**Numéro UAI** : immatriculation de l’établissement auprès du rectorat, nécessaire pour l’enregistrement des contrats ([[démarche à vérifier]]).',
    '**Cohérence** : les noms, fonctions et engagements cités doivent être identiques dans toutes les pièces.',
    '**Sincérité** : ne présenter comme réalisés que les actions et les partenariats effectivement engagés. Les surlignages jaunes signalent les points à compléter ou à vérifier.',
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
