// Génère les visuels YEBA IA (PNG) à partir de gabarits HTML — charte YEBA FORMATIONS.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUT = process.argv[2];
const HERE = __dirname;
const NAVY = '#1B3A6B', GOLD = '#C9AB4C', BLACK = '#121212', WHITE = '#FFFFFF';
const LOGO = 'data:image/svg+xml;base64,' + fs.readFileSync(path.join(HERE, '..', 'logo', 'logo-yeba-formations_couleur_transparent.svg')).toString('base64');
const FONTS = fs.readFileSync(path.join(HERE, 'fonts-local.css'), 'utf8')
  .replace(/fonts\/([^)]+)/g, (_, f) => 'data:font/woff2;base64,' + fs.readFileSync(path.join(HERE, 'fonts', f)).toString('base64'));

// Motif réseau (points reliés), déterministe.
function network(w, h, color, opacity, n = 38, seed = 7) {
  let s = seed; const r = () => (s = (s * 9301 + 49297) % 233280) / 233280;
  const pts = Array.from({ length: n }, () => [r() * w, r() * h]);
  let lines = '';
  pts.forEach((p, i) => pts.slice(i + 1).forEach(q => {
    const d = Math.hypot(p[0] - q[0], p[1] - q[1]);
    if (d < w * 0.2) lines += `<line x1="${p[0]}" y1="${p[1]}" x2="${q[0]}" y2="${q[1]}"/>`;
  }));
  const dots = pts.map(p => `<circle cx="${p[0]}" cy="${p[1]}" r="5"/>`).join('');
  return `<svg class="net" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" style="opacity:${opacity}">
    <g stroke="${color}" stroke-width="2">${lines}</g><g fill="${color}">${dots}</g></svg>`;
}

const ICONS = {
  lock: '<rect x="18" y="44" width="64" height="46" rx="6"/><path d="M32 44V30a18 18 0 0 1 36 0v14"/><circle cx="50" cy="66" r="5"/>',
  card: '<rect x="10" y="24" width="80" height="54" rx="7"/><line x1="10" y1="40" x2="90" y2="40"/><line x1="22" y1="62" x2="46" y2="62"/>',
  health: '<path d="M50 86S14 64 14 38a18 18 0 0 1 36-6 18 18 0 0 1 36 6c0 26-36 48-36 48z"/><path d="M50 44v20M40 54h20"/>',
  contacts: '<rect x="18" y="12" width="64" height="76" rx="6"/><circle cx="50" cy="40" r="11"/><path d="M32 72a18 18 0 0 1 36 0"/>',
  folder: '<path d="M10 28h30l8 10h42v46H10z"/><path d="M40 60h20"/>',
  cyclone: '<circle cx="50" cy="50" r="11"/><path d="M39 50C39 28 56 14 80 14M61 50C61 72 44 86 20 86"/><path d="M39 50C30 42 30 30 36 22M61 50C70 58 70 70 64 78"/>',
  rocket: '<path d="M50 12c16 12 22 32 16 52H34C28 44 34 24 50 12z"/><circle cx="50" cy="38" r="7"/><path d="M34 64l-10 14h16M66 64l10 14H60M44 72v14M56 72v14"/>',
  tools: '<path d="M22 78l30-30M60 18a14 14 0 0 0-8 22l-30 30 8 8 30-30a14 14 0 0 0 22-8l-10 4-8-8z"/>',
  shield: '<path d="M50 10l34 12v24c0 22-15 36-34 44C31 82 16 68 16 46V22z"/><rect x="38" y="46" width="24" height="18" rx="3"/><path d="M42 46v-6a8 8 0 0 1 16 0v6"/>',
  scale: '<path d="M50 14v70M30 84h40M18 30h64"/><path d="M18 30l-12 26h24zM82 30l-12 26h24z"/>',
  grad: '<path d="M8 40l42-18 42 18-42 18z"/><path d="M26 48v18c14 10 34 10 48 0V48M88 42v24"/>',
  star: '<path d="M50 12l11 24 26 3-19 18 5 26-23-13-23 13 5-26-19-18 26-3z"/>',
};
const icon = (k, size, color, sw = 5) =>
  `<svg viewBox="0 0 100 100" width="${size}" height="${size}" fill="none" stroke="${color}" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round">${ICONS[k]}</svg>`;

const BASE = `${FONTS}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,sans-serif}
.page{position:relative;overflow:hidden;display:flex;flex-direction:column;justify-content:center;padding:96px}
.net{position:absolute;inset:0}
.h{font-family:Montserrat,sans-serif;font-weight:800;line-height:1.05;letter-spacing:-1px}
.t{font-family:Inter,sans-serif;font-weight:600;line-height:1.25}
.foot{position:absolute;left:0;right:0;bottom:0;height:120px;display:flex;align-items:center;justify-content:space-between;padding:0 64px;font-family:Montserrat;font-weight:700;font-size:36px}
.pill{display:inline-block;border-radius:999px;padding:10px 28px;font-family:Montserrat;font-weight:700;font-size:34px;letter-spacing:1px}
.num{position:absolute;top:60px;right:72px;font-family:Montserrat;font-weight:700;font-size:34px}
.logo{height:92px;border-radius:14px}
`;

function footer(bg, fg) {
  return `<div class="foot" style="background:${bg};color:${fg}"><span>YEBA IA · L'IA, simplement.</span><span style="font-size:28px">yebaformations.re</span></div>`;
}

// ---------- Carrousel : 5 choses à ne jamais taper ----------
function carouselRGPD() {
  const W = 1080, H = 1350, pages = [];
  pages.push(`<div class="page" style="width:${W}px;height:${H}px;background:${BLACK};color:${WHITE}">
    ${network(W, H, GOLD, .18)}
    <div class="pill" style="background:${GOLD};color:${BLACK};position:relative;align-self:flex-start">LE DROIT SANS MIGRAINE</div>
    <div class="h" style="font-size:420px;color:${GOLD};position:relative;margin-top:10px">5</div>
    <div class="h" style="font-size:96px;position:relative">choses à ne <span style="color:${GOLD}">JAMAIS</span> taper dans une IA</div>
    ${footer(GOLD, BLACK)}</div>`);
  const items = [['lock', 'Tes mots de passe'], ['card', 'Carte bancaire, IBAN'], ['health', 'Données de santé'],
    ['contacts', 'Noms + coordonnées clients'], ['folder', 'Documents confidentiels']];
  items.forEach(([k, txt], i) => pages.push(`<div class="page" style="width:${W}px;height:${H}px;background:${WHITE};color:${NAVY};align-items:flex-start">
    <div class="num" style="color:${NAVY}">${i + 2}/7</div>
    <div style="width:250px;height:250px;border-radius:50%;background:${NAVY};display:flex;align-items:center;justify-content:center">${icon(k, 150, GOLD, 6)}</div>
    <div class="h" style="font-size:230px;margin-top:40px">${i + 1}.</div>
    <div class="h" style="font-size:112px">${txt}</div>
    ${footer(NAVY, WHITE)}</div>`));
  pages.push(`<div class="page" style="width:${W}px;height:${H}px;background:${NAVY};color:${WHITE}">
    ${network(W, H, GOLD, .15)}
    <div class="h" style="font-size:130px;position:relative">Remplace.<br>Anonymise.<br><span style="color:${GOLD}">Résume.</span></div>
    <div class="t" style="font-size:52px;margin-top:56px;position:relative">« Client A » au lieu du vrai nom.</div>
    <div class="t" style="font-size:44px;margin-top:40px;position:relative;color:${GOLD}">↗ Partage à ton équipe</div>
    <div class="t" style="font-size:30px;margin-top:40px;position:relative;opacity:.9">RGPD : art. 5 (minimisation) · art. 9 · art. 32</div>
    ${footer(GOLD, NAVY)}</div>`);
  return { name: 'carrousel_5-choses-a-ne-jamais-taper', W, H, pages };
}

// ---------- Carrousel : IA Act = alerte cyclonique ----------
function carouselIAAct() {
  const W = 1080, H = 1350, pages = [];
  pages.push(`<div class="page" style="width:${W}px;height:${H}px;background:${NAVY};color:${WHITE}">
    ${network(W, H, GOLD, .15)}
    <div class="pill" style="background:${GOLD};color:${NAVY};position:relative;align-self:flex-start">LE DROIT SANS MIGRAINE</div>
    <div style="position:relative;margin:50px 0 30px">${icon('cyclone', 260, GOLD, 6)}</div>
    <div class="h" style="font-size:118px;position:relative">L'IA Act =<br>une alerte <span style="color:${GOLD}">cyclone</span></div>
    <div class="t" style="font-size:48px;margin-top:40px;position:relative">La loi européenne sur l'IA en 4 niveaux →</div>
    ${footer(GOLD, NAVY)}</div>`);
  const lv = [
    ['#5B2A86', WHITE, 'VIOLETTE', 'INTERDIT', 'Notation sociale des citoyens', 'art. 5'],
    ['#B3261E', WHITE, 'ROUGE', 'HAUT RISQUE', 'IA qui trie des CV', 'annexe III'],
    ['#F08A24', BLACK, 'ORANGE', 'TRANSPARENCE', 'Chatbot, vidéo IA : il faut le dire', 'art. 50'],
    ['#3E9B4F', BLACK, 'PAS D\'ALERTE', 'RISQUE MINIMAL', 'Filtre anti-spam : tu es libre', '—'],
  ];
  lv.forEach(([bg, fg, lvl, what, ex, ref], i) => pages.push(`<div class="page" style="width:${W}px;height:${H}px;background:${bg};color:${fg}">
    <div class="num" style="color:${fg}">${i + 2}/6</div>
    <div class="h" style="font-size:${lvl.length > 9 ? 92 : 120}px">${lvl}</div>
    <div class="h" style="font-size:${what.length > 11 ? 86 : 124}px;margin-top:10px">= ${what}</div>
    <div style="height:10px;width:220px;background:${fg};margin:60px 0"></div>
    <div class="t" style="font-size:66px">Ex. : ${ex}</div>
    <div class="t" style="font-size:34px;margin-top:40px;opacity:.9">IA Act · ${ref}</div>
    ${footer(NAVY, WHITE)}</div>`));
  pages.push(`<div class="page" style="width:${W}px;height:${H}px;background:${NAVY};color:${WHITE}">
    ${network(W, H, GOLD, .15)}
    <div class="h" style="font-size:96px;position:relative">La plupart des TPE :<br><span style="color:${GOLD}">orange</span> ou <span style="color:${GOLD}">pas d'alerte</span>.</div>
    <div class="h" style="font-size:80px;margin-top:60px;position:relative">Pas de panique.<br>De la méthode.</div>
    <div class="t" style="font-size:30px;margin-top:50px;position:relative;opacity:.9">Analogie pédagogique simplifiée · Règlement (UE) 2024/1689</div>
    ${footer(GOLD, NAVY)}</div>`);
  return { name: 'carrousel_ia-act-alerte-cyclone', W, H, pages };
}

// ---------- Carrousel : R-C-T-F ----------
function carouselRCTF() {
  const W = 1080, H = 1350, pages = [];
  pages.push(`<div class="page" style="width:${W}px;height:${H}px;background:${NAVY};color:${WHITE}">
    ${network(W, H, GOLD, .15)}
    <div class="pill" style="background:${GOLD};color:${NAVY};position:relative;align-self:flex-start">L'IA EN 30 S CHRONO</div>
    <div class="h" style="font-size:104px;position:relative;margin-top:50px">4 lettres qui changent tout</div>
    <div class="h" style="font-size:200px;position:relative;color:${GOLD};margin-top:40px">R·C·T·F</div>
    ${footer(GOLD, NAVY)}</div>`);
  [['R', 'Rôle', '« Tu es un assistant commercial. »'], ['C', 'Contexte', '« Je tiens un garage à Saint-Pierre. »'],
   ['T', 'Tâche', '« Écris une relance pour un devis non signé. »'], ['F', 'Format', '« 5 lignes, ton chaleureux, vouvoiement. »']]
    .forEach(([l, w, ex], i) => pages.push(`<div class="page" style="width:${W}px;height:${H}px;background:${WHITE};color:${NAVY}">
      <div class="num">${i + 2}/6</div>
      <div class="h" style="font-size:520px;line-height:.9">${l}</div>
      <div class="h" style="font-size:120px">${w}</div>
      <div class="t" style="font-size:60px;margin-top:40px;color:${BLACK}">${ex}</div>
      ${footer(NAVY, WHITE)}</div>`));
  pages.push(`<div class="page" style="width:${W}px;height:${H}px;background:${NAVY};color:${WHITE}">
    ${network(W, H, GOLD, .15)}
    <div class="h" style="font-size:120px;position:relative">Enregistre.<br>Essaie.<br><span style="color:${GOLD}">Gagne du temps.</span></div>
    ${footer(GOLD, NAVY)}</div>`);
  return { name: 'carrousel_recette-RCTF', W, H, pages };
}

// ---------- Couvertures Stories à la une ----------
function highlights() {
  const W = 1080, H = 1920;
  const list = [['rocket', 'Commencer'], ['tools', 'Outils'], ['shield', 'RGPD'], ['scale', 'IA Act'], ['grad', 'Formations'], ['star', 'Avis']];
  return list.map(([k, w]) => ({ name: `a-la-une_${w.toLowerCase().replace(/ /g, '-')}`, W, H, pages: [
    `<div class="page" style="width:${W}px;height:${H}px;background:${NAVY};align-items:center">
      <div style="width:760px;height:760px;border-radius:50%;border:10px solid ${GOLD};display:flex;flex-direction:column;align-items:center;justify-content:center">
        ${icon(k, 330, GOLD, 5)}
        <div class="h" style="font-size:86px;color:${WHITE};margin-top:20px">${w}</div>
      </div></div>`] }));
}

// ---------- Couvertures des 14 Reels ----------
function reelCovers() {
  const W = 1080, H = 1920;
  const R = [
    ['1A', 'Coulisses', 'L\'IA est simple.', 'On vous l\'a mal expliquée.'],
    ['1B', 'L\'IA en 30 s', 'Des milliers d\'outils IA.', 'Il t\'en faut 1.'],
    ['2A', 'L\'IA en 30 s', 'ChatGPT ne réfléchit pas.', 'Il cuisine.'],
    ['2B', 'Le droit sans migraine', 'Ce <span style="white-space:nowrap">copier-coller</span>', 'peut te coûter cher.'],
    ['3A', 'L\'IA en 30 s', '4 lettres', 'qui changent tout.'],
    ['3B', 'Mythe ou réalité', 'L\'IA va', 'te remplacer ?'],
    ['4A', 'Actu IA décodée', 'L\'info IA', 'de la semaine.'],
    ['4B', 'Le droit sans migraine', 'La loi IA =', 'une alerte cyclone.'],
    ['5A', 'L\'IA en 30 s', '1 TPE-PME sur 4', 'utilise déjà l\'IA.', 96],
    ['5B', 'Le droit sans migraine', '5 choses à ne jamais', 'taper dans une IA.'],
    ['6A', 'Test péi', 'La pub d\'un snack', 'en 2 minutes.'],
    ['6B', 'Le droit sans migraine', 'Cette personne', 'n\'existe pas.'],
    ['7A', 'Coulisses', 'De la vente', 'à l\'IA.'],
    ['7B', 'L\'IA en 30 s', 'Tu choisis', 'la prochaine vidéo.'],
  ];
  // Texte dans la zone centrale 1080x1440 (recadrage 3:4 de la grille du profil).
  return R.map(([id, rub, a, b, fs = 118]) => ({ name: `couverture-reel_${id}`, W, H, pages: [
    `<div class="page" style="width:${W}px;height:${H}px;background:${NAVY};color:${WHITE};padding:0 90px">
      ${network(W, H, GOLD, .16, 44, id.charCodeAt(0) + id.charCodeAt(1))}
      <div style="position:relative">
        <div class="pill" style="background:${GOLD};color:${NAVY}">${rub.toUpperCase()}</div>
        <div class="h" style="font-size:${fs}px;margin-top:50px">${a}</div>
        <div class="h" style="font-size:${fs}px;color:${GOLD}">${b}</div>
        <div class="t" style="font-size:40px;margin-top:60px">YEBA IA · L'IA, simplement.</div>
      </div></div>`] }));
}

// ---------- Pastille « Généré par IA » (fond transparent) ----------
function badge() {
  return { name: 'pastille_genere-par-IA', W: 640, H: 150, transparent: true, pages: [
    `<div style="width:640px;height:150px;display:flex;align-items:center;justify-content:center">
      <div class="pill" style="background:${BLACK};color:${WHITE};border:5px solid ${GOLD};font-size:46px;padding:18px 40px">✦ Généré par IA</div></div>`] };
}

// ---------- Post « Qui suis-je » avec logo (mentions légales exactes) ----------
function aboutPost() {
  const W = 1080, H = 1350;
  return { name: 'post_qui-sommes-nous', W, H, pages: [
    `<div class="page" style="width:${W}px;height:${H}px;background:${WHITE};color:${NAVY};align-items:center;text-align:center;padding:80px">
      <img src="${LOGO}" style="height:360px">
      <div class="h" style="font-size:96px;margin-top:40px">YEBA IA</div>
      <div class="h" style="font-size:60px;color:${BLACK};margin-top:14px">L'IA, simplement.</div>
      <div class="t" style="font-size:44px;margin-top:50px">Usage de l'IA · RGPD · IA Act<br>expliqués sans jargon</div>
      <div class="t" style="font-size:24px;margin-top:70px;color:${BLACK};line-height:1.45;font-weight:400">
        YEBA FORMATIONS · SIRET 814 622 262 00032 · Saint-Denis, La Réunion<br>
        Déclaration d'activité enregistrée sous le n° 04 97 36763 97 auprès du préfet de région de La Réunion.<br>
        Cet enregistrement ne vaut pas agrément de l'État.<br>
        Certification qualité (certificat n° 25FOR02027.1) délivrée au titre de la catégorie : actions de formation.</div>
      ${footer(NAVY, WHITE)}</div>`] };
}


// ---------- Couverture Facebook (1640x624, zone sûre centrale) ----------
function fbCover() {
  const W = 1640, H = 624;
  return { name: 'couverture-facebook', W, H, pages: [
    `<div class="page" style="width:${W}px;height:${H}px;background:${NAVY};color:${WHITE};padding:0;align-items:center;text-align:center">
      ${network(W, H, GOLD, .18, 60, 3)}
      <div style="position:relative;display:flex;flex-direction:column;align-items:center">
        <div class="h" style="font-size:108px">L'IA, <span style="color:${GOLD}">simplement.</span></div>
        <div class="t" style="font-size:42px;margin-top:22px">L'IA sans jargon. Le droit sans migraine.</div>
        <div style="display:flex;gap:46px;margin-top:40px;align-items:center;justify-content:center">
          ${[['tools','Outils'],['shield','RGPD'],['scale','IA Act']].map(([k,w])=>`<div style="display:flex;align-items:center;gap:14px">${icon(k,70,GOLD,6)}<span class="h" style="font-size:40px">${w}</span></div>`).join('')}
        </div>
        <div class="t" style="font-size:26px;margin-top:36px;opacity:.95">Par YEBA FORMATIONS · yebaformations.re</div>
      </div></div>`] };
}

// ---------- Post de lancement (4:5) ----------
function launchPost() {
  const W = 1080, H = 1350;
  return { name: 'post_lancement', W, H, pages: [
    `<div class="page" style="width:${W}px;height:${H}px;background:${NAVY};color:${WHITE}">
      ${network(W, H, GOLD, .16, 40, 11)}
      <div style="position:relative">
        <div class="pill" style="background:${GOLD};color:${NAVY}">NOUVEAU · YEBA IA</div>
        <div class="h" style="font-size:132px;margin-top:50px">L'IA est simple.</div>
        <div class="h" style="font-size:104px;color:${GOLD};margin-top:10px">On vous l'a mal expliquée.</div>
        <div class="t" style="font-size:50px;margin-top:60px">1 vidéo = 1 problème = 1 solution</div>
      </div>
      <div class="foot" style="background:${GOLD};color:${NAVY};height:150px;font-size:48px;justify-content:center">Abonne-toi · YEBA IA</div></div>`] };
}

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const jobs = [carouselRCTF(), carouselRGPD(), carouselIAAct(), ...highlights(), ...reelCovers(), badge(), aboutPost(), fbCover(), launchPost()];
  for (const j of jobs) {
    const dir = path.join(OUT, j.name.split('_')[0]);
    fs.mkdirSync(dir, { recursive: true });
    for (let i = 0; i < j.pages.length; i++) {
      const page = await browser.newPage({ viewport: { width: j.W, height: j.H } });
      await page.setContent(`<html><head><style>${BASE}</style></head><body style="${j.transparent ? 'background:transparent' : ''}">${j.pages[i]}</body></html>`);
      await page.evaluate(() => document.fonts.ready);
      const suffix = j.pages.length > 1 ? `_${String(i + 1).padStart(2, '0')}` : '';
      await page.screenshot({ path: path.join(dir, `${j.name}${suffix}.png`), omitBackground: !!j.transparent });
      await page.close();
    }
  }
  await browser.close();
  console.log('ok', jobs.length);
})();
