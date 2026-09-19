# 03 — L'usine à contenu vidéo (souveraine, 1 journée = 1 mois)

**Contrainte de conception :** vous formez ~120 jours/an. Tout système exigeant votre
présence quotidienne s'arrêtera en semaine 3. On conçoit donc pour **une seule journée de
production par mois**, produisant **16 vidéos**, soit 4 publications/semaine.

---

## 1. Décor : fond vert + OBS (décision actée le 19/09/2026)

**Votre choix : fond vert avec incrustation locale sous OBS.** C'est la seule des trois
options qui combine un arrière-plan modifiable *et* un traitement **100 % sur votre
machine** : votre visage ne quitte jamais votre ordinateur. Sur le plan de la souveraineté,
c'est la meilleure des trois. C'est aussi la plus exigeante à régler — donc on la règle
une fois, correctement, et on ne touche plus.

> J'avais recommandé le coin réel pour des raisons de crédibilité perçue. Vous avez
> tranché. **La façon de neutraliser mon objection est simple : n'incrustez pas un faux
> bureau.** Un faux mur de bureau derrière un vrai type se voit en trois secondes et
> travaille contre un discours de confiance. Utilisez le fond vert pour ce qu'il fait
> vraiment bien (§1.3).

### 1.1 — Contrainte physique à vérifier AVANT d'acheter

```
  [fond vert] ←1,5 à 2 m→ [vous] ←1,5 à 2 m→ [caméra]
  ⇒ profondeur nécessaire : 3,5 à 4 m
```

Le recul entre vous et le fond n'est pas négociable : c'est lui qui évite le **spill**
(reflet vert sur les cheveux, les épaules et la peau), le défaut qui trahit immédiatement
une incrustation amateur.

**Mesurez votre pièce aujourd'hui.** Si vous n'avez pas 3,5 m :
- **Repli A** — fond vert **rapproché** (1 m) + éclairage de contre-jour derrière vous pour
  décoller la silhouette. Fonctionne, mais exige un réglage fin et un cadrage serré.
- **Repli B** — **plan buste très serré** sur fond vert à 1 m : moins de surface de fond,
  moins de spill, résultat propre. C'est le repli que je recommande en petite pièce.
- **Repli C** — retour au coin réel de 1,20 m (doc initial). Sans honte : c'est une
  contrainte de pièce, pas un renoncement.

### 1.2 — Matériel et réglages

| Élément | Choix | Prix indicatif |
|---|---|---|
| Fond vert | Toile **tendue** sur cadre (pas de tissu pendu : les plis créent des ombres impossibles à incruster) — 2×2 m minimum, ou panneau pliable | 60-120 € |
| Éclairage du **fond** | **2 panneaux LED dédiés au fond**, à 45° de chaque côté, réglés identiques | 70-140 € |
| Éclairage du **sujet** | Softbox principale 60×60 à 45° + **contre-jour derrière vous** | 90-160 € |
| Total supplémentaire vs coin réel | | **+150 à 250 €** |

**Le principe que tout le monde rate : le fond et vous êtes éclairés séparément.** Un fond
vert éclairé par la même lumière que vous donne un vert irrégulier, donc une incrustation
qui bave. Deux sources pour le fond, deux pour vous.

**Réglages OBS — filtre « Incrustation par chrominance » :**

| Paramètre | Valeur de départ | À ajuster si |
|---|---|---|
| Type de couleur clé | Vert | — |
| Similarité | **380-420** | Trop bas : trous dans le fond. Trop haut : vous disparaissez |
| Lissage | **75-85** | Contours durs ou tremblants |
| **Réduction du déversement** (spill) | **95-110** | **Liseré vert sur les cheveux et les épaules** |
| Luminosité / Contraste | 0 | Ne toucher qu'en dernier recours |

**Trois règles de tournage :**
1. **Ne portez jamais de vert** — ni turquoise, ni kaki, ni motif vert. Vous deviendriez
   transparent par endroits. Testez chaque tenue **avant** la journée de tournage.
2. **Verrouillez le préréglage OBS** une fois réglé : même position de caméra, mêmes
   marques au sol, mêmes lumières. Vous retrouvez le réglage chaque mois sans refaire
   30 minutes de calage.
3. **Enregistrez déjà incrusté dans OBS** (pas d'incrustation en post-production) : pour
   16 vidéos en une journée, c'est ce qui vous fait gagner deux heures de montage.

### 1.3 — Ce que vous mettez derrière (le point décisif)

**N'incrustez pas un faux décor de bureau.** Le fond vert vous donne quelque chose de bien
plus puissant : **la capacité de mettre l'information derrière vous.**

| Usage | Effet | Pilier concerné |
|---|---|---|
| **Capture d'écran plein cadre** de l'outil dont vous parlez | Vous démontrez au lieu de raconter | Pilier 3 |
| **Schéma ou chronologie** (ex. le calendrier de l'IA Act) | Vous devenez le professeur devant son tableau | Pilier 2 |
| **Chiffre géant** (« 11 h/mois ») qui apparaît au bon moment | Mémorisation immédiate | Pilier 1 |
| **Aplat uni à vos couleurs de marque** + votre logo discret | Fond par défaut, sobre, cohérent | Tous |
| **Photo réelle de La Réunion prise par vous** | Ancrage local, jamais une banque d'images | Pilier 5 |

> **Règle de marque : jamais de faux bureau, jamais de photo de banque d'images.**
> Aplat de marque par défaut, contenu pédagogique quand vous démontrez, photo réelle du
> territoire quand vous parlez du péi. Ce sont les trois seuls fonds autorisés.

**Et un élément à garder dans le cadre malgré le fond vert :** votre **certificat Qualiopi**
n'est plus dans le décor. Compensez par un **bandeau permanent discret en bas de cadre** :
`YEBA FORMATIONS · Qualiopi · NDA 04973676397`. Preuve permanente, sans un mot, et cohérent
sur les 16 vidéos.

---

## 2. Matériel — budget 750 à 1 150 € (une fois)

| Poste | Choix | Prix indicatif | Pourquoi |
|---|---|---|---|
| Caméra | **Votre smartphone** en source OBS (via câble USB ou application de caméra virtuelle) | 0 € | Meilleur rapport qualité/simplicité. N'achetez pas d'appareil photo. |
| Micro | **Micro-cravate sans fil** (2 émetteurs) | 100-180 € | **Le son est 70 % de la qualité perçue.** Le poste le plus rentable de la liste. |
| Fond vert | Toile tendue sur cadre, 2×2 m minimum | 60-120 € | Les plis sont l'ennemi n°1 de l'incrustation |
| Éclairage fond | 2 panneaux LED dédiés | 70-140 € | **Indispensable** : sans lui, l'incrustation bave |
| Éclairage sujet | Softbox 60×60 + contre-jour | 90-160 € | Décolle votre silhouette du fond |
| Trépied | Trépied colonne + rotule smartphone | 40-80 € | Cadrage identique d'un mois à l'autre |
| Téléprompteur | Application locale sur tablette | 0-30 € | Divise par 3 le temps de tournage |
| Acoustique | 2 panneaux mousse + tapis + rideau | 40-80 € | Enlève l'écho de chambre |
| Ordinateur | **Le vôtre** — vérifier qu'il tient l'incrustation en temps réel | 0 € | À tester avant d'acheter le reste |

**Ce qu'il ne faut PAS acheter :** appareil photo hybride, stabilisateur, deuxième caméra,
abonnement à un studio IA d'avatars. Aucun besoin, et chacun ajoute du frottement.

> ⚠️ **Test à faire en premier, avant tout achat :** installez OBS, mettez un drap vert ou
> un mur uni, et vérifiez que **votre machine tient l'incrustation en direct sans saccade**.
> Si elle rame, il faut enregistrer brut et incruster dans Kdenlive en post-production —
> ce qui change complètement l'organisation de la journée de tournage (§8).

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
| **8h00-8h45** | Installation fond vert, 2 lumières fond + 2 sujet, son, **chargement du préréglage OBS**, test d'incrustation sur 20 s | Cadre et clé validés |
| **8h45-11h15** | Tournage des 16 vidéos **déjà incrustées dans OBS**, téléprompteur, 2 prises max | 16 rushes prêts à monter |
| **11h15-11h45** | Captures d'écran OBS pour le pilier 3 | 4 démos |
| **13h30-14h00** | Transcription Whisper en local, en lot | 16 fichiers `.srt` |
| **14h00-16h30** | Montage Kdenlive : modèle + sous-titres + export | 16 MP4 verticaux |
| **16h30-17h30** | Rédaction des légendes, programmation sur 4 semaines | Mois publié |

> ⚠️ **Si votre machine ne tient pas l'incrustation en direct** (§2) : tournez sur fond vert brut, et ajoutez **1 h 30 d'incrustation dans Kdenlive** en début d'après-midi. La journée passe alors à 8 h 30. Testez-le **avant** de planifier la première journée.

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
