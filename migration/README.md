# Migration sécurisée Airtable → Baserow

Outil d'extraction des données de la base Airtable (référence FICTIVE) vers
Baserow (cloud UE), sans ressaisie manuelle. Contexte, garde-fous et
séquence complète : `docs/ANIM_LOISIRS_974_FINALISATION.md` (§6).

```bash
python -m migration plan    --base appGyK0pp3tlRABVA   # analyse, n'écrit rien
python -m migration migrate --base appGyK0pp3tlRABVA --workspace <ID> --database-name "Anim'Loisirs 974 — RECETTE"
python -m migration verify  --base appGyK0pp3tlRABVA   # rapprochement seul
```

Phases reprenables : `schema`, `data`, `links`, `verify`.

| Garde-fou | Où |
|---|---|
| Airtable en lecture seule (GET uniquement) | `airtable_source.py` |
| Refus si données RÉELLES sans `PASSAGE_REEL_AUTORISE=Oui` + `--confirm-real` | `engine.py` (`guard_real_data`) |
| Champs exclus (minimisation RGPD) | `config_anim_loisirs.json` |
| État et rapports sans valeur de cellule, ignorés par Git | `migration_state/` |
| Confirmation « MIGRER » avant toute écriture | `__main__.py` |

Champs calculés (formules, cumuls, recherches, comptages) : non copiés en
valeurs figées, listés « À RECRÉER » dans `migration_state/plan_migration.md`.

Tests hors ligne : `python -m unittest discover -s tests -v`
