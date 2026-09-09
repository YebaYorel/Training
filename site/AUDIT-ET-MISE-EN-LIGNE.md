# Audit du site YEBA FORMATIONS — avis froid, et plan de mise en ligne

*9 septembre 2026*

## Avertissement sur le périmètre

Je n'ai **pas eu accès au site**. Le domaine `stitch.withgoogle.com` est bloqué
par la politique réseau de cette session, et le fichier d'export ne contient que
la liste des écrans, sans URL téléchargeable.

Ce que j'ai réellement examiné : **la charte graphique** (image fournie) et
**l'architecture de l'information**, telle que la révèle la liste des 13 écrans.
C'est suffisant pour un verdict structurel. Ce n'est pas suffisant pour un audit
de code — voir la fin du document.

---

# PARTIE I — LA CHARTE GRAPHIQUE

## Ce qui est bon, et qui doit être conservé

**La palette.** Bleu profond `#1B3A6B` + or `#C9A84C` : c'est le bon couple pour
vendre de la confiance et de la conformité. Ce n'est pas original, mais
l'originalité n'est pas ce qu'on achète chez un consultant RGPD. C'est juste.

**Le motif « 974 ».** Le réseau de points avec la silhouette de l'île est le
seul élément vraiment ancré localement de toute la charte. Il est relégué en bas
à droite comme un ornement. **C'est ton meilleur actif visuel, et il est
sous-exploité.**

**Le contraste bleu/blanc.** 11,27:1. Excellent, AAA sur toute la ligne.

## Les trois problèmes, du plus grave au moins grave

### 1. Le logo dit l'inverse de ce que tu vends

Un **œil ouvert au sommet de pyramides triangulaires**. Ce symbole a une lecture
immédiate et universelle : l'Œil de la Providence, l'imagerie maçonnique, et
dans le langage courant d'aujourd'hui — **la surveillance**.

Tu vends du RGPD, c'est-à-dire *la protection des personnes contre la
surveillance*. Tu vends de la gouvernance de l'IA, c'est-à-dire *l'encadrement
des systèmes qui observent*. Et ton logo est un œil qui surveille depuis le
sommet d'une pyramide.

Ce n'est pas une question de goût. C'est une **contradiction entre le signe et
le discours**, et elle jouera contre toi précisément auprès du public le plus
sensible à ces sujets. À La Réunion comme ailleurs, la défiance envers l'IA
passe par l'imaginaire de la surveillance : tu l'alimentes en haut de chaque
page.

**Ce qu'il faut faire.** Garde les trois formes triangulaires — elles peuvent
lire comme des **pitons**, ce qui serait un ancrage réunionnais fort et
immédiat. Remplace l'œil par autre chose au sommet : un point de connexion, un
nœud de réseau, ou rien. La géométrie du logo fonctionne. C'est l'œil qui doit
partir.

> Si tu tiens à l'œil pour des raisons personnelles, c'est ton entreprise et ta
> décision. Mais alors sache que tu paieras ce choix en objections que personne
> ne te formulera à voix haute.

### 2. L'or sur blanc est illisible — et c'est mesurable

J'ai calculé les ratios de contraste de ta palette selon la méthode WCAG 2.1 :

| Combinaison | Ratio | AA texte normal (4,5) | AA grand texte (3,0) | AAA (7,0) |
|---|---:|:---:|:---:|:---:|
| **Or sur blanc** | **2,29:1** | ❌ | ❌ | ❌ |
| Or sur bleu | 4,93:1 | ✅ | ✅ | ❌ |
| Or sur noir | 8,20:1 | ✅ | ✅ | ✅ |
| Bleu sur blanc | 11,27:1 | ✅ | ✅ | ✅ |
| Blanc sur bleu | 11,27:1 | ✅ | ✅ | ✅ |
| Bleu sur noir | 1,66:1 | ❌ | ❌ | ❌ |

**Le mot « FORMATIONS » de ton logo principal est en or sur fond clair. Il échoue
au niveau le plus permissif de la norme.** Idem pour tout titre ou tout bouton
doré sur fond blanc.

Pour n'importe qui, ce serait un défaut. Pour **toi**, qui es référent handicap
en organisme de formation et qui écris dans tes propres programmes « contrastes
conformes au niveau AA du référentiel WCAG 2.1 », c'est une contradiction
frontale entre ce que tu affiches et ce que tu vends.

**La règle à graver, et je l'ai appliquée dans le bandeau cookies fourni :**

> **L'or ne touche jamais le blanc.** L'or vit sur le bleu ou sur le noir.
> Sur fond clair, le texte est bleu `#1B3A6B` ou noir `#121212`.
> L'or sur fond clair est réservé aux **surfaces**, jamais au texte : filets,
> aplats, soulignements décoratifs, bordures.

Cette règle ne t'appauvrit pas : elle produit une identité plus tranchée — de
grands aplats bleus et noirs où l'or éclate, et des zones claires sobres. C'est
plus premium que de l'or partout.

### 3. Poiret One est un mauvais choix, et les images sont datées

**Poiret One** est une police décorative à graisse très fine, sans variantes de
graisse réelles. En dessous de 24 px elle devient illisible ; sur un écran non
rétina elle se délite ; pour un lecteur malvoyant elle est hostile. Tu
revendiques l'accessibilité et tu retiens la police la moins accessible de la
charte.

**Correction :** Montserrat pour les titres (elle est déjà là, elle est
géométrique et solide), Inter pour tout le texte courant. **Deux familles,
c'est un système. Trois, c'est une hésitation.** Poiret One, si tu y tiens
absolument, en usage unique et à très grande taille — un slogan sur la page
d'accueil, rien d'autre.

**Le style d'images « Cyber-Garage Premium ».** Tunnels bleus, néons, le mot
« AI » qui brille. Ce sont des images d'IA générative reconnaissables au premier
coup d'œil, et tout le monde en produit depuis trois ans. Elles ne disent pas
« premium ». Elles disent « j'ai tapé *AI futuristic* dans un générateur ».

Le seul visuel qui vaut quelque chose dans cette planche, c'est **ton portrait
en noir et blanc**. Il est bon. Il est réel.

**Correction :** ton marché, ce sont des dirigeants de TPE-PME réunionnaises.
Ce qui les convainc, ce n'est pas un tunnel de néons : c'est **toi, en salle,
devant de vraies personnes**. Trois photos de session réelle — toi au
paperboard, un groupe en atelier, une remise d'attestation — valent dix fois
toute cette imagerie. Et elles sont infalsifiables, ce qu'un visuel généré n'est
pas. Fais venir un photographe une demi-journée sur ta prochaine session : c'est
le meilleur investissement marketing que tu puisses faire à ce stade.

*(Pense au consentement écrit des stagiaires photographiés : c'est un
traitement de données à part, base légale consentement — art. 6.1.a et 7 du
RGPD — libre, spécifique et révocable. Tes programmes prévoient déjà la
clause.)*

---

# PARTIE II — L'ARCHITECTURE DU SITE

## Ce que révèle la liste des écrans

| Écran | Lecture |
|---|---|
| Accueil Premium | |
| Accueil Immersif & Social Proof | **Deux pages d'accueil** |
| Catalogue de Formations | |
| Catalogue Optimisé & Responsive | **Deux catalogues** |
| Dashboard Sécurité & IA Trust | Pièce de démonstration |
| Programme Formation Détaillé — IA | |
| Programme Formation Détaillé — RGPD | |
| Mentions Légales & Confidentialité | |
| Design System, Shader ×2, logo, photo | Ressources de travail |

## Verdict froid : c'est un travail de designer, pas un outil de vente

Tu as deux accueils et deux catalogues. Ce ne sont pas des pages, ce sont des
**variantes non arbitrées**. Un site qui n'a pas tranché son accueil n'est pas
prêt à être mis en ligne.

Et surtout : **il manque tout ce qui fait vendre.**

| Page manquante | Pourquoi elle est décisive |
|---|---|
| **Financement** | Premier réflexe d'un dirigeant réunionnais : « qui paie ? ». OPCO, plan de développement, France Travail, Région. Sans cette page, tu perds le prospect avant même le catalogue. |
| **Tarifs, même en fourchette** | Un site sans prix fait fuir les TPE. « À partir de X € la journée » suffit à qualifier. |
| **Qui suis-je** | Tu es ton produit. Tes certifications — Google AI, Qualiopi, ANSSI, CNIL, référent handicap — sont ton avantage concurrentiel et elles doivent avoir leur page, avec les logos et les numéros. |
| **Preuves** | Témoignages nommés, taux de satisfaction, nombre de stagiaires formés. Ton Airtable contient déjà ces champs. |
| **Contact** | Aucun formulaire de contact dans la liste. C'est l'unique chose qu'un site vitrine doit faire. |
| **Accessibilité** | Obligatoire dans ton positionnement, et déclaration attendue. |
| **CGV, cookies, politique de confidentialité** | Fournis dans `juridique/`. Un seul écran « Mentions légales & Confidentialité » ne couvre pas les quatre obligations. |

Le « Dashboard Sécurité & IA Trust » est une belle pièce de démonstration. Mais
sur un site vitrine, un tableau de bord ne convertit personne : il impressionne
un confrère, pas un acheteur. Garde-le comme **preuve de savoir-faire** dans une
page « ce que je peux construire pour vous », pas comme page principale.

## Est-il « à la hauteur de La Réunion » ? Est-il vendeur ?

**À la hauteur : oui, techniquement.** Le niveau graphique dépasse la moyenne
des sites d'organismes de formation locaux, qui sont pour beaucoup des gabarits
génériques mal remplis. Tu es au-dessus.

**Vendeur : non, pas en l'état.** Un beau site n'est pas un site qui vend. Il
manque le chemin : *un problème reconnu → une preuve → un financement → un seul
appel à l'action*. En l'état, un visiteur admire et repart.

Et une chose que tu ne dois pas rater : ton positionnement réel n'est pas
« formation IA ». C'est **« le seul à La Réunion qui forme à l'IA ET qui vous met
en conformité »**. Cette phrase n'apparaît nulle part dans l'architecture. C'est
pourtant tout ce que tu vends, et c'est ce qui te distingue de tes concurrents.

---

# PARTIE III — LES CORRECTIONS, RÉSOLUES

## 1. Arborescence à retenir

```
Accueil  ── une seule version. Trancher.
│
├── Formations
│   ├── IA Générative        ├── Automatisation
│   ├── RGPD & Cybersécurité ├── Copilot Microsoft 365
│   ├── Vente                └── Management
│
├── Conseil & Audit          ← RGPD / IA Act / gouvernance. Ta marge la plus forte.
├── Financements             ← OPCO, PDC, France Travail, Région. Page décisive.
├── Qui suis-je              ← certifications, parcours, portrait
├── Références & Avis        ← preuves chiffrées
├── Accessibilité            ← déclaration + référent handicap
├── Contact                  ← formulaire + téléphone + délai de réponse annoncé
│
└── Pied de page : Mentions légales · Confidentialité · Cookies · CGV ·
                   Gérer mes cookies · Accessibilité
```

**Suppressions :** le second accueil, le second catalogue. **Déplacement :** le
dashboard vers « Conseil & Audit », en preuve.

## 2. Structure de la page d'accueil

1. **Une phrase, qui nomme le problème du client** — pas ton offre.
   Par exemple : *« Vos équipes utilisent déjà l'IA. Sans règles, sans
   formation, et sans savoir où partent vos données. »*
2. **Ta réponse en une ligne** + un seul bouton : « Parler de votre situation ».
3. **Les certifications**, en bandeau : Qualiopi, NDA, Google AI, ANSSI, CNIL,
   référent handicap. Ce bandeau est ton argument le plus fort et il doit être
   visible sans faire défiler la page.
4. **Trois portes d'entrée** : Former mes équipes · Mettre en place l'IA ·
   Me mettre en conformité.
5. **Une preuve** : un témoignage nommé, un chiffre.
6. **Le financement** : « 80 % de nos formations sont financées. Voyons
   comment. »
7. **Rappel de l'appel à l'action.** Le même que celui du haut. Un seul.

## 3. Règles de la charte, corrigées

```css
:root{
  --yeba-bleu:#1B3A6B;   /* texte sur clair, fonds, aplats */
  --yeba-or:#C9A84C;     /* JAMAIS en texte sur fond clair */
  --yeba-noir:#121212;   /* texte long, fonds profonds */
  --yeba-blanc:#FFFFFF;
}
/* Titres : Montserrat 700. Texte : Inter 400/600. Deux familles, pas trois. */
/* Corps de texte : 18px minimum. Ton public a plus de 45 ans en moyenne. */
/* Cibles tactiles : 44 × 44 px minimum. */
/* Focus clavier visible partout : outline 3px or sur fond sombre, bleu sur clair. */
```

## 4. Ce qui doit être vrai avant de publier

- [ ] Un seul accueil, un seul catalogue
- [ ] L'œil retiré du logo, ou décision assumée par écrit
- [ ] Aucun texte or sur fond clair, nulle part
- [ ] Poiret One retirée du texte courant
- [ ] Photos réelles de session à la place des visuels générés
- [ ] Page Financements, page Contact, page Qui suis-je
- [ ] Les cinq documents de `juridique/` publiés et liés en pied de page
- [ ] Bandeau cookies actif **avant** tout script de mesure d'audience
- [ ] Aucun bouton de paiement immédiat pour un particulier *(voir
      `juridique/00-LIRE-DABORD.md` — c'est le risque juridique n°1)*

---

# PARTIE IV — MISE EN LIGNE

## Choix de l'hébergeur

| | OVHcloud | Infomaniak | Scaleway |
|---|---|---|---|
| Pays | 🇫🇷 France | 🇨🇭 Suisse | 🇫🇷 France |
| UE | Oui | **Non** — adéquation | Oui |
| Offre vitrine | Perso ~ 40 €/an | Site web ~ 70 €/an | Plutôt cloud |
| Adapté | ✅ | ✅ | Surdimensionné |

**Recommandation : OVHcloud, hébergement en France.** Pour ton discours de
souveraineté, tu ne peux pas te permettre un hébergeur hors UE.

> ⚠️ **Infomaniak est suisse, pas européen.** Une décision d'adéquation rend le
> transfert licite, mais ce n'est pas l'Union. Ne le présente jamais comme
> « hébergement UE » à un client : c'est le genre d'approximation qui détruit une
> crédibilité d'auditeur RGPD.

## Les 12 étapes

1. **Domaine** — `yebaformations.re`, avec protection des données WHOIS.
2. **Hébergement** — offre mutualisée avec certificat TLS gratuit inclus.
3. **DNS** — A/AAAA vers l'hébergement, puis **SPF, DKIM, DMARC, CAA**
   (`securite/durcissement.md`, § 4).
4. **Messagerie professionnelle** — `contact@`, `security@`, `dmarc@`.
5. **HTTPS** — certificat activé, redirection permanente, HSTS.
6. **Dépôt des fichiers** — par SFTP ou Git. **Jamais de FTP en clair.**
7. **En-têtes de sécurité** — `.htaccess` fourni.
8. **Bandeau cookies** — installé et testé **avant** tout script de mesure.
9. **Documents juridiques** — publiés, liés en pied de page de chaque page.
10. **Sauvegarde** — automatique quotidienne, **et une restauration testée**.
11. **Vérifications** — `securityheaders.com` (cible A), `ssllabs.com` (cible A),
    `wave.webaim.org`, Lighthouse.
12. **Référencement** — `sitemap.xml`, `robots.txt`, fiche établissement locale,
    et surtout : les mots-clés que tapent réellement tes prospects
    (« formation IA Réunion », « RGPD 974 », « organisme formation Qualiopi
    Saint-Denis »).

## Coût annuel réaliste

| Poste | Ordre de grandeur |
|---|---|
| Domaine `.re` | 15 à 25 € |
| Hébergement mutualisé | 40 à 80 € |
| Messagerie professionnelle | 0 à 60 € |
| **Médiateur de la consommation** | 50 à 300 € — **obligatoire si tu vends à des particuliers** |
| Photographe (une demi-journée) | 300 à 600 €, une fois |
| **Total récurrent** | **≈ 150 à 450 € par an** |

Aucun de ces montants ne justifie de retarder la mise en ligne. Le seul poste
qui pourrait bloquer, c'est la relecture juridique des CGV — et elle est moins
chère qu'un litige.

---

# CE QU'IL ME MANQUE POUR ALLER PLUS LOIN

**Pour l'audit de sécurité du code**, il me faut le code. Deux voies :

**Voie 1 — le MCP Stitch, sur ta machine.** Je l'ai déjà déclaré dans
`.mcp.json` du dépôt et documenté le jeton dans `.env.example`. Il te faut :
un compte Google Cloud, l'API Stitch activée, un jeton placé dans
`STITCH_API_TOKEN`. Depuis **Claude Code sur ton poste**, je pourrai alors lire
et modifier tes écrans directement.

> Dans **cette** session cloud, le domaine `stitch.withgoogle.com` est bloqué par
> la politique réseau de l'environnement. La configuration est prête, mais elle
> ne fonctionnera pas ici.
> *(Sources : [Codelab Google](https://codelabs.developers.google.com/design-to-code-with-antigravity-stitch) ·
> [byteiota](https://byteiota.com/google-stitch-free-ai-ui-generator-with-mcp-support-for-claude-code-and-cursor/))*

**Voie 2 — l'export, tout de suite.** Dans Stitch, exporte en HTML/CSS ou
Tailwind et dépose les fichiers dans `site/source/` du dépôt. Je peux alors
auditer réellement : injections, gestion des formulaires, secrets exposés,
dépendances vulnérables, accessibilité du balisage, performance.

C'est la voie la plus rapide, et elle ne dépend d'aucune configuration.
