---
title: "Feuille 3 — Glossaire Airtable"
---

Colonne « En simple » = la phrase à dire si l'examinateur demande « expliquez-le à un non-technicien ». 🔒 = point de cybersécurité.

| Terme | Définition technique | En simple |
|---|---|---|
| **Workspace** (espace de travail) | Conteneur de bases ; porte la facturation et les collaborateurs. | Le bâtiment qui contient les classeurs. |
| **Base** | Base de données relationnelle composée de tables ; identifiant `app…`. | Un classeur complet pour un sujet. |
| **Table** | Ensemble d'enregistrements d'un même type ; identifiant `tbl…`. | Un onglet du classeur. |
| **Enregistrement** (record) | Une ligne ; identifiant unique `rec…`. | Une fiche. |
| **Champ** (field) | Une colonne typée ; identifiant `fld…`. | Une case à remplir sur la fiche. |
| **Champ primaire** | Premier champ, nom affiché de l'enregistrement dans les liens. | Le titre de la fiche. |
| **Types de champs** | Texte, texte long, sélection unique/multiple, date, devise, pourcentage, case à cocher, email, téléphone, pièce jointe… | Le format de la case : un prix, une date, une photo. |
| **Sélection unique** (single select) | Liste fermée de valeurs (ex. statut). | Un menu déroulant : pas de faute de frappe possible. |
| **Lien vers une autre table** (linked record) | Relation entre tables ; crée un champ inverse automatique. | Une ficelle entre deux fiches. |
| **Relation 1-N / N-N** | Un-à-plusieurs (1 client → N chantiers) ; plusieurs-à-plusieurs (artisans ↔ chantiers). | Un client a plusieurs chantiers ; un artisan va sur plusieurs chantiers. |
| **Lookup** (recherche) | Affiche un champ d'un enregistrement lié. | Lire l'info au bout de la ficelle. |
| **Rollup** (agrégation) | Calcule sur les enregistrements liés : `SUM(values)`, `AVERAGE(values)`… | Additionner tout ce qui est au bout des ficelles. |
| **Count** | Nombre d'enregistrements liés. | Compter les ficelles. |
| **Formule** | Champ calculé (`IF`, `DATETIME_DIFF`, `TODAY()`, `ROUND`…). | Une calculatrice intégrée à la fiche. |
| **Created time / Last modified time** | Horodatage automatique ; requis par le déclencheur Make « Watch Records ». | Le tampon dateur. |
| **Vue** (view) | Présentation filtrée/triée/groupée d'une table : grille, kanban, calendrier, galerie, chronologie, formulaire. | Une paire de lunettes différente sur les mêmes données. |
| **Filtre / tri / regroupement** | Conditions d'affichage, ordre, sections. | Ne montrer que ce qui compte, dans le bon ordre. |
| **Vue verrouillée / personnelle** | Vue non modifiable par les autres / visible par son seul créateur. | Une vue que personne ne peut dérégler. |
| **Interface** (Interface Designer) | Application construite sur la base, avec pages et permissions propres. | Un tableau de bord sur mesure, plus simple que le classeur. |
| **Page de tableau de bord** | Page d'indicateurs : nombres, graphiques, grilles. | L'écran du patron. |
| **Élément « nombre » / graphique** | Indicateur agrégé (somme, moyenne) / barres, courbes, secteurs. | Un compteur, un graphique. |
| **Filtre de périmètre** (record scope) | Restriction fixée par le concepteur : les lignes exclues ne sont jamais envoyées à l'utilisateur. 🔒 | On ne montre jamais ce que la personne n'a pas à voir. |
| **Page de détail d'enregistrement** | Page qui affiche une fiche complète depuis une liste. | Ouvrir la fiche en grand. |
| **Formulaire** | Saisie qui crée un enregistrement, partageable par lien. | Un questionnaire qui remplit le classeur tout seul. |
| **Automatisation** | Déclencheur (création, mise à jour, condition, horaire) + actions (email, script, mise à jour). | « Quand ceci arrive, fais cela. » |
| **Exécuter un script** (Run a script) | Action JavaScript d'automatisation (ex. `fetch` vers un webhook Make) ; non disponible en offre gratuite. | Un petit programme qui sonne chez Make. |
| **Exécution d'automatisation** (run) | Chaque déclenchement compte dans le quota mensuel (100/mois en Free, 25 000 en Team). | Chaque coup de sonnette est compté. |
| **API REST** | Accès programmatique aux données ; limite ≈ 5 requêtes/s par base. | La porte de service pour les autres logiciels. |
| **Personal Access Token (PAT)** | Jeton d'accès limité par *scopes* et par base. 🔒 | Un badge qui n'ouvre qu'une porte précise. |
| **Scopes** | Droits du jeton : `data.records:read`, `data.records:write`, `schema.bases:read`… 🔒 | Ce que le badge a le droit de faire. |
| **OAuth** | Autorisation déléguée sans partager le mot de passe. 🔒 | Prêter sa voiture sans donner les clés de la maison. |
| **Rôles** | Owner, Creator, Editor, Commenter, Read-only. 🔒 | Qui peut tout changer, qui peut seulement regarder. |
| **Snapshot / historique de révisions** | Sauvegarde restaurable de la base ; historique par fiche. 🔒 | Revenir en arrière en cas d'erreur. |
| **Synchronisation** (sync) | Copie d'une table vers une autre base. | Un miroir d'onglet. |
| **Champ IA** (Airtable AI) | Champ généré par l'IA d'Airtable, à crédits. Non utilisé ici : l'IA passe par Make. | L'IA intégrée d'Airtable. |
| **Typecast** | Conversion automatique d'une valeur texte vers le type du champ lors d'une écriture API. | Airtable remet la donnée au bon format. |
| **Résidence des données UE** | Stockage des contenus en Europe (Francfort) — offre Enterprise Scale uniquement. 🔒 | Garder les papiers en Europe. |

*Sources : support.airtable.com ; limites des offres d'après les comparatifs 2026 (jetadmin.io, softr.io) — à revérifier sur airtable.com/pricing le jour de l'examen.*
