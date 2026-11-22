---
name: yeba-powerpoint
description: Crée ou améliore un PowerPoint (.pptx) de formation ou de présentation d'entreprise pour YEBA FORMATIONS — ultramoderne, transitions Morph/Prisme/Vortex, et accessible à un public malvoyant ou en situation de handicap (gros caractères, mots-clés, fort contraste, aucun mot coupé, aucune ligne qui traverse le texte). Utiliser pour tout « PowerPoint », « diaporama », « slides », « présentation » ou « support de formation » demandé par Aurélien.
---

# PowerPoint YEBA — moderne ET accessible

## 0. Avant de produire (questions obligatoires si l'info manque)

1. **Pour quel organisme ?** Si Aurélien ne précise rien → charte YEBA FORMATIONS.
   S'il cite un **autre centre de formation** → **aucune mention de YEBA
   FORMATIONS** (ni logo, ni nom, ni pied de page, ni métadonnées « Auteur » du
   fichier) : le contrat l'interdit. Demander alors la charte de ce centre.
2. **Couleurs / polices** : lire `charte.json`. Toute valeur `null` = **demander**
   les codes exacts. Ne jamais inventer une couleur « qui ressemble ».
3. Sujet, public (niveau, handicaps connus), nombre de jours, horaires, pauses
   (Aurélien les donne : ne pas les supposer).

## 1. Règles de fond (non négociables)

| Règle | Valeur |
|---|---|
| Titres | ≥ 40 pt, gras |
| Texte | ≥ 28 pt (jamais < 24 pt) |
| Contenu | **mots-clés**, pas de phrases : ≤ 6 mots par ligne, ≤ 20 mots par diapo |
| Contraste | ≥ 4,5:1 (WCAG 2.1 AA), viser 7:1 (AAA) |
| Polices | sans empattement, pas d'italique long, pas de MAJUSCULES sur plus de 3 mots |
| Mots | jamais coupés en fin de ligne (zone assez large, césure désactivée) |
| Lignes / formes | ne traversent **jamais** un texte |
| Images | texte alternatif rempli (lecteurs d'écran) |
| Couleur | jamais seule porteuse de sens (ajouter icône ou mot) |
| Format | 16:9, une idée par diapo, ordre de lecture logique |

Exemples « saisissants » : un exemple concret réunionnais par notion clé
(commerce de Saint-Pierre, hôtel de l'Ouest, PME du BTP à Saint-Denis…),
présenté en gros visuel + 3 mots, le détail allant dans les notes du formateur.

## 2. Fabrication

1. Construire le .pptx avec le skill **pptx** d'Anthropic (`anthropic-skills:pptx`)
   ou python-pptx, en fixant **explicitement** chaque taille de police.
2. Nommer les objets récurrents avec le préfixe `!!` (ex. `!!titre`, `!!logo`)
   pour que Morph les anime d'une diapo à l'autre.
3. Ajouter les transitions :
   ```bash
   python .claude/skills/yeba-powerpoint/scripts/transitions.py entree.pptx sortie.pptx \
     --defaut morph --diapo 1:vortex --diapo 8:prisme
   python .claude/skills/yeba-powerpoint/scripts/transitions.py --liste
   ```
   Doser : Morph partout + 2-3 effets forts (ouverture, changement de module,
   conclusion). Trop d'effets fatiguent et gênent les personnes sensibles au
   mouvement / épileptiques → éviter `vortex` et `nid-abeille` si le public
   n'est pas connu, proposer une version « sans animation ».
4. Contrôler :
   ```bash
   python .claude/skills/yeba-powerpoint/scripts/verifier_accessibilite.py sortie.pptx
   ```
   Corriger toutes les ERREURS, puis les ALERTES pertinentes.
5. Vérifier visuellement : `soffice --headless --convert-to pdf sortie.pptx`
   puis regarder chaque page (LibreOffice affiche les effets modernes en fondu,
   c'est normal : le rendu Morph se voit dans PowerPoint 2019+ / Microsoft 365).

## 3. Variante « ultramoderne web »

Pour une présentation à l'écran très animée (salon, pitch, public exigeant),
proposer aussi le skill **frontend-slides** (HTML animé, plein écran) — en
conservant les mêmes règles d'accessibilité et en respectant
`prefers-reduced-motion`. Le .pptx reste le livrable de référence
(Qualiopi : support remis au stagiaire).

## 3 bis. Illustrations explicatives : skill `anatomy`

Quand une diapo ou une ressource doit **expliquer un mécanisme** (un flux de
données, un workflow d'IA, le circuit d'un document RGPD…), proposer d'abord
`anatomy` (figure isométrique SVG « objet réel », exportable en PNG/PDF A4).
Il est installé hors dépôt (`npx skills add wheresryan22/anatomy -g -a claude-code`,
MIT, commit audité `1482e84`) : le réinstaller en début de session si absent.

Garde-fous **propres à notre public** (les exemples fournis ne les respectent pas) :

| Point | Règle |
|---|---|
| Contraste | Les figures d'origine sont gris clair sur blanc cassé : **illisibles** pour un public malvoyant. Utiliser le thème **sombre** ou renforcer les traits, puis mesurer le contraste (≥ 4,5:1). Si impossible → schéma en formes natives PowerPoint. |
| Marques | Ne jamais garder un logo ou une marque tiers dans une figure (l'exemple `desk-computer` affiche le logo d'un éditeur d'IA). |
| Texte | Mots dans la figure ≥ 24 pt une fois insérée ; `anatomy` évite le texte dans le dessin : légender dans la diapo, pas dans l'image. |
| Format | Insérer le **PNG** (`scripts/capture.mjs`, `--scale 2`) avec **texte alternatif** rempli ; garder la source SVG/HTML hors dépôt. |
| Organisme | Autre centre de formation → la carte « Fig n » et tout nom propre de l'outil sont retirés ; aucune mention de YEBA. |
| Taille | Une figure « Figure » (40-80 pièces) peut prendre ~1 h : annoncer le délai ; sinon schéma natif. |
| Publication | Ne **jamais** publier vers la galerie communautaire sans « oui » explicite (`references/publish.md`). |

## 4. Livrables d'une formation (rappel)

PowerPoint + grille critériée + ressource PDF complète + évaluation de
10 questions, au niveau demandé.

## 5. Réflexes RGPD / IA Act à signaler

- **RGPD** : aucune donnée personnelle réelle de stagiaire ou de client dans les
  exemples (prénoms fictifs) ; images de personnes = droit à l'image.
- **IA Act art. 50** : si des visuels/vidéos sont générés par IA et
  représentent des personnes ou lieux réels de façon réaliste, l'indiquer
  (« image générée par IA »).
- Dépôt GitHub **public** : ne pas committer les .pptx/.pdf clients (déjà
  ignorés par `.gitignore`).
