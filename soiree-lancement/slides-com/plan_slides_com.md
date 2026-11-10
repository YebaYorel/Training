# Plan de montage Slides.com — « YEBA — Saison 1 »

Slides.com est l'éditeur en ligne bâti sur Reveal.js (même moteur que `revealjs/index.html`).
Deux voies, de la plus fidèle à la plus souple :

1. **Importer** `dist/YEBA_Soiree_Lancement.pdf` (images figées) ou le `.pptx` via le menu d'import de Slides.com
   (disponibilité selon votre offre : à vérifier dans votre compte). Les vidéos (générique, épisodes, fonds) ne
   sont pas reprises par l'import PDF : les ajouter comme *background video* depuis `dist/videos/`.
2. **Reconstruire** chaque slide avec le plan ci-dessous, puis activer *Auto-Animate* entre slides
   consécutives et donner le même *Animation ID* aux éléments qui doivent glisser (équivalent Morphose).

Réglages d'identité (Theme → Custom CSS) : fond `#121212`, texte `#FFFFFF`, accent `#C9A84C`,
police Montserrat. Copier le bloc CSS de `revealjs/build_reveal.py` (variable `CSS`) pour un rendu identique.

> ⚖️ RGPD : Slides.com héberge vos présentations en ligne. Vérifier la localisation des serveurs et le
> contrat de sous-traitance (art. 28 RGPD) avant d'y déposer autre chose que ce contenu public.
> Garder la présentation **privée** tant que la date, le lieu et les rôles ne sont pas validés.
> ⚖️ IA Act (art. 50) : les 4 clips générés par IA (Grok) doivent rester signalés comme contenus générés par IA.

| Slide | Texte projeté | Fond / vidéo | Animation à régler |
|---|---|---|---|
| P00 | *(vidéo plein écran)* | `dist/videos/yeba-preshow.mp4` | Lecture automatique en boucle, sans son. Le présentateur passe à la suite quand la salle est installée. |
| G01 | *(vidéo plein écran)* | `dist/videos/yeba-saison1-generique.mp4` | Lecture automatique, son inclus, passage automatique à la slide suivante à la fin. |
| V01 | *(vidéo plein écran)* | `assets/videos/clip-introduction.mp4` | Lecture automatique, passage automatique à la fin. |
| S01 | SAISON 1 · SOIRÉE DE LANCEMENT · Sous le baobab de la connaissance, · les graines du savoir. · [DATE À PRÉCISER] · [LIEU À PRÉCISER] · La Réunion | `dist/videos/fond-cover.mp4` | Fond vivant en boucle. Slogan en fondu montant. Morphose : le logo file en bas à droite sur la slide suivante. |
| S02 | CE SOIR · Moins de bruit sur l'IA. · Plus de décisions. | `dist/videos/fond-ambiance-noir.mp4` | Ligne 1 en fondu montant, ligne 2 (or) 0,4 s après. |
| S03 | Saison 1 · 7 épisodes · Le casting — Présentation · Les racines — Histoire · La promesse — L'offre YEBA · L'atelier — Nos formations · Les outils — Applications & sites web · Le diagnostic — Audit & devis · Le final — Mot de fin & offre soirée | `dist/videos/fond-ambiance-noir.mp4` | Cette slide revient avant chaque épisode : la Morphose fait glisser le repère or et change le grand numéro (effet « GPS »). |
| E1 | *(vidéo plein écran)* | `dist/videos/yeba-episode-1.mp4` | Lecture automatique avec sting sonore, passage automatique. |
| S04 | 3 visages. · 1 mission. · Aurélien LUMEKA · Directeur · IA & gouvernance · Stan · [Rôle à préciser] · Antho · [Rôle à préciser] | `dist/videos/fond-ambiance-noir.mp4` | Cartes en fondu montant, décalées de 0,15 s. |
| S05 | Certifié. · Pas autoproclamé. · Google AI Specialist · Google Professional AI · SecNumacadémie ANSSI · MOOC CNIL — RGPD · Référent handicap | `dist/videos/fond-ambiance-noir.mp4` | Pastilles en zoom léger, une par une. |
| S06 | Saison 1 · 7 épisodes · Le casting — Présentation · Les racines — Histoire · La promesse — L'offre YEBA · L'atelier — Nos formations · Les outils — Applications & sites web · Le diagnostic — Audit & devis · Le final — Mot de fin & offre soirée | `dist/videos/fond-ambiance-noir.mp4` | Morphose : le repère glisse. |
| E2 | *(vidéo plein écran)* | `dist/videos/yeba-episode-2.mp4` | Lecture automatique, sting, passage automatique. |
| S07 | Pas de mot pour « formation ». · Alors maman a dit : Ko yeba. Le savoir. | `dist/videos/fond-ambiance-terre.mp4` | Ligne blanche puis ligne or, en fondu lent. |
| S08 | YEBA · « Savoir, connaître » — en lingala | `dist/videos/fond-ambiance-terre.mp4` | Zoom d'entrée ; à la slide suivante, Morphose par caractère : E, B, A s'effacent, le Y reste. |
| S09 | Y · L'arbre de la connaissance · L'arbre à palabres | `dist/videos/fond-ambiance-terre.mp4` | Morphose par caractère depuis YEBA ; étiquettes en fondu gauche puis droite. |
| S10 | Sous le baobab, · on transmet. · Histoires · Vérités · Générations | `dist/videos/fond-baobab.mp4` | Le baobab pousse (vidéo 6 s, image finale tenue), texte en fondu montant synchronisé. |
| S11 | Des racines. · Un réseau. · HÉRITAGE · Afrique · Baobab · Transmission · MODERNITÉ · IA · Réseau · Pitons 974 | `dist/videos/fond-ambiance-terre.mp4` | Les mots montent colonne par colonne ; l'emblème apparaît en dernier. |
| S12 | 5 valeurs · Transmission vivante · Bienveillance engagée · Allégresse & énergie · Élévation collective · Authenticité enracinée | `dist/videos/fond-ambiance-terre.mp4` | Une valeur par clic, pour la commenter. |
| S13 | Le chemin · Avril 2021 · Création · 2021 → 2025 · Vente · Management · Soft skills · 2026 · IA · RGPD · IA Act · Ce soir · Nouvelle équipe | `dist/videos/fond-ambiance-terre.mp4` | La ligne se trace de gauche à droite, les jalons s'allument un à un. |
| S14 | Saison 1 · 7 épisodes · Le casting — Présentation · Les racines — Histoire · La promesse — L'offre YEBA · L'atelier — Nos formations · Les outils — Applications & sites web · Le diagnostic — Audit & devis · Le final — Mot de fin & offre soirée | `dist/videos/fond-ambiance-noir.mp4` | Morphose : le repère glisse. |
| E3 | *(vidéo plein écran)* | `dist/videos/yeba-episode-3.mp4` | Lecture automatique, sting, passage automatique. |
| V02 | *(vidéo plein écran)* | `assets/videos/clip-intelligence-artificielle.mp4` | Lecture automatique, passage automatique. |
| S15 | QUESTION · Vos équipes utilisent déjà l'IA. · Avec quelles données ? | `dist/videos/fond-flux.mp4` | Ligne 1 automatique ; ligne or au clic, après 3 secondes de silence. |
| S16 | 3 métiers. · 1 seul interlocuteur. · Former — Intra · Inter · Séminaires · Implémenter — Workflows · Sites · Applications · Sécuriser — RGPD · IA Act · Audit | `dist/videos/fond-ambiance-noir.mp4` | Colonnes en fondu montant décalé. |
| S17 | Nos offres. · Votre format. · Inter — Catalogue · Intra — Sur-mesure · Séminaire dirigeants — Résidentiel · Implémentation IA — Workflows · sites · Conseil & audit — RGPD · IA Act | `dist/videos/fond-ambiance-noir.mp4` | Tuiles en fondu montant décalé de 0,12 s. |
| S18 | UNE JOURNÉE YEBA · 7 h · de formation par jour · Inscription : 15 jours ouvrés avant · Formation · Déjeuner · Formation · 08h30 · 12h00 · 13h00 · 16h30 | `dist/videos/fond-journee.mp4` | Le soleil se lève à 08h30 et se couche à 16h30 (vidéo 6 s, image finale tenue) ; heures en fondu synchronisé. |
| S19 | La confiance · se prouve. · Condition de prise en charge OPCO · QUALIOPI · N° 25FOR02027.1 · Actions de formation · Qualitia (COFRAC) · NDA · N° 04973676397 · Préfet de La Réunion · Cet enregistrement ne vaut pas agrément de l'État. | `dist/videos/fond-sceau.mp4` | Panneaux en fondu montant ; bandeau OPCO en dernier. |
| S20 | Vous formez. · On s'occupe du reste. · Dossier OPCO — monté avec vous · Devis — 5 jours ouvrés · Paiement OPCO — direct (subrogation) | `dist/videos/fond-ambiance-noir.mp4` | Tuiles en fondu montant décalé ; Morphose vers la slide suivante (les tuiles glissent à gauche). |
| S21 | Petit groupe. · Grand suivi. · 8 stagiaires — maximum par session · Attestations — sous 15 jours · Référent handicap — parcours adaptés | `dist/videos/fond-ambiance-noir.mp4` | Morphose depuis 1/2, tuiles en fondu montant décalé. |
| S22 | NOTRE LIGNE · Souveraineté par défaut. · Outils européens d'abord. | `dist/videos/fond-ambiance-noir.mp4` | Ligne 1 puis ligne or. |
| S23 | NOTRE PROMESSE · Nous ne vendons pas la conformité. · Nous vous aidons à la prouver. | `dist/videos/fond-ambiance-noir.mp4` | Ligne 1 puis ligne or en fondu lent. |
| S24 | Saison 1 · 7 épisodes · Le casting — Présentation · Les racines — Histoire · La promesse — L'offre YEBA · L'atelier — Nos formations · Les outils — Applications & sites web · Le diagnostic — Audit & devis · Le final — Mot de fin & offre soirée | `dist/videos/fond-ambiance-noir.mp4` | Morphose : le repère glisse. |
| E4 | *(vidéo plein écran)* | `dist/videos/yeba-episode-4.mp4` | Lecture automatique, sting, passage automatique. |
| V03 | *(vidéo plein écran)* | `assets/videos/clip-ai-or.mp4` | Lecture automatique, passage automatique. |
| S25 | NOTRE MÉTHODE · On ne repart pas avec des notes. · On repart avec un livrable. | `dist/videos/fond-ambiance-bleu.mp4` | Ligne 1 puis ligne or. |
| S26 | 11 formations. · 5 familles. · IA générative au travail · Copilot Microsoft 365 · Agents IA · IA souveraine · Automatisation sans code · Site internet IA · Emailing IA · Conformité RGPD & IA Act · Séminaire dirigeants IA · Vente & négociation · Manager au quotidien · Assistant IA perso | `dist/videos/fond-ambiance-noir.mp4` | Tuiles en cascade (0,06 s). Chaque tuile porte le nom !!tuile-FOR-XXXX : sur les slides suivantes, la tuile s'agrandit en bandeau (zoom Morphose). |
| S27 | Gagner du temps. · En sécurité. Avec des preuves. · IA générative au travail · Demander · Produire · Prouver · 2 jours · 14 h · Inter | `dist/videos/fond-ambiance-noir.mp4` | Morphose (zoom depuis la tuile) ; puces en fondu latéral ; pastilles en zoom. |
| S28 | Déléguer à l'IA. · Sous contrôle humain. · Agents IA · Autonomie mesurée · Traçabilité · Arrêt d'urgence · 2 jours · 14 h · Avancé | `dist/videos/fond-ambiance-noir.mp4` | Morphose depuis la tuile. |
| S29 | Votre site. · À voix haute. En 1 jour. · Site internet IA · Dicter · Corriger · Publier conforme · 7 h · Intra · Sans code | `dist/videos/fond-ambiance-noir.mp4` | Morphose depuis la tuile. |
| S30 | Des emails · qui obtiennent une réponse. · Emailing IA · Segmenter · Rédiger avec l'IA · Mesurer · 1 jour · 7 h · Intra · RGPD inclus | `dist/videos/fond-ambiance-noir.mp4` | Morphose depuis la tuile. |
| S31 | DÉMO LIVE · Un site internet. · Décrit à voix haute. Devant vous. | `dist/videos/fond-ambiance-noir.mp4` | Pastille en pulsation continue ; titre en fondu montant. |
| S32 | PROCHAINEMENT · À suivre… · Assistant IA perso — Nouvelle formation | `dist/videos/fond-bientot.mp4` | Carte en fondu montant ; « À suivre… » scintille. |
| S33 | ET MAINTENANT · Former, c'est bien. · Équiper, c'est mieux. | `dist/videos/fond-ambiance-bleu.mp4` | Ligne 1 puis ligne or ; Morphose vers l'agenda. |
