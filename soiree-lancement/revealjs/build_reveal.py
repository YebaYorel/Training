"""Génère la version Reveal.js (HTML/CSS) de la soirée de lancement YEBA FORMATIONS.

Source unique : ../contenu/slides.json  →  revealjs/index.html
    python revealjs/build_reveal.py

- 100 % hors ligne : reveal.js, police Montserrat et images sont servis localement
  (aucun appel à un CDN pendant la soirée : aucune donnée ne sort de la salle).
- « Auto-Animate » de Reveal.js = équivalent web de la Morphose PowerPoint : les éléments
  qui portent le même data-id d'une slide à l'autre glissent / se transforment.
- Touche S : vue orateur avec les notes (durée, texte à dire, alertes RGPD / IA Act).
- Respecte « réduire les animations » du système (accessibilité).
"""
import html
import json
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent
C = json.loads((RACINE / "contenu" / "slides.json").read_text(encoding="utf-8"))
PAL = C["palette"]
e = html.escape


def ident(nom):
    return nom.replace("!!", "").replace(" ", "-").replace("É", "E").replace("Ô", "O").replace("È", "E")


def deux(s, cls="titre"):
    out = f'<span class="blanc">{e(s["titre"])}</span>'
    if s.get("titre_or"):
        out += f'<br><span class="or">{e(s["titre_or"])}</span>'
    return f'<h2 class="{cls}" data-id="titre">{out}</h2>'


def logo():
    return '<img class="petit-logo" data-id="logo" src="../assets/embleme-fond-sombre.png" alt="Emblème YEBA FORMATIONS">'


def l_cover(s):
    return f"""
  <img class="logo-cover" data-id="logo" src="../assets/logo-yeba-fond-sombre.png"
       alt="Logo YEBA FORMATIONS : trois pitons reliés en réseau">
  <p class="kicker centre">{e(s['kicker'])}</p>
  <h1 class="titre-cover" data-id="titre"><span class="blanc">{e(s['titre'])}</span><br><span class="or">{e(s['titre_or'])}</span></h1>
  <p class="meta">{e(C['meta']['date'])} · {e(C['meta']['lieu'])} · La Réunion</p>"""


def l_statement(s):
    fond = {"QUESTION": "bleu", "L'IMAGE À RETENIR": "bleu_nuit", "ET MAINTENANT": "bleu"}.get(s.get("kicker"), "noir")
    extra = ""
    if s["id"] == "S19":
        extra = '<img class="illu illu-etoiles" src="../assets/illustrations/etoiles-ue.png" alt="Cercle de douze points dorés">'
    if s["id"] == "S22":
        extra = '<img class="illu illu-jauge" src="../assets/illustrations/jauge-or.png" alt="Compte-tours doré">'
    etroit = " etroit" if extra else ""
    return fond, f"""
  <div class="barre" data-id="barre"></div>
  <p class="kicker">{e(s['kicker'])}</p>
  <h2 class="titre statement{etroit}" data-id="titre"><span class="blanc">{e(s['titre'])}</span><br>
    <span class="or fragment fade-up">{e(s['titre_or'])}</span></h2>
  {extra}{logo()}"""


def l_agenda(s):
    a = s["agenda_actif"]
    items = "".join(
        f'<li class="{"actif" if i == a else ""}"><span class="n" data-id="agn{i}">{i + 1:02d}</span>'
        f'<span class="t" data-id="ag{i}">{e(t)}</span></li>'
        for i, t in enumerate(C["agenda"])
    )
    return f"""
  <h2 class="titre-petit" data-id="titre">{e(s['titre'])}</h2>
  <ol class="agenda" style="--actif:{a}">{items}<div class="marqueur" data-id="marqueur"></div></ol>
  <div class="agenda-big" data-id="agbig">{a + 1:02d}</div>{logo()}"""


def l_team(s):
    cartes = "".join(
        f'<div class="carte fragment fade-up" data-id="carte{i}"><div class="photo">{e(c["initiales"])}</div>'
        f'<div class="nom">{e(c["nom"])}</div><div class="role">{e(c["role"])}</div></div>'
        for i, c in enumerate(s["cartes"])
    )
    return f"""
  <h2 class="titre-ligne" data-id="titre"><span class="blanc">{e(s['titre'])}</span> <span class="or">{e(s['titre_or'])}</span></h2>
  <div class="cartes">{cartes}</div>{logo()}"""


def l_badges(s):
    b = "".join(f'<div class="badge fragment zoom-in">{e(x)}</div>' for x in s["items"])
    return f"""
  <h2 class="titre-ligne" data-id="titre"><span class="blanc">{e(s['titre'])}</span> <span class="or">{e(s['titre_or'])}</span></h2>
  <div class="badges">{b}</div>{logo()}"""


def l_word(s):
    return f"""
  <h2 class="mot-geant" data-id="yeba">{e(s['titre'])}</h2>
  <p class="traduction">{e(s['texte'])}</p>{logo()}"""


def l_quote(s):
    return f"""
  <div class="guillemets" aria-hidden="true">«</div>
  <blockquote class="citation" data-id="titre"><span class="blanc">{e(s['titre'])}</span><br>
    <span class="or">{mots(s['titre_or'])}</span></blockquote>{logo()}"""


def mots(txt):
    """Chaque mot apparaît l'un après l'autre (effet « parole » qui respecte le retour à la ligne)."""
    return " ".join(f'<span class="mot-a-mot" style="--i:{i}">{e(m)}</span>' for i, m in enumerate(txt.split(" ")))


def l_tree(s):
    g, d = s["branches"]
    return f"""
  <h2 class="y-geant" data-id="yeba">{e(s['titre'])}</h2>
  <div class="branche gauche fragment fade-left"><strong>{e(g)}</strong><span>Genèse · Savoir</span></div>
  <div class="branche droite fragment fade-right"><strong>{e(d)}</strong><span>Afrique · Transmission</span></div>{logo()}"""


def l_baobab(s):
    return f"""
  <div class="baobab-texte">{deux(s)}<p class="sous">{e(s['texte'])}</p></div>
  <img class="baobab" data-id="baobab" src="../assets/illustrations/baobab-or.png" alt="Silhouette dorée d'un baobab, l'arbre à palabres">{logo()}"""


def l_split(s):
    col = lambda b: f'<p class="kicker centre">{e(b["label"])}</p>' + "".join(f"<p class=\"mot\">{e(m)}</p>" for m in b["mots"])
    return f"""
  <div class="moitie droite-bleue" data-id="droite"></div>
  <div class="split">
    <div><h2 class="titre-ligne centre" data-id="titre"><span class="blanc">{e(s['titre'])}</span></h2>{col(s['gauche'])}</div>
    <div><h2 class="titre-ligne centre"><span class="or">{e(s['titre_or'])}</span></h2>{col(s['droite'])}</div>
  </div>
  <img class="embleme" data-id="embleme" src="../assets/embleme-fond-sombre.png" alt="Emblème YEBA : trois pitons en réseau">"""


def l_values(s):
    v = "".join(f'<li class="fragment fade-up"><span class="n">{i + 1:02d}</span>{e(x)}</li>' for i, x in enumerate(s["items"]))
    return f"""
  <h2 class="titre-petit" data-id="titre">{e(s['titre'])}</h2>
  <ol class="valeurs">{v}</ol>{logo()}"""


def l_timeline(s):
    et = "".join(
        f'<div class="jalon fragment fade-in{" dernier" if i == len(s["etapes"]) - 1 else ""}">'
        f'<div class="date">{e(x["date"])}</div><div class="point"></div><div class="txt">{e(x["texte"])}</div></div>'
        for i, x in enumerate(s["etapes"])
    )
    return f"""
  <h2 class="titre-petit" data-id="titre">{e(s['titre'])}</h2>
  <div class="frise"><div class="ligne" data-id="ligne"></div>{et}</div>{logo()}"""


def l_bignumber(s):
    return f"""
  <div class="grand-chiffre" data-id="titre"><span class="compteur" data-de="7" data-a="8">8</span>&nbsp;h</div>
  <div class="explication"><p class="blanc">{e(s['texte'])}</p><p class="or fragment fade-up">{e(s['texte_or'])}</p></div>{logo()}"""


def l_pillars(s):
    p = "".join(
        f'<div class="pilier fragment fade-up"><div class="filigrane">0{i + 1}</div><div class="verbe">{e(x["titre"])}</div>'
        f'<div class="trait"></div><div class="detail">{e(x["texte"])}</div></div>'
        for i, x in enumerate(s["items"])
    )
    return f"""
  <h2 class="titre-ligne" data-id="titre"><span class="blanc">{e(s['titre'])}</span> <span class="or">{e(s['titre_or'])}</span></h2>
  <div class="piliers">{p}</div>{logo()}"""


def l_formats(s):
    it = {x["titre"]: x for x in s["items"]}
    ordre = ["Intra", "Séminaire", "Inter", "Sur-mesure"]
    t = "".join(
        f'<div class="format fragment zoom-in {"or-plein" if k == "Séminaire" else ""} f{i}"><strong>{e(k)}</strong><span>{e(it[k]["texte"])}</span></div>'
        for i, k in enumerate(ordre)
    )
    return f"""
  <h2 class="titre-ligne" data-id="titre"><span class="blanc">{e(s['titre'])}</span> <span class="or">{e(s['titre_or'])}</span></h2>
  <div class="formats">{t}</div>{logo()}"""


def l_garage(s):
    tuiles = "".join(
        f'<div class="tuile" data-id="tuile-{ident(x["code"])}" style="--c:#{s["familles"][x["famille"]]}">'
        f'<span data-id="code-{ident(x["code"])}">{e(x["code"])}</span></div>'
        for x in s["items"]
    )
    leg = "".join(f'<span><i style="background:#{c}"></i>{e(f)}</span>' for f, c in s["familles"].items())
    return f"""
  <h2 class="titre-petit" data-id="titre">{e(s['titre'])}</h2>
  <div class="garage">{tuiles}</div><div class="legende">{leg}</div>{logo()}"""


def l_focus(s):
    garage = next(x for x in C["slides"] if x["layout"] == "garage")
    fam = next(i["famille"] for i in garage["items"] if i["code"] == s["code"])
    coul = garage["familles"][fam]
    puces = "".join(f'<li class="fragment fade-left"><span class="or">—</span> {e(p)}</li>' for p in s["puces"])
    chips = "".join(f'<span class="chip">{e(c)}</span>' for c in s["chips"])
    onde = '<div class="onde" aria-hidden="true">' + "<i></i>" * 14 + "</div>" if s["code"] == "CARROSSERIE" else ""
    return f"""
  <div class="bande" data-id="tuile-{ident(s['code'])}" style="--c:#{coul}">
    <span class="code-vertical" data-id="code-{ident(s['code'])}" style="font-size:{min(74, int(800 / (0.78 * len(s['code']))))}px">{e(s['code'])}</span></div>
  <div class="focus">
    <p class="kicker">{e(s['famille'])}</p>
    {deux(s, 'titre focus-titre')}
    <ul class="puces">{puces}</ul>
    <div class="chips">{chips}</div>
  </div>{onde}{logo()}"""


def l_demo(s):
    return f"""
  <div class="live" data-id="live"><i></i>{e(s['kicker'])}</div>
  {deux(s, 'titre demo')}{logo()}"""


LAYOUTS = {
    "cover": l_cover, "statement": l_statement, "agenda": l_agenda, "team": l_team, "badges": l_badges,
    "word": l_word, "quote": l_quote, "tree": l_tree, "baobab": l_baobab, "split": l_split, "values": l_values,
    "timeline": l_timeline, "bignumber": l_bignumber, "pillars": l_pillars, "formats": l_formats,
    "garage": l_garage, "focus": l_focus, "demo": l_demo,
}


def section(s):
    res = LAYOUTS[s["layout"]](s)
    fond, corps = res if isinstance(res, tuple) else ("noir", res)
    notes = (f"[{s['id']}] {s['partie']} — ≈ {s['duree_s']} s\n\n{s['notes']}\n\nVISUEL : {s['visuel']}\n\n"
             f"ANIMATION : {s['animation']}")
    cache = ' data-visibility="hidden"' if s.get("cache") else ""
    return (f'<section data-auto-animate data-background-color="#{PAL[fond]}" class="l-{s["layout"]}" '
            f'id="{s["id"]}"{cache}>{corps}\n  <aside class="notes">{e(notes)}</aside>\n</section>')


CSS = """
@font-face{font-family:Montserrat;font-weight:400;font-display:block;src:url(fonts/montserrat-latin-400-normal.woff2) format('woff2')}
@font-face{font-family:Montserrat;font-weight:700;font-display:block;src:url(fonts/montserrat-latin-700-normal.woff2) format('woff2')}
@font-face{font-family:Montserrat;font-weight:800;font-display:block;src:url(fonts/montserrat-latin-800-normal.woff2) format('woff2')}
@font-face{font-family:Montserrat;font-weight:900;font-display:block;src:url(fonts/montserrat-latin-900-normal.woff2) format('woff2')}
:root{--noir:#121212;--bleu:#1B3A6B;--nuit:#0E2140;--or:#C9A84C;--blanc:#fff;--gris:#B8BCC6;--gris2:#8C93A0;--carte:#1C1C1C}
html,body{background:var(--noir)}
.reveal{font-family:Montserrat,system-ui,sans-serif;color:var(--blanc);font-size:46px}
.reveal .slides section{height:100%;text-align:left;padding:0;box-sizing:border-box}
.reveal h1,.reveal h2{font-family:Montserrat;font-weight:800;text-transform:none;letter-spacing:-.01em;margin:0;line-height:1.08;hyphens:none;word-break:keep-all;overflow-wrap:normal}
.blanc{color:var(--blanc)}.or{color:var(--or)}.centre{text-align:center!important}
.kicker{position:absolute;left:158px;top:150px;font-weight:800;font-size:40px;letter-spacing:.3em;color:var(--or);margin:0;text-transform:uppercase}
.petit-logo{position:absolute;right:48px;bottom:30px;width:112px;margin:0!important}
.titre-petit{position:absolute;left:96px;top:54px;font-size:62px}
.titre-ligne{position:absolute;left:96px;top:54px;right:96px;font-size:76px;white-space:nowrap}
/* cover */
.logo-cover{position:absolute;left:50%;top:40px;width:430px;transform:translateX(-50%);margin:0!important}
.l-cover .kicker{left:0;right:0;top:455px;text-align:center}
.titre-cover{position:absolute;left:0;right:0;top:520px;text-align:center;font-size:68px}
.meta{position:absolute;left:0;right:0;bottom:50px;text-align:center;color:var(--gris);font-size:40px;margin:0}
/* statement */
.barre{position:absolute;left:54px;top:210px;width:17px;height:516px;background:var(--or)}
.statement{position:absolute;left:114px;top:225px;width:1300px;font-size:106px}
.statement.etroit{width:900px;font-size:88px}
.illu{position:absolute;margin:0!important}
.illu-etoiles{right:110px;top:80px;width:260px;animation:tourne 30s linear infinite}
.illu-jauge{right:70px;top:150px;width:540px}
@keyframes tourne{to{transform:rotate(360deg)}}
/* agenda */
.agenda{position:absolute;left:96px;top:170px;list-style:none;margin:0;padding:0 0 0 42px;width:900px}
.agenda li{display:flex;align-items:center;height:96px;font-size:48px;color:var(--gris2);font-weight:400}
.agenda li .n{width:112px;font-weight:800;font-size:46px}
.agenda li.actif{color:var(--blanc);font-weight:800;font-size:54px}.agenda li.actif .n{color:var(--or)}
.marqueur{position:absolute;left:0;top:calc(var(--actif) * 96px + 14px);width:17px;height:68px;background:var(--or)}
.agenda-big{position:absolute;right:70px;top:170px;font-weight:900;font-size:360px;line-height:1;color:var(--or)}
/* team */
.cartes{position:absolute;left:96px;right:96px;top:222px;display:flex;gap:54px;justify-content:center}
.carte{width:432px;height:552px;background:var(--carte);border:2px solid var(--or);border-radius:26px;text-align:center;padding-top:42px;box-sizing:border-box}
.photo{width:228px;height:228px;margin:0 auto;border-radius:50%;background:var(--bleu);border:4px solid var(--or);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:72px}
.nom{font-weight:800;font-size:46px;margin-top:40px}.role{color:var(--gris);font-size:40px;margin-top:18px;padding:0 20px}
/* badges */
.badges{position:absolute;left:96px;right:96px;top:240px;display:grid;grid-template-columns:repeat(3,1fr);gap:48px 42px}
.badge{height:210px;border:3px solid var(--or);border-radius:40px;background:var(--carte);display:flex;align-items:center;justify-content:center;text-align:center;font-weight:800;font-size:44px;padding:0 20px}
/* mot / Y */
.mot-geant{position:absolute;left:0;right:0;top:120px;text-align:center;font-weight:900;font-size:420px;color:var(--or);line-height:1}
.traduction{position:absolute;left:0;right:0;top:640px;text-align:center;font-weight:800;font-size:60px;margin:0}
.y-geant{position:absolute;left:0;right:0;top:40px;text-align:center;font-weight:900;font-size:640px;color:var(--or);line-height:1}
.branche{position:absolute;top:150px;width:470px;font-size:56px}.branche strong{display:block;font-weight:800;line-height:1.1}
.branche span{display:block;color:var(--gris);font-size:42px;margin-top:20px}
.branche.gauche{left:72px;text-align:right}.branche.droite{right:72px}
/* citation */
.guillemets{position:absolute;left:30px;top:10px;font-weight:900;font-size:340px;color:#4A3F22;line-height:1}
.citation{position:absolute;left:288px;top:230px;width:1220px;margin:0;padding:0;border:0;box-shadow:none;font-style:normal;font-weight:800;font-size:88px;line-height:1.1;background:none}
.mot-a-mot{display:inline-block;opacity:0}
.present .mot-a-mot{animation:parole .5s ease-out forwards;animation-delay:calc(1.2s + var(--i) * .35s)}
@keyframes parole{from{opacity:0;transform:translateY(.3em)}to{opacity:1;transform:none}}
/* baobab */
.baobab-texte{position:absolute;left:96px;top:220px;width:720px}
.baobab-texte .titre{font-size:100px}.sous{color:var(--gris);font-size:46px;margin-top:40px}
.baobab{position:absolute;right:130px;top:40px;height:760px;margin:0!important;transform-origin:bottom}
.present .baobab{animation:pousse 1.6s cubic-bezier(.2,.8,.2,1) both}
@keyframes pousse{from{transform:scaleY(.2);opacity:0}}
/* split */
.moitie.droite-bleue{position:absolute;left:50%;top:0;width:50%;height:100%;background:var(--bleu)}
.split{position:absolute;inset:0;display:grid;grid-template-columns:1fr 1fr}
.split>div{position:relative;padding-top:210px;text-align:center}
.split .titre-ligne{left:0;right:0;font-size:84px}
.split .kicker{position:static;margin:40px 0 10px}.mot{font-weight:800;font-size:60px;margin:6px 0}
.embleme{position:absolute;left:50%;bottom:60px;width:430px;transform:translateX(-50%);margin:0!important}
/* valeurs */
.valeurs{position:absolute;left:96px;top:170px;list-style:none;margin:0;padding:0}
.valeurs li{font-weight:800;font-size:66px;height:130px;display:flex;align-items:center}
.valeurs .n{color:var(--or);font-weight:900;font-size:80px;width:204px}
/* frise */
.frise{position:absolute;left:108px;right:108px;top:300px;display:flex}
.frise .ligne{position:absolute;left:0;right:0;top:196px;height:8px;background:var(--or);transform-origin:left}
.present .frise .ligne{animation:trace 1.6s ease-out both}@keyframes trace{from{transform:scaleX(0)}}
.jalon{flex:1;text-align:center;position:relative}
.jalon .date{height:150px;display:flex;align-items:flex-end;justify-content:center;color:var(--or);font-weight:800;font-size:52px;white-space:nowrap}
.jalon .point{width:40px;height:40px;border-radius:50%;background:var(--or);margin:30px auto 0}.jalon.dernier .point{background:#fff;width:58px;height:58px;margin-top:21px}
.jalon .txt{font-size:42px;margin-top:50px;padding:0 20px}
/* grand chiffre */
.grand-chiffre{position:absolute;left:40px;top:90px;width:880px;text-align:center;font-weight:900;font-size:470px;line-height:1;color:var(--or)}
.explication{position:absolute;left:950px;top:260px;width:580px;font-weight:800;font-size:60px}.explication p{margin:0 0 40px}
/* piliers */
.piliers{position:absolute;left:96px;right:96px;top:250px;display:flex;gap:54px}
.pilier{flex:1}.filigrane{font-weight:900;font-size:180px;color:#2A2A2A;line-height:1}
.verbe{font-weight:800;font-size:70px;margin-top:10px}.trait{width:120px;height:11px;background:var(--or);margin:26px 0}
.detail{color:var(--or);font-weight:800;font-size:44px}
/* formats */
.formats{position:absolute;left:96px;right:96px;top:222px;display:grid;grid-template-columns:5fr 1fr 5.4fr;grid-template-rows:264px 264px;gap:30px 36px}
.format{background:var(--nuit);border-radius:22px;padding:0 48px;display:flex;flex-direction:column;justify-content:center}
.format strong{font-weight:800;font-size:72px}.format span{color:var(--or);font-weight:800;font-size:44px}
.format.or-plein{background:var(--or);color:var(--noir)}.format.or-plein span{color:var(--noir)}
.f0{grid-column:1}.f1{grid-column:2/4}.f2{grid-column:1/3}.f3{grid-column:3}
/* garage */
.garage{position:absolute;left:96px;right:96px;top:170px;display:grid;grid-template-columns:repeat(4,1fr);gap:28px}
.tuile{height:156px;background:var(--carte);border:3px solid var(--c);display:flex;align-items:center;justify-content:center;text-align:center;font-weight:800;font-size:38px;padding:0 14px}
.legende{position:absolute;left:96px;top:760px;display:flex;gap:44px;font-size:40px}
.legende i{display:inline-block;width:36px;height:36px;margin-right:16px;vertical-align:-4px}
/* focus */
.bande{position:absolute;left:0;top:0;width:492px;height:100%;background:var(--c);display:flex;align-items:center;justify-content:center}
.code-vertical{transform:rotate(-90deg);white-space:nowrap;color:var(--noir);font-weight:900;font-size:74px}
.focus{position:absolute;left:576px;top:0;right:80px;height:100%}
.focus .kicker{left:0;top:66px;font-size:40px}
.focus-titre{position:absolute;left:0;top:140px;right:0;font-size:90px}
.puces{position:absolute;left:0;top:470px;list-style:none;margin:0;padding:0}
.puces li{font-weight:800;font-size:54px;margin-bottom:22px}
.chips{position:absolute;left:0;top:730px;display:flex;gap:28px}
.chip{border:3px solid var(--or);border-radius:60px;padding:14px 34px;font-weight:800;font-size:40px}
.onde{position:absolute;right:60px;top:470px;height:110px;display:flex;gap:10px;align-items:center}
.onde i{width:12px;height:30%;background:var(--or);border-radius:6px;animation:onde 1.1s ease-in-out infinite}
.onde i:nth-child(3n){animation-delay:-.3s}.onde i:nth-child(3n+1){animation-delay:-.6s}.onde i:nth-child(4n){animation-delay:-.9s}
@keyframes onde{50%{height:100%}}
/* démo */
.live{position:absolute;left:96px;top:120px;background:#E53935;border-radius:60px;padding:14px 40px;font-weight:800;font-size:44px;letter-spacing:.12em;display:flex;align-items:center;gap:22px}
.live i{width:26px;height:26px;border-radius:50%;background:#fff;animation:pulse 1.2s ease-in-out infinite}
@keyframes pulse{50%{opacity:.2}}
.demo{position:absolute;left:96px;top:300px;right:96px;font-size:124px}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}.mot-a-mot{opacity:1}}
"""

JS = """
Reveal.initialize({
  width: 1600, height: 900, margin: 0, center: false, hash: true, controls: true, progress: true,
  transition: 'fade', transitionSpeed: 'slow', autoAnimateDuration: 1.2,
  autoAnimateEasing: 'cubic-bezier(.65,0,.35,1)', plugins: [RevealNotes]
});
// Compteur 7 → 8 sur la slide « 8 h »
Reveal.on('slidechanged', ev => {
  ev.currentSlide.querySelectorAll('.compteur').forEach(c => {
    const de = +c.dataset.de, a = +c.dataset.a; c.textContent = de;
    setTimeout(() => { c.textContent = a; }, 1300);
  });
});
"""


def construire():
    sections = "\n".join(section(s) for s in C["slides"])
    doc = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>YEBA FORMATIONS — Soirée de lancement</title>
<link rel="stylesheet" href="vendor/reset.css">
<link rel="stylesheet" href="vendor/reveal.css">
<style>{CSS}</style>
</head>
<body>
<div class="reveal"><div class="slides">
{sections}
</div></div>
<script src="vendor/reveal.js"></script>
<script src="vendor/plugin/notes.js"></script>
<script>{JS}</script>
</body>
</html>
"""
    (ICI / "index.html").write_text(doc, encoding="utf-8")
    print("OK :", ICI / "index.html")


if __name__ == "__main__":
    construire()
