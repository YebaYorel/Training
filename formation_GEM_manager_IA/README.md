# Formation 1 jour — « Manager aujourd'hui : posture et intelligence artificielle »

Kit pédagogique complet, prêt à animer. Commanditaire : **GEM Formation**.
Horaires : **8h00 → 17h00**, déjeuner 12h-13h, pauses de 15 min à 10h et 15h.

- **Matin (8h20-12h00)** — La psychologie du dirigeant
- **Après-midi (13h00-17h00)** — IA et responsabilité en entreprise

## Contenu du kit

| Dossier | Fichier | Usage |
|---|---|---|
| `01_diaporama` | `Diaporama_Manager_et_IA_GEM.pptx` | 69 diapositives, écrit gros (28 pt min.), contrastes WCAG AA |
| `02_videos` | `Video_1_Les_trois_positions_du_manager.html` | 2 min 30 — à ouvrir dans un navigateur, hors ligne |
| `02_videos` | `Video_2_La_pyramide_des_risques_IA_Act.html` | 2 min 55 — idem |
| `02_videos` | `Scripts_voix_off_videos_1_et_2.pdf` | Texte minuté à dire, conseils de diction |
| `03_jeux` | `Kit_jeux_et_exercices.pdf` | 8 jeux, cartes à découper, corrigés animateur |
| `04_grilles_evaluation` | `Grille_evaluation_1_Posture_manageriale.pdf` | Jeu de rôle « La réunion de 9h » — 7 critères /21 |
| `04_grilles_evaluation` | `Grille_evaluation_2_Usage_responsable_IA.pdf` | Atelier « Mon chantier IA » — 7 critères /21 |
| `05_quiz_stagiaires` | `Quiz_1_Psychologie_du_dirigeant.pdf` | 10 questions, 10 min |
| `05_quiz_stagiaires` | `Quiz_2_IA_RGPD_IA_Act.pdf` | 10 questions, 10 min |
| `06_corriges` | `CORRIGE_Quiz_1_...pdf` / `CORRIGE_Quiz_2_...pdf` | **Feuilles distinctes** — à ne pas distribuer |
| `07_fiches_ressources` | `Fiche_ressource_1_Psychologie_du_dirigeant.pdf` | Remise aux stagiaires |
| `07_fiches_ressources` | `Fiche_ressource_2_IA_RGPD_IA_Act.pdf` | Remise aux stagiaires |
| `08_conducteur` | `Conducteur_animation_journee.pdf` | Déroulé minuté, matériel, vigilances |

## Accessibilité (public malvoyant)

Le diaporama applique et **vérifie automatiquement** :
- titres 40 pt, corps 28 pt (jamais sous 24 pt), police Verdana ;
- contrastes ≥ 4,5:1 (WCAG 2.1 AA) sur tous les couples texte/fond ;
- mots-clés, pas de phrases ; aucune ligne ne coupe un mot ; aucun texte hors cadre ;
- alignement à gauche, pas de blocs capitales, pas de texte sur image.

Contrôle : `python3 _build/build_deck.py` échoue si une règle est violée.

## Régénérer les supports

```bash
pip install python-pptx reportlab
cd _build
python3 build_deck.py        # diaporama + contrôle accessibilité
python3 doc_ressource1.py doc_ressource2.py   # (lancer séparément)
python3 doc_quiz.py doc_grilles.py doc_jeux.py doc_conducteur.py doc_videos.py
```

Couleurs : constantes en tête de `_build/deck_engine.py` et `_build/docs_engine.py`
(palette neutre accessible — à remplacer par la charte GEM Formation si elle est fournie).

## Points à valider avant la session

1. **Volume horaire** : la commande indique 7 h ; le créneau 8h-17h moins 1 h de déjeuner
   et 2 pauses de 15 min donne **7 h 30** de face-à-face. À trancher sur la convention.
2. **Charte graphique GEM Formation** : couleurs et logo non fournis — palette neutre appliquée.
3. **Profil des participants** : managers en poste ou futurs responsables ? Le minutage du
   jeu n°4 (nombre de passages) en dépend.
4. **Références réglementaires** : à revérifier à la date de la session (Légifrance,
   Journal officiel de l'UE, CNIL). Le calendrier de l'IA Act peut évoluer.
