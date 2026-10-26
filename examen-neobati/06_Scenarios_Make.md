---
title: "Feuille 6 — Scénarios Make : fiches de construction et de documentation"
---

## 0. Se connecter à Make (à faire par toi, une seule fois)

1. Va sur **make.com** › *Get started free* › inscris-toi avec l'adresse **du client** (pour l'examen : une adresse de démonstration à ton nom). Choisis l'hébergement **EU** (zone EU1/EU2). Active la **double authentification** (profil › *Password & 2FA*).
2. Crée l'organisation **« Atelier NéoBâti »**.
3. **Connexions** (menu *Connections* › *Add*) :
   - **Airtable** : de préférence par **Personal Access Token** créé sur airtable.com/create/tokens, scopes `data.records:read`, `data.records:write`, `schema.bases:read`, accès limité à la base « NEOBATI – Gestion des chantiers (v2 examen) ».
   - **Mistral AI** : clé API créée sur console.mistral.ai (nom : `make-neobati`).
   - **Email** : connexion SMTP de la messagerie du domaine (ou app Brevo).
4. Pour que **je construise les scénarios automatiquement** : ajoute le connecteur Make dans claude.ai › Paramètres › Connecteurs (https://claude.ai/customize/connectors ; le dépôt make-skills indique le serveur MCP `https://mcp.make.com/claude`), puis ouvre une **nouvelle session**. Sinon, construis-les à la main avec les fiches ci-dessous : c'est aussi le meilleur entraînement pour l'oral.

## 1. Conventions

- Nom : `S<n> – <objet>` ; une note de description dans chaque scénario.
- Tout envoi vers un client vérifie `Opposition aux relances` (RGPD art. 21).
- Les **calculs** sont faits par les formules Airtable ; Make lit des champs déjà prêts (« Alerte devis », « Niveau de relance », « Alerte pilotage »).
- Chaque module sensible (Airtable, Mistral, email) porte un **gestionnaire d'erreurs** (motif S0).
- Après chaque modification : *Run once* de test, puis **export du blueprint** (sauvegarde).

## 2. Déclencheur Airtable → Make (S1, S2, S6)

Dans Airtable › *Automations* : déclencheur « Quand un enregistrement est créé » (DEMANDES, RAPPORTS TERRAIN) ou « Quand un enregistrement est mis à jour » sur le champ *Équipe affectée* (CHANTIERS) → action **« Exécuter un script »** (offre Team ou supérieure). Variables d'entrée : `webhookUrl`, `token`, et les champs utiles du déclencheur.

```javascript
// Envoie l'événement à Make avec un jeton secret (vérifié par un filtre Make)
const { webhookUrl, token, ...donnees } = input.config();
const reponse = await fetch(webhookUrl, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ token, ...donnees })
});
if (!reponse.ok) {
  throw new Error(`Make a répondu ${reponse.status}`); // visible dans l'historique Airtable
}
```

*Optimisation* : le script envoie directement les champs nécessaires (payload complet), donc Make n'a pas besoin de relire l'enregistrement : **1 opération économisée par exécution**.
*Alternative offre gratuite* : module Make **Airtable › Watch Records** (polling, champ « Créé le » / « Reçue le » déjà créé), toutes les 15 min — plus coûteux (voir §5).

## 3. Les fiches

### S1 – Nouvelle demande client  ·  déclencheur : webhook (instantané)

| # | Module | Réglage clé | Op. |
|---|---|---|---|
| 1 | Webhooks › Custom webhook | Reçoit `token, recordId, nom, prenom, email, objet, description` | 1 |
| — | Filtre « Jeton valide » | `{{1.token}}` = jeton stocké ; sinon arrêt | 0 |
| 2 | Airtable › Search Records | Table CLIENTS, formule `LOWER({Email}) = LOWER('{{1.email}}')`, limite 1 | 1 |
| 3 | Flow Control › If-else | Branche « Nouveau client » si `{{2.id}}` n'existe pas ; sinon « Client existant » | 0 |
| 4 | Airtable › Create a Record (branche Nouveau) | CLIENTS : Nom, Prénom, Email, Statut = Prospect, Date premier/dernier contact = aujourd'hui | 1 |
| 5 | Merge | Récupère l'identifiant client (créé ou trouvé) | 0 |
| 6 | Airtable › Update a Record | DEMANDES : Client créé = id, Statut demande = Traitée | 1 |
| 7 | Mistral AI › Create a Chat Completion | Prompt P1 (accusé de réception) | 1 |
| 8 | Email › Send an email | Au demandeur, expéditeur `contact@atelierneobati.fr` | 1 |
| 9 | Airtable › Create a Record | INTERACTIONS : Canal = Formulaire, Généré par IA = oui | 1 |
| 10 | Email › Send an email | Au chargé d'affaires : « Nouvelle demande : {{1.objet}} » | 1 |

**8 opérations** par demande (7 si le client existe déjà). *Si Make refuse une branche vide « Client existant », y placer Tools › Set variable (`clientId = {{2.id}}`) : + 1 opération.*

### S2 – Rapport terrain → résumé IA  ·  déclencheur : webhook (instantané)

| # | Module | Réglage clé | Op. |
|---|---|---|---|
| 1 | Custom webhook | Reçoit `token, recordId, chantierId, chantier, avancement, notes, probleme` + filtre jeton | 1 |
| 2 | Mistral AI › Create a Chat Completion | Prompt P2, température 0,2 | 1 |
| 3 | Airtable › Update a Record | RAPPORTS TERRAIN : Résumé IA = `{{trim(first(split(2.result; "###")))}}`, Points de suivi IA = `{{trim(last(split(2.result; "###")))}}`, Traité par Make = oui | 1 |
| 4 | Airtable › Update a Record | CHANTIERS `{{1.chantierId}}` : Avancement physique, Dernier résumé IA, Dernière remontée terrain | 1 |
| 5 | Airtable › Create a Record | INTERACTIONS : Note terrain, Interne, Généré par IA = oui | 1 |
| 6 | Email (filtre `{{1.probleme}}` = true) | À Paul : « Problème signalé sur {{1.chantier}} » + résumé | 1 |

**5 opérations** par rapport (+1 si problème).

### S3 – Relance des devis  ·  planifié : lundi → vendredi, 8 h 00

| # | Module | Réglage clé | Op. |
|---|---|---|---|
| 1 | Airtable › Search Records | DEVIS, formule ci-dessous | 1 |
| 2 | Mistral AI | Prompt P3 | 1 |
| 3 | Email | Au client (`Email client`) | 1 |
| 4 | Airtable › Update a Record | Nombre de relances + 1, Date dernière relance = aujourd'hui | 1 |
| 5 | Airtable › Create a Record | INTERACTIONS : Email, Sortant, Généré par IA | 1 |

Formule de recherche :
`AND({Alerte devis} = 'À relancer', {Opposition client (relances)} = 0, OR({Date dernière relance} = BLANK(), DATETIME_DIFF(TODAY(), {Date dernière relance}, 'days') >= 3))`
→ relance à J-5 puis au plus tôt 3 jours après, **2 relances maximum** (plafond dans la formule « Alerte devis »).
*Le module Search Records renvoie un bundle par devis : c'est un itérateur implicite, pas besoin d'Iterator.*

### S4 – Relance des factures et acomptes  ·  planifié : lundi → vendredi, 8 h 05

| # | Module | Réglage clé | Op. |
|---|---|---|---|
| 1 | Airtable › Search Records | FACTURES : `AND({Niveau de relance} != 'OK', OR({Date dernière relance} = BLANK(), DATETIME_DIFF(TODAY(), {Date dernière relance}, 'days') >= 7))` | 1 |
| 2 | If-else | Branche A « Escalade direction » ; branche B « Relance 1 ou 2 » | 0 |
| 3A | Email à Paul | Facture, client, montant TTC, jours de retard : **décision humaine** (mise en demeure ?) | 1 |
| 3B | Mistral AI | Prompt P4 (ton selon niveau ; mention 40 € si Type de client = Entreprise) | 1 |
| 4B | Email au client | | 1 |
| 5 | Merge puis Airtable › Update a Record | Nombre de relances + 1, Date dernière relance | 1 |
| 6 | Airtable › Create a Record | INTERACTIONS | 1 |

Règles : relance au plus **tous les 7 jours** ; niveaux calculés dans Airtable (1–15 j courtoise, 16–30 j ferme, > 30 j escalade).
*Démo au 26/10/2026* : FAC-2026-103 (acompte C2, 3 600 € HT, 4 320 € TTC, 20 jours de retard) → « Relance 2 – ferme ».

### S5 – Synthèse direction  ·  planifié : lundi → vendredi, 7 h 45

| # | Module | Réglage clé | Op. |
|---|---|---|---|
| 1 | Airtable › Search Records | CHANTIERS : `{Alerte pilotage} = 'À traiter'` | 1 |
| 2 | Tools › Text aggregator | Une ligne par chantier : `• {{1.Nom chantier}} — retard {{1.Jours de retard}} j — budget : {{1.Alerte budget}} — acompte : {{1.Alerte acompte}}` | 1 |
| 3 | Email à Paul | Objet « Chantiers à traiter ce matin » | 1 |

Au 26/10/2026 : 2 lignes (C2 retard 10 j + acompte non reçu ; C4 dépassement budget). Si aucun chantier : rien n'est envoyé.

### S6 – Notification d'affectation  ·  déclencheur : webhook (mise à jour de « Équipe affectée »)

| # | Module | Réglage clé | Op. |
|---|---|---|---|
| 1 | Custom webhook | `token, chantier, adresse, dateDebut, emails` + filtre jeton | 1 |
| 2 | Email | Un seul email à toute l'équipe : chantier, adresse, date de début, lien page Terrain | 1 |

### S0 – Motif de gestion des erreurs (sur chaque module Airtable, Mistral, Email)

| Erreur prévisible | Détection | Directive Make | Trace |
|---|---|---|---|
| Connexion / API (401, 5xx), délai dépassé | Gestionnaire d'erreurs | **Break** : 3 essais, toutes les 15 min (exécution incomplète stockée) | LOGS ERREURS + email `admin@` |
| Quota dépassé (429) | Gestionnaire d'erreurs | **Break** | LOGS ERREURS |
| Mistral indisponible | Gestionnaire d'erreurs du module IA | **Resume** avec un texte standard pré-écrit | LOGS ERREURS (« Résumé non généré ») |
| Données manquantes (email vide, montant vide) | **Filtre** en amont | Le bundle est arrêté ; route d'erreur → **Ignore** | LOGS ERREURS « Données manquantes » |
| Jeton webhook invalide | Filtre « Jeton valide » | Arrêt | Historique Make |

Réglages du scénario : *Allow storing of incomplete executions* = oui ; notifications d'erreur = oui ; *Data is confidential* = oui pour S1, S3, S4.
Chaque route d'erreur : **Airtable › Create a Record** (LOGS ERREURS : date, nom du scénario, module, type, message `{{error.message}}`, action) puis **Email** à `admin@`.

## 4. Prompts (prompt système · prompt utilisateur)

**Règles communes (système)** : « Tu es l'assistant administratif d'Atelier NéoBâti, entreprise artisanale de rénovation à Nantes. Tu écris en français correct, vouvoiement, ton professionnel et chaleureux. Tu n'inventes **aucune** information absente des données fournies ; si une information manque, tu écris "non précisé". Tu ne mentionnes aucune donnée personnelle autre que le nom fourni. »

- **P1 – Accusé de réception** : « Rédige un email de 80 mots maximum à {{prénom}} {{nom}} qui remercie pour la demande "{{objet}}", annonce un rappel du chargé d'affaires sous 48 h ouvrées. Signature : Zineb Durieux, Atelier NéoBâti. »
- **P2 – Résumé terrain** : « Notes brutes du chef de chantier pour {{chantier}} (avancement déclaré {{avancement}} %) : {{notes}}. Réponds exactement au format : RÉSUMÉ en 3 phrases maximum, puis la ligne `###`, puis 1 à 3 POINTS DE SUIVI numérotés, chacun avec le rôle responsable (direction, administratif, chargé d'affaires, chantier). »
- **P3 – Relance devis** : « Rédige une relance courtoise de 120 mots maximum pour le devis {{référence}} de {{montant}} € HT, valable jusqu'au {{date de validité}}, adressée à {{nom client}}. Propose un échange téléphonique. Aucune pression commerciale. »
- **P4 – Relance facture** : « Niveau : {{Niveau de relance}}. Facture {{référence}}, {{montant TTC}} € TTC, échéance {{date}}, {{jours}} jours de retard, client {{nom}} ({{type de client}}). Relance 1 : rappel aimable. Relance 2 : ton ferme et courtois, demande de règlement sous 8 jours ; **si le client est une entreprise**, rappelle l'indemnité forfaitaire de recouvrement de 40 € (art. L441-10 du Code de commerce). 150 mots maximum. »

Réglages Mistral : modèle « small » ou équivalent, **température 0,2**, longueur maximale 400 tokens.

## 5. Budget d'opérations (hypothèses à valider avec Paul Durieux)

| Scénario | Volume / mois | Op. par exécution | Total |
|---|---|---|---|
| S1 Demandes | 8 demandes | 8 | 64 |
| S2 Rapports | 60 rapports (3 binômes × 20 jours) + 6 problèmes | 5 (+1) | 306 |
| S3 Devis | 22 exécutions + 10 relances | 1 + 4 par relance | 62 |
| S4 Factures | 22 exécutions + 10 relances | 1 + 4 par relance | 62 |
| S5 Synthèse | 22 exécutions | 3 | 66 |
| S6 Affectations | 20 | 2 | 40 |
| S0 Erreurs | marge | — | 10 |
| **Total** | | | **≈ 610 opérations / mois** |

**Comparaison** : si S1, S2 et S6 étaient en polling toutes les 15 min : 3 × 96 vérifications/jour × 30 jours = **8 640** opérations supplémentaires → **≈ 9 250 / mois**, soit **15 fois plus**.
**Offre conseillée** : Make **Core** (10 000 crédits, scénarios actifs illimités). L'offre gratuite (1 000 crédits) suffirait en volume mais limite à **2 scénarios actifs**. Côté Airtable : 8 + 60 + 20 = **88 exécutions d'automatisation / mois**.
*Sources : comparatifs Make 2026 (activepieces.com, eesel.ai) et Airtable 2026 (jetadmin.io) — à revérifier sur les pages tarifs officielles.*

**RGPD** : Mistral AI = sous-traitant (DPA) ; seules les données nécessaires sont envoyées dans les prompts (pas d'adresse ni de téléphone). **IA Act** : génération de texte, risque limité ; escalade > 30 jours toujours décidée par un humain.
