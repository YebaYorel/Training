---
title: "Feuille 5 — Implémenter le workspace Airtable et les workflows Make chez le client"
---

**Principe** : tout appartient au client (comptes, domaine, carte bancaire, données). Le freelance est un **invité temporaire**. **Il n'y a pas de serveur à acheter** : Airtable, Make et Mistral sont des services **SaaS** (les serveurs sont chez l'éditeur).
*En simple : « On ne construit pas l'usine chez le client, on lui loue des machines dans le cloud, mais à son nom et avec ses clés. »*

## 1. Schéma d'architecture

<div class="archi">
<div class="row"><div class="box people">👷 3 chefs de chantier<br><small>smartphone · formulaire « Rapport terrain » · page Terrain</small></div><div class="box people">🧑‍💼 Paul · Zineb · chargé d'affaires<br><small>PC · interface Direction / Administratif</small></div><div class="box people">🏠 Clients<br><small>formulaire « Nouvelle demande » · emails</small></div></div>
<div class="arrow">⬇ HTTPS (chiffré) · comptes nominatifs + 2FA</div>
<div class="row"><div class="box core">📊 <b>AIRTABLE</b> — base NEOBATI<br><small>12 tables · formules · interfaces · formulaires<br>Automatisation « Exécuter un script » → webhook</small></div></div>
<div class="arrow">⬇ webhook + jeton secret  ⬆ API Airtable (PAT limité à 1 base)</div>
<div class="row"><div class="box core">⚙️ <b>MAKE</b> — organisation « Atelier NéoBâti » · zone EU<br><small>S1 demande · S2 rapport IA · S3 devis · S4 factures · S5 synthèse · S6 affectation · S0 erreurs</small></div></div>
<div class="arrow">⬇ clés API stockées dans les connexions Make</div>
<div class="row"><div class="box ext">🤖 Mistral AI<br><small>résumés, relances</small></div><div class="box ext">✉️ Messagerie du domaine<br><small>SMTP (OVHcloud / Infomaniak) ou Brevo</small></div><div class="box ext">🗄️ Sauvegardes<br><small>CSV + blueprints · stockage UE</small></div></div>
</div>

## 2. Ce qu'il faut (matériel, comptes, données)

| Élément | Choix recommandé | Au nom de | Pourquoi |
|---|---|---|---|
| Postes bureau | 3 PC à jour (OS supporté, antivirus, session nominative) | Client | Paul, Zineb, chargé d'affaires |
| Smartphones terrain | 3 téléphones **professionnels**, verrouillage + chiffrement | Client | 1 par binôme / chef de chantier |
| Connexion | Internet bureau + 4G terrain | Client | SaaS = besoin de réseau |
| Nom de domaine | `atelierneobati.fr` | Client | Adresses emails et propriété des comptes |
| Adresse « propriétaire » | `admin@atelierneobati.fr` (boîte partagée Paul + Zineb) | Client | Ne jamais dépendre de la boîte d'un salarié ou du freelance |
| Airtable | Workspace « Atelier NéoBâti », offre **Team** (action script + 25 000 exécutions) | Client | Propriétaire : `admin@` |
| Make | Organisation « Atelier NéoBâti », **zone EU**, offre **Core** (scénarios actifs illimités) | Client | Propriétaire : `admin@` |
| Mistral AI | Compte La Plateforme + clé API dédiée « make-neobati » | Client | Éditeur français |
| Emails sortants | SMTP du domaine ou Brevo (éditeur français) | Client | Expéditeur = le client, pas le freelance |
| Mots de passe | Gestionnaire européen (ex. Proton Pass, Suisse) ou KeePassXC (local) | Client | 🔒 aucun secret dans un email ou un fichier |
| Données de départ | Export Excel des clients, devis, factures, chantiers en cours | Client | Import CSV dans Airtable après nettoyage |

**Coût récurrent indicatif** (à vérifier le jour de la vente) : Airtable Team ≈ 20 $/éditeur/mois en annuel × 3 éditeurs ≈ **60 $/mois** ; Make Core ≈ **9 $/mois** en annuel (10 000 crédits) ; Mistral : quelques euros selon le volume (~150 appels/mois). *Sources : jetadmin.io et activepieces.com, comparatifs octobre 2026 — non confirmés sur les pages officielles, inaccessibles depuis mon environnement.*

## 3. Les étapes du déploiement

| Étape | Livrable | Qui |
|---|---|---|
| J0 · Audit | Cartographie des processus, liste des données, registre RGPD (art. 30) mis à jour | Freelance + Paul |
| J1 · Comptes | Domaine, `admin@`, Airtable, Make (zone EU), Mistral, SMTP créés **par le client** ; freelance invité | Client (guidé) |
| J1 · Contrats | DPA Airtable, Make, Mistral, prestataire email signés ; contrat freelance avec clause de réversibilité | Client |
| J2-J4 · Construction | Base, interfaces, formulaires, 6 scénarios + S0, jeu de test fictif | Freelance |
| J5 · Recette | Tests de chaque scénario (cas normal + cas d'erreur), validation par Paul | Freelance + Paul |
| J6 · Import | Import des vraies données, contrôle des totaux (CA, factures ouvertes) | Freelance + Zineb |
| J7 · Formation | 1 session par rôle (direction, administratif, terrain) + maîtrise de l'IA (IA Act, art. 4) | Freelance |
| J7 · Mise en production | Activation des scénarios, publication des formulaires | Freelance + Paul |
| J+30 · Passation | Retrait des droits du freelance (ou contrat de maintenance), revue des journaux | Paul |

## 4. Cybersécurité (checklist de mise en production) 🔒

- [ ] **2FA** activée sur Airtable, Make, Mistral, messagerie, pour **tous** les comptes.
- [ ] Rôles au **moindre privilège** : artisans = formulaire + page Terrain ; seul `admin@` est propriétaire.
- [ ] **Personal Access Token** Airtable dédié à Make : scopes `data.records:read`, `data.records:write`, `schema.bases:read`, **une seule base**, nom explicite, rotation annuelle.
- [ ] Webhooks Make protégés par un **jeton secret** vérifié par un filtre ; URL jamais publiée.
- [ ] Clés API uniquement dans les **connexions Make** ; option « données confidentielles » sur les scénarios qui manipulent des données clients.
- [ ] **Sauvegardes** : snapshot Airtable + export CSV mensuel + export des **blueprints** Make à chaque modification, stockés dans un espace UE du client.
- [ ] **Procédure de départ** d'un salarié : retrait des accès le jour même, rotation des secrets partagés.
- [ ] Smartphones terrain : code de verrouillage, mises à jour, pas de photos de documents personnels des clients.
- [ ] Alertes d'erreur Make envoyées à `admin@` ; table LOGS ERREURS revue chaque semaine.

*Référence : ANSSI, « Guide d'hygiène informatique » (mesures d'authentification, de sauvegarde et de gestion des droits).*

## 5. Autonomie du client : qui fait quoi après la livraison

| Situation | Qui | Action (runbook) |
|---|---|---|
| Une relance n'est pas partie | Zineb | Make › Historique du scénario S3/S4 › lire l'erreur › table LOGS ERREURS |
| Erreur « 401 / connexion » | Zineb | Make › Connexions › Réautoriser (jeton expiré ou révoqué) |
| Erreur « 429 / quota » | Personne | Réessai automatique (Break) ; si 3 échecs : relancer l'exécution incomplète |
| Nouvel artisan | Zineb | Ajouter dans RESSOURCES + l'inviter sur la page Terrain |
| Un salarié part | Paul | Retirer ses accès Airtable/Make le jour même |
| Crédits Make bientôt épuisés | Paul | Make › Organisation › Utilisation ; vérifier qu'aucun scénario ne boucle |
| Modifier un texte de relance | Chargé d'affaires | Modifier le prompt dans S3/S4, tester avec « Run once », exporter le blueprint |

## 6. Option souveraine (alternative à proposer)

Même architecture avec **Baserow** (base de données, éditeur néerlandais, cloud UE) à la place d'Airtable et **n8n** auto-hébergé sur un serveur UE (OVHcloud ou Scaleway en France ; la brochure École Cube cite un hébergement Hostinger à 4,99 €/an) à la place de Make. Avantages : données en UE, pas de facturation à l'opération. Contreparties : maintenance du serveur (mises à jour, sauvegardes, supervision) à contractualiser.

*RGPD : les données restent en UE, donc pas de transfert hors UE à encadrer. IA Act : inchangé (risque limité).*
