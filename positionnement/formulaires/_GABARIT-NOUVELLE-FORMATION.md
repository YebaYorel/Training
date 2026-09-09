# Gabarit — blocs communs + méthode pour créer un nouveau positionnement

Ce fichier contient (1) les **blocs 0 et E**, identiques pour toutes les
formations, et (2) la méthode pour produire une nouvelle banque d'items.

---

## BLOC 0 — En-tête (commun, non scoré)

> Présent en haut du formulaire en ligne **et** en haut du PDF A4.

```
┌──────────────────────────────────────────────────────────────────┐
│  TEST DE POSITIONNEMENT                          [ QR ]          │
│  Formation : ................................. (réf. FOR-000X)   │
│  Session du : ..../..../........                                 │
│  Réf. inscription : INS-□□□□□                                    │
│  Nom, Prénom : ................................................  │
└──────────────────────────────────────────────────────────────────┘
```

- Le **QR code** encode uniquement `INS-xxxxx` (référence d'inscription).
  Il permet de rattacher la feuille à la bonne personne **sans lire le nom** :
  aucun OCR d'écriture manuscrite n'est nécessaire pour l'identification.
- Le nom manuscrit ne sert qu'au contrôle visuel humain. Il n'est jamais
  extrait automatiquement.
- En version papier, le QR est **pré-imprimé** au moment de l'édition : une
  feuille = un stagiaire. Pas de feuille vierge générique.

**Consigne à imprimer sous l'en-tête :**

> Ce questionnaire n'est **pas un examen** et n'est **pas noté**. Il sert
> uniquement à adapter le contenu de la formation à votre niveau et à vos
> besoins. Répondez spontanément : « je ne sais pas » est une réponse utile.
> Durée : environ 15 minutes.

---

## BLOC E — Aménagement et information (commun, non scoré)

**E1.** Avez-vous besoin d'un aménagement particulier pour suivre cette
formation dans de bonnes conditions (rythme, supports, salle, matériel,
déplacement) ?
`☐ Non` `☐ Oui`

**E2.** Si oui, précisez **l'aménagement souhaité** :
`.............................................................................`

> 🔒 **Ne jamais demander la nature du handicap, ni de justificatif médical.**
> C'est une donnée de santé au sens de l'**article 9 du RGPD**, interdite de
> collecte hors base légale spécifique. On demande le **besoin**, jamais la
> **cause**. Ta base Airtable contient déjà deux champs neutralisés à ce titre
> dans APPRENANTS (`⚠️ NE PAS REMPLIR — Type de handicap`, `⚠️ NE PAS REMPLIR —
> Document RQTH`) : ils sont **à supprimer**, pas seulement à masquer.

**E3.** Souhaitez-vous être contacté(e) avant la formation pour en parler ?
`☐ Non` `☐ Oui`

**Mention d'information à imprimer en pied de formulaire :**

> **Traitement de vos réponses.** Vos réponses sont traitées par
> [ORGANISME] afin d'adapter le contenu de la formation à laquelle vous êtes
> inscrit(e) et de justifier de notre démarche qualité (Qualiopi, indicateur 8).
> Base légale : exécution du contrat de formation. Destinataires : le
> responsable pédagogique et le formateur de votre session, exclusivement.
> Conservation : 3 ans à compter de la fin de la formation (durée de contrôle
> des financeurs). Une **synthèse anonyme** du groupe est transmise au
> formateur. Vos réponses **ne sont pas notées** et ne conditionnent pas votre
> accès à la formation. Vous disposez d'un droit d'accès, de rectification,
> d'effacement et d'opposition : [CONTACT]. Réclamation possible auprès de la
> CNIL (cnil.fr).
>
> **Aide automatisée.** Vos réponses sont pré-analysées par un outil
> automatisé. **Aucune décision n'est prise par cet outil** : la synthèse est
> systématiquement relue et validée par le responsable pédagogique avant
> utilisation. *(Information au titre de l'article 50 du règlement (UE)
> 2024/1689 sur l'intelligence artificielle.)*

> ℹ️ `[ORGANISME]` et `[CONTACT]` sont des variables : mettre **YEBA
> FORMATIONS** pour tes formations propres, et le nom du **centre donneur
> d'ordre** pour les prestations sous-traitées où ton centre ne doit pas
> apparaître.

---

## Méthode pour créer une nouvelle banque d'items

### 1. Partir des objectifs pédagogiques, jamais du programme

Les objectifs (« le stagiaire sera capable de… ») sont déjà formulés en
capacités observables. Le programme, lui, est une liste de contenus : il ne dit
pas ce que le stagiaire doit *savoir faire*. On positionne sur des capacités.

### 2. Regrouper les objectifs en 4 domaines

Tes formations ont toutes **5 objectifs**. Regroupe-les en **4 domaines** de
poids comparable en temps de formation. Règle empirique qui marche bien :

| Domaine | Nature |
|---|---|
| D1 | **Comprendre** — les notions, le vocabulaire, ce que ça fait et ne fait pas |
| D2 | **Méthode** — le geste technique central du métier visé |
| D3 | **Appliquer** — le transfert dans la situation de travail |
| D4 | **Cadre** — risques, conformité, mesure, suites |

### 3. Écrire 2 items d'auto-positionnement par domaine (bloc B)

Formulation obligatoire : **« Je sais / je suis capable de + verbe d'action »**.
Jamais « Je connais X » (impossible à se situer), jamais deux idées dans un item.

### 4. Écrire 3 QCM par domaine (bloc C)

Règles strictes :
- **3 options, une seule correcte.** Pas de « toutes les réponses ».
- Les 2 distracteurs sont des **erreurs réellement commises** par les débutants,
  pas des absurdités. Un distracteur ridicule ne mesure rien.
- Une seule phrase, pas de négation, pas de piège de formulation.
- Le QCM porte sur **le même domaine** que les items B correspondants — sinon
  l'indice de calibration ne veut rien dire.
- Difficulté croissante dans le domaine : 1 facile, 1 moyen, 1 discriminant.

### 5. Écrire les 3 questions ouvertes (bloc D)

Toujours les mêmes trois intentions :
- **D1** — une situation de travail concrète où appliquer la formation
- **D2** — ce qui bloque aujourd'hui
- **D3** — ce que la personne attend absolument de ces journées

Ces réponses ne sont **pas scorées**. Elles servent à choisir les **exemples**
du cours — c'est ce qui rend une formation « saisissante » plutôt que générique.

### 6. Déclarer le tout dans `analyse/referentiels.json`

Ajouter une entrée `FOR-000X` avec les 4 domaines, le corrigé des 12 QCM, et le
poids horaire de chaque domaine. Le moteur de scoring fonctionne alors sans
aucune modification de code.
