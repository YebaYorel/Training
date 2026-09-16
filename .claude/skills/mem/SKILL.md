---
name: mem
description: Mémoire hiérarchique persistante entre sessions, stockée en local dans ~/.claude/memory/. Utiliser pour conserver les préférences de travail, les décisions techniques, les conventions d'un projet et les enseignements réutilisables d'une session à l'autre. Commandes - mem load (début de session), mem save (persister un enseignement), mem recall (retrouver un contexte), mem show (afficher l'état), mem forget (effacer). Interdit pour les données personnelles de clients, prospects ou stagiaires.
metadata:
  source: https://github.com/hanfang/claude-memory-skill (MIT)
  adaptation: YEBA FORMATIONS — portage au format SKILL.md + barrière RGPD
---

# Mémoire persistante

Système de mémoire hiérarchique en fichiers Markdown, stocké **exclusivement en
local** sur le poste de l'utilisateur, dans `~/.claude/memory/`.

## ⛔ Barrière RGPD — à lire avant tout `save`

Ce dossier n'est **ni chiffré, ni journalisé, ni purgé automatiquement**. Il est
donc **hors périmètre** pour toute donnée personnelle.

**Ne jamais écrire en mémoire :**

- nom, prénom, e-mail, téléphone, adresse d'un prospect, client ou stagiaire ;
- situation de handicap, santé, appartenance syndicale, origine, opinions
  (données sensibles — art. 9 RGPD, interdiction de principe) ;
- résultats d'évaluation, émargements, rémunérations, numéros de contrat ;
- identifiants, jetons, mots de passe, clés d'API.

**Si l'information à retenir contient une de ces catégories :**

1. l'anonymiser (« un OPCO du BTP » plutôt que la raison sociale), **ou**
2. la router vers la base Baserow (cloud UE, finalité, durée de conservation et
   base légale définies) plutôt que vers la mémoire locale.

En cas de doute, ne pas écrire et demander à l'utilisateur.

**Ce qui est légitime en mémoire :** préférences de travail, conventions de
code, choix d'architecture, méthodes pédagogiques qui fonctionnent, pièges
rencontrés, structure d'un dépôt — c'est-à-dire du savoir-faire, pas des
personnes.

## Structure

```
~/.claude/memory/
├── core.md              # Synthèses + pointeurs (chargé à chaque session)
├── me.md                # Profil de travail de l'utilisateur
├── topics/<sujet>.md    # Entrées détaillées par sujet
└── projects/<projet>.md # Connaissance propre à un projet
```

## Actions

### `load` — début de session

Lancer en arrière-plan au démarrage. Déléguer à un agent :

1. lire `~/.claude/memory/me.md` ;
2. lire `~/.claude/memory/core.md` ;
3. si le répertoire est un dépôt Git, lire `projects/<nom-du-dépôt>.md` ;
4. renvoyer une synthèse de contexte brève à l'agent principal.

### `save <observation>` — persister un enseignement

Passer d'abord la **barrière RGPD** ci-dessus, puis :

1. déterminer le sujet (créer le fichier si besoin) ;
2. ajouter à `topics/<sujet>.md` au format :

   ```markdown
   ## <Titre court> [AAAA-MM-JJ]
   <L'enseignement en 1 à 3 phrases.>
   ```

3. si l'enseignement est structurant ou récurrent, ajouter dans `core.md` une
   synthèse d'une ligne suivie du pointeur `→ topics/<sujet>.md`.

### `recall <requête>` — retrouver un contexte

1. chercher la requête dans `core.md` ;
2. suivre les pointeurs vers les fichiers de sujets concernés ;
3. renvoyer les entrées pertinentes.

### `show` — afficher l'état

Lister les fichiers de `~/.claude/memory/`, afficher `core.md`, puis les
premières lignes de chaque fichier de sujet.

### `forget <sujet>` — effacer

Supprimer `topics/<sujet>.md` et retirer l'entrée correspondante de `core.md`.
Appliquer sans discuter dès que l'utilisateur le demande : c'est le support du
**droit à l'effacement** (art. 17 RGPD) si une donnée personnelle a malgré tout
été écrite par erreur.

## Quand écrire

- l'utilisateur dit « retiens que… » ou équivalent ;
- résolution d'un problème non trivial ;
- découverte d'une préférence de travail ;
- apprentissage propre à un projet ;
- un motif se répète sur plusieurs sessions.

## Quand relire

- démarrage d'un travail inhabituel ;
- blocage sur un problème (chercher un cas similaire passé) ;
- l'utilisateur demande « tu te souviens de… » ;
- le contexte mémorisé aiderait manifestement.

## Principes

- **Arrière-plan** : `load` et `save` ne bloquent pas l'agent principal.
- **Hiérarchique** : synthèses dans `core.md` → détails dans `topics/`.
- **Catégorisé** : pas de fourre-tout, chaque entrée a un sujet.
- **Atomique** : un bloc `##` = un souvenir.
- **Éditable** : Markdown brut, l'utilisateur peut corriger ou supprimer à tout
  moment, sans outil.
