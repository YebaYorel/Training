# Versions smartphone 2026 — YEBA FORMATIONS

Format écran de téléphone **1080 × 1920 px (9:16)**, lisible sans zoom (texte courant ≥ 29 px, prix ≥ 40 px), fonds identiques aux versions A4 et animées.

| Fichier | Contenu | Pour l'envoyer |
|---|---|---|
| `grille-tarifaire/YEBA-grille-tarifaire-2026-smartphone.pdf` | 4 écrans : couverture, pôles 01-02, pôles 03-04, conseil + modalités + contact | PDF à faire défiler (WhatsApp « Document », e-mail, Olvid, AirDrop) |
| `grille-tarifaire/images/ecran-01…04.jpg` | les mêmes écrans en images | Statut WhatsApp, story, message |
| `catalogue/YEBA-catalogue-2026-smartphone.pdf` | 18 écrans : couverture, sommaire, 1 écran par formation et par service, format intra, parcours, contact | PDF à faire défiler |
| `catalogue/images/ecran-01…18.jpg` | les mêmes écrans en images | Envoyer seulement la fiche qui intéresse le prospect |

## Sources
Mêmes données que le catalogue A4 (`livrables/catalogue-2026`) : base Airtable « YEBA FORMATIONS », CATALOGUE FORMATIONS, CONFIG SYSTÈME, YEBA-DOC-03 (CGV v1.1), YEBA-DOC-12 (politique tarifaire v3.1), charte YEBA-IDENT-2026.

## Régénérer
Copier `source/` dans le dossier source du catalogue (qui contient `gen.py`, les polices et les images), puis : `python3 mobile.py && node rmobile.mjs`.
Le script de rendu resserre automatiquement une fiche trop longue et signale tout élément hors écran.
