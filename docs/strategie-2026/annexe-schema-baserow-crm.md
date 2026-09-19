# Annexe — Schéma Baserow du pilotage commercial

Base unique **« Pilotage YEBA 2026 »**, 4 tables. Souveraineté : Baserow cloud UE
(Baserow B.V., Pays-Bas). À créer via le serveur MCP `baserow` de ce dépôt.

> ⚠️ Le serveur MCP `baserow` n'a pas pu se connecter lors de la session du 19/09/2026
> (`CONNECTION_CLOSED`). Vérifier `.env` et `python -m baserow.cli check` avant création.

---

## Table 1 — `Comptes cibles` (objectif : 300 lignes)

| Champ | Type | Options / notes |
|---|---|---|
| Entreprise | `text` | |
| Dirigeant | `text` | Donnée personnelle |
| Fonction | `text` | |
| Secteur | `single_select` | Hôtellerie-restauration · BTP · Commerce · Services · Santé · Agro · Transport · Autre |
| Commune | `single_select` | |
| Effectif estimé | `number` | Indicateur de solvabilité OPCO |
| Téléphone | `phone_number` | Donnée personnelle |
| Email pro | `email` | Donnée personnelle |
| Source | `single_select` | Annuaire public · Recommandation · Réseau social · Atelier · CCI · Cabinet comptable |
| **Base légale** | `single_select` | **Intérêt légitime (B2B)** · Consentement · Relation contractuelle |
| Statut | `single_select` | À contacter · Contacté · RDV programmé · Diagnostic fait · Devis envoyé · Client · Perdu · **Opposé** |
| Date dernier contact | `date` | **Déclenche la purge à 3 ans** |
| Utilise déjà l'IA | `boolean` | Qualification article 4 |
| Notes | `long_text` | **Jamais de donnée sensible** (santé, opinions, origine) |

## Table 2 — `Affaires`

| Champ | Type | Options |
|---|---|---|
| Compte | `link_row` → `Comptes cibles` | |
| Offre | `single_select` | Pack Essentiel art.4 · Formation IA · Sprint · Copilote · Diagnostic gouvernance |
| Montant HT | `number` | |
| Statut | `single_select` | Proposée · Négociation · Gagnée · Perdue |
| Motif de perte | `single_select` | Prix · Timing · Concurrent · Pas de budget · Sans réponse |
| Financement | `single_select` | OPCO · Fonds propres · CPF · Mixte |
| **Autorisation communication** | `single_select` | **Accordée · Refusée · Non demandée** |
| Date signature | `date` | |
| Récurrent | `boolean` | Isole le CA d'abonnement |

## Table 3 — `Abonnements Copilote`

| Champ | Type | Notes |
|---|---|---|
| Client | `link_row` → `Comptes cibles` | |
| Mensualité HT | `number` | |
| Date de début / Fin d'engagement | `date` | |
| Statut | `single_select` | Actif · Suspendu · Résilié |
| Rapport mensuel remis | `boolean` | **L'indicateur de rétention n°1** |
| Heures gagnées cumulées | `number` | Alimente les cas clients |

## Table 4 — `Journal de publication`

| Champ | Type | Notes |
|---|---|---|
| Date / Réseau / Pilier | `date` / `single_select` / `single_select` | Piliers 1 à 5 (doc 03 §5) |
| Accroche utilisée | `text` | Pour identifier ce qui marche |
| Vues 48 h | `number` | Indicateur secondaire |
| **Partages en DM** | `number` | **Signal algorithmique n°1 (pondéré 3-5× les likes)** |
| **Conversations initiées** | `number` | **Indicateur de pilotage** |
| **RDV générés** | `number` | **Indicateur de pilotage** |
| Contenu IA | `boolean` | **Traçabilité IA Act art. 50** |

---

## ⚖️ RGPD — à appliquer dès la création

- **Finalité** : prospection commerciale B2B et gestion de la relation client.
- **Base légale** : intérêt légitime (B2B), conformément à la doctrine CNIL, sous réserve
  d'information préalable et d'un droit d'opposition simple.
- **Minimisation** : aucun champ de donnée sensible. Pas de date de naissance, pas de
  photo, pas d'appréciation personnelle dans les notes.
- **Conservation** : purge automatique **3 ans après le dernier contact** (vue filtrée +
  routine n8n mensuelle).
- **Droit d'opposition** : le statut `Opposé` doit **exclure définitivement** le compte de
  toute campagne. Ne jamais supprimer la ligne : conserver le minimum nécessaire pour
  prouver le respect de l'opposition.
- **Registre art. 30** : ce traitement doit y figurer.
- **Sous-traitance art. 28** : contrat à conclure avec Baserow B.V.
- **Accès** : compte de service dédié, révocable, distinct du compte personnel.
