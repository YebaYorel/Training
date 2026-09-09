# Modèles de synthèse

Deux documents, deux usages. Le premier ne quitte jamais la base ; le second
part au formateur avec la mallette.

> ⚠️ **Le document que tu m'avais transmis.** Tu évoques « l'analyse de
> positionnement que tu m'avais transmis » : je ne l'ai pas dans cette session,
> et il n'est pas dans ce dépôt. Les modèles ci-dessous sont donc **ma
> proposition**, pas une reprise de la tienne. Envoie-la-moi et je cale le
> format exact — les champs et le moteur ne changeront pas, seul le rendu.

---

## A. Fiche individuelle *(usage interne — ne pas diffuser)*

```
FICHE DE POSITIONNEMENT — {Réf. inscription}
Formation : {Titre}   Session : {Date}   Reçu le : {Date}   Canal : {En ligne | Papier}

NIVEAU GLOBAL : {Découverte | Intermédiaire | Avancé}   ({score}/100)

┌─────────────────────────────────────────────────────────────────┐
│ Domaine                          Déclaré   Réel   Écart         │
├─────────────────────────────────────────────────────────────────┤
│ D1 {libellé}                        67      33     +34  ⚠️ SUR   │
│ D2 {libellé}                        50      67     -17     ok    │
│ D3 {libellé}                        33      33       0     ok    │
│ D4 {libellé}                        17      67     -50  ⚠️ SOUS  │
└─────────────────────────────────────────────────────────────────┘

CONTEXTE (bloc A) : {fonction} · {taille} · {fréquence d'usage} · {outils}

SES MOTS (bloc D, non scoré — à relire) :
  Situation visée : « ... »
  Ce qui bloque   : « ... »
  Attente forte   : « ... »

AMÉNAGEMENT DEMANDÉ : {Non | Oui — besoin exprimé : ...}

CONDUITE À TENIR EN SALLE
  • D1 surestimation → ouvrir par un cas qui met en défaut, avant tout apport
  • D4 sous-estimation → le faire démontrer, l'installer en pair-aidant
```

> **Cette fiche ne sort pas de la base.** Elle ne va ni au stagiaire, ni à son
> employeur, ni à l'OPCO. Le formateur reçoit la synthèse de groupe, et les
> profils individuels seulement s'il anime lui-même la session.

---

## B. Synthèse de session *(pour le formateur — jointe à la mallette J-2)*

Générée par `scoring.py`. Structure :

1. **Décisions par domaine** — moyenne, écart-type, APPUYER / AJUSTER /
   ALLÉGER / DIFFÉRENCIER
2. **Répartition des niveaux** dans le groupe
3. **Réallocation de temps proposée**, en minutes
4. **Aménagements à prévoir**
5. **À vérifier** — réponses incomplètes ou extraction douteuse

À compléter à la main, parce qu'aucun script ne le fera correctement :

6. **Top 3 des attentes** — regroupement thématique des réponses D3
7. **Trois situations à réutiliser en salle** — verbatims du bloc D
8. **Profils à surveiller** — sans nommer : « un participant très en avance sur
   D2, à mobiliser en binôme » ; « deux participants qui se surestiment sur D1,
   prévoir la mise en défaut »

> Les points 6 à 8 sont ce qui transforme une synthèse en **outil d'animation**.
> Le calcul donne les proportions ; les mots des stagiaires donnent les
> exemples. C'est la partie que tu ne dois pas automatiser.

---

## C. Ce qui part au stagiaire

**Rien de chiffré. Aucun score, aucun niveau, aucun classement.**

Un simple accusé de réception :

```
Bonjour {Prénom},

J'ai bien reçu votre questionnaire, merci d'avoir pris le temps.

Vos réponses ont été prises en compte pour construire le programme du
{date}. Nous reviendrons notamment sur {thème issu de son bloc D}.

À très bientôt,
{Signature}
```

> Renvoyer un score à un stagiaire transforme un positionnement en évaluation.
> Pédagogiquement, c'est contre-productif : le stagiaire arrive étiqueté et se
> comporte comme tel. Juridiquement, c'est le premier pas vers le régime « haut
> risque » de l'IA Act (annexe III — évaluation des acquis d'apprentissage).
>
> La phrase « nous reviendrons notamment sur… », en revanche, vaut de l'or :
> elle prouve au stagiaire que le questionnaire a servi à quelque chose. C'est
> ce qui fait remonter le taux de réponse aux sessions suivantes.

---

## D. Preuve Qualiopi (indicateur 8)

L'auditeur demandera trois choses. Elles doivent être produites **sans
recherche** :

| Preuve | Où elle se trouve |
|---|---|
| La **procédure** de positionnement | `../00-ARCHITECTURE.md` + le formulaire de la formation |
| La **trace d'envoi** | `MAILING LOG`, horodaté par l'automatisation A1 |
| L'**exploitation** du résultat | Synthèse de session **validée**, + trace de l'ajustement du déroulé |

> La troisième est celle qui manque le plus souvent en audit. Collecter des
> questionnaires ne suffit pas : il faut montrer **ce qu'on en a fait**. D'où le
> champ `Réallocation proposée` et le champ `Validée par` — ils existent pour
> cette raison autant que pour la pédagogie.
