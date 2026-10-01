// Capture d'une page HTML locale en PNG : node capture.js page.html sortie.png largeur hauteur
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const [, , page, sortie, l, h] = process.argv;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: +l, height: +h } });
  await p.goto('file://' + page);
  await p.waitForTimeout(700);
  await p.screenshot({ path: sortie });
  await b.close();
})();
