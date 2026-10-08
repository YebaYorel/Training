import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';
const dir = path.dirname(new URL(import.meta.url).pathname);
const fps = +(process.env.FPS || 25), only = process.argv[2];
const fr = dir + '/aframes'; fs.rmSync(fr, { recursive: true, force: true }); fs.mkdirSync(fr);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
await p.goto('file://' + dir + '/catalogue_anim.html');
await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(600);
const D = await p.evaluate(() => window.D); console.log('durée', D);
const times = only ? only.split(',').map(Number) : [...Array(Math.round(fps * D)).keys()].map(i => i / fps);
const st = await p.$('#stage');
for (let i = 0; i < times.length; i++) {
  await p.evaluate(async t => { await setT(t); await new Promise(r => requestAnimationFrame(() => r())); }, times[i]);
  await st.screenshot({ path: `${fr}/f${String(i).padStart(5, '0')}.png` });
}
await b.close();
