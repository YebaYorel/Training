#!/usr/bin/env bash
# Sonde de composition du générique v3 (voir sonde_composition.ts). 100 % local, aucun rendu.
set -euo pipefail
cd "$(dirname "$0")/.."
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
node_modules/.bin/esbuild scripts/sonde_composition.ts --bundle --platform=node --outfile="$TMP/sonde.js" --log-level=warning
node "$TMP/sonde.js"
