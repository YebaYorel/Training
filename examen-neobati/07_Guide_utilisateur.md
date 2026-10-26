---
title: "Guide utilisateur — Système de gestion des chantiers Atelier NéoBâti"
---

*Livrable exigé par le sujet (« guides utilisateurs et fiches de scénarios »). Une page par rôle, plus la maintenance.*

## 1. Structure de la base (12 tables)

| Groupe | Tables | Rôle |
|---|---|---|
| Cœur métier (sujet) | CLIENTS · DEVIS · CHANTIERS · ETAPES · RESSOURCES · FACTURES | Les objets suivis |
| Coûts (annexe) | POINTAGES (heures × coût horaire) · ACHATS (fournitures, sous-traitance) | Calcul de la marge |
| Saisie | DEMANDES (formulaire client) · RAPPORTS TERRAIN (formulaire mobile) | Entrées automatisées par Make |
| Traçabilité | INTERACTIONS · LOGS ERREURS | Historique et incidents |

CHANTIERS est la table centrale : chaque chantier est relié à **1 client**, ses devis, factures, pointages, achats, étapes, rapports et à son équipe.

## 2. Direction (Paul Durieux)

- Ouvrir l'interface **NEOBATI – Pilotage › Direction – Tableau de bord**.
- Bloc « Chantiers ouverts » : nombre de chantiers, devis signés, coûts engagés, reste à facturer, tableau des **alertes** (retard, budget, acompte).
- Bloc « Rentabilité » : marge moyenne et marge par chantier **terminé** (la marge d'un chantier en cours est provisoire : regarder l'**écart budget**).
- Email « Chantiers à traiter ce matin » à 7 h 45 (S5) ; email immédiat si un chef de chantier coche « Problème signalé » (S2).
- Factures en retard de plus de 30 jours : **c'est vous qui décidez** de la suite (S4 ne relance pas le client à ce niveau).

## 3. Administratif (Zineb Durieux)

- Page **Administratif – Devis et factures** : factures non payées triées par retard, devis en attente triés par date d'expiration.
- À réception d'un paiement : FACTURES › renseigner **Date de paiement**, **Montant encaissé HT**, **Statut paiement = Payée**. Les relances s'arrêtent automatiquement.
- Nouveau devis : DEVIS › référence `DEV-AAAA-NNN`, lier Client et Chantier, Statut = Envoyé, Date de validité. La relance J-5 est automatique (2 maximum).
- Si un client refuse les relances : CLIENTS › cocher **Opposition aux relances**.
- **Chaque lundi (5 min)** : LOGS ERREURS › traiter les lignes non résolues ; Make › Historique.

## 4. Chargé d'affaires

- Reçoit par email chaque nouvelle demande (S1) ; la fiche client est déjà créée en « Prospect ».
- Renseigne POINTAGES et ACHATS (ou les fait saisir) : sans eux, la marge est fausse.
- Ajuste les textes des relances (prompts S3/S4) avec l'aide du guide des scénarios.

## 5. Chefs de chantier (3 binômes)

- Sur le téléphone : ouvrir le **formulaire « Rapport terrain »** (lien en favori), choisir le chantier, son nom, l'avancement, dicter les notes, ajouter les photos, cocher « Problème » si besoin. **1 minute.**
- Interface **NEOBATI – Terrain (artisans)**, page **Terrain – Mes étapes** : filtrer par chantier ou par responsable, voir les étapes à faire et celles en retard.
- Un email arrive à chaque nouvelle affectation (S6).
- Interdits : photos de documents personnels du client, informations de santé dans les notes.

## 6. Bonnes pratiques de maintenance

| Fréquence | Action | Qui |
|---|---|---|
| Hebdomadaire | LOGS ERREURS + historique Make | Zineb |
| Mensuelle | Consommation de crédits Make ; export CSV des tables ; contrôle des prospects à purger (« Date de purge RGPD ») | Paul / Zineb |
| À chaque modification | *Run once* de test + export du blueprint Make | Celui qui modifie |
| Annuelle | Rotation du jeton Airtable et des clés API ; revue des accès ; mise à jour du registre RGPD | Paul |
| Départ d'un salarié | Retrait immédiat des accès | Paul |

**Ne jamais** renommer un champ utilisé par Make (Alerte devis, Niveau de relance, Alerte pilotage, Traité par Make…) sans mettre à jour le scénario concerné.
