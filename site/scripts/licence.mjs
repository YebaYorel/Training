#!/usr/bin/env node
// Outil d'émission des licences YEBA Studio (à lancer sur le poste de YEBA FORMATIONS uniquement).
//
//   npm run licence -- cles                       → crée la paire de clés (une seule fois !)
//   npm run licence -- emettre --offre bpf --poste K7QM-2XPA-9RTD --nom "Marie Hoarau" \
//        --email marie@exemple.re --organisme "OF Exemple" [--jours 365] [--debut 2026-10-01]
//   npm run licence -- verifier <licence> <code-poste>
//
// La clé PRIVÉE reste dans .env (LICENCE_CLE_PRIVEE) : ne jamais la committer, ne jamais l'envoyer.
// La clé PUBLIQUE est écrite dans site/espace/src/licence-cle.json (elle peut être publiée).
import { readFile, writeFile, appendFile } from 'node:fs/promises'
import { existsSync } from 'node:fs'
import { resolve, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { randomUUID } from 'node:crypto'
import { OFFRES, CODE_POSTE_VALIDE, signer, verifier } from '../espace/src/licence.js'

const RACINE = resolve(dirname(fileURLToPath(import.meta.url)), '../..')
const FICHIER_PUBLIC = resolve(RACINE, 'site/espace/src/licence-cle.json')
const ENV = resolve(RACINE, '.env')
const b64 = (o) => Buffer.from(o).toString('base64')

export async function chargerClePrivee(texte = process.env.LICENCE_CLE_PRIVEE) {
  if (!texte) throw new Error('LICENCE_CLE_PRIVEE absente (.env). Lancez d’abord : npm run licence -- cles')
  return crypto.subtle.importKey('pkcs8', Buffer.from(texte, 'base64'), { name: 'Ed25519' }, false, ['sign'])
}

/** Construit la charge d'une licence à partir d'une offre (logique partagée avec le serveur). */
export function chargeLicence({ offre, poste, nom, email, organisme, debut = new Date(), jours, reference }) {
  const o = OFFRES[offre]
  if (!o) throw new Error(`Offre inconnue : ${offre} (${Object.keys(OFFRES).join(', ')})`)
  if (!CODE_POSTE_VALIDE.test(poste || '')) throw new Error('Code poste invalide (format XXXX-XXXX-XXXX).')
  const d = new Date(debut)
  const duree = jours ?? o.jours
  const fin = duree ? new Date(d.getTime() + duree * 86400000).toISOString().slice(0, 10) : null
  return {
    lic: reference || randomUUID().slice(0, 8).toUpperCase(),
    off: offre,
    nom: String(nom || '').slice(0, 80),
    email: String(email || '').slice(0, 120),
    org: String(organisme || '').slice(0, 120),
    poste,
    deb: d.toISOString().slice(0, 10),
    fin,
  }
}

function options(argv) {
  const o = {}
  for (let i = 0; i < argv.length; i++) if (argv[i].startsWith('--')) o[argv[i].slice(2)] = argv[i + 1]?.startsWith('--') ? true : argv[++i]
  return o
}

async function lireEnv() {
  if (!existsSync(ENV)) return
  for (const l of (await readFile(ENV, 'utf8')).split('\n')) {
    const m = l.match(/^\s*([A-Z_]+)\s*=\s*(.*)\s*$/)
    if (m && !process.env[m[1]]) process.env[m[1]] = m[2].replace(/^["']|["']$/g, '')
  }
}

async function principal() {
  await lireEnv()
  const [cmd, ...reste] = process.argv.slice(2)
  const o = options(reste)
  if (cmd === 'cles') {
    if (process.env.LICENCE_CLE_PRIVEE && !o.forcer) throw new Error('Une clé privée existe déjà dans .env. Refaire les clés invaliderait TOUTES les licences vendues. (--forcer pour passer outre.)')
    const paire = await crypto.subtle.generateKey({ name: 'Ed25519' }, true, ['sign', 'verify'])
    const pub = b64(await crypto.subtle.exportKey('raw', paire.publicKey)).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '')
    const priv = b64(await crypto.subtle.exportKey('pkcs8', paire.privateKey))
    await writeFile(FICHIER_PUBLIC, JSON.stringify({ publique: pub, creee: new Date().toISOString().slice(0, 10) }, null, 2) + '\n')
    await appendFile(ENV, `\n# Clé privée de signature des licences YEBA Studio — NE JAMAIS PARTAGER\nLICENCE_CLE_PRIVEE=${priv}\n`, { mode: 0o600 })
    console.log('Clés créées. Publique → site/espace/src/licence-cle.json ; privée → .env (LICENCE_CLE_PRIVEE).')
    console.log('Reconstruisez le logiciel (npm run build) pour qu’il connaisse la nouvelle clé publique.')
  } else if (cmd === 'emettre') {
    const charge = chargeLicence({ offre: o.offre, poste: o.poste, nom: o.nom, email: o.email, organisme: o.organisme, debut: o.debut || new Date(), jours: o.jours != null ? Number(o.jours) : undefined })
    const code = await signer(charge, await chargerClePrivee())
    console.log(JSON.stringify(charge, null, 2))
    console.log('\nLicence à transmettre au client :\n\n' + code + '\n')
  } else if (cmd === 'verifier') {
    const r = await verifier(reste[0], reste[1])
    console.log(r.ok ? `VALIDE — ${r.charge.off} pour ${r.charge.nom} (${r.charge.org})${r.charge.fin ? ' jusqu’au ' + r.charge.fin : ', perpétuelle'}` : `REFUSÉE — ${r.raison}`)
  } else {
    console.log('Commandes : cles | emettre | verifier (voir l’en-tête du fichier).')
  }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  principal().catch((e) => {
    console.error('Erreur :', e.message)
    process.exit(1)
  })
}
