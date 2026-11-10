#!/bin/bash
# Démarrage de session Claude Code — outils de présentation YEBA FORMATIONS.
# Installe (si absents) : python-pptx, Pillow, numpy, scipy, lxml, fontTools, dépendances npm Remotion + Reveal.js,
# police Montserrat. Idempotent et non interactif. Aucun secret, aucune donnée personnelle.
set -uo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
SL="$ROOT/soiree-lancement"
etat=()

# 1. Python : python-pptx, Pillow (vraiment chargeable : certains systèmes ont un PIL cassé), numpy/scipy
#    (bande-son, calques), lxml, fontTools — puis dépendances du dépôt
TEST_PY='import pptx, lxml, numpy, scipy, fontTools; from PIL import Image, ImageDraw, ImageFont, ImageFilter'
if python3 -c "$TEST_PY" 2>/dev/null; then
  etat+=("python-pptx ✅")
else
  python3 -m pip install -q python-pptx lxml numpy scipy fonttools brotli >/dev/null 2>&1 || true
  python3 -c "from PIL import Image, ImageFont" 2>/dev/null || python3 -m pip install -q --ignore-installed pillow >/dev/null 2>&1 || true
  if python3 -c "$TEST_PY" 2>/dev/null; then etat+=("python-pptx ✅ (installé)"); else etat+=("python-pptx ‼️ python3 -m pip install -r soiree-lancement/requirements.txt"); fi
fi
[ -f "$SL/requirements.txt" ] && python3 -m pip install -q -r "$SL/requirements.txt" >/dev/null 2>&1 || true
[ -f "$ROOT/requirements.txt" ] && python3 -m pip install -q -r "$ROOT/requirements.txt" >/dev/null 2>&1 || true

# 2. Node : Remotion et Reveal.js
if command -v npm >/dev/null 2>&1; then
  for d in remotion revealjs; do
    if [ -f "$SL/$d/package.json" ] && [ ! -d "$SL/$d/node_modules" ]; then
      (cd "$SL/$d" && npm install --no-audit --no-fund --silent >/dev/null 2>&1) || true
    fi
  done
  [ -d "$SL/remotion/node_modules/remotion" ] && etat+=("Remotion ✅") || etat+=("Remotion ‼️ cd soiree-lancement/remotion && npm install")
else
  etat+=("Remotion ‼️ Node.js absent")
fi
[ -f "$SL/revealjs/vendor/reveal.js" ] && etat+=("Reveal.js ✅ (hors ligne)") || etat+=("Reveal.js ‼️ vendor manquant")

# 3. Police Montserrat (rendu fidèle des aperçus)
if [ -d "$SL/assets/fonts" ] && ! fc-list 2>/dev/null | grep -qi "Montserrat"; then
  mkdir -p "$HOME/.fonts" && cp "$SL"/assets/fonts/*.ttf "$HOME/.fonts/" 2>/dev/null && fc-cache -f >/dev/null 2>&1 || true
fi

# 4. Outils sans installation (fichiers du dépôt)
[ -f "$SL/vba/YebaAnimations.bas" ] && etat+=("VBA ✅")
[ -f "$SL/slides-com/plan_slides_com.md" ] && etat+=("Slides.com ✅ (plan + PDF)")
[ -f "$SL/felo/prompt_felo_slides.md" ] && etat+=("Felo Slides ✅ (prompt)")

# Message injecté dans le contexte de Claude au démarrage
echo "OUTILS DE PRÉSENTATION YEBA : ${etat[*]}"
echo "Skills : presentation-yeba (chef d'orchestre), python-pptx, reveal-js, remotion, vba-powerpoint, slides-com, felo-slides."
echo "Tout reconstruire : bash soiree-lancement/build_all.sh [--videos] — vidéos : générique 80 s, 7 cartes d'épisode, 9 fonds vivants (dist/videos/)"
exit 0
