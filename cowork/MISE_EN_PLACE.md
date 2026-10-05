# Mettre Cowork au travail sur vos financements — pas à pas

Objectif : Cowork (Claude sur votre ordinateur) va lui-même sur les sites des
financeurs, télécharge les règles et formulaires, les range, surveille les
changements et prépare vos dossiers. **Vous gardez la main sur les connexions,
les signatures et les envois.**

> Les noms exacts des menus peuvent évoluer ; en cas de doute, la page d'aide
> officielle est : https://support.claude.com (rechercher « Cowork »).

## Étape 1 — Installer (15 min)
1. Installer l'application **Claude pour ordinateur** (Windows ou Mac) depuis claude.com/download et se connecter avec le compte **aurelienlumeka@gmail.com**.
2. Ouvrir l'onglet **Cowork**.
3. Installer l'extension **Claude in Chrome** (claude.com/claude-in-chrome) et l'associer au même compte : c'est elle qui permet à Cowork de naviguer sur les sites des financeurs et de télécharger les PDF.
   Source : [claude.com/blog/cowork-chrome-side-panel](https://claude.com/blog/cowork-chrome-side-panel) · [support.claude.com – Cowork](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile)

## Étape 2 — Créer le dossier de travail (5 min)
Sur votre ordinateur : `Documents/YEBA-Financements/` avec les sous-dossiers
décrits dans le skill (00_Dossier_permanent … 99_Veille). Dans Cowork, **autoriser
l'accès à ce dossier uniquement** (pas à tout le disque).
Copiez-y `financements/README.md` (le guide) depuis le dépôt.

## Étape 3 — Installer le skill « financements-yeba » (5 min)
1. Compresser le dossier `cowork/financements-yeba/` en **financements-yeba.zip** (le fichier SKILL.md doit être à l'intérieur du dossier compressé).
2. Dans Claude : **Paramètres → Capacités → Skills → Importer un skill** → choisir le zip → activer.
3. Test : dans Cowork, écrire « Quelles pièces me faut-il pour un dossier AKTO ? » → Cowork doit citer le skill et les sources.

## Étape 4 — Vous connecter vous-même aux portails (une fois, 30 min)
Cowork ne doit **jamais** connaître vos mots de passe. Dans Chrome, connectez-vous
vous-même (et laissez la session ouverte quand vous lancez une tâche) :
| Portail | Adresse | Pour |
|---|---|---|
| EFP Connect / Mon Activité Formation | via of.moncompteformation.gouv.fr | BPF, EDOF |
| EDOF | https://of.moncompteformation.gouv.fr | CPF |
| Formanoo (Carif-Oref Réunion) | https://web.reunionprospectivecompetences.org | France Travail, visibilité |
| OPCO EP « Mes services en ligne OF » | https://www.opcoep.fr | paiements OPCO EP |
| myAtlas | https://www.opco-atlas.fr/prestataire/espace-organisme-formation.html | paiements Atlas |
| Portail des aides Région | https://aides.regionreunion.com/reunion-portail/ | Région |
| URSSAF, impots.gouv | espaces professionnels | attestations du dossier permanent |

## Étape 5 — Programmer les tâches automatiques (5 min)
Dans Cowork, taper `/schedule` (ou menu **Tâches planifiées**) et créer :

**Tâche 1 — « Veille financements » — mensuelle, le 1er du mois à 7 h**
> Utilise le skill financements-yeba, tâche A : veille mensuelle complète. Télécharge les documents officiels dans YEBA-Financements, mets à jour 99_Veille/veille.md et produis le rapport du mois. Ne soumets rien.

**Tâche 2 — « Pièces qui expirent » — hebdomadaire, le lundi à 7 h**
> Utilise le skill financements-yeba : vérifie dans 00_Dossier_permanent les dates de validité (URSSAF 6 mois, Kbis 3 mois, Qualiopi, assurance) et liste ce qui expire dans les 45 jours, avec le lien pour renouveler.

**Tâche 3 — « Échéances réglementaires » — mensuelle**
> Liste les échéances des 60 prochains jours : BPF (avant le 31 mai), déclaration de sous-traitance EDOF (1er mai – 30 septembre), audit Qualiopi, dates limites des appels à projets Région / Département / FSE+ trouvés.

Source fonctionnalités (tâches planifiées, skills, connecteurs) : [datacamp.com – tutoriel Cowork](https://www.datacamp.com/tutorial/claude-cowork-tutorial) · [nextstart.ai – configurer Cowork (sept. 2026)](https://www.nextstart.ai/2026/06/30/configurer-claude-cowork/).

## Étape 6 — Utilisation au quotidien (exemples de demandes)
- « Prépare le dossier OPCO pour un cabinet d'expertise comptable de 12 salariés, formation IA de 14 h en novembre » → Cowork identifie Atlas, télécharge la grille de la branche, prépare convention + programme + email au client.
- « Pré-remplis ma demande d'enregistrement Formanoo » → Cowork remplit, s'arrête, vous vérifiez et envoyez.
- « Qu'est-ce qui a changé ce mois-ci dans les règles OPCO ? »

## Ce que Cowork fera / ne fera pas
| Fera | Ne fera pas (volontairement) |
|---|---|
| Lire les pages publiques, télécharger les PDF, les ranger, les comparer | Se connecter avec vos identifiants FranceConnect / ProConnect |
| Préparer conventions, programmes, emails, tableaux de suivi | Signer, envoyer un formulaire, payer |
| Pré-remplir des formulaires pendant que vous êtes connecté | Traiter les données personnelles des stagiaires (RGPD) |
| Vous alerter des échéances et des changements de règles | Inventer une règle introuvable : il écrit « NON TROUVÉ » |

## RGPD / IA Act
- **RGPD** : Cowork travaille en local mais les contenus traités transitent par Anthropic (États-Unis). Limitez-le aux documents publics et aux documents d'entreprise de YEBA ; aucune pièce d'identité ni donnée de stagiaire. Inscrivez « Veille et préparation administrative assistée par IA » à votre registre.
- **IA Act art. 4** : vous utilisez un système d'IA dans votre activité → documentez l'outil et votre formation à son usage (preuve de « mesures de maîtrise de l'IA »). Le système ne prend aucune décision sur des personnes : pas de haut risque.
