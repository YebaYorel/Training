---
name: remotion
description: Produire des vidéos motion design YEBA (intro de soirée, transitions de partie, compteurs animés) en React avec Remotion, rendues localement en MP4 pour PowerPoint ou Reveal.js.
---

# Remotion (vidéo en React, rendu local)

Projet : `soiree-lancement/remotion/` — compositions `Intro` (10 s) et `SectionTitle` (5 s, props
`numero`, `titre`, `accroche`). Charte dans `src/charte.tsx` (couleurs + chargement Montserrat local).

```bash
cd soiree-lancement/remotion
npm install                 # une fois
npm run studio              # éditeur visuel dans le navigateur
npm run render:all          # → ../dist/yeba-intro.mp4 et ../dist/yeba-transition-formations.mp4
# Autre partie : npx remotion render src/index.ts SectionTitle ../dist/partie05.mp4 \
#   --props='{"numero":"05","titre":"Applications & sites web","accroche":"Équiper, c est mieux."}'
```
Environnement cloud sans Chrome téléchargeable : ajouter
`--browser-executable=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`.

⚖️ Licence Remotion : gratuite pour les particuliers et les entreprises de 3 salariés maximum ;
au-delà, licence entreprise payante (vérifier sur remotion.pro avant usage commercial élargi).
Rendu 100 % local : aucune donnée transmise.
