---
name: yeba-charte
description: Charte graphique officielle de YEBA FORMATIONS (bleu #1B3A6B, or #C9AB4C, noir #121212, blanc ; Montserrat Bold, Inter, Poiret One ; style « Cyber-Garage Premium »). À appliquer à TOUTE production visuelle pour YEBA — PowerPoint, PDF, documents Word, site web, visuels réseaux sociaux, e-mails, devis, propositions commerciales — sauf si Aurélien travaille pour un autre centre de formation.
---

# Charte YEBA FORMATIONS

Valeurs exactes, contrastes et règles : `.claude/skills/yeba-powerpoint/charte.json`
(source unique, à lire avant de produire).

## Quand l'appliquer

- **Par défaut** : toute production pour Aurélien.
- **Jamais** quand il cite un autre centre de formation : ni couleurs, ni logo,
  ni nom YEBA, ni métadonnées (le contrat l'interdit). Demander la charte de ce centre.

## Règles express

| Élément | Règle |
|---|---|
| Couleur dominante | Bleu `#1B3A6B` |
| Accents | Or `#C9AB4C` — **jamais en texte sur fond blanc** (contraste 2,2:1) |
| Fonds sombres | Noir `#121212` (texte blanc ou or) |
| Titres | Montserrat Bold |
| Texte | Inter |
| Poiret One | Décoratif, ≥ 54 pt, couverture d'une présentation d'entreprise uniquement |
| Images | « Cyber-Garage Premium » : fonds sombres, néons bleu/or, réseaux de points, motif 974 |
| Pictogrammes | Trait fin or, coins arrondis (RGPD, IA, cybersécurité, cloud) |
| Logo | Utiliser les fichiers fournis. Ne jamais le redessiner ni le générer par IA. Fichiers absents → demander |

## Par support

- **PowerPoint** → skill `yeba-powerpoint` (applique la charte + l'accessibilité).
- **Site web / HTML** → `yeba-tokens.css` (variables CSS). Polices **auto-hébergées**,
  jamais chargées depuis Google Fonts : charger une police depuis les serveurs de
  Google transmet l'adresse IP du visiteur aux États-Unis → **RGPD** (LG München,
  20/01/2022, 3 O 17493/20). Les 3 polices sont sous licence libre OFL.
- **Word / PDF** → titres Montserrat Bold bleu, texte Inter noir sur blanc,
  filets or uniquement décoratifs.
- **Fichiers .pptx/.docx** : Montserrat et Inter ne sont pas installées par défaut
  sur Windows → les incorporer au fichier ou prévoir le repli (Arial Black / Arial).

## Réflexes RGPD / IA Act

- **IA Act art. 50** : un visuel « Cyber-Garage » généré par IA qui montre une
  personne réaliste doit être signalé comme généré par IA.
- **RGPD / droit à l'image** : un portrait de personne réelle exige son accord écrit.
