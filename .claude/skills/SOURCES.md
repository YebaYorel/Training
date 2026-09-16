# Provenance et attribution

Traçabilité des 26 skills de `.claude/skills/`. Sans ce fichier, une skill est
du texte d'origine inconnue que l'agent exécute comme une instruction.

## Versions d'origine

Dépôts clonés et audités le **16 septembre 2026**. Les commits sont épinglés :
c'est ce qui rend l'installation reproductible et vérifiable.

| Dépôt | Commit | Licence |
|---|---|---|
| [ckorhonen/claude-skills](https://github.com/ckorhonen/claude-skills) | `39896345ef47beced8bbfeece5e772f0d978b8c6` | MIT — © 2025 Chris Korhonen |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `15de38fb70bc80ae9276fa7703b48ae861a672e6` | MIT — © 2024 Next Level Builder |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) | `8da1f030185bdfe8471220585162991eaeb970e9` | MIT — © 2025 Hardik Pandya |
| [hanfang/claude-memory-skill](https://github.com/hanfang/claude-memory-skill) | `c290e3eea033aede1617efdb5b7ad2f58ee0b415` | MIT — © 2024 |
| [rebelytics/one-skill-to-rule-them-all](https://github.com/rebelytics/one-skill-to-rule-them-all) | `7518a858cf5b550bf3dc61b1b625f4cb0b5fa87f` | **CC BY 4.0** |

Vérifier qu'une skill n'a pas dérivé de sa source :

```bash
git clone https://github.com/ckorhonen/claude-skills.git /tmp/verif
git -C /tmp/verif checkout 39896345ef47beced8bbfeece5e772f0d978b8c6
diff -r /tmp/verif/skills/brainstorming .claude/skills/brainstorming
```

## Attribution CC BY 4.0 — `task-observer`

`task-observer` provient de **rebelytics/one-skill-to-rule-them-all**, sous
licence [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

Contrairement aux licences MIT des quatre autres dépôts, CC BY 4.0 impose trois
obligations à **toute réutilisation publique** — support de formation remis à un
stagiaire, article, livrable client :

1. **Citer l'auteur** : rebelytics / *One Skill to Rule Them All*.
2. **Indiquer un lien vers la licence** : https://creativecommons.org/licenses/by/4.0/
3. **Signaler si des modifications ont été apportées.**

**Modifications apportées ici :** aucune sur le contenu. Le dépôt d'origine
place `SKILL.md` à sa racine ; seuls `SKILL.md`, `references/`, `scripts/` et
`LICENSE.txt` ont été extraits vers un sous-dossier `task-observer/`, sans
altération des fichiers.

## Modifications apportées aux autres skills

| Skill | Modification |
|---|---|
| `mem` | **Réécrite.** La source (hanfang) n'était pas une skill : pas de `SKILL.md`, pas d'en-tête YAML, et un `install.sh` qui écrivait dans `~/.claude/commands/` **et modifiait le `~/.claude/CLAUDE.md` global de l'utilisateur**. Portée au format skill, sans effet de bord, et complétée d'une barrière RGPD interdisant d'y stocker des données personnelles. Le comportement fonctionnel d'origine (load / save / recall / show / forget, structure `core.md` + `topics/`) est conservé. |
| `ui-styling` | Dossier `canvas-fonts/` retiré (5,5 Mo de polices binaires, inutiles hors génération d'images sur canevas). Récupérables depuis le dépôt d'origine au commit épinglé. |
| Toutes les autres | Copiées sans modification. |

## Skills présentes dans les dépôts mais non installées

Voir `README.md`, section « Ce qui a été volontairement écarté » : 3 pour
dépendance hors UE avérée, 9 supplémentaires du même type non retenues, 1 pour
risque de chaîne d'approvisionnement (`skill-finder`), 1 pour doublon
fonctionnel (`continuous-learning`), ~30 pour hors-sujet.

## Avertissement de sécurité

Une skill est **du texte que l'agent lit comme une instruction**. Installer une
skill revient à accorder à son auteur un droit d'écriture sur le comportement
de l'agent.

Les 26 skills installées ont fait l'objet d'un contrôle automatisé : absence de
secrets en dur, absence de `curl … | bash`, absence de `rm -rf` sur des chemins
sensibles, absence d'appel réseau vers un service hors UE. **Ce contrôle n'est
pas une relecture ligne à ligne des 234 fichiers** : il écarte les pièges
grossiers, pas une instruction malveillante rédigée en langage naturel.

Conséquences pratiques :

- avant toute mise à jour (`git pull` puis `install-skills.sh`), relire le
  `git diff` — une skill peut changer de comportement sans changer de nom ;
- n'ajouter aucune skill sans l'avoir lue, ce qui est précisément la raison
  pour laquelle `skill-finder` (installation automatique depuis Internet) a été
  écartée ;
- ne jamais placer d'identifiant ou de secret dans un fichier de skill.
