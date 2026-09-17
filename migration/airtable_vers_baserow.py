#!/usr/bin/env python3
"""
Migration Airtable → Baserow pour YEBA FORMATIONS.

    python migration/airtable_vers_baserow.py --plan      # n'écrit RIEN, montre tout
    python migration/airtable_vers_baserow.py --tables "CATALOGUE FORMATIONS"
    python migration/airtable_vers_baserow.py --executer  # migration complète

Variables attendues dans .env :
    AIRTABLE_TOKEN     jeton d'API Airtable (lecture)
    BASEROW_API_URL    https://api.baserow.io
    BASEROW_EMAIL      compte de service, rôle Builder
    BASEROW_PASSWORD   mot de passe du compte de service
    BASEROW_WORKSPACE_ID

═══ CE QUE CE SCRIPT NE FAIT PAS, ET POURQUOI ═══════════════════════════
Une migration Airtable → Baserow n'est pas transposable à 100 %. Quatre
familles de champs demandent une reprise manuelle ; le script les recense
dans un rapport plutôt que de produire une conversion approximative et
silencieuse :

  formula (38)              Baserow a ses propres fonctions. Traduire une
                            formule automatiquement produirait des calculs
                            faux sans le signaler — donc on ne traduit pas.
  multipleAttachments (34)  Les fichiers doivent être téléchargés depuis
                            Airtable puis re-téléversés. Le champ est créé
                            vide ; les fichiers sont à reporter.
  multipleLookupValues (96) Dépend des liens. Recréé après coup dans
                            l'interface, une fois les liaisons vérifiées.
  aiText, createdBy, count   Sans équivalent direct. Signalés, non migrés.

Tout le reste — texte, nombres, dates, sélecteurs, cases, e-mails,
téléphones, URL et LIENS ENTRE TABLES — est migré automatiquement.

═══ RGPD ════════════════════════════════════════════════════════════════
1. Les champs dont le nom contient « NE PAS REMPLIR » ne sont JAMAIS migrés :
   ils relèvent de l'article 9 (données de santé). Vérifié le 17/09/2026 :
   ils sont vides côté Airtable. Ils doivent être supprimés, pas déplacés.
2. La migration déplace des données personnelles de stagiaires vers un
   nouveau sous-traitant. Avant de lancer --executer :
      • signer l'accord de sous-traitance Baserow (art. 28) ;
      • mettre à jour le registre des traitements (art. 30) : Baserow B.V.,
        Pays-Bas, remplace Airtable Inc., États-Unis ;
      • une fois la migration VÉRIFIÉE, supprimer les données chez Airtable
        (art. 5.1.e) — une copie oubliée reste un transfert hors UE.
3. Aucune information des personnes n'est requise au seul titre du
   changement de sous-traitant : le responsable de traitement et les
   finalités sont inchangés. La mention d'information doit toutefois être
   corrigée si elle nommait Airtable ou citait les États-Unis.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parent
BASE_AIRTABLE = "appQ2zqc80kkc6MR1"

# ─── Correspondance des types ────────────────────────────────────────────
SIMPLES = {
    "singleLineText": ("text", {}),
    "multilineText": ("long_text", {}),
    "richText": ("long_text", {}),
    "aiText": ("long_text", {}),
    "email": ("email", {}),
    "url": ("url", {}),
    "phoneNumber": ("phone_number", {}),
    "checkbox": ("boolean", {}),
    "number": ("number", {"number_decimal_places": 0}),
    "autoNumber": ("number", {"number_decimal_places": 0}),
    "count": ("number", {"number_decimal_places": 0}),
    "currency": ("number", {"number_decimal_places": 2}),
    "percent": ("number", {"number_decimal_places": 2}),
    "duration": ("number", {"number_decimal_places": 2}),
    "rating": ("number", {"number_decimal_places": 0}),
    "date": ("date", {"date_format": "EU"}),
    "dateTime": ("date", {"date_format": "EU", "date_include_time": True}),
    "createdTime": ("date", {"date_format": "EU", "date_include_time": True}),
    "lastModifiedTime": ("date", {"date_format": "EU", "date_include_time": True}),
    "singleSelect": ("single_select", {}),
    "multipleSelects": ("multiple_select", {}),
    "multipleAttachments": ("file", {}),
}
LIENS = {"multipleRecordLinks"}
REPRISE_MANUELLE = {
    "formula": "syntaxe de formule propre à chaque outil — à réécrire",
    "rollup": "dépend des liens — à recréer après vérification",
    "multipleLookupValues": "dépend des liens — à recréer après vérification",
    "createdBy": "champ système sans équivalent",
    "lastModifiedBy": "champ système sans équivalent",
    "button": "sans équivalent",
    "barcode": "sans équivalent",
}
# Champs jamais migrés, quel que soit leur type (art. 9 RGPD)
def interdit(nom):
    return "NE PAS REMPLIR" in nom


# ─── Accès HTTP ──────────────────────────────────────────────────────────
def _appel(url, entetes, donnees=None, methode=None):
    corps = json.dumps(donnees).encode() if donnees is not None else None
    if corps:
        entetes = {**entetes, "Content-Type": "application/json"}
    req = urllib.request.Request(url, data=corps, headers=entetes, method=methode)
    for essai in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                brut = r.read()
                return json.loads(brut) if brut else {}
        except urllib.error.HTTPError as e:
            if e.code == 429 and essai < 3:      # limite de débit
                time.sleep(2 ** essai)
                continue
            raise RuntimeError(f"{e.code} sur {url}\n{e.read().decode('utf-8','replace')[:400]}")
        except urllib.error.URLError as e:
            if essai < 3:
                time.sleep(2 ** essai)
                continue
            raise RuntimeError(f"Réseau injoignable : {e}")


class Airtable:
    def __init__(self, jeton, url=None):
        self.h = {"Authorization": f"Bearer {jeton}"}
        # Configurable pour permettre de rejouer la migration contre un
        # simulateur avant de la lancer sur les données réelles.
        self.url = (url or os.environ.get("AIRTABLE_API_URL")
                    or "https://api.airtable.com").rstrip("/")

    def schema(self):
        return _appel(f"{self.url}/v0/meta/bases/{BASE_AIRTABLE}/tables", self.h)

    def lignes(self, table_id):
        out, params = [], {"pageSize": 100}
        while True:
            url = f"{self.url}/v0/{BASE_AIRTABLE}/{table_id}?" + urllib.parse.urlencode(params)
            rep = _appel(url, self.h)
            out += rep.get("records", [])
            if not rep.get("offset"):
                return out
            params["offset"] = rep["offset"]


class Baserow:
    def __init__(self, url, email, mdp):
        self.url = url.rstrip("/")
        jeton = _appel(f"{self.url}/api/user/token-auth/", {}, {"email": email, "password": mdp})
        self.h = {"Authorization": f"JWT {jeton['token']}"}

    def creer_base(self, workspace_id, nom):
        return _appel(f"{self.url}/api/applications/workspace/{workspace_id}/", self.h,
                      {"name": nom, "type": "database"})

    def creer_table(self, base_id, nom):
        return _appel(f"{self.url}/api/database/tables/database/{base_id}/", self.h, {"name": nom})

    def champs(self, table_id):
        return _appel(f"{self.url}/api/database/fields/table/{table_id}/", self.h)

    def creer_champ(self, table_id, corps):
        return _appel(f"{self.url}/api/database/fields/table/{table_id}/", self.h, corps)

    def supprimer_champ(self, champ_id):
        return _appel(f"{self.url}/api/database/fields/{champ_id}/", self.h, methode="DELETE")

    def creer_lignes(self, table_id, lignes):
        return _appel(f"{self.url}/api/database/rows/table/{table_id}/batch/?user_field_names=true",
                      self.h, {"items": lignes})

    def maj_lignes(self, table_id, lignes):
        return _appel(f"{self.url}/api/database/rows/table/{table_id}/batch/?user_field_names=true",
                      self.h, {"items": lignes}, methode="PATCH")


# ─── Conversion ──────────────────────────────────────────────────────────
def aplatir(valeur):
    if isinstance(valeur, dict):
        return valeur.get("name") or valeur.get("url") or valeur.get("text") or ""
    if isinstance(valeur, list):
        return [aplatir(v) for v in valeur]
    return valeur


def cible_liee(champ):
    """Identifiant de la table pointée par un champ de liaison.

    Même précaution que pour les options de sélecteur : l'API REST le place
    sous « options.linkedTableId », d'autres sources sous « config ». Le
    connecteur MCP, lui, ne le renvoie pas du tout — d'où l'alerte bruyante
    en passe 2 plutôt qu'un saut silencieux.
    """
    for cle in ("options", "config"):
        cible = (champ.get(cle) or {}).get("linkedTableId")
        if cible:
            return cible
    return None


def choix_de(champ):
    """Les options d'un sélecteur.

    L'API REST Metadata d'Airtable les place sous « options.choices », le
    connecteur MCP sous « config.choices ». On accepte les deux plutôt que de
    parier sur l'une : un sélecteur migré sans ses options arrive vide dans
    Baserow, et les valeurs des lignes sont alors refusées en silence.
    """
    for cle in ("options", "config"):
        choix = (champ.get(cle) or {}).get("choices")
        if choix:
            return choix
    return []


def definition_champ(champ):
    """Retourne le corps de création Baserow, ou None si non migrable."""
    t = champ["type"]
    if t not in SIMPLES:
        return None
    type_bas, options = SIMPLES[t]
    corps = {"name": champ["name"][:255], "type": type_bas, **options}
    if type_bas in ("single_select", "multiple_select"):
        choix = choix_de(champ)
        if not choix:
            print(f"  ⚠ « {champ['name']} » : sélecteur sans options lisibles — "
                  "les valeurs de ce champ ne seront pas reprises.")
        corps["select_options"] = [{"value": c["name"][:255], "color": "blue"} for c in choix]
    return corps


def valeur_pour(champ, brute):
    t = champ["type"]
    v = aplatir(brute)
    if v is None or v == "" or v == []:
        return None
    if t in ("multipleAttachments",):
        return None                      # fichiers repris séparément
    if t == "multipleSelects":
        return v if isinstance(v, list) else [v]
    if t == "checkbox":
        return bool(v)
    if t in ("number", "currency", "percent", "autoNumber", "count", "rating", "duration"):
        return v
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    return v


# ─── Migration ───────────────────────────────────────────────────────────
def migrer(args):
    from dotenv import load_dotenv
    load_dotenv(RACINE.parent / ".env")

    jeton_at = os.environ.get("AIRTABLE_TOKEN")
    if not jeton_at:
        sys.exit("AIRTABLE_TOKEN absent de .env")

    at = Airtable(jeton_at)
    schema = at.schema()
    tables = schema["tables"]
    if args.tables:
        voulues = {t.strip() for t in args.tables.split(",")}
        tables = [t for t in tables if t["name"] in voulues]
        if not tables:
            sys.exit(f"Aucune table ne correspond à : {args.tables}")

    rapport = {"migre": [], "reprise_manuelle": [], "exclu_rgpd": []}

    # ── Inventaire, toujours affiché ──
    print(f"\n{'TABLE':34} {'CHAMPS':>7} {'AUTO':>6} {'LIENS':>6} {'MANUEL':>7} {'RGPD':>5}")
    print("─" * 70)
    for t in tables:
        auto = liens = manuel = rgpd = 0
        for c in t["fields"]:
            if interdit(c["name"]):
                rgpd += 1
                rapport["exclu_rgpd"].append(f"{t['name']} → {c['name']}")
            elif c["type"] in LIENS:
                liens += 1
            elif c["type"] in SIMPLES:
                auto += 1
            else:
                manuel += 1
                rapport["reprise_manuelle"].append(
                    f"{t['name']} → {c['name']} ({c['type']}) : "
                    f"{REPRISE_MANUELLE.get(c['type'], 'type non pris en charge')}")
        print(f"{t['name'][:34]:34} {len(t['fields']):>7} {auto:>6} {liens:>6} {manuel:>7} {rgpd:>5}")

    print("─" * 70)
    print(f"{len(tables)} tables · {sum(len(t['fields']) for t in tables)} champs")
    print(f"Reprise manuelle : {len(rapport['reprise_manuelle'])} champs")
    print(f"Exclus RGPD art. 9 : {len(rapport['exclu_rgpd'])} champs")

    if not args.executer:
        (RACINE / "rapport-migration.json").write_text(
            json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nMode --plan : rien n'a été écrit dans Baserow.")
        print(f"Rapport détaillé : {RACINE / 'rapport-migration.json'}")
        return

    # ── Écriture dans Baserow ──
    url = os.environ.get("BASEROW_API_URL", "https://api.baserow.io")
    email, mdp = os.environ.get("BASEROW_EMAIL"), os.environ.get("BASEROW_PASSWORD")
    ws = os.environ.get("BASEROW_WORKSPACE_ID")
    if not all([email, mdp, ws]):
        sys.exit("BASEROW_EMAIL, BASEROW_PASSWORD et BASEROW_WORKSPACE_ID sont requis pour --executer")

    br = Baserow(url, email, mdp)
    base = br.creer_base(int(ws), args.nom)
    print(f"\nBase Baserow créée : « {args.nom} » (id {base['id']})")

    corresp_tables, corresp_lignes = {}, {}

    # Passe 1 — tables, champs simples, lignes
    for t in tables:
        tb = br.creer_table(base["id"], t["name"])
        corresp_tables[t["name"]] = tb["id"]
        # Baserow crée Name/Notes/Active par défaut : on retire Notes et Active
        for c in br.champs(tb["id"]):
            if c["name"] in ("Notes", "Active"):
                br.supprimer_champ(c["id"])

        migrables = [c for c in t["fields"]
                     if not interdit(c["name"]) and c["type"] in SIMPLES]
        for c in migrables:
            d = definition_champ(c)
            if d:
                br.creer_champ(tb["id"], d)

        lignes_at = at.lignes(t["id"])
        paquet = []
        for rec in lignes_at:
            f = rec.get("fields", {})
            ligne = {}
            for c in migrables:
                v = valeur_pour(c, f.get(c["name"]))
                if v is not None:
                    ligne[c["name"][:255]] = v
            paquet.append(ligne)

        cree = []
        for i in range(0, len(paquet), 200):
            rep = br.creer_lignes(tb["id"], paquet[i:i + 200])
            cree += rep.get("items", [])
        corresp_lignes[t["name"]] = {
            rec["id"]: cree[i]["id"] for i, rec in enumerate(lignes_at) if i < len(cree)
        }
        print(f"  ✓ {t['name']:32} {len(migrables):>3} champs · {len(cree):>4} lignes")
        rapport["migre"].append({"table": t["name"], "champs": len(migrables), "lignes": len(cree)})

    # Passe 2 — liens entre tables, une fois toutes les tables créées
    print("\nLiens entre tables :")
    noms_at = {t["id"]: t["name"] for t in schema["tables"]}
    attendus = sum(1 for t in tables for c in t["fields"]
                   if c["type"] in LIENS and not interdit(c["name"]))
    faits = perdus = 0

    for t in tables:
        tid = corresp_tables[t["name"]]
        for c in t["fields"]:
            if c["type"] not in LIENS or interdit(c["name"]):
                continue
            cible_at = cible_liee(c)
            cible_nom = noms_at.get(cible_at)
            if not cible_at:
                # Silence interdit ici : une migration qui paraît réussie mais
                # perd ses relations est pire qu'une migration qui échoue.
                perdus += 1
                print(f"  ✗ {t['name']} → {c['name']} : table liée non indiquée par l'API")
                rapport["reprise_manuelle"].append(
                    f"{t['name']} → {c['name']} (lien) : l'API n'a pas indiqué la table "
                    "cible — lien à recréer à la main")
                continue
            if cible_nom not in corresp_tables:
                perdus += 1
                print(f"  ✗ {t['name']} → {c['name']} : table « {cible_nom} » hors périmètre")
                rapport["reprise_manuelle"].append(
                    f"{t['name']} → {c['name']} : table liée « {cible_nom} » hors périmètre")
                continue
            faits += 1
            br.creer_champ(tid, {"name": c["name"][:255], "type": "link_row",
                                 "link_row_table_id": corresp_tables[cible_nom]})
            # Remplissage des liaisons
            maj = []
            for rec in at.lignes(t["id"]):
                ids_at = rec.get("fields", {}).get(c["name"]) or []
                ids_br = [corresp_lignes[cible_nom][i] for i in ids_at
                          if i in corresp_lignes.get(cible_nom, {})]
                if ids_br and rec["id"] in corresp_lignes[t["name"]]:
                    maj.append({"id": corresp_lignes[t["name"]][rec["id"]],
                                c["name"][:255]: ids_br})
            for i in range(0, len(maj), 200):
                br.maj_lignes(tid, maj[i:i + 200])
            print(f"  ✓ {t['name']} → {c['name']} ({len(maj)} liaisons)")

    rapport["liens"] = {"attendus": attendus, "crees": faits, "perdus": perdus}
    (RACINE / "rapport-migration.json").write_text(
        json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nLiens : {faits}/{attendus} créés.")
    if perdus:
        print(f"\n{'═' * 66}")
        print(f"⚠ MIGRATION INCOMPLÈTE — {perdus} liaison(s) sur {attendus} non créée(s).")
        print("Les tables et les lignes sont en place, mais les relations")
        print("manquantes doivent être recréées à la main dans Baserow avant")
        print("toute suppression des données chez Airtable.")
        print(f"Détail : {RACINE / 'rapport-migration.json'}")
        print(f"{'═' * 66}")

    print(f"\nRapport : {RACINE / 'rapport-migration.json'}")
    print("\nÀ FAIRE ENSUITE, dans cet ordre :")
    print("  1. Vérifier les données dans Baserow, table par table.")
    print("  2. Recréer les formules et les lookups (voir le rapport).")
    print("  3. Reporter les pièces jointes.")
    print("  4. Mettre à jour le registre des traitements (art. 30).")
    print("  5. SEULEMENT ENSUITE : supprimer les données chez Airtable (art. 5.1.e).")
    if perdus:
        sys.exit(2)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Migration Airtable → Baserow")
    p.add_argument("--executer", action="store_true", help="écrit réellement dans Baserow")
    p.add_argument("--plan", action="store_true", help="inventaire seul (défaut)")
    p.add_argument("--tables", help="migrer seulement ces tables, séparées par des virgules")
    p.add_argument("--nom", default="YEBA FORMATIONS", help="nom de la base créée dans Baserow")
    migrer(p.parse_args())
