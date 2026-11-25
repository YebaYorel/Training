---
name: yeba-realisation-formation
description: Section « Réalisation de formation » d'Airtable. Aurélien écrit un sujet et un temps de formation (dates facultatives) dans la table RÉALISATION DE FORMATION ou dans la conversation ; le skill pose D'ABORD la question « aux couleurs de YEBA FORMATIONS ou pour un autre centre ? », recommande TOUS les objectifs pédagogiques du sujet, puis produit le pack complet (PowerPoint qui répond à chaque objectif, grille critériée, quiz de 10 questions + corrigé, ressource complète Word ou PDF) via yeba-ingenierie-formation, et dépose les liens et la preuve dans Airtable.
---

# Réalisation de formation — de la ligne Airtable au pack livré

Base `appQ2zqc80kkc6MR1` · table RÉALISATION DE FORMATION `tblPrqJqluoHMbK5x` ·
JOURNAL DES PREUVES `tblmdeNVCQhf9NW4T` · MISSIONS & CONTRATS `tbl1gThEYdf0xZAaV`.

## Étape 0 — Les questions, avant toute production

Poser ces questions en un seul message (outil de question si disponible), sans rien supposer :

1. **« Est-ce pour YEBA FORMATIONS (charte, logo) ou pour un autre centre (marque blanche, aucune trace de YEBA) ? »** Toujours en premier, même si la ligne semble évidente. Autre centre → demander son nom et s'il a une charte imposée.
2. Durée : reprendre celle de la ligne. Absente → la demander. Une mission liée a un référentiel → proposer la durée calculée (skill `yeba-duree-referentiel`).
3. Horaires, jours et pauses : ceux d'Aurélien, jamais supposés (CLAUDE.md).
4. Public, niveau, nombre, handicaps connus ; format (intra, inter, CFA, distanciel).
5. Ressource finale : Word, PDF ou les deux.

Écrire la réponse dans la ligne (« Aux couleurs de YEBA ? », etc.) et passer le statut à « En production ». En attendant la réponse : statut « Question posée à Aurélien ».

## Étape 1 — Objectifs pédagogiques complets

- Lister **tous** les objectifs du sujet (pas trois au hasard) : un objectif général + les objectifs opérationnels qui couvrent le sujet de bout en bout, via `yeba-bloom` (verbe observable, condition, critère de réussite, niveau de Bloom).
- Le nombre d'objectifs doit tenir dans la durée : environ 1 objectif opérationnel par tranche de 1 h 30 à 2 h, évaluation comprise. Sujet trop large pour la durée → le dire et proposer un découpage ; ne pas comprimer en silence.
- Écrire la liste dans « Objectifs pédagogiques (Bloom) ».

## Étape 2 — Le pack (chaîne `yeba-ingenierie-formation`)

Ordre imposé : `yeba-bruner` → `yeba-deroule-pedagogique` → `yeba-vulgarisation` → `yeba-powerpoint` + `yeba-charte` (ou charte neutre si marque blanche) → ressource (`anthropic-skills:docx` et/ou `anthropic-skills:pdf`) → grille critériée → quiz de 10 questions.

Règles d'alignement (Biggs) vérifiées avant livraison :
- chaque objectif a **au moins une slide** qui l'enseigne (numéros de slides notés) ;
- chaque objectif a **une ligne dans la grille** (4 niveaux observables) ;
- chaque objectif a **au moins une question** du quiz ; niveaux de Bloom variés ; corrigé expliqué ;
- la ressource reprend tout le détail que le PowerPoint ne montre pas (exemples, glossaire, sources).

Écrire le tableau « objectif → slides → ligne de grille → questions » dans « Tableau d'alignement ».

## Étape 3 — Rangement et preuve

- Fichiers produits dans `livrables-prives/<sujet>/` (ignoré par Git : dépôt public, propriété intellectuelle).
- Déposer sur Google Drive si Aurélien le souhaite, puis coller les liens dans les colonnes « Lien … ».
- Statut « Livré » ; JOURNAL DES PREUVES : « Formation produite — <sujet> », volets Qualiopi (ind. 5, 6, 11) et, si le sujet touche l'IA ou des données, RGPD / IA Act.
- Marque blanche : vérifier qu'aucun fichier (y compris propriétés du document et noms de fichiers) ne contient « YEBA ».

## Réflexe conformité

- **Qualiopi** : objectifs, durée, modalités d'évaluation, accessibilité = indicateurs 1, 5, 6, 11, 26.
- **IA Act art. 4** : toute formation à l'IA sert de preuve de « maîtrise de l'IA » pour le client : le signaler sur l'attestation.
- **RGPD** : aucune donnée réelle de stagiaire ou de client dans les exemples (données fictives).
