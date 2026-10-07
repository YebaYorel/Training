import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';
const dir = path.dirname(new URL(import.meta.url).pathname);
const fps = +(process.env.FPS || 25), D = 14, only = process.argv[2];
fs.rmSync(dir + '/frames', { recursive: true, force: true }); fs.mkdirSync(dir + '/frames');
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: 640, height: 960 }, deviceScaleFactor: +(process.env.DSF || 2) });
await p.goto('file://' + dir + '/anim.html#capture' + (process.env.LITE ? '-lite' : ''));
await p.evaluate(() => document.fonts.ready);
await p.waitForTimeout(400);
const stage = await p.$('#stage');
const times = only ? only.split(',').map(Number) : [...Array(fps * D).keys()].map(i => i / fps);
for (let i = 0; i < times.length; i++) {
  await p.evaluate(t => setT(t), times[i]);
  await stage.screenshot({ path: `${dir}/frames/f${String(i).padStart(4, '0')}.png` });
}
await b.close();
console.log('frames', times.length);
