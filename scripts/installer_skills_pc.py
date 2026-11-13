"""Installe les skills et plugins de ce dépôt pour TOUS les projets de ce PC.

  python scripts/installer_skills_pc.py            # aperçu (ne modifie rien)
  python scripts/installer_skills_pc.py --appliquer

- copie .claude/skills/* vers ~/.claude/skills/ (skills « utilisateur ») ;
- copie .claude/agents/*.md vers ~/.claude/agents/ (agents « utilisateur » : conseillers du Roast Room) ;
- déclare les marketplaces et installe les plugins au niveau « user ».
Un skill ou un agent déjà présent n'est jamais écrasé.
Dans les sessions cloud, rien à faire : le dossier .claude/ du dépôt suffit.
"""
import json
import pathlib
import shutil
import subprocess
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
SOURCE = RACINE / ".claude" / "skills"
CIBLE = pathlib.Path.home() / ".claude" / "skills"


def main() -> int:
    appliquer = "--appliquer" in sys.argv
    CIBLE.mkdir(parents=True, exist_ok=True) if appliquer else None
    for skill in sorted(p for p in SOURCE.iterdir() if (p / "SKILL.md").exists()):
        dest = CIBLE / skill.name
        if dest.exists():
            print(f"déjà présent, ignoré : {dest}")
            continue
        print(f"copie : {skill.name} -> {dest}")
        if appliquer:
            shutil.copytree(skill, dest)
    agents_src, agents_dest = RACINE / ".claude" / "agents", pathlib.Path.home() / ".claude" / "agents"
    for agent in sorted(agents_src.glob("*.md")) if agents_src.is_dir() else []:
        dest = agents_dest / agent.name
        if dest.exists():
            print(f"déjà présent, ignoré : {dest}")
            continue
        print(f"copie : agent {agent.stem} -> {dest}")
        if appliquer:
            agents_dest.mkdir(parents=True, exist_ok=True)
            shutil.copy2(agent, dest)
    reglages = json.loads((RACINE / ".claude" / "settings.json").read_text(encoding="utf-8"))
    claude = shutil.which("claude") or shutil.which("claude.cmd")
    for nom, decl in reglages.get("extraKnownMarketplaces", {}).items():
        cmd = [claude or "claude", "plugin", "marketplace", "add", decl["source"]["repo"], "--scope", "user"]
        print("commande :", " ".join(cmd))
        if appliquer and claude:
            subprocess.call(cmd)
    for plugin, actif in reglages.get("enabledPlugins", {}).items():
        if actif:
            cmd = [claude or "claude", "plugin", "install", plugin, "--scope", "user"]
            print("commande :", " ".join(cmd))
            if appliquer and claude:
                subprocess.call(cmd)
    if not appliquer:
        print("\nAperçu seulement. Relancer avec --appliquer pour installer.")
    elif not claude:
        print("\n'claude' introuvable dans le PATH : plugins non installés (skills copiés).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
