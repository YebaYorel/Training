# Système de positionnement YEBA FORMATIONS — architecture

Qualiopi **indicateur 8** : « Le prestataire détermine les procédures de
positionnement et d'évaluation des acquis à l'entrée de la prestation. »
*(source : [référentiel national qualité — Digiforma, indicateur 8](https://www.digiforma.com/certification-qualiopi/criteres/critere-2/indicateur-8-positionnement-entree/))*

> ⚠️ **Écart repéré dans ta base Airtable.** Plusieurs champs du CATALOGUE sont
> étiquetés « Indicateur 8 » pour l'**accessibilité handicap** (`Doc - Accessibilité
> handicap`, `Adaptations possibles`), et le champ `Questionnaire positionnement
> envoyé` est étiqueté « Indicateur 5 ». Or l'indicateur 8 est le **positionnement
> à l'entrée**, et le handicap relève d'un autre indicateur du critère 7.
> À corriger avant audit : un auditeur qui suit tes propres étiquettes ne trouvera
> pas la preuve au bon endroit. À vérifier sur ta version du référentiel.

---

## 1. Le principe directeur : une structure, N formations

Le piège classique est de créer un formulaire par formation. On se retrouve avec
7 formulaires, 7 grilles, 7 traitements — impossible à maintenir, et aucune
comparaison possible d'une session à l'autre.

Ici : **une structure unique en 5 blocs, identique pour toutes les formations.**
Seul le *contenu des items* change. Conséquence directe : **un seul moteur
d'analyse** (`analyse/scoring.py`) traite les 7 formations, et les 3 suivantes.

```
                    RÉFÉRENTIEL D'ITEMS (1 fichier JSON par formation)
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
      Formulaire en ligne      PDF A4 recto-verso       Moteur de scoring
        (voie normale)          (voie de secours)        (voie unique)
              │                       │                       │
              │                  scan/photo                   │
              │                       ▼                       │
              │              OCR structuré (UE)               │
              │                       │                       │
              └───────────────────────┴──────────────────────►│
                                                              ▼
                                              Synthèse individuelle + groupe
                                                              │
                                              ┌───────────────┴──────────────┐
                                              ▼                              ▼
                                    Décision pédagogique            Preuve Qualiopi ind. 8
                                  APPUYER / AJUSTER / ALLÉGER
```

**Le point clé :** le PDF papier n'est pas un document séparé, c'est un *rendu*
du même référentiel. On connaît donc à l'avance le nombre d'items, leur ordre et
leurs modalités. Lire une feuille scannée revient à lire **des cases cochées à
positions connues** — pas à déchiffrer de l'écriture libre. C'est ce qui rend
l'automatisation fiable et bon marché.

---

## 2. Les 5 blocs du formulaire

| Bloc | Contenu | Rôle | Scoré ? |
|---|---|---|---|
| **0** | Réf. inscription + QR code, formation, session | Rattachement machine | non |
| **A** | 6 questions de contexte (fonction, ancienneté, outils…) | Adapter les exemples du cours | non |
| **B** | 8 items d'**auto-positionnement** (échelle 0–3) | Ce que le stagiaire *croit* savoir | oui |
| **C** | 12 **QCM** à réponse unique vérifiable | Ce qu'il *sait* réellement | oui |
| **D** | 3 questions ouvertes courtes | Attentes, blocages, cas concret | non (transcrit) |
| **E** | Aménagement nécessaire + information RGPD | Qualiopi handicap + licéité | non |

Durée de passation visée : **12 à 15 minutes**. Tient sur un A4 recto-verso.

### Échelle du bloc B (4 niveaux, faciles à cocher)

| | Niveau |
|---|---|
| **0** | Je ne connais pas |
| **1** | J'en ai entendu parler |
| **2** | Je sais faire avec de l'aide |
| **3** | Je sais faire seul et je peux l'expliquer à quelqu'un |

### Les 4 domaines de compétence

Chaque formation est découpée en **4 domaines**, alignés sur ses objectifs
pédagogiques Qualiopi (indicateur 5). Chaque domaine reçoit :
- **2 items d'auto-positionnement** (bloc B) → score sur 6
- **3 QCM** (bloc C) → score sur 3

Ce découpage n'est pas décoratif : c'est l'unité sur laquelle se prend la
décision pédagogique « j'appuie / j'ajuste / j'allège ».

---

## 3. L'idée qui fait la différence : l'indice de calibration

Un test qui ne demande que « vous sentez-vous à l'aise ? » ne vaut rien : les
plus faibles se surestiment, les plus compétents se sous-estiment. On mesure
donc **les deux**, et on regarde **l'écart**.

Pour chaque domaine :

```
auto  = (somme des 2 items B) / 6  × 100
réel  = (somme des 3 QCM C)   / 3  × 100
calibration = auto − réel
```

| Calibration | Lecture | Ce que tu fais en salle |
|---|---|---|
| **> +25** | **Surestimation** — il croit savoir | Ouvrir par un cas qui met en défaut, avant tout apport théorique |
| **−25 à +25** | Calibré | Progression normale |
| **< −25** | **Sous-estimation** — il sait mais n'ose pas | Le valoriser, le faire démontrer, en faire un pair-aidant |

C'est l'information que ni un QCM seul, ni une auto-évaluation seule ne donnent.
Et c'est directement actionnable le matin même.

---

## 4. Décision pédagogique automatique (niveau groupe)

Pour chaque domaine, on calcule la **moyenne du groupe (M)** et son
**écart-type (σ)**. La règle :

| Condition | Décision | Traduction concrète |
|---|---|---|
| σ ≥ 20 | **DIFFÉRENCIER** *(prioritaire)* | Groupe hétérogène : binômes fort/faible, parcours à 2 vitesses |
| M < 40 | **APPUYER** | Module socle : plus de temps, exercices guidés, reprise des bases |
| 40 ≤ M < 70 | **AJUSTER** | Volume prévu conservé, exemples calés sur le bloc A |
| M ≥ 70 et σ < 15 | **ALLÉGER** | Rappel express (20–30 min), temps réinvesti sur les domaines faibles |

### ⚠️ Limite de précision à connaître avant d'interpréter

Avec **3 QCM par domaine**, le score « réel » d'un domaine ne peut prendre que
quatre valeurs : **0, 33, 67 ou 100**. Une seule réponse change le score de
33 points. Conséquences à tenir :

- **Au niveau individuel**, un écart inférieur à 34 points entre deux stagiaires
  sur un domaine **ne signifie rien**. Ne jamais classer les stagiaires entre eux.
- **L'indice de calibration** doit être lu comme un **signal**, pas comme une
  mesure. « Cette personne se surestime nettement » est exploitable ; « elle se
  surestime de 28 points » ne l'est pas.
- **Au niveau du groupe**, en revanche, la moyenne est robuste : les erreurs
  individuelles se compensent. C'est bien pour la décision **collective** que ce
  test est fiable — et c'est son objet.

C'est le prix d'un test de 15 minutes tenant sur un A4. L'alternative (30 QCM,
45 minutes) ferait chuter le taux de réponse bien plus qu'elle ne gagnerait en
précision. Arbitrage assumé.

> **Garde-fou contractuel.** « ALLÉGER » ne veut **jamais** dire supprimer. Les
> objectifs annoncés au programme sont contractuels (Qualiopi ind. 5 et 6) et
> doivent tous être traités et évalués. On ajuste la **profondeur** et le **temps**,
> jamais le périmètre annoncé. Retirer une notion annoncée = non-conformité.

Le temps libéré par un « ALLÉGER » est **réaffecté** au domaine classé
« APPUYER » le plus faible. Le moteur propose cette réallocation en minutes.

---

## 5. Où vivent les données

### Cœur neutre, portable

Le référentiel (`formulaires/*.md` → JSON) et le moteur (`analyse/scoring.py`)
**ne dépendent d'aucun éditeur**. Ils fonctionnent à l'identique sur Airtable
aujourd'hui et sur Baserow demain. C'est volontaire : voir
`conformite/RGPD-IA-ACT.md`, section souveraineté.

### Nouvelles tables à créer dans Airtable

**Table `POSITIONNEMENT — RÉPONSES`** (une ligne = un stagiaire × une session)

| Champ | Type | Note |
|---|---|---|
| Réf. positionnement | formula | `POS-` + autonumber |
| Inscription | link_row → INSCRIPTIONS | **seul lien vers l'identité** |
| Formation | lookup (from Inscription) | |
| Session | lookup (from Inscription) | |
| Canal | single_select | En ligne / Papier |
| Date de réponse | date | |
| Réponses brutes (JSON) | long text | sortie du formulaire ou de l'OCR |
| Scan original | attachment | uniquement si canal = Papier |
| Statut traitement | single_select | Reçu / À valider / Validé / Écarté |
| Confiance extraction | percent | rempli par l'OCR ; < 90 % ⇒ À valider |
| Score D1..D4 (réel) | number ×4 | |
| Auto D1..D4 | number ×4 | |
| Calibration D1..D4 | formula ×4 | `auto − réel` |
| Niveau global | single_select | Découverte / Intermédiaire / Avancé |
| Aménagement demandé | checkbox | **oui/non uniquement** |
| Aménagement — nature | long text | *jamais* de donnée de santé |
| Synthèse individuelle | long text | générée |
| Validé par | single_select | le formateur qui a relu |

> **Minimisation (RGPD art. 5.1.c).** Cette table ne contient **ni nom, ni e-mail,
> ni téléphone** : uniquement le lien vers INSCRIPTIONS. L'identité reste dans
> APPRENANTS. Les réponses sont ainsi pseudonymisées au sein même de la base.

**Table `POSITIONNEMENT — SYNTHÈSE SESSION`** (une ligne = une session)

| Champ | Type |
|---|---|
| Session | link_row → SESSIONS |
| Nb réponses / Nb inscrits | number / rollup |
| Taux de réponse | formula |
| Moyenne + écart-type D1..D4 | number ×8 |
| Décision D1..D4 | single_select (APPUYER/AJUSTER/ALLÉGER/DIFFÉRENCIER) |
| Réallocation proposée (min) | long text |
| Top 3 attentes | long text |
| Aménagements à prévoir | long text |
| Synthèse formateur (PDF) | attachment |
| Validée par | single_select |
| Date de validation | date |

### Champs à ajouter aux tables existantes

Sur **INSCRIPTIONS** :
- `Positionnement dû` — formula (voir `automatisations/A1-envoi-positionnement.md`)
- `Positionnement relancé` — checkbox
- `Positionnement reçu` — checkbox
- *(`Positionnement envoyé` existe déjà — `fldCaaUucLn2aAIm8`)*

Sur **SESSIONS** :
- `Synthèse positionnement prête` — checkbox
- *(`Questionnaire positionnement envoyé` existe déjà — `fldQAplzrLprtrd6p`)*

Sur **CATALOGUE FORMATIONS** :
- *(`Questions test de positionnement`, `Réponses attendues`, `Lien vers le
  formulaire de positionnement` existent déjà — à remplir depuis `formulaires/`)*

---

## 6. Les deux automatisations

| | Nom | Déclencheur | Détail |
|---|---|---|---|
| **A1** | Envoi du test | `Positionnement dû = OUI` sur INSCRIPTIONS | `automatisations/A1-envoi-positionnement.md` |
| **A2** | Ingestion + analyse | Réponse reçue (en ligne) **ou** scan déposé (papier) | `automatisations/A2-ingestion-et-analyse.md` |

---

## 7. Fichiers de ce dossier

```
positionnement/
├── 00-ARCHITECTURE.md              ← vous êtes ici
├── formulaires/
│   ├── FOR-0001_IA-Generative.md
│   ├── FOR-0002_Automatisation.md
│   ├── FOR-0003_RGPD-Cybersecurite.md
│   ├── FOR-0004_Vente-Initiation.md
│   └── _GABARIT-NOUVELLE-FORMATION.md
├── analyse/
│   ├── scoring.py                  ← moteur exécutable
│   ├── referentiels.json           ← corrigés + mapping domaines
│   └── modeles-de-synthese.md
├── automatisations/
│   ├── A1-envoi-positionnement.md
│   └── A2-ingestion-et-analyse.md
└── conformite/
    └── RGPD-IA-ACT.md              ← à lire avant mise en service
```
