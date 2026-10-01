"""Lecture Airtable en LECTURE SEULE.

Sécurité :
* seules des requêtes GET sont émises (vérifié dans `_get`) ; le jeton
  personnel (PAT) doit de toute façon être créé avec les seuls scopes
  `data.records:read` et `schema.bases:read`, limité à UNE base ;
* le jeton n'est jamais journalisé ni écrit sur disque ;
* HTTPS obligatoire.

Sources : https://airtable.com/developers/web/api/introduction
          https://airtable.com/developers/web/api/rate-limits (5 req/s par base)
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict, Iterator, List, Optional

import requests

API_URL = "https://api.airtable.com"


class AirtableError(RuntimeError):
    def __init__(self, message: str, status: Optional[int] = None):
        super().__init__(message)
        self.status = status


class AirtableSource:
    """Client Airtable minimal, en lecture seule."""

    MIN_INTERVAL = 0.22  # ≈ 4,5 req/s : sous la limite de 5 req/s par base

    def __init__(self, token: Optional[str] = None, timeout: int = 30) -> None:
        self.token = token or os.getenv("AIRTABLE_PAT")
        if not self.token:
            raise AirtableError(
                "AIRTABLE_PAT absent : créez un jeton personnel Airtable en lecture "
                "seule (data.records:read + schema.bases:read), limité à la base à migrer."
            )
        self.timeout = timeout
        self._session = requests.Session()
        self._last_call = 0.0

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{API_URL}{path}"
        assert url.startswith("https://"), "HTTPS obligatoire"
        for attempt in range(6):
            wait = self.MIN_INTERVAL - (time.monotonic() - self._last_call)
            if wait > 0:
                time.sleep(wait)
            self._last_call = time.monotonic()
            resp = self._session.request(
                "GET",
                url,
                headers={"Authorization": f"Bearer {self.token}"},
                params=params,
                timeout=self.timeout,
            )
            if resp.status_code == 429:  # Airtable impose 30 s de pause
                time.sleep(30)
                continue
            if resp.status_code in (502, 503, 504):
                time.sleep(2 ** attempt)
                continue
            if resp.status_code >= 400:
                # Le corps d'erreur Airtable ne contient pas de données d'enregistrement.
                raise AirtableError(f"GET {path} → HTTP {resp.status_code}: {resp.text[:300]}", resp.status_code)
            return resp.json()
        raise AirtableError(f"GET {path} : échecs répétés (limitation de débit ?)")

    def get_schema(self, base_id: str) -> List[Dict[str, Any]]:
        """Schéma complet (tables, champs, options) — format de l'API meta."""
        return self._get(f"/v0/meta/bases/{base_id}/tables")["tables"]

    def iter_records(self, base_id: str, table_id: str) -> Iterator[Dict[str, Any]]:
        """Tous les enregistrements d'une table, valeurs indexées par ID de champ."""
        params: Dict[str, Any] = {"pageSize": 100, "returnFieldsByFieldId": "true"}
        while True:
            page = self._get(f"/v0/{base_id}/{table_id}", params)
            yield from page.get("records", [])
            offset = page.get("offset")
            if not offset:
                return
            params["offset"] = offset
