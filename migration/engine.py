"""Moteur de migration Airtable → Baserow, en 4 phases reprenables.

    1. schema  : base + tables + champs (liens en dernier, une seule fois par paire)
    2. data    : lignes par lots de 200 (+ pièces jointes : Baserow les télécharge
                 lui-même depuis l'URL temporaire Airtable, sans passer par le disque)
    3. links   : relations entre tables (deuxième passe, une fois toutes les lignes créées)
    4. verify  : rapprochement source/destination : nombre de lignes et nombre de
                 valeurs renseignées par champ. Le rapport ne contient AUCUNE donnée
                 personnelle, seulement des noms de champs et des compteurs.

Garde-fous :
* Airtable en lecture seule (voir airtable_source.py) ;
* refus de migrer si la base n'est pas en mode FICTIF, sauf si le paramètre
  PASSAGE_REEL_AUTORISE vaut « Oui » ET que l'option --confirm-real est donnée ;
* champs exclus par configuration (dépréciés, secrets physiques, santé
  non nécessaire) : minimisation RGPD art. 5.1.c ;
* le fichier d'état ne stocke que des IDENTIFIANTS techniques (correspondances
  ID Airtable ↔ ID Baserow), jamais de valeur de cellule. Il est ignoré par Git.
"""

from __future__ import annotations

import json
import os
from typing import Any, Callable, Dict, Iterable, List, Optional

from .mapping import COMPUTED_TYPES, computed_formula_readable, convert_value, is_empty, plan_field

ID_FIELD_NAME = "ID Airtable (migration)"
BATCH = 200


class MigrationError(RuntimeError):
    pass


def _chunks(items: List[Any], size: int) -> Iterable[List[Any]]:
    for i in range(0, len(items), size):
        yield items[i:i + size]


class Migration:
    def __init__(
        self,
        source: Any,
        target: Any,
        base_id: str,
        config: Optional[Dict[str, Any]] = None,
        state_path: Optional[str] = None,
        log: Callable[[str], None] = print,
        schema: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        self.source = source
        self.target = target
        self.base_id = base_id
        self.config = config or {}
        self.state_path = state_path
        self.log = log
        self._schema = schema
        self.state: Dict[str, Any] = {"base_id": base_id, "tables": {}}
        if state_path and os.path.exists(state_path):
            with open(state_path, encoding="utf-8") as fh:
                self.state = json.load(fh)
            if self.state.get("base_id") != base_id:
                raise MigrationError("Le fichier d'état concerne une autre base Airtable.")

    # ------------------------------------------------------------------ état
    def save(self) -> None:
        if not self.state_path:
            return
        os.makedirs(os.path.dirname(self.state_path) or ".", exist_ok=True)
        tmp = self.state_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(self.state, fh, ensure_ascii=False, indent=1)
        os.replace(tmp, self.state_path)

    # ---------------------------------------------------------------- schéma
    @property
    def schema(self) -> List[Dict[str, Any]]:
        if self._schema is None:
            self._schema = self.source.get_schema(self.base_id)
        return self._schema

    def _excluded_table(self, table: Dict[str, Any]) -> bool:
        return table["name"] in self.config.get("exclude_tables", [])

    def _excluded_field(self, table: Dict[str, Any], af: Dict[str, Any]) -> bool:
        name = af["name"]
        if f"{table['name']}::{name}" in self.config.get("exclude_fields", []):
            return True
        upper = name.upper()
        return any(p.upper() in upper for p in self.config.get("exclude_field_patterns", []))

    def tables(self) -> List[Dict[str, Any]]:
        return [t for t in self.schema if not self._excluded_table(t)]

    def fields(self, table: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [f for f in table["fields"] if not self._excluded_field(table, f)]

    def _all_names(self) -> Dict[str, str]:
        return {f["id"]: f["name"] for t in self.schema for f in t["fields"]}

    # ------------------------------------------------------------------ plan
    def plan(self) -> Dict[str, Any]:
        """Analyse sans rien écrire : ce qui sera créé, calculé, ignoré, exclu."""
        kept_tables = {t["id"] for t in self.tables()}
        names = self._all_names()
        out: Dict[str, Any] = {"tables": [], "excluded_tables": [], "totals": {}}
        totals = {"migrés": 0, "liens": 0, "calculés": 0, "ignorés": 0, "exclus": 0}
        for table in self.schema:
            if table["id"] not in kept_tables:
                out["excluded_tables"].append(table["name"])
                continue
            entry: Dict[str, Any] = {"name": table["name"], "fields": []}
            for af in table["fields"]:
                if self._excluded_field(table, af):
                    entry["fields"].append((af["name"], "EXCLU", "exclu par configuration (minimisation)"))
                    totals["exclus"] += 1
                    continue
                btype, opts, note = plan_field(af)
                if btype == "link_row" and opts.get("_linked_table") not in kept_tables:
                    btype, note = None, "lien vers une table exclue — ignoré"
                if btype is None:
                    if af["type"] in COMPUTED_TYPES:
                        totals["calculés"] += 1
                        note = f"À RECRÉER : {computed_formula_readable(af, names)}"
                        entry["fields"].append((af["name"], "CALCULÉ", note))
                    else:
                        totals["ignorés"] += 1
                        entry["fields"].append((af["name"], "IGNORÉ", note))
                    continue
                totals["liens" if btype == "link_row" else "migrés"] += 1
                entry["fields"].append((af["name"], btype, note))
            out["tables"].append(entry)
        out["totals"] = totals
        return out

    # ----------------------------------------------------------- garde-fou
    def guard_real_data(self, confirm_real: bool) -> str:
        """Bloque la migration de données RÉELLES sans double autorisation."""
        g = self.config.get("guard")
        if not g:
            if not confirm_real:
                raise MigrationError("Aucun garde-fou configuré : relancez avec --confirm-real après vérification.")
            return "garde-fou absent, confirmé manuellement"
        table = next((t for t in self.schema if t["name"] == g["table"]), None)
        if table is None:
            raise MigrationError(f"Table de garde « {g['table']} » introuvable.")
        fid = {f["name"]: f["id"] for f in table["fields"]}
        values: Dict[str, str] = {}
        for rec in self.source.iter_records(self.base_id, table["id"]):
            cells = rec.get("fields", {})
            key = cells.get(fid.get(g["key_field"]))
            if key in (g["mode_key"], g["allow_key"]):
                values[key] = str(cells.get(fid.get(g["value_field"]), "")).strip()
        mode = values.get(g["mode_key"], "")
        if mode.upper() == "FICTIF":
            return "mode FICTIF"
        if values.get(g["allow_key"], "").lower() == "oui" and confirm_real:
            return f"mode {mode or 'inconnu'} — passage au réel autorisé et confirmé"
        raise MigrationError(
            f"Mode de données « {mode or 'inconnu'} » : migration de données réelles REFUSÉE. "
            f"Conditions : {g['allow_key']} = Oui dans la table {g['table']} ET option --confirm-real."
        )

    # ---------------------------------------------------------- phase schema
    def create_schema(self, workspace_id: Optional[int], database_name: Optional[str],
                      database_id: Optional[int] = None) -> None:
        st = self.state
        if not st.get("database_id"):
            if database_id:
                if self.target.list_tables(database_id):
                    raise MigrationError("La base Baserow cible n'est pas vide : choisissez une base neuve.")
                st["database_id"] = database_id
            else:
                if not (workspace_id and database_name):
                    raise MigrationError("Indiquez --workspace et --database-name (ou --database-id).")
                st["database_id"] = self.target.create_database(workspace_id, database_name)["id"]
                self.log(f"Base Baserow créée : {database_name} (id={st['database_id']})")
            self.save()
        db = st["database_id"]
        kept = {t["id"] for t in self.tables()}

        # 1) Tables + champ primaire + champ de traçabilité
        for table in self.tables():
            ts = st["tables"].setdefault(table["id"], {"name": table["name"], "fields": {}, "selects": {}, "rows": {}})
            if "bt" not in ts:
                primary = next(f for f in table["fields"] if f["id"] == table["primaryFieldId"])
                bt = self.target.create_table(db, table["name"], primary_field_name=primary["name"])
                ts["bt"] = bt["id"]
                bprimary = next(f for f in self.target.list_fields(bt["id"]) if f.get("primary"))
                btype, opts, _ = plan_field(primary)
                if btype not in (None, "text", "link_row"):
                    self.target.update_field(bprimary["id"], type=btype, **opts)
                ts["fields"][primary["id"]] = {"bf": bprimary["id"], "owner": True}
                self._remember_selects(ts, primary["id"], bprimary)
                self.save()
            if "id_field" not in ts:
                ts["id_field"] = self.target.create_field(ts["bt"], ID_FIELD_NAME, "text")["id"]
                self.save()
            self.log(f"Table prête : {table['name']}")

        # 2) Champs simples
        for table in self.tables():
            ts = st["tables"][table["id"]]
            for af in self.fields(table):
                if af["id"] in ts["fields"]:
                    continue
                btype, opts, _ = plan_field(af)
                if btype in (None, "link_row"):
                    continue
                bf = self.target.create_field(ts["bt"], af["name"], btype, **opts)
                ts["fields"][af["id"]] = {"bf": bf["id"], "owner": True}
                self._remember_selects(ts, af["id"], bf)
                self.save()

        # 3) Liens (une seule création par paire ; Baserow crée le champ inverse)
        for table in self.tables():
            ts = st["tables"][table["id"]]
            for af in self.fields(table):
                if af["type"] != "multipleRecordLinks" or af["id"] in ts["fields"]:
                    continue
                opts = af.get("options") or {}
                target_tid = opts.get("linkedTableId")
                if target_tid not in kept:
                    continue
                tgt_table = next(t for t in self.schema if t["id"] == target_tid)
                inv_id = opts.get("inverseLinkFieldId")
                inv = next((f for f in self.fields(tgt_table) if f["id"] == inv_id), None)
                self_link = target_tid == table["id"]
                with_related = inv is not None and not self_link
                bf = self.target.create_field(
                    ts["bt"], af["name"], "link_row",
                    link_row_table_id=st["tables"][target_tid]["bt"],
                    has_related_field=with_related,
                )
                ts["fields"][af["id"]] = {"bf": bf["id"], "owner": True}
                if with_related and bf.get("link_row_related_field_id"):
                    rel_id = bf["link_row_related_field_id"]
                    try:
                        self.target.update_field(rel_id, name=inv["name"])
                    except Exception:  # noqa: BLE001 — nom déjà pris : on garde le nom automatique
                        self.log(f"  ⚠ champ inverse non renommé : {tgt_table['name']} :: {inv['name']}")
                    st["tables"][target_tid]["fields"][inv["id"]] = {"bf": rel_id, "owner": False}
                self.save()
        self.state["schema_done"] = True
        self.save()

    def _remember_selects(self, ts: Dict[str, Any], af_id: str, bf: Dict[str, Any]) -> None:
        opts = bf.get("select_options")
        if opts:
            ts["selects"][af_id] = {o["value"]: o["id"] for o in opts}

    # ------------------------------------------------------------ phase data
    def copy_data(self) -> None:
        if not self.state.get("schema_done"):
            raise MigrationError("Phase « schema » non terminée.")
        upload = getattr(self.target, "upload_file_via_url", None)
        for table in self.tables():
            ts = self.state["tables"][table["id"]]
            fields = [f for f in self.fields(table)
                      if f["id"] in ts["fields"] and f["type"] != "multipleRecordLinks"]
            pending: List[Dict[str, Any]] = []
            pending_recs: List[str] = []
            skipped = 0
            for rec in self.source.iter_records(self.base_id, table["id"]):
                if rec["id"] in ts["rows"]:
                    continue  # reprise après interruption
                cells = rec.get("fields", {})
                row: Dict[str, Any] = {f"field_{ts['id_field']}": rec["id"]}
                for af in fields:
                    if af["id"] not in cells:
                        continue
                    val = convert_value(af, cells[af["id"]], ts["selects"].get(af["id"]), upload)
                    if val is None:
                        skipped += 1
                        continue
                    row[f"field_{ts['fields'][af['id']]['bf']}"] = val
                pending.append(row)
                pending_recs.append(rec["id"])
                if len(pending) == BATCH:
                    self._flush(ts, pending, pending_recs)
            if pending:
                self._flush(ts, pending, pending_recs)
            ts["data_done"] = True
            self.save()
            note = f" ({skipped} valeur(s) non convertible(s), voir rapport)" if skipped else ""
            self.log(f"Données copiées : {table['name']} — {len(ts['rows'])} ligne(s){note}")

    def _flush(self, ts: Dict[str, Any], rows: List[Dict[str, Any]], recs: List[str]) -> None:
        res = self.target.create_rows(ts["bt"], rows, user_field_names=False)
        for rec_id, item in zip(recs, res["items"]):
            ts["rows"][rec_id] = item["id"]
        rows.clear()
        recs.clear()
        self.save()

    # ----------------------------------------------------------- phase links
    def copy_links(self) -> None:
        for table in self.tables():
            ts = self.state["tables"][table["id"]]
            if ts.get("links_done"):
                continue
            links = [f for f in self.fields(table)
                     if f["type"] == "multipleRecordLinks" and ts["fields"].get(f["id"], {}).get("owner")]
            if not links:
                ts["links_done"] = True
                continue
            updates: List[Dict[str, Any]] = []
            missing = 0
            for rec in self.source.iter_records(self.base_id, table["id"]):
                row_id = ts["rows"].get(rec["id"])
                if row_id is None:
                    continue
                upd: Dict[str, Any] = {"id": row_id}
                for af in links:
                    targets = rec.get("fields", {}).get(af["id"])
                    if not targets:
                        continue
                    trows = self.state["tables"][af["options"]["linkedTableId"]]["rows"]
                    ids = [trows[r] for r in targets if r in trows]
                    missing += len(targets) - len(ids)
                    upd[f"field_{ts['fields'][af['id']]['bf']}"] = ids
                if len(upd) > 1:
                    updates.append(upd)
            for chunk in _chunks(updates, BATCH):
                self.target.update_rows(ts["bt"], chunk, user_field_names=False)
            ts["links_done"] = True
            self.save()
            note = f" — ⚠ {missing} lien(s) vers des lignes absentes" if missing else ""
            self.log(f"Liens posés : {table['name']} ({len(updates)} ligne(s)){note}")

    # ---------------------------------------------------------- phase verify
    def verify(self) -> Dict[str, Any]:
        """Compare lignes et valeurs renseignées, champ par champ. Aucune valeur exportée."""
        report: Dict[str, Any] = {"tables": [], "ok": True}
        for table in self.tables():
            ts = self.state["tables"][table["id"]]
            mapped = [f for f in self.fields(table) if f["id"] in ts["fields"]]
            src_rows, src_counts = 0, {f["id"]: 0 for f in mapped}
            for rec in self.source.iter_records(self.base_id, table["id"]):
                src_rows += 1
                cells = rec.get("fields", {})
                for af in mapped:
                    if not is_empty(cells.get(af["id"])):
                        src_counts[af["id"]] += 1
            dst_rows, dst_counts = 0, {f["id"]: 0 for f in mapped}
            page = 1
            while True:
                res = self.target.list_rows(ts["bt"], page=page, size=200, user_field_names=False)
                for row in res["results"]:
                    dst_rows += 1
                    for af in mapped:
                        if not is_empty(row.get(f"field_{ts['fields'][af['id']]['bf']}")):
                            dst_counts[af["id"]] += 1
                if not res.get("next"):
                    break
                page += 1
            gaps = [(af["name"], src_counts[af["id"]], dst_counts[af["id"]])
                    for af in mapped if src_counts[af["id"]] != dst_counts[af["id"]]]
            ok = src_rows == dst_rows and not gaps
            report["ok"] &= ok
            report["tables"].append({"name": table["name"], "airtable": src_rows,
                                     "baserow": dst_rows, "ecarts": gaps, "ok": ok})
        return report


# ------------------------------------------------------------------ rapports
def plan_to_markdown(plan: Dict[str, Any]) -> str:
    t = plan["totals"]
    lines = [
        "# Plan de migration Airtable → Baserow",
        "",
        "_Rapport sans donnée personnelle : noms de tables/champs et types uniquement._",
        "",
        f"- Champs migrés : **{t['migrés']}** · liens : **{t['liens']}** · "
        f"calculés à recréer : **{t['calculés']}** · ignorés : **{t['ignorés']}** · "
        f"exclus (minimisation) : **{t['exclus']}**",
    ]
    if plan["excluded_tables"]:
        lines.append(f"- Tables exclues : {', '.join(plan['excluded_tables'])}")
    for table in plan["tables"]:
        lines += ["", f"## {table['name']}", "", "| Champ | Type Baserow | Remarque |", "|---|---|---|"]
        for name, btype, note in table["fields"]:
            lines.append(f"| {name} | {btype} | {str(note).replace('|', '¦').replace(chr(10), ' ')} |")
    return "\n".join(lines) + "\n"


def verify_to_markdown(report: Dict[str, Any]) -> str:
    lines = [
        "# Rapprochement d'import Airtable → Baserow",
        "",
        "_Compteurs uniquement — aucune valeur de cellule._",
        "",
        f"**Résultat global : {'CONFORME' if report['ok'] else 'ÉCARTS À ANALYSER'}**",
        "",
        "| Table | Lignes Airtable | Lignes Baserow | État |",
        "|---|---|---|---|",
    ]
    for t in report["tables"]:
        lines.append(f"| {t['name']} | {t['airtable']} | {t['baserow']} | {'OK' if t['ok'] else 'ÉCART'} |")
    for t in report["tables"]:
        if t["ecarts"]:
            lines += ["", f"### Écarts — {t['name']}", "", "| Champ | Renseignés Airtable | Renseignés Baserow |", "|---|---|---|"]
            lines += [f"| {n} | {a} | {b} |" for n, a, b in t["ecarts"]]
    lines += ["", "Validation Direction : nom, date, signature → à reporter dans le registre."]
    return "\n".join(lines) + "\n"
