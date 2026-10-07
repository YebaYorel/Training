import { chromium } from 'playwright';
import path from 'path';
const dir = path.dirname(new URL(import.meta.url).pathname);
const out = process.argv[2] || dir;
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' }).catch(() => chromium.launch());
const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
await p.goto('file://' + dir + '/grille.html');
await p.evaluate(() => document.fonts.ready);
await p.waitForTimeout(300);
await p.pdf({ path: out + '/grille.pdf', width: '210mm', height: '297mm', printBackground: true, preferCSSPageSize: true });
const pages = await p.$$('.page');
for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: `${dir}/preview-${i + 1}.png` });
// overflow check
const ov = await p.evaluate(() => [...document.querySelectorAll('.page *')].filter(e => e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).overflow === 'visible' && e.clientWidth > 0).map(e => e.className + ':' + e.textContent.slice(0, 30)).slice(0, 10));
console.log('overflow', ov);
await b.close();
