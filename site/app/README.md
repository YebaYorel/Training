# YEBA IA-Expertise — application

Application à huit pages : accueil, formations, veille IA, RGPD & IA Act,
à propos, contact, mentions légales, politique de confidentialité.

```
index.html     structure, en-tête, pied de page, assistant, consentement
styles.css     charte, thèmes clair et sombre, animations
contenu.js     TOUT le texte — c'est le seul fichier à ouvrir pour éditer
app.js         routeur, transitions, filtres, assistant, consentement
scene.js       scène animée du héros
```

## Modifier le contenu

Tout est dans `contenu.js`. Aucune connaissance technique requise.

- **Ajouter une formation** : **dans Airtable**, puis `python site/build.py`.
  Le catalogue vit dans `formations.js`, qui est GÉNÉRÉ — ne l'éditez jamais à
  la main, il serait écrasé. Le filtre par domaine et le sélecteur du
  formulaire se mettent à jour seuls.
  L'accroche commerciale, elle, n'est pas dans Airtable : elle se règle dans le
  dictionnaire `ACCROCHES` de `site/build.py`.
- **Ajouter une brève de veille** : ajouter une entrée en tête de `VEILLE`.
  Les trois champs `resume`, `impact` et `source` sont obligatoires — une brève
  sans source n'est pas de la veille.
- **Enrichir l'assistant** : ajouter une entrée à `FAQ` avec ses mots-clés.

## Votre photographie

La page « À propos » affiche un cadre en attente. Pour le remplacer :

1. Déposer votre portrait dans ce dossier sous le nom `portrait.jpg`
   (format portrait 4/5, 1000 × 1250 px suffisent).
2. Dans `app.js`, page `apropos`, remplacer le contenu de `.portrait-cadre` par :
   `<img src="portrait.jpg" alt="Aurélien Lumeka" width="1000" height="1250">`

Je n'ai pas votre photographie et je n'en invente pas.

## La scène animée : un choix, pas un pis-aller

Les personnes du héros sont **dessinées au code**, pas photographiées. Trois
raisons, dans cet ordre :

1. **Les photos de banque d'images sont le cliché du secteur.** Un visiteur
   reconnaît en une seconde une salle de formation générique. L'effet est
   l'inverse de celui recherché.
2. **Une photo de personne identifiable est une donnée personnelle.** Publier
   des clichés de vos stagiaires suppose le consentement écrit de chacun, et
   relève de l'article 9 du RGPD si un handicap y est visible. Une silhouette
   dessinée n'engage rien.
3. **Aucune licence à gérer, aucun fichier lourd.** La scène pèse quelques
   kilo-octets et s'adapte à toutes les tailles d'écran.

Six carnations réelles sont réparties aléatoirement à chaque chargement, sans
qu'aucune soit traitée comme la valeur par défaut. Les personnages sourient,
saluent le visiteur et s'entraident autour d'une table — conformément à la
scène demandée.

## L'assistant : ce qu'il est, et ce qu'il n'est pas

C'est un **moteur de correspondance de mots-clés** sur une liste de réponses
que vous avez validées. Aucun modèle de langage n'est appelé, et rien de ce que
le visiteur écrit ne quitte son navigateur. L'assistant le dit lui-même dès son
premier message.

Ce choix n'est pas une limitation subie :

- un vrai agent conversationnel exige un serveur, donc une clé d'API — qui
  serait exposée si elle était placée dans la page ;
- il enverrait les questions des visiteurs à un tiers, ce qui est un traitement
  de données à déclarer, avec sa base légale et sa mention d'information ;
- il peut inventer une réponse fausse sur vos tarifs ou votre certification,
  ce qui vous engage.

**Pour aller plus loin** : un assistant à modèle de langage suppose un serveur
dans l'Union européenne. Mistral (France) et Scaleway (France) exposent des API
compatibles. Il faudra alors une mention d'information, une base légale et une
durée de conservation des échanges — la politique de confidentialité devra être
complétée en conséquence.

## Le bandeau de consentement

Le site **ne dépose aucun traceur**. Le panneau ne prétend donc pas recueillir
un consentement sans objet : il informe, et conserve votre choix pour le jour
où une mesure d'audience serait ajoutée.

Le choix est conservé dans le stockage local du navigateur. C'est un stockage
strictement nécessaire au service demandé par l'utilisateur, donc **exempté de
consentement** au sens de l'article 82 de la loi Informatique et Libertés et des
lignes directrices de la CNIL.

Si vous ajoutez une mesure d'audience : Matomo auto-hébergé dans l'UE, configuré
selon l'exemption CNIL, reste dispensé de consentement.

## Accessibilité

- **Atkinson Hyperlegible** pour le corps du texte, police dessinée par le
  Braille Institute pour les personnes malvoyantes.
- Contrastes conformes à votre charte : l'or ne sert jamais de couleur de texte
  sur fond clair (2,29:1 — échec), `--or-texte` (#7A6019) prend le relais.
- Lien d'évitement, focus visible, `aria-current` sur la navigation,
  `aria-live` sur les résultats de filtrage et le fil de l'assistant,
  `aria-expanded` sur le lanceur, fermeture par la touche Échap.
- `prefers-reduced-motion` : la scène est rendue en image fixe, le rideau de
  transition est désactivé, les révélations n'ont pas lieu.
- Thèmes clair et sombre, y compris pour le réglage « système ».

## Limites connues

1. ~~Catalogue recopié à la main~~ — **corrigé**. `build.py` génère
   `formations.js` depuis Airtable, avec le filtre de marque blanche et le
   contrôle d'éligibilité CPF appliqués à la génération. Il n'y a plus qu'une
   seule source de vérité.
2. **La veille est manuelle.** Un flux automatique suppose un serveur. Les
   entrées sont datées et sourcées à la main dans `contenu.js`.
3. **Le formulaire n'envoie rien** : il ouvre votre messagerie. Aucune collecte,
   donc aucun traitement à déclarer — mais aucune mesure de conversion non plus.
4. **Les mentions légales sont incomplètes.** Forme juridique, capital social,
   RCS, TVA intracommunautaire, hébergeur et médiateur de la consommation sont
   signalés en jaune dans la page. Ce ne sont pas des détails : le médiateur est
   une obligation dès qu'un particulier finance lui-même une formation
   (code de la consommation, art. L.612-1).
5. **Pas de rendu serveur.** Les moteurs de recherche indexent aujourd'hui le
   JavaScript, mais une version statique par page resterait préférable pour le
   référencement. À envisager si le trafic devient un objectif prioritaire.

## Sources

Base Airtable `appQ2zqc80kkc6MR1`, tables `CONFIG SYSTEME` et
`CATALOGUE FORMATIONS`, relevées le 17/09/2026.
Règlement (UE) 2016/679 · Règlement (UE) 2024/1689 · loi Informatique et
Libertés, art. 82 · code du travail, art. L.6352-12 · code de la consommation,
art. L.121-2 et L.612-1 · CGI, art. 261-4-4° a.
