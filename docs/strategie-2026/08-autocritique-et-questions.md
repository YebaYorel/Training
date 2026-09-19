# 08 — Autocritique de ma propre solution, et ce qu'il me manque

> Vous m'avez demandé d'être intransigeant. Le pire manque de rigueur serait de l'être
> avec votre plan et pas avec le mien. Voici les failles de ce que je viens de vous
> proposer, par dimension, puis les corrections que j'y apporte.

---

## 1. Faille économique — la plus sérieuse

**Le défaut :** mon plan vous demande **~110 heures sur 12 semaines** alors que je constate
moi-même que le temps est votre ressource la plus rare, et que votre trésorerie se tend.
Je vous propose d'investir massivement dans un canal (le contenu) dont le retour est à
6-12 mois, pendant que votre socle CFA se contracte de 10 à 33 %. **Si votre trésorerie ne
tient pas 6 mois, ce plan vous fait couler plus vite, pas moins vite.**

**Deuxième défaut :** mes prix sont des **hypothèses**. Si votre marché local plafonne à
700 €/jour de formation, le modèle à 139 750 € s'effondre et il faut tout recalculer.

**✅ Levé le 19/09/2026 :** trésorerie **supérieure à 6 mois** de charges fixes et
**8 à 10 h/semaine** disponibles. **Le plan complet est exécutable.** Cette faille tombe.

**Ce qui reste :**
- Mes prix restent des hypothèses `[H]`. Si votre marché plafonne à 700 €/jour, le modèle à
  139 750 € s'effondre et il faut tout recalculer. **Donnez-moi vos tarifs réels.**
- La marge est mince : 9 h/semaine sur 12 semaines, sans imprévu. **Si une semaine saute,
  coupez le contenu, jamais la prospection.**

---

## 2. Faille stratégique — je peux me tromper sur le coin d'entrée

**Le défaut :** je mise gros sur l'**article 4 de l'IA Act**. Trois risques réels :
1. **L'argument peut ne pas mordre.** Une obligation sans sanction autonome directe ne
   déclenche pas toujours l'achat. Un dirigeant de TPE qui a survécu au RGPD sans rien
   faire ne bougera peut-être pas plus pour l'IA Act.
2. **Le Digital Omnibus a créé un brouillard médiatique.** Beaucoup de dirigeants ont
   retenu « l'IA Act est reporté ». Vous devrez d'abord défaire cette croyance avant de
   vendre — ce qui allonge le cycle.
3. **C'est un argument par la peur**, et vous voulez être « le gars simple et marrant ».
   Il y a une **tension réelle** entre votre positionnement éditorial et votre coin
   commercial. Je ne l'avais pas assez relevée.

**Correction :**
- **Séparer les registres.** Le contenu public = productivité, humour, démonstrations
  (« je vous fais gagner des heures »). Le rendez-vous commercial = conformité (« et au
  passage, voici votre obligation »). La peur ne fait pas un bon contenu social ; elle fait
  un excellent argument en rendez-vous.
- **Test de validation en 4 semaines** : sur 80 appels, mesurer le taux de transformation
  de l'accroche « article 4 » **contre** celle du « gain de temps ». **Si l'article 4 ne
  convertit pas mieux après 40 appels, on bascule.** L'hypothèse est réfutable — c'est ce
  qui la rend utilisable.

---

## 3. Faille concurrentielle — j'ai peut-être sous-estimé l'écart

**Le défaut :** j'ai identifié MAIA (2019), la CCI (7 sites), Le Cube, Flowt, SavoirIA,
et 7 Ambassadeurs IA labellisés. Mais **je n'ai pas vérifié leurs tarifs, leur capacité
réelle, ni s'ils couvrent déjà l'angle conformité**. Il est possible que l'un d'eux vende
déjà exactement le Pack article 4. Dans ce cas, votre « quasi-vide concurrentiel » n'existe
pas et tout le positionnement doit bouger.

**Correction :** **enquête concurrentielle de 3 heures, en semaine 1, avant de graver
l'offre.** Appelez-les en tant que prospect. Demandez leurs tarifs, leurs délais, leur
offre conformité. C'est légal, c'est normal, et ça vaut mieux que mes recherches web.
**Je ne peux pas faire ce travail à votre place : ces informations ne sont pas publiques.**

---

## 4. Faille juridique — les limites de ce que je vous ai dit

**Le défaut :** j'ai cité des textes avec leurs dates, mais je ne suis **pas juriste**, et
cinq points restent ouverts (doc 06 §7) : votre qualification fournisseur/déployeur sous
l'IA Act, l'applicabilité de la directive accessibilité 2019/882, le périmètre de votre RC
Pro, votre statut sur les données de stagiaires CFA, la rédaction de CGV mixtes.

**Risque supplémentaire que je n'avais pas assez souligné :** en vous positionnant
publiquement comme référent conformité, vous **augmentez votre exposition**. Un consultant
en conformité qui se trompe est jugé plus sévèrement qu'un formateur généraliste. Votre
communication crée l'obligation de tenir le niveau.

**Correction :** **une consultation d'avocat en droit du numérique en semaine 2, avant
la première vente de conformité.** Budget à prévoir. C'est la dépense la plus rentable du
trimestre, parce qu'elle protège tout le reste.

---

## 5. Faille technique — j'avais décidé pour vous, vous avez corrigé

**Le défaut :** je recommandais Astro pour la vitesse et la sécurité, en minimisant le fait
que **cela vous rendait dépendant de moi pour changer une virgule**. Pour un dirigeant seul,
c'est un handicap opérationnel réel que j'avais sous-pondéré au profit de l'élégance technique.

**✅ Arbitré le 19/09/2026 : WordPress chez OVHcloud.** Votre autonomie éditoriale prime.
J'exécute sans rediscuter.

**Ce que ce choix crée, et que j'ai intégré au doc 05 :** une routine de mises à jour
hebdomadaire, une discipline de 12 extensions maximum, et surtout **la fermeture des
5 fuites que WordPress crée par défaut** (Google Fonts, Gravatar, émojis, oEmbed, XML-RPC).
Ce dernier point n'était pas dans ma version Astro parce qu'il n'existait pas — il devient
**le travail de conformité principal du site**, et presque personne ne le fait.

**Même mouvement sur le décor vidéo :** vous avez choisi le **fond vert + OBS** contre mon
coin réel. Mon objection portait sur la crédibilité d'un faux décor, pas sur la technique —
et le traitement 100 % local du fond vert est en réalité **meilleur que ma proposition sur
le plan de la souveraineté**. J'ai donc gardé mon objection uniquement là où elle vaut :
**jamais de faux bureau en fond**. Trois fonds autorisés seulement (aplat de marque, contenu
pédagogique, photo réelle du péi). Le fond vert cesse d'être un cache-misère et devient un
outil pédagogique.

---

## 6. Faille de cohérence — la contradiction que je n'ai pas totalement résolue

**Le défaut :** votre règle est « pas d'outils qui ne respectent pas la souveraineté
européenne ». Mon architecture en couches est une **atténuation**, pas une résolution.
Publier sur Instagram, c'est alimenter un acteur américain, quelle que soit l'élégance de
mon schéma. Et vous utilisez actuellement **Claude, outil américain**, pour bâtir votre
stratégie.

**Je ne vais pas prétendre que ce problème est réglé. Il ne l'est pas.** Il est arbitré.

**Correction — la règle exacte, à appliquer sans exception :**
1. Les plateformes américaines reçoivent **votre message public**, jamais un fichier, jamais
   une donnée de prospect, jamais un pixel.
2. **Aucune donnée personnelle de client, stagiaire ou prospect** ne transite par une
   session Claude, y compris celle-ci. Pour tout travail sur données réelles : **Mistral**
   ou modèle local.
3. Vous **dites publiquement l'arbitrage** au lieu de le cacher : « je diffuse là où sont
   mes clients, je stocke là où la loi européenne s'applique ». **C'est une position
   défendable et honnête. Prétendre à une pureté totale serait un mensonge qu'un
   concurrent vous ferait payer.**

---

## 7. Faille sociale et politique — le terrain réunionnais

**Le défaut :** j'ai raisonné avec des données publiques et des références nationales. Je
ne connais pas de l'intérieur les rapports de force locaux : qui décide, quels réseaux
comptent, comment la recommandation circule réellement à La Réunion, quelle est la
tolérance locale à un discours « conformité » perçu comme importé de métropole. Je peux
vous avoir proposé un ton qui passe mal sur place.

**Risque social spécifique :** un discours « l'IA va vous faire gagner du temps » est
entendu par les salariés comme « l'IA va supprimer des postes », dans un territoire où le
chômage est structurellement élevé. **Si vous ne traitez pas cette peur frontalement, vous
serez perçu comme le vendeur de la machine qui licencie.**

**Correction :**
- **Faites un pilier de contenu de cette objection**, ne l'évitez pas :
  *« Je n'ai jamais fait licencier personne. Voilà ce que l'IA a remplacé chez ce client :
  la saisie, pas le salarié. »* — avec un cas réel à l'appui.
- **Vous êtes réunionnais et vous connaissez le terrain mieux que moi. Sur le ton, la
  langue, les codes et les réseaux : votre jugement prime sur mes recommandations.**
  Corrigez-moi sans hésiter.

---

## 8. Faille écologique — un angle mort assumé

**Le défaut :** mon plan augmente votre consommation numérique (vidéo, VPS, stockage,
modèles). Je l'ai présenté comme un avantage (traitement local moins coûteux que les
générateurs en ligne) sans le chiffrer. **C'est un argument que je n'ai pas prouvé.**

**Correction :** ne faites **pas** d'argument écologique tant que vous ne pouvez pas le
chiffrer. Un argument environnemental non étayé, sur un marché où l'on peut vous le
demander (commande publique, grands comptes), est un risque d'accusation d'écoblanchiment.
Contentez-vous du fait vérifiable : **traitement local = pas de transfert, donc moins
d'empreinte et zéro exposition des données.** C'est vrai et suffisant.

---

## 9. Ce qui reste solide après cette autocritique

1. **Le revenu récurrent est la seule vraie réponse à votre fragilité.** Rien dans cette
   critique ne l'affaiblit.
2. **Vendre avant de communiquer.** L'ordre reste juste, quelle que soit la version du plan.
3. **Séparer diffusion et données.** L'architecture tient.
4. **Ne pas dire « audit ».** Tient.
5. **Ne pas auditer son propre ouvrage.** Tient.
6. **Votre vraie force est d'être un excellent formateur-vendeur dans un secteur peuplé de
   techniciens qui ne savent pas vendre.** C'est le seul avantage qui ne se copie pas en
   six mois.

---

## 10. Ce qu'il me manque encore pour être précis à 100 %

*Je ne les invente pas. Tant que je ne les ai pas, tout chiffre de ce dossier marqué **[H]**
est une hypothèse de travail, pas une recommandation.*

### Bloquant pour chiffrer
1. **Votre CA 2025 et le prévisionnel 2026**, et la part exacte du CFA.
2. **Vos tarifs réels** : prix d'une journée intra, prix de votre journée en sous-traitance CFA.
3. **Votre trésorerie disponible** en nombre de mois de charges fixes. *(Détermine si on
   exécute le plan complet ou la version allégée — c'est la question la plus importante.)*
4. **Nombre de jours réellement facturés** en 2025, et prévision 2026.

### Bloquant pour produire
5. **Vos codes couleurs hexadécimaux** et votre **logo** (versions carrée, horizontale, fond sombre).
6. **Votre adresse professionnelle** et votre **téléphone professionnel** (mentions légales, fiche locale).
7. **Disposez-vous d'un second numéro** pour WhatsApp Business ?
8. **Combien d'heures par semaine**, réellement et durablement, pouvez-vous consacrer à ce plan ?

### ✅ Tranché le 19/09/2026
- Trésorerie **> 6 mois** · **8-10 h/semaine** → **plan complet**
- Site → **WordPress chez OVHcloud**
- Vidéo → **fond vert + incrustation OBS en local**

### Nouvelles questions créées par ces choix
9. **Quelle est la profondeur de votre pièce de tournage ?** Il faut **3,5 m** entre le fond
   vert et la caméra. En dessous, on bascule sur le plan buste serré (doc 03 §1.1).
10. **Quelle machine utilisez-vous pour monter ?** (processeur, mémoire, système) — si elle
    ne tient pas l'incrustation OBS en direct, la journée de production passe de 7 h à 8 h 30.

### Utile, non bloquant
- Avez-vous déjà des clients entreprise en direct, ou uniquement du CFA ?
- Avez-vous déjà tenté la prospection téléphonique, et avec quels résultats ?
- Êtes-vous seul, ou avez-vous un appui administratif ?
- Votre RC Pro couvre-t-elle déjà le conseil ? *(Vérifiable en un appel.)*
