#!/usr/bin/env node
// Serveur YEBA Studio — minimal, sans dépendance, à héberger dans l'UE (Scaleway, OVH VPS, Clever Cloud…).
// Trois rôles, rien de plus :
//   1. Paiement : crée un paiement Mollie (société néerlandaise) pour une offre, au prix fixé ICI (jamais par le client).
//   2. Licence : une fois le paiement « paid », signe la licence liée au poste du client (Ed25519).
//   3. IA : relaie vers Mistral AI (Paris) les demandes des licences CARBURANT / Parcours, avec quotas.
// Aucune donnée de stagiaire n'est stockée ici. Les textes envoyés à l'IA sont pseudonymisés par le logiciel.
//
// Variables d'environnement : voir serveur/README.md.
import { createServer } from 'node:http'
import { OFFRES, CODE_POSTE_VALIDE, signer, verifier } from '../site/espace/src/licence.js'
import { chargeLicence, chargerClePrivee } from '../site/scripts/licence.mjs'

const E = process.env
const PORT = Number(E.PORT || 8787)
const ORIGINES = (E.ORIGINES || 'http://127.0.0.1:5180').split(',').map((s) => s.trim())
const MOLLIE = E.MOLLIE_API || 'https://api.mollie.com'
const MISTRAL = E.MISTRAL_API || 'https://api.mistral.ai'
const MODELE = E.MISTRAL_MODELE || 'mistral-small-latest'
const AIRTABLE_BASE = E.AIRTABLE_BASE_ID || 'appQ2zqc80kkc6MR1'
const T_LICENCES = 'tblCr0eK7l3mWZINx'
const QUOTA_IA_JOUR = Number(E.QUOTA_IA_JOUR || 60)

/* ---------- Outils HTTP ---------- */
function repondre(res, code, corps, req) {
  const origine = req?.headers.origin
  if (origine && ORIGINES.includes(origine)) {
    res.setHeader('Access-Control-Allow-Origin', origine)
    res.setHeader('Vary', 'Origin')
  }
  res.setHeader('Content-Type', 'application/json; charset=utf-8')
  res.setHeader('X-Content-Type-Options', 'nosniff')
  res.setHeader('Cache-Control', 'no-store')
  res.statusCode = code
  res.end(JSON.stringify(corps))
}

async function lireJson(req, max = 16384) {
  let taille = 0
  const morceaux = []
  for await (const m of req) {
    taille += m.length
    if (taille > max) throw Object.assign(new Error('Requête trop volumineuse.'), { code: 413 })
    morceaux.push(m)
  }
  try {
    return JSON.parse(Buffer.concat(morceaux).toString('utf8') || '{}')
  } catch {
    throw Object.assign(new Error('JSON invalide.'), { code: 400 })
  }
}

// Limiteur en mémoire (suffisant pour une instance ; à déporter si plusieurs instances)
const compteurs = new Map()
function limite(cle, max, fenetreMs) {
  const maintenant = Date.now()
  const c = compteurs.get(cle)
  if (!c || c.fin < maintenant) {
    compteurs.set(cle, { n: 1, fin: maintenant + fenetreMs })
    return true
  }
  c.n++
  return c.n <= max
}
setInterval(() => {
  const m = Date.now()
  for (const [k, v] of compteurs) if (v.fin < m) compteurs.delete(k)
}, 600000).unref()

const texte = (v, max) => String(v ?? '').replace(/[\u0000-\u001f]/g, ' ').trim().slice(0, max)
const EMAIL = /^[^\s@]{1,64}@[^\s@]{1,190}\.[a-z]{2,}$/i
const SIRET = /^\d{14}$/

/* ---------- Mollie ---------- */
async function mollie(chemin, options = {}) {
  if (!E.MOLLIE_API_KEY) throw Object.assign(new Error('Paiement non configuré.'), { code: 503 })
  const r = await fetch(MOLLIE + chemin, {
    ...options,
    headers: { Authorization: `Bearer ${E.MOLLIE_API_KEY}`, 'Content-Type': 'application/json' },
  })
  const j = await r.json().catch(() => ({}))
  if (!r.ok) throw Object.assign(new Error('Le service de paiement a refusé la demande.'), { code: 502, detail: j?.detail })
  return j
}

/* ---------- Airtable (registre des licences, facultatif) ---------- */
async function airtable(chemin, options = {}) {
  if (!E.AIRTABLE_TOKEN) return null
  const r = await fetch(`${E.AIRTABLE_API || 'https://api.airtable.com'}/v0/${AIRTABLE_BASE}/${T_LICENCES}${chemin}`, {
    ...options,
    headers: { Authorization: `Bearer ${E.AIRTABLE_TOKEN}`, 'Content-Type': 'application/json' },
  })
  return r.ok ? r.json() : null
}
async function dejaClientCarburant(siret) {
  const j = await airtable(`?maxRecords=1&filterByFormula=${encodeURIComponent(`AND({SIRET client}='${siret}',{Offre}='carburant')`)}`)
  return j ? j.records.length > 0 : true // sans registre : pas de 1er mois à 1 € (évite l'abus)
}
async function enregistrerLicence(charge, montant) {
  const existe = await airtable(`?maxRecords=1&filterByFormula=${encodeURIComponent(`{Référence paiement}='${charge.lic}'`)}`)
  if (!existe || existe.records.length) return
  await airtable('', {
    method: 'POST',
    body: JSON.stringify({
      typecast: true,
      records: [{ fields: {
        'N° licence': charge.lic, Offre: charge.off, 'Organisme client': charge.org, 'SIRET client': charge.siret || '',
        'Utilisateur (nom)': charge.nom, 'Email utilisateur': charge.email, 'Code poste': charge.poste,
        Début: charge.deb, Fin: charge.fin, 'Montant payé HT': montant, 'Référence paiement': charge.lic, Statut: 'Active',
        'Transferts de poste': 0, 'Tarif pionnier gelé': charge.off === 'carburant',
      } }],
    }),
  })
}

/* ---------- IA (Mistral) ---------- */
const TACHES = {
  relance: {
    json: false,
    systeme:
      "Tu rédiges, en français professionnel et courtois, un courriel de relance de paiement d'un organisme de formation vers un OPCO ou une entreprise. " +
      "Utilise UNIQUEMENT les faits fournis (références, montants, dates). N'invente aucun chiffre, aucune date, aucune référence. " +
      "Structure : objet, formule d'appel, rappel factuel, pièces jointes rappelées, demande claire avec délai, formule de politesse. 180 mots maximum.",
  },
  accord: {
    json: true,
    systeme:
      "Tu extrais les informations d'un accord de prise en charge OPCO collé par l'utilisateur. Réponds en JSON strict : " +
      '{"opco":string|null,"numero_dossier":string|null,"entreprise":string|null,"formation":string|null,"date_debut":"AAAA-MM-JJ"|null,' +
      '"date_fin":"AAAA-MM-JJ"|null,"heures":number|null,"montant_accorde_ht":number|null,"subrogation":boolean|null,"pieces_exigees":string[],"remarques":string}. ' +
      "Mets null quand l'information n'est pas écrite dans le texte. N'invente rien.",
  },
  expliquer: {
    json: false,
    systeme:
      "Tu expliques en 3 phrases simples, à un dirigeant d'organisme de formation, pourquoi l'alerte fournie bloque ou retarde un paiement, " +
      "puis tu donnes l'action concrète à faire. Pas de jargon, pas de chiffres inventés.",
  },
  convocation: {
    json: false,
    systeme:
      "Tu rédiges un courriel de convocation chaleureux et clair pour une formation professionnelle, à partir des informations fournies " +
      "(intitulé, dates, horaires, lieu, contact, aménagements handicap). N'invente aucune information manquante : écris [à compléter]. 150 mots maximum.",
  },
}

async function mistral(tache, contenu) {
  if (!E.MISTRAL_API_KEY) throw Object.assign(new Error('IA non configurée sur le serveur.'), { code: 503 })
  const t = TACHES[tache]
  const r = await fetch(`${MISTRAL}/v1/chat/completions`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${E.MISTRAL_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: MODELE,
      temperature: 0.2,
      max_tokens: 700,
      messages: [
        { role: 'system', content: t.systeme },
        { role: 'user', content: contenu },
      ],
      ...(t.json ? { response_format: { type: 'json_object' } } : {}),
    }),
  })
  if (!r.ok) throw Object.assign(new Error('Le service d’IA est indisponible, réessayez dans un instant.'), { code: 502 })
  const j = await r.json()
  const sortie = j.choices?.[0]?.message?.content ?? ''
  if (!t.json) return { texte: sortie }
  try {
    return { donnees: JSON.parse(sortie) }
  } catch {
    return { texte: sortie }
  }
}

/* ---------- Routes ---------- */
async function routeur(req, res) {
  const url = new URL(req.url, 'http://local')
  const ip = req.headers['x-forwarded-for']?.split(',')[0].trim() || req.socket.remoteAddress
  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST')
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type')
    res.setHeader('Access-Control-Max-Age', '600')
    return repondre(res, 204, {}, req)
  }
  if (req.headers.origin && !ORIGINES.includes(req.headers.origin)) return repondre(res, 403, { erreur: 'Origine refusée.' })

  if (req.method === 'GET' && url.pathname === '/api/sante') {
    return repondre(res, 200, { ok: true, paiement: !!E.MOLLIE_API_KEY, ia: !!E.MISTRAL_API_KEY, offres: Object.fromEntries(Object.entries(OFFRES).map(([k, o]) => [k, { nom: o.nom, prix: o.prix, libelle: o.libellePrix }])) }, req)
  }

  if (req.method === 'POST' && url.pathname === '/api/commande') {
    if (!limite('cmd:' + ip, 10, 3600000)) return repondre(res, 429, { erreur: 'Trop de tentatives, réessayez plus tard.' }, req)
    const b = await lireJson(req)
    const offre = OFFRES[b.offre] ? b.offre : null
    const poste = texte(b.poste, 14)
    const email = texte(b.email, 120)
    const siret = texte(b.siret, 14).replace(/\s/g, '')
    const nom = texte(b.nom, 80)
    const organisme = texte(b.organisme, 120)
    if (!offre || !CODE_POSTE_VALIDE.test(poste) || !EMAIL.test(email) || !SIRET.test(siret) || nom.length < 2 || organisme.length < 2) {
      return repondre(res, 400, { erreur: 'Informations incomplètes : offre, code poste, nom, email, organisme et SIRET (14 chiffres) sont requis.' }, req)
    }
    let prix = OFFRES[offre].prix
    if (offre === 'carburant' && OFFRES.carburant.premierMois && !(await dejaClientCarburant(siret))) prix = OFFRES.carburant.premierMois
    const p = await mollie('/v2/payments', {
      method: 'POST',
      body: JSON.stringify({
        amount: { currency: 'EUR', value: prix.toFixed(2) },
        description: `YEBA Studio — ${OFFRES[offre].nom}`,
        redirectUrl: `${E.URL_APPLI || ORIGINES[0]}/#licences`,
        locale: 'fr_FR',
        metadata: { offre, poste, nom, email, organisme, siret },
      }),
    })
    return repondre(res, 200, { paiement: p.id, url: p._links?.checkout?.href, montant: prix }, req)
  }

  if (req.method === 'GET' && url.pathname === '/api/licence') {
    const id = texte(url.searchParams.get('paiement'), 40)
    if (!/^tr_[A-Za-z0-9]{6,30}$/.test(id)) return repondre(res, 400, { erreur: 'Référence de paiement invalide.' }, req)
    if (!limite('lic:' + ip, 60, 3600000)) return repondre(res, 429, { erreur: 'Trop de tentatives.' }, req)
    const p = await mollie(`/v2/payments/${id}`)
    if (p.status !== 'paid') return repondre(res, 200, { etat: p.status }, req)
    const m = p.metadata || {}
    const charge = { ...chargeLicence({ offre: m.offre, poste: m.poste, nom: m.nom, email: m.email, organisme: m.organisme, debut: p.paidAt || new Date(), reference: p.id }), siret: m.siret }
    const licence = await signer(charge, await chargerClePrivee())
    enregistrerLicence(charge, Number(p.amount?.value || 0)).catch(() => {})
    return repondre(res, 200, { etat: 'paid', licence }, req)
  }

  if (req.method === 'POST' && url.pathname === '/api/ia') {
    const b = await lireJson(req, 24000)
    const v = await verifier(b.licence, texte(b.poste, 14))
    if (!v.ok) return repondre(res, 403, { erreur: v.raison }, req)
    const modules = OFFRES[v.charge.off].modules
    if (!modules.includes('carburant') && !modules.includes('parcours')) return repondre(res, 403, { erreur: 'Votre offre n’inclut pas l’IA.' }, req)
    if (!TACHES[b.tache]) return repondre(res, 400, { erreur: 'Tâche inconnue.' }, req)
    if (!limite('ia:' + v.charge.lic + ':' + new Date().toISOString().slice(0, 10), QUOTA_IA_JOUR, 86400000)) {
      return repondre(res, 429, { erreur: `Quota du jour atteint (${QUOTA_IA_JOUR} demandes). Il se renouvelle demain.` }, req)
    }
    const contenu = texte(b.contenu, 6000)
    if (contenu.length < 10) return repondre(res, 400, { erreur: 'Texte trop court.' }, req)
    return repondre(res, 200, { ...(await mistral(b.tache, contenu)), avertissement: 'Texte produit par une IA (Mistral) : relisez avant tout envoi.' }, req)
  }

  return repondre(res, 404, { erreur: 'Introuvable.' }, req)
}

export function demarrer(port = PORT) {
  const serveur = createServer((req, res) =>
    routeur(req, res).catch((e) => repondre(res, e.code && e.code < 600 ? e.code : 500, { erreur: e.code ? e.message : 'Erreur interne.' }, req)),
  )
  serveur.headersTimeout = 10000
  serveur.requestTimeout = 15000
  return new Promise((ok) => serveur.listen(port, E.HOTE || '127.0.0.1', () => ok(serveur)))
}

if (process.argv[1]?.endsWith('serveur.mjs')) {
  demarrer().then(() => console.log(`Serveur YEBA Studio sur le port ${PORT} — paiement ${E.MOLLIE_API_KEY ? 'actif' : 'NON configuré'}, IA ${E.MISTRAL_API_KEY ? 'active' : 'NON configurée'}.`))
}
