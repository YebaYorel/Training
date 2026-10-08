import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';
const dir = path.dirname(new URL(import.meta.url).pathname);
const mode = process.argv[2], only = process.argv[3];
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
if (mode === 'photo') {
  const p = await b.newPage({ viewport: { width: 2400, height: 1600 } });
  await p.goto('file://' + dir + '/photo.html'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  await (await p.$('#photo')).screenshot({ path: dir + '/out/photo.png' });
} else {
  fs.rmSync(dir + '/frames', { recursive: true, force: true }); fs.mkdirSync(dir + '/frames');
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + dir + '/cardanim.html'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  const fps = 30, times = only ? only.split(',').map(Number) : [...Array(fps * 10).keys()].map(i => i / fps);
  const st = await p.$('#stage');
  for (let i = 0; i < times.length; i++) {
    await p.evaluate(t => setT(t), times[i]);
    
    await st.screenshot({ path: `${dir}/frames/f${String(i).padStart(4, '0')}.png` });
  }
}
await b.close();
