// Redessine le logo YEBA FORMATIONS en vectoriel, sans l'œil, et exporte les déclinaisons.
const opentype = require('opentype.js');
const fs = require('fs');
const path = require('path');

const OUT = process.argv[2];
const NAVY = '#1B3A6B', GOLD = '#C9AB4C', WHITE = '#FFFFFF';
const F700 = opentype.parse(fs.readFileSync(path.join(__dirname, 'mont1.ttf')).buffer);
const F800 = opentype.parse(fs.readFileSync(path.join(__dirname, 'mont2.ttf')).buffer);

// Texte -> tracé, calé sur une largeur cible, avec interlettrage.
function textPath(font, str, x, baseline, width, tracking, fill) {
  const probe = size => {
    let w = 0;
    for (const ch of str) w += font.getAdvanceWidth(ch, size) + tracking * size;
    return w - tracking * size;
  };
  let size = 100;
  size = size * width / probe(size);
  let cx = x, d = '';
  for (const ch of str) {
    d += font.getPath(ch, cx, baseline, size).toPathData(2);
    cx += font.getAdvanceWidth(ch, size) + tracking * size;
  }
  return `<path d="${d}" fill="${fill}"/>`;
}

// Géométrie des trois pyramides (repère du logo d'origine agrandi ×3).
const TRI = {
  L: [[370, 270], [205, 520], [535, 520]],
  M: [[548, 205], [378, 520], [718, 520]],
  R: [[730, 270], [565, 520], [895, 520]],
};
const NODES = {
  L: [[365, 372], [405, 440], [312, 462]],
  M: [[548, 300], [494, 365], [606, 365], [556, 410], [486, 452], [612, 442]],
  R: [[733, 372], [692, 440], [788, 462]],
};

const lerp = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t];
function edgePoints(t) {
  const pts = [];
  for (let i = 0; i < 3; i++) for (const k of [0.3, 0.55, 0.8]) pts.push(lerp(t[i], t[(i + 1) % 3], k));
  return pts.concat(t);
}
function network(key) {
  const nodes = NODES[key], tri = TRI[key], anchors = edgePoints(tri);
  const seen = new Set(), segs = [];
  const add = (a, b) => {
    const id = [a, b].map(p => p.join(',')).sort().join('|');
    if (!seen.has(id)) { seen.add(id); segs.push([a, b]); }
  };
  nodes.forEach(n => {
    nodes.filter(m => m !== n).sort((a, b) => Math.hypot(a[0] - n[0], a[1] - n[1]) - Math.hypot(b[0] - n[0], b[1] - n[1]))
      .slice(0, 3).forEach(m => add(n, m));
    anchors.slice().sort((a, b) => Math.hypot(a[0] - n[0], a[1] - n[1]) - Math.hypot(b[0] - n[0], b[1] - n[1]))
      .slice(0, 2).forEach(a => add(n, a));
  });
  return { segs, nodes };
}

function mark(stroke) {
  let s = '';
  for (const k of ['L', 'M', 'R']) {
    const { segs, nodes } = network(k);
    s += `<g clip-path="url(#clip${k})">` + segs.map(([a, b]) =>
      `<line x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}" stroke="${stroke}" stroke-width="5.5" stroke-linecap="round"/>`).join('') + '</g>';
    s += nodes.map(n => `<circle cx="${n[0]}" cy="${n[1]}" r="12" fill="${stroke}"/>`).join('');
  }
  for (const k of ['L', 'M', 'R']) {
    s += `<polygon points="${TRI[k].map(p => p.join(',')).join(' ')}" fill="none" stroke="${stroke}" stroke-width="15" stroke-linejoin="miter"/>`;
  }
  return s;
}

const defs = `<defs>
  <linearGradient id="g" gradientUnits="userSpaceOnUse" x1="430" y1="0" x2="640" y2="0">
    <stop offset="0" stop-color="${NAVY}"/><stop offset="1" stop-color="${GOLD}"/></linearGradient>
  ${Object.entries(TRI).map(([k, t]) => `<clipPath id="clip${k}"><polygon points="${t.map(p => p.join(',')).join(' ')}"/></clipPath>`).join('')}
</defs>`;

// Déclinaisons : [nom, fond, couleur du symbole, couleur YEBA, couleur FORMATIONS, avec texte]
const VARIANTS = [
  ['logo-yeba-formations_couleur_transparent', null, 'url(#g)', NAVY, GOLD, true],
  ['logo-yeba-formations_couleur_fond-blanc', WHITE, 'url(#g)', NAVY, GOLD, true],
  ['logo-yeba-formations_fond-bleu', NAVY, 'url(#g2)', WHITE, GOLD, true],
  ['symbole_or_fond-bleu', NAVY, GOLD, null, null, false],
  ['symbole_bleu_fond-or', GOLD, NAVY, null, null, false],
  ['symbole_couleur_transparent', null, 'url(#g)', null, null, false],
];
// Sur fond bleu, le dégradé part du blanc pour que la pyramide gauche reste visible.
const defsDark = defs.replace('</defs>', `<linearGradient id="g2" gradientUnits="userSpaceOnUse" x1="430" y1="0" x2="640" y2="0">
  <stop offset="0" stop-color="${WHITE}"/><stop offset="1" stop-color="${GOLD}"/></linearGradient></defs>`);

const svgs = {};
for (const [name, bg, sym, yeba, form, withText] of VARIANTS) {
  const vb = withText ? [106, 120, 940, 800] : [185, 185, 730, 355];
  let body = mark(sym);
  if (withText) {
    body += textPath(F800, 'YEBA', 205, 745, 750, 0.02, yeba);
    body += textPath(F700, 'FORMATIONS', 192, 852, 768, 0.08, form);
  }
  let bgRect = '';
  if (bg) {
    // Symbole seul : carré (photo de profil) ; logo complet : marge autour.
    if (!withText) { vb.splice(0, 4, 90, -98, 920, 920); }
    bgRect = `<rect x="${vb[0]}" y="${vb[1]}" width="${vb[2]}" height="${vb[3]}" fill="${bg}"/>`;
  }
  svgs[name] = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb.join(' ')}" width="${vb[2]}" height="${vb[3]}">${sym === 'url(#g2)' ? defsDark : defs}${bgRect}${body}</svg>`;
}

fs.mkdirSync(OUT, { recursive: true });
for (const [n, s] of Object.entries(svgs)) fs.writeFileSync(path.join(OUT, n + '.svg'), s);

(async () => {
  const { chromium } = require('playwright');
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const [n, s] of Object.entries(svgs)) {
    const [, , w, h] = s.match(/viewBox="([^"]+)"/)[1].split(' ').map(Number);
    const scale = 2000 / w;
    const p = await b.newPage({ viewport: { width: Math.round(w * scale), height: Math.round(h * scale) } });
    await p.setContent(`<body style="margin:0;background:transparent">${s.replace(/width="[^"]+" height="[^"]+">/, `width="${Math.round(w * scale)}" height="${Math.round(h * scale)}">`)}</body>`);
    await p.screenshot({ path: path.join(OUT, n + '.png'), omitBackground: true });
    await p.close();
  }
  await b.close();
  console.log('ok');
})();
