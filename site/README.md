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

## Section publique « Qualiopi : la preuve, pas la promesse »

`npm run sync` (ou `sync-export`) écrit aussi `site/src/documents.json` depuis la table DOCUMENTS OFFICIELS.
Règle de publication appliquée par le script, jamais par le site :

- un document n'est listé que s'il s'adresse à l'extérieur (Public, Prospects, Stagiaires, Clients entreprises) ;
- texte intégral lisible en ligne **seulement** si « En vigueur » ET sans aucun marqueur de travail
  (« à vérifier », « à compléter », « [ … ] », « Action A-… », « interne », ⚠️…) ; sinon « Recevoir le document » (courriel) ;
- mentions légales et confidentialité renvoient vers les pages du site (versions à jour) ;
- aucun statut interne (incomplet, à valider, score d'auto-audit) n'est jamais publié.

`site/src/rnq.json` contient la synthèse publique des 33 indicateurs (le texte du décret fait foi).

## Espace YEBA (privé) — Coffre Qualiopi, Parcours, BPF

Outil de pilotage **local**, jamais déployé (absent de `npm run build`, bloqué par `.htaccess`).

```bash
npm run espace          # http://127.0.0.1:5180 — démo fictive, ou vos données si AIRTABLE_TOKEN est dans .env
npm run espace:apercu   # fichier HTML autonome de démonstration (données fictives uniquement)
```

- Jeton Airtable : portée **data.records:read** uniquement, sur la seule base YEBA. Il reste dans `.env`,
  est ajouté par le proxy local côté serveur et n'arrive jamais dans le navigateur.
- Le proxy n'accepte que : GET, la base appQ2zqc80kkc6MR1, 10 tables listées, requêtes de la page elle-même
  (même origine, hôte 127.0.0.1/localhost). Tout le reste répond 403/405.
- Minimisation RGPD : ni email, ni téléphone, ni date de naissance, ni aménagements des apprenants ne sont lus.
- BPF : **préparation**. Rubriques à contrôler avec la notice cerfa n° 50199 avant télédéclaration
  sur Mon Activité Formation (avant le 31 mai N+1).

## YEBA Studio (logiciels vendus aux organismes de formation)

- Code : `site/espace/` (même application que l'Espace YEBA interne). Publication : `npm run build:tout` → le site dans `dist/`, le logiciel dans `dist/studio/`.
- Modes : **démo** (fictive), **espace client** (données chiffrées AES-256 sur le PC, code personnel 8 à 12 chiffres + clé de secours), **interne** (Airtable, seulement sur votre poste avec `npm run espace`).
- Licences : signées Ed25519, liées au code poste, vérifiées hors ligne. `npm run licence -- cles` (une seule fois, sur VOTRE poste), puis `npm run licence -- emettre …`.
- Paiement et IA : `serveur/` (voir serveur/README.md). Sans serveur : commande par e-mail + lien de paiement Mollie.
- Prix : `site/espace/src/licence.js` (OFFRES) — c'est la seule source ; le site, IFA et le serveur la lisent.

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

## Sécurité — à respecter à chaque mise en ligne
1. **Envoyer uniquement le contenu de `dist/`** chez OVH (jamais le dépôt entier). Le fichier `dist/.htaccess` doit être présent :
   il impose HTTPS, la politique de sécurité du contenu (CSP), l'interdiction d'intégrer le site dans une autre page,
   et rend introuvables les fichiers cachés (`.git`, `.env`) et de développement.
2. **HSTS** : n'activer la ligne `Strict-Transport-Security` qu'une fois le certificat HTTPS actif (sinon le site devient inaccessible).
3. **Rappels IFA** : quand `VITE_RAPPEL_ENDPOINT` est défini, ajouter son origine à `connect-src` dans `.htaccess`,
   et **limiter le débit côté serveur** (n8n / Baserow). Le champ piège et le délai de 3 s ne suffisent pas contre un robot déterminé.
4. **Comptes** : double authentification sur GitHub, OVH, Gmail, Airtable (condition de la garantie cyber Hiscox).
5. **Dépendances** : `npm audit` avant chaque mise en ligne ; `npm ci` (versions verrouillées) plutôt que `npm install`.
6. Tester en local avec les mêmes en-têtes : `npm run build && npm run preview`.
