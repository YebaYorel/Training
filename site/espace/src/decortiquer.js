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

export const TYPES = ['REAC', 'Référentiel d’évaluation (RE)', 'Référentiel de certification (RC)', 'Fiche RNCP', 'Fiche RS', 'Syllabus / programme', 'Autre document']

export function typeDocument(texte, nom = '') {
  const t = norm(texte.slice(0, 200000) + ' ' + nom)
  const n = (re) => (t.match(re) || []).length
  const score = {
    REAC: n(/referentiel d.emploi|\breac\b|referentiel emploi activites competences/g) * 3 + n(/activites? types?/g),
    'Référentiel d’évaluation (RE)': n(/referentiel d.evaluation|\brev\b|mise en situation professionnelle|entretien technique|questionnaire professionnel|entretien final|dossier professionnel|epreuve de synthese|evaluations? passees? en cours de formation|\becf\b/g) * 1.5,
    'Référentiel de certification (RC)': n(/referentiel de certification|\brc\b|criteres? d.evaluation|modalites d.evaluation/g) * 1.5,
    'Fiche RNCP': n(/\brncp\s?\d{3,6}|france competences|blocs? de competences|code nsf|niveau de qualification|nomenclature/g) * 2,
    'Fiche RS': n(/\brs\s?\d{3,6}\b|repertoire specifique|competences attestees/g) * 3,
    'Syllabus / programme': n(/syllabus|objectifs? pedagogiques?|prerequis|programme de formation|seance|modalites pedagogiques|deroule|plan de cours/g) * 1.5,
  }
  const [type, valeur] = Object.entries(score).sort((a, b) => b[1] - a[1])[0]
  return valeur >= 3 ? type : 'Autre document'
}

/* ---------- Extraction de la structure ---------- */

const VERBE = /^(?:[-•▪●◦■□✓✔►>*·]|\d+(?:\.\d+)*[.)]?|[a-z][.)])\s+/i
const RE_AT = /^\s*(?:activit[ée]s?[- ]types?|AT)\s*(?:n[°o.]?\s*)?(\d{1,2})\s*[:\-–—.)]*\s*(.*)$/i
const RE_BLOC = /^\s*(?:CCP|BC|bloc(?:\s+de\s+comp[ée]tences?)?|certificat\s+de\s+comp[ée]tences?\s+professionnelles?)\s*(?:n[°o.]?\s*)?(\d{1,2})\s*[:\-–—.)]*\s*(.*)$/i
const RE_BLOC_RNCP = /RNCP\s?\d{3,6}\s?BC\s?(\d{1,2})\s*[:\-–—.)]*\s*(.{4,200})$/i
const RE_RUBRIQUE_COMP = /^\s*comp[ée]tences?\s+(professionnelles?|transversales?|techniques?|cl[ée]s?|attest[ée]es?|vis[ée]es?)\b/i
const RE_FIN_RUBRIQUE = /^\s*(?:crit[èe]res?|modalit[ée]s?|conditions?|dur[ée]e|pr[ée]requis|public|contexte|situation|[ée]preuve|objectifs?|r[ée]sultat)/i

const court = (titre, max = 30) => {
  const t = (titre || '').replace(/\s+/g, ' ').replace(/[:;.,\s]+$/, '').trim()
  if (t.length <= max) return t
  const coupe = t.slice(0, max)
  return coupe.slice(0, Math.max(coupe.lastIndexOf(' '), 12)).trim() + '…'
}

/** Épreuves et modalités reconnues (sigles des référentiels d'évaluation compris). */
export const EPREUVES = [
  { cle: 'MSP', nom: 'Mise en situation professionnelle', re: /mise en situation professionnelle/i, sigle: 'MSP' },
  { cle: 'ET', nom: 'Entretien technique', re: /entretien technique/i, sigle: 'ET' },
  { cle: 'QP', nom: 'Questionnaire professionnel', re: /questionnaire professionnel/i, sigle: 'QP' },
  { cle: 'QPP', nom: 'Questionnaire à partir de productions', re: /questionnaire (?:à|a) partir de productions?/i, sigle: 'QPP' },
  { cle: 'EF', nom: 'Entretien final avec le jury', re: /entretien final/i, sigle: 'EF' },
  { cle: 'PRES', nom: 'Présentation d’un projet', re: /pr[ée]sentation d.un projet/i },
  { cle: 'SOUT', nom: 'Soutenance orale', re: /soutenance/i },
  { cle: 'ECRIT', nom: 'Épreuve écrite', re: /[ée]preuve [ée]crite|examen [ée]crit/i },
  { cle: 'CAS', nom: 'Étude de cas', re: /[ée]tude de cas/i },
  { cle: 'QCM', nom: 'QCM', re: /\bQCM\b|questionnaire [àa] choix multiples?/i },
  { cle: 'MS', nom: 'Mise en situation', re: /mise en situation(?! professionnelle)|cas pratique/i },
  { cle: 'ECF', nom: 'Évaluations passées en cours de formation (ECF)', re: /[ée]valuations? pass[ée]es? en cours de formation/i, sigle: 'ECF' },
]
/** Dossiers que l'apprenant doit préparer. */
export const DOSSIERS = [
  { nom: 'Dossier professionnel (DP)', re: /dossier professionnel/i, sigle: 'DP' },
  { nom: 'Dossier de synthèse de pratique professionnelle (DSPP)', re: /dossier de synth[èe]se/i, sigle: 'DSPP' },
  { nom: 'Dossier de projet', re: /dossier de projet/i },
  { nom: 'Rapport / mémoire professionnel', re: /rapport (?:d.activit[ée]|professionnel|de stage)|m[ée]moire professionnel/i },
  { nom: 'Portfolio / portefeuille de preuves', re: /portfolio|portefeuille de (?:preuves|comp[ée]tences)/i },
  { nom: 'Livret d’évaluation (ECF)', re: /livret d.[ée]valuation/i },
]

/** Un sigle (ET, DP…) ne compte que s'il est isolé et que la ligne n'est pas un titre tout en majuscules. */
function sigleDans(l, sigle) {
  const lettres = l.replace(/[^A-Za-zÀ-ÿ]/g, '')
  const majuscules = lettres.replace(/[^A-ZÀ-Ý]/g, '').length
  if (lettres.length > 12 && majuscules / lettres.length > 0.6) return false
  return new RegExp(`(?:^|[\\s(,;/+])${sigle}(?=$|[\\s),;/+:.])`).test(l)
}
export const correspond = (e, l) => e.re.test(l) || (!!e.sigle && sigleDans(l, e.sigle))
/** Position de l'épreuve dans la ligne (pour lire SA durée, juste après son nom). */
function positionDe(e, l) {
  const m = l.match(e.re)
  if (m) return m.index
  const s = e.sigle && l.match(new RegExp(`(?:^|[\\s(,;/+])${e.sigle}(?=$|[\\s),;/+:.])`))
  return s ? s.index : 0
}

const RE_DUREE = /(\d{1,2})\s*h(?:eures?)?\s*(\d{2})?(?!\w)|(\d{1,3})\s*min(?:utes?)?/i
const enHeures = (m) => (m ? (m[3] ? Number(m[3]) / 60 : Number(m[1]) + (m[2] ? Number(m[2]) / 60 : 0)) : 0)

export function extraire(documents) {
  const docs = documents.filter((d) => d.texte)
  const res = { programme: '', rncp: '', rs: '', niveau: '', activites: [], blocs: [], evaluation: [], duree: '', dureeTotaleH: 0, sources: [], libre: [], epreuves: [], dossiers: [], seances: [], lignesEval: [], types: new Set() }
  for (const d of docs) {
    const type = typeDocument(d.texte, d.nom)
    res.types.add(type)
    res.sources.push({ chemin: d.chemin, type })
    const lignes = d.texte.split('\n').map((l) => l.trim()).filter(Boolean)
    const joint = d.texte.slice(0, 80000)
    const docEval = /RE\)|RC\)|RNCP|RS|REAC/.test(type)
    res.rncp ||= joint.match(/RNCP\s?(\d{3,6})/i)?.[1] || ''
    res.rs ||= joint.match(/\bRS\s?(\d{3,6})\b/)?.[1] || ''
    res.niveau ||= joint.match(/niveau\s*(?:de qualification\s*)?:?\s*(\d)\b/i)?.[1] || joint.match(/niveau\s+(\d)\s*\(/i)?.[1] || ''
    res.duree ||= joint.match(/dur[ée]e[^\n]{0,40}?(\d{1,4})\s*(heures?|h\b|jours?)/i)?.slice(1, 3).join(' ') || ''
    if (!res.dureeTotaleH) {
      const m = joint.match(/dur[ée]e\s+(?:totale|globale|de (?:la )?formation|en centre|du parcours)[^\n\d]{0,40}(\d{1,4})\s*(heures|h\b|jours?)/i)
      if (m) res.dureeTotaleH = /jour/i.test(m[2]) ? Number(m[1]) * 7 : Number(m[1])
    }
    if (!res.programme) {
      const t = joint.match(/(?:intitul[ée](?:\s+de la (?:certification|formation))?|titre professionnel|certification)\s*:?\s*([^\n]{6,120})/i)
      if (t) res.programme = t[1].replace(/^[:\s«"]+|[»"\s]+$/g, '')
    }
    let courant = null
    let enComp = false
    for (const [k, l] of lignes.entries()) {
      let m
      // Épreuves, dossiers, lignes d'évaluation (tous types de documents)
      for (const e of EPREUVES) {
        if (correspond(e, l) && l.length < 260) {
          const duree = enHeures(l.slice(positionDe(e, l), positionDe(e, l) + 45).match(RE_DUREE))
          const ex = res.epreuves.find((x) => x.cle === e.cle)
          if (!ex) res.epreuves.push({ cle: e.cle, nom: e.nom, heures: duree, detail: l.slice(0, 200) })
          else if (!ex.heures && duree) ex.heures = duree
        }
      }
      for (const dos of DOSSIERS) if (correspond(dos, l) && !res.dossiers.includes(dos.nom)) res.dossiers.push(dos.nom)
      if (docEval && EPREUVES.some((e) => correspond(e, l))) res.lignesEval.push([lignes[k - 1] || '', l, lignes[k + 1] || ''].join(' '))
      // Séances d'un syllabus avec leur durée
      if ((m = l.match(/^(?:s[ée]ance|module|journ[ée]e|session|cours)\s*(\d{1,2})\s*[:\-–—.)(]*\s*(.{4,140})$/i))) {
        const h = enHeures(l.match(RE_DUREE))
        res.seances.push({ num: Number(m[1]), titre: m[2].replace(RE_DUREE, '').replace(/[()\-–—:\s]+$/, '').trim(), heures: h })
      }
      // Structure : activités types, blocs, compétences
      if ((m = l.match(RE_AT)) && m[2] && m[2].length >= 4 && l.length < 220) {
        const num = Number(m[1])
        courant = res.activites.find((a) => a.num === num) || (res.activites.push({ num, titre: m[2].trim(), competences: [] }), res.activites.at(-1))
        enComp = false
        continue
      }
      if (((m = l.match(RE_BLOC_RNCP)) || (m = l.match(RE_BLOC))) && m[2] && m[2].length >= 4 && l.length < 260) {
        const num = Number(m[1])
        const titre = m[2].replace(/^bloc\s*\d+\s*[:\-–—.]*\s*/i, '').trim()
        courant = res.blocs.find((b) => b.num === num) || (res.blocs.push({ num, titre, competences: [] }), res.blocs.at(-1))
        enComp = false
        continue
      }
      if (RE_RUBRIQUE_COMP.test(l)) {
        if (!courant && /attest|vis[ée]/i.test(l)) {
          courant = { num: res.blocs.length + 1, titre: res.rs ? 'Compétences attestées' : 'Compétences visées', competences: [] }
          res.blocs.push(courant)
        }
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
        if (texte && !courant.competences.includes(texte) && !EPREUVES.some((e) => correspond(e, texte) && texte.length < 60)) courant.competences.push(texte)
      } else if (!courant && VERBE.test(l) && l.length >= 12 && l.length <= 160) res.libre.push(l.replace(VERBE, '').trim())
    }
    for (const l of lignes) {
      const m = l.match(/^(?:(?:module|partie|chapitre|s[ée]ance|s[ée]quence|unit[ée])\s*\d+\s*[:\-–—.)]*\s*|(\d{1,2})[.)]\s+)([A-ZÀ-Ý][^\n]{5,110})$/i)
      if (m && l.length < 130 && !/\d{4,}/.test(l)) res.libre.push((m[2] || l).trim())
    }
  }
  res.libre = [...new Set(res.libre)].slice(0, 60)
  res.activites.sort((a, b) => a.num - b.num)
  res.blocs.sort((a, b) => a.num - b.num)
  const vues = new Set()
  res.seances = res.seances.filter((x) => (vues.has(x.num + x.titre) ? false : vues.add(x.num + x.titre))).sort((a, b) => a.num - b.num)
  res.types = [...res.types]
  return res
}

/* ---------- Plan de formation ---------- */

export const HEURES_PAR_JOUR = 7 // 8h-12h + 13h-16h (horaires donnés par Aurélien)
export const PARTIES = ['Partie I — Notions et repères', 'Partie II — Mise en pratique', 'Partie III — Évaluation et bilan']
const REPARTITION_PARTIES = [0.3, 0.5, 0.2]
const STOP = new Set('de la le les des du un une et en au aux pour par sur dans avec son sa ses leur leurs ou à l d qui que est sont'.split(' '))
const mots = (s) => norm(s).split(/[^a-z0-9]+/).filter((m) => m.length > 3 && !STOP.has(m))
const pertinence = (texte, sujet) => {
  const cible = new Set(mots(sujet))
  return cible.size ? mots(texte).filter((m) => cible.has(m)).length : 0
}
const demi = (h) => Math.max(0.5, Math.round(h * 2) / 2)

/** Modalités d'évaluation rattachées à une compétence (par recoupement de vocabulaire). */
function evaluationsDe(competence, lignesEval) {
  const cles = mots(competence)
  if (cles.length < 2) return []
  const seuil = Math.max(2, Math.ceil(cles.length * 0.5))
  const trouvees = new Set()
  for (const l of lignesEval) {
    const lm = new Set(mots(l))
    if (cles.filter((c) => lm.has(c)).length >= seuil) for (const e of EPREUVES) if (correspond(e, l)) trouvees.add(e.nom)
  }
  return [...trouvees]
}

/** Heures de base par compétence selon la nature de la certification (estimation, à valider). */
const BASE_PAR_COMPETENCE = { TP: 35, RNCP: 28, RS: 7, Syllabus: 3.5, Libre: 7, Sujet: 3.5 }

/**
 * Construit le plan harmonisé.
 *  - extraction : résultat de extraire() (un ou plusieurs documents mélangés : REAC + RE, RNCP + RC, RS, syllabus…) ;
 *  - sujet : texte libre (cible et nomme) ;
 *  - options : { seqParAt, restreindre, nomProgramme, dureeTotale } (dureeTotale en heures, prioritaire sur l'estimation).
 */
export function construirePlan(extraction, sujet = '', { seqParAt = 3, restreindre = false, nomProgramme = '', dureeTotale = 0 } = {}) {
  const sujetNet = sujet.trim()
  let unites = extraction.activites.length ? extraction.activites : extraction.blocs
  const rubrique = extraction.activites.length ? 'AT' : extraction.blocs.length ? 'Bloc' : ''
  let nature = extraction.activites.length ? 'TP' : extraction.rs ? 'RS' : extraction.blocs.length ? 'RNCP' : ''
  let origine = rubrique ? `Documents (${rubrique === 'AT' ? 'activités types' : extraction.rs ? 'compétences de la fiche RS' : 'blocs de compétences'})` : ''
  if (restreindre && sujetNet && unites.length) {
    const garde = unites.filter((u) => pertinence(u.titre + ' ' + u.competences.join(' '), sujetNet) > 0)
    if (garde.length) unites = garde
  }
  if (!unites.length && extraction.seances.length >= 2) {
    const n = Math.ceil(extraction.seances.length / Math.max(1, seqParAt))
    unites = Array.from({ length: n }, (_, i) => {
      const lot = extraction.seances.slice(i * seqParAt, (i + 1) * seqParAt)
      return { num: i + 1, titre: lot.length > 1 ? `Séances ${lot[0].num} à ${lot.at(-1).num}` : `Séance ${lot[0].num}`, competences: lot.map((x) => x.titre), heuresSeances: lot.map((x) => x.heures) }
    })
    origine = 'Séances du syllabus'
    nature = 'Syllabus'
  }
  if (!unites.length && extraction.libre.length >= 3) {
    const lot = Math.ceil(extraction.libre.length / 3)
    unites = [0, 1, 2].map((i) => ({ num: i + 1, titre: `Partie ${i + 1} du document`, competences: extraction.libre.slice(i * lot, (i + 1) * lot) })).filter((u) => u.competences.length)
    origine = 'Titres repérés dans les documents'
    nature = 'Libre'
  }
  if (!unites.length) {
    const s = sujetNet || 'le sujet'
    unites = [
      { num: 1, titre: `Comprendre ${s}`, competences: [`Situer ${s} et ses enjeux`, `Maîtriser le vocabulaire de ${s}`, `Identifier les acteurs et les règles de ${s}`] },
      { num: 2, titre: `Pratiquer ${s}`, competences: [`Appliquer les méthodes de ${s} sur des cas réels`, `Utiliser les outils de ${s}`, `Analyser une situation de ${s}`] },
      { num: 3, titre: `Évaluer et progresser en ${s}`, competences: [`Mesurer ses résultats en ${s}`, `Corriger ses erreurs`, `Construire un plan d'amélioration`] },
    ]
    origine = 'Squelette bâti sur le sujet seul — à valider par le formateur'
    nature = 'Sujet'
  }
  const estTP = nature === 'TP'
  const programme = nomProgramme || extraction.programme || (sujetNet ? court(sujetNet, 40) : '') || 'Formation'
  const epreuves = extraction.epreuves
  const dossiers = extraction.dossiers.length ? extraction.dossiers : estTP ? ['Dossier professionnel (DP) — à confirmer avec le référentiel d’évaluation'] : []

  // 1. Cœur : activités types / blocs → séquences → parties
  const coeur = []
  for (const [i, u] of unites.entries()) {
    const comps = u.competences.length ? u.competences : [u.titre]
    const n = Math.max(1, Math.min(seqParAt, comps.length))
    const taille = Math.ceil(comps.length / n)
    const sequences = Array.from({ length: n }, (_, k) => {
      const lot = comps.slice(k * taille, (k + 1) * taille)
      const heuresDoc = (u.heuresSeances || []).slice(k * taille, (k + 1) * taille).reduce((a, h) => a + (h || 0), 0)
      const evaluations = [...new Set(lot.flatMap((c) => evaluationsDe(c, extraction.lignesEval)))]
      return { nom: `Sq ${k + 1} — ${court(lot[0], 34)}`, competences: lot, evaluations, heuresDoc, parties: PARTIES.map((p) => ({ nom: p })) }
    }).filter((s) => s.competences.length)
    coeur.push({ nom: `${nature === 'TP' ? 'AT' : rubrique === 'Bloc' ? 'Bloc' : 'Module'} ${u.num ?? i + 1} — ${court(u.titre, 36)}`, type: 'at', titre: u.titre, sequences })
  }

  // 2. Préparation (avant les AT) : accueil, certification, dossiers à constituer
  const prep = [
    { nom: 'Sq 1 — Accueil et positionnement', competences: ['Présenter la formation, les objectifs et le calendrier', 'Positionner chaque apprenant (questionnaire, entretien)', 'Recueillir les besoins d’adaptation (référent handicap)'], evaluations: [], poids: 1 },
  ]
  if (epreuves.length || nature !== 'Sujet') {
    prep.push({ nom: 'Sq 2 — Comprendre la certification et l’examen', competences: ['Expliquer le référentiel et les blocs ou activités types', `Présenter les épreuves : ${epreuves.length ? epreuves.map((e) => e.nom + (e.heures ? ` (${formatH(e.heures)})` : '')).join(', ') : 'à préciser avec le référentiel d’évaluation'}`, 'Planifier les échéances jusqu’à l’examen'], evaluations: [], poids: 1 })
  }
  for (const [k, d] of dossiers.entries()) {
    prep.push({ nom: `Sq ${prep.length + 1} — ${court(d.replace(/ —.*$/, ''), 34)}`, competences: [`Comprendre les attendus du ${d.replace(/ —.*$/, '')}`, 'Choisir les situations professionnelles à présenter', 'Planifier la rédaction et les relectures avec le formateur'], evaluations: [], poids: 1, dossier: true, rang: k })
  }

  // 3. Révision et examen final (après les AT)
  const rev = [
    { nom: 'Sq 1 — Révisions ciblées', competences: coeur.map((n) => `Réviser ${n.nom.replace(/ —.*/, '')} : ${court(n.titre, 60)}`), evaluations: [], poids: 2 },
    { nom: 'Sq 2 — Examen blanc', competences: epreuves.length ? epreuves.map((e) => `Simuler l’épreuve « ${e.nom} »${e.heures ? ` (${formatH(e.heures)})` : ''}`) : ['Simuler l’épreuve finale dans les conditions réelles (modalités à préciser)'], evaluations: epreuves.map((e) => e.nom), poids: 2 },
  ]
  if (epreuves.some((e) => ['EF', 'SOUT', 'PRES', 'ET'].includes(e.cle)) || dossiers.length) {
    rev.push({ nom: 'Sq 3 — Préparer l’oral devant le jury', competences: ['S’entraîner à présenter son dossier en temps limité', 'Répondre aux questions du jury', 'Gérer le stress et le temps'], evaluations: [], poids: 1 })
  }

  // 4. Estimation des heures
  const nbComp = coeur.reduce((a, n) => a + n.sequences.reduce((b, s) => b + s.competences.length, 0), 0)
  const coeurEstime = coeur.reduce((a, n) => a + n.sequences.reduce((b, s) => b + (s.heuresDoc || s.competences.length * BASE_PAR_COMPETENCE[nature]), 0), 0)
  const total = Number(dureeTotale) || extraction.dureeTotaleH || 0
  const parts = { prep: estTP ? 0.06 : 0.08, rev: estTP ? 0.12 : 0.1 }
  let source
  let hCoeur
  let hPrep
  let hRev
  if (total) {
    hPrep = total * parts.prep
    hRev = total * parts.rev
    hCoeur = total - hPrep - hRev
    source = Number(dureeTotale) ? 'Durée totale saisie, répartie automatiquement' : 'Durée totale trouvée dans les documents, répartie automatiquement'
  } else {
    hCoeur = coeurEstime
    hPrep = Math.max(3.5, hCoeur * parts.prep / (1 - parts.prep - parts.rev))
    hRev = Math.max(3.5, hCoeur * parts.rev / (1 - parts.prep - parts.rev)) + epreuves.reduce((a, e) => a + (e.heures || 0), 0)
    source = `Estimation (${BASE_PAR_COMPETENCE[nature]} h par compétence, profil ${nature}) — à valider`
  }
  const repartir = (seqs, heures, poids) => {
    const somme = seqs.reduce((a, s) => a + poids(s), 0) || 1
    for (const s of seqs) {
      s.heures = demi((heures * poids(s)) / somme)
      s.parties = PARTIES.map((p, i) => ({ nom: p, heures: demi(s.heures * REPARTITION_PARTIES[i]) }))
    }
  }
  repartir(prep, hPrep, (s) => s.poids)
  repartir(rev, hRev, (s) => s.poids)
  const toutesSeqCoeur = coeur.flatMap((n) => n.sequences)
  repartir(toutesSeqCoeur, hCoeur, (s) => (total ? s.competences.length : s.heuresDoc || s.competences.length * BASE_PAR_COMPETENCE[nature]))

  const noeuds = [
    { nom: estTP ? 'Préparation du TP' : 'Préparation', type: 'preparation', sequences: prep },
    ...coeur,
    { nom: estTP ? 'Révision TP (type examen final)' : 'Révision et examen final', type: 'revision', sequences: rev },
  ]
  for (const n of noeuds) n.heures = n.sequences.reduce((a, s) => a + s.heures, 0)
  const heuresTotales = noeuds.reduce((a, n) => a + n.heures, 0)

  // 5. Progression pédagogique (ordre, cumul, jour indicatif)
  let cumul = 0
  const progression = noeuds.flatMap((n) =>
    n.sequences.map((s) => {
      const debut = cumul
      cumul += s.heures
      return { bloc: n.nom, sequence: s.nom, heures: s.heures, jourDebut: Math.floor(debut / HEURES_PAR_JOUR) + 1, jourFin: Math.max(1, Math.ceil(cumul / HEURES_PAR_JOUR)) }
    }),
  )

  return {
    programme, rncp: extraction.rncp, rs: extraction.rs, niveau: extraction.niveau, origine, nature, types: extraction.types || [],
    evaluation: extraction.evaluation.slice(0, 8), epreuves, dossiers, noeuds, progression, sujet: sujetNet,
    heures: { total: heuresTotales, jours: Math.ceil(heuresTotales / HEURES_PAR_JOUR), source, nbCompetences: nbComp },
    examen: deroulementExamen(epreuves, dossiers),
  }
}

export function formatH(h) {
  if (!h) return ''
  const e = Math.floor(h)
  const m = Math.round((h - e) * 60)
  return e ? `${e} h${m ? String(m).padStart(2, '0') : ''}` : `${m} min`
}

/** Texte « comment se passera l'examen », bâti uniquement sur ce que disent les documents. */
export function deroulementExamen(epreuves, dossiers) {
  if (!epreuves.length && !dossiers.length) return ['Modalités d’examen non trouvées dans les documents : ajoutez le référentiel d’évaluation (RE), le référentiel de certification (RC) ou la fiche RNCP/RS.']
  const l = []
  if (dossiers.length) l.push(`Avant l’examen, l’apprenant remet : ${dossiers.join(', ')}.`)
  const hors = epreuves.filter((e) => e.cle !== 'ECF')
  if (hors.length) l.push(`Le jour de l’examen : ${hors.map((e) => e.nom + (e.heures ? ` (${formatH(e.heures)})` : '')).join(', ')}.`)
  if (epreuves.some((e) => e.cle === 'ECF')) l.push('Des évaluations passées en cours de formation (ECF) complètent le dossier présenté au jury.')
  const duree = hors.reduce((a, e) => a + (e.heures || 0), 0)
  if (duree) l.push(`Durée cumulée des épreuves trouvées : ${formatH(duree)} (à vérifier dans le référentiel).`)
  return l
}

/* ---------- Exports ---------- */

export const cleDate = (noeud, seq) => `${noeud.nom}|${seq.nom}`
export const fichierSur = (s) => s.replace(/[\\/:*?"<>|]/g, '-').replace(/\s+/g, ' ').trim()

/** Texte Markdown du plan (à coller dans Drive / Airtable). */
export function planMarkdown(plan, dates = {}) {
  const l = [
    `# ${plan.programme}`,
    '',
    `Source : ${plan.origine}${plan.rncp ? ` · RNCP${plan.rncp}` : ''}${plan.rs ? ` · RS${plan.rs}` : ''}${plan.niveau ? ` · niveau ${plan.niveau}` : ''}`,
    `Documents croisés : ${plan.types.length ? plan.types.join(' + ') : 'aucun (sujet seul)'}`,
    `Durée : ${formatH(plan.heures.total)} soit ${plan.heures.jours} jour(s) de ${HEURES_PAR_JOUR} h — ${plan.heures.source}`,
    '',
    '## Comment se passera l’examen',
    ...plan.examen.map((x) => `- ${x}`),
    '',
  ]
  for (const n of plan.noeuds) {
    l.push(`## ${n.nom} — ${formatH(n.heures)}`)
    for (const s of n.sequences || []) {
      l.push(`### ${s.nom} — ${formatH(s.heures)}${dates[cleDate(n, s)] ? ` — ${dates[cleDate(n, s)]}` : ''}`, ...s.competences.map((c) => `- ${c}`))
      if (s.evaluations?.length) l.push(`- Évaluée par : ${s.evaluations.join(', ')}`)
      l.push(...s.parties.map((p) => `  - ${p.nom}${p.heures ? ` (${formatH(p.heures)})` : ''}`), '')
    }
  }
  l.push('## Progression pédagogique', '', '| Bloc | Séquence | Durée | Jour(s) |', '|---|---|---|---|', ...plan.progression.map((p) => `| ${p.bloc} | ${p.sequence} | ${formatH(p.heures)} | ${p.jourDebut === p.jourFin ? 'J' + p.jourDebut : `J${p.jourDebut} à J${p.jourFin}`} |`))
  if (plan.evaluation.length) l.push('', '## Critères et modalités repérés', ...plan.evaluation.map((e) => `- ${e}`))
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
    for (const s of n.sequences || []) {
      const sd = fichierSur(s.nom + (dates[cleDate(n, s)] ? ` — ${dates[cleDate(n, s)]}` : ''))
      for (const p of s.parties) ajout(`${dossier}/${sd}/${fichierSur(p.nom)}/_a-remplir.txt`, `${s.nom} (${formatH(s.heures)})\n${p.nom}${p.heures ? ` (${formatH(p.heures)})` : ''}\n\nCompétences visées :\n${s.competences.map((c) => '- ' + c).join('\n')}\n${s.evaluations?.length ? `\nÉvaluée par : ${s.evaluations.join(', ')}\n` : ''}`)
    }
  }
  return zip.generateAsync({ type: 'blob' })
}
