// Étape finale de `npm run build` :
//  1. insère dans dist/index.html le HTML complet de la page (pré-rendu React) : moteurs de recherche,
//     IA et réseaux sociaux lisent le contenu sans exécuter JavaScript, et le texte s'affiche tout de suite ;
//  2. ajoute les données structurées schema.org (organisme de formation + formations) ;
//  3. écrit robots.txt, sitemap.xml et llms.txt à partir du catalogue réel.
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const ICI = dirname(fileURLToPath(import.meta.url))
const RACINE = resolve(ICI, '../..')
const DIST = resolve(RACINE, 'dist')
const SSR = resolve(RACINE, 'dist-ssr')
const SITE = 'https://www.yebaformations.re'

const { render, ENTREPRISE, FORMATIONS, slugFormation } = await import(pathToFileURL(resolve(SSR, 'entry-server.js')).href)
const { pageFormation } = await import(pathToFileURL(resolve(ICI, 'pages-formations.mjs')).href)
const CATALOGUE = JSON.parse(readFileSync(resolve(ICI, '../src/catalogue.json'), 'utf8'))
const PROGRAMMES = JSON.parse(readFileSync(resolve(ICI, '../public/documents/index.json'), 'utf8'))

/** JSON sûr dans une balise <script> : aucun « </script> » ni « <!-- » ne peut s'y glisser. */
const jsonSur = (o) => JSON.stringify(o).replace(/</g, '\\u003c').replace(/>/g, '\\u003e').replace(/&/g, '\\u0026')
const echapper = (t) => String(t).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c])
const titreCourt = (t) => t.split(' : ')[0].trim()
const sousTitre = (t) => (t.includes(' : ') ? t.split(' : ').slice(1).join(' : ').trim() : '')

// ---------- 1. Données structurées ----------
const organisme = {
  '@type': ['EducationalOrganization', 'LocalBusiness'],
  '@id': `${SITE}/#organisme`,
  name: ENTREPRISE.nom,
  url: `${SITE}/`,
  logo: `${SITE}/media/logo-yeba.png`,
  image: `${SITE}/media/hero-poster.jpg`,
  description:
    "Organisme de formation certifié Qualiopi à La Réunion : formations à l'IA générative, à l'automatisation, à la vente et au management ; mise en place de solutions d'IA ; conseil RGPD et IA Act pour les TPE-PME.",
  email: ENTREPRISE.email,
  telephone: ENTREPRISE.telLien.replace('tel:', ''),
  founder: { '@type': 'Person', name: ENTREPRISE.dirigeant },
  address: {
    '@type': 'PostalAddress',
    streetAddress: '9 rue Françoise Châtelain',
    postalCode: '97490',
    addressLocality: 'Sainte-Clotilde',
    addressRegion: 'La Réunion',
    addressCountry: 'FR',
  },
  areaServed: { '@type': 'AdministrativeArea', name: 'La Réunion' },
  identifier: [
    { '@type': 'PropertyValue', propertyID: 'SIRET', value: ENTREPRISE.siret.replace(/\s/g, '') },
    { '@type': 'PropertyValue', propertyID: "Numéro de déclaration d'activité", value: ENTREPRISE.nda },
  ],
  hasCredential: {
    '@type': 'EducationalOccupationalCredential',
    name: 'Certification Qualiopi — catégorie actions de formation',
    identifier: ENTREPRISE.qualiopi,
    recognizedBy: { '@type': 'Organization', name: ENTREPRISE.certificateur },
  },
  knowsLanguage: 'fr',
}

const formations = CATALOGUE.formations.map((f) => {
  const prog = PROGRAMMES.find((p) => p.ref === f.ref)
  const heures = Number(f.heures) || null
  const cours = {
    '@type': 'Course',
    '@id': `${SITE}/#${f.ref}`,
    courseCode: f.ref,
    name: titreCourt(f.titre),
    description: sousTitre(f.titre) || titreCourt(f.titre),
    inLanguage: 'fr',
    provider: { '@id': `${SITE}/#organisme` },
    ...(f.prerequis ? { coursePrerequisites: f.prerequis.slice(0, 300) } : {}),
    ...(f.public ? { audience: { '@type': 'Audience', audienceType: f.public.slice(0, 200) } } : {}),
    url: `${SITE}/${slugFormation(f)}`,
    hasCourseInstance: {
      '@type': 'CourseInstance',
      courseMode: 'Onsite',
      location: { '@type': 'Place', name: 'La Réunion' },
      ...(heures ? { courseWorkload: `PT${heures}H` } : {}),
    },
  }
  const prix = f.tarifs?.interTotal
  if (prix) {
    cours.offers = { '@type': 'Offer', category: 'Paid', price: prix, priceCurrency: 'EUR', availability: 'https://schema.org/InStock' }
  }
  return cours
})

const donnees = {
  '@context': 'https://schema.org',
  '@graph': [
    organisme,
    { '@type': 'WebSite', '@id': `${SITE}/#site`, url: `${SITE}/`, name: ENTREPRISE.nom, inLanguage: 'fr', publisher: { '@id': `${SITE}/#organisme` } },
    ...formations,
  ],
}

// ---------- 2. Pré-rendu ----------
let html = readFileSync(resolve(DIST, 'index.html'), 'utf8')
if (!html.includes('<div id="racine"></div>')) throw new Error('index.html : <div id="racine"></div> introuvable')
const contenu = render()
html = html
  .replace('<div id="racine"></div>', `<div id="racine">${contenu}</div>`)
  .replace('<!--donnees-structurees-->', `<script type="application/ld+json">${jsonSur(donnees)}</script>`)
writeFileSync(resolve(DIST, 'index.html'), html)

// ---------- 2 bis. Une page par formation ----------
const css = (readFileSync(resolve(DIST, 'mentions-legales.html'), 'utf8').match(/href="\.?\/?(assets\/legal-[^"]+\.css)"/) || [])[1]
if (!css) throw new Error('Feuille de style des pages légales introuvable dans dist/mentions-legales.html')
mkdirSync(resolve(DIST, 'formations'), { recursive: true })
const pagesFormations = FORMATIONS.map((f) => ({ f, slug: slugFormation(f) }))
for (const { f, slug } of pagesFormations) {
  const fiche = CATALOGUE.formations.find((x) => x.ref === f.ref) || {}
  const autres = pagesFormations.filter((p) => p.f.ref !== f.ref).map((p) => ({ nom: p.f.nom, slug: p.slug }))
  const programmePdf = PROGRAMMES.find((p) => p.ref === f.ref)?.programme
  writeFileSync(resolve(DIST, slug), pageFormation({ f, fiche, slug, css, site: SITE, entreprise: ENTREPRISE, autres, programmePdf }))
}

// ---------- 3. Fichiers pour les robots ----------
const aujourdhui = new Date().toISOString().slice(0, 10)
const pages = ['', 'mentions-legales.html', 'confidentialite.html', 'cgv-logiciels.html']
const urls = [
  ...pages.map((p) => ({ loc: `${SITE}/${p}`, prio: p ? '0.3' : '1.0' })),
  ...pagesFormations.map((p) => ({ loc: `${SITE}/${p.slug}`, prio: '0.8' })),
  ...PROGRAMMES.map((p) => ({ loc: `${SITE}/${p.programme}`, prio: '0.6' })),
]
writeFileSync(
  resolve(DIST, 'sitemap.xml'),
  `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls
    .map((u) => `  <url><loc>${echapper(encodeURI(u.loc))}</loc><lastmod>${aujourdhui}</lastmod><priority>${u.prio}</priority></url>`)
    .join('\n')}\n</urlset>\n`,
)

writeFileSync(
  resolve(DIST, 'robots.txt'),
  `# YEBA FORMATIONS — ${SITE}
User-agent: *
Allow: /
Disallow: /studio/

Sitemap: ${SITE}/sitemap.xml
`,
)

const lignesFormations = CATALOGUE.formations
  .map((f) => {
    const prog = PROGRAMMES.find((p) => p.ref === f.ref)
    const duree = f.heures ? ` — ${f.jours} j, ${f.heures} h` : ''
    const lien = `${SITE}/${slugFormation(f)}`
    return `- [${titreCourt(f.titre)}](${lien}): ${sousTitre(f.titre)}${duree}`
  })
  .join('\n')

writeFileSync(
  resolve(DIST, 'llms.txt'),
  `# ${ENTREPRISE.nom}

> Organisme de formation professionnelle à La Réunion (974), certifié Qualiopi (n° ${ENTREPRISE.qualiopi}, catégorie actions de formation). Formations à l'intelligence artificielle générative, à l'automatisation, à la vente et au management ; mise en place de solutions d'IA ; conseil RGPD et IA Act pour les TPE-PME. Formations finançables par les OPCO.

- Dirigeant et formateur : ${ENTREPRISE.dirigeant}
- Adresse : ${ENTREPRISE.adresse}
- Contact : ${ENTREPRISE.email} — ${ENTREPRISE.telAffiche}
- Numéro de déclaration d'activité : ${ENTREPRISE.nda} (cet enregistrement ne vaut pas agrément de l'État)
- SIRET : ${ENTREPRISE.siret}

## Formations (une page détaillée par formation)

${lignesFormations}

## Informations légales

- [Mentions légales](${SITE}/mentions-legales.html)
- [Politique de confidentialité](${SITE}/confidentialite.html)
`,
)

if (existsSync(SSR)) rmSync(SSR, { recursive: true, force: true })
console.log(`Pré-rendu : ${Math.round(contenu.length / 1024)} Ko de HTML, ${pagesFormations.length} pages formation, ${formations.length} formations en données structurées, robots.txt, sitemap.xml (${urls.length} URL), llms.txt.`)
