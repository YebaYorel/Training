import { chromium } from 'playwright';
import path from 'path';
const dir = path.dirname(new URL(import.meta.url).pathname);
const out = process.argv[2] || dir;
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: 1400, height: 1000 }, deviceScaleFactor: 1 });
await p.goto('file://' + dir + '/card.html');
// Faces à plat, 85 x 55 mm à 600 dpi (1 mm = 23,622 px), coins droits
await p.evaluate(() => build('flat', { mm: 23.622 }));
await (await p.$('#tr')).screenshot({ path: out + '/recto-600dpi.png' });
await (await p.$('#tv')).screenshot({ path: out + '/verso-600dpi.png' });
// PDF imprimeur : 2 pages 91 x 61 mm, fond perdu 3 mm
const p2 = await b.newPage();
await p2.goto('file://' + dir + '/card.html');
await p2.evaluate(() => build('print'));
await p2.pdf({ path: out + '/carte-impression.pdf', width: '91mm', height: '61mm', printBackground: true, preferCSSPageSize: true });
await b.close();
