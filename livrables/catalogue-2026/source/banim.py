import gen
css=open('style.css').read()
P=gen.pages(True)
P[0]=P[0].replace('class="page cover"','class="page cover wide"',1)
P[-1]=P[-1].replace('class="page back"','class="page back wide"',1).replace('viewBox="0 0 297 210"','viewBox="0 0 373.33 210"')
slots=''.join(f'<div class="slot{" w" if i in (0,len(P)-1) else ""}" id="s{i}">{p}</div>' for i,p in enumerate(P))
extra='''
html,body{background:#05080F}
#stage{position:relative;width:1920px;height:1080px;overflow:hidden;background:#05080F}
#bd{position:absolute;inset:-60px;background:url(clean2x.jpg) 50% 50%/cover;filter:blur(26px) saturate(1.1);opacity:.35}
#bdv{position:absolute;inset:0;background:radial-gradient(70% 70% at 50% 50%,rgba(5,8,15,.35),rgba(5,8,15,.92))}
.slot{position:absolute;left:196px;top:0;width:1527px;height:1080px;transform-origin:50% 50%;box-shadow:0 0 80px rgba(0,0,0,.7);opacity:0}
.slot.w{left:0;width:1920px;box-shadow:none}
.slot>.page{position:absolute;left:0;top:0;transform-origin:0 0;transform:scale(1.36068)}
.page.wide{width:373.33mm}
.cover.wide img.cimg{left:56.7mm;height:210mm;width:auto}
.back.wide .bimg{left:-1.1mm}
.back.wide .bflare{left:146.2mm}
.back.wide .bveil{left:122.2mm}
.back.wide .bburst{left:96.7mm}
.back.wide .blogo{left:160.2mm;transform-origin:50% 50%}
.gut{position:absolute;top:0;bottom:0;width:196px;display:flex;align-items:center;justify-content:center}
.gut span{writing-mode:vertical-rl;transform:rotate(180deg);font-family:Mono,monospace;font-size:15px;letter-spacing:.4em;color:rgba(226,196,110,.55);text-transform:uppercase}
.gut.r span{transform:none}
'''
js='''
const S=[...document.querySelectorAll('.slot')], N=S.length;
const START=[0]; const DUR=[7].concat(Array(N-2).fill(6.2)).concat([9]);
for(let i=1;i<N;i++) START.push(START[i-1]+DUR[i-1]);
const D=START[N-1]+DUR[N-1], X=.8;
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x)), span=(t,a,b)=>cl((t-a)/(b-a));
const ease=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2}, out=x=>1-Math.pow(1-cl(x),3);
const RV=S.map(s=>[...s.querySelectorAll('.rv')]);
const LAB=['','Sommaire','Pôle 01 · IA','Pôle 01 · IA','Pôle 02 · Automatisation','Pôle 03 · RGPD & IA Act','Pôle 04 · Vente & Management','Comment ça se passe','Tarifs',''];
const gl=document.getElementById('gl'), gr=document.getElementById('gr');
// traînées de la dernière page
const sk=document.getElementById('sk'); const VX=186.7, VY=118; const LINES=[];
let seed=7; const rnd=()=>{seed=(seed*16807)%2147483647;return seed/2147483647};
for(let k=0;k<40;k++){const a=rnd()*Math.PI*2; if(Math.sin(a)>.2&&Math.abs(Math.cos(a))<.35) continue;
  const L=260, l=document.createElementNS('http://www.w3.org/2000/svg','line');
  l.setAttribute('x1',VX);l.setAttribute('y1',VY);l.setAttribute('x2',VX+L*Math.cos(a));l.setAttribute('y2',VY+L*Math.sin(a)*.6);
  l.setAttribute('stroke',k%3?'#45D3F5':'#F3D98A');l.setAttribute('stroke-width',[.3,.45,.6][k%3]);l.setAttribute('stroke-dasharray',(3+rnd()*7).toFixed(1)+' 240');
  sk.appendChild(l); LINES.push([l,rnd()*250]);}
const cv=document.getElementById('cvid'), bimg=document.getElementById('bimg'), blogo=document.getElementById('blogo'), bb=document.getElementById('bburst');
async function setT(t){
  t=((t%D)+D)%D;
  for(let i=0;i<N;i++){
    const s=START[i], e=s+DUR[i];
    let o=0, lt=t-s;
    if(i===0 && t>D-X){ o=ease(span(t,D-X,D)); lt=0; }
    else if(t>=s-(i?X:0) && t<e){ o = i? ease(span(t,s-X,s)) : 1; if(t>e-X && i<N-1) o=Math.min(o,1); }
    if(i===N-1 && t>D-X) o=1-ease(span(t,D-X,D));
    S[i].style.opacity=o; S[i].style.display=o>0?'block':'none';
    if(o<=0) continue;
    const inn = i && i<N-1;
    const sl = i ? (1-ease(span(t,s-X,s)))*70 : 0;
    S[i].style.transform=`translateX(${t<s?sl:0}px) scale(${inn?1+.018*cl(lt/DUR[i]):1})`;
    if(i>0 && i<N-1) RV[i].forEach((el,j)=>{const k=out(span(lt,.15+j*.07,.75+j*.07)); el.style.opacity=k; el.style.transform=`translateY(${(1-k)*14}px)`;});
    if(i===N-1){ RV[i].forEach(el=>{el.style.opacity=1});
      const p=out(span(lt,.3,4.6));
      bimg.style.transform=`scale(${1+.14*p})`;
      blogo.style.transform=`scale(${.55+.45*p})`;
      const g=3+9*p+7*Math.exp(-Math.pow((lt-4.2)/.6,2));
      blogo.style.filter=`drop-shadow(0 0 ${g*.3}px rgba(255,214,120,.95)) drop-shadow(0 0 ${g}px rgba(255,190,90,.6))`;
      bb.style.opacity=.9*Math.exp(-Math.pow((lt-4.2)/.6,2))+.3*p; bb.style.transform=`rotate(${lt*5}deg) scale(${.8+.3*p})`;
      for(const [l,o0] of LINES) l.setAttribute('stroke-dashoffset',(o0-lt*120*(1+.5*p))%250);
    }
  }
  // gouttières : nom du pôle
  let cur=0; for(let i=0;i<N;i++) if(t>=START[i]) cur=i;
  gl.firstChild.textContent=gr.firstChild.textContent=LAB[cur]||'';
  const go=(cur>0&&cur<N-1)? ease(span(t-START[cur],0,.6)) : 0; gl.style.opacity=gr.style.opacity=go;
  // vidéo de couverture
  if(S[0].style.opacity>0){
    const lt0 = t>D-X ? 0 : t;
    const f=Math.min(145,1+Math.floor(lt0*24)), src='vf/f'+String(f).padStart(3,'0')+'.jpg';
    if(!cv.src.endsWith(src)){cv.src=src; await cv.decode();}
  }
}
window.setT=setT; window.D=D; setT(0);
'''
html=('<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Catalogue 2026 animé — YEBA FORMATIONS</title><style>'+css+extra+'</style></head><body>'
 '<div id="stage"><div id="bd"></div><div id="bdv"></div><div class="gut" id="gl" style="left:0"><span>x</span></div><div class="gut r" id="gr" style="right:0"><span>x</span></div>'+slots+'</div>'
 '<script>'+js+'</script></body></html>')
open('catalogue_anim.html','w').write(html)
