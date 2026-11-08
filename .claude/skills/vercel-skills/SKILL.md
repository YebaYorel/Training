---
name: vercel-skills
description: Lanceur des skills officiels Vercel (vercel-labs/agent-skills) — web-design-guidelines (règles d'interface web), react-best-practices, composition-patterns, react-view-transitions (transitions animées), vercel-optimize (performance Next.js), deploy-to-vercel, writing-guidelines. Utiliser pour concevoir, relire ou optimiser un site web React / Next.js, ou le déployer.
---

# Skills Vercel (lanceur)

Le dépôt d'origine **n'a pas de licence** : il n'est pas recopié dans ce dépôt,
il est récupéré à la demande, à une version relue.

## 1. Récupérer la version figée

```bash
python scripts/lanceur_depot.py vercel-labs/agent-skills 1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62 vercel-agent-skills
```

« ARRÊT » affiché = s'arrêter et prévenir Aurélien.

## 2. Choisir le skill utile et le suivre

Dans `.claude/vendor-cache/vercel-agent-skills/skills/` :

| Besoin | Dossier |
|---|---|
| Relire l'interface d'un site (accessibilité, ergonomie) | `web-design-guidelines` |
| Code React / Next.js performant | `react-best-practices`, `composition-patterns` |
| Transitions animées entre pages | `react-view-transitions` |
| Optimiser la vitesse d'un site Vercel | `vercel-optimize` |
| Déployer | `deploy-to-vercel` |
| Rédaction de textes d'interface | `writing-guidelines` |

Lire le `SKILL.md` du dossier choisi en entier, puis l'appliquer.

## 3. Réflexes YEBA

- Charte `yeba-charte` et `yeba-tokens.css` (polices auto-hébergées).
- **RGPD** : Vercel héberge aux États-Unis par défaut. Pour un site qui collecte
  des données (formulaire de contact, inscriptions), choisir une région UE ou un
  hébergeur UE, et le mentionner au client.
