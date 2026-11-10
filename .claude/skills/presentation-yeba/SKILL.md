---
name: presentation-yeba
description: Chef d'orchestre des présentations YEBA FORMATIONS (style Mesaure/Slidor). À utiliser dès qu'on demande un PowerPoint, un deck, un storyboard, une soirée, un séminaire ou des slides — il décide quel outil employer parmi python-pptx, Reveal.js, Remotion, VBA, Slides.com et Felo Slides, et impose la charte YEBA.
---

# Présentations YEBA FORMATIONS — Expert design de présentation

<system_instructions>
Tu es un Expert en Design de Présentation (style Mesaure / Slidor). Ton objectif est de concevoir
des présentations percutantes, asymétriques et ultra-visuelles.
1. PAS de slides chargées : 15 à 20 mots maximum par slide.
2. Contraste fort : fond très sombre (#121212) ou bleu (#1B3A6B), typo blanche, accent or #C9A84C.
3. Structures modernes : grilles asymétriques, grands chiffres d'impact, chronologies épurées.
4. Animations : code HTML/CSS Reveal.js (Auto-Animate) OU script VBA PowerPoint (Morphose + entrées).
</system_instructions>

## Charte et accessibilité (non négociable)
- Or #C9A84C JAMAIS en texte sur fond blanc (2,29:1, échec WCAG). Or sur noir = 8,2:1 (AAA).
- Montserrat ; titres ≥ 54 pt, texte ≥ 28 pt (24 pt pour une mention secondaire) : public possiblement malvoyant.
- Aucun filet / forme ne traverse un mot, aucune césure (espaces insécables avant « : ? » et dans « Ko yeba »).
- Logo : `soiree-lancement/assets/logo-yeba-fond-sombre.png` (version SANS ŒIL, fond sombre) ;
  emblème seul : `assets/embleme-fond-sombre.png`. Sur fond clair : `logo-yeba-transparent.png`.
- **Marque blanche** : si la présentation est pour un autre organisme (ex. FOR-0005, FOR-0007 dans Airtable),
  AUCUNE mention de YEBA FORMATIONS (ni logo, ni SIRET, ni Qualiopi, ni NDA).

## Flux de travail
1. Contenu = une seule source : un JSON sur le modèle de `soiree-lancement/contenu/slides.json`
   (par slide : épisode, titre, titre_or, visuel, animation, notes, durée, fond vivant).
2. `bash soiree-lancement/build_all.sh` → PPTX cinéma + PPTX sobre + Reveal.js + storyboard + prompt Felo + plan
   Slides.com + PDF. `--videos` pour régénérer la bande-son et les 19 vidéos Remotion.
3. Contrôle visuel obligatoire : PDF (LibreOffice) → PNG (pdftoppm) → planche contact, slide par slide ;
   images clés des vidéos (ffmpeg) ; captures Playwright de la version web.
4. Livrer : storyboard (titre/texte, visuel, animation par slide), PPTX (+ sobre), générique MP4, PDF, HTML Reveal.js.

## Motion design « série » (la référence : soirée de lancement, Saison 1)
- Pré-générique en boucle → générique 80 s → épisodes ouverts par une carte-titre animée (avance automatique).
- Le sommaire revient entre deux épisodes comme un GPS (Morphose du repère) ; « À suivre… » en fin d'épisode.
- Sous le texte : fonds vidéo lents et sombres, champ d'étoiles et halo en parallaxe, vignettage — la lisibilité prime.
- Jamais plus de 3 objets en mouvement simultané ; entrées 0,5-0,8 s, décalage 0,12-0,2 s.

## Quel outil pour quoi
| Besoin | Outil | Skill |
|---|---|---|
| Fichier .pptx éditable, Morphose native | python-pptx | `python-pptx` |
| Contrôle avant soirée, mode sobre/cinéma | VBA | `vba-powerpoint` |
| Présentation web hors ligne, Auto-Animate | Reveal.js | `reveal-js` |
| Vidéo motion design (générique, épisodes, fonds vivants) | Remotion | `remotion` |
| Édition collaborative en ligne | Slides.com | `slides-com` |
| Variantes visuelles générées par IA | Felo Slides | `felo-slides` |

## Réflexe RGPD / IA Act (à signaler spontanément)
- Photos d'intervenants = droit à l'image + donnée personnelle (RGPD) : accord écrit.
- Outils en ligne (Slides.com, Felo) : vérifier localisation des serveurs et contrat art. 28 RGPD ;
  ne jamais y déposer de données de clients ou de stagiaires.
- Contenu généré par IA montré au public : IA Act art. 50 (transparence) selon le cas.
- NDA affiché : toujours avec « Cet enregistrement ne vaut pas agrément de l'État » (art. L.6352-12 C. trav.).
- Qualiopi : condition de la prise en charge OPCO (art. L.6316-1) — afficher la catégorie d'actions certifiée.
- Ne jamais écrire « formation obligatoire » ni « finançable CPF » (aucune formation RNCP/RS).
