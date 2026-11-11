---
name: openmontage
description: Lanceur d'OpenMontage (calesthio/OpenMontage, AGPL-3.0, ~78 000 étoiles) — studio de production vidéo par agents : recherche, script, génération d'images et de plans, montage, musique, composition Remotion ; peut partir d'une vidéo de référence. Utiliser pour produire une vidéo promotionnelle, un teaser de formation, une vidéo explicative ou un court métrage.
---

# OpenMontage (lanceur)

OpenMontage est un projet complet (164 Mo, code + outils) : il est récupéré à la
demande, à une version relue, dans un cache ignoré par Git.

## 1. Récupérer la version figée

```bash
python scripts/lanceur_depot.py calesthio/OpenMontage d21f5d4eaa08422b09c7091757a05affcbabb35b openmontage
```

« ARRÊT » affiché = s'arrêter et prévenir Aurélien.

## 2. Travailler DANS le dossier OpenMontage

Se placer dans `.claude/vendor-cache/openmontage/`, lire `AGENT_GUIDE.md` en
entier (point d'entrée obligatoire du projet), puis suivre ses consignes et
ses skills (`.claude/skills/` de ce dossier). Installer ses dépendances
seulement après avoir montré à Aurélien la liste de ce qui va être installé.

## 3. Points d'attention

- **Clés API** : les générateurs (fal.ai, Google, etc.) demandent des clés et sont
  **payants** ; services hors UE. Annoncer le coût estimé avant de lancer.
- **RGPD / droit à l'image** : pas de visage ni de voix d'une personne réelle
  sans son accord écrit.
- **IA Act art. 50** : une vidéo générée par IA réaliste (personnes, lieux réels)
  doit être signalée comme telle.
- **Licence AGPL-3.0** : utilisable librement pour produire des vidéos ; si
  Aurélien modifie OpenMontage **et** le propose comme service en ligne à des
  tiers, il devra publier ses modifications.
