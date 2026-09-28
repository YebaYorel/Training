---
name: python-pptx
description: Générer ou modifier des PowerPoint (.pptx) YEBA par script Python avec python-pptx — gabarits sombres, Morphose injectée dans le XML, notes orateur, texte alternatif, slides masquées. À utiliser pour toute création/édition de .pptx dans ce dépôt.
---

# python-pptx (bibliothèque MIT, exécution 100 % locale)

Référence : `soiree-lancement/pptx/build_pptx.py` (18 gabarits : cover, statement, agenda, team, badges,
word, quote, tree, baobab, split, values, timeline, bignumber, pillars, formats, garage, focus, demo).

## Commandes
```bash
python3 soiree-lancement/pptx/build_pptx.py          # → soiree-lancement/dist/YEBA_Soiree_Lancement.pptx
soffice --headless --convert-to pdf --outdir /tmp soiree-lancement/dist/YEBA_Soiree_Lancement.pptx
pdftoppm -r 45 -png /tmp/YEBA_Soiree_Lancement.pdf /tmp/s   # puis REGARDER les PNG
```

## Techniques clés
- **Morphose** : fonction `morphose(slide, option)` → `mc:AlternateContent` avec `p159:morph`
  (repli `p:fade`), inséré juste après `p:clrMapOvr`. `option="byChar"` pour un mot qui se transforme.
- **Appariement Morphose** : même nom d'objet préfixé `!!` sur deux slides consécutives
  (`!!logo`, `!!marqueur`, `!!tuile-CODE`…).
- **Taille auto sans débordement** : `taille_qui_tient()` mesure les vrais glyphes Montserrat
  (`assets/fonts/*.ttf`) → plus grand corps possible, jamais de mot coupé.
- Layout « Titre seul » pour que chaque slide ait un vrai titre (lecteurs d'écran), `lang="fr-FR"`,
  `descr` (texte alternatif) sur chaque image, slide masquée via `show="0"`.
- Vidéo : `shapes.add_movie(...)` ; lecture auto réglée ensuite par la macro VBA.
