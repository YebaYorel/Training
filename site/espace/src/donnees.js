// Chargement des données de l'Espace YEBA.
// • Mode « démo » : données fictives (demo.js) — aucune donnée personnelle réelle.
// • Mode « direct » : lecture seule d'Airtable via le proxy local /airtable (vite.espace.config.js),
//   qui ajoute le jeton côté serveur. Le jeton n'arrive JAMAIS dans le navigateur.
// Identifiants de champs stables (un renommage dans Airtable ne casse rien).

const T = {
  indicateurs: 'tblBAwsuKf6Nw8w8Z',
  documents: 'tblSCxGvNSDdH3Blt',
  sessions: 'tblg3KHANR7nq4cH6',
  inscriptions: 'tblUWW5ken5sAUDJk',
  presences: 'tblUF2NHzUmDECDIW',
  evaluations: 'tbllQ4ydL7V62z4kC',
  factures: 'tbl6oAUGfGVBRy7Jl',
  clients: 'tblVLHyTCywkNtmvr',
  formateurs: 'tblgqWIeM7l5qWV8H',
  apprenants: 'tblm9YJud4dK7gD9d',
}

// Minimisation (RGPD art. 5.1.c) : on ne demande que les champs utiles à l'écran — jamais email,
// téléphone, date de naissance ni aménagements des apprenants.
const CHAMPS = {
  indicateurs: {
    n: 'fld6TEv6yHMEomhXU', libelle: 'fldz75ntgZaVJOpW9', critere: 'fldOhbKxX0OnhTWPz', preuves: 'fld2R8cY5rd3pTJf2',
    statut: 'fldog0TrBJSfmJha9', score: 'fldHXR7LucVaqolhG', fichiers: 'fld5FrkBmrI2Gg2Rs', verif: 'fldPmnPK8K6IcTclq',
    prochainAudit: 'fldbQq4SvmePjrRD3', observations: 'fldClSUyYpxuOp3so', actions: 'fldm1O43UWVRldcOz',
    responsable: 'fldu6ycG5cxWO3SDC', nbDocs: 'fld2HXfoOypscbTZe', documents: 'fldujy0FEhQa9b3Cw',
  },
  documents: {
    ref: 'fldFfYg5S7zrqgROf', titre: 'fldFCGhX6WU0PWlsm', version: 'fldqQiP8xnhi84YJ0', statut: 'fldMOFv8zq7OW4BW1',
    date: 'fldyCwllaCBJYedcE', rnq: 'fldS2LL5ZlqPs5ZKI',
  },
  sessions: {
    nom: 'fldNjbYsciSwdUzuc', formation: 'fldv6eSVLQd9juRcs', heures: 'fldbZPoKlbpTOip6J', jours: 'fldaT51SDtAfW8Qbs',
    formateur: 'fldBW9tT98MgFGmLJ', client: 'fldn6I6ix2jjU9F8a', type: 'fldMF7SFMhwYFz7K5', debut: 'fldZYdDetuJDMTNsF',
    fin: 'fldaTV5honw4xJqQL', lieu: 'fldOTKtqKr0sQKhLC', statut: 'fldDJgDZEyHxMmw3q', coutFormateur: 'fldlv3yY7Wy6IBGSy',
    places: 'fldqQx5E0d6APrNL1',
  },
  inscriptions: {
    apprenant: 'fldEGYpvn5SnWJSaP', session: 'fldtHZop33C8Rj2MB', statut: 'fldEN3GdbO3dAiRaG', financement: 'fldIDdTMRCF7NnTDk',
    programme: 'fldRgHz3zBRfkhTDq', convention: 'fldd651EQg0iH6JDm', convocation: 'fldfOUy2H646nHziZ',
    reglement: 'fld9BshTOy8LLe4Zs', rgpd: 'fldnVGJ3OK7m4qv6v', amenagement: 'fldIBBRSSHlY98Tjw',
    positionnement: 'fldCaaUucLn2aAIm8', evalChaud: 'fldCjftEagLsBgZ3q', evalFroid: 'fldHKJL8xDodefrRn',
    attestation: 'fldq0BnnnyPY8l1sm',
  },
  presences: {
    apprenant: 'fld5Xxq9Auw9WYe1E', session: 'fldndaO4Bjg8rTulS', inscription: 'fld9ykGR2qHCQOOvP', date: 'fldMJzp6Glvqiw9Nt',
    matin: 'fldyds0cPXhygrTFr', apresMidi: 'fldEVaWUzNnriqki0', motif: 'fldI9hQaozxWIaxhF',
  },
  evaluations: {
    apprenant: 'fld2o8eHsyrBTAJ0r', session: 'fld3Gm7768WQ0fLUC', type: 'fldtAu7sWSrqS7BAh', date: 'fldCaPWDs5Nr28pbL',
    score: 'fldyzNA1us94QjSAL', max: 'fldqhHjVyykc5cSeO', resultat: 'fldvh7HWs8HBISf7a',
  },
  factures: {
    ref: 'fldYJsUF9bXfQIG2n', type: 'fldlWhqXWJVyl3fBO', client: 'fldxHqI05EOPX8ABS', session: 'fldrec0RZrydBbCEJ',
    montantHT: 'fldrl7ibiAXBiWalV', date: 'fldOfeimF96O4rxtn', statut: 'fldH33pDaAFsJ93vz', encaisse: 'fld7mJwcwlaycfkb6',
    datePaiement: 'fldmcR4ivQyzsh3kk',
  },
  clients: { nom: 'fldnLXDHDfgyR2NoE', type: 'fldlqt4YzfTrjN1ey' },
  formateurs: { nom: 'fldjKrZRBweGoIumy', type: 'flds07Pp88RCf2Jnw' },
  apprenants: { nom: 'fldd30LNm9EjqnjCT' },
}

export { PIECES } from './pieces.js'

const nom = (v) => (v && typeof v === 'object' && !Array.isArray(v) ? v.name : v)
const premier = (v) => (Array.isArray(v) ? v[0] : v)
const lien = (v) => {
  const x = premier(v)
  return x && typeof x === 'object' ? x.id : x || null
}
const liens = (v) => (Array.isArray(v) ? v.map((x) => (typeof x === 'object' ? x.id : x)) : [])
const nombre = (v) => {
  const x = premier(v)
  return typeof x === 'number' ? x : Number(x) || 0
}
const texte = (v) => {
  const x = premier(v)
  return typeof x === 'string' ? x : x?.name || ''
}

async function lireTable(table, champs) {
  const lignes = []
  let offset
  do {
    const p = new URLSearchParams({ returnFieldsByFieldId: 'true', pageSize: '100' })
    Object.values(champs).forEach((id) => p.append('fields[]', id))
    if (offset) p.set('offset', offset)
    const r = await fetch(`/airtable/v0/appQ2zqc80kkc6MR1/${table}?${p}`, { credentials: 'same-origin' })
    if (!r.ok) throw new Error(`Lecture ${table} impossible (HTTP ${r.status}).`)
    const j = await r.json()
    for (const rec of j.records) {
      const o = { id: rec.id }
      for (const [cle, id] of Object.entries(champs)) o[cle] = rec.fields[id]
      lignes.push(o)
    }
    offset = j.offset
  } while (offset)
  return lignes
}

export async function chargerDirect() {
  const brut = Object.fromEntries(
    await Promise.all(Object.entries(T).map(async ([cle, table]) => [cle, await lireTable(table, CHAMPS[cle])])),
  )
  const index = (l, f) => Object.fromEntries(l.map((x) => [x.id, f(x)]))
  return {
    mode: 'direct',
    charge: new Date().toISOString(),
    indicateurs: brut.indicateurs
      .map((x) => ({
        n: nombre(x.n),
        critere: Number((texte(x.critere).match(/Critère (\d)/) || [])[1]) || null,
        critereTexte: texte(x.critere),
        libelle: texte(x.libelle).replace(/\n?\[Synthèse[^\]]*\]/g, '').trim(),
        preuves: texte(x.preuves),
        statut: nom(x.statut) || '',
        score: nom(x.score) || '',
        verif: x.verif || null,
        prochainAudit: x.prochainAudit || null,
        observations: texte(x.observations),
        actions: texte(x.actions),
        responsable: texte(x.responsable),
        nbDocs: nombre(x.nbDocs),
        documents: liens(x.documents),
        fichiers: (x.fichiers || []).map((f) => ({ nom: f.filename, url: f.url, taille: f.size })),
      }))
      .sort((a, b) => a.n - b.n),
    documents: brut.documents.map((x) => ({
      id: x.id, ref: texte(x.ref), titre: texte(x.titre), version: texte(x.version), statut: nom(x.statut) || '', date: x.date || null, rnq: texte(x.rnq),
    })),
    clients: index(brut.clients, (x) => ({ nom: texte(x.nom), type: nom(x.type) || null })),
    formateurs: index(brut.formateurs, (x) => ({ nom: texte(x.nom), type: nom(x.type) || null })),
    apprenants: index(brut.apprenants, (x) => ({ nom: texte(x.nom) })),
    sessions: brut.sessions.map((x) => ({
      id: x.id, nom: texte(x.nom), formation: texte(x.formation), heures: nombre(x.heures), jours: nombre(x.jours),
      formateurs: liens(x.formateur), client: lien(x.client), type: nom(x.type) || '', debut: x.debut || null,
      fin: x.fin || x.debut || null, lieu: texte(x.lieu), statut: nom(x.statut) || '', coutFormateur: nombre(x.coutFormateur),
      places: nombre(x.places), sousTraiteeA: null,
    })),
    inscriptions: brut.inscriptions.map((x) => ({
      id: x.id, apprenant: lien(x.apprenant), session: lien(x.session), statut: nom(x.statut) || '', financement: nom(x.financement) || '',
      pieces: Object.fromEntries(PIECES.map(([k]) => [k, !!x[k]])),
    })),
    presences: brut.presences.map((x) => ({
      id: x.id, apprenant: lien(x.apprenant), session: lien(x.session), inscription: lien(x.inscription), date: x.date || null,
      matin: !!x.matin, apresMidi: !!x.apresMidi, motif: nom(x.motif) || '',
    })),
    evaluations: brut.evaluations.map((x) => ({
      id: x.id, apprenant: lien(x.apprenant), session: lien(x.session), type: nom(x.type) || '', date: x.date || null,
      score: typeof x.score === 'number' ? x.score : null, max: typeof x.max === 'number' ? x.max : null, resultat: nom(x.resultat) || '',
    })),
    factures: brut.factures.map((x) => ({
      id: x.id, ref: texte(x.ref), type: nom(x.type) || '', client: lien(x.client), session: lien(x.session),
      montantHT: nombre(x.montantHT), date: x.date || null, statut: nom(x.statut) || '', encaisse: nombre(x.encaisse), datePaiement: x.datePaiement || null,
    })),
  }
}

/** Vérifie si le proxy local est actif (Espace lancé avec `npm run espace`). */
export async function proxyDisponible() {
  try {
    const r = await fetch('/airtable/etat', { credentials: 'same-origin' })
    if (!r.ok) return false
    const j = await r.json()
    return j.jeton === true
  } catch {
    return false
  }
}
