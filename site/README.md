# Site YEBA FORMATIONS

Site vitrine animé (React + Framer Motion, compilé par Vite en site statique).

| Commande | Effet |
|---|---|
| `npm install` | installe les dépendances |
| `npm run dev` | aperçu en direct sur http://localhost:5173 |
| `npm run build` | site final dans `dist/` → à déposer chez l'hébergeur (cible : OVHcloud) |
| `npm run apercu` | un seul fichier `apercu/index.html`, médias inclus, pour relire hors ligne |

## Où modifier quoi
- **Formations, coordonnées, certifications** : `site/src/data.js` (repris d'Airtable, table CATALOGUE FORMATIONS / CONFIG SYSTEME).
- **Textes des sections** : `site/src/App.jsx`.
- **Couleurs, tailles** : `site/src/styles.css` (charte : bleu #1B3A6B, or #C9A84C — jamais d'or en texte sur blanc).
- **Pages légales** : `site/mentions-legales.html`, `site/confidentialite.html` — les zones jaunes « [À …] » sont à compléter **avant** la mise en ligne.

## Choix RGPD / accessibilité
- Aucun cookie, aucun traceur, aucune ressource externe (polices auto-hébergées) : pas de bandeau cookies nécessaire.
- Pas de formulaire : contact par téléphone ou e-mail (minimisation).
- Bouton « Confort de lecture » : taille du texte, contraste renforcé, pause des animations (préférences stockées dans le navigateur du visiteur uniquement).
- `prefers-reduced-motion` respecté ; polices Atkinson Hyperlegible (conçue pour les malvoyants) et Montserrat.
