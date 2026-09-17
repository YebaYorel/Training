# Connecter un modèle d'IA à Baserow

Écran : **Paramètres du projet → IA générative**. Deux fournisseurs y sont
proposés, Anthropic et Mistral. Le choix entre les deux n'est pas technique,
il est juridique — voir « Lequel activer » plus bas.

## Les identifiants de modèles à saisir

Le champ **Modèles activés** attend une liste séparée par des virgules.

⚠️ **Ne recopiez pas l'exemple affiché par Baserow.** Son texte d'aide propose
`claude-3-5-sonnet-20241022, claude-3-opus-20240229` : ce sont des modèles de
générations antérieures. Les saisir revient à payer pour d'anciens modèles, ou
à obtenir une erreur s'ils ont été retirés.

Identifiants actuels, à copier tels quels — **sans jamais y ajouter de suffixe
de date** :

```
claude-haiku-4-5,claude-sonnet-5,claude-opus-5
```

| Modèle | Identifiant | Entrée $/M | Sortie $/M | Pour quel usage |
|---|---|---|---|---|
| Haiku 4.5 | `claude-haiku-4-5` | 1 $ | 5 $ | Classer, étiqueter, résumer une ligne |
| Sonnet 5 | `claude-sonnet-5` | 2 $ | 10 $ | Rédaction courante, synthèses |
| Opus 5 | `claude-opus-5` | 5 $ | 25 $ | Analyse, raisonnement, textes engageants |

Mettez Haiku en premier : c'est celui que vous utiliserez le plus, et il coûte
cinq fois moins cher qu'Opus pour étiqueter une ligne.

## La clé d'API

1. [console.anthropic.com](https://console.anthropic.com) → **Settings → API Keys
   → Create Key**. Nommez-la `baserow-yeba` : une clé par usage se révoque sans
   rien casser d'autre.
2. Elle s'affiche **une seule fois**. Copiez-la immédiatement.
3. Collez-la dans le champ **Clé d'API** de Baserow.
4. Dans la console, fixez un **plafond de dépense mensuel** dès le premier jour.

⚠️ **Le champ Clé d'API n'est pas un champ d'identification.** Votre navigateur
peut y proposer une adresse e-mail par autocomplétion : ignorez la suggestion.
Une clé commence par `sk-ant-`.

⚠️ **Facturation distincte de votre abonnement Claude.** L'API se paie à l'usage,
sur un compteur séparé. Un abonnement, même payant, ne couvre pas les appels API.

## Lequel activer : la question n'est pas technique

Vous quittez Airtable **parce qu'il est américain**. Brancher Anthropic sur
Baserow réintroduit exactement le problème que la migration devait résoudre.

Concrètement : un champ IA posé sur la table `APPRENANTS` envoie le nom, la
situation et le parcours de vos stagiaires à un sous-traitant établi aux
États-Unis. C'est un transfert hors Union européenne — **RGPD, art. 44 à 49** —
et il n'est pas couvert par l'accord de sous-traitance que vous signerez avec
Baserow, qui ne concerne que Baserow.

**Mistral est proposé juste en dessous, dans le même écran.** Société française,
traitement dans l'Union européenne. Pour les tables contenant des personnes,
c'est le seul choix cohérent avec ce que vous vendez.

### La règle à appliquer

| Table | Contenu | Fournisseur |
|---|---|---|
| `APPRENANTS`, `INSCRIPTIONS`, `PRESENCES & EMARGEMENTS`, `EVALUATIONS`, `ENTREPRISES & CLIENTS`, `FORMATEURS & PRESTATAIRES`, `STAGES & ALTERNANCES`, `MAILING LOG` | données personnelles | **Mistral** — exclusivement |
| `CATALOGUE FORMATIONS`, `CONFIG SYSTEME`, `DOCUMENTS OFFICIELS YEBA`, `RESSOURCES PÉDAGOGIQUES`, `INDICATEURS QUALIOPI`, `PARTENAIRES & FINANCEURS`, `FOURNISSEURS`, `CHARGES & ABONNEMENTS` | aucune donnée personnelle | Anthropic ou Mistral, au choix |

Activer les deux fournisseurs est parfaitement possible : le modèle se choisit
champ par champ. Ce qui compte, c'est de ne jamais poser un champ Anthropic sur
une table de la première ligne.

**Si vous n'activez qu'un seul fournisseur, activez Mistral.** Vous perdrez un
peu en qualité de rédaction ; vous garderez l'argument qui vous distingue.

## RGPD — les trois points à traiter avant d'activer

1. **Registre des traitements (art. 30).** Ajouter le fournisseur retenu comme
   sous-traitant, avec la finalité exacte des champs IA et le pays de traitement.
2. **Accord de sous-traitance (art. 28).** Celui de Baserow ne couvre pas le
   fournisseur d'IA : c'est un second sous-traitant, avec son propre acte.
3. **Mention d'information.** Si un champ IA traite des données de stagiaires,
   votre politique de confidentialité doit le dire. Elle ne le dit pas
   aujourd'hui — voir `site/app/` page « confidentialité ».

## IA Act — la question qui change le niveau de risque

Un champ IA qui **résume** ou **reformule** relève du risque minimal : aucune
obligation particulière.

Un champ IA qui **note, classe ou trie des personnes** bascule en **annexe III —
haut risque** : analyse d'impact, documentation technique, journalisation et
supervision humaine deviennent obligatoires (règlement (UE) 2024/1689).

Concrètement, dans votre base :

- « Résumer les objectifs de cette formation » → risque minimal ;
- « Évaluer l'aptitude de ce candidat » ou « classer ces prospects par
  potentiel » → **haut risque**, ne pas déployer sans le dossier complet.

## Vérifier que la connexion fonctionne

1. Ouvrez `CATALOGUE FORMATIONS` — aucune donnée personnelle, c'est le bon banc
   d'essai.
2. Ajoutez un champ de type **IA**, modèle `claude-haiku-4-5`.
3. Invite de test : *« Résume ce programme en une phrase de vingt mots
   maximum. »*
4. Générez sur une seule ligne.

Si rien ne se produit : vérifiez que la clé commence par `sk-ant-`, qu'un
plafond de dépense n'est pas déjà atteint, et que l'identifiant du modèle ne
comporte pas de suffixe de date.

## Un point que je n'ai pas pu vérifier

Le site de Baserow est inaccessible depuis cet environnement (blocage du proxy
réseau). Je n'ai donc **pas pu confirmer** que Baserow transmet bien les
identifiants de modèles récents sans les valider contre une liste interne.
Le champ étant libre, il devrait les accepter tels quels — mais faites le test
sur une ligne avant de généraliser.

## Sources

- Identifiants et tarifs des modèles : documentation de l'API Claude
  (référence interne, cache du 24/06/2026).
- [Configurer l'IA générative dans Baserow](https://baserow.io/user-docs/configure-generative-ai)
- RGPD (UE) 2016/679, art. 28, 30, 44 à 49.
- Règlement (UE) 2024/1689 sur l'intelligence artificielle, art. 6 et annexe III.
