# Migration Airtable → Baserow

## Le blocage, et sa cause

Le serveur MCP `baserow` échouait avec `CONNECTION_CLOSED`. Ce message ne dit
rien de la cause : il signifie seulement que le processus est mort avant de
répondre. Trois pannes en cascade, chacune masquant la suivante :

| # | Symptôme | Cause réelle |
|---|---|---|
| 1 | `ModuleNotFoundError: No module named 'dotenv'` | `requirements.txt` n'a jamais été installé. Les conteneurs distants sont reclonés à neuf à chaque session. |
| 2 | `Cannot uninstall PyJWT 2.7.0, RECORD file not found` | PyJWT installé par Debian, sans métadonnées pip. Fait échouer **toute** l'installation, pas seulement ce paquet. |
| 3 | `No module named 'mcp.server.fastmcp'` | Le SDK `mcp` est passé en 2.x, où `FastMCP` a été renommé `MCPServer`. Le serveur utilise l'API 1.x. |

### Corrections appliquées

- `requirements.txt` : `mcp` épinglé en `<2`.
- `.mcp.json` : la commande passe de `python` à `python3`.
- `.claude/setup.sh` : installe les dépendances, contourne le conflit PyJWT et
  réinstalle le SDK en 1.x s'il détecte une 2.x.
- `.claude/settings.json` : hook `SessionStart` qui lance ce script à chaque
  ouverture de session. **C'est ce qui rend la correction permanente** : sans
  lui, le prochain conteneur repart avec la même panne.

Vérification :

```bash
bash .claude/setup.sh
printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"t","version":"1"}}}' \
  | python3 baserow_mcp_server.py
```

Le serveur doit répondre `"serverInfo":{"name":"baserow-yeba"}`.

## Ce qui reste bloqué : les identifiants

Le serveur démarre, mais **aucun `.env` n'existe** : il ne peut pas
s'authentifier auprès de Baserow. La migration ne peut donc pas être lancée
depuis cette session.

```bash
cp .env.example .env
# puis renseigner :
#   AIRTABLE_TOKEN          jeton de lecture Airtable
#   BASEROW_EMAIL           compte de service, rôle Builder
#   BASEROW_PASSWORD
#   BASEROW_WORKSPACE_ID    obtenu via l'outil list_workspaces
```

`.env` est ignoré par Git. Ne jamais l'y committer.

## Deux voies, selon ce que vous avez sous la main

### Voie A — import CSV (aucun identifiant Baserow requis)

C'est celle qui débloque immédiatement, et qui évite le piège des cookies.

```bash
python migration/export_csv.py --sans-donnees-perso   # commencer sans les stagiaires
python migration/export_csv.py                        # les 19 tables
```

Puis dans Baserow : **Base de données → Ajouter une table → Importer un
fichier → CSV**, en cochant « première ligne = en-têtes ». Aucun cookie n'est
demandé par cette voie.

**Ce que le CSV perd** : les liens entre tables deviennent du texte, les pièces
jointes ne suivent pas, les formules sont figées en valeurs. C'est la limite de
tout import par fichier.

### ⛔ Ce qu'il ne faut pas faire : l'import Airtable natif de Baserow

Il réclame les cookies `__Host-airtable-session` et `.sig`. Ce ne sont pas des
identifiants d'API mais une **session complète** : qui les détient est vous,
sur toutes vos bases, sans mot de passe ni double authentification, et sans
pouvoir révoquer ce seul accès. Les coller dans un formulaire tiers — ou les
transmettre à quiconque — est précisément la manœuvre qu'un organisme formant à
la cybersécurité doit refuser.

Un jeton d'API Airtable en lecture seule, lui, se crée sur
https://airtable.com/create/tokens et se révoque en un clic.

### Voie B — migration par API (conserve les liens)

```bash
python migration/airtable_vers_baserow.py --plan        # n'écrit rien
python migration/airtable_vers_baserow.py --tables "CATALOGUE FORMATIONS" --executer
python migration/airtable_vers_baserow.py --executer    # les 19 tables
```

**Migrer d'abord une seule table.** `CATALOGUE FORMATIONS` ne contient aucune
donnée personnelle : c'est le bon banc d'essai pour vérifier la conversion
avant de toucher aux tables de stagiaires.

## Ce qui passe, et ce qui ne passe pas

Mesuré sur votre schéma réel — 19 tables, 517 champs :

| | Champs | Part |
|---|---|---|
| Migrés automatiquement | **380** | 73 % |
| Reprise manuelle | 135 | 26 % |
| Exclus (RGPD art. 9) | 2 | — |

Passent automatiquement : texte, texte long, nombres, montants, pourcentages,
dates, cases à cocher, e-mails, téléphones, URL, sélecteurs simples et
multiples (avec leurs options), **et les liens entre tables**.

Ne passent pas, et pourquoi :

| Type | Nombre | Motif |
|---|---|---|
| `multipleLookupValues` | 96 | Dépend des liens. À recréer une fois les liaisons vérifiées. |
| `formula` | 38 | Les fonctions de Baserow ne sont pas celles d'Airtable. **Traduire automatiquement produirait des calculs faux sans le signaler** — le script préfère ne rien écrire. |
| `multipleAttachments` | 34 | Le champ est créé, vide. Les fichiers doivent être téléchargés puis re-téléversés. |
| `count`, `createdBy`, `aiText` | 3 | Sans équivalent direct. |

Les 135 champs concernés sont listés nommément dans `rapport-migration.json`
après un `--plan`.

## Ordre des opérations

Le script procède en deux passes, et cet ordre n'est pas négociable : un lien
ne peut être créé que si la table cible existe déjà.

1. Tables, champs simples, lignes.
2. Champs `link_row`, puis remplissage des liaisons à partir d'une table de
   correspondance entre identifiants Airtable et Baserow.

## RGPD — ce que cette migration engage

Elle déplace des données personnelles de stagiaires d'un sous-traitant
américain vers un sous-traitant néerlandais. Ce n'est pas une opération
technique neutre.

**Avant `--executer` :**

1. **Signer l'accord de sous-traitance Baserow** (art. 28). Sans acte
   juridique encadrant le traitement, le transfert est irrégulier — même vers
   l'Union européenne.
2. **Mettre à jour le registre des traitements** (art. 30) : Baserow B.V.,
   Pays-Bas, remplace Airtable Inc., États-Unis.
3. **Corriger la mention d'information** si elle nommait Airtable ou citait un
   hébergement hors UE.

**Après vérification des données :**

4. **Supprimer les données chez Airtable** (art. 5.1.e — limitation de la
   conservation). Une base laissée en place reste un transfert hors UE actif,
   et la migration n'aura rien résolu.
5. **Supprimer les deux champs de l'article 9** plutôt que de les migrer :
   `⚠️ NE PAS REMPLIR — Type de handicap` et `Document RQTH`. Vérifié le
   17/09/2026 : ils sont **vides**. Le script ne les migre jamais, quel que
   soit leur contenu.

**Ce qui n'est pas requis :** informer individuellement les personnes du seul
changement de sous-traitant. Le responsable de traitement et les finalités
sont inchangés ; l'article 13 ne l'impose pas.

## Pourquoi ce chantier compte commercialement

Votre `CONFIG SYSTEME` exige, pour l'hébergement, « un prestataire non soumis
à une législation d'accès extraterritorial ». Airtable Inc. est une société
américaine, soumise au CLOUD Act. Vos tables `APPRENANTS`, `INSCRIPTIONS`,
`PRESENCES` et `EVALUATIONS` y hébergent des données de stagiaires réunionnais.

C'est une contradiction interne entre votre exigence écrite et votre outil
réel. Elle est sans gravité tant qu'elle n'est pas relevée — mais c'est
exactement le point qu'un client averti, ou un concurrent, peut soulever
pendant que vous vendez la souveraineté des données.

## Sources

- Base Airtable `appQ2zqc80kkc6MR1`, schéma relevé le 17/09/2026.
- API Baserow : https://baserow.io/api-docs
- RGPD (UE) 2016/679, art. 5.1.e, 9, 13, 28, 30, 44-49.
