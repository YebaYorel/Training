# Versions smartphone ANIMÉES (1080 x 1920) — mêmes écrans que mobile.py, enchaînés comme un défilement de téléphone
import sys
from mobile import grille, catalogue

EXTRA = '''
html,body{background:#05080F;overflow:hidden}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;background:#05080F}
#stage>.s{position:absolute;left:0;top:0;will-change:transform,opacity}
.swipe{display:none}
.sk{position:absolute;left:0;top:0;width:1080px;pointer-events:none;mix-blend-mode:screen}
.halo{position:absolute;border-radius:50%;pointer-events:none;mix-blend-mode:screen;
  background:radial-gradient(closest-side,rgba(255,214,120,.55),rgba(255,190,90,.18) 45%,transparent)}
.prog{position:absolute;left:72px;right:72px;top:40px;height:5px;display:flex;gap:6px;z-index:9}
.prog i{flex:1;background:rgba(255,255,255,.18);position:relative;overflow:hidden}
.prog i b{position:absolute;inset:0;background:var(--gold);transform-origin:0 50%}
'''

JS = r'''
const S=[...document.querySelectorAll('#stage>.s')], N=S.length;
// fiches trop longues : même resserrage que la version PDF
const over=s=>{const f=s.querySelector('.foot');return f&&f.getBoundingClientRect().bottom>s.getBoundingClientRect().bottom-84+3};
for(const s of S) if(s.classList.contains('f')) for(const c of ['cpt','cpt2']) if(over(s)) s.classList.add(c);
const DUR=S.map((s,i)=>i===0?COVER:(i===N-1?LAST:HOLD));
const START=[0]; for(let i=1;i<N;i++) START.push(START[i-1]+DUR[i-1]);
const D=START[N-1]+DUR[N-1], X=.7;
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x)), span=(t,a,b)=>cl((t-a)/(b-a));
const ease=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2}, out=x=>1-Math.pow(1-cl(x),3);
const SEL='.top,.kick,h1,h2,.sub,.lead,.pill,.chips span,.meta span,.lbl,.txt,.f li,.legend,.box,.row,.consult li,.fact,.cta,.tile,.steps li,.price>div,.fin span,.note,.legal,.foot,.name,.role,.cl>div,.tiles+.legend';
const RV=S.map(s=>[...s.querySelectorAll(SEL)]);
// barre de progression façon « story »
const pg=document.createElement('div'); pg.className='prog'; pg.innerHTML='<i><b></b></i>'.repeat(N); document.getElementById('stage').appendChild(pg);
const PB=[...pg.querySelectorAll('b')];
// traînées lumineuses depuis le point de fuite (couverture et dernier écran)
let seed=11; const rnd=()=>{seed=(seed*16807)%2147483647;return seed/2147483647};
function streaks(s,vx,vy,h){
  const ns='http://www.w3.org/2000/svg', sv=document.createElementNS(ns,'svg');
  sv.setAttribute('class','sk'); sv.setAttribute('viewBox',`0 0 1080 ${h}`); sv.style.height=h+'px';
  const L=[]; for(let k=0;k<46;k++){const a=rnd()*Math.PI*2; if(Math.sin(a)<-.85) continue;
    const l=document.createElementNS(ns,'line'), R=1400;
    l.setAttribute('x1',vx);l.setAttribute('y1',vy);l.setAttribute('x2',vx+R*Math.cos(a));l.setAttribute('y2',vy+R*Math.sin(a)*.75);
    l.setAttribute('stroke',k%3?'#45D3F5':'#F3D98A');l.setAttribute('stroke-width',[1.2,2,2.8][k%3]);l.setAttribute('stroke-linecap','round');
    l.setAttribute('stroke-dasharray',`${(30+rnd()*90).toFixed(0)} 1400`); l.style.opacity=.35+rnd()*.5;
    sv.appendChild(l); L.push([l,rnd()*1400,.7+rnd()*.8]);}
  s.querySelector('.img').after(sv); return L;}
const C=S[0], CI=C.querySelector('.img'), CL=C.querySelector('.logo'), CS=streaks(C,540,505,1150);
const ch=document.createElement('div'); ch.className='halo'; Object.assign(ch.style,{left:'290px',top:'255px',width:'500px',height:'500px'}); CI.after(ch);
const B=S[N-1].classList.contains('back')?S[N-1]:null, BI=B&&B.querySelector('.img'), BL=B&&B.querySelector('.blogo'), BB=B&&B.querySelector('.burst'), BS=B?streaks(B,540,600,1240):[];
function setT(t){
  t=cl(t,0,D-1e-4);
  let cur=0; for(let i=0;i<N;i++) if(t>=START[i]-X) cur=i;
  for(let i=0;i<N;i++){
    const s=S[i], st=START[i];
    let show=false, tx=0, op=1;
    if(i===cur){ show=true; if(i>0 && t<st){ tx=(1-ease(span(t,st-X,st)))*1080; } }
    else if(i===cur-1 && t<START[cur]){ show=true; const e=ease(span(t,START[cur]-X,START[cur])); tx=-e*320; op=1-.65*e; }
    s.style.display=show?'flex':'none'; if(!show) continue;
    s.style.transform=`translateX(${tx.toFixed(1)}px)`; s.style.opacity=op;
    const lt=Math.max(0,t-st), base=i===0?.5:.25, step=i===0?.12:Math.min(.07,1.5/Math.max(1,RV[i].length));
    RV[i].forEach((el,j)=>{const k=out(span(lt,base+j*step,base+j*step+.55)); el.style.opacity=k; el.style.transform=`translateY(${((1-k)*22).toFixed(1)}px)`;});
    if(i===0){ const p=span(lt,0,COVER+X);
      CI.style.transform=`scale(${1+.07*p})`; CI.style.transformOrigin='50% 44%';
      for(const [l,o,v] of CS) l.setAttribute('stroke-dashoffset',(-(o+lt*900*v)%1400).toFixed(0));
      const pulse=.55+.45*Math.sin(lt*2.4); ch.style.opacity=.35+.4*pulse;
      const k=out(span(lt,.2,1.4)); CL.style.opacity=k; CL.style.transform=`translateX(-50%) scale(${.85+.15*k})`;
      CL.style.filter=`drop-shadow(0 0 ${(4+10*pulse).toFixed(1)}px rgba(255,214,120,.6))`; }
    if(i===N-1&&B){ const p=out(span(lt,.2,4.2)), fl=Math.exp(-Math.pow((lt-3.6)/.55,2));
      BI.style.transform=`scale(${1+.12*p})`; BI.style.transformOrigin='50% 30%';
      BL.style.transform=`translateX(-50%) scale(${.55+.45*p})`;
      const g=4+10*p+12*fl; BL.style.filter=`drop-shadow(0 0 ${(g*.35).toFixed(1)}px rgba(255,214,120,.95)) drop-shadow(0 0 ${g.toFixed(1)}px rgba(255,190,90,.6))`;
      BB.style.opacity=(.85*fl+.35*p).toFixed(3); BB.style.transform=`rotate(${lt*6}deg) scale(${.8+.3*p})`;
      for(const [l,o,v] of BS) l.setAttribute('stroke-dashoffset',(-(o+lt*700*v*(1+.6*p))%1400).toFixed(0)); }
  }
  PB.forEach((b,i)=>{b.style.transform=`scaleX(${span(t,START[i],START[i]+DUR[i]).toFixed(4)})`;});
}
window.setT=setT; window.D=D; setT(0);
'''

def build(name, html, cover, hold, last, title):
    head, rest = html.split('<body>', 1)
    body = rest.rsplit('</body>', 1)[0]
    head = head.replace('</style>', EXTRA + '</style>').replace('<title>', '<title>' + title + ' — ', 1)
    js = f'const COVER={cover},HOLD={hold},LAST={last};' + JS
    open(name, 'w').write(f'{head}<body><div id="stage">{body}</div><script>{js}</script></body></html>')

if __name__ == '__main__':
    build('grille_mobile_anim.html', grille(), 6, 8, 9, 'animé')
    build('catalogue_mobile_anim.html', catalogue(), 6, 6.5, 9, 'animé')
