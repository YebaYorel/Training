# Grille tarifaire 2026 — YEBA FORMATIONS (mise à jour du 08/10/2026)

| Fichier | Usage |
|---|---|
| `YEBA-grille-tarifaire-2026.pdf` | PDF A4, 2 pages (couverture + tarifs) — pièce jointe, impression |
| `YEBA-tarifs-2026-email.gif` | Version animée **pour le corps du mail** (600 px, 14 s en boucle, 3,3 Mo) — couverture = vidéo « IA » |
| `YEBA-tarifs-2026-anime.mp4` | Version animée HD (1280×1920) — WhatsApp, LinkedIn, écran salon — couverture = vidéo « IA » |

**Source des prix :** Airtable, table CATALOGUE FORMATIONS (champs « Tarif inter HT / jour / personne »
et « Tarif intra HT / jour / groupe »), relevés le 07/10/2026.
Exclues : FOR-0005 et FOR-0007 (marque blanche), FOR-0001 (archivée), FOR-0017 (en développement, retirée sur décision du dirigeant).

**Règles affichées (décision du dirigeant, 07/10/2026) :** journée de 7 h (08h30–12h00 / 13h00–16h30) ;
6 stagiaires minimum, 8 maximum, en inter comme en intra ; lieu communiqué par le formateur 15 jours avant ;
FOR-0011 sur 2 jours (14 h).

## Airtable aligné le 07/10/2026
- CONFIG SYSTÈME : horaires (08h30–12h00 / 13h00–16h30, 7 h) et barèmes A, B, C.
- CATALOGUE : formule « Durée en jours » = heures ÷ 7 ; FOR-0011 renommée « (2 jours) ».
- YEBA-DOC-12 : prix par jour du catalogue, 7 h, 6 à 8 participants, seuils recalculés.
- YEBA-DOC-03 (CGV) art. 6.3 : en deçà de 6 inscrits, report ; remboursement intégral si l'effectif n'est pas atteint un mois après la date initiale.

## 08/10/2026
- Frais de salle et de restauration retirés de la plaquette et de YEBA-DOC-12 (v3.1).
- Charte YEBA-IDENT-2026 appliquée : logo monochrome blanc sur fond uni (#121212 / #1B3A6B), plus de logo sur photo ni dégradé.
- Mention de transparence IA (règlement (UE) 2024/1689, art. 50) ajoutée en pied de page.
- Animation : l'image fixe de couverture est remplacée par la vidéo « IA » (source/assets/ia-anim.mp4).

## Régénérer
Dans `source/` : `npm i playwright @fontsource/montserrat @fontsource/jetbrains-mono`,
extraire les images de la vidéo (`ffmpeg -i assets/ia-anim.mp4 -q:v 2 assets/vf/f%03d.jpg`), puis `node render.mjs .` (PDF) et `node capture.mjs` + ffmpeg (animation ; `LITE=1 FPS=10 DSF=1` pour le GIF e-mail).
