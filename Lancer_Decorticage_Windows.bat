@echo off
REM Double-cliquez sur ce fichier pour ouvrir le logiciel de decorticage.
REM Premiere fois : installation automatique (2-3 min). Sans internet si le dossier "paquets" est present.
cd /d "%~dp0"
set PY=.venv\Scripts\python.exe
if exist %PY% (
  %PY% -c "import decorticage.app, openpyxl, pdfplumber, docx, PIL" 2>nul || rmdir /s /q .venv
)
if not exist %PY% (
  echo Installation du logiciel...
  py -3 -m venv .venv 2>nul || python -m venv .venv
  if not exist %PY% (
    echo Python est introuvable. Installez Python 3.13 depuis https://www.python.org en cochant "Add Python to PATH".
    pause
    exit /b 1
  )
  if exist paquets (
    %PY% -m pip install --no-index --find-links paquets -r requirements-decorticage.txt || %PY% -m pip install -r requirements-decorticage.txt
  ) else (
    %PY% -m pip install -r requirements-decorticage.txt
  )
)
%PY% -m decorticage
pause
