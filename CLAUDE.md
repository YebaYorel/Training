# Intégration Baserow — instructions pour Claude Code

Ce dépôt connecte **Baserow** (cloud UE, hébergé par Baserow B.V., Pays-Bas) à
Claude Code pour YEBA FORMATIONS. Objectif : concevoir et remplir des bases de
données puissantes, en respectant la **souveraineté des données européennes**.

## Comment utiliser Baserow ici

Un serveur MCP `baserow` est enregistré dans `.mcp.json`. Après configuration,
tu disposes des outils : `baserow_health_check`, `list_workspaces`,
`create_database`, `create_table_with_schema`, `create_field`, `list_rows`,
`create_rows`, `update_row`, `delete_row`, etc.

Repli sans MCP : `python -m baserow.cli check` puis les sous-commandes.

## Modèle d'authentification (important)

- **Créer/modifier la structure** (base, table, champ) → nécessite le **JWT**
  (compte de service `BASEROW_EMAIL`/`BASEROW_PASSWORD`, rôle Builder).
- **Lire/écrire des lignes** → le **Database Token** (`BASEROW_TOKEN`) suffit ;
  le client l'utilise en priorité pour limiter l'usage du JWT.

## Règles de conception d'une base « ingénieuse »

1. Toujours `list_workspaces` d'abord pour récupérer le `workspace_id`.
2. Nommer explicitement tables et champs (français, sans abréviation obscure).
3. Utiliser les bons types : `single_select` pour un statut, `link_row` pour
   relier deux tables (ex. Prospects ↔ Formations), `date`, `email`, `number`.
4. Préférer `create_table_with_schema` pour poser un schéma complet d'un coup.
5. **Minimisation RGPD** : ne créer que les champs de données personnelles
   réellement nécessaires ; éviter les champs sensibles (santé, opinions) sauf
   base légale explicite.

## Réflexe RGPD / IA Act (à signaler spontanément)

Quand une base contient des **données personnelles** (nom, email, téléphone de
prospects/stagiaires) → **RGPD** : finalité définie, minimisation, durée de
conservation, base légale. Baserow cloud UE facilite la localisation UE.
Si une base alimente un traitement décisionnel automatisé (scoring, tri de
candidats) → vérifier l'**IA Act** (niveau de risque).

## Sécurité

- Secrets uniquement dans `.env` (ignoré par Git). Ne jamais les committer.
- Compte de service dédié, révocable, distinct du compte personnel.
