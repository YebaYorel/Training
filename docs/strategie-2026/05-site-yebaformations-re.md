# 05 — www.yebaformations.re : architecture, conformité, référencement

**Principe directeur :** votre site n'est pas une plaquette. C'est **l'unique endroit
souverain où une intention se transforme en rendez-vous**. Les réseaux sont loués ; le
site est possédé.

Et il a une seconde fonction, décisive : **il est votre première démonstration.** Un
consultant en IA et en conformité dont le site est lent, non accessible et bardé de
traceurs américains n'a pas besoin d'être critiqué — il s'est disqualifié seul.

---

## 1. Commande OVHcloud — ordre exact

1. **Domaine `yebaformations.re`** — le `.re` est géré par l'AFNIC ; l'enregistrement est
   soumis à conditions d'éligibilité (lien avec le territoire). Vous les remplissez
   (SIRET actif à La Réunion). *Tarif à vérifier directement sur le site OVHcloud : je ne
   l'invente pas.*
   - Réserver aussi **`yebaformations.fr`** et **`yeba-formations.re`** en redirection :
     protection de marque et fautes de frappe. Coût marginal, valeur défensive élevée.
2. **DNSSEC : activer.** Deux clics dans l'espace client OVH. Protège contre le
   détournement de résolution DNS. Vous vendez la sécurité : montrez-la.
3. **Boîtes e-mail** — `contact@`, `aurelien@`, `facturation@`.
   **À créer en premier**, tout le reste en dépend (doc 02).
4. **SPF, DKIM, DMARC** — configurer les trois. Sans eux, vos e-mails de prospection
   finissent en indésirables et votre domaine peut être usurpé. Commencez DMARC en
   `p=none`, passez à `p=quarantine` après 4 semaines d'observation.
5. **Hébergement** — voir §2.
6. **VPS OVHcloud** (le plus petit) pour **n8n** + **Matomo** auto-hébergés.

---

## 2. WordPress chez OVHcloud (décision actée le 19/09/2026)

**Votre choix : WordPress.** Raison retenue : **l'autonomie éditoriale**. Vous devez pouvoir
changer un tarif un dimanche soir depuis votre téléphone, sans dépendre de moi ni d'un
développeur. Sur une entreprise solo, c'est un argument qui l'emporte sur la performance
brute — j'avais sous-pondéré ce point.

**Ce que vous perdez, dit franchement :** une surface d'attaque plus large, une routine de
mises à jour hebdomadaire, et une vigilance permanente sur les scripts tiers. **Ce n'est
pas grave à condition de tenir la discipline ci-dessous.** Un WordPress bien tenu vaut
mieux qu'un site statique qu'on n'ose plus modifier.

### 2.1 — Installation

1. **Hébergement OVHcloud** — prendre une offre **avec accès SSH, PHP 8.3+ et sauvegardes
   automatiques** (les offres d'entrée de gamme ne les ont pas toutes). *Tarifs à vérifier
   directement chez OVHcloud : je ne les invente pas.*
2. **Module WordPress en 1 clic** depuis l'espace client OVH.
3. **Identifiant administrateur : jamais `admin`, jamais `yeba`, jamais votre prénom.**
4. **URL de connexion modifiée** (plugin dédié) : élimine 95 % des attaques automatisées.
5. **2FA sur le compte administrateur.** Obligatoire — vous vendez la sécurité.
6. **PHP 8.3+, HTTPS forcé, HSTS activé.**

### 2.2 — Thème : un thème de blocs natif, jamais un constructeur de pages

| ❌ À éviter | ✅ À choisir |
|---|---|
| Elementor, Divi, WPBakery | **Thème de blocs natif** (Twenty Twenty-Five) ou **GeneratePress** / **Kadence** |
| Thèmes « multi-usages » à 60 démos | Thème léger, `accessibility-ready`, < 100 ko de CSS |

**Pourquoi pas de constructeur de pages :** ils ajoutent 300 à 800 ko de code, dégradent
l'accessibilité (structure de titres cassée, focus clavier perdu) et vous enferment. L'éditeur
de site natif de WordPress suffit largement pour vos 9 pages, et il est plus simple à
prendre en main.

### 2.3 — Extensions : la liste courte, et elle est presque entièrement française

> **Règle : moins de 12 extensions actives.** Chaque extension est une porte d'entrée
> potentielle et un risque de casse à la mise à jour.

| Besoin | Extension | Éditeur | Pourquoi ce choix |
|---|---|---|---|
| Référencement | **SEOPress** | 🇫🇷 France (Rennes) | Équivalent Yoast, sans traceur, éditeur français |
| Sécurité | **SecuPress** | 🇫🇷 France | Audit, pare-feu, blocage des attaques par force brute |
| Performance | **WP Rocket** | 🇫🇷 France (WP Media) | Le meilleur cache du marché, éditeur français |
| Images | **Imagify** | 🇫🇷 France (WP Media) | Compression + WebP |
| Formulaires + e-mail | **Brevo pour WordPress** | 🇫🇷 France | Formulaires **et** envois, un seul sous-traitant, hébergé en France |
| Statistiques | **Matomo** (connecté à votre instance auto-hébergée) | 🇪🇺 / auto-hébergé | Pas de transfert hors UE |
| **Polices en local** | **OMGF** (ou désactivation manuelle) | — | **Critique — voir 2.4** |
| Sauvegardes | **UpdraftPlus** + sauvegardes OVH | — | Double filet |
| Rendez-vous | **Cal.com** auto-hébergé, intégré par iframe, ou module Brevo | 🇪🇺 | Pas Calendly |

**Extensions à bannir absolument :**
- **Les « overlays d'accessibilité »** (AccessiBe, UserWay et assimilés). Ils ne rendent pas
  un site accessible, dégradent souvent l'expérience des utilisateurs de lecteurs d'écran,
  et ont fait l'objet de contentieux. **Pour un référent handicap, en installer un serait
  une faute professionnelle visible.** L'accessibilité se fait dans le thème et le contenu,
  pas avec une surcouche.
- Google Analytics, Google Site Kit, pixel Meta, Jetpack, Hotjar : transferts et traceurs.

### 2.4 — Les 5 fuites que WordPress crée par défaut, et qu'il faut fermer

C'est le vrai travail de conformité d'un WordPress, et presque personne ne le fait :

| Fuite par défaut | Ce qui part | Correction |
|---|---|---|
| **Google Fonts** chargées à distance par le thème | **L'adresse IP de chaque visiteur part vers Google (USA)** — motif de condamnations en Europe | **Héberger les polices en local** (OMGF ou intégration manuelle) |
| **Gravatar** sur les commentaires | IP + empreinte de l'e-mail vers Automattic (USA) | Désactiver les commentaires (vous n'en avez pas besoin) |
| **Émojis WordPress** | Requête vers `s.w.org` | Désactivé par WP Rocket ou une ligne dans `functions.php` |
| **`oEmbed`** (YouTube, Twitter intégrés) | Traceurs tiers dès le chargement | Héberger vos vidéos ou utiliser une intégration à clic différé |
| **XML-RPC** et énumération des utilisateurs | Surface d'attaque | Désactivés par SecuPress |

> **Le jour où ces 5 points sont fermés, vous pouvez écrire en page d'accueil :**
> *« Ce site ne transmet aucune donnée hors de l'Union européenne. »* — et c'est vrai,
> vérifiable par n'importe qui avec l'inspecteur réseau de son navigateur. **Aucun de vos
> concurrents locaux ne peut l'écrire.** C'est un argument de vente, pas une case à cocher.

### 2.5 — Routine de maintenance (30 min/mois, non négociable)

| Fréquence | Action |
|---|---|
| **Automatique** | Mises à jour mineures de WordPress et correctifs de sécurité |
| **Hebdomadaire** | Vérifier les mises à jour d'extensions, les appliquer après sauvegarde |
| **Mensuel** | Audit SecuPress · test de restauration de sauvegarde · vérification qu'aucun script tiers n'est apparu |
| **Trimestriel** | Test d'accessibilité au clavier · test de vitesse **depuis La Réunion** · revue des comptes utilisateurs |

**Test de non-régression à faire après chaque mise à jour majeure :** ouvrir la page
`/ia-act-article-4`, remplir le formulaire, vérifier l'arrivée dans Baserow. Deux minutes.
Un formulaire cassé silencieusement pendant trois semaines, c'est trois semaines de
prospects perdus sans le savoir.

---

## 3. Arborescence (9 pages, pas 30)

```
/                          Accueil — la promesse + la preuve + le diagnostic
/ia-act-article-4          ⭐ PAGE PIVOT — l'obligation, expliquée, + autodiagnostic
/formations                Catalogue : IA opérationnelle, conformité, vente/management
/implementation            Sprints IA : méthode, exemples, tarif à partir de
/gouvernance               Diagnostic RGPD & IA Act (jamais le mot « audit »)
/resultats                 Cas clients chiffrés (le nerf de la guerre)
/a-propos                  Vous. Parcours, certifications, pourquoi La Réunion
/contact                   Formulaire + prise de rendez-vous + WhatsApp
/liens                     Votre page de liens (remplace Linktree)

/mentions-legales   /confidentialite   /cgv   /accessibilite   /handicap
```

**`/ia-act-article-4` est la page la plus importante du site.** C'est la seule sur laquelle
vous pouvez être premier sur l'île à court terme. Elle doit contenir : l'obligation citée
avec ses dates exactes, ce qu'elle implique concrètement, **un autodiagnostic en 7 questions**
qui débouche sur une capture de contact, et le Pack Essentiel à 1 490 €.

---

## 4. Le moteur de conversion

**Une seule action principale par page.** Le bouton est toujours le même :
**« Diagnostic gratuit — 20 minutes »**.

- **Prise de rendez-vous** : **Cal.com auto-hébergé** sur votre VPS OVHcloud, ou le module
  de rendez-vous de **Brevo** (France). **Pas Calendly** (États-Unis, traceurs).
- **Formulaire** : 4 champs maximum — prénom, entreprise, e-mail professionnel, besoin en
  une phrase. Chaque champ supplémentaire coûte des conversions.
- **Aimant à contacts** : *« Article 4 de l'IA Act — la checklist des 7 points »*, PDF de
  2 pages, accessible (balisé, contrasté, lisible par lecteur d'écran). C'est le document
  que les gens s'envoient entre dirigeants.
- **Cas clients** : format imposé — `Secteur · Problème · Ce qui a été fait · Temps gagné
  mesuré · Verbatim du dirigeant`. **Sans chiffre, ce n'est pas un cas client, c'est une
  publicité.**

---

## 5. Référencement local : le vrai gisement

Le volume de recherche est faible à La Réunion, mais la **concurrence est presque nulle** et
l'**intention d'achat est maximale**. Quelqu'un qui tape « formation IA Réunion » n'est pas
curieux : il cherche un prestataire.

**Expressions à viser** (une page ou un article dédié par expression) :
`formation intelligence artificielle La Réunion` · `formation IA entreprise 974` ·
`IA Act article 4 formation obligatoire` · `mise en conformité RGPD Réunion` ·
`automatisation TPE Réunion` · `formation ChatGPT entreprise Réunion` ·
`organisme formation Qualiopi IA Réunion` · `consultant IA 974`.

**Éléments techniques indispensables :**
- **Données structurées** `Organization` + `LocalBusiness` + `Course` (JSON-LD) : permet
  l'affichage enrichi des formations.
- **Fiche d'établissement Google** : à créer et vérifier. Inévitable pour le local, même
  si c'est un acteur américain — **on n'y met aucune donnée client, seulement vos
  informations publiques d'entreprise.**
- **Annuaires** : Pages Jaunes, annuaires d'organismes de formation, CCI Réunion,
  répertoire des organismes certifiés Qualiopi. Chaque citation cohérente
  (**même nom, même adresse, même téléphone partout**) renforce le local.
- **Visibilité dans les moteurs de réponse IA** : ChatGPT, Perplexity, Mistral et Gemini
  citent des sources. Pour être cité quand on demande « qui forme à l'IA à La Réunion »,
  il faut : des pages factuelles bien structurées, des dates, des chiffres, un `llms.txt`
  à la racine, et des mentions sur des sites tiers crédibles (presse locale, CCI,
  annuaires). **C'est le référencement des 3 prochaines années, et personne ne le fait
  encore sur l'île.** Avantage disponible immédiatement.

---

## 6. Accessibilité — obligation ET argument commercial

Vous êtes **référent handicap en organisme de formation**. Un site inaccessible serait
une contradiction exploitable par n'importe quel concurrent.

- Référentiel : **RGAA / WCAG 2.1 niveau AA** au minimum.
- Contraste ≥ 4,5:1 pour le texte courant, ≥ 7:1 recommandé pour vous.
- Navigation complète au clavier, focus visible, ordre de tabulation logique.
- Textes alternatifs sur toutes les images, hiérarchie de titres H1→H2→H3 respectée.
- Vidéos : sous-titres **et** transcription textuelle sur la page.
- Taille de police de base **18 px minimum**, redimensionnement à 200 % sans perte.
- **Page `/accessibilite`** : déclaration de conformité + moyen de signaler un problème.
- **Page `/handicap`** : votre procédure d'accueil des personnes en situation de handicap,
  vos coordonnées de référent handicap, vos partenaires (Agefiph, Cap Emploi).
  **C'est exigé côté Qualiopi et c'est un différenciateur commercial réel.**

> ⚖️ **Point à faire vérifier** : la **directive (UE) 2019/882** sur l'accessibilité des
> produits et services, transposée en France, impose des obligations d'accessibilité à
> certains services numériques destinés aux consommateurs depuis le 28 juin 2025.
> L'applicabilité à votre cas dépend de votre chiffre d'affaires, de votre effectif et du
> caractère B2C ou B2B de vos ventes en ligne. **Je ne tranche pas : à faire confirmer**
> (doc 08). Dans tous les cas, viser WCAG AA vous met à l'abri.

---

## 7. Conformité du site — checklist opposable

| Élément | Exigence | Statut |
|---|---|---|
| Mentions légales | Dénomination, SIRET **814 622 262 00032**, adresse, directeur de publication, hébergeur (OVH SAS, 2 rue Kellermann, 59100 Roubaix) | À rédiger |
| Mentions organisme de formation | **NDA 04973676397** + « cet enregistrement ne vaut pas agrément de l'État » (mention légale obligatoire) | À rédiger |
| Qualiopi | Logo + **mention des catégories d'actions certifiées** (usage encadré) | À rédiger |
| CGV / CGU | Délais, rétractation, modalités de report/annulation, règlement intérieur | À rédiger |
| Politique de confidentialité | Finalités, bases légales, durées, destinataires, droits, **pages sociales incluses** | À rédiger |
| Registre des traitements | Obligatoire (art. 30 RGPD) — **prospects, stagiaires, candidatures, site** | À créer **[Baserow]** |
| Durée de conservation prospects | **3 ans après le dernier contact** (recommandation CNIL) | À paramétrer |
| Statistiques | **Matomo auto-hébergé**, configuré selon les critères d'exemption CNIL | À installer |
| **Bandeau cookies** | **Aucun** — si Matomo est exempté et qu'il n'y a **aucun traceur tiers** | Objectif |
| Pixel Meta / Google Analytics | **Non installés** | Décision ferme |
| Formulaire | Mention d'information + case de consentement **non pré-cochée** pour la newsletter | À intégrer |
| HTTPS | Certificat SSL activé chez OVH | À activer |
| Sauvegardes | Dépôt Git + sauvegarde OVH | À configurer |

**Le pari « zéro bandeau cookies » est une décision commerciale, pas seulement juridique.**
Un site de conseil en conformité qui n'a pas besoin de vous harceler avec un bandeau est
l'argument de vente le plus élégant que vous puissiez avoir. Il suffit de le dire en une
ligne sur la page confidentialité : *« Ce site ne dépose aucun traceur publicitaire et ne
transmet aucune donnée hors de l'Union européenne. »*

---

## 8. Ce que la plupart oublient (et qui fait la différence)

1. **Page `/resultats` avec de vrais chiffres** — sans autorisation écrite signée, elle
   reste vide. C'est pourquoi la clause du doc 06 est prioritaire.
2. **Le PDF checklist en version accessible** — balisé, pas une image scannée.
3. **Une vraie adresse et un vrai téléphone visibles** — sur un marché insulaire, l'absence
   d'adresse physique tue la confiance.
4. **Une page `/liens`** qui remplace Linktree : vous récupérez vos statistiques de clics
   au lieu de les offrir.
5. **Temps de chargement < 1,5 s** depuis La Réunion. Testez depuis l'île, pas depuis un
   outil hébergé en Europe — la latence océan Indien est réelle.
6. **Un flux RSS** — c'est ce qui permet aux agrégateurs et aux moteurs de réponse IA de
   suivre vos publications.
7. **Le formulaire qui envoie une réponse en moins de 5 minutes.** Le taux de conversion
   d'un lead recontacté en 5 minutes est sans commune mesure avec celui d'un lead recontacté
   le lendemain. Automatisation n8n prioritaire.
8. **Version créole d'une page d'accueil ?** — à débattre. Fort signal d'appartenance,
   mais risque d'être perçu comme opportuniste s'il est mal fait. **À trancher par vous.**

---

## 9. Plan de réalisation

| Étape | Contenu | Délai |
|---|---|---|
| 1 | Domaine + DNS + DNSSEC + boîtes mail + SPF/DKIM/DMARC | J+2 |
| 2 | Installation WordPress, thème de blocs, charte (vos couleurs), fermeture des 5 fuites (§2.4) | J+7 |
| 3 | Pages `/`, `/ia-act-article-4`, `/contact` + autodiagnostic | J+14 |
| 4 | Pages restantes + pages légales + Matomo + Cal.com | J+21 |
| 5 | Données structurées, `llms.txt`, fiche Google, annuaires | J+28 |
| 6 | Cas clients au fil des autorisations signées | continu |

> **Ce que je peux vous préparer ici, prêt à coller dans WordPress :** la charte CSS
> (une fois vos couleurs connues), les textes complets des 9 pages, les 5 pages légales,
> le code de fermeture des 5 fuites du §2.4, le script de l'autodiagnostic en 7 questions,
> le PDF checklist accessible et la configuration n8n. **Vous gardez la main sur
> l'éditeur : je fournis le contenu et le code, vous publiez.**
> Il me manque : **vos codes couleurs hexadécimaux**, votre **logo**, votre **adresse
> postale professionnelle** et votre **téléphone professionnel**.

---

## ⚖️ Réflexe RGPD / IA Act sur ce document

- **RGPD** — un formulaire de contact est un traitement : finalité, base légale (mesures
  précontractuelles ou intérêt légitime), durée (3 ans après dernier contact), information
  au moment de la collecte, inscription au registre art. 30.
- **RGPD** — Matomo auto-hébergé et correctement configuré peut relever de l'exemption de
  consentement de la CNIL : pas de bandeau. **Conditions à respecter strictement**
  (finalité limitée à la mesure d'audience, pas de recoupement, durée limitée, IP
  anonymisée). Vérifiez la configuration, ne présumez pas l'exemption.
- **RGPD** — hébergement OVHcloud en France : données au repos dans l'UE. Aucun transfert
  hors UE si vous n'ajoutez aucun script tiers. **La discipline, c'est de ne jamais en
  ajouter « juste un ».**
- **RGPD** — si vous créez une fiche d'établissement Google : n'y publiez que des
  informations d'entreprise, jamais de données de clients, et modérez les avis sans y
  répondre avec des informations personnelles.
- **IA Act art. 50** — si vous installez un agent conversationnel sur le site, il doit
  informer l'utilisateur qu'il s'adresse à une IA. **Obligation applicable depuis le
  02/08/2026.** Recommandation : pas de chatbot en phase 1. Votre avantage, c'est de
  répondre vous-même.
- **IA Act** — si vous publiez sur le site des visuels générés par IA, marquez-les.
