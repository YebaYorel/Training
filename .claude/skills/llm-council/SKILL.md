---
name: llm-council
description: Soumet une question, une idée ou une décision à un conseil de 5 conseillers IA (contradicteur, premiers principes, expansionniste, regard extérieur, exécutant) qui se relisent anonymement puis rendent un verdict. Utiliser quand Aurélien dit « council this », « passe ça au conseil », « conseil LLM », ou veut challenger une décision importante (offre, prix, recrutement, investissement).
---

# LLM Council (lanceur)

Le skill d'origine (github.com/tenfoldmarc/llm-council-skill) **n'a pas de licence** :
il n'est donc pas recopié dans ce dépôt public. Ce lanceur le récupère, à une
version figée et relue, dans un cache local ignoré par Git, puis le suit.

## Étape 1 — Récupérer la version figée (une seule fois par machine/session)

```bash
CACHE="${CLAUDE_PROJECT_DIR:-.}/.claude/vendor-cache/llm-council-skill"
PIN=0dc03275b0ddf542545da3a9684510fff31df353
if [ ! -f "$CACHE/SKILL.md" ]; then
  git clone -q https://github.com/tenfoldmarc/llm-council-skill.git "$CACHE"
fi
git -C "$CACHE" fetch -q --depth 1 origin "$PIN" 2>/dev/null || true
git -C "$CACHE" -c advice.detachedHead=false checkout -q "$PIN"
git -C "$CACHE" rev-parse HEAD
```

Si le commit affiché n'est pas `0dc03275…`, **arrêter** et prévenir Aurélien
(le dépôt amont a pu être réécrit : ne pas exécuter une version non relue).

## Étape 2 — Suivre le skill

Lire `.claude/vendor-cache/llm-council-skill/SKILL.md` en entier et appliquer
sa méthode à la question posée.

## Adaptations obligatoires pour YEBA FORMATIONS

- Répondre **en français**.
- Les rapports `council-report-*.html` et `council-transcript-*.md` sont ignorés
  par Git (dépôt public) : ne jamais les forcer dans un commit.
- **RGPD** : ne pas mettre de données personnelles de clients/stagiaires dans la
  question soumise au conseil (minimisation, art. 5.1.c) — anonymiser d'abord.
- **IA Act** : le verdict est une aide à la décision, pas une décision
  automatisée ; si la question porte sur des personnes (recrutement,
  évaluation de stagiaires), le signaler : usage potentiellement « à haut
  risque » (annexe III, points 3 et 4) → décision humaine obligatoire.
