"""Génère tous les visuels Instagram YEBA IA (posts, carrousel, couvertures
de réels, couvertures « À la une », photo de profil, maquette du profil).

Usage : python src/generate.py            (depuis instagram-yeba-ia/)
Dépendances : pip install playwright pillow  (Chromium déjà présent)
"""
import os
import random
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "src" / "assets"
BUILD = ROOT / "src" / "_build"
OUT = ROOT / "visuels"

CHROMIUM = os.environ.get("CHROMIUM_PATH", "/opt/pw-browsers/chromium")
NAVY, NAVY_DEEP, GOLD, CREAM, INK = "#1B3A6B", "#0F2344", "#C9AB4C", "#F7F3E8", "#0B1A33"

FONTS = "".join(
    f"@font-face{{font-family:'Montserrat';font-weight:{w};src:url('{(ASSETS / 'fonts' / f'Montserrat-{w}.woff2').as_uri()}') format('woff2')}}"
    for w in (500, 600, 700, 800, 900))

BASE_CSS = f"""
{FONTS}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Montserrat',sans-serif;-webkit-font-smoothing:antialiased}}
.c{{position:relative;overflow:hidden;display:flex;flex-direction:column}}
.navy{{background:radial-gradient(120% 90% at 80% 0%,{NAVY} 0%,{NAVY_DEEP} 70%);color:#fff}}
.cream{{background:{CREAM};color:{NAVY}}}
.gold{{background:linear-gradient(160deg,#D9BE68 0%,{GOLD} 55%,#B8963A 100%);color:{INK}}}
.net{{position:absolute;inset:0;z-index:0;-webkit-mask-image:linear-gradient(180deg,#000 0%,transparent 17%)}}
.z{{position:relative;z-index:1}}
.tag{{display:inline-block;font-weight:800;font-size:38px;letter-spacing:4px;padding:16px 30px;border-radius:60px}}
.navy .tag{{background:{GOLD};color:{INK}}}
.cream .tag{{background:{NAVY};color:#fff}}
.gold .tag{{background:{INK};color:{GOLD}}}
.hl-navy{{color:{GOLD}}} .hl-cream{{color:#8A6D1A}} .hl-gold{{color:{GOLD};background:{INK};padding:0 14px;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.foot{{display:flex;align-items:center;gap:22px;font-weight:800;font-size:32px;letter-spacing:2px}}
.foot img{{height:58px}}
.foot .s{{font-weight:600;font-size:24px;letter-spacing:.5px;opacity:.85;white-space:nowrap}}
.foot>div:last-child{{white-space:nowrap}}
.src{{font-size:22px;font-weight:600;opacity:.8;line-height:1.35}}
"""


def fr(t):
    """Espaces insécables typographiques : jamais de « ? » ou « » » seul en début de ligne."""
    for a, b in ((" ?", "&nbsp;?"), (" !", "&nbsp;!"), (" »", "&nbsp;»"), ("« ", "«&nbsp;"),
                 (" :", "&nbsp;:"), (" %", "&nbsp;%"), (" →", "&nbsp;→")):
        t = t.replace(a, b)
    return t


def net_svg(w, h, color, opacity, seed, n=26):
    """Réseau de nœuds reliés, rappel du logo YEBA."""
    rnd = random.Random(seed)
    pts = [(rnd.uniform(0, w), rnd.uniform(0, h)) for _ in range(n)]
    lines = []
    for i, (x, y) in enumerate(pts):
        near = sorted(pts, key=lambda p: (p[0] - x) ** 2 + (p[1] - y) ** 2)[1:3]
        for (a, b) in near:
            lines.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{a:.0f}" y2="{b:.0f}"/>')
    dots = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([7, 9, 12])}"/>' for x, y in pts)
    return (f'<svg class="net" viewBox="0 0 {w} {h}" preserveAspectRatio="none">'
            f'<g stroke="{color}" stroke-width="4" opacity="{opacity}">{"".join(lines)}</g>'
            f'<g fill="{color}" opacity="{opacity}">{dots}</g></svg>')


def net_for(theme, w, h, seed):
    return {"navy": net_svg(w, h, GOLD, .16, seed), "cream": net_svg(w, h, NAVY, .07, seed),
            "gold": net_svg(w, h, "#FFFFFF", .20, seed)}[theme]


def mark_for(theme):
    return "mark_white.png" if theme == "navy" else "mark.png"


def footer(theme, right=""):
    return (f'<div class="foot z"><img src="../assets/{mark_for(theme)}">'
            f'<div>YEBA IA<div class="s">IA · RGPD · Cyber · IA Act — 974</div></div>'
            f'<div style="margin-left:auto;font-size:32px">{right}</div></div>')


def page(w, h, theme, body, seed=1, pad="90px 84px 70px"):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head>'
            f'<body><div id="c" class="c {theme}" style="width:{w}px;height:{h}px;padding:{pad}">'
            f'{net_for(theme, w, h, seed)}{body}</div></body></html>')


# ---------------------------------------------------------------- POSTS 3:4
W, H = 1080, 1440


def post(theme, tag, hook, sub, right="", seed=1, src=""):
    hl = f"hl-{theme}"
    hook = fr(hook).replace("[", f'<span class="{hl}">').replace("]", "</span>")
    sub = fr(sub)
    body = (f'<div class="z"><span class="tag">{tag}</span></div>'
            f'<div class="z" style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:44px">'
            f'<div style="font-weight:900;font-size:94px;line-height:1.14;letter-spacing:-1px">{hook}</div>'
            f'<div style="font-weight:600;font-size:48px;line-height:1.3">{sub}</div></div>'
            + (f'<div class="src z" style="margin-bottom:26px">{src}</div>' if src else "")
            + footer(theme, right))
    return page(W, H, theme, body, seed)


POSTS = {
    "post01_manifeste": post(
        "navy", "BIENVENUE", "L'IA ne va pas vous [remplacer.]",
        "Quelqu'un qui sait s'en servir… peut-être.<br><b>Ici, on vous apprend à être ce quelqu'un.</b>",
        "Abonnez-vous ↗", seed=3),
    "post04_rgpd_mythe": post(
        "gold", "RGPD", "« Le RGPD, c'est pour les [grosses boîtes.] »",
        '<span style="display:inline-block;border:8px solid #fff;color:#fff;background:#0B1A33;'
        'padding:6px 30px;font-weight:900;font-size:76px;transform:rotate(-4deg)">FAUX</span>'
        '<br><br>Un seul fichier clients suffit. Même sur Excel.',
        "Enregistrez ⌑", seed=9, src="Source : RGPD, art. 2 et 4 — champ d'application sans seuil de taille"),
    "post05_pyramide_mythe": post(
        "cream", "FORMATION ADULTE", "« On retient 10 % de ce qu'on lit… » [Mythe.]",
        "La célèbre pyramide de l'apprentissage n'a jamais été démontrée.<br><b>Ce qui marche vraiment ? →</b>",
        "Enregistrez ⌑", seed=5,
        src="Source : K. Letrud, « A rebuttal of NTL Institute's learning pyramid », Education, 2012"),
    "post09_cta_diag": post(
        "gold", "PASSEZ À L'ACTION", "Votre entreprise est-elle [prête pour l'IA ?]",
        "IA · RGPD · Cyber · IA Act<br><b>Écrivez « DIAG » en message privé.</b>",
        "DM « DIAG » ✉", seed=11),
}


def about_post():
    certifs = ["Google AI Specialist", "Google Professional AI", "SecNumacadémie — ANSSI",
               "MOOC RGPD — CNIL", "Référent handicap", "Organisme certifié Qualiopi*"]
    items = "".join(f'<div style="display:flex;gap:22px;align-items:center;font-weight:700;font-size:42px">'
                    f'<span style="width:22px;height:22px;border-radius:50%;background:{GOLD};flex:none"></span>{c}</div>'
                    for c in certifs)
    body = (f'<div class="z"><span class="tag">QUI SUIS-JE ?</span></div>'
            f'<div class="z" style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:40px">'
            f'<div style="font-weight:900;font-size:88px;line-height:1.05">Aurélien LUMEKA</div>'
            f'<div style="font-weight:600;font-size:44px;line-height:1.3">Formateur vente &amp; management depuis 2021.'
            f'<br><b style="color:#9A7B22">Aujourd\'hui : l\'IA qui fait gagner du temps, en toute conformité.</b></div>'
            f'<div style="display:flex;flex-direction:column;gap:18px">{items}</div></div>'
            f'<div class="src z" style="margin-bottom:26px">* Actions de formation — certificat 25FOF02027.1</div>'
            + footer("cream", "La Réunion 974"))
    return page(W, H, "cream", body, 7)


POSTS["post02_qui_suis_je"] = about_post()

# ------------------------------------------------ CARROUSEL IA ACT (7 slides)
SRC_ACT = "Source : Règlement (UE) 2024/1689 (IA Act), art. 4 et 113 — eur-lex.europa.eu"


def slide(theme, n, title, content, seed, src=SRC_ACT, cover=False):
    hl = f"hl-{theme}"
    title, content = fr(title), fr(content)
    title = title.replace("[", f'<span class="{hl}">').replace("]", "</span>")
    size = 96 if cover else 80
    body = (f'<div class="z" style="display:flex;justify-content:space-between;align-items:center">'
            f'<span class="tag">IA ACT</span><span style="font-weight:800;font-size:34px">{n}/7</span></div>'
            f'<div class="z" style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:48px">'
            f'<div style="font-weight:900;font-size:{size}px;line-height:1.06">{title}</div>{content}</div>'
            f'<div class="src z" style="margin-bottom:26px">{src}</div>'
            + footer(theme, "Swipez →" if n < 7 else ""))
    return page(W, H, theme, body, seed)


def bullets(items, size=46):
    return ('<div style="display:flex;flex-direction:column;gap:26px">' + "".join(
        f'<div style="display:flex;gap:26px;font-weight:700;font-size:{size}px;line-height:1.25">'
        f'<span style="flex:none;width:64px;height:64px;border-radius:50%;background:currentColor;'
        f'display:flex;align-items:center;justify-content:center"><span style="filter:invert(1);'
        f'font-weight:900;font-size:34px">{i + 1}</span></span><span>{t}</span></div>'
        for i, t in enumerate(items)) + "</div>")


P = lambda t, s=48: f'<div style="font-weight:600;font-size:{s}px;line-height:1.32">{t}</div>'
CAROUSEL = {
    "carrousel_ia_act_1": slide("cream", 1, "Vos salariés utilisent l'IA ? [Vous avez une obligation.]",
                                P("ChatGPT, Copilot, Gemini, Mistral… <b>Lisez ceci avant votre prochain prompt.</b>"),
                                21, cover=True),
    "carrousel_ia_act_2": slide("navy", 2, "IA Act = [la loi européenne] sur l'IA",
                                P("Règlement (UE) 2024/1689.<br>En vigueur depuis le <b>1er août 2024</b>.<br>"
                                  "Il s'applique <b>par étapes</b>, jusqu'en 2027."), 22),
    "carrousel_ia_act_3": slide("gold", 3, "Article 4 : [la maîtrise de l'IA]",
                                P("Les entreprises qui <b>utilisent</b> l'IA doivent veiller à ce que leur "
                                  "personnel ait un <b>niveau suffisant de maîtrise de l'IA</b>.<br><br>"
                                  "Applicable depuis le <b>2 février 2025</b>."), 23),
    "carrousel_ia_act_4": slide("cream", 4, "Qui est concerné ? [Vous, sûrement.]",
                                P("Le texte vise les <b>fournisseurs</b> d'IA… <b>et les « déployeurs »</b> : "
                                  "toute entreprise qui utilise un système d'IA dans son activité pro.<br><br>"
                                  "Chatbot, rédaction de devis, tri de CV, compta assistée…"), 24),
    "carrousel_ia_act_5": slide("navy", 5, "Concrètement, [on fait quoi ?]",
                                bullets(["Lister les outils d'IA utilisés", "Écrire une charte d'usage",
                                         "Former selon le poste et le risque", "Garder les preuves (attestations)"]), 25),
    "carrousel_ia_act_6": slide("gold", 6, "Et le RGPD ? [Il s'ajoute.]",
                                P("Données clients ou salariés dans une IA = <b>RGPD aussi</b>.<br><br>"
                                  "IA Act + RGPD = <b>double conformité</b>. On les traite ensemble, pas l'un sans l'autre."),
                                26, src="Sources : Règlement (UE) 2024/1689 ; RGPD (UE) 2016/679 — cnil.fr"),
    "carrousel_ia_act_7": slide("cream", 7, "Formez vos équipes, [ici à La Réunion.]",
                                P("Formation intra ou inter-entreprise · Audit IA Act &amp; RGPD<br><br>"
                                  '<span style="background:#1B3A6B;color:#fff;padding:14px 30px;border-radius:50px;'
                                  'font-weight:800">DM « IA ACT »</span>'), 27,
                                src="Enregistrez ce post · Partagez-le à votre dirigeant·e"),
}

# ---------------------------------------------- COUVERTURES DE RÉELS 9:16
RW, RH = 1080, 1920


def reel_cover(theme, kicker, hook, seed):
    hl = f"hl-{theme}"
    hook = fr(hook).replace("[", f'<span class="{hl}">').replace("]", "</span>")
    # Texte clé dans la zone centrale 3:4 (y 240→1680) : c'est ce que montre la grille.
    body = (f'<div class="z" style="position:absolute;left:84px;right:84px;top:300px;bottom:300px;'
            f'display:flex;flex-direction:column;justify-content:center;gap:50px">'
            f'<div><span class="tag">{kicker}</span></div>'
            f'<div style="font-weight:900;font-size:100px;line-height:1.07">{hook}</div>'
            f'<div style="font-weight:800;font-size:44px;display:flex;align-items:center;gap:20px">'
            f'<span style="width:74px;height:74px;border-radius:50%;background:currentColor;display:flex;'
            f'align-items:center;justify-content:center"><span style="filter:invert(1);font-size:34px">▶</span></span>'
            f'RÉEL · 15 s</div></div>'
            f'<div class="z" style="position:absolute;left:84px;right:84px;bottom:320px">{footer(theme)}</div>')
    return page(RW, RH, theme, body, seed, pad="0")


REEL_COVERS = {
    "reel01_couverture": reel_cover("cream", "IA &amp; DONNÉES", "Vous avez collé quoi dans [ChatGPT] ce matin ?", 31),
    "reel02_couverture": reel_cover("navy", "IA ACT", "3 dates que [votre entreprise] doit connaître", 32),
    "reel03_couverture": reel_cover("cream", "CYBER", "Ce mail de votre banque est-il [un piège ?]", 33),
}

# -------------------------------------------------- COUVERTURES « À LA UNE »
ICONS = {  # tracés SVG 200x200, trait or
    "ia": '<rect x="50" y="50" width="100" height="100" rx="14"/><text x="100" y="118" font-size="48" '
          'font-weight="900" text-anchor="middle" fill="currentColor" stroke="none">IA</text>'
          + "".join(f'<line x1="{x}" y1="22" x2="{x}" y2="50"/><line x1="{x}" y1="150" x2="{x}" y2="178"/>'
                    f'<line x1="22" y1="{x}" x2="50" y2="{x}"/><line x1="150" y1="{x}" x2="178" y2="{x}"/>'
                    for x in (75, 100, 125)),
    "rgpd": '<path d="M100 20 L165 45 V100 C165 140 135 168 100 182 C65 168 35 140 35 100 V45 Z"/>'
            + "".join(f'<circle cx="{100 + 38 * __import__("math").cos(a * 0.5236):.1f}" '
                      f'cy="{100 + 38 * __import__("math").sin(a * 0.5236):.1f}" r="5" fill="currentColor"/>'
                      for a in range(12)),
    "cyber": '<rect x="45" y="90" width="110" height="85" rx="14"/><path d="M70 90 V65 a30 30 0 0 1 60 0 V90"/>'
             '<circle cx="100" cy="128" r="10" fill="currentColor"/><line x1="100" y1="138" x2="100" y2="155"/>',
    "iaact": '<line x1="100" y1="30" x2="100" y2="170"/><line x1="40" y1="55" x2="160" y2="55"/>'
             '<line x1="60" y1="170" x2="140" y2="170"/><path d="M40 55 L15 115 H65 Z"/><path d="M160 55 L135 115 H185 Z"/>',
    "formations": '<path d="M100 40 L185 80 L100 120 L15 80 Z"/><path d="M55 100 V140 C80 162 120 162 145 140 V100"/>'
                  '<line x1="175" y1="85" x2="175" y2="140"/>',
    "avis": '<path d="M100 22 L122 72 L176 76 L135 112 L148 166 L100 138 L52 166 L65 112 L24 76 L78 72 Z"/>',
    "moi": '<circle cx="100" cy="70" r="36"/><path d="M35 178 C40 130 70 115 100 115 C130 115 160 130 165 178"/>',
    "contact": '<path d="M30 45 H170 V140 H90 L55 172 V140 H30 Z"/><circle cx="70" cy="93" r="8" fill="currentColor"/>'
               '<circle cx="100" cy="93" r="8" fill="currentColor"/><circle cx="130" cy="93" r="8" fill="currentColor"/>',
}


def highlight(key, theme):
    color = GOLD if theme == "navy" else NAVY
    body = (f'<div class="z" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">'
            f'<svg width="560" height="560" viewBox="0 0 200 200" fill="none" stroke="{color}" stroke-width="9" '
            f'stroke-linecap="round" stroke-linejoin="round" style="color:{color}">{ICONS[key]}</svg></div>')
    return page(1080, 1920, theme, body, seed=40 + len(key), pad="0")


# ------------------------------------------------------ PHOTO DE PROFIL
def profile_pic():
    body = ('<div class="z" style="position:absolute;inset:0;display:flex;flex-direction:column;'
            'align-items:center;justify-content:center;gap:34px">'
            '<img src="../assets/mark.png" style="width:640px">'
            f'<div style="font-weight:900;font-size:230px;line-height:.9;letter-spacing:-4px;color:{NAVY}">'
            f'YEBA <span style="color:{GOLD}">IA</span></div></div>')
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body>'
            f'<div id="c" class="c" style="width:1080px;height:1080px;background:#fff">{body}</div></body></html>')


# ------------------------------------------------------ MAQUETTE DU PROFIL
BIO = ("🤖 L'IA, le RGPD &amp; la cyber… <b>enfin clairs</b><br>"
       "🎓 Formations &amp; audits TPE-PME · 974<br>"
       "✅ Organisme Qualiopi · Google AI<br>"
       "👇 Écrivez « DIAG » en DM")  # 134 caractères (limite Instagram : 150)
HL_LABELS = [("moi", "Qui suis-je"), ("ia", "IA"), ("rgpd", "RGPD"), ("cyber", "Cyber"),
             ("iaact", "IA Act"), ("formations", "Formations"), ("avis", "Avis"), ("contact", "Contact")]
GRID = ["post09_cta_diag", "reel02_couverture", "post05_pyramide_mythe",
        "post04_rgpd_mythe", "reel03_couverture", "carrousel_ia_act_1",
        "reel01_couverture", "post02_qui_suis_je", "post01_manifeste"]


def folder(name):
    return "reels" if name.startswith("reel") else "carrousel_ia_act" if name.startswith("carrousel") else "posts"


def mockup():
    hls = "".join(f'<div style="text-align:center;width:150px"><div style="width:130px;height:130px;border-radius:50%;'
                  f'border:3px solid #ddd;padding:6px;margin:0 auto"><div style="width:100%;height:100%;border-radius:50%;'
                  f'background:url(../../visuels/a_la_une/{k}.png) center/cover"></div></div>'
                  f'<div style="font-size:24px;margin-top:10px;font-weight:600">{lbl}</div></div>'
                  for k, lbl in HL_LABELS[:6])
    cells = "".join(f'<div style="aspect-ratio:3/4;background:url(../../visuels/{folder(g)}/{g}.png) '
                    f'center/cover"></div>' for g in GRID)
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}'
            f'body{{font-family:-apple-system,"Montserrat",sans-serif;background:#fff;color:#111}}</style></head><body>'
            f'<div id="c" style="width:1080px;padding:40px 0 0">'
            f'<div style="padding:0 40px;font-weight:800;font-size:44px;margin-bottom:34px">yeba.ia ✓</div>'
            f'<div style="display:flex;align-items:center;gap:60px;padding:0 40px">'
            f'<div style="width:220px;height:220px;border-radius:50%;background:url(../../visuels/profil/photo_profil.png) '
            f'center/cover;border:2px solid #eee;flex:none"></div>'
            f'<div style="display:flex;gap:70px;font-size:28px;text-align:center"><div><b style="font-size:40px">9</b><br>publications</div>'
            f'<div><b style="font-size:40px">—</b><br>followers</div><div><b style="font-size:40px">—</b><br>suivi(e)s</div></div></div>'
            f'<div style="padding:26px 40px;font-size:29px;line-height:1.45"><b>YEBA IA | IA · RGPD · Cyber 974</b><br>'
            f'<span style="color:#737373">Formation</span><br>{BIO}<br><span style="color:#00376b;font-weight:600">🔗 lien du site</span></div>'
            f'<div style="display:flex;gap:14px;padding:0 40px 26px">'
            + "".join(f'<div style="flex:1;background:{c};color:{t};border-radius:14px;padding:18px;text-align:center;'
                      f'font-weight:700;font-size:28px">{lbl}</div>'
                      for lbl, c, t in [("Suivre", "#0095f6", "#fff"), ("Message", "#efefef", "#111"),
                                        ("Demander un diag", "#efefef", "#111")])
            + f'</div><div style="display:flex;gap:18px;padding:0 30px 30px">{hls}</div>'
            f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:4px">{cells}</div></div></body></html>')


# ------------------------------------------------------------------ RENDU
def render(pw_page, html, out, w, h):
    BUILD.mkdir(parents=True, exist_ok=True)
    f = BUILD / (out.stem + ".html")
    f.write_text(html, encoding="utf-8")
    pw_page.set_viewport_size({"width": w, "height": h})
    pw_page.goto(f.as_uri())
    pw_page.evaluate("document.fonts.ready")
    pw_page.wait_for_timeout(150)
    out.parent.mkdir(parents=True, exist_ok=True)
    pw_page.locator("#c").screenshot(path=str(out))
    print("✓", out.relative_to(ROOT))


def main():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROMIUM)
        pg = b.new_page()
        for k, html in {**POSTS, **CAROUSEL}.items():
            render(pg, html, OUT / folder(k) / f"{k}.png", W, H)
        for k, html in REEL_COVERS.items():
            render(pg, html, OUT / "reels" / f"{k}.png", RW, RH)
        themes = ["navy", "cream"]
        for i, (k, _) in enumerate(HL_LABELS):
            render(pg, highlight(k, themes[i % 2]), OUT / "a_la_une" / f"{k}.png", 1080, 1920)
        render(pg, profile_pic(), OUT / "profil" / "photo_profil.png", 1080, 1080)
        # La maquette pointe vers visuels/ depuis src/_build/ → chemins ../../visuels
        render(pg, mockup().replace("../../visuels", str(OUT.as_uri())), OUT / "maquette_profil.png", 1080, 2600)
        b.close()


if __name__ == "__main__":
    main()
