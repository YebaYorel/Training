"""Lanceur du serveur MCP Playwright (navigateur piloté par Claude).

Pourquoi un lanceur : le même `.mcp.json` doit marcher
- dans les sessions Claude Code cloud (Chromium préinstallé dans /opt/pw-browsers,
  sans bac à sable possible dans le conteneur),
- et sur le PC local (Windows/Mac), où Playwright utilise Chrome installé.

Version figée (épinglée) pour éviter qu'une mise à jour amont non relue
ne s'exécute automatiquement.
"""
import glob
import os
import shutil
import subprocess
import sys

PLAYWRIGHT_MCP_VERSION = "0.0.83"


def main() -> int:
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if not npx:
        sys.stderr.write("playwright_mcp: Node.js (npx) introuvable. Installer Node.js LTS.\n")
        return 1
    args = [npx, "-y", f"@playwright/mcp@{PLAYWRIGHT_MCP_VERSION}", "--headless"]
    # Conteneur cloud : Chromium préinstallé + pas de sandbox noyau disponible.
    candidates = sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome"))
    if candidates:
        args += ["--executable-path", candidates[-1], "--no-sandbox"]
    args += sys.argv[1:]
    return subprocess.call(args, env=os.environ.copy())


if __name__ == "__main__":
    sys.exit(main())
