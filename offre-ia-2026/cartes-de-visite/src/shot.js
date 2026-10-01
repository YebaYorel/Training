const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const p=await b.newPage({viewport:{width:2420,height:1000},deviceScaleFactor:1});
await p.goto('file://'+__dirname+'/'+process.argv[2]);await p.waitForTimeout(800);
await p.screenshot({path:process.argv[3],fullPage:true});await b.close();})();
