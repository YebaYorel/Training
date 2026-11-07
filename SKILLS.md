# Skills, plugins et serveurs MCP — inventaire YEBA FORMATIONS

Tout est **versionné dans ce dépôt** (`.claude/`, `.mcp.json`) : chaque nouvelle
session Claude Code (cloud ou PC) ouvrant ce dépôt les retrouve automatiquement.
Pour les avoir dans **tous** les projets du PC : `python scripts/installer_skills_pc.py --appliquer`.

Relecture de sécurité effectuée le 2026-11-07 : hooks, scripts, appels réseau,
licences. Les **skills copiés** sont figés à un commit : une mise à jour amont
n'est jamais exécutée sans relecture. ⚠️ Les **4 plugins** (section suivante)
suivent en revanche la version publiée par leur auteur : ils sont plus à jour,
mais une version modifiée par l'auteur s'installerait sans relecture.

## 1. Installés et actifs

### Skills copiés dans `.claude/skills/` (fonctionnent sans connexion au dépôt d'origine)

| Skill(s) | Usage | Source @ commit | Licence |
|---|---|---|---|
| `founder-board`, `-brand`, `-cfo`, `-competitors`, `-consumer`, `-launch`, `-marketing`, `-offer`, `-ops`, `-plan`, `-pricing` | Tester une idée de business (conseil d'administration virtuel, CFO, panel de 100 acheteurs…) | Jakeschincariol/founder-skill @ `fd9385b` | MIT |
| `arena` | 100 sous-agents s'affrontent sur une même tâche | Jakeschincariol/arena-skill @ `df07b8e` | MIT |
| `ig-*` (13) | Instagram : légendes, carrousels, reels, DM, audit… | Jakeschincariol/instagram-agent-skill @ `d03c56b` | MIT |
| `frontend-slides` | Présentations HTML animées, ultramodernes | zarazhangrui/frontend-slides @ `9906a34` | MIT |
| `theme-factory` | Thèmes visuels prêts pour slides/documents | anthropics/skills @ `2c5958e` | Apache 2.0 |
| `yeba-powerpoint` | **Créé pour YEBA** : .pptx accessibles + transitions Morph/Prisme/Vortex + contrôle automatique | ce dépôt | — |
| `caveman`, `ultracave` | Mode réponses ultra-courtes (sur demande : `/caveman`) | JuliusBrussee/caveman @ `c310c9d` | Apache 2.0 |
| `task-observer` | Méta-skill « One Skill to Rule Them All » : améliore les skills | rebelytics/one-skill-to-rule-them-all @ `046b8f2` | CC BY 4.0 |
| `headroom` | Doc : réduire les tokens dans une appli qui appelle un LLM | chopratejas/headroom @ `12864fc` | Apache 2.0 |
| `llm-council` | Conseil de 5 IA → verdict. **Lanceur** : télécharge l'original (sans licence, donc non republié) dans un cache ignoré par Git | tenfoldmarc/llm-council-skill @ `0dc0327` | aucune |

### Plugins déclarés dans `.claude/settings.json` (installés au démarrage)

| Plugin | Usage | Remarque |
|---|---|---|
| `context-mode` | Garde les sorties d'outils hors du contexte (sessions plus longues) | 100 % local, sans télémétrie (Elastic License 2.0) |
| `cost-guardian` | Suivi des coûts / budget Claude Code | local |
| `video-context` | Claude « regarde » une vidéo (images clés + transcription whisper **locale**) | installe ffmpeg / yt-dlp / whisper au 1er usage |
| `linkedin-skills` | 12 skills LinkedIn (posts, commentaires, profil…) | la **publication** passe par l'API Publora (tiers) : brouillons OK sans compte |

Déjà disponibles via ton compte claude.ai (rien à installer) : `pptx`, `docx`,
`pdf`, `xlsx`, `canva-creator`, Gamma, Canva, `/security-review`.

### Serveurs MCP (`.mcp.json`)

| Serveur | État | Pourquoi |
|---|---|---|
| `baserow` | actif | existant (UE, Pays-Bas) |
| `playwright` | actif | navigateur piloté, local, version figée 0.0.83 (`scripts/playwright_mcp.py`) |
| `perplexity` | **désactivé** | société US : requêtes traitées hors UE. Activer via `/mcp` + variable `PERPLEXITY_API_KEY` |
| `composio` | **désactivé** | société US + concentre les accès OAuth à toutes tes applis (risque sécurité élevé). Activer via `/mcp` |

## 2. Non installés — décision motivée

| Demande | Raison | Alternative |
|---|---|---|
| **OmniRoute** | Passerelle vers ~350 fournisseurs d'IA gratuits (dont hors UE et qui entraînent leurs modèles sur les données envoyées) → incompatible souveraineté UE / RGPD art. 44+ pour des données clients | Mistral (FR) si besoin d'un 2e modèle |
| **claude-mem** | Par défaut, envoie l'activité de session à un service hébergé (CMEM Pro) ou à OpenRouter/Gemini → transfert hors UE | Mémoire native : `CLAUDE.md` + mémoire claude.ai. Mode local possible (`--provider host`) sur ton PC, à valider ensemble |
| **Agent-Reach** | Copie les cookies de connexion de ton Chrome et scrape X, Reddit, plateformes chinoises → risque sécurité (vol de session) + collecte de données personnelles par scraping (RGPD, recommandations CNIL) + CGU | Playwright MCP sur sites publics, au cas par cas |
| **higgsfield-ai/higgsfield** | Ce dépôt n'est **pas** l'outil vidéo Higgsfield AI : c'est un framework d'entraînement de LLM sur GPU (2023), inutile ici | Préciser l'outil voulu |
| **OpenMontage** | Projet complet (studio vidéo) dont les skills dépendent de son propre code et de clés API (fal.ai, Google…) : à utiliser dans **son propre dépôt** | Le cloner dans une session dédiée |
| **headroom (plugin)** | Le plugin reroute Claude Code via un proxy local : risque de casser les sessions cloud | Skill de documentation installé |
| **Firecrawl, PostHog** (connecteurs claude.ai) | Ne s'installent pas depuis un dépôt : claude.ai → Paramètres → Connecteurs | PostHog : choisir la région **UE** (Francfort). Firecrawl : US |
| **Security Sweep** | Aucun dépôt fourni | `/security-review` (intégré) en attendant le lien exact |

## 3. Mettre à jour une source

Ne jamais « tirer » la dernière version à l'aveugle : relire le diff amont,
puis recopier le dossier et mettre à jour le commit dans ce tableau.
