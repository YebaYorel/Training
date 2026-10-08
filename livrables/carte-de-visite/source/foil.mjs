import { chromium } from 'playwright';
import path from 'path';
const dir = path.dirname(new URL(import.meta.url).pathname);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage();
await p.goto('file://' + dir + '/card.html');
await p.evaluate(() => build('foil'));
await p.pdf({ path: dir + '/out/carte-dorure-verso.pdf', width: '91mm', height: '61mm', printBackground: true });
await b.close();
