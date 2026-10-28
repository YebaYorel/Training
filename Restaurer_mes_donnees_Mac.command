#!/bin/bash
# Restaure la sauvegarde la plus récente placée à côté du logiciel.
cd "$(dirname "$0")" || exit 1
if [ ! -x .venv/bin/python ]; then echo "Lancez d'abord Lancer_Decorticage_Mac.command une fois."; read -r; exit 1; fi
.venv/bin/python -m decorticage restaurer
read -r -p "Appuyez sur Entrée pour fermer."
