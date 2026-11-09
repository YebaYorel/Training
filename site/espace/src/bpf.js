// Préparation du Bilan Pédagogique et Financier (cerfa n° 10443, déclaration sur « Mon Activité Formation »).
// OUTIL DE PRÉPARATION : les rubriques reprennent la structure du formulaire (cadres C à G) sans en recopier
// les numéros de ligne. Avant télédéclaration, chaque montant est contrôlé ligne à ligne avec la notice officielle.
// Échéance : 31 mai de l'année N+1 (art. L.6352-11 et R.6352-22 du code du travail).

export const RUBRIQUES_C = [
  { id: 'entreprises', libelle: 'Entreprises pour la formation de leurs salariés' },
  { id: 'opco-pdc', libelle: 'OPCO — plan de développement des compétences et autres financements' },
  { id: 'opco-pro', libelle: 'OPCO — contrats de professionnalisation' },
  { id: 'opco-cpf', libelle: 'OPCO / Caisse des Dépôts — compte personnel de formation' },
  { id: 'publics-agents', libelle: 'Pouvoirs publics pour la formation de leurs agents' },
  { id: 'france-travail', libelle: 'France Travail' },
  { id: 'region', libelle: 'Conseils régionaux' },
  { id: 'particuliers', libelle: 'Personnes à titre individuel et à leurs frais' },
  { id: 'autres-of', libelle: 'Autres organismes de formation (vous êtes sous-traitant)' },
  { id: 'autres', libelle: 'Autres produits au titre de la formation professionnelle' },
  { id: 'a-classer', libelle: 'À classer (type de client inconnu)' },
]

export const TYPES_STAGIAIRES = [
  { id: 'salaries', libelle: 'Salariés d’employeurs privés' },
  { id: 'demandeurs', libelle: 'Personnes en recherche d’emploi' },
  { id: 'particuliers', libelle: 'Particuliers à leurs propres frais' },
  { id: 'autres', libelle: 'Autres stagiaires (agents publics, bénévoles…)' },
]

const STATUTS_SESSION_EXCLUS = ['Annulée', 'Reportée', 'En construction']
const STATUTS_INSCRIPTION_RETENUS = ['Confirmé', 'Présent', 'Absent', 'Abandon']
const TYPES_FORMATEUR_EXTERNES = ['Externe (Indépendant)', 'Vacataire', 'Sous-traitant']

/** Rubrique du cadre C selon le type de client et le mode de financement de la session. */
export function rubriqueClient(typeClient, financement) {
  switch (typeClient) {
    case 'Entreprise privéé': // orthographe exacte du choix Airtable
    case 'Entreprise privée':
    case 'TPE':
    case 'PME':
    case 'Association 1901':
      return 'entreprises'
    case 'OPCO':
      return financement === 'Contrat Pro' ? 'opco-pro' : financement === 'CPF' ? 'opco-cpf' : 'opco-pdc'
    case 'Collectivité':
      return 'publics-agents'
    case 'France Travail':
      return 'france-travail'
    case 'Particulier':
      return 'particuliers'
    case 'Organisme de formation':
      return 'autres-of'
    default:
      return 'a-classer'
  }
}

function typeStagiaire(financement, typeClient) {
  if (financement === 'France Travail') return 'demandeurs'
  if (typeClient === 'Particulier' || (financement === 'Autofinancement' && !typeClient)) return 'particuliers'
  if (typeClient === 'Collectivité') return 'autres'
  return 'salaries'
}

const annee = (d) => (d ? Number(String(d).slice(0, 4)) : null)
const arrondi = (n) => Math.round(n * 100) / 100

/**
 * @param {object} db    données normalisées (voir donnees.js)
 * @param {number} exercice  année civile (micro-entreprise : exercice = année civile)
 * @param {object} options  { base: 'factures' | 'encaissements', charges: {...}, nsf: { [formation]: code }, reclassement: { [clientId]: rubrique } }
 */
export function calculerBpf(db, exercice, options = {}) {
  const { base = 'factures', charges = {}, nsf = {}, reclassement = {} } = options
  const alertes = []
  const sessionsParId = Object.fromEntries(db.sessions.map((s) => [s.id, s]))

  // ---------- Cadre C : produits ----------
  const produits = Object.fromEntries(RUBRIQUES_C.map((r) => [r.id, 0]))
  const detailC = []
  for (const f of db.factures) {
    if (f.type !== 'Facture' || ['Brouillon', 'Avoir émis'].includes(f.statut)) continue
    const montant = base === 'encaissements' ? f.encaisse || 0 : f.montantHT || 0
    const date = base === 'encaissements' ? f.datePaiement || f.date : f.date
    if (annee(date) !== exercice || !montant) continue
    const client = db.clients[f.client] || {}
    const session = sessionsParId[f.session]
    const financement = session && db.inscriptions.find((i) => i.session === session.id)?.financement
    const rub = reclassement[f.client] || rubriqueClient(client.type, financement)
    produits[rub] += montant
    detailC.push({ ref: f.ref, client: client.nom || '—', typeClient: client.type || '—', rubrique: rub, montant })
  }
  for (const f of db.factures) {
    if (f.type === 'Avoir' && annee(f.date) === exercice && f.montantHT) {
      alertes.push({ niveau: 'info', texte: `Avoir ${f.ref} (${f.montantHT} € HT) : à déduire de la rubrique du client concerné.` })
    }
  }
  const totalC = arrondi(Object.values(produits).reduce((a, b) => a + b, 0))
  if (produits['a-classer'] > 0) {
    alertes.push({ niveau: 'bloquant', texte: `${produits['a-classer']} € de produits sans type de client : classez-les avant de déclarer.` })
  }

  // ---------- Sessions de l'exercice ----------
  // Seules les sessions réalisées (commencées) comptent : une session future n'a ni heures ni stagiaires à déclarer.
  const auj = options.aujourdhui || new Date().toISOString().slice(0, 10)
  const sessions = db.sessions.filter((s) => annee(s.debut) === exercice && s.debut <= auj && !STATUTS_SESSION_EXCLUS.includes(s.statut))
  const idsSessions = new Set(sessions.map((s) => s.id))

  // ---------- Cadre E : formateurs ----------
  const formateurs = { internes: new Map(), externes: new Map() }
  for (const s of sessions) {
    const heures = s.heures || 0
    const liste = s.formateurs.length ? s.formateurs : ['?']
    for (const id of liste) {
      const f = db.formateurs[id] || { nom: 'Formateur non renseigné', type: null }
      if (!db.formateurs[id]) alertes.push({ niveau: 'alerte', texte: `Session « ${s.nom} » sans formateur principal.` })
      const cle = TYPES_FORMATEUR_EXTERNES.includes(f.type) ? 'externes' : 'internes'
      const m = formateurs[cle]
      m.set(id, (m.get(id) || 0) + heures / liste.length)
    }
  }
  const cadreE = {
    internes: { nombre: formateurs.internes.size, heures: arrondi([...formateurs.internes.values()].reduce((a, b) => a + b, 0)) },
    externes: { nombre: formateurs.externes.size, heures: arrondi([...formateurs.externes.values()].reduce((a, b) => a + b, 0)) },
  }

  // ---------- Cadre F : stagiaires et heures-stagiaires (à partir des émargements) ----------
  const f1 = Object.fromEntries(TYPES_STAGIAIRES.map((t) => [t.id, { stagiaires: new Set(), heures: 0 }]))
  const parFormation = {}
  const sousTraitees = { stagiaires: new Set(), heures: 0 }
  for (const ins of db.inscriptions) {
    if (!idsSessions.has(ins.session) || !STATUTS_INSCRIPTION_RETENUS.includes(ins.statut)) continue
    const s = sessionsParId[ins.session]
    const demiJournee = s.jours ? s.heures / s.jours / 2 : 0
    const lignes = db.presences.filter((p) => p.inscription === ins.id)
    if (!lignes.length && s.statut === 'Terminée') {
      alertes.push({ niveau: 'bloquant', texte: `Aucun émargement pour ${db.apprenants[ins.apprenant]?.nom || 'un stagiaire'} — « ${s.nom} ». Sans émargement, pas d'heures déclarables.` })
    }
    const heures = lignes.reduce((a, p) => a + (p.matin ? demiJournee : 0) + (p.apresMidi ? demiJournee : 0), 0)
    const client = db.clients[s.client] || {}
    if (heures === 0) continue // inscrit sans aucune demi-journée émargée : non déclarable
    const type = typeStagiaire(ins.financement, client.type)
    f1[type].stagiaires.add(ins.apprenant)
    f1[type].heures += heures
    const pf = (parFormation[s.formation] ||= { stagiaires: new Set(), heures: 0 })
    pf.stagiaires.add(ins.apprenant)
    pf.heures += heures
    if (s.sousTraiteeA) {
      sousTraitees.stagiaires.add(ins.apprenant)
      sousTraitees.heures += heures
    }
  }
  const cadreF1 = TYPES_STAGIAIRES.map((t) => ({ ...t, stagiaires: f1[t.id].stagiaires.size, heures: arrondi(f1[t.id].heures) }))
  const totalStagiaires = cadreF1.reduce((a, l) => a + l.stagiaires, 0)
  const totalHeures = arrondi(cadreF1.reduce((a, l) => a + l.heures, 0))
  const cadreF4 = Object.entries(parFormation).map(([formation, v]) => ({
    formation,
    nsf: nsf[formation] || '',
    stagiaires: v.stagiaires.size,
    heures: arrondi(v.heures),
  }))
  const sansNsf = cadreF4.filter((l) => !l.nsf)
  if (sansNsf.length) alertes.push({ niveau: 'alerte', texte: `Codes NSF (spécialités de formation) à renseigner : ${sansNsf.length} formation(s), cadre F-4.` })
  if (totalHeures > 0 && totalC === 0) alertes.push({ niveau: 'alerte', texte: 'Des heures sont réalisées mais aucun produit n’est rattaché à l’exercice.' })
  if (totalC > 0 && totalHeures === 0) alertes.push({ niveau: 'alerte', texte: 'Des produits sont déclarés sans aucune heure-stagiaire émargée.' })

  // ---------- Cadre D : charges (saisie) ----------
  const cadreD = {
    total: Number(charges.total) || 0,
    salairesFormateurs: Number(charges.salairesFormateurs) || 0,
    achatsPrestations: Number(charges.achatsPrestations ?? 0) || 0,
  }
  const coutsExternes = arrondi(
    sessions.filter((s) => s.formateurs.some((id) => TYPES_FORMATEUR_EXTERNES.includes(db.formateurs[id]?.type))).reduce((a, s) => a + (s.coutFormateur || 0), 0),
  )
  if (!cadreD.total) alertes.push({ niveau: 'alerte', texte: 'Cadre D : saisissez le total des charges de l’exercice (source : votre comptabilité).' })

  const echeance = new Date(`${exercice + 1}-05-31T23:59:59+04:00`)
  return {
    exercice,
    base,
    echeance,
    cadreC: { produits, total: totalC, detail: detailC },
    cadreD: { ...cadreD, suggestionAchats: coutsExternes },
    cadreE,
    cadreF: { f1: cadreF1, totalStagiaires, totalHeures, f3: [{ libelle: 'Autres formations professionnelles', stagiaires: totalStagiaires, heures: totalHeures }], f4: cadreF4 },
    cadreG: { stagiaires: sousTraitees.stagiaires.size, heures: arrondi(sousTraitees.heures) },
    alertes,
  }
}

/** Export CSV (séparateur « ; », lisible par Excel / LibreOffice en français). */
export function bpfEnCsv(b) {
  const L = [['Cadre', 'Rubrique', 'Valeur']]
  for (const r of RUBRIQUES_C) L.push(['C', r.libelle, b.cadreC.produits[r.id]])
  L.push(['C', 'Total des produits', b.cadreC.total])
  L.push(['D', 'Total des charges', b.cadreD.total])
  L.push(['D', 'dont salaires des formateurs', b.cadreD.salairesFormateurs])
  L.push(['D', 'dont achats de prestations de formation', b.cadreD.achatsPrestations])
  L.push(['E', 'Formateurs internes — nombre', b.cadreE.internes.nombre])
  L.push(['E', 'Formateurs internes — heures', b.cadreE.internes.heures])
  L.push(['E', 'Formateurs externes — nombre', b.cadreE.externes.nombre])
  L.push(['E', 'Formateurs externes — heures', b.cadreE.externes.heures])
  for (const l of b.cadreF.f1) {
    L.push(['F-1', l.libelle + ' — stagiaires', l.stagiaires])
    L.push(['F-1', l.libelle + ' — heures', l.heures])
  }
  for (const l of b.cadreF.f4) L.push(['F-4', `${l.formation} (NSF ${l.nsf || '?'})`, `${l.stagiaires} stagiaires / ${l.heures} h`])
  L.push(['G', 'Stagiaires confiés à un autre organisme', b.cadreG.stagiaires])
  L.push(['G', 'Heures confiées à un autre organisme', b.cadreG.heures])
  const cellule = (v) => {
    const t = String(v ?? '')
    // Neutralise l'injection de formules dans un tableur (=, +, -, @ en début de cellule)
    const sur = /^[=+\-@\t\r]/.test(t) ? "'" + t : t
    return /[;"\n]/.test(sur) ? `"${sur.replace(/"/g, '""')}"` : sur
  }
  return '﻿' + L.map((l) => l.map((v) => (typeof v === 'number' ? String(v).replace('.', ',') : cellule(v))).join(';')).join('\r\n')
}
