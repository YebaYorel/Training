---
name: python-pptx
description: Générer ou modifier des PowerPoint (.pptx) YEBA par script Python avec python-pptx — motion design natif (Morphose, chronologie d'animations, vidéos en lecture automatique, fonds vidéo vivants), notes orateur, texte alternatif, slides masquées. À utiliser pour toute création/édition de .pptx dans ce dépôt.
---

# python-pptx (bibliothèque MIT, exécution 100 % locale)

Référence : `soiree-lancement/pptx/build_pptx.py` (21 gabarits : cover, statement, agenda, team, badges, word, quote,
tree, baobab, split, values, timeline, pillars, offres, journee, confiance, avantages, atelier, focus, demo, bientot + video).

```bash
python3 soiree-lancement/pptx/build_pptx.py            # version cinéma (fonds vidéo vivants)
python3 soiree-lancement/pptx/build_pptx.py --sobre    # mêmes fonds en images fixes
soffice --headless --convert-to pdf --outdir /tmp soiree-lancement/dist/YEBA_Soiree_Lancement.pptx
pdftoppm -r 40 -png /tmp/YEBA_Soiree_Lancement.pdf /tmp/s   # puis REGARDER chaque PNG
```
Le script s'arrête (code 2) et liste les textes qui ne tiennent pas : ne jamais livrer avec une alerte.

## Techniques clés
- **Chronologie native** (classe `Chrono`) : `<p:timing>` écrit à la main — groupe 0 lancé à l'ouverture
  (`onBegin`), groupes suivants au clic ; effets fondu, fondu montant, zoom, balayage avec décélération ;
  `mediacall playFrom(0.0)` + `p:video` (`repeatCount="indefinite"`, `mute="1"`) pour les fonds.
- `film()` retire le « clic = lecture/pause » que python-pptx ajoute (`a:hlinkClick` + `p:timing` par défaut).
- **Morphose** : `mc:AlternateContent` (`p159:morph`, repli `p:fade`) juste après `p:clrMapOvr`, `advTm` = avance
  automatique à la fin des vidéos ; appariement par nom `!!xxx` sur deux slides consécutives.
- **Calques** (`calques()`) : fond vidéo, étoiles `!!etoiles` (parallaxe), halo `!!halo`, vignettage — puis `au_fond()`
  les descend SOUS le titre (l'espace réservé Titre est créé en premier : sans cela, le fond le recouvre).
- **Typographie** (`typo()`) : espaces insécables à la française, « · » et « → » jamais en début de ligne,
  mots de 1-2 lettres jamais seuls en fin de ligne. Mesure réelle des glyphes Montserrat (800, 400 et Black 900),
  hauteur de ligne réelle 1,22 ; `verifier_slide()` refuse tout groupe insécable plus large que sa zone.
- Carrousel : groupes `!!av{page}-{i}-*` posés hors champ (±W) que la Morphose fait glisser.
- Post-it rouges hors champ (`a-confirmer`) : visibles en édition, jamais projetés.
