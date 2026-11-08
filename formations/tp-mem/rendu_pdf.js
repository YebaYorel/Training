// Convertit des fichiers HTML en PDF (Chromium préinstallé). Usage : node rendu_pdf.js a.html a.pdf [b.html b.pdf ...]
const { chromium } = require('playwright');
(async () => {
  const args = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (let i = 0; i < args.length; i += 2) {
    await page.goto('file://' + require('path').resolve(args[i]), { waitUntil: 'load' });
    const paysage = (await page.evaluate(() => document.body.dataset.orientation)) === 'paysage';
    await page.pdf({
      path: args[i + 1], format: 'A4', landscape: paysage, printBackground: true,
      margin: { top: '16mm', bottom: '18mm', left: '15mm', right: '15mm' },
      displayHeaderFooter: true, headerTemplate: '<span></span>',
      footerTemplate: '<div style="font-family:Arial;font-size:10px;width:100%;text-align:center;color:#333">' +
        document_title(args[i]) + ' · page <span class="pageNumber"></span> / <span class="totalPages"></span></div>'
    });
    console.log('PDF', args[i + 1]);
  }
  await browser.close();
})();
function document_title(p) {
  return 'TP Manager d’établissement marchand · ' + require('path').basename(p, '.html').replace(/_/g, ' ');
}
