# Compétences « agent-desktop » : provenance et règles YEBA

Ce fichier est propre à YEBA FORMATIONS. Il ne fait pas partie de l'œuvre copiée et ne la modifie pas.

## Origine et licence

- **Source** : https://github.com/vercel-labs/agent-desktop, version **1.3.0** (11/11/2026), commit
  `947b051fb7a03a797ad12b9bb942d4ffc6f91735` (12/11/2026). Copie faite le 13/11/2026.
- **Auteur et licence** : Vercel Labs, licence **Apache-2.0**. Le fichier `LICENSE` est joint ; l'amont n'a pas de
  fichier NOTICE.
- **Copié à l'identique** depuis le dossier `skills/` de l'amont, 4 compétences :
  - `agent-desktop` avec ses `references/` ;
  - `agent-desktop-windows` ;
  - `agent-desktop-macos` ;
  - `agent-desktop-linux`.
- **Fichiers YEBA séparés** : ce `PROVENANCE.md` et `mettre-a-jour.sh`.

## Ce qui a été relu avant l'installation (13/11/2026)

- **Les compétences** : uniquement de la documentation (Markdown), sans script, sans hook, sans clé.
- **Le programme** : un outil en ligne de commande écrit en Rust, sans modèle d'IA intégré. Il est prudent par
  défaut :
  - il agit par l'accessibilité du système, sans bouger la souris ni prendre le focus ;
  - les clics et la frappe physiques exigent l'option `--headed`.
- **L'installateur npm** télécharge le binaire de la version depuis les « Releases » GitHub de vercel-labs.

## Ce qui n'a pas été copié

- **`agent-desktop-ffi`** : bibliothèque C, utile seulement pour programmer avec agent-desktop.
- **`jev-desktop`** : elle exige une clé `TYPESAFE_API_KEY` d'un service tiers et le dépôt complet. Elle enverrait le
  contenu de l'écran à ce service.

## À quoi il sert chez YEBA

Il permet de piloter des applications de bureau **sur l'ordinateur d'Aurélien**, sans captures d'écran : lire une
fenêtre, cliquer, remplir un formulaire, naviguer dans les menus. Usages visés :
- automatiser des tâches répétitives dans des logiciels sans API, comme un logiciel de gestion de formation ou un
  portail ouvert dans une application ;
- préparer des fichiers Office.

Pour le web, préférer Playwright ou Chrome DevTools, déjà installés.

**Il ne fonctionne pas dans une session cloud**, faute de bureau. Il faut une session Claude Code ouverte sur
l'ordinateur.

## Installation sur l'ordinateur (une fois)

```bash
npm install -g agent-desktop@1.3.0
agent-desktop status                 # plateforme, autorisations, surfaces prises en charge
agent-desktop permissions --guide    # macOS : accorder « Accessibilité » au terminal
```

Sur macOS ou Linux, `brew install agent-desktop` fonctionne aussi.

## Garde-fous YEBA

- **Sécurité** : l'outil lit tout ce qui s'affiche, messagerie et dossiers clients compris, et peut cliquer ou taper.
  - Il reste en mode sans souris par défaut. Le mode `--headed` (souris et clavier physiques) demande l'accord
    explicite d'Aurélien pour la tâche en cours.
  - Fermer les fenêtres sensibles avant usage : banque, messagerie, dossiers de stagiaires.
  - Ne jamais lui faire saisir un mot de passe : Aurélien le tape lui-même.
  - Confirmation avant toute action irréversible : envoi, paiement, suppression.
- **RGPD** :
  - les instantanés, captures, presse-papiers et journaux contiennent des données personnelles ;
  - ils remontent dans la conversation Claude (Anthropic, États-Unis), ce qui est un transfert hors UE (chapitre V) ;
  - ne pas l'utiliser sur des écrans montrant des données de stagiaires ou de clients, sauf nécessité et base
    légale ;
  - ne jamais committer ces fichiers.
- **IA Act** :
  - agent-desktop n'a pas de modèle, c'est Claude qui agit ;
  - aucune décision qui a un effet sur une personne sans validation humaine : évaluer un stagiaire (annexe III,
    point 3) ou trier des candidatures (annexe III, point 4) relève du haut risque.

## Mettre à jour

Lancer `bash .claude/skills/agent-desktop/mettre-a-jour.sh`, puis relire le diff. Changer aussi la version dans la
commande `npm install` ci-dessus.
