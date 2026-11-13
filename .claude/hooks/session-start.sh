#!/bin/bash
# Démarrage de session Claude Code — outils de présentation et compétences YEBA FORMATIONS.
# Session cloud ($CLAUDE_CODE_REMOTE=true) : installe ce qui manque. Liste : python-pptx, Pillow, numpy, scipy, lxml,
# fontTools, dépendances Python du dépôt, npm Remotion + Reveal.js, police Montserrat, yt-dlp, FFmpeg.
# Le conteneur est ensuite mis en cache : les sessions suivantes démarrent sans réinstaller.
# Ordinateur personnel : n'installe rien (aucune installation silencieuse chez Aurélien), vérifie seulement.
# Idempotent et non interactif. Aucun secret, aucune donnée personnelle.
set -uo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
SL="$ROOT/soiree-lancement"
etat=()
CLOUD=false; [ "${CLAUDE_CODE_REMOTE:-}" = "true" ] && CLOUD=true
manque() { etat+=("$1 ‼️ $2"); }   # outil absent : nom + commande qui l'installe

# 1. Python : python-pptx, Pillow (vraiment chargeable : certains systèmes ont un PIL cassé), numpy/scipy
#    (bande-son, calques), lxml, fontTools
TEST_PY='import pptx, lxml, numpy, scipy, fontTools; from PIL import Image, ImageDraw, ImageFont, ImageFilter'
if python3 -c "$TEST_PY" 2>/dev/null; then
  etat+=("python-pptx ✅")
elif $CLOUD; then
  python3 -m pip install -q python-pptx lxml numpy scipy fonttools brotli >/dev/null 2>&1 || true
  python3 -c "from PIL import Image, ImageFont" 2>/dev/null || python3 -m pip install -q --ignore-installed pillow >/dev/null 2>&1 || true
  if python3 -c "$TEST_PY" 2>/dev/null; then etat+=("python-pptx ✅ (installé)"); else manque python-pptx "python3 -m pip install -r soiree-lancement/requirements.txt"; fi
else
  manque python-pptx "python3 -m pip install -r soiree-lancement/requirements.txt"
fi

#    Dépendances Python du dépôt (requirements.txt de la racine et de la soirée) : installées seulement si l'un de
#    ces fichiers a changé depuis la dernière installation réussie. L'empreinte est rangée avec les paquets : un
#    conteneur neuf ne l'a pas, donc il installe.
REQS=(); for f in "$SL/requirements.txt" "$ROOT/requirements.txt"; do [ -f "$f" ] && REQS+=("$f"); done
PYSITE="$(python3 -I -c 'import sysconfig; print(sysconfig.get_path("purelib"))' 2>/dev/null || true)"
EMPREINTE="$PYSITE/.yeba-session-start.sha256"
if $CLOUD && [ ${#REQS[@]} -gt 0 ] && [ -n "$PYSITE" ] && ! sha256sum --check --status "$EMPREINTE" 2>/dev/null; then
  rm -f "$EMPREINTE"   # effacée d'abord : un échec relancera l'installation à la session suivante
  ok=true
  # Second essai avec --ignore-installed : un paquet installé par Debian (sans fichier RECORD, ex. PyJWT exigé
  # par « mcp ») ne peut pas être mis à jour par pip ; on installe alors une version à côté.
  for f in "${REQS[@]}"; do
    python3 -m pip install -q -r "$f" >/dev/null 2>&1 \
      || python3 -m pip install -q --ignore-installed -r "$f" >/dev/null 2>&1 \
      || ok=false
  done
  if $ok; then sha256sum "${REQS[@]}" > "$EMPREINTE" 2>/dev/null || rm -f "$EMPREINTE"
  else manque "dépendances Python" "python3 -m pip install -r requirements.txt"; fi
fi

# 2. Node : Remotion et Reveal.js
if command -v npm >/dev/null 2>&1; then
  if $CLOUD; then
    for d in remotion revealjs; do
      if [ -f "$SL/$d/package.json" ] && [ ! -d "$SL/$d/node_modules" ]; then
        (cd "$SL/$d" && npm install --no-audit --no-fund --silent >/dev/null 2>&1) || true
      fi
    done
  fi
  [ -d "$SL/remotion/node_modules/remotion" ] && etat+=("Remotion ✅") || manque Remotion "cd soiree-lancement/remotion && npm install"
else
  etat+=("Remotion ‼️ Node.js absent")
fi
[ -f "$SL/revealjs/vendor/reveal.js" ] && etat+=("Reveal.js ✅ (hors ligne)") || etat+=("Reveal.js ‼️ vendor manquant")

# 3. Police Montserrat (rendu fidèle des aperçus)
if $CLOUD && [ -d "$SL/assets/fonts" ] && ! fc-list 2>/dev/null | grep -qi "Montserrat"; then
  mkdir -p "$HOME/.fonts" && cp "$SL"/assets/fonts/*.ttf "$HOME/.fonts/" 2>/dev/null && fc-cache -f >/dev/null 2>&1 || true
fi

# 4. Outils sans installation (fichiers du dépôt)
[ -f "$SL/vba/YebaAnimations.bas" ] && etat+=("VBA ✅")
[ -f "$SL/slides-com/plan_slides_com.md" ] && etat+=("Slides.com ✅ (plan + PDF)")
[ -f "$SL/felo/prompt_felo_slides.md" ] && etat+=("Felo Slides ✅ (prompt)")

# 5. Compétence vidéo « watch » (bradautomates/claude-video, MIT) : yt-dlp + FFmpeg, moteur LOCAL imposé.
#    Souveraineté : jamais Gemini (Google), Groq ni OpenAI ; la vidéo et l'audio restent dans la session (voir CLAUDE.md).
#    Pas de Deno : il ne sert qu'à YouTube, qui refuse les adresses des centres de données (voir CLAUDE.md).
WATCH="$ROOT/.claude/skills/watch/scripts"
if [ -d "$WATCH" ]; then
  if $CLOUD; then
    command -v yt-dlp >/dev/null 2>&1 || python3 -m pip install -q -U "yt-dlp[default]" >/dev/null 2>&1 || true
    if ! command -v ffmpeg >/dev/null 2>&1 || ! command -v ffprobe >/dev/null 2>&1; then
      (timeout 180 apt-get install -y -qq ffmpeg >/dev/null 2>&1 \
        || (timeout 120 apt-get update -qq >/dev/null 2>&1 && timeout 180 apt-get install -y -qq ffmpeg >/dev/null 2>&1)) || true
    fi
  fi
  # Réglage de sécurité, posé partout (ce n'est pas une installation) : moteur local, jamais d'envoi de la vidéo.
  if [ ! -f "$HOME/.config/watch/.env" ]; then
    python3 "$WATCH/setup.py" --engine local --backend none --detail balanced >/dev/null 2>&1 || true
  elif ! grep -q '^WATCH_ENGINE="local"' "$HOME/.config/watch/.env"; then
    python3 "$WATCH/setup.py" --engine local >/dev/null 2>&1 || true
  fi
  if python3 "$WATCH/setup.py" --check >/dev/null 2>&1; then etat+=("Vidéo /watch ✅ (moteur local)")
  else manque "Vidéo /watch" "python3 .claude/skills/watch/scripts/setup.py --json"; fi
fi

# 6. Compétence learnharness (amosblomqvist/learnharness, AGPL) : Python standard, rien à installer
[ -f "$ROOT/.claude/skills/learnharness/scripts/graph.py" ] && etat+=("LearnHarness ✅ (lecture seule)")

# Message injecté dans le contexte de Claude au démarrage
echo "OUTILS YEBA : ${etat[*]}"
echo "Skills : presentation-yeba (présentations événementielles), python-pptx, reveal-js, remotion, vba-powerpoint, slides-com, felo-slides, watch (regarder une vidéo, moteur local), learnharness (historique d'apprentissage, lecture seule), learnharness-app (lanceur de l'application)."
echo "Soirée : bash soiree-lancement/build_all.sh [--videos] régénère PPTX, PDF et vidéos dans soiree-lancement/dist/ (non versionné)."
$CLOUD || echo "Poste local : aucune installation automatique ; chaque ‼️ donne la commande à lancer si besoin."
exit 0
