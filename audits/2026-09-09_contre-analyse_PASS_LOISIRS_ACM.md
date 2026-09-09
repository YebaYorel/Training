# Contre-analyse critique de l'audit PASS LOISIRS 2.0 — ACM (2026-2027)

**Base auditée :** `appGyK0pp3tlRABVA` — PASS LOISIRS 2.0 — ACM (2026-2027)
**Date de lecture :** 9 septembre 2026
**Objet :** réponse à la demande de Stan — « pour chaque référence A01 à A12, confirmer, nuancer ou invalider le constat en montrant la formule, le résultat ou l'automatisation qui justifie la conclusion ».
**Mode d'intervention : LECTURE SEULE.** Aucune donnée, formule, automatisation, interface ni paramètre n'a été modifié. Aucun courrier n'a été envoyé. Aucun enregistrement de test n'a été créé. Conformément à la demande (« les corrections seront à préparer séparément de l'analyse »), ce document ne contient que des constats et des propositions.

---

## 1. Méthode et différence avec l'audit du 8 septembre

L'audit initial a travaillé par simulation : 21 scénarios rejoués dans un évaluateur local, rapprochés de 69 valeurs déjà calculées par Airtable. Cette contre-analyse a procédé autrement, ce qui explique qu'elle puisse **durcir certains constats et en nuancer d'autres** :

| Ce que j'ai fait | Ce que cela apporte |
|---|---|
| Lecture du **texte source des formules** (`get_table_schema`) et de leurs `referencedFieldIds` | Prouve ce qu'une formule **ne regarde pas**, sans avoir à le déduire |
| Lecture des **options réelles** de chaque liste de choix citée dans les formules | Vérifie qu'aucune branche n'est morte par écart de libellé — contrôle absent de l'audit initial |
| Lecture des **4 automatisations** de la base | L'audit les déclarait « non inspectées ». Elles le sont désormais |
| Lecture des **enregistrements vivants** au 9 septembre | Confirme ou infirme les montants sur l'état actuel, pas sur celui de la veille |

**Périmètre non couvert, assumé :** je n'ai pas relu les métadonnées des 5 interfaces et de leurs 17 pages. Les filtres exacts de pages, la restriction « aujourd'hui » et les droits par rôle restent donc **non re-vérifiés** (voir A12).

---

## 2. Trois faits nouveaux, transversaux, que les deux rapports ne pouvaient pas établir

### T1 — Les quatre automatisations de la base sont TOUTES désactivées

`list_automations` renvoie `deploymentStatus: "undeployed"` pour les quatre :

| Automatisation | État | Rôle prévu |
|---|---|---|
| Alerte immédiate — dérogation de départ (+ e-mail) | **undeployed** | Trace + alerte sur dérogation |
| Alerte immédiate — identité non vérifiée à un départ (+ e-mail) | **undeployed** | Filet de rattrapage du trou A01 |
| Veille quotidienne — capacité, documents, départs bloqués | **undeployed** | Veille 7h00 Indian/Reunion |
| Confirmation d'inscription aux familles (+ documents PDF) | **undeployed** | Courrier A05 |

**Ce que cela change.** Deux lectures opposées, toutes deux vraies :

- *Rassurant à court terme* : aucun courrier ne peut partir aujourd'hui (A05), et aucune alerte erronée ne circule. Le pack PDF vide est sans conséquence immédiate.
- *Préoccupant à moyen terme* : le filet de sécurité censé rattraper A01 (« identité non vérifiée ») **n'existe pas encore**. Et surtout, ces quatre automatisations s'activeront vraisemblablement **le même jour**, sans recette préalable, sur un modèle de données dont les verdicts sont encore faux. **L'activation est le moment de risque maximal**, pas l'état actuel.

**Recommandation :** activer une automatisation à la fois, après correction du verdict ou du calcul dont elle dépend, et jamais avant.

### T2 — Aucune fonction d'intelligence artificielle n'est présente dans la base

Les quatre automatisations n'emploient que des nœuds `createRecord`, `updateRecord`, `findRecords`, `sendEmail` et `repeatingGroup`. **Aucun nœud `aiGenerate`, `aiGenerateStructuredOutput` ou `aiGenerateImage`.** Les 31 champs calculés sont des formules déterministes. Ce point est déterminant pour la qualification réglementaire (section 5).

### T3 — Aucune branche morte : les libellés testés correspondent aux options réelles

J'ai comparé chaque chaîne littérale des formules aux options effectivement définies. **Toutes correspondent exactement**, y compris les différences de casse entre tables (`"Encaissé"` dans Encaissements, `"ENCAISSÉ"` dans Échéancier — ce sont bien deux listes distinctes, correctement écrites). C'est un contrôle que l'audit initial n'avait pas fait et qui aurait pu invalider plusieurs de ses constats : ils tiennent tous.

---

## 3. Tableau de contre-analyse A01 → A12

Légende des conclusions : **CONFIRMÉ** (défaut démontré sur formule ou donnée) · **CONFIRMÉ ET DURCI** (l'audit laissait un doute que je lève) · **NUANCÉ** (constat exact mais partiellement compensé ailleurs) · **PARTIEL** (non entièrement re-vérifié).

| Réf | Conclusion | Preuve (lue le 09/09/2026) | Correction minimale | Effets sur l'existant | Test de validation |
|---|---|---|---|---|---|
| **A01** | **CONFIRMÉ ET DURCI** | Formule `CONTRÔLE DÉPART` (`fldNbCfSLuSX6LvdJ`). Ses `referencedFieldIds` (9 champs) **n'incluent ni « Agent ayant remis l'enfant » (`fld7HHxlxWMKMU4lX`) ni « Horodatage départ » (`fldSjFs4g1LuEqpZS`)**. Trou 1 : branche `lien = "OUI"` → `IF({Identité vérifiée}="Non vérifiée","A VERIFIER","CONFORME")` ; les options réelles sont « Oui - pièce contrôlée », « Non requise - personne connue », « Non vérifiée » — **une cellule vide n'est aucune des trois ⇒ CONFORME**. Trou 2 : le contrôle enfant/lien est gardé par `AND(NOT({Récupéré via le lien}=BLANK()), NOT({Enfant}=BLANK()), …)` ⇒ **Enfant vide sauve la garde et retombe sur CONFORME**. Durcissement : l'alerte censée rattraper ce cas est **undeployed** (T1) | Exiger explicitement : un enfant unique, un lien unique correspondant à cet enfant, une valeur d'identité **parmi les valeurs admises** (pas « non vide »), un agent et un horodatage, avant tout verdict CONFORME. Sortir la dérogation en parcours distinct | Des départs déjà saisis peuvent changer de verdict. Aucun n'existe (table vide) : **le coût de correction est nul aujourd'hui, il ne le sera plus après la rentrée** | Identité vide ⇒ jamais CONFORME. Enfant vide ⇒ jamais CONFORME. Mauvais enfant ⇒ BLOQUE. Agent absent ⇒ jamais CONFORME. Puis vérifier que l'interface **refuse** la clôture |
| **A02** | **CONFIRMÉ, chiffres reproduits à l'identique** | `Enfants.Tarif dû` (`fldgGebw9ombhJnX6`) = rollup sur le lien Inscriptions → `Tarif final`. `Reste dû` = `ROUND({Tarif dû} − {Total affecté}, 2)`. **Valeurs vivantes : Tarif dû 3 784 · Total affecté 0 · Reste dû 3 784 · Statut « NON RÉGLÉ »**. Les 5 inscriptions lues : 1 326 (Brouillon) + 1 258 (Brouillon) + 0 (Brouillon) + 0 (Brouillon) + 1 200 (Clôturée) = **3 784**, dont **2 584 de brouillons** | Séparer trois notions : prix **simulé**, montant **engagé**, montant **exigible**. Exclure les brouillons de l'exigible. Statuer sur Validée / Clôturée / Annulée | Le « Reste dû » affiché passera de 3 784 € à 1 200 € sur la fiche témoin. Tout écran ou courrier qui affiche ce montant doit être revu **en même temps** | Créer/modifier un brouillon ⇒ l'exigible ne bouge pas. Une clôture conserve sa dette. Une annulation la retire selon la règle retenue |
| **A03** | **CONFIRMÉ** | `Dossier global` (`fldoO8I1p2tQmIGDS`). `referencedFieldIds` = Renseignements, Sanitaire, Vaccins, **Photo**, RC, Statut RC. **N'inclut PAS** « Choix photo recueilli » (`fldchdb5fDCcRmrS1`), « Photo autorisée » (`fldlRhlBdvmA2Kbge`), ni « Règlement intérieur » (`fldF5FAuO78NmcEbO`). Exige `{Photo}="Oui"` ; options réelles Oui / Non / À vérifier ⇒ **un refus photo rend le dossier INCOMPLET**. Vaccins admis à « À vérifier » (`OR(="OK", ="À vérifier")`) | Remplacer le critère « Photo = Oui » par « Choix photo **recueilli** », sans exiger l'autorisation. Intégrer le Règlement intérieur. Trancher le sort de Vaccins = « À vérifier » | Des dossiers aujourd'hui INCOMPLET deviendront COMPLET (refus photo) et inversement (RI manquant). Prévenir avant, sinon la liste du jour change sans explication | Refus photo documenté + reste conforme ⇒ COMPLET. RI manquant ⇒ jamais COMPLET |
| **A04** | **CONFIRMÉ ET AGGRAVÉ** | `Validité document` (`fld0DcCmayHNd88ZW`). `referencedFieldIds` = **uniquement** Statut du document, Motif si non fourni, Date d'expiration. **Ni Fichier, ni Date de réception, ni « Contrôlé par », ni Type de document.** Ligne vide : statut ∉ {Manquant, Refusé par la famille, Sans objet} et expiration vide ⇒ `IF({Statut}="Reçu à contrôler","A CONTROLER","VALIDE")` ⇒ **VALIDE**. Aggravation : « Refusé par la famille » + motif ⇒ « REFUS ASSUME (dossier non bloque) » **quel que soit le type parmi les 12 options réelles, y compris « Fiche sanitaire », « PAI », « Ordonnance », « Attestation responsabilité civile », « Pièce judiciaire »** | Réserver VALIDE à un état explicite de réception **et** de contrôle, avec fichier et contrôleur. Qualifier chaque type en obligatoire / facultatif et n'appliquer « refus non bloquant » qu'aux pièces facultatives | Des lignes aujourd'hui VALIDE repasseront à contrôler. Table vide à ce jour : correction sans reprise de données | Ligne vide ⇒ jamais VALIDE. Refus d'un PAI ou d'une attestation RC ⇒ bloquant. Refus photo ⇒ non bloquant |
| **A05** | **CONFIRMÉ**, et le risque est **différé** | `Confirmation d'inscription — état` (`fldMWC7LPSFunhuCF`) contient littéralement `{Total encaissé sur l'inscription} < 100` et `" / 100 EUR)"`. Aucun lookup vers Paramètres ⇒ **ACOMPTE_DEFAUT n'est structurellement pas lisible** par cette formule. S08 : 42 € payés 42 € ⇒ `AND(42>0, 42<100)` vrai ⇒ EN ATTENTE. S09 : Tarif final 0 ⇒ `AND(0>0,…)` faux ⇒ **PRETE A ENVOYER**. Les 5 inscriptions affichent « EN ATTENTE - inscription non validee » | Porter l'acompte via un lookup ou une valeur unique de référence. Traiter le cas « total < acompte ». Distinguer **gratuité validée** et **prix non établi** (un `Tarif final = 0` sans motif ne doit pas ouvrir l'envoi) | L'automatisation étant **undeployed**, corriger maintenant est sans effet de bord. Sa garde anti-doublon (« Confirmation envoyée le » posée **avant** l'envoi) est bien conçue : la conserver | Petit engagement soldé ⇒ traité selon la règle. Prix absent ⇒ envoi refusé. Relance de l'action ⇒ pas de second courrier |
| **A06** | **CONFIRMÉ** | `Nb mercredis retenu` = `IF({Nb sessions reliées} > 0, {Nb sessions reliées}, {Nb mercredis engagés})`. `Nb sessions reliées` est un `count` **sans condition**. Données vivantes : les 5 inscriptions ont 0 session reliée et 34 mercredis manuels ⇒ 34 retenus. **Une seule session reliée ⇒ 1 ⇒ Tarif normal 39 €** au lieu de 1 326 € | Ne jamais dériver le tarif d'un planning en cours de construction : introduire un état « planning en préparation » et ne basculer sur le comptage réel qu'une fois le planning déclaré complet | Tant qu'aucune session n'est reliée, rien ne change (34 partout). Le risque naît **au premier rattachement de session** | Année / période / alternance / inscription tardive ⇒ bonnes dates et bon tarif. Rattachement partiel ⇒ le tarif ne s'effondre pas |
| **A07** | **CONFIRMÉ** | `Sessions.Nb inscriptions reliées` (`fldaThbG8zRTlIqKN`) est un `count` dont la configuration ne contient **que** `recordLinkFieldId` — **aucune condition**. `Contrôle capacité` compare ce compteur brut à `Capacité`. Il ne compte donc ni enfants distincts, ni créneaux, et **brouillons, annulations et doublons pèsent autant qu'une inscription valide** | Définir si la capacité porte sur les enfants accueillis dans la journée ou sur l'occupation par créneau, puis ne compter que les statuts qui réservent réellement une place | Le compteur affiché baissera (les 5 brouillons cessent de consommer des places). Les tableaux de bord de capacité changeront de valeur | Un doublon ne consomme pas 2 places. Une annulation libère. Deux validations simultanées sur la dernière place ⇒ décision explicite |
| **A08** | **CONFIRMÉ sur les 3 cas, mais NUANCÉ** | `Anomalie encaissement` : le statut **« Remboursé » n'est couvert par aucune des 4 branches** (la 4ᵉ ne liste que « Reçu », « Prévu », « Rejeté ») ⇒ remboursement 100 € affecté −150 € : **aucune anomalie**. `Anomalie échéance` : la branche ne se déclenche qu'à `ROUND({Total affecté},2) = 0` ⇒ échéance 132,60 € ENCAISSÉ avec 1 € affecté : **aucune anomalie**. `Statut paiement` : `IF({Tarif dû}=0,"À PARAMÉTRER")` ⇒ gratuité indiscernable. **Nuance en faveur de la base :** le cas « rejet après affectation » **est** couvert par `AND(OR(Statut="Reçu","Prévu","Rejeté"), {Total affecté} != 0)` ⇒ « AFFECTE MAIS NON ENCAISSE ». **Asymétrie précise :** l'Échéancier n'a pas l'équivalent du « RESTE A AFFECTER » qui existe pourtant sur les Encaissements | (1) Étendre la 4ᵉ branche à « Remboursé » et contrôler les écarts **dans les deux sens** (valeurs absolues). (2) Ajouter sur l'Échéancier le contrôle de paiement partiel, symétrique de celui des Encaissements. (3) Distinguer gratuité validée et prix manquant | Purement additif : de nouvelles anomalies apparaîtront sur des lignes aujourd'hui silencieuses. Aucune ligne existante (tables vides) | Règlement de fratrie compté une fois. Remboursement partiel puis total ⇒ soldes cohérents. ENCAISSÉ ne masque pas un paiement partiel |
| **A09** | **CONFIRMÉ ET DURCI — le doute est levé** | La table Enfants ne porte que **3 rollups** : Total encaissé, Tarif dû, Total affecté (solde réel). **Aucun ne porte sur le lien « Pénalités & avoirs » (`fldEDh7iSN2PwlYBG`).** `Reste dû` ne référence que Tarif dû et Total affecté. **Durcissement décisif :** l'audit laissait ouverte l'hypothèse d'« une automatisation non visible ». J'ai lu les 4 automatisations : **aucune ne touche Pénalités & avoirs**. Le constat passe donc de « à vérifier » à **« établi : il n'existe aucun circuit, ni formule ni automatisation »** | Choisir **un seul** circuit d'impact (soit un rollup conditionné au statut « validé », soit une écriture en Affectations), le documenter, et interdire l'autre | Aucun : la fonction n'est aujourd'hui raccordée à rien. C'est une construction, pas une reprise | Pénalité approuvée ⇒ le dû augmente **une seule fois**. Avoir approuvé ⇒ diminue une seule fois. Ligne brouillon ⇒ aucun effet |
| **A10** | **CONFIRMÉ ET ÉTENDU** | Les 4 barèmes lus : JC_AN 39/37 « À l'année » · JC_PER 42/40 « Période » · DJR 32/30 « Toutes » · DJS 28/26 « Toutes ». Tous « Validé ». **Version barème, Valable du et Valable jusqu'au sont vides sur les quatre.** Vérifié : 39 × 34 = 1 326 et 37 × 34 = 1 258. **Extension importante :** « Tarif applicable » est un lien **manuel** (`multipleRecordLinks`), et « Tarif unité 1 enfant / fratrie » sont des rollups sur ce lien. **Il n'existe donc aucun mécanisme de correspondance** entre Formule/Créneau/Repas et le barème : le rapprochement est **entièrement humain**. Le problème dépasse l'écart de libellés signalé par l'audit | Renseigner version et date de début sur les 4 barèmes. Définir la règle de choix du barème (ponctuel, alternance, vacances) et, à terme, l'automatiser au lieu de la laisser au lien manuel | Renseigner « Valable du » n'affecte aucun calcul (aucune formule ne lit ces champs) : correction **sans risque**. En revanche, automatiser le choix du barème modifiera des tarifs — protéger d'abord les prix contractuels figés | Chaque combinaison commercialisée trouve **un** barème. Un changement de version ne modifie pas un prix figé (vérifié : TEST-T18 reste à 1 200 € via `Date validation prix`) |
| **A11** | **CONFIRMÉ ET AGGRAVÉ par les données** | `Clé anti-doublon` = `ARRAYJOIN({Enfant},"+") & " | " & {Saison} & " | " & {Type programme} & " | " & {Période} & " | " & {Créneau}`. Ni date, ni session. **Aggravation :** les **5 inscriptions actuelles portent déjà exactement la même clé** — `TEST FICTIF - Recette T14 \| 2026-2027 \| MERCREDI \|  \| JOURNÉE` (Période vide n'apporte rien). La clé ne discrimine donc **rien** dans le jeu présent. Rappel technique : un champ `formula` **n'impose aucune unicité** dans Airtable — il ne peut pas rejeter une création | Définir le doublon **par type d'inscription** et intégrer une empreinte des dates ou sessions. Surtout : porter le rejet dans le **processus** de création, pas dans un champ calculé | Recalcul d'un champ d'affichage : aucun effet sur les montants | Deux journées ponctuelles distinctes ⇒ admises. Seconde création du même engagement ⇒ détectée. Homonyme légitime ⇒ non bloqué |
| **A12** | **PARTIEL — confirmé sur le schéma, non re-vérifié sur les pages** | **Confirmé :** Inscriptions porte **trois** champs manuels indépendants — Formule (`fldd40hVmnTi6TKmV`), Créneau (`fldkNYDEB4MzjaZ52`), Repas (`fld1R7k1P0ZcJ53dX`) — sans lien entre eux, tandis que Tarifs n'est indexé que sur Formule. **La désynchronisation est structurelle, pas seulement affaire d'interface.** **Confirmé :** `result.options.precision = 0` sur Tarif unitaire retenu, Tarif normal, Tarif final, Tarif dû, Reste dû, Total affecté, Total encaissé, Montant effectif, Total affecté à l'échéance. Les calculs conservent bien les centimes (`ROUND(x, 2)`) : **c'est un défaut d'affichage, pas de calcul** — 1 193,40 € s'afficherait « 1 193 ». **Non re-vérifié :** filtres de pages, restriction « aujourd'hui », droits par rôle | Passer à 2 décimales les champs monétaires destinés aux familles et à la comptabilité. Faire du couple Créneau+Repas la **source unique** et en dériver Formule (ou l'inverse), jamais les deux en saisie libre | Le passage à 2 décimales est cosmétique et sans risque. La refonte Formule/Créneau/Repas touche les tarifs **et** les courriers : à faire en une fois | Un montant à centimes s'affiche juste partout. Comptes de test animateur / administratif / comptable ⇒ vérifier ce que chaque rôle voit et peut modifier |

---

## 4. Les trois catégories demandées par Stan

> « Il faut distinguer les défauts démontrés, les règles métier à décider et les fonctions simplement non testées. »

### 4.1 Défauts démontrés — formule ou donnée à l'appui (9)

A01 (deux trous + absence de contrôle agent/horodatage), A02 (3 784 € reproduits), A03 (Photo/RI/Vaccins), A04 (ligne vide VALIDE + refus généralisé aux pièces critiques), A05 (seuil 100 € en dur), A06 (bascule 34 → 1), A07 (compteur sans condition), A08 (3 angles morts, dont « Remboursé » non couvert), A09 (aucun circuit — **établi, plus seulement supposé**), A10 (identité des barèmes + absence de correspondance), A11 (clé non discriminante, prouvée sur 5 lignes identiques).

### 4.2 Règles métier à décider — je ne peux pas trancher à votre place

| Sujet | Ce que dit la base aujourd'hui | Décision attendue |
|---|---|---|
| Acompte | 100 € **écrit en dur** dans la formule ; le paramètre ACOMPTE_DEFAUT existe mais n'est pas lu | Montant, application par programme, et sort d'un total inférieur à l'acompte |
| Prix exigible | Brouillons inclus (3 784 € constatés) | Sort financier de Validée / Clôturée / Annulée |
| Capacité | Compteur brut de lignes liées vs 40 | Enfants dans la journée **ou** occupation par créneau ; statuts qui réservent |
| Alternance | Champ « Ancrage alternance » présent, aucune règle démontrée | Premier ou second mercredi ; continuité ou réinitialisation entre périodes |
| Fratrie | Drapeau manuel Oui/Non | Rang, période de référence, dérogations |
| Dossier complet | Anciens indicateurs (Photo = Oui) | Liste des pièces réellement requises et traitement des « À vérifier » |
| Barèmes | 4 barèmes, ponctuel/alternance/vacances non couverts | Règle de choix, et automatisation ou non du lien « Tarif applicable » |
| Fermeture | HEURE_FERMETURE présent dans les 36 paramètres | Heure de référence pour les retards et pénalités |

### 4.3 Fonctions non testées — ni par l'audit, ni par moi

Le déclenchement réel des automatisations (elles sont désactivées, donc **non testables en l'état**) · les filtres exacts des 17 pages · les permissions par rôle · les validations concurrentes sur la dernière place · les exports et la restauration · la génération effective du planning et de l'alternance (aucune inscription validée, aucune présence).

**Un point de méthode important :** l'absence de présences ne prouve rien. Aucune inscription n'est « Validée », donc rien ne devait en produire. Ne concluez pas à une panne.

---

## 5. Réflexe RGPD et IA Act — signalé spontanément

### 5.1 RGPD — c'est ici que se situe le risque le plus lourd, et l'audit ne le traite pas

L'audit initial l'écrit lui-même : « L'audit ne formule pas d'avis de conformité juridique. » Or cette base traite des **données d'enfants mineurs**, incluant :

- une table **Santé** (17 champs) et un lookup `⚠️ Alerte santé (DÉTAIL MÉDICAL)` remonté **jusque sur la fiche Enfants** → **données de santé, article 9 RGPD** (catégorie particulière) ;
- des champs **Restriction judiciaire**, **Détail restriction**, et un type de document « Pièce judiciaire » → **article 10 RGPD** (données relatives aux décisions de justice), dont le traitement est strictement encadré.

**Points à traiter, par ordre de gravité :**

1. **Souveraineté et transfert hors UE — point bloquant à instruire.** Airtable est édité par une société établie aux États-Unis. Héberger des données de santé et des données judiciaires **concernant des mineurs** sur un service non européen suppose au minimum : un acte d'exécution d'adéquation ou des garanties appropriées, un contrat de sous-traitance conforme à l'**article 28**, et une analyse du transfert (**chapitre V**). La base contient d'ailleurs déjà les paramètres `HEBERGEMENT_REGION`, `MECANISME_TRANSFERT`, `DPA_CONCLU` et `HDS_QUALIFICATION` — quelqu'un a **identifié le sujet sans le clore**. *Je n'ai pas lu la valeur de ces paramètres : à vérifier avant toute mise en production.*
   **Cela contredit frontalement votre propre règle de souveraineté européenne** et le choix de Baserow (cloud UE) posé dans ce dépôt. Si le client maintient Airtable, il faut une décision écrite et motivée ; si c'est négociable, une base UE est le choix cohérent.

2. **AIPD très probablement obligatoire (article 35).** Croisement de données sensibles, de données judiciaires et de **personnes vulnérables (mineurs)**. Le paramètre `AIPD_STATUT` existe : sa valeur doit être « réalisée », pas « à faire », avant la rentrée.

3. **Minimisation (article 5.1.c) — un défaut de conception concret.** Le lookup `⚠️ Alerte santé (DÉTAIL MÉDICAL)` diffuse le **détail médical** sur la fiche Enfants, largement consultée. La base propose pourtant déjà la bonne pratique : `Consigne du jour (sans détail médical)`. **Recommandation : ne jamais exposer le champ DÉTAIL MÉDICAL dans les interfaces animateurs ; n'y laisser que la consigne du jour.**

4. **Minimisation, second cas.** La `Clé anti-doublon` recopie le **nom complet de l'enfant en clair** dans un champ technique, visible dans les vues et emporté dans tout export. Préférer l'identifiant d'enregistrement.

5. **Point positif à souligner.** Les descriptions des automatisations montrent une vraie culture RGPD : e-mails limités à des compteurs et des liens, aucun nom d'enfant, envoi **séparé** à chaque titulaire de l'autorité parentale pour ne pas révéler l'adresse de l'un à l'autre en cas de séparation, exclusion des personnes sous restriction judiciaire. C'est du bon travail : à conserver tel quel.

6. **Réserve.** Le destinataire des alertes est une adresse Gmail. Même sans donnée personnelle dans le corps du message, une messagerie grand public comme canal d'alerte opérationnelle d'un ACM est un point de gouvernance à arbitrer.

7. **Article 22 — décision automatisée.** Si la gestion de capacité venait à trancher automatiquement l'attribution d'une place (A07), on entrerait dans le champ des décisions automatisées : intervention humaine et information des familles deviendraient nécessaires. **Aujourd'hui ce n'est pas le cas** — la formule affiche un dépassement, elle ne décide pas.

### 5.2 IA Act — analyse et conclusion

**Le règlement (UE) 2024/1689 (IA Act) ne s'applique pas en l'état à cette base.** Justification : un système d'IA suppose une capacité d'inférence. Or (T2) la base ne contient **aucune fonction générative ni prédictive** — 31 formules déterministes et 4 automatisations à nœuds classiques. Des règles de calcul explicites ne sont pas un système d'IA.

**Ce qui ferait basculer la qualification**, et qu'il faut surveiller : l'ajout d'un tri ou d'un score automatisé de dossiers, d'une priorisation d'admission, ou d'un nœud `aiGenerate` (disponible dans Airtable). Le paramètre `IA_FONCTIONS_ACTIVEES` présent dans la base suggère que la question est déjà posée en interne. **Tant qu'il reste à « aucune », vous êtes hors champ IA Act — c'est un argument à faire valoir, et une raison de ne pas ajouter d'IA sans nécessité.**

---

## 6. Critique de ma propre analyse — failles et limites

Exercice imposé, et utile ici :

- **Logique.** Mes conclusions A01, A04, A05 reposent sur la lecture du texte des formules, pas sur une exécution dans Airtable. Le risque résiduel est faible (j'ai vérifié que les libellés testés existent réellement), mais **une exécution réelle reste supérieure à toute lecture**. Les recettes du tableau ne sont pas facultatives.
- **Périmètre.** Je n'ai pas relu les 17 pages d'interface. A12 est donc **partiel** et je l'affiche comme tel plutôt que de le confirmer par confort.
- **Agrégations.** Le connecteur n'expose ni la fonction d'agrégation des rollups ni leurs conditions. Pour A02, je m'appuie sur le **résultat** (3 784 €), qui est une preuve suffisante ; pour d'autres rollups, je ne peux pas certifier l'absence de condition. **Je l'ai dit là où c'était le cas plutôt que de généraliser.**
- **Temporalité.** La base a été modifiée entre l'audit (8/09) et ma lecture (9/09) — certains champs datent du 8 à 14h19. Mes constats valent pour l'état du **9 septembre 2026** et devront être revérifiés si le développement se poursuit.
- **Faisabilité et économie.** Je recommande d'activer les automatisations une par une. Leurs descriptions signalent une contrainte de **quota mensuel sur plan gratuit** — d'où leur fusion en une veille unique. Une recette poussée consommera ce quota. **À budgéter : un plan payant sera probablement nécessaire avant la rentrée**, ce n'est pas un détail technique mais une ligne de coût.
- **Juridique.** Je ne suis pas votre conseil juridique et ce document n'est pas un avis de conformité. La section 5 identifie des points à instruire ; la qualification définitive (notamment HDS et transfert hors UE) demande une analyse dédiée avec le responsable de traitement.
- **Angle mort assumé.** Je n'ai pas examiné les tables Sorties, Incidents, Économat, Préinscriptions, Registre des traitements, Accès/jetons, ni Incidents de sécurité. Elles sortent du périmètre A01–A12 mais **le Registre des traitements et les Accès/jetons mériteraient une revue propre**, surtout au vu de la section 5.

---

## 7. Ce dont j'ai besoin de vous avant d'aller plus loin

Je ne peux pas inventer ces réponses, et elles conditionnent les corrections :

1. **Voulez-vous que je prépare les corrections ?** Les deux rapports demandent explicitement de les traiter **séparément de l'analyse** — je m'y suis tenu. Dites-moi si je passe à la phase suivante.
2. **Qui est responsable de traitement** — l'ACM lui-même, une collectivité ? Cela détermine qui doit porter l'AIPD et le registre.
3. **Airtable est-il imposé par le client, ou négociable ?** C'est la question la plus lourde de la section 5, et elle conditionne tout le reste.
4. **Les huit règles métier du § 4.2** — je peux vous proposer une option par défaut argumentée pour chacune si vous préférez arbitrer sur pièces.
5. **Quelle est votre position contractuelle sur ce dossier ?** Vous m'avez indiqué que YEBA FORMATIONS ne doit pas apparaître lorsque vous intervenez pour un autre organisme : **je n'ai mentionné aucune enseigne dans ce document.** Confirmez-moi le cas échéant s'il doit être signé.

---

## 8. Traçabilité des sources

**Source primaire — lecture directe de la base, 9 septembre 2026 :**
- Schéma des 29 tables et 415 champs (`list_tables_for_base`)
- Texte source et `referencedFieldIds` des formules citées, configuration des rollups et compteurs (`get_table_schema`)
- Options réelles des listes de choix de Encaissements, Échéancier, Mouvements de départ, Dossiers, Documents (`get_table_schema`)
- **Les 4 automatisations, leur statut de déploiement et leurs nœuds** (`list_automations`) — élément non couvert par l'audit initial
- Enregistrements de Enfants (1), Inscriptions (5), Tarifs (4), Paramètres (36) (`list_records_for_table`)

**Sources documentaires fournies :**
- *Audit fonctionnel — PASS LOISIRS 2.0 — ACM*, 8 septembre 2026 (Stan)
- *Synthèse pour Aurélien — Audit ACM*, 8 septembre 2026 (Stan)

**Références réglementaires citées :** Règlement (UE) 2016/679 (RGPD), articles 5.1.c, 9, 10, 22, 28, 35 et chapitre V ; Règlement (UE) 2024/1689 (IA Act), définition du système d'IA.
*Ces références sont citées de mémoire professionnelle et n'ont pas été re-consultées en ligne au cours de cette analyse : à confirmer sur les textes officiels (EUR-Lex, CNIL) avant tout usage opposable devant un client.*

**Références techniques Airtable** (agrégations conditionnées, valeurs vides, fonctions de formule, lookups) : citées par l'audit initial, **non re-consultées ici**. Mes conclusions ne reposent pas sur elles mais sur la lecture directe des configurations et des résultats.

---

**Livrable : contre-analyse et propositions. Aucune correction appliquée, aucune donnée modifiée, aucun courrier envoyé, aucun scénario injecté dans Airtable.**
