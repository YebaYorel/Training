"""Client Baserow — YEBA FORMATIONS.

Deux modes d'authentification, conformément au modèle de sécurité Baserow :

* JWT (email + mot de passe d'un compte de service Builder) → requis pour créer
  ou modifier la STRUCTURE (bases/applications, tables, champs). Le jeton JWT
  expire (~10-15 min) : il est renouvelé automatiquement sur erreur 401.
* Database Token (Authorization: Token …) → suffit pour les DONNÉES (lignes).

Source du modèle d'auth : https://baserow.io/user-docs/personal-api-tokens
et https://baserow.io/user-docs/database-api

Aucune donnée n'est envoyée ailleurs que vers votre instance Baserow (UE).
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict, Iterable, List, Optional

import requests


class BaserowError(RuntimeError):
    """Erreur renvoyée par l'API Baserow, avec le corps de réponse si présent."""

    def __init__(self, message: str, status: Optional[int] = None, body: Any = None):
        super().__init__(message)
        self.status = status
        self.body = body


class BaserowClient:
    """Client minimal et robuste pour l'API REST Baserow."""

    def __init__(
        self,
        api_url: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
        timeout: int = 30,
    ) -> None:
        self.api_url = (api_url or os.getenv("BASEROW_API_URL", "https://api.baserow.io")).rstrip("/")
        self.email = email or os.getenv("BASEROW_EMAIL")
        self.password = password or os.getenv("BASEROW_PASSWORD")
        self.database_token = token or os.getenv("BASEROW_TOKEN") or None
        self.timeout = timeout

        self._jwt: Optional[str] = None
        self._session = requests.Session()

    # ------------------------------------------------------------------ auth
    def _authenticate(self) -> str:
        """Obtient un JWT via email + mot de passe (compte de service)."""
        if not self.email or not self.password:
            raise BaserowError(
                "Identifiants JWT manquants : renseignez BASEROW_EMAIL et "
                "BASEROW_PASSWORD (compte de service Builder) pour créer de la structure."
            )
        resp = self._session.post(
            f"{self.api_url}/api/user/token-auth/",
            json={"email": self.email, "password": self.password},
            timeout=self.timeout,
        )
        if resp.status_code != 200:
            raise BaserowError(
                "Échec d'authentification JWT auprès de Baserow.",
                status=resp.status_code,
                body=_safe_json(resp),
            )
        data = resp.json()
        # Baserow récent : "access_token" ; anciennes versions : "token".
        jwt = data.get("access_token") or data.get("token")
        if not jwt:
            raise BaserowError("Réponse d'auth inattendue (aucun jeton).", body=data)
        self._jwt = jwt
        return jwt

    def _jwt_header(self) -> Dict[str, str]:
        if not self._jwt:
            self._authenticate()
        return {"Authorization": f"JWT {self._jwt}"}

    def _token_header(self) -> Dict[str, str]:
        if not self.database_token:
            raise BaserowError("BASEROW_TOKEN non défini pour l'accès aux données.")
        return {"Authorization": f"Token {self.database_token}"}

    # --------------------------------------------------------------- request
    def _request(
        self,
        method: str,
        path: str,
        *,
        auth: str = "jwt",
        params: Optional[Dict[str, Any]] = None,
        json_body: Any = None,
        _retried: bool = False,
    ) -> Any:
        """Effectue une requête. auth = 'jwt' | 'token' | 'auto'.

        'auto' : privilégie le Database Token si présent (limite l'usage du JWT),
        sinon bascule sur JWT. Utilisé pour les opérations sur les lignes.
        """
        url = f"{self.api_url}{path}"
        if auth == "auto":
            headers = self._token_header() if self.database_token else self._jwt_header()
        elif auth == "token":
            headers = self._token_header()
        else:
            headers = self._jwt_header()

        resp = self._session.request(
            method, url, headers=headers, params=params, json=json_body, timeout=self.timeout
        )

        # JWT expiré → on se ré-authentifie une fois puis on retente.
        if resp.status_code == 401 and auth in ("jwt", "auto") and not _retried:
            self._jwt = None
            headers_use_jwt = auth == "jwt" or (auth == "auto" and not self.database_token)
            if headers_use_jwt:
                self._authenticate()
                return self._request(
                    method, path, auth=auth, params=params, json_body=json_body, _retried=True
                )

        if resp.status_code >= 400:
            raise BaserowError(
                f"{method} {path} → HTTP {resp.status_code}",
                status=resp.status_code,
                body=_safe_json(resp),
            )
        if resp.status_code == 204 or not resp.content:
            return None
        return resp.json()

    # =============================================================== WORKSPACES
    def list_workspaces(self) -> List[Dict[str, Any]]:
        """Liste les workspaces (groupes) accessibles au compte de service."""
        return self._request("GET", "/api/workspaces/")

    # ============================================================== APPLICATIONS
    def list_databases(self, workspace_id: int) -> List[Dict[str, Any]]:
        """Liste les bases (applications de type database) d'un workspace."""
        apps = self._request("GET", f"/api/applications/workspace/{workspace_id}/")
        return [a for a in apps if a.get("type") == "database"]

    def create_database(self, workspace_id: int, name: str) -> Dict[str, Any]:
        """Crée une nouvelle base (application). Requiert JWT (compte Builder)."""
        return self._request(
            "POST",
            f"/api/applications/workspace/{workspace_id}/",
            json_body={"name": name, "type": "database"},
        )

    # =================================================================== TABLES
    def list_tables(self, database_id: int) -> List[Dict[str, Any]]:
        return self._request("GET", f"/api/database/tables/database/{database_id}/")

    def create_table(self, database_id: int, name: str) -> Dict[str, Any]:
        """Crée une table (avec un champ primaire 'Name' par défaut)."""
        return self._request(
            "POST",
            f"/api/database/tables/database/{database_id}/",
            json_body={"name": name},
        )

    def delete_table(self, table_id: int) -> None:
        self._request("DELETE", f"/api/database/tables/{table_id}/")

    # =================================================================== FIELDS
    def list_fields(self, table_id: int) -> List[Dict[str, Any]]:
        return self._request("GET", f"/api/database/fields/table/{table_id}/")

    def create_field(self, table_id: int, name: str, field_type: str, **options: Any) -> Dict[str, Any]:
        """Crée un champ.

        field_type : 'text', 'long_text', 'number', 'boolean', 'date', 'email',
        'url', 'phone_number', 'rating', 'single_select', 'multiple_select',
        'link_row', 'formula', ...
        options : paramètres propres au type (ex. select_options=[{'value': 'A'}],
        link_row_table_id=123, number_decimal_places=2, date_format='ISO').
        """
        body = {"name": name, "type": field_type, **options}
        return self._request("POST", f"/api/database/fields/table/{table_id}/", json_body=body)

    def update_field(self, field_id: int, **changes: Any) -> Dict[str, Any]:
        return self._request("PATCH", f"/api/database/fields/{field_id}/", json_body=changes)

    def delete_field(self, field_id: int) -> None:
        self._request("DELETE", f"/api/database/fields/{field_id}/")

    # ===================================================================== ROWS
    def list_rows(
        self,
        table_id: int,
        *,
        page: int = 1,
        size: int = 100,
        user_field_names: bool = True,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "page": page,
            "size": size,
            "user_field_names": str(user_field_names).lower(),
        }
        if search:
            params["search"] = search
        return self._request(
            "GET", f"/api/database/rows/table/{table_id}/", auth="auto", params=params
        )

    def create_row(self, table_id: int, values: Dict[str, Any], user_field_names: bool = True) -> Dict[str, Any]:
        return self._request(
            "POST",
            f"/api/database/rows/table/{table_id}/",
            auth="auto",
            params={"user_field_names": str(user_field_names).lower()},
            json_body=values,
        )

    def create_rows(self, table_id: int, rows: Iterable[Dict[str, Any]], user_field_names: bool = True) -> Dict[str, Any]:
        """Insertion en lot (endpoint batch)."""
        return self._request(
            "POST",
            f"/api/database/rows/table/{table_id}/batch/",
            auth="auto",
            params={"user_field_names": str(user_field_names).lower()},
            json_body={"items": list(rows)},
        )

    def update_row(self, table_id: int, row_id: int, values: Dict[str, Any], user_field_names: bool = True) -> Dict[str, Any]:
        return self._request(
            "PATCH",
            f"/api/database/rows/table/{table_id}/{row_id}/",
            auth="auto",
            params={"user_field_names": str(user_field_names).lower()},
            json_body=values,
        )

    def delete_row(self, table_id: int, row_id: int) -> None:
        self._request("DELETE", f"/api/database/rows/table/{table_id}/{row_id}/", auth="auto")

    # ============================================================= COMMODITÉS
    def create_table_with_schema(
        self,
        database_id: int,
        name: str,
        fields: List[Dict[str, Any]],
        drop_default_extra: bool = True,
    ) -> Dict[str, Any]:
        """Crée une table puis y applique un schéma complet en une passe.

        `fields` : liste de dicts {name, type, ...options}. Le PREMIER champ
        renomme/retype le champ primaire par défaut ('Name'). Les champs
        'Notes' et 'Active' créés par défaut par Baserow sont supprimés si
        drop_default_extra=True.

        Renvoie {'table': ..., 'fields': [...]}.
        """
        table = self.create_table(database_id, name)
        table_id = table["id"]
        existing = self.list_fields(table_id)
        primary = next((f for f in existing if f.get("primary")), existing[0] if existing else None)
        extras = [f for f in existing if not f.get("primary")]

        created: List[Dict[str, Any]] = []
        for idx, spec in enumerate(fields):
            spec = dict(spec)
            fname = spec.pop("name")
            ftype = spec.pop("type")
            if idx == 0 and primary:
                # Le champ primaire ne peut pas toujours changer de type ; on tente,
                # sinon on renomme seulement.
                try:
                    created.append(self.update_field(primary["id"], name=fname, type=ftype, **spec))
                except BaserowError:
                    created.append(self.update_field(primary["id"], name=fname))
            else:
                created.append(self.create_field(table_id, fname, ftype, **spec))

        if drop_default_extra:
            for f in extras:
                try:
                    self.delete_field(f["id"])
                except BaserowError:
                    pass

        return {"table": table, "fields": created}

    def check_token(self) -> bool:
        """Valide le Database Token seul (sans mot de passe)."""
        if not self.database_token:
            raise BaserowError("BASEROW_TOKEN non défini.")
        self._request("GET", "/api/database/tokens/check/", auth="token")
        return True

    def health_check(self) -> Dict[str, Any]:
        """Diagnostic tolérant : teste le jeton ET le mot de passe séparément,
        sans planter si l'un des deux échoue. Renvoie un état lisible."""
        result: Dict[str, Any] = {"api_url": self.api_url}

        # --- Jeton (données) ---
        if self.database_token:
            try:
                self.check_token()
                result["token"] = "OK"
            except BaserowError as exc:
                result["token"] = f"ÉCHEC ({exc.status}): {exc.body}"
        else:
            result["token"] = "absent"

        # --- Mot de passe (structure) ---
        has_pw = bool(self.email and self.password and self.password not in ("change-me", ""))
        if has_pw:
            try:
                self._authenticate()
                ws = self.list_workspaces()
                result["jwt"] = "OK"
                result["workspaces"] = [{"id": w["id"], "name": w["name"]} for w in ws]
            except BaserowError as exc:
                result["jwt"] = f"ÉCHEC ({exc.status}): {exc.body}"
        else:
            result["jwt"] = "absent"

        return result


def _safe_json(resp: requests.Response) -> Any:
    try:
        return resp.json()
    except ValueError:
        return resp.text[:500]
