/* Fabrique le pack du Jour 2 Excel (MUM) avec le moteur du Pilotage YEBA.
   node fabriquer.js <dossier_sortie>
   La date réelle de la session n'est pas connue : les documents affichent « date à compléter ». */
const fs = require('fs'), path = require('path');
const NM = process.env.NODE_MODULES_DIR || '/tmp/claude-0/-home-user-Training/ae3dbc59-f9ec-5b68-9c3b-51565a7e3450/scratchpad/web/';
const req = require('module').createRequire(NM + 'x.js');
globalThis.ExcelJS = req('exceljs'); globalThis.docx = req('docx'); globalThis.JSZip = req('jszip'); globalThis.PptxGenJS = req('pptxgenjs');
global.window = globalThis;
const RACINE = path.resolve(__dirname, '../../..');
for (const f of ['referentiels', 'extraction', 'pedagogie', 'plan', 'planification', 'programme', 'exports', 'moteur']) require(RACINE + '/web/src/' + f + '.js');
for (const f of ['donnees', 'suivi', 'generateur', 'documents', 'finances']) require(RACINE + '/web/pilotage/src/' + f + '.js');
const D = globalThis.Decorticage, P = globalThis.Pilotage;
const SORTIE = process.argv[2];
const C = require('./contenu.js');
const DATE = '2026-11-03';                 // date technique (non affichée)
D.fr = () => '……/……/……';                   // date de session à compléter à la main
D.JOURS = D.JOURS.map(() => 'Date :');
(async () => {
  const lire = (n) => fs.readFileSync(NM + n, 'utf8'), brut = lire('js_REAC.txt');
  const analyse = { reac: D.analyserReac(brut, brut), fiche: D.analyserFiche(lire('js_FICHE.txt')), noms: {} };
  analyse.re = D.analyserRe(lire('js_RE.txt'), analyse.reac);
  const identite = P.identiteYeba(), charte = Object.assign({ nom_organisme: 'YEBA FORMATIONS' }, P.initiales().charte);
  const png = fs.readFileSync(RACINE + '/web/pilotage/src/logo_yeba.png');
  const logo = { dataURL: 'data:image/png;base64,' + png.toString('base64'), base64: png.toString('base64'), ext: 'png', octets: new Uint8Array(png), ratio: 520 / 443 };
  const r = { heures_centre: 21, date_debut: DATE, jours: '1', creneaux: '08:00-12:00, 13:00-17:00', pauses: '10:00-10:20, 15:00-15:20', afficher_nom: true, afficher_logo: true };
  const ctx = Object.assign(D.construireContexte(analyse, r, charte, logo), { pied: P.blocMarque(identite), titre: C.module, sigle: 'MUM' });
  const hm = (s) => { const m = /(\d+)h(\d+)/.exec(s); return +m[1] * 60 + +m[2]; };
  const seance = Object.assign({ numero: 2, type_seance: 'apprentissage', at: 0 }, C.seance);
  const lignes = C.pack.deroule.filter((d) => d.objectif).map((d) => ({ date: D.lireDate(DATE), debut: hm(d.debut), fin: hm(d.fin), minutes: hm(d.fin) - hm(d.debut), seance,
    objectif: { texte: C.pack.objectifs_seance[d.objectif - 1], niveau: D.niveauBloom(C.pack.objectifs_seance[d.objectif - 1]), contenus: [], criteres: [], activite: d.activite, exemple: '' } }));
  const jour = { date: DATE, lignes, seances: [seance], minutes: lignes.reduce((t, l) => t + l.minutes, 0) };
  const m = P.matiereSeance(ctx, jour), pack = P.normaliserPack(JSON.parse(JSON.stringify(C.pack)), m);
  const fichiers = await P.fabriquerSeance(ctx, jour, pack, logo, identite);
  const dc = { charte: ctx.charte, nomOrg: ctx.nomOrg, logo, pied: ctx.pied };
  fichiers.push([`Corriges_${DATE}`, await D.docWord(dc, `Corrigés et fiche d'animation — ${pack.titre} — DOCUMENT FORMATEUR`, (o) => {
    o.encadre('Document réservé au formateur', ['Corrigés des missions, règles des jeux et indices de l\'escape game.', 'Le corrigé complet du classeur est fourni à part : Classeur_missions_CORRIGE_FORMATEUR.xlsx.']);
    pack.exercices.forEach((e, i) => { o.h2(`${i + 1}. ${e.titre} (${e.duree_minutes} min, ${e.modalite})`); o.p(`Consigne : ${e.consigne}`); o.p(`Corrigé / attendus : ${e.corrige || '—'}`); o.p(`Objectif : ${pack.objectifs_seance[e.objectif - 1] || ''}`); });
  })]);
  fichiers.push([`QuizApprenants_${DATE}`, await D.docWord(dc, `Quiz — ${pack.titre}`, (o) => {
    o.p('Nom ou code stagiaire : ……   Entourez la bonne réponse. 10 questions, 15 minutes.');
    pack.quiz.forEach((q, i) => { o.h2(`Question ${i + 1}`); o.p(q.question); q.choix.forEach((x, j) => o.puce(`${'ABCD'[j]}. ${x}`)); });
    o.p('Score : …… / 10');
  })]);
  const NOMS = { Seance: '1_Diaporama', Essentiel_journee: '2_Ressource_fin_de_cours', Exercices: '3_Missions_apprenants', Corriges: '4_Corriges_et_animation_FORMATEUR', Grille_criteriee: '5_Grille_evaluation_5_criteres', QuizApprenants: '6_Quiz_apprenants', Quiz_FORMATEUR: '7_Quiz_reponses_FORMATEUR', Fiche_seance_preuve: '8_Fiche_seance_preuve_Qualiopi' };
  fs.mkdirSync(SORTIE, { recursive: true });
  for (const [n, b] of fichiers) {
    const base = n.replace(`_${DATE}_${ctx.sigle}`, '').replace(`_${DATE}`, '').replace(/\.(pptx|docx)$/, ''), ext = /\.pptx$/.test(n) ? 'pptx' : 'docx';
    fs.writeFileSync(path.join(SORTIE, `${NOMS[base] || base}_MUM_J2_Excel.${ext}`), Buffer.from(await b.arrayBuffer()));
  }
  console.log(`${fichiers.length} fichiers, ${jour.minutes / 60} h, ${pack.diapositives.length} diapos, ${pack.exercices.length} exercices, ${pack.quiz.length} questions`);
})().catch((e) => { console.error(e); process.exit(1); });
