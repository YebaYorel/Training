"""Génère les supports texte depuis ../contenu/slides.json (v2 « YEBA — Saison 1 ») :
  - storyboard.md                 : storyboard épisode par épisode, slide par slide
                                    (1. titre & texte ultra-court, 2. visuel / mise en page, 3. animation / transition)
  - felo/prompt_felo_slides.md    : prompt prêt à coller dans Felo Slides (sans aucune donnée personnelle)
  - slides-com/plan_slides_com.md : plan de montage pour Slides.com
Contrôle aussi la règle Mesaure/Slidor : 15 à 20 mots projetés au maximum par slide.
"""
import json
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
C = json.loads((RACINE / "contenu" / "slides.json").read_text(encoding="utf-8"))
EXCEPTIONS_MOTS = {
    "agenda": "sommaire de la série",
    "atelier": "carte du catalogue",
    "confiance": "mention légale obligatoire (art. L.6352-12 du Code du travail)",
    "journee": "horaires",
    "cover": "couverture : signature de marque + date et lieu",
}


def _textes(x):
    if isinstance(x, str):
        return [x]
    return [" — ".join(x[k] for k in ("titre", "nom", "texte", "label") if isinstance(x.get(k), str))]


def texte_visible(s):
    """Texte réellement projeté (pour le décompte de mots)."""
    L = s["layout"]
    if L == "video":
        return ""
    if L == "agenda":
        return " · ".join([s["titre"]] + [f"{e['titre']} — {e['sujet']}" for e in C["episodes"]])
    m = [s.get(k, "") for k in ("kicker", "titre", "titre_or", "texte", "mention", "nom")]
    for cle in ("items", "puces", "chips", "branches", "cartes", "segments"):
        for x in s.get(cle, []):
            m += _textes(x) if not isinstance(x, dict) or cle != "cartes" else [x["nom"], x["role"]]
    for e in s.get("etapes", []):
        m += [e["date"], e["texte"]]
    for cote in ("gauche", "droite"):
        if cote in s:
            m += [s[cote]["label"]] + s[cote]["mots"]
    for bloc in ("qualiopi", "nda"):
        if bloc in s:
            m += [s[bloc][k] for k in ("titre", "ligne1", "ligne2")]
    if L == "journee":
        h = C["meta"]["horaires"]
        m += [h["debut"], h["pause_debut"], h["pause_fin"], h["fin"]]
    if L == "cover":
        m = [s["kicker"], s["titre"], s["titre_or"], f"{C['meta']['date']} · {C['meta']['lieu']} · La Réunion"]
    return " · ".join(t for t in m if t)


def nb_mots(t):
    return len([w for w in t.replace("·", " ").replace("—", " ").replace("→", " ").split() if any(ch.isalnum() for ch in w)])


def storyboard():
    visibles = [s for s in C["slides"] if not s.get("cache")]
    total = sum(s["duree_s"] for s in visibles)
    L = [
        "# Storyboard — « YEBA — Saison 1 » · soirée de lancement YEBA FORMATIONS",
        "",
        f"> Public : {C['meta']['public']}.  ",
        f"> Durée totale de la soirée : ≈ {C['meta']['duree_totale_min']} min — épisodes 1 à 4 construits ici : ≈ {round(total / 60)} min "
        "(épisodes 5 à 7 : slides masquées, à construire).  ",
        "> Fichier généré automatiquement depuis `contenu/slides.json` — ne pas modifier à la main.",
        "",
        "## Le concept : une série",
        "",
        "La soirée se regarde comme une saison de série : pré-générique en boucle pendant l'accueil, **générique d'ouverture "
        "de 80 s** (motion design Remotion, bande-son originale synchronisée), puis 7 épisodes. Chaque épisode s'ouvre sur "
        "sa carte-titre animée (4,5 s, avance automatique) ; la slide « Saison 1 · 7 épisodes » revient entre deux épisodes "
        "comme un GPS (la Morphose fait glisser le repère). L'épisode 4 se termine sur un « À suivre… ».",
        "",
        "## Règles de design appliquées",
        "",
        *[f"- {r}" for r in C["meta"]["regles_design"]],
        "",
        "## Déroulé",
        "",
        "| # | Épisode | Slide | Mots projetés | Fond animé | Durée |",
        "|---|---|---|---|---|---|",
    ]
    for s in C["slides"]:
        etat = " *(masquée — à construire)*" if s.get("cache") else ""
        titre = s.get("titre", "") + (" " + s["titre_or"] if s.get("titre_or") else "")
        L.append(f"| {s['id']} | {s.get('episode', 0)} · {s['partie']} | {titre}{etat} | {nb_mots(texte_visible(s))} | "
                 f"{s.get('fond', '—') if s['layout'] != 'video' else 'vidéo plein écran'} | {s['duree_s']} s |")
    L.append("")
    episode = None
    for s in visibles:
        if s.get("episode", 0) != episode:
            episode = s.get("episode", 0)
            ep = next((e for e in C["episodes"] if e["numero"] == episode), None)
            entete = "Ouverture" if ep is None else f"Épisode {episode} — {ep['titre']} ({ep['sujet']})"
            L += [f"# {entete}", ""]
        texte = texte_visible(s) or "(vidéo plein écran — aucun texte projeté)"
        fond = f" Fond vivant : `{s['fond']}` (Remotion, boucle muette ; image fixe en version sobre)." if s.get("fond") else ""
        L += [
            f"## {s['id']} — {s['partie']} · gabarit `{s['layout']}`",
            "",
            "**1. Titre & texte ultra-court**",
            "",
            f"> {texte}",
            "",
            f"*({nb_mots(texte_visible(s))} mots projetés)*",
            "",
            f"**2. Idée visuelle / mise en page** — {s['visuel']}{fond}",
            "",
            f"**3. Animation / transition** — {s['animation']}",
            "",
            f"**Notes orateur ({s['duree_s']} s)** — {s['notes']}",
            "",
        ]
    (RACINE / "storyboard.md").write_text("\n".join(L), encoding="utf-8")


def felo():
    L = [
        "# Prompt Felo Slides — « YEBA — Saison 1 »",
        "",
        "> ⚠️ Souveraineté des données : Felo est un service d'IA en ligne dont l'éditeur est établi hors de l'Union",
        "> européenne (à vérifier dans ses conditions d'utilisation avant usage). Ce prompt ne contient **aucune donnée",
        "> personnelle** (ni nom de client, ni coordonnées, ni prix) : ne pas en ajouter. Le PowerPoint de référence reste",
        "> `dist/YEBA_Soiree_Lancement.pptx` ; Felo sert uniquement à explorer des variantes visuelles.",
        "",
        "## À coller dans Felo Slides",
        "",
        "```text",
        "Agis comme un expert en présentation PowerPoint et en motion design (style Mesaure / Slidor).",
        "Crée la présentation d'une soirée de lancement pour un organisme de formation réunionnais, pensée comme",
        "une SÉRIE : « Saison 1 », 7 épisodes, une carte-titre par épisode, un sommaire qui revient comme un GPS.",
        "Public : dirigeants de TPE-PME triés sur le volet. Langue : français.",
        "",
        "Règles de design impératives :",
        "- 15 à 20 mots maximum par slide, des mots-clés, jamais de phrases longues.",
        "- Fond très sombre #121212, bleu #1B3A6B ou terre #1A120C, texte blanc, accent or #C9A84C. Jamais d'or sur blanc.",
        "- Police Montserrat, très grande (titres 54 pt et plus, texte 28 pt minimum) : public pouvant être malvoyant.",
        "- Grilles asymétriques, grands chiffres d'impact, chronologies épurées. Aucune ligne ne traverse un mot.",
        "- Transitions Morphose entre slides consécutives ; halo de lumière et champ d'étoiles en parallaxe lente.",
        "",
        "Contenu, slide par slide :",
    ]
    for s in C["slides"]:
        if s.get("cache") or s["layout"] == "video":
            continue
        L.append(f"{s['id']}. [Épisode {s.get('episode', 0)} · {s['partie']}] {texte_visible(s)}  → visuel : {s['visuel']}")
    L += ["```", ""]
    (RACINE / "felo" / "prompt_felo_slides.md").write_text("\n".join(L), encoding="utf-8")


def slides_com():
    L = [
        "# Plan de montage Slides.com — « YEBA — Saison 1 »",
        "",
        "Slides.com est l'éditeur en ligne bâti sur Reveal.js (même moteur que `revealjs/index.html`).",
        "Deux voies, de la plus fidèle à la plus souple :",
        "",
        "1. **Importer** `dist/YEBA_Soiree_Lancement.pdf` (images figées) ou le `.pptx` via le menu d'import de Slides.com",
        "   (disponibilité selon votre offre : à vérifier dans votre compte). Les vidéos (générique, épisodes, fonds) ne",
        "   sont pas reprises par l'import PDF : les ajouter comme *background video* depuis `dist/videos/`.",
        "2. **Reconstruire** chaque slide avec le plan ci-dessous, puis activer *Auto-Animate* entre slides",
        "   consécutives et donner le même *Animation ID* aux éléments qui doivent glisser (équivalent Morphose).",
        "",
        "Réglages d'identité (Theme → Custom CSS) : fond `#121212`, texte `#FFFFFF`, accent `#C9A84C`,",
        "police Montserrat. Copier le bloc CSS de `revealjs/build_reveal.py` (variable `CSS`) pour un rendu identique.",
        "",
        "> ⚖️ RGPD : Slides.com héberge vos présentations en ligne. Vérifier la localisation des serveurs et le",
        "> contrat de sous-traitance (art. 28 RGPD) avant d'y déposer autre chose que ce contenu public.",
        "> Garder la présentation **privée** tant que la date, le lieu et les rôles ne sont pas validés.",
        "> ⚖️ IA Act (art. 50) : les 4 clips générés par IA (Grok) doivent rester signalés comme contenus générés par IA.",
        "",
        "| Slide | Texte projeté | Fond / vidéo | Animation à régler |",
        "|---|---|---|---|",
    ]
    for s in C["slides"]:
        if s.get("cache"):
            continue
        if s["layout"] == "video":
            v = C["videos"][s["video"]]
            L.append(f"| {s['id']} | *(vidéo plein écran)* | `{v['fichier']}` | {s['animation']} |")
        else:
            fond = f"`{C['fonds'][s['fond']]['fichier']}`" if s.get("fond") else "—"
            L.append(f"| {s['id']} | {texte_visible(s)} | {fond} | {s['animation']} |")
    (RACINE / "slides-com" / "plan_slides_com.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def controle_mots():
    alertes = []
    for s in C["slides"]:
        n = nb_mots(texte_visible(s))
        if n > 20 and s["layout"] not in EXCEPTIONS_MOTS:
            alertes.append(f"{s['id']} : {n} mots (> 20)")
    return alertes


if __name__ == "__main__":
    storyboard()
    felo()
    slides_com()
    for a in controle_mots():
        print("⚠️ ", a)
    print("OK : storyboard.md, felo/prompt_felo_slides.md, slides-com/plan_slides_com.md")
