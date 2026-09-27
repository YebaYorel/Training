# PASS LOISIRS 2.0 — Rapport de passation à ASTRA 6

- **Date** : 27/09/2026
- **Rédigé pour** : ASTRA 6 (binôme), à la demande d'Aurélien LUMEKA
- **Base concernée** : Airtable, workspace « Pass Loisirs 2.0 », base `PASS LOISIRS 2.0 — ACM (2026-2027)` (`appGyK0pp3tlRABVA`)
- **Mode de la base** : `MODE_DONNEES = FICTIF` (16 enfants « TEST », e-mails en alias `+…@` de la boîte projet)

**Sources**
- Extrait de la base Airtable `appGyK0pp3tlRABVA` : schéma, texte des 82 formules et des 65 champs calculés reliés, 9 automatisations, 26 pages d'interface, Paramètres et enregistrements de test. Lecture du 27/09/2026.
- Extrait du document « Pass Loisirs 2.0 — Audit de la base et étude de marché » du 23/09/2026 (fichier Word fourni par Aurélien). Il est désigné ci-dessous comme **l'audit du 23/09**.
- Étape 1 du chantier : `audits/pass-loisirs-2.0/01-photographie-existant.md`.

---

## 0. En une minute

1. **Deux correctifs P0 demandés par Aurélien : faits, publiés et vérifiés.**
   - L'animateur ne voit plus les liens adulte-enfant.
   - Le code du portail n'est plus lisible dans aucune interface.
2. **Un défaut de calcul trouvé, puis corrigé.** Les soldes par enfant du tableau de bord comptable incluaient les brouillons et les annulations : 3 784 € affichés au lieu de 1 200 €, −663 € sur un enfant qui ne devait rien.
3. **Dix-sept champs renommés**, sans perte de données : coquilles, homonymes, champs obsolètes signalés par ⛔.
4. **Registre des accès amorcé** (il était vide). Paramètres complétés avec les réponses d'Aurélien. Six traces ajoutées au journal d'audit.
5. **Ce qui reste ne peut pas se faire par l'API.** Il faut des réglages manuels dans l'éditeur d'interface (section 4) et des décisions de la direction (section 6).
6. **Rien n'a été supprimé en données**, et aucune automatisation n'a été activée.

---

## 1. Réponses d'Aurélien du 27/09 (à intégrer comme acquises)

| Question | Réponse | Où c'est inscrit dans la base |
|---|---|---|
| Documents joints ? | Oui : l'audit du 23/09 (Word). Aucun code source ni ZIP. | — |
| Forfait Airtable | **Gratuit**, passage au forfait supérieur souhaité | Paramètre `FORFAIT_AIRTABLE` (À VALIDER) |
| Responsable de traitement | **PASS LOISIRS 2.0**, gérée par **Stan**, associé d'Aurélien | Paramètre `RESPONSABLE_TRAITEMENT` (À VALIDER : forme juridique, SIRET et nom complet manquants) |
| Correctifs P0-1 et P0-2 | Autorisés | Journal d'audit `ASTRA-2026-09-27-01` et `-02` |

## 2. Modifications effectuées dans la base

Toutes les modifications ont été tracées au **Journal d'audit** (`ASTRA-2026-09-27-01` à `-05`). Les renommages et les changements de formule sont **réversibles**.

### 2.1 P0-1 — Interface Animateur : droits de récupération retirés

- **Avant** : la page « Enfants du jour — consignes utiles » (`pagAbLBEByEuiqCBi`) laissait l'animateur **modifier le champ « Liens personne-enfant »**. Or c'est ce lien qui fonde un départ sécurisé.
- **Fait** :
  - Une nouvelle page a été créée (`pagc7S4murBSqdKQA`), avec le même nom et les mêmes colonnes utiles : Nom, Classe, Vigilance sanitaire, Consigne du jour sans détail médical, Nage.
  - Elle ne contient **plus** le champ « Liens personne-enfant ».
  - Elle est limitée aux enfants dont « Actif » vaut Oui.
  - L'ancienne page a été supprimée et l'interface republiée.
- **Vérifié** : la page publiée n'expose plus le lien.
- **Limite** : l'API ne permet de régler ni le caractère modifiable des champs, ni la création d'enregistrements. Nom, Classe et Nage restent modifiables, et la création en ligne reste active (voir 4.1).
- **Étiquette** : RGPD art. 32 (sécurité) + sécurité des mineurs.

### 2.2 P0-2 — Code d'accès physique du portail masqué

- **Correction de mon étape 1.** Le tableau de bord « 01 · Vue d'ensemble » ne montrait en réalité qu'**une** ligne de Paramètres (MODE_DONNEES), à cause d'un filtre invisible via l'API.
- **Exposition réelle** : la page Direction « **Paramètres et points à trancher** » (`pagv8hwEge5g0bdgU`) affichait les 40 paramètres, **code compris**, dans une colonne modifiable.
- **Fait** :
  - Création du champ **« Valeur confidentielle (direction) »** (`fldM1FbFEdCknp05o`) dans Paramètres. Il ne figure dans aucune interface.
  - La valeur du code y a été **déplacée**, pas supprimée.
  - Le champ « Valeur » contient désormais : « Communiqué en main propre lors du premier jour d'accueil ».
- **Effet secondaire voulu** : l'automatisation de confirmation (`wflpiz64wtdqQeXXm`, non déployée) lit ce champ « Valeur ». Si elle est un jour activée, elle **n'enverra plus le code par e-mail**, conformément à l'audit du 23/09 (§2, P0).
- **À faire par la direction** : **changer le code**, car il a été lisible dans une interface.
- **Étiquette** : sécurité physique, RGPD art. 32.

### 2.3 Soldes par enfant faux sur le tableau de bord comptable (nouveau constat, corrigé)

- **Cause** :
  - « Reste dû » et « Statut paiement » (table Enfants) étaient calculés à partir de « Tarif dû ».
  - Or « Tarif dû » additionne **toutes** les inscriptions, y compris **Brouillon** et **Annulée**.
  - Ces deux champs sont affichés sur « 09 · Comptabilité et alertes ».
- **Fait** : les deux formules s'appuient désormais sur « Montant à facturer (net) ». La description de chaque champ explique la correction.
- **Vérifié sur les fiches de test** :

| Fiche | Reste dû avant | Reste dû après | Attendu (« Reste à payer (net) ») |
|---|---|---|---|
| TEST FICTIF - Recette T14 | 3 784 | **1 200** | 1 200 |
| TEST - LEBON Manon | −663 | **0** | 0 |
| TEST - BEGUE Jade | −50 | **0** | 0 |
| TEST - VIENNE Sarah | 80 | 80 | 80 |

- Pourquoi corriger la formule plutôt que la page : recréer les tableaux de bord aurait fait perdre leurs **filtres cachés**, que l'API ne restitue pas.
- **Étiquette** : sans objet RGPD (logique financière). L'exactitude des montants facturés relève du droit de la consommation et de la comptabilité.

### 2.4 Hygiène du schéma : 17 renommages, aucune donnée touchée

Les formules, automatisations et interfaces désignent les champs par leur **identifiant**. Un renommage ne casse donc rien.

| Table | Champ (identifiant) | Nouveau nom |
|---|---|---|
| Sessions | `fldMVVzDWsudod855` | Allergènes du menu |
| Enfants | `fldl365UukaoW1YmF` | Allergènes (auto) |
| Santé | `fldJJvLNFCFiWu0eL` | Allergènes déclarés |
| Présences | `fldIKeE2NJB91fKix` | Allergènes enfant |
| Présences | `fldUcEHL05lolACKB` | Allergènes du menu servi |
| Menus | `fldI9KETEtC0VWWHa` | Allergènes présents |
| Équipe | `fldhcNAJpF98JD61z` | Départs remis (en tant qu'agent) |
| Équipe | `fldWMS3gbflph8jEx` | Dérogations de départ autorisées (en tant que responsable) |
| Enfants | `fldgGebw9ombhJnX6` | ⛔ OBSOLÈTE — Tarif dû (brouillons et annulations inclus) |
| Enfants | `fldoupkkMBdRMZZ4g` | ⛔ OBSOLÈTE — Total encaissé (brut, risque de double comptage) |
| Enfants | `fldhe9vXbdWBTyuYe` | ⛔ À SUPPRIMER — détail médical (hors habilitation) |
| Enfants | `fld3SYpHDxoj2kL06` | ⛔ DÉPRÉCIÉ — Responsables (ancienne table) |
| Enfants | `fldJwZmT01Z2lvQxX` | ⛔ DÉPRÉCIÉ — Personnes autorisées (ancienne table) |
| Présences | `fldtaYEsA4YYuv6Dr` | ⛔ DÉPRÉCIÉ — Récupéré par (texte libre) |
| Présences | `fldrlgE8PPdHmqMBP` | ⛔ DÉPRÉCIÉ — Autorisé (case) |
| Présences | `fldLHXGLD68H7JIey` | ⛔ DÉPRÉCIÉ — Arrivée (texte) |
| Présences | `fldmauNlQ0c7oandm` | ⛔ DÉPRÉCIÉ — Départ (texte) |

### 2.5 Registre des accès, paramètres et journal

- **« Accès, jetons et partages » était vide** : le contrôle S05 de l'audit n'avait jamais été exécuté.
- Ligne créée : **ACC-001**, le connecteur Airtable de l'assistant Claude.
  - Il expose des données de santé et passe par Anthropic, aux États-Unis.
  - C'est un **transfert hors UE**, acceptable seulement en mode FICTIF.
  - **Avant le passage en RÉEL** : révoquer ce connecteur, ou l'encadrer par un contrat de sous-traitance et un mécanisme de transfert. *(RGPD art. 28 et 44+ ; IA Act : simple assistance, aucune décision automatisée.)*
- Paramètres renseignés : `RESPONSABLE_TRAITEMENT` et `FORFAIT_AIRTABLE` (nouveau), tous deux au statut À VALIDER.
- Journal d'audit : 5 traces `ASTRA-2026-09-27-01` à `-05`.
  - **Précision** : l'horodatage que j'ai déclaré dépasse de 5 à 9 minutes l'heure d'enregistrement réelle (10h20 UTC).
  - C'est « Horodatage système (non falsifiable) » qui fait foi. Selon la règle de la base, une trace ne se corrige pas : elle est laissée en l'état et signalée ici.

## 3. Audit des formules : les 82 formules et 65 champs calculés reliés lus en entier

L'étape 1 n'avait pas pu lire le texte des formules. C'est fait. **Les 147 champs calculés sont valides : aucune formule n'est cassée.** Voici les constats.

| # | Constat | Gravité | Étiquette |
|---|---|---|---|
| F1 | **La pénalité de retard s'applique dès le 1er retard**, alors que la règle vaut « dès le 2e retard » (`PENALITE_DECLENCHE_A = 2`, CDC §12). La formule « Pénalité retard (EUR) » ne compte pas les retards précédents. Correction impossible dans une formule de ligne : il faut un compteur par enfant et par saison, ou un contrôle humain avant facturation. | **P1**, risque de litige avec les familles | Droit de la consommation / règlement intérieur |
| F2 | **Barèmes écrits en dur**, alors que la base affirme « jamais en dur » : 25 € et 18h00 (1080) dans les pénalités ; 07h00, 08h30 et 16h30 (420, 510, 990) dans « Contrôle horaires » ; acompte vacances de **100 €** dans « Acompte exigible », alors que `ACOMPTE_DEFAUT` est encore À VALIDER. Modifier les Paramètres ne change donc rien aux calculs. | P1 | — |
| F3 | **Taux d'encadrement unique de 12 enfants par animateur** dans « 📋 SYNTHÈSE DU JOUR », sans tenir compte de l'âge. Or les taux réglementaires dépendent de l'âge (moins ou plus de 6 ans) et du type d'accueil (périscolaire, notamment le mercredi, ou extrascolaire). Un groupe de moins de 6 ans à 12 pour 1 passerait « OK ». **Taux exacts à vérifier sur Légifrance** (Code de l'action sociale et des familles, art. R227-15 et suivants) avant de coder la règle. | **P1 sécurité** | Réglementation ACM |
| F4 | « ⚠ ALERTE REPAS » croise bien les 14 allergènes INCO, mais **ni les régimes** (sans porc, végétarien, médical) ni les textures. « Régime spécial » est saisi dans Santé mais jamais croisé avec « Sans porc prévu ? » du menu. | P2 | RGPD art. 9 si le régime est médical ; donnée pouvant révéler une conviction religieuse (art. 9) : minimiser |
| F5 | Logique solide, à conserver telle quelle : « CONTRÔLE DÉPART » (restriction judiciaire bloquante, pièce d'identité exigée, lien d'un autre enfant détecté), « Autorisation valable aujourd'hui », « Détection d'antidatage », « DÉLAI 72 H », « Validité document », anti-doublons, relances progressives. | ✔ | RGPD art. 10, 32, 33 |
| F6 | « Tarif normal » **privilégie déjà les lignes de prestation** quand il y en a, et ne retombe sur l'ancien tarif qu'à défaut. L'audit du 23/09 parle de « deux modèles de tarification qui coexistent » : c'est vrai, mais le passage de l'un à l'autre est **contrôlé**, pas contradictoire. La vraie incohérence était dans les soldes (corrigée en 2.3). | Nuance | — |

## 4. Actions manuelles restantes (impossibles par l'API)

Elles sont à faire par Stan ou Aurélien dans l'**éditeur d'interface** Airtable, ou par ASTRA 6 s'il dispose d'un accès à l'écran. Ordre conseillé :

1. **Page Animateur « Enfants du jour »** : passer Nom complet, Classe et Nage en lecture seule, et désactiver « Ajouter des enregistrements ». Même chose pour « Liste du jour » : l'animateur peut aujourd'hui créer une présence pour n'importe quel enfant.
2. **Page Direction « Journal d'audit »** : **tous les champs sont modifiables**, y compris l'horodatage, l'acteur et le résultat. Les traces sont donc falsifiables. Il faut tout passer en lecture seule. Côté base, interdire la suppression de lignes si le forfait retenu le permet. *(RGPD art. 32 et responsabilité, art. 5-2.)*
3. **Supprimer le champ « ⛔ À SUPPRIMER — détail médical (hors habilitation) »** (`fldhe9vXbdWBTyuYe`, table Enfants). Aucune formule ne s'en sert (vérifié). **Vérifier avant suppression** qu'aucune automatisation ni vue ne l'utilise : je n'ai pas lu le détail des 9 automatisations nœud par nœud, sauf la confirmation. *(RGPD art. 9.)*
4. **Changer le code du portail** et le mettre à jour dans « Valeur confidentielle (direction) ».
5. **Page brouillon « 10 · Soldes fiables »** (`pag6fcIH4tdqh8hrT`) : la publier ou la supprimer. Attention : **publier l'interface « Anim'Loisirs 974 — Pilote ACM » la publiera aussi**. C'est pour cette raison que je n'ai pas republié cette interface.
6. **Compléter le registre des accès** : collaborateurs nominatifs, liens de partage, formulaires, boîtes Gmail des alertes et de l'expédition. *(Contrôle S05.)*
7. **Contrôles à l'écran** : région d'hébergement, MFA de chaque compte, partages publics. Ils sont invisibles via le connecteur.

## 5. Corrections de mes propres constats de l'étape 1

| Constat de l'étape 1 | Ce qui est vrai après vérification |
|---|---|
| P0-2 : « code visible sur le tableau de bord 01 » | **Faux sur ce point** : filtre caché. L'exposition était sur la page Direction « Paramètres et points à trancher ». Corrigé dans les deux cas. |
| « Le texte des formules n'est pas lisible » | **Faux** : l'outil `get_table_schema` le renvoie. Les formules sont auditées (section 3). |
| P1-5 : « deux modèles de prix » | Nuancé (F6) : le vrai défaut était dans les soldes. |

**Écarts avec l'audit du 23/09 à éclaircir** :
- Cet audit mentionne **39 tables** et 14 paramètres « À RENSEIGNER » ; le 27/09 j'en compte **36** et 13.
- Soit 3 tables ont été supprimées entre-temps, soit le décompte différait. **À demander à Aurélien ou Stan**, car une suppression de tables doit figurer au journal.

## 6. Ce qui reste bloquant avant toute donnée réelle (P0 ouverts)

| P0 | Qui décide | Statut |
|---|---|---|
| Responsable de traitement complet (forme juridique, SIRET, représentant) | Stan | En cours : À VALIDER |
| Contrat de sous-traitance (DPA) signé, région d'hébergement, mécanisme de transfert hors UE | Stan + Aurélien | À RENSEIGNER |
| AIPD (quasi certaine : santé de mineurs) | Stan, avec l'accompagnement d'Aurélien | À RENSEIGNER |
| Qualification HDS du suivi sanitaire | Direction, après analyse | À RENSEIGNER |
| Pièces jointes sensibles servies hors habilitation (5 tables) | Architecture cible (couche serveur) | Non conforme, reconnu dans la base |
| Adresses Gmail d'expédition et d'alertes | Stan | À remplacer par un domaine propre et une messagerie européenne, avec MFA |
| Restauration de sauvegarde testée | Stan | À RENSEIGNER |
| MFA sur tous les comptes | Stan | À RENSEIGNER |
| Cloisonnement entre associations (produit multi-clients) | Architecture cible | Retenu dans l'audit du 23/09 : une base par association |

## 7. Suite du plan du binôme : où en est-on

| Étape | Statut au 27/09 | Prochaine action pour ASTRA 6 |
|---|---|---|
| 1. Photographie de l'existant | **Fait** | — |
| 2. Audit fonctionnel des parcours (préinscription → documents) | Partiel : formules auditées (section 3) | Dérouler chaque parcours sur les fiches TEST, **automatisations désactivées**, avec un jeu de cas (fratrie, parents séparés, restriction judiciaire, retard, allergie) |
| 3. Architecture, sécurité et conformité | Partiel : P0 listés, 2 corrigés | Traiter la section 4, puis l'AIPD |
| 4. Étude de marché | Faite dans l'audit du 23/09, avec des prix non vérifiés (proxy bloqué) | Vérifier chaque prix et demander des démos (MonEspaceACM, Silia, Kananas) |
| 5. Décision produit | Ébauchée (audit du 23/09, §5, §6 et §9) | À faire valider par Stan et Aurélien |
| 6. Architecture cible et feuille de route | Baserow retenu dans l'audit du 23/09, Firebase écarté | **Le serveur MCP Baserow de ce dépôt ne se connecte toujours pas**, faute de fichier `.env`. Voir le `README.md` du dépôt |

**Recommandation sur le forfait Airtable** (question d'Aurélien) : ne payer le forfait supérieur que si la transition vers Baserow dure plus de quelques mois.
- En gratuit, la base ne peut pas tenir une saison réelle : 1 360 présences pour les seuls mercredis, sans compter le journal.
- Un forfait supérieur ne règle ni la localisation hors UE ni le transfert.
- Les quotas et les prix sont à vérifier le jour J sur airtable.com/pricing. Je ne les cite pas de mémoire.

## 8. Autocritique de cette intervention

| Angle | Faille | Correction ou garde-fou |
|---|---|---|
| Sécurité | La page Animateur autorise encore la création d'enfants et la modification de noms. | Action manuelle 4.1, en tête de liste. |
| Sécurité | Le code du portail reste en clair dans la base, pour les collaborateurs qui ont accès à la base entière. | Il n'est plus dans aucune interface. Le vrai remède est le code de retrait par enfant et par jour (audit du 23/09, levier 4). |
| Juridique | En lisant la base, l'assistant a lui-même fait transiter des données (fictives) hors UE. | Inscrit au registre (ACC-001), avec la condition de révocation avant le passage en RÉEL. |
| Logique | J'ai d'abord déclaré à tort que le tableau de bord 01 exposait le code. | Corrigé et documenté (section 5). Leçon pour ASTRA 6 : **toujours lire une page avec `list_records_for_page`** avant de conclure sur ce qu'elle affiche. |
| Faisabilité | Je n'ai pas lu le détail de 8 des 9 automatisations. | Action 4.3 : vérifier avant toute suppression de champ. |
| Traçabilité | Horodatages déclarés approximatifs dans le journal. | Signalé en 2.5. L'horodatage système fait foi. |
| Économique | Aucun coût engagé. Le forfait supérieur reste une décision de la direction. | Section 7. |

## 9. Questions ouvertes pour Aurélien ou Stan

1. Quels sont la forme juridique, le SIRET et le nom complet du représentant de PASS LOISIRS 2.0 ? Quel est le lien juridique avec « Anim'Loisirs 974 » ?
2. Trois tables ont-elles été supprimées entre le 23/09 et le 27/09 (39 → 36) ? Si oui, lesquelles et pourquoi ?
3. Qui a accès à l'interface « Anim'Loisirs 974 — Pilote ACM » ? Elle donne des droits d'écriture larges sur presque toutes les tables.
4. Faut-il publier ou supprimer la page brouillon « 10 · Soldes fiables » ?
5. Pour F1 : la pénalité doit-elle vraiment ne s'appliquer qu'à partir du 2e retard **par enfant et par saison** ? Ou par période ?
