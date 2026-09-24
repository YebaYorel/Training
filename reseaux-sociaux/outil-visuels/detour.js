// Détoure le logo : les pixels proches de la couleur de fond deviennent transparents.
const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});const p=await b.newPage();
const src='data:image/jpeg;base64,'+fs.readFileSync('logo.jpg').toString('base64');
const out=await p.evaluate(async(src)=>{const im=new Image();im.src=src;await im.decode();const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const x=c.getContext('2d');x.drawImage(im,0,0);
const d=x.getImageData(0,0,c.width,c.height),a=d.data;const bg=[a[0],a[1],a[2]];
for(let i=0;i<a.length;i+=4){const dist=Math.hypot(a[i]-bg[0],a[i+1]-bg[1],a[i+2]-bg[2]);a[i+3]=Math.max(0,Math.min(255,(dist-18)*255/70));}
x.putImageData(d,0,0);return c.toDataURL('image/png');},src);
fs.writeFileSync('logo-transparent.png',Buffer.from(out.split(',')[1],'base64'));await b.close();})();
