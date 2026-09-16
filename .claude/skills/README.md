# Skills Claude Code — YEBA FORMATIONS

26 skills sélectionnées dans 5 dépôts publics, filtrées sur un critère unique :
**aucune donnée ne doit sortir de l'Union européenne**.

## Installation permanente

Trois niveaux de permanence, du plus large au plus étroit.

### 1. Tous vos projets, sur votre poste (recommandé)

```bash
git clone https://github.com/YebaYorel/Training.git
cd Training
./.claude/install-skills.sh --dry-run   # simulation, n'écrit rien
./.claude/install-skills.sh             # copie vers ~/.claude/skills/
```

Les skills deviennent disponibles dans **toutes** vos sessions Claude Code, quel
que soit le projet. Le script ne télécharge rien et ne modifie pas votre
`~/.claude/CLAUDE.md` ; si une skill du même nom existe déjà, l'ancienne version
est sauvegardée en `~/.claude/skills/.<nom>.bak-<horodatage>` avant écrasement.

Mise à jour ultérieure : `git pull` puis relancer le script.

### 2. Toutes vos surfaces (Claude Code web, bureau, CLI, claude.ai)

Les sessions distantes comme celle-ci tournent dans un conteneur **détruit après
inactivité** : `~/.claude/skills/` y est éphémère. Ce qui survit est ce qui est
synchronisé depuis votre compte (mécanisme `~/.claude/skills/synced/`).

Pour qu'une skill vous suive partout : **claude.ai → Réglages → Capacités →
Skills → Téléverser**, en envoyant un `.zip` du dossier de la skill
(`SKILL.md` à la racine de l'archive).

```bash
cd .claude/skills && zip -r ../../stop-slop.zip stop-slop
```

### 3. Ce dépôt uniquement

Rien à faire : les skills de `.claude/skills/` sont chargées automatiquement
dans toute session ouverte sur ce dépôt. C'est déjà actif.

## Inventaire

### Formation, pédagogie et communication

| Skill | Usage |
|---|---|
| `stop-slop` | Supprime les tics d'écriture de l'IA. À passer sur **tout** support remis à un stagiaire ou à un client. |
| `practical-typography` | Typographie (Butterick) : corps, interlignage, césures. Support direct de l'**accessibilité visuelle** de vos PowerPoint. |
| `slides` | Présentations HTML structurées, avec graphiques Chart.js. |
| `design-system` | Jetons de design en trois couches — permet de figer les couleurs YEBA une fois pour toutes. |
| `brand` | Voix de marque, identité visuelle, cohérence des supports. |
| `banner-design` | Bannières réseaux sociaux, web et print. |
| `brainstorming` | Dialogue structuré pour concevoir une offre ou un programme avant de rédiger. |
| `idea-md` | Formalise une intuition en note de concept exploitable. |
| `scientific-critical-thinking` | Évalue la rigueur d'une affirmation ou d'une étude. Utile pour ne pas relayer de contre-vérité en formation IA. |

### Prospection et visibilité

| Skill | Usage |
|---|---|
| `direct-mail-strategist` | Campagnes de publipostage et mesure d'impact incrémental — pour toucher les TPE-PME réunionnaises en direct. |
| `seo-optimizer` | Audit SEO, métadonnées, données structurées, Core Web Vitals. |
| `ceo-review` | Relit une proposition commerciale sous l'angle d'un dirigeant. |

### Implémentation de workflows et solutions IA

| Skill | Usage |
|---|---|
| `mcp-builder` | Construire un serveur MCP propre (le connecteur Baserow de ce dépôt en est un). |
| `mcp-tester` | Auditer et tester des serveurs MCP de bout en bout. |
| `writing-plans` / `executing-plans` | Plan d'implémentation écrit, puis exécution avec points de contrôle. |
| `systematic-debugging` | Méthode de diagnostic avant toute correction. |
| `skimmable` | Passe de simplification finale : code lisible et relisable. |
| `ui-ux-pro-max` | 79 styles, 192 palettes, 74 appariements de polices, 119 règles UX, 25 types de graphiques, 22 stacks — **données locales**, aucun appel réseau. |
| `ui-styling` | shadcn/ui, Radix, Tailwind, accessibilité des composants. |
| `qmd` | Recherche hybride **locale** dans vos notes Markdown. Aucun envoi réseau. |
| `mem` | Mémoire persistante entre sessions. **Encadrée RGPD — voir ci-dessous.** |
| `task-observer` | Observe vos sessions et repère ce qui mérite de devenir une skill réutilisable. |

### Gouvernance, sécurité et audit

| Skill | Usage |
|---|---|
| `security-best-practices` | Revue de sécurité par langage (Python, JS/TS, Go), OWASP Top 10, chaîne d'approvisionnement, gestion des secrets. |
| `security-threat-model` | Modélisation de menaces STRIDE/PASTA ancrée dans un dépôt réel, avec considérations propres aux systèmes d'IA. |
| `cto-review` | Relecture technique : « est-ce que ça tient à l'échelle ? ». |

## Ce qui a été volontairement écarté

### Écarté pour non-souveraineté des données

| Skill | Motif |
|---|---|
| `design` (ui-ux-pro-max) | Génère logos et icônes via **Google Gemini**. Double motif : collision de nom avec la skill `design` native d'Anthropic. |
| `markdown-fetch` | Convertit les pages via **Cloudflare Workers AI** (États-Unis). |
| `llm-evaluation` | Utilise **GPT-4.1 d'OpenAI** comme juge d'évaluation. |
| `gemini-visual`, `gemini-image-generator`, `nano-banana` | Google Gemini. |
| `imagegen` | OpenAI Image API. |
| `codex-advisor`, `llm-advisor` | OpenAI Codex / GPT-4.1 / Gemini. |
| `google` | Google Workspace via CLI `gog`. |
| `cloudflare-manager` | Compte Cloudflare (États-Unis). |
| `bird-fast`, `poke-assistant`, `autopredict`, `opensea-api` | X/Twitter, poke.com, Polymarket, OpenSea. |

Transférer des données à ces services relève des **art. 44 à 49 du RGPD**
(transferts hors UE). C'est juridiquement praticable via le *Data Privacy
Framework*, mais commercialement intenable pour un cabinet qui vend la
souveraineté des données. Ces skills restent réinstallables en une commande —
voir « Réactiver une skill écartée » ci-dessous.

### Écarté pour risque de sécurité

`skill-finder` installe automatiquement des skills depuis Internet. Une skill
est du texte que l'agent exécute comme une instruction : l'installation
automatique depuis une source non vérifiée est une **porte ouverte à une
compromission de la chaîne d'approvisionnement**. Toute skill ajoutée ici doit
être relue avant installation.

### Écarté pour doublon fonctionnel

`continuous-learning` fait le même travail que `task-observer`. Deux skills
concurrentes sur le même déclencheur dégradent le choix de l'agent.

### Écarté pour hors-sujet

Métro de New York, jeux Playdate, NFT, shaders 3D, CoreML, Gaussian Splats,
applications macOS/iOS, Freshdesk, publipostage américain (Poplar) — sans
rapport avec vos trois activités. Chaque skill installée consomme du contexte à
chaque session et dilue la pertinence des autres : **l'élagage est une décision
technique, pas une préférence esthétique.**

### Réactiver une skill écartée

```bash
git clone --depth 1 https://github.com/ckorhonen/claude-skills.git /tmp/cs
cp -r /tmp/cs/skills/<nom-de-la-skill> ~/.claude/skills/
```

## RGPD et IA Act — ce qui vous engage

**Les skills elles-mêmes ne sont pas un traitement de données personnelles :**
ce sont des fichiers Markdown d'instructions. Aucune formalité n'est due pour
leur simple installation.

**Trois points appellent cependant votre vigilance.**

1. **`mem` — RGPD.** Elle écrit en clair dans `~/.claude/memory/`, sans
   chiffrement, sans durée de conservation, sans journalisation. Y consigner le
   nom d'un stagiaire, son e-mail ou *a fortiori* sa situation de handicap
   constituerait un traitement sans base légale ni information des personnes
   (**art. 5, 6, 13 et 9** du RGPD), hors de votre registre (**art. 30**) et
   sans mesure de sécurité appropriée (**art. 32**). Le `SKILL.md` porte une
   barrière explicite qui l'interdit et redirige ces données vers Baserow
   (cloud UE), où finalité, durée et base légale sont définies. **Cette barrière
   est une instruction, pas un contrôle technique : elle réduit le risque, elle
   ne le supprime pas.** Un contrôle effectif supposerait un chiffrement du
   dossier et une purge programmée.

2. **`security-threat-model` et `security-best-practices` — IA Act.** Ces
   skills produisent une analyse, jamais une conformité. Un audit RGPD ou IA Act
   remis à un client engage **votre** responsabilité professionnelle, pas celle
   de l'outil. Leur sortie est un brouillon à vérifier intégralement.

3. **Votre position de déployeur — IA Act, art. 4.** L'obligation de *littératie
   en IA* s'applique depuis le **2 février 2025** à tout déployeur de systèmes
   d'IA, y compris pour ses propres équipes. Elle est déjà satisfaite dans votre
   cas (Google AI Specialist, Google Professional AI, MOOC CNIL,
   SecNumAcadémie), mais elle doit être **documentée** : c'est précisément un
   argument opposable en rendez-vous client, et un point à faire figurer dans
   vos audits.

**Classification IA Act de ces outils :** assistance à la production de contenu
et au développement logiciel → **risque minimal** (art. 6 *a contrario*). Aucune
obligation au titre du haut risque. Attention toutefois : **si vous construisez
pour un client un workflow de tri de candidatures, de scoring de prospects ou
d'évaluation de salariés, vous basculez en annexe III — haut risque**, avec
analyse d'impact, documentation technique, journalisation et supervision
humaine. Les skills ne changent pas cette classification ; l'usage que vous en
faites, si.

## Licences

| Dépôt | Licence |
|---|---|
| ckorhonen/claude-skills | MIT — © 2025 Chris Korhonen |
| nextlevelbuilder/ui-ux-pro-max-skill | MIT — © 2024 Next Level Builder |
| hardikpandya/stop-slop | MIT — © 2025 Hardik Pandya |
| hanfang/claude-memory-skill | MIT — © 2024 |
| rebelytics/one-skill-to-rule-them-all | **CC BY 4.0** — attribution obligatoire |

Les quatre licences MIT autorisent la redistribution dans ce dépôt, y compris
commerciale, à condition de conserver les fichiers `LICENSE` — ils sont
présents dans chaque dossier concerné.

`task-observer` relève de **Creative Commons Attribution 4.0**, et non de MIT :
toute réutilisation publique (support de formation, article, prestation client)
doit **citer rebelytics/one-skill-to-rule-them-all**. C'est une obligation, pas
une convention d'usage.

## Sources

- Dépôts : les 5 URL GitHub ci-dessus, clonés et audités le 16 septembre 2026.
- Format des skills et emplacements de chargement : documentation Claude Code,
  https://code.claude.com/docs
- RGPD : Règlement (UE) 2016/679, art. 5, 6, 9, 13, 17, 30, 32, 44-49.
- IA Act : Règlement (UE) 2024/1689, art. 4 (littératie, applicable depuis le
  02/02/2025), art. 6 et annexe III (classification), art. 50 (transparence).
