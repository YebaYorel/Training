---
name: remotion
description: Produire des vidéos motion design YEBA (générique de série, cartes d'épisode, fonds vivants en boucle, bande-son synchronisée) en React avec Remotion, rendues localement en MP4 pour PowerPoint ou Reveal.js.
---

# Remotion (vidéo en React, rendu 100 % local)

Projet : `soiree-lancement/remotion/` — « YEBA — Saison 1 ».

| Composition | Rôle | Sortie (`dist/videos/`) |
|---|---|---|
| `PreShow` | boucle d'accueil 20 s (sans son) | `yeba-preshow.mp4` |
| `Generique` | générique d'ouverture 80 s, 9 scènes, bande-son | `yeba-saison1-generique.mp4` |
| `Episode` (props `numero`, `titre`, `sujet`, `motif`, `teinte`) | carte-titre 4,5 s + sting | `yeba-episode-N.mp4` |
| `Ambiance` / `FondCover` / `FondBaobab` / `FondJournee` / `FondSceau` / `FondFlux` / `FondBientot` | fonds vivants sous le texte du PPTX | `fond-*.mp4` |

```bash
cd soiree-lancement/remotion
npm install                       # une fois
npm run studio                    # éditeur visuel
npm run son                       # bande-son synthétisée (numpy/scipy, -16 LUFS) → public/audio/
npm run rendre                    # rendu des 19 vidéos + affiche .jpg de chacune
node scripts/rendre.mjs generique ep-2                 # seulement certains travaux
node scripts/rendre.mjs --images 600,1200 generique    # images de contrôle (dossier DOSSIER_IMAGES)
```
Le navigateur est détecté seul (`/opt/pw-browsers/chromium_headless_shell-*` en cloud, sinon Remotion le télécharge).

## Bible motion design (règles tenues partout)
- Une seule chronologie : `src/timeline.json` (images clés, temps forts, accords) partagée par la vidéo ET la musique.
- Courbes : EXPO (.16,1,.3,1) pour les entrées, QUINT pour les transformations, jamais linéaire.
- Boucles sans couture : chaque mouvement a une période qui divise la durée de la boucle ; aléatoire déterministe (mulberry32).
- **Aucun trait ne traverse un mot** : constellations, anneaux et flux restent hors des zones de texte ; les reflets dorés
  (`BalayageOr`) passent SOUS des panneaux opaques et sont rognés hors des titres (prop `zone`) ; une scène qui sort
  doit avoir disparu avant que les traits de la suivante n'apparaissent.
- Contrôle obligatoire : extraire des images (`ffmpeg -ss T -i x.mp4 -frames:v 1`) aux temps forts et les regarder.
  Plus simple : la compétence `watch` sur le MP4 rendu (`--detail efficient`, ou `--timestamps` aux temps forts), moteur local.

⚖️ Licence Remotion : gratuite pour les particuliers et les entreprises de 3 salariés maximum ; au-delà, licence
entreprise payante (vérifier sur remotion.pro). Musique synthétisée par script : aucun droit d'auteur tiers.
Rendu local : aucune donnée transmise.
