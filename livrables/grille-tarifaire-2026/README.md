# Grille tarifaire 2026 — YEBA FORMATIONS

| Fichier | Usage |
|---|---|
| `YEBA-grille-tarifaire-2026.pdf` | PDF A4, 2 pages (couverture + tarifs) — pièce jointe, impression |
| `YEBA-tarifs-2026-email.gif` | Version animée **pour le corps du mail** (600 px, 14 s en boucle, 2,3 Mo) |
| `YEBA-tarifs-2026-anime.mp4` | Version animée HD (1280×1920) — WhatsApp, LinkedIn, écran salon |

**Source des prix :** Airtable « YEBA FORMATIONS - Centre de formation (Adaptable) »,
table DOCUMENTS OFFICIELS YEBA, **YEBA-DOC-12 v3.0 du 02/10/2026** (grille arrêtée par le dirigeant).
FOR-0005 et FOR-0007 (marque blanche) et FOR-0001 (archivée) sont exclues.

## À corriger dans Airtable (CATALOGUE FORMATIONS non aligné sur DOC-12 v3.0)
| Fiche | Catalogue (inter / intra par jour) | DOC-12 v3.0 |
|---|---|---|
| FOR-0003 Conformité RGPD & IA Act | 690 € / 2 100 € | 990 € / 2 900 € |
| FOR-0004 Vente & négociation | 690 € / 2 100 € | 690 € / 2 300 € |
| FOR-0008 Manager au quotidien | 790 € / 2 400 € | 690 € / 2 300 € |
| FOR-0011 IA générative au travail | 790 € / 2 400 € | 890 € / 2 700 € |
| FOR-0002 Automatisation sans code | 990 € / 2 900 € | 890 € / 2 700 € |

## Régénérer
Dans `source/` : `npm i playwright @fontsource/montserrat @fontsource/jetbrains-mono`,
puis `node render.mjs .` (PDF) et `node capture.mjs` + ffmpeg (animation ; `LITE=1 FPS=10 DSF=1` pour le GIF e-mail).
