// Génération de documents Word (.docx) modifiables, dans le navigateur (aucun envoi réseau).
// La bibliothèque « docx » (MIT) n'est chargée qu'au premier document demandé.
// Mise en forme accessible : vrais titres Word (navigation, lecteurs d'écran), Arial 11, contrastes forts.

const A_COMPLETER = /(\[À COMPLÉTER[^\]]*\])/

/** Valeur ou repère jaune « [À COMPLÉTER : …] » bien visible dans Word. */
export const v = (val, libelle) => (val != null && String(val).trim() !== '' ? String(val) : `[À COMPLÉTER : ${libelle}]`)

export async function genererDocx({ titre, organisme: o = {}, blocs, essai = false, sujet = '' }) {
  const d = await import('docx')
  const { AlignmentType, BorderStyle, Document, Footer, Header, HeadingLevel, LevelFormat, Packer, PageNumber, Paragraph, ShadingType, Table, TableCell, TableRow, TextRun, WidthType } = d
  const couleur = (o.couleur || '#1B3A6B').replace('#', '').toUpperCase()
  let liste = 0

  const runs = (texte, opts = {}) =>
    String(texte ?? '')
      .split(A_COMPLETER)
      .filter((x) => x !== '')
      .map((morceau) => (A_COMPLETER.test(morceau) ? new TextRun({ text: morceau, bold: true, highlight: 'yellow', ...opts }) : new TextRun({ text: morceau, ...opts })))

  const para = (texte, opts = {}, popts = {}) => new Paragraph({ children: runs(texte, opts), spacing: { after: 120 }, ...popts })

  function cellule(texte, { entete = false, largeur } = {}) {
    return new TableCell({
      width: largeur ? { size: largeur, type: WidthType.PERCENTAGE } : undefined,
      shading: entete ? { type: ShadingType.CLEAR, fill: couleur, color: 'auto' } : undefined,
      margins: { top: 80, bottom: 80, left: 100, right: 100 },
      children: String(texte ?? '').split('\n').map((l) => new Paragraph({ children: runs(l, entete ? { bold: true, color: 'FFFFFF' } : {}) })),
    })
  }

  const enfants = []
  let dernierType = null
  for (const b of blocs.filter(Boolean)) {
    const [type, contenu] = Object.entries(b)[0]
    if ((type === 'num' || type === 'li') && dernierType !== type) liste++
    dernierType = type
    switch (type) {
      case 'h1':
        enfants.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: runs(contenu), spacing: { before: 240, after: 160 } }))
        break
      case 'h2':
        enfants.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: runs(contenu), spacing: { before: 240, after: 120 } }))
        break
      case 'h3':
        enfants.push(new Paragraph({ heading: HeadingLevel.HEADING_3, children: runs(contenu), spacing: { before: 160, after: 80 } }))
        break
      case 'p':
        enfants.push(para(contenu))
        break
      case 'gras':
        enfants.push(para(contenu, { bold: true }))
        break
      case 'petit':
        enfants.push(para(contenu, { size: 18, color: '4A5870' }))
        break
      case 'li':
        enfants.push(new Paragraph({ children: runs(contenu), numbering: { reference: 'puces', level: 0 }, spacing: { after: 60 } }))
        break
      case 'num':
        enfants.push(new Paragraph({ children: runs(contenu), numbering: { reference: 'numeros', level: 0, instance: liste }, spacing: { after: 60 } }))
        break
      case 'case':
        enfants.push(para('☐  ' + contenu))
        break
      case 'encadre':
        enfants.push(
          new Paragraph({
            children: runs(contenu),
            border: { left: { style: BorderStyle.SINGLE, size: 24, color: 'C9A84C', space: 8 } },
            shading: { type: ShadingType.CLEAR, fill: 'F6F1E3', color: 'auto' },
            spacing: { before: 120, after: 160 },
            indent: { left: 200 },
          }),
        )
        break
      case 'champs': // lignes « Libellé : ……… » à remplir
        for (const l of contenu) enfants.push(para(`${l} : ………………………………………………………………`))
        break
      case 'table': {
        const { entetes, lignes, largeurs } = contenu
        enfants.push(
          new Table({
            width: { size: 100, type: WidthType.PERCENTAGE },
            rows: [
              new TableRow({ tableHeader: true, children: entetes.map((e, i) => cellule(e, { entete: true, largeur: largeurs?.[i] })) }),
              ...lignes.map((l) => new TableRow({ cantSplit: true, children: l.map((c, i) => cellule(c, { largeur: largeurs?.[i] })) })),
            ],
          }),
          new Paragraph({ text: '' }),
        )
        break
      }
      case 'signatures':
        enfants.push(
          new Table({
            width: { size: 100, type: WidthType.PERCENTAGE },
            rows: [new TableRow({ children: contenu.map((s) => new TableCell({ margins: { top: 100, bottom: 900, left: 100, right: 100 }, children: [para(s, { bold: true }), para('Date et signature :')] })) })],
          }),
        )
        break
      case 'saut':
        enfants.push(new Paragraph({ pageBreakBefore: true, children: [] }))
        break
      default:
        enfants.push(para(contenu))
    }
  }

  const piedTexte = [o.nom, o.siret && `SIRET ${o.siret}`, o.nda && `Déclaration d’activité n° ${o.nda}${o.prefecture ? ` auprès du ${o.prefecture}` : ''}`].filter(Boolean).join(' · ')
  const doc = new Document({
    creator: o.nom || 'Organisme de formation',
    title: titre,
    subject: sujet,
    styles: {
      default: { document: { run: { font: 'Arial', size: 22 } } },
      paragraphStyles: [
        { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 34, bold: true, color: couleur } },
        { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 27, bold: true, color: couleur } },
        { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 23, bold: true, color: '121212' } },
      ],
    },
    numbering: {
      config: [
        { reference: 'puces', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
        { reference: 'numeros', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      ],
    },
    sections: [
      {
        properties: { page: { margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } },
        headers: {
          default: new Header({
            children: [
              new Paragraph({
                border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: couleur, space: 4 } },
                children: [
                  new TextRun({ text: o.nom || '[À COMPLÉTER : nom de l’organisme]', bold: true, color: couleur }),
                  ...(essai ? [new TextRun({ text: '   —   DOCUMENT D’ESSAI YEBA STUDIO, NON VALABLE', bold: true, color: 'A3262A' })] : []),
                ],
              }),
            ],
          }),
        },
        footers: {
          default: new Footer({
            children: [
              new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [new TextRun({ text: piedTexte, size: 16, color: '4A5870' }), new TextRun({ children: ['   —   Page ', PageNumber.CURRENT, ' / ', PageNumber.TOTAL_PAGES], size: 16, color: '4A5870' })],
              }),
            ],
          }),
        },
        children: enfants,
      },
    ],
  })
  return Packer.toBlob(doc)
}

export function telechargerBlob(nom, blob) {
  const url = URL.createObjectURL(blob)
  const a = Object.assign(document.createElement('a'), { href: url, download: nom })
  document.body.append(a)
  a.click()
  a.remove()
  setTimeout(() => URL.revokeObjectURL(url), 2000)
}

export const nomFichier = (t) => t.normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^A-Za-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 80) + '.docx'
