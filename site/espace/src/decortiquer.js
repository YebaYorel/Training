// Décortiquer — lit un dossier complet (REAC, fiche RNCP, référentiel, syllabus, programme…)
// et en tire un plan de formation : Programme → Préparation / AT n → Séquences → Parties → Révision.
// Tout se passe dans le navigateur (ou Node pour les tests) : aucun fichier n'est envoyé nulle part (RGPD).
// Sans document, le plan est un squelette bâti uniquement sur le SUJET donné, signalé « à valider ».
import JSZip from 'jszip'

export const LIMITE_FICHIER = 250 * 1024 * 1024 // au-delà : ignoré, signalé
export const LIMITE_TEXTE = 6_000_000 // caractères conservés par document
const IGNORES = /(^|\/)(\.git|node_modules|__MACOSX|\.DS_Store|Thumbs\.db|~\$[^/]*)(\/|$)/i

const sansAccent = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '')
const norm = (s) => sansAccent(s || '').toLowerCase()
const nettoyer = (t) => t.replace(/\r/g, '\n').replace(/[ \t ]+/g, ' ').replace(/\n{3,}/g, '\n\n').trim()
const decoderXml = (s) => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&amp;/g, '&')

/* ---------- Lecture des fichiers ---------- */

function xmlVersTexte(xml, saut) {
  return decoderXml(xml.replace(new RegExp(`</(${saut})>`, 'g'), '\n').replace(/<w:tab\/>/g, ' ').replace(/<[^>]+>/g, ''))
}

async function pdfVersTexte(octets) {
  const pdfjs = await import('pdfjs-dist/legacy/build/pdf.mjs')
  // Lecteur dans le fil principal : fonctionne partout (y compris fichier unique hors ligne), sans fichier de worker à servir
  globalThis.pdfjsWorker ||= await import('pdfjs-dist/legacy/build/pdf.worker.mjs')
  const doc = await pdfjs.getDocument({ data: new Uint8Array(octets), useSystemFonts: true, isEvalSupported: false, verbosity: 0 }).promise
  const pages = []
  for (let i = 1; i <= doc.numPages; i++) {
    const page = await doc.getPage(i)
    const contenu = await page.getTextContent()
    let ligne = ''
    for (const it of contenu.items) {
      ligne += it.str
      ligne += it.hasEOL ? '\n' : ' '
    }
    pages.push(ligne)
    if (pages.join('').length > LIMITE_TEXTE) break
  }
  return pages.join('\n')
}

/** Lit un fichier (File ou {name, arrayBuffer()}) → { chemin, nom, ext, texte, erreur? } */
export async function lireFichier(f) {
  const chemin = f.webkitRelativePath || f._chemin || f.name
  const nom = f.name
  const ext = (nom.split('.').pop() || '').toLowerCase()
  const base = { chemin, nom, ext, taille: f.size }
  if (IGNORES.test(chemin)) return { ...base, ignore: 'fichier système' }
  if (f.size > LIMITE_FICHIER) return { ...base, ignore: 'fichier trop volumineux (> 250 Mo)' }
  try {
    let texte = ''
    if (['txt', 'md', 'csv', 'tsv', 'json', 'xml', 'yml', 'yaml', 'log'].includes(ext)) texte = await f.text()
    else if (['html', 'htm'].includes(ext)) texte = decoderXml((await f.text()).replace(/<(script|style)[\s\S]*?<\/\1>/gi, '').replace(/<\/(p|div|li|tr|h\d|br)>/gi, '\n').replace(/<[^>]+>/g, ' '))
    else if (ext === 'rtf') texte = (await f.text()).replace(/\\par[d]?/g, '\n').replace(/\\'[0-9a-f]{2}/gi, '').replace(/\\[a-z]+-?\d* ?/gi, '').replace(/[{}]/g, '')
    else if (ext === 'pdf') texte = await pdfVersTexte(await f.arrayBuffer())
    else if (['docx', 'docm', 'odt', 'ods', 'odp', 'pptx', 'xlsx'].includes(ext)) {
      const zip = await JSZip.loadAsync(await f.arrayBuffer())
      const lire = async (p) => (await zip.file(p)?.async('string')) || ''
      if (ext === 'docx' || ext === 'docm') texte = xmlVersTexte(await lire('word/document.xml'), 'w:p')
      else if (ext.startsWith('od')) texte = xmlVersTexte(await lire('content.xml'), 'text:p|text:h|table:table-row')
      else if (ext === 'pptx') {
        const diapos = Object.keys(zip.files).filter((n) => /^ppt\/slides\/slide\d+\.xml$/.test(n)).sort((a, b) => parseInt(a.match(/\d+/)[0]) - parseInt(b.match(/\d+/)[0]))
        for (const n of diapos) texte += xmlVersTexte(await lire(n), 'a:p') + '\n'
      } else {
        const partages = [...(await lire('xl/sharedStrings.xml')).matchAll(/<si>([\s\S]*?)<\/si>/g)].map((m) => xmlVersTexte(m[1], 'x'))
        for (const n of Object.keys(zip.files).filter((x) => /^xl\/worksheets\/sheet\d+\.xml$/.test(x))) {
          const xml = await lire(n)
          for (const ligne of xml.match(/<row[\s\S]*?<\/row>/g) || []) {
            const cellules = [...ligne.matchAll(/<c ([^>]*?)(?:\/>|>([\s\S]*?)<\/c>)/g)].map((c) => {
              const v = c[2]?.match(/<v>([\s\S]*?)<\/v>/)?.[1] ?? c[2]?.match(/<t[^>]*>([\s\S]*?)<\/t>/)?.[1] ?? ''
              return /t="s"/.test(c[1]) ? partages[Number(v)] ?? '' : decoderXml(v)
            })
            texte += cellules.filter(Boolean).join(' | ') + '\n'
          }
        }
      }
    } else return { ...base, ignore: `format .${ext || '?'} non pris en charge (utilisez PDF, Word, Excel, PowerPoint, texte ou HTML)` }
    texte = nettoyer(texte).slice(0, LIMITE_TEXTE)
    if (!texte) return { ...base, ignore: ext === 'pdf' ? 'aucun texte (PDF scanné : à passer en OCR avant)' : 'fichier vide' }
    return { ...base, texte }
  } catch (e) {
    return { ...base, ignore: 'illisible : ' + (e?.message || e) }
  }
}

/** Lit tous les fichiers, quatre à la fois, avec progression. */
export async function lireTout(fichiers, surProgres = () => {}) {
  const sortie = new Array(fichiers.length)
  let suivant = 0
  let faits = 0
  async function travailleur() {
    while (suivant < fichiers.length) {
      const i = suivant++
      sortie[i] = await lireFichier(fichiers[i])
      surProgres(++faits, fichiers.length, sortie[i])
    }
  }
  await Promise.all(Array.from({ length: Math.min(4, fichiers.length) }, travailleur))
  return sortie
}

/** Fichiers d'un glisser-déposer, dossiers compris (récursif). */
export async function fichiersDepuisDepot(dataTransfer) {
  const sortie = []
  const lireEntree = (e, chemin = '') =>
    new Promise((ok) => {
      if (e.isFile) e.file((f) => (Object.defineProperty(f, '_chemin', { value: chemin + f.name }), sortie.push(f), ok()), ok)
      else {
        const lecteur = e.createReader()
        const tout = []
        const lot = () =>
          lecteur.readEntries(async (liste) => {
            if (!liste.length) {
              for (const x of tout) await lireEntree(x, chemin + e.name + '/')
              ok()
            } else (tout.push(...liste), lot())
          }, ok)
        lot()
      }
    })
  const entrees = [...dataTransfer.items].map((i) => i.webkitGetAsEntry?.()).filter(Boolean)
  if (!entrees.length) return [...dataTransfer.files]
  for (const e of entrees) await lireEntree(e)
  return sortie
}

/* ---------- Reconnaissance du type de document ---------- */

export function typeDocument(texte, nom = '') {
  const t = norm(texte.slice(0, 200000) + ' ' + nom)
  const n = (re) => (t.match(re) || []).length
  const score = {
    REAC: n(/referentiel d.emploi|\breac\b|activites? types?|referentiel emploi activites competences/g) * 2 + n(/activite[- ]type/g),
    'Fiche RNCP': n(/\brncp\s?\d{3,6}|france competences|blocs? de competences|code nsf|niveau de qualification/g) * 2,
    'Référentiel de certification': n(/referentiel de certification|\bccp\b|modalites d.evaluation|criteres d.evaluation|epreuve/g) * 1.5,
    'Syllabus / programme': n(/syllabus|objectifs? pedagogiques?|prerequis|programme de formation|seance|modalites pedagogiques|deroule/g) * 1.5,
  }
  const [type, valeur] = Object.entries(score).sort((a, b) => b[1] - a[1])[0]
  return valeur >= 3 ? type : 'Autre document'
}

/* ---------- Extraction de la structure ---------- */

const VERBE = /^(?:[-•▪●◦■□✓✔►>*·]|\d+(?:\.\d+)*[.)]?|[a-z][.)])\s+/i
const RE_AT = /^\s*(?:activit[ée]s?[- ]types?|AT)\s*(?:n[°o.]?\s*)?(\d{1,2})\s*[:\-–—.)]*\s*(.*)$/i
const RE_BLOC = /^\s*(?:CCP|BC|bloc(?:\s+de\s+comp[ée]tences?)?|certificat\s+de\s+comp[ée]tences?\s+professionnelles?)\s*(?:n[°o.]?\s*)?(\d{1,2})\s*[:\-–—.)]*\s*(.*)$/i
const RE_RUBRIQUE_COMP = /^\s*comp[ée]tences?\s+(professionnelles?|transversales?|techniques?|cl[ée]s?)\b/i
const RE_FIN_RUBRIQUE = /^\s*(?:crit[èe]res?|modalit[ée]s?|conditions?|dur[ée]e|pr[ée]requis|public|contexte|situation|[ée]preuve|objectifs?|r[ée]sultat)/i

const court = (titre, max = 30) => {
  let t = (titre || '').replace(/\s+/g, ' ').replace(/[:;.,\s]+$/, '').trim()
  if (t.length <= max) return t
  const coupe = t.slice(0, max)
  return coupe.slice(0, Math.max(coupe.lastIndexOf(' '), 12)).trim() + '…'
}

export function extraire(documents) {
  const docs = documents.filter((d) => d.texte)
  const res = { programme: '', rncp: '', niveau: '', activites: [], blocs: [], evaluation: [], duree: '', sources: [], libre: [] }
  for (const d of docs) {
    const type = typeDocument(d.texte, d.nom)
    res.sources.push({ chemin: d.chemin, type })
    const lignes = d.texte.split('\n').map((l) => l.trim()).filter(Boolean)
    const joint = d.texte.slice(0, 60000)
    res.rncp ||= joint.match(/RNCP\s?(\d{3,6})/i)?.[1] || ''
    res.niveau ||= joint.match(/niveau\s*(?:de qualification\s*)?:?\s*(\d)\b/i)?.[1] || joint.match(/niveau\s+(\d)\s*\(/i)?.[1] || ''
    res.duree ||= joint.match(/dur[ée]e[^\n]{0,40}?(\d{1,4})\s*(heures?|h\b|jours?)/i)?.slice(1, 3).join(' ') || ''
    if (!res.programme) {
      const t = joint.match(/(?:intitul[ée](?:\s+de la (?:certification|formation))?|titre professionnel|certification)\s*:?\s*([^\n]{6,120})/i)
      if (t) res.programme = t[1].replace(/^[:\s«"]+|[»"\s]+$/g, '')
    }
    let courant = null // { kind: 'at'|'bloc', ref }
    let enComp = false
    for (const l of lignes) {
      let m
      if ((m = l.match(RE_AT)) && m[2] && m[2].length >= 4 && l.length < 220) {
        const num = Number(m[1])
        courant = res.activites.find((a) => a.num === num) || (res.activites.push({ num, titre: m[2].trim(), competences: [] }), res.activites.at(-1))
        enComp = false
        continue
      }
      if ((m = l.match(RE_BLOC)) && m[2] && m[2].length >= 4 && l.length < 220) {
        const num = Number(m[1])
        const bloc = res.blocs.find((b) => b.num === num) || (res.blocs.push({ num, titre: m[2].trim(), competences: [] }), res.blocs.at(-1))
        courant = bloc
        enComp = false
        continue
      }
      if (RE_RUBRIQUE_COMP.test(l)) {
        enComp = true
        continue
      }
      if (RE_FIN_RUBRIQUE.test(l) && !VERBE.test(l)) {
        if (/crit[èe]res?|[ée]preuve|modalit[ée]s?\s+d.[ée]valuation/i.test(l)) res.evaluation.push(l.slice(0, 200))
        enComp = false
        continue
      }
      if (courant && (enComp || VERBE.test(l)) && l.length >= 12 && l.length <= 220) {
        const texte = l.replace(VERBE, '').trim()
        if (texte && !courant.competences.includes(texte)) courant.competences.push(texte)
      } else if (!courant && VERBE.test(l) && l.length >= 12 && l.length <= 160) res.libre.push(l.replace(VERBE, '').trim())
    }
    // Titres libres : numérotés « 1. », « Partie », « Module », « Séance »
    for (const l of lignes) {
      const m = l.match(/^(?:(?:module|partie|chapitre|s[ée]ance|s[ée]quence|unit[ée])\s*\d+\s*[:\-–—.)]*\s*|(\d{1,2})[.)]\s+)([A-ZÀ-Ý][^\n]{5,110})$/i)
      if (m && l.length < 130 && !/\d{4,}/.test(l)) res.libre.push((m[2] || l).trim())
    }
  }
  res.libre = [...new Set(res.libre)].slice(0, 60)
  res.activites.sort((a, b) => a.num - b.num)
  res.blocs.sort((a, b) => a.num - b.num)
  return res
}

/* ---------- Plan de formation ---------- */

export const PARTIES = ['Partie I — Notions et repères', 'Partie II — Mise en pratique', 'Partie III — Évaluation et bilan']
const STOP = new Set('de la le les des du un une et en au aux pour par sur dans avec son sa ses leur leurs ou à l d qui que'.split(' '))
const mots = (s) => norm(s).split(/[^a-z0-9]+/).filter((m) => m.length > 3 && !STOP.has(m))
const pertinence = (texte, sujet) => {
  const cible = new Set(mots(sujet))
  return cible.size ? mots(texte).filter((m) => cible.has(m)).length : 0
}

/**
 * Construit le plan.
 *  - extraction : résultat de extraire() (peut être vide) ;
 *  - sujet : texte libre donné par Aurélien (prioritaire pour cibler et pour nommer) ;
 *  - options : { seqParAt, restreindre } (restreindre = ne garder que ce qui touche le sujet s'il y a des correspondances).
 */
export function construirePlan(extraction, sujet = '', { seqParAt = 3, restreindre = false, nomProgramme = '' } = {}) {
  const sujetNet = sujet.trim()
  let unites = extraction.activites.length ? extraction.activites : extraction.blocs
  const rubrique = extraction.activites.length ? 'AT' : extraction.blocs.length ? 'Bloc' : ''
  let origine = rubrique ? `Documents (${rubrique === 'AT' ? 'activités types' : 'blocs de compétences'})` : ''
  if (restreindre && sujetNet && unites.length) {
    const garde = unites.filter((u) => pertinence(u.titre + ' ' + u.competences.join(' '), sujetNet) > 0)
    if (garde.length) unites = garde
  }
  if (!unites.length && extraction.libre.length >= 3) {
    const lot = Math.ceil(extraction.libre.length / 3)
    unites = [0, 1, 2].map((i) => ({ num: i + 1, titre: `Partie ${i + 1} du document`, competences: extraction.libre.slice(i * lot, (i + 1) * lot) })).filter((u) => u.competences.length)
    origine = 'Titres repérés dans les documents'
  }
  if (!unites.length) {
    const s = sujetNet || 'le sujet'
    unites = [
      { num: 1, titre: `Comprendre ${s}`, competences: [`Situer ${s} et ses enjeux`, `Maîtriser le vocabulaire de ${s}`, `Identifier les acteurs et les règles de ${s}`] },
      { num: 2, titre: `Pratiquer ${s}`, competences: [`Appliquer les méthodes de ${s} sur des cas réels`, `Utiliser les outils de ${s}`, `Analyser une situation de ${s}`] },
      { num: 3, titre: `Évaluer et progresser en ${s}`, competences: [`Mesurer ses résultats en ${s}`, `Corriger ses erreurs`, `Construire un plan d'amélioration`] },
    ]
    origine = 'Squelette bâti sur le sujet seul — à valider par le formateur'
  }
  const programme = nomProgramme || extraction.programme || (sujetNet ? court(sujetNet, 40) : '') || 'Formation'
  const noeuds = [{ nom: 'Préparation du TP', type: 'preparation' }]
  for (const [i, u] of unites.entries()) {
    const comps = u.competences.length ? u.competences : [u.titre]
    // On répartit les compétences sur au plus `seqParAt` séquences
    const n = Math.max(1, Math.min(seqParAt, comps.length))
    const taille = Math.ceil(comps.length / n)
    const sequences = Array.from({ length: n }, (_, k) => {
      const lot = comps.slice(k * taille, (k + 1) * taille)
      return { nom: `Sq ${k + 1} — ${court(lot[0], 34)}`, competences: lot, parties: PARTIES.map((p) => ({ nom: p })) }
    }).filter((s) => s.competences.length)
    noeuds.push({ nom: `${rubrique === 'Bloc' ? 'Bloc' : 'AT'} ${u.num ?? i + 1} — ${court(u.titre, 36)}`, type: 'at', titre: u.titre, sequences })
  }
  noeuds.push({ nom: 'Révision TP (type examen final)', type: 'revision' })
  return { programme, rncp: extraction.rncp, niveau: extraction.niveau, origine, evaluation: extraction.evaluation.slice(0, 8), noeuds, sujet: sujetNet }
}

/* ---------- Exports ---------- */

export const cleDate = (noeud, seq) => `${noeud.nom}|${seq.nom}`
export const fichierSur = (s) => s.replace(/[\\/:*?"<>|]/g, '-').replace(/\s+/g, ' ').trim()

/** Texte Markdown du plan (à coller dans Drive / Airtable). */
export function planMarkdown(plan, dates = {}) {
  const l = [`# ${plan.programme}`, '', `Source : ${plan.origine}${plan.rncp ? ` · RNCP${plan.rncp}` : ''}${plan.niveau ? ` · niveau ${plan.niveau}` : ''}`, '']
  for (const n of plan.noeuds) {
    l.push(`## ${n.nom}`)
    for (const s of n.sequences || []) {
      l.push(`### ${s.nom}${dates[cleDate(n, s)] ? ` — ${dates[cleDate(n, s)]}` : ''}`, ...s.competences.map((c) => `- ${c}`), '')
    }
  }
  if (plan.evaluation.length) l.push('## Modalités d’évaluation repérées', ...plan.evaluation.map((e) => `- ${e}`))
  return l.join('\n')
}

/** ZIP de l'arborescence à déposer dans Drive : un dossier par niveau, nom court + date. */
export async function arborescenceZip(plan, dates = {}) {
  const zip = new JSZip()
  const racine = fichierSur(plan.programme)
  const ajout = (chemin, contenu) => zip.file(`${racine}/${chemin}`, contenu)
  ajout('_PLAN.md', planMarkdown(plan, dates))
  for (const n of plan.noeuds) {
    const dossier = fichierSur(n.nom)
    if (!n.sequences) ajout(`${dossier}/_a-remplir.txt`, `Dossier « ${n.nom} ».\nÀ remplir par les documents de ce niveau.`)
    for (const s of n.sequences || []) {
      const sd = fichierSur(s.nom + (dates[cleDate(n, s)] ? ` — ${dates[cleDate(n, s)]}` : ''))
      for (const p of s.parties) ajout(`${dossier}/${sd}/${fichierSur(p.nom)}/_a-remplir.txt`, `${s.nom}\n${p.nom}\n\nCompétences visées :\n${s.competences.map((c) => '- ' + c).join('\n')}\n`)
    }
  }
  return zip.generateAsync({ type: 'blob' })
}
