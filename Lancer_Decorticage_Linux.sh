#!/bin/bash
# Double-cliquez sur ce fichier pour ouvrir le logiciel de décorticage (Mac).
# Première fois : installation automatique (2-3 min). Sans internet si le dossier « paquets » est présent.
cd "$(dirname "$0")" || exit 1
PY=.venv/bin/python
if [ -x "$PY" ] && ! "$PY" -c "import decorticage.app, openpyxl, pdfplumber, docx, PIL" 2>/dev/null; then rm -rf .venv; fi
if [ ! -x "$PY" ]; then
  echo "Installation du logiciel..."
  python3 -m venv .venv || { echo "Installez Python 3.13 depuis https://www.python.org puis relancez."; read -r; exit 1; }
  if [ -d paquets ]; then
    "$PY" -m pip install --no-index --find-links paquets -r requirements-decorticage.txt \
      || "$PY" -m pip install -r requirements-decorticage.txt
  else
    "$PY" -m pip install -r requirements-decorticage.txt
  fi
fi
"$PY" -m decorticage
