# 11 — Aller chercher les contrats : OPCO, plateformes et prospection

---

## 1. ⚠️ Correction préalable : « scruter les bases de données des OPCO »

**Cette approche n'est pas praticable, et il faut le savoir avant de perdre des semaines.**

Les OPCO **ne publient pas la liste de leurs entreprises adhérentes.** Ce ne sont pas des
bases ouvertes : ce sont des fichiers de gestion paritaire. Vous ne pouvez ni les consulter,
ni les acheter, ni les obtenir auprès d'un conseiller.

⚖️ **Et si vous en obteniez une par un autre canal, l'utiliser serait problématique :**
détournement de finalité (art. 5.1.b RGPD — données collectées pour la gestion de la
formation, pas pour la prospection d'un tiers), absence de base légale, et absence
d'information des personnes. **Ne cherchez pas cette porte : elle n'existe pas, et celle
qui y ressemble est piégée.**

**L'article 4 de l'IA Act ne change rien à cela.** Il crée une obligation **chez
l'employeur** ; il ne vous ouvre aucun droit d'accès à un fichier.

**Bonne nouvelle : il existe deux voies bien meilleures, et vous n'en utilisez aucune.**

---

## 2. Voie A — Le ciblage légal et gratuit : la base SIRENE

**`annuaire-entreprises.data.gouv.fr`** et l'**API Recherche d'entreprises** (open data,
gratuite, sans compte) donnent, pour toute la France : **SIREN/SIRET, raison sociale,
adresse, commune, code NAF, tranche d'effectif, date de création, état administratif**.
Filtrage par **secteur + localisation + taille**. C'est exactement ce qu'il vous faut pour
bâtir vos 300 comptes cibles (doc 07, action n°10).

**Requête type pour votre secteur de tête :**

| Paramètre | Valeur |
|---|---|
| Département | **974** |
| Codes NAF (hôtellerie-restauration) | `55.10Z` hôtels · `55.20Z` hébergement touristique · `56.10A` restauration traditionnelle · `56.10C` restauration rapide · `56.30Z` débits de boissons *(à confirmer dans l'annuaire)* |
| Tranche d'effectif | **3 à 49 salariés** — en dessous : pas de budget formation ; au-dessus : cycle de vente long |
| État | Actif uniquement |

> **Pourquoi « 3 salariés minimum » :** les deux tiers des entreprises réunionnaises sont
> des indépendants **sans aucun salarié** (INSEE). Sans salarié, pas de contribution
> formation, pas de plan de développement des compétences, **et l'article 4 de l'IA Act
> a beaucoup moins de prise**. Filtrer sur l'effectif divise votre liste par trois et
> multiplie votre taux de transformation.

### Les deux limites à connaître

1. **SIRENE ne contient ni e-mail ni contact nominatif.** Elle sert à **cibler**, pas à
   joindre. Le nom du dirigeant se trouve ensuite sur le site de l'entreprise, LinkedIn,
   ou en appelant le standard. C'est du travail — c'est aussi ce qui fait que vos
   concurrents ne le font pas.
2. ⚖️ **Le statut « diffusion partielle »** (qui a remplacé « non-diffusible » en 2023)
   concerne des entreprises, notamment des personnes physiques, dont les informations
   **ne doivent pas être rediffusées ni utilisées à des fins de prospection**.
   **Excluez-les systématiquement de votre liste.** C'est une ligne de code ou un filtre —
   et c'est exactement le genre de rigueur que vous pourrez montrer en rendez-vous.

**Où ça va :** table `Comptes cibles` de votre base Baserow (annexe schéma), avec les champs
`Source = Annuaire des entreprises (open data)` et `Base légale = Intérêt légitime (B2B)`.

---

## 3. Voie B — Se faire référencer : les entreprises viennent à vous

C'est la voie que vous n'utilisez pas et qui rapporte le plus pour l'effort fourni.

### 3.1 — Les catalogues OPCO

**7 OPCO sur les 11 nationaux sont représentés à La Réunion** — parmi eux **AFDAS**,
**OCAPIAT**, **OPCO Mobilités** (délégation régionale Réunion) et **AKTO**.

Plusieurs OPCO référencent les organismes de formation dans des **annuaires consultés par
leurs entreprises adhérentes** (OPCO Mobilités publie par exemple un « catalogue de
référence des organismes de formation »). **La certification Qualiopi est le prérequis — vous
l'avez.** La procédure est généralement simple : transmission du certificat en cours de
validité + dossier de référencement en ligne, propre à chaque OPCO.

**Action, semaine 2 :** demander le dossier de référencement aux **7 délégations réunionnaises**,
une par une. Comptez une demi-journée au total. **C'est le meilleur rapport temps/retour de
tout votre plan** : vous passez du statut de démarcheur à celui de prestataire référencé.

### 3.2 — Le conseiller OPCO : le prescripteur que tout le monde oublie

Les OPCO ont pour mission d'**accompagner les TPE-PME dans la définition de leurs besoins
de formation**. Leurs conseillers en région **orientent** les entreprises. Un conseiller qui
vous connaît vaut cinquante appels à froid.

**Action :** obtenir un rendez-vous de présentation avec le conseiller formation de chacune
des délégations. Message : *« Je suis l'organisme certifié Qualiopi qui traite l'obligation
de l'article 4 de l'IA Act, en présentiel, sur l'île. Vos adhérents vont vous poser la
question — je vous donne de quoi y répondre. »* **Vous leur rendez service. C'est tout
l'intérêt de l'angle réglementaire.**

### 3.3 — Le Carif-Oref et les plateformes d'offre

- **Carif-Oref de La Réunion** *(à confirmer : la structure qui apparaît est `mio-reunion.re`)* —
  c'est le référentiel régional de l'offre de formation, consulté par les prescripteurs et
  France Travail. **Y référencer votre offre est indispensable et gratuit. Vérifiez la
  procédure exacte auprès d'eux.**
- **DEETS Réunion — dispositif « Ambassadeurs IA »** : 7 ambassadeurs labellisés.
  **Candidature = notoriété institutionnelle gratuite.** Prioritaire.
- **EDOF / Mon Compte Formation** : possible, mais **à ne pas prioriser**. Le CPF est en
  recul de 33 % en 2026 et plafonné à 1 500 € pour les certifications du Répertoire
  Spécifique depuis le 26/02/2026. L'effort administratif y est disproportionné par rapport
  au retour pour votre modèle intra-entreprise.
- **CCI Réunion** : ne l'affrontez pas, **branchez-vous dessus**. Proposez d'intervenir dans
  leur programme plutôt que de vendre contre lui.

---

## 4. Voie C — La prospection directe (celle qui paie les factures les 6 premiers mois)

⚖️ **Le cadre légal, exactement.** En **B2B**, la prospection par e-mail ou messagerie est
autorisée dès lors que : le message est **en rapport avec l'activité professionnelle** du
destinataire, la personne est **informée** au moment de la collecte, et un **moyen
d'opposition simple** est fourni. La base légale est l'**intérêt légitime**. En **B2C**,
le **consentement préalable** reste obligatoire pour l'e-mail et le SMS.
Le **téléphone** relève de règles distinctes : **vérifiez Bloctel** pour tout appel vers un
professionnel exerçant en nom propre.

**Séquence recommandée, par compte cible :**

| Jour | Canal | Objet |
|---|---|---|
| J0 | **Téléphone** | Une seule question : « quelqu'un chez vous utilise-t-il un outil d'IA ? » |
| J+1 | **E-mail** (si l'appel a abouti) | La checklist art. 4, avec la mention d'information et le lien de désinscription |
| J+4 | **LinkedIn** | Demande de connexion personnalisée, jamais de pitch en message d'ouverture |
| J+10 | **Téléphone** | Relance unique. **Puis on arrête.** |

**Trois règles que je vous demande de tenir :**
1. **Jamais plus de deux relances.** Un dirigeant qui ne répond pas deux fois n'achètera pas,
   et votre réputation sur une île se joue à cela.
2. **Statut `Opposé` = exclusion définitive** dans Baserow. Jamais de « on retentera l'an
   prochain ».
3. **Traçabilité de la source** pour chaque contact. Le jour où quelqu'un demande « où
   avez-vous eu mon numéro ? », vous devez pouvoir répondre en trois secondes.

---

## 5. L'ordre de priorité, avec le retour attendu

| # | Action | Temps | Retour attendu |
|---|---|---|---|
| 1 | **Référencement auprès des 7 OPCO réunionnais** | ½ j | Flux entrant durable, effort unique |
| 2 | **Rendez-vous avec les conseillers OPCO** | 2 j | Prescription — le meilleur canal |
| 3 | **Candidature Ambassadeurs IA (DEETS)** | ½ j | Crédibilité institutionnelle |
| 4 | **Référencement Carif-Oref Réunion** | ½ j | Visibilité prescripteurs |
| 5 | **Liste de 300 comptes via l'Annuaire des entreprises** | 1,5 j | La matière de votre prospection |
| 6 | **80 appels sortants** | 4 j | 20 rendez-vous, 6 ventes *(doc 07)* |
| 7 | **2 partenariats experts-comptables** | 1 j | Accès à plusieurs centaines de TPE |
| 8 | EDOF / Mon Compte Formation | 2 j | **Faible — à faire en dernier, ou pas du tout** |

> **Les actions 1 à 4 coûtent 3,5 jours au total et aucune n'est faite aujourd'hui.**
> C'est, de loin, le meilleur rendement de votre trimestre — et c'est du travail
> administratif, pas de la vente. Vous pouvez le faire un samedi.

---

## ⚖️ Réflexe RGPD / IA Act sur ce document

- **RGPD** — traitement « prospection commerciale B2B » : à **inscrire au registre art. 30**,
  base légale **intérêt légitime**, durée **3 ans après le dernier contact**, information
  au premier contact, droit d'opposition dans chaque message.
- **RGPD** — **excluez les établissements en « diffusion partielle »** de toute prospection.
- **RGPD** — le nom et la fonction d'un dirigeant sont des **données personnelles**, même en
  contexte professionnel. Minimisez : nom, fonction, téléphone pro, e-mail pro. **Pas de
  notes d'appréciation personnelle dans les commentaires.**
- **RGPD** — ne synchronisez **jamais** votre liste de prospection dans WhatsApp Business ni
  dans un outil publicitaire (audiences personnalisées par import de fichier).
- **IA Act art. 4** — c'est votre argument, pas votre droit d'accès. Formulez-le comme un
  service rendu au dirigeant, jamais comme une menace.
- **IA Act art. 50** — si vous utilisez l'IA pour rédiger vos messages de prospection, cela
  ne crée pas d'obligation de marquage (ce n'est pas du contenu synthétique publié au
  public). En revanche, **un agent conversationnel automatisé qui prospecterait à votre
  place devrait s'annoncer comme IA.** Recommandation : **n'automatisez pas le premier
  contact.** Sur un marché de 4 600 TPE-PME, votre voix est le produit.

**Sources** : [Annuaire des entreprises — API](https://annuaire-entreprises.data.gouv.fr/donnees/api-entreprises) ·
[data.gouv.fr — base SIRENE](https://www.data.gouv.fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret) ·
[INSEE — SIRENE open data](https://www.insee.fr/fr/information/3591226) ·
[DEETS Réunion — les OPCO](https://reunion.deets.gouv.fr/Les-operateurs-de-competences) ·
[OPCO Mobilités — délégation La Réunion](https://www.opcomobilites.fr/votre-delegation-regionale/la-reunion) ·
[OPCO Mobilités — catalogue de référence des OF](https://www.opcomobilites.fr/entreprise/former-et-qualifier-mes-collaborateurs/catalogue-de-reference-des-organismes-de-formation) ·
[MIO Réunion — les OPCO](https://mio-reunion.re/opco/) ·
[CNIL — prospection commerciale](https://www.cnil.fr/fr/la-prospection-commerciale) ·
[Certifopac — Datadock/Qualiopi et financeurs](https://certifopac.fr/qualiopi/financeurs/datadock/)
