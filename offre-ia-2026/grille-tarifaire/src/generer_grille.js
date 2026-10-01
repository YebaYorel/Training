// Grille tarifaire 2026 — Formations IA — YEBA FORMATIONS
// Génère 3 fichiers Word (une version par charte) : node generer_grille.js
// Prérequis : python3 generer_visuels.py (bandeaux + QR)
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType,
  ShadingType, AlignmentType, LineRuleType, BorderStyle, LevelFormat, Footer, PageNumber, VerticalAlign,
  TableLayoutType,
} = require('docx');

const ICI = __dirname;
const SORTIE = path.join(ICI, '..');

// ---------- Données (une seule source : modifier ici, puis relancer) ----------
const PRIX = {
  n1Inter: '790 €', n2Inter: '999 €',
  n1Intra: '3 890 €', n2Intra: '4 990 €',
  n1Supp: '350 €', n2Supp: '450 €',
  duo: '1 590 €', duoBarre: '1 789 €',
};
const CONTACT = {
  tel: '+262 6 93 32 24 45', mail: 'contact@yebaformations.com', web: 'yebaformations.re',
  adr: '9 rue Françoise Châtelain, 97490 Saint-Denis', url: 'yebaformations.re/tarifs',
};

const VERSIONS = [
  { code: 'V1', fichier: 'Grille_tarifaire_IA_2026_V1_Bleu-nuit-et-or', nom: 'Version 1 — Bleu nuit & or',
    sombre: '1B3A6B', nuit: '070F20', clair: 'F7F4EC', encre: '1B3A6B', or: 'C9A84C', doux: 'DBE3F0', titre: 'Montserrat' },
  { code: 'V2', fichier: 'Grille_tarifaire_IA_2026_V2_Heritage_creme-brun-or', nom: 'Version 2 — Héritage crème, brun & or',
    sombre: '4A3F31', nuit: '241E16', clair: 'F4EFDF', encre: '3F3529', or: 'C5A35A', doux: 'E9E1CC', titre: 'Playfair Display' },
  { code: 'V3', fichier: 'Grille_tarifaire_IA_2026_V3_Fusion_bleu-creme-or', nom: 'Version 3 — Fusion bleu nuit, crème & or',
    sombre: '1B3A6B', nuit: '070F20', clair: 'F4EFDF', encre: '1B3A6B', or: 'C9A84C', doux: 'DBE3F0', titre: 'Playfair Display' },
];

// ---------- Mise en page ----------
const LARGEUR = 10466; // A4 (11906) − 2 × 720 de marge
const CORPS = 'Inter';
const pt = (n) => n * 2; // docx : demi-points
const AUCUNE = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const SANS_BORDURE = { top: AUCUNE, bottom: AUCUNE, left: AUCUNE, right: AUCUNE };

function construire(v) {
  const t = (texte, o = {}) => new TextRun({ text: texte, font: o.font || CORPS, size: pt(o.size || 12),
    bold: o.bold, color: o.color || '1E1E1E', italics: o.italics, strike: o.strike, characterSpacing: o.spacing });
  const p = (runs, o = {}) => new Paragraph({ children: Array.isArray(runs) ? runs : [runs],
    alignment: o.align || AlignmentType.LEFT, spacing: o.image ? { before: 0, after: o.after ?? 0 } : { before: o.before || 0, after: o.after ?? 100, line: o.line || 288, lineRule: LineRuleType.AUTO },
    numbering: o.puce ? { reference: 'puces', level: 0 } : undefined, keepNext: o.keepNext, pageBreakBefore: o.saut,
    border: o.filet ? { bottom: { style: BorderStyle.SINGLE, size: 12, color: v.or, space: 4 } } : undefined });
  const titre = (texte, o = {}) => p(t(texte, { font: v.titre, size: o.size || 18, bold: true, color: o.color || v.encre }),
    { before: o.saut ? 0 : (o.before ?? 280), after: 120, filet: o.filet ?? true, keepNext: true, saut: o.saut });
  const cellule = (enfants, o = {}) => new TableCell({ children: enfants, width: { size: o.w, type: WidthType.DXA },
    shading: o.fond ? { type: ShadingType.CLEAR, color: 'auto', fill: o.fond } : undefined,
    margins: { top: o.mh ?? 140, bottom: o.mh ?? 140, left: o.ml ?? 200, right: o.ml ?? 200 },
    verticalAlign: o.va || VerticalAlign.CENTER, columnSpan: o.span,
    borders: o.bordures || { top: AUCUNE, left: AUCUNE, right: AUCUNE,
      bottom: { style: BorderStyle.SINGLE, size: 4, color: 'D8D2C2' } } });
  const tableau = (largeurs, lignes) => new Table({ width: { size: LARGEUR, type: WidthType.DXA },
    columnWidths: largeurs, layout: TableLayoutType.FIXED, rows: lignes });

  const image = (fichier, l, h, alt) => new ImageRun({ type: 'png', data: fs.readFileSync(fichier),
    transformation: { width: l, height: h }, altText: { title: alt, description: alt, name: alt } });

  // ---- Bandeau ----
  const bandeau = p(image(path.join(ICI, 'visuels', `bandeau_${v.code}.png`), 698, 158,
    'YEBA FORMATIONS — bandeau décoratif : pistes de circuit dorées autour du logo'), { after: 160, image: true });

  // ---- Fiche formation (colonne) ----
  const fiche = (niveau, nom, prix, lignes, livrables, motsCles) => [
    p(t(niveau, { size: 11, bold: true, color: v.or, spacing: 40 }), { after: 40 }),
    p(t(nom, { font: v.titre, size: 22, bold: true, color: 'FFFFFF' }), { after: 60 }),
    p(t('2 jours · 14 heures · présentiel', { size: 12, color: v.doux }), { after: 0 }),
  ];
  const corpsFiche = (lignes, livrables, motsCles, prix) => [
    ...lignes.map(([k, val]) => p([t(k + ' : ', { bold: true, color: v.encre }), t(val)], { after: 80 })),
    p(t('Vous repartez avec :', { bold: true, color: v.encre }), { before: 80, after: 40 }),
    ...livrables.map((l) => p(t(l), { puce: true, after: 40 })),
  ];
  const prixFiche = (prix) => [p([t(prix, { font: v.titre, size: 28, bold: true, color: v.encre }), t('  par personne, déjeuner inclus', { size: 12 })], { after: 0 })];
  const demi = (LARGEUR - 240) / 2;
  const fiches = tableau([demi, 240, demi], [
    new TableRow({ children: [
      cellule(fiche('NIVEAU 1 · INTERMÉDIAIRE', 'IA PILOTE'), { w: demi, fond: v.sombre, bordures: SANS_BORDURE }),
      cellule([p(t(''))], { w: 240, bordures: SANS_BORDURE }),
      cellule(fiche('NIVEAU 2 · AVANCÉ', 'IA ARCHITECTE'), { w: demi, fond: v.nuit, bordures: SANS_BORDURE }),
    ] }),
    new TableRow({ children: [
      cellule(corpsFiche(
        [['Pour qui', 'salariés, dirigeants, indépendants qui utilisent l\'IA sans méthode'],
         ['Prérequis', 'utiliser un ordinateur et une messagerie']],
        ['20 prompts prêts pour votre métier', 'la charte d\'usage IA de votre entreprise', 'une attestation « maîtrise de l\'IA »'],
        'Prompts · Fiabilité · RGPD · IA Act', PRIX.n1Inter), { w: demi, fond: v.clair, va: VerticalAlign.TOP, bordures: SANS_BORDURE }),
      cellule([p(t(''))], { w: 240, bordures: SANS_BORDURE }),
      cellule(corpsFiche(
        [['Pour qui', 'utilisateurs réguliers qui veulent automatiser'],
         ['Prérequis', 'avoir suivi IA PILOTE ou réussir le test de positionnement']],
        ['un workflow automatisé, construit sur votre cas réel', 'votre registre des usages IA', 'votre matrice des risques IA Act'],
        'Assistants · Automatisation · Registre · Risques', PRIX.n2Inter), { w: demi, fond: v.clair, va: VerticalAlign.TOP, bordures: SANS_BORDURE }),
    ] }),
    new TableRow({ cantSplit: true, children: [
      cellule(prixFiche(PRIX.n1Inter), { w: demi, fond: v.clair, mh: 60, bordures: SANS_BORDURE }),
      cellule([p(t(''))], { w: 240, bordures: SANS_BORDURE }),
      cellule(prixFiche(PRIX.n2Inter), { w: demi, fond: v.clair, mh: 60, bordures: SANS_BORDURE }),
    ] }),
  ]);

  // ---- Tableau des tarifs ----
  const L = [4666, 2900, 2900];
  const entete = new TableRow({ tableHeader: true, children: [
    cellule([p(t('Formule', { bold: true, color: 'FFFFFF' }), { after: 0 })], { w: L[0], fond: v.sombre }),
    cellule([p(t('IA PILOTE', { bold: true, color: 'FFFFFF' }), { after: 0, align: AlignmentType.CENTER })], { w: L[1], fond: v.sombre }),
    cellule([p(t('IA ARCHITECTE', { bold: true, color: 'FFFFFF' }), { after: 0, align: AlignmentType.CENTER })], { w: L[2], fond: v.sombre }),
  ] });
  const ligne = (libelle, detail, a, b, fond) => new TableRow({ cantSplit: true, children: [
    cellule([p(t(libelle, { bold: true, color: v.encre }), { after: 20 }), p(t(detail, { size: 11, color: '444444' }), { after: 0 })], { w: L[0], fond, mh: 90 }),
    cellule([p(t(a, { font: v.titre, size: 16, bold: true, color: v.encre }), { after: 0, align: AlignmentType.CENTER })], { w: L[1], fond, mh: 90 }),
    cellule([p(t(b, { font: v.titre, size: 16, bold: true, color: v.encre }), { after: 0, align: AlignmentType.CENTER })], { w: L[2], fond, mh: 90 }),
  ] });
  const ligneFusion = (libelle, detail, runs, fond) => new TableRow({ cantSplit: true, children: [
    cellule([p(t(libelle, { bold: true, color: v.encre }), { after: 20 }), p(t(detail, { size: 11, color: '444444' }), { after: 0 })], { w: L[0], fond, mh: 90 }),
    cellule([p(runs, { after: 0, align: AlignmentType.CENTER })], { w: L[1] + L[2], span: 2, fond, mh: 90 }),
  ] });
  const tarifs = tableau(L, [
    entete,
    ligne('Inter-entreprises', 'par personne · en hôtel · déjeuner et pauses inclus', PRIX.n1Inter, PRIX.n2Inter),
    ligne('Intra-entreprise', 'groupe jusqu\'à 8 personnes · dans vos locaux', PRIX.n1Intra, PRIX.n2Intra, v.clair),
    ligne('Personne supplémentaire', 'en intra, de 9 à 12 personnes', PRIX.n1Supp, PRIX.n2Supp),
    ligneFusion('Duo IA PILOTE + IA ARCHITECTE', '4 jours · inter-entreprises · par personne',
      [t(PRIX.duo, { font: v.titre, size: 16, bold: true, color: v.encre }), t('   au lieu de ', { size: 11, color: '444444' }),
       t(PRIX.duoBarre, { size: 11, color: '444444', strike: true })], v.clair),
    ligneFusion('3e inscrit de la même entreprise', 'et suivants, sur la même session inter',
      [t('− 15 %', { font: v.titre, size: 16, bold: true, color: v.encre })]),
  ]);

  // ---- Encadré (fond coloré, filet or à gauche) ----
  const encadre = (enfants, fond, couleurFilet) => tableau([LARGEUR], [new TableRow({ cantSplit: true, children: [
    cellule(enfants, { w: LARGEUR, fond, ml: 280, mh: 200, bordures: { top: AUCUNE, bottom: AUCUNE, right: AUCUNE,
      left: { style: BorderStyle.SINGLE, size: 36, color: couleurFilet } } })] })]);

  // ---- Financements ----
  const F = [3000, 3700, 3766];
  const fin = (a, b, c, fond) => new TableRow({ cantSplit: true, children: [
    cellule([p(t(a, { bold: true, color: v.encre, size: 11 }), { after: 0 })], { w: F[0], fond, mh: 90 }),
    cellule([p(t(b, { size: 11 }), { after: 0 })], { w: F[1], fond, mh: 90 }),
    cellule([p(t(c, { size: 11 }), { after: 0 })], { w: F[2], fond, mh: 90 })] });
  const financements = tableau(F, [
    new TableRow({ tableHeader: true, children: ['Vous êtes', 'Qui peut financer', 'Ce que nous faisons'].map((h, i) =>
      cellule([p(t(h, { bold: true, color: 'FFFFFF' }), { after: 0 })], { w: F[i], fond: v.sombre })) }),
    fin('Employeur', 'Votre OPCO (plan de développement des compétences), selon ses critères', 'Devis, programme, dossier de prise en charge prêts à déposer'),
    fin('Dirigeant non salarié, indépendant', 'Votre fonds d\'assurance formation : AGEFICE, FIF PL, CMA…', 'Dossier monté avec vous, dépôt 2 mois avant', v.clair),
    fin('Demandeur d\'emploi', 'France Travail (AIF), Région Réunion', 'Devis transmis à votre conseiller'),
    fin('Personne en situation de handicap', 'Agefiph (surcoûts d\'adaptation)', 'Référent handicap dédié', v.clair),
  ]);

  // ---- QR + contact ----
  const Q = [2700, LARGEUR - 2700];
  const blocQR = tableau(Q, [new TableRow({ cantSplit: true, children: [
    cellule([p(image(path.join(ICI, 'visuels', `qr_${v.code}.png`), 150, 150,
      `QR code vers ${CONTACT.url} : grille tarifaire et dates de sessions`), { after: 0, align: AlignmentType.CENTER, image: true })],
      { w: Q[0], fond: 'FFFFFF', bordures: SANS_BORDURE }),
    cellule([
      p(t('Scannez : sessions, inscription, grille à jour', { font: v.titre, size: 15, bold: true, color: 'FFFFFF' }), { after: 120 }),
      p(t(CONTACT.url, { size: 13, bold: true, color: v.or }), { after: 120 }),
      p(t(`${CONTACT.tel}  ·  ${CONTACT.mail}`, { size: 12, color: 'FFFFFF' }), { after: 40 }),
      p(t(CONTACT.adr, { size: 12, color: v.doux }), { after: 0 }),
    ], { w: Q[1], fond: v.sombre, ml: 320, bordures: SANS_BORDURE }),
  ] })]);

  const enfants = [
    bandeau,
    p(t('Formations Intelligence Artificielle', { font: v.titre, size: 26, bold: true, color: v.encre }), { after: 40 }),
    p(t('Grille tarifaire 2026  ·  Inter-entreprises et intra-entreprise', { size: 14, color: '333333' }), { after: 120 }),
    p([t('Maîtriser l\'IA', { bold: true, color: v.encre }), t('   ·   ', { color: v.encre }),
       t('Protéger vos données', { bold: true, color: v.encre }), t('   ·   ', { color: v.encre }),
       t('Répondre à l\'IA Act', { bold: true, color: v.encre })], { after: 200 }),
    fiches,
    p(t(''), { after: 60 }),
    encadre([
      p(t('IA Act — article 4 : la maîtrise de l\'IA', { font: v.titre, size: 15, bold: true, color: v.or }), { after: 80 }),
      p(t('Les entreprises qui utilisent l\'IA doivent prendre des mesures pour développer la maîtrise de l\'IA de leur personnel (règlement européen sur l\'IA, art. 4 modifié en 2026).',
        { color: 'FFFFFF' }), { after: 60 }),
      p(t('Nos formations et leur attestation constituent une mesure concrète et traçable.', { bold: true, color: 'FFFFFF' }), { after: 0 }),
    ], v.sombre, v.or),

    titre('Tarifs 2026', { saut: true }),
    tarifs,
    p(t('Dès 5 salariés à former, l\'intra-entreprise devient plus avantageux pour vous.', { bold: true, color: v.encre }), { before: 140, after: 0 }),

    titre('Inclus en inter-entreprises', { before: 240 }),
    tableau([LARGEUR / 2, LARGEUR / 2], [new TableRow({ cantSplit: true, children: [
      cellule(['Salle de formation en hôtel à La Réunion', 'Déjeuner, collation et pauses (thé, café, jus)',
        'Supports remis à chacun (16 points sur demande)'].map((x) => p(t(x), { puce: true, after: 40 })),
        { w: LARGEUR / 2, ml: 0, mh: 40, va: VerticalAlign.TOP, bordures: SANS_BORDURE }),
      cellule(['Livrables personnalisés et attestation', 'Une question par courriel dans le mois qui suit'].map((x) => p(t(x), { puce: true, after: 40 })),
        { w: LARGEUR / 2, ml: 0, mh: 40, va: VerticalAlign.TOP, bordures: SANS_BORDURE }),
    ] })]),

    p(t(''), { after: 200 }),
    encadre([
      p(t('Votre retour sur investissement', { font: v.titre, size: 15, bold: true, color: v.encre }), { after: 80 }),
      p([t('Exemple : ', { bold: true }), t('1 heure gagnée par semaine × 46 semaines × 35 € de coût horaire chargé = '),
         t('1 610 € par an et par salarié.', { bold: true, color: v.encre })], { after: 40 }),
      p(t('IA PILOTE est remboursée en moins de 6 mois. Calcul indicatif : à refaire avec vos chiffres.', { size: 11, color: '444444' }), { after: 0 }),
    ], v.clair, v.or),
    p(t(''), { after: 120 }),
    titre('Financer votre formation', { saut: true }),
    financements,
    p(t('La prise en charge et son montant sont décidés par votre financeur, selon ses propres critères. Obtenez son accord écrit avant le démarrage.',
      { size: 11, italics: true, color: '444444' }), { before: 100, after: 200 }),

    titre('Accessibilité'),
    p(t('Formations accessibles aux personnes en situation de handicap. Diaporamas en gros caractères et contrastes renforcés, supports en 16 points sur demande. Signalez votre besoin d\'aménagement au référent handicap, Aurélien LUMEKA : aucun justificatif médical n\'est demandé.'), { after: 200 }),

    blocQR,

    titre('Conditions', { size: 14 }),
    ...['Tarifs nets en euros. TVA non applicable, article 293 B du CGI. Tarifs valables jusqu\'au 31/12/2026.',
      'Inscription au plus tard 15 jours ouvrés avant la session. Session confirmée à partir de 4 inscrits, sinon report ou remboursement intégral.',
      'Intra : déplacement hors Saint-Denis et salle extérieure sur devis. Conditions générales de vente remises avec le devis.'].map((x) => p(t(x, { size: 11 }), { puce: true, after: 40 })),
  ];

  const pied = new Footer({ children: [
    p(t(`YEBA FORMATIONS · ${CONTACT.adr} · SIRET 814 622 262 00032`, { size: 9, color: '555555' }), { align: AlignmentType.CENTER, after: 0 }),
    p(t('Déclaration d\'activité n° 04973676397 (cet enregistrement ne vaut pas agrément de l\'État) · Certification Qualiopi n° 25FOR02027.1, délivrée au titre de la catégorie : actions de formation',
      { size: 9, color: '555555' }), { align: AlignmentType.CENTER, after: 0 }),
    new Paragraph({ alignment: AlignmentType.CENTER, children: [
      new TextRun({ children: ['Page ', PageNumber.CURRENT, ' / ', PageNumber.TOTAL_PAGES], font: CORPS, size: pt(9), color: '555555' })] }),
  ] });

  return new Document({
    creator: 'YEBA FORMATIONS', title: `Grille tarifaire 2026 — Formations IA (${v.nom})`,
    description: 'Grille tarifaire des formations Intelligence Artificielle IA PILOTE et IA ARCHITECTE',
    styles: { default: { document: { run: { font: CORPS, size: pt(12) } } } },
    numbering: { config: [{ reference: 'puces', levels: [{ level: 0, format: LevelFormat.BULLET, text: '■',
      alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 260 } }, run: { color: v.encre, size: pt(8) } } }] }] },
    sections: [{ properties: { page: { size: { width: 11906, height: 16838 },
      margin: { top: 680, bottom: 820, left: 720, right: 720, footer: 360 } } },
      footers: { default: pied }, children: enfants }],
  });
}

(async () => {
  for (const v of VERSIONS) {
    const buf = await Packer.toBuffer(construire(v));
    const f = path.join(SORTIE, `${v.fichier}.docx`);
    fs.writeFileSync(f, buf);
    console.log('→', path.basename(f));
  }
})();
