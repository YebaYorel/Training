# Durcissement du site — configuration à appliquer

> ⚠️ **Ce document ne remplace pas un audit du code.** Il couvre la couche
> serveur et les défauts de configuration, qui représentent l'essentiel des
> failles réellement exploitées sur les sites vitrines. L'audit du code lui-même
> demande le code — voir `../AUDIT-DESIGN.md`, section « ce qu'il me manque ».

## 1. Les en-têtes HTTP — le socle

| En-tête | Rôle | Sans lui |
|---|---|---|
| `Content-Security-Policy` | Restreint les sources de scripts, styles, images | Une injection XSS s'exécute librement |
| `Strict-Transport-Security` | Impose HTTPS pour 2 ans | Interception possible sur wifi public |
| `X-Content-Type-Options` | Empêche la réinterprétation de type | Un fichier uploadé peut être exécuté |
| `Referrer-Policy` | Limite la fuite d'URL vers les tiers | Vos URL internes fuitent |
| `Permissions-Policy` | Coupe caméra, micro, géolocalisation | Une iframe compromise peut les demander |
| `X-Frame-Options` | Interdit l'affichage en cadre | Clickjacking sur vos formulaires |
| `Cross-Origin-Opener-Policy` | Isole le contexte de navigation | Fuites entre onglets |

### Apache — `.htaccess`

```apache
<IfModule mod_headers.c>
  Header always set Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'; upgrade-insecure-requests"
  Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
  Header always set X-Content-Type-Options "nosniff"
  Header always set X-Frame-Options "DENY"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()"
  Header always set Cross-Origin-Opener-Policy "same-origin"
  Header always set Cross-Origin-Resource-Policy "same-origin"
  # Ne jamais annoncer la version du serveur ni la pile technique
  Header always unset X-Powered-By
  Header always unset Server
</IfModule>

# HTTPS obligatoire
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteCond %{HTTPS} !=on
  RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
</IfModule>

# Interdire l'accès aux fichiers sensibles
<FilesMatch "(^\.|composer\.(json|lock)|package(-lock)?\.json|\.env|\.git|\.sql|\.bak|\.old|~)$">
  Require all denied
</FilesMatch>

# Pas d'indexation de répertoire
Options -Indexes

ServerSignature Off
```

### Nginx

```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'; upgrade-insecure-requests" always;
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=()" always;
add_header Cross-Origin-Opener-Policy "same-origin" always;

server_tokens off;

location ~ /\.(?!well-known) { deny all; }
location ~* \.(sql|bak|old|log|env)$ { deny all; }
```

> **La CSP est volontairement stricte : `'self'` partout, aucun
> `'unsafe-inline'`.** Cela impose deux choses au site : les polices sont
> hébergées chez toi (bénéfice RGPD au passage, aucun transfert d'IP vers un
> tiers), et aucun style ni script écrit directement dans le HTML.
>
> Si un générateur de site produit du style en ligne, **ne relâche pas la CSP
> avec `'unsafe-inline'`** : cela annule l'essentiel de sa protection. Utilise
> un `nonce` par requête, ou sors les styles dans un fichier.

## 2. Vérifier après mise en ligne

| Outil | Ce qu'il vérifie |
|---|---|
| `securityheaders.com` | Les en-têtes ci-dessus. Cible : note **A** minimum |
| `ssllabs.com/ssltest` | Configuration TLS. Cible : note **A** |
| `observatory.mozilla.org` | Vue d'ensemble |
| `wave.webaim.org` | Accessibilité |
| Lighthouse (Chrome) | Performance, accessibilité, SEO |

Commande de contrôle en ligne de commande :

```bash
curl -sSI https://yebaformations.re | grep -iE 'content-security|strict-transport|x-content-type|x-frame|referrer|permissions'
```

## 3. Formulaires — les cinq protections indispensables

Ce sont les points d'entrée réels d'un site vitrine. Par ordre d'importance :

1. **Jeton anti-CSRF** — un jeton aléatoire par session, vérifié à la
   soumission. Sans lui, un tiers peut faire soumettre le formulaire à un
   visiteur à son insu.
2. **Validation côté serveur** — la validation HTML est un confort pour
   l'utilisateur, jamais une sécurité : elle se contourne en trois secondes.
   Tout champ est revalidé côté serveur : type, longueur maximale, format.
3. **Échappement à l'affichage** — toute donnée saisie qui est réaffichée
   (page de confirmation, courriel de notification) doit être échappée. C'est
   la faille XSS classique, et elle passe très souvent par le courriel de
   notification que tu reçois toi-même.
4. **Limitation de débit** — maximum 5 soumissions par adresse IP et par
   10 minutes. Sans cela, ta boîte est noyée sous le spam en une semaine.
5. **Piège à robots** — un champ caché ; s'il est rempli, la soumission est
   silencieusement rejetée. **Préférable à un CAPTCHA tiers**, qui transmet
   l'adresse IP de tes visiteurs hors UE et nécessite un consentement.

**Ne jamais injecter une donnée saisie dans un en-tête de courriel** (champs
`From`, `Reply-To`, `Subject`) sans filtrage strict des retours à la ligne :
c'est la faille d'injection d'en-tête, qui transforme ton formulaire en relais
de spam et fait blacklister ton domaine.

## 4. Courriel — protéger ton domaine de l'usurpation

Sans ces trois enregistrements DNS, n'importe qui peut envoyer un courriel qui
paraît venir de `contact@yebaformations.re`. Pour quelqu'un qui vend de la
cybersécurité, c'est une faille difficile à assumer.

```dns
; SPF — qui a le droit d'envoyer pour ce domaine
yebaformations.re.  TXT  "v=spf1 include:[[SPF_HEBERGEUR]] -all"

; DMARC — que faire des messages non conformes
_dmarc.yebaformations.re.  TXT  "v=DMARC1; p=quarantine; rua=mailto:dmarc@yebaformations.re; pct=100; adkim=s; aspf=s"

; DKIM — signature cryptographique, clé fournie par l'hébergeur de messagerie
[[SELECTEUR]]._domainkey.yebaformations.re.  TXT  "v=DKIM1; k=rsa; p=[[CLE_PUBLIQUE]]"
```

Démarre en `p=quarantine`, surveille les rapports pendant un mois, puis passe en
`p=reject`. Ajoute aussi un enregistrement **CAA** pour restreindre les
autorités de certification autorisées à émettre un certificat pour ton domaine.

## 5. Sauvegardes — la règle 3-2-1

Trois copies, sur deux supports différents, dont une hors site.

**Et le point que tout le monde saute : tester la restauration.** Une sauvegarde
jamais restaurée n'est pas une sauvegarde, c'est une hypothèse. Teste une
restauration complète **avant** la mise en ligne, puis tous les six mois.

## 6. Ce qui ne doit jamais être mis en ligne

- `.env`, `.git/`, sauvegardes `.sql`, fichiers `.bak` et `~`
- clés d'API en clair dans le code source ou dans le HTML
- pages d'administration accessibles sans authentification forte
- messages d'erreur détaillés affichant chemins, versions ou requêtes
- comptes de test avec mots de passe par défaut

**Vérification :** `https://yebaformations.re/.git/config` doit renvoyer une
erreur 403 ou 404. Si le fichier s'affiche, tout ton historique de code est
public — et avec lui, tous les secrets qui y ont jamais transité.

## 7. Priorisation honnête

Si tu ne fais que trois choses avant la mise en ligne :

1. **HTTPS forcé + HSTS** — sans quoi tout le reste est théorique.
2. **SPF, DKIM, DMARC** — protège ta réputation et ta délivrabilité.
3. **Formulaire : validation serveur, échappement, limitation de débit.**

La CSP et les autres en-têtes viennent juste après. Le reste est du confort.
