# Sécurité de l'application ACM PASS LOISIRS

Référentiel de sécurité de la couche applicative, dérivé de l'audit du
07/09/2026 (constats S01–S07, M01–M06, J01–J07, G01–G02 ; contrôles C01–C12).

Ce document décrit ce qui est **implémenté**, ce qui est **impossible sans la
couche serveur**, et ce qui reste **à décider**. Il ne prétend pas établir la
conformité : l'audit rappelle qu'« un résultat “non testé” ne doit pas devenir
“conforme” ».

---

## 1. Les cinq règles

| # | Règle | État |
|---|---|---|
| 1 | Le secret ne quitte jamais le serveur | **Implémentée** — `securite/config.py` |
| 2 | Autorisation par objet, à chaque requête | **Implémentée** — `securite/autorisation.py` |
| 3 | Le serveur refuse | **Implémentée** — `securite/depart.py` |
| 4 | Filtrage en sortie, par rôle | **Implémentée** — `filtrer_sortie()` |
| 5 | Les fichiers passent par le serveur | **À implémenter** — dépend de l'hébergement |

---

## 2. Vecteurs d'attaque et état de la couverture

| Réf | Vecteur | Couverture |
|---|---|---|
| A1 | Jeton d'API exposé côté navigateur | **Couvert** : refus de démarrer sans secret d'environnement ; jeton jamais sérialisé ; empreinte SHA-256 dans les journaux |
| A2 | Partage public d'interface | **Non couvert par le code** — décision d'exploitation. Paramètre `PARTAGES_PUBLICS_AUTORISES = Non` ; tout partage doit être inscrit dans « Accès, jetons et partages » |
| A3 | URL de pièce jointe consommable hors habilitation | **Non couvert** — exige la route serveur de la règle 5 |
| A4 | Verdict de départ non bloquant | **Couvert** : le verdict est recalculé côté serveur et l'écriture est refusée |
| A5 | Édition directe des champs de droits | **Partiellement** : `Intégrité des droits` rend l'altération visible ; l'interdire exige des permissions par champ (plan supérieur) |
| A6 | Suppression des traces d'audit | **Partiellement** : `Horodatage système` détecte les trous ; le contrôle C09 exige un journal hors de portée de l'utilisateur |
| A7 | IDOR sur le portail parent | **Couvert** : `exiger_lecture_enfant()`, message neutre (pas de confirmation d'existence) |
| A8 | Saturation du formulaire public | **Couvert** : `LimiteurDebit` + `GardeAntiRejeu` + liste blanche de champs |
| A9 | Injection indirecte | **Atténué** : caractères de dissimulation supprimés, longueurs bornées. La protection réelle est de ne jamais traiter un contenu stocké comme une instruction |
| A10 | Hameçonnage sur la boîte d'alertes | **Atténué** : aucun contenu personnel dans les e-mails, avertissement en pied de message. Exige la MFA sur la boîte |

---

## 3. Ce que le code refuse — recette exécutable

```bash
python3 acm_passloisirs/tests/test_securite.py
```

25 contrôles, tous au vert au 08/09/2026. Les plus structurants :

- une **restriction judiciaire** bloque le départ **même avec une dérogation
  d'un responsable habilité** ;
- un **animateur ne peut pas s'auto-autoriser** une dérogation — correction du
  défaut `supervisor_override=True` relevé par l'audit dans le kit initial ;
- une autorisation **expirée**, **révoquée**, ou portant sur **un autre
  enfant**, bloque ;
- un **parent ne lit pas l'enfant d'une autre famille**, et le refus ne
  confirme pas l'existence de l'enregistrement ;
- l'**animateur ne reçoit ni finances, ni détail médical, ni pièce
  judiciaire** — mais reçoit la consigne opérationnelle utile à la sécurité de
  l'enfant ;
- le **prestataire technique** n'obtient aucun champ métier ;
- le formulaire public **refuse tout détail de santé** et tout champ non prévu ;
- le serveur **refuse de démarrer** sans secret, avec une clé de session trop
  courte, ou avec une origine générique.

---

## 4. Variables d'environnement

Aucune valeur par défaut sur les secrets : l'absence provoque un arrêt.

| Variable | Rôle |
|---|---|
| `ACM_JETON_BASE` | Accès à la base. **Jamais** dans le dépôt ni côté navigateur |
| `ACM_CLE_SESSION` | Signature des sessions. 32 caractères minimum |
| `ACM_ORIGINES_AUTORISEES` | Liste explicite. `*` refusé |
| `ACM_COOKIE_SECURISE` | `1` en production (non modifiable en production) |
| `ACM_DUREE_SESSION_MINUTES` | Défaut : 30 |

En-têtes appliqués à toutes les réponses (`EN_TETES_SECURITE`) : politique de
sécurité de contenu en `default-src 'none'`, `frame-ancestors 'none'`,
`Referrer-Policy: no-referrer`, `Cache-Control: no-store`, HSTS.

---

## 5. Hébergement et souveraineté

Hébergeurs visés : Scaleway (Paris), OVHcloud, Clever Cloud — tous européens,
tous avec un contrat de sous-traitance signable.

**Si la qualification HDS conclut à l'obligation** (paramètre
`HDS_QUALIFICATION`, non tranché), l'hébergeur doit être certifié HDS **sur
toute la chaîne**, pas seulement pour le stockage. Un hébergement européen seul
ne suffit pas.

---

## 6. RGPD et IA Act

**RGPD.** La couche serveur est un traitement à part entière : à inscrire au
registre (sous-traitant, hébergeur, journaux, durées). Les journaux applicatifs
contiennent des données personnelles — durée proportionnée, repère CNIL de 6 à
12 mois. Un portail parent déclenche l'obligation d'information et l'exercice
des droits par une voie identifiée. **L'AIPD doit être réexaminée** avant mise
en service : l'audit l'exige pour toute migration ou fonction nouvelle.

**IA Act.** Aucun composant décrit ici n'est un système d'IA : les calculs sont
déterministes, et l'audit rappelle qu'aucune conformité IA Act n'en découle.
Les obligations de transparence n'apparaîtraient qu'avec le chatbot envisagé —
et le vecteur A9 deviendrait alors un risque réel, à tester sur données
fictives avant toute activation.

---

## 7. Limites connues

1. Le limiteur de débit est **en mémoire du processus** : avec plusieurs
   instances, l'état doit être déporté, sinon la protection est divisée par le
   nombre d'instances.
2. Le **proxy de fichiers** (règle 5) n'est pas écrit : il dépend du choix de
   stockage, non tranché.
3. **Aucun test d'intrusion réel** n'a été mené. Ces tests prouvent que les
   règles écrites refusent ce qu'elles doivent refuser — pas qu'il n'existe pas
   d'autre chemin.
4. Tant que les données restent dans une base où les rôles ont un accès direct,
   les contrôles **C09** (protection des traces) et une partie de **C02**
   restent hors d'atteinte, quelles que soient les interfaces.
