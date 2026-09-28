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

# Présentations YEBA FORMATIONS (soirée de lancement et suivantes)

Outils toujours disponibles au démarrage (hook `.claude/hooks/session-start.sh`) :
**python-pptx, Reveal.js, Remotion, VBA, Slides.com, Felo Slides** — un skill par outil dans
`.claude/skills/`, orchestrés par le skill `presentation-yeba` (règles Mesaure/Slidor + charte).

- Source unique du contenu : `soiree-lancement/contenu/slides.json`
- Tout reconstruire : `bash soiree-lancement/build_all.sh` (`--videos` pour Remotion)
- Charte : fond #121212 / #1B3A6B, texte blanc, or #C9A84C (jamais en texte sur blanc),
  Montserrat, 15-20 mots/slide, titres ≥ 54 pt, texte ≥ 28 pt, aucun mot coupé ni barré.
- Logo : version **sans œil** (`soiree-lancement/assets/`).
- Marque blanche : pour un autre organisme, AUCUNE mention de YEBA FORMATIONS.
- Toujours contrôler visuellement (PDF → PNG) avant de livrer.
