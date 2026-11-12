#!/usr/bin/env bash
# Reconstruit TOUS les supports de « YEBA — Saison 1 » depuis contenu/slides.json.
#   bash soiree-lancement/build_all.sh            → calques + PPTX cinéma & sobre + Reveal.js + storyboard/Felo/Slides.com + PDF
#   bash soiree-lancement/build_all.sh --videos   → idem, précédé des bandes-son et du rendu des vidéos Remotion
#                                                   (générique v3 « La graine » 60 i/s ≈ 35 min, fonds v3, cartes d'épisode)
set -euo pipefail
ICI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ICI"

python3 assets/generer_illustrations.py
python3 assets/generer_calques.py
if [[ "${1:-}" == "--videos" ]]; then
  ( cd remotion && npm run --silent tout )   # bande-son synthétisée puis rendu (générique, épisodes, fonds)
fi
if [[ ! -f dist/videos/yeba-saison1-generique-v3.mp4 ]]; then
  echo "‼️ Vidéos absentes : lancer « bash build_all.sh --videos » (rendu Remotion local)." >&2
  exit 1
fi
python3 pptx/build_pptx.py            # version cinéma : fonds vidéo vivants
python3 pptx/build_pptx.py --sobre    # version sobre : mêmes fonds en images fixes
python3 revealjs/build_reveal.py
python3 outils/generer_supports.py
python3 outils/generer_accueil.py      # prototype « Accueil Saison 1 » → dist/accueil/
if command -v soffice >/dev/null 2>&1; then
  # PDF depuis une copie où chaque vidéo est remplacée par son image (sinon LibreOffice embarque les MP4 : ~100 Mo)
  python3 pptx/build_pptx.py --images
  soffice --headless --convert-to pdf --outdir dist dist/YEBA_Soiree_Lancement_IMAGES.pptx >/dev/null 2>&1 \
    && mv -f dist/YEBA_Soiree_Lancement_IMAGES.pdf dist/YEBA_Soiree_Lancement.pdf \
    && echo "OK : dist/YEBA_Soiree_Lancement.pdf (pour Slides.com / impression / envoi)" || echo "PDF non généré (LibreOffice indisponible)"
  rm -f dist/YEBA_Soiree_Lancement_IMAGES.pptx
fi
