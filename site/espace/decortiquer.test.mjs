// Test du module Ingénierie : node site/espace/decortiquer.test.mjs
// Cas : REAC + RE mélangés, fiche RNCP + RC, fiche RS, syllabus à séances, sujet seul, formats (docx, pdf, xlsx, html).
import assert from 'node:assert/strict'
import { Document, Packer, Paragraph } from 'docx'
import JSZip from 'jszip'
import { lireTout, extraire, construirePlan, typeDocument, arborescenceZip, planMarkdown, HEURES_PAR_JOUR } from './src/decortiquer.js'

const mk = (octets, nom, chemin) => Object.assign(new File([octets], nom), { _chemin: chemin })
const docx = async (texte) => Packer.toBuffer(new Document({ sections: [{ children: texte.split('\n').map((t) => new Paragraph(t)) }] }))

const REAC = `Référentiel d'emploi, activités et compétences (REAC)
Titre professionnel Manager d'espace marchand
Niveau 5 RNCP 38123
Activité type 1 : Assurer la gestion de l'espace marchand
Compétences professionnelles
• Organiser l'implantation des produits en rayon
• Gérer les stocks et les approvisionnements
• Analyser les écarts d'inventaire
Activité type 2 : Manager l'équipe commerciale
Compétences professionnelles
• Planifier l'activité de l'équipe
• Animer une réunion d'équipe
• Conduire un entretien individuel
Activité type 3 : PILOTER LA PERFORMANCE ET LES RÉSULTATS
Compétences professionnelles
• Construire un tableau de bord commercial
• Analyser le chiffre d'affaires`
const RE = `Référentiel d'évaluation (RE) — Titre professionnel Manager d'espace marchand
Modalités d'évaluation pour l'obtention du titre
Mise en situation professionnelle : 2 h 30
Entretien technique : 30 min
Questionnaire professionnel : 1 h
Entretien final : 20 min
Le candidat présente son dossier professionnel (DP) au jury.
Évaluations passées en cours de formation (ECF) pour chaque CCP.
Compétences évaluées
Organiser l'implantation des produits en rayon : MSP + ET
Conduire un entretien individuel : MSP + EF
Construire un tableau de bord commercial : QP`

// PDF minimal (une page de texte) écrit à la main
function pdf(texte) {
  const flux = `BT /F1 12 Tf 50 700 Td (${texte}) Tj ET`
  const objs = ['<< /Type /Catalog /Pages 2 0 R >>', '<< /Type /Pages /Kids [3 0 R] /Count 1 >>', '<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>', `<< /Length ${flux.length} >>\nstream\n${flux}\nendstream`, '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>']
  let s = '%PDF-1.4\n'
  const offs = []
  objs.forEach((o, i) => (offs.push(s.length), (s += `${i + 1} 0 obj\n${o}\nendobj\n`)))
  const x = s.length
  s += `xref\n0 ${objs.length + 1}\n0000000000 65535 f \n` + offs.map((o) => String(o).padStart(10, '0') + ' 00000 n \n').join('') + `trailer\n<< /Size ${objs.length + 1} /Root 1 0 R >>\nstartxref\n${x}\n%%EOF`
  return Buffer.from(s, 'latin1')
}
const xl = new JSZip()
xl.file('xl/sharedStrings.xml', '<sst><si><t>Épreuve</t></si><si><t>Mise en situation</t></si></sst>')
xl.file('xl/worksheets/sheet1.xml', '<worksheet><sheetData><row><c t="s"><v>0</v></c><c t="s"><v>1</v></c></row></sheetData></worksheet>')

// 1. Formats + REAC + RE mélangés
const lus = await lireTout([
  mk(await docx(REAC), 'REAC-MEM.docx', 'TP/REAC-MEM.docx'),
  mk(await docx(RE), 'RE-MEM.docx', 'TP/RE-MEM.docx'),
  mk(pdf('Fiche RNCP38999 blocs de competences niveau 6'), 'fiche.pdf', 'TP/fiche.pdf'),
  mk(await xl.generateAsync({ type: 'uint8array' }), 'grille.xlsx', 'TP/sous/grille.xlsx'),
  mk('<html><body><h1>Syllabus</h1><p>Objectifs pédagogiques</p></body></html>', 'syl.html', 'TP/syl.html'),
  mk('x', 'photo.png', 'TP/photo.png'),
  mk('x', '.DS_Store', 'TP/.DS_Store'),
])
for (const l of lus) console.log(' ', l.chemin, '→', l.ignore ? 'ignoré : ' + l.ignore : typeDocument(l.texte, l.nom))
assert.equal(typeDocument(lus[0].texte), 'REAC')
assert.equal(typeDocument(lus[1].texte), 'Référentiel d’évaluation (RE)')
assert.ok(lus[2].texte.includes('RNCP38999'), 'PDF lu')
assert.ok(lus[5].ignore && lus[6].ignore, 'fichiers inutiles écartés')

const ex = extraire(lus)
assert.equal(ex.activites.length, 3)
assert.deepEqual(ex.epreuves.map((e) => e.cle).sort(), ['ECF', 'EF', 'ET', 'MS', 'MSP', 'QP'].sort())
assert.equal(ex.epreuves.find((e) => e.cle === 'MSP').heures, 2.5)
assert.equal(ex.epreuves.find((e) => e.cle === 'ET').heures, 0.5)
assert.ok(ex.dossiers.includes('Dossier professionnel (DP)'))
assert.ok(!ex.epreuves.some((e) => e.detail.startsWith('Activité type 3')), 'titre en majuscules contenant « ET » non pris pour un entretien technique')

const plan = construirePlan(ex, '', { nomProgramme: 'TP MEM' })
const noms = plan.noeuds.map((n) => n.nom)
assert.equal(noms[0], 'Préparation du TP')
assert.equal(noms.at(-1), 'Révision TP (type examen final)')
assert.ok(plan.noeuds[0].sequences.some((s) => /Dossier professionnel/.test(s.nom)), 'préparation au DP')
const sqImplantation = plan.noeuds[1].sequences.find((s) => s.competences.includes("Organiser l'implantation des produits en rayon"))
assert.ok(sqImplantation.evaluations.includes('Mise en situation professionnelle'), 'compétence reliée à son épreuve')
assert.ok(plan.heures.total > 100 && plan.heures.source.startsWith('Estimation'))
assert.equal(plan.heures.jours, Math.ceil(plan.heures.total / HEURES_PAR_JOUR))
console.log('  REAC+RE :', noms.join(' | '), '·', plan.heures.total, 'h ·', plan.heures.jours, 'j')
console.log('  Examen :', plan.examen.join(' '))

// 2. Durée totale imposée
const p2 = construirePlan(ex, '', { dureeTotale: 420 })
assert.ok(Math.abs(p2.heures.total - 420) <= 6, `total ≈ 420 h (obtenu ${p2.heures.total})`)

// 3. Fiche RNCP + référentiel de certification
const rncp = extraire([{ chemin: 'r.txt', nom: 'r.txt', texte: `Fiche RNCP38808 - Responsable d'activité commerciale et marketing
France Compétences - Niveau 6
RNCP38808BC01 - Élaborer le plan d'action commercial et marketing
- Mobiliser des sources d'information digitales pour exercer une veille
- Réaliser une analyse concurrentielle omnicanale
RNCP38808BC02 - Piloter l'activité commerciale
- Construire des tableaux de bord de suivi
Modalités d'évaluation : étude de cas et soutenance orale de 30 min` }])
assert.equal(rncp.blocs.length, 2)
assert.equal(rncp.rncp, '38808')
const p3 = construirePlan(rncp)
assert.ok(p3.noeuds[1].nom.startsWith('Bloc 1'))
assert.ok(p3.epreuves.some((e) => e.cle === 'SOUT') && p3.epreuves.some((e) => e.cle === 'CAS'))
console.log('  RNCP :', p3.noeuds.map((n) => n.nom).join(' | '), '·', p3.heures.total, 'h')

// 4. Fiche RS
const rs = extraire([{ chemin: 's.txt', nom: 's.txt', texte: `Répertoire spécifique RS6789 - Utiliser l'IA générative en entreprise
Compétences attestées :
- Rédiger des requêtes efficaces pour un outil d'IA générative
- Vérifier la fiabilité d'une réponse produite par une IA
- Respecter le RGPD et le règlement européen sur l'IA
Modalités d'évaluation : QCM de 30 minutes et mise en situation` }])
assert.equal(rs.rs, '6789')
const p4 = construirePlan(rs)
assert.equal(p4.nature, 'RS')
assert.ok(p4.heures.total < 60, 'formation courte pour un RS')
console.log('  RS :', p4.noeuds.map((n) => n.nom).join(' | '), '·', p4.heures.total, 'h')

// 5. Syllabus à séances
const syl = extraire([{ chemin: 'y.txt', nom: 'y.txt', texte: `Syllabus — Excel pour la gestion
Objectifs pédagogiques : maîtriser les tableaux
Séance 1 : Découvrir l'interface (3h)
Séance 2 : Formules de base (3h30)
Séance 3 : Tableaux croisés dynamiques (3h)
Séance 4 : Graphiques (2h)` }])
assert.equal(syl.seances.length, 4)
const p5 = construirePlan(syl)
assert.equal(p5.nature, 'Syllabus')
console.log('  Syllabus :', p5.noeuds.map((n) => n.nom).join(' | '), '·', p5.heures.total, 'h')

// 6. Sujet seul
const p6 = construirePlan(extraire([]), 'RGPD et IA Act en TPE')
assert.ok(p6.origine.startsWith('Squelette'))
assert.ok(p6.examen[0].startsWith('Modalités d’examen non trouvées'))

// 7. Exports
const md = planMarkdown(plan)
assert.ok(md.includes('## Comment se passera l’examen') && md.includes('## Progression pédagogique'))
const z = await JSZip.loadAsync(await (await arborescenceZip(plan)).arrayBuffer())
assert.ok(Object.keys(z.files).some((f) => f.includes('Préparation du TP/Sq 3 — Dossier professionnel')))
console.log('\nTous les tests passent ✔')
