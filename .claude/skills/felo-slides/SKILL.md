---
name: felo-slides
description: Générer un prompt prêt à coller dans Felo Slides (générateur de slides par IA) à partir du contenu YEBA, pour explorer des variantes visuelles — sans aucune donnée personnelle.
---

# Felo Slides

Felo Slides est un service web (pas d'intégration locale) : Claude produit le prompt, l'utilisateur le colle.

- Prompt généré : `soiree-lancement/felo/prompt_felo_slides.md`
  (`python3 soiree-lancement/outils/generer_supports.py` le régénère depuis `contenu/slides.json`)
- Le prompt impose la charte (noir/bleu/or, Montserrat, 15-20 mots, Morphose).

⚖️ Souveraineté : éditeur établi hors UE (à vérifier dans ses CGU) → n'y coller QUE du contenu public ;
jamais de nom de client, de stagiaire, de prix négocié ni de document interne (RGPD, chap. V : transferts).
Contenu généré par IA et projeté : IA Act art. 50 selon le cas. Le livrable de référence reste le .pptx python-pptx.
