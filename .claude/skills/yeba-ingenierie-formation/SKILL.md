---
name: yeba-ingenierie-formation
description: Chef d'orchestre de la conception d'une formation YEBA (intra, inter, CFA). À utiliser dès qu'Aurélien demande une formation, un module, un programme, un support, un « pack formation », un déroulé ou une progression. Enchaîne analyse du besoin → objectifs (Bloom) → progression (Bruner) → déroulé minute par minute → PowerPoint → ressource PDF → grille critériée → évaluation de 10 questions → indicateurs Qualiopi, avec vulgarisation et accessibilité handicap.
---

# Ingénierie de formation YEBA — de la demande au pack complet

Objectif : des formations **simples à produire pour Aurélien**, mais **techniques,
rigoureuses, magnifiques et vulgarisées** pour les stagiaires.

## Étape 0 — Cadrage (ne rien inventer : demander ce qui manque)

| Information | Obligatoire |
|---|---|
| Sujet + niveau visé | oui |
| Public (métier, niveau, nombre, handicaps connus) | oui |
| Format : intra / inter / CFA, présentiel / distanciel | oui |
| Nombre de jours, horaires, pauses | oui (Aurélien les donne) |
| Organisme : YEBA ou **autre centre** (alors aucune trace de YEBA) | oui |
| Lieu (hôtel, salle) et matériel | si présentiel |
| Prérequis, financement (OPCO, CPF…) | utile |

## Étape 1 — Chaîne de production (dans cet ordre)

1. **Besoin et positionnement** : questionnaire d'entrée (Qualiopi ind. 4 et 8).
2. **Objectifs opérationnels** → skill `yeba-bloom` (verbes observables, niveau
   Bloom, critère de réussite). Qualiopi ind. 5.
3. **Progression** → skill `yeba-bruner` (spirale, enactif → iconique →
   symbolique, étayage).
4. **Déroulé minute par minute** → skill `yeba-deroule-pedagogique`.
5. **Vulgarisation** de chaque notion technique → skill `yeba-vulgarisation`.
6. **PowerPoint** → skills `yeba-powerpoint` + `yeba-charte`.
7. **Ressource PDF complète** (le « livre » du stagiaire : tout le détail que le
   PowerPoint ne montre pas, exemples, glossaire, sources) → skill `pdf`/`docx`.
8. **Grille critériée** : 1 ligne par objectif ; 4 niveaux (non acquis / en
   cours / acquis / expert) décrits par des comportements observables.
9. **Évaluation de 10 questions** : au moins 1 question par objectif, niveaux
   Bloom variés (pas uniquement « mémoriser »), corrigé expliqué, 1 cas pratique.
10. **Satisfaction et suivi** → skill `yeba-donnees-formation` (à chaud, à froid,
    Kirkpatrick).

Contrôle de cohérence final (**alignement pédagogique**, Biggs 1996) :
chaque objectif doit avoir **une activité** qui l'entraîne **et une évaluation**
qui le mesure. Présenter ce tableau de contrôle à Aurélien.

## Indicateurs Qualiopi couverts par le pack

| Pièce | Indicateurs (référentiel national qualité) |
|---|---|
| Programme (objectifs, durée, prérequis, modalités, accessibilité) | 1, 5, 6 |
| Positionnement d'entrée | 4, 8 |
| Déroulé, supports | 6, 10 |
| Évaluations, grille | 11 |
| Adaptations handicap | 26 |
| Satisfaction, amélioration | 30, 32 |

## Accessibilité (Aurélien est référent handicap)

Pour chaque pack, ajouter une section « Adaptations possibles » : version gros
caractères, sous-titres, documents compatibles lecteur d'écran, temps majoré
pour l'évaluation, pauses supplémentaires. Ne **jamais** stocker la nature d'un
handicap sans nécessité : c'est une **donnée de santé** (RGPD art. 9).

## Réflexes RGPD / IA Act

- **IA Act, annexe III point 3** : une IA qui **évalue les acquis** ou oriente/admet
  des apprenants est un système **à haut risque**. Claude peut aider à rédiger
  l'évaluation, mais la **correction et la décision restent humaines**
  (Aurélien), et cela doit être écrit dans le programme.
- **RGPD** : exemples avec personnes fictives, aucune donnée réelle de stagiaire
  dans les supports.
