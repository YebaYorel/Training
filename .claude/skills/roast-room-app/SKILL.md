---
name: roast-room-app
description: Lanceur de la salle visuelle du Roast Room (nateherkai/roast-room, MIT) — la table animée où les conseillers (Hormozi, Paul Graham de Y Combinator, Gary Vaynerchuk, Bezos, Buffett…) débattent en direct sur http://localhost:4730, avec le verdict téléchargeable en PDF. Utiliser quand Aurélien demande d'ouvrir, lancer ou montrer la salle du Roast Room. Pour faire débattre une décision, utiliser la compétence roast-room (la salle est facultative).
---

# Roast Room : la salle visuelle (lanceur)

L'application compte 70 fichiers pour Node 20, dont des caricatures de personnes réelles. Elle n'est pas recopiée
dans ce dépôt public : le lanceur la récupère à la demande, à la version relue, dans un cache que Git ignore. Le
conseil lui-même (compétence `roast-room` et conseillers `.claude/agents/council-*.md`) est installé à demeure.

## 1. Récupérer la version figée (depuis la racine du dépôt)

```bash
python scripts/lanceur_depot.py nateherkai/roast-room e40f40652d5690c4d9f928c4794c673a99f2cd0e roast-room-app
```

Si le script affiche « ARRÊT », s'arrêter et prévenir Aurélien.

## 2. Préparer le cache (sans risque à relancer)

```bash
C=.claude/vendor-cache/roast-room-app
mkdir -p sessions
# 1) la salle lit les séances de CE dépôt (sessions/, ignoré par Git) ; on y copie une fois les 3 exemples
if [ ! -L "$C/sessions" ]; then cp -rn "$C/sessions/." sessions/; rm -rf "$C/sessions"; ln -s "$PWD/sessions" "$C/sessions"; fi
# 2) même composition du conseil que la compétence installée
ln -sf "$PWD/.claude/skills/roast-room/roster.json" "$C/.claude/skills/roast-room/roster.json"
# 3) RGPD : pas de Google Fonts (polices locales ; Montserrat installée sur le PC)
sed -i.bak '/fonts\.googleapis\.com\|fonts\.gstatic\.com/d' "$C/app/public/index.html"
```

## 3. Démarrer, en arrière-plan

```bash
cd .claude/vendor-cache/roast-room-app && COUNCIL_RUNNER=viewer node app/server.mjs
```

- **Lecture seule imposée** (`COUNCIL_RUNNER=viewer`) : la salle se contente de lire les fichiers de séance que la
  compétence `roast-room` écrit.
  - Ne jamais passer en mode `api` : il appellerait l'API Anthropic avec une clé, facturée à part.
  - Ne jamais créer de `.env` dans le cache.
- **Session cloud** : signaler le port 4730 avec l'outil `report_preview_port`.
- **Ordinateur** : ouvrir http://localhost:4730. Le serveur n'écoute qu'en local (127.0.0.1).

Relu le 13/11/2026 : serveur Node sans dépendance. En mode lecture seule, aucun appel réseau. La page chargeait
Google Fonts ; l'étape 2 retire ce chargement.

## Points d'attention

- **Caricatures** de personnes réelles, fournies par l'auteur : usage local uniquement. Ne jamais les reprendre dans un
  support YEBA (droit à l'image).
- **Simulations** : la salle met en scène des sièges simulés, pas les vraies personnes (voir
  `roast-room/PROVENANCE.md`).
- **Licence MIT** : © 2026 AI Automation Society.
