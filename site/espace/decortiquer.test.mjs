import { Document, Packer, Paragraph } from 'docx'
import JSZip from 'jszip'
import { lireTout, extraire, construirePlan, typeDocument, arborescenceZip, planMarkdown } from './src/decortiquer.js'

const reacTexte = `Référentiel d'emploi, activités et compétences (REAC)
Titre professionnel Manager d'espace marchand
Niveau 5 (Bac+2) RNCP 38xxx
Activité type 1 : Assurer la gestion de l'espace marchand
Compétences professionnelles
• Organiser l'implantation des produits en rayon
• Gérer les stocks et les approvisionnements
• Analyser les écarts d'inventaire
Critères d'évaluation : exactitude des relevés
Activité type 2 : Manager l'équipe commerciale
Compétences professionnelles
• Planifier l'activité de l'équipe
• Animer une réunion d'équipe
• Conduire un entretien individuel
Activité type 3 : Piloter la performance de l'unité
Compétences professionnelles
• Construire un tableau de bord commercial
• Analyser le chiffre d'affaires
Modalités d'évaluation : mise en situation professionnelle de 2 heures`
const doc = new Document({ sections: [{ children: reacTexte.split('\n').map((t) => new Paragraph(t)) }] })
const docx = await Packer.toBuffer(doc)
const mk = (octets, nom, chemin) => Object.assign(new File([octets], nom), { _chemin: chemin })

// PDF minimal à la main (une page, texte)
const pdfTxt = 'BT /F1 12 Tf 50 700 Td (Fiche RNCP38999 blocs de competences niveau 6) Tj ET'
const objs = ['<< /Type /Catalog /Pages 2 0 R >>', '<< /Type /Pages /Kids [3 0 R] /Count 1 >>', '<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>', `<< /Length ${pdfTxt.length} >>\nstream\n${pdfTxt}\nendstream`, '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>']
let pdf = '%PDF-1.4\n', offs = []
objs.forEach((o, i) => { offs.push(pdf.length); pdf += `${i + 1} 0 obj\n${o}\nendobj\n` })
const x = pdf.length
pdf += `xref\n0 ${objs.length + 1}\n0000000000 65535 f \n` + offs.map((o) => String(o).padStart(10, '0') + ' 00000 n \n').join('') + `trailer\n<< /Size ${objs.length + 1} /Root 1 0 R >>\nstartxref\n${x}\n%%EOF`

// xlsx minimal
const xl = new JSZip()
xl.file('xl/sharedStrings.xml', '<sst><si><t>Épreuve</t></si><si><t>Mise en situation</t></si></sst>')
xl.file('xl/worksheets/sheet1.xml', '<worksheet><sheetData><row><c t="s"><v>0</v></c><c t="s"><v>1</v></c></row></sheetData></worksheet>')

const fichiers = [
  mk(docx, 'REAC-MEM.docx', 'dossier/REAC-MEM.docx'),
  mk(Buffer.from(pdf, 'latin1'), 'fiche.pdf', 'dossier/fiche.pdf'),
  mk(await xl.generateAsync({ type: 'uint8array' }), 'grille.xlsx', 'dossier/sous/grille.xlsx'),
  mk('<html><body><h1>Syllabus</h1><p>Objectifs pédagogiques</p></body></html>', 'syl.html', 'dossier/syl.html'),
  mk('x', 'image.png', 'dossier/image.png'),
  mk('x', '.DS_Store', 'dossier/.DS_Store'),
]
const lus = await lireTout(fichiers)
for (const l of lus) console.log(l.chemin, '→', l.ignore ? 'IGNORÉ: ' + l.ignore : `${l.texte.length} car. · ${typeDocument(l.texte, l.nom)}`)
const ex = extraire(lus)
console.log(JSON.stringify({ programme: ex.programme, rncp: ex.rncp, niveau: ex.niveau, activites: ex.activites.map((a) => [a.num, a.titre, a.competences.length]), eval: ex.evaluation }, null, 1))
const plan = construirePlan(ex, 'manager une équipe commerciale', { restreindre: true })
console.log(plan.origine, '|', plan.noeuds.map((n) => n.nom + (n.sequences ? ` [${n.sequences.length} sq]` : '')))
const vide = construirePlan(extraire([]), 'Excel pour la gestion de stock')
console.log(vide.origine, '|', vide.noeuds.map((n) => n.nom))
const blob = await arborescenceZip(plan, { [`${plan.noeuds[1].nom}|${plan.noeuds[1].sequences[0].nom}`]: '2026-12-03' })
const z = await JSZip.loadAsync(await blob.arrayBuffer())
console.log(Object.keys(z.files).filter((f) => f.endsWith('/')).slice(0, 6), Object.keys(z.files).length, 'entrées')
