"""Jeu-quiz projeté, en équipes — un seul fichier HTML, sans internet, sans compte, sans aucune collecte.

Pourquoi pas Kahoot / Wooclap / Mentimeter ?  Ils demandent aux stagiaires un téléphone, une connexion et souvent
un pseudo ou un compte : autant de données personnelles envoyées à un tiers, parfois hors UE. Ici, rien ne sort
de l'ordinateur du formateur : c'est la solution la plus sobre au regard du RGPD (minimisation, art. 5.1.c)
et elle fonctionne même si le Wi-Fi du C.R.E.P.S est capricieux. Les équipes répondent avec les cartons A / B / C du kit.
"""
import json

import donnees as D
from quiz_data import QUIZ

GABARIT = r"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Quiz — Marilyn Institut</title>
<style>
:root{--bleu:#1B3A6B;--bleuf:#12284C;--or:#C9A84C;--orc:#F4EDDA;--noir:#121212;--casse:#F7F7F5;--vert:#1E6B3A;--rouge:#A31E1E}
*{box-sizing:border-box}html,body{margin:0;height:100%;font-family:Verdana,"DejaVu Sans",Arial,sans-serif;background:var(--casse);color:var(--noir)}
button{font-family:inherit;cursor:pointer}
.ecran{display:none;height:100vh;padding:2.5vh 4vw;flex-direction:column;overflow:hidden}.actif{display:flex}
.bandeau{display:flex;justify-content:space-between;align-items:center;gap:2vw;margin-bottom:1.2vh}
.equipes{display:flex;gap:1.5vw}
.eq{background:var(--bleu);color:#fff;border-radius:14px;padding:1vh 1.5vw;font-size:clamp(18px,2.2vw,34px);font-weight:700;display:flex;align-items:center;gap:1vw}
.eq b{color:var(--or);font-size:1.3em}.eq button{background:var(--or);color:var(--bleuf);border:0;border-radius:8px;font-size:.8em;font-weight:700;padding:.2em .6em}
.num{font-size:clamp(18px,2vw,30px);color:#5A5F6A;font-weight:700}
.theme{display:inline-block;background:var(--orc);border:2px solid var(--or);border-radius:10px;padding:.3em .8em;font-size:clamp(18px,1.8vw,28px);font-weight:700;color:var(--bleu)}
h1{font-size:min(3.6vw,6.2vh);color:var(--bleu);margin:1.5vh 0 2vh;line-height:1.2}
.choix{display:grid;gap:1.4vh}
.c{display:flex;align-items:center;gap:2vw;background:#fff;border:3px solid #D5DAE2;border-radius:18px;padding:1.2vh 2vw;font-size:min(2.7vw,4.6vh);text-align:left}
.c .l{flex:0 0 auto;width:1.6em;height:1.6em;border-radius:12px;background:var(--bleu);color:var(--or);display:flex;align-items:center;justify-content:center;font-weight:900}
.c.bon{border-color:var(--vert);background:#E7F3EA}.c.bon .l{background:var(--vert);color:#fff}
.c.faux{opacity:.45}
.c .tag{margin-left:auto;font-weight:700;color:var(--vert);white-space:nowrap}
.expl{display:none;margin-top:1.6vh;background:var(--bleu);color:#fff;border-radius:18px;padding:1.4vh 2vw;font-size:min(2vw,3.5vh);line-height:1.3}
.expl.v{display:block}
.pied{margin-top:auto;display:flex;justify-content:space-between;align-items:center;gap:2vw;padding-top:1.2vh}
.btn{background:var(--bleu);color:#fff;border:0;border-radius:14px;padding:1vh 2vw;font-size:min(2vw,3.6vh);font-weight:700}
.btn.or{background:var(--or);color:var(--bleuf)}
.chrono{font-size:min(4vw,7vh);font-weight:900;color:var(--bleu);min-width:3.2em;text-align:center}
.chrono.fin{color:var(--rouge)}
.titre{background:var(--bleu);color:#fff;justify-content:center;align-items:flex-start;overflow:auto}
.titre h1{color:#fff;font-size:min(5.5vw,9vh)}.titre p{font-size:clamp(22px,2.4vw,40px);color:var(--or);font-weight:700}
.titre label{font-size:clamp(20px,2vw,32px);display:block;margin:1.5vh 0 .5vh}
.titre input{font:inherit;font-size:clamp(22px,2.2vw,36px);padding:.3em .5em;border-radius:10px;border:0;width:min(640px,80vw)}
.aide{font-size:clamp(14px,1.2vw,20px);color:#5A5F6A}.titre .aide{color:#DDE3EC;margin-top:3vh}
.podium{font-size:clamp(28px,3.4vw,56px);line-height:1.6}
</style></head><body>
<section class="ecran titre actif" id="accueil" aria-label="Accueil du quiz">
  <p>MARILYN INSTITUT · L'OR DES ÎLES</p>
  <h1>Le grand quiz<br>de la relation cliente</h1>
  <label for="e1">Équipe 1</label><input id="e1" value="Équipe Vanille">
  <label for="e2">Équipe 2</label><input id="e2" value="Équipe Frangipanier">
  <p style="margin-top:4vh"><button class="btn or" onclick="demarrer()">Commencer ▶</button></p>
  <p class="aide">Aucune donnée n'est collectée ni envoyée : ce quiz fonctionne sans internet, sur cet ordinateur uniquement.<br>
  Clavier : Espace = révéler · → = question suivante · 1 / 2 = +1 point à l'équipe · C = chrono 30 s</p>
</section>
<section class="ecran" id="jeu" aria-live="polite">
  <div class="bandeau"><span class="num" id="num"></span>
    <div class="equipes"><div class="eq"><span id="n1"></span><b id="s1">0</b><button onclick="point(1)" aria-label="Un point équipe 1">+1</button></div>
    <div class="eq"><span id="n2"></span><b id="s2">0</b><button onclick="point(2)" aria-label="Un point équipe 2">+1</button></div></div></div>
  <div><span class="theme" id="theme"></span></div>
  <h1 id="q"></h1>
  <div class="choix" id="choix"></div>
  <div class="expl" id="expl"></div>
  <div class="pied"><button class="btn" onclick="lancerChrono()">⏱ 30 s</button><span class="chrono" id="chrono"></span>
    <span><button class="btn or" id="rev" onclick="reveler()">Révéler</button> <button class="btn" onclick="suivante()">Suivante ▶</button></span></div>
</section>
<section class="ecran titre" id="fin" aria-label="Résultats">
  <p>Résultats</p><h1>Bravo à toutes !</h1><div class="podium" id="podium"></div>
  <p class="aide">N'oubliez pas : chacune remplit aussi sa feuille-réponse individuelle — c'est elle qui compte pour l'attestation.</p>
  <p><button class="btn or" onclick="location.reload()">Rejouer</button></p>
</section>
<script>
const QUIZ = __QUIZ__;
let i=0, s=[0,0], revele=false, t=null;
const $=id=>document.getElementById(id);
function demarrer(){ $('n1').textContent=$('e1').value; $('n2').textContent=$('e2').value; montrer('jeu'); afficher(); }
function montrer(id){ document.querySelectorAll('.ecran').forEach(e=>e.classList.remove('actif')); $(id).classList.add('actif'); }
function afficher(){
  const q=QUIZ[i]; revele=false; stopChrono(); $('chrono').textContent='';
  $('num').textContent='Question '+(i+1)+' / '+QUIZ.length; $('theme').textContent=q.theme; $('q').textContent=q.q;
  $('choix').innerHTML=q.choix.map((c,k)=>'<div class="c" id="c'+k+'"><span class="l">'+'ABC'[k]+'</span><span>'+c+'</span></div>').join('');
  $('expl').className='expl'; $('expl').textContent=q.explication; $('rev').disabled=false;
}
function reveler(){ if(revele) return; revele=true; stopChrono(); const q=QUIZ[i];
  q.choix.forEach((_,k)=>{ const e=$('c'+k); if(k===q.bonne){ e.classList.add('bon'); e.insertAdjacentHTML('beforeend','<span class="tag">✔ Bonne réponse</span>'); } else e.classList.add('faux'); });
  $('expl').classList.add('v'); $('rev').disabled=true; }
function suivante(){ if(!revele){ reveler(); return; } if(i<QUIZ.length-1){ i++; afficher(); } else finir(); }
function point(n){ s[n-1]++; $('s'+n).textContent=s[n-1]; }
function finir(){ const n1=$('e1').value, n2=$('e2').value;
  $('podium').innerHTML = n1+' : <b style="color:var(--or)">'+s[0]+'</b> point'+(s[0]>1?'s':'')+'<br>'+n2+' : <b style="color:var(--or)">'+s[1]+'</b> point'+(s[1]>1?'s':'')+
   '<br>'+(s[0]===s[1]?'Égalité parfaite — l\'équipe Marilyn gagne !':((s[0]>s[1]?n1:n2)+' remporte le quiz !'));
  montrer('fin'); }
function lancerChrono(){ stopChrono(); let r=30; $('chrono').className='chrono'; $('chrono').textContent=r;
  t=setInterval(()=>{ r--; $('chrono').textContent=r>0?r:'Temps !'; if(r<=5) $('chrono').className='chrono fin'; if(r<=0) stopChrono(); },1000); }
function stopChrono(){ if(t){ clearInterval(t); t=null; } }
document.addEventListener('keydown',e=>{ if($('accueil').classList.contains('actif')) return;
  if(e.key===' '){ e.preventDefault(); reveler(); } else if(e.key==='ArrowRight') suivante();
  else if(e.key==='1') point(1); else if(e.key==='2') point(2); else if(e.key.toLowerCase()==='c') lancerChrono(); });
</script></body></html>
"""


def construire():
    out = D.SORTIE / "04_PEDAGOGIE" / "Quiz_interactif_Marilyn.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(GABARIT.replace("__QUIZ__", json.dumps(QUIZ, ensure_ascii=False)), encoding="utf-8")
    return out


if __name__ == "__main__":
    print(construire())
