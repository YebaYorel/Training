---
name: slides-com
description: Préparer une présentation YEBA pour Slides.com (éditeur en ligne bâti sur Reveal.js) — import PDF/PPTX, reconstruction avec Auto-Animate, CSS de la charte, précautions RGPD.
---

# Slides.com

Slides.com n'expose pas d'API publique de création : Claude prépare les fichiers, l'utilisateur importe.

1. `bash soiree-lancement/build_all.sh` → `dist/YEBA_Soiree_Lancement.pdf` et `.pptx`
2. Plan de montage généré : `soiree-lancement/slides-com/plan_slides_com.md`
   (texte projeté + animation à régler par slide)
3. Dans Slides.com : importer le PDF/PPTX (selon l'offre) ou reconstruire ; activer Auto-Animate et
   donner le même *Animation ID* aux éléments qui doivent glisser ; coller le CSS de
   `revealjs/build_reveal.py` (variable `CSS`) dans Theme → Custom CSS.

⚖️ RGPD : service en ligne — vérifier la localisation d'hébergement et le contrat de sous-traitance
(art. 28) ; présentation en mode privé ; aucune donnée de client ou de stagiaire.
