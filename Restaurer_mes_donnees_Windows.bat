@echo off
REM Restaure la sauvegarde la plus recente placee a cote du logiciel.
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  echo Lancez d'abord Lancer_Decorticage_Windows.bat une fois pour installer le logiciel.
  pause
  exit /b 1
)
.venv\Scripts\python.exe -m decorticage restaurer
pause
