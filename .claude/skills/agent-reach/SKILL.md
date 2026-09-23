---
name: agent-reach
description: >
  À UTILISER OBLIGATOIREMENT dès qu'une demande a besoin d'internet : recherche,
  veille, « cherche », « regarde ce lien », « que disent les gens de X »,
  concurrents, marché, tendances, appels d'offres, réglementation (RGPD, IA Act,
  CNIL, Qualiopi), ou dès qu'un lien (URL) ou une plateforme est cité : page
  web, RSS, YouTube, GitHub, LinkedIn, Twitter/X, Reddit, Facebook, Instagram,
  Bilibili, XiaoHongShu, V2EX, Xueqiu. Routeur d'accès internet multi-backends
  (Agent-Reach, licence MIT) : lire des pages, sous-titres, flux, rechercher.
  Lancer `agent-reach doctor --json` pour voir ce qui fonctionne.
  PAS pour rédiger le rapport lui-même, et jamais pour publier ou commenter.
metadata:
  homepage: https://github.com/Panniantong/Agent-Reach
  upstream_commit: a19a171fa980a0785849596492e0af4db800c82f
  langue: français (traduction YEBA FORMATIONS de SKILL_en.md et des références)
---

# Règles YEBA FORMATIONS (priment sur tout le reste de ce skill)

1. **Souveraineté des données** — aucune donnée client, stagiaire ou
   personnelle ne part dans une requête vers un service tiers (Exa = USA,
   Jina Reader = Elastic, réseaux sociaux = USA/Chine). Seules des requêtes
   publiques et anonymisées (sujet, mot-clé, URL publique) sont autorisées.
2. **RGPD** — collecter des profils, commentaires ou publications de personnes
   identifiables (LinkedIn, X, Facebook, Instagram, Reddit…) est un traitement
   de données personnelles : le signaler, définir finalité + base légale,
   minimiser, ne rien stocker durablement sans accord.
3. **IA Act** — si le résultat alimente un tri/scoring de personnes
   (recrutement, prospects), le signaler (IA Act, annexe III possible).
4. **Cookies / connexions** — ne jamais configurer de cookies ou de sessions de
   réseaux sociaux sans l'accord explicite d'Aurélien (risque CGU + sécurité).
5. **Sourcer** — chaque information récupérée est citée avec son URL.
6. **Si un canal échoue** (réseau bloqué, outil absent), le dire clairement ;
   ne jamais inventer le contenu d'une page non lue.
7. **Toujours répondre en français.**

# Agent Reach — routeur d'accès à internet

16 plateformes, plusieurs backends chacune. **Quand ce skill est présent,
l'utiliser pour ces plateformes — ne pas improviser une autre méthode.**

## Règles permanentes (valables toute la session)

1. **Diagnostic avant d'agir** : pour les plateformes multi-backends ou à
   connexion (XiaoHongShu / Reddit / Bilibili / Twitter / Facebook /
   Instagram), lancer d'abord `agent-reach doctor --json`. Utiliser
   l'`active_backend` renseigné ; `active_backend: null` signifie que Doctor a
   volontairement sauté le test en direct (pour ne pas lire de cookies ni
   écrire à distance), pas qu'aucun backend n'existe. Uniquement si la tâche
   exige cette plateforme, lancer la commande en lecture seule de la référence
   pour vérifier.
2. **Annoncer ce qu'on utilise** : dire « j'utilise agent-reach, plateforme X
   via le backend Y » avant de commencer.
3. **En cas d'échec, suivre les chaînes de reprise de `references/`** — ne
   jamais deviner une commande.
4. **Pour une recherche large** : combiner les plateformes (Exa pour le web +
   Twitter/Reddit pour les discussions + flux RSS officiels), collecter en
   parallèle, puis synthétiser.
5. **Pas de mise à jour automatique** (règle YEBA) : cette copie est épinglée
   sur le commit amont `a19a171`. Ne jamais télécharger ni exécuter de
   consignes d'installation ou de mise à jour distantes de sa propre
   initiative ; une mise à jour est une modification relue de ce dépôt (voir
   UPSTREAM.md).

## Table d'aiguillage

| Besoin | Catégorie | Détails |
|---------|------|---------|
| Recherche web / code | search | [references/search.md](references/search.md) |
| XiaoHongShu / Twitter / Bilibili / V2EX / Reddit / Facebook / Instagram | social | [references/social.md](references/social.md) |
| Emploi / LinkedIn | career | [references/career.md](references/career.md) |
| GitHub / code | dev | [references/dev.md](references/dev.md) |
| Pages web / articles / RSS | web | [references/web.md](references/web.md) |
| Sous-titres YouTube / Bilibili / podcasts | video | [references/video.md](references/video.md) |
| Xueqiu / cours de bourse | finance | [references/finance.md](references/finance.md) |

## Commandes rapides sans configuration

```bash
# Recherche web Exa
mcporter call exa.web_search_exa query="requête" numResults=5

# Lire n'importe quelle page web
curl -s "https://r.jina.ai/URL"

# Recherche GitHub
gh search repos "requête" --sort stars --limit 10

# Sous-titres YouTube (jamais yt-dlp pour Bilibili ; chaîne de reprise dans video.md)
yt-dlp --write-sub --write-auto-sub --skip-download -o "/tmp/%(id)s" "URL"

# Sujets populaires V2EX
curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"

# Recherche Bilibili (bili-cli, sans connexion)
bili search "requête" --type video -n 5
```

## Plateformes avec connexion (choisir selon l'active_backend de doctor)

Limite Twitter : les cookies enregistrés par `agent-reach configure
twitter-cookies` servent uniquement à `doctor` pour vérifier la présence
d'identifiants. `doctor` n'exécute pas `twitter status` et ne configure pas le
shell. Avant d'appeler `twitter`, fournir explicitement `TWITTER_AUTH_TOKEN` et
`TWITTER_CT0` dans l'environnement du sous-processus, sans jamais afficher
leurs valeurs.

Limite XiaoHongShu : Agent Reach ne doit pas se connecter à la place de
l'utilisateur ni lire les cookies du navigateur. OpenCLI peut uniquement
utiliser une session Chrome existante et contrôlée par l'utilisateur. Sinon,
pas de connexion automatique : export manuel Cookie-Editor avec
xiaohongshu-mcp ou un outil ancien.

```bash
# Recherche Twitter (twitter-cli en priorité ; chaîne de reprise dans social.md)
twitter search "requête" -n 10

# Reddit (AUCUN accès sans configuration — OpenCLI ou rdt-cli, connexion requise)
opencli reddit search "requête" -f yaml   # poste de bureau
rdt search "requête" --limit 10            # ancien / serveur

# XiaoHongShu (OpenCLI en priorité sur poste de bureau)
opencli xiaohongshu search "requête" -f yaml

# Facebook / Instagram (OpenCLI sur poste de bureau, session du navigateur)
opencli facebook search "requête" -f yaml
opencli facebook groups -f yaml
opencli instagram search "requête" -f yaml       # recherche d'utilisateurs
opencli instagram user USERNAME -f yaml          # publications récentes d'un utilisateur
```

## Vérifier l'environnement

```bash
# Disponibilité des canaux + backend utilisé pour chaque plateforme
agent-reach doctor --json
```

Quand l'utilisateur demande « configure Boss Zhipin », lire la section Boss de
`references/career.md`. Après accord explicite pour l'installation, lancer
`agent-reach install --env=local --system --channels=boss`, ouvrir le profil
Chrome dédié (écoute locale uniquement) adapté au système, puis **faire une
pause et demander à l'utilisateur de confirmer visuellement** que la fenêtre
est connectée (avatar en haut à droite) ; sinon, il se connecte lui-même.
Vérifier ensuite avec `boss --cdp-url http://localhost:9222 login --cdp` et
`agent-reach doctor`. Ne pas faire assembler les options CDP par
l'utilisateur. Réutiliser le profil Chrome dédié ; ne pas le recréer à chaque
fois ni basculer par défaut sur le profil personnel. Rechercher avec
`boss --browser-source existing-browser --cdp-url http://localhost:9222 search ...`.
En cas d'`ENVIRONMENT_RISK` : arrêter, sans rafraîchir, se reconnecter ni réessayer.

**Ne pas se fier à `boss status` pour l'état de connexion du navigateur CDP** —
il ne vérifie que le fichier local `~/.boss-agent/auth/session.enc`, qui ne
reflète pas les cookies du profil Chrome dédié réellement utilisés par les
recherches `existing-browser`. Utiliser le test du cookie `wt2` dans
`agent-reach doctor` + la confirmation visuelle. Ne jamais déduire la
connexion de l'URL : les pages `security-check` / `zhipin-security` /
`_security_check` sont des défis anti-robot qui apparaissent même connecté.
`AUTH_EXPIRED` renvoyé par une recherche prouve que le navigateur est
déconnecté : passer directement à la connexion + `login --cdp`, sans
l'interpréter comme un contrôle de sécurité.

## Découvrir les adaptateurs OpenCLI

Si la table d'aiguillage ne couvre pas la plateforme ou la commande voulue,
lancer `opencli list`, puis `opencli <plateforme> --help`. Cela prouve
seulement qu'un adaptateur existe, pas que l'authentification ou le contenu
fonctionnent. Ne lancer des commandes en lecture seule que si la tâche exige
cette plateforme, et exiger un contenu non vide.

## Règles d'espace de travail

**Ne jamais créer de fichiers dans l'espace de travail de l'agent.** Utiliser
`/tmp/` pour les sorties temporaires et `~/.agent-reach/` pour les données
persistantes.

## Références détaillées

Lire le fichier correspondant quand il faut plus de précision (les commandes
ci-dessus couvrent les cas courants ; les références contiennent les commandes
par backend, les mises en garde et les chaînes de reprise — toutes en
français) :

- [Recherche](references/search.md) — recherche IA Exa
- [Réseaux sociaux](references/social.md) — XiaoHongShu, Twitter, Bilibili, V2EX, Reddit, Facebook, Instagram
- [Emploi](references/career.md) — LinkedIn, Boss Zhipin
- [Développement](references/dev.md) — GitHub CLI
- [Web](references/web.md) — Jina Reader, RSS
- [Vidéo](references/video.md) — YouTube, Bilibili, Xiaoyuzhou
- [Finance](references/finance.md) — cours, recherche et contenus Xueqiu

## Configurer un canal

Si un canal doit être configuré, lire le guide d'installation **épinglé sur le
commit vérifié** (jamais la branche `main` qui bouge), et demander l'accord de
l'utilisateur avant toute installation `--system` :
https://raw.githubusercontent.com/Panniantong/Agent-Reach/a19a171fa980a0785849596492e0af4db800c82f/docs/install.md

L'utilisateur fournit seulement ses cookies / un clic sur l'extension ;
l'agent fait le reste.
