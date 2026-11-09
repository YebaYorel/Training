// Contrôle du dossier dist/ avant de le déposer chez l'hébergeur.
//   npm run verifier     → rapport (n'empêche rien)
//   npm run publier      → construit le site PUIS refuse de terminer si un point bloquant subsiste
//
// Bloquant : champ légal non rempli, contenu payant (Pack Qualiopi, livrets) publié, secret, fichier
// technique exposé (cartes de code source, fichiers .env…), ancienne adresse de contact.
import { readdirSync, readFileSync, statSync } from 'node:fs'
import { dirname, extname, relative, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const ICI = dirname(fileURLToPath(import.meta.url))
const DIST = resolve(ICI, '../../dist')
const strict = process.argv.includes('--strict')

function fichiers(dossier) {
  return readdirSync(dossier).flatMap((n) => {
    const p = resolve(dossier, n)
    return statSync(p).isDirectory() ? fichiers(p) : [p]
  })
}

const TEXTE = new Set(['.html', '.js', '.css', '.json', '.txt', '.xml', '.svg', '.webmanifest'])
// Phrases tirées du texte complet des modèles du Pack Qualiopi : leur présence = fuite du contenu vendu.
const EXTRAITS_PAYANTS = [
  'Vous signez la feuille d’émargement à chaque demi-journée',
  'Ce livret rassemble tout ce qu’il faut savoir avant et pendant votre formation',
  'Accusé de réception sous 48 heures ouvrées, réponse motivée',
]
const REGLES = [
  { nom: 'Champ légal à compléter', re: /class="a-completer"|\[À (COMPLÉTER|RELEVER|DOCUMENTER|VALIDER)/, ext: ['.html'] },
  { nom: 'Ancienne adresse de contact', re: /yebaformations@gmail\.com/ },
  { nom: 'Secret ou jeton', re: /AIRTABLE_TOKEN\s*=|LICENCE_CLE_PRIVEE\s*=|\bpat[A-Za-z0-9]{14}\.[A-Za-z0-9]{40,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|sk_live_[A-Za-z0-9]{10,}/ },
  { nom: 'Contenu payant du Pack Qualiopi', re: new RegExp(EXTRAITS_PAYANTS.map((e) => e.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|')) },
]
const INTERDITS = [
  { nom: 'Carte de code source (.map)', re: /\.map$/ },
  { nom: 'Fichier de configuration ou secret', re: /(^|\/)\.env|\.(md|log|bak|sql|py|mjs)$/ },
  { nom: 'Livret d’accueil (réservé aux inscrits)', re: /livret/i },
]

const problemes = []
for (const f of fichiers(DIST)) {
  const rel = relative(DIST, f)
  for (const i of INTERDITS) if (i.re.test(rel)) problemes.push(`${i.nom} : ${rel}`)
  if (!TEXTE.has(extname(f))) continue
  const contenu = readFileSync(f, 'utf8')
  for (const r of REGLES) {
    if (r.ext && !r.ext.includes(extname(f))) continue
    const n = (contenu.match(new RegExp(r.re.source, 'g')) || []).length
    if (n) problemes.push(`${r.nom} : ${rel} (${n})`)
  }
}

if (!problemes.length) {
  console.log('✅ Contrôle avant publication : rien à signaler, dist/ peut être déposé chez l’hébergeur.')
} else {
  console.log(`${strict ? '❌' : '⚠️ '} Contrôle avant publication : ${problemes.length} point(s) à régler avant la mise en ligne :`)
  for (const p of problemes) console.log('   - ' + p)
  if (strict) process.exit(1)
}
