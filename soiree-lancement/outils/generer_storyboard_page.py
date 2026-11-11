"""Page web du storyboard (à partager avec l'équipe) : dist/storyboard/index.html + vignettes + générique 720p.

    python3 outils/generer_storyboard_page.py      (après build_all.sh : il lit dist/YEBA_Soiree_Lancement.pdf)

- Vignette de chaque slide projetée (rendu du PDF), texte projeté, visuel, animation, notes orateur, durée.
- Minimisation (la page est destinée à être hébergée en ligne) : aucun tarif, aucune politique de remise,
  aucune coordonnée — ces informations restent dans les notes du PowerPoint.
"""
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "pptx"))
sys.path.insert(0, str(RACINE / "outils"))
import build_pptx as P  # noqa: E402
from generer_supports import nb_mots, texte_visible  # noqa: E402

C = P.C
T = json.loads((RACINE / "remotion" / "src" / "timeline.json").read_text(encoding="utf-8"))
SORTIE = RACINE / "dist" / "storyboard"
PDF = RACINE / "dist" / "YEBA_Soiree_Lancement.pdf"
GENERIQUE = RACINE / "dist" / "videos" / "yeba-saison1-generique.mp4"

# Notes réécrites pour la version en ligne (tarifs et remises retirés : ils restent dans le PowerPoint)
NOTES_EN_LIGNE = {
    "S17": ("Effectifs : 6 minimum, 8 maximum, en inter comme en intra. Séminaire dirigeants IA (FOR-0014) : 6 à 8 dirigeants "
            "à huis clos, jamais deux concurrents directs sur la même session. Tarifs : jamais projetés (ni ici, ni à l'épisode 6) ; "
            "les repères de réponse orale sont dans les notes du PowerPoint."),
    "S36": "À CONSTRUIRE : épisode 7 — Mot de fin avec offre spéciale soirée (conditions à définir par Aurélien).",
}

SCENES = [
    ("coldOpen", "Ouverture", "Un point de lumière, des étoiles, « La Réunion · 974 »."),
    ("ici", "Ici", "« Ici, le savoir se partage. » Les pitons se relient en constellation."),
    ("yeba", "YEBA", "En lingala, un seul mot : YEBA, « savoir, connaître »."),
    ("baobab", "Le baobab", "Le Y devient arbre : « Sous le baobab, on transmet. »"),
    ("chemin", "Le chemin", "Odomètre 2021 → 2026 : création, vente, management, IA, RGPD, IA Act."),
    ("metiers", "3 métiers", "Former · Implémenter · Sécuriser — un seul interlocuteur."),
    ("formations", "11 formations", "Le montage des formations sur le tempo, puis « Bientôt : Assistant IA perso »."),
    ("confiance", "La confiance", "Qualiopi n° 25FOR02027.1 · NDA n° 04973676397 · 7 h par jour."),
    ("final", "Final", "Onde de choc, logo, « Sous le baobab de la connaissance, les graines du savoir. »"),
]

e = lambda t: html.escape(P.typo(t or ""), quote=False)  # noqa: E731


def tc(frame):
    s = frame / T["fps"]
    return f"{int(s // 60)}:{s % 60:04.1f}".replace(".", ",")


def vignettes():
    """Une vignette JPEG 960 px par page du PDF ; appariement page ↔ slide par la séquence du PowerPoint."""
    tmp = SORTIE / "_pages"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    subprocess.run(["pdftoppm", "-jpeg", "-jpegopt", "quality=80", "-scale-to-x", "960", "-scale-to-y", "-1", str(PDF), str(tmp / "p")],
                   check=True, stderr=subprocess.DEVNULL)  # avertissements de police sans conséquence
    pages = sorted(tmp.glob("p-*.jpg"), key=lambda f: int(re.findall(r"\d+", f.stem)[-1]))
    projetees = [(s, r) for s, r in P.sequence() if not s.get("cache")]
    if len(pages) != len(projetees):
        raise SystemExit(f"PDF ({len(pages)} pages) et séquence ({len(projetees)} slides) ne correspondent pas : relancer build_all.sh")
    (SORTIE / "img").mkdir(exist_ok=True)
    noms = {}
    for page, (s, retour) in zip(pages, projetees):
        if retour:
            continue
        nom = f"img/{s['id']}.jpg"
        shutil.move(str(page), SORTIE / nom)
        noms[s["id"]] = nom
    shutil.rmtree(tmp)
    for n in (5, 6, 7):  # épisodes masqués : l'affiche de leur carte-titre
        src = RACINE / "dist" / "videos" / f"yeba-episode-{n}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", "scale=960:-2", "-q:v", "4", str(SORTIE / f"img/E{n}.jpg")], check=True)
        noms[f"E{n}"] = f"img/E{n}.jpg"
    return noms


def video():
    (SORTIE / "video").mkdir(exist_ok=True)
    cible = SORTIE / "video" / "generique-720p.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(GENERIQUE), "-vf", "scale=1280:-2", "-c:v", "libx264", "-preset", "slow",
                    "-crf", "25", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "112k", "-movflags", "+faststart", str(cible)], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(RACINE / "dist" / "videos" / "yeba-saison1-generique.jpg"),
                    "-vf", "scale=1280:-2", "-q:v", "4", str(SORTIE / "video" / "generique.jpg")], check=True)
    taille = cible.stat().st_size / 1e6
    if taille > 14.5:
        raise SystemExit(f"Générique 720p trop lourd pour la page ({taille:.1f} Mo)")
    return taille


def bloc_slide(s, noms):
    titre = s.get("titre", "") + (" " + s["titre_or"] if s.get("titre_or") else "")
    notes = NOTES_EN_LIGNE.get(s["id"], s["notes"])
    projete = texte_visible(s)
    if s["layout"] == "video":
        v = C["videos"][s["video"]]
        nature = "Vidéo plein écran" + (" · avance seule" if s.get("avance") else "") + (" · en boucle" if v["boucle"] else "")
        projete_html = f'<p class="vide">{e(nature)} ({str(v["duree_s"]).replace(".", ",")} s)</p>'
    else:
        projete_html = f'<p class="projete">{e(projete)}</p><p class="compte">{nb_mots(projete)} mots projetés</p>'
    ia = ""
    if s["layout"] == "video" and s["video"].startswith("clip-"):
        ia = '<p class="alerte">Clip généré par IA (Grok) : le dire au public — IA Act, art. 50.</p>'
    fond = f'<span class="puce-fond">fond animé : {e(s["fond"])}</span>' if s.get("fond") else ""
    img = noms.get(s["id"])
    vignette = (f'<img src="{img}" alt="Slide {s["id"]} : {html.escape(titre)}" loading="lazy" width="960" height="540">'
                if img else '<div class="sans-image">masquée</div>')
    return f"""
      <article class="slide" id="{s['id']}">
        <figure class="vignette">{vignette}<figcaption><span class="code">{s['id']}</span><span class="duree">{s['duree_s']} s</span></figcaption></figure>
        <div class="fiche">
          <h3>{e(titre)}</h3>
          <dl>
            <div><dt>À l'écran</dt><dd>{projete_html}{ia}</dd></div>
            <div><dt>Visuel</dt><dd>{e(s['visuel'])} {fond}</dd></div>
            <div><dt>Animation</dt><dd>{e(s['animation'])}</dd></div>
            <div class="dire"><dt>À dire</dt><dd>{e(notes)}</dd></div>
          </dl>
        </div>
      </article>"""


def page(noms, taille_video):
    visibles = [s for s in C["slides"] if not s.get("cache")]
    total = sum(s["duree_s"] for s in visibles)
    eps = {0: ("Ouverture", "Accueil, générique, couverture")}
    eps.update({ep["numero"]: (ep["titre"], ep["sujet"]) for ep in C["episodes"]})
    nav = "".join(f'<a href="#ep-{n}">{"Ouverture" if n == 0 else f"Ép. {n}"}</a>' for n in sorted(eps))
    scenes = "".join(
        f'<li><span class="tc">{tc(T["scenes"][cle][0])}</span><strong>{e(nom)}</strong><span>{e(txt)}</span></li>'
        for cle, nom, txt in SCENES
    )
    sections = []
    for n in sorted(eps):
        titre_ep, sujet = eps[n]
        du_ep = [s for s in C["slides"] if s.get("episode", 0) == n]
        vis = [s for s in du_ep if not s.get("cache")]
        if not vis:  # épisodes 5 à 7 : à construire (note de la slide d'agenda masquée)
            agenda = next(s for s in du_ep if s["layout"] != "video")
            note = NOTES_EN_LIGNE.get(agenda["id"], agenda["notes"])
            sections.append(f"""
    <section class="episode a-construire" id="ep-{n}">
      <header><p class="sur">Épisode {n}</p><h2>{e(titre_ep)}</h2><p class="sujet">{e(sujet)} · à construire</p></header>
      <div class="carte-ep"><img src="{noms[f'E{n}']}" alt="Carte-titre de l'épisode {n}" loading="lazy" width="960" height="540">
        <p>{e(note)}</p></div>
    </section>""")
            continue
        minutes = round(sum(s["duree_s"] for s in vis) / 60)
        slides = "".join(bloc_slide(s, noms) for s in vis)
        entete = "Ouverture" if n == 0 else f"Épisode {n}"
        sections.append(f"""
    <section class="episode" id="ep-{n}">
      <header><p class="sur">{entete}</p><h2>{e(titre_ep)}</h2>
        <p class="sujet">{e(sujet)} · ≈ {minutes} min · {len(vis)} slides · <span class="qui">intervenant : à répartir</span></p></header>
      {slides}
    </section>""")
    return f"""<title>Storyboard YEBA Saison 1</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700;800;900&display=swap">
<style>
/* Mise en page : guide d'épisodes de série — vignette 16:9 à gauche, fiche à droite ; charte YEBA (noir, or, bleu nuit). */
:root {{
  --bg: #121212; --surface: #1A1A1E; --surface-2: #202026; --line: #2E2D33;
  --fg: #FFFFFF; --muted: #B8BCC6; --gold: #C9AB4C; --gold-ink: #C9AB4C; --blue: #1B3A6B; --alert: #E8A33D;
  --display: "Montserrat", "Segoe UI", system-ui, sans-serif; --body: "Montserrat", "Segoe UI", system-ui, sans-serif;
  color-scheme: dark;
}}
@media (prefers-color-scheme: light) {{ :root:not([data-theme="dark"]) {{
  --bg: #F4F5F7; --surface: #FFFFFF; --surface-2: #ECEEF2; --line: #D7DAE0;
  --fg: #121212; --muted: #4A4F5A; --gold: #C9AB4C; --gold-ink: #7A5E16; --blue: #1B3A6B; --alert: #8A4B00; color-scheme: light; }} }}
:root[data-theme="light"] {{
  --bg: #F4F5F7; --surface: #FFFFFF; --surface-2: #ECEEF2; --line: #D7DAE0;
  --fg: #121212; --muted: #4A4F5A; --gold: #C9AB4C; --gold-ink: #7A5E16; --blue: #1B3A6B; --alert: #8A4B00; color-scheme: light; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--fg); font-family: var(--body); font-size: 17px; line-height: 1.55; }}
.page {{ max-width: 1180px; margin: 0 auto; padding-block: 40px 64px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }}
h1, h2, h3 {{ font-family: var(--display); text-wrap: balance; margin: 0; }}
.sur {{ margin: 0; text-transform: uppercase; letter-spacing: .22em; font-weight: 800; font-size: 13px; color: var(--gold-ink); }}
.entete {{ display: grid; gap: 14px; padding-bottom: 28px; border-bottom: 1px solid var(--line); }}
.entete h1 {{ font-size: clamp(36px, 6vw, 64px); font-weight: 900; letter-spacing: -.02em; line-height: 1.05; }}
.entete h1 span {{ color: var(--gold-ink); }}
.chapo {{ max-width: 62ch; margin: 0; color: var(--muted); font-size: 18px; }}
.meta {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 4px 0 0; padding: 0; list-style: none; }}
.meta li {{ border: 1px solid var(--line); border-radius: 999px; padding: 4px 12px; font-size: 14px; font-weight: 600; }}
nav.episodes {{ position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: var(--bg); display: flex; gap: 6px; flex-wrap: wrap;
  padding-block: 12px; border-bottom: 1px solid var(--line); }}
body::before {{ content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: var(--bg); }}
nav.episodes a {{ color: var(--fg); text-decoration: none; font-weight: 700; font-size: 14px; padding: 6px 12px; border-radius: 8px; background: var(--surface-2); }}
nav.episodes a:hover, nav.episodes a:focus-visible {{ outline: 2px solid var(--gold); outline-offset: 1px; }}
.lecture {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 12px; margin: 28px 0 8px; }}
.lecture div {{ background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 12px 14px; font-size: 15px; color: var(--muted); }}
.lecture b {{ display: block; color: var(--fg); font-size: 14px; letter-spacing: .08em; text-transform: uppercase; }}
.generique {{ display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); gap: 28px; margin-top: 40px; align-items: start; }}
.generique video {{ width: 100%; max-width: 100%; aspect-ratio: 16 / 9; border-radius: 10px; background: #000; display: block; }}
.generique h2 {{ font-size: 30px; font-weight: 800; margin: 6px 0 10px; }}
.generique ol {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 8px; }}
.generique li {{ display: grid; grid-template-columns: 64px minmax(0, 1fr); column-gap: 10px; font-size: 15px; }}
.generique li span:last-child {{ grid-column: 2; color: var(--muted); }}
.tc {{ grid-row: span 2; font-variant-numeric: tabular-nums; font-weight: 800; color: var(--gold-ink); }}
.consigne {{ margin: 14px 0 0; padding: 10px 14px; border-left: 4px solid var(--gold); background: var(--surface); font-weight: 600; }}
.episode {{ margin-top: 56px; display: grid; gap: 18px; scroll-margin-top: 70px; }}
.episode > header {{ display: grid; gap: 4px; padding-bottom: 10px; border-bottom: 2px solid var(--gold); }}
.episode h2 {{ font-size: clamp(28px, 4vw, 40px); font-weight: 900; }}
.sujet {{ margin: 0; color: var(--muted); font-weight: 600; }}
.qui {{ color: var(--alert); }}
.slide {{ display: grid; grid-template-columns: minmax(0, 420px) minmax(0, 1fr); gap: 22px; padding: 18px; background: var(--surface);
  border: 1px solid var(--line); border-radius: 12px; scroll-margin-top: 70px; }}
.vignette {{ margin: 0; display: grid; gap: 8px; align-content: start; }}
.vignette img {{ width: 100%; height: auto; border-radius: 6px; display: block; background: #000; }}
.sans-image {{ aspect-ratio: 16 / 9; display: grid; place-items: center; background: var(--surface-2); border-radius: 6px; color: var(--muted); }}
figcaption {{ display: flex; justify-content: space-between; font-size: 14px; font-weight: 700; color: var(--muted); font-variant-numeric: tabular-nums; }}
.code {{ color: var(--gold-ink); letter-spacing: .06em; }}
.fiche {{ min-width: 0; display: grid; gap: 10px; }}
.fiche h3 {{ font-size: 22px; font-weight: 800; line-height: 1.25; }}
dl {{ margin: 0; display: grid; gap: 10px; }}
dl div {{ display: grid; grid-template-columns: 112px minmax(0, 1fr); gap: 12px; }}
dt {{ font-size: 13px; font-weight: 800; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); padding-top: 3px; }}
dd {{ margin: 0; min-width: 0; overflow-wrap: anywhere; }}
.dire dd {{ font-size: 16px; }}
.projete {{ margin: 0; font-weight: 700; }}
.compte, .vide {{ margin: 2px 0 0; font-size: 14px; color: var(--muted); }}
.alerte {{ margin: 6px 0 0; font-size: 14px; font-weight: 700; color: var(--alert); }}
.puce-fond {{ display: inline-block; margin-left: 4px; font-size: 13px; font-weight: 700; color: var(--gold-ink); }}
.a-construire .carte-ep {{ display: grid; grid-template-columns: minmax(0, 420px) minmax(0, 1fr); gap: 22px; align-items: center; }}
.a-construire img {{ width: 100%; height: auto; border-radius: 6px; display: block; }}
.preparer {{ margin-top: 64px; display: grid; gap: 16px; scroll-margin-top: 70px; }}
.preparer h2 {{ font-size: clamp(28px, 4vw, 40px); font-weight: 900; }}
.colonnes {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 14px; }}
.colonnes section {{ background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 16px 18px; }}
.colonnes h3 {{ font-size: 16px; letter-spacing: .1em; text-transform: uppercase; color: var(--gold-ink); margin-bottom: 8px; }}
.colonnes ul {{ margin: 0; padding-left: 18px; display: grid; gap: 6px; }}
footer {{ margin-top: 56px; padding-top: 18px; border-top: 1px solid var(--line); color: var(--muted); font-size: 14px; display: grid; gap: 6px; }}
footer p {{ margin: 0; max-width: 90ch; }}
@media (max-width: 760px) {{
  .generique, .slide, .a-construire .carte-ep {{ grid-template-columns: minmax(0, 1fr); }}
  dl div {{ grid-template-columns: minmax(0, 1fr); gap: 2px; }}
  body {{ font-size: 16px; }}
}}
@media (prefers-reduced-motion: reduce) {{ * {{ scroll-behavior: auto !important; }} }}
</style>
<div class="page">
  <header class="entete">
    <p class="sur">YEBA FORMATIONS · document interne de l'équipe</p>
    <h1>Storyboard <span>Saison 1</span></h1>
    <p class="chapo">La soirée de lancement se regarde comme une série : un générique, puis des épisodes. Pour chaque slide :
      ce qui est à l'écran, ce qui bouge et ce qu'on dit.</p>
    <ul class="meta">
      <li>Épisodes 1 à 4 construits · ≈ {round(total / 60)} min</li>
      <li>{len(noms) - 3} slides projetées</li>
      <li>Date et lieu : à préciser</li>
      <li>Version du {C['meta']['sources_verifiees_le']}</li>
    </ul>
  </header>
  <nav class="episodes" aria-label="Épisodes">{nav}<a href="#preparer">À préparer</a></nav>

  <div class="lecture" aria-label="Comment lire une fiche">
    <div><b>À l'écran</b>Le texte projeté, mot pour mot (20 mots au plus).</div>
    <div><b>Visuel · Animation</b>Ce que le public voit et ce qui bouge, déjà réglé dans le PowerPoint.</div>
    <div><b>À dire</b>Les notes orateur : messages clés, sources, vigilances RGPD / IA Act.</div>
    <div><b>Durée</b>Temps de parole visé, en secondes, sous la vignette.</div>
  </div>

  <section class="generique" id="generique" aria-labelledby="titre-generique">
    <video controls preload="none" poster="video/generique.jpg" playsinline>
      <source src="video/generique-720p.mp4" type="video/mp4">
    </video>
    <div>
      <p class="sur">Générique d'ouverture · 1 min 20</p>
      <h2 id="titre-generique">Le générique, scène par scène</h2>
      <ol>{scenes}</ol>
      <p class="consigne">Lumière baissée, personne ne parle pendant le générique : il enchaîne seul sur la couverture.</p>
    </div>
  </section>
{''.join(sections)}

  <section class="preparer" id="preparer">
    <p class="sur">Avant le jour J</p>
    <h2>À préparer</h2>
    <div class="colonnes">
      <section><h3>Contenu</h3><ul>
        <li>Date et lieu de la soirée (couverture)</li>
        <li>Rôle de Stan et d'Antho, et qui présente chaque épisode</li>
        <li>Épisodes 5, 6, 7 : sites et applications, audit et devis (sans tarif projeté), mot de fin et offre de la soirée</li>
        <li>Démo live : scénario écrit, entreprise fictive, vidéo de secours enregistrée</li>
      </ul></section>
      <section><h3>Salle et technique</h3><ul>
        <li>Répétition complète sur le PC de la salle : son du générique, fluidité des fonds animés (sinon version sobre)</li>
        <li>Télécommande de présentation, câble HDMI, micros, clé USB avec le PDF de secours</li>
        <li>Lumière réglable pour le générique</li>
      </ul></section>
      <section><h3>Juridique</h3><ul>
        <li>Accord écrit des intervenants pour leurs photos (droit à l'image, RGPD)</li>
        <li>Clips Grok : annoncer à l'oral qu'ils sont générés par IA (IA Act, art. 50)</li>
        <li>Invitations et liste des invités : mention d'information RGPD, durée de conservation</li>
        <li>Musique d'ambiance pendant l'accueil : déclaration SACEM à vérifier avec le lieu (le générique, lui, est une musique originale)</li>
      </ul></section>
    </div>
  </section>

  <footer>
    <p>Document interne YEBA FORMATIONS, généré depuis la source du PowerPoint. Les tarifs n'y figurent pas : ils restent dans les notes du PowerPoint.</p>
    <p>Sources : base Airtable YEBA FORMATIONS (catalogue, CONFIG SYSTÈME, notice YEBA-DOC-13), document de marque YEBA FORMATIONS. Générique fabriqué par programme (Remotion), musique originale synthétisée.</p>
  </footer>
</div>
"""


if __name__ == "__main__":
    SORTIE.mkdir(parents=True, exist_ok=True)
    noms = vignettes()
    taille = video()
    (SORTIE / "index.html").write_text(page(noms, taille), encoding="utf-8")
    poids = sum(f.stat().st_size for f in SORTIE.rglob("*") if f.is_file()) / 1e6
    print(f"OK : {SORTIE / 'index.html'} ({len(noms)} vignettes, générique 720p {taille:.1f} Mo, total {poids:.1f} Mo)")
