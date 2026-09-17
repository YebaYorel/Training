#!/usr/bin/env python3
"""
Simulateur des API Airtable et Baserow, pour rejouer la migration à blanc.

    python migration/simulateur.py &
    AIRTABLE_API_URL=http://127.0.0.1:8777 \
    AIRTABLE_TOKEN=test BASEROW_API_URL=http://127.0.0.1:8777 \
    BASEROW_EMAIL=t@t.re BASEROW_PASSWORD=x BASEROW_WORKSPACE_ID=1 \
    python migration/airtable_vers_baserow.py --executer

Pourquoi : la migration écrit dans une base réelle contenant des données de
stagiaires. La rejouer contre un simulateur prouve que le script fonctionne
AVANT qu'il ne touche à quoi que ce soit. Un script de migration qu'on lance
pour la première fois sur les vraies données est un pari, pas une méthode.

Le simulateur sert le schéma Airtable réel (schema-airtable.json) et des
lignes factices, puis se comporte comme Baserow : il vérifie les corps reçus
et refuse ce que Baserow refuserait.
"""

import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

RACINE = Path(__file__).resolve().parent
PORT = int(os.environ.get("PORT_SIMULATEUR", 8777))

SCHEMA = json.loads((RACINE / "schema-airtable.json").read_text(encoding="utf-8"))


def enrichir_liens(schema):
    """Ajoute options.linkedTableId aux champs de liaison.

    Le schéma exporté vient du connecteur MCP, qui ne renvoie pas cette clé.
    L'API REST Metadata d'Airtable, elle, la fournit. On la reconstitue ici
    en rapprochant le nom du champ de celui d'une table, afin de vérifier que
    la passe 2 du migrateur fonctionne quand la donnée est présente.

    Les champs qu'on ne sait pas résoudre restent sans cible : le test couvre
    donc les deux cas, celui qui réussit et celui qui doit alerter.
    """
    par_nom = {t["name"].upper(): t["id"] for t in schema["tables"]}
    resolus = 0
    for t in schema["tables"]:
        for c in t["fields"]:
            if c["type"] != "multipleRecordLinks":
                continue
            base = c["name"].upper().rstrip(" 2").strip()
            if base in par_nom:
                c.setdefault("options", {})["linkedTableId"] = par_nom[base]
                resolus += 1
    return resolus


RESOLUS = enrichir_liens(SCHEMA)

# État de la base Baserow simulée
ETAT = {"bases": {}, "tables": {}, "champs": {}, "lignes": {}, "sequence": 1000}


def _id():
    ETAT["sequence"] += 1
    return ETAT["sequence"]


def _ref(table_id, n):
    """Identifiant de ligne factice, stable et reproductible d'un appel à
    l'autre — sans quoi les liaisons pointeraient dans le vide."""
    return f"rec{table_id[-6:]}{n:03d}"


def lignes_factices(table):
    """Trois lignes par table, avec des valeurs plausibles selon le type."""
    out = []
    for n in range(3):
        f = {}
        for c in table["fields"]:
            t, nom = c["type"], c["name"]
            if "NE PAS REMPLIR" in nom:
                continue                       # jamais de données art. 9
            if t == "singleLineText":
                f[nom] = f"{nom} {n + 1}"
            elif t in ("multilineText", "richText", "aiText"):
                f[nom] = f"Texte long pour {nom}, ligne {n + 1}."
            elif t == "email":
                f[nom] = f"contact{n + 1}@exemple.re"
            elif t == "phoneNumber":
                f[nom] = "0693 00 00 0%d" % n
            elif t == "url":
                f[nom] = "https://exemple.re"
            elif t == "checkbox":
                f[nom] = n % 2 == 0
            elif t in ("number", "currency", "percent", "autoNumber", "count", "rating", "duration"):
                f[nom] = (n + 1) * 7
            elif t in ("date", "dateTime", "createdTime", "lastModifiedTime"):
                f[nom] = "2026-09-1%d" % n
            elif t == "singleSelect":
                choix = (c.get("options") or c.get("config") or {}).get("choices") or []
                if choix:
                    f[nom] = {"id": "sel", "name": choix[n % len(choix)]["name"]}
            elif t == "multipleSelects":
                choix = (c.get("options") or c.get("config") or {}).get("choices") or []
                if choix:
                    f[nom] = [{"id": "sel", "name": choix[0]["name"]}]
            elif t == "multipleRecordLinks":
                # Références vers deux lignes de la table cible. C'est ce qui
                # permet de vérifier le point le plus délicat du migrateur :
                # la correspondance entre identifiants Airtable et Baserow.
                cible = (c.get("options") or {}).get("linkedTableId")
                if cible:
                    f[nom] = [_ref(cible, 0), _ref(cible, 1)]
        out.append({"id": _ref(table["id"], n), "fields": f})
    return out


class Gestionnaire(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass                                   # silence : le test affiche son propre rapport

    def _repondre(self, code, corps):
        brut = json.dumps(corps).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(brut)))
        self.end_headers()
        self.wfile.write(brut)

    def _corps(self):
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}")

    # ── Airtable ──
    def do_GET(self):
        chemin = self.path.split("?")[0]
        if chemin.endswith("/tables") and "/meta/bases/" in chemin:
            return self._repondre(200, SCHEMA)

        m = re.match(r"^/v0/app\w+/(tbl\w+)$", chemin)
        if m:
            table = next((t for t in SCHEMA["tables"] if t["id"] == m.group(1)), None)
            if not table:
                return self._repondre(404, {"error": "table inconnue"})
            return self._repondre(200, {"records": lignes_factices(table)})

        # Baserow : liste des champs d'une table
        m = re.match(r"^/api/database/fields/table/(\d+)/$", chemin)
        if m:
            tid = int(m.group(1))
            return self._repondre(200, ETAT["champs"].get(tid, []))

        return self._repondre(404, {"error": f"GET non simulé : {chemin}"})

    # ── Baserow ──
    def do_POST(self):
        chemin, corps = self.path.split("?")[0], self._corps()

        if chemin == "/api/user/token-auth/":
            if not corps.get("email") or not corps.get("password"):
                return self._repondre(400, {"error": "identifiants manquants"})
            return self._repondre(200, {"token": "jwt-simule"})

        m = re.match(r"^/api/applications/workspace/(\d+)/$", chemin)
        if m:
            bid = _id()
            ETAT["bases"][bid] = corps.get("name")
            return self._repondre(200, {"id": bid, "name": corps.get("name")})

        m = re.match(r"^/api/database/tables/database/(\d+)/$", chemin)
        if m:
            tid = _id()
            ETAT["tables"][tid] = {"base": int(m.group(1)), "nom": corps.get("name")}
            # Baserow crée trois champs par défaut
            ETAT["champs"][tid] = [
                {"id": _id(), "name": "Name", "type": "text", "primary": True},
                {"id": _id(), "name": "Notes", "type": "long_text"},
                {"id": _id(), "name": "Active", "type": "boolean"},
            ]
            ETAT["lignes"][tid] = []
            return self._repondre(200, {"id": tid, "name": corps.get("name")})

        m = re.match(r"^/api/database/fields/table/(\d+)/$", chemin)
        if m:
            tid = int(m.group(1))
            if not corps.get("name"):
                return self._repondre(400, {"error": "nom de champ manquant"})
            if corps.get("type") == "link_row" and not corps.get("link_row_table_id"):
                return self._repondre(400, {"error": "link_row_table_id manquant"})
            champ = {"id": _id(), **corps}
            ETAT["champs"].setdefault(tid, []).append(champ)
            return self._repondre(200, champ)

        m = re.match(r"^/api/database/rows/table/(\d+)/batch/$", chemin)
        if m:
            tid = int(m.group(1))
            connus = {c["name"] for c in ETAT["champs"].get(tid, [])}
            creees = []
            for item in corps.get("items", []):
                inconnus = set(item) - connus
                if inconnus:
                    # Baserow rejette un champ inconnu : on fait pareil,
                    # sinon le test validerait une migration qui échouerait.
                    return self._repondre(400, {"error": f"champs inconnus : {sorted(inconnus)}"})
                ligne = {"id": _id(), **item}
                ETAT["lignes"][tid].append(ligne)
                creees.append(ligne)
            return self._repondre(200, {"items": creees})

        return self._repondre(404, {"error": f"POST non simulé : {chemin}"})

    def do_PATCH(self):
        chemin, corps = self.path.split("?")[0], self._corps()
        m = re.match(r"^/api/database/rows/table/(\d+)/batch/$", chemin)
        if m:
            tid = int(m.group(1))
            connus = {c["name"] for c in ETAT["champs"].get(tid, [])}
            for item in corps.get("items", []):
                inconnus = set(item) - connus - {"id"}
                if inconnus:
                    return self._repondre(400, {"error": f"champs inconnus : {sorted(inconnus)}"})
            return self._repondre(200, {"items": corps.get("items", [])})
        return self._repondre(404, {"error": f"PATCH non simulé : {chemin}"})

    def do_DELETE(self):
        if re.match(r"^/api/database/fields/(\d+)/$", self.path):
            cid = int(self.path.strip("/").split("/")[-1])
            for tid, liste in ETAT["champs"].items():
                ETAT["champs"][tid] = [c for c in liste if c["id"] != cid]
            return self._repondre(204, {})
        return self._repondre(404, {"error": "DELETE non simulé"})


def resume():
    """Rapport d'état, appelé par le script de test après la migration."""
    return {
        "bases": len(ETAT["bases"]),
        "tables": len(ETAT["tables"]),
        "champs": sum(len(v) for v in ETAT["champs"].values()),
        "lignes": sum(len(v) for v in ETAT["lignes"].values()),
    }


if __name__ == "__main__":
    serveur = HTTPServer(("127.0.0.1", PORT), Gestionnaire)
    print(f"Simulateur Airtable + Baserow sur http://127.0.0.1:{PORT}", flush=True)
    try:
        serveur.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
