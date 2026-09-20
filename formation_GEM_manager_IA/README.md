# Formation 1 jour — « Manager aujourd'hui : posture et intelligence artificielle »

Kit pédagogique complet, prêt à animer. Commanditaire : **GEM Formation**.

| | |
|---|---|
| **Modalité** | Formation **à distance** (classe virtuelle synchrone) |
| **Horaires** | **9h00 → 17h00**, déjeuner 12h30-13h30, pauses 15 min à 10h30 et 15h15 |
| **Durée** | **7 h 00** (9h-17h moins l'heure de déjeuner), pauses incluses |
| **Public** | Stagiaires du TP **Manager d'Établissement Marchand** (MEM), RNCP41853, niveau 5 |
| **Matin** | 9h20-12h30 — La psychologie du dirigeant |
| **Après-midi** | 13h30-17h00 — IA et responsabilité en entreprise |

Le matin nourrit le **bloc 1 du titre** (« manager l'équipe de son périmètre »).
L'après-midi est un apport transverse qui s'y rattache par deux compétences du
bloc 1 : lutter contre les discriminations (biais algorithmiques) et organiser
la sécurité au travail.

## Contenu du kit

| Dossier | Fichier | Usage |
|---|---|---|
| `01_diaporama` | `Diaporama_Manager_et_IA_GEM.pptx` | 73 diapositives, écrit gros, contrastes vérifiés |
| `02_videos` | `Video_1_Les_trois_positions_du_manager.html` | 2 min 30 — navigateur, hors ligne |
| `02_videos` | `Video_2_La_pyramide_des_risques_IA_Act.html` | 2 min 55 — idem |
| `02_videos` | `Scripts_voix_off_videos_1_et_2.pdf` | Texte minuté à dire pendant la diffusion |
| `03_jeux` | `Kit_jeux_et_exercices.pdf` | 8 jeux **conçus pour la visio**, corrigés, variantes de repli |
| `04_grilles_evaluation` | `Grille_evaluation_1_Posture_manageriale.pdf` | Jeu « Le brief de 8h » — 7 critères /21 |
| `04_grilles_evaluation` | `Grille_evaluation_2_Usage_responsable_IA.pdf` | Atelier « Mon chantier IA » — 7 critères /21 |
| `05_quiz_stagiaires` | `Quiz_1_...pdf` / `Quiz_2_...pdf` | 10 questions, 10 min |
| `05_quiz_stagiaires` | `Feuille_reponses_Quiz_1.pdf` / `..._2.pdf` | **PDF remplissable à l'écran**, à renvoyer |
| `06_corriges` | `CORRIGE_Quiz_1_...pdf` / `CORRIGE_Quiz_2_...pdf` | **Feuilles distinctes** — ne pas distribuer |
| `07_fiches_ressources` | `Fiche_ressource_1_...pdf` / `..._2_...pdf` | Remises aux stagiaires, sources citées |
| `08_conducteur` | `Conducteur_animation_journee.pdf` | Déroulé minuté, checklist J-7/J-1/J, plan B technique |
| `09_dispositif_distance` | `Dispositif_a_distance_et_conformite.pdf` | FOAD, traçabilité, qualité, RGPD visio, souveraineté |

## Charte graphique

Tout part de `_build/charte.py` (ou `_build/charte.json`). Pour appliquer
la charte GEM Formation :

```bash
cd _build
python3 extraire_charte.py ../charte/logo_gem.png      # depuis le logo
python3 extraire_charte.py --couleurs "#0B4F8A" "#E2001A"   # ou à la main
python3 build_deck.py && for f in doc_*.py feuille_reponses.py; do python3 $f; done
```

Le script **assombrit automatiquement** une couleur de marque trop claire
jusqu'à obtenir un contraste conforme, et refuse de générer si l'accessibilité
n'est pas atteinte. Le vert et le rouge restent sémantiques (validation /
interdit) : ils portent du sens pédagogique, pas de l'identité.

## Accessibilité (public malvoyant, à distance)

Le diaporama applique et **vérifie automatiquement** :
- titres 40 pt, corps 28 pt (jamais sous 24 pt), police Verdana ;
- contrastes ≥ 4,5:1 (WCAG 2.1 AA) sur tous les couples texte/fond ;
- mots-clés, pas de phrases ; aucune ligne ne coupe un mot ; aucun texte hors cadre.

Contrôle bloquant : `python3 _build/build_deck.py` échoue si une règle est violée.

**À distance, le point décisif** : envoyer le diaporama en PDF à J-7. Le partage
d'écran compresse l'image et ruine le travail fait sur la taille des caractères.

## Points à valider avant la session

1. **Charte GEM Formation** : leur site n'est pas accessible depuis
   l'environnement de génération. Fournir le logo ou les codes hexadécimaux.
2. **Effectif** : le kit fonctionne de 6 à 16 stagiaires. Hors de cette plage,
   voir les arbitrages dans `09_dispositif_distance`.
3. **Outil de visio** : salles séparées, sondage et message privé sont utilisés.
4. **Référentiel TP MEM** : aligner les grilles sur la version en vigueur
   (arrêté du 4 décembre 2025) — non téléchargeable depuis cet environnement.
5. **Références réglementaires** : à revérifier à la date de la session.
   Le calendrier de l'IA Act peut évoluer.
