"""Tests hors ligne de la migration (faux Airtable + faux Baserow en mémoire).

    python -m unittest discover -s tests -v
"""

import copy
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from migration.engine import ID_FIELD_NAME, Migration, MigrationError, plan_to_markdown, verify_to_markdown  # noqa: E402
from migration.mapping import convert_value, plan_field  # noqa: E402

CONFIG = {
    "guard": {"table": "Paramètres", "key_field": "Clé", "value_field": "Valeur",
              "mode_key": "MODE_DONNEES", "allow_key": "PASSAGE_REEL_AUTORISE"},
    "exclude_field_patterns": ["DÉPRÉCIÉ"],
    "exclude_fields": ["Paramètres::Valeur confidentielle (direction)"],
}

SCHEMA = [
    {"id": "tblPAR", "name": "Paramètres", "primaryFieldId": "fldCLE", "fields": [
        {"id": "fldCLE", "name": "Clé", "type": "singleLineText"},
        {"id": "fldVAL", "name": "Valeur", "type": "singleLineText"},
        {"id": "fldSEC", "name": "Valeur confidentielle (direction)", "type": "singleLineText"},
    ]},
    {"id": "tblFAM", "name": "Familles", "primaryFieldId": "fldFNOM", "fields": [
        {"id": "fldFNOM", "name": "Nom famille", "type": "singleLineText"},
        {"id": "fldFENF", "name": "Enfants", "type": "multipleRecordLinks",
         "options": {"linkedTableId": "tblENF", "inverseLinkFieldId": "fldEFAM"}},
    ]},
    {"id": "tblENF", "name": "Enfants", "primaryFieldId": "fldENOM", "fields": [
        {"id": "fldENOM", "name": "Prénom", "type": "singleLineText"},
        {"id": "fldEFAM", "name": "Famille", "type": "multipleRecordLinks",
         "options": {"linkedTableId": "tblFAM", "inverseLinkFieldId": "fldFENF"}},
        {"id": "fldFRAT", "name": "Fratrie", "type": "multipleRecordLinks",
         "options": {"linkedTableId": "tblENF"}},
        {"id": "fldSTAT", "name": "Statut", "type": "singleSelect",
         "options": {"choices": [{"id": "s1", "name": "Actif", "color": "greenBright"},
                                 {"id": "s2", "name": "Inactif", "color": "grayBright"}]}},
        {"id": "fldNAIS", "name": "Naissance", "type": "date", "options": {"dateFormat": {"name": "european"}}},
        {"id": "fldPAI", "name": "PAI fourni", "type": "checkbox"},
        {"id": "fldDOC", "name": "Pièces", "type": "multipleAttachments"},
        {"id": "fldAGE", "name": "Âge", "type": "formula",
         "options": {"formula": "DATETIME_DIFF(TODAY(), {fldNAIS}, 'years')"}},
        {"id": "fldOLD", "name": "⛔ DÉPRÉCIÉ — ancien champ", "type": "singleLineText"},
    ]},
]


def records(mode="FICTIF", allow="Non"):
    return {
        "tblPAR": [
            {"id": "recP1", "fields": {"fldCLE": "MODE_DONNEES", "fldVAL": mode}},
            {"id": "recP2", "fields": {"fldCLE": "PASSAGE_REEL_AUTORISE", "fldVAL": allow}},
            {"id": "recP3", "fields": {"fldCLE": "CODE_PORTAIL", "fldVAL": "en main propre", "fldSEC": "1234"}},
        ],
        "tblFAM": [
            {"id": "recF1", "fields": {"fldFNOM": "Famille TEST A", "fldFENF": ["recE1", "recE2"]}},
            {"id": "recF2", "fields": {"fldFNOM": "Famille TEST B", "fldFENF": ["recE3"]}},
        ],
        "tblENF": [
            {"id": "recE1", "fields": {"fldENOM": "Léa", "fldEFAM": ["recF1"], "fldFRAT": ["recE2"],
                                       "fldSTAT": "Actif", "fldNAIS": "2017-05-02", "fldPAI": True,
                                       "fldDOC": [{"url": "https://dl.airtable.test/x", "filename": "fiche.pdf"}],
                                       "fldAGE": 9, "fldOLD": "ne doit pas partir"}},
            {"id": "recE2", "fields": {"fldENOM": "Noé", "fldEFAM": ["recF1"], "fldFRAT": ["recE1"],
                                       "fldSTAT": "Inactif"}},
            {"id": "recE3", "fields": {"fldENOM": "Inès", "fldEFAM": ["recF2"]}},
        ],
    }


class FakeAirtable:
    def __init__(self, recs):
        self.recs = recs
        self.calls = []

    def get_schema(self, base_id):
        return copy.deepcopy(SCHEMA)

    def iter_records(self, base_id, table_id):
        self.calls.append(table_id)
        yield from copy.deepcopy(self.recs[table_id])


class FakeBaserow:
    """Imite le comportement utile de l'API Baserow (liens réciproques inclus)."""

    def __init__(self):
        self.next_id = 1
        self.tables = {}   # id -> {"name", "fields": {fid: field}, "rows": {rid: row}}
        self.uploads = []

    def _id(self):
        self.next_id += 1
        return self.next_id

    def create_database(self, ws, name):
        return {"id": self._id(), "name": name}

    def list_tables(self, db):
        return []

    def create_table(self, db, name, primary_field_name=None):
        tid = self._id()
        fid = self._id()
        self.tables[tid] = {"name": name, "rows": {},
                            "fields": {fid: {"id": fid, "name": primary_field_name, "type": "text", "primary": True}}}
        return {"id": tid, "name": name}

    def list_fields(self, tid):
        return list(self.tables[tid]["fields"].values())

    def _field_table(self, fid):
        return next(t for t in self.tables.values() if fid in t["fields"])

    def create_field(self, tid, name, ftype, **opts):
        names = {f["name"] for f in self.tables[tid]["fields"].values()}
        assert name not in names, f"nom en double : {name}"
        fid = self._id()
        field = {"id": fid, "name": name, "type": ftype, **opts}
        if ftype in ("single_select", "multiple_select"):
            field["select_options"] = [{"id": self._id(), **o} for o in opts["select_options"]]
        self.tables[tid]["fields"][fid] = field
        if ftype == "link_row" and opts.get("has_related_field"):
            rid = self._id()
            tgt = opts["link_row_table_id"]
            self.tables[tgt]["fields"][rid] = {"id": rid, "name": self.tables[tid]["name"], "type": "link_row",
                                               "link_row_table_id": tid, "related": fid}
            field["related"] = rid
            field["link_row_related_field_id"] = rid
        return field

    def update_field(self, fid, **changes):
        self._field_table(fid)["fields"][fid].update(changes)
        return self._field_table(fid)["fields"][fid]

    def upload_file_via_url(self, url):
        self.uploads.append(url)
        return {"name": f"stored_{len(self.uploads)}.pdf"}

    def create_rows(self, tid, rows, user_field_names=True):
        assert not user_field_names
        assert len(rows) <= 200
        items = []
        for r in rows:
            rid = self._id()
            self.tables[tid]["rows"][rid] = {"id": rid, **r}
            items.append({"id": rid})
        return {"items": items}

    def update_rows(self, tid, rows, user_field_names=True):
        for r in rows:
            row = self.tables[tid]["rows"][r["id"]]
            for k, v in r.items():
                if k == "id":
                    continue
                row[k] = v
                fid = int(k.split("_")[1])
                field = self.tables[tid]["fields"][fid]
                rel = field.get("related")
                if rel:  # entretien du côté inverse, comme Baserow
                    tgt = self.tables[field["link_row_table_id"]]
                    for trow in tgt["rows"].values():
                        cur = set(trow.get(f"field_{rel}", []))
                        cur.discard(r["id"])
                        if trow["id"] in v:
                            cur.add(r["id"])
                        trow[f"field_{rel}"] = sorted(cur)
        return {"items": rows}

    def list_rows(self, tid, page=1, size=100, user_field_names=True):
        rows = list(self.tables[tid]["rows"].values())
        start = (page - 1) * size
        return {"results": rows[start:start + size], "next": start + size < len(rows) or None}


class MappingTests(unittest.TestCase):
    def test_types(self):
        self.assertEqual(plan_field({"type": "formula"})[0], None)
        self.assertEqual(plan_field({"type": "currency", "options": {"precision": 0}})[1]["number_decimal_places"], 2)
        self.assertEqual(plan_field({"type": "dateTime", "options": {"timeZone": "Indian/Reunion"}})[1]
                         ["date_force_timezone"], "Indian/Reunion")
        self.assertEqual(plan_field({"type": "singleCollaborator"})[0], "text")

    def test_collaborateur_minimise(self):
        v = convert_value({"type": "singleCollaborator"}, {"id": "usr1", "email": "x@y.fr", "name": "Stan"})
        self.assertEqual(v, "Stan")

    def test_select_inconnu_non_invente(self):
        self.assertIsNone(convert_value({"type": "singleSelect"}, "Zzz", {"Actif": 3}))


class MigrationTests(unittest.TestCase):
    def run_all(self, recs=None, state_path=None, target=None):
        src = FakeAirtable(recs or records())
        tgt = target or FakeBaserow()
        mig = Migration(src, tgt, "appTEST", CONFIG, state_path, log=lambda *_: None)
        mig.guard_real_data(confirm_real=False)
        mig.create_schema(1, "Anim'Loisirs 974 — TEST")
        mig.copy_data()
        mig.copy_links()
        return mig, src, tgt

    def test_migration_complete_et_conforme(self):
        mig, _, tgt = self.run_all()
        report = mig.verify()
        self.assertTrue(report["ok"], verify_to_markdown(report))
        self.assertEqual({t["name"]: t["baserow"] for t in report["tables"]},
                         {"Paramètres": 3, "Familles": 2, "Enfants": 3})
        self.assertEqual(tgt.uploads, ["https://dl.airtable.test/x"])

    def test_exclusions_minimisation(self):
        _, _, tgt = self.run_all()
        all_names = {f["name"] for t in tgt.tables.values() for f in t["fields"].values()}
        self.assertNotIn("Valeur confidentielle (direction)", all_names)
        self.assertNotIn("⛔ DÉPRÉCIÉ — ancien champ", all_names)
        self.assertNotIn("Âge", all_names)  # calculé : à recréer, pas figé
        self.assertIn(ID_FIELD_NAME, all_names)
        dump = repr(tgt.tables)
        self.assertNotIn("1234", dump)
        self.assertNotIn("ne doit pas partir", dump)

    def test_lien_reciproque_cree_une_seule_fois(self):
        mig, _, tgt = self.run_all()
        fam = mig.state["tables"]["tblFAM"]
        enf = mig.state["tables"]["tblENF"]
        self.assertTrue(fam["fields"]["fldFENF"]["owner"])
        self.assertFalse(enf["fields"]["fldEFAM"]["owner"])
        self.assertEqual(tgt.tables[enf["bt"]]["fields"][enf["fields"]["fldEFAM"]["bf"]]["name"], "Famille")

    def test_garde_fou_reel(self):
        src = FakeAirtable(records(mode="RÉEL", allow="Non"))
        mig = Migration(src, FakeBaserow(), "appTEST", CONFIG, log=lambda *_: None)
        with self.assertRaises(MigrationError):
            mig.guard_real_data(confirm_real=True)
        src = FakeAirtable(records(mode="RÉEL", allow="Oui"))
        mig = Migration(src, FakeBaserow(), "appTEST", CONFIG, log=lambda *_: None)
        with self.assertRaises(MigrationError):
            mig.guard_real_data(confirm_real=False)
        self.assertIn("autorisé", mig.guard_real_data(confirm_real=True))

    def test_reprise_sans_doublon(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "state.json")
            mig, _, tgt = self.run_all(state_path=path)
            mig2 = Migration(FakeAirtable(records()), tgt, "appTEST", CONFIG, path, log=lambda *_: None)
            mig2.create_schema(1, "x")
            mig2.copy_data()
            self.assertTrue(mig2.verify()["ok"])
            with open(path, encoding="utf-8") as fh:
                state = fh.read()
            self.assertNotIn("Léa", state)  # l'état ne contient que des identifiants

    def test_plan_sans_donnees(self):
        mig = Migration(None, None, "appTEST", CONFIG, schema=copy.deepcopy(SCHEMA))
        md = plan_to_markdown(mig.plan())
        self.assertIn("À RECRÉER", md)
        self.assertIn("{Naissance}", md)
        self.assertIn("EXCLU", md)


if __name__ == "__main__":
    unittest.main()
