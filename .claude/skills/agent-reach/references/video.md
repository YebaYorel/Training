# Vidéo / Podcast

Sous-titres et transcriptions : YouTube, Bilibili, podcasts Xiaoyuzhou.

## YouTube (yt-dlp)

### Récupérer les métadonnées d'une vidéo

```bash
yt-dlp --dump-json "URL"
```

### Télécharger les sous-titres

```bash
# Télécharger les sous-titres (sans la vidéo)
yt-dlp --write-sub --write-auto-sub --sub-lang "fr,en" --skip-download -o "/tmp/%(id)s" "URL"

# Puis lire le fichier .vtt
cat /tmp/VIDEO_ID.*.vtt
```

### Récupérer les commentaires

```bash
# Extraire les commentaires (au mieux, pas de garantie d'exhaustivité)
yt-dlp --write-comments --skip-download --write-info-json \
  --extractor-args "youtube:max_comments=20" \
  -o "/tmp/%(id)s" "URL"
# Les commentaires sont dans le champ comments du fichier .info.json
```

> ⚠️ RGPD : les commentaires contiennent des pseudonymes = données
> personnelles. Ne les conserver que si la finalité le justifie.

### Rechercher des vidéos

```bash
yt-dlp --dump-json "ytsearch5:requête"
```

> **Sous-titres** : ceux déposés manuellement sont fiables ; les sous-titres
> automatiques peuvent contenir des lignes répétées, à nettoyer.
> **Commentaires** : `--write-comments` repose sur la page web (pas sur l'API
> YouTube Data), certains commentaires peuvent manquer.

### Chaîne de reprise si les sous-titres échouent (dans l'ordre, s'arrêter dès qu'on a du contenu)

`doctor` vérifie seulement que yt-dlp et le runtime JS s'exécutent, sans
interroger de vidéo précise ; `active_backend: yt-dlp` ne garantit donc pas que
les sous-titres de la vidéo visée fonctionnent.

1. Commencer par la commande `yt-dlp --write-sub --write-auto-sub` ci-dessus.
2. Si vérification anti-robot, réponse vide ou aucun fichier de sous-titres, et
   qu'OpenCLI est connecté : `opencli youtube transcript "URL" -f yaml`.
3. Si OpenCLI renvoie `Caption URL returned empty response`, réessayer au plus
   3 fois : c'est une URL de sous-titres à durée limitée qui a expiré, pas une
   vidéo sans sous-titres.
4. Toujours en échec, ou vidéo réellement sans sous-titres :
   `agent-reach transcribe "URL"` (téléchargement de l'audio + transcription).

Le succès = un contenu de sous-titres/transcription réellement non vide, pas un
code de sortie ni le résultat de `doctor`.

### Solution de repli sans sous-titres : transcription Whisper

```bash
# Vidéo sans sous-titres : télécharger l'audio et le transcrire avec Whisper (clé Groq gratuite)
agent-reach transcribe "https://www.youtube.com/watch?v=VIDEO_ID"
agent-reach transcribe ./audio_local.mp3 -o /tmp/transcript.txt
```

> `agent-reach transcribe` accepte uniquement une URL http(s) publique ou un
> fichier audio local. Après une recherche `ytsearch5:`, choisir d'abord l'URL
> précise dans les résultats de yt-dlp, puis transcrire.
> Configurer d'abord une clé : `agent-reach configure groq-key` (saisie masquée ;
> gratuit, console.groq.com) ou `agent-reach configure openai-key`. Le mode auto
> utilise uniquement le premier fournisseur configuré (Groq en priorité, sinon
> OpenAI) et s'arrête en cas d'échec, sans envoyer l'audio à un autre.
> `--allow-provider-fallback` autorise explicitement le basculement : le même
> audio peut alors être traité par Groq ET OpenAI, avec des frais OpenAI
> possibles ; à n'utiliser qu'après avoir confirmé que le contenu peut être
> partagé avec les deux.
>
> ⚠️ Règle YEBA : Groq et OpenAI sont américains (hors UE). Ne jamais
> transcrire un enregistrement contenant la voix ou les données d'un client ou
> d'un stagiaire (RGPD : la voix est une donnée personnelle).

## Bilibili (bili-cli en principal, OpenCLI pour les sous-titres)

> ⚠️ **Ne pas utiliser yt-dlp pour Bilibili** : l'anti-robot de Bilibili bloque
> yt-dlp (erreur 412) dans tous les cas testés (dernière version,
> direct/proxy/avec cookie). yt-dlp sert uniquement pour YouTube.

### Détails / recherche / tendances / classements (bili-cli, lecture seule, sans connexion)

```bash
# Détails d'une vidéo (titre, auteur, durée, statistiques, sous-titres disponibles)
bili video BVxxx

# Rechercher des vidéos
bili search "requête" --type video -n 5

# Vidéos populaires / classement
bili hot -n 10
bili rank -n 10

# Télécharger l'audio et le découper en WAV prêt pour la transcription
bili audio BVxxx
```

### Sous-titres (OpenCLI, nécessite Chrome sur un poste de bureau)

```bash
# Sous-titres phrase par phrase avec horodatage
opencli bilibili subtitle BVxxx

# OpenCLI sait aussi chercher / lire les métadonnées (solution de secours)
opencli bilibili search "requête" -f yaml
opencli bilibili video BVxxx -f yaml
```

### Repli sans configuration : appel direct de l'API de recherche

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
curl -s -c /tmp/bili_ck.txt -o /dev/null -A "$UA" "https://www.bilibili.com/"
curl -s -b /tmp/bili_ck.txt -A "$UA" -e "https://www.bilibili.com/" \
  "https://api.bilibili.com/x/web-interface/search/all/v2?keyword=REQUETE&page=1"
```

> **Installer bili-cli** : `pipx install bilibili-cli` (plus maintenu depuis
> mars 2026 mais fonctionnel ; pas de connexion nécessaire en lecture seule).

## Podcasts Xiaoyuzhou

### Transcrire un épisode (option --polish pour améliorer la ponctuation)

```bash
# Produit un fichier Markdown dans /tmp/. --polish ajoute ponctuation et paragraphes via Llama 3.3 70B
~/.agent-reach/tools/xiaoyuzhou/transcribe.sh --polish "https://www.xiaoyuzhoufm.com/episode/EPISODE_ID"
```

### Prérequis

1. **ffmpeg** : `brew install ffmpeg` (macOS) ou `apt install ffmpeg`
2. **Clé API Groq** (gratuite) : https://console.groq.com/keys
3. **Configurer la clé** : `agent-reach configure groq-key` (saisie masquée)
4. **Premier lancement** : `agent-reach install --env=auto --system --channels=xiaoyuzhou` (accord explicite requis)

### Vérifier l'état

```bash
agent-reach doctor
```

## Guide de choix

| Situation | Outil recommandé |
|-----|---------|
| Sous-titres YouTube | yt-dlp ; si échec OpenCLI (3 essais max) → agent-reach transcribe |
| Détails / recherche Bilibili | bili-cli |
| Sous-titres Bilibili | opencli bilibili subtitle |
| Transcription de podcast | transcribe.sh Xiaoyuzhou |
| Audio/vidéo sans sous-titres | agent-reach transcribe (pour Bilibili, d'abord `bili audio`) |
