const fs = require('fs');
const rdv = require('./rdv');
const { placeholders } = require('./lib');
const pieces = fs.readdirSync(__dirname).filter((f) => /^p\d+\.js$/.test(f) && f !== 'p99.js').sort().map((f) => require('./' + f));
module.exports = {
  num: 'NI',
  slug: 'NOTE_INTERNE_demarches_contacts_et_modeles_de_mails',
  title: 'Démarches à engager, intervenants à solliciter et modèles de courriels — Promotion MEM 2027-2028',
  objet: 'Feuille de route personnelle : agrément MEM, financement, intervenants des Rendez-vous du mois, vérifications juridiques et modèles de courriels prêts à envoyer.',
  blocks: [
    ['h1', '1. Points stratégiques à sécuriser'],
    ['ul', [
    '**Périmètre** : une seule formation par apprentissage en 2027, le **titre professionnel Manager d’établissement marchand (RNCP 41853)**, pour un groupe de 8 à 10 apprentis, du 1er mars 2027 au 29 février 2028. Toutes les pièces sont rédigées sur ce périmètre.',
    '**Qualiopi** : l’audit d’extension « apprentissage » ne peut avoir lieu qu’après l’entrée en formation d’un premier apprenti (courriel du certificateur du 14/10/2026). Obtenir **par écrit de chaque OPCO** les conditions de financement des premiers contrats pendant cette période, avant de signer avec les employeurs.',
    '**Agrément MEM** : déposer la demande auprès de la DEETS La Réunion dès le premier trimestre 2027, et au plus tard 6 mois avant la session de février 2028.',
    '**Capacité** : un formateur permanent. L’intervenant expert du CCP 3 et le sous-traitant chargé du placement doivent être identifiés avant mars 2027.',
    '**Rendez-vous du mois** : 48 heures de formation en plus des 420 heures d’enseignement ; à annexer à la convention de formation pour que les employeurs s’engagent à libérer les apprentis.',
    '**Sincérité** : ne présenter comme réalisés que les actions et partenariats effectivement engagés. Les surlignages jaunes signalent les points à compléter ou à vérifier avant l’envoi.',
    ]],
    ['h1', '2. Courriel d’envoi du dossier à la DEETS'],
    ['p', 'Objet : Extension de la déclaration d’activité à l’apprentissage — YEBA FORMATIONS (NDA 04973676397) — transmission des pièces'],
    ['p', 'Madame, Monsieur,'],
    ['p', 'Suite à notre entretien téléphonique et à votre courriel du 20 octobre 2026, je vous prie de trouver ci-joint les pièces demandées dans le cadre de l’instruction de la modification de notre déclaration d’activité, en application de l’article L.6351-5 du Code du travail. Notre première promotion préparera le titre professionnel Manager d’établissement marchand (RNCP 41853) à compter du 1er mars 2027. Le bordereau joint récapitule les pièces transmises ; les pièces n° 19 et 20 détaillent le programme des Rendez-vous du mois et le planning annuel de la promotion. [[Le cas échéant : les pièces n° 01 à 03 vous seront adressées au plus tard le …]]'],
    ['p', 'Je reste à votre disposition pour tout complément d’information.'],
    ['p', 'Veuillez agréer, Madame, Monsieur, mes salutations distinguées.'],
    ['p', 'Aurélien LUMEKA — Directeur de YEBA FORMATIONS — [[téléphone]]'],
    ['h1', '3. Agrément pour la session du titre MEM'],
    ['ul', [
      'Titre professionnel Manager d’établissement marchand, RNCP 41853, niveau 5, ministère du Travail ; fiche valable jusqu’au 02/03/2031 ; 3 CCP.',
      'Démarche en ligne « DEETS 974 — demande d’agrément pour organiser des sessions » sur demarche.numerique.gouv.fr ; dépôt au plus tard 6 mois avant la session. Textes cités par les formulaires des DREETS : arrêté du 22 décembre 2015 et arrêtés du 21 juillet 2016.',
      'Lors de votre prochain échange avec la DEETS, demander le contact du **service chargé des titres professionnels** et un rendez-vous préalable.',
      'Plan B : présenter les apprentis à une session d’un centre déjà agréé pour le MEM à La Réunion [[à identifier]].',
    ]],
    ['h1', '4. Financement des premiers contrats'],
    ['p', 'L’audit d’extension Qualiopi ne peut avoir lieu qu’après l’entrée du premier apprenti. Écrire à chaque OPCO concerné par vos futurs employeurs (commerce et distribution notamment) pour obtenir par écrit : les conditions de prise en charge des contrats démarrant avant l’extension, le niveau de prise en charge du titre MEM, et le calendrier de facturation.'],
    ['h1', '5. Intervenants à solliciter pour les Rendez-vous du mois'],
    ['table', ['Date', 'Rendez-vous', 'Intervenants à solliciter', 'À solliciter avant'], rdv.map((r, i) => [r.date, r.titre, r.partenaires, i < 5 ? '31 janvier 2027' : '30 juin 2027']), [2500, 2400, 3200, 1538]],
    ['h1', '6. Vérifications avant envoi ou avant l’ouverture'],
    ['ul', [
      'Vérifier sur Légifrance la rédaction en vigueur des articles cités : L.6231-2, L.6222-12-1, L.6222-18, L.6222-18-2, L.6222-39, L.6211-2, L.6224-1, L.6223-8-1, L.6111-8 du Code du travail.',
      'Vérifier l’article relatif au conseil de perfectionnement des CFA et les délais de la visite d’information et de prévention des apprentis.',
      'Vérifier l’échéance du bilan pédagogique et financier.',
      'Ne mentionner dans les tableaux « actions engagées » (pièces 08 et 17) que des actions réellement réalisées, avec leur preuve.',
      'Pour les formations réalisées pour le compte d’autres centres, vérifier ce que vos contrats autorisent à mentionner.',
    ]],
    ['h1', '7. Modèle de courriel — sollicitation d’un intervenant'],
    ['p', 'Objet : Invitation à intervenir auprès de nos apprentis managers — [[date du Rendez-vous]]'],
    ['p', 'Madame, Monsieur,'],
    ['p', 'YEBA FORMATIONS, organisme de formation implanté à la Technopole de La Réunion, ouvre en mars 2027 sa première promotion d’apprentis préparant le titre professionnel Manager d’établissement marchand. Chaque mois, nos 8 à 10 apprentis vivent un « Rendez-vous du mois » : une rencontre avec un acteur de l’économie réunionnaise, en lien direct avec leur futur métier.'],
    ['p', 'Nous serions honorés de vous accueillir le [[date]], de 13 h à 17 h, dans nos locaux du 7 rue Henri Cornu, Immeuble Rodrigue 2, à Sainte-Clotilde, pour un échange autour du thème « [[thème]] ». Les apprentis prépareront leurs questions en amont ; votre intervention pourrait durer de 1 h 30 à 2 heures.'],
    ['p', 'Je me tiens à votre disposition pour en convenir ensemble.'],
    ['p', 'Aurélien LUMEKA — Directeur de YEBA FORMATIONS — [[téléphone]]'],
    ['h1', '8. Modèle de courriel — présentation aux entreprises'],
    ['p', 'Objet : Recrutez votre futur manager en apprentissage — titre professionnel MEM, rentrée le 1er mars 2027'],
    ['p', 'Madame, Monsieur,'],
    ['p', 'YEBA FORMATIONS ouvre le 1er mars 2027 une formation par apprentissage au titre professionnel Manager d’établissement marchand (niveau 5, bac+2). Pendant 12 mois, l’apprenti passe une semaine par mois au CFA et trois semaines dans votre magasin, où il apprend à manager une équipe, développer les ventes et piloter la rentabilité de son périmètre.'],
    ['p', 'Nous prenons en charge les démarches (contrat, convention, dépôt auprès de l’OPCO), présélectionnons des candidats motivés et formons gratuitement votre maître d’apprentissage. Vous trouverez en pièce jointe le planning de l’année et le programme des Rendez-vous du mois.'],
    ['p', 'Puis-je vous proposer un rendez-vous de 30 minutes pour en parler ?'],
    ['p', 'Aurélien LUMEKA — Directeur de YEBA FORMATIONS — [[téléphone]]'],
    ['h1', '9. Liste de contrôle : éléments surlignés à compléter'],
    ...pieces.flatMap((d) => {
      const ph = placeholders(d.blocks);
      return ph.length ? [['h2', `Pièce ${d.num} — ${ph.length} élément(s)`], ['ul', ph]] : [];
    }),
    ['rgpd', [
      '**RGPD** — Prospection d’entreprises par courriel : en B2B, elle est possible si le message concerne l’activité professionnelle du destinataire, avec un moyen simple de s’opposer à de nouveaux envois. Les coordonnées des intervenants et des entreprises sont tenues dans Baserow (hébergement UE) et conservées [[durée à fixer]].',
    ]],
  ],
};
