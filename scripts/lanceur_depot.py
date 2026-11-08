"""Télécharge un dépôt de skills à une version FIGÉE dans un cache ignoré par Git.

Utilisé par les skills « lanceurs » (huashu-design, vercel-skills, openmontage,
llm-council) : le code tiers n'est pas recopié dans le dépôt (licence absente,
fichiers lourds ou licence AGPL), mais récupéré à la demande et vérifié.

  python scripts/lanceur_depot.py <owner/repo> <commit_complet> <nom_dossier>

Affiche le chemin du cache. Refuse de continuer si le commit obtenu ne
correspond pas au commit relu (dépôt amont réécrit = version non relue).
"""
import os
import pathlib
import subprocess
import sys


def run(*args, cwd=None):
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    depot, commit, nom = sys.argv[1:]
    racine = pathlib.Path(os.environ.get("CLAUDE_PROJECT_DIR") or pathlib.Path(__file__).resolve().parent.parent)
    cache = racine / ".claude" / "vendor-cache" / nom
    if not (cache / ".git").exists():
        cache.parent.mkdir(parents=True, exist_ok=True)
        run("git", "init", "-q", str(cache))
        run("git", "remote", "add", "origin", f"https://github.com/{depot}.git", cwd=cache)
    actuel = run("git", "rev-parse", "HEAD", cwd=cache) if _a_un_commit(cache) else ""
    if actuel != commit:
        try:
            run("git", "fetch", "-q", "--depth", "1", "origin", commit, cwd=cache)
            run("git", "-c", "advice.detachedHead=false", "checkout", "-q", "FETCH_HEAD", cwd=cache)
        except subprocess.CalledProcessError as exc:
            print(f"ARRÊT : impossible de récupérer {depot}@{commit} ({exc.stderr.strip()[:200]}).")
            return 1
    obtenu = run("git", "rev-parse", "HEAD", cwd=cache)
    if obtenu != commit:
        print(f"ARRÊT : commit obtenu {obtenu} différent du commit relu {commit}. Prévenir Aurélien.")
        return 1
    print(cache)
    return 0


def _a_un_commit(cache: pathlib.Path) -> bool:
    return subprocess.run(["git", "rev-parse", "--verify", "-q", "HEAD"], cwd=cache, capture_output=True).returncode == 0


if __name__ == "__main__":
    sys.exit(main())
