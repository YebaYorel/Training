# Catalogue des formations 2026 — YEBA FORMATIONS

| Fichier | Usage |
|---|---|
| `YEBA-catalogue-2026.pdf` | Version non animée : A4 paysage, 10 pages — envoi par e-mail, impression, salons |
| `YEBA-catalogue-2026-anime.mp4` | Version animée HD : 1920 × 1080 (16:9), 1 min 05, 28 Mo — écran, salon, présentation client, LinkedIn |
| `YEBA-catalogue-2026-anime-leger.mp4` | Même vidéo en 1280 × 720, 8,8 Mo — WhatsApp, Olvid, iMessage, e-mail |
| `apercus/` | Les 10 pages en image |

## Les 10 pages
1. Couverture — le couloir « IA » (animé dans la vidéo)
2. Sommaire — les 4 pôles, preuves de compétence, chiffres clés
3–4. Pôle 01 · IA — IA générative au travail, IA souveraine, Séminaire dirigeants IA, Site internet IA, Emailing IA, Copilot Microsoft 365
5. Pôle 02 · Automatisation — Automatisation sans code (n8n), Agents IA, Implémentation sur mesure
6. Pôle 03 · RGPD & IA Act — Conformité RGPD & IA Act, Audit & conseil en gouvernance
7. Pôle 04 · Vente & Management — Vente & négociation, Manager au quotidien, Format intra
8. Comment ça se passe — parcours en 6 étapes, horaires, effectif, lieu, financement, handicap, RGPD & IA Act
9. Tarifs en un coup d'œil
10. Dernière page — le logo dans « l'œil » du couloir, coordonnées, bloc-marque légal, mention de transparence IA

## Sources
Contenu tiré de la base Airtable « YEBA FORMATIONS - Centre de formation (Adaptable) » :
CATALOGUE FORMATIONS (objectifs, public, prérequis, programme, financements, tarifs), CONFIG SYSTÈME,
YEBA-DOC-03 (CGV v1.1), YEBA-DOC-12 (politique tarifaire v3.1), YEBA-IDENT-2026 (charte).
Exclues : FOR-0005 et FOR-0007 (marque blanche), FOR-0001 (archivée), FOR-0017 (en développement).

## Régénérer
Dans `source/` : `python3 build.py && node render.mjs` (PDF) ; `python3 banim.py && node capanim.mjs` puis ffmpeg (vidéo).
Images nécessaires : `ia2x.jpg` (couverture), `clean2x.jpg` (couloir sans « AI »), `logo-white.png`, `vf/` (images de la vidéo IA).
