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
- `data-auto-animate` sur chaque `<section>` + même `data-id` sur les éléments à faire glisser.
- Étapes au clic : classe `fragment` (`fade-up`, `zoom-in`, `fade-left`…).
- Toujours prévoir `@media (prefers-reduced-motion: reduce)` (accessibilité).
- Contrôle : capture headless
  `chrome --headless=new --screenshot --window-size=1600,900 "http://localhost:8000/revealjs/index.html?fragments=false#/S05"`
