# 02 — Mise en place des réseaux professionnels YEBA FORMATIONS

> **Ce que je ne peux pas faire, dit clairement.** Je n'ai ni vos identifiants, ni accès à
> votre téléphone, ni à votre double authentification, ni à votre pièce d'identité. Je ne
> peux donc **pas créer les comptes à votre place** — et il ne faut pas qu'un tiers le
> fasse : une création de compte professionnel Meta engage votre identité et votre
> responsabilité d'éditeur. Ce document est le **runbook complet** : chaque écran, chaque
> champ, chaque texte est pré-rédigé. Comptez **2 h 30 en une seule séance**.

---

## Décision préalable : créer, ne pas convertir

Vous vouliez « faire la partie professionnelle » de vos comptes personnels. **Non.**
Trois raisons, par ordre de gravité :

1. **RGPD.** Vos contacts personnels ne constituent pas une base de prospection licite.
   Convertir le compte vous met en tentation permanente de les démarcher, et de synchroniser
   votre répertoire. La séparation physique est la seule protection qui tienne.
2. **Sécurité.** Un compte personnel de 10 ans traîne des sessions, des applications tierces
   et des mots de passe anciens. Le jour où il est compromis, la marque tombe avec.
3. **Signal.** Un dirigeant qui vous découvre doit tomber sur un actif professionnel net,
   pas sur vos photos de famille de 2017.

**Exception acceptée :** votre **profil LinkedIn personnel reste personnel et devient votre
principal actif** — sur LinkedIn, la personne surperforme la page. On crée quand même une
**Page entreprise YEBA FORMATIONS**, mais elle sert de vitrine et de preuve d'existence, pas
de canal principal.

---

## Étape 1 — Socle d'identité (30 min, à faire AVANT tout compte)

| Élément | Valeur | Statut |
|---|---|---|
| Nom d'usage partout | `YEBA FORMATIONS` | ✅ |
| Identifiant / @handle | `@yebaformations` (identique sur les 3) | à réserver |
| Adresse e-mail dédiée | `contact@yebaformations.re` | **bloquant — à créer chez OVH en premier** |
| Numéro professionnel | ligne **dédiée**, pas votre mobile perso | **bloquant — voir §4** |
| Logo | carré 1080×1080, lisible à 40 px | à fournir |
| Couleurs de marque | **?** — non documentées, je ne les invente pas | **à me donner** |
| Site | `https://www.yebaformations.re` | en cours (doc 05) |
| SIRET | 814 622 262 00032 | ✅ |
| NDA | 04973676397 | ✅ |
| Qualiopi | 25FOF02027.1 | ✅ |

> ⚠️ **Créez `contact@yebaformations.re` avant tout le reste.** Créer les comptes sociaux
> sur une adresse Gmail personnelle, c'est se condamner à une migration douloureuse plus
> tard, et c'est un point faible de sécurité. OVH fournit les boîtes avec le domaine.

**Mentions obligatoires à placer dans chaque bio** (organisme de formation) :
`Organisme de formation certifié Qualiopi — NDA 04973676397` + lien vers vos mentions
légales. La certification Qualiopi impose des règles d'usage du logo : n'utilisez le logo
Qualiopi qu'avec la mention de la ou des catégories d'actions concernées.

---

## Étape 2 — Meta : l'ordre est impératif

L'erreur classique est de créer l'Instagram d'abord. **Faites l'inverse**, sinon vous
devrez tout redéfaire.

### 2.1 — Compte Meta Business (Business Manager) — *en premier*
1. `business.facebook.com` → Créer un compte professionnel.
2. Nom : `YEBA FORMATIONS` · e-mail : `contact@yebaformations.re`.
3. **Paramètres → Informations sur l'entreprise** : renseigner SIRET, adresse, site.
4. **Sécurité : activer la double authentification obligatoire pour tous** (Paramètres →
   Centre de sécurité → exiger la 2FA).
5. Créer immédiatement **un second administrateur** (personne de confiance). Un seul admin
   = perte définitive du compte en cas de piratage ou de perte du téléphone.

### 2.2 — Page Facebook professionnelle
- Créée **depuis** le Business Manager (Comptes → Pages → Ajouter → Créer une page).
- Catégorie : `Centre de formation professionnelle` (+ `Service de conseil aux entreprises`).
- Bouton d'action principal : **« Réserver »** pointant vers votre page de prise de RDV
  souveraine (doc 05), **pas** vers Messenger.
- Zone : La Réunion. Renseigner les horaires réels.
- **À propos** — texte prêt :

> YEBA FORMATIONS forme et accompagne les TPE-PME réunionnaises sur l'intelligence
> artificielle, l'automatisation des tâches et la conformité RGPD / IA Act.
> Formations en intra et inter-entreprise · Implémentation de workflows · Mise en
> conformité article 4 de l'IA Act.
> Organisme certifié Qualiopi — NDA 04973676397 · Référent handicap.
> 📍 La Réunion · 🔗 www.yebaformations.re

### 2.3 — Compte Instagram professionnel
- **Nouveau compte**, e-mail `contact@yebaformations.re`, handle `@yebaformations`.
- Paramètres → Type de compte → **Entreprise** (pas Créateur : le type Entreprise donne
  accès aux coordonnées, à la catégorie et à la programmation).
- **Lier à la Page Facebook depuis le Business Manager**, pas depuis l'application.
- Catégorie affichée : `Centre de formation`.
- **Bio** — 150 caractères max, version prête (139 car.) :

```
IA & conformité pour les TPE-PME péi 🇷🇪
Je vous fais gagner des heures, sans vous mettre hors la loi
Qualiopi · NDA 04973676397
👇 Diagnostic gratuit
```

- **Lien** : `https://www.yebaformations.re/liens` — **votre propre page de liens**.
  Pas Linktree (société américaine, traceurs, et vous lui offrez vos statistiques de clics).
  Une page HTML de 30 lignes chez OVH fait le même travail, en mieux et en souverain.
- **Story à la une n°1 « Qui je suis »**, n°2 « Résultats clients », n°3 « IA Act ».

### 2.4 — WhatsApp Business
- **Application WhatsApp Business** (gratuite), sur un **numéro différent** de votre
  WhatsApp personnel. Si vous n'avez qu'un téléphone : eSIM seconde ligne, ou
  WhatsApp Business sur numéro fixe (validation par appel vocal).
- ⚠️ **Ne validez jamais « autoriser l'accès aux contacts » à l'installation.** Cette
  synchronisation transfère à Meta les coordonnées de personnes qui n'y ont pas consenti.
  C'est le piège RGPD n°1 de WhatsApp Business (voir doc 06).
- Configurer : profil (adresse, site, horaires, catalogue), **message d'accueil**,
  **message d'absence**, **réponses rapides** (`/tarif`, `/qualiopi`, `/rdv`, `/opco`).
- **Étiquettes** à créer : `Prospect froid`, `Diagnostic programmé`, `Devis envoyé`,
  `Client actif`, `Abonné Copilote`, `Opposé à la prospection`.
- **Ne pas** passer à WhatsApp Business Platform (API) tant que vous n'avez pas
  > 50 conversations/semaine. Coût et complexité injustifiés avant.

### 2.5 — LinkedIn
- **Profil personnel** : c'est votre actif principal. Titre à changer — le titre actuel
  type « Directeur de YEBA FORMATIONS » ne dit rien à un acheteur. Version prête :

```
Je rends l'IA utile et légale dans les TPE-PME réunionnaises
| Formation · Automatisation · RGPD & IA Act | Qualiopi
```

- Section **Infos** : problème → preuve → offre → appel à l'action (structure, pas slogan).
- **Sélection (Featured)** : 1 lien diagnostic, 1 PDF « Article 4 IA Act : la checklist
  des 7 points », 1 vidéo de résultat client.
- **Page entreprise YEBA FORMATIONS** : créée depuis le profil, secteur
  `Services de formation professionnelle`, taille, localisation La Réunion. Vous vous
  y associez comme salarié pour que le logo apparaisse sur votre profil.

---

## Étape 3 — Sécurité (non négociable, 20 min)

| Mesure | Pourquoi |
|---|---|
| 2FA par **application TOTP** (pas SMS) sur Meta, IG, LinkedIn, OVH | Le SMS est vulnérable au SIM swapping |
| Gestionnaire de mots de passe **Bitwarden** ou **KeePassXC** | Souverain/open source. Jamais de mot de passe réutilisé |
| **Second administrateur** sur Business Manager et Page LinkedIn | Perte du compte sinon |
| Codes de récupération imprimés, hors ligne | Téléphone perdu = accès perdu |
| Revue trimestrielle des applications tierces connectées | Accès dormants |

*Cohérent avec votre SecNumAcadémie ANSSI : appliquez-vous ce que vous enseignez.*

---

## Étape 4 — Ce qui bloque et que vous seul pouvez lever

| Bloquant | Décision attendue de vous |
|---|---|
| Boîte `contact@yebaformations.re` | Commander le domaine + l'offre mail chez OVH (doc 05) |
| Numéro professionnel dédié WhatsApp | Seconde ligne mobile / eSIM, ou numéro fixe |
| Couleurs de marque exactes (codes hexadécimaux) | **À me transmettre** — je ne les inventerai pas |
| Logo en version carrée et version sur fond sombre | À fournir ou à produire |
| Deuxième administrateur de confiance | À désigner |

---

## Étape 5 — Répartition des rôles (ne pas faire la même chose partout)

| Réseau | Rôle | Cible | Objectif mesuré |
|---|---|---|---|
| **LinkedIn** | Autorité & prospection | Dirigeants, DRH, experts-comptables, institutions | Conversations initiées / semaine |
| **Instagram** | Notoriété locale & personnalité | Dirigeants 25-45, salariés prescripteurs | Partages en DM (signal n°1 de l'algorithme) |
| **Facebook** | Couverture locale & groupes | Dirigeants 35-60, réseaux d'entrepreneurs péi | Clics vers le diagnostic |
| **WhatsApp Business** | Conversion & fidélisation | Prospects chauds, clients, anciens stagiaires | Taux de réponse, ventes |
| **YouTube (Shorts)** | Archive & recherche | Recherche « formation IA Réunion » | Vues issues de la recherche |

> **Ne pilotez jamais sur les vues.** Trois chiffres, et trois seulement :
> **conversations initiées**, **diagnostics programmés**, **CA signé**.
> Tout le reste est du bruit qui flatte l'ego et ne paie pas les charges.

---

## Étape 6 — Groupes et communautés à rejoindre en semaine 1 (distribution empruntée)

À vérifier et candidater : CCI Réunion (formations et réseaux d'entreprises), **dispositif
« Ambassadeurs IA » de la DEETS Réunion** (7 ambassadeurs labellisés — candidatez),
clubs d'entrepreneurs locaux, groupes Facebook d'entrepreneurs réunionnais, réseaux
d'experts-comptables. **Une place d'ambassadeur institutionnel vaut plusieurs mois de Reels.**

Sources : [DEETS Réunion — Ambassadeurs IA](https://reunion.deets.gouv.fr/Ambassadeurs-IA-a-vos-cotes-pour-vous-expliquer-comment-l-IA-peut-ameliorer-les) ·
[CCI Réunion](https://reunion.cci.fr/formation/166206/ia-et-productivite-outils-et-bonnes-pratiques)

---

## ⚖️ Réflexe RGPD / IA Act sur ce document

- **RGPD.** Une page Facebook et un compte Instagram professionnels font de vous un
  **responsable conjoint du traitement avec Meta** pour les statistiques d'audience
  (CJUE, *Wirtschaftsakademie Schleswig-Holstein*, C-210/16). Conséquence concrète :
  votre politique de confidentialité doit mentionner vos pages sociales et leurs
  statistiques. À prévoir dans le doc 05.
- **RGPD.** WhatsApp Business : la synchronisation du répertoire transfère des données de
  tiers sans base légale. **Refuser l'accès aux contacts.**
- **RGPD.** Transferts vers les États-Unis (Meta, LinkedIn) : couverts par le **Data
  Privacy Framework**, adéquation du 10/07/2023, **confirmée par le Tribunal de l'UE le
  03/09/2025**, **pourvoi pendant devant la CJUE (C-703/25 P)**. Valide aujourd'hui,
  à surveiller.
- **IA Act.** Si vous publiez du contenu généré ou substantiellement modifié par IA
  (voix clonée, avatar, image générée), l'**article 50 est applicable depuis le
  2 août 2026** : marquage et information. Voir doc 06.
