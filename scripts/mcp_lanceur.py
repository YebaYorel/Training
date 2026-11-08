"""Lanceur unique des serveurs MCP tiers (versions FIGÉES, compatible cloud et PC).

  python scripts/mcp_lanceur.py chrome-devtools | powerpoint | google-ads | meta-ads

Pourquoi un lanceur :
- figer chaque version (une mise à jour amont ne s'exécute pas sans relecture) ;
- dans le conteneur cloud, utiliser le Chromium préinstallé (pas de bac à sable
  noyau disponible) ; sur le PC, le Chrome installé.
Les identifiants (Google Ads, Meta) viennent de variables d'environnement
(.env local ou secrets de l'environnement cloud), jamais du dépôt.
"""
import glob
import os
import shutil
import subprocess
import sys

VERSIONS = {
    "chrome-devtools": "1.12.0",   # npm chrome-devtools-mcp, publié le 2026-10-22
    "powerpoint": "2.0.7",         # PyPI office-powerpoint-mcp-server, 2025-12-31
    "google-ads": "0.0.5",         # PyPI google-ads-mcp (officiel Google), 2026-10-09
    "meta-ads": "1.6.1",           # npm @mikusnuz/meta-ads-mcp, 2026-10-19
}


def outil(*noms):
    for n in noms:
        chemin = shutil.which(n)
        if chemin:
            return chemin
    sys.stderr.write(f"mcp_lanceur : aucun de {noms} n'est installé.\n")
    sys.exit(1)


def chromium_cloud():
    trouves = sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome"))
    return trouves[-1] if trouves else None


def commande(nom):
    v = VERSIONS[nom]
    if nom == "chrome-devtools":
        cmd = [outil("npx", "npx.cmd"), "-y", f"chrome-devtools-mcp@{v}", "--headless", "--isolated"]
        chrome = chromium_cloud()
        if chrome:
            cmd += ["--executablePath", chrome, "--chromeArg=--no-sandbox", "--chromeArg=--disable-setuid-sandbox"]
        return cmd
    if nom == "powerpoint":
        return [outil("uvx", "uvx.exe"), "--from", f"office-powerpoint-mcp-server=={v}", "ppt_mcp_server"]
    if nom == "google-ads":
        return [outil("uvx", "uvx.exe"), "--from", f"google-ads-mcp=={v}", "google-ads-mcp"]
    if nom == "meta-ads":
        return [outil("npx", "npx.cmd"), "-y", f"@mikusnuz/meta-ads-mcp@{v}"]
    raise SystemExit(f"Serveur inconnu : {nom} (choix : {', '.join(VERSIONS)})")


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in VERSIONS:
        print(__doc__)
        return 2
    return subprocess.call(commande(sys.argv[1]) + sys.argv[2:], env=os.environ.copy())


if __name__ == "__main__":
    sys.exit(main())
