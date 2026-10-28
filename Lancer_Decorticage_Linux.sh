#!/bin/bash
# Double-cliquez sur ce fichier pour ouvrir le logiciel de décorticage (Mac).
# Première fois : installation automatique (connexion internet requise, 2-3 min).
cd "$(dirname "$0")" || exit 1
PY=.venv/bin/python
if [ -x "$PY" ] && ! "$PY" -c "import decorticage.app" 2>/dev/null; then rm -rf .venv; fi
if [ ! -x "$PY" ]; then
  echo "Installation du logiciel..."
  python3 -m venv .venv || { echo "Installez Python 3 depuis python.org puis relancez."; read -r; exit 1; }
  "$PY" -m pip install --upgrade pip
  "$PY" -m pip install -r requirements-decorticage.txt
fi
"$PY" -m decorticage
