# Site YEBA FORMATIONS

Site vitrine animé (React + Framer Motion, compilé par Vite en site statique).

| Commande | Effet |
|---|---|
| `npm install` | installe les dépendances |
| `npm run dev` | aperçu en direct sur http://localhost:5173 |
| `npm run build` | site final dans `dist/` → à déposer chez l'hébergeur (cible : OVHcloud) |
| `npm run apercu` | un seul fichier `apercu/index.html`, médias inclus, pour relire hors ligne |
| `npm run sync` | **met à jour le catalogue depuis Airtable** (jeton `AIRTABLE_TOKEN` dans `.env`, lecture seule) |

## Connexion Airtable
Le site ne contacte jamais Airtable depuis le navigateur du visiteur : aucun jeton n'est exposé.
`npm run sync` lit la base « YEBA FORMATIONS - Centre de formation » et écrit `site/src/catalogue.json`, puis `npm run build`.
- **Publiées** : fiches « Active » dont la marque YEBA est obligatoire. **Jamais** de marque blanche (FOR-0005, FOR-0007).
- **Reprises d'Airtable** : durée, type, tarifs (bloc public auto), prérequis, modalités d'évaluation et d'accès,
  adaptations handicap, financements, indicateurs de résultats (RNQ indicateurs 1 et 2), sessions inter à venir.
- **Éditorial** (dans `data.js`) : nom court, accroche, mots-clés, badge, filtre. Une nouvelle fiche Airtable
  apparaît automatiquement, avec des valeurs par défaut, même sans éditorial.
- Jeton : créer un *personal access token* Airtable avec la seule portée `data.records:read`, limité à cette base.

## Où modifier quoi
- **Formations** : dans Airtable, puis `npm run sync`. **Accroches et mots-clés** : `site/src/data.js`.
- **Textes des sections** : `site/src/App.jsx`.
- **Couleurs, tailles** : `site/src/styles.css` (charte : bleu #1B3A6B, or #C9A84C — jamais d'or en texte sur blanc).
- **Pages légales** : `site/mentions-legales.html`, `site/confidentialite.html` — les zones jaunes « [À …] » sont à compléter **avant** la mise en ligne.

## Choix RGPD / accessibilité
- Aucun cookie, aucun traceur, aucune ressource externe (polices auto-hébergées) : pas de bandeau cookies nécessaire.
- Pas de formulaire : contact par téléphone ou e-mail (minimisation).
- Bouton « Confort de lecture » : taille du texte, contraste renforcé, pause des animations (préférences stockées dans le navigateur du visiteur uniquement).
- `prefers-reduced-motion` respecté ; polices Atkinson Hyperlegible (conçue pour les malvoyants) et Montserrat.
