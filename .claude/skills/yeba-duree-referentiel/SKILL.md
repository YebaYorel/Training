---
name: yeba-duree-referentiel
description: Calcule la durée de formation à partir d'un référentiel (RNCP, RS, REAC, RE/RC, REV ou syllabus client) pour la section « Missions & contrats » d'Airtable, quand cette durée n'est pas claire. Lit la fiche (France compétences, Vocaneo), découpe en blocs et compétences, applique une méthode écrite et vérifiable, compare aux heures du contrat, écrit le résultat et la méthode dans MISSIONS & CONTRATS, puis propose de lancer la réalisation de la formation.
---

# Durée d'une formation à partir de son référentiel

Table MISSIONS & CONTRATS `tbl1gThEYdf0xZAaV` : champs « Type de référentiel »,
« Code fiche (RNCP / RS) », « Durée calculée par Claude (h) », « Méthode de calcul de
la durée », « Écart contrat / référentiel (h) » (formule automatique).

## Ce qu'il faut savoir (pour l'expliquer simplement à Aurélien)

| Référentiel | Ce qu'il dit de la durée |
|---|---|
| **RNCP** (titres, diplômes) | La fiche France compétences ne fixe **pas** de durée : elle décrit des blocs de compétences. La durée est choisie par l'organisme, justifiée par le positionnement (Qualiopi ind. 4). |
| **RS** (répertoire spécifique) | Idem, mais compétences plus courtes et ciblées (souvent 7 à 70 h). |
| **REAC / RC** (titres professionnels du ministère du Travail) | Le REAC décrit activités et compétences ; le RC (référentiel de certification) décrit les épreuves. Les durées « indicatives » publiées par l'AFPA ou les arrêtés de titre servent de repère, pas d'obligation. |
| **RE / REV** | Référentiel d'évaluation : il donne la durée des **épreuves** (mise en situation, entretien, dossier) : à ajouter au temps de formation. |
| **Syllabus client** | Le donneur d'ordre fixe souvent les heures : on vérifie seulement qu'elles suffisent. |

Source à citer : fiche officielle sur francecompetences.fr (hôte autorisé dans l'environnement) ou outil MCP Vocaneo `get_certification` / `search_certifications`.

## Méthode de calcul (toujours écrite dans Airtable)

1. Lister blocs → compétences (C1.1, C1.2…) → critères d'évaluation, depuis la fiche officielle.
2. Pondérer chaque compétence selon son niveau de Bloom visé :
   - mémoriser / comprendre : 3 à 4 h ;
   - appliquer : 5 à 7 h ;
   - analyser / évaluer / créer (étude de cas, projet) : 7 à 14 h.
3. Ajouter : positionnement d'entrée (1 à 2 h par bloc), évaluations formatives (10 % du total), épreuves certificatives (durées du RE/RC), accompagnement du dossier professionnel si exigé.
4. Ajuster au public : débutants +20 %, public expérimenté ou VAE partielle −20 % (à justifier par le positionnement).
5. Arrondir à la demi-journée (3,5 h) ou à la journée (7 h) supérieure.
6. Résultat = fourchette basse / haute + valeur retenue. Écrire dans « Méthode de calcul » : la fiche (code, date de la version), le tableau compétence → heures, les ajouts, l'ajustement.

## Contrôle avec le contrat

- Comparer à la durée du contrat (heures par jour × nombre de dates, déjà dans la ligne). L'écart s'affiche seul.
- Écart > 15 % : le signaler à Aurélien avec la conséquence (contrat trop court = risque de non-réussite et de reproche Qualiopi ; trop long = tarif à revoir).
- Ne **jamais** modifier les heures contractuelles : seul Aurélien négocie.

## Ensuite

Proposer de créer la ligne correspondante dans RÉALISATION DE FORMATION (liée à la mission) pour produire le pack avec `yeba-realisation-formation`. Ligne de preuve dans JOURNAL DES PREUVES (section « Missions & contrats », type « Calcul »).

Réflexe conformité : **Qualiopi** ind. 1 (information sur la durée), 4 (positionnement), 5 (objectifs) ; **RGPD** : aucun ; **IA Act** : aucun, sauf si un outil d'IA trie ou note les candidats (alors haut risque, annexe III, point 3).
