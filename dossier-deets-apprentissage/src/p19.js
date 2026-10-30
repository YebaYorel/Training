const rdv = require('./rdv');
const fiches = rdv.flatMap((r, i) => [
  ['h2', `${i + 1}. ${r.mois} — ${r.titre}`],
  ['table', ['Rubrique', 'Détail'], [
    ['Date et horaire', `${r.date}, 13 h – 17 h`],
    ['Nature', r.type],
    ['Déroulé', r.contenu],
    ['Lien avec la formation', r.lien],
    ['Intervenants et partenaires', r.partenaires],
    ['Coût estimé', r.cout],
  ], [2600, 7038]],
]);
module.exports = {
  num: '19',
  slug: '19_Programme_des_Rendez-vous_du_mois_MEM',
  title: 'Programme des Rendez-vous du mois — Promotion MEM 2027-2028',
  objet: 'Programme annuel des rencontres, visites, activités culturelles, artistiques, sportives et solidaires proposées aux apprentis préparant le titre Manager d’établissement marchand, en complément des 420 heures d’enseignement.',
  blocks: [
    ['h1', '1. L’esprit de l’année'],
    ['p', 'YEBA FORMATIONS veut que chaque apprenti puisse dire, en février 2028 : « J’ai adoré cette année, je ne l’ai pas vue passer. » Apprendre un métier exigeant ne s’oppose pas au plaisir d’apprendre : un groupe soudé, des rencontres marquantes et des défis concrets sont les meilleurs remèdes contre la démotivation et l’abandon.'],
    ['p', 'Chaque mois, un **Rendez-vous du mois** réunit la promotion pendant une demi-journée, en dehors des semaines au CFA. Il est toujours relié au métier de manager d’établissement marchand : manager une équipe, développer le commerce, piloter la rentabilité, ou préparer son avenir (emploi, création d’entreprise).'],
    ['table', ['Principe', 'Application'], [
      ['Ne pas réduire les heures d’enseignement', 'Les 420 heures d’enseignement restent entières. Les Rendez-vous ajoutent 48 heures de formation (12 × 4 heures), soit 468 heures au total (pièce n° 18).'],
      ['Un jour fixe, connu d’avance', 'Un jeudi par mois, de 13 h à 17 h, pendant une semaine en entreprise. Le calendrier est remis à l’employeur avant la signature du contrat et annexé à la convention de formation.'],
      ['Un temps de formation à part entière', 'Ce temps est rémunéré comme du temps de formation. La présence est obligatoire et donne lieu à un émargement ; une absence est justifiée comme une absence au CFA.'],
      ['Des apprentis acteurs', 'Les apprentis préparent leurs questions, organisent certains événements (tournoi solidaire, collecte de Noël) et rédigent une courte trace dans leur livret, réutilisable dans leur dossier professionnel.'],
    ], [3200, 6438]],

    ['h1', '2. Le calendrier en un coup d’œil'],
    ['table', ['Mois', 'Date', 'Rendez-vous', 'Nature'], rdv.map((r) => [r.mois, r.date, `**${r.titre}**`, r.type]), [1700, 2600, 3200, 2138]],
    ['p', 'Le programme couvre ainsi toutes les dimensions de l’année : la cohésion du groupe (mars), le numérique et la cybersécurité (avril), la culture (mai et décembre), l’expression artistique (juillet), le sport et la solidarité (août et décembre), la création et la reprise d’entreprise (juin, septembre et octobre), l’emploi (novembre), la découverte d’une grande entreprise (janvier) et la reconnaissance du parcours (février).'],

    ['h1', '3. Fiches détaillées'],
    ...fiches,

    ['h1', '4. Obligations des apprentis lors des Rendez-vous'],
    ['ul', [
      '**Présence obligatoire** et émargement en début et en fin de séance ; prévenir le CFA et l’employeur en cas d’empêchement, avec justificatif.',
      '**Préparation** : trois questions écrites, remises la veille, pour chaque rencontre avec un intervenant.',
      '**Tenue et posture professionnelles**, adaptées au lieu (tenue de sport le jour du tournoi).',
      '**Trace écrite** : une demi-page dans le livret d’apprentissage (ce que j’ai appris, ce que j’applique dans mon magasin), sous 8 jours.',
      '**Respect des règles** du règlement intérieur, y compris hors des locaux.',
    ]],

    ['h1', '5. Banque d’idées de remplacement'],
    ['p', 'Si un intervenant se désiste ou si la promotion exprime d’autres envies (via ses délégués), ces activités peuvent remplacer un Rendez-vous, sur le même créneau de 4 heures et avec le même lien au métier.'],
    ['table', ['Idée', 'Déroulé', 'Lien avec la formation'], [
      ['Client mystère croisé', 'Chaque apprenti visite incognito le magasin d’un camarade et rédige un rapport d’expérience client ; restitution collective.', 'CCP 2 : expérience client'],
      ['Concours de vitrines', 'Les apprentis réalisent une vitrine ou un îlot dans leur magasin ; vote des maîtres d’apprentissage et des clients.', 'CCP 2 : merchandising'],
      ['Théâtre d’improvisation', 'Atelier animé par un comédien : oser prendre la parole, gérer l’imprévu, tenir un groupe.', 'CCP 1 : brief et animation d’équipe'],
      ['Gérer les clients difficiles', 'Atelier avec un professionnel de la médiation : désamorcer un conflit, se protéger, rester calme.', 'CCP 1 ; santé et sécurité au travail'],
      ['Visite du Grand Port Maritime', 'Comprendre comment une île s’approvisionne : conteneurs, délais, coûts.', 'CCP 2 : approvisionnement'],
      ['Producteurs et marché forain', 'Rencontre avec des producteurs locaux et réflexion sur les produits péi en magasin.', 'CCP 2 : assortiment ; circuits courts'],
      ['Anti-gaspillage et dons', 'Rencontre avec une association d’aide alimentaire : dons d’invendus, obligations des magasins.', 'CCP 3 : démarque ; responsabilité sociétale'],
      ['Ce que j’attends d’un manager', 'Table ronde avec des responsables du recrutement de grandes enseignes.', 'Insertion ; CCP 1'],
      ['Mon image professionnelle', 'Posture, tenue, profil sur les réseaux professionnels, photo professionnelle.', 'Insertion professionnelle'],
      ['Gérer son budget', 'Atelier sur les finances personnelles avec une association spécialisée.', 'Prévention des difficultés matérielles et du décrochage'],
      ['Escape game « Le magasin piégé »', 'Énigmes à résoudre en équipe dans un temps limité ; débriefing sur la prise de décision.', 'CCP 1 : décision, coopération'],
      ['Repas partagé péi', 'Chaque apprenti apporte un plat de sa famille ; échange sur la diversité culturelle de l’île.', 'Cohésion ; diversité'],
      ['Randonnée accessible', 'Sortie nature accessible à tous, avec un guide.', 'Cohésion ; santé'],
      ['Sauveteur secouriste du travail', 'Formation certifiante aux premiers secours au travail (2 jours, hors Rendez-vous, avec l’accord des employeurs).', 'Santé et sécurité ; atout sur le CV'],
    ], [2600, 4600, 2438]],

    ['h1', '6. Faire face à la réalité du terrain'],
    ['p', 'Une année réussie n’est pas une année sans difficulté. Les Rendez-vous sont aussi des moments pour repérer et soutenir les apprentis qui décrochent (pièce n° 11) :'],
    ['ul', [
      '**Binômes d’entraide** formés dès mars : chaque apprenti a un camarade référent qui prend de ses nouvelles entre les semaines au CFA.',
      '**Point informel** du référent avec chaque apprenti à la fin de chaque Rendez-vous ; toute absence non justifiée déclenche un appel le jour même.',
      '**Activité de repli** prévue pour chaque Rendez-vous (intempéries, alerte cyclonique, désistement d’un intervenant) : atelier en salle tiré de la banque d’idées.',
      '**Questionnaire de satisfaction** de deux minutes à la fin de chaque Rendez-vous ; bilan avec les délégués au conseil de perfectionnement de juin et de décembre.',
    ]],

    ['h1', '7. Organisation et budget'],
    ['ul', [
      'Pilotage : Aurélien LUMEKA, référent vie de l’apprenti, avec les délégués de la promotion.',
      'Sollicitation des intervenants : de janvier à mars 2027 pour le premier semestre, en juin 2027 pour le second ; confirmation écrite au plus tard un mois avant chaque date.',
      'Déplacements : les Rendez-vous ont lieu à Saint-Denis, sauf le tournoi et la visite de janvier ; transport organisé par le CFA [[mode de transport et prise en charge à définir]].',
      'Budget annuel prévisionnel : [[montant à chiffrer]] €, principalement pour le team building, la rencontre artistique, la cérémonie et les transports. Les rencontres avec les institutions, les financeurs et les professionnels sont en principe gratuites.',
      'Assurance responsabilité civile de l’organisme vérifiée pour chaque activité extérieure ; autorisation des représentants légaux pour les mineurs.',
    ]],
    ['rgpd', [
      '**RGPD** — Droit à l’image : autorisation écrite et révocable avant toute photo ou vidéo publiée. La liste des participants transmise à un partenaire se limite au nom et au prénom. Au job dating, les CV ne sont remis aux enseignes qu’avec l’accord de chaque apprenti.',
      '**IA Act** — Le Rendez-vous « IA et cybersécurité » contribue à l’obligation de maîtrise de l’IA (article 4) des futurs managers. Les apprentis y apprennent aussi que trier des candidatures avec une IA est un usage **à haut risque** (annexe III, domaine « emploi »).',
    ]],
  ],
};
