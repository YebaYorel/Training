# Emploi et recrutement

LinkedIn, Boss Zhipin (site d'emploi chinois).

> ⚠️ **Règles YEBA — RGPD + IA Act** : consulter des profils de personnes =
> traitement de données personnelles (RGPD : finalité, base légale,
> minimisation, information des personnes). Utiliser ces données pour trier,
> noter ou présélectionner des candidats relève potentiellement de l'**IA Act,
> annexe III (emploi) = haut risque** : le signaler systématiquement.
> Les CGU de LinkedIn interdisent l'extraction automatisée : accord explicite
> d'Aurélien requis avant tout usage.

## LinkedIn

```bash
# Récupérer un profil
mcporter call linkedin.get_person_profile linkedin_username="username" sections="experience,education"

# Rechercher des personnes
mcporter call linkedin.search_people keywords="AI engineer" location="La Réunion"

# Récupérer une fiche entreprise
mcporter call linkedin.get_company_profile company_name="openai" sections="posts,jobs"

# Rechercher des offres d'emploi
mcporter call linkedin.search_jobs keywords="software engineer" location="Remote" max_pages=2
```

> **Connexion requise** : avant la première utilisation, lancer
> `uvx mcp-server-linkedin@latest --login` pour enregistrer une session valide.

### Solution de repli

Si le MCP n'est pas disponible, utiliser Jina Reader :

```bash
curl -s "https://r.jina.ai/https://linkedin.com/in/username"
```

## Boss Zhipin

Quand l'utilisateur demande « configure Boss Zhipin », suivre cette section :
installation, lancement d'un Chrome dédié, attente de la connexion manuelle par
l'utilisateur, vérification finale. Ne pas lui imposer d'emblée les détails
techniques (port 9222…), et ne jamais saisir à sa place identifiants, QR code
ou captcha à glissière.

> **Distinction clé : page de connexion ≠ contrôle anti-robot.** Sur
> zhipin.com on peut arriver sur trois pages : `web/geek/job` (connecté),
> `web/user/` (non connecté : QR code / téléphone), ou une **page de contrôle
> de sécurité** anti-robot (URL contenant `security-check` / `zhipin-security`
> / `_security_check`). Cette dernière n'a rien à voir avec la connexion : **elle
> apparaît même connecté** (quasi systématique avec un Chrome ayant un port de
> débogage CDP). Ne jamais déduire l'état de connexion de l'URL.

> **Deux stockages de session (en mode CDP strict existing-browser, c'est le
> navigateur qui fait foi).** Les deux sont nécessaires, **ne jamais les
> supprimer**, mais ils authentifient des canaux différents :
>
> | Stockage | Rôle |
> |---|---|
> | `~/.boss-agent/auth/session.enc` | ① Prérequis obligatoire : `_get_browser()` appelle toujours `get_token()` ; s'il est illisible → `AuthRequired`, et la recherche CDP échoue avant même de se connecter au navigateur ; ② ce **n'est pas** l'identifiant utilisé pour la recherche : en CDP (réutilisation de `contexts[0]` du vrai Chrome), ses cookies ne sont injectés que dans la branche « sans contexte », donc jamais appliqués ; ③ le canal httpx (opérations à faible risque : `status`/`detail`/`cities`/`job_card_httpx`) utilise réellement ses cookies + stoken, et `force_refresh()` (code 37) le réécrit |
> | Cookies du profil Chrome dédié | Identifiants réellement utilisés en CDP pour les opérations sensibles (search/greet…) |
>
> **`boss status` / `status --live` ne vérifient que session.enc** — même
> `logged_in: true` ne prouve pas que le navigateur CDP est connecté. Donc :
> 1. Après le lancement du Chrome dédié, **faire une pause et demander à
>    l'utilisateur de confirmer visuellement** qu'il est connecté (avatar en
>    haut à droite) avant toute recherche ;
> 2. la ligne boss de `doctor` teste directement la présence du cookie `wt2`
>    dans le navigateur : c'est elle qui fait foi ;
> 3. **`AUTH_EXPIRED` est la vérité terrain** : si la recherche le renvoie,
>    passer directement à la procédure de connexion (connexion dans la fenêtre
>    dédiée → `login --cdp`), sans l'interpréter comme un contrôle de sécurité ;
>    la page `_security_check` ne se traite (captcha) qu'en l'absence d'`AUTH_EXPIRED` ;
> 4. ne pas supprimer session.enc pour « nettoyer » ; pour le rafraîchir,
>    lancer `login --cdp`.

> **Dépendances** : l'API CDP stricte publique vient des PR #403–#407 de
> boss-agent-cli (fusionnées en amont). L'installateur Agent Reach est épinglé
> sur le commit amont `4c991b77086a203173bf08a4cb64a23af6514fe6` et non sur une
> branche mobile ; à remplacer par une contrainte de version à la sortie d'une
> version officielle.

Diagnostic (sans effet de bord, sans recherche) :

```bash
agent-reach doctor          # ligne boss : off = non installé ou CDP injoignable ; warn = chaîne prête,
                            # le message indique si le cookie wt2 est présent dans le navigateur (il fait foi)
```

Recherche + fiche de poste via l'API publique (`browser_source` /
`job_card_browser` / `JobItem.lid`). Comme pipx/uv tool sont isolés, un
`python` ordinaire ne peut pas forcément importer l'outil installé ; utiliser
`uv run --with` pour avoir le script et les dépendances épinglées dans le même
interpréteur :

```bash
uv run --isolated --no-project \
  --with 'git+https://github.com/can4hou6joeng4/boss-agent-cli.git@4c991b77086a203173bf08a4cb64a23af6514fe6' \
  python - <<'PY'
from pathlib import Path

from boss_agent_cli.api.client import AccountRiskError, BossClient, EnvironmentRiskError
from boss_agent_cli.auth.manager import AuthManager
from boss_agent_cli.platforms.zhipin import BossPlatform

auth = AuthManager(Path.home() / ".boss-agent")

# Mode CDP strict : réutilise le navigateur connecté, erreur immédiate si CDP échoue, jamais headless
with BossClient(
    auth,
    cdp_url="http://localhost:9222",
    browser_source="existing-browser",
) as boss:
    raw = boss.search_jobs("大模型", city="深圳", page=1)  # « grand modèle » à Shenzhen
    if raw.get("code") != 0:
        code, message = BossPlatform(boss).parse_error(raw)
        raise RuntimeError(f"{code}: {message}")
    items = raw.get("zpData", {}).get("jobList", [])
    for item in items:
        card = boss.job_card_browser(item["securityId"], item["lid"])
        post_desc = card.get("zpData", {}).get("jobCard", {}).get(
            "postDescription", ""
        )
        print(item.get("jobName"), post_desc)

# AccountRiskError / EnvironmentRiskError → arrêt immédiat, pas de nouvel essai automatique ;
# un code 37 indiquant clairement l'expiration du token/stoken est rafraîchi et réessayé une seule fois par BossClient.
PY
```

### Diagnostic et remise en état (à vérifier avant toute collecte)

Si avant une recherche `agent-reach doctor` indique boss en `off` ou `warn`,
suivre cette procédure, sans deviner en lisant le code source :

1. **Le port CDP répond-il ?**
   ```bash
   curl -s http://localhost:9222/json/version   # champ Browser présent = port OK
   ```

2. **Chrome de débogage non lancé / fermé** : lancer le Chrome dédié selon le
   système (session indépendante, sans toucher au navigateur habituel) :
   ```bash
   # macOS
   open -na "Google Chrome" --args --remote-debugging-address=127.0.0.1 \
     --remote-debugging-port=9222 --user-data-dir="$HOME/.boss-chrome-profile" \
     "https://www.zhipin.com/web/geek/job"

   # Linux
   google-chrome --remote-debugging-address=127.0.0.1 \
     --remote-debugging-port=9222 --user-data-dir="$HOME/.boss-chrome-profile" \
     "https://www.zhipin.com/web/geek/job"
   ```

   Windows PowerShell :
   ```powershell
   Start-Process chrome.exe -ArgumentList '--remote-debugging-address=127.0.0.1','--remote-debugging-port=9222',"--user-data-dir=$env:USERPROFILE\.boss-chrome-profile",'https://www.zhipin.com/web/geek/job'
   ```

   Écouter uniquement sur l'adresse locale (127.0.0.1). Tout processus ayant
   accès au port 9222 contrôle entièrement ce Chrome : ne jamais l'exposer sur
   le réseau. Réutiliser durablement ce profil dédié pour garder une session
   stable ; ne pas le supprimer/recréer à chaque fois, ni basculer par défaut
   sur le Chrome personnel. Fermer la fenêtre dédiée quand elle ne sert pas.

   **Première étape après le lancement : pause, et confirmation visuelle par
   l'utilisateur qu'il est connecté (avatar en haut à droite).** Ne pas
   remplacer cette étape par `boss status`, qui ne vérifie que session.enc.

3. **Connexion manuelle par l'utilisateur (si le navigateur n'est pas
   connecté)** : se fier d'abord au test de cookie de doctor (pas de wt2 =
   non connecté), puis à la confirmation visuelle ; `boss status` n'est
   qu'indicatif. L'utilisateur se connecte ou scanne le QR code dans la fenêtre
   dédiée. Une fois confirmé, enregistrer la session CDP :
   ```bash
   boss --cdp-url http://localhost:9222 login --cdp
   ```

   Si la fenêtre reste sur une page de contrôle de sécurité
   (`security-check` / `zhipin-security`), c'est un défi anti-robot, pas une
   page de connexion : attendre la validation automatique ou laisser
   l'utilisateur passer le captcha, sans relancer une connexion par QR code.

4. **La session est-elle valide ?** (test du cookie navigateur + expiration du stoken)
   ```bash
   agent-reach doctor     # voir le résultat du test du cookie wt2 dans le message de la ligne boss
   boss status            # reflète uniquement session.enc, indicatif
   ```

5. **Traitement des codes d'erreur** (recherche / fiche de poste) :
   - `AUTH_EXPIRED` (utilisateur non connecté) → **vérité terrain** : le
     navigateur CDP n'est pas connecté (quoi que dise `boss status`) ; passer à
     l'étape 3 + `login --cdp`, sans parler de contrôle de sécurité ;
   - code 36 (ACCOUNT_RISK) → arrêt immédiat, traitement manuel sur le site
     BOSS, pas de nouvel essai automatique ;
   - code 9 (RATE_LIMITED) → attendre, puis réessayer ;
   - code 37 + message `环境存在异常` (« anomalie d'environnement ») →
     `ENVIRONMENT_RISK` : arrêt immédiat, pas de rafraîchissement de token, pas
     de reconnexion, pas de nouvel essai ;
   - seul un code 37 dont le message indique clairement l'expiration du
     token/stoken est un `TOKEN_REFRESH_FAILED` ; le client rafraîchit et
     réessaie une seule fois, puis reconnexion si l'échec persiste.

Quand l'utilisateur demande de lancer la recherche, l'agent doit imposer le mode
CDP strict (options globales avant la sous-commande) :

```bash
boss --browser-source existing-browser --cdp-url http://localhost:9222 search "大模型" --city 广州 --page 1   # « grand modèle » à Canton (le site attend du chinois)
```

Ne pas enchaîner les pages sans prévenir. Tant que la PR #383 de
boss-agent-cli (budget persistant de 5 à 10 s entre recherches) n'est pas
publiée, l'agent doit lui-même espacer et sérialiser les appels.

> **L'attente est normale, ce n'est pas un blocage** : en cas de limitation,
> boss-agent-cli attend silencieusement 5 à 10 s (message visible seulement en
> terminal interactif ; Agent Reach appelle avec `--json` et ne le voit pas).
> Pendant l'attente : ne pas réessayer, ne pas lancer un nouveau navigateur,
> ne pas changer de profil.
