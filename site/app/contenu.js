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

/* Catalogue — importé de formations.js, GÉNÉRÉ depuis Airtable par
   `python site/build.py`. Ne jamais éditer le catalogue ici : il serait
   écrasé à la prochaine génération, et les deux sources divergeraient. */
import { FORMATIONS as CATALOGUE } from './formations.js';

/* Surcouche éditoriale : précisions d'accessibilité propres à certaines
   formations. Elles relèvent de la pédagogie, pas de la gestion, et n'ont
   donc pas leur place dans Airtable. Rapprochées par identifiant de fiche. */
const NOTES_HANDICAP = {
  rec1H1ma1PJSh1gnO:
    "La saisie clavier est acceptée en substitution intégrale de la dictée : la "
    + "compétence évaluée est la structuration de la demande, pas la production "
    + "sonore. Parcours entièrement réalisable au clavier.",
  recpSsg0jyP4uj2ed:
    "Les jeux de rôle peuvent se tenir en trio fermé, ou être remplacés par un "
    + "rôle d'observateur à la grille critériée, ou par une étude de cas écrite.",
};

export const FORMATIONS = CATALOGUE.map((f) => ({
  ...f,
  noteHandicap: NOTES_HANDICAP[f.id],
}));

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
