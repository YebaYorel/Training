# Générateur de visuels YEBA IA

Refait tous les PNG de `../visuels/` aux couleurs de YEBA FORMATIONS
(#1B3A6B, #C9AB4C, #121212, #FFFFFF — Montserrat Bold + Inter, polices sous licence OFL).

```bash
cd reseaux-sociaux/outil-visuels
npm i playwright opentype.js   # une seule fois
node logo.js ../logo        # redessine le logo (sans l'œil) en SVG + PNG
node build.js ../visuels    # régénère les 43 visuels
```

Pour changer un texte : modifier `build.js` (ex. tableau des couvertures de Reels), relancer.
