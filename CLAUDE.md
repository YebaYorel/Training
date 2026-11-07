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

## Charte YEBA FORMATIONS — à appliquer à CHAQUE production

Skill `yeba-charte` ; valeurs exactes dans `.claude/skills/yeba-powerpoint/charte.json`.

- Bleu `#1B3A6B` (dominante) · Or `#C9AB4C` (accents) · Noir `#121212` · Blanc `#FFFFFF`
- Titres **Montserrat Bold** · Texte **Inter** · **Poiret One** décoratif seulement (≥ 54 pt, jamais en formation)
- **Or jamais en texte sur fond blanc** (contraste 2,2:1, illisible) ; or OK sur noir (8,4:1) ou bleu (5,1:1)
- Images « Cyber-Garage Premium » (fonds sombres, néons bleu/or, réseaux de points, motif 974)
- Logo : fichiers fournis uniquement, jamais redessiné ni généré par IA
- **Exception** : travail pour un autre centre de formation → aucune trace de YEBA
- Web : polices auto-hébergées (pas de Google Fonts → RGPD)

## Skills et plugins installés

Inventaire complet, sources figées et refus motivés : `SKILLS.md`.

- **Tester une idée de business** → skills `founder-*` (commencer par `founder-plan`
  ou `founder-board`), `llm-council` pour challenger une décision, `arena` si une
  réponse ne convient pas.
- **PowerPoint** → toujours `yeba-powerpoint` (accessibilité + transitions), avec
  `anthropic-skills:pptx` pour la fabrication ; `frontend-slides` pour une version web animée.
- Les sorties de travail (`founder/`, `instagram/`, `linkedin/`, `.arena/`, rapports
  du conseil, .pptx/.pdf) sont **ignorées par Git** : ce dépôt est **public**.
- Ne pas activer `caveman` par défaut : Aurélien veut un raisonnement détaillé.
