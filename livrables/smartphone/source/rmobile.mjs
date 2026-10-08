import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';
const dir = path.dirname(new URL(import.meta.url).pathname);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
for (const name of ['grille_mobile', 'catalogue_mobile']) {
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + dir + '/' + name + '.html');
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  await p.evaluate(() => { const over = s => { const f = s.querySelector('.foot'); return f && f.getBoundingClientRect().bottom > s.getBoundingClientRect().bottom - 84 + 3; };
    for (const s of document.querySelectorAll('.s.f')) for (const c of ['cpt', 'cpt2']) if (over(s)) s.classList.add(c); });
  await p.pdf({ path: `${dir}/out/${name}.pdf`, width: '1080px', height: '1920px', printBackground: true, preferCSSPageSize: true });
  const od = `${dir}/out/${name}`; fs.rmSync(od, { recursive: true, force: true }); fs.mkdirSync(od);
  const ss = await p.$$('.s');
  for (let i = 0; i < ss.length; i++) await ss[i].screenshot({ path: `${od}/${String(i + 1).padStart(2, '0')}.png` });
  const ov = await p.evaluate(() => [...document.querySelectorAll('.s')].map((s, i) => {
    const r = s.getBoundingClientRect(); const bad = [...s.querySelectorAll('*')].filter(e => { const q = e.getBoundingClientRect(); return q.height > 0 && (q.bottom > r.bottom + 1 || q.right > r.right + 1); });
    const f = s.querySelector('.foot'); const prev = f && f.previousElementSibling; const clash = f && prev && prev.getBoundingClientRect().bottom > f.getBoundingClientRect().top + 1;
    const lg = s.querySelector('.back .legal'); const cl = s.querySelector('.back .cl'); const c2 = lg && cl && cl.getBoundingClientRect().bottom > lg.getBoundingClientRect().top - 10; const cls=[...s.classList].filter(c=>c.startsWith('cpt')).join('+');
    return (bad.length || clash || c2 || cls) ? `écran ${i + 1}: ${bad.length} hors cadre${clash ? ', chevauchement pied' : ''}${c2 ? ', contact/mentions' : ''}${cls ? ' ['+cls+']' : ''}` : null; }).filter(Boolean));
  console.log(name, ss.length, ov);
  await p.close();
}
await b.close();
