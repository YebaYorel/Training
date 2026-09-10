# YEBA FORMATIONS — RAPPORT D'AUDIT DE CONFORMITÉ ET PLAN D'ACTION

Réf. **YEBA-AUDIT-2026-01** | Édition du 10/09/2026
Périmètre audité : base Airtable « YEBA FORMATIONS — Centre de formation (Adaptable) »
(`appQ2zqc80kkc6MR1`), **19 tables**, et l'intégralité des documents et écrits qu'elle contient.
Référentiels : code du travail (formation professionnelle), Référentiel National Qualité
(Qualiopi), RGPD, règlement (UE) 2024/1689, code de commerce, code de la consommation, BOFiP.

---

## 1. CE QUI A ÉTÉ AUDITÉ, ET CE QUI N'A PAS PU L'ÊTRE

**Audité intégralement :**
- 19 tables, leurs champs, leurs descriptions et leurs options de listes.
- Les 7 fiches du `CATALOGUE FORMATIONS` : objectifs, prérequis, public, programmes détaillés
  (de 7 000 à 24 000 caractères chacun), modalités d'évaluation, délais d'accès, tarifs.
- Les 4 fiches de `RESSOURCES PÉDAGOGIQUES` (livret, grille critériée, quiz Copilot).
- La table `CONFIG SYSTÈME` (18 paramètres), `INDICATEURS QUALIOPI` (32 lignes),
  `FORMATEURS & PRESTATAIRES`, `APPRENANTS`, `INSCRIPTIONS`, `SESSIONS`, `DEVIS & FACTURES`.

**Non auditable dans cette session — à vérifier vous-même :**

| Élément | Motif |
|---|---|
| `conditions_generales_de_vente.pdf` (78 Ko) | La politique réseau de l'environnement bloque le domaine des pièces jointes Airtable. **Contenu jamais lu.** |
| `reglement_interieur.pdf` (379 Ko) | Idem. |
| Les 6 fichiers `.docx` et `.pptx` joints aux fiches | Idem. |

> **Conséquence à assumer.** Les CGV et le règlement intérieur livrés ici sont **écrits à neuf**,
> pas corrigés. C'est ce que vous demandiez — un corpus homogène — mais **relisez les anciens PDF
> avant de les archiver** : une clause spécifique que vous aviez négociée avec un client pourrait
> s'y trouver et se perdre.

---

## 2. LES CINQ CONSTATS QUI COMPTENT

### Constat 1 — Le socle documentaire était incomplet aux deux tiers

Sur les 14 documents qu'un organisme certifié Qualiopi doit pouvoir produire à un auditeur,
à un OPCO ou à un client, **2 existaient** (CGV et règlement intérieur, en pièce jointe).

**Manquaient totalement :** mentions légales, politique de confidentialité, convention de
formation, **contrat de formation pour les particuliers**, convention de sous-traitance,
charte qualité, politique handicap, procédure de réclamation, charte d'usage de l'IA,
politique tarifaire, notice des financements, charte graphique.

### Constat 2 — Une non-conformité immédiate sur la vente aux particuliers

Aucun **contrat de formation professionnelle** (art. L.6353-3 du code du travail) n'existait.
Or ce contrat est **obligatoire** dès qu'une personne physique paie sa formation elle-même,
et il seul porte les protections d'ordre public : **délai de rétractation de 10 jours**,
**interdiction d'encaisser quoi que ce soit avant son expiration**, **plafond de 30 % au premier
versement**.

Utiliser une convention de formation à la place — ce qui est l'usage quand le bon document
n'existe pas — expose à la nullité de la clause de prix et à une sanction administrative.

### Constat 3 — Le CPF n'est pas mobilisable, et le dire serait trompeur

Le champ « Code RNCP ou RS » est **vide sur les 7 fiches**. Sans certification enregistrée,
une action n'est pas éligible au CPF (art. L.6323-6). L'option « CPF » figurait pourtant dans
la liste des financements de la base.

Annoncer un financement CPF indisponible est une **pratique commerciale trompeuse**
(art. L.121-2 du code de la consommation). L'option a été retirée des fiches.

### Constat 4 — Les tarifs rendaient l'offre invendable

| Fiche | Tarif inter enregistré | Réalité |
|---|---|---|
| Initiation à la vente (7 h) | **35 €** | Une journée de formation à 35 € |
| Management en institut (7 h) | **107,14 €** | Exactement 1 500 ÷ 14 : un artefact de calcul |
| Vente-conseil en institut (7 h) | **48,21 €** | Même nature |
| Automatisation, RGPD & Cyber, Copilot | **aucun** | 3 fiches sans prix |

La publication des tarifs est une **obligation** (RNQ, indicateur 1). Trois fiches sur sept
étaient donc non conformes, et trois autres affichaient des montants qui auraient détruit
votre positionnement.

### Constat 5 — L'incohérence de souveraineté

Vous vendez du conseil en gouvernance des données et vous exigez la souveraineté européenne.
**Votre base de gestion — nom, prénom, email, téléphone, employeur, résultats d'évaluation de
chaque stagiaire — est hébergée par Airtable Inc., société de droit américain.** Votre
messagerie professionnelle est chez Google LLC.

Ce n'est **pas illicite** : les transferts hors UE sont admis sous garanties (RGPD, chapitre V).
Mais ils doivent être documentés — ils le sont désormais, à la section 4 de votre politique de
confidentialité. Et surtout : **c'est l'objection que vous poserez à vos propres prospects.**
Un concurrent, un DRH averti ou un auditeur vous la posera.

---

## 3. CE QUI A ÉTÉ PRODUIT

### 3.1 Identité

- **Logo vectoriel sans l'œil** (`yeba/identite/logo-yeba-sans-oeil.svg`). L'œil sur pyramide
  se lisait comme un symbole de surveillance — l'inverse exact de ce que vous vendez.
  Remplacé par un nœud de connexion ; les trois formes se lisent comme des pitons.
- **Charte graphique** : palette, **règle de contraste WCAG 2.1** (l'or ne touche jamais le
  blanc en texte : 2,29 : 1, échec à tous les niveaux), corps typographiques minimaux,
  bloc-marque, encart assurance, règle de marque blanche.

### 3.2 Les 14 documents du socle

| Réf. | Document | Statut |
|---|---|---|
| YEBA-IDENT | Charte graphique et règles de marque | En vigueur |
| YEBA-DOC-01 | Mentions légales | Incomplet — 8 données à fournir |
| YEBA-DOC-02 | Politique de confidentialité | En vigueur |
| YEBA-DOC-03 | Conditions générales de vente | Incomplet — assurance, médiateur |
| YEBA-DOC-04 | Règlement intérieur | **Diffusable en l'état** |
| YEBA-DOC-05 | Convention de formation (entreprise) | Incomplet — assurance |
| YEBA-DOC-06 | **Contrat de formation (particulier)** | Incomplet — médiateur (bloquant) |
| YEBA-DOC-07 | Convention de sous-traitance (volets A et B) | **Diffusable en l'état** |
| YEBA-DOC-08 | Politique handicap et accessibilité | **Diffusable en l'état** |
| YEBA-DOC-09 | Procédure de réclamation | Incomplet — médiateur |
| YEBA-DOC-10 | Charte qualité | À valider |
| YEBA-DOC-11 | Charte d'usage de l'IA | **Diffusable en l'état** |
| YEBA-DOC-12 | Politique tarifaire | À valider — 6 points |
| YEBA-DOC-13 | Notice des financements | **Diffusable en l'état** |

Tous portent la même trame : référence, version, date, base légale citée article par article,
et le **bloc-marque normalisé**. Tous sont stockés **en texte intégral** dans la nouvelle table
`DOCUMENTS OFFICIELS YEBA` de la base, et versionnés dans le dépôt Git.

### 3.3 La base devenue une base YEBA FORMATIONS

| Ce qui a été fait | Où |
|---|---|
| Table `DOCUMENTS OFFICIELS YEBA` créée, 14 documents chargés en texte intégral | Nouvelle table |
| Champ **« Marque / Confidentialité contractuelle »** créé et renseigné sur les 7 fiches | `CATALOGUE FORMATIONS` |
| Champ **« Tarifs affichés (texte public) »** créé et renseigné sur les 7 fiches | `CATALOGUE FORMATIONS` |
| Tarifs inter et intra fixés sur les 5 formations du catalogue YEBA | `CATALOGUE FORMATIONS` |
| Tarifs artefacts (107,14 € et 48,21 €) effacés sur les 2 fiches en sous-traitance | `CATALOGUE FORMATIONS` |
| Durée, domaine, type, statut, accessibilité, régime TVA complétés sur les fiches incomplètes | `CATALOGUE FORMATIONS` |
| Option « CPF » retirée des financements éligibles | `CATALOGUE FORMATIONS` |
| 22 paramètres d'entreprise ajoutés (assurance, TVA, DEETS, barèmes, médiateur, marque blanche…) | `CONFIG SYSTÈME` |

---

## 4. LE PLAN D'ACTION — 13 ACTIONS

### Priorité 1 — À traiter sous 15 jours

| # | Action | Pourquoi | Qui |
|---|---|---|---|
| **A-04** | **Adhérer à un dispositif de médiation de la consommation** et publier les coordonnées du médiateur | **Obligation légale** (C. conso, art. L.612-1). Amende administrative encourue (art. L.641-1). **Bloque la signature de tout contrat avec un particulier.** | Dirigeant |
| **A-09** | **Utiliser le contrat YEBA-DOC-06 pour tout particulier**, et jamais la convention | Le contrat seul porte la rétractation de 10 jours et l'échelonnement légal (L.6353-5 et L.6353-6) | Dirigeant |
| **A-14** | **Transmettre l'attestation d'assurance RC Pro** — assureur, n° de police, montant, validité, étendue | 5 documents contiennent un encart assurance à trous. Un OPCO ou un donneur d'ordre public le réclame systématiquement | Dirigeant → à me transmettre |
| **A-08** | **Trancher la question CPF** : partenariat avec un certificateur RS (voie rapide) ou dépôt propre | Sans RNCP/RS, aucune communication CPF n'est licite. Le partenariat est la voie recommandée sur « IA générative » et « protection des données » | Dirigeant |

### Priorité 2 — À traiter sous 1 à 2 mois

| # | Action | Pourquoi |
|---|---|---|
| **A-12** | **Reprendre les 32 lignes de `INDICATEURS QUALIOPI`** : toutes sont en « C (non conforme) », aucune preuve renseignée | En l'état, votre propre auto-audit déclare l'organisme non conforme sur les 32 indicateurs. Un auditeur qui ouvre cette table part avec un a priori très défavorable |
| **A-07** | **Lancer la préparation de l'audit Qualiopi** — certificat valable jusqu'au **16/02/2027** | La préparation se mène 6 mois avant. Le point de contrôle était dû au 16/08/2026 : **vous êtes déjà en retard** |
| **A-06** | **Décider de la mention publiée sur les indicateurs de résultats** — la mention transitoire proposée, ou des chiffres réels | Publier un taux inventé est plus grave que ne rien publier |
| **A-11** | **Supprimer les 2 champs neutralisés** de `APPRENANTS` : « Type de handicap » et « Document RQTH » | Données de santé (RGPD art. 9). La suppression ne peut se faire que manuellement dans l'interface Airtable |
| **A-05** | **Formaliser un contact référencé** avec l'Agefiph Océan Indien ou la Ressource Handicap Formation | Les indicateurs 26 et 28 exigent une preuve de mobilisation effective, pas une liste de noms |
| **A-10** | **Réclamer un contrat écrit** au donneur d'ordre de FOR-0005 et FOR-0007, s'il n'existe pas | Sans écrit, l'étendue de la marque blanche et le délai de paiement ne sont pas opposables |

### Priorité 3 — Structurel

| # | Action | Pourquoi |
|---|---|---|
| **A-01** | **Migrer la base de gestion vers un hébergement UE** et basculer la messagerie sur le nom de domaine | Cohérence avec votre positionnement. Le dépôt technique existe déjà (intégration Baserow, cloud UE, Pays-Bas) |
| **A-02** | **Vérifier et attester les 4 mesures de sécurité** : double authentification, gestionnaire de mots de passe, chiffrement du poste, sauvegarde 3-2-1 testée | Vous enseignez ces mesures en formation RGPD & Cybersécurité |
| **A-03** | **Ouvrir le registre des violations de données** | Obligatoire même sans violation à déclarer (RGPD art. 33.5) |
| **A-13** | **Vérifier sur EUR-Lex la référence au « règlement (UE) 2026/1744 »** citée dans vos supports pédagogiques | Cette référence figure dans le livret Copilot et le quiz. Elle **n'a pas pu être vérifiée à la source** ici. Une référence juridique inexacte devant un client de conseil RGPD est un dommage de crédibilité disproportionné |

---

## 5. CRITIQUE DE MON PROPRE TRAVAIL

Vous demandez systématiquement que je cherche les failles de ma propre proposition. Voici les
sept que j'identifie.

**Faille juridique — le numéro Qualiopi.** Vous avez tranché pour `25FOR02027.1`. Or vos propres
supports pédagogiques rédigés le 09/09/2026 portent `25FOF02027.1`, et votre profil professionnel
aussi. **J'ai appliqué votre décision partout, mais deux sources sur trois disaient l'inverse.**
Un numéro de certification erroné sur une convention est un faux en écriture commerciale.
**Vérifiez sur le certificat papier avant diffusion.** Les supports pédagogiques anciens portent
encore `FOF` et devront être alignés sur ce que dit le certificat.

**Faille juridique — les durées de conservation.** J'ai retenu 5 ans pour les pièces d'exécution
et 10 ans pour les pièces comptables. Ces durées sont défendables et usuelles, mais certains
financeurs imposent des durées contractuelles plus longues. **Vérifiez les conventions de vos
OPCO avant de figer la politique de confidentialité.**

**Faille économique — la grille tarifaire.** Je l'ai construite sur une lecture du marché
réunionnais et sur vos coûts internes, **sans étude concurrentielle réelle** : je n'ai pas eu
accès aux tarifs de vos concurrents. 490 € par personne et par jour sur l'IA est cohérent avec
un positionnement de rareté, mais si trois organismes locaux affichent 350 €, l'argument ne
tiendra que si la preuve de rareté est visible **avant** le prix. C'est pourquoi la grille est
marquée « à valider », et non « en vigueur ».

**Faille économique — les tarifs de conseil.** Les cinq montants de la section 5 de la politique
tarifaire **ne reposent sur aucune donnée existante dans votre base**. Ce sont des propositions
calibrées sur un budget de TPE réunionnaise. Traitez-les comme un point de départ de discussion,
pas comme un acquis.

**Faille de faisabilité — la charge administrative.** Les engagements de la charte qualité
(réponse en 48 h, devis en 5 jours, attestation en 15 jours, évaluation à froid à J+30, revue
trimestrielle) sont **opposables** : un client peut vous les rappeler. Pour une structure
unipersonnelle en pleine activité de formation, tenir douze engagements chiffrés suppose des
automatisations. **Si vous n'êtes pas certain de tenir un délai, corrigez-le maintenant :**
il vaut mieux annoncer 72 h et tenir que 48 h et manquer.

**Faille technique — les typographies non vérifiables.** Les PDF existants n'ont pas pu être
lus. Je ne peux donc **pas** affirmer que le nouveau corpus ne perd rien de l'ancien. Le seul
moyen de le savoir est de les ouvrir et de comparer.

**Faille de méthode — le report de l'AI Act.** Vos supports affirment qu'un règlement de 2026
a reporté au 2 décembre 2027 les obligations des systèmes à haut risque. **Je n'ai pas pu
vérifier cette référence à la source.** Je l'ai donc reprise dans la charte IA **assortie d'une
réserve explicite**, et je ne l'ai citée dans aucun document contractuel. C'est la seule position
défendable : sur un sujet où vous vendez de l'expertise, citer un texte qu'on n'a pas vérifié est
le risque le plus élevé de tout ce dossier.

---

## 6. CE QUE JE VOUS DEMANDE POUR ALLER PLUS LOIN

1. **L'attestation d'assurance RC Pro** — 5 informations. Elle débloque 5 documents.
2. **Le certificat Qualiopi** — pour trancher `FOR` ou `FOF` de façon définitive.
3. **Forme juridique, capital, RCS, code APE, n° de TVA intracommunautaire.**
4. **Le nom de votre hébergeur de site** et le pays de ses serveurs.
5. **Votre validation, ligne par ligne, de la grille tarifaire.**
6. **Le contrat de sous-traitance** de FOR-0005 et FOR-0007, s'il existe — pour vérifier
   l'étendue exacte de la clause de confidentialité que j'ai supposée.

---
────────────────────────────────────────
**YEBA FORMATIONS** — Aurélien LUMEKA, directeur
9 rue Françoise Châtelain, 97490 Sainte-Clotilde, La Réunion
Tél. 0693 32 24 45 — yebaformations@gmail.com
SIRET 814 622 262 00032
Déclaration d'activité n° 04973676397 auprès du Préfet de La Réunion.
*Cet enregistrement ne vaut pas agrément de l'État.*
Certification **Qualiopi n° 25FOR02027.1** délivrée au titre de la catégorie
**actions de formation** — organisme certificateur Qualitia (accrédité COFRAC).
Référent handicap : Aurélien LUMEKA — yebaformations@gmail.com
────────────────────────────────────────

*Ce rapport a été conçu avec l'assistance d'un système d'IA générative
(règlement (UE) 2024/1689, art. 50). Les références juridiques doivent être vérifiées à la
source avant toute diffusion à un tiers, conformément à la charte YEBA-DOC-11.*
