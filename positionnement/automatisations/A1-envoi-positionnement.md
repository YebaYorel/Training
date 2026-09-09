# Automatisation A1 — Envoi du test de positionnement

## Pourquoi J-15 (et pas J-7, ni à l'inscription)

Tu m'as laissé apprécier le délai. Voici le raisonnement, parce que le chiffre
n'est pas arbitraire — il est contraint par les deux bouts :

**Borne basse.** Il te faut du temps *après* la dernière réponse pour exploiter
le test : dépouiller, décider APPUYER/AJUSTER/ALLÉGER, refaire le déroulé, et
briefer le formateur. Compte **3 jours ouvrés minimum**, et la synthèse doit
partir avec la mallette formateur — que ton système envoie déjà à **J-2**
(champ `Mallette due (J-2)`). Donc : **dernière réponse utile à J-4**.

**Borne haute.** Un test envoyé trop tôt arrive avant que la formation soit
« réelle » dans la tête du stagiaire : il le range et l'oublie. Et sur une
session encore non confirmée, tu fais travailler des gens qui ne viendront
peut-être pas. Au-delà de 3 semaines, le taux de réponse s'effondre.

**Entre les deux, il faut loger deux relances.** D'où :

| Jour | Événement | Condition |
|---|---|---|
| **J-15** | Envoi initial | Inscription **et** session confirmées |
| **J-8** | Relance automatique | Pas de réponse reçue |
| **J-4** | **Alerte interne** (pas de mail au stagiaire) | Toujours pas de réponse |
| **J-2** | Synthèse groupe jointe à la mallette formateur | — |
| **J-0** | Passation papier en ouverture pour les manquants | 10 min, avant le café |

> **Cas de l'inscription tardive** (fréquent en intra) : si l'inscription est
> confirmée à moins de 15 jours de la session, l'envoi part **immédiatement**.
> La formule ci-dessous gère les deux cas sans branche supplémentaire.

> **Le filet J-0 n'est pas un détail.** Aucun envoi automatique n'atteint 100 %.
> La passation papier de 10 minutes en ouverture garantit que **chaque**
> stagiaire est positionné — ce que l'auditeur Qualiopi vérifiera sur
> l'indicateur 8. C'est précisément ce que la voie papier de l'automatisation A2
> sert à absorber sans ressaisie.

---

## Champs Airtable à créer

Sur la table **INSCRIPTIONS** (`tblUWW5ken5sAUDJk`).

### 1. `Date début session` — rollup *(préalable technique)*

`Date de début (from Session)` est un **lookup**, donc un tableau.
`DATETIME_DIFF()` appliqué directement dessus se comporte mal.

- Type : **Rollup**
- Table liée : `Session` → champ `Date de début`
- Fonction d'agrégation : `MAX(values)`

Toutes les formules ci-dessous s'appuient sur ce rollup, pas sur le lookup.

### 2. `Positionnement dû` — formule

```
IF(
  AND(
    {Statut Inscription} = "Confirmée",
    {Positionnement envoyé} = 0,
    {Email stagiaire (auto)} != BLANK(),
    {Date début session} != BLANK(),
    DATETIME_DIFF({Date début session}, TODAY(), 'days') <= 15,
    DATETIME_DIFF({Date début session}, TODAY(), 'days') >= 0
  ),
  "OUI",
  "NON"
)
```

> Vérifie le libellé exact de l'option `Confirmée` dans ton `Statut Inscription` :
> une majuscule ou un accent qui diffère et la formule renvoie « NON » en
> silence. C'est le mode de panne le plus fréquent de ce type d'automatisation.

### 3. `Positionnement à relancer` — formule

```
IF(
  AND(
    {Positionnement envoyé} = 1,
    {Positionnement reçu} = 0,
    {Positionnement relancé} = 0,
    DATETIME_DIFF({Date début session}, TODAY(), 'days') <= 8,
    DATETIME_DIFF({Date début session}, TODAY(), 'days') >= 0
  ),
  "OUI",
  "NON"
)
```

### 4. `Positionnement en souffrance` — formule *(déclenche l'alerte interne)*

```
IF(
  AND(
    {Positionnement envoyé} = 1,
    {Positionnement reçu} = 0,
    DATETIME_DIFF({Date début session}, TODAY(), 'days') <= 4,
    DATETIME_DIFF({Date début session}, TODAY(), 'days') >= 0
  ),
  "OUI",
  "NON"
)
```

Plus les cases : `Positionnement relancé` (checkbox), `Positionnement reçu`
(checkbox). `Positionnement envoyé` existe déjà (`fldCaaUucLn2aAIm8`).

---

## Les trois automatisations Airtable

### A1-a · Envoi initial

- **Déclencheur :** « À une heure programmée » — tous les jours à **06 h 00**
  (heure de La Réunion, UTC+4). Ne pas utiliser le déclencheur « quand un
  enregistrement correspond aux critères » : il se redéclenche à chaque
  modification de ligne et produit des doublons d'envoi.
- **Étape 1 — Rechercher** : vue `Positionnement à envoyer`
  (filtre : `Positionnement dû` = "OUI").
- **Étape 2 — Répéter** pour chaque enregistrement :
  - **Envoyer un e-mail** (modèle ci-dessous)
  - **Mettre à jour** : `Positionnement envoyé` ✅
  - **Créer** une ligne dans `MAILING LOG` : type = « Positionnement »,
    destinataire, session liée, apprenant lié, statut = « Envoyé »

### A1-b · Relance

Identique, sur la vue `Positionnement à relancer`, avec l'objet
« Il vous reste quelques minutes ? » et la case `Positionnement relancé` ✅.

### A1-c · Alerte interne à J-4

- **Déclencheur :** programmé, tous les jours à 06 h 15.
- **Recherche :** vue `Positionnement en souffrance`.
- **Action :** créer une ligne dans `ALERTES & TÂCHES` —
  titre « Positionnement non reçu — J-4 », type « Pédagogique »,
  priorité « Haute », échéance = date de début − 2 jours,
  lié à l'apprenant et à la session,
  description : « Appeler le stagiaire. Si pas de réponse : prévoir la
  passation papier en ouverture de session (10 min). »

> **Pas de troisième e-mail au stagiaire.** Au bout de deux relances non suivies
> d'effet, un mail de plus ne sert à rien : c'est un appel qu'il faut. Et
> l'appel a un autre bénéfice — il fait souvent remonter une difficulté
> (lecture, numérique, langue, disponibilité) qu'aucun formulaire ne capte.

---

## Modèle d'e-mail — envoi initial

**Objet :** `{Titre formation} — 15 minutes pour préparer votre formation`

```
Bonjour {Nom Prénom},

Vous êtes inscrit(e) à la formation « {Titre formation} », qui débute le
{Date de début} à {Lieu}.

Avant de commencer, j'ai besoin de 15 minutes de votre temps.

👉 {Lien vers le formulaire de positionnement}

Ce questionnaire n'est pas un examen et n'est pas noté. Personne ne verra
vos réponses en dehors de votre formateur. Il sert à une seule chose :
construire la formation autour de VOTRE niveau et de VOS situations de
travail, plutôt que de vous servir un contenu standard.

Concrètement, vos réponses décident de ce sur quoi nous passerons plus de
temps, et de ce que nous survolerons. Répondez spontanément : « je ne sais
pas » est une réponse utile — c'est même la plus utile.

Merci de répondre avant le {Date de début − 4 jours}.

Vous préférez le remplir avec moi plutôt que seul(e) devant un écran ?
Appelez-moi au {Téléphone}, nous le faisons ensemble en 10 minutes. Une
version papier en grands caractères est aussi disponible sur demande.

Si vous avez besoin d'un aménagement particulier pour suivre la formation
dans de bonnes conditions, la dernière question du formulaire est faite
pour ça — ou répondez simplement à ce message.

Bien cordialement,
{Signature}
```

> **Trois choses à ne jamais retirer de ce mail :** « pas un examen »,
> « pas noté », et l'explication de l'usage réel des réponses. Sans elles, le
> stagiaire répond ce qu'il croit qu'on attend de lui — et ton test mesure sa
> capacité à deviner, pas son niveau.

---

## Modèle d'e-mail — relance

**Objet :** `{Titre formation} — il vous reste quelques minutes ?`

```
Bonjour {Nom Prénom},

Votre formation « {Titre formation} » démarre dans {N} jours et je n'ai pas
encore reçu votre questionnaire de préparation.

👉 {Lien vers le formulaire de positionnement}   (15 minutes)

Si vous préférez, appelez-moi et nous le remplissons ensemble au téléphone
en 10 minutes : {Téléphone}.

Sans réponse de votre part, nous le ferons sur place en ouverture de
session — mais je n'aurai alors plus le temps d'adapter le programme.

Bien cordialement,
{Signature}
```

---

## Conformité

| Point | Statut |
|---|---|
| **RGPD — base légale** | Exécution du contrat de formation (art. 6.1.b). Pas de consentement à recueillir : le test fait partie de la prestation. |
| **RGPD — information** | Assurée par la mention en pied de formulaire (voir `_GABARIT-NOUVELLE-FORMATION.md`), pas par l'e-mail. |
| **RGPD — destinataires** | Responsable pédagogique + formateur de la session. À ne pas transmettre à l'entreprise cliente ni à l'OPCO : ils financent, ils ne sont pas destinataires des réponses individuelles. |
| **RGPD — prospection** | ❌ Ne **jamais** greffer d'offre commerciale sur ce mail. Le changement de finalité rendrait le traitement illicite. |
| **IA Act** | A1 n'embarque aucune IA : simple envoi conditionnel. Hors périmètre. |
| **Qualiopi ind. 8** | Le `MAILING LOG` horodaté constitue la preuve d'envoi ; la synthèse validée constitue la preuve d'exploitation. Les deux sont demandées en audit. |
