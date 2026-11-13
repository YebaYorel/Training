#!/usr/bin/env bash
# Met à jour la compétence « watch » depuis son dépôt d'origine (licence MIT). Relire le diff avant de committer.
set -euo pipefail
ICI="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 -q https://github.com/bradautomates/claude-video "$TMP/src"
cp "$TMP/src/skills/watch/SKILL.md" "$ICI/SKILL.md"
cp "$TMP/src/skills/watch/scripts/"*.py "$ICI/scripts/"
cp "$TMP/src/LICENSE" "$ICI/LICENSE"
echo "Copié : $(grep -m1 'version:' "$ICI/SKILL.md" | tr -d ' ') · commit $(git -C "$TMP/src" rev-parse --short HEAD)"
git -C "$ICI" diff --stat -- . || true
echo "À faire : relire « git diff .claude/skills/watch », mettre à jour PROVENANCE.md, puis committer."
