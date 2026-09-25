#!/usr/bin/env node
// Synchronise le catalogue public du site avec Airtable
// (base « YEBA FORMATIONS - Centre de formation (Adaptable) »).
//
//   Mode direct :  AIRTABLE_TOKEN=pat... node site/scripts/airtable-sync.mjs
//   Mode export :  node site/scripts/airtable-sync.mjs --depuis site/airtable
//                  (catalogue-brut.json + sessions-brut.json au format { records: [{ id, fields }] })
//
// Écrit site/src/catalogue.json — seul fichier lu par le site.
// Règles de publication (CONFIG SYSTEME) appliquées ici, pas dans le site :
//   • seules les fiches « Active » et dont la marque YEBA est obligatoire sont publiées
//     (jamais de marque blanche / sous-traitance) ;
//   • aucun tarif si le bloc public commence par ⛔ ;
//   • aucune donnée personnelle : ni client, ni formateur, ni apprenant.
// RGPD : le jeton reste dans l'environnement (.env, secret CI), jamais dans le code ni dans Git.

import { readFile, writeFile } from 'node:fs/promises'
import { resolve, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const ICI = dirname(fileURLToPath(import.meta.url))
const SORTIE = resolve(ICI, '../src/catalogue.json')
const BASE = process.env.AIRTABLE_BASE_ID || 'appQ2zqc80kkc6MR1'
const T_CATALOGUE = 'tblEYxI7LpLZpBPlo'
const T_SESSIONS = 'tblg3KHANR7nq4cH6'

// Identifiants de champs (stables même si un champ est renommé dans Airtable)
const C = {
  ref: 'fldWPKxIdTNSNiK6n', titre: 'fld6Xp5Zw0J0XQSh5', statut: 'fldcMSEP0XWMPuUdR', marque: 'fldpLRGUwDSgGt145',
  type: 'fldjiurLwibphehvH', public: 'fld7CazsUxGR1OxSF', heures: 'fldgkIZrOJeDAxT2F', jours: 'fldmM09bgaAjwhfwY',
  prerequis: 'fldIFQ1HzJaBBoykp', methodes: 'fldNUqS1VCsf2erCm', evaluation: 'fld474uBdXZ6UOltS',
  acces: 'fldbsvcmvRBqUysLD', adaptations: 'fldADYnLuEBfmqnI9', financements: 'fld0grIzQO2B1Vhlq',
  satisfaction: 'fldOOz2pqtG4YpV5Z', reussite: 'fldqIJ1fMpImp1d9x', sessions: 'fldRVW750ot7ierMJ',
  formes: 'fldivCa49hCqSugPe', tarifs: 'fldoIGoiOTyCsZ57q', revision: 'fldpNLAhe2tUe5vOt', rncp: 'fld3WJqOymGw8R35b',
}
const S = {
  formation: 'fldXgTjZg5EtYosdJ', type: 'fldMF7SFMhwYFz7K5', debut: 'fldZYdDetuJDMTNsF', fin: 'fldaTV5honw4xJqQL',
  lieu: 'fldOTKtqKr0sQKhLC', places: 'fldqQx5E0d6APrNL1', restantes: 'fldxfFymB8BV1mUnf', statut: 'fldDJgDZEyHxMmw3q',
}
const MARQUES_PUBLIQUES = ['Catalogue YEBA — marque YEBA obligatoire', 'Client direct — marque YEBA obligatoire']
const STATUTS_SESSION_PUBLICS = ['Planifiée', 'Confirmée', 'Ouverte', 'Inscriptions ouvertes']

const nom = (v) => (v && typeof v === 'object' && !Array.isArray(v) ? v.name : v)
const noms = (v) => (Array.isArray(v) ? v.map(nom).filter(Boolean) : [])
const texte = (v) => (typeof v === 'string' ? v.trim() : '')
const pourcent = (v) => (typeof v === 'number' ? Math.round(v * 100) : null)

/** Coupe les blocs « internes » (consignes en majuscules, ⚠️) pour ne garder que le texte destiné au public. */
function textePublic(v) {
  return texte(v)
    .split(/\n\s*\n/)
    .filter((p) => !/^(⚠️|⛔|FICHE ARCHIV|NE PAS)/.test(p.trim()))
    .join('\n\n')
    .trim()
}

/** Extrait les montants du bloc « TARIFS (bloc public auto) ». */
function lireTarifs(bloc) {
  const t = texte(bloc)
  if (!t || t.startsWith('⛔')) return null
  const n = (re) => {
    const m = t.match(re)
    return m ? Number(m[1].replace(/\s/g, '')) : null
  }
  const tarifs = {
    interTotal: n(/INTER-ENTREPRISES\s*:\s*([\d\s]+)\s*€/),
    interJour: n(/INTER-ENTREPRISES[^\n]*soit\s*([\d\s]+)\s*€/),
    intraTotal: n(/INTRA-ENTREPRISE\s*:\s*([\d\s]+)\s*€/),
    intraJour: n(/INTRA-ENTREPRISE[^\n]*soit\s*([\d\s]+)\s*€/),
    supplement: n(/au-delà de \d+, par jour\s*:\s*([\d\s]+)\s*€/),
    mentionTva: /293 B/.test(t) ? 'TVA non applicable, art. 293 B du CGI' : null,
  }
  return tarifs.interTotal || tarifs.intraTotal ? tarifs : null
}

export function transformer(catalogue, sessions, aujourdHui = new Date()) {
  const refParId = {}
  const formations = []
  for (const r of catalogue.records) {
    const f = r.fields
    refParId[r.id] = f[C.ref]
    if (nom(f[C.statut]) !== 'Active') continue
    if (!MARQUES_PUBLIQUES.includes(nom(f[C.marque]))) continue
    formations.push({
      ref: f[C.ref],
      titre: texte(f[C.titre]),
      type: nom(f[C.type]) || null,
      public: textePublic(f[C.public]),
      heures: f[C.heures] ?? null,
      jours: typeof f[C.jours] === 'number' ? f[C.jours] : null,
      prerequis: textePublic(f[C.prerequis]),
      methodes: noms(f[C.methodes]),
      evaluation: textePublic(f[C.evaluation]),
      acces: textePublic(f[C.acces]),
      adaptations: textePublic(f[C.adaptations]),
      financements: noms(f[C.financements]),
      certification: texte(f[C.rncp]) || null,
      tarifs: lireTarifs(f[C.tarifs]),
      indicateurs: {
        satisfaction: pourcent(f[C.satisfaction]),
        reussite: pourcent(f[C.reussite]),
        sessions: f[C.sessions] ?? null,
        stagiaires: f[C.formes] ?? null,
      },
      revision: f[C.revision] ? String(f[C.revision]).slice(0, 10) : null,
    })
  }
  const refsPubliques = new Set(formations.map((f) => f.ref))
  const jour = aujourdHui.toISOString().slice(0, 10)
  const agenda = sessions.records
    .map((r) => r.fields)
    .filter((s) => nom(s[S.type]) === 'Inter-entreprise')
    .filter((s) => STATUTS_SESSION_PUBLICS.includes(nom(s[S.statut])))
    .filter((s) => s[S.debut] && s[S.debut] >= jour)
    .map((s) => ({
      ref: refParId[(s[S.formation] || [])[0]?.id ?? (s[S.formation] || [])[0]],
      debut: s[S.debut],
      fin: s[S.fin] || s[S.debut],
      lieu: texte(s[S.lieu]),
      placesRestantes: typeof s[S.restantes] === 'number' ? s[S.restantes] : null,
    }))
    .filter((s) => refsPubliques.has(s.ref))
    .sort((a, b) => a.debut.localeCompare(b.debut))
  formations.sort((a, b) => a.ref.localeCompare(b.ref))
  // Pas d’identifiant de base dans le fichier livré au navigateur (aucune aide à la reconnaissance)
  return { synchronise: new Date().toISOString(), formations, agenda }
}

async function toutLire(table, jeton) {
  const records = []
  let offset
  do {
    const url = new URL(`https://api.airtable.com/v0/${BASE}/${table}`)
    url.searchParams.set('returnFieldsByFieldId', 'true')
    if (offset) url.searchParams.set('offset', offset)
    const rep = await fetch(url, { headers: { Authorization: `Bearer ${jeton}` } })
    if (!rep.ok) throw new Error(`Airtable ${table} : HTTP ${rep.status} — vérifiez le jeton et sa portée (data.records:read).`)
    const json = await rep.json()
    records.push(...json.records.map((r) => ({ id: r.id, fields: r.fields })))
    offset = json.offset
  } while (offset)
  return { records }
}

async function principal() {
  const i = process.argv.indexOf('--depuis')
  let catalogue, sessions
  if (i > -1) {
    const dossier = resolve(process.argv[i + 1])
    catalogue = JSON.parse(await readFile(resolve(dossier, 'catalogue-brut.json'), 'utf8'))
    sessions = JSON.parse(await readFile(resolve(dossier, 'sessions-brut.json'), 'utf8'))
  } else {
    const jeton = process.env.AIRTABLE_TOKEN
    if (!jeton) throw new Error('AIRTABLE_TOKEN manquant (voir .env.example).')
    ;[catalogue, sessions] = await Promise.all([toutLire(T_CATALOGUE, jeton), toutLire(T_SESSIONS, jeton)])
  }
  const sortie = transformer(catalogue, sessions)
  await writeFile(SORTIE, JSON.stringify(sortie, null, 2) + '\n')
  console.log(`catalogue.json : ${sortie.formations.length} formations publiques, ${sortie.agenda.length} session(s) inter à venir.`)
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  principal().catch((e) => {
    console.error('Échec de la synchronisation :', e.message)
    process.exit(1)
  })
}
