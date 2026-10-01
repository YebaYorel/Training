# Anim'Loisirs 974 / PASS LOISIRS 2.0 : dossier de finalisation avant Baserow

État constaté le **01/10/2026** sur la base Airtable `appGyK0pp3tlRABVA`
(« PASS LOISIRS 2.0 — ACM (2026-2027) ») et sur ce dépôt.
Destinataires : Aurélien LUMEKA, Stan Vellard.

> Légende réglementaire, appliquée à chaque point : **[RGPD]** ou **[IA Act]**.
> Aucun secret (mot de passe, jeton, code d'accès) ne figure dans ce document.

---

## 0. Synthèse : ce qui est fait, ce qui reste à faire de votre côté

| # | Sujet | État au 01/10/2026 | Qui agit |
|---|---|---|---|
| 1 | MFA Airtable des comptes ayant accès à la base | **Non prouvée** (Paramètres `MFA_OBLIGATOIRE` = « À RENSEIGNER ») | Stan + Aurélien, chacun sur son compte |
| 2 | MFA Airtable liée à animloisirs974@gmail.com | **Non prouvée.** Voir §1 : selon le mode de connexion, c'est la MFA **Google** qui s'applique | Titulaire de la boîte |
| 3 | MFA des boîtes animloisirs974@ et acm.passloisirs2.0@gmail.com | **Non vérifiable à distance** : aucun outil ne donne accès aux réglages de sécurité d'un compte Google tiers | Titulaire de chaque boîte |
| 4 | Accès Baserow + API/MCP + dépôt | Code prêt (client, serveur MCP, outil de migration). **Connexion inactive** : identifiants absents et réseau bloqué dans l'environnement cloud | Aurélien (paramétrage) |
| 5 | Région d'hébergement Airtable | **Déterminée par déduction documentée**, à confirmer par écrit (§4) | Aurélien (courriel au support) |
| 6 | Règles et textes des relances | **Analysés : 9 corrections proposées**, dont 3 bloquantes (§5) | Validation Stan + Aurélien |
| 7 | Extraction Airtable → Baserow sécurisée | **Outil livré et testé hors ligne** (`migration/`), plan réel généré sur votre base | Lancement après les points 1 à 4 |

**Pourquoi je ne peux pas « confirmer » une MFA moi-même** : la MFA protège justement
contre un tiers qui agirait à la place du titulaire. Aucune API Airtable ou Google ne
permet à un outil externe de lire ou d'activer la MFA d'un compte personnel. La preuve
doit venir du titulaire (capture d'écran datée, §1.3).

---

## 1. MFA / 2FA Airtable (points 1 et 2)  **[RGPD art. 32 : sécurité]**

### 1.1 Point préalable décisif : comment vous connectez-vous à Airtable ?

D'après la documentation Airtable (extrait de résultat de recherche, page non consultée
en direct) : *la 2FA Airtable ne peut être configurée que si le compte a été créé avec
un mot de passe choisi. Un compte qui se connecte avec Google ne peut pas utiliser cette
procédure.*

| Mode de connexion du compte | Où se règle la MFA |
|---|---|
| E-mail + mot de passe Airtable | Dans Airtable (§1.2) |
| Bouton « Continue with Google » | **Dans le compte Google** (§2) : la MFA Google protège alors l'accès Airtable |

➡️ **Question à trancher** : animloisirs974@gmail.com est-elle un **compte Airtable**
(et lequel : Stan ?), ou seulement la boîte des alertes ? Le registre du 01/10/2026 ne
recense que **deux collaborateurs** de la base : Stan Vellard (Créateur) et Aurélien
LUMEKA (Propriétaire de l'espace).

### 1.2 Procédure Airtable (compte avec mot de passe)

1. Ouvrir `https://airtable.com/account` (ou avatar en haut à droite → **Account**).
2. Cliquer sur **Set up two-factor authentication** → se ré-identifier → **Enable**.
3. Scanner le QR code avec une application d'authentification (TOTP).
   - Recommandé (souveraineté, open source) : **Aegis** (Android) ou **Ente Auth**
     (Android/iOS, chiffré de bout en bout). Éviter le SMS, exposé au détournement de
     carte SIM.
4. Saisir le code à 6 chiffres. **Conserver les codes de secours** dans un gestionnaire
   de mots de passe : **KeePassXC** (local, open source) ou **Proton Pass** (Suisse,
   pays bénéficiant d'une décision d'adéquation de la Commission européenne).

Limite du forfait **Free** : un propriétaire d'espace ne peut pas **imposer** la 2FA à
ses collaborateurs. Cette exigence est réservée à l'offre Enterprise (option « On for
members only / all users », extrait de résultat de recherche). Chacun doit donc
l'activer lui-même et en apporter la preuve.

### 1.3 Preuve à conserver (une ligne par compte)

- Capture de la page Account montrant la 2FA activée, **date visible**, sans QR code ni
  code de secours.
- À consigner dans la table **« Accès, jetons et partages »** : Type = MFA, Détenteur,
  État = Vérifiée, date.
- Quand **tous** les comptes sont prouvés : `MFA_OBLIGATOIRE` → Statut « Validé ».

---

## 2. MFA des boîtes Gmail (point 3)  **[RGPD art. 32]**

Ces deux boîtes sont des **points d'entrée critiques** : réinitialisation des mots de
passe, réception des alertes (EMAIL_ALERTES) et adresse affichée aux familles
(EMAIL_EXPEDITEUR).

**Procédure, pour chaque boîte** (animloisirs974@gmail.com et acm.passloisirs2.0@gmail.com) :

1. `https://myaccount.google.com/security` → **Validation en deux étapes** → Activer.
2. Méthode principale : **clé d'accès (passkey)** ou application TOTP. Éviter le SMS
   comme méthode unique.
3. **Options de récupération** : téléphone et e-mail de secours appartenant à la
   structure, pas à un ancien bénévole. Générer les **codes de secours** et les ranger
   dans le gestionnaire de mots de passe.
4. Contrôler **« Vos appareils »** et **« Applications tierces ayant accès au compte »** :
   retirer tout ce qui n'est pas identifié.
5. Compte **non partagé** : une personne titulaire nommée par boîte (exigence déjà
   inscrite dans `EMAIL_ALERTES`).
6. Preuve : capture « Validation en deux étapes : activée depuis le … », consignée
   comme en §1.3.

⚠️ **Constat de souveraineté [RGPD art. 28 et 44]** : une boîte **Gmail gratuite**
relève des conditions grand public de Google (société américaine). Je n'ai trouvé
aucune trace d'un contrat de sous-traitance (art. 28) signé pour ces boîtes, et une
boîte gratuite n'en prévoit pas, à ma connaissance. C'est acceptable en phase FICTIF
(aucune donnée réelle), mais **pas pour l'exploitation réelle**. Cible pour la mise en
production : une messagerie sur **nom de domaine propre** chez un hébergeur
européen. Pistes, à comparer sur pièces (DPA, localisation) : OVHcloud (France),
Infomaniak (Suisse), mailbox.org (Allemagne).

---

## 3. Accès complet Baserow + API/MCP + dépôt (point 4)

### 3.1 Ce qui est prêt dans le dépôt

| Élément | Fichier | Rôle |
|---|---|---|
| Client Baserow | `baserow/client.py` | JWT pour la structure, jeton pour les données ; reprise automatique sur limitation de débit ; mises à jour en lot ; import de fichiers par URL |
| Serveur MCP | `baserow_mcp_server.py` + `.mcp.json` | Outils Baserow natifs dans Claude Code |
| Outil de migration | `migration/` | Extraction Airtable → Baserow sécurisée (§6) |
| Tests | `tests/test_migration.py` | 9 tests hors ligne, tous au vert |

### 3.2 Ce que j'ai constaté le 01/10/2026

- `baserow_health_check` → `token: absent`, `jwt: absent` : **aucun identifiant n'est
  configuré** dans l'environnement où je travaille.
- Le réseau de l'environnement cloud **refuse** `api.baserow.io` et `api.airtable.com`.

### 3.3 Actions (Aurélien), dans cet ordre

1. **Baserow** : créer un **compte de service dédié** (ex. `service-claude@<domaine>`),
   rôle **Builder** dans le workspace Anim'Loisirs. Ce compte sert uniquement à Claude
   et à la migration ; il est révocable sans toucher à vos comptes personnels.
2. **Baserow → Paramètres → Jetons de base de données** : jeton limité au workspace
   Anim'Loisirs.
3. **Airtable → `https://airtable.com/create/tokens`** : jeton personnel **en lecture
   seule**, avec les seuls scopes `data.records:read` et `schema.bases:read`, et l'accès
   limité à **la seule base** `appGyK0pp3tlRABVA`. **À révoquer le jour où la migration
   est validée.**
4. **Environnement cloud Claude Code** (menu de l'environnement dans la barre de titre
   de la session → **Edit**) :
   - *Network access* : ajouter `api.baserow.io` et `api.airtable.com` ;
   - variables d'environnement : `BASEROW_EMAIL`, `BASEROW_PASSWORD`, `BASEROW_TOKEN`,
     `BASEROW_WORKSPACE_ID`, `AIRTABLE_PAT`, `AIRTABLE_BASE_ID=appGyK0pp3tlRABVA`.
   - Une **nouvelle session** prend ces valeurs en compte.
   - **Ne jamais coller ces secrets dans une conversation.**
5. **En local (PC de Stan ou d'Aurélien)** : `cp .env.example .env`, remplir, puis
   `python -m baserow.cli check`. Le résultat attendu est « ✅ TOUT est connecté ».
6. **Dépôt GitHub `yebayorel/training`** : ajouter Stan comme collaborateur
   (GitHub → Settings → Collaborators). Je ne peux pas le faire à votre place.
7. Inscrire chaque jeton dans **« Accès, jetons et partages »** (détenteur, périmètre,
   rotation prévue : `ROTATION_JETONS_MOIS` = 3).

---

## 4. Région d'hébergement Airtable (point 5)  **[RGPD art. 44 à 49 : transferts]**

### 4.1 Ce que disent les sources (extraits de résultats de recherche)

- Airtable propose une résidence des données aux **États-Unis (par défaut)**, en Europe
  et en Australie, **réservée aux clients Enterprise Scale**.
- Même avec la résidence UE (Francfort, sauvegardes en Irlande), les **données
  utilisateur, d'authentification, les métadonnées et les données de support restent
  aux États-Unis**.

### 4.2 Conclusion pour votre base

Votre espace est au forfait **Free** (paramètre `FORFAIT_AIRTABLE`). La résidence UE
n'y est pas proposée. **Hypothèse de travail retenue : hébergement aux États-Unis,
donc transfert hors UE.** Cette déduction est solide, mais ce n'est pas une
attestation : c'est pourquoi `HEBERGEMENT_REGION` reste « Non attestée » tant
qu'Airtable ne l'a pas confirmé par écrit.

**Conséquence pratique** : cela **conforte** votre décision. Airtable ne doit recevoir
**aucune donnée réelle** (enfants, santé, restrictions judiciaires). Il reste la
**référence fonctionnelle FICTIVE**, et les données réelles naissent directement dans
Baserow (Baserow B.V., Pays-Bas, hébergement UE, à attester de la même manière avec un
DPA signé).

### 4.3 Courriel prêt à envoyer au support Airtable (copie à archiver)

> Objet : Data residency and transfer mechanism, base appGyK0pp3tlRABVA
>
> Hello,
> For our GDPR records, could you please confirm in writing:
> 1. the region where the content (records, attachments, history) of base
>    `appGyK0pp3tlRABVA` is stored, on our current Free plan;
> 2. the legal transfer mechanism used for EU personal data (EU-US Data Privacy
>    Framework certification of the contracting entity, and/or Standard Contractual
>    Clauses);
> 3. how a Free-plan workspace can accept your Data Processing Addendum (art. 28 GDPR),
>    and the current list of sub-processors.
> Thank you,
> [Nom], PASS LOISIRS 2.0

Réponse à reporter dans `HEBERGEMENT_REGION`, `MECANISME_TRANSFERT` et `DPA_CONCLU`.
Vérification complémentaire possible : rechercher « Airtable » sur
`dataprivacyframework.gov` (inscription active et périmètre couvert).

---

## 5. Validation des règles et textes des relances (point 6)  **[RGPD]**

### 5.1 Règles analysées (formule « Relance », table Factures)

| Règle | Valeur actuelle | Avis |
|---|---|---|
| Préconditions | facture envoyée, non annulée, reste dû > 0 | ✅ Correct |
| Niveau 1 | ≥ 7 jours de retard, aucune relance antérieure | ✅ |
| Niveau 2 | ≥ 21 jours de retard, après niveau 1 | ✅ |
| Niveau 3 | ≥ 45 jours de retard, après niveau 2 | ✅ |
| Délai entre deux relances | ≥ 10 jours | ✅ |
| Après niveau 3 | arrêt, traitement humain | ✅ Bonne pratique |
| Anti-doublon | niveau et date posés **avant** l'envoi | ✅ |
| Destinataires | personne active, e-mail présent, **aucune restriction judiciaire** (formule de la table Personnes) | ✅ Filtre vérifié |
| Un e-mail par destinataire | groupe répété, aucun CC/BCC | ✅ |

### 5.2 Défauts relevés

| # | Défaut | Gravité | Correction proposée |
|---|---|---|---|
| R1 | Expéditeur « votre organisme ACM » et signature « L'équipe votre organisme ACM » | **Bloquant** | Nom légal du responsable de traitement (question Q1) |
| R2 | « Répondez à ce message » : l'action *Send email* d'Airtable envoie depuis la messagerie d'Airtable, pas depuis acm.passloisirs2.0@gmail.com. **Je n'ai pas pu vérifier** où arrivent les réponses | **Bloquant** | Écrire en clair l'adresse et le téléphone de contact dans le corps ; vérifier au test d'envoi |
| R3 | Niveau 3 : « avant transmission du dossier » et « l'accueil pourra être suspendu » | **Bloquant** juridiquement | N'annoncer **que** des suites réellement prévues par le **règlement de fonctionnement** signé par les familles (Q3). Une menace vague ou non appliquée peut être contestée |
| R4 | Nom de l'enfant dans l'**objet** du courriel (`Jeunes (courrier)`) | Moyenne **[RGPD art. 5.1.c, minimisation]** | Objet sans nom : l'objet s'affiche sur les écrans verrouillés et les notifications |
| R5 | Objet identique aux 3 niveaux (« Rappel ») | Faible | Rappel / 2e rappel / Dernier rappel |
| R6 | Aucun moyen de paiement indiqué | Moyenne | Ajouter les modes de règlement (Q2) |
| R7 | `Montants (courrier)` sans accents : « RESTE A REGLER », « TROP-PERCU », « a vous rembourser » | Faible (image) | Corriger (texte en §5.4) |
| R8 | Champ « Nb relances envoyées » jamais incrémenté par l'automatisation | Faible | Le supprimer ou l'alimenter dans l'action de mise à jour |
| R9 | Déclencheur « record matches conditions » sur une formule qui dépend de `TODAY()`. Je ne peux pas garantir que ce déclencheur réagit au simple passage du temps. `TODAY()` est en outre calculé en heure UTC, soit un décalage possible d'un jour entre 0 h et 4 h à La Réunion | **À tester** | Test dédié (§5.5). Repli si le test échoue : automatisation planifiée (cron) quotidienne à 8 h, heure de La Réunion, qui cherche les factures « RELANCE A ENVOYER » |

### 5.3 Textes corrigés proposés (à valider)

Variables entre crochets = paramètres à créer ou à confirmer (Q1 à Q4).

**Objets**
- N1 : `Rappel — facture [N° facture]`
- N2 : `Deuxième rappel — facture [N° facture]`
- N3 : `Dernier rappel — facture [N° facture]`

**Corps commun**
> Bonjour [Prénom] [Nom],
>
> [paragraphe du niveau]
>
> **Facture** : [N°] — **Jeune(s)** : [Jeunes] — **Échéance** : [Échéance]
> **Montants** : [Montants]
> **Détail** : [Détail]
>
> **Pour régler** : [MODES_REGLEMENT]
> **Une question, un désaccord, une difficulté ?** Écrivez à [EMAIL_CONTACT] ou
> appelez le [TEL_ADMINISTRATIF] ([HORAIRES_SECRETARIAT]). Si vous avez déjà réglé,
> merci de ne pas tenir compte de ce message.
>
> Ce message vous est adressé personnellement.
>
> Bien cordialement,
> [NOM_STRUCTURE]

**Niveau 1 (rappel bienveillant)**
> Sauf erreur de notre part, cette facture est arrivée à échéance et nous n'avons pas
> encore reçu votre règlement. Un oubli est vite arrivé.

**Niveau 2 (ferme, avec une solution)**
> Malgré notre premier rappel, cette facture reste impayée. Si vous traversez une
> difficulté, contactez-nous : un échelonnement est possible. Les services sociaux de
> votre commune (CCAS) ou la CAF peuvent aussi vous orienter vers des aides aux
> loisirs des enfants.

**Niveau 3 (dernier rappel, à aligner sur le règlement de fonctionnement)**
> Nos deux précédents rappels sont restés sans réponse. Sans règlement ni prise de
> contact sous 15 jours, [SUITE_PRÉVUE_PAR_LE_RÈGLEMENT, ex. : « nous vous adresserons
> une mise en demeure par lettre recommandée » / « conformément à l'article X du
> règlement de fonctionnement, … »]. Nous préférons trouver une solution avec vous :
> un simple message suffit pour en discuter.

### 5.4 Formule « Montants (courrier) » corrigée (accents)

```
"Total : " & ROUND(IF({Total facture net (EUR)}=BLANK(),0,{Total facture net (EUR)}),2) & " €" &
" | Déjà réglé : " & ROUND(IF({Total encaissé}=BLANK(),0,{Total encaissé}),2) & " €" &
IF({Reste dû}>0, " | Reste à régler : " & {Reste dû} & " €",
  IF({Reste dû}<0, " | Trop-perçu de " & ABS({Reste dû}) & " € à vous rembourser ou à reporter",
  " | Facture soldée, merci")) &
IF({Acompte exigible}>0, " | Dont acompte de réservation : " & ROUND({Acompte exigible},2) & " €", "")
```

### 5.5 Protocole de test d'envoi (aucune vraie famille)

- **Destinataires TEST contrôlés** grâce à l'adressage « + » de Gmail : par exemple
  `acm.passloisirs2.0+parent1@gmail.com` et `…+parent2@gmail.com`. Tout arrive dans la
  boîte de l'équipe, et chaque adresse reste distincte pour vérifier l'envoi séparé.
  À faire **après** l'activation de la MFA sur cette boîte.
- Scénarios minimum : N1 à J+7 ; N2 tenté à J+15 (doit être **refusé** : délai de
  10 jours) puis à J+21 ; N3 à J+45 ; facture soldée (aucun envoi) ; destinataire avec
  restriction judiciaire (**aucun envoi**) ; **R9** : une facture TEST qui devient échue
  sans aucune modification manuelle doit déclencher seule.
- Pour chaque scénario : courriel reçu (objet, accents, montants), adresse de réponse
  effective (R2), statut et date sur la facture, trace au Journal d'audit.
- Consigner le résultat dans « Règles métier — migration » (ligne RECETTE_EMAILS).

---

## 6. Extraction sécurisée Airtable → Baserow (point 7)

### 6.1 Pourquoi un outil maison plutôt que l'import natif de Baserow

D'après la documentation Baserow (extrait de résultat de recherche), l'import natif
demande un **lien de partage public** de toute la base Airtable. Ce lien contredit
votre règle validée `PARTAGES_PUBLICS_AUTORISES = Non` : une page lisible sans
authentification, potentiellement indexable. Il est donc **écarté** **[RGPD art. 32]**.

L'outil `migration/` passe par les **API officielles** des deux services :

| Garde-fou | Effet |
|---|---|
| Airtable en **lecture seule** | Le code refuse toute requête autre que GET, et le jeton n'a que des scopes de lecture |
| Verrou **FICTIF / RÉEL** | Refus si `MODE_DONNEES` ≠ FICTIF, sauf `PASSAGE_REEL_AUTORISE = Oui` **et** option `--confirm-real` |
| **Minimisation** | 10 champs exclus : les 9 champs DÉPRÉCIÉS ou OBSOLÈTES (dont « Santé repérée ») et la « Valeur confidentielle (direction) » (code physique) |
| **Aucune copie locale** | Les pièces jointes passent directement d'Airtable à Baserow, qui les télécharge lui-même |
| **État sans données** | Le fichier de reprise ne contient que des identifiants techniques ; il est ignoré par Git |
| **Rapprochement** | Rapport ligne par ligne et champ par champ, avec des compteurs uniquement (condition du passage au réel, audit p. 21) |
| **Reprise** | Une interruption n'entraîne ni doublon ni perte : il suffit de relancer la même phase |
| Confirmation | Il faut taper `MIGRER` avant toute écriture |

### 6.2 Plan réel calculé sur votre base (hors ligne, sans données)

| Élément | Nombre |
|---|---|
| Tables | 39 |
| Champs au total | 758 |
| Champs migrés tels quels | 464 |
| Liens entre tables | 110 |
| **Champs calculés à recréer** dans Baserow (formules, cumuls, recherches, comptages) | **174** |
| Champs exclus (minimisation) | 10 |

Les champs calculés **ne sont pas copiés en valeurs figées** : copiés ainsi, ils se
désynchroniseraient en silence (un « Reste dû » figé est faux dès le premier
paiement). Leurs formules d'origine, rendues lisibles avec les noms de champs, sont
listées dans `migration_state/plan_migration.md`, à régénérer avec la commande
ci-dessous. Elles serviront de cahier des charges pour les recréer dans Baserow, ce
que je peux faire ensuite par l'outil MCP.

### 6.3 Mode d'emploi

```bash
python -m migration plan    --base appGyK0pp3tlRABVA            # analyse, n'écrit rien
python -m migration migrate --base appGyK0pp3tlRABVA \
       --workspace <ID> --database-name "Anim'Loisirs 974 — RECETTE"
# → migration_state/rapprochement.md : CONFORME ou écarts à analyser
```

Ce qui **ne se migre pas** automatiquement : les vues, interfaces, formulaires et
automatisations Airtable. Ils seront reconstruits dans l'application Anim'Loisirs 974,
à partir des règles déjà documentées dans la table « Règles métier — migration ».

---

## 7. Séquence recommandée

1. **Sécurité des comptes** : MFA Airtable (§1) et Gmail (§2), preuves consignées.
2. **Décisions** sur Q1 à Q5 (§9), puis correction des relances (§5).
3. **Tests fictifs Airtable** : les 8 envois selon le protocole §5.5, et les points
   « À tester exécution » de la table « Règles métier — migration ».
4. **Gel d'Airtable** comme référence fonctionnelle : réglages de l'espace →
   collaborateurs en lecture, aucune automatisation déployée, export du schéma
   archivé (`python -m migration plan`), puis date de gel notée dans Paramètres.
5. **Baserow** : accès (§3), migration vers une base **RECETTE**, rapprochement
   validé par la Direction, recréation des 174 champs calculés, puis matérialisation
   de l'application Anim'Loisirs 974.
6. **Données réelles** : seulement dans Baserow, après AIPD, DPA Baserow signé,
   restauration testée et `PASSAGE_REEL_AUTORISE = Oui`.
7. **Révocation** du jeton Airtable de migration.

---

## 8. Signalements RGPD / IA Act

| Sujet | Qualification |
|---|---|
| Données d'enfants, santé (PAI, allergies), restrictions judiciaires | **[RGPD art. 9 et art. 35]** : AIPD requise avant le réel (`AIPD_STATUT` = À RENSEIGNER) |
| Airtable aux États-Unis (déduction §4) | **[RGPD chap. V]** : FICTIF uniquement, ce qui est déjà le cas |
| Gmail gratuit comme expéditeur et boîte d'alertes | **[RGPD art. 28 et 32]** : à remplacer avant le réel (§2) |
| Code physique du portail stocké dans Airtable | **[RGPD art. 32]** : il apparaît en clair dans une base hébergée hors UE et a été lu lors de cette analyse. **Recommandation : changer le code** et le conserver uniquement dans un gestionnaire de mots de passe. Il est exclu de la migration |
| Relances automatiques | **[RGPD art. 22]** : il ne s'agit pas d'une décision produisant des effets juridiques. En revanche, une **suspension d'accueil** (niveau 3) doit rester une **décision humaine**, ce que prévoit l'arrêt après le niveau 3 |
| Formules de relance, cycle des retards | **[IA Act]** : **hors périmètre**. Ce sont des règles déterministes et non un système d'IA au sens de l'art. 3.1. Si un score, une prédiction ou un tri automatisé des familles était ajouté, l'analyse IA Act serait à refaire (`IA_FONCTIONS_ACTIVEES` = Aucune) |
| Claude Code (cet assistant) lisant la base | **[RGPD art. 28]** : acceptable sur données FICTIVES. Sur données réelles, ne pas brancher d'assistant IA à la base sans analyse préalable |

---

## 9. Questions ouvertes (je ne peux pas y répondre sans vous)

- **Q1** : nom légal à afficher comme expéditeur et signature : « PASS LOISIRS 2.0 »,
  « Anim'Loisirs 974 », ou les deux ? Quel est le lien juridique entre les deux
  (paramètre `RESPONSABLE_TRAITEMENT` encore « À VALIDER ») ?
- **Q2** : modes de règlement acceptés (chèque, virement avec IBAN, espèces, CESU,
  ANCV, aides CAF…) ?
- **Q3** : que prévoit **réellement** le règlement de fonctionnement en cas d'impayé
  (mise en demeure, suspension, délai) ?
- **Q4** : téléphone administratif et horaires de secrétariat à afficher
  (`TEL_URGENCE_STRUCTURE` est vide, et un numéro d'urgence n'est pas un numéro de
  facturation) ?
- **Q5** : animloisirs974@gmail.com est-elle un compte Airtable (de qui ?) ou
  seulement la boîte d'alertes ? Et quel forfait Baserow est retenu ? Les quotas
  (lignes, stockage) sont à comparer au volume réel d'une saison :
  34 mercredis × 40 places = 1 360 présences, hors vacances et journal d'audit.

---

## 10. Autocritique de cette proposition, puis corrections apportées

| Angle | Faille potentielle | Correction / parade |
|---|---|---|
| Sécurité | Le jeton Airtable donne accès à toute la base pendant la migration | Lecture seule, une seule base, révocation à la fin, jamais en clair dans un fichier versionné |
| Sécurité | Le compte de service Baserow (rôle Builder) est puissant | Compte dédié, MFA, inscrit au registre, désactivé hors des périodes de construction |
| Juridique | La région Airtable est **déduite**, pas attestée | Courriel §4.3. Aucune donnée réelle n'entre dans Airtable : le risque résiduel est nul tant que le mode FICTIF est respecté |
| Juridique | Textes de niveau 3 non alignés sur le règlement de fonctionnement | Variable [SUITE_PRÉVUE…] **bloquante** tant que Q3 n'est pas tranchée |
| Logique | Les 174 champs calculés font l'essentiel de l'intelligence métier, et ils ne migrent pas d'un clic | Inventaire exhaustif généré, recréation pilotée par MCP, vérification des résultats sur les mêmes fixtures que les tests Airtable (ex. RETARD_CYCLIQUE) |
| Logique | Les pourcentages sont stockés en fraction (0,5) dans Baserow | Signalé dans le plan (2 champs) ; affichage à régler dans Baserow |
| Faisabilité | L'outil a été testé **hors ligne** uniquement : le réseau est bloqué ici | Premier lancement réel sur une base **RECETTE** Baserow, jamais sur la base finale ; rapprochement obligatoire |
| Faisabilité | Les URL de pièces jointes Airtable sont temporaires | Les pièces sont transférées pendant la phase « data », dans la foulée de la lecture |
| Économique | Payer un forfait Airtable supérieur uniquement pour la transition | Inutile : la résidence UE est réservée à l'offre Enterprise, et Airtable reste sur données FICTIVES |
| Social | Les relances peuvent toucher des familles en difficulté | Paliers progressifs, échelonnement proposé dès le niveau 2, orientation CCAS/CAF, arrêt humain |
| Écologique | Les relectures multiples de la base Airtable (données, liens, contrôle) | Volume faible (données fictives), quelques minutes d'exécution. Acceptable |
| Politique / souveraineté | Gmail et Airtable sont américains | Tolérés en FICTIF ; trajectoire documentée vers Baserow et une messagerie UE |

---

## Sources

- Airtable, résidence des données (extraits de résultats de recherche, pages non
  consultées en direct car l'accès réseau est bloqué dans l'environnement) :
  [Data residency at Airtable](https://support.airtable.com/articles/3345708696-data-residency-at-airtable),
  [European Data Residency FAQs](https://www.airtable.com/company/data-residency-faqs),
  [Introducing data residency](https://blog.airtable.com/data-residency-for-airtable-customers/)
- Airtable, 2FA : [Enabling two-factor authentication](https://support.airtable.com/docs/enabling-two-factor-authentication),
  [Admin panel settings](https://support.airtable.com/articles/9656884884-settings-airtable-admin-panel)
- Airtable, jetons personnels et limites de débit :
  [API introduction](https://airtable.com/developers/web/api/introduction),
  [Rate limits](https://airtable.com/developers/web/api/rate-limits)
- Baserow, import Airtable par lien public :
  [Import your Airtable base into Baserow](https://baserow.io/user-docs/import-airtable-to-baserow) ;
  API : [Database API](https://baserow.io/user-docs/database-api)
- Base Airtable `appGyK0pp3tlRABVA` : tables Paramètres, Règles métier — migration,
  automatisation « Relance des factures impayées », formules de la table Factures,
  formule « Email financier sécurisé » de la table Personnes (lues le 01/10/2026)
- RGPD : Règlement (UE) 2016/679 (art. 5, 9, 22, 28, 32, 35, 44 à 49) ; CNIL
- IA Act : Règlement (UE) 2024/1689, art. 3.1 —
  [eur-lex.europa.eu](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
