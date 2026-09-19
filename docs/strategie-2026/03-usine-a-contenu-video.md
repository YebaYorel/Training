# 03 — L'usine à contenu vidéo (souveraine, 1 journée = 1 mois)

**Contrainte de conception :** vous formez ~120 jours/an. Tout système exigeant votre
présence quotidienne s'arrêtera en semaine 3. On conçoit donc pour **une seule journée de
production par mois**, produisant **16 vidéos**, soit 4 publications/semaine.

---

## 1. Le fond de la chambre : je vous déconseille le fond virtuel

Vous demandez un arrière-plan modifié. Analysons avant de trancher.

**Option A — Fond virtuel IA (détourage logiciel).**
Coût 0-25 €/mois. Mais : contours qui bavent sur les cheveux et les mains, halo lumineux,
décrochage dès que vous bougez — et surtout **effet « faux »** immédiatement perceptible.
Vous vendez la confiance et la conformité : un décor visiblement truqué travaille contre
votre promesse. De plus, la plupart des outils de détourage en ligne **envoient votre
visage à un serveur tiers hors UE** : incompatible avec votre règle de souveraineté.

**Option B — Fond vert + OBS (local).**
Détourage propre, traitement **100 % sur votre machine**, zéro transfert. Mais exige un
éclairage séparé du fond, ~2 m de recul, et un décor virtuel crédible. Réalisable, mais
c'est la solution la plus exigeante en réglage.

**Option C — Coin réel de 1,2 m (recommandée).**
Vous n'avez pas besoin de cacher votre chambre. Vous avez besoin de **1,20 m de mur**.
Un panneau, une couleur de marque, une étagère, deux objets, une plante, un éclairage.
Coût 250-400 € une fois. Résultat : vrai, chaleureux, cohérent d'une vidéo à l'autre,
zéro traitement, zéro transfert, zéro bug en tournage.

> **Décision : Option C en principal, Option B en secours** pour les plans où vous voulez
> incruster un schéma ou une capture d'écran derrière vous. Steve Jobs avait raison sur ce
> point précis : un vrai type devant un faux mur perd plus qu'il ne gagne.

**Composition du coin (achats concrets) :**
panneau ou toile tendue dans **votre couleur de marque** (à me communiquer) · une étagère
avec 3 objets seulement (un livre sur l'IA, un objet péi identifiable, une plante) · votre
**certificat Qualiopi encadré** visible en arrière-plan flou — preuve permanente sans un
mot · éclairage principal en softbox 60×60 à 45°, un petit éclairage d'appoint derrière
pour décoller la silhouette du mur.

---

## 2. Matériel — budget 600 à 900 € (une fois)

| Poste | Choix | Prix indicatif | Pourquoi |
|---|---|---|---|
| Caméra | **Votre smartphone**, objectif principal, 4K 25 ou 50 i/s | 0 € | Meilleur rapport qualité/simplicité. N'achetez pas d'appareil photo. |
| Micro | **Micro-cravate sans fil** (2 émetteurs) | 100-180 € | **Le son est 70 % de la qualité perçue.** Le poste le plus rentable. |
| Éclairage | Softbox LED 60×60 + petit panneau d'appoint | 90-160 € | Supprime les ombres et le teint verdâtre |
| Trépied | Trépied colonne + rotule smartphone | 40-80 € | Cadrage identique d'un mois à l'autre |
| Téléprompteur | Application téléprompteur locale sur tablette | 0-30 € | Divise par 3 le temps de tournage |
| Décor | Panneau + étagère + objets | 150-300 € | Voir §1 |
| Acoustique | 2 panneaux mousse + tapis + rideau | 40-80 € | Enlève l'écho de chambre |

**Ce qu'il ne faut PAS acheter :** appareil photo hybride, stabilisateur, deuxième caméra,
abonnement à un studio IA d'avatars. Vous n'en avez aucun besoin et ça ajoute du frottement.

---

## 3. La pile logicielle souveraine

| Fonction | Outil retenu | Souveraineté | Coût |
|---|---|---|---|
| Enregistrement | Application caméra du téléphone | Local | 0 € |
| Capture d'écran / démos | **OBS Studio** | Local, open source | 0 € |
| **Transcription / sous-titres** | **Whisper en local** (`faster-whisper` ou `whisper.cpp`) | **100 % local, aucun transfert** | 0 € |
| Montage vertical | **Kdenlive** (KDE, Europe) ou **Shotcut** | Local, open source | 0 € |
| Montage avancé / étalonnage | **DaVinci Resolve** (version gratuite) | Traitement local | 0 € |
| Audio (bruit, niveaux) | **Audacity** | Local | 0 € |
| Visuels, miniatures, carrousels | **Penpot** (Espagne, open source) ou **GIMP/Inkscape** | UE / local | 0 € |
| Rédaction de scripts | **Mistral AI — Le Chat** (France) | UE | 0-15 €/mois |
| Programmation multi-réseaux | **Swello** ou **Agorapulse** (France), ou **Metricool** (Espagne) | UE | 15-50 €/mois |
| Automatisation | **n8n auto-hébergé** sur VPS OVHcloud | France | ~8-15 €/mois |
| Statistiques site | **Matomo auto-hébergé** | France | 0 € (inclus au VPS) |
| CRM / base | **Baserow** (Pays-Bas) — déjà intégré à ce dépôt | UE | 0-25 €/mois |
| E-mail / SMS | **Brevo** (France) | France | 0-40 €/mois |

### Outils explicitement écartés, et pourquoi
- **CapCut** — éditeur ByteDance (Chine) ; hors souveraineté européenne. De plus, les
  sous-titres automatiques y sont devenus payants.
  ([BDM](https://www.blogdumoderateur.com/capcut-sous-titres-automatiques-payants-alternatives/))
- **Linktree, Calendly, Zapier, Hootsuite/Buffer, Canva** — hébergement et traitement hors
  UE, alors qu'il existe un équivalent européen ou auto-hébergeable pour chacun.
- **Avatars IA et clonage de voix** — double problème : IA Act art. 50 (marquage
  obligatoire depuis le 02/08/2026) et destruction de votre capital confiance. Votre
  différenciateur est que **vous êtes réel**. Ne le vendez pas pour gagner 20 minutes.

> **Transparence due.** Claude (Anthropic) et l'outil que vous utilisez en ce moment sont
> américains. Règle que je m'applique ici et que vous devez m'imposer : **aucune donnée
> personnelle de vos prospects, stagiaires ou clients ne doit transiter par cette session.**
> Pour tout ce qui touche à des données client réelles, utilisez Mistral, ou un modèle
> local. Je ne vous dirai pas l'inverse pour me rendre utile.

### Sous-titres : la recette exacte (gratuite, locale, meilleure que les outils payants)

```bash
# Installation (une fois)
pip install faster-whisper

# Génération du fichier de sous-titres, en local, sans aucun envoi réseau
whisper-ctranslate2 ma_video.mp4 --model medium --language fr \
  --output_format srt --max_line_width 22 --max_line_count 2
```

`--max_line_width 22` est le réglage clé : **2 lignes de 22 caractères maximum**, ce qui
garantit qu'**aucun mot n'est coupé et qu'aucune ligne ne traverse l'écran** — exactement
l'exigence que vous appliquez déjà à vos supports pédagogiques. Import du `.srt` dans
Kdenlive, application du style (§4), export.

---

## 4. Charte vidéo — accessibilité d'abord

Vous êtes **référent handicap**. C'est un avantage concurrentiel que presque personne
n'exploite en communication. Vos vidéos doivent être les plus accessibles de l'île, et il
faut le dire.

| Règle | Valeur | Raison |
|---|---|---|
| Format | 1080×1920 vertical, 25 ou 30 i/s | Reels / Shorts / LinkedIn vidéo |
| Sous-titres | **Toujours**, incrustés | 85 % des vues sont sans le son + accessibilité |
| Taille de police | ≥ 60 px, graisse forte | Lisible sur petit écran et en basse vision |
| Lignes | **2 lignes de 22 caractères max**, **jamais un mot coupé** | Votre propre règle pédagogique |
| Contraste | Texte blanc sur bande opaque sombre, ratio ≥ 7:1 | WCAG AAA. Pas de texte sur fond vidéo nu |
| Zone sûre | Rien dans les 250 px du haut ni les 420 px du bas | L'interface des applications masque ces zones |
| Couleur | **Jamais l'information par la couleur seule** | Daltonisme |
| Flashs | Aucun effet clignotant rapide | Épilepsie photosensible |
| Description | Transcription intégrale en commentaire épinglé | Lecteurs d'écran, référencement |

**À publier une fois, et à répéter :** *« Toutes mes vidéos sont sous-titrées et
transcrites. Formation accessible : je suis référent handicap. »* C'est un argument que
vos concurrents ne peuvent pas copier sans la compétence.

---

## 5. Les 5 piliers de contenu (rotation fixe)

| Pilier | % | Intention | Format type | Exemple de titre |
|---|---|---|---|---|
| **1. La preuve** | 30 % | Vendre | Avant/après chronométré chez un vrai client péi | « 11 h par mois rendues à ce garage de Saint-Pierre » |
| **2. Le piège légal** | 25 % | Autorité + peur utile | Vous, face caméra, 40 s | « Votre salarié utilise ChatGPT ? Vous êtes hors la loi depuis février 2025 » |
| **3. Le geste technique** | 20 % | Utilité immédiate | Capture d'écran OBS | « Trier 200 mails de fournisseurs en 4 minutes » |
| **4. Vrai / Faux** | 15 % | Portée | Punchy, 20 s | « Non, l'IA ne va pas remplacer votre comptable. Voilà ce qu'elle remplace. » |
| **5. L'humain péi** | 10 % | Confiance | Coulisses, humour, créole | « Ce que je réponds quand on me dit "mi compran pa l'IA" » |

**Le pilier 1 est celui qui fait vivre l'entreprise.** Sans autorisation écrite de vos
clients, il n'existe pas — d'où la clause obligatoire du doc 06.

---

## 6. Les accroches (hooks) — la seule seconde qui compte

Le *watch time* est le signal n°1 de l'algorithme Instagram en 2026, et **les partages en
DM pèsent 3 à 5 fois plus que les likes**. Vous ne cherchez pas l'approbation, vous cherchez
le réflexe « j'envoie ça à mon associé ». ([Sprout Social](https://sproutsocial.com/insights/instagram-algorithm/))

**Règles :** pas de bonjour. Pas de logo au début. Pas de « aujourd'hui on va parler de ».
La **première image est déjà le résultat**. Le premier mot est déjà le conflit.

**20 accroches prêtes, calibrées pour un dirigeant réunionnais :**

1. « Votre salarié a ouvert ChatGPT ce matin. Vous êtes en infraction. »
2. « J'ai chronométré. 11 heures par mois. Un seul outil. »
3. « Ce devis, il met 40 minutes à le faire. Regardez. » *(chrono à l'écran)*
4. « Non. L'IA ne remplacera pas votre comptable. Elle remplacera ça. »
5. « 35 millions d'euros d'amende. Pour une ligne oubliée. »
6. « Arrêtez de payer pour ça. C'est gratuit et c'est mieux. »
7. « Trois entreprises péi sur quatre font cette erreur avec l'IA. »
8. « On m'a dit : "l'IA, c'est pour les grosses boîtes". J'ai pris un caméra. »
9. « Votre concurrent a fait ça la semaine dernière. Vous, non. »
10. « Ce que personne ne vous dit sur ChatGPT et vos données clients. »
11. « Combien de temps vous passez sur vos plannings ? Dites-le en commentaire. »
12. « J'ai testé pendant 30 jours. Voilà ce qui marche vraiment à La Réunion. »
13. « Si vous utilisez l'IA sans ça, vous prenez un risque juridique. »
14. « Le truc le plus rentable que j'ai installé cette année coûte 0 €. »
15. « Vous avez une obligation légale depuis 19 mois et personne ne vous l'a dit. »
16. « Mi compran pa l'IA. Normal. On vous l'explique mal. »
17. « Cette entreprise de Saint-Denis a économisé un mi-temps. Sans licencier. »
18. « Deux minutes. Et vous saurez si votre entreprise est en règle. »
19. « Le piège du CPF et de l'IA : ce qu'on ne vous a pas dit. »
20. « Je vais vous montrer mon écran. C'est moins joli que ce qu'on vous vend. »

**Structure des 45 secondes :**
`0,0-1,0 s` accroche · `1-4 s` le conflit ou l'enjeu · `4-30 s` la démonstration
(**une seule idée**) · `30-40 s` la preuve chiffrée · `40-45 s` appel à l'action.

---

## 7. Les appels à l'action (rotation, jamais le même)

| Type | Formulation | Quand |
|---|---|---|
| Conversation | « Écrivez-moi **IA ACT** en commentaire, je vous envoie la checklist. » | Pilier 2 |
| Partage | « Envoyez ça à un chef d'entreprise qui utilise ChatGPT sans le savoir. » | Pilier 2 et 4 — **c'est l'action qui déclenche l'algorithme** |
| Diagnostic | « 20 minutes, gratuit, sans engagement. Lien en bio. » | Pilier 1 et 3 |
| Local | « Vous êtes de quel côté de l'île ? Je me déplace. » | Pilier 5 |
| Aucun | *(vidéo sans CTA)* | 1 vidéo sur 5 — sinon vous devenez un panneau publicitaire |

---

## 8. La journée de production mensuelle (7 h chrono)

| Créneau | Tâche | Sortie |
|---|---|---|
| J-7, 1 h | Écriture des 16 scripts (Mistral + votre relecture) | 16 scripts de 90 mots |
| **8h00-8h30** | Installation décor, lumière, son, test | Cadre validé |
| **8h30-11h00** | Tournage des 16 vidéos, téléprompteur, 2 prises max | 16 rushes |
| **11h00-11h30** | Captures d'écran OBS pour le pilier 3 | 4 démos |
| **13h30-14h00** | Transcription Whisper en local, en lot | 16 fichiers `.srt` |
| **14h00-16h30** | Montage Kdenlive : modèle + sous-titres + export | 16 MP4 verticaux |
| **16h30-17h30** | Rédaction des légendes, programmation sur 4 semaines | Mois publié |

**Ne montez jamais une vidéo isolément.** Le coût de démarrage (installer, éclairer, se
mettre en voix) est le même pour 1 que pour 16. C'est toute l'économie du système.

---

## 9. Automatisation raisonnable (n8n auto-hébergé, OVHcloud)

Trois automatisations, pas trente. Chacune supprime une corvée réelle :

1. **Commentaire déclencheur → ressource.** Quelqu'un commente « IA ACT » → n8n détecte via
   l'API → réponse automatique invitant à envoyer un message privé → envoi du PDF par Brevo
   après consentement explicite dans la conversation.
   *⚖️ RGPD : l'envoi du PDF par e-mail suppose une collecte licite de l'adresse. Le
   commentaire public n'est pas un consentement. Faites passer par un formulaire.*
2. **Nouveau prospect → Baserow.** Formulaire du site → ligne Baserow (nom, entreprise,
   besoin, source, date, base légale, origine) → relance automatique J+2 et J+9.
3. **Publication → journal.** Chaque publication est enregistrée dans Baserow avec sa date,
   son pilier, son accroche, ses vues à 48 h et **le nombre de conversations générées**.
   Sans ce tableau, vous pilotez à l'aveugle pendant un an.

**Ce qu'il ne faut PAS automatiser :** les réponses aux commentaires, les messages privés,
les remerciements. Sur un marché de 4 600 TPE-PME, la réponse personnelle **est** le produit.
Un DM automatique vous grille définitivement auprès d'un dirigeant qui se connaît un réseau.

---

## 10. Rythme réaliste et tableau de bord

- **4 publications/semaine** : 2 Reels IG (+ miroir FB), 1 vidéo LinkedIn, 1 post texte
  LinkedIn. Le mix recommandé en 2026 est de 3-4 Reels/semaine pour une entreprise, les
  Reels touchant **6,1× plus de comptes** que les posts de feed.
- **Zéro publication** pendant vos semaines de formation intensive : le stock mensuel
  couvre. C'est la raison d'être de la production en lot.

**Tableau de bord mensuel (Baserow) — 6 colonnes, pas plus :**
`publications` · `vues` · **`partages en DM`** · **`conversations initiées`** ·
**`diagnostics programmés`** · **`CA signé attribué`**.

> Si au bout de 90 jours les colonnes 4-5-6 sont à zéro pendant que la colonne 2 monte,
> **le système est un échec** et il faut changer le contenu, pas persévérer. Les vues ne
> sont pas une monnaie.

---

## ⚖️ Réflexe RGPD / IA Act sur ce document

- **IA Act art. 50 — applicable depuis le 02/08/2026.** Tout contenu synthétique (voix
  clonée, avatar, image ou vidéo générée) doit être marqué comme tel. Les sous-titres
  générés par Whisper à partir de votre propre voix ne sont pas du contenu synthétique ;
  une voix off clonée, si. Recommandation : n'en utilisez pas, et **affichez-le comme un
  engagement** — « 100 % vrai, 0 % avatar ». C'est un différenciateur.
- **IA Act art. 4** — vous êtes vous-même déployeur d'IA : votre propre niveau de maîtrise
  et celui de vos éventuels prestataires doit être assuré et **documenté**. Faites-le pour
  vous d'abord : c'est votre meilleure étude de cas.
- **RGPD** — filmer chez un client : information préalable des personnes filmées, recueil
  du consentement écrit pour l'image, **et** autorisation du dirigeant pour la publication.
  Modèle à produire (doc 06).
- **RGPD** — un commentaire public n'est pas une base de collecte. Ne constituez jamais une
  liste de diffusion à partir de commentaires ou d'abonnés.
- **Écologie** — argument à ne pas surjouer : le montage local et les modèles de
  transcription légers consomment bien moins que les générateurs vidéo en ligne. C'est
  vrai, c'est vérifiable, et c'est un point recevable en appel d'offres public.
