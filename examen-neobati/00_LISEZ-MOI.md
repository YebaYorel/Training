---
title: "Dossier d'examen NEOBATI — sommaire"
---

**Candidat** : Aurélien LUMEKA · **Titre** : Product Builder No-Code (RNCP 39108, niveau 6) · **Cas** : Atelier NéoBâti (sujet École Cube « Déployer des systèmes automatisés — Airtable + Make + I.A »).

| Feuille | Fichier | Contenu |
|---|---|---|
| 1 | `01_Oral_20_minutes` | Déroulé minuté, texte technique + version simple, chiffres clés, limites |
| 2 | `02_Questions_examinateurs` | 10 questions / réponses + 3 questions à poser au jury |
| 3 | `03_Glossaire_Airtable` | Termes Airtable avec définitions |
| 4 | `04_Glossaire_Make` | Termes Make avec définitions |
| 5 | `05_Implementation_chez_le_client` | Schéma d'architecture, matériel, comptes au nom du client, cybersécurité, autonomie |
| 6 | `06_Scenarios_Make` | Connexion à Make, fiches S0 à S6, prompts, budget d'opérations |
| 7 | `07_Guide_utilisateur` | Guide par rôle + maintenance (livrable du sujet) |
| 8 | `08_Chiffres_et_pourquoi` | Les chiffres de l'annexe pas à pas ; pourquoi Airtable, Make, les liens, rollups et formules |
| 9 | `09_Failles_cybersecurite` | Audit de sécurité Airtable + Make (document sensible, hors dépôt public) |

## Ce qui est construit dans Airtable

- Base **« NEOBATI – Gestion des chantiers (v2 examen) »** : https://airtable.com/app66nfSc639ML85K
- Interface **NEOBATI – Pilotage** (publiée) : pages Direction et Administratif (bureau uniquement).
- Interface **NEOBATI – Terrain (artisans)** (publiée) : page « Terrain – Mes étapes », sans aucune donnée financière.
- Formulaires (créés **non publiés**, à relire puis publier) :
  - Nouvelle demande client : https://airtable.com/app66nfSc639ML85K/pagTGm4R3utpnTan3/edit
  - Rapport terrain : https://airtable.com/app66nfSc639ML85K/pagsoyynNuAxgALyV/edit
- Données de démonstration fictives (emails en `example.com`) : 5 clients, 5 chantiers, 5 devis, 6 factures, 6 pointages, 5 achats, 15 étapes, 10 ressources (9 personnes + 1 matériel). Tarifs : menuisier 45 €/h, peintre 40 €/h (annexe), électricien 40 €/h (hypothèse).

## Pourquoi une v2 plutôt que l'ancienne base « NEOBÂTI - Nantes (2015) »

L'ancienne base (conservée intacte) ne passait pas le critère « base relationnelle complète, cohérente et fonctionnelle » :

1. **Aucune relation** entre tables (le client d'un chantier était un simple texte) → aucun rollup, donc aucune marge possible.
2. Formule « Jours retard paiement » comparant à `"IMPAYEE"` alors que l'option s'appelle « Impayée » → toujours 0.
3. « Montant TTC » divisant une **sélection** (« 10% ») par 100 → résultat faux.
4. Formule « En retard » des étapes syntaxiquement incohérente.
5. Montant HT des factures en **dollars**.
6. Option « Arrêt maladie » = **donnée de santé** (RGPD art. 9) inutile.
7. Pas de table d'heures ni d'achats liée aux chantiers, pas d'interface, pas de formulaire.

## À faire de ton côté

- [ ] Ouvrir la base, vérifier l'affichage des formats (les champs calculés s'affichent sans décimales : régler l'affichage en € si souhaité).
- [ ] Relire puis publier les 2 formulaires.
- [ ] Créer ton compte Make (feuille 6, §0) et construire S2 + S4 en priorité (les plus démonstratifs à l'oral).
- [ ] Revérifier le jour de l'examen les tarifs Make et Airtable sur leurs sites officiels.
