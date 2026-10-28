#!/bin/bash
# Crée une sauvegarde de vos données (projets, charte, tarifs) à côté du logiciel.
cd "$(dirname "$0")" || exit 1
.venv/bin/python -m decorticage sauvegarder
read -r -p "Appuyez sur Entrée pour fermer."
