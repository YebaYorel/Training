---
name: reveal-js
description: Créer ou modifier la version web (HTML/CSS) des présentations YEBA avec Reveal.js — Auto-Animate (équivalent Morphose), fragments, vue orateur, 100 % hors ligne. À utiliser pour toute présentation HTML, ou quand on demande le code HTML/CSS des animations.
---

# Reveal.js 6 (MIT) — présentation web hors ligne

- Générateur : `soiree-lancement/revealjs/build_reveal.py` → `soiree-lancement/revealjs/index.html`
- Bibliothèque embarquée dans `revealjs/vendor/` (aucun CDN : rien ne sort de la salle le jour J).
  Mise à jour : `cd soiree-lancement/revealjs && npm install && cp node_modules/reveal.js/dist/{reveal.js,reveal.css,reset.css} vendor/`
- Polices : `revealjs/fonts/*.woff2` (Montserrat, OFL).

## Présenter
```bash
cd soiree-lancement && python3 -m http.server 8000
# ouvrir http://localhost:8000/revealjs/index.html — touche S = vue orateur (notes), F = plein écran
```

## Règles d'animation
- Le générateur importe `pptx/build_pptx.py` : même typographie, mêmes corps de titre, même séquence de slides.
- `data-auto-animate` sur chaque `<section>` + même `data-id` sur les éléments à faire glisser (titre, logo,
  agenda, étoiles et halo en parallaxe, tuile du catalogue → bande de la fiche).
- **Piège** : un élément apparié par Auto-Animate reçoit `transform: none` à la fin du morph → ne jamais mettre de
  `data-id` sur un élément pivoté ou centré par `transform` (centrer avec `calc()`).
- Entrées automatiques : classe `entree` + `--d` (délai) ; clic seulement là où le PowerPoint attend un clic (`fragment`).
- Fonds vivants : `data-background-video` (+ `-loop`, `-muted`) avec l'image fixe en `data-background-image` ;
  vidéos plein écran : `data-autoslide` = durée + 150 ms.
- `prefers-reduced-motion` : fonds vidéo retirés (image fixe), Auto-Animate et animations CSS coupés.
- Contrôle : captures Playwright 1600×900 après la fin des animations (≥ 4,5 s par slide), puis planche contact.
