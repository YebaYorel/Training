#!/usr/bin/env python3
"""Migration sécurisée Airtable → Baserow.

    python -m migration plan    --base appXXXX [--schema-file schema.json]
    python -m migration migrate --base appXXXX --workspace 123 --database-name "Anim'Loisirs 974"
    python -m migration verify  --base appXXXX

Sous-phases (reprise après incident) : schema, data, links, verify.
Toutes les écritures se font côté Baserow ; Airtable est lu en lecture seule.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from dotenv import load_dotenv

from .engine import Migration, MigrationError, plan_to_markdown, verify_to_markdown

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG = os.path.join(HERE, "config_anim_loisirs.json")
OUT_DIR = "migration_state"  # ignoré par Git


def _write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"→ {path}")


def main(argv=None) -> int:
    load_dotenv()
    ap = argparse.ArgumentParser(description="Migration Airtable → Baserow (lecture seule côté Airtable)")
    ap.add_argument("phase", choices=["plan", "migrate", "schema", "data", "links", "verify"])
    ap.add_argument("--base", default=os.getenv("AIRTABLE_BASE_ID"), help="ID de la base Airtable (app…)")
    ap.add_argument("--config", default=DEFAULT_CONFIG)
    ap.add_argument("--schema-file", help="Schéma JSON (API meta) pour un plan hors ligne")
    ap.add_argument("--workspace", type=int, default=int(os.getenv("BASEROW_WORKSPACE_ID") or 0) or None)
    ap.add_argument("--database-name")
    ap.add_argument("--database-id", type=int)
    ap.add_argument("--confirm-real", action="store_true",
                    help="Autorise des données RÉELLES (exige aussi PASSAGE_REEL_AUTORISE=Oui)")
    ap.add_argument("--yes", action="store_true", help="Ne pas demander de confirmation interactive")
    args = ap.parse_args(argv)
    if not args.base:
        ap.error("--base (ou AIRTABLE_BASE_ID) requis")

    with open(args.config, encoding="utf-8") as fh:
        config = json.load(fh)
    state_path = os.path.join(OUT_DIR, f"{args.base}.json")

    schema = None
    if args.schema_file:
        with open(args.schema_file, encoding="utf-8") as fh:
            data = json.load(fh)
        schema = data["tables"] if isinstance(data, dict) else data

    try:
        if args.phase == "plan":
            source = None if schema else _source()
            mig = Migration(source, None, args.base, config, None, schema=schema)
            _write(os.path.join(OUT_DIR, "plan_migration.md"), plan_to_markdown(mig.plan()))
            return 0

        from baserow import BaserowClient

        target = BaserowClient()
        target.database_token = None  # structure + données : compte de service (JWT) uniquement
        if not target.api_url.startswith("https://"):
            raise MigrationError("BASEROW_API_URL doit être en HTTPS.")
        mig = Migration(_source(), target, args.base, config, state_path, schema=schema)

        if args.phase in ("migrate", "schema", "data"):
            verdict = mig.guard_real_data(args.confirm_real)
            print(f"Garde-fou données : {verdict}")
            if not args.yes:
                plan = mig.plan()["totals"]
                print(f"Prévu : {plan['migrés']} champs, {plan['liens']} liens, "
                      f"{plan['exclus']} exclus, {plan['calculés']} calculés à recréer.")
                if input("Tapez MIGRER pour écrire dans Baserow : ").strip() != "MIGRER":
                    print("Abandon : rien n'a été écrit.")
                    return 1

        if args.phase in ("migrate", "schema"):
            mig.create_schema(args.workspace, args.database_name, args.database_id)
        if args.phase in ("migrate", "data"):
            mig.copy_data()
        if args.phase in ("migrate", "links"):
            mig.copy_links()
        if args.phase in ("migrate", "verify"):
            report = mig.verify()
            _write(os.path.join(OUT_DIR, "rapprochement.md"), verify_to_markdown(report))
            print("✅ CONFORME" if report["ok"] else "⚠ ÉCARTS À ANALYSER (voir rapprochement.md)")
            return 0 if report["ok"] else 2
    except MigrationError as exc:
        print(f"[REFUS] {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001
        # Message tronqué : on évite de recracher un corps de réponse contenant des données.
        print(f"[ERREUR] {type(exc).__name__}: {str(exc)[:300]}", file=sys.stderr)
        print("L'état est sauvegardé : relancez la même phase pour reprendre.", file=sys.stderr)
        return 1
    return 0


def _source():
    from .airtable_source import AirtableSource

    return AirtableSource()


if __name__ == "__main__":
    raise SystemExit(main())
