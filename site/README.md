# Site public YEBA FORMATIONS

Site vitrine alimenté par le catalogue Airtable, sans qu'aucune donnée
personnelle ni aucune clé d'API ne quitte votre poste.

## Architecture

```
Airtable (CATALOGUE FORMATIONS)
        │   lecture au moment de la génération, sur VOTRE poste
        ▼
   site/build.py   ── filtre marque blanche ── contrôle CPF ──►  refus si échec
        │
        ├──► site/data/formations.json     (données brutes)
        └──► site/app/formations.js        (module importé par l'application)
                        │
                        ▼
              site/app/  — l'application en huit pages
              (données embarquées, aucun appel réseau)
```

Deux pages coexistent dans ce dépôt :

| | Fichier | Usage |
|---|---|---|
| Vitrine d'une page | `site/index.html` | première version, conservée comme référence |
| **Application** | `site/app/` | **la version en service** — voir `site/app/README.md` |

Le visiteur ne contacte jamais Airtable. Sa clé d'API reste sur votre machine ;
elle n'est jamais présente dans la page publiée. Le site n'émet aucune requête
vers un service tiers : pas de mesure d'audience, pas de traceur, pas de police
distante appelée à l'insu du visiteur.

## Régénérer le catalogue

```bash
export AIRTABLE_TOKEN="…"        # depuis .env, jamais dans Git
python site/build.py --check     # simulation : affiche publiables / exclues
python site/build.py             # écrit site/data/formations.json
```

`build.py` écrit deux fichiers :

- `site/data/formations.json` — les données, lisibles telles quelles ;
- `site/app/formations.js` — le module importé par l'application.

Rien à recopier à la main : les deux contrôles ci-dessous s'appliquent à la
génération, donc à ce que le site affiche.

## Les deux contrôles bloquants

`build.py` refuse de générer si l'un des deux échoue. Ce ne sont pas des
avertissements de confort : chacun correspond à une sanction réelle.

### 1. Marque blanche — risque contractuel

Le champ `Marque / Confidentialité contractuelle` fait foi, fiche par fiche.
Le filtre est une **liste blanche** : seules `Catalogue YEBA` et
`Client direct` sont publiées. Toute autre valeur — y compris vide ou nouvelle —
est exclue par défaut.

Actuellement exclues : **FOR-0005** et **FOR-0007** (sous-traitance). Le contrat
du donneur d'ordre interdit toute apparition de YEBA FORMATIONS sur les supports
remis au client final : ni logo, ni nom, ni SIRET, ni n° Qualiopi.

**Ne jamais convertir ce filtre en liste noire.** Une liste noire publie par
défaut toute fiche dont la valeur n'a pas été prévue. Ici, l'oubli doit exclure,
jamais publier.

### 2. Mention du CPF — risque pénal

Aucune formation ne porte de code RNCP ou RS : aucune n'est éligible au CPF
(code du travail, art. L.6323-6). Écrire « finançable par le CPF » sur le site
ou un devis serait une **pratique commerciale trompeuse** (code de la
consommation, art. L.121-2). `build.py` échoue si la chaîne apparaît.

Le site affiche l'inverse, de façon assumée : « Nos formations ne portent pas de
code RNCP ou RS : elles ne sont pas éligibles au CPF. »

## Mentions obligatoires présentes dans la page

| Mention | Fondement |
|---|---|
| « Cet enregistrement ne vaut pas agrément de l'État » | code du travail, art. L.6352-12 |
| N° de déclaration d'activité 04973676397 | art. L.6351-1 |
| Qualiopi n° 25FOR02027.1, catégorie et certificateur | décret n° 2019-565 |
| Délai d'accès (15 jours ouvrés) | RNQ, indicateur 1 — mention publique |
| Accessibilité handicap et coordonnées du référent | RNQ, indicateur 26 |
| « TVA non applicable — art. 261-4-4° a du CGI » | CGI, art. 261-4-4° a |

Le pied de page reproduit **à l'identique** le bloc-marque normalisé de la table
`CONFIG SYSTEME`. Toute modification se fait dans Airtable, puis se répercute
ici — jamais l'inverse.

## Choix de conception

**Couleurs** — charte officielle : bleu `#1B3A6B`, or `#C9A84C`, noir `#121212`.
Les contrastes ayant été mesurés dans votre charte, la règle est appliquée
strictement : **l'or ne touche jamais le blanc en texte** (2,29:1, échec à tous
les niveaux). Il sert aux filets, aux surfaces et au texte sur fond sombre
(8,20:1 sur noir, niveau AAA). Sur fond clair, une variante `--or-profond`
(`#8A6F22`) prend le relais pour le texte.

**Typographie** — *Atkinson Hyperlegible* pour le corps du texte : police
dessinée par le Braille Institute pour les personnes malvoyantes, avec des
formes de lettres délibérément dissemblables pour éviter les confusions.
Pour un organisme dont le dirigeant est référent handicap, ce choix est un
argument, pas une décoration. *Fraunces* en titrage.

**Accessibilité** — lien d'évitement, structure de titres continue, cibles
tactiles d'au moins 44 px, focus visible en or, `aria-pressed` sur les filtres,
annonce vocale du nombre de résultats, `prefers-reduced-motion` respecté
(l'animation du héros ne démarre pas du tout). Le contenu est **visible par
défaut** : les animations de révélation ne s'appliquent qu'une fois JavaScript
chargé, donc rien n'est masqué sans JS ni pour un lecteur d'écran.

**Formulaire** — il n'envoie rien à un serveur : il compose un courriel local
via `mailto:`. **Aucune collecte, donc aucun traitement de données personnelles
à déclarer, aucune base légale à établir, aucun sous-traitant à encadrer.**
C'est la solution la plus sobre juridiquement ; voir ses limites ci-dessous.

## Limites connues

1. ~~Catalogue recopié à la main~~ — **corrigé**. `build.py` génère
   `app/formations.js`, importé par `app/contenu.js`. Le catalogue n'existe
   plus qu'en un seul endroit : Airtable.

2. **Le formulaire `mailto:` a un coût de conversion.** Il ouvre le logiciel de
   messagerie du visiteur, ce qui échoue sur les postes sans client configuré,
   et l'on ne mesure rien. C'est un arbitrage assumé en faveur de la sobriété
   juridique. L'alternative conforme est un point de collecte hébergé dans
   l'Union européenne (Baserow, cloud UE, Pays-Bas) — elle suppose alors une
   finalité déclarée, une base légale, une durée de conservation, une mention
   d'information et une inscription au registre des traitements.

3. **`build.py` n'a pas été exécuté** contre l'API Airtable depuis cet
   environnement : le jeton n'y est pas disponible. Les données de
   `formations.json` ont été relevées via le connecteur Airtable de la session.
   Lancer `python site/build.py --check` sur votre poste pour valider le script
   de bout en bout.

4. **Le site n'est pas hébergé.** Il est publié en tant qu'artefact Claude. Pour
   une mise en ligne sur votre nom de domaine, l'hébergeur doit être situé dans
   l'Union européenne et ne pas être soumis à une législation d'accès
   extraterritorial — c'est l'exigence inscrite dans votre propre CONFIG SYSTEME,
   paramètre « Hébergeur du site internet », aujourd'hui `[À CONFIRMER]`.

5. **Deux paramètres bloquants pour la mise en ligne** restent ouverts dans
   CONFIG SYSTEME et sont des mentions légales obligatoires : la **forme
   juridique**, le **capital social**, le **RCS** et le **médiateur de la
   consommation** (art. L.612-1 du code de la consommation — obligatoire dès
   qu'un seul particulier finance lui-même une formation ; non-conformité
   ouverte, action A-04).

## Sources

Base Airtable `appQ2zqc80kkc6MR1`, tables `CATALOGUE FORMATIONS` et
`CONFIG SYSTEME`, relevées le 17/09/2026.
