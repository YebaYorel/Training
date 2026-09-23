# Origine du skill agent-reach

- Source : https://github.com/Panniantong/Agent-Reach (licence MIT, voir LICENSE)
- Commit vérifié : `a19a171fa980a0785849596492e0af4db800c82f` (16/09/2026)
- `SKILL.md` = traduction française de `agent_reach/skill/SKILL_en.md` + règles YEBA (RGPD, IA Act,
  souveraineté) + suppression de l'auto-mise-à-jour distante.
- `references/` = traduction française + règles YEBA ajoutées.

## Mettre à jour (volontairement manuel)
1. Lire le diff amont entre l'ancien et le nouveau commit (sécurité).
2. Retraduire les passages modifiés de `SKILL_en.md` / `references/` en français, garder le bloc « Règles YEBA ».
3. Changer le commit dans ce fichier, `SKILL.md` et `.claude/hooks/agent-reach-setup.sh`.
