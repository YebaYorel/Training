#!/usr/bin/env bash
# Met à jour la copie de la compétence learnharness depuis l'amont (amosblomqvist/learnharness, AGPL-3.0).
# Copie à l'identique SKILL.md, LICENSE, references/ et scripts/ ; ne lance aucun code de l'amont.
# Relire ensuite « git diff .claude/skills/learnharness », mettre à jour PROVENANCE.md, puis committer.
set -euo pipefail
ICI="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 -q https://github.com/amosblomqvist/learnharness "$TMP/src"
AMONT="$TMP/src/skills/learnharness"
cp "$AMONT/SKILL.md" "$AMONT/LICENSE" "$ICI/"
rm -rf "$ICI/references" "$ICI/scripts"
cp -r "$AMONT/references" "$AMONT/scripts" "$ICI/"
echo "Copié : application $(grep -m1 '"version"' "$TMP/src/package.json" | tr -d ' ,') · commit $(git -C "$TMP/src" rev-parse --short HEAD)"
git -C "$ICI" diff --stat -- . || true
echo "À faire : relire « git diff .claude/skills/learnharness », mettre à jour PROVENANCE.md, puis committer."
