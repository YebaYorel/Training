"""Génère les supports texte depuis ../contenu/slides.json :
  - storyboard.md                 : le storyboard slide par slide (titre, texte, visuel, animation, notes)
  - felo/prompt_felo_slides.md    : prompt prêt à coller dans Felo Slides (sans aucune donnée personnelle)
  - slides-com/plan_slides_com.md : plan de montage pour Slides.com
"""
import json
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
C = json.loads((RACINE / "contenu" / "slides.json").read_text(encoding="utf-8"))


def texte_visible(s):
    """Texte réellement projeté (pour le décompte de mots)."""
    morceaux = [s.get("kicker", ""), s.get("titre", ""), s.get("titre_or", ""), s.get("texte", ""), s.get("texte_or", "")]
    for cle in ("items", "puces", "chips", "branches"):
        for x in s.get(cle, []):
            morceaux.append(x if isinstance(x, str) else " ".join(str(v) for v in x.values() if isinstance(v, str)))
    for c in s.get("cartes", []):
        morceaux += [c["nom"], c["role"]]
    for e in s.get("etapes", []):
        morceaux += [e["date"], e["texte"]]
    for cote in ("gauche", "droite"):
        if cote in s:
            morceaux += [s[cote]["label"]] + s[cote]["mots"]
    if s["layout"] == "agenda":
        morceaux = [s["titre"]] + C["agenda"]
    if s["layout"] == "garage":
        morceaux = [s["titre"]] + [i["code"] for i in s["items"]]
    return " ".join(m for m in morceaux if m)


def nb_mots(t):
    return len([m for m in t.replace("·", " ").replace("—", " ").split() if any(ch.isalnum() for ch in m)])


def storyboard():
    total = sum(s["duree_s"] for s in C["slides"] if not s.get("cache"))
    L = [
        "# Storyboard — Soirée de lancement YEBA FORMATIONS",
        "",
        f"> Public : {C['meta']['public']}.  ",
        f"> Durée totale de la soirée : ≈ {C['meta']['duree_totale_min']} min — parties traitées ici "
        f"(Présentation → Formations) : ≈ {round(total / 60)} min.  ",
        "> Fichier généré automatiquement depuis `contenu/slides.json` — ne pas modifier à la main.",
        "",
        "## Règles de design appliquées",
        "",
        *[f"- {r}" for r in C["meta"]["regles_design"]],
        "",
        "## Déroulé",
        "",
        "| # | Partie | Slide | Mots projetés | Durée |",
        "|---|---|---|---|---|",
    ]
    for s in C["slides"]:
        etat = " *(masquée — à construire)*" if s.get("cache") else ""
        L.append(f"| {s['id']} | {s['partie']} | {s.get('titre', '')}{etat} | {nb_mots(texte_visible(s))} | {s['duree_s']} s |")
    L.append("")
    for s in C["slides"]:
        if s.get("cache"):
            continue
        L += [
            f"## {s['id']} — {s['partie']} · gabarit `{s['layout']}`",
            "",
            "**1. Titre & texte ultra-court**",
            "",
            f"> {texte_visible(s)}",
            "",
            f"*({nb_mots(texte_visible(s))} mots projetés)*",
            "",
            f"**2. Idée visuelle / mise en page** — {s['visuel']}",
            "",
            f"**3. Animation / transition** — {s['animation']}",
            "",
            f"**Notes orateur ({s['duree_s']} s)** — {s['notes']}",
            "",
        ]
    (RACINE / "storyboard.md").write_text("\n".join(L), encoding="utf-8")


def felo():
    L = [
        "# Prompt Felo Slides — Soirée de lancement YEBA FORMATIONS",
        "",
        "> ⚠️ Souveraineté des données : Felo est un service d'IA en ligne dont l'éditeur est établi hors de l'Union",
        "> européenne (à vérifier dans ses conditions d'utilisation avant usage). Ce prompt ne contient **aucune donnée",
        "> personnelle** (ni nom de client, ni coordonnées, ni prix) : ne pas en ajouter. Le PowerPoint de référence reste",
        "> `dist/YEBA_Soiree_Lancement.pptx` ; Felo sert à explorer des variantes visuelles.",
        "",
        "## À coller dans Felo Slides",
        "",
        "```text",
        "Agis comme un expert en présentation PowerPoint et en motion design (style Mesaure / Slidor).",
        "Crée une présentation de lancement pour un organisme de formation réunionnais, destinée à des dirigeants",
        "de TPE-PME triés sur le volet. Langue : français.",
        "",
        "Règles de design impératives :",
        "- 15 à 20 mots maximum par slide, des mots-clés, jamais de phrases longues.",
        "- Fond très sombre #121212 ou bleu #1B3A6B, texte blanc, accent or #C9A84C. Jamais d'or sur fond blanc.",
        "- Police Montserrat, très grande (titres 54 pt et plus, texte 28 pt minimum) : public pouvant être malvoyant.",
        "- Grilles asymétriques, grands chiffres d'impact, chronologies épurées. Aucune ligne ne traverse un mot.",
        "- Transitions Morphose entre slides consécutives.",
        "",
        "Contenu, slide par slide :",
    ]
    for s in C["slides"]:
        if s.get("cache"):
            continue
        L.append(f"{s['id']}. [{s['partie']}] {texte_visible(s)}  → visuel : {s['visuel']}")
    L += ["```", ""]
    (RACINE / "felo" / "prompt_felo_slides.md").write_text("\n".join(L), encoding="utf-8")


def slides_com():
    L = [
        "# Plan de montage Slides.com",
        "",
        "Slides.com est l'éditeur en ligne bâti sur Reveal.js (même moteur que `revealjs/index.html`).",
        "Deux voies, de la plus fidèle à la plus souple :",
        "",
        "1. **Importer** `dist/YEBA_Soiree_Lancement.pdf` ou le `.pptx` via le menu d'import de Slides.com",
        "   (disponibilité selon votre offre : à vérifier dans votre compte).",
        "2. **Reconstruire** chaque slide avec le plan ci-dessous, puis activer *Auto-Animate* entre slides",
        "   consécutives et donner le même *Animation ID* aux éléments qui doivent glisser (équivalent Morphose).",
        "",
        "Réglages d'identité (Theme → Custom CSS) : fond `#121212`, texte `#FFFFFF`, accent `#C9A84C`,",
        "police Montserrat. Copier le bloc CSS de `revealjs/build_reveal.py` (variable `CSS`) pour un rendu identique.",
        "",
        "> ⚖️ RGPD : Slides.com héberge vos présentations en ligne. Vérifier la localisation des serveurs et le",
        "> contrat de sous-traitance (art. 28 RGPD) avant d'y déposer autre chose que ce contenu public.",
        "> Garder la présentation **privée** tant que les champs [DATE], [LIEU] et les rôles ne sont pas validés.",
        "",
        "| Slide | Texte projeté | Animation à régler |",
        "|---|---|---|",
    ]
    for s in C["slides"]:
        if s.get("cache"):
            continue
        L.append(f"| {s['id']} | {texte_visible(s)} | {s['animation']} |")
    (RACINE / "slides-com" / "plan_slides_com.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def controle_mots():
    alertes = []
    for s in C["slides"]:
        n = nb_mots(texte_visible(s))
        if n > 20 and s["layout"] not in ("agenda", "garage"):
            alertes.append(f"{s['id']} : {n} mots (> 20)")
    return alertes


if __name__ == "__main__":
    storyboard()
    felo()
    slides_com()
    for a in controle_mots():
        print("⚠️ ", a)
    print("OK : storyboard.md, felo/prompt_felo_slides.md, slides-com/plan_slides_com.md")
