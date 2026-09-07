#!/usr/bin/env python3
"""CLI Baserow — YEBA FORMATIONS.

Filet de sécurité pour tester la connexion et piloter Baserow sans MCP.

Exemples :
    python -m baserow.cli check
    python -m baserow.cli workspaces
    python -m baserow.cli databases --workspace 123
    python -m baserow.cli create-database --workspace 123 --name "CRM YEBA"
    python -m baserow.cli tables --database 456
"""

from __future__ import annotations

import argparse
import json
import sys

from dotenv import load_dotenv

from baserow import BaserowClient, BaserowError


def _print(obj) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def main(argv=None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description="CLI Baserow — YEBA FORMATIONS")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("check", help="Vérifie la connexion (JWT + workspaces)")
    sub.add_parser("workspaces", help="Liste les workspaces")

    p = sub.add_parser("databases", help="Liste les bases d'un workspace")
    p.add_argument("--workspace", type=int, required=True)

    p = sub.add_parser("create-database", help="Crée une base")
    p.add_argument("--workspace", type=int, required=True)
    p.add_argument("--name", required=True)

    p = sub.add_parser("tables", help="Liste les tables d'une base")
    p.add_argument("--database", type=int, required=True)

    p = sub.add_parser("fields", help="Liste les champs d'une table")
    p.add_argument("--table", type=int, required=True)

    args = parser.parse_args(argv)
    client = BaserowClient()

    try:
        if args.cmd == "check":
            # Ce qui a été lu dans .env (masqué) — pour repérer typo/espace.
            print("=== Ce que je lis dans .env ===")
            print(f"  API_URL      : {client.api_url}")
            print(f"  EMAIL        : {client.email!r}")
            pw = client.password or ""
            print(f"  PASSWORD     : {'*' * len(pw)}  ({len(pw)} caractères)")
            tok = client.database_token or ""
            print(f"  TOKEN        : {'défini (' + str(len(tok)) + ' car.)' if tok else 'vide'}")
            print()
            result = client.health_check()
            print("=== Résultat de la connexion ===")
            _print(result)
            print()
            token_ok = result.get("token") == "OK"
            jwt_ok = result.get("jwt") == "OK"
            if token_ok and jwt_ok:
                print("✅ TOUT est connecté : données ET création de bases possibles.")
            elif token_ok:
                print("✅ JETON OK → Claude peut LIRE/ÉCRIRE des données tout de suite.")
                print("ℹ️  Mot de passe non validé → la CRÉATION de bases se fera plus tard.")
            elif jwt_ok:
                print("✅ MOT DE PASSE OK → création de bases possible.")
            else:
                print("❌ Ni le jeton ni le mot de passe ne sont acceptés. Copiez-moi ce résultat.")
        elif args.cmd == "workspaces":
            _print(client.list_workspaces())
        elif args.cmd == "databases":
            _print(client.list_databases(args.workspace))
        elif args.cmd == "create-database":
            _print(client.create_database(args.workspace, args.name))
        elif args.cmd == "tables":
            _print(client.list_tables(args.database))
        elif args.cmd == "fields":
            _print(client.list_fields(args.table))
    except BaserowError as exc:
        print(f"[ERREUR] {exc}", file=sys.stderr)
        if exc.body:
            print(json.dumps(exc.body, indent=2, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
