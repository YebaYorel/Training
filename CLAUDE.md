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

## Identité YEBA FORMATIONS — valeurs de référence

Source de vérité pour toute pièce produite au nom de YEBA FORMATIONS
(devis, convention, convocation, attestation, certificat de réalisation,
support pédagogique). **Recopier depuis ici, ne jamais ressaisir de
mémoire ni reprendre un ancien document sans vérifier.**

| Rubrique | Valeur exacte |
|---|---|
| Raison sociale | YEBA FORMATIONS |
| Directeur / référent handicap | Aurélien LUMEKA |
| SIRET | 814 622 262 00032 |
| Code APE | 85.59Z |
| Adresse | 9 rue François Châtelain — Les Calebassiers, Bât A — Entrée 1 — Porte 0042, 97490 Sainte-Clotilde (La Réunion) |
| Téléphone | +262 6 93 32 24 45 |
| Déclaration d'activité (NDA) | 04973676397, auprès du préfet de région de La Réunion — *ne vaut pas agrément de l'État* |
| **Certification Qualiopi** | **25FOR02027.1** — catégorie « actions de formation » |
| Adresse électronique institutionnelle | contact@yebaformations.re |
| Adresse électronique de contact documents | yebaformations@proton.me |
| Régime de TVA | non applicable, article 293 B du CGI (franchise en base) |

### Pièges connus — à vérifier à chaque production

- **Qualiopi : `25FOR02027.1`**, avec un **R**. La forme `25FOF02027.1`
  circule dans d'anciens documents : elle est **fausse**. Un numéro de
  certification erroné sur une pièce déposée à un OPCO est un motif de
  rejet et fragilise le document en cas de contrôle.
- **Ne jamais écrire `yebaformations@gmail.re`** (domaine inexistant) ni
  `yebaformations@gmail.com` (abandonné au profit de Proton).
- **Deux adresses coexistent** (`contact@yebaformations.re` et
  `yebaformations@proton.me`) : demander laquelle doit figurer avant de
  produire une pièce contractuelle, plutôt que de panacher.
- **Coordonnées bancaires** : jamais dans ce dépôt (public). Les reprendre
  depuis la source interne au moment de produire la pièce.
- **Lieux de formation** : jamais par défaut ni par reprise d'un ancien
  devis — le lieu se confirme dossier par dossier.

### Réflexe conformité sur ces pièces

- **RGPD** — Une pièce nominative (devis client, convention, feuille
  d'émargement) porte des données à caractère personnel : finalité
  d'exécution et de traçabilité (art. 6.1.b et 6.1.c), conservation
  3 ans, hébergement UE. Ne jamais committer ces pièces dans ce dépôt.
- **IA Act** — Tout support conçu avec l'assistance d'une IA générative
  porte la mention de transparence de l'article 50 du règlement
  (UE) 2024/1689. Aucun système d'IA n'intervient dans l'évaluation des
  stagiaires : hors annexe III (haut risque).
