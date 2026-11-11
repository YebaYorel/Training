---
name: yeba-donnees-formation
description: Extraction et traitement des données de formation YEBA — questionnaires de positionnement, évaluations, satisfaction à chaud et à froid (Kirkpatrick), émargements, exports Excel/Google Forms/PDF ; nettoyage, anonymisation, indicateurs Qualiopi (satisfaction, réussite, abandon, progression), tableaux de bord, stockage dans Baserow (UE). Utiliser pour « extraire les données », « analyser les évaluations », « résultats de formation », « bilan », « indicateurs », « taux de satisfaction ».
---

# Données de formation : extraire, traiter, prouver

## 1. Ce qu'on collecte (et seulement ça : minimisation RGPD)

| Donnée | Pourquoi | Base légale RGPD | Conservation conseillée* |
|---|---|---|---|
| Émargements | preuve de réalisation (Qualiopi, financeurs) | obligation légale / contrat | durée exigée par le financeur |
| Positionnement d'entrée | adapter la formation (Qualiopi ind. 8) | contrat | durée de la formation + 1 an |
| Évaluation des acquis | mesurer l'atteinte des objectifs (ind. 11) | contrat | idem |
| Satisfaction à chaud / à froid | amélioration continue (ind. 30, 32) | intérêt légitime | 3 ans, **anonymisée** si possible |
| Besoin d'adaptation handicap | accessibilité (ind. 26) | **donnée de santé (art. 9)** : consentement explicite | durée strictement nécessaire |

*Durées indicatives à valider par Aurélien selon ses contrats et financeurs :
**ne pas les présenter comme une obligation légale chiffrée**.

## 2. Extraction (de quoi à quoi)

| Source | Méthode |
|---|---|
| Excel / CSV / export Google Forms | pandas (`read_excel`, `read_csv`), skill `xlsx` |
| PDF d'évaluations remplis | skill `pdf` (extraction de texte et de champs de formulaire) |
| Feuilles papier scannées | transcription manuelle ou OCR **local** ; pas d'envoi à un service d'OCR hors UE |
| Baserow (base YEBA) | MCP `baserow` : `list_rows` |

Avant tout traitement :
1. **Anonymiser ou pseudonymiser** : remplacer nom/prénom par un identifiant
   (S01, S02…) ; la table de correspondance reste chez Aurélien, hors du dépôt Git.
2. Ne jamais committer les fichiers de données (le dépôt est **public**).

## 3. Traitement (les indicateurs qui comptent)

| Indicateur | Calcul |
|---|---|
| Taux de satisfaction | réponses « satisfait » + « très satisfait » / répondants |
| Taux de réussite | stagiaires ayant atteint le seuil / stagiaires évalués |
| Progression | score de fin − score de positionnement (moyenne et par objectif) |
| Taux d'abandon | (inscrits − ayant terminé) / inscrits |
| Taux de réponse | répondants / stagiaires |
| Atteinte par objectif | % de réussite aux questions liées à chaque objectif Bloom |

Toujours afficher **l'effectif (n)** à côté d'un pourcentage : « 100 % (n = 3) » ne
vaut pas « 92 % (n = 48) ».

Lecture **Kirkpatrick** (4 niveaux) : 1. Réaction (satisfaction) ·
2. Apprentissage (acquis) · 3. Comportement (mise en pratique, à froid
1 à 3 mois après) · 4. Résultats (impact pour l'entreprise : temps gagné,
CA, erreurs évitées). Le niveau 4 est **l'argument commercial** d'Aurélien
auprès des PME : le mesurer quand c'est possible.

## 4. Restitution

- Tableau de bord (skills `xlsx`, `data:build-dashboard`), aux couleurs YEBA.
- Bilan de session d'une page pour le client, et version anonymisée pour la
  communication commerciale.
- Questions ouvertes : regrouper par thèmes, citer des verbatims
  **anonymisés**.

## 5. Réflexes RGPD / IA Act (obligatoires)

- **RGPD** : finalité écrite, minimisation, pseudonymisation, durée de
  conservation, information des stagiaires (mention dans la convocation).
- **IA Act, annexe III point 3 b)** : utiliser une IA pour **évaluer les acquis
  d'apprentissage** = système **à haut risque**. Claude peut calculer des
  statistiques agrégées et proposer une analyse, mais la **note et la
  validation individuelle restent une décision humaine** (Aurélien).
- Stockage : Baserow cloud UE (Pays-Bas). Pas de données de stagiaires dans
  un outil hébergé hors UE.
