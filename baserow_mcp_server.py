#!/usr/bin/env python3
"""Serveur MCP Baserow — YEBA FORMATIONS.

Expose Baserow à Claude Code sous forme d'outils natifs. Enregistré via
« .mcp.json », il permet à Claude de créer des bases, tables, champs et lignes
directement dans votre instance Baserow (cloud UE), sans qu'aucune donnée ne
transite par un service tiers.

Lancement autonome (debug) :  python3 baserow_mcp_server.py
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()  # charge .env (secrets locaux, jamais committés)

from mcp.server.fastmcp import FastMCP  # noqa: E402

from baserow import BaserowClient, BaserowError  # noqa: E402

mcp = FastMCP("baserow-yeba")
_client: Optional[BaserowClient] = None


def client() -> BaserowClient:
    global _client
    if _client is None:
        _client = BaserowClient()
    return _client


def _wrap(fn):
    """Convertit les erreurs Baserow en message lisible pour Claude."""
    try:
        return fn()
    except BaserowError as exc:
        return {"error": str(exc), "status": exc.status, "detail": exc.body}


# --------------------------------------------------------------------- OUTILS
@mcp.tool()
def baserow_health_check() -> Dict[str, Any]:
    """Vérifie la connexion à Baserow (auth JWT + liste des workspaces)."""
    return _wrap(lambda: client().health_check())


@mcp.tool()
def list_workspaces() -> Any:
    """Liste les workspaces (groupes) accessibles."""
    return _wrap(lambda: client().list_workspaces())


@mcp.tool()
def list_databases(workspace_id: int) -> Any:
    """Liste les bases de données d'un workspace."""
    return _wrap(lambda: client().list_databases(workspace_id))


@mcp.tool()
def create_database(workspace_id: int, name: str) -> Any:
    """Crée une nouvelle base de données dans un workspace."""
    return _wrap(lambda: client().create_database(workspace_id, name))


@mcp.tool()
def list_tables(database_id: int) -> Any:
    """Liste les tables d'une base."""
    return _wrap(lambda: client().list_tables(database_id))


@mcp.tool()
def create_table(database_id: int, name: str) -> Any:
    """Crée une table simple (champ primaire 'Name')."""
    return _wrap(lambda: client().create_table(database_id, name))


@mcp.tool()
def list_fields(table_id: int) -> Any:
    """Liste les champs (colonnes) d'une table."""
    return _wrap(lambda: client().list_fields(table_id))


@mcp.tool()
def create_field(table_id: int, name: str, field_type: str, options_json: str = "{}") -> Any:
    """Crée un champ. field_type : text, long_text, number, boolean, date,
    email, url, phone_number, rating, single_select, multiple_select,
    link_row, formula, ... options_json : JSON des options propres au type
    (ex. {"select_options":[{"value":"Chaud"},{"value":"Froid"}]})."""
    options = json.loads(options_json or "{}")
    return _wrap(lambda: client().create_field(table_id, name, field_type, **options))


@mcp.tool()
def create_table_with_schema(database_id: int, name: str, fields_json: str) -> Any:
    """Crée une table ET son schéma complet en une fois.
    fields_json : liste JSON de champs, ex.
    [{"name":"Entreprise","type":"text"},
     {"name":"Statut","type":"single_select",
      "select_options":[{"value":"Prospect"},{"value":"Client"}]},
     {"name":"CA","type":"number","number_decimal_places":2}]
    Le premier champ devient le champ primaire."""
    fields: List[Dict[str, Any]] = json.loads(fields_json)
    return _wrap(lambda: client().create_table_with_schema(database_id, name, fields))


@mcp.tool()
def list_rows(table_id: int, page: int = 1, size: int = 100, search: str = "") -> Any:
    """Liste les lignes d'une table (noms de champs lisibles)."""
    return _wrap(lambda: client().list_rows(table_id, page=page, size=size, search=search or None))


@mcp.tool()
def create_rows(table_id: int, rows_json: str) -> Any:
    """Insère plusieurs lignes en lot. rows_json : liste JSON d'objets
    {nom_de_champ: valeur}."""
    rows = json.loads(rows_json)
    return _wrap(lambda: client().create_rows(table_id, rows))


@mcp.tool()
def update_row(table_id: int, row_id: int, values_json: str) -> Any:
    """Met à jour une ligne. values_json : objet JSON {champ: valeur}."""
    values = json.loads(values_json)
    return _wrap(lambda: client().update_row(table_id, row_id, values))


@mcp.tool()
def delete_row(table_id: int, row_id: int) -> Any:
    """Supprime une ligne."""
    return _wrap(lambda: (client().delete_row(table_id, row_id), {"deleted": row_id})[1])


if __name__ == "__main__":
    mcp.run()
