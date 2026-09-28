---
name: vba-powerpoint
description: Écrire ou adapter des macros VBA PowerPoint pour YEBA — appliquer la Morphose partout, poser des animations d'entrée automatiques d'après le nom des objets, régler la lecture vidéo, vérifier l'accessibilité (tailles < 24 pt).
---

# VBA PowerPoint

Module de référence : `soiree-lancement/vba/YebaAnimations.bas`

## Installation côté utilisateur
1. Ouvrir le .pptx → Alt + F11 → Fichier → Importer un fichier… → `YebaAnimations.bas`
2. Alt + F8 → `YebaToutAppliquer` (Morphose + animations + vidéo auto)
3. `YebaVerifierAccessibilite` → liste tout texte < 24 pt
4. Enregistrer en .pptx (les effets restent, la macro n'est pas nécessaire)

## Conventions
- Les effets sont choisis d'après le préfixe du nom d'objet (volet Sélection, Alt + F10) :
  `kicker`, `!!titre`, `!!carte`, `!!badge`, `!!num`/`!!val`, `!!ligne`, `!!baobab`, `puce`, `chip`, `!!live`…
- Objets `!!logo`, `!!ag*`, `!!marqueur`, `!!tuile-*`, `!!code-*`, `!!yeba` : laissés à la Morphose.
- Morphose : `ppEffectMorphByObject` / `ppEffectMorphByChar` (Microsoft 365 / PowerPoint 2019+),
  repli automatique `ppEffectFadeSmoothly`.
- Sécurité : ne jamais distribuer de .pptm à des clients ; livrer un .pptx sans macro.
