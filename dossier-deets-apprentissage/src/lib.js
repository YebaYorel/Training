// Générateur commun des pièces du dossier DEETS (extension apprentissage).
// Mini-balisage du texte : **gras**, [[à compléter]] (surligné jaune).
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, Header, Footer,
  AlignmentType, HeadingLevel, LevelFormat, WidthType, ShadingType, BorderStyle,
  PageNumber, PageBreak, HighlightColor, TableLayoutType, PageOrientation, ImageRun,
} = require('docx');

// Charte YEBA FORMATIONS 2026 : bleu #1B3A6B, or #C9AB4C, noir #121212.
// L'or (contraste 2,2:1 sur blanc) sert aux filets et fonds, jamais au texte (accessibilité).
const COLORS = { primary: '1B3A6B', accent: 'C9AB4C', text: '121212', light: 'EEF1F6', gold: 'F7F1DF', grey: '4D4D4D' };
const FONT = 'Inter';
const TITLE_FONT = 'Montserrat';
const LOGO = fs.readFileSync(require('path').join(__dirname, 'assets', 'logo_yeba.png'));
const PAGE_W = 11906, MARGIN = 1134; // A4, marges 2 cm
let CONTENT_W = PAGE_W - 2 * MARGIN; // élargi en paysage par build()

const IDENT = {
  nom: 'YEBA FORMATIONS',
  siret: '814 622 262 00032',
  nda: '04973676397',
  qualiopi: '25FOR02027.1',
  dirigeant: 'Aurélien LUMEKA',
  uai: '9742022E',
  lieu: '7 rue Henri Cornu, Immeuble Rodrigue 2, Technopole Réunion / Technor, 97490 Sainte-Clotilde (Saint-Denis)',
  version: 'Version 3 du 30/10/2026',
  tel: '+262 693 32 24 45',
  mail: 'yebaformations@gmail.com',
};

function runs(text, base = {}) {
  const out = [];
  for (const part of String(text).split(/(\*\*[^*]+\*\*|\[\[[^\]]+\]\])/)) {
    if (!part) continue;
    if (part.startsWith('**')) out.push(new TextRun({ text: part.slice(2, -2), bold: true, font: FONT, ...base }));
    else if (part.startsWith('[[')) out.push(new TextRun({ text: '[' + part.slice(2, -2) + ']', bold: true, highlight: HighlightColor.YELLOW, font: FONT, ...base }));
    else out.push(new TextRun({ text: part, font: FONT, ...base }));
  }
  return out;
}

const p = (t, o = {}) => new Paragraph({ children: runs(t, o.run || {}), spacing: { after: 120, line: 288 }, alignment: o.align || AlignmentType.JUSTIFIED, ...(o.para || {}) });
const h1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: t, font: TITLE_FONT })], spacing: { before: 300, after: 140 }, keepNext: true });
const h2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text: t, font: TITLE_FONT })], spacing: { before: 200, after: 100 }, keepNext: true });
const li = (t, ref = 'bul', level = 0) => new Paragraph({ numbering: { reference: ref, level }, children: runs(t), alignment: AlignmentType.JUSTIFIED, spacing: { after: 60, line: 276 } });

function cell(text, w, o = {}) {
  const lines = Array.isArray(text) ? text : [text];
  return new TableCell({
    width: { size: w, type: WidthType.DXA },
    shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill, color: 'auto' } : undefined,
    margins: { top: 60, bottom: 60, left: 90, right: 90 },
    // Texte justifié dans les colonnes assez larges ; à gauche dans les colonnes étroites (évite les grands blancs).
    children: lines.map((l) => new Paragraph({ children: runs(l, o.run || {}), alignment: w >= 3500 && !o.run && String(l).length > 140 ? AlignmentType.JUSTIFIED : AlignmentType.LEFT, spacing: { after: 40 } })),
  });
}

function table(headers, rows, widths) {
  const total = CONTENT_W;
  if (!widths) widths = headers.map(() => Math.floor(total / headers.length));
  const sum = widths.reduce((a, b) => a + b, 0);
  widths = widths.map((w) => Math.floor((w * total) / sum));
  widths[widths.length - 1] += total - widths.reduce((a, b) => a + b, 0);
  const border = { style: BorderStyle.SINGLE, size: 4, color: 'A6A6A6' };
  return new Table({
    width: { size: total, type: WidthType.DXA },
    columnWidths: widths,
    layout: TableLayoutType.FIXED,
    borders: { top: border, bottom: border, left: border, right: border, insideHorizontal: border, insideVertical: border },
    rows: [
      new TableRow({ tableHeader: true, children: headers.map((hd, i) => cell(hd, widths[i], { fill: COLORS.primary, run: { bold: true, color: 'FFFFFF' } })) }),
      ...rows.map((r, ri) => new TableRow({ cantSplit: JSON.stringify(r).length < 400, children: r.map((c, i) => cell(c, widths[i], { fill: ri % 2 ? COLORS.light : undefined })) })),
    ],
  });
}

// Encadré (note, point de vigilance RGPD / IA Act, etc.)
function box(title, lines, fill = COLORS.gold, edge = COLORS.accent) {
  const b = { style: BorderStyle.SINGLE, size: 12, color: edge };
  const nb = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: [CONTENT_W],
    borders: { top: nb, bottom: nb, right: nb, left: b, insideHorizontal: nb, insideVertical: nb },
    rows: [new TableRow({ children: [new TableCell({
      width: { size: CONTENT_W, type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill, color: 'auto' },
      margins: { top: 100, bottom: 100, left: 160, right: 120 },
      children: [
        new Paragraph({ children: [new TextRun({ text: title, bold: true, color: COLORS.primary, font: TITLE_FONT })], spacing: { after: 60 } }),
        ...lines.map((l) => new Paragraph({ children: runs(l), alignment: AlignmentType.JUSTIFIED, spacing: { after: 50 } })),
      ],
    })] })],
  });
}
const rgpd = (lines) => box('Conformité RGPD / IA Act', lines, COLORS.light, COLORS.primary);
const spacer = () => new Paragraph({ children: [], spacing: { after: 80 } });

function cover(num, title, objet) {
  return [
    new Paragraph({ children: [new ImageRun({ type: 'png', data: LOGO, transformation: { width: 120, height: 102 }, altText: { title: 'Logo YEBA FORMATIONS', description: 'Logo YEBA FORMATIONS', name: 'logo' } })], spacing: { after: 80 } }),
    new Paragraph({ children: [new TextRun({ text: 'Organisme de formation — Extension de la déclaration d’activité à la formation par apprentissage', size: 20, color: COLORS.grey, font: FONT })], border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: COLORS.accent, space: 6 } }, spacing: { after: 240 } }),
    new Paragraph({ children: [new TextRun({ text: num === 'NI' ? 'Note interne — ne pas transmettre' : `Pièce n° ${num}`, bold: true, size: 24, color: COLORS.grey, font: TITLE_FONT })], spacing: { after: 60 } }),
    new Paragraph({ children: [new TextRun({ text: title, bold: true, size: 32, color: COLORS.primary, font: TITLE_FONT })], spacing: { after: 160 } }),
    table(['Rubrique', 'Information'], num === 'NI' ? [
      ['Usage', 'Document de travail interne — ne pas joindre au dossier DEETS'],
      ['Objet', objet],
      ['Rédigé pour', `${IDENT.dirigeant}, Directeur`],
      ['Version', IDENT.version],
    ] : [
      ['Destinataire', 'DEETS La Réunion — Service de contrôle de la formation professionnelle'],
      ['Référence', 'Courriel de la DEETS du 20 octobre 2026 — instruction au titre de l’article L.6351-5 du Code du travail'],
      ['Objet de la pièce', objet],
      ['Organisme', `${IDENT.nom} — SIRET ${IDENT.siret} — NDA ${IDENT.nda} — UAI ${IDENT.uai}`],
      ['Lieu de formation', IDENT.lieu],
      ['Certification Qualiopi', `n° ${IDENT.qualiopi} (actions de formation). Extension à la catégorie « actions de formation par apprentissage » engagée : l’audit d’extension sera réalisé dès l’entrée en formation du premier apprenti (courriel de l’organisme certificateur du 14/10/2026).`],
      ['Responsable', `${IDENT.dirigeant}, Directeur — ${IDENT.tel} — ${IDENT.mail}`],
      ['Version', IDENT.version],
    ], [2600, 7038]),
    spacer(),
  ];
}

function signature() {
  return [
    spacer(),
    p(`Fait à Saint-Denis, le [[date d’envoi]].`, { align: AlignmentType.LEFT }),
    p(`${IDENT.dirigeant}, Directeur de ${IDENT.nom}`, { align: AlignmentType.LEFT, run: { bold: true } }),
    p('Signature et cachet :', { align: AlignmentType.LEFT }),
  ];
}

// Construit un document à partir d'une liste de blocs.
// Blocs : ['h1',t] ['h2',t] ['p',t] ['ul',[..]] ['ol',[..]] ['table',headers,rows,widths?] ['box',titre,[..]] ['rgpd',[..]] ['pb']
let olCounter = 0;
function build({ num, title, objet, blocks, file, landscape }) {
  CONTENT_W = (landscape ? 16838 : PAGE_W) - 2 * MARGIN;
  const children = [...cover(num, title, objet)];
  const numberingConfigs = [{ reference: 'bul', levels: [
    { level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 567, hanging: 283 } } } },
    { level: 1, format: LevelFormat.BULLET, text: '–', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1134, hanging: 283 } } } },
  ] }];
  for (const b of blocks) {
    const [k, ...a] = b;
    if (k === 'h1') children.push(h1(a[0]));
    else if (k === 'h2') children.push(h2(a[0]));
    else if (k === 'p') children.push(p(a[0]));
    else if (k === 'ul') a[0].forEach((t) => Array.isArray(t) ? t.forEach((s) => children.push(li(s, 'bul', 1))) : children.push(li(t)));
    else if (k === 'ol') {
      const ref = 'ol' + (++olCounter);
      numberingConfigs.push({ reference: ref, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 567, hanging: 340 } } } }] });
      a[0].forEach((t) => children.push(li(t, ref)));
    } else if (k === 'table') { children.push(table(a[0], a[1], a[2])); children.push(spacer()); }
    else if (k === 'box') { children.push(box(a[0], a[1])); children.push(spacer()); }
    else if (k === 'rgpd') { children.push(rgpd(a[0])); children.push(spacer()); }
    else if (k === 'pb') children.push(new Paragraph({ children: [new PageBreak()] }));
    else throw new Error('bloc inconnu ' + k);
  }
  if (num !== 'NI') children.push(...signature());

  const small = { size: 16, color: COLORS.grey, font: FONT };
  const doc = new Document({
    creator: IDENT.dirigeant,
    title: `${IDENT.nom} — ${num === 'NI' ? 'Note interne' : 'Pièce ' + num} — ${title}`,
    styles: {
      default: { document: { run: { font: FONT, size: 22, color: COLORS.text } } },
      paragraphStyles: [
        { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 28, bold: true, color: COLORS.primary, font: TITLE_FONT }, paragraph: { outlineLevel: 0, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: COLORS.accent, space: 4 } } } },
        { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 24, bold: true, color: COLORS.primary, font: TITLE_FONT }, paragraph: { outlineLevel: 1 } },
      ],
    },
    numbering: { config: numberingConfigs },
    sections: [{
      properties: { page: { size: { width: PAGE_W, height: 16838, orientation: landscape ? PageOrientation.LANDSCAPE : PageOrientation.PORTRAIT }, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } } },
      headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: num === 'NI' ? `${IDENT.nom} — Note interne` : `${IDENT.nom} — Dossier apprentissage — Pièce ${num}`, ...small })] })] }) },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
        new TextRun({ text: `SIRET ${IDENT.siret} — NDA ${IDENT.nda} — Qualiopi ${IDENT.qualiopi} — Page `, ...small }),
        new TextRun({ children: [PageNumber.CURRENT], ...small }), new TextRun({ text: ' / ', ...small }),
        new TextRun({ children: [PageNumber.TOTAL_PAGES], ...small }),
      ] })] }) },
      children,
    }],
  });
  return Packer.toBuffer(doc).then((buf) => fs.writeFileSync(file, buf));
}

// Liste des mentions [[à compléter]] d'un ensemble de blocs (pour le bordereau).
function placeholders(blocks) {
  const s = new Set();
  const walk = (x) => { if (typeof x === 'string') (x.match(/\[\[[^\]]+\]\]/g) || []).forEach((m) => s.add(m.slice(2, -2))); else if (Array.isArray(x)) x.forEach(walk); };
  walk(blocks);
  return [...s];
}

module.exports = { build, placeholders, IDENT };
