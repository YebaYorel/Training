"""Génère la version Reveal.js (HTML/CSS) de « YEBA — Saison 1 », jumelle du PowerPoint.

Source unique : ../contenu/slides.json  →  revealjs/index.html
    python3 revealjs/build_reveal.py

- 100 % hors ligne : reveal.js, Montserrat, images et vidéos sont servis localement (aucun CDN :
  aucune donnée ne sort de la salle).
- Même mise en page que le PowerPoint : les corps de titre sont calculés par le même moteur de mesure
  (pptx/build_pptx.py), la même typographie française (espaces insécables, aucun mot coupé).
- « Auto-Animate » = Morphose web : les objets qui portent le même data-id glissent d'une slide à
  l'autre (titre, logo, agenda, champ d'étoiles et halo en parallaxe, tuiles du catalogue → fiche).
- Fonds vidéo vivants (Remotion) en boucle muette ; si le système demande « réduire les animations »,
  chaque fond vidéo est remplacé par son image fixe et les animations CSS sont coupées.
- Vidéos plein écran (générique, épisodes, clips) : avance automatique à la fin.
- Touche S : vue orateur avec les notes (durée, texte à dire, alertes RGPD / IA Act).
"""
import html
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent
sys.path.insert(0, str(RACINE / "pptx"))
import build_pptx as P  # noqa: E402  (mesure des textes, typographie, séquence : une seule source de vérité)

C = P.C
PAL = C["palette"]
PXI = 120  # pixels par pouce (1600 px = 13,333 in)
K = PXI / 72  # pixels par point


def e(t):
    return html.escape(P.typo(t), quote=False)


def px(pt):
    return round(pt * K)


# Halo de lumière par gabarit : (x, y, taille) en pouces, comme dans le PowerPoint
HALO = {
    "cover": (6.67, 1.9, 8.5), "statement": (3.2, 3.9, 9.5), "agenda": (10.6, 3.7, 8.0), "team": (6.67, 4.2, 10),
    "badges": (6.67, 4.3, 10), "word": (6.67, 3.0, 10), "quote": (2.2, 2.2, 8), "tree": (6.67, 3.6, 9),
    "baobab": (3.3, 3.6, 8.5), "split": (3.3, 6.2, 8), "values": (1.6, 4.0, 8), "timeline": (6.67, 4.1, 10),
    "pillars": (6.67, 4.6, 10), "offres": (9.4, 2.4, 9), "journee": (2.0, 1.6, 7), "confiance": (9.7, 3.9, 9),
    "avantages": (6.67, 4.6, 10), "atelier": (6.67, 4.0, 10), "focus": (2.05, 3.75, 8), "demo": (2.0, 1.6, 8),
    "bientot": (10.6, 3.0, 9),
}
FOND_COULEUR = {"noir": PAL["noir"], "terre": PAL["terre"], "bleu": PAL["bleu"], "bleu_nuit": PAL["bleu_nuit"]}
HALO_TEINTE = {"noir": "or", "terre": "terre", "bleu": "bleu", "bleu_nuit": "bleu"}


def calques(s, idx):
    """Champ d'étoiles + halo (data-id identiques d'une slide à l'autre → parallaxe par Auto-Animate) + vignettage."""
    import math

    dx = (-1.6 + 0.55 * math.sin(idx * 0.55)) * PXI
    dy = (-0.95 + 0.4 * math.cos(idx * 0.42)) * PXI
    hx, hy, t = HALO[s["layout"]]
    teinte = HALO_TEINTE.get(s.get("teinte", "noir"), "or")
    return (f'<img class="calque" data-id="etoiles" src="../assets/calques/etoiles.png" alt="" '
            f'style="left:{dx:.0f}px;top:{dy:.0f}px;width:2000px">'
            f'<img class="calque" data-id="halo" src="../assets/calques/halo-{teinte}.png" alt="" '
            f'style="left:{(hx - t / 2) * PXI:.0f}px;top:{(hy - t / 2) * PXI:.0f}px;width:{t * PXI:.0f}px">'
            f'<img class="calque vignette" src="../assets/calques/vignette.png" alt="">')


def logo():
    return '<img class="petit-logo" data-id="logo" src="../assets/embleme-fond-sombre.png" alt="Emblème YEBA FORMATIONS">'


def deux_tons(s, pt, cls="titre", fragment_or=False):
    """Titre blanc + titre or, même corps (calculé par le moteur du PowerPoint)."""
    out = f'<span class="blanc">{e(s["titre"])}</span>'
    if s.get("titre_or"):
        frag = ' class="or fragment fade-up"' if fragment_or else ' class="or"'
        out += f"<br><span{frag}>{e(s['titre_or'])}</span>"
    return f'<h2 class="{cls}" data-id="titre" style="font-size:{px(pt)}px">{out}</h2>'


def une_ligne(s, pt_max=54, largeur=11.73):
    txt = P.typo(s["titre"] + " " + s.get("titre_or", ""))
    pt = pt_max
    while pt > 36 and P.largeur_texte(txt, pt) > largeur - 0.3:
        pt -= 2
    return (f'<h2 class="titre-ligne" data-id="titre" style="font-size:{px(pt)}px"><span class="blanc">{e(s["titre"])}</span> '
            f'<span class="or">{e(s.get("titre_or", ""))}</span></h2>')


# ───────────────────────────── gabarits ─────────────────────────────

def l_cover(s):
    pt = P.lignes(s, 44, P.W - 1.6, 1.85)
    meta = f"{C['meta']['date']} · {C['meta']['lieu']} · La Réunion"
    return f"""
  <img class="logo-cover" data-id="logo" src="../assets/logo-yeba-fond-sombre.png" alt="Logo YEBA FORMATIONS : trois pitons reliés en réseau">
  <p class="kicker centre" style="top:446px;left:0;right:0">{e(s['kicker'])}</p>
  {deux_tons(s, pt, 'titre titre-cover')}
  <p class="meta">{e(meta)}</p>"""


def l_statement(s):
    largeur = 9.3 if s["id"] == "S22" else 10.8
    pt = P.lignes(s, 64, largeur, 4.3)
    illu = ('<img class="illu-ue" src="../assets/illustrations/etoiles-ue.png" alt="Cercle de douze points dorés évoquant le drapeau européen">'
            if s["id"] == "S22" else "")
    return f"""
  <div class="barre" data-id="barre"></div>
  <p class="kicker">{e(s['kicker'])}</p>
  <div class="statement" style="width:{largeur * PXI:.0f}px">{deux_tons(s, pt, fragment_or=s.get('kicker') == 'QUESTION')}</div>
  {illu}{logo()}"""


def l_agenda(s):
    a = s["agenda_actif"]
    li = "".join(
        f'<li class="{"actif" if i == a else ""}"><span class="n" data-id="agn{i}">{i + 1:02d}</span>'
        f'<span class="t" data-id="ag{i}">{e(ep["titre"])}</span><span class="s" data-id="ags{i}">{e(ep["sujet"])}</span></li>'
        for i, ep in enumerate(C["episodes"])
    )
    return f"""
  <h2 class="titre-agenda" data-id="titre-agenda">{e(s['titre'])}</h2>
  <ol class="agenda" style="--actif:{a}">{li}<div class="marqueur" data-id="marqueur"></div></ol>
  <div class="agenda-big" data-id="agbig">{a + 1:02d}</div>{logo()}"""


def l_team(s):
    cartes = "".join(
        f'<div class="carte entree" style="--d:{0.6 + i * 0.18:.2f}s" data-id="carte{i}"><div class="photo">{e(c["initiales"])}</div>'
        f'<div class="nom">{e(c["nom"])}</div><div class="role">{e(c["role"])}</div></div>'
        for i, c in enumerate(s["cartes"])
    )
    return f"""{une_ligne(s)}<div class="cartes">{cartes}</div>{logo()}"""


def l_badges(s):
    b = "".join(f'<div class="badge entree zoom" style="--d:{0.5 + i * 0.14:.2f}s">{e(x)}</div>' for i, x in enumerate(s["items"]))
    return f"""{une_ligne(s)}<div class="badges">{b}</div>{logo()}"""


def l_word(s):
    return f"""
  <h2 class="mot-geant" data-id="yeba">{e(s['titre'])}</h2>
  <p class="traduction">{e(s['texte'])}</p>{logo()}"""


def l_quote(s):
    pt = P.lignes(s, 54, 10.2, 4.4)
    mots = " ".join(f'<span class="mot-a-mot" style="--i:{i}">{html.escape(m, quote=False)}</span>'
                    for i, m in enumerate(P.typo(s["titre_or"]).split(" ")))
    return f"""
  <div class="guillemets" aria-hidden="true">«</div>
  <blockquote class="citation" data-id="titre" style="font-size:{px(pt)}px"><span class="blanc">{e(s['titre'])}</span><br>
    <span class="or">{mots}</span></blockquote>{logo()}"""


def l_tree(s):
    g, d = s["branches"]
    return f"""
  <h2 class="y-geant" data-id="yeba">{e(s['titre'])}</h2>
  <div class="branche gauche entree" style="--d:.5s"><strong>{e(g)}</strong><span>{e('Genèse · Savoir')}</span></div>
  <div class="branche droite entree" style="--d:1.1s"><strong>{e(d)}</strong><span>{e('Afrique · Transmission')}</span></div>{logo()}"""


def l_baobab(s):
    pt = P.lignes(s, 60, 6.2, 3.0)
    arbre = "" if s.get("fond") else '<img class="baobab" src="../assets/illustrations/baobab-or.png" alt="Silhouette dorée d\'un baobab">'
    return f"""
  <div class="baobab-texte">{deux_tons(s, pt)}<p class="sous">{e(s['texte'])}</p></div>{arbre}{logo()}"""


def l_split(s):
    def col(b):
        return f'<p class="label">{e(b["label"])}</p>' + "".join(f'<p class="mot">{e(m)}</p>' for m in b["mots"])

    return f"""
  <div class="moitie-bleue" data-id="droite"></div>
  <div class="split">
    <div><h2 class="titre-split" data-id="titre"><span class="blanc">{e(s['titre'])}</span></h2>{col(s['gauche'])}</div>
    <div><h2 class="titre-split"><span class="or">{e(s['titre_or'])}</span></h2>{col(s['droite'])}</div>
  </div>
  <img class="embleme" data-id="embleme" src="../assets/embleme-fond-sombre.png" alt="Emblème YEBA : trois pitons en réseau">"""


def l_values(s):
    v = "".join(f'<li class="fragment fade-up"><span class="n">{i + 1:02d}</span>{e(x)}</li>' for i, x in enumerate(s["items"]))
    return f"""<h2 class="titre-petit" data-id="titre">{e(s['titre'])}</h2><ol class="valeurs">{v}</ol>{logo()}"""


def l_timeline(s):
    n = len(s["etapes"])
    et = "".join(
        f'<div class="jalon{" dernier" if i == n - 1 else ""}" style="--i:{i}"><div class="date">{e(x["date"])}</div><div class="point"></div>'
        f'<div class="txt">{"<br>".join(e(m.strip()) for m in x["texte"].split("·"))}</div></div>'
        for i, x in enumerate(s["etapes"])
    )
    return f"""<h2 class="titre-petit" data-id="titre">{e(s['titre'])}</h2>
  <div class="frise"><div class="ligne"></div>{et}</div>{logo()}"""


def l_pillars(s):
    p = "".join(
        f'<div class="pilier entree" style="--d:{0.6 + i * 0.26:.2f}s"><div class="filigrane">0{i + 1}</div><div class="verbe">{e(x["titre"])}</div>'
        f'<div class="trait"></div><div class="detail">{e(x["texte"])}</div></div>'
        for i, x in enumerate(s["items"])
    )
    return f"""{une_ligne(s, 50)}<div class="piliers">{p}</div>{logo()}"""


def l_offres(s):
    t = "".join(
        f'<div class="offre entree{" phare" if x.get("phare") else ""} o{i}" style="--d:{0.6 + i * 0.14:.2f}s"><strong>{e(x["titre"])}</strong><span>{e(x["texte"])}</span></div>'
        for i, x in enumerate(s["items"])
    )
    return f"""{une_ligne(s)}<div class="offres">{t}</div>{logo()}"""


def l_journee(s):
    hor = C["meta"]["horaires"]
    h = P._heure
    h0, h1 = h(hor["debut"]), h(hor["fin"])
    xh = lambda v: (260 + (v - h0) / (h1 - h0) * 1400) / 1920 * 1600  # noqa: E731  (même repère que la vidéo)
    yb = 860 / 1080 * 900
    heures = "".join(
        f'<span class="heure {c}" style="left:{xh(h(v)):.0f}px;top:{yb + 17:.0f}px">{e(v)}</span>'
        for v, c in ((hor["debut"], "c"), (hor["pause_debut"], "d"), (hor["pause_fin"], "g"), (hor["fin"], "c"))
    )
    segs = "".join(
        f'<span class="segment{" pause" if g.get("pause") else ""}" style="left:{(xh(h(g["de"])) + xh(h(g["a"]))) / 2:.0f}px;top:{yb - 86:.0f}px">{e(g["label"])}</span>'
        for g in s["segments"]
    )
    frise = "" if s.get("fond") else f'<div class="frise-jour" style="left:{xh(h0):.0f}px;width:{xh(h1) - xh(h0):.0f}px;top:{yb - 3:.0f}px"></div>'
    return f"""
  <p class="kicker" style="left:96px;top:50px">{e(s['kicker'])}</p>
  <h2 class="sept-h" data-id="titre">{e(s['titre'])}</h2>
  <p class="sous-sept">{e(s['texte'])}</p>
  {frise}{segs}{heures}
  <p class="mention">{e(s['mention'])}</p>{logo()}"""


def l_confiance(s):
    q, n = s["qualiopi"], s["nda"]
    return f"""{une_ligne(s)}
  <div class="panneaux">
    <div class="panneau entree" style="--d:.7s"><strong>{e(q['titre'])}</strong><b>{e(q['ligne1'])}</b><small>{e(q['ligne2'])}</small></div>
    <div class="panneau entree" style="--d:1.05s"><strong>{e(n['titre'])}</strong><b class="moyen">{e(n['ligne1'])}</b><small>{e(n['ligne2'])}</small></div>
  </div>
  <div class="bandeau entree" style="--d:1.6s"><span class="or">✓</span> {e(s['texte'])}</div>{logo()}"""


def l_avantages(s):
    tuiles = "".join(
        f'<div class="avantage entree" style="--d:{0.6 + i * 0.18:.2f}s" data-id="av-{s["id"]}-{i}"><img src="../assets/pictos/{x["icone"]}.png" alt="">'
        f'<strong>{e(x["titre"])}</strong><span>{e(x["texte"])}</span></div>'
        for i, x in enumerate(s["items"])
    )
    pt = min(P.lignes(a, 54, 11.5, 2.4) for a in P.AVANTAGES)
    kicker = f'<p class="kicker" style="left:96px;top:50px">{e(s["kicker"])}</p>' if s.get("kicker") else ""
    return f"""
  {kicker}
  <div class="titre-avantages">{deux_tons(s, pt)}</div>
  <div class="avantages">{tuiles}</div>{logo()}"""


def l_atelier(s, retour=False):
    at = P.ATELIER
    tuiles = "".join(
        f'<div class="tuile{" bientot" if x.get("bientot") else ""}" data-id="tuile-{x["ref"]}" style="--c:#{at["familles"][x["famille"]]}">'
        f'<span data-id="nom-{x["ref"]}">{e(x["nom"])}</span>{"<em>bientôt</em>" if x.get("bientot") else ""}</div>'
        for x in at["items"]
    )
    leg = "".join(f'<span><i style="background:#{c}"></i>{e(f)}</span>' for f, c in at["familles"].items())
    return f"""
  <h2 class="titre-atelier" data-id="titre-atelier"><span class="blanc">{e(at['titre'])}</span> <span class="or">{e(at['titre_or'])}</span></h2>
  <div class="atelier">{tuiles}</div><div class="legende">{leg}</div>{logo()}"""


def l_focus(s):
    # La tuile du catalogue (data-id tuile-REF) se transforme en bande. Le nom pivoté ne porte PAS de data-id :
    # Auto-Animate imposerait « transform: none » à la fin du morph et annulerait la rotation.
    at = P.ATELIER
    item = next(i for i in at["items"] if i["ref"] == s["ref"])
    coul = at["familles"][item["famille"]]
    puces = "".join(f'<li class="entree" style="--d:{1.15 + i * 0.2:.2f}s"><span class="or">—</span> {e(p)}</li>' for i, p in enumerate(s["puces"]))
    chips = "".join(f'<span class="chip">{e(c)}</span>' for c in s["chips"])
    return f"""
  <div class="bande" data-id="tuile-{s['ref']}" style="--c:#{coul}"><span class="nom-vertical">{e(s['nom'])}</span></div>
  <div class="focus">
    {deux_tons(s, P.FOCUS_PT, 'titre focus-titre')}
    <ul class="puces">{puces}</ul>
    <div class="chips">{chips}</div>
  </div>{logo()}"""


def l_demo(s):
    pt = P.lignes(s, 72, P.W - 1.6, 4.2)
    return f"""
  <div class="live" data-id="live"><i></i>{e(s['kicker'])}</div>
  <div class="demo">{deux_tons(s, pt)}</div>{logo()}"""


def l_bientot(s):
    cartes = "".join(f'<div class="carte-bientot entree" style="--d:{0.9 + i * 0.22:.2f}s"><strong>{e(x["titre"])}</strong><span>{e(x["texte"])}</span></div>'
                     for i, x in enumerate(s["items"]))
    return f"""
  <p class="kicker" style="left:96px;top:60px">{e(s['kicker'])}</p>
  <h2 class="titre-bientot" data-id="titre">{e(s['titre'])}</h2>
  <div class="bientots{' un' if len(s['items']) == 1 else ''}">{cartes}</div>{logo()}"""


LAYOUTS = {
    "cover": l_cover, "statement": l_statement, "agenda": l_agenda, "team": l_team, "badges": l_badges, "word": l_word,
    "quote": l_quote, "tree": l_tree, "baobab": l_baobab, "split": l_split, "values": l_values, "timeline": l_timeline,
    "pillars": l_pillars, "offres": l_offres, "journee": l_journee, "confiance": l_confiance, "avantages": l_avantages,
    "atelier": l_atelier, "focus": l_focus, "demo": l_demo, "bientot": l_bientot,
}


def section(s, idx, retour=False):
    cache = ' data-visibility="hidden"' if s.get("cache") else ""
    notes = f"[{s['id']}] Épisode {s.get('episode', 0)} · {s['partie']} — ≈ {s['duree_s']} s\n\n{s['notes']}"
    if s["layout"] == "video":
        v = C["videos"][s["video"]]
        boucle = " data-background-video-loop" if v["boucle"] else ""
        auto = f' data-autoslide="{int(v["duree_s"] * 1000) + 150}"' if s.get("avance") else ""
        return (f'<section data-background-color="#000" data-background-image="../{v["apercu"]}" data-background-video="../{v["fichier"]}"{boucle}{auto} '
                f'data-background-size="cover" id="{s["id"]}"{cache}>'
                f'<h2 class="sr-only">{html.escape(s["titre"])}</h2>\n  <aside class="notes">{html.escape(notes)}</aside>\n</section>')
    corps = l_atelier(s, True) if retour else LAYOUTS[s["layout"]](s)
    fond_attr = ""
    if s.get("fond"):
        f = C["fonds"][s["fond"]]
        fond_attr = (f' data-background-image="../{f["apercu"]}" data-background-video="../{f["fichier"]}" data-background-video-muted'
                     f'{" data-background-video-loop" if f["boucle"] else ""} data-yeba-poster="../{f["apercu"]}"')
    couleur = FOND_COULEUR.get(s.get("teinte", "noir"), PAL["noir"])
    notes += f"\n\nVISUEL : {s['visuel']}\n\nANIMATION : {s['animation']}"
    return (f'<section data-auto-animate data-background-color="#{couleur}"{fond_attr} class="l-{s["layout"]}" '
            f'id="{s["id"]}"{cache}>{calques(s, idx)}{corps}\n  <aside class="notes">{html.escape(notes)}</aside>\n</section>')


CSS = """
@font-face{font-family:Montserrat;font-weight:400;font-display:block;src:url(fonts/montserrat-latin-400-normal.woff2) format('woff2')}
@font-face{font-family:Montserrat;font-weight:700;font-display:block;src:url(fonts/montserrat-latin-700-normal.woff2) format('woff2')}
@font-face{font-family:Montserrat;font-weight:800;font-display:block;src:url(fonts/montserrat-latin-800-normal.woff2) format('woff2')}
@font-face{font-family:Montserrat;font-weight:900;font-display:block;src:url(fonts/montserrat-latin-900-normal.woff2) format('woff2')}
:root{--noir:#121212;--bleu:#1B3A6B;--nuit:#0E2140;--or:#C9A84C;--or-clair:#E9D7A0;--blanc:#fff;--gris:#B8BCC6;--gris2:#8C93A0;--verre:rgba(255,255,255,.06)}
html,body{background:var(--noir)}
.reveal{font-family:Montserrat,system-ui,sans-serif;color:var(--blanc);font-size:47px;line-height:1.22}
.reveal .slides section{height:100%;text-align:left;padding:0;box-sizing:border-box}
.reveal .slides section>*{position:absolute;margin:0}
.reveal h1,.reveal h2{font-family:Montserrat;font-weight:800;text-transform:none;letter-spacing:-.01em;margin:0;line-height:1.22;
  hyphens:none;word-break:normal;overflow-wrap:normal;text-shadow:none}
.reveal img{margin:0;max-width:none;max-height:none}
.sr-only{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.blanc{color:var(--blanc)}.or{color:var(--or)}.centre{text-align:center!important}
.calque{pointer-events:none}.vignette{left:0;top:0;width:1600px;height:900px}
.kicker{left:114px;top:142px;font-weight:800;font-size:37px;letter-spacing:.3em;color:var(--or);text-transform:uppercase}
.petit-logo{right:48px;bottom:30px;width:114px}
.titre-ligne{left:96px;top:54px;right:96px;white-space:nowrap}
.titre-petit{left:96px;top:54px;font-size:73px}
/* couverture */
.logo-cover{left:calc(50% - 216px);top:36px;width:432px}
.titre-cover{left:96px;right:96px;top:504px;text-align:center}
.meta{left:0;right:0;bottom:60px;text-align:center;color:var(--gris);font-size:40px}
/* déclaration */
.barre{left:54px;top:210px;width:14px;height:516px;background:var(--or)}
.statement{left:114px;top:222px;height:516px;display:flex;align-items:center}
.statement h2{position:static}
.illu-ue{right:84px;top:90px;width:264px;animation:tourne 40s linear infinite}
@keyframes tourne{to{transform:rotate(360deg)}}
/* agenda */
.titre-agenda{left:96px;top:50px;font-size:57px}
.agenda{left:96px;top:166px;list-style:none;padding:0 0 0 42px;width:1100px}
.agenda li{display:flex;align-items:center;height:95px;font-size:47px;color:var(--gris2);font-weight:400;white-space:nowrap}
.agenda li .n{width:108px;font-weight:800}.agenda li .t{width:426px}.agenda li .s{font-size:40px}
.agenda li.actif{color:var(--blanc);font-weight:800}.agenda li.actif .t{font-size:53px}.agenda li.actif .n,.agenda li.actif .s{color:var(--or)}
.marqueur{left:0;top:calc(var(--actif) * 95px + 14px);width:16px;height:66px;background:var(--or)}
.agenda-big{right:66px;top:300px;font-weight:900;font-size:250px;line-height:1;color:var(--or)}
/* équipe */
.cartes{left:60px;right:60px;top:204px;display:flex;gap:36px;justify-content:center}
.carte{position:relative!important;width:462px;height:582px;background:var(--verre);border:2px solid rgba(201,168,76,.55);border-radius:30px;text-align:center;padding-top:42px;box-sizing:border-box}
.photo{width:216px;height:216px;margin:0 auto;border-radius:50%;background:var(--bleu);border:4px solid var(--or);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:73px}
.nom{font-weight:800;font-size:47px;margin-top:34px;padding:0 24px;line-height:1.15}.role{color:var(--gris);font-size:40px;margin-top:20px;padding:0 24px}
/* badges */
.badges{left:90px;right:90px;top:240px;display:flex;flex-wrap:wrap;gap:50px 38px;justify-content:center}
.badge{position:relative!important;width:444px;height:210px;border:3px solid var(--or);border-radius:42px;background:var(--verre);display:flex;align-items:center;justify-content:center;text-align:center;font-weight:800;font-size:44px;padding:0 24px;box-sizing:border-box}
/* mot / Y */
.mot-geant{left:0;right:0;top:110px;text-align:center;font-weight:900;font-size:416px;color:var(--or);line-height:1}
.traduction{left:0;right:0;top:640px;text-align:center;font-weight:800;font-size:60px}
.y-geant{left:0;right:0;top:40px;text-align:center;font-weight:900;font-size:566px;color:var(--or);line-height:1}
.branche{top:150px;width:534px;font-size:47px}.branche strong{display:block;font-weight:800;line-height:1.15}
.branche span{display:block;color:var(--gris);font-size:43px;margin-top:22px;font-weight:400}
.branche.gauche{left:36px;text-align:right}.branche.droite{right:36px}
/* citation */
.guillemets{left:30px;top:10px;font-weight:900;font-size:333px;color:#5A4A22;line-height:1}
.citation{left:288px;top:222px;width:1224px;padding:0;border:0;box-shadow:none;font-style:normal;font-weight:800;line-height:1.22;background:none}
.mot-a-mot{display:inline-block;opacity:0}
.present .mot-a-mot{animation:parole .5s ease-out forwards;animation-delay:calc(1.2s + var(--i) * .3s)}
@keyframes parole{from{opacity:0;transform:translateY(.3em)}to{opacity:1;transform:none}}
/* baobab */
.baobab-texte{left:96px;top:192px;width:760px}.baobab-texte h2{position:static}
.sous{color:var(--gris);font-size:47px;margin-top:36px!important;position:static!important}
.baobab{right:120px;top:72px;height:720px}
/* deux mondes */
.moitie-bleue{left:800px;top:0;width:800px;height:900px;background:rgba(27,58,107,.88)}
.split{left:0;top:0;width:1600px;height:900px;display:grid;grid-template-columns:1fr 1fr}
.split>div{position:relative;padding-top:54px;text-align:center}
.titre-split{position:static!important;font-size:83px}
.label{color:var(--or);font-weight:800;font-size:40px;letter-spacing:.3em;margin:48px 0 8px!important}
.mot{font-weight:800;font-size:60px;margin:4px 0!important}
.embleme{left:calc(50% - 216px);bottom:48px;width:432px}
/* valeurs */
.valeurs{left:96px;top:174px;list-style:none;padding:0}
.valeurs li{font-weight:800;font-size:67px;height:130px;display:flex;align-items:center}
.valeurs .n{color:var(--or);font-weight:900;font-size:80px;width:204px}
/* frise */
.frise{left:42px;right:42px;top:300px;height:500px;display:flex}
.frise .ligne{position:absolute;left:0;right:0;top:165px;height:7px;background:var(--or);transform-origin:left}
.present .frise .ligne{animation:trace 1.5s ease-out both}@keyframes trace{from{transform:scaleX(0)}}
.jalon{flex:1;text-align:center;position:relative}
.present .jalon{animation:apparait .6s ease-out both;animation-delay:calc(.9s + var(--i) * .38s)}
@keyframes apparait{from{opacity:0;transform:translateY(20px)}}
.jalon .date{height:140px;display:flex;align-items:flex-end;justify-content:center;color:var(--or);font-weight:800;font-size:57px;white-space:nowrap}
.jalon .point{width:41px;height:41px;border-radius:50%;background:var(--or);margin:8px auto 0}
.jalon.dernier .point{background:#fff;width:60px;height:60px;margin-top:-2px}
.jalon .txt{font-size:47px;margin-top:48px;line-height:1.2}
/* piliers */
.piliers{left:96px;right:96px;top:236px;display:flex;gap:54px}
.pilier{position:relative!important;flex:1}.filigrane{font-weight:900;font-size:183px;color:#2E2A20;line-height:1}
.verbe{font-weight:800;font-size:66px;margin-top:6px;white-space:nowrap}.trait{width:120px;height:10px;background:var(--or);margin:24px 0}
.detail{color:var(--or);font-weight:800;font-size:47px;line-height:1.2}
/* offres */
.offres{left:96px;right:96px;top:222px;display:grid;grid-template-columns:repeat(6,1fr);grid-template-rows:264px 264px;gap:26px}
.offre{position:relative!important;border:1.5px solid rgba(201,168,76,.5);background:var(--verre);border-radius:26px;padding:0 46px;display:flex;flex-direction:column;justify-content:center}
.offre strong{font-weight:800;font-size:54px;line-height:1.1}.offre span{color:var(--or);font-weight:800;font-size:43px;margin-top:8px}
.offre.phare{background:var(--or);border:0}.offre.phare strong,.offre.phare span{color:var(--noir)}
.o0{grid-column:1/3}.o1{grid-column:3/5}.o2{grid-column:5/7}.o3{grid-column:1/4}.o4{grid-column:4/7}
/* journée */
.sept-h{left:84px;top:86px;font-weight:900;font-size:200px;color:var(--or);line-height:1;white-space:nowrap}
.sous-sept{left:440px;top:150px;font-weight:800;font-size:50px;white-space:nowrap}
.frise-jour{height:6px;background:var(--or)}
.heure{transform:translateX(-50%);font-weight:800;font-size:40px;white-space:nowrap}
.heure.d{transform:translateX(calc(-100% + 30px))}.heure.g{transform:translateX(-30px)}
.segment{transform:translateX(-50%);font-weight:800;font-size:40px;color:var(--or);white-space:nowrap}
.segment.pause{color:var(--gris)}
.mention{left:96px;bottom:22px;color:var(--gris);font-size:40px}
/* confiance */
.panneaux{left:96px;right:96px;top:228px;display:flex;gap:60px}
.panneau{position:relative!important;flex:1;height:426px;background:var(--nuit);border:2px solid rgba(201,168,76,.6);border-radius:28px;padding:0 54px;display:flex;flex-direction:column;justify-content:center}
.panneau strong{font-weight:900;font-size:100px;color:var(--or);line-height:1}.panneau b{font-weight:800;font-size:50px;margin-top:18px}
.panneau b.moyen{font-size:43px}.panneau small{color:var(--gris);font-size:40px;margin-top:10px;line-height:1.2}
.bandeau .or{margin-right:18px}.bandeau{left:96px;right:96px;top:686px;height:102px;background:var(--nuit);border:2px solid var(--or);border-radius:60px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:47px}
/* avantages */
.titre-avantages{left:96px;top:84px}.titre-avantages h2{position:static}
.avantages{left:84px;right:84px;top:372px;display:flex;gap:38px}
.avantage{position:relative!important;flex:1;height:408px;background:var(--verre);border:1.5px solid rgba(201,168,76,.55);border-radius:28px;padding:34px 30px;box-sizing:border-box}
.avantage img{width:114px;display:block}.avantage strong{display:block;font-weight:800;font-size:50px;margin-top:22px;line-height:1.15}
.avantage span{display:block;color:var(--or);font-weight:800;font-size:43px;margin-top:8px;line-height:1.2}
/* atelier */
.titre-atelier{left:96px;top:48px;font-size:80px;white-space:nowrap}
.atelier{left:61px;right:61px;top:180px;display:grid;grid-template-columns:repeat(4,1fr);gap:22px 20px}
.tuile{position:relative!important;height:146px;background:var(--verre);border:3px solid var(--c);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;font-weight:800;font-size:38px;line-height:1.15;padding:0 10px}
.tuile.bientot{border-style:dashed}.tuile em{font-style:normal;color:var(--or);font-size:36px}
.legende{left:61px;top:686px;width:1100px;display:flex;flex-wrap:wrap;gap:12px 46px;font-size:40px}
.legende span{white-space:nowrap}.legende i{display:inline-block;width:34px;height:34px;margin-right:14px;vertical-align:-4px}
/* fiche formation */
.bande{left:0;top:0;width:492px;height:900px;background:var(--c);display:flex;align-items:center;justify-content:center}
.nom-vertical{transform:rotate(-90deg);width:820px;text-align:center;color:var(--noir);font-weight:900;font-size:70px;line-height:1.1}
.focus{left:576px;top:0;right:80px;height:900px}.focus>*{position:absolute;margin:0}
.focus-titre{left:0;top:66px;right:0}
.puces{left:0;top:480px;list-style:none;padding:0!important;margin:0!important}
.puces li{font-weight:800;font-size:53px;margin-bottom:12px}
.chips{left:0;top:726px;display:flex;gap:28px}
.chip{border:3px solid var(--or);border-radius:60px;padding:12px 32px;font-weight:800;font-size:40px;white-space:nowrap}
/* démo */
.live{left:96px;top:120px;background:#E53935;border-radius:60px;padding:14px 40px;font-weight:800;font-size:43px;letter-spacing:.12em;display:flex;align-items:center;gap:22px}
.live i{width:26px;height:26px;border-radius:50%;background:#fff;animation:pulse 1.2s ease-in-out infinite}
@keyframes pulse{50%{opacity:.2}}
.demo{left:96px;top:252px;right:96px;height:504px;display:flex;align-items:center}.demo h2{position:static}
/* à suivre */
.titre-bientot{left:96px;top:114px;font-size:147px;white-space:nowrap}
.bientots{left:84px;right:84px;top:384px;display:flex;gap:38px}
.carte-bientot{position:relative!important;flex:1;height:300px;background:var(--verre);border:1.5px solid rgba(201,168,76,.55);border-radius:30px;padding:0 42px;display:flex;flex-direction:column;justify-content:center}
.carte-bientot strong{font-weight:800;font-size:53px;line-height:1.15}.carte-bientot span{color:var(--or);font-weight:800;font-size:40px;margin-top:10px}
.bientots.un{right:auto;width:768px}.bientots.un .carte-bientot{height:312px}.bientots.un strong{font-size:80px}.bientots.un span{font-size:50px}
.present .entree{animation:apparait .7s cubic-bezier(.16,1,.3,1) both;animation-delay:var(--d,0s)}
.present .entree.zoom{animation-name:zoome}@keyframes zoome{from{opacity:0;transform:scale(.82)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}.mot-a-mot{opacity:1}}
"""

JS = """
// « Réduire les animations » : fonds vidéo → images fixes, avant l'initialisation de Reveal.
const SOBRE = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (SOBRE) {
  document.querySelectorAll('section[data-yeba-poster]').forEach(s => {
    s.removeAttribute('data-background-video');
  });
}
Reveal.initialize({
  width: 1600, height: 900, margin: 0, center: false, hash: true, controls: true, progress: true,
  transition: 'fade', transitionSpeed: 'slow', backgroundTransition: 'fade',
  autoAnimateDuration: 1.2, autoAnimateEasing: 'cubic-bezier(.65,0,.35,1)', autoAnimateUnmatched: true,
  autoAnimate: !SOBRE, autoSlideStoppable: true, plugins: [RevealNotes]
});
"""


def construire():
    sections = []
    for idx, (s, retour) in enumerate(P.sequence()):
        sections.append(section(s, idx, retour))
    doc = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>YEBA — Saison 1 · Soirée de lancement</title>
<link rel="stylesheet" href="vendor/reset.css">
<link rel="stylesheet" href="vendor/reveal.css">
<style>{CSS}</style>
</head>
<body>
<div class="reveal"><div class="slides">
{chr(10).join(sections)}
</div></div>
<script src="vendor/reveal.js"></script>
<script src="vendor/plugin/notes.js"></script>
<script>{JS}</script>
</body>
</html>
"""
    (ICI / "index.html").write_text(doc, encoding="utf-8")
    print(f"OK : {ICI / 'index.html'} ({len(sections)} slides)")


if __name__ == "__main__":
    construire()
