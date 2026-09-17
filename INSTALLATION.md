# YEBA — installation et reprise du projet

Document destiné à toute personne qui reprend ce code. Il dit ce qui existe,
ce qui n'existe pas, et comment lancer l'ensemble.

## Avertissement à lire avant de coder

**Il n'y a pas de couche serveur dans ce dépôt.** Ni API, ni base applicative,
ni module d'authentification. Le site est **100 % statique** : du HTML, du CSS
et du JavaScript exécutés dans le navigateur du visiteur.

Ce n'est pas un oubli, c'est le choix d'architecture. Il est détaillé dans
« Où est la sécurité » ci-dessous. Ne cherchez pas un dossier `server/` ou
`api/` : il n'y en a pas, et en ajouter un change la position juridique du
projet.

## Dépôt

```
https://github.com/YebaYorel/Training
branche : claude/sharp-mccarthy-4lskdp
```

Le dépôt appartient au compte **YebaYorel**. Pour donner accès à un
prestataire : GitHub → Settings → Collaborators → Add people, en **lecture**
d'abord. Ne transmettez jamais vos identifiants GitHub : la collaboration se
fait par invitation nominative, révocable.

```bash
git clone https://github.com/YebaYorel/Training.git
cd Training
git checkout claude/sharp-mccarthy-4lskdp
```

## Arborescence

```
site/
  index.html              vitrine d'une page — première version, conservée
  build.py                Airtable → JSON + module JS (filtres contractuels)
  data/formations.json    catalogue extrait, lisible tel quel
  logo-yeba-sans-oeil.svg logo officiel, version du 09/09/2026
  app/                    ◄── L'APPLICATION EN SERVICE
    index.html            structure, en-tête, pied de page, assistant, cookies
    styles.css            charte, thèmes clair et sombre, animations
    contenu.js            TOUT le texte éditorial
    formations.js         catalogue GÉNÉRÉ — ne jamais éditer à la main
    app.js                routeur, transitions, filtres, assistant, consentement
    scene.js              scène animée du héros (canvas)

migration/
  airtable_vers_baserow.py   migration par API, conserve les liens
  export_csv.py              export CSV, sans identifiants Baserow
  simulateur.py              rejoue la migration à blanc, sans rien écrire
  schema-airtable.json       schéma des 19 tables, 517 champs
  ia-generative-baserow.md   connecter un modèle d'IA à Baserow
  README.md                  le blocage rencontré et sa résolution

baserow/                     client Python et interface en ligne de commande
baserow_mcp_server.py        serveur MCP : 13 outils Baserow pour Claude Code
.claude/setup.sh             prépare l'environnement Python au démarrage
.claude/settings.json        déclenche setup.sh à chaque session
.mcp.json                    déclaration du serveur MCP
```

## Lancer le site — deux minutes

Aucune dépendance, aucune compilation, aucun `npm install`.

```bash
cd site/app
python3 -m http.server 8000
```

Puis ouvrir `http://localhost:8000`.

**Un serveur local est indispensable** : la page charge des modules
JavaScript (`import`), que les navigateurs refusent depuis un fichier ouvert
en `file://`. N'importe quel serveur statique convient.

### Mise en production

Déposer le contenu de `site/app/` sur n'importe quel hébergement statique.
Rien d'autre à configurer.

**Contrainte d'hébergement** : votre `CONFIG SYSTEME` exige « un prestataire
non soumis à une législation d'accès extraterritorial ». L'hébergeur doit donc
être européen et hors CLOUD Act — OVHcloud, Scaleway, Infomaniak, Hetzner.
Un hébergement américain contredirait le discours du site lui-même.

## Lancer les outils de migration

```bash
pip install --ignore-installed PyJWT -r requirements.txt
cp .env.example .env     # puis renseigner, voir ci-dessous
```

Si l'installation échoue sur `PyJWT`, c'est le conflit Debian connu :
`.claude/setup.sh` le contourne, lancez-le.

```bash
python migration/export_csv.py --sans-donnees-perso   # export CSV
python migration/airtable_vers_baserow.py --plan      # migration, à blanc
python site/build.py --check                          # catalogue, à blanc
```

Tous ces scripts ont un mode qui **n'écrit rien**. Utilisez-le en premier.

## Variables d'environnement

Elles vivent dans `.env`, à la racine. **Ce fichier est ignoré par Git et ne
doit jamais y entrer.** Le modèle est `.env.example`.

| Variable | Où l'obtenir | Portée |
|---|---|---|
| `AIRTABLE_TOKEN` | airtable.com/create/tokens — **lecture seule** | Lire la base source |
| `BASEROW_API_URL` | `https://api.baserow.io` | — |
| `BASEROW_EMAIL` | compte de service dédié, rôle Builder | Créer tables et champs (JWT) |
| `BASEROW_PASSWORD` | idem | idem |
| `BASEROW_TOKEN` | Baserow → paramètres de la base → jetons | Lire et écrire des lignes |
| `BASEROW_WORKSPACE_ID` | visible dans l'URL Baserow | Cible de la migration |

### Comment les transmettre

**Jamais par messagerie instantanée, jamais par courriel.** Un message reste
sur les serveurs du service, dans les sauvegardes, et sur le téléphone de
chaque participant.

Trois voies acceptables :

1. **Le prestataire crée ses propres identifiants.** Le meilleur cas : rien à
   transmettre. Créez-lui un compte de service Baserow nominatif et un jeton
   Airtable en lecture seule, qu'il configure lui-même.
2. **Un gestionnaire de mots de passe** avec partage (Bitwarden, 1Password,
   Dashlane). Le secret n'est jamais en clair dans une conversation.
3. **Un lien à usage unique et expiration courte** (`onetimesecret.com` ou
   équivalent auto-hébergé), transmis séparément du contexte.

Dans tous les cas : **un jeu d'identifiants par personne**, pour pouvoir
révoquer l'accès de l'un sans casser celui des autres.

## Où est la sécurité, puisqu'il n'y a pas de serveur

C'est la question centrale, et la réponse tient en une phrase : **la sécurité
vient de ce que le site ne fait pas.**

| Risque habituel | Pourquoi il n'existe pas ici |
|---|---|
| Fuite de clé d'API | Aucune clé n'est présente dans la page. `site/build.py` lit Airtable **sur votre poste**, à la génération ; le visiteur ne contacte jamais Airtable. |
| Injection SQL | Aucune base interrogée depuis le navigateur. |
| XSS | Toute donnée insérée via `innerHTML` passe par `esc()` — `site/app/app.js`, en haut du fichier. La seule saisie du visiteur (l'assistant) y passe aussi. |
| Fuite de données personnelles | Le formulaire n'envoie rien à un serveur : il compose un courriel local (`mailto:`). Aucune collecte, donc aucun traitement à déclarer. |
| Traceurs, mesure d'audience | Aucun. Aucune police distante, aucun script tiers, aucun appel réseau sortant. |
| Compromission de serveur | Il n'y a pas de serveur applicatif à compromettre. |

Les deux contrôles qui protègent l'entreprise sont dans **`site/build.py`**,
fonctions `filtrer()` et `controler()` :

- **Filtre de marque blanche** — liste blanche sur le champ
  `Marque / Confidentialité contractuelle`. Seules `Catalogue YEBA` et
  `Client direct` sont publiées. Toute autre valeur, y compris vide ou
  nouvelle, est exclue. Les fiches FOR-0005 et FOR-0007 sont sous contrat de
  sous-traitance interdisant toute mention de YEBA : les publier serait une
  violation contractuelle. **Ne jamais convertir ce filtre en liste noire.**
- **Contrôle d'éligibilité au CPF** — la génération échoue si une fiche
  affirme une éligibilité. Aucune formation ne porte de code RNCP ou RS :
  l'annoncer serait une pratique commerciale trompeuse (code de la
  consommation, art. L.121-2).

**Ces deux contrôles sont la couche de sécurité métier du projet.** Toute
évolution qui court-circuite `build.py` — édition directe de `formations.js`,
autre source de données — les désactive.

## Si vous ajoutez une couche serveur

Un backend devient nécessaire pour : un formulaire qui enregistre, un
assistant à modèle de langage, un espace stagiaire, une mesure d'audience.

Chacun de ces ajouts **crée un traitement de données personnelles** là où il
n'y en a aucun aujourd'hui. Sont alors requis :

- une finalité, une base légale et une durée de conservation ;
- une inscription au registre des traitements (art. 30) ;
- une mention d'information mise à jour (art. 13) ;
- un hébergement dans l'Union européenne ;
- un accord de sous-traitance avec chaque prestataire (art. 28).

Le fichier `site/app/README.md` détaille la voie recommandée pour l'assistant :
un proxy minimal en UE devant Mistral ou Scaleway, jamais une clé d'API dans
la page.

## État du projet

**Fait et vérifié** : application à huit pages, catalogue généré depuis la
source avec les deux contrôles bloquants, mentions légales et politique de
confidentialité, assistant local, gestion du consentement, accessibilité
(police Atkinson Hyperlegible, contrastes de la charte, `prefers-reduced-motion`),
outils de migration éprouvés contre un simulateur.

**Non fait, et pourquoi** :

| Point | Motif |
|---|---|
| Photographie du dirigeant | Non fournie. Emplacement en attente sur la page « À propos », marche à suivre dans `site/app/README.md`. |
| Six mentions légales | Forme juridique, capital social, RCS, TVA intracommunautaire, hébergeur, médiateur de la consommation. Signalées en jaune dans la page. Le médiateur est une obligation dès qu'un particulier finance lui-même une formation (art. L.612-1). |
| Veille automatique | Suppose un serveur. Les brèves sont saisies à la main dans `contenu.js`, chacune avec sa source. |
| Rendu côté serveur | Le référencement s'en accommode aujourd'hui, mais une version statique par page serait préférable si le trafic devient prioritaire. |
| Bascule vers Baserow | Le site lit encore Airtable via `build.py`. À rebrancher sur Baserow une fois la base cible stabilisée. |

## Sources

Base Airtable `appQ2zqc80kkc6MR1`, relevée le 17/09/2026.
RGPD (UE) 2016/679, art. 13, 28, 30, 32, 44-49 · règlement (UE) 2024/1689 ·
code du travail, art. L.6352-12 · code de la consommation, art. L.121-2 et
L.612-1 · CGI, art. 261-4-4° a.
