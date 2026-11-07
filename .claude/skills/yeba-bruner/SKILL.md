---
name: yeba-bruner
description: Processus brunérien appliqué aux formations YEBA — curriculum en spirale, trois modes de représentation (enactif → iconique → symbolique), étayage et ses 6 fonctions, apprentissage par la découverte. Utiliser pour construire une progression pédagogique, ordonner des notions complexes, rendre un sujet technique accessible, ou quand Aurélien parle de « Bruner », « spirale », « étayage », « progression ».
---

# Le processus brunérien — rendre le complexe apprenable

Sources : Bruner, J. S. (1960), *The Process of Education* (curriculum en
spirale) ; Bruner (1966), *Toward a Theory of Instruction* (modes de
représentation) ; Wood, Bruner & Ross (1976), « The role of tutoring in
problem solving » (étayage).

Principe de Bruner : **tout sujet peut être enseigné à tout public sous une forme
honnête**, si on choisit le bon mode de représentation. C'est la clé du
« terriblement technique mais vulgarisé ».

## 1. Les 3 modes de représentation — chaque notion les traverse dans l'ordre

| Mode | Le stagiaire… | En formation YEBA | Exemple : « un workflow d'IA » |
|---|---|---|---|
| **E – Enactif** (agir) | manipule, fait, vit | jeu, manipulation, jeu de rôle, atelier sur son poste | Les stagiaires se passent des fiches papier pour traiter une commande : ils **sont** le workflow |
| **I – Iconique** (voir) | voit une image, un schéma | schéma, infographie, vidéo, carte mentale | Schéma déclencheur → étapes → résultat, aux couleurs YEBA |
| **S – Symbolique** (abstraire) | manipule le langage, les règles, les formules | définition, vocabulaire technique, logique, code | Vocabulaire : déclencheur, webhook, API, condition, boucle |

Règle : **E → I → S**, jamais l'inverse. Commencer par la définition fait
décrocher un public non technique.

## 2. La spirale — revenir sur les notions, plus haut à chaque tour

```
Tour 1 (jour 1 matin)  : découvrir la notion        (E + I, Bloom 1-2)
Tour 2 (jour 1 après-midi) : l'utiliser sur un cas guidé (I + S, Bloom 3)
Tour 3 (jour 2)        : l'appliquer à SON entreprise  (S, Bloom 4-6)
```

Chaque tour reprend la notion précédente avant d'aller plus loin
(récupération en mémoire = meilleur ancrage). Dans le déroulé, marquer chaque
retour d'un 🔁.

## 3. L'étayage — les 6 fonctions du formateur (Wood, Bruner & Ross, 1976)

| Fonction | Ce que fait Aurélien | Exemple concret |
|---|---|---|
| 1. Enrôlement | donne envie, accroche | « Combien d'heures par semaine perdez-vous à recopier des devis ? » |
| 2. Réduction des degrés de liberté | simplifie la tâche | Il fournit le modèle de prompt, les stagiaires ne remplissent que 3 cases |
| 3. Maintien de l'orientation | garde le cap sur l'objectif | Rappel de l'objectif affiché en coin de diapo |
| 4. Signalisation des caractéristiques déterminantes | montre ce qui compte | « Regardez : c'est CE champ qui contient une donnée personnelle » |
| 5. Contrôle de la frustration | rassure, dédramatise l'erreur | « Cette erreur, 80 % des entreprises la font » |
| 6. Démonstration | montre le geste expert | Démonstration en direct, puis les stagiaires refont |

**Désétayage** : retirer l'aide progressivement (modèle complet → modèle à trous
→ page blanche) jusqu'à l'autonomie. Prévoir explicitement ce retrait dans le
déroulé.

## 4. Découverte guidée

Poser un problème réel **avant** de donner la solution ; laisser les stagiaires
chercher 5 à 10 min, puis structurer. Exemple : « Voici le fichier clients
d'un hôtel de Saint-Gilles. Trouvez tout ce qui pose problème RGPD. » Ensuite
seulement : le cours sur les données personnelles.

## 5. Sortie attendue de ce skill

Pour chaque notion clé : un tableau **Notion | Activité E | Support I | Formalisation S | Tours de spirale | Étayage prévu | Désétayage**.
