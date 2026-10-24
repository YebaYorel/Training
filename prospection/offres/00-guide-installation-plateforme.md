# Guide d'installation — Plateforme IA souveraine YEBA FORMATIONS

> **But** : installer, dans l'ordre, tout ce qu'il faut pour faire tourner les solutions proposées aux
> structures (assistant IA, comptes rendus automatiques, automatisations, base de données, chatbot
> transparent, coffre-fort de mots de passe, supervision, sauvegardes) **sur des serveurs en France**,
> avec des outils européens ou open source auto-hébergés.
>
> **Deux usages du même guide** :
> 1. **Votre plateforme** (YEBA FORMATIONS) : démonstrations, formations, vos propres automatisations.
> 2. **Le « kit client »** (étape 20) : le même déploiement, **au nom du client, sur un serveur qu'il
>    loue lui-même** — c'est ce qui rend l'offre reproductible et conforme aux licences.
>
> Les prix sont ceux trouvés en octobre 2026 (sources en fin de document) ; **vérifiez-les au moment
> de commander**. Tout ce qui est marqué **[À VÉRIFIER]** n'a pas pu être confirmé par une source primaire.

---

## Vue d'ensemble (ce que vous allez construire)

```
                    Internet (HTTPS uniquement)
                               │
                        ┌──────▼──────┐
                        │    Caddy    │  certificats HTTPS automatiques + journaux
                        └──────┬──────┘
   ┌──────────────┬────────────┼─────────────┬──────────────┬───────────────┐
   │              │            │             │              │               │
 ia.domaine   auto.domaine  base.domaine  coffre.domaine  statut.domaine   (interne)
 Open WebUI      n8n          Baserow      Vaultwarden    Uptime Kuma     Whisper
 (assistant)  (automates)   (base de       (mots de       (surveille     (transcription
     │            │          données)       passe)         tout)          locale)
     │            ├─── PostgreSQL (mémoire de n8n)
     └────────────┴─── API Mistral (France) ou Albert (État, pour les administrations)

 Autour : CrowdSec (bloque les attaquants) · pare-feu · sauvegardes chiffrées (restic → stockage objet OVH)
```

| Brique | Rôle | Éditeur / pays | Licence | Coût |
|---|---|---|---|---|
| VPS OVHcloud | le serveur | OVHcloud, France | — | VPS-1 : 7,79 €/mois depuis le 01/04/2026 ; VPS-2 ≈ 11,75 $ ; VPS-3 ≈ 23,50 $ (prix forum) **[À VÉRIFIER]** |
| *(alternative)* Hetzner CX33 | le serveur | Hetzner, Allemagne | — | 8,49 €/mois depuis le 15/06/2026 |
| Ubuntu Server 24.04 LTS | système | Canonical (R.-U.) | libre | gratuit |
| Docker + Compose | fait tourner les services | Docker Inc. | Apache 2.0 | gratuit |
| Caddy | HTTPS automatique | projet open source | Apache 2.0 | gratuit |
| n8n | automatisations | n8n GmbH, Berlin | Sustainable Use License (voir étape 20) | gratuit auto-hébergé |
| Baserow | base de données / CRM | Baserow B.V., Pays-Bas | open source (+ Premium) | gratuit auto-hébergé ; Premium ≈ 10 $/utilisateur/mois (source tierce) |
| Open WebUI | interface de l'assistant IA | projet open source | BSD-3 + clause de marque (logo à conserver au-delà de 50 utilisateurs) | gratuit |
| API Mistral | le « cerveau » IA | Mistral AI, France | commercial | à l'usage (ex. Mistral Small 4 ≈ 0,15 $ / 0,60 $ par million de tokens, entrée / sortie — source tierce 2026) |
| Albert API | le « cerveau » IA des administrations | DINUM (État) | — | gratuit pour l'administration, dans la limite des capacités (2024) **[conditions 2026 À VÉRIFIER]** |
| faster-whisper / Speaches | transcription audio locale | open source | MIT | gratuit (tourne sur le VPS) |
| *(alternative)* Voxtral API | transcription | Mistral AI, France | commercial | ≈ 0,003 $/minute (Mini Transcribe 2) |
| Vaultwarden | coffre-fort de mots de passe | open source | AGPL-3.0 | gratuit |
| Uptime Kuma | supervision | open source | MIT | gratuit |
| CrowdSec | blocage des attaquants | CrowdSec, France | MIT | gratuit |
| restic | sauvegardes chiffrées | open source | BSD-2 | gratuit (+ stockage objet OVH, **prix À VÉRIFIER**) |
| Brevo | envoi d'emails (SMTP) | Brevo, France | commercial | gratuit 300 emails/jour ; Starter dès ≈ 9 $/mois |
| Logiciel PIA | analyses d'impact RGPD | CNIL, France | open source | gratuit |

**Pourquoi pas ChatGPT, Copilot ou Gemini ?** Ce sont d'excellents outils, mais ils sont édités par des
sociétés américaines soumises au *Cloud Act*, même quand les données sont stockées en Europe. Votre
positionnement (et celui de vos clients publics) repose sur la **souveraineté européenne** : on s'en tient
donc à Mistral (France), à Albert (État) ou à des modèles ouverts exécutés sur vos serveurs.

---

## Étape 0 — Prérequis (½ journée)

**Comptes à créer (au nom de YEBA FORMATIONS)** :
1. **OVHcloud** (serveur, nom de domaine, stockage objet) — activer la double authentification.
2. **Mistral AI — La Plateforme** (clé API, offre payante) — activer la double authentification ;
   télécharger et signer l'accord de sous-traitance (DPA) proposé par Mistral **[À VÉRIFIER : emplacement du DPA]**.
   ⚠️ N'utilisez **jamais la version gratuite** de Le Chat avec des données clients : plusieurs sources
   indiquent que les conversations gratuites servent à entraîner les modèles par défaut (août 2026).
3. **Brevo** (envoi d'emails) — compte gratuit pour commencer.

**Sur votre ordinateur** :
- Un terminal (Windows : « Terminal » ; Mac : « Terminal »).
- Une clé SSH : `ssh-keygen -t ed25519 -C "aurelien@yeba"` → gardez le fichier `~/.ssh/id_ed25519.pub`
  (c'est la partie publique, à donner au serveur ; l'autre partie ne quitte **jamais** votre ordinateur).
- Le **logiciel PIA de la CNIL** (téléchargement sur cnil.fr) pour les analyses d'impact.

**Documents RGPD à ouvrir dès maintenant** (vous les compléterez au fil de l'eau) :
- Registre des traitements (modèle CNIL).
- Liste des sous-traitants : OVHcloud, Mistral AI, Brevo (+ DPA de chacun).

---

## Étape 1 — Nom de domaine et DNS (30 min)

1. Chez OVHcloud, utilisez votre domaine (ex. `yebaformations.re`) ou achetez-en un.
2. Créez ces sous-domaines (enregistrements **A**) pointant vers l'adresse IP du serveur (vous l'aurez à l'étape 2) :
   `ia`, `auto`, `base`, `coffre`, `statut`.
3. Pour l'envoi d'emails (étape 15) : préparez les enregistrements **SPF**, **DKIM**, **DMARC** que Brevo vous donnera.

---

## Étape 2 — Commander le serveur (15 min)

| Usage | Taille conseillée | Pourquoi |
|---|---|---|
| Votre plateforme (avec transcription locale) | **OVHcloud VPS-3** (8 vCore, 24 Go RAM, 200 Go — caractéristiques d'avant la hausse de 2026, **À VÉRIFIER**) | Whisper a besoin de processeur et de mémoire |
| Kit client sans transcription locale | **VPS-2** (6 vCore, 12 Go) ou **Hetzner CX33** | Suffisant pour n8n + Baserow + Open WebUI |
| Petite commune / TPE | **VPS-1** (4 vCore, 8 Go) | Démarrage ; la transcription passe par l'API Voxtral |

- **Localisation** : un datacenter **en France** (ex. Gravelines, Roubaix, Strasbourg).
- **Système** : **Ubuntu 24.04 LTS**.
- **Clé SSH** : collez votre `id_ed25519.pub` à la commande.
- Depuis La Réunion, la latence vers la France (~180-200 ms) est sans gêne pour ces applications web.
- **Données publiques sensibles** (ex. données sociales du Département) : un VPS classique ne suffit
  pas forcément ; l'acheteur peut exiger un hébergement **qualifié SecNumCloud (ANSSI)** — à poser
  comme question **avant** de chiffrer.

---

## Étape 3 — Première connexion et sécurisation (1 h)

Inspirée des recommandations de l'ANSSI pour les systèmes GNU/Linux.

```bash
# Depuis votre ordinateur (remplacez l'IP)
ssh ubuntu@IP_DU_SERVEUR

# 1. Mises à jour
sudo apt update && sudo apt full-upgrade -y

# 2. Fuseau horaire de La Réunion
sudo timedatectl set-timezone Indian/Reunion

# 3. Créer votre utilisateur d'administration
sudo adduser yeba
sudo usermod -aG sudo yeba
sudo mkdir -p /home/yeba/.ssh
sudo cp ~/.ssh/authorized_keys /home/yeba/.ssh/
sudo chown -R yeba:yeba /home/yeba/.ssh && sudo chmod 700 /home/yeba/.ssh

# 4. Interdire la connexion par mot de passe et la connexion « root »
sudo tee /etc/ssh/sshd_config.d/99-yeba.conf >/dev/null <<'EOF'
PasswordAuthentication no
PermitRootLogin no
KbdInteractiveAuthentication no
EOF
sudo systemctl restart ssh
# ⚠️ AVANT de fermer la session, ouvrez un 2e terminal et vérifiez : ssh yeba@IP_DU_SERVEUR

# 5. Pare-feu : seulement SSH, HTTP, HTTPS
sudo apt install -y ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# 6. Mises à jour de sécurité automatiques
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades

# 7. Mémoire d'appoint (utile pour Whisper)
sudo fallocate -l 4G /swapfile && sudo chmod 600 /swapfile
sudo mkswap /swapfile && sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

> ⚠️ **Docker et le pare-feu** : Docker ouvre lui-même les ports qu'on lui demande de publier, sans passer par `ufw`.
> C'est pourquoi, dans ce guide, **seul Caddy publie des ports (80 et 443)** ; tous les autres services restent internes.

---

## Étape 4 — Installer Docker (15 min)

```bash
# Dépôt officiel Docker pour Ubuntu
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
| sudo tee /etc/apt/sources.list.d/docker.list >/dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker yeba    # puis déconnectez-vous / reconnectez-vous
docker run --rm hello-world     # test
```

---

## Étape 5 — Dossier du projet et secrets (15 min)

```bash
sudo mkdir -p /opt/yeba/{caddy,logs/caddy,backups}
sudo chown -R yeba:yeba /opt/yeba
cd /opt/yeba

# Génère des mots de passe solides
openssl rand -hex 24   # à répéter pour chaque secret ci-dessous
```

Créez `/opt/yeba/.env` (**ne jamais le copier ailleurs ni l'envoyer par email** ; rangez une copie dans Vaultwarden, étape 11) :

```dotenv
DOMAINE=yebaformations.re
EMAIL_ADMIN=contact@yebaformations.re

POSTGRES_USER=n8n
POSTGRES_PASSWORD=__secret_1__
POSTGRES_DB=n8n

N8N_ENCRYPTION_KEY=__secret_2__

# Clé API Mistral (La Plateforme) — ou clé Albert pour une administration
MISTRAL_API_KEY=__votre_cle__

VAULTWARDEN_ADMIN_TOKEN=__secret_3__
```

```bash
chmod 600 /opt/yeba/.env
```

---

## Étape 6 — Caddy (HTTPS automatique) (15 min)

`/opt/yeba/caddy/Caddyfile` (remplacez `yebaformations.re` par votre domaine) :

```caddyfile
{
	email contact@yebaformations.re
}

(journal) {
	log {
		output file /var/log/caddy/access.log {
			roll_size 10mb
			roll_keep 5
		}
		format json
	}
}

ia.yebaformations.re {
	import journal
	reverse_proxy openwebui:8080
}

auto.yebaformations.re {
	import journal
	reverse_proxy n8n:5678
}

base.yebaformations.re {
	import journal
	reverse_proxy baserow:80
}

coffre.yebaformations.re {
	import journal
	reverse_proxy vaultwarden:80
}

statut.yebaformations.re {
	import journal
	reverse_proxy uptime-kuma:3001
}
```

---

## Étapes 7 à 12 — Tous les services en un seul fichier

`/opt/yeba/docker-compose.yml` :

```yaml
services:
  caddy:
    image: caddy:2
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./caddy/Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
      - caddy_config:/config
      - ./logs/caddy:/var/log/caddy

  # Étape 7 — mémoire de n8n
  postgres:
    image: postgres:16
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - pg_data:/var/lib/postgresql/data

  # Étape 7 — automatisations
  n8n:
    image: docker.n8n.io/n8nio/n8n:latest   # en production : figer une version précise
    restart: unless-stopped
    depends_on: [postgres]
    environment:
      DB_TYPE: postgresdb
      DB_POSTGRESDB_HOST: postgres
      DB_POSTGRESDB_DATABASE: ${POSTGRES_DB}
      DB_POSTGRESDB_USER: ${POSTGRES_USER}
      DB_POSTGRESDB_PASSWORD: ${POSTGRES_PASSWORD}
      N8N_HOST: auto.${DOMAINE}
      N8N_PROTOCOL: https
      WEBHOOK_URL: https://auto.${DOMAINE}/
      N8N_ENCRYPTION_KEY: ${N8N_ENCRYPTION_KEY}
      GENERIC_TIMEZONE: Indian/Reunion
      TZ: Indian/Reunion
      N8N_DIAGNOSTICS_ENABLED: "false"
      N8N_PERSONALIZATION_ENABLED: "false"
    volumes:
      - n8n_data:/home/node/.n8n

  # Étape 8 — base de données / CRM
  baserow:
    image: baserow/baserow:latest           # en production : figer une version précise
    restart: unless-stopped
    environment:
      BASEROW_PUBLIC_URL: https://base.${DOMAINE}
    volumes:
      - baserow_data:/baserow/data

  # Étape 9 — assistant IA (interface)
  openwebui:
    image: ghcr.io/open-webui/open-webui:main
    restart: unless-stopped
    environment:
      WEBUI_URL: https://ia.${DOMAINE}
      ENABLE_SIGNUP: "false"
      ENABLE_OLLAMA_API: "false"
      OPENAI_API_BASE_URL: https://api.mistral.ai/v1
      OPENAI_API_KEY: ${MISTRAL_API_KEY}
      SCARF_NO_ANALYTICS: "true"
      DO_NOT_TRACK: "true"
      ANONYMIZED_TELEMETRY: "false"
    volumes:
      - openwebui_data:/app/backend/data

  # Étape 10 — transcription audio locale (aucun son ne sort du serveur)
  whisper:
    image: ghcr.io/speaches-ai/speaches:latest-cpu   # [À VÉRIFIER] nom exact de l'image sur github.com/speaches-ai/speaches
    restart: unless-stopped
    volumes:
      - whisper_cache:/home/ubuntu/.cache/huggingface

  # Étape 11 — coffre-fort de mots de passe
  vaultwarden:
    image: vaultwarden/server:latest
    restart: unless-stopped
    environment:
      DOMAIN: https://coffre.${DOMAINE}
      SIGNUPS_ALLOWED: "false"
      ADMIN_TOKEN: ${VAULTWARDEN_ADMIN_TOKEN}
    volumes:
      - vw_data:/data

  # Étape 12 — supervision
  uptime-kuma:
    image: louislam/uptime-kuma:1
    restart: unless-stopped
    volumes:
      - kuma_data:/app/data

volumes:
  caddy_data:
  caddy_config:
  pg_data:
  n8n_data:
  baserow_data:
  openwebui_data:
  whisper_cache:
  vw_data:
  kuma_data:
```

```bash
cd /opt/yeba
docker compose pull
docker compose up -d
docker compose ps          # tous les services doivent être « running »
docker compose logs -f caddy   # vérifier l'obtention des certificats HTTPS (Ctrl+C pour quitter)
```

### Étape 7 — n8n (30 min)
1. Ouvrez `https://auto.votredomaine` → créez le compte propriétaire (mot de passe long + rangé dans Vaultwarden).
2. Paramètres → activez la **double authentification**.
3. Identifiants (*Credentials*) à créer : **Mistral Cloud** (clé API), **Baserow** (URL `http://baserow` + jeton), **Brevo** (clé API ou SMTP).

### Étape 8 — Baserow (30 min)
1. Ouvrez `https://base.votredomaine` → créez le compte administrateur.
2. Paramètres d'administration → **désactivez l'inscription publique**.
3. Créez un *Database token* pour n8n (lecture/écriture des lignes uniquement).
4. Le dépôt `Training` contient déjà un client Python et un serveur MCP Baserow pour créer les tables depuis Claude Code.

### Étape 9 — Open WebUI + Mistral (45 min)
1. Ouvrez `https://ia.votredomaine` → le **premier compte créé devient administrateur** : créez-le immédiatement.
2. Administration → Connexions : vérifiez que les modèles Mistral apparaissent (l'API Mistral est compatible OpenAI).
3. Administration → Utilisateurs : créez les comptes à la main (l'inscription est fermée).
4. **Bannière de transparence** (IA Act, art. 50) : Administration → Paramètres → Bannières → texte :
   *« Vous utilisez un assistant d'intelligence artificielle. Ses réponses peuvent contenir des erreurs : vérifiez-les. Ne saisissez aucune donnée sensible. »*
5. **Pour une administration** : remplacez l'URL et la clé par celles d'**Albert API** (DINUM) **[URL et conditions À VÉRIFIER auprès de la DINUM]**.
6. Licence : gardez le **logo et le nom « Open WebUI » visibles** (obligatoire au-delà de 50 utilisateurs) ;
   alternative entièrement MIT : **LibreChat**.

### Étape 10 — Transcription locale (30 min)
- Le service `whisper` n'est **pas exposé sur Internet** : seul n8n l'appelle, à l'adresse
  `http://whisper:8000/v1/audio/transcriptions` (format compatible OpenAI).
- Premier appel = téléchargement du modèle (quelques minutes). Modèle conseillé en français sur processeur :
  `Systran/faster-whisper-medium` (plus précis) ou `small` (plus rapide) **[À VÉRIFIER : noms exacts]**.
- Sans serveur assez puissant : utilisez l'**API Voxtral** de Mistral (≈ 0,003 $/minute).
- **Exemple de coût API** : 20 h de réunions par mois × 60 min × 0,003 $ ≈ **3,60 $/mois**.

### Étape 11 — Vaultwarden (20 min)
1. Ouvrez `https://coffre.votredomaine/admin` avec le `VAULTWARDEN_ADMIN_TOKEN` → **invitez** votre adresse email (l'inscription libre reste fermée).
2. Installez l'extension Bitwarden (compatible) sur votre navigateur et votre téléphone → serveur auto-hébergé : `https://coffre.votredomaine`.
3. Rangez-y **tous** les secrets du `.env`, la phrase de passe des sauvegardes et les comptes OVH / Mistral / Brevo.

### Étape 12 — Uptime Kuma (15 min)
1. Ouvrez `https://statut.votredomaine` → compte administrateur.
2. Ajoutez une sonde HTTPS par service (ia, auto, base, coffre) → alerte par email (via Brevo SMTP).

---

## Étape 13 — CrowdSec : bloquer les attaquants (30 min)

```bash
# Installation par le script officiel (vérifiez la commande sur docs.crowdsec.net)
curl -s https://install.crowdsec.net | sudo sh
sudo apt install -y crowdsec crowdsec-firewall-bouncer-iptables
sudo cscli version            # version ≥ 1.7.8 (correctifs de sécurité)

# Lire les journaux de Caddy
sudo cscli collections install crowdsecurity/caddy
sudo tee /etc/crowdsec/acquis.d/caddy.yaml >/dev/null <<'EOF'
filenames:
  - /opt/yeba/logs/caddy/access.log
labels:
  type: caddy
EOF
sudo systemctl restart crowdsec
sudo cscli metrics            # vérifier que les journaux sont lus
```

Dans `/etc/crowdsec/bouncers/crowdsec-firewall-bouncer.yaml`, ajoutez la chaîne **`DOCKER-USER`** à
`iptables_chains` (sinon les blocages ne s'appliquent pas au trafic qui va vers Docker), puis
`sudo systemctl restart crowdsec-firewall-bouncer`.

---

## Étape 14 — Sauvegardes chiffrées (1 h) — *ne sautez jamais cette étape*

1. OVHcloud → **Object Storage** (compatible S3) → créez un conteneur dans un datacenter **différent** de celui du VPS → générez des identifiants S3.
2. Installez restic et préparez le dépôt :

```bash
sudo apt install -y restic
sudo tee /opt/yeba/backups/restic.env >/dev/null <<'EOF'
AWS_ACCESS_KEY_ID=__cle_s3__
AWS_SECRET_ACCESS_KEY=__secret_s3__
RESTIC_REPOSITORY=s3:https://s3.gra.io.cloud.ovh.net/yeba-sauvegardes
RESTIC_PASSWORD=__phrase_de_passe_longue__
EOF
sudo chmod 600 /opt/yeba/backups/restic.env
# [À VÉRIFIER] l'adresse exacte du point d'accès S3 dans votre console OVHcloud
sudo bash -c 'set -a; . /opt/yeba/backups/restic.env; restic init'
```

3. Script `/opt/yeba/backups/sauvegarde.sh` :

```bash
#!/usr/bin/env bash
set -euo pipefail
cd /opt/yeba
set -a; . /opt/yeba/backups/restic.env; set +a
# Base n8n (cohérente, sans arrêt)
docker compose exec -T postgres pg_dump -U n8n n8n > /opt/yeba/backups/n8n.sql
# Baserow : arrêt bref pour une copie cohérente (≈ 1 min, la nuit)
docker compose stop baserow
restic backup /opt/yeba /var/lib/docker/volumes --exclude /opt/yeba/logs
docker compose start baserow
# Garder 7 jours, 4 semaines, 6 mois
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --prune
```

```bash
sudo chmod 700 /opt/yeba/backups/sauvegarde.sh
# Tous les jours à 3 h (heure de La Réunion)
echo "0 3 * * * root /opt/yeba/backups/sauvegarde.sh >> /var/log/yeba-sauvegarde.log 2>&1" | sudo tee /etc/cron.d/yeba-sauvegarde
```

4. **Testez une restauration** dès la première semaine (`restic snapshots`, puis `restic restore latest --target /tmp/test-restauration`). Une sauvegarde jamais restaurée n'est pas une sauvegarde.
5. Rangez `RESTIC_PASSWORD` dans Vaultwarden **et** sur papier dans un coffre : sans elle, les sauvegardes sont illisibles.

---

## Étape 15 — Envoi d'emails (Brevo) (30 min)

1. Brevo → Expéditeurs et domaines → authentifiez votre domaine → copiez **SPF, DKIM, DMARC** dans la zone DNS OVHcloud.
2. Récupérez les paramètres **SMTP** de Brevo → configurez-les dans n8n, Uptime Kuma et Vaultwarden.
3. Prospection : chaque email comporte un **lien de désinscription** et la mention d'information RGPD (voir `README.md`).

---

## Étape 16 — Les automatisations de base (2 à 3 jours, une seule fois)

À construire dans n8n, puis à **exporter en JSON** (Menu → *Download*) pour les réimporter chez chaque client :

| Code | Automatisation | Nœuds n8n |
|---|---|---|
| **A1** | Compte rendu de réunion | *Form Trigger* (dépôt du fichier audio) → *HTTP Request* vers `http://whisper:8000/v1/audio/transcriptions` → *Mistral Cloud Chat Model* (consigne « compte rendu : décisions, actions, responsables, échéances ») → *Baserow* (archive) → *Send Email* |
| **A2** | Parcours stagiaire (Qualiopi) | *Form Trigger* (inscription) → *Baserow* (ligne stagiaire) → *Brevo* (convocation) → *Wait* J-1 (rappel) → *Wait* J+1 (enquête de satisfaction) → *Wait* J+60 (enquête d'impact « avez-vous mis en œuvre ? ») → *Baserow* (indicateurs) |
| **A3** | Rapport d'indicateurs hebdomadaire | *Schedule Trigger* (lundi 7 h) → *Baserow* (lecture) → *Code* (calculs) → *Mistral* (synthèse en 10 lignes) → *Send Email* au commanditaire |
| **A4** | Chatbot public transparent | *Chat Trigger* (widget intégrable au site) → *AI Agent* + *Mistral* + documents **publics** uniquement → message d'accueil obligatoire « Vous échangez avec un assistant automatique » → bouton « parler à un agent » |
| **A5** | Réécriture en FALC (Facile à lire et à comprendre) | *Form Trigger* (texte) → *Mistral* (consigne FALC) → relecture humaine obligatoire → *Send Email* |
| **A6** | Prospection B2B maîtrisée | *Baserow* (prospects) → *Mistral* (brouillon personnalisé) → **validation humaine** → *Brevo* (envoi avec désinscription) → *Baserow* (statut) |

> Les consignes (*prompts*) de chaque automatisation sont données dans `00-catalogue-ia-et-solutions.md`.

---

## Étape 17 — Conformité (1 jour, puis à chaque nouveau client)

1. **Registre des traitements** : une fiche par automatisation (finalité, données, durée, destinataires).
2. **Sous-traitants** : DPA signés avec OVHcloud, Mistral AI, Brevo ; vous-même êtes **sous-traitant (art. 28)** de vos clients → contrat de sous-traitance avec chacun.
3. **Analyse d'impact (AIPD)** avec le logiciel PIA de la CNIL dès qu'il y a données sensibles (santé, handicap, données sociales) ou personnes vulnérables.
4. **Information des personnes** : mention sur chaque formulaire ; information préalable avant tout enregistrement de réunion.
5. **IA Act** : tenez une **cartographie des usages IA** (table Baserow) avec, pour chacun, la catégorie : interdit / haut risque (annexe III, applicable au 02/12/2027) / transparence (art. 50, applicable depuis le 02/08/2026) / risque minimal. **Aucune décision automatisée sur des personnes** (sélection, notation, orientation) dans vos solutions.
6. **Durées de conservation** : par exemple journaux techniques 6 mois, comptes rendus selon la politique du client, prospects 3 ans après le dernier contact.

---

## Étape 18 — Recette (½ journée)

- [ ] Les 5 adresses répondent en HTTPS (cadenas) ; `whisper` n'est **pas** accessible depuis Internet.
- [ ] Connexion SSH par mot de passe refusée.
- [ ] `sudo cscli metrics` montre des journaux lus.
- [ ] Une restauration de sauvegarde a été testée.
- [ ] Double authentification active partout (OVH, Mistral, Brevo, n8n, Vaultwarden).
- [ ] La bannière IA s'affiche dans Open WebUI.
- [ ] A1 à A6 testées avec des **données fictives**.

---

## Étape 19 — Exploitation (1 h par mois)

```bash
cd /opt/yeba
docker compose pull && docker compose up -d     # mises à jour des services (après lecture des notes de version)
docker image prune -f
sudo apt update && sudo apt full-upgrade -y
```
- Chaque mois : revue des comptes utilisateurs, lecture des alertes Uptime Kuma et CrowdSec, contrôle des sauvegardes.
- Chaque trimestre : test de restauration, revue du registre et de la cartographie IA.

---

## Étape 20 — Répliquer chez un client (le « kit client »)

1. **Le client loue son propre VPS** (à son nom, sa carte bancaire) et sa **propre clé Mistral** (ou Albert).
   → Les données et les coûts sont les siens ; vous êtes prestataire. C'est aussi la lecture la plus sûre
   de la licence n8n : les sources disponibles indiquent qu'**une instance hébergée par vous pour plusieurs
   clients** serait considérée comme « n8n proposé en service » (licence commerciale nécessaire). Si vous
   tenez à mutualiser, utilisez **Activepieces** (édition communautaire sous licence MIT).
2. Vous refaites les étapes 1 à 15 sur son serveur (≈ 1 journée avec l'habitude).
3. Vous **importez** les automatisations JSON (A1 à A6) et vous les adaptez.
4. Vous livrez : le dossier de documentation, les accès administrateur au client, le registre et la cartographie IA complétés, la charte d'usage.
5. Option : contrat de maintenance mensuel (étape 19) avec un accès que le client peut révoquer.

---

## Budget mensuel indicatif (hors votre temps)

| Poste | Votre plateforme | Kit client type |
|---|---|---|
| Serveur | VPS-3 ≈ 23,50 $ **[À VÉRIFIER]** | VPS-1 7,79 € à VPS-2 ≈ 11,75 $ |
| API Mistral | quelques euros (ex. 1 000 requêtes × 2 000 tokens en entrée et 500 en sortie avec Mistral Small 4 ≈ **0,60 $**) | idem, selon l'usage |
| Transcription | 0 (locale) | Voxtral ≈ 0,003 $/minute si non locale |
| Emails | Brevo gratuit (300/jour) | idem |
| Stockage des sauvegardes | **À VÉRIFIER** (Object Storage OVH) | idem |

---

## Sources
- Hausse des VPS OVHcloud 2026 — extrait de [next.ink](https://next.ink/225720/ovhcloud-augmente-fortement-le-prix-de-ses-vps-2026-et-ipv4/) ; prix VPS-2/VPS-3 — [lowendtalk.com](https://lowendtalk.com/discussion/comment/4739653) ; anciennes caractéristiques — [vpsbenchmarks.com](https://www.vpsbenchmarks.com/hosters/ovhcloud)
- Hetzner juin 2026 — extrait de [wz-it.com](https://wz-it.com/en/blog/hetzner-price-increase-june-2026-cpx-ccx-alternatives/)
- Prix Mistral API et Voxtral — extrait de [mistral.ai/pricing](https://mistral.ai/en/pricing) et [curlscape.com](https://curlscape.com/blog/mistral-api-pricing-2026)
- Le Chat / version gratuite et entraînement — extrait de [tech-insider.org](https://tech-insider.org/fr/mistral-vibe-gratuit-entrainement-ia-donnees-2026/) et [donneespersonnelles.fr](https://www.donneespersonnelles.fr/mistral-rgpd)
- Licence n8n — extrait de [nordflux.de](https://nordflux.de/en/guides/n8n-sustainable-use-license-erklaert) et [community.n8n.io](https://community.n8n.io/t/can-i-use-n8n-cloud-to-manage-workflows-for-multiple-consulting-clients/236130?tl=fr)
- Licence Open WebUI — extrait de [docs.openwebui.com/license](https://docs.openwebui.com/license/)
- Activepieces (MIT) — extrait de [automationatlas.io](https://automationatlas.io/answers/activepieces-review-2026/)
- Albert / DINUM — extrait de [banquedesterritoires.fr](https://www.banquedesterritoires.fr/albert-mode-demploi-lacces-des-collectivites-lia-de-letat-precise) et [next.ink](https://next.ink/brief_article/albert-lia-souveraine-de-la-dinum-ne-sera-pas-generalisee-dans-sa-forme-actuelle/)
- CrowdSec — extrait de [linuxfr.org](https://linuxfr.org/news/crowdsec-la-cybersecurite-collaborative-open-source-et-gratuite-pour-linux) et [it-connect.fr](https://it-connect.fr/reverse-proxy-traefik-integration-de-crowdsec-pour-bloquer-les-attaques/)
- Logiciel PIA — extrait de [cnil.fr](https://www.cnil.fr/fr/PIA-privacy-impact-assessment)
- Brevo — extrait de [emailtooltester.com](https://www.emailtooltester.com/en/reviews/brevo/pricing/)
- Baserow Premium — extrait de [getapp.com](https://getapp.com/sales-software/a/baserow/)
- Voxtral (licences) — extrait de [mistral.ai](https://mistral.ai/fr/news/voxtral-transcribe-2)
