const fs = require('fs'), path = require('path');
const NM = '/tmp/claude-0/-home-user-Training/ae3dbc59-f9ec-5b68-9c3b-51565a7e3450/scratchpad/web/'; const req = require('module').createRequire(NM + 'x.js');
globalThis.ExcelJS = req('exceljs'); globalThis.docx = req('docx'); globalThis.JSZip = req('jszip'); globalThis.PptxGenJS = req('pptxgenjs');
global.window = globalThis;
for (const f of ['referentiels', 'extraction', 'pedagogie', 'plan', 'planification', 'programme', 'exports', 'moteur']) require('/home/user/Training/web/src/' + f + '.js');
for (const f of ['donnees', 'suivi', 'generateur', 'documents', 'finances']) require('/home/user/Training/web/pilotage/src/' + f + '.js');
const D = globalThis.Decorticage, P = globalThis.Pilotage;
const SORTIE = process.argv[2];
const COURS = require('./cours_v2.js');
(async () => {
  const lire = (n) => fs.readFileSync(NM + n, 'utf8'), brut = lire('js_REAC.txt');
  const analyse = { reac: D.analyserReac(brut, brut), fiche: D.analyserFiche(lire('js_FICHE.txt')), noms: {} };
  analyse.re = D.analyserRe(lire('js_RE.txt'), analyse.reac);
  const identite = P.identiteYeba(), charte = Object.assign({ nom_organisme: 'YEBA FORMATIONS' }, (() => { const c = P.initiales().charte; return c; })());
  const png = fs.readFileSync('/home/user/Training/web/pilotage/src/logo_yeba.png');
  const logo = { dataURL: 'data:image/png;base64,' + png.toString('base64'), base64: png.toString('base64'), ext: 'png', octets: new Uint8Array(png), ratio: 520 / 443 };
  const r = { heures_centre: 455, date_debut: '2026-11-02', jours: '1', creneaux: '08:00-12:00, 13:00-16:00', pauses: '10:00-10:15, 14:30-14:45', afficher_nom: true, afficher_logo: true };
  const ctx = Object.assign(D.construireContexte(analyse, r, charte, logo), { pied: P.blocMarque(identite) });
  const plan1 = analyse.reac.competences[0].plan;
  const hm = (s) => { const m = /(\d+)h(\d+)/.exec(s); return +m[1] * 60 + +m[2]; };
  fs.mkdirSync(SORTIE, { recursive: true });
  for (const [k, c] of COURS.entries()) {
    const g = c.seance.partie ? plan1.parties.find((p) => p.numero === c.seance.partie) : null;
    const seance = Object.assign({ numero: k + 1, type_seance: 'apprentissage', at: c.seance.cp ? 1 : 0 }, c.seance,
      g ? { partie_titre: g.titre, action: g.petites.map((x) => `${g.numero}.${x.numero} ${x.texte}`).join(' ; '), criteres_partie: g.criteres, epreuves: plan1.epreuves, bloc: plan1.bloc } : {});
    const lignes = c.pack.deroule.filter((d) => d.objectif).map((d) => ({ date: D.lireDate(c.date), debut: hm(d.debut), fin: hm(d.fin), minutes: hm(d.fin) - hm(d.debut), seance,
      objectif: { texte: c.pack.objectifs_seance[d.objectif - 1], niveau: D.niveauBloom(c.pack.objectifs_seance[d.objectif - 1]), contenus: [], criteres: [], activite: d.activite, exemple: '' } }));
    const jour = { date: c.date, lignes, seances: [seance], minutes: lignes.reduce((t, l) => t + l.minutes, 0) };
    const m = P.matiereSeance(ctx, jour), pack = P.normaliserPack(c.pack, m);
    const fichiers = await P.fabriquerSeance(ctx, jour, pack, logo, identite);
    const dossier = path.join(SORTIE, `Cours_${k + 1}_${c.date}`); fs.mkdirSync(dossier, { recursive: true });
    for (const [n, b] of fichiers) fs.writeFileSync(path.join(dossier, n.replace(`_${c.date}_${ctx.sigle}`, '').replace('.', `_cours${k + 1}.`)), Buffer.from(await b.arrayBuffer()));
    console.log(`Cours ${k + 1} : ${fichiers.length} fichiers, ${jour.minutes / 60} h de formation (${pack.diapositives.length} diapos)`);
  }
  fs.writeFileSync(path.join(SORTIE, '.ctx_ok'), '1');
})().catch((e) => { console.error(e); process.exit(1); });
