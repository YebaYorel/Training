const fs = require('fs'), path = require('path');
const NM = '/tmp/claude-0/-home-user-Training/ae3dbc59-f9ec-5b68-9c3b-51565a7e3450/scratchpad/web/'; const req = require('module').createRequire(NM + 'x.js');
globalThis.docx = req('docx'); global.window = globalThis;
for (const f of ['referentiels', 'pedagogie', 'planification', 'exports']) require('/home/user/Training/web/src/' + f + '.js');
for (const f of ['donnees', 'documents']) require('/home/user/Training/web/pilotage/src/' + f + '.js');
const D = globalThis.Decorticage, P = globalThis.Pilotage, seq = require('./seq.json');
const png = fs.readFileSync('/home/user/Training/web/pilotage/src/logo_yeba.png');
const ctx = { charte: Object.assign({}, P.initiales().charte), nomOrg: 'YEBA FORMATIONS', logo: { octets: new Uint8Array(png), ratio: 520 / 443 }, pied: P.blocMarque(P.identiteYeba()) };
(async () => {
  const fr = (iso) => iso.split('-').reverse().join('/');
  const b = await D.docWord(ctx, 'TP Manager d\'établissement marchand — Séquençage des 48 sessions', (o) => {
    o.encadre('Cadre', ['48 lundis du 02/11/2026 au 25/10/2027, 08h00–12h00 et 13h00–16h00 (6 h 30 de formation), soit 312 heures.', 'Ordre : intégration et mise à niveau → AT1 → AT3 → productions → AT2 → finalisation → examen blanc → remédiation et oral.', 'Lundis exclus : ' + Object.entries(seq.exclus).map(([d, m]) => `${fr(d)} (${m})`).join(' ; '), 'Chaque session commence par un rituel spirale (rappel actif de la session précédente) et se termine par un ticket de sortie.']);
    o.h2('Vue d\'ensemble');
    o.tableau([['N°', 'Date', 'Phase', 'Thème', 'Évaluation']].concat(seq.lignes.map((l) => [String(l.n), fr(l.date), l.phase, l.titre, l.evaluation])));
    o.saut(); o.h2('Le détail, session par session');
    for (const l of seq.lignes) {
      o.h3(`Session ${l.n} — ${fr(l.date)} — ${l.titre}`);
      o.p(`Phase : ${l.phase} · Cumul : ${l.cumul} h${l.epreuve ? ' · Épreuve préparée : ' + l.epreuve : ''}`);
      l.contenu.split('\n').forEach((x) => o.puce(x));
      o.p(`Fils rouges : ${l.fil}`); o.p(`Évaluation : ${l.evaluation}`);
      if (l.criteres.length) { o.note('Critères de performance du REAC visés :'); l.criteres.forEach((c) => o.puce('✔ ' + c, 1)); }
    }
  });
  fs.writeFileSync(path.join(process.argv[2], 'Sequencage_MEM_48_sessions.docx'), Buffer.from(await b.arrayBuffer()));
  console.log('docx ok');
})().catch((e) => { console.error(e); process.exit(1); });
