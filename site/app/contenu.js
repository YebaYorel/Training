/* Contenu éditorial — YEBA FORMATIONS
 *
 * Tout le texte du site est ici, séparé du code. Pour modifier une formation,
 * ajouter une brève de veille ou corriger une mention légale, c'est ce seul
 * fichier qu'on ouvre.
 *
 * Source des données d'organisme et de catalogue : base Airtable
 * appQ2zqc80kkc6MR1, tables CONFIG SYSTEME et CATALOGUE FORMATIONS.
 * Régénérer le catalogue avec `python site/build.py`.
 */

export const ORGANISME = {
  nom: 'YEBA FORMATIONS',
  dirigeant: 'Aurélien LUMEKA',
  fonction: 'Directeur et formateur',
  depuis: 'avril 2021',
  adresse: '9 rue Françoise Châtelain',
  ville: '97490 Sainte-Clotilde, La Réunion',
  tel: '0693 32 24 45',
  telLien: '+262693322445',
  email: 'yebaformations@gmail.com',
  siret: '814 622 262 00032',
  nda: '04973676397',
  qualiopi: '25FOR02027.1',
  qualiopiValidite: '16/02/2027',
  certificateur: 'Qualitia (accrédité COFRAC)',
  horaires: '08h30–12h00 / 13h00–16h30',
  delaiAcces: '15 jours ouvrés',
  autorite: 'DEETS de La Réunion',
};

/* Certifications réelles du dirigeant. Ne rien ajouter ici qui ne soit
   détenu et justifiable : une certification annoncée à tort est une
   pratique commerciale trompeuse (code de la consommation, art. L.121-2). */
export const CERTIFICATIONS = [
  { nom: 'Google AI Specialist', emetteur: 'Google' },
  { nom: 'Google Professional AI', emetteur: 'Google' },
  { nom: 'Référent handicap en organisme de formation', emetteur: 'Formation certifiante' },
  { nom: 'SecNumAcadémie', emetteur: 'ANSSI' },
  { nom: 'MOOC RGPD', emetteur: 'CNIL' },
  { nom: 'Qualiopi 25FOR02027.1', emetteur: 'Qualitia — COFRAC' },
];

export const FORMATIONS = [
  {
    id: 'automatisation', titre: 'Automatisation', domaine: 'Automatisation',
    type: 'Inter-entreprise', heures: 14, jours: 2, tarif: 490,
    accroche: 'Vos tâches répétitives, faites une fois pour toutes.',
    public: 'Dirigeants de TPE-PME, indépendants et fonctions administratives.',
    objectifs: [
      'Repérer dans votre activité les tâches réellement automatisables',
      'Concevoir un enchaînement : déclencheur, conditions, actions',
      'Mettre en place une automatisation sans écrire de code',
      'Sécuriser les données traitées au regard du RGPD',
      'Mesurer le temps gagné et fiabiliser le processus',
    ],
    prerequis: 'Usage courant des outils bureautiques et du web. Aucune programmation.',
  },
  {
    id: 'copilot', titre: 'Copilot pour Microsoft 365', domaine: 'IA Générative',
    type: 'Intra-entreprise', heures: 14, jours: 2, tarif: 425,
    accroche: 'Périmètre, Prompt, Production, Preuve.',
    public: 'Salariés et dirigeants équipés de Microsoft 365 qui produisent chaque semaine des documents ou des analyses.',
    objectifs: [
      "Comprendre pourquoi un assistant relié à vos données ne se pilote pas comme un outil grand public",
      "Déterminer si l'assistant peut atteindre un document donné",
      'Formuler une demande en désignant explicitement les sources',
      'Diagnostiquer une réponse décevante et choisir le bon correctif',
      'Trier : je saisis, j’anonymise d’abord, je ne saisis jamais',
    ],
    prerequis: 'Licence Copilot active et nominative par stagiaire, documents professionnels réels accessibles, administrateur joignable. Conditions vérifiées par écrit 5 jours ouvrés avant.',
  },
  {
    id: 'emailing', titre: "Emailings professionnels avec l'IA", domaine: 'IA Générative',
    type: 'Intra-entreprise', heures: 14, jours: 2, tarif: 425,
    accroche: 'Un courriel qui obtient une réponse.',
    public: 'Dirigeants, commerciaux, fonctions administratives et chargés de communication.',
    objectifs: [
      'Constituer et segmenter une base de contacts conforme au RGPD',
      "Écrire l'objet, l'accroche, le corps et l'appel à l'action",
      'Concevoir une séquence de courriels et en régler le rythme',
      'Être reçu : délivrabilité, désinscription, expéditeur identifié',
      'Corriger à partir des indicateurs réels',
    ],
    prerequis: 'Usage courant d’une messagerie et d’un tableur. Venez avec votre situation réelle.',
  },
  {
    id: 'ia-generative', titre: 'IA Générative', domaine: 'IA Générative',
    type: 'Inter-entreprise', heures: 14, jours: 2, tarif: 490,
    accroche: 'Comprendre, piloter, vérifier.',
    public: 'Professionnels, indépendants et salariés souhaitant intégrer l’IA dans leur quotidien.',
    objectifs: [
      'Expliquer le fonctionnement et les limites des modèles',
      'Rédiger des consignes efficaces et itérer',
      'Mobiliser l’IA sur des tâches métier concrètes',
      'Maîtriser les risques : confidentialité, erreurs factuelles, biais',
      'Rester conforme au RGPD et au règlement européen sur l’IA',
    ],
    prerequis: 'Aisance avec un navigateur et les outils bureautiques.',
  },
  {
    id: 'site-vocal', titre: 'Produire un site Internet en vocal', domaine: 'IA Générative',
    type: 'Intra-entreprise', heures: 14, jours: 2, tarif: 425,
    accroche: 'Votre site, à la voix. Et vous le gardez.',
    public: 'Dirigeants de TPE, artisans, commerçants et créateurs sans site — ou avec un site qu’ils ne peuvent pas modifier seuls.',
    objectifs: [
      'Formuler à l’oral un cahier des charges exploitable',
      'Piloter un générateur de site et corriger par itérations',
      'Vérifier chaque contenu : textes, tarifs, coordonnées',
      'Mettre en ligne un site conforme : mentions, confidentialité, traceurs',
      'Le maintenir seul, sans rappeler un prestataire',
    ],
    prerequis: 'Usage courant d’un ordinateur. Aucune compétence en développement. Venez avec votre projet réel.',
    noteHandicap: 'La saisie clavier est acceptée en substitution intégrale de la dictée : la compétence évaluée est la structuration de la demande, pas la production sonore. Parcours entièrement réalisable au clavier.',
  },
  {
    id: 'rgpd-cyber', titre: 'RGPD & Cybersécurité', domaine: 'RGPD & Conformité',
    type: 'Inter-entreprise', heures: 14, jours: 2, tarif: 490,
    accroche: 'Savoir quoi faire dans les 72 heures.',
    public: 'Dirigeants, responsables administratifs, et tout salarié manipulant des données personnelles.',
    objectifs: [
      'Identifier les traitements soumis au RGPD dans votre activité',
      'Appliquer les six principes : licéité, minimisation, exactitude, conservation, sécurité, responsabilité',
      'Constituer et tenir à jour un registre des traitements',
      'Prévenir hameçonnage, rançongiciel et mots de passe faibles',
      'Réagir à une violation : mesures conservatoires et notification CNIL sous 72 h',
    ],
    prerequis: 'Aucun prérequis technique.',
  },
  {
    id: 'vente', titre: 'Initiation à la vente', domaine: 'Vente & Management',
    type: 'Inter-entreprise', heures: 7, jours: 1, tarif: 390,
    accroche: 'De la découverte à la signature.',
    public: 'Créateurs d’entreprise, indépendants, commerciaux débutants.',
    objectifs: [
      'Dérouler un entretien, de la préparation à la conclusion',
      'Mener une découverte par un questionnement structuré',
      'Construire une proposition de valeur adaptée au besoin',
      'Traiter les objections courantes avec méthode',
      'Conclure et organiser le suivi',
    ],
    prerequis: 'Aucun prérequis.',
    noteHandicap: 'Les jeux de rôle peuvent se tenir en trio fermé, ou être remplacés par un rôle d’observateur à la grille critériée, ou par une étude de cas écrite.',
  },
];

/* Veille — à compléter à la main. Chaque entrée porte sa date et sa source :
   une brève sans source n'est pas de la veille, c'est une rumeur. */
export const VEILLE = [
  {
    date: '2026-09-15', categorie: 'IA Act',
    titre: 'Obligations des modèles à usage général : où en est-on',
    resume: "Les obligations applicables aux modèles d'IA à usage général sont entrées en vigueur le 2 août 2025. Les fournisseurs doivent tenir une documentation technique, publier un résumé des données d'entraînement et respecter le droit d'auteur.",
    impact: "Vous êtes déployeur, pas fournisseur : ces obligations ne pèsent pas sur vous. En revanche, elles conditionnent ce que vos fournisseurs doivent pouvoir vous remettre — exigez-le par écrit.",
    source: 'Règlement (UE) 2024/1689, art. 53 à 55',
  },
  {
    date: '2026-09-10', categorie: 'RGPD',
    titre: 'Assistants IA connectés aux fichiers de l’entreprise',
    resume: "Un assistant relié à la bureautique d'une entreprise hérite des droits d'accès de la personne qui l'utilise. Si ces droits sont trop larges, l'assistant expose des documents que le salarié n'aurait jamais ouverts de lui-même.",
    impact: "Avant tout déploiement : auditer les droits d'accès. C'est la première séquence de la journée 2 de la formation Copilot.",
    source: 'RGPD art. 5.1.f et 32 — sécurité du traitement',
  },
  {
    date: '2026-09-02', categorie: 'Formation',
    titre: 'Littératie en IA : une obligation, pas une bonne pratique',
    resume: "Depuis le 2 février 2025, tout déployeur de systèmes d'IA doit veiller à ce que son personnel dispose d'un niveau suffisant de maîtrise de l'IA.",
    impact: "L'obligation ne prévoit pas de format imposé, mais elle suppose de pouvoir en apporter la preuve. Une attestation de formation en est une.",
    source: 'Règlement (UE) 2024/1689, art. 4',
  },
];

/* Base de connaissances de l'assistant. Chaque entrée associe des mots-clés à
   une réponse vérifiée. Aucun modèle de langage n'est appelé : rien de ce que
   le visiteur écrit ne quitte son navigateur. */
export const FAQ = [
  {
    cles: ['cpf', 'compte personnel', 'mon compte formation'],
    reponse: "Nos formations ne sont pas éligibles au CPF : aucune ne porte de code RNCP ou RS. Nous préférons le dire clairement. En revanche, elles sont finançables par votre OPCO, votre plan de développement des compétences, France Travail, l'AIF ou la Région Réunion.",
  },
  {
    cles: ['financement', 'opco', 'financer', 'prise en charge', 'aide', 'subvention'],
    reponse: "Les formations sont finançables par votre OPCO, votre plan de développement des compétences, France Travail, l'AIF et la Région Réunion. Le montage du dossier fait partie de la prestation — c'est ce que couvre le délai de 15 jours ouvrés avant le démarrage.",
  },
  {
    cles: ['prix', 'tarif', 'coût', 'cout', 'combien', 'euros'],
    reponse: "De 390 à 490 € HT par jour et par personne en inter-entreprise, selon le domaine. En intra, le tarif est au groupe. La formation professionnelle est exonérée de TVA (art. 261-4-4° a du CGI) ; le conseil et l'audit y sont soumis, au taux de 8,5 % en outre-mer.",
  },
  {
    cles: ['handicap', 'accessible', 'accessibilité', 'aménagement', 'rqth', 'malvoyant', 'sourd'],
    reponse: "Toutes nos formations sont accessibles. Aucun justificatif médical n'est demandé : seul le besoin d'aménagement est recueilli, conformément à l'article 9 du RGPD. Supports en corps 26 points minimum, contrastes conformes WCAG 2.1 AA, consignes à l'oral et à l'écrit. Référent handicap : Aurélien Lumeka, réponse sous 48 h ouvrées.",
  },
  {
    cles: ['délai', 'delai', 'quand', 'inscription', 'inscrire', 'démarrer', 'commencer'],
    reponse: "Comptez 15 jours ouvrés minimum entre l'inscription et le démarrage. Ce délai couvre le montage du dossier de financement, l'envoi du test de positionnement et la convocation. Le parcours : prise de contact, analyse du besoin, devis sous 5 jours ouvrés, convention signée, démarrage.",
  },
  {
    cles: ['horaire', 'heure', 'journée', 'pause', 'durée'],
    reponse: "Les journées se déroulent de 08h30 à 12h00 puis de 13h00 à 16h30, soit 7 heures de formation. Pauses de 15 minutes à 10h00 et 15h00, pause méridienne d'une heure.",
  },
  {
    cles: ['qualiopi', 'certifié', 'certification', 'certifie', 'sérieux'],
    reponse: "YEBA FORMATIONS est certifié Qualiopi sous le n° 25FOR02027.1 au titre des actions de formation, par Qualitia, organisme accrédité COFRAC, jusqu'au 16/02/2027. Déclaration d'activité n° 04973676397 auprès du Préfet de La Réunion — cet enregistrement ne vaut pas agrément de l'État.",
  },
  {
    cles: ['rgpd', 'données', 'donnees', 'confidentialité', 'conformité', 'cnil'],
    reponse: "C'est l'un de nos domaines : formation RGPD & Cybersécurité, et missions de conseil en gouvernance. Ce site lui-même ne dépose aucun traceur et ne mesure pas votre audience — il n'y a rien à consentir. Nos outils de travail sont choisis pour rester dans l'Union européenne.",
  },
  {
    cles: ['ia act', 'ia-act', 'règlement ia', 'reglement ia', 'risque', 'haut risque'],
    reponse: "Le règlement (UE) 2024/1689 classe les systèmes par niveau de risque. Les outils de productivité relèvent du risque minimal. Attention : un tri de candidatures, un scoring de prospects ou une évaluation de salariés bascule en annexe III — haut risque, avec analyse d'impact, documentation et supervision humaine. Nous qualifions chaque projet avant de le déployer.",
  },
  {
    cles: ['intra', 'inter', 'chez nous', 'sur site', 'locaux', 'distance', 'visio'],
    reponse: "En intra, nous venons dans vos locaux et le programme est ajusté à votre activité. En inter, vous rejoignez un groupe à Sainte-Clotilde. Toutes nos formations sont en présentiel : la manipulation accompagnée est ce qui fait la différence.",
  },
  {
    cles: ['contact', 'joindre', 'téléphone', 'telephone', 'appeler', 'devis', 'rendez-vous'],
    reponse: "Par téléphone au 0693 32 24 45, ou par courriel à yebaformations@gmail.com. Un appel de quinze minutes suffit généralement à savoir si une formation est la bonne réponse — ou si autre chose le serait davantage.",
  },
  {
    cles: ['formation', 'formations', 'catalogue', 'proposez', 'apprendre'],
    reponse: "Sept formations : IA générative, Copilot pour Microsoft 365, emailings avec l'IA, produire un site en vocal, automatisation, RGPD & cybersécurité, et initiation à la vente. Chacune se termine par un livrable que vous emportez.",
  },
  {
    cles: ['qui', 'aurélien', 'aurelien', 'lumeka', 'formateur', 'expérience'],
    reponse: "Aurélien Lumeka dirige YEBA FORMATIONS depuis avril 2021. Formateur en vente, management et compétences comportementales, il s'est spécialisé en IA, implémentation de solutions en entreprise et gouvernance RGPD / IA Act. Certifié Google AI Specialist, Google Professional AI, SecNumAcadémie (ANSSI), MOOC RGPD de la CNIL, et référent handicap.",
  },
];

export const REPONSE_PAR_DEFAUT =
  "Je n'ai pas la réponse à cette question. Essayez un mot comme « tarif », « financement », « handicap », « délai » ou « RGPD ». Pour tout le reste, Aurélien répond directement au 0693 32 24 45.";
