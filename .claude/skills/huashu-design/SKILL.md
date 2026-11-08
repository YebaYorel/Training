---
name: huashu-design
description: Lanceur du skill huashu-design (alchaincyf/huashu-design, MIT, ~29 000 étoiles) — designs haute fidélité en HTML, prototypes d'apps, présentations PowerPoint ÉDITABLES (.pptx), animations, infographies, revue experte ; propose trois directions visuelles avant de produire. Utiliser pour une présentation ou un visuel « waouh », une infographie, une animation, un prototype, quand on veut plusieurs pistes créatives.
---

# huashu-design (lanceur)

Le skill d'origine pèse 41 Mo (musiques, images d'exemple) : il n'est pas
recopié dans le dépôt, il est téléchargé à la demande à une version relue.

## 1. Récupérer la version figée

```bash
python scripts/lanceur_depot.py alchaincyf/huashu-design b2460b031c33ff32d2bf3b97263527daa231e4de huashu-design
```

Le script affiche le dossier du cache. S'il affiche « ARRÊT », s'arrêter et
prévenir Aurélien.

## 2. Suivre le skill

Lire `.claude/vendor-cache/huashu-design/SKILL.md` en entier et l'appliquer.
Les chemins `references/`, `scripts/`, `assets/` qu'il cite sont relatifs à ce
dossier. Le skill est rédigé en chinois : travailler et répondre **en français**.

## 3. Adaptations obligatoires YEBA

- Appliquer la charte `yeba-charte` (sauf travail pour un autre centre de
  formation) et, pour un support de formation, les règles d'accessibilité de
  `yeba-powerpoint` (vérifier le .pptx avec `verifier_accessibilite.py`).
- **Ne pas utiliser la voix off / synthèse vocale ByteDance (Volcengine)** prévue
  par certains scripts : service hors UE (Chine), **RGPD** chapitre V. Utiliser
  une voix enregistrée ou une solution locale.
- **IA Act art. 50** : signaler les visuels générés par IA représentant des
  personnes ou des lieux réels de façon réaliste.
