# Plan de montage Slides.com

Slides.com est l'éditeur en ligne bâti sur Reveal.js (même moteur que `revealjs/index.html`).
Deux voies, de la plus fidèle à la plus souple :

1. **Importer** `dist/YEBA_Soiree_Lancement.pdf` ou le `.pptx` via le menu d'import de Slides.com
   (disponibilité selon votre offre : à vérifier dans votre compte).
2. **Reconstruire** chaque slide avec le plan ci-dessous, puis activer *Auto-Animate* entre slides
   consécutives et donner le même *Animation ID* aux éléments qui doivent glisser (équivalent Morphose).

Réglages d'identité (Theme → Custom CSS) : fond `#121212`, texte `#FFFFFF`, accent `#C9A84C`,
police Montserrat. Copier le bloc CSS de `revealjs/build_reveal.py` (variable `CSS`) pour un rendu identique.

> ⚖️ RGPD : Slides.com héberge vos présentations en ligne. Vérifier la localisation des serveurs et le
> contrat de sous-traitance (art. 28 RGPD) avant d'y déposer autre chose que ce contenu public.
> Garder la présentation **privée** tant que les champs [DATE], [LIEU] et les rôles ne sont pas validés.

| Slide | Texte projeté | Animation à régler |
|---|---|---|
| V1 | Vidéo — Introduction | Lecture automatique à l'arrivée sur la slide (réglée par la macro VBA), une seule fois, son inclus. Transition Fondu en entrée, Morphose vers la slide suivante. |
| S01 | SOIRÉE DE LANCEMENT Sous le baobab de la connaissance, les graines du savoir. [DATE] · [LIEU] · La Réunion | Précédée de la vidéo Remotion « yeba-intro.mp4 » (10 s) en plein écran. Transition Morphose vers S02 : le logo rétrécit et file en haut à gauche. |
| S02 | CE SOIR Moins de bruit sur l'IA. Plus de décisions. | Morphose (le logo arrive en haut à gauche). Ligne 1 en fondu, ligne 2 en or 0,6 s après (VBA). |
| S03 | Le fil de la soirée Présentation Histoire L'offre YEBA Nos formations Applications & sites web Audit & devis Mot de fin — offre soirée | Morphose. Ce même slide revient à chaque changement de partie : le marqueur or glisse sur l'étape suivante (effet « GPS »). |
| S04 | 3 visages. 1 mission. Aurélien LUMEKA Directeur · IA & gouvernance Stan [Rôle à préciser] Antho [Rôle à préciser] | Morphose. Cartes en apparition échelonnée gauche → droite (VBA, 0,3 s d'écart). Chaque intervenant prend la parole quand sa carte apparaît. |
| S05 | Certifié. Pas autoproclamé. Qualiopi Google AI Specialist Google Professional AI SecNumacadémie ANSSI MOOC CNIL — RGPD Référent handicap | Morphose. Pastilles en zoom léger, une par une (VBA). |
| S06 | Le fil de la soirée Présentation Histoire L'offre YEBA Nos formations Applications & sites web Audit & devis Mot de fin — offre soirée | Morphose : le marqueur glisse de « Présentation » à « Histoire ». |
| S07 | Pas de mot pour « formation ». Alors maman a dit : Ko yeba. Le savoir. | Morphose depuis l'agenda. Ligne or en machine à écrire (Reveal.js) / fondu mot à mot (VBA). Suspense : le mot YEBA n'est révélé qu'à la slide suivante. |
| S08 | YEBA « Savoir, connaître » — en lingala | Morphose. Le mot YEBA arrive en zoom depuis le centre ; à la slide suivante, E, B et A s'effacent et le Y reste (Morphose par caractère). |
| S09 | Y L'arbre de la connaissance L'arbre à palabres | Morphose depuis le mot YEBA : les lettres E, B, A s'effacent, le Y reste et grandit. Étiquettes en apparition gauche puis droite. |
| S10 | Sous le baobab, on transmet. Histoires · Vérités · Générations | Morphose. Le baobab « pousse » (entrée par le bas, VBA « Balayer vers le haut »). |
| S11 | Des racines. Un réseau. HÉRITAGE Afrique Baobab Transmission MODERNITÉ IA Réseau Pitons 974 | Morphose : les deux moitiés glissent l'une vers l'autre et l'emblème se pose au centre. |
| S12 | 5 valeurs Transmission vivante Bienveillance engagée Allégresse & énergie Élévation collective Authenticité enracinée | Morphose. Chaque valeur apparaît au clic (VBA : apparition au clic, pas automatique) pour que l'orateur la commente. |
| S13 | Le chemin Avril 2021 Création 2021 → 2025 Vente · Management · Soft skills 2026 IA · RGPD · IA Act Ce soir Nouvelle équipe | Morphose. La ligne or se trace de gauche à droite (VBA « Balayer »), les jalons s'allument un à un. |
| S14 | Le fil de la soirée Présentation Histoire L'offre YEBA Nos formations Applications & sites web Audit & devis Mot de fin — offre soirée | Morphose : le marqueur glisse. |
| V2 | Vidéo — Intelligence artificielle | Lecture automatique à l'arrivée sur la slide (réglée par la macro VBA), une seule fois, son inclus. Transition Fondu en entrée, Morphose vers la slide suivante. |
| S15 | QUESTION Vos équipes utilisent déjà l'IA. Avec quelles données ? | Morphose. Silence de 3 secondes avant la ligne or (apparition au clic). |
| S16 | 3 métiers. 1 seul interlocuteur. Former Intra · Inter · Séminaires Implémenter Workflows · Sites · Applications Sécuriser RGPD · IA Act · Audit | Morphose. Colonnes en entrée échelonnée par le bas (VBA). |
| S17 | 8 h par journée de formation. Le standard du marché : 7 h. | Morphose. Le chiffre compte de 7 à 8 (compteur Reveal.js / vidéo Remotion) ; en PowerPoint, zoom d'entrée. |
| S18 | Chez vous. Chez nous. Ou au vert. Intra Dans vos locaux Inter Multi-entreprises Séminaire Dirigeants · Résidentiel Sur-mesure Votre besoin | Morphose. Tuiles en « rebond » léger (VBA). |
| S19 | NOTRE LIGNE Souveraineté par défaut. Outils européens d'abord. | Morphose. Les 12 points or se placent en cercle (VBA : apparition « Roue »). |
| S20 | NOTRE PROMESSE Nous ne vendons pas la conformité. Nous vous aidons à la prouver. | Morphose. Ligne 1 en fondu ; ligne 2 en fondu lent (1,2 s) au clic suivant. |
| S21 | Le fil de la soirée Présentation Histoire L'offre YEBA Nos formations Applications & sites web Audit & devis Mot de fin — offre soirée | Morphose : le marqueur glisse. Option : insérer ici la vidéo Remotion « yeba-transition-formations.mp4 ». |
| V3 | Vidéo — AI | Lecture automatique à l'arrivée sur la slide (réglée par la macro VBA), une seule fois, son inclus. Transition Fondu en entrée, Morphose vers la slide suivante. |
| S22 | L'IMAGE À RETENIR Votre entreprise est un moteur. Nos formations en sont les pièces. | Morphose. L'aiguille de la jauge monte (VBA : rotation 120°). |
| S23 | Le garage YEBA ALLUMAGE-TURBO PILOTE AUTOMATIQUE COPILOTE MOTEUR FERMÉ CARROSSERIE INJECTION RÉGLAGE MOTEUR CONTRÔLE TECHNIQUE TABLEAU DE BORD TRACTION EMBRAYAGE SUR-MESURE | Morphose. Chaque tuile porte un nom !!tuile-XXX : sur les 4 slides suivantes, la tuile concernée s'agrandit jusqu'à devenir la slide (zoom Morphose). |
| S24 | Comprendre. Produire. Prouver. J1 · Bien demander J2 · Produire J3 · Automatiser & prouver 3 jours · 24 h 4 à 10 pers. Inter | Morphose (zoom depuis la tuile). Les 3 jours apparaissent comme les rapports d'une boîte de vitesses (VBA échelonné). |
| S25 | Des agents IA. Sous contrôle humain. Autonomie mesurée Traçabilité Arrêt d'urgence 2 jours · 16 h 4 à 8 pers. Avancé | Morphose (zoom depuis la tuile). |
| S26 | Votre site internet. À la voix. En 1 jour. Dicter Corriger Publier conforme 1 jour · 8 h Intra Sans code | Morphose (zoom depuis la tuile). Onde sonore animée (Reveal.js / Remotion). |
| S27 | Des emails qui obtiennent une réponse. Segmenter Rédiger avec l'IA Mesurer 1 jour · 8 h Intra RGPD inclus | Morphose (zoom depuis la tuile). |
| S28 | DÉMO LIVE Un site internet. Dicté. Devant vous. | Morphose. Puis bascule vers l'écran de démonstration. |
| S29 | ET MAINTENANT Former, c'est bien. Équiper, c'est mieux. | Morphose vers l'agenda (marqueur sur « Applications & sites web »). |
