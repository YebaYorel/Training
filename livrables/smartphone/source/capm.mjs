import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';
const dir = path.dirname(new URL(import.meta.url).pathname);
const [name, only] = process.argv.slice(2); const fps = +(process.env.FPS || 25);
const fr = `${dir}/mframes_${name}`; if (!only) { fs.rmSync(fr, { recursive: true, force: true }); fs.mkdirSync(fr); }
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto(`file://${dir}/${name}_anim.html`);
await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(600);
const D = await p.evaluate(() => window.D); console.log(name, 'durée', D);
const times = only ? only.split(',').map(Number) : [...Array(Math.round(fps * D)).keys()].map(i => i / fps);
for (let i = 0; i < times.length; i++) {
  await p.evaluate(t => new Promise(r => { setT(t); requestAnimationFrame(() => requestAnimationFrame(r)); }), times[i]);
  await p.screenshot({ path: only ? `${dir}/out/chk_${name}_${times[i]}.jpg` : `${fr}/f${String(i).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 93 });
}
await b.close();
