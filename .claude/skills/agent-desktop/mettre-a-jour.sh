#!/usr/bin/env bash
# Met à jour la copie des compétences agent-desktop depuis l'amont (vercel-labs/agent-desktop, Apache-2.0).
# Copie à l'identique agent-desktop (+ references), agent-desktop-windows, -macos, -linux ; ne lance aucun code.
# Relire ensuite le diff, mettre à jour PROVENANCE.md (version, commit, commande npm), puis committer.
set -euo pipefail
ICI="$(cd "$(dirname "$0")" && pwd)"
SKILLS="$(cd "$ICI/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
git clone --depth 1 -q https://github.com/vercel-labs/agent-desktop "$TMP/src"
for s in agent-desktop agent-desktop-windows agent-desktop-macos agent-desktop-linux; do
  find "$SKILLS/$s" -mindepth 1 -maxdepth 1 ! -name PROVENANCE.md ! -name mettre-a-jour.sh ! -name LICENSE -exec rm -rf {} +
  cp -r "$TMP/src/skills/$s/." "$SKILLS/$s/"
done
cp "$TMP/src/LICENSE" "$ICI/LICENSE"
echo "Copié : $(grep -m1 '^## \[' "$TMP/src/CHANGELOG.md" | cut -c1-40) · commit $(git -C "$TMP/src" rev-parse --short HEAD)"
git -C "$SKILLS" diff --stat -- . || true
echo "À faire : relire le diff, mettre à jour PROVENANCE.md (version, commit, npm install agent-desktop@X.Y.Z), puis committer."
