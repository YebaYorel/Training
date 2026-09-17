#!/usr/bin/env bash
# Prépare l'environnement Python au démarrage d'une session Claude Code.
#
# Sans ce script, le serveur MCP baserow échoue au démarrage avec
# CONNECTION_CLOSED : les conteneurs distants sont reclonés à neuf et
# requirements.txt n'y est jamais installé.
#
# Trois pièges connus, corrigés ici :
#   1. dotenv et mcp absents           → le serveur meurt à l'import
#   2. PyJWT installé par Debian       → fait échouer TOUTE l'installation
#   3. SDK mcp 2.x                     → FastMCP y est renommé MCPServer,
#                                        le serveur utilise l'API 1.x

set -u
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 0

if python3 -c "from mcp.server.fastmcp import FastMCP" 2>/dev/null; then
  echo "Environnement Baserow déjà prêt."
  exit 0
fi

echo "Installation des dépendances Baserow…"
# --ignore-installed PyJWT : contourne le paquet Debian dépourvu de RECORD,
# qui fait avorter l'installation entière.
pip install -q --ignore-installed PyJWT -r requirements.txt 2>&1 | grep -viE "warning|notice" || true

# Le SDK a pu s'installer en 2.x malgré l'épinglage si une version traînait.
if ! python3 -c "from mcp.server.fastmcp import FastMCP" 2>/dev/null; then
  echo "SDK mcp incompatible détecté — réinstallation en version 1.x…"
  pip uninstall -y -q mcp 2>/dev/null
  rm -rf /usr/local/lib/python3.11/dist-packages/mcp \
         /usr/local/lib/python3.11/dist-packages/mcp-*.dist-info 2>/dev/null
  pip install -q --ignore-installed PyJWT "mcp<2" 2>&1 | grep -viE "warning|notice" || true
fi

if python3 -c "from mcp.server.fastmcp import FastMCP" 2>/dev/null; then
  echo "✓ Serveur MCP baserow prêt."
else
  echo "⚠ Le SDK mcp reste inutilisable — lancer : pip install --ignore-installed PyJWT 'mcp<2'"
fi

[ -f .env ] || echo "⚠ Aucun .env : le serveur démarrera mais ne pourra pas s'authentifier auprès de Baserow."
exit 0
