#!/usr/bin/env bash
# Met à jour la copie du Roast Room depuis l'amont (nateherkai/roast-room, MIT).
# Copie à l'identique la compétence roast-room (sans newroaster) et les conseillers council-*.md ;
# ne lance aucun code de l'amont. Relire ensuite le diff, mettre à jour PROVENANCE.md, puis committer.
set -euo pipefail
ICI="$(cd "$(dirname "$0")" && pwd)"
RACINE="$(cd "$ICI/../../.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
git clone --depth 1 -q https://github.com/nateherkai/roast-room "$TMP/src"
AMONT="$TMP/src/.claude"
cp "$AMONT/skills/roast-room/SKILL.md" "$AMONT/skills/roast-room/roster.json" "$TMP/src/LICENSE" "$ICI/"
rm -rf "$ICI/brains" "$ICI/references" "$ICI/scripts"
cp -r "$AMONT/skills/roast-room/brains" "$AMONT/skills/roast-room/references" "$AMONT/skills/roast-room/scripts" "$ICI/"
cp "$AMONT"/agents/council-*.md "$RACINE/.claude/agents/"
echo "Copié : commit $(git -C "$TMP/src" rev-parse --short HEAD)"
echo "Outils des conseillers (attendu : Read, Grep, Glob) :"
grep -h "^tools:" "$RACINE"/.claude/agents/council-*.md | sort | uniq -c
git -C "$RACINE" diff --stat -- .claude/skills/roast-room .claude/agents || true
echo "Attention : roster.json a été remplacé ; refaire la composition par défaut si elle avait été changée (/roast-room board)."
echo "À faire : relire le diff, mettre à jour PROVENANCE.md (commit), puis committer."
