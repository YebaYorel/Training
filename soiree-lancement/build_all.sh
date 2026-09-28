#!/usr/bin/env bash
# Reconstruit TOUS les supports de la soirée depuis contenu/slides.json.
#   bash soiree-lancement/build_all.sh            → PPTX + Reveal.js + storyboard/Felo/Slides.com
#   bash soiree-lancement/build_all.sh --videos   → idem + rendu des vidéos Remotion (plus long)
set -euo pipefail
ICI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ICI"

python3 assets/generer_illustrations.py
if [[ "${1:-}" == "--videos" ]]; then
  ( cd remotion && npm run --silent render:all \
      && npx remotion still src/index.ts Intro ../dist/yeba-intro-poster.png --frame=240 )
fi
python3 pptx/build_pptx.py
python3 revealjs/build_reveal.py
python3 outils/generer_supports.py
if command -v soffice >/dev/null 2>&1; then
  soffice --headless --convert-to pdf --outdir dist dist/YEBA_Soiree_Lancement.pptx >/dev/null 2>&1 \
    && echo "OK : dist/YEBA_Soiree_Lancement.pdf (pour Slides.com)" || echo "PDF non généré (LibreOffice indisponible)"
fi
