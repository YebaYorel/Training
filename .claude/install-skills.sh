#!/usr/bin/env bash
#
# Installe les skills de ce dépôt dans ~/.claude/skills/ pour les rendre
# disponibles dans TOUS vos projets Claude Code, de façon permanente.
#
#   ./.claude/install-skills.sh              # installe / met à jour
#   ./.claude/install-skills.sh --dry-run    # simule, n'écrit rien
#   ./.claude/install-skills.sh --list       # liste les skills disponibles
#
# Ce script n'exécute aucun téléchargement et ne modifie jamais votre
# ~/.claude/CLAUDE.md : il se contente de copier des fichiers.

set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/skills" && pwd)"
DST="$HOME/.claude/skills"
STAMP="$(date +%Y%m%d-%H%M%S)"
DRY=0

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY=1 ;;
    --list)
      echo "Skills disponibles dans $SRC :"
      for d in "$SRC"/*/; do
        n="$(basename "$d")"
        desc="$(grep -m1 '^description:' "$d/SKILL.md" 2>/dev/null | cut -c14-95)"
        printf '  %-28s %s\n' "$n" "$desc"
      done
      exit 0 ;;
    -h|--help) sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "Option inconnue : $arg" >&2; exit 2 ;;
  esac
done

[ -d "$SRC" ] || { echo "Erreur : $SRC introuvable." >&2; exit 1; }
mkdir -p "$DST"

installed=0 updated=0 backed_up=0

for d in "$SRC"/*/; do
  name="$(basename "$d")"
  target="$DST/$name"

  if [ -e "$target" ]; then
    # Une skill du même nom existe déjà : on la sauvegarde avant d'écraser,
    # pour ne jamais détruire un travail personnel.
    if diff -rq "$d" "$target" >/dev/null 2>&1; then
      continue                       # identique, rien à faire
    fi
    if [ "$DRY" -eq 1 ]; then
      echo "[simulation] MAJ      $name (sauvegarde de l'existant)"
    else
      mv "$target" "$DST/.$name.bak-$STAMP"
      cp -r "$d" "$target"
      backed_up=$((backed_up + 1))
    fi
    updated=$((updated + 1))
  else
    if [ "$DRY" -eq 1 ]; then
      echo "[simulation] INSTALL  $name"
    else
      cp -r "$d" "$target"
    fi
    installed=$((installed + 1))
  fi
done

if [ "$DRY" -eq 1 ]; then
  echo
  echo "Simulation : $installed à installer, $updated à mettre à jour. Aucun fichier écrit."
  exit 0
fi

echo "Installées : $installed — Mises à jour : $updated — Sauvegardes : $backed_up"
echo "Destination : $DST"
[ "$backed_up" -gt 0 ] && echo "Versions précédentes conservées en $DST/.<nom>.bak-$STAMP"
echo
echo "Ouvrez une NOUVELLE session Claude Code, puis vérifiez avec : /skills"
