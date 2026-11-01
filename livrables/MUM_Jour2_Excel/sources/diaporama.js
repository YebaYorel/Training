/* Diaporama projeté — MUM · Excel · demi-journée (8h00 – 12h00).
   Conçu pour la projection : texte ≥ 24 pt (mots-clés 32 à 60 pt), contraste ≥ 7:1 sur les textes principaux,
   exemples Excel dessinés à l'écran, explication complète du formateur dans les notes de chaque diapositive.
   node diaporama.js <fichier.pptx> */
const path = require('path');
const NM = process.env.NODE_MODULES_DIR || '/tmp/claude-0/-home-user-Training/ae3dbc59-f9ec-5b68-9c3b-51565a7e3450/scratchpad/web/';
const PptxGenJS = require('module').createRequire(NM + 'x.js')('pptxgenjs');
const fs = require('fs');
const RACINE = path.resolve(__dirname, '../../..');
const LOGO = 'data:image/png;base64,' + fs.readFileSync(RACINE + '/web/pilotage/src/logo_yeba.png').toString('base64');

const MARINE = '1B3A6B', OR = 'C9AB4C', NOIR = '121212', BLANC = 'FFFFFF', CLAIR = 'EEF2F8', GRIS = '4A5868';
const VERT = '1E7B3A', ROUGE = 'B3261E', JAUNE = 'FFF2B3', VERT_C = 'D7EFDD', ROUGE_C = 'F9DEDC';
const FT = 'Montserrat', FB = 'Inter';
const W = 13.33, H = 7.5;

const pptx = new PptxGenJS();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'YEBA FORMATIONS'; pptx.company = 'YEBA FORMATIONS'; pptx.title = 'Excel : piloter son activité par les chiffres';
let n = 0;

// ------------------------------------------------------------------ gabarits
function base(titre, opts = {}) {
  const s = pptx.addSlide(); n++;
  s.background = { color: BLANC };
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: W, h: 1.3, fill: { color: MARINE }, line: { color: MARINE } });
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 1.3, w: W, h: 0.08, fill: { color: OR }, line: { color: OR } });
  s.addText(titre, { x: 0.5, y: 0.1, w: 10.6, h: 1.1, fontFace: FT, fontSize: opts.taille || 40, bold: true, color: BLANC, valign: 'middle', fit: 'shrink' });
  s.addImage({ data: LOGO, x: 11.75, y: 0.17, w: 1.12, h: 0.95 });
  if (opts.repere) s.addText(opts.repere, { x: 9.0, y: 0.1, w: 2.6, h: 1.1, fontFace: FB, fontSize: 24, bold: true, color: OR, align: 'right', valign: 'middle' });
  s.addText(`YEBA FORMATIONS · MUM · Excel`, { x: 0.5, y: 6.95, w: 7, h: 0.45, fontFace: FB, fontSize: 16, color: GRIS });
  s.addText(String(n), { x: 11.8, y: 6.95, w: 1, h: 0.45, fontFace: FB, fontSize: 16, color: GRIS, align: 'right' });
  return s;
}
function plein(fond = MARINE) {
  const s = pptx.addSlide(); n++;
  s.background = { color: fond };
  return s;
}
const note = (s, t) => s.addNotes(t);
function carte(s, x, y, w, h, grand, petit, fond = CLAIR, couleur = MARINE, tg = 40, tp = 24) {
  s.addShape(pptx.ShapeType.roundRect, { x, y, w, h, fill: { color: fond }, line: { color: fond }, rectRadius: 0.12 });
  if (petit) {
    s.addText(grand, { x: x + 0.15, y: y + 0.1, w: w - 0.3, h: h * 0.58, fontFace: FT, fontSize: tg, bold: true, color: couleur, align: 'center', valign: 'bottom', fit: 'shrink' });
    s.addText(petit, { x: x + 0.15, y: y + h * 0.6, w: w - 0.3, h: h * 0.36, fontFace: FB, fontSize: tp, color: couleur === BLANC ? BLANC : NOIR, align: 'center', valign: 'top', fit: 'shrink' });
  } else {
    s.addText(grand, { x: x + 0.15, y, w: w - 0.3, h, fontFace: FT, fontSize: tg, bold: true, color: couleur, align: 'center', valign: 'middle', fit: 'shrink' });
  }
}
function lignes(s, items, y0 = 1.65, hl = 0.92) {
  items.forEach(([v, c], i) => {
    const y = y0 + i * (hl + 0.12);
    s.addShape(pptx.ShapeType.roundRect, { x: 0.6, y, w: 12.1, h: hl, fill: { color: i % 2 ? CLAIR : MARINE }, line: { color: i % 2 ? CLAIR : MARINE }, rectRadius: 0.08 });
    s.addText(v, { x: 0.9, y, w: 4.6, h: hl, fontFace: FT, fontSize: 34, bold: true, color: i % 2 ? MARINE : OR, valign: 'middle' });
    s.addText(c, { x: 5.6, y, w: 6.9, h: hl, fontFace: FB, fontSize: 32, bold: true, color: i % 2 ? NOIR : BLANC, valign: 'middle' });
  });
}
function rond(s, x, y, d, texte, fond = OR, couleur = NOIR, t = 32) {
  s.addShape(pptx.ShapeType.ellipse, { x, y, w: d, h: d, fill: { color: fond }, line: { color: fond } });
  s.addText(texte, { x, y, w: d, h: d, fontFace: FT, fontSize: t, bold: true, color: couleur, align: 'center', valign: 'middle' });
}
function fleche(s, x, y, w, couleur = OR) {
  s.addShape(pptx.ShapeType.rightArrow, { x, y, w, h: 0.55, fill: { color: couleur }, line: { color: couleur } });
}
/* grille façon Excel : cols = lettres, lignes = [{num, cells:[...]}], marque = {r, c, fond} */
function grille(s, x, y, cols, lignes, opts = {}) {
  const t = opts.taille || 24, hl = opts.h || 0.62;
  const lg = opts.largeurs || cols.map(() => 2.2);
  const entete = [{ text: '', options: { fill: { color: 'D9DEE6' } } }].concat(cols.map((c) => ({ text: c, options: { bold: true, align: 'center', fill: { color: 'D9DEE6' }, color: NOIR } })));
  const rows = [entete].concat(lignes.map((l, i) => [{ text: String(l.num), options: { bold: true, align: 'center', fill: { color: 'D9DEE6' }, color: NOIR } }]
    .concat(l.cells.map((v, j) => {
      const o = typeof v === 'object' && v !== null ? v : { t: v };
      const mk = (opts.marques || []).find((m) => m.r === i && m.c === j);
      return { text: o.t == null ? '' : String(o.t), options: { align: o.a || (typeof o.t === 'number' || /^[-\d\s,]+( €)?$/.test(String(o.t)) ? 'right' : 'left'),
        bold: !!(o.b || mk), color: o.col || NOIR, fill: { color: (mk && mk.fond) || o.fond || BLANC } } };
    }))));
  s.addTable(rows, { x, y, colW: [0.7].concat(lg), rowH: hl, fontFace: FB, fontSize: t, border: { type: 'solid', pt: 1, color: '9AA5B1' }, valign: 'middle', margin: 0.06 });
}
function barre(s, x, y, w, ref, formule, t = 32) {
  s.addShape(pptx.ShapeType.rect, { x, y, w, h: 0.85, fill: { color: BLANC }, line: { color: GRIS, width: 1.5 } });
  s.addText(ref, { x, y, w: 1.3, h: 0.85, fontFace: FB, fontSize: 24, bold: true, color: NOIR, align: 'center', valign: 'middle' });
  s.addShape(pptx.ShapeType.line, { x: x + 1.3, y, w: 0, h: 0.85, line: { color: GRIS, width: 1.5 } });
  s.addText('fx', { x: x + 1.3, y, w: 0.8, h: 0.85, fontFace: FB, fontSize: 24, italic: true, color: GRIS, align: 'center', valign: 'middle' });
  s.addText(formule, { x: x + 2.1, y, w: w - 2.2, h: 0.85, fontFace: 'Consolas', fontSize: t, bold: true, color: MARINE, valign: 'middle', fit: 'shrink' });
}
function bloc(numero, titre, horaire, notes) {
  const s = plein(MARINE);
  s.addText(String(numero), { x: 0.8, y: 1.6, w: 3, h: 3.6, fontFace: FT, fontSize: 200, bold: true, color: OR, valign: 'middle' });
  s.addText(titre, { x: 3.9, y: 2.3, w: 8.8, h: 1.6, fontFace: FT, fontSize: 60, bold: true, color: BLANC, valign: 'middle', fit: 'shrink' });
  s.addText(horaire, { x: 3.9, y: 3.9, w: 8.8, h: 0.9, fontFace: FB, fontSize: 32, color: OR, valign: 'middle' });
  s.addImage({ data: LOGO, x: 11.75, y: 6.2, w: 1.12, h: 0.95 });
  note(s, notes);
}
function mission(num, titre, duree, modalite, etapes, feuille, but, notes) {
  const s = base(`Mission ${num} · ${titre}`, { taille: 38 });
  carte(s, 0.5, 1.75, 3.6, 1.5, duree, modalite, OR, NOIR, 44, 24);
  carte(s, 0.5, 3.45, 3.6, 1.5, but, 'pour réussir', VERT_C, VERT, 34, 22);
  s.addText(`Feuille « ${feuille} »`, { x: 0.5, y: 5.2, w: 3.6, h: 1.0, fontFace: FB, fontSize: 24, bold: true, color: MARINE, align: 'center', valign: 'middle', fit: 'shrink' });
  etapes.forEach((e, i) => {
    rond(s, 4.6, 1.8 + i * 1.22, 0.95, String(i + 1));
    s.addText(e, { x: 5.75, y: 1.8 + i * 1.22, w: 7.1, h: 0.95, fontFace: FB, fontSize: 30, bold: true, color: NOIR, valign: 'middle', fit: 'shrink' });
  });
  note(s, notes);
}
function vraiFaux(num, affirmation, notes) {
  const s = base(`Le juste chiffre · ${num} / 4`, { repere: '10h15' });
  s.addText(affirmation, { x: 0.8, y: 1.9, w: 11.7, h: 2.6, fontFace: FT, fontSize: 44, bold: true, color: MARINE, align: 'center', valign: 'middle', fit: 'shrink' });
  carte(s, 1.5, 4.8, 4.6, 1.8, 'VRAI', 'côté fenêtre', VERT_C, VERT, 48, 24);
  carte(s, 7.2, 4.8, 4.6, 1.8, 'FAUX', 'côté porte', ROUGE_C, ROUGE, 48, 24);
  note(s, notes);
}

// ================================================================== OUVERTURE
let s = plein(MARINE);
s.addShape(pptx.ShapeType.rect, { x: 0, y: 5.35, w: W, h: 0.1, fill: { color: OR }, line: { color: OR } });
s.addText('EXCEL', { x: 0.8, y: 0.9, w: 10, h: 1.6, fontFace: FT, fontSize: 96, bold: true, color: OR });
s.addText('Piloter son activité\npar les chiffres', { x: 0.8, y: 2.5, w: 10.5, h: 2.4, fontFace: FT, fontSize: 52, bold: true, color: BLANC, valign: 'top' });
s.addText('Titre professionnel MUM · Bureautique · 8h00 – 12h00', { x: 0.8, y: 5.6, w: 11, h: 0.7, fontFace: FB, fontSize: 28, color: BLANC });
s.addText('YEBA FORMATIONS', { x: 0.8, y: 6.4, w: 8, h: 0.6, fontFace: FT, fontSize: 24, bold: true, color: OR });
s.addImage({ data: LOGO, x: 10.6, y: 0.7, w: 2.1, h: 1.79 });
note(s, "Accueil à la porte, chacun s'installe devant un poste avec le classeur de missions ouvert. Je présente la matinée en une phrase : « Ce matin, vous apprenez à répondre à votre direction avec des chiffres justes, en quelques secondes. »");

s = plein(MARINE);
s.addText('“', { x: 0.6, y: 0.3, w: 2, h: 2, fontFace: 'Georgia', fontSize: 200, color: OR });
s.addText('Lorsque vous pouvez mesurer ce dont vous parlez et l\'exprimer en chiffres, vous en savez quelque chose.', { x: 1.3, y: 1.5, w: 10.8, h: 3.2, fontFace: FT, fontSize: 44, bold: true, color: BLANC, valign: 'middle', fit: 'shrink' });
s.addText('Lord Kelvin, physicien', { x: 1.3, y: 4.85, w: 10.8, h: 0.7, fontFace: FB, fontSize: 32, bold: true, color: OR });
s.addText('Conférence « Electrical Units of Measurement », Londres, 3 mai 1883 · traduction', { x: 1.3, y: 5.55, w: 10.8, h: 0.6, fontFace: FB, fontSize: 22, color: BLANC });
note(s, "Je lis la citation lentement. Lord Kelvin (William Thomson), physicien, l'a prononcée en 1883 devant l'Institution of Civil Engineers de Londres (recueil Popular Lectures and Addresses, vol. 1, 1889). Je fais le lien : « En magasin, c'est pareil. Dire \"le stock va bien\", c'est une impression. Dire \"le stock vaut 2 838,80 € et 5 produits sont sous le seuil\", c'est savoir. Ce matin, on passe de l'impression au chiffre. » Question au groupe : « Dans votre magasin, quel chiffre regardez-vous chaque matin ? »");

s = base("L'appel de 8h05", { repere: '8h05' });
carte(s, 0.6, 1.8, 7.6, 1.9, '« Combien vaut ton stock ? »', null, CLAIR, MARINE, 36);
carte(s, 0.6, 3.95, 7.6, 1.9, '« Que dois-tu recommander ? »', null, CLAIR, MARINE, 36);
rond(s, 9.2, 2.2, 3.2, '2 min', OR, NOIR, 60);
s.addText('Sur l\'ardoise', { x: 8.7, y: 5.55, w: 4.2, h: 0.7, fontFace: FB, fontSize: 28, bold: true, color: MARINE, align: 'center' });
note(s, "Je joue la directrice régionale au téléphone. Chacun répond seul sur l'ardoise en 2 minutes à partir de la liste papier des 12 produits. On ne corrige pas : on garde les ardoises, on y revient à 11h50 avec le classeur. Le but : faire sentir qu'à la main, c'est long et incertain.");

s = base('Votre matinée');
[['8h00', 'Ouverture'], ['8h15', '1 · Saisir'], ['8h45', '2 · Calculer'], ['10h00', 'Pause'], ['10h15', '3 · Trier et décider'], ['11h15', '4 · Corriger'], ['11h30', 'Coffre · Quiz · Bilan']].forEach(([h, t], i) => {
  const y = 1.65 + i * 0.73, pause = t === 'Pause';
  s.addShape(pptx.ShapeType.roundRect, { x: 1.2, y, w: 10.9, h: 0.62, fill: { color: pause ? OR : (i % 2 ? BLANC : CLAIR) }, line: { color: pause ? OR : CLAIR }, rectRadius: 0.08 });
  s.addText(h, { x: 1.4, y, w: 2.2, h: 0.62, fontFace: FT, fontSize: 28, bold: true, color: pause ? NOIR : MARINE, valign: 'middle' });
  s.addText(t, { x: 3.7, y, w: 8.2, h: 0.62, fontFace: FB, fontSize: 28, bold: true, color: NOIR, valign: 'middle' });
});
note(s, "La matinée en 4 blocs, une pause de 15 minutes à 10h00, fin à 12h00. Chaque bloc se termine par une mission dans le classeur. Je précise : la pause est tenue à la minute.");

s = base('Ce matin, vous saurez');
lignes(s, [['SAISIR', 'un tableau fiable'], ['CALCULER', 'total · moyenne'], ['TRIER', 'filtrer · décider'], ['CORRIGER', 'les erreurs'], ['RÉPONDRE', 'à la direction']]);
note(s, "Les 5 objectifs de la matinée, un par verbe. Ils correspondent aux 5 critères de la grille d'évaluation. Je montre que le dernier, RÉPONDRE, est le vrai métier du manager : les 4 premiers servent à ça.");

s = base('Votre rôle ce matin');
carte(s, 0.6, 1.8, 3.8, 2.3, 'Manager', 'RUN\'ATTITUDE', MARINE, BLANC, 40, 26);
carte(s, 4.75, 1.8, 3.8, 2.3, 'Chaudron', 'votre boutique', CLAIR, MARINE, 40, 26);
carte(s, 8.9, 1.8, 3.8, 2.3, 'Direction', 'régionale', CLAIR, MARINE, 40, 26);
carte(s, 0.6, 4.4, 12.1, 1.9, '12 produits · 4 missions · 1 coffre', null, OR, NOIR, 40);
note(s, "Fil rouge : vous êtes manager de la boutique RUN'ATTITUDE du Chaudron (enseigne fictive). Votre direction régionale vous confie 4 missions sur le stock. À la fin, les résultats des missions ouvrent le coffre de l'escape game.");

s = base('Le classeur de missions');
s.addShape(pptx.ShapeType.rect, { x: 0.8, y: 1.9, w: 3.4, h: 1.4, fill: { color: JAUNE }, line: { color: GRIS, width: 1.5 } });
s.addText('Case jaune', { x: 0.8, y: 1.9, w: 3.4, h: 1.4, fontFace: FT, fontSize: 32, bold: true, color: NOIR, align: 'center', valign: 'middle' });
s.addText('J\'écris ici, et seulement ici', { x: 4.5, y: 1.9, w: 8.2, h: 1.4, fontFace: FB, fontSize: 32, bold: true, color: NOIR, valign: 'middle' });
carte(s, 0.8, 3.55, 1.6, 1.3, '✔', null, VERT_C, VERT, 60);
s.addText('Juste', { x: 2.6, y: 3.55, w: 3.2, h: 1.3, fontFace: FB, fontSize: 32, bold: true, color: VERT, valign: 'middle' });
carte(s, 6.4, 3.55, 1.6, 1.3, '✘', null, ROUGE_C, ROUGE, 60);
s.addText('À revoir', { x: 8.2, y: 3.55, w: 4.5, h: 1.3, fontFace: FB, fontSize: 32, bold: true, color: ROUGE, valign: 'middle' });
carte(s, 0.8, 5.1, 11.9, 1.4, 'Feuille « Tableau de bord » = votre score', null, MARINE, BLANC, 32);
note(s, "Je montre le classeur à l'écran. Règle unique : on écrit dans les cases jaunes. La colonne Contrôle passe au vert ✔ quand c'est juste, au rouge ✘ sinon. La feuille Tableau de bord compte les ✔ : chacun voit sa progression, et moi je vois qui a besoin d'aide. Le classeur fonctionne sans internet et sans macro, sous Excel comme sous LibreOffice.");

// ================================================================== BLOC 1
bloc(1, 'Saisir', '8h15 – 8h45', "Bloc 1 : 10 minutes de démonstration, puis 20 minutes de Mission 1.");

s = base('Où est la cellule B7 ?', { repere: 'Bloc 1' });
grille(s, 0.6, 1.7, ['A', 'B', 'C', 'D'], [4, 5, 6, 7, 8].map((r) => ({ num: r, cells: ['', '', '', ''] })), { largeurs: [1.4, 1.4, 1.4, 1.4], h: 0.75, marques: [{ r: 3, c: 1, fond: OR }] });
carte(s, 7.3, 1.8, 5.4, 1.3, 'Colonne B', 'une lettre', CLAIR, MARINE, 36, 22);
s.addText('+', { x: 7.3, y: 3.15, w: 5.4, h: 0.6, fontFace: FT, fontSize: 40, bold: true, color: MARINE, align: 'center', valign: 'middle' });
carte(s, 7.3, 3.8, 5.4, 1.3, 'Ligne 7', 'un chiffre', CLAIR, MARINE, 36, 22);
carte(s, 7.3, 5.35, 5.4, 1.2, '= B7', null, OR, NOIR, 44);
note(s, "Une cellule a une adresse, comme une maison : la lettre de la colonne, puis le numéro de la ligne. Jeu de 2 minutes : je dis une adresse (B7, D4, A8), les stagiaires cliquent dessus dans Excel et lisent la Zone Nom (en haut à gauche) pour vérifier.");

s = base('Texte ou nombre ?', { repere: 'Bloc 1' });
s.addText('Nombre', { x: 0.6, y: 1.6, w: 5.8, h: 0.7, fontFace: FT, fontSize: 32, bold: true, color: VERT });
grille(s, 0.6, 2.35, ['C'], [{ num: 6, cells: [{ t: 24, a: 'right' }] }, { num: 7, cells: [{ t: 35, a: 'right' }] }, { num: 8, cells: [{ t: '=SOMME → 59', a: 'right', b: true, fond: VERT_C, col: VERT }] }], { largeurs: [4.6], h: 0.7, taille: 28 });
s.addText('Texte', { x: 6.9, y: 1.6, w: 5.8, h: 0.7, fontFace: FT, fontSize: 32, bold: true, color: ROUGE });
grille(s, 6.9, 2.35, ['C'], [{ num: 6, cells: [{ t: 24, a: 'right' }] }, { num: 7, cells: [{ t: '35␣', a: 'left' }] }, { num: 8, cells: [{ t: '=SOMME → 24', a: 'right', b: true, fond: ROUGE_C, col: ROUGE }] }], { largeurs: [4.6], h: 0.7, taille: 28 });
carte(s, 0.6, 5.45, 12.1, 1.2, 'À gauche = texte = pas calculé', null, MARINE, BLANC, 34);
note(s, "Démonstration en direct. Un nombre s'aligne à droite. Si on tape « 35 » suivi d'un espace (ou précédé d'une apostrophe), Excel le prend pour du texte : il s'aligne à gauche et SOMME l'ignore. Résultat : 24 au lieu de 59, et la direction reçoit un chiffre faux sans que personne ne s'en aperçoive. C'est exactement le piège de la Mission 1 : 3 quantités sont dans ce cas.");

s = base('Un tableau lisible', { repere: 'Bloc 1' });
s.addText('Avant', { x: 0.6, y: 1.55, w: 5.9, h: 0.6, fontFace: FT, fontSize: 30, bold: true, color: ROUGE });
grille(s, 0.6, 2.2, ['B', 'C'], [{ num: 5, cells: ['Produit', 'Prix'] }, { num: 6, cells: ['Sac en va', '29'] }, { num: 7, cells: ['Paréo', '####'] }], { largeurs: [2.6, 2.4], h: 0.64, taille: 26 });
s.addText('Après', { x: 6.9, y: 1.55, w: 5.9, h: 0.6, fontFace: FT, fontSize: 30, bold: true, color: VERT });
grille(s, 6.9, 2.2, ['B', 'C'], [{ num: 5, cells: [{ t: 'Produit', b: true, col: BLANC, fond: MARINE }, { t: 'Prix', b: true, col: BLANC, fond: MARINE, a: 'right' }] }, { num: 6, cells: ['Sac en vacoa', '29,00 €'] }, { num: 7, cells: ['Paréo', '22,00 €'] }], { largeurs: [2.6, 2.4], h: 0.64, taille: 26 });
[['En-tête', 'gras · couleur'], ['Largeur', 'double-clic'], ['Format', 'monétaire €']].forEach(([a, b], i) => carte(s, 0.6 + i * 4.1, 5.1, 3.9, 1.5, a, b, CLAIR, MARINE, 30, 24));
note(s, "Trois gestes. 1) En-tête : on sélectionne la ligne de titres, gras et fond de couleur. 2) Largeur : double-clic sur la bordure à droite de la lettre de colonne, la colonne s'ajuste au contenu (plus de nom coupé, plus de ####). 3) Format monétaire : Accueil > Nombre > Monétaire, Excel affiche 29,00 € sans qu'on tape le symbole.");

mission(1, 'Le stock', '20 min', 'seul', ['Mettre l\'en-tête en forme', 'Ajuster les colonnes', 'Format € sur les prix', 'Retaper les 3 nombres « texte »'], 'Mission 1 · Stock', '12 ✔',
  "Individuel, 20 minutes. Je circule. Indice si quelqu'un bloque sur les pièges : « Regardez l'alignement de la colonne Quantité. » Les 3 quantités en texte : Tongs Lagon (35), Savon combava (40), Gourde inox (27). Réussite : 12 ✔ dans la colonne Contrôle.");

// ================================================================== BLOC 2
bloc(2, 'Calculer', '8h45 – 10h00', "Bloc 2 : 25 minutes de démonstration, 45 minutes de Mission 2 en binôme, 5 minutes de mise en commun.");

s = base('Tout commence par =', { repere: 'Bloc 2' });
s.addText('Je tape', { x: 0.6, y: 1.65, w: 12, h: 0.6, fontFace: FT, fontSize: 30, bold: true, color: MARINE });
barre(s, 0.6, 2.3, 12.1, 'E6', '=C6*D6', 40);
s.addText('Excel affiche', { x: 0.6, y: 3.55, w: 12, h: 0.6, fontFace: FT, fontSize: 30, bold: true, color: MARINE });
grille(s, 0.6, 4.2, ['C', 'D', 'E'], [{ num: 6, cells: [24, '19,90 €', { t: '477,60 €', b: true }] }], { largeurs: [2.0, 2.6, 3.0], h: 0.95, taille: 32, marques: [{ r: 0, c: 2, fond: OR }] });
carte(s, 9.3, 4.2, 3.4, 1.9, '*', 'multiplier', OR, NOIR, 60, 26);
note(s, "Toute formule commence par le signe égal. L'étoile * veut dire multiplier (la croix × n'existe pas au clavier). La cellule affiche le résultat, 477,60 € ; la barre de formule, en haut, montre le calcul. Démonstration : je clique sur E6, je tape =, je clique sur C6, je tape *, je clique sur D6, Entrée. Je montre que si je change la quantité, le résultat se met à jour tout seul : c'est tout l'intérêt.");

s = base('La valeur d\'un produit', { repere: 'Bloc 2' });
carte(s, 0.6, 1.8, 3.5, 2.0, '24', 'quantité', CLAIR, MARINE, 60, 24);
s.addText('×', { x: 4.1, y: 1.8, w: 0.9, h: 2.0, fontFace: FT, fontSize: 60, bold: true, color: MARINE, align: 'center', valign: 'middle' });
carte(s, 5.0, 1.8, 3.5, 2.0, '19,90 €', 'prix unitaire', CLAIR, MARINE, 54, 24);
s.addText('=', { x: 8.5, y: 1.8, w: 0.9, h: 2.0, fontFace: FT, fontSize: 60, bold: true, color: MARINE, align: 'center', valign: 'middle' });
carte(s, 9.4, 1.8, 3.4, 2.0, '477,60 €', 'valeur', OR, NOIR, 50, 24);
carte(s, 0.6, 4.35, 12.2, 1.9, 'T-shirt « 974 » : ce que vaut le rayon', null, MARINE, BLANC, 34);
note(s, "La valeur du stock d'un produit, c'est ce qu'il représente en euros sur l'étagère : quantité × prix unitaire. 24 T-shirts à 19,90 € = 477,60 €. C'est ce chiffre que la direction veut connaître, produit par produit, puis au total.");

s = base('La poignée de recopie', { repere: 'Bloc 2' });
grille(s, 0.6, 1.7, ['E'], [{ num: 6, cells: ['=C6*D6'] }, { num: 7, cells: ['=C7*D7'] }, { num: 8, cells: ['=C8*D8'] }, { num: 9, cells: ['=C9*D9'] }], { largeurs: [4.2], h: 0.9, taille: 32, marques: [{ r: 0, c: 0, fond: OR }] });
s.addShape(pptx.ShapeType.downArrow, { x: 5.8, y: 2.6, w: 0.9, h: 2.7, fill: { color: OR }, line: { color: OR } });
carte(s, 7.2, 1.8, 5.5, 1.9, 'Petit carré ■', 'en bas à droite', CLAIR, MARINE, 36, 24);
carte(s, 7.2, 4.0, 5.5, 1.9, 'Je tire vers le bas', 'la formule suit la ligne', MARINE, BLANC, 34, 24);
note(s, "On ne retape pas 12 fois la formule. On sélectionne E6, on attrape le petit carré en bas à droite de la cellule (le curseur devient une croix noire), on tire jusqu'à E17. Excel adapte les adresses : en ligne 7, la formule devient =C7*D7, etc. Astuce : un double-clic sur le petit carré recopie jusqu'en bas du tableau.");

s = base('SOMME : le total', { repere: 'Bloc 2' });
grille(s, 0.6, 1.7, ['E'], [{ num: 6, cells: ['477,60 €'] }, { num: 7, cells: ['116,00 €'] }, { num: '…', cells: [{ t: '…', a: 'center' }] }, { num: 17, cells: ['567,00 €'] }, { num: 19, cells: [{ t: '2 838,80 €', b: true }] }], { largeurs: [4.0], h: 0.78, taille: 30, marques: [{ r: 4, c: 0, fond: OR }] });
barre(s, 5.6, 1.8, 7.1, 'E19', '=SOMME(E6:E17)', 36);
carte(s, 5.6, 3.1, 7.1, 1.5, 'E6:E17', 'de E6 jusqu\'à E17', CLAIR, MARINE, 40, 24);
carte(s, 5.6, 4.85, 7.1, 1.5, '2 838,80 €', 'valeur du stock', OR, NOIR, 44, 24);
note(s, "SOMME additionne une plage. Les deux-points se lisent « jusqu'à » : E6:E17, c'est de E6 jusqu'à E17, soit les 12 produits. Résultat : 2 838,80 €. C'est la première réponse à l'appel de 8h05. Raccourci : Alt + = propose la somme automatiquement.");

s = base('MOYENNE : la valeur type', { repere: 'Bloc 2' });
barre(s, 0.6, 1.8, 12.1, 'D20', '=MOYENNE(D6:D17)', 38);
carte(s, 0.6, 3.1, 5.8, 3.2, '15,27 €', 'prix moyen de nos produits', OR, NOIR, 60, 26);
carte(s, 6.9, 3.1, 5.8, 3.2, '10 · 20 · 60', 'moyenne = 30', CLAIR, MARINE, 50, 28);
note(s, "MOYENNE additionne puis divise par le nombre de valeurs. Exemple de tête : 10 + 20 + 60 = 90, divisé par 3 = 30. Dans notre boutique, le prix moyen des 12 produits est 15,27 €. Utile pour situer un produit : un sac à 29 € est presque deux fois plus cher que la moyenne.");

mission(2, 'La valeur', '45 min', 'en binôme', ['Valeur : =C6*D6', 'Recopier jusqu\'à E17', 'Total : SOMME', 'Prix moyen : MOYENNE'], 'Mission 2 · Valeur', '14 ✔',
  "En binôme : le pilote tient la souris, le copilote dicte et vérifie. Au signal (toutes les 10 minutes), on échange les rôles. Le contrôle exige une formule : un résultat tapé à la main affiche ✘, même s'il est juste. Attendus : total 2 838,80 €, prix moyen 15,27 €. Mise en commun de 5 minutes à 9h55.");

s = plein(OR);
s.addText('Pause', { x: 0, y: 1.8, w: W, h: 2.0, fontFace: FT, fontSize: 110, bold: true, color: NOIR, align: 'center' });
s.addText('10h00 – 10h15', { x: 0, y: 4.0, w: W, h: 1.0, fontFace: FT, fontSize: 48, bold: true, color: NOIR, align: 'center' });
s.addText('Je sauvegarde mon classeur avant de me lever', { x: 0, y: 5.3, w: W, h: 0.8, fontFace: FB, fontSize: 30, bold: true, color: NOIR, align: 'center' });
note(s, "Pause de 15 minutes. Avant de se lever : Ctrl + S. Reprise à 10h15 précises, debout, pour le réveil.");

// ================================================================== RÉVEIL
vraiFaux(1, '=C6*D6 multiplie C6 par D6', "VRAI. L'étoile * est le signe de la multiplication dans Excel.");
vraiFaux(2, '=SOMME(B2:B5) additionne seulement B2 et B5', "FAUX. Les deux-points veulent dire « jusqu'à » : B2, B3, B4 et B5. Pour seulement deux cellules, on écrirait =B2+B5.");
vraiFaux(3, 'Un nombre aligné à gauche est peut-être du texte', "VRAI. Par défaut, un nombre s'aligne à droite. À gauche, c'est souvent un espace ou une apostrophe : SOMME l'ignore.");
vraiFaux(4, 'La moyenne de 10, 20 et 60 est 30', "VRAI. 10 + 20 + 60 = 90 ; 90 ÷ 3 = 30.");

// ================================================================== BLOC 3
bloc(3, 'Trier et décider', '10h25 – 11h15', "Bloc 3 : 15 minutes de démonstration, 35 minutes de Mission 3 en groupe de 3.");

s = base('Trier sans tout casser', { repere: 'Bloc 3' });
s.addText('✘ Une seule colonne', { x: 0.6, y: 1.55, w: 6, h: 0.6, fontFace: FT, fontSize: 28, bold: true, color: ROUGE });
grille(s, 0.6, 2.2, ['B', 'C'], [{ num: 6, cells: ['Bob soleil', { t: 3, fond: ROUGE_C }] }, { num: 7, cells: ['Casquette', { t: 4, fond: ROUGE_C }] }, { num: 8, cells: ['Tongs', { t: 6, fond: ROUGE_C }] }], { largeurs: [3.1, 1.9], h: 0.64, taille: 26 });
s.addText('✔ Tout le tableau', { x: 6.9, y: 1.55, w: 6, h: 0.6, fontFace: FT, fontSize: 28, bold: true, color: VERT });
grille(s, 6.9, 2.2, ['B', 'C'], [{ num: 6, cells: ['Bob soleil', { t: 3, fond: VERT_C }] }, { num: 7, cells: ['Confiture', { t: 4, fond: VERT_C }] }, { num: 8, cells: ['Sac vacoa', { t: 6, fond: VERT_C }] }], { largeurs: [3.1, 1.9], h: 0.64, taille: 26 });
[['Tout sélectionner', 'en-têtes compris'], ['Données', 'Trier'], ['Quantité', 'croissant']].forEach(([a, b], i) => carte(s, 0.6 + i * 4.1, 5.1, 3.9, 1.5, a, b, CLAIR, MARINE, 28, 22));
note(s, "Le piège classique : on sélectionne seulement la colonne Quantité et on trie. Les quantités changent de place, mais pas les noms : la Casquette se retrouve avec 4, les Tongs avec 6. Le tableau est faux et rien ne prévient. La bonne méthode : sélectionner tout le tableau, en-têtes compris (ou cliquer dans le tableau), Données > Trier, colonne Quantité, du plus petit au plus grand.");

s = base('Filtrer : voir l\'essentiel', { repere: 'Bloc 3' });
grille(s, 0.6, 1.7, ['B', 'C ▼'], [{ num: 6, cells: ['Bob soleil', 3] }, { num: 7, cells: ['Confiture goyavier', 4] }, { num: 8, cells: ['Sac en vacoa', 6] }, { num: 9, cells: ['Casquette Piton', 8] }, { num: 10, cells: ['Café Bourbon', 9] }], { largeurs: [4.3, 1.8], h: 0.78, taille: 26 });
carte(s, 7.9, 1.8, 4.8, 1.5, 'Données', 'Filtrer', CLAIR, MARINE, 36, 24);
carte(s, 7.9, 3.5, 4.8, 1.5, '▼ Quantité', 'Inférieur à 10', CLAIR, MARINE, 34, 24);
carte(s, 7.9, 5.2, 4.8, 1.3, '5 produits', null, OR, NOIR, 40);
note(s, "Données > Filtrer : une flèche ▼ apparaît sur chaque en-tête. Flèche de la colonne Quantité > Filtres numériques > Inférieur à… > 10. Excel masque les autres lignes sans les supprimer. On voit tout de suite les 5 produits sous le seuil. Pour tout réafficher : Données > Effacer.");

s = base('SI : Excel décide pour vous', { repere: 'Bloc 3' });
carte(s, 0.6, 2.4, 4.0, 2.2, 'C6 < 10 ?', 'la question', MARINE, BLANC, 44, 24);
fleche(s, 4.75, 2.65, 1.3, VERT); fleche(s, 4.75, 3.95, 1.3, ROUGE);
carte(s, 6.2, 1.75, 6.5, 1.6, 'Oui → « Oui »', 'à recommander', VERT_C, VERT, 38, 24);
carte(s, 6.2, 3.65, 6.5, 1.6, 'Non → « Non »', 'stock suffisant', ROUGE_C, ROUGE, 38, 24);
barre(s, 0.6, 5.6, 12.1, 'F6', '=SI(C6<10;"Oui";"Non")', 34);
note(s, "La fonction SI pose une question et donne une réponse si c'est vrai, une autre si c'est faux. =SI(C6<10;\"Oui\";\"Non\") : si la quantité est inférieure à 10, Excel écrit Oui, sinon Non. Les points-virgules séparent les 3 parties ; le texte s'écrit entre guillemets. On recopie avec la poignée : Excel décide ligne par ligne. Sur un poste en anglais : IF, avec des virgules.");

s = base('NB.SI : compter les Oui', { repere: 'Bloc 3' });
barre(s, 0.6, 1.8, 12.1, 'F19', '=NB.SI(F6:F17;"Oui")', 38);
carte(s, 0.6, 3.2, 5.8, 3.1, '5', 'produits à recommander', OR, NOIR, 110, 26);
carte(s, 6.9, 3.2, 5.8, 3.1, 'Réponse', 'à l\'appel de 8h05', MARINE, BLANC, 50, 26);
note(s, "NB.SI compte les cellules qui remplissent une condition : ici, les « Oui » de F6 à F17. Résultat : 5 produits à recommander. C'est la deuxième réponse à la directrice.");

mission(3, 'Alerte rupture', '35 min', 'groupe de 3', ['Trier par quantité', 'Filtrer < 10', 'Colonne SI : Oui / Non', 'Compter avec NB.SI'], 'Mission 3 · Alerte', '13 ✔',
  "Groupe de 3. Une étoile ★ récompense chaque ligne remplie avec la fonction SI plutôt qu'à la main. Attendu : 5 produits (Bob soleil 3, Confiture 4, Sac en vacoa 6, Casquette 8, Café 9). Le Mug (12) et la Vanille (15) ne sont pas sous le seuil : je vérifie que personne ne les ajoute.");

// ================================================================== BLOC 4
bloc(4, 'Corriger', '11h15 – 11h30', "Bloc 4 : 3 minutes de démonstration, 12 minutes de Mission 4.");

s = base('Les 3 erreurs à connaître', { repere: 'Bloc 4' });
[['####', 'colonne trop étroite', 'élargir'], ['#VALEUR!', 'du texte dans le calcul', 'taper un nombre'], ['#DIV/0!', 'diviseur vide ou 0', 'remplir le diviseur']].forEach(([e, c, r], i) => {
  const x = 0.6 + i * 4.1;
  s.addShape(pptx.ShapeType.roundRect, { x, y: 1.75, w: 3.9, h: 1.4, fill: { color: ROUGE_C }, line: { color: ROUGE_C }, rectRadius: 0.1 });
  s.addText(e, { x, y: 1.75, w: 3.9, h: 1.4, fontFace: 'Consolas', fontSize: 40, bold: true, color: ROUGE, align: 'center', valign: 'middle' });
  s.addText(c, { x, y: 3.3, w: 3.9, h: 1.3, fontFace: FB, fontSize: 26, bold: true, color: NOIR, align: 'center', valign: 'middle', fit: 'shrink' });
  s.addShape(pptx.ShapeType.downArrow, { x: x + 1.6, y: 4.6, w: 0.7, h: 0.6, fill: { color: OR }, line: { color: OR } });
  carte(s, x, 5.25, 3.9, 1.35, r, null, VERT_C, VERT, 28);
});
note(s, "Trois messages à reconnaître. #### : ce n'est pas une erreur de calcul, la colonne est trop étroite pour afficher le nombre ; on élargit. #VALEUR! : une cellule du calcul contient du texte (ici la quantité écrite « douze ») ; on tape le nombre 12. #DIV/0! : on divise par une cellule vide ou nulle (le nombre de clients n'est pas rempli) ; on saisit 415. Le réflexe du manager : ne jamais envoyer un tableau qui affiche un #.");

mission(4, 'Chasse aux erreurs', '12 min', 'en binôme', ['Repérer les 3 erreurs', 'Écrire la cause', 'Réparer', 'Vérifier les ✔'], 'Mission 4 · Erreurs', '3 ✔',
  "En binôme, 12 minutes. Attendus : D9 = 166,80 € (12 × 13,90 €) ; D11 = panier moyen 30,00 € (12 450 ÷ 415) ; colonne D élargie. Le ✔ de l'erreur #### apparaît après un recalcul (touche F9).");

// ================================================================== FIN
s = base('Le coffre du Chaudron', { repere: '11h30' });
['Code 1', 'Code 2', 'Code 3', 'Code 4'].forEach((c, i) => {
  rond(s, 0.75 + i * 3.1, 1.75, 1.6, '🔒', MARINE, BLANC, 44);
  s.addText(c, { x: 0.35 + i * 3.1, y: 3.4, w: 2.4, h: 0.6, fontFace: FT, fontSize: 28, bold: true, color: MARINE, align: 'center' });
});
[['Équipe', 'de 3'], ['10 min', 'chrono'], ['2 indices', '+1 min chacun']].forEach(([a, b], i) => carte(s, 0.6 + i * 4.1, 4.4, 3.9, 1.9, a, b, i === 1 ? OR : CLAIR, i === 1 ? NOIR : MARINE, 40, 24));
note(s, "Escape game final, feuille « Le coffre ». Chaque code est un résultat des missions : 1) nombre de produits à recommander ; 2) valeur du stock arrondie à l'euro ; 3) panier moyen réparé ; 4) prix moyen arrondi à l'euro. Réponses : 5 · 2839 · 30 · 15. Le message « COFFRE OUVERT » s'affiche quand les 4 sont justes. Indice 1 : « relisez la Mission 3 ». Indice 2 : « le panier moyen se répare en Mission 4 ». La première équipe qui ouvre le coffre choisit l'ordre de passage au quiz de correction.");

s = base('Quiz', { repere: '11h40' });
carte(s, 0.6, 1.9, 3.9, 3.0, '10', 'questions', MARINE, BLANC, 96, 28);
carte(s, 4.7, 1.9, 3.9, 3.0, '10', 'minutes', OR, NOIR, 96, 28);
carte(s, 8.8, 1.9, 3.9, 3.0, 'Seul', 'sans classeur', CLAIR, MARINE, 64, 28);
s.addText('Corrigé ensemble juste après', { x: 0.6, y: 5.3, w: 12.1, h: 0.9, fontFace: FB, fontSize: 32, bold: true, color: MARINE, align: 'center' });
note(s, "Quiz papier de 10 questions, 10 minutes, seul et sans le classeur. Je ramasse, puis correction orale rapide des 2 ou 3 questions les plus ratées. Les scores alimentent la traçabilité (positionnement Qualiopi).");

s = base('Réponse à la directrice', { repere: '11h50' });
carte(s, 0.6, 1.8, 5.9, 2.4, '2 838,80 €', 'valeur du stock', OR, NOIR, 60, 26);
carte(s, 6.8, 1.8, 5.9, 2.4, '5 produits', 'à recommander', OR, NOIR, 56, 26);
carte(s, 0.6, 4.5, 12.1, 1.9, 'Ardoise de 8h05 · comparez !', null, MARINE, BLANC, 40);
note(s, "On ressort les ardoises de 8h05. Qui avait trouvé 2 838,80 € ? Qui avait les 5 bons produits ? En 2 minutes à la main, presque personne ; avec le classeur, quelques secondes et zéro erreur. Je reviens à la citation de Kelvin : vous pouvez maintenant exprimer votre stock en chiffres, donc vous en savez quelque chose.");

s = base('À retenir');
lignes(s, [['=', 'toute formule commence ainsi'], ['SOMME', 'le total'], ['MOYENNE', 'la valeur type'], ['SI · NB.SI', 'décider · compter'], ['Zéro #', 'avant d\'envoyer']], 1.6, 0.9);
note(s, "Les 5 réflexes et les 3 règles de sécurité. La ressource de fin de cours (PDF) reprend tout avec des exemples. Je fais relever le score du Tableau de bord : objectif 100 %.");

s = base('Avant de partir', { repere: '11h55' });
carte(s, 0.6, 1.8, 5.9, 2.2, 'Ticket de sortie', '1 geste maîtrisé · 1 à revoir', MARINE, BLANC, 40, 24);
carte(s, 6.8, 1.8, 5.9, 2.2, 'Bonus maison', 'feuille « Bonus · Ventes »', CLAIR, MARINE, 40, 24);
carte(s, 0.6, 4.35, 12.1, 2.0, 'Ctrl + S · copie sur la clé USB', null, OR, NOIR, 40);
note(s, "Ticket de sortie sur post-it : un geste maîtrisé, un geste à revoir. Je les lis pour ajuster la séance suivante. Bonus à la maison : la feuille « Bonus · Ventes » (total, moyenne, meilleur jour, écart à l'objectif), corrigée au début de la prochaine séance. Chacun enregistre et copie son classeur sur sa clé USB.");

pptx.writeFile({ fileName: process.argv[2] }).then((f) => console.log(`${n} diapositives → ${f}`));
