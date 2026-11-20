// Générateur de factures / devis YEBA FORMATIONS (PDF, charte YEBA).
// Usage : node site/scripts/factures/generer.cjs donnees.json sortie.pdf
// Les données réelles (client, IBAN) restent HORS du dépôt public : dossier donnees/ ignoré par Git.
const fs = require('fs')
const path = require('path')
const { chromium } = require('playwright')

const [, , source, sortie] = process.argv
const d = JSON.parse(fs.readFileSync(source, 'utf8'))
const ICI = __dirname
const font = (f) => 'data:font/woff2;base64,' + fs.readFileSync(f).toString('base64')
const RACINE = path.join(__dirname, '..', '..', '..')
const MONT = path.join(RACINE, 'node_modules/@fontsource/montserrat/files/montserrat-latin-')
const INTER = path.join(__dirname, 'polices/inter-latin-')
const LOGO = 'data:image/png;base64,' + fs.readFileSync(path.join(RACINE, 'site/scripts/documents-pdf/logo-yeba.png')).toString('base64')
const eur = (n) => n.toLocaleString('fr-FR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).replace(/[\u202f\u00a0]/g, '\u00a0') + '\u00a0€'
const h = (n) => (n ? `${String(n).replace('.', ',')} h` : '—')
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;')

let totalHT = 0
let prevues = 0
let realisees = 0
const blocs = d.blocs.map((b) => {
  let sous = 0
  const lignes = b.lignes.map((l) => {
    const montant = l.realisees * b.taux
    sous += montant
    prevues += l.prevues
    realisees += l.realisees
    const fait = l.realisees > 0
    return `<tr class="${fait ? '' : 'non'}">
      <td class="date">${esc(l.date)}<span class="pastille ${fait ? 'ok' : 'ko'}">${fait ? 'Réalisée' : 'Non réalisée — non facturée'}</span></td>
      <td class="intitule">${esc(l.intitule || '')}</td>
      <td class="c">${h(l.prevues)}</td>
      <td class="c">${fait ? h(l.realisees) : '0 h'}</td>
      <td class="r">${fait ? eur(b.taux) : '—'}</td>
      <td class="r montant">${eur(montant)}</td>
    </tr>`
  })
  totalHT += sous
  return `<section class="bloc">
    <div class="bloc-tete">
      <div><h3>${esc(b.titre)}</h3><p>${esc(b.detail)}</p></div>
      <p class="contrat">${esc(b.contrat)}</p>
    </div>
    <table>
      <colgroup><col style="width:24%"><col><col style="width:8%"><col style="width:9%"><col style="width:9%"><col style="width:11%"></colgroup>
      <thead><tr><th>Date contractuelle</th><th>Intitulé de l’action de formation</th><th class="c">Prévues</th><th class="c">Réalisées</th><th class="r">Taux HT</th><th class="r">Montant HT</th></tr></thead>
      <tbody>${lignes.join('')}</tbody>
      <tfoot><tr><td colspan="5">Sous-total ${esc(b.titre)}</td><td class="r">${eur(sous)}</td></tr></tfoot>
    </table>
  </section>`
})

const reseau = `<svg class="reseau" viewBox="0 0 260 120" aria-hidden="true">${[[20,30],[70,15],[120,45],[170,20],[220,50],[60,80],[140,95],[200,100],[245,15]].map(([x,y],i,a)=>a.slice(i+1).filter(([u,v])=>Math.hypot(u-x,v-y)<75).map(([u,v])=>`<line x1="${x}" y1="${y}" x2="${u}" y2="${v}"/>`).join('')).join('')}${[[20,30],[70,15],[120,45],[170,20],[220,50],[60,80],[140,95],[200,100],[245,15]].map(([x,y])=>`<circle cx="${x}" cy="${y}" r="3.2"/>`).join('')}</svg>`

const html = `<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>${esc(d.type)} ${esc(d.numero)}</title><style>
@font-face{font-family:Montserrat;font-weight:700;src:url(${font(MONT + '700-normal.woff2')})}
@font-face{font-family:Montserrat;font-weight:800;src:url(${font(MONT + '800-normal.woff2')})}
@font-face{font-family:Montserrat;font-weight:900;src:url(${font(MONT + '900-normal.woff2')})}
@font-face{font-family:Inter;font-weight:400;src:url(${font(INTER + '400-normal.woff2')})}
@font-face{font-family:Inter;font-weight:500;src:url(${font(INTER + '500-normal.woff2')})}
@font-face{font-family:Inter;font-weight:600;src:url(${font(INTER + '600-normal.woff2')})}
@font-face{font-family:Inter;font-weight:700;src:url(${font(INTER + '700-normal.woff2')})}
:root{--bleu:#1B3A6B;--or:#C9AB4C;--noir:#121212;--gris:#5b6472;--trait:#e3e7ee;--fond:#f5f7fb}
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,sans-serif;color:var(--noir);font-size:8.8pt;line-height:1.38;width:210mm;height:297mm;overflow:hidden;position:relative;background:#fff}
.liseret{position:absolute;left:0;top:0;bottom:0;width:7mm;background:linear-gradient(180deg,var(--bleu) 0%,var(--bleu) 72%,var(--or) 72%,var(--or) 100%)}
.page{padding:9mm 13mm 14mm 18mm;zoom:.86}
header{display:flex;justify-content:space-between;align-items:flex-start}
header img{width:23mm}
.titre{text-align:right}
.titre h1{font-family:Montserrat;font-weight:900;font-size:27pt;letter-spacing:.06em;color:var(--bleu);line-height:1}
.titre .num{display:inline-block;margin-top:2mm;background:var(--bleu);color:#fff;font-family:Montserrat;font-weight:800;font-size:11pt;padding:1.6mm 4mm;border-radius:2mm;letter-spacing:.04em}
.titre .num b{color:var(--or)}
.meta{margin-top:2.5mm;color:var(--gris);font-size:8.6pt}
.meta strong{color:var(--noir)}
.bandeau{margin-top:4mm;background:var(--bleu);color:#fff;border-radius:3mm;display:grid;grid-template-columns:1fr 1fr;position:relative;overflow:hidden}
.bandeau>div{padding:3.6mm 5mm}
.bandeau>div+div{border-left:1px solid rgba(201,171,76,.45)}
.bandeau .etiquette{font-family:Montserrat;font-weight:800;font-size:7.4pt;letter-spacing:.18em;color:var(--or);text-transform:uppercase;margin-bottom:1.5mm}
.bandeau h2{font-family:Montserrat;font-weight:800;font-size:12pt;margin-bottom:1mm}
.bandeau p{font-size:8.2pt;opacity:.95;line-height:1.3}
.bandeau .petit{font-size:7.6pt;opacity:.8;margin-top:.8mm}
.reseau{position:absolute;right:-8mm;bottom:-6mm;width:70mm;opacity:.18}
.reseau line{stroke:var(--or);stroke-width:1}.reseau circle{fill:var(--or)}
.objet{margin-top:3.5mm;font-family:Montserrat;font-weight:700;font-size:10.5pt;color:var(--bleu);border-left:2.5mm solid var(--or);padding:1mm 0 1mm 3mm}
.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm;margin-top:3.5mm}
.kpi{display:flex;align-items:baseline;gap:2.5mm;background:var(--fond);border-radius:2.5mm;padding:1.6mm 4mm;border-top:1.2mm solid var(--bleu)}
.kpi strong{font-family:Montserrat;font-weight:900;font-size:14pt;color:var(--bleu)}
.kpi span{font-size:8pt;color:var(--gris)}
.kpi.alerte{border-top-color:var(--or)}
.bloc{margin-top:3.5mm;break-inside:avoid}
.bloc-tete{display:flex;justify-content:space-between;align-items:flex-end;gap:5mm;margin-bottom:1.4mm}
.bloc h3{font-family:Montserrat;font-weight:800;font-size:11pt;color:var(--bleu)}
.bloc-tete p{font-size:7.6pt;color:var(--gris)}
.bloc-tete .contrat{white-space:nowrap;font-weight:600;color:var(--noir)}
table{width:100%;border-collapse:collapse}
th{white-space:nowrap;font-family:Montserrat;font-weight:700;font-size:7.2pt;letter-spacing:.08em;text-transform:uppercase;color:var(--bleu);background:var(--or);padding:1.5mm 2.5mm;text-align:left}
th:first-child{border-radius:1.5mm 0 0 0}th:last-child{border-radius:0 1.5mm 0 0}
td{padding:1.1mm 2mm;border-bottom:1px solid var(--trait);vertical-align:middle}
.c{text-align:center}.r{text-align:right}
td.date{font-weight:600}
td.montant{font-weight:700}
tr.non td{color:#6b7280}
tr.non td:first-child{box-shadow:inset 1mm 0 0 var(--or)}
td.intitule{font-size:7.9pt;line-height:1.3}
.pastille{display:block;width:max-content;margin-top:.8mm;font-size:6.9pt;font-weight:700;padding:.3mm 2mm;border-radius:10mm;white-space:nowrap;background:#fff}
.pastille.ok{color:var(--bleu);border:1px solid var(--bleu)}
.pastille.ko{color:#5b6472;border:1px solid var(--or)}
tfoot td{font-weight:700;background:var(--fond);border-bottom:0}
.bas{display:grid;grid-template-columns:1.25fr 1fr;gap:6mm;margin-top:5mm;break-inside:avoid}
.paiement{background:var(--fond);border-radius:3mm;padding:3mm 4.5mm;font-size:8.2pt}
.paiement h4{font-family:Montserrat;font-weight:800;font-size:9pt;color:var(--bleu);margin-bottom:1.5mm;letter-spacing:.04em}
.paiement .iban{font-family:Montserrat;font-weight:700;font-size:9.6pt;letter-spacing:.04em;margin:1mm 0}
.totaux{border-radius:3mm;overflow:hidden;border:1px solid var(--trait)}
.totaux div{display:flex;justify-content:space-between;padding:1.8mm 4mm;font-size:8.8pt}
.totaux div+div{border-top:1px solid var(--trait)}
.totaux .tva{font-size:8pt;color:var(--gris)}
.totaux .net{background:var(--bleu);color:#fff;padding:3mm 4mm}
.totaux .net span{font-family:Montserrat;font-weight:800;letter-spacing:.06em;text-transform:uppercase;font-size:9pt;align-self:center}
.totaux .net strong{font-family:Montserrat;font-weight:900;font-size:19pt;color:var(--or)}
.conditions{margin-top:3.5mm;font-size:7.3pt;color:var(--gris);display:grid;gap:.8mm}
footer{position:absolute;left:18mm;right:13mm;bottom:7mm;border-top:1px solid var(--trait);padding-top:2.5mm;display:flex;justify-content:space-between;font-size:7.4pt;color:var(--gris)}
footer b{color:var(--bleu);font-family:Montserrat;font-weight:800;letter-spacing:.08em}
</style></head><body>
<div class="liseret"></div>
<div class="page">
<header>
  <img src="${LOGO}" alt="YEBA FORMATIONS">
  <div class="titre"><h1>${esc(d.type)}</h1><div class="num">N° <b>${esc(d.numero)}</b></div>
  <p class="meta">Émise le <strong>${esc(d.date)}</strong> · Échéance : <strong>${esc(d.echeance)}</strong></p></div>
</header>
<div class="bandeau">
  <div><p class="etiquette">Émetteur</p><h2>${esc(d.emetteur.nom)}</h2><p>${esc(d.emetteur.titulaire)}</p>${d.emetteur.lignes.map((l) => `<p>${esc(l)}</p>`).join('')}<p class="petit">${d.emetteur.contact.map(esc).join(' · ')}</p><p class="petit">${d.emetteur.legal.map(esc).join('<br>')}</p></div>
  <div><p class="etiquette">Facturé à</p><h2>${esc(d.client.nom)}</h2>${d.client.attention ? `<p>${esc(d.client.attention)}</p>` : ""}${d.client.lignes.map((l) => `<p>${esc(l)}</p>`).join('')}<p class="petit">${d.client.legal.map(esc).join('<br>')}</p></div>
  ${reseau}
</div>
<p class="objet">${esc(d.objet)}</p>
<div class="kpis">
  <div class="kpi"><strong>${h(prevues)}</strong><span>prévues aux contrats</span></div>
  <div class="kpi"><strong>${h(realisees)}</strong><span>réalisées et facturées</span></div>
  <div class="kpi alerte"><strong>${String(prevues - realisees).replace(".", ",")}&nbsp;h</strong><span>non réalisées — non facturées</span></div>
</div>
${blocs.join('')}
<div class="bas">
  <div class="paiement"><h4>RÈGLEMENT PAR ${esc(d.paiement.mode.toUpperCase())}</h4>
    <p>Titulaire : ${esc(d.paiement.titulaire)}</p><p class="iban">IBAN ${esc(d.paiement.iban)}</p><p>BIC ${esc(d.paiement.bic)}</p>
    <p style="margin-top:1.5mm">Merci d’indiquer la référence <strong>${esc(d.numero)}</strong> dans le libellé du virement.</p></div>
  <div class="totaux">
    <div><span>Total heures facturées</span><span>${h(realisees)}</span></div>
    <div><span>Total HT</span><span>${eur(totalHT)}</span></div>
    <div class="tva"><span>${esc(d.tva)}</span><span>0,00 €</span></div>
    <div class="net"><span>Net à payer</span><strong>${eur(totalHT)}</strong></div>
  </div>
</div>
<div class="conditions">${d.conditions.map((c) => `<p>${esc(c)}</p>`).join('')}</div>
</div>
<footer><span><b>YEBA FORMATIONS</b> · Organisme de formation · Sainte-Clotilde, La Réunion</span><span>${esc(d.type)} ${esc(d.numero)} · page 1/1</span></footer>
</body></html>`

;(async () => {
  fs.writeFileSync(sortie.replace(/\.pdf$/, '.html'), html)
  const b = await chromium.launch()
  const p = await b.newPage()
  await p.setContent(html, { waitUntil: 'networkidle' })
  await p.evaluate(() => document.fonts.ready)
  await p.pdf({ path: sortie, format: 'A4', printBackground: true, preferCSSPageSize: true })
  await p.setViewportSize({ width: 794, height: 1123 })
  await p.screenshot({ path: sortie.replace(/\.pdf$/, '.png'), fullPage: true })
  await b.close()
  console.log(JSON.stringify({ totalHT, prevues, realisees }))
})()
