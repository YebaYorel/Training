# Grille tarifaire 2026 — Formations IA (YEBA FORMATIONS)

| Fichier | Charte |
|---|---|
| `Grille_tarifaire_IA_2026_V1_Bleu-nuit-et-or.docx` | V1 — Bleu nuit & or (charte officielle) |
| `Grille_tarifaire_IA_2026_V2_Heritage_creme-brun-or.docx` | V2 — Héritage crème, brun & or |
| `Grille_tarifaire_IA_2026_V3_Fusion_bleu-creme-or.docx` | V3 — Fusion bleu nuit, crème & or |

`apercu-pdf/` : les mêmes en PDF, pour comparer sans ouvrir Word.

**Polices** (gratuites, licence OFL, à installer sur votre PC pour un rendu identique) : Inter (texte),
Montserrat (titres V1), Playfair Display (titres V2/V3). Sans elles, Word les remplace automatiquement.

**Régénérer** (après modification des prix dans `src/generer_grille.js`, bloc `PRIX`) :
```bash
cd src && python3 generer_visuels.py && NODE_PATH=/opt/node22/lib/node_modules node generer_grille.js
```
