# Versions smartphone 2026 — YEBA FORMATIONS

Format écran de téléphone **1080 × 1920 px (9:16)**, lisible sans zoom (texte courant ≥ 29 px, prix ≥ 40 px), fonds identiques aux versions A4 et animées.

| Fichier | Contenu | Pour l'envoyer |
|---|---|---|
| `grille-tarifaire/YEBA-grille-tarifaire-2026-smartphone.pdf` | 4 écrans : couverture, pôles 01-02, pôles 03-04, conseil + modalités + contact | PDF à faire défiler (WhatsApp « Document », e-mail, Olvid, AirDrop) |
| `grille-tarifaire/images/ecran-01…04.jpg` | les mêmes écrans en images | Statut WhatsApp, story, message |
| `catalogue/YEBA-catalogue-2026-smartphone.pdf` | 18 écrans : couverture, sommaire, 1 écran par formation et par service, format intra, parcours, contact | PDF à faire défiler |
| `grille-tarifaire/YEBA-grille-tarifaire-2026-smartphone-anime.mp4` | Version animée : 1080 × 1920, 31 s, 4,4 Mo — défilement façon « story », couverture IA animée | Statut WhatsApp, story Instagram/Facebook, Reels, envoi direct |
| `grille-tarifaire/…-anime-leger.mp4` | Même vidéo en 720 × 1280, 1,4 Mo | Messageries, réseau mobile faible |
| `catalogue/YEBA-catalogue-2026-smartphone-anime.mp4` | Version animée : 1080 × 1920, 1 min 59, 17 Mo — 18 écrans, dernier écran avec le logo dans le couloir | Envoi direct, YouTube Shorts, salon sur tablette verticale |
| `catalogue/…-anime-leger.mp4` | Même vidéo en 720 × 1280, 5 Mo | WhatsApp, Olvid, e-mail |
| `catalogue/images/ecran-01…18.jpg` | les mêmes écrans en images | Envoyer seulement la fiche qui intéresse le prospect |

## Sources
Mêmes données que le catalogue A4 (`livrables/catalogue-2026`) : base Airtable « YEBA FORMATIONS », CATALOGUE FORMATIONS, CONFIG SYSTÈME, YEBA-DOC-03 (CGV v1.1), YEBA-DOC-12 (politique tarifaire v3.1), charte YEBA-IDENT-2026.

## Régénérer
Copier `source/` dans le dossier source du catalogue (qui contient `gen.py`, les polices et les images), puis : `python3 mobile.py && node rmobile.mjs` (PDF et images) ; `python3 manim.py && node capm.mjs grille_mobile && node capm.mjs catalogue_mobile`, puis ffmpeg (H.264, yuv420p, +faststart) pour les vidéos.
Les statuts WhatsApp sont limités à 60 s par séquence : le catalogue animé (2 min) y sera découpé automatiquement — préférer la grille animée (31 s) pour un statut.
Le script de rendu resserre automatiquement une fiche trop longue et signale tout élément hors écran.
