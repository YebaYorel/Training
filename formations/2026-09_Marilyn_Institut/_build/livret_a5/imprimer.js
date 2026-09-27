// Imprime le livret HTML en PDF A5 avec Chromium et signale toute page dont le contenu déborde.
const path = require('path');
const { chromium } = require(require.resolve('playwright', { paths: ['/tmp/claude-0', process.cwd()] }));
(async () => {
  const [src, dst] = process.argv.slice(2);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const p = await b.newPage();
  await p.goto('file://' + path.resolve(src));
  await p.evaluate(() => document.fonts.ready);
  const deb = await p.evaluate(() => [...document.querySelectorAll('.page')].map((s, i) => {
    const bas = s.getBoundingClientRect().bottom - 12 * 3.78; // marge basse (numéro de page)
    let max = 0; s.querySelectorAll('*').forEach(el => { if (!el.classList.contains('num')) max = Math.max(max, el.getBoundingClientRect().bottom); });
    return max > bas ? i + 1 : null; }).filter(Boolean));
  if (deb.length) console.log('DEBORDEMENT pages', deb.join(', '));
  await p.pdf({ path: dst, width: '148mm', height: '210mm', printBackground: true, preferCSSPageSize: true });
  await b.close();
})();
