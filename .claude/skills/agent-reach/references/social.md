# Réseaux sociaux et communautés

XiaoHongShu, Twitter/X, Bilibili, V2EX, Reddit, Facebook, Instagram.

> ⚠️ **Règles YEBA — RGPD** : publications, profils et commentaires de
> personnes identifiables = données personnelles. Définir la finalité avant
> toute collecte, ne garder que le strict nécessaire, ne rien stocker
> durablement sans accord. Si les données servent à trier/noter des personnes
> → signaler l'**IA Act**. Toute configuration de cookie ou de session
> nécessite l'accord explicite d'Aurélien (CGU des plateformes + sécurité).
> Lecture seule uniquement : jamais de publication, commentaire ou « j'aime ».

## XiaoHongShu (réseau social chinois, plusieurs backends)

XiaoHongShu a trois backends : **lancer d'abord `agent-reach doctor --json` et
regarder l'`active_backend` de xiaohongshu**, puis utiliser le groupe de
commandes correspondant.

### Backend A : OpenCLI (préféré sur poste de bureau)

```bash
# Rechercher des notes
opencli xiaohongshu search "requête" -f yaml

# Lire une note + statistiques (utiliser l'URL complète des résultats, avec xsec_token)
opencli xiaohongshu note "NOTE_URL" -f yaml

# Commentaires (réponses imbriquées incluses)
opencli xiaohongshu comments NOTE_ID -f yaml

# Fil de recommandations de l'accueil
opencli xiaohongshu feed -f yaml

# Notes publiques d'un utilisateur
opencli xiaohongshu user USER_ID -f yaml
```

> Nécessite Chrome ouvert avec l'extension OpenCLI. OpenCLI utilise uniquement
> une session Chrome existante et contrôlée par l'utilisateur ; Agent Reach ne
> se connecte pas à sa place et ne lit pas les cookies du navigateur.
> `agent-reach configure xhs-cookies` n'injecte pas de cookie dans OpenCLI.
> Sans session existante : pas de connexion automatique ; passer aux backends
> B/C avec export manuel via Cookie-Editor.

### Backend B : xiaohongshu-mcp (usage serveur)

```bash
# Avant authentification : l'utilisateur exporte manuellement ses cookies avec Cookie-Editor, puis import explicite
agent-reach configure xhs-cookies

# Vérifier l'état (lecture seule)
mcporter call xiaohongshu.check_login_status --timeout 120000

# Rechercher
mcporter call xiaohongshu.search_feeds keyword="requête" --timeout 120000

# Détail d'une note + commentaires (feed_id et xsec_token issus des résultats de recherche)
mcporter call xiaohongshu.get_feed_detail feed_id="..." xsec_token="..." --timeout 120000
```

> Le premier appel télécharge un navigateur headless d'environ 150 Mo : toujours
> mettre `--timeout 120000`. Authentification uniquement par export manuel
> Cookie-Editor ; après import, lancer `check_login_status`. Cette commande
> enregistre les cookies du domaine xiaohongshu.com fournis par l'utilisateur
> (qui doit en valider l'étendue) ; les cookies d'autres domaines sont ignorés.

### Backend C : xhs-cli (ancien, plus maintenu depuis mars 2026)

```bash
xhs search "requête"        # recherche
xhs read NOTE_ID_OR_URL     # lire une note (URL/ID issus d'une recherche obligatoire)
xhs comments NOTE_ID_OR_URL # commentaires
xhs hot                     # tendances
xhs feed                    # recommandations
```

> Instable connu : `xhs user` / `xhs user-posts` / `xhs favorites` peuvent
> renvoyer une erreur d'API (non corrigée en amont). Pour une nouvelle
> installation, préférer les backends A/B.

### Remarques communes

> **Limite d'authentification** : Agent Reach ne doit pas se connecter à
> XiaoHongShu à la place de l'utilisateur ni lire les cookies du navigateur.
>
> **xsec_token** : XiaoHongShu impose un xsec_token, **impossible de lire une
> note avec un note_id nu**. Procédure : rechercher/parcourir le fil, puis lire
> via l'URL/ID complet du résultat. Valable pour les trois backends.
>
> **Fréquence** : les requêtes rapprochées (recherches en masse, commentaires
> en profondeur) déclenchent un captcha, impossible à contourner. Espacer de
> 2 à 3 secondes.
>
> **Écriture (publier/commenter/aimer)** : lecture seule recommandée (et
> imposée par les règles YEBA).

## Twitter/X (twitter-cli)

### Prérequis d'authentification

Les cookies enregistrés (saisie masquée) via `agent-reach configure
twitter-cookies` servent uniquement à `agent-reach doctor` pour vérifier que les
identifiants sont présents. `doctor` n'exécute pas `twitter status` et ne
configure pas le shell. Avant toute commande `twitter`, fournir explicitement,
dans le même shell ou sous-processus :

```bash
export TWITTER_AUTH_TOKEN="..."
export TWITTER_CT0="..."
```

### Commandes stables

```bash
# Fil d'accueil (le plus stable)
twitter feed -n 20

# Lire un tweet (avec réponses)
twitter tweet URL_OR_ID

# Lire un article long / X Article
twitter article URL_OR_ID

# Publications d'un utilisateur
twitter user-posts @username -n 20

# Profil d'un utilisateur
twitter user @username
```

### Commandes potentiellement instables

```bash
# Rechercher des tweets (Twitter change souvent ses endpoints GraphQL, 404 possible)
twitter search "requête" -n 10

# likes (depuis 2024, uniquement les siens — limite de la plateforme)
twitter likes
```

### Chaîne de reprise si la recherche échoue (dans l'ordre, s'arrêter au premier succès)

1. Réessayer une fois (échecs ponctuels fréquents) : `twitter search "requête" -n 10`
2. Mettre à jour puis réessayer : `pipx upgrade twitter-cli && twitter search "requête" -n 10`
3. Passer à OpenCLI (poste de bureau, session du navigateur) : `opencli twitter search "requête" -f yaml`
4. Sinon, contourner avec les commandes stables `twitter feed` / `twitter user-posts @quelquun`

### Remarques importantes

> **Installation** : `pipx install twitter-cli` (version 0.8.5 minimum)
>
> **Authentification** : uniquement export manuel via Cookie-Editor, puis
> variables d'environnement `TWITTER_AUTH_TOKEN` + `TWITTER_CT0` ; ne pas
> compter sur une lecture automatique du navigateur.
>
> **Risque IP** : éviter les appels fréquents depuis un VPS / IP de datacenter,
> surtout followers/following : risque de blocage du compte. Utiliser un
> proxy résidentiel ou l'environnement local.
>
> **OpenCLI en secours** : si OpenCLI est installé sur le poste,
> `opencli twitter search/article/user-posts -f yaml` fonctionne entièrement
> (session du navigateur, sans variables de cookie).
>
> **Format de sortie** : préférer `--yaml` ou `--json` (structuré, plus
> facile à exploiter par l'agent).

## Bilibili

> ⚠️ **Ne pas utiliser yt-dlp pour Bilibili** (bloqué par l'anti-robot, erreur
> 412, sans solution). Utiliser bili-cli / OpenCLI.

```bash
# Recherche / tendances / détails vidéo (bili-cli, lecture seule, sans connexion)
bili search "requête" --type video -n 5
bili hot -n 10
bili video BVxxx

# Sous-titres (OpenCLI, Chrome sur poste de bureau)
opencli bilibili subtitle BVxxx
```

> Commandes détaillées (transcription audio, appel direct de l'API) :
> voir [video.md](video.md).

## V2EX (forum tech chinois, API publique)

Pas d'authentification : appel direct de l'API publique.

### Sujets populaires

```bash
curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"
```

### Sujets d'une rubrique (nœud)

```bash
# node_name par ex. : python, tech, jobs, qna, programmers
curl -s "https://www.v2ex.com/api/topics/show.json?node_name=python&page=1" -H "User-Agent: agent-reach/1.0"
```

### Détail d'un sujet

```bash
# topic_id dans l'URL, ex. https://www.v2ex.com/t/1234567
curl -s "https://www.v2ex.com/api/topics/show.json?id=TOPIC_ID" -H "User-Agent: agent-reach/1.0"
```

### Réponses d'un sujet

```bash
curl -s "https://www.v2ex.com/api/replies/show.json?topic_id=TOPIC_ID&page=1" -H "User-Agent: agent-reach/1.0"
```

### Informations d'un utilisateur

```bash
curl -s "https://www.v2ex.com/api/members/show.json?username=USERNAME" -H "User-Agent: agent-reach/1.0"
```

### Exemple d'appel en Python

```python
from agent_reach.channels.v2ex import V2EXChannel

ch = V2EXChannel()

# Sujets populaires
topics = ch.get_hot_topics(limit=10)
for t in topics:
    print(f"[{t['node_title']}] {t['title']} ({t['replies']} réponses)")

# Sujets d'un nœud
node_topics = ch.get_node_topics("python", limit=5)

# Détail d'un sujet + réponses
topic = ch.get_topic(1234567)
print(topic["title"], "—", topic["author"])

# Informations d'un utilisateur
user = ch.get_user("Livid")
```

> **Liste des nœuds** : https://www.v2ex.com/planes

## Reddit (plusieurs backends, connexion obligatoire)

**Reddit n'a pas d'accès sans configuration** : les endpoints anonymes `.json`
sont bloqués (403), et l'API officielle n'est quasiment plus accordée depuis
novembre 2025 (validation manuelle). Les deux backends reposent sur une
session connectée : lancer d'abord `agent-reach doctor --json` et regarder
l'`active_backend` de reddit.

### Backend A : OpenCLI (préféré sur poste de bureau, session du navigateur)

```bash
# Rechercher des publications
opencli reddit search "requête" -f yaml

# Lire une publication complète + commentaires
opencli reddit read POST_ID -f yaml

# Parcourir un subreddit / tendances / Popular
opencli reddit subreddit LocalLLaMA -f yaml
opencli reddit hot -f yaml
opencli reddit popular -f yaml

# Informations d'un subreddit (abonnés, description)
opencli reddit subreddit-info LocalLLaMA -f yaml
```

> Nécessite Chrome ouvert et une connexion à reddit.com dans le navigateur.

### Backend B : rdt-cli (ancien / serveur, plus maintenu depuis mars 2026)

```bash
rdt search "requête" --limit 10 # rechercher des publications
rdt read POST_ID                # lire une publication + commentaires
rdt sub python --limit 20       # parcourir un subreddit
rdt popular --limit 10          # tendances
rdt all --limit 10              # /r/all
```

> **Installation** : `pipx install 'git+https://github.com/public-clis/rdt-cli.git'`
> (la version PyPI est en retard, installer la v0.4.2+ depuis GitHub). Lancer
> d'abord `rdt login` pour pouvoir chercher et lire (sur serveur sans
> navigateur, écrire le cookie à la main, voir les indications de doctor).
> Préférer la sortie `--yaml`.

### Option avancée : API officielle + PRAW (uniquement avec des identifiants existants)

Les utilisateurs ayant créé une « script app » Reddit avant novembre 2025
(client_id/client_secret) peuvent utiliser PRAW sur l'API officielle
(100 requêtes/minute gratuites). Les nouvelles demandes sont validées à la main
et quasiment refusées pour les projets personnels : **ne pas recommander cette
voie aux nouveaux utilisateurs**.

## Facebook (OpenCLI, connexion obligatoire)

Facebook passe par OpenCLI, en réutilisant la session facebook.com du Chrome
de l'utilisateur. Lancer d'abord `agent-reach doctor --json` : l'`active_backend`
de facebook doit normalement être `OpenCLI`. Ne pas proposer Jina/Exa/Graph API
comme voie par défaut.

```bash
# Rechercher personnes / pages / publications
opencli facebook search "requête" -f yaml

# Informations d'un profil ou d'une page
opencli facebook profile zuck -f yaml

# Fil d'actualité du compte connecté
opencli facebook feed --limit 10 -f yaml

# Groupes visibles par le compte / activité récente
opencli facebook groups --limit 20 -f yaml
```

> Nécessite Chrome ouvert avec l'extension OpenCLI et une connexion à
> facebook.com. Pour les groupes, seule la lecture de la liste et de
> l'activité récente visible par le compte est prise en charge, pas
> l'ensemble des publications et commentaires d'un groupe quelconque.

## Instagram (OpenCLI, connexion obligatoire)

Instagram passe par OpenCLI, en réutilisant la session instagram.com du Chrome
de l'utilisateur. Lancer d'abord `agent-reach doctor --json` : l'`active_backend`
d'instagram doit normalement être `OpenCLI`. Ne pas revenir par défaut à
instaloader (historiquement instable : cookies/401/429).

```bash
# Rechercher des utilisateurs (pas une recherche de mots-clés dans les publications)
opencli instagram search "requête" -f yaml

# Profil d'un utilisateur
opencli instagram profile nasa -f yaml

# Publications récentes d'un utilisateur
opencli instagram user nasa --limit 12 -f yaml

# Explorer / Découvrir
opencli instagram explore --limit 20 -f yaml

# Éléments enregistrés du compte
opencli instagram saved --limit 20 -f yaml
```

> Nécessite Chrome ouvert avec l'extension OpenCLI et une connexion à
> instagram.com. `instagram search` cherche des utilisateurs ; pour lire des
> publications, identifier d'abord le nom d'utilisateur puis
> `instagram user USERNAME`. En cas de 429 / « login required », demander à
> l'utilisateur de se reconnecter dans Chrome et réduire la fréquence.
