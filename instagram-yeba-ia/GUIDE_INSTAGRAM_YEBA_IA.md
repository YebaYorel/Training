# YEBA IA — Kit Instagram complet

> Compte : **YEBA IA**, créé par YEBA FORMATIONS (La Réunion, 974).
> Thèmes : IA · formation pour adultes · RGPD · cybersécurité · IA Act.
> Contenu du kit : ce guide, les visuels dans `visuels/`, et les scripts qui les régénèrent dans `src/`.

---

## 0. Le raisonnement, étape par étape

**Contraintes analysées**
1. **Cible** : dirigeants de TPE-PME réunionnaises (plus de 80 % du tissu local d'après l'INSEE, chiffre que vous m'avez donné) et leurs salariés. Ce sont des gens pressés et pas techniciens : ils ont peur des amendes, mais aussi de « rater le train de l'IA ».
2. **Objectif** : générer des demandes de formation (intra et inter) et d'audit, pas seulement des « likes ».
3. **Sujets arides** (RGPD, IA Act) → il faut un format **mythe / vérité, quiz, réel très court**. Les longs textes juridiques ne marchent pas.
4. **Accessibilité** (vous êtes Référent handicap) : texte gros, contraste fort, sous-titres incrustés, texte alternatif. Aucune ligne décorative ne passe sous un mot.
5. **Crédibilité** : chaque affirmation juridique est **sourcée** sur le visuel. Vos concurrents ne le font pas, c'est un avantage.
6. **Souveraineté** : Instagram appartient à Meta (USA). On ne peut pas l'éviter, mais on **n'y fait transiter aucune donnée client**. La collecte de prospects se fait chez vous (voir §10).

**Options évaluées**

| Option | Pour | Contre | Verdict |
|---|---|---|---|
| A. Page « vitrine » corporate | Rassurante | Ennuyeuse, peu partagée | ❌ |
| B. Humour / mèmes seuls | Viral | Décrédibilise un expert conformité | ❌ |
| C. **« Expert qui vulgarise »** : mythes cassés, quiz, réels 15 s, sources visibles, touche créole | Rassure, instruit, surprend et se partage | Demande de la régularité | ✅ **Retenu** |

---

## 1. Profil (à copier-coller)

**Nom d'utilisateur**, à choisir (dites-moi celui que vous avez pris) : `@yeba.ia` · `@yeba_ia` · `@yeba.ia.974`

**Champ « Nom »** (il est indexé par la recherche Instagram, on y met donc des mots-clés) :
```
YEBA IA | IA · RGPD · Cyber 974
```

**Bio : version recommandée (134 caractères / 150 max)**
```
🤖 L'IA, le RGPD & la cyber… enfin clairs
🎓 Formations & audits TPE-PME · 974
✅ Organisme Qualiopi · Google AI
👇 Écrivez « DIAG » en DM
```

**Bio : variante créole (127 caractères)** : elle se démarque et crée une connivence locale.
```
Mi explik aou l'IA, le RGPD et la cyber 🌋
Formations & audits TPE-PME · La Réunion
Organisme Qualiopi · Google AI
👇 DM « DIAG »
```
> ⚠️ Dans la bio, écrivez « Organisme Qualiopi » et non « Formateur certifié Qualiopi » : la certification Qualiopi est délivrée à l'**organisme**, pas à la personne.

**Réglages**
- Passez en **compte professionnel**, catégorie « Éducation » ou « Service de formation ».
- Boutons : « Envoyer un e-mail » + « Réserver » (renvoie vers votre page de rendez-vous).
- Lien de bio : une page de **votre** site. Lequel avez-vous ? (question en §13)
- Photo de profil : `visuels/profil/photo_profil.png`. Le logo et « YEBA IA » restent lisibles à 110 px.

**Stories « À la une »** (`visuels/a_la_une/`, en alternance bleu/crème) :

| Fichier | Nom à afficher | Contenu à y mettre |
|---|---|---|
| moi.png | Qui suis-je | Parcours, certifications, photos terrain |
| ia.png | IA | Astuces outils, avant/après |
| rgpd.png | RGPD | Mythes, obligations, checklists |
| cyber.png | Cyber | Arnaques du moment, réflexes |
| iaact.png | IA Act | Dates, articles, FAQ |
| formations.png | Formations | Programmes, prochaines sessions, lieux |
| avis.png | Avis | Témoignages **avec accord écrit** |
| contact.png | Contact | Comment réserver un diagnostic |

---

## 2. Charte visuelle (extraite du logo)

| Élément | Valeur |
|---|---|
| Bleu YEBA | `#1B3A6B` (fond profond `#0F2344`) |
| Or YEBA | `#C9AB4C` |
| Crème | `#F7F3E8` |
| Police | **Montserrat** 700/800/900 (proche du logo, licence libre OFL) |
| Motif | Réseau de nœuds du logo, **uniquement en haut** du visuel (jamais derrière un mot) |
| Format posts | **1080×1440 (3:4)** : c'est le format de la grille Instagram depuis janvier 2025 *(annonce d'Adam Mosseri, Instagram, janv. 2025 ; à revérifier dans l'app)* |
| Format réels / stories | 1080×1920. Texte clé placé dans la zone centrale, hors des 420 px du bas et des 170 px de droite (zones couvertes par l'interface Instagram) |
| Taille du texte | Accroche ≥ 94 px, texte ≥ 44 px sur 1080 px. Contraste ≥ 4,5:1 (WCAG AA) |

La grille alterne **or / bleu / crème** en « carré latin » : aucune case n'a la même couleur que ses voisines (voir `visuels/maquette_profil.png`).

---

## 3. Les 6 piliers éditoriaux

| Pilier | Part | Format roi | Objectif |
|---|---|---|---|
| 🤖 IA pratique (outils, prompts, gains de temps) | 30 % | Réel démo écran | Surprendre, attirer |
| 🛡️ RGPD | 15 % | Mythe / vérité | Rassurer, faire peur « utile » |
| 🔐 Cybersécurité | 15 % | Réel « arnaque du jour » | Protéger, créer du partage |
| ⚖️ IA Act | 15 % | Carrousel sourcé | Asseoir l'expertise |
| 🎓 Formation adulte (neurosciences, pédagogie) | 10 % | Mythe cassé | Se démarquer des concurrents |
| 🌋 Coulisses 974 & preuve sociale | 15 % | Photo / réel face caméra | Créer la confiance |

**Règle des 4 C** pour chaque post : **C**apter (accroche) → **C**larifier (1 idée) → **C**rédibiliser (source) → **C**onvertir (appel à l'action).

---

## 4. Les 9 publications de lancement (visuels prêts)

Publiez-les **dans l'ordre 1 → 9**, idéalement sur 2 semaines, pour que la grille s'affiche comme sur la maquette (le plus récent apparaît en haut à gauche).

### P1 · Manifeste · `posts/post01_manifeste.png`
**Légende :**
> L'IA ne va pas vous remplacer.
> Quelqu'un qui sait s'en servir… peut-être. 👀
>
> Bienvenue sur YEBA IA. Ici, chaque semaine :
> 🤖 des astuces IA qui font gagner des heures
> 🛡️ le RGPD sans jargon
> 🔐 les arnaques du moment, décryptées
> ⚖️ l'IA Act expliqué aux TPE-PME
>
> Le tout depuis La Réunion, pour les entreprises de La Réunion. 🌋
> 👉 Abonnez-vous et activez la cloche 🔔
>
> #IA #LaRéunion #TPE #FormationPro #IntelligenceArtificielle

**Texte alternatif :** « Fond bleu nuit. Texte : L'IA ne va pas vous remplacer. Quelqu'un qui sait s'en servir, peut-être. Logo YEBA IA. »

### P2 · Qui suis-je · `posts/post02_qui_suis_je.png`
> Qui se cache derrière YEBA IA ? 👋
> Aurélien LUMEKA. Formateur en vente et management depuis 2021, j'ai vu des équipes perdre des heures sur des tâches qu'une IA fait en 30 secondes… et d'autres coller des fichiers clients dans ChatGPT sans savoir que c'est un risque RGPD.
> Mon métier aujourd'hui : **vous faire gagner du temps avec l'IA, sans mettre votre entreprise en danger.**
> 💬 Dites-moi en commentaire : vous utilisez déjà l'IA au travail ? Oui / Non / En cachette 😅
>
> *La certification qualité a été délivrée au titre de la catégorie d'action suivante : ACTIONS DE FORMATION.*

> ⚠️ **Mention Qualiopi obligatoire.** Elle est exigée par la charte d'usage de la marque Qualiopi chaque fois que vous communiquez sur la certification. **Remplacez le visuel par une vraie photo de vous** dès que possible (voir §7) : un visage multiplie la confiance.

### P3 · Réel « ChatGPT ce matin » · `reels/reel01_chatgpt.mp4` (couverture `reel01_couverture.png`)
> Vous avez collé quoi dans ChatGPT ce matin ? 😬
> 1️⃣ Un fichier clients → données personnelles = **RGPD**
> 2️⃣ Un contrat confidentiel → secret des affaires exposé
> 3️⃣ Une réponse copiée sans vérifier → l'IA peut inventer
> La solution, ce n'est pas d'interdire l'IA. C'est de **former vos équipes**.
> 👇 Commentez « IA » et je vous envoie la checklist « 10 règles d'or de l'IA au bureau ».

🏷️ *RGPD (données personnelles envoyées à un tiers, souvent hors UE) + IA Act art. 4 (maîtrise de l'IA).*

### P4 · Carrousel IA Act (7 slides) · `carrousel_ia_act/`
> 🚨 Vos salariés utilisent l'IA ? Vous avez une obligation (et beaucoup l'ignorent).
> Depuis le 2 février 2025, l'**article 4 de l'IA Act** demande aux entreprises qui utilisent l'IA de veiller à ce que leur personnel ait un niveau suffisant de **maîtrise de l'IA**.
> Swipez 👉 pour savoir quoi faire concrètement.
> 📌 Enregistrez ce post et envoyez-le à votre dirigeant·e.
>
> Source : Règlement (UE) 2024/1689, art. 4 et 113 (EUR-Lex).

> ⚠️ **À vérifier avant publication.** Le « Digital Omnibus » proposé par la Commission européenne en novembre 2025 prévoit de modifier l'article 4 (le transformer en obligation de promotion pour les États et la Commission) et de décaler certaines échéances « haut risque ». Je ne peux pas confirmer s'il a été adopté à ce jour (sept. 2026). **Vérifiez sur eur-lex.europa.eu**, puis adaptez la slide 3 si besoin (« obligation » → « recommandation forte »). Si c'est le cas, c'est d'ailleurs un excellent sujet de réel : « L'IA Act a changé : ce qui reste obligatoire ».

### P5 · Réel phishing · `reels/reel03_phishing.mp4`
> Ce mail vient vraiment de votre banque ? 🎣
> 3 indices en 10 secondes : l'urgence, l'expéditeur, le lien.
> Au moindre doute → 17cyber.gouv.fr ou cybermalveillance.gouv.fr
> 🔁 Partagez à la personne qui gère les mails dans votre entreprise.

🏷️ *Cybersécurité ; RGPD si le piratage expose des données (violation à notifier à la CNIL sous 72 h, art. 33 RGPD).*

### P6 · Mythe RGPD · `posts/post04_rgpd_mythe.png`
> « Le RGPD, c'est pour les grosses boîtes. » ❌ FAUX.
> Le RGPD s'applique dès que vous traitez des données personnelles : un fichier clients, un agenda de RDV, des CV reçus… Même sur Excel. Même à 2 salariés.
> Ce qui change pour une TPE : certaines obligations sont allégées (registre simplifié dans certains cas), **mais pas le principe**.
> 💬 Vrai ou faux suivant ? Proposez-moi une idée reçue en commentaire !
>
> Source : RGPD, art. 2, 4 et 30 §5.

### P7 · Mythe pédagogique · `posts/post05_pyramide_mythe.png`
> « On retient 10 % de ce qu'on lit, 90 % de ce qu'on fait. » Vous l'avez déjà vu en formation ? 🙋
> C'est un **mythe** : ces pourcentages n'ont jamais été démontrés scientifiquement.
> Ce qui marche vraiment pour les adultes : **la récupération active** (se tester), **l'espacement** (revoir à J+1, J+7, J+30) et **la mise en situation réelle**.
> C'est ce qu'on applique dans chaque formation YEBA. 🎯
>
> Source : K. Letrud, « A rebuttal of NTL Institute's learning pyramid », *Education*, 2012.

> 💡 Ce post vise aussi **les responsables formation et RH**, vos acheteurs directs.

### P8 · Réel IA Act dates · `reels/reel02_ia_act.mp4`
> 3 dates que votre entreprise doit connaître ⚖️
> 📅 1er août 2024 : entrée en vigueur
> 📅 2 février 2025 : pratiques interdites + maîtrise de l'IA
> 📅 2 août 2026 : la majorité des règles, dont la transparence des contenus générés par IA
> 👉 DM « IA ACT » pour un point rapide sur votre situation.

(Même vérification « Omnibus » que pour P4.)

### P9 · Appel à l'action · `posts/post09_cta_diag.png`
> Votre entreprise est-elle prête pour l'IA ? 🤔
> En 30 minutes, on regarde ensemble : vos outils, vos risques RGPD, vos obligations IA Act, vos gains de temps possibles.
> ✉️ Écrivez « DIAG » en message privé.

> ❓ **À valider par vous** : ce diagnostic est-il gratuit, payant, en visio ou en présentiel ? Je n'ai rien inventé dans le visuel ; complétez la légende.

**Hashtags** : 3 à 5 maximum par post (Instagram réduit l'intérêt des longues listes ; vérifiez la limite en vigueur dans l'app). Écrivez-les en CamelCase pour que les lecteurs d'écran les prononcent bien : `#IntelligenceArtificielle #IaAct #RGPD #CyberSécurité #LaRéunion #Reunion974 #TPE #PME #FormationPro #974`.

---

## 5. 15 scripts de réels (3 déjà montés + 12 à tourner)

Format : **accroche 0-2 s** → 3 temps → appel à l'action. Durée de 12 à 25 s. **Sous-titres toujours incrustés** (accessibilité + 80 % des vues se font sans le son).

| # | Accroche (0-2 s) | Déroulé | Appel à l'action | Pilier |
|---|---|---|---|---|
| 1 ✅ | « STOP. Vous avez collé quoi dans ChatGPT ce matin ? » | 3 erreurs : fichier clients / contrat / réponse non vérifiée | Commentez « IA » | IA + RGPD |
| 2 ✅ | « Votre entreprise utilise l'IA ? L'IA Act vous concerne. » | 3 dates | DM « IA ACT » | IA Act |
| 3 ✅ | « Ce mail vient de votre banque ? » | 3 indices | DM « CYBER » | Cyber |
| 4 | « J'ai fait en 4 minutes ce qui prenait 2 heures à ma cliente. » | Écran : devis/compte rendu généré par IA. Avant/après chronomètre | « Vous voulez la méthode ? Commentez TEMPS » | IA |
| 5 | « Ce salarié vient de coûter X € à son patron… » *(cas réel sanctionné par la CNIL, à sourcer)* | Récit + la règle enfreinte | Enregistrez | RGPD |
| 6 | « Kossa i lé l'IA ? » 🌋 | Explication en créole, 20 s, avec un rougail en fond 😄 | Partagez à un gramoune | IA / 974 |
| 7 | « Votre mot de passe se trouve en 1 seconde si… » | 3 règles + gestionnaire (Bitwarden, KeePass) | DM « CYBER » | Cyber |
| 8 | « L'IA a inventé une loi. Et l'avocat l'a citée au tribunal. » | Affaire *Mata v. Avianca* (USA, 2023) → leçon : vérifier | Commentez VÉRIF | IA |
| 9 | « Vrai ou faux : je peux filmer mes salariés en continu ? » | Réponse CNIL : non, sauf cas précis | Quiz en story | RGPD |
| 10 | « Pourquoi vos salariés oublient 70 %… » ❌ *piège* → « En fait, ce chiffre est inventé. » | Retournement de situation, puis méthode par espacement | Suivez pour d'autres mythes | Formation |
| 11 | « Le deepfake de votre patron vous demande un virement. » | L'arnaque au président 2.0 + procédure de double validation | Partagez à la compta | Cyber + IA Act art. 50 |
| 12 | « 3 IA européennes que vos concurrents ne connaissent pas » | Mistral Le Chat, DeepL, Infomaniak Euria *(à tester et vérifier avant)* | Enregistrez | IA + souveraineté |
| 13 | « Ce que je vois dans 9 audits RGPD sur 10… » *(uniquement si c'est vrai dans vos audits)* | 3 manques fréquents | DM « DIAG » | RGPD |
| 14 | POV : « Le formateur arrive et dit “aujourd'hui pas de PowerPoint” » | Coulisses d'une vraie session (visages floutés sans accord) | « Tag un collègue à former » | Formation |
| 15 | « Question d'abonné : … » | Réponse face caméra en 30 s | Posez vos questions en story | Tous |

**Musique** : utilisez uniquement la bibliothèque sonore d'Instagram, qui est licenciée pour les comptes pro (« audio commercial »). Un titre du commerce ajouté hors de cette bibliothèque risque le blocage.

---

## 6. Banque de 40 accroches et 15 appels à l'action

**Accroches** (1 phrase, moins de 2 s, un seul message) :
1. « Arrêtez de faire ça avec ChatGPT. »
2. « Votre stagiaire utilise l'IA. Vous le saviez ? »
3. « Ce mail va coûter cher à votre entreprise. »
4. « 90 % des TPE font cette erreur RGPD. » *(uniquement avec une source chiffrée)*
5. « L'IA Act, en 15 secondes. Chrono. »
6. « J'ai demandé à l'IA de remplacer mon comptable. »
7. « Ne cliquez pas. »
8. « Votre fichier Excel est illégal ? »
9. « La phrase qui fait fuir vos stagiaires en formation. »
10. « Kossa i lé le RGPD ? »
11. « Personne ne vous dit ça sur l'IA. »
12. « Ça, c'est interdit depuis 2025. »
13. « Test : êtes-vous piratable ? »
14. « L'IA m'a menti. Voici comment je l'ai vu. »
15. « 3 outils IA gratuits et européens. »
16. « Votre concurrent le fait déjà. »
17. « Le jour où un salarié a partagé tout le fichier clients… »
18. « Si vous avez un site web, regardez ça. »
19. « Ma cliente a gagné 5 h par semaine. » *(chiffre réel uniquement)*
20. « Vrai ou faux ? »
21. « Ce que la CNIL contrôle en premier. »
22. « Le mot de passe le plus utilisé au monde est… »
23. « Pourquoi j'ai refusé ce client. »
24. « Formation obligatoire ? Oui, pour l'IA. » *(sous réserve Omnibus)*
25. « Ce PowerPoint endort vos équipes. »
26. « L'erreur n° 1 des patrons avec l'IA. »
27. « Deepfake ou pas deepfake ? »
28. « Je vous montre ma boîte à outils IA. »
29. « Le RGPD en 3 mots. »
30. « Avant / après l'IA. »
31. « On m'a posé cette question 12 fois cette semaine. »
32. « Votre WhatsApp pro est-il conforme ? »
33. « Ne donnez JAMAIS ça à une IA. »
34. « Ça marche aussi à Saint-Pierre. » (ou Saint-Denis, Saint-Paul…)
35. « Le jargon IA traduit en créole. »
36. « Pourquoi vos salariés cachent qu'ils utilisent l'IA. »
37. « 1 minute pour sécuriser votre boîte mail. »
38. « Ce qu'un audit RGPD révèle en 30 minutes. »
39. « La pire formation que j'ai vue. »
40. « Et si l'IA faisait vos devis ? »

**Appels à l'action** (un seul par post) : Commentez « IA » · DM « DIAG » · Enregistrez 📌 · Partagez à votre dirigeant·e · Taguez un collègue · Répondez au sondage en story · Activez la cloche 🔔 · Écrivez « CHECKLIST » · Réservez via le lien en bio · Dites « OUI » si vous voulez la suite · Votez A ou B · Posez votre question en story · Envoyez à la personne qui gère la compta · Rejoignez la prochaine session · Suivez pour la partie 2.

> ⚠️ Les mots-clés en commentaire (« IA », « CHECKLIST ») promettent un envoi. **Envoyez-le à la main** ou avec l'outil officiel de Meta. Évitez les robots de DM tiers : c'est de la sous-traitance de données, non européenne dans la plupart des cas.

---

## 7. Photos saisissantes : plan de prise de vue

Le logo, ce sont **trois montagnes connectées**. À La Réunion, les pitons font écho à ce logo, c'est votre signature visuelle.

| # | Photo | Où | Pourquoi |
|---|---|---|---|
| 1 | Vous de dos face au **Piton de la Fournaise**, ordinateur sous le bras | Pas de Bellecombe | Image de marque forte, rappel du logo |
| 2 | Portrait de face, fond neutre, sourire, veste bleu marine | Studio / mur clair | Photo de profil alternative et post « Qui suis-je » |
| 3 | Vous devant un paperboard griffonné « IA / RGPD » | En session | Preuve que vous êtes sur le terrain |
| 4 | Mains sur un clavier, écran flouté, café péi | Bureau | Pour les posts « astuces » |
| 5 | Groupe en atelier (visages **seulement avec accord écrit**) | Salle d'hôtel | Preuve sociale, vend l'inter-entreprise |
| 6 | Vous à **Piton Maïdo** au lever du soleil, t-shirt YEBA | Maïdo | Post « Pourquoi YEBA » |
| 7 | Plan serré sur vos certificats (numéros masqués si besoin) | Bureau | Crédibilité |

> ⚠️ **Drones** : le cœur du Parc national de La Réunion et plusieurs zones proches de l'aéroport sont réglementés. Vérifiez sur la carte Géoportail « Restrictions UAS » avant tout vol. Sinon, utilisez un photographe local.
> ⚠️ **Droit à l'image** (code civil art. 9 + RGPD) : faites signer une **autorisation écrite** à chaque personne reconnaissable, stagiaires compris. L'autorisation précise : Instagram, durée, retrait possible.

---

## 8. Calendrier des 4 premières semaines

Rythme tenable : **3 publications + stories quotidiennes**.

| Semaine | Lundi (réel) | Mercredi (carrousel / post) | Vendredi (réel ou post) | Stories |
|---|---|---|---|---|
| S1 | P1 Manifeste + P2 Qui suis-je | P3 Réel ChatGPT | P4 Carrousel IA Act | Coulisses du lancement, sondage « Vous utilisez l'IA ? » |
| S2 | P5 Réel phishing | P6 Mythe RGPD | P7 Mythe pyramide | Quiz « Vrai/Faux du lundi » |
| S3 | P8 Réel IA Act | P9 CTA DIAG | Réel 4 « 2 h → 4 min » | Question box « Posez-moi vos questions IA » |
| S4 | Réel 6 « Kossa i lé l'IA » | Carrousel « 10 règles d'or de l'IA au bureau » | Réel 15 (réponses aux questions de la S3) | Témoignage (avec accord) + lien vers une session |

**Routines stories** (5 min/jour) :
- Lundi : **Vrai/Faux** (sticker quiz).
- Mardi : **arnaque de la semaine**, avec une capture anonymisée.
- Mercredi : **coulisses**.
- Jeudi : **outil IA testé**.
- Vendredi : **question de la semaine** (boîte à questions), qui devient un réel la semaine suivante.

---

## 9. Idées pour devenir viral (à valider avec vous)

1. **« Kossa i lé… ? »** : une série où vous expliquez un terme tech en créole. Personne ne le fait, c'est très partageable localement.
2. **« L'arnaque de la semaine 974 »** : des arnaques qui touchent vraiment La Réunion (faux SMS colis, faux EDF…). Utile et partagé par les familles.
3. **« Défi IA en live »** : un·e commerçant·e local·e vous donne une tâche et vous la résolvez avec l'IA en 60 s. Vous faites de la pub à ce commerce et il repartage : effet réseau.
4. **Collabs Instagram** (post co-signé) avec la CCI Réunion, un expert-comptable, un hôtel partenaire qui accueille vos séminaires.
5. **Quiz géant « Êtes-vous RGPD-proof ? »** en 10 stories, avec un score final. Vous proposez le DIAG à ceux qui obtiennent un score faible.
6. **Série « Mythes de la formation »** : casser les idées reçues des RH, ce qui vous différencie de vos concurrents formateurs.

---

## 10. Outils conseillés (priorité à la souveraineté UE)

| Besoin | Outil | Origine | Remarque |
|---|---|---|---|
| Programmer les publications | **Meta Business Suite** | USA (Meta) | Gratuit. Les données sont déjà chez Meta, donc pas de transfert supplémentaire |
| Planification multi-réseaux | **Swello** · **Agorapulse** | 🇫🇷 France | *À vérifier : hébergement UE dans leurs conditions* |
| Montage de réels | **CapCut** ❌ → **DaVinci Resolve** (local) ou **Kdenlive** (libre, local) | Rien ne quitte votre ordinateur | CapCut (ByteDance) : conditions d'utilisation larges sur vos contenus |
| Sous-titres automatiques | **Sous-titres natifs Instagram**, ou **Whisper** en local | — | N'envoyez pas vos vidéos clients sur des services inconnus |
| Visuels | Les scripts de ce dépôt (`src/`), ou **Penpot** (libre, 🇪🇸) | UE | Canva : société australienne, à éviter pour les données clients |
| IA textuelle | **Mistral Le Chat** (🇫🇷) | UE | Pour rédiger vos légendes |
| Collecte de prospects (« DIAG ») | **Formulaire Baserow** (déjà connecté à ce dépôt, cloud UE) | 🇳🇱 Pays-Bas | Le lien de bio pointe vers ce formulaire. Le CRM est alimenté directement |
| Lien de bio | Une page de votre site | — | Plutôt que Linktree (hébergé hors UE) |

---

## 11. Conformité : ce que ce compte doit respecter

| Sujet | Règle | RGPD / IA Act / autre |
|---|---|---|
| **Prospects en DM** | Ne copiez pas les données des DM dans un fichier sans informer la personne. Le formulaire Baserow porte une mention d'information : finalité, durée (3 ans après le dernier contact, recommandation CNIL pour la prospection), droits | **RGPD** art. 6 et 13 |
| **CPF** ⚠️ | **Interdiction de démarcher** les titulaires de compte CPF par téléphone, SMS, courriel **ou réseaux sociaux** (loi n° 2022-1587 du 19 déc. 2022). Ne faites jamais de DM spontanés du type « Utilisez votre CPF ». Parlez de vos formations, sans relancer | Code du travail |
| **Visuels ou voix générés par IA** | Depuis le **2 août 2026**, les hypertrucages (deepfakes) doivent être signalés. Activez l'étiquette « Info IA » d'Instagram et écrivez « Contenu généré par IA » si une voix, un visage ou une image réaliste est synthétique | **IA Act** art. 50 |
| **Qualiopi** | Mention obligatoire (catégorie d'action) chaque fois que vous en parlez. Logo utilisé uniquement dans sa version officielle, sans déformation | Charte d'usage de la marque Qualiopi |
| **Témoignages / avis** | Accord écrit, avis réels uniquement, jamais d'avis rédigés à la place du client | Code de la consommation (pratiques commerciales trompeuses) + **RGPD** |
| **Photos de stagiaires** | Autorisation écrite et révocable | **RGPD** + code civil art. 9 |
| **Jeux-concours** | Règlement, gratuité de participation, mention « Instagram n'est pas associé » | Code de la consommation L121-20 + règles Meta |
| **Chiffres cités** | Toujours avec une source. Aucun chiffre inventé | Crédibilité + pratiques commerciales |
| **Accessibilité** | Texte alternatif sur chaque post, sous-titres sur chaque réel, emojis avec modération (ils sont lus à voix haute par les lecteurs d'écran) | Bonnes pratiques RGAA / WCAG |

---

## 12. Indicateurs de suivi (à regarder chaque mois)

- **Enregistrements + partages** par post : le meilleur signal de valeur pour l'algorithme.
- **Taux de visionnage des réels** à 3 s : si moins de 60 %, l'accroche est à retravailler.
- **Nombre de DM « DIAG »** → rendez-vous → devis → CA. C'est le seul indicateur qui paie.
- Abonnés **locaux** (Statistiques → Audience → Villes) : visez plus de 50 % à La Réunion.

---

## 13. Autocritique de la proposition, puis corrections

| Faille détectée | Type | Correction apportée |
|---|---|---|
| L'article 4 de l'IA Act a pu être modifié par l'« Omnibus numérique » | Juridique | Avertissement ajouté en P4/P8. **Vérification EUR-Lex obligatoire** avant publication |
| La bio initiale faisait 171 caractères (limite : 150) | Faisabilité | Réécrite à 134 caractères |
| « Formateur certifié Qualiopi » est inexact | Juridique | Remplacé par « Organisme Qualiopi » + mention de catégorie |
| Lignes du motif derrière le texte : gênant pour la lecture | Accessibilité | Motif limité au haut des visuels et masqué sous le texte |
| Or sur blanc : contraste insuffisant | Accessibilité | Surlignage « marqueur » bleu nuit sur fond or |
| DM par mot-clé + CPF = risque de démarchage illégal | Légal | Règle §11 : répondre, jamais relancer sur le CPF |
| Instagram = Meta (USA), transfert hors UE | Souveraineté / RGPD | Aucune donnée client sur Instagram ; collecte via Baserow UE |
| Réels muets = moins de portée | Technologique | Ajouter un son de la bibliothèque Instagram au moment de publier |
| Posts sans visage humain = confiance plus faible | Social / commercial | Plan photo (§7) + remplacer P2 par une vraie photo |
| Coût en temps (3 posts + stories par semaine) | Économique | Scripts réutilisables ; 1 demi-journée de tournage = 1 mois de réels |
| Chiffres « 90 % », « 5 h/semaine » dans la banque d'accroches | Éthique / légal | Marqués « uniquement avec source ou chiffre réel » |
| Numéro 17Cyber / sites officiels susceptibles d'évoluer | Fiabilité | Vérifier que 17cyber.gouv.fr est toujours actif avant de republier |
| Écologie : vidéos lourdes, IA générative énergivore | Écologique | Réels courts (15 s), rendu local, IA seulement là où elle apporte de la valeur |

---

## 14. Régénérer ou modifier les visuels

```bash
cd instagram-yeba-ia
pip install playwright pillow imageio-ffmpeg
python src/generate.py   # posts, carrousel, couvertures, « À la une », profil, maquette
python src/reels.py      # 3 réels MP4 animés (15 s)
```
Les textes se modifient directement dans `src/generate.py` (dictionnaires `POSTS`, `CAROUSEL`, `REEL_COVERS`) et `src/reels.py` (`REELS`). Les crochets `[ ]` mettent un mot en couleur.

### Sources citées
- Règlement (UE) 2024/1689 (IA Act), art. 4, 50, 113 : eur-lex.europa.eu
- Règlement (UE) 2016/679 (RGPD), art. 2, 4, 6, 13, 30, 33 : eur-lex.europa.eu ; cnil.fr
- Loi n° 2022-1587 du 19 décembre 2022 (fraude au CPF) : legifrance.gouv.fr
- Charte d'usage de la marque Qualiopi : travail-emploi.gouv.fr
- K. Letrud, « A rebuttal of NTL Institute's learning pyramid », *Education*, vol. 133, 2012
- Cybermalveillance.gouv.fr ; 17cyber.gouv.fr (plateforme lancée fin 2024)
- Annonce du format de grille 3:4 : Adam Mosseri (Instagram), janvier 2025
- Tissu économique TPE-PME à La Réunion : INSEE (chiffre fourni par YEBA FORMATIONS)
