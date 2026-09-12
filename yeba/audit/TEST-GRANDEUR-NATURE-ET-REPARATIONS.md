# Test grandeur nature du workspace YEBA FORMATIONS — et réparations

**Référence** : YEBA-AUDIT-03
**Version** : 1.0
**Date** : 11 septembre 2026
**Base testée** : Airtable « YEBA FORMATIONS » — `appQ2zqc80kkc6MR1`
**Objet** : simulation complète de trois parcours clients, relevé des défauts, réparation de la base.

---

## 1. Ce qui a été simulé

Trois parcours ont été créés de bout en bout dans la base réelle, avec des données préfixées `ZZTEST-`,
puis **intégralement supprimées** à l'issue du test (vérification faite : plus aucune occurrence
de `ZZTEST` dans aucune table).

| # | Scénario | Ce qui a été créé |
|---|---|---|
| 1 | **Client intra-entreprise** — une boulangerie veut former 6 salariés au RGPD | 1 entreprise, 3 apprenants, 1 session intra sur 2 jours, 3 inscriptions |
| 2 | **Client inter-entreprise** — un cabinet inscrit 1 salarié à une session IA | 1 entreprise, 1 apprenant, 1 session inter, 1 inscription |
| 3 | **Trois jeunes en autofinancement** — formation RGPD & IA Act | 3 apprenants sans employeur, 1 session passée, 3 inscriptions |

Rôles endossés pour la lecture des résultats : directeur, secrétaire, comptable, juriste, stagiaire.

---

## 2. Ce qui marchait déjà

Il faut le dire, parce que ce n'est pas rien :

- Le calcul automatique du **nombre d'inscrits** et des **places restantes** : juste, à la place près.
- Le **pourcentage de réussite** par stagiaire.
- La **référence d'inscription** et l'**e-mail stagiaire** reconstitués automatiquement.
- L'alerte **mallette formateur J-2** et son récapitulatif automatique.
- L'automatisation **A-01** se déclenchait bien et journalisait dans MAILING LOG.

---

## 3. Les défauts trouvés

Classés par gravité. « Bloquant » signifie : obligation légale non tenue ou stagiaire non informé.

### 3.1 Bloquants

| # | Défaut constaté pendant le test | Conséquence réelle |
|---|---|---|
| D-01 | **A-02 (convocation J-7) était désactivée.** | Aucun stagiaire n'a jamais reçu de convocation depuis la création de la base. Manquement à l'art. L.6353-8 c. trav. et au RNQ ind. 3. |
| D-02 | **Le courriel « documents légaux » de A-01 joignait les champs « Règlement intérieur PDF *signé* » et « RGPD PDF *signé* »** — c'est-à-dire les documents que le stagiaire doit *retourner*, donc vides à l'inscription. | Le stagiaire recevait un message affirmant « veuillez trouver en pièce jointe le règlement intérieur, les CGV, la politique de confidentialité » **sans aucune pièce jointe**. Pire qu'un oubli : une affirmation fausse dans un flux contractuel. |
| D-03 | **A-01 ne se déclenchait que sur le statut « Confirmé ».** Les trois jeunes, passés en « Présent », n'ont rien reçu. | Ni règlement intérieur, ni CGV, ni politique de confidentialité. Exactement le cas que vous redoutiez. |
| D-04 | **Le champ « Prêt à envoyer » valait OUI dès J+2 après l'inscription, sans regarder la date de session.** | Les courriels de bienvenue et de positionnement seraient partis pour une session **déjà terminée en août**. |
| D-05 | **Aucun formulaire n'existe dans la base** (`standaloneForms: []`, `embeddedForms: []`). | La porte d'entrée est fermée : l'automatisation « 1️⃣ Pré-inscription reçue » ne peut jamais se déclencher, et il n'y a ni test de positionnement ni questionnaire de satisfaction à envoyer. |
| D-06 | **Aucune automatisation n'existait pour l'attestation de fin de formation.** | Manquement à l'art. L.6353-1 al. 3 c. trav. — pièce systématiquement réclamée en contrôle DEETS. |
| D-07 | **« Automation 1 » utilisait `getBaseMetadata(champ,"id")` une dizaine de fois.** | Le devis client aurait été envoyé en imprimant les identifiants techniques : « Durée … `fldbZPoKlbpTOip6J` h sur `fldaT51SDtAfW8Qbs` jour(s) ». Elle se déclenchait en outre à la *création d'une fiche entreprise*, donc avant qu'il existe le moindre devis. |
| D-08 | **Ce même message annonçait « TVA non applicable, art. 293 B du CGI ».** | 293 B, c'est la franchise en base (petits chiffres d'affaires). Votre régime est l'**exonération de l'art. 261-4-4° a du CGI**, réservée aux organismes de formation déclarés. Mauvais article sur un devis = mention opposable erronée. |
| D-09 | **Aucun traitement du cas « particulier ».** Pas de contrat de formation, pas de délai de rétractation, pas de plafond d'acompte. | Les trois jeunes en autofinancement relèvent des art. L.6353-3 à L.6353-7 c. trav. : contrat, 10 jours de rétractation, aucun encaissement avant terme puis 30 % maximum. Rien de tout cela n'existait. |

### 3.2 Défauts de fiabilité

| # | Défaut | Détail |
|---|---|---|
| D-10 | **SESSIONS · « Rappel J-7 dû » renvoyait `0`** au lieu de OUI/NON | `AND(...)` imbriqué dans un `IF` avec résultat numérique, et `WORKDAY_DIFF = 7` exactement — donc vrai un seul jour, et faux si ce jour tombe un week-end. |
| D-11 | **Le champ « Mention » n'était jamais rempli et aucun seuil n'était défini** | Un stagiaire à 11/20 (55 %) n'était signalé nulle part, alors que les programmes annoncent un seuil de 7/10. |
| D-12 | **Le tableau de bord affiche « Nombre d'inscrits »** (champ texte manuel, vide) au lieu de « Nb inscrits (auto) » qui, lui, fonctionne | Les compteurs de l'interface sont faux. |
| D-13 | **Rien ne crée les lignes de PRESENCES & EMARGEMENTS ni d'EVALUATIONS** | Saisie manuelle, par stagiaire et par demi-journée. |
| D-14 | **Le chiffre d'affaires session n'est pas dérivé du tarif catalogue** | « Marge brute » n'a donc aucun sens tant que le CA est saisi à la main. |

### 3.3 Bruit et données parasites

| # | Constat |
|---|---|
| D-15 | **47 enregistrements dans ALERTES & TÂCHES**, dont 32 « Non-conformité — Indicateur N » du 10/08 jamais clôturées, **6 doublons « Mise en demeure — FAC-0001 »** (10/08, 16/08, 22/08, 27/08, 01/09, 06/09, 11/09) sur une seule facture d'avril, 2 « Récap du jour », 2 fiches vides d'avril. |
| D-16 | **MAILING LOG** : 3 enregistrements vides d'avril + un résidu « BELLUCCI Monica ». |
| D-17 | **Table `SUIVI ANTHO`** : table modèle Airtable par défaut (Name / Notes / Assignee / Status / Attachments), 3 enregistrements entièrement vides. |
| D-18 | Champs obsolètes ou interdits toujours présents (voir § 6, suppression manuelle obligatoire). |

### 3.4 Une découverte qui vous concerne directement

**Un processus extérieur à Airtable écrit toujours dans la base.** Les alertes « Mise en demeure —
FAC-0001 » se recréent tous les 5 à 6 jours — la dernière datée du **11/09/2026, aujourd'hui** — et
« Récap du jour — Radar Inscriptions » est daté du 10/09. **Aucune des automatisations Airtable n'a de
déclencheur horaire** : ces écritures viennent donc d'un outil tiers (Make, n8n, Zapier ou un script).

Je ne peux ni le voir ni l'arrêter depuis la base. À vérifier de votre côté : il tourne en boucle sur une
seule facture d'avril de 2 000 € et pollue votre table d'alertes depuis un mois.

---

## 4. Les réparations effectuées

### 4.1 Formules corrigées

| Champ | Avant | Après |
|---|---|---|
| SESSIONS · `Rappel J-7 dû` | renvoyait `0` | renvoie OUI/NON sur une fenêtre J-7 → J-1, session Confirmée uniquement |
| INSCRIPTIONS · `Prêt à envoyer` | OUI dès J+2 après inscription, même pour une session passée | OUI seulement si la session **n'a pas encore démarré** ; le délai de vérification de 2 jours est ignoré quand la session démarre dans 10 jours ou moins, pour ne jamais envoyer trop tard |

### 4.2 Champs créés — le poste de pilotage

Deux champs, et deux seulement, à lire au quotidien. Tout le reste travaille derrière.

**SESSIONS · `⚠️ Contrôle avant ouverture`**
Passe en revue, à votre place : formation rattachée, dates, horaires, lieu, formateur, pack légal
rattaché, PDF réellement en ligne, programme PDF, cohérence places/inscrits, seuil minimum d'ouverture,
et session non confirmée à moins de 10 jours du départ. Tant qu'il n'affiche pas
**« ✅ Session conforme — prête à partir »**, rien ne part. C'est volontaire (voir § 4.4).

**INSCRIPTIONS · `🧭 Contrôle dossier stagiaire`**
Se règle tout seul sur la phase du stagiaire — **avant / pendant / après** la formation — et n'affiche
que ce qui reste à faire, **avec le fondement juridique en clair** :
⛔ = bloquant, ⚠️ = à traiter, ✅ = rien à faire.

> Exemple de ce qu'il affiche :
> *« AVANT LA FORMATION — ⛔ Règlement intérieur non envoyé (R.6352-1 c. trav. : porté à la connaissance
> du stagiaire AVANT son entrée en formation). ⚠️ Test de positionnement non envoyé (RNQ ind. 4 :
> analyse du besoin du bénéficiaire — preuve exigée à l'audit). »*

### 4.3 Champs créés — le régime contractuel (le cas des trois jeunes)

| Champ | Ce qu'il fait |
|---|---|
| `Régime contractuel (auto)` | Dit s'il faut une **convention** (art. L.6353-2 — un tiers finance) ou un **contrat de formation professionnelle** (art. L.6353-3 à L.6353-7 — le stagiaire paie lui-même), et rappelle les obligations attachées |
| `Fin du délai de rétractation (10 j)` | Date calculée depuis la signature (art. L.6353-5) |
| `💶 Encaissement autorisé ?` | Répond à la seule question de la comptabilité : ⛔ contrat non signé / ⛔ délai en cours jusqu'au JJ/MM/AAAA / ✅ acompte encaissable, plafonné à 30 % (art. L.6353-6) |
| `Résultat calculé (seuil 70 %)` | Applique le seuil annoncé dans vos programmes (7/10) et propose la mention. Sous 70 % : *« ⚠️ Ajourné — prévoir un entretien et tracer la suite donnée (RNQ ind. 11 et 30) »* |
| `Nb de lignes d'émargement` | Zéro = aucune feuille d'émargement, pièce exigée en contrôle (L.6362-1) |
| `Consentement RGPD`, `Situation de handicap`, `Aménagements nécessaires` | Remontés de la fiche apprenant pour déclencher le réflexe référent handicap sans jamais collecter de donnée de santé (RGPD art. 9) |

### 4.3 bis  Deux contradictions publiques tranchées

| Point | Décision | Ce qui a été corrigé |
|---|---|---|
| **Délai d'accès** | **15 jours ouvrés partout** | La charte qualité (YEBA-DOC-10, engagement n° 3) annonçait 15 jours, les fiches FOR-0009 et FOR-0010 annonçaient 10. Deux délais publics contradictoires, relevés en audit (RNQ ind. 1). Les deux fiches sont réécrites sur 15 jours ouvrés, avec la justification du délai (montage du financement, test de positionnement, convocation). |
| **Référent handicap** | **Aurélien LUMEKA, nommément désigné** | Le socle documentaire le nommait déjà ; la base Airtable, non. A-01, A-02 et A-04 disent désormais « votre référent handicap est Aurélien LUMEKA — yebaformations@gmail.com — 0693 32 24 45 ». Le RNQ ind. 26 attend un interlocuteur identifié, pas une fonction anonyme. |

### 4.4 La chaîne de preuve Qualiopi

C'est votre demande sur le test de positionnement, généralisée à tous les documents.

```
DOCUMENTS OFFICIELS YEBA ──┬── 🎯 Indicateurs Qualiopi prouvés ──→ INDICATEURS QUALIOPI
   (la vie de l'entreprise) │                                          (l'audit)
                            └── 📚 Sessions où ce document est remis ──→ SESSIONS
                                                                         (la formation)
```

Concrètement :
- Sur **INDICATEURS QUALIOPI**, un champ `📄 Documents de preuve YEBA`. Les **13 documents du socle ont
  été rattachés** à leurs indicateurs (DOC-01 → ind. 1 et 3 ; DOC-04 règlement intérieur → ind. 3, 9,
  16, 28 ; DOC-08 handicap → ind. 1, 8, 20, 26, 28, 32 ; DOC-10 charte qualité → les 7 critères ; etc.).
- Sur **SESSIONS**, un champ `📎 Pack légal remis aux stagiaires` : vous y rattachez une fois les
  documents remis, et leurs PDF descendent automatiquement jusqu'au courriel du stagiaire
  (`Pack légal (PDF auto)` → `Pack légal (PDF) (from Session)`).
- Un même document apparaît donc **simultanément** dans les documents de l'entreprise, dans les
  documents de la formation et dans le dossier Qualiopi. Un clic depuis l'indicateur montre à
  l'auditeur où le document a réellement été remis.

**Verrou associé** : le `⚠️ Contrôle avant ouverture` de la session n'affiche « conforme » que si le pack
est rattaché **et** que les PDF sont réellement en ligne. A-01 ne part que sur une session conforme.
Résultat : le défaut D-02 — annoncer des pièces jointes inexistantes — est structurellement impossible.

### 4.5 Automatisations

| Automatisation | État | Ce qui a été fait |
|---|---|---|
| **A-01 — Pack d'accueil stagiaire** | reconstruite | Un seul courriel : programme + règlement intérieur + CGV + politique de confidentialité en pièces jointes réelles, accessibilité et référent handicap, information RGPD art. 13 complète, transparence IA (AI Act art. 50), procédure de réclamation. Déclenchement élargi à **Confirmé ET Présent**. Quatre verrous : session conforme, session non démarrée, envoi unique, pack réellement disponible. Coche les 5 cases de traçabilité et journalise. |
| **A-02 — Convocation J-7** | corrigée, **à activer** | Statuts élargis, verrou « session conforme », corps complété (règlement intérieur applicable, émargement et son lien avec le financement, annulation, accessibilité, attestation à venir), journalisation ajoutée. |
| **A-03 — Attestation de fin de formation** | **créée** | Part dès que la session est finie et la note saisie. Contient les **quatre mentions exigées** par l'art. L.6353-1 al. 3 : objectifs, nature, durée, résultats de l'évaluation des acquis. Coche « générée » et « envoyée », journalise. |
| **A-04 — Devis + convention au client entreprise** | **reconstruite** (ex-« Automation 1 ») | Déplacée sur DEVIS & FACTURES, déclenchée quand vous passez un devis au statut « Envoyé ». Toutes les valeurs sont de vraies valeurs. TVA corrigée en **art. 261-4-4° a du CGI**. Délais harmonisés avec vos CGV (48 h ouvrées / 15 jours ouvrés). Programme et pack légal en pièces jointes. Réserve explicite sur le financement OPCO. |
| **A-08 — Veille hebdomadaire du directeur** | **créée** | Chaque lundi 7 h (heure de La Réunion), un courriel unique listant les dossiers stagiaires bloqués et les sessions non conformes. C'est le filet : plus aucun envoi ne peut être muet sans que vous le sachiez. |

### 4.6 Nettoyage

| Élément | Action |
|---|---|
| ALERTES & TÂCHES | **43 enregistrements supprimés** sur 47. Les 32 « Non-conformité — Indicateur N » sont intégralement conservées dans INDICATEURS QUALIOPI (statut et score par indicateur) : rien n'est perdu. Des 7 « Mise en demeure — FAC-0001 », **la plus récente est conservée** (11/09) et les 6 doublons supprimés. Restent 4 alertes réelles. |
| MAILING LOG | 4 enregistrements parasites supprimés (3 vides d'avril + résidu « BELLUCCI Monica »). |
| Table `SUIVI ANTHO` | **supprimée** — table modèle Airtable, 3 enregistrements entièrement vides. Restauration possible via l'identifiant d'action `actlEWzln46KInwIS`. |
| Données de test | **intégralement effacées** : 2 entreprises, 6 apprenants, 3 sessions, 6 inscriptions, 3 lignes MAILING LOG. Vérifié : plus aucune occurrence de `ZZTEST`. |

---

## 5. Ce que l'API Airtable ne permet pas — et qui reste à faire à la main

Trois limites techniques, pas des oublis. Je les ai vérifiées une par une.

### 5.1 Activer les automatisations — 4 clics

L'API expose l'état de déploiement mais **aucun outil ne permet d'activer une automatisation**. À faire
dans Airtable → onglet *Automatisations* → bouton en haut à droite :

1. **A-02 — Convocation J-7** → **Activer** ← *la plus urgente : aucune convocation n'est jamais partie*
2. **A-03 — Attestation de fin de formation** → **Activer**
3. **A-04 — Devis + convention au client entreprise** → **Activer**
4. **A-08 — Veille hebdomadaire du directeur** → **Activer**
5. **A-01** est déjà active, mais elle a été réécrite : ouvrez-la et cliquez sur **Mettre à jour** pour
   publier la nouvelle version.

### 5.2 Créer les formulaires — la porte d'entrée

L'API ne sait créer que des pages `visualization`, `dashboard` et `recordDetail` : **pas de formulaire**.
Trois formulaires sont à créer à la main (Airtable → *Interfaces* → *Form*, ou une vue Formulaire) :

| Formulaire | Table | Champs | Utilité |
|---|---|---|---|
| **Pré-inscription** | APPRENANTS | Nom, civilité, e-mail, téléphone, entreprise, fonction, niveau, session souhaitée, situation de handicap (oui/non) + aménagements souhaités, consentement RGPD | Déclenche l'automatisation « 1️⃣ Pré-inscription reçue », aujourd'hui inerte |
| **Test de positionnement** | EVALUATIONS (type « Positionnement ») | Attentes, niveau perçu, cas concret à traiter, contraintes | **RNQ ind. 4** — analyse du besoin. C'est votre exemple : le test part, revient, s'analyse, et la fiche devient l'élément de preuve |
| **Évaluation à chaud** | EVALUATIONS (type « À chaud ») | Satisfaction, atteinte des objectifs, formateur, organisation, verbatim | **RNQ ind. 30 et 31** |

⚠️ Sur le formulaire de pré-inscription : **ne demandez jamais la nature du handicap**, seulement les
aménagements souhaités. Une donnée de santé relève de l'art. 9 du RGPD et vous n'avez aucune base légale
pour la collecter.

### 5.3 Supprimer des champs et renommer une option de liste

L'API n'expose ni `delete_field` ni la modification des options d'une liste déroulante.

**À supprimer** (clic droit sur l'en-tête de colonne → *Supprimer le champ*) :

| Table | Champ |
|---|---|
| CATALOGUE FORMATIONS | `⚠️ Ancien bloc tarifaire manuel (obsolète)` |
| INSCRIPTIONS | `⚠️ Ancien SESSIONS (obsolète — ne pas utiliser)` |
| APPRENANTS | `Field 47` |
| APPRENANTS | `Entreprise` (liste déroulante en doublon du lien « Entreprise employeur ») |
| APPRENANTS | `⚠️ NE PAS REMPLIR — Type de handicap` ← **RGPD art. 9, donnée de santé** |
| APPRENANTS | `⚠️ NE PAS REMPLIR — Document RQTH` ← **RGPD art. 9, donnée de santé** |

**À renommer** — DEVIS & FACTURES, champ « Statut TVA », option
`Exonéré TVA Art.264-4-4a CGI` → **`Exonéré TVA — art. 261-4-4° a du CGI`**.
L'article 264 ne traite pas de ce sujet ; cette mention figure sur vos factures.

### 5.4 Corriger le tableau de bord

Interface « Cockpit YEBA », page *Tableau de bord* : le compteur pointe sur le champ texte
« Nombre d'inscrits » (vide). Le remplacer par **« Nb inscrits (auto) »**, qui fonctionne.

---

## 6. La contrainte qui commande tout le reste : le quota gratuit

**Airtable plan Free = 100 exécutions d'automatisation par mois.**

C'est la vraie limite de votre centre de formation automatisé, et elle n'est pas technique mais
arithmétique. Un parcours stagiaire complet consomme aujourd'hui **5 exécutions** : pack d'accueil,
positionnement, convocation, évaluation à chaud, attestation — auxquelles s'ajoutera l'évaluation à
froid J+30, soit 6.

| Stagiaires par mois | Exécutions consommées | Verdict |
|---|---|---|
| 10 | ~60 + 5 (veille + devis) | ✅ tient |
| 15 | ~90 + 5 | ⚠️ à la limite |
| 20 et plus | ~125 | ⛔ le quota saute, et **les courriels cessent de partir sans prévenir** |

C'est pour cette raison que la veille du directeur est **hebdomadaire et non quotidienne** : en
quotidien elle aurait mangé 30 exécutions par mois, soit un tiers du quota, au détriment des courriels
destinés aux stagiaires.

Le jour où vous dépassez une douzaine de stagiaires par mois, le plan Team (25 000 exécutions) devient
la condition de fonctionnement, pas un confort. **Surveillez le compteur** : Airtable → menu du compte →
*Usage*.

> **RGPD** — Airtable Inc. est une société américaine. Les données de vos stagiaires (identité,
> coordonnées, parcours) y sont hébergées hors UE. Le transfert repose sur les clauses contractuelles
> types (décision (UE) 2021/914) et le Data Privacy Framework. Ce point est déjà déclaré dans votre
> politique de confidentialité (DOC-02) et doit figurer à votre registre des traitements (RGPD art. 30).
> Même remarque pour Gmail, utilisé comme service d'envoi par les automatisations.
>
> **AI Act** — aucun des mécanismes installés ici n'est un système d'IA : ce sont des formules et des
> déclencheurs déterministes. Le règlement (UE) 2024/1689 ne s'y applique pas. Attention en revanche si
> vous branchez un jour un tri ou un scoring automatique de candidats : l'annexe III, point 3, classe ces
> systèmes en **haut risque** dans le domaine de l'éducation et de la formation professionnelle.

---

## 7. Critique de ce que je viens de livrer

Par honnêteté, voici où ce travail est faible.

**Le verrou « session conforme » peut rendre le système muet.** J'ai choisi de bloquer les envois
plutôt que de laisser partir un courriel mensonger. Le risque symétrique est réel : une session jamais
rendue conforme n'envoie rien, en silence. C'est pourquoi A-08 existe. Mais A-08 est hebdomadaire : une
session créée le mardi pour le vendredi suivant peut passer six jours sans alerte. **Prenez l'habitude
de regarder la colonne « ⚠️ Contrôle avant ouverture » à chaque création de session.**

**Toute la chaîne repose sur des PDF qui n'existent pas encore.** Les 13 documents sont écrits, mais le
champ « Fichier mis en page » est vide partout. Tant qu'il l'est, aucune session ne sera « conforme » et
A-01 n'enverra rien. **C'est l'action numéro un.**

**Les quatre automatisations que j'ai écrites n'ont jamais tourné.** Elles sont validées
syntaxiquement par l'API — ce qui exclut les erreurs de structure — mais pas exécutées. Testez chacune
sur un enregistrement bidon avant de compter dessus, et supprimez-le ensuite.

**L'attestation part en corps de courriel, pas en PDF.** Juridiquement recevable : les quatre mentions
de l'art. L.6353-1 y sont. Mais un employeur ou un OPCO attendra souvent un document signé. Déposez
votre PDF dans « Attestation PDF » avant que l'automatisation ne parte, il sera joint.

**Les 32 indicateurs Qualiopi sont tous notés « C (non conforme) ».** C'est le réglage par défaut, jamais
repris — vous êtes certifié 25FOR02027.1. Tant que ce n'est pas corrigé, votre tableau de bord Qualiopi
raconte l'inverse de la réalité. Avec la chaîne de preuve désormais en place, la reprise se fait
indicateur par indicateur, en regardant les documents rattachés.

**Le processus externe qui écrit dans la base m'échappe complètement.** Je l'ai détecté, je ne peux pas
l'inspecter. Tant qu'il tourne, il recréera des doublons et pourra contredire ce qui vient d'être posé.

**Ce que je n'ai pas pu vérifier.** Les PDF déjà présents dans la base (CGV et règlement intérieur
d'origine) restent illisibles depuis cet environnement : la politique réseau bloque l'accès à
`v5.airtableusercontent.com`. Les documents du socle ont donc été **réécrits**, pas corrigés. Relisez-les
avant d'archiver les anciens.

**Ce qui reste en attente de votre part.** L'encart Assurance : les cinq emplacements réservés dans la
charte graphique (assureur, n° de police, garanties, montants, validité) restent vides tant que je n'ai
pas l'attestation de votre assureur. Vous m'avez dit que vous me l'envoyez — dès réception, je remplis
la charte, les mentions légales et les modèles de convention.

**FOR-0008 attend trois informations.** Vous avez choisi de la compléter plutôt que de l'archiver, mais
la fiche est vide : il me manque l'**intitulé**, le **domaine** et la **durée visée** en heures. Donnez-moi
ces trois éléments et je la monte au standard des autres, avec barème tarifaire et bloc tarifs
automatique. En attendant, elle reste visible dans le catalogue en statut « En développement ».

---

## 8. Vos cinq prochaines actions, dans l'ordre

1. **Mettre les 13 PDF en ligne** dans DOCUMENTS OFFICIELS YEBA, champ « Fichier mis en page ».
   Sans cela, rien ne part.
2. **Rattacher le pack légal** sur une session, vérifier qu'elle passe à « ✅ Session conforme »,
   puis dupliquer cette session comme modèle.
3. **Activer A-02, A-03, A-04, A-08** et **mettre à jour A-01** (§ 5.1).
4. **Créer les trois formulaires** (§ 5.2) — sans eux, la porte d'entrée reste fermée.
5. **Supprimer les six champs** du § 5.3, dont les deux champs de données de santé.

Et deux choses qui dépendent de vous : **l'attestation de votre assureur** (pour l'encart Assurance) et
**l'intitulé, le domaine et la durée de FOR-0008** (pour la monter au standard).

---

YEBA FORMATIONS — SIRET 814 622 262 00032
Déclaration d'activité n° 04973676397 auprès du préfet de La Réunion. Cet enregistrement ne vaut pas agrément de l'État.
Certification Qualiopi n° 25FOR02027.1 au titre de la catégorie « actions de formation ».
