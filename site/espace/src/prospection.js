// Prospection & appels d'offres — logique pure (testée par site/espace/test-prospection.mjs).
//
// Trois règles PERMANENTES, voulues par Aurélien LUMEKA (2026-11-22) :
//   1. Chaque message à un professionnel parle de SON métier, et lui laisse dire « STOP » (ou « STP »)
//      quand il le souhaite : sa demande est enregistrée et bloque tout nouvel envoi.
//   2. Expéditeur : uniquement l'adresse de travail. Jamais l'adresse personnelle.
//   3. Rien ne part sans la validation d'Aurélien : l'outil propose, Aurélien décide et envoie lui-même.
//
// RGPD (prospection B2B, position CNIL) : message en rapport avec la profession de la personne,
// identité de l'expéditeur, origine des coordonnées, opposition simple et gratuite, durée de conservation
// limitée (3 ans après le dernier contact). Aucune donnée sensible.

export const EXPEDITEUR = 'yebaformations@gmail.com'
export const ADRESSE_INTERDITE = 'aurelienlumeka@gmail.com'
export const MOTS_STOP = /(^|[^a-zà-ÿ])(stop|stp)([^a-zà-ÿ]|$)/i
export const CONSERVATION_MOIS = 36

export const SIGNATURE = [
  'Aurélien LUMEKA',
  'Directeur, YEBA FORMATIONS (La Réunion)',
  'Organisme certifié Qualiopi n° 25FOR02027.1 · NDA 04973676397',
  'SIRET 814 622 262 00032 · ' + EXPEDITEUR,
]

/* ───────── Métiers : une accroche concrète par métier (règle 1) ───────── */
export const METIERS = {
  commerce: {
    libelle: 'Commerce de détail',
    accroche: 'Dans un commerce, chaque minute passée sur les stocks, les commandes ou les plannings est une minute de moins avec les clients.',
    offre: 'des formations courtes en vente, management d’équipe et IA appliquée au commerce (relances clients, fiches produits, suivi des stocks)',
  },
  hotellerie: {
    libelle: 'Hôtellerie, restauration, tourisme',
    accroche: 'En hôtellerie-restauration, l’accueil fait la différence, mais les réservations, les avis en ligne et les plannings dévorent le temps des équipes.',
    offre: 'des formations en relation client, management et IA pour répondre aux avis, préparer les plannings et gagner du temps en réception',
  },
  btp: {
    libelle: 'BTP, artisanat',
    accroche: 'Dans le BTP, les devis, les comptes rendus de chantier et les dossiers administratifs grignotent les soirées des chefs d’entreprise.',
    offre: 'des formations pratiques pour rédiger devis et comptes rendus plus vite avec l’IA, et pour sécuriser vos données (RGPD)',
  },
  sante: {
    libelle: 'Santé, aide à la personne',
    accroche: 'Dans le soin et l’aide à la personne, le temps administratif pèse sur le temps auprès des bénéficiaires, et les données manipulées sont sensibles.',
    offre: 'des formations en communication, management bienveillant et conformité RGPD des données de santé',
  },
  transport: {
    libelle: 'Transport, logistique',
    accroche: 'En transport et logistique, un planning ou une tournée mal optimisés coûtent cher chaque jour.',
    offre: 'des formations en management d’équipe et en outils d’IA pour planifier, suivre et communiquer plus vite',
  },
  services: {
    libelle: 'Cabinet, conseil, services aux entreprises',
    accroche: 'Dans un cabinet, la valeur est dans le conseil, pas dans la mise en forme des documents ou la recherche d’informations.',
    offre: 'des formations pour intégrer l’IA dans vos méthodes de travail, en conformité avec le RGPD et l’IA Act',
  },
  collectivite: {
    libelle: 'Collectivité, association',
    accroche: 'Dans une collectivité ou une association, les équipes doivent faire plus avec des moyens comptés, en respectant des règles strictes sur les données.',
    offre: 'des formations en management, soft skills et usage responsable de l’IA (RGPD, IA Act)',
  },
}

const sansAccent = (s) => (s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()

/** Le texte parle-t-il vraiment du métier du destinataire ? (contrôle de la règle 1) */
export function parleDuMetier(texte, prospect) {
  const m = METIERS[prospect.metier]
  if (!m) return false
  const t = sansAccent(texte)
  return t.includes(sansAccent(m.accroche).slice(0, 40)) || (prospect.metierPrecis && t.includes(sansAccent(prospect.metierPrecis)))
}

/** Brouillon de premier message. L'IA peut l'améliorer ensuite, mais les contrôles restent les mêmes. */
export function redigerEmail(p) {
  const m = METIERS[p.metier]
  if (!m) throw new Error('Choisissez le métier du destinataire : le message doit parler de son métier.')
  const metier = p.metierPrecis ? `${p.metierPrecis} (${m.libelle.toLowerCase()})` : m.libelle.toLowerCase()
  const bonjour = p.contactNom ? `Bonjour ${p.contactNom},` : 'Bonjour,'
  const objet = `${p.entreprise} : gagner du temps dans votre métier de ${p.metierPrecis || m.libelle.toLowerCase()}`
  const corps = [
    bonjour,
    '',
    `Je vous écris parce que votre activité de ${metier} chez ${p.entreprise} correspond exactement à ce que nous accompagnons à La Réunion.`,
    '',
    m.accroche,
    '',
    `YEBA FORMATIONS propose ${m.offre}. Les formations se font dans vos locaux ou en inter-entreprises, et peuvent être financées par votre OPCO.`,
    '',
    'Seriez-vous d’accord pour un échange de 15 minutes, sans engagement, afin de voir ce qui vous ferait gagner le plus de temps ?',
    '',
    'Bien cordialement,',
    ...SIGNATURE,
    '',
    `Vos coordonnées professionnelles proviennent de : ${p.source || '[source à préciser]'}.`,
    'Vous ne souhaitez plus recevoir de message de ma part ? Répondez simplement STOP : je ne vous écrirai plus.',
  ].join('\n')
  return { objet, corps }
}

const normEmail = (e) => (e || '').trim().toLowerCase()
const domaine = (e) => normEmail(e).split('@')[1] || ''

/** Contrôles BLOQUANTS avant d'ouvrir le message dans la messagerie (règles 1, 2, 3 + RGPD). */
export function controlesEnvoi(p, message, etat) {
  const erreurs = []
  const e = normEmail(p.email)
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(e)) erreurs.push('Adresse e-mail du destinataire invalide.')
  if (!METIERS[p.metier]) erreurs.push('Règle 1 : métier du destinataire non renseigné.')
  else if (!parleDuMetier(message.corps, p)) erreurs.push('Règle 1 : le message ne parle plus du métier du destinataire.')
  if (!MOTS_STOP.test(message.corps)) erreurs.push('Règle 1 : la phrase « Répondez STOP » a disparu du message.')
  if (!p.source?.trim()) erreurs.push('RGPD : origine des coordonnées non renseignée.')
  if (estOppose(e, etat)) erreurs.push('STOP : cette personne (ou son entreprise) a demandé à ne plus être contactée.')
  if (normEmail(etat?.expediteur || EXPEDITEUR) !== EXPEDITEUR) erreurs.push(`Règle 2 : l’expéditeur doit être ${EXPEDITEUR}.`)
  if (e === ADRESSE_INTERDITE) erreurs.push('Règle 2 : adresse personnelle détectée.')
  if (p.statut !== 'valide') erreurs.push('Règle 3 : message pas encore validé par Aurélien.')
  return erreurs
}

export function estOppose(email, etat) {
  const e = normEmail(email)
  return (etat?.oppositions || []).some((o) => o.email === e || (o.domaine && o.domaine === domaine(e)))
}

/** Une réponse contient STOP / STP : on enregistre l'opposition (adresse, et domaine si demandé). */
export function enregistrerOpposition(etat, email, { toutLeDomaine = false, motif = 'Réponse STOP' } = {}) {
  const e = normEmail(email)
  const o = { email: e, date: new Date().toISOString().slice(0, 10), motif }
  if (toutLeDomaine && !/^(gmail|yahoo|hotmail|outlook|orange|wanadoo|free|laposte|icloud|live)\./.test(domaine(e))) o.domaine = domaine(e)
  const oppositions = (etat.oppositions || []).filter((x) => x.email !== e)
  return {
    ...etat,
    oppositions: [o, ...oppositions],
    prospects: (etat.prospects || []).map((p) => (normEmail(p.email) === e || (o.domaine && domaine(p.email) === o.domaine) ? { ...p, statut: 'stop' } : p)),
  }
}

export const detecterStop = (reponse) => MOTS_STOP.test(reponse || '')

/** Ouvre la fenêtre « Nouveau message » de Gmail sur le compte de TRAVAIL (authuser), pré-remplie. Aurélien clique sur Envoyer. */
export function lienGmail(p, message) {
  const q = new URLSearchParams({ authuser: EXPEDITEUR, view: 'cm', fs: '1', to: normEmail(p.email), su: message.objet, body: message.corps })
  return 'https://mail.google.com/mail/?' + q.toString()
}

/** Prospects dont la conservation dépasse 3 ans sans contact (RGPD) : à supprimer. */
export function aPurger(etat, aujourdhui = new Date()) {
  const limite = new Date(aujourdhui)
  limite.setMonth(limite.getMonth() - CONSERVATION_MOIS)
  return (etat.prospects || []).filter((p) => new Date(p.dernierContact || p.cree) < limite)
}

/* ───────── Veille des appels d'offres (BOAMP, open data DILA) ───────── */
// Thèmes de YEBA FORMATIONS et poids : sert à PROPOSER un ordre de priorité, jamais à décider.
export const THEMES = [
  ['intelligence artificielle', 5], ['ia ', 3], ['numerique', 3], ['digital', 2], ['bureautique', 4], ['rgpd', 5],
  ['donnees personnelles', 4], ['cybersecurite', 4], ['management', 4], ['manager', 3], ['vente', 3], ['commercial', 3],
  ['relation client', 4], ['accueil', 2], ['soft skills', 4], ['communication', 2], ['competences transversales', 3],
  ['savoirs de base', 2], ['formation professionnelle', 2], ['formation continue', 2], ['formation', 1],
]

export function requeteBoamp({ departement = '974', jours = 120, aujourdhui = new Date() } = {}) {
  const depuis = new Date(aujourdhui)
  depuis.setDate(depuis.getDate() - jours)
  const d = (x) => x.toISOString().slice(0, 10)
  const conditions = [
    `(search(objet,"formation") or descripteur_libelle="Formation")`,
    `dateparution>=date'${d(depuis)}'`,
  ]
  if (departement) conditions.push(`code_departement="${departement}"`)
  else conditions.push('(' + ['intelligence artificielle', 'numérique', 'bureautique', 'RGPD', 'management', 'relation client', 'vente', 'cybersécurité'].map((m) => `search(objet,"${m}")`).join(' or ') + ')')
  return new URLSearchParams({
    where: conditions.join(' and '),
    order_by: 'dateparution desc',
    limit: '100',
    select: 'idweb,objet,nomacheteur,dateparution,datelimitereponse,nature_libelle,type_marche,descripteur_libelle,code_departement,url_avis,procedure_libelle',
  }).toString()
}

export function scoreAvis(a, aujourdhui = new Date()) {
  const t = ' ' + sansAccent(`${a.objet} ${(a.descripteur_libelle || []).join(' ')}`) + ' '
  const raisons = []
  let score = 0
  for (const [mot, poids] of THEMES) {
    if (t.includes(mot)) {
      score += poids
      raisons.push(mot.trim())
    }
  }
  if ((a.code_departement || []).includes('974')) {
    score += 3
    raisons.push('La Réunion')
  }
  const ouvert = estOuvert(a, aujourdhui)
  if (!ouvert) score = Math.min(score, 2)
  return { score, raisons: [...new Set(raisons)], ouvert }
}

export function estOuvert(a, aujourdhui = new Date()) {
  if (a.nature_libelle && !/avis de march/i.test(a.nature_libelle)) return false
  if (!a.datelimitereponse) return false
  return new Date(a.datelimitereponse) > aujourdhui
}

export function joursRestants(a, aujourdhui = new Date()) {
  if (!a.datelimitereponse) return null
  return Math.ceil((new Date(a.datelimitereponse) - aujourdhui) / 86400000)
}

/** Proposition (règles transparentes) ; la décision GO / NO-GO appartient à Aurélien seul. */
export function proposition(a, aujourdhui = new Date()) {
  const { score, ouvert } = scoreAvis(a, aujourdhui)
  const j = joursRestants(a, aujourdhui)
  if (!ouvert) return { niveau: 'info', texte: 'Clos ou résultat : à garder pour connaître les acheteurs et les attributaires.' }
  if (j !== null && j < 5) return { niveau: 'attention', texte: `Moins de 5 jours : répondre seulement si le dossier est déjà prêt (${j} j).` }
  if (score >= 7) return { niveau: 'fort', texte: 'Proposition : étudier le DCE en priorité (thème YEBA + délai suffisant).' }
  if (score >= 4) return { niveau: 'moyen', texte: 'Proposition : lire le règlement de consultation, vérifier les lots.' }
  return { niveau: 'faible', texte: 'Proposition : peu aligné avec l’offre YEBA, à écarter sauf lot précis.' }
}

export function normaliserAvis(r) {
  return {
    idweb: r.idweb,
    objet: r.objet,
    acheteur: r.nomacheteur,
    parution: r.dateparution,
    limite: r.datelimitereponse,
    nature: r.nature_libelle,
    procedure: r.procedure_libelle,
    departements: r.code_departement || [],
    descripteurs: r.descripteur_libelle || [],
    url: r.url_avis || `https://www.boamp.fr/pages/avis/?q=idweb:${r.idweb}`,
  }
}

export const STATUTS_AO = {
  nouveau: 'Nouveau', etude: 'À étudier', go: 'GO (décidé par Aurélien)', no_go: 'NO-GO (décidé par Aurélien)',
  reponse: 'Réponse en cours', depose: 'Déposé', gagne: 'Gagné', perdu: 'Perdu',
}
export const STATUTS_PROSPECT = {
  brouillon: 'Brouillon', a_valider: 'À valider par Aurélien', valide: 'Validé : prêt à envoyer',
  envoye: 'Envoyé (par Aurélien)', repondu: 'A répondu', stop: 'STOP : ne plus contacter',
}

export const ETAT_VIDE = { version: 1, expediteur: EXPEDITEUR, prospects: [], oppositions: [], ao: {}, journal: [] }

export function journaliser(etat, message) {
  if (!message) return etat
  return { ...etat, journal: [{ date: new Date().toISOString(), message }, ...(etat.journal || [])].slice(0, 500) }
}
