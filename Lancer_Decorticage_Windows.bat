@echo off
REM Double-cliquez sur ce fichier pour ouvrir le logiciel de decorticage.
REM Premiere fois : installation automatique (connexion internet requise, 2-3 min).
cd /d "%~dp0"
set PY=.venv\Scripts\python.exe
if exist %PY% (
  %PY% -c "import decorticage.app" 2>nul || rmdir /s /q .venv
)
if not exist %PY% (
  echo Installation du logiciel...
  py -3 -m venv .venv 2>nul || python -m venv .venv
  %PY% -m pip install --upgrade pip
  %PY% -m pip install -r requirements-decorticage.txt
)
%PY% -m decorticage
pause
