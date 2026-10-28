// Génère toutes les pièces Word du dossier dans ../word
const path = require('path');
const fs = require('fs');
const { build } = require('./lib');
const only = process.argv[2];
const files = fs.readdirSync(__dirname).filter((f) => /^p\d+\.js$/.test(f)).sort();
(async () => {
  for (const f of files) {
    const d = require('./' + f);
    if (only && d.num !== only) continue;
    const out = path.join(__dirname, '..', 'word', `${d.slug}.docx`);
    await build({ ...d, file: out });
    console.log('OK', out);
  }
})().catch((e) => { console.error(e); process.exit(1); });
