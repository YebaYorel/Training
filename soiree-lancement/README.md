# « YEBA — Saison 1 » · soirée de lancement YEBA FORMATIONS

Aurélien, Stan et Antho · public : dirigeants et cadres dirigeants de TPE-PME triés sur le volet · 1 h à 1 h 15.

La soirée se regarde **comme une série** : pré-générique en boucle pendant l'accueil, **générique d'ouverture de 80 s**
(motion design + bande-son originale), puis 7 épisodes ouverts chacun par sa carte-titre animée. Épisodes 1 à 4
construits (présentation, histoire, offre YEBA, formations : ≈ 36 min de temps de parole prévu) ; épisodes 5 à 7 déjà en place, masqués
(applications & sites web, audit & devis, mot de fin avec offre soirée).

## Livrables

| Fichier | Rôle | Outil |
|---|---|---|
| `dist/YEBA_Soiree_Lancement.pptx` | **La présentation « cinéma »** : animations natives, Morphose, fonds vidéo vivants, générique et épisodes en lecture automatique, notes orateur | python-pptx |
| `dist/YEBA_Soiree_Lancement_SOBRE.pptx` | Même présentation, fonds en **images fixes** (PC modeste, public sensible au mouvement) | python-pptx |
| `dist/videos/yeba-saison1-generique.mp4` | **Le générique** : 80 s, 1080p, son −16 LUFS (offres, Qualiopi, NDA, horaires, 11 formations) | Remotion |
| `dist/videos/yeba-episode-1…7.mp4` | Cartes-titres d'épisode (4,5 s, sting sonore) | Remotion |
| `dist/videos/yeba-preshow.mp4`, `fond-*.mp4` | Boucle d'accueil et 9 fonds vivants (sans son) | Remotion |
| `dist/YEBA_Soiree_Lancement.pdf` | Export figé (Slides.com, impression, envoi) | LibreOffice |
| `revealjs/index.html` | Version web hors ligne, jumelle du PPTX (Auto-Animate, fonds vidéo, touche S = notes) | Reveal.js |
| `vba/YebaAnimations.bas` | Contrôle avant soirée, mode sobre / cinéma, suppression des post-it avant envoi | VBA |
| `storyboard.md` | Storyboard épisode par épisode : texte, visuel, animation, notes, durée, mots projetés | — |
| `felo/prompt_felo_slides.md` · `slides-com/plan_slides_com.md` | Prompt Felo (sans donnée personnelle) · plan de montage Slides.com | Felo · Slides.com |
| `outils/generer_storyboard_page.py` → `dist/storyboard/` | Storyboard en page web (vignettes, générique 720p, notes sans tarifs) à partager avec l'équipe | — |
| `accueil/index.html` → `outils/generer_accueil.py` → `dist/accueil/` | **Prototype « Accueil Saison 1 »** : parcours de l'invité (QR, fiche, place sur plan, affiche, e-mails H-5 et retard, arrivée, village IA avec passeport, J+1) et la régie technique ; polices embarquées, aucun service tiers | — |
| Base Airtable « YEBA — Saison 1 · Accueil des invités » (`app3Kv7p5WOhut5Un`) | Invités, Groupes, Places, Épisodes, Accroches, Stands, Sondage, Paramètres ; aucune donnée personnelle à ce stade | Airtable |
| `accueil/schema_saison1.json` · `outils/migrer_vers_baserow.py` | Schéma commun Airtable / Baserow ; migration en une commande (essai à blanc par défaut, `--creer`, `--copier-airtable`) | Baserow |

## Mode d'emploi (10 minutes)

1. Installer **Montserrat** (`assets/fonts/*.ttf`, licence OFL) : double-clic → Installer.
2. Ouvrir `dist/YEBA_Soiree_Lancement.pptx` avec **Microsoft 365 ou PowerPoint 2019+** (Morphose ; sinon fondu).
3. Facultatif : `Alt + F11` → Importer `vba/YebaAnimations.bas` → `Alt + F8` → **YebaVerifier** (rapport complet).
4. Les post-it **rouges à droite des slides** (hors champ, jamais projetés) listent ce qu'il reste à confirmer.
5. Diaporama en **mode Présentateur**. Le générique et les cartes d'épisode avancent seuls ; tout le reste au clic.
6. **Répétition sur place** : son du générique (vidéoprojecteur + enceintes), fluidité des fonds vidéo sur le PC de
   la salle. Si ça saccade : `YebaModeSobre` ou la version `_SOBRE`.

Modifier un texte : éditer `contenu/slides.json`, puis `bash build_all.sh` (PPTX × 2, HTML, storyboard, Felo,
Slides.com, PDF se mettent à jour ensemble ; `--videos` pour régénérer musique et vidéos).

## Déroulé de la saison

| Épisode | Contenu | Moments forts |
|---|---|---|
| Accueil | Pré-show en boucle | Logo, champ d'étoiles, « la soirée commence dans quelques instants » |
| Générique | 80 s : La Réunion → YEBA → le baobab → le chemin 2021-2026 → 3 métiers → 11 formations → Qualiopi · NDA · 7 h/jour → logo | Cœur qui bat, odomètre des années, montage des formations sur le tempo, onde de choc finale |
| 1 · Le casting | Les 3 intervenants, les certifications | Cartes en cascade ; « Certifié. Pas autoproclamé. » |
| 2 · Les racines | « Ko yeba », YEBA → Y (Morphose par caractère), le baobab, 5 valeurs, le chemin | Le Y devient l'arbre ; le baobab se dessine en vidéo |
| 3 · La promesse | 3 métiers, **nos offres**, **la journée 7 h**, **Qualiopi + NDA**, **vos avantages**, souveraineté | Le soleil traverse la journée 08h30 → 16h30 ; sceau doré derrière Qualiopi ; carrousel des avantages |
| 4 · L'atelier | Carte des 11 formations → zoom sur 4 fiches → démo live → « À suivre… » | Zoom avant / arrière entre la carte et chaque fiche ; teaser des **avantages à venir** |
| 5 · 6 · 7 | Outils · Diagnostic · Final (masqués) | Cartes d'épisode prêtes |

## Ce qui a été ajouté à votre demande

- **Les offres** (S17) : inter (catalogue), intra (sur-mesure), séminaire dirigeants résidentiel (mis en avant),
  implémentation IA (workflows, sites), conseil & audit RGPD · IA Act. Tarifs jamais projetés (décision du 10/11/2026).
- **Qualiopi + NDA** (S19 et générique) : certificat Qualiopi n° 25FOR02027.1 (actions de formation, Qualitia, accrédité
  COFRAC), NDA n° 04973676397 (Préfet de La Réunion) avec la mention obligatoire « Cet enregistrement ne vaut pas agrément
  de l'État », et le bandeau « Condition de prise en charge OPCO ».
- **Les horaires** (S18 et générique) : 08h30-12h00 / 13h00-16h30 = 7 h par jour, inscription 15 jours ouvrés avant.
- **Les avantages** : ceux déjà garantis (S20-S21 : dossier OPCO monté avec vous, devis sous 5 jours ouvrés, paiement
  OPCO direct en subrogation, 8 stagiaires maximum, attestations sous 15 jours, référent handicap) et **ceux à venir**
  (S32 « À suivre… » : Assistant IA perso). L'espace en ligne et l'émargement numérique ne sont pas annoncés : ils seront
  ajoutés quand ils existeront dans Airtable (décision du 10/11/2026).
- **La vidéo de motion design** : le générique, 7 cartes d'épisode, 9 fonds vivants, une boucle d'accueil.

## Bible motion design (tenue partout)

Une seule chronologie (`remotion/src/timeline.json`) partagée par l'image et la musique · courbes « expo » pour les
entrées, jamais linéaires · 3 objets en mouvement au maximum · fonds lents et sombres sous le texte · étoiles et halo
en parallaxe d'une slide à l'autre (Morphose) · **aucun trait ne traverse un mot** (constellations, anneaux, flux et
reflets dorés passent hors des textes ou sous des panneaux opaques) · titres ≥ 54 pt, texte ≥ 24 pt (22 pt
seulement sur la carte du catalogue) · 20 mots projetés au maximum par slide (exceptions : couverture, sommaire,
carte du catalogue, horaires, mention légale) · aucune césure, espaces insécables à la française.

## Sources

- Histoire, valeurs, slogan : document de marque « YEBA FORMATIONS » (pièce jointe fournie).
- Base Airtable « YEBA FORMATIONS - Centre de formation (Adaptable) », consultée le 10/11/2026 :
  *CATALOGUE FORMATIONS* (intitulés, durées, statuts, FOR-0017 « En développement ») ; *CONFIG SYSTÈME* (horaires
  modifiés le 07/10/2026, NDA, Qualiopi, barèmes) ; *DOCUMENTS OFFICIELS* YEBA-DOC-13 « Notice des financements
  mobilisables » v1.0 §5 et §7 (engagements de service) ; *STUDIO — FEUILLE DE ROUTE* (éléments « Prévu »).
- Code du travail, art. L.6352-12 (mention NDA) et L.6316-1 (Qualiopi, condition des financements publics ou mutualisés).
- Code de la consommation, art. L.121-2 (pratiques commerciales trompeuses) ; CGI art. 293 B (TVA non applicable).
- Illustrations, pictogrammes, calques et musique : produits par script dans ce dépôt (aucun droit tiers).

## ⚖️ RGPD / IA Act — à traiter avant la soirée

| Point | Texte | Action |
|---|---|---|
| Clips Grok (xAI) : Introduction, IA, AI, Conclusion | **IA Act art. 50** + conditions d'utilisation xAI | Dire à l'oral qu'ils sont générés par IA ; vérifier l'usage commercial autorisé |
| Générique, épisodes, fonds | IA Act : non concerné | Fabriqués par programme (Remotion), sans IA générative ; musique synthétisée |
| Photos de Stan et Antho (initiales pour l'instant) | RGPD + droit à l'image | Accord écrit avant projection ou diffusion |
| Liste d'invités, émargement de la soirée | RGPD art. 5, 6, 13 | Finalité, base légale, durée de conservation, mention d'information |
| Espace en ligne et émargement numérique (à venir, non annoncés) | RGPD art. 5, 28, 30 ; C. conso L.121-2 | Le jour où ils existent : hébergement UE, registre (YEBA-DOC-16), durée de conservation |
| Storyboard en ligne (page privée claude.ai, hors UE) | RGPD (minimisation) | Aucun tarif, aucune coordonnée, aucune donnée de client ; partage limité à l'équipe |
| « Souveraineté par défaut » (S22) | RGPD chap. V | Vrai une fois la migration vers des outils UE terminée (Brevo, Baserow/OVHcloud) |
| Démo live (S31) | RGPD + IA Act art. 50 | Entreprise fictive ou accord écrit ; annoncer que le site est généré par IA |
| Felo Slides, Slides.com | RGPD art. 28 et chap. V | Contenu public uniquement, jamais de données de clients ou de stagiaires |
| Site d'inscription (QR) : fiche invité | RGPD art. 5, 6, 13 | 4 champs obligatoires ; mention d'information à l'écran ; adresse de contact à ajouter ; effacement à 3 mois (proposition à valider) |
| Base Airtable de la soirée (États-Unis) | RGPD chap. V, art. 28 et 30 | Transfert hors UE à inscrire au registre, base légale du transfert à vérifier dans le contrat Airtable ; aucun champ IA d'Airtable utilisé ; migration Baserow prête (`outils/migrer_vers_baserow.py`) |
| Passeport du village IA, rencontres ciblées | RGPD art. 5-1-c, 6-1-a | Tampons gardés sur le téléphone (aucun suivi des déplacements) ; rencontres sur case décochée par défaut, prénom et entreprise seulement |
| Case « place facile d'accès » | RGPD art. 9 (donnée pouvant révéler un handicap) | Facultative, consentement explicite par la case, utilisée pour le seul placement, effacée à J+1 |
| Prénoms des accompagnants | RGPD art. 14 | Prénom seul et facultatif ; information remise à l'arrivée |
| Mur d'étoiles (prénom projeté) | RGPD art. 6-1-a | Case décochée par défaut ; sans case cochée, étoile anonyme |
| Accroches d'affiche, résumés « Précédemment », récap J+1 | IA Act art. 50 (transparence) ; RGPD art. 28 | Textes écrits avec Mistral et relus ; aucune donnée personnelle envoyée à l'IA ; mention « écrit avec l'IA » |
| Placement automatique des sièges | IA Act, considérant 12 | Règles fixes : ce n'est pas de l'IA, ne pas le présenter comme tel (C. conso L.121-2) |
| Captation de la soirée pour le récap J+1 | RGPD art. 13 | Annoncer la captation au public ; ne transcrire que les intervenants |
| Aucune formation RNCP/RS | C. conso L.121-2 | Ne jamais dire « finançable CPF » ni « formation obligatoire » |

## À confirmer par vous

- [ ] Date et lieu (S01) · rôles de Stan et d'Antho + photos (S04)
- [ ] Certificat Qualiopi 25FOR02027.1 (confirmé le 10/11/2026) : validité au 16/02/2027 d'après Airtable → renouvellement à anticiper
- [ ] Le logo officiel Qualiopi (fourni par Qualitia) peut remplacer le mot « QUALIOPI » en S19, avec sa mention d'usage
- [x] Licence Remotion : YEBA FORMATIONS compte 1 personne (réponse du 10/11/2026) → licence gratuite (jusqu'à 3 salariés) ; à revoir si l'équipe dépasse 3 personnes
- [x] Prix : jamais projetés, ni à l'épisode 3 ni à l'épisode 6 (décision du 10/11/2026) ; repères oraux dans les notes de S17
- [x] FOR-0011 : 2 jours (14 h) — fiche Airtable remise en cohérence le 10/11/2026 (sauvegarde : `../airtable-sauvegardes/`)
- [x] FOR-0011 validée par Aurélien LUMEKA (10/11/2026) ; correspondance quiz / objectifs remise en O1 à O10 → régénérer les PDF joints à la fiche
- [x] Autres programmes : horaires laissés tels quels (décision du 10/11/2026)
- [ ] Photo du plan d'évacuation (non reçue) · Wi-Fi / 4G de la salle · adresse de contact RGPD · offre soirée (5 propositions) · outil de la démo live · budget cadeaux
