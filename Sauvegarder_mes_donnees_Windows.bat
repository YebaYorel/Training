@echo off
REM Cree une sauvegarde de vos donnees (projets, charte, tarifs) a cote du logiciel.
cd /d "%~dp0"
.venv\Scripts\python.exe -m decorticage sauvegarder
pause
