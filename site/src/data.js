// Contenus publics du site.
// • catalogue.json est GÉNÉRÉ depuis Airtable (npm run sync) : il décide QUELLES formations sont publiées
//   (Active + marque YEBA obligatoire, jamais de marque blanche) et porte les informations réglementaires
//   (durée, tarifs, prérequis, évaluation, accès, handicap, financements, indicateurs — RNQ ind. 1 et 2).
// • EDITORIAL ci-dessous n'apporte que la mise en scène : nom court, accroche, mots-clés, badge, filtre.
// Jamais de mention « finançable CPF » (aucune certification RNCP/RS) ni « formation obligatoire ».
import catalogue from './catalogue.json'

export const ENTREPRISE = {
  nom: 'YEBA FORMATIONS',
  dirigeant: 'Aurélien LUMEKA',
  adresse: '9 rue Françoise Châtelain, 97490 Sainte-Clotilde, La Réunion',
  telAffiche: '0693 32 24 45',
  telLien: 'tel:+262693322445',
  email: 'yebaformations@gmail.com',
  siret: '814 622 262 00032',
  nda: '04973676397',
  qualiopi: '25FOR02027.1',
  certificateur: 'Qualitia (accrédité COFRAC)',
}

export const FILTRES = [
  { id: 'tout', label: 'Tout voir' },
  { id: 'ia', label: 'IA générative' },
  { id: 'auto', label: 'Automatisation' },
  { id: 'gouv', label: 'RGPD & IA Act' },
  { id: 'dirigeants', label: 'Dirigeants' },
  { id: 'metiers', label: 'Vente & management' },
]

const EDITORIAL = [
  {
    ref: 'FOR-0011',
    nom: 'ALLUMAGE-TURBO',
    sousTitre: "L'IA générative au travail : usages, sécurité, preuves",
    cat: 'ia',
    jours: 3,
    heures: 24,
    effectif: '4 à 10 stagiaires',
    format: 'Inter-entreprise',
    badge: 'Le socle',
    public: 'Tout salarié, manager ou dirigeant qui utilise, ou va utiliser, un outil d’IA générative.',
    cles: ['Bien demander', 'Trier les données', 'Détecter les erreurs', 'Assistant sur mesure'],
    objectifs: [
      'Expliquer ce que fait un modèle de langage et ce qu’il ne fait pas',
      'Formuler une demande complète : rôle, contexte, format, contrainte',
      'Classer une information : je saisis / j’anonymise / je ne saisis jamais',
      'Détecter une réponse fausse, inventée ou biaisée',
      'Conduire un processus métier complet assisté par l’IA',
      'Construire un assistant personnalisé réutilisable',
      'Rédiger les mentions de transparence et les mesures de gouvernance',
      'Repartir avec le dossier de preuve des mesures IA de son poste',
    ],
  },
  {
    ref: 'FOR-0013',
    nom: 'PILOTE AUTOMATIQUE',
    sousTitre: 'Agents IA sous contrôle humain — niveau avancé',
    cat: 'ia',
    jours: 2,
    heures: 16,
    effectif: '4 à 8 stagiaires',
    format: 'Inter-entreprise',
    badge: 'Avancé',
    public: 'Dirigeants, référents IA, chefs de projet et profils techniques, ou anciens d’ALLUMAGE-TURBO.',
    cles: ['Agents autonomes', 'Point d’arrêt humain', 'Traçabilité', 'Arrêt d’urgence'],
    objectifs: [
      'Distinguer assistant, agent et système multi-agents',
      'Mettre en service un agent qui exécute une tâche de bout en bout',
      'Chaîner deux agents avec une validation humaine obligatoire',
      'Fixer le niveau d’autonomie acceptable selon le risque',
      'Tracer qui a décidé, quand, sur quelle donnée',
      'Qualifier un système au regard de l’IA Act',
      'Rédiger la procédure d’arrêt d’urgence et de reprise manuelle',
    ],
  },
  {
    ref: 'FOR-0015',
    nom: 'MOTEUR FERMÉ',
    sousTitre: 'IA locale souveraine : vos données ne sortent pas',
    cat: 'ia',
    jours: 2,
    heures: 16,
    effectif: '4 à 8 stagiaires',
    format: 'Inter-entreprise',
    badge: 'Souveraineté',
    public: 'Cabinets comptables et juridiques, santé, RH, bureaux d’études, collectivités : données sensibles.',
    cles: ['IA sur votre poste', 'Réseau coupé', 'Vos documents', 'Coût sur 36 mois'],
    objectifs: [
      'Distinguer un modèle local d’un modèle distant',
      'Installer un moteur local et faire répondre un modèle sur son poste',
      'Démontrer, réseau coupé, qu’aucune donnée ne quitte la machine',
      'Choisir la taille de modèle que le matériel peut porter',
      'Brancher le modèle sur un fonds documentaire d’entreprise',
      'Chiffrer une solution locale sur 36 mois face à un abonnement',
    ],
  },
  {
    ref: 'FOR-0006',
    nom: 'COPILOTE',
    sousTitre: 'Microsoft 365 par la méthode des 4 P',
    cat: 'ia',
    jours: 2,
    heures: 16,
    effectif: '4 à 8 stagiaires',
    format: 'Intra-entreprise',
    public: 'Équipes équipées de Microsoft 365 qui produisent chaque semaine documents, analyses, courriels.',
    cles: ['Périmètre', 'Prompt', 'Production', 'Preuve'],
    objectifs: [
      'Savoir ce que l’assistant voit, à partir des droits en place',
      'Construire une demande en désignant ses sources',
      'Diagnostiquer une réponse décevante et la corriger',
      'Enchaîner plusieurs applications sur un processus complet',
      'Argumenter trois mesures de gouvernance pour sa structure',
    ],
  },
  {
    ref: 'FOR-0002',
    nom: 'RÉGLAGE MOTEUR',
    sousTitre: 'Automatiser sans coder avec n8n',
    cat: 'auto',
    jours: 2,
    heures: 16,
    effectif: 'Jusqu’à 10 stagiaires',
    format: 'Inter-entreprise',
    public: 'Dirigeants de TPE-PME, indépendants et fonctions administratives.',
    cles: ['Déclencheur', 'Conditions', 'Actions', 'Temps gagné'],
    objectifs: [
      'Repérer les tâches répétitives automatisables',
      'Concevoir un workflow : déclencheur → conditions → actions',
      'Mettre en place une automatisation formulaire → base → e-mail',
      'Sécuriser les données traitées, dans le respect du RGPD',
      'Mesurer le gain de temps et fiabiliser le processus',
    ],
  },
  {
    ref: 'FOR-0009',
    nom: 'CARROSSERIE',
    sousTitre: 'Produire son site internet à la voix',
    cat: 'auto',
    jours: 1,
    heures: 8,
    effectif: 'Jusqu’à 10 stagiaires',
    format: 'Intra-entreprise',
    public: 'Artisans, commerçants, indépendants : sans site, ou dépendants d’un prestataire pour chaque ligne.',
    cles: ['Cahier des charges oral', 'Génération guidée', 'Site conforme', 'Autonomie'],
    objectifs: [
      'Formuler à l’oral un cahier des charges exploitable',
      'Piloter à la voix un outil de génération de site',
      'Vérifier chaque contenu : textes, tarifs, coordonnées',
      'Mettre en ligne un site conforme : mentions, cookies, accessibilité',
      'Faire évoluer son site seul',
    ],
  },
  {
    ref: 'FOR-0010',
    nom: 'INJECTION',
    sousTitre: 'Emailing professionnel assisté par l’IA',
    cat: 'auto',
    jours: 1,
    heures: 8,
    effectif: 'Jusqu’à 10 stagiaires',
    format: 'Intra-entreprise',
    public: 'Dirigeants, commerciaux, chargés de communication qui écrivent à des clients ou prospects.',
    cles: ['Base conforme', 'Objet qui accroche', 'Séquences', 'Délivrabilité'],
    objectifs: [
      'Constituer une base de contacts conforme au RGPD',
      'Rédiger avec l’IA un courriel qui obtient une réponse',
      'Concevoir une séquence de courriels et son rythme',
      'Paramétrer l’envoi pour être reçu',
      'Corriger à partir des indicateurs réels',
    ],
  },
  {
    ref: 'FOR-0003',
    nom: 'CONTRÔLE TECHNIQUE',
    sousTitre: 'Gouvernance RGPD et IA Act',
    cat: 'gouv',
    jours: 1,
    heures: 8,
    effectif: 'Jusqu’à 10 stagiaires',
    format: 'Inter-entreprise',
    badge: 'Gouvernance',
    public: 'Dirigeants, responsables administratifs, et tout salarié qui manipule des données personnelles.',
    cles: ['6 principes', 'Registre', 'Menaces cyber', 'Violation : 72 h'],
    objectifs: [
      'Identifier les données personnelles et traitements de son activité',
      'Appliquer les 6 principes clés du RGPD',
      'Constituer et tenir à jour un registre des traitements',
      'Prévenir hameçonnage, rançongiciel, mots de passe faibles',
      'Réagir à une violation de données : mesures + notification CNIL sous 72 h',
    ],
  },
  {
    ref: 'FOR-0014',
    nom: 'TABLEAU DE BORD',
    sousTitre: 'Séminaire dirigeants en résidentiel',
    cat: 'dirigeants',
    jours: 2,
    heures: 16,
    effectif: '6 à 8 dirigeants, huis clos',
    format: 'Inter-entreprise',
    badge: 'Dirigeants',
    public: 'Dirigeants de TPE-PME réunionnaises de 3 à 50 salariés. Jamais deux concurrents sur la même session.',
    cles: ['3 tâches à automatiser', 'Plan d’agents', 'Charte IA', 'Budget 12 mois'],
    objectifs: [
      'Identifier les trois tâches qui libèrent le plus de temps de dirigeant',
      'Les qualifier au regard de l’IA Act',
      'Fixer le niveau d’autonomie de chaque agent envisagé',
      'Construire le plan d’agents de son entreprise',
      'Rédiger la charte d’usage de l’IA, diffusable dès le retour',
      'Établir budget, calendrier à 12 mois et critère d’arrêt',
    ],
  },
  {
    ref: 'FOR-0004',
    nom: 'TRACTION',
    sousTitre: 'Vendre et négocier',
    cat: 'metiers',
    jours: 1,
    heures: 8,
    effectif: 'Jusqu’à 10 stagiaires',
    format: 'Inter-entreprise',
    public: 'Créateurs d’entreprise, indépendants, commerciaux débutants.',
    cles: ['Découverte', 'Proposition de valeur', 'Objections', 'Conclusion'],
    objectifs: [
      'Dérouler les étapes d’un entretien de vente',
      'Mener une découverte client par un questionnement structuré',
      'Construire une proposition de valeur adaptée',
      'Traiter les objections avec méthode',
      'Conclure et organiser le suivi client',
    ],
  },
  {
    ref: 'FOR-0008',
    nom: 'EMBRAYAGE',
    sousTitre: 'Manager au quotidien',
    cat: 'metiers',
    jours: 1,
    heures: 8,
    effectif: '4 à 10 stagiaires',
    format: 'Inter-entreprise',
    badge: 'Bientôt',
    public: 'Encadrants de proximité, chefs d’équipe, dirigeants de TPE qui encadrent directement.',
    cles: ['Poser un cadre', 'Déléguer', 'Recadrer', 'Reconnaître'],
    objectifs: null, // programme en cours de finalisation : ne pas diffuser d'objectifs (RNQ ind. 1)
  },
]

export const CERTIFS = [
  'Certifié Qualiopi — actions de formation',
  'Google AI Specialist',
  'Google Professional AI',
  'SecNumacadémie — ANSSI',
  'MOOC RGPD — CNIL',
  'Référent handicap en organisme de formation',
  'Déclaration d’activité n° 04973676397',
]

/* ---------- Fusion Airtable + éditorial ---------- */
const CAT_PAR_DEFAUT = 'ia'
function fusionner(fiche, edito) {
  const [nomCourt, ...reste] = fiche.titre.split(' — ')
  return {
    ...(edito ?? { nom: nomCourt, sousTitre: reste.join(' — '), cat: CAT_PAR_DEFAUT, cles: [], objectifs: null }),
    ref: fiche.ref,
    jours: fiche.jours ?? edito?.jours,
    heures: fiche.heures ?? edito?.heures,
    format: fiche.type ?? edito?.format,
    public: edito?.public || fiche.public,
    prerequis: fiche.prerequis,
    evaluation: fiche.evaluation,
    acces: fiche.acces,
    adaptations: fiche.adaptations,
    financements: fiche.financements,
    tarifs: fiche.tarifs,
    indicateurs: fiche.indicateurs,
    revision: fiche.revision,
  }
}
const parRef = Object.fromEntries(EDITORIAL.map((e) => [e.ref, e]))
const publiees = new Set(catalogue.formations.map((f) => f.ref))
// Ordre éditorial d'abord, puis toute nouvelle fiche publiée dans Airtable
export const FORMATIONS = [
  ...EDITORIAL.filter((e) => publiees.has(e.ref)).map((e) => fusionner(catalogue.formations.find((f) => f.ref === e.ref), e)),
  ...catalogue.formations.filter((f) => !parRef[f.ref]).map((f) => fusionner(f)),
]
export const AGENDA = catalogue.agenda
export const SYNCHRO = catalogue.synchronise

export const euros = (n) => (n == null ? '' : n.toLocaleString('fr-FR') + ' €')

/* ---------- Parcours par profil ---------- */
export const PROFILS = [
  {
    id: 'dirigeant',
    titre: 'Je dirige une TPE-PME',
    texte: 'Décider où l’IA vous fera gagner du temps, sans risque juridique.',
    refs: ['FOR-0014', 'FOR-0003', 'FOR-0011'],
  },
  {
    id: 'manager',
    titre: 'Je manage ou je gère les RH',
    texte: 'Équiper vos équipes et poser des règles claires.',
    refs: ['FOR-0011', 'FOR-0008', 'FOR-0003', 'FOR-0006'],
  },
  {
    id: 'salarie',
    titre: 'Je veux gagner du temps au quotidien',
    texte: 'Des gestes concrets, dès le lendemain de la formation.',
    refs: ['FOR-0011', 'FOR-0002', 'FOR-0010', 'FOR-0009'],
  },
  {
    id: 'technique',
    titre: 'Je suis référent informatique',
    texte: 'Déployer des agents et une IA locale sous contrôle.',
    refs: ['FOR-0013', 'FOR-0015', 'FOR-0002'],
  },
]

/* ---------- Diagnostic express (calcul local, rien n'est envoyé) ---------- */
export const DIAGNOSTIC = [
  {
    q: 'Vos équipes utilisent-elles déjà un outil d’IA (ChatGPT, Copilot, Mistral…) ?',
    r: [
      { t: 'Pas encore', m: 0, refs: ['FOR-0011'] },
      { t: 'Oui, chacun de son côté, sans règles', m: 1, refs: ['FOR-0011', 'FOR-0003'], alerte: 'regles' },
      { t: 'Oui, avec des règles écrites', m: 3, refs: ['FOR-0013'] },
    ],
  },
  {
    q: 'Manipulez-vous des données sensibles (santé, RH, juridique, comptabilité) ?',
    r: [
      { t: 'Oui, tous les jours', m: 0, refs: ['FOR-0015', 'FOR-0003'], alerte: 'sensible' },
      { t: 'Parfois', m: 1, refs: ['FOR-0003'] },
      { t: 'Non', m: 2, refs: [] },
    ],
  },
  {
    q: 'Combien d’heures par semaine partent en tâches répétitives (devis, relances, ressaisies) ?',
    r: [
      { t: 'Moins de 2 heures', m: 2, refs: [] },
      { t: 'Entre 2 et 5 heures', m: 1, refs: ['FOR-0002'] },
      { t: 'Plus de 5 heures', m: 0, refs: ['FOR-0002'], alerte: 'automatiser' },
    ],
  },
  {
    q: 'Votre entreprise travaille-t-elle sous Microsoft 365 ?',
    r: [
      { t: 'Oui', m: 1, refs: ['FOR-0006'] },
      { t: 'Non', m: 1, refs: [] },
      { t: 'Je ne sais pas', m: 0, refs: [] },
    ],
  },
  {
    q: 'Avez-vous un inventaire de vos usages d’IA et une charte interne ?',
    r: [
      { t: 'Non, rien d’écrit', m: 0, refs: ['FOR-0003', 'FOR-0014'], alerte: 'preuve' },
      { t: 'En cours', m: 1, refs: ['FOR-0003'] },
      { t: 'Oui, à jour', m: 3, refs: [] },
    ],
  },
  {
    q: 'Votre priorité pour les six prochains mois ?',
    r: [
      { t: 'Gagner du temps', m: 0, refs: ['FOR-0002', 'FOR-0011'] },
      { t: 'Sécuriser nos pratiques', m: 0, refs: ['FOR-0003'] },
      { t: 'Vendre plus', m: 0, refs: ['FOR-0004', 'FOR-0010'] },
      { t: 'Mieux piloter l’entreprise', m: 0, refs: ['FOR-0014'] },
    ],
  },
]
export const ALERTES = {
  regles: 'Des usages sans règles écrites : c’est le premier point à sécuriser (RGPD et IA Act).',
  sensible: 'Avec des données sensibles, privilégiez une IA locale ou européenne, et un tri strict de ce qui est saisi.',
  automatiser: 'Plus de 5 heures par semaine : une automatisation se rembourse souvent en quelques semaines.',
  preuve: 'Sans inventaire ni charte, vous ne pouvez pas prouver les mesures prises. Un audit de gouvernance s’impose.',
}

/* ---------- Financement ---------- */
export const FINANCEURS = {
  OPCO: 'Votre opérateur de compétences peut prendre en charge tout ou partie de la formation de vos salariés, selon ses critères.',
  'Plan PDC': 'Le plan de développement des compétences : l’entreprise finance la formation de ses salariés, avec ou sans aide.',
  'France Travail': 'Pour les demandeurs d’emploi, sur accord de France Travail.',
  AIF: 'L’aide individuelle à la formation de France Travail, sur devis validé par votre conseiller.',
  Région: 'Selon les dispositifs ouverts par la Région Réunion au moment de votre demande.',
}

/* ---------- Questions fréquentes ---------- */
export const FAQ = [
  [
    'Mes formations peuvent-elles être financées ?',
    'Oui, selon votre situation : OPCO, plan de développement des compétences, France Travail (AIF) ou dispositifs de la Région. Nous sommes certifiés Qualiopi, condition exigée par les financeurs publics et paritaires. Nous vous aidons à monter la demande.',
  ],
  [
    'Et le CPF ?',
    'Pas aujourd’hui : aucune de nos formations n’est enregistrée au RNCP ou au Répertoire spécifique, condition pour être éligible au CPF. Nous préférons vous le dire clairement.',
  ],
  [
    'Combien de temps avant de démarrer ?',
    '15 jours ouvrés minimum entre l’inscription et le premier jour. Ce délai sert à vous envoyer le test de positionnement et à adapter le contenu à vos dossiers réels.',
  ],
  [
    'Intra ou inter, quelle différence ?',
    'En intra, nous venons dans vos locaux, pour votre équipe, sur vos cas. En inter, vous rejoignez d’autres entreprises en salle de séminaire : idéal pour une ou deux personnes.',
  ],
  [
    'Nos données sont-elles en sécurité pendant la formation ?',
    'Chaque stagiaire travaille avec un compte professionnel, jamais personnel. Nous apprenons à trier ce qui peut être saisi, ce qui doit être anonymisé et ce qui ne doit jamais l’être.',
  ],
  [
    'Je suis en situation de handicap. Comment ça se passe ?',
    'Signalez simplement votre besoin d’aménagement : aucun justificatif médical n’est demandé. Supports agrandis, rythme adapté, pauses supplémentaires : le référent handicap étudie chaque situation avant l’entrée en formation.',
  ],
  [
    'Qu’est-ce que je reçois à la fin ?',
    'Une attestation de fin de formation, les résultats de l’évaluation, et des livrables utilisables dès le lendemain : bibliothèque de demandes, charte, plan d’action.',
  ],
]
