"""Migration « YEBA — Saison 1 · Accueil des invités » : Airtable (aujourd'hui) → Baserow (demain, cloud UE).

Source unique du schéma : accueil/schema_saison1.json (le même qui a servi à créer la base Airtable).

    python3 soiree-lancement/outils/migrer_vers_baserow.py                 # essai à blanc : affiche ce qui serait créé
    python3 soiree-lancement/outils/migrer_vers_baserow.py --creer         # crée la base, les tables, les liens et les contenus de départ
    python3 soiree-lancement/outils/migrer_vers_baserow.py --creer --copier-airtable   # … puis recopie les lignes d'Airtable

Identifiants lus dans .env (jamais dans le code) : BASEROW_API_URL, BASEROW_EMAIL, BASEROW_PASSWORD (compte de service
« Builder »), BASEROW_WORKSPACE_ID ; pour la copie : AIRTABLE_TOKEN (jeton personnel en lecture seule sur la base),
AIRTABLE_BASE_ID (app3Kv7p5WOhut5Un par défaut).

RGPD : la copie conserve la date d'inscription d'origine (preuve du consentement, art. 7-1) dans un champ
« … (origine Airtable) ». Une fois la copie vérifiée, supprimer la base Airtable (fin du transfert hors UE, chap. V)
et l'inscrire dans le registre des traitements (art. 30).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DEPOT = RACINE.parent
SCHEMA = json.loads((RACINE / "accueil" / "schema_saison1.json").read_text(encoding="utf-8"))
TYPES = {"texte", "texte_long", "email", "choix", "case", "nombre", "date", "lien", "date_creation"}


def charger_env():
    """Lit .env à la racine du dépôt sans dépendance externe (les valeurs déjà présentes dans l'environnement gagnent)."""
    chemin = DEPOT / ".env"
    if chemin.exists():
        for ligne in chemin.read_text(encoding="utf-8").splitlines():
            ligne = ligne.strip()
            if ligne and not ligne.startswith("#") and "=" in ligne:
                cle, val = ligne.split("=", 1)
                os.environ.setdefault(cle.strip(), val.strip().strip('"').strip("'"))


def champ_baserow(c, ids_tables=None):
    """Traduit un champ du schéma commun en spécification Baserow (nom, type, options)."""
    t = c["type"]
    spec = {"name": c["nom"]}
    if t == "texte":
        spec["type"] = "text"
    elif t == "texte_long":
        spec["type"] = "long_text"
    elif t == "email":
        spec["type"] = "email"
    elif t == "choix":
        spec.update(type="single_select", select_options=[{"value": v, "color": "light-gray"} for v in c["choix"]])
    elif t == "case":
        spec["type"] = "boolean"
    elif t == "nombre":
        spec.update(type="number", number_decimal_places=0)
    elif t == "date":
        spec.update(type="date", date_format="EU", date_include_time=False)
    elif t == "date_creation":
        spec.update(type="created_on", date_format="EU", date_include_time=True, date_time_format="24")
    elif t == "lien":
        spec.update(type="link_row", link_row_table_id=(ids_tables or {}).get(c["vers"], f"<id de {c['vers']}>"))
    if c.get("description"):
        spec["description"] = c["description"]
    return spec


def verifier_schema():
    noms = {T["nom"] for T in SCHEMA["tables"]}
    for T in SCHEMA["tables"]:
        assert T["champs"][0]["type"] in ("texte", "texte_long"), f"{T['nom']} : le champ primaire doit être un texte"
        for c in T["champs"]:
            assert c["type"] in TYPES, f"{T['nom']}.{c['nom']} : type inconnu {c['type']}"
            if c["type"] == "lien":
                assert c["vers"] in noms, f"{T['nom']}.{c['nom']} : table liée absente ({c['vers']})"
    for table, lignes in SCHEMA.get("donnees", {}).items():
        T = next(T for T in SCHEMA["tables"] if T["nom"] == table)
        champs = {c["nom"] for c in T["champs"]}
        for ligne in lignes:
            inconnus = set(ligne) - champs
            assert not inconnus, f"{table} : champs inconnus dans les données {inconnus}"


def essai():
    verifier_schema()
    print(f"Base Baserow à créer : « {SCHEMA['base']} »\n")
    for T in SCHEMA["tables"]:
        simples = [c for c in T["champs"] if c["type"] != "lien"]
        liens = [c for c in T["champs"] if c["type"] == "lien"]
        print(f"■ {T['nom']} — {len(simples)} champs, {len(liens)} lien(s)")
        for c in T["champs"]:
            s = champ_baserow(c)
            print(f"    {s['name']:<38} {s['type']}")
    n = sum(len(v) for v in SCHEMA.get("donnees", {}).values())
    print(f"\nContenus de départ : {n} lignes ({', '.join(f'{k} {len(v)}' for k, v in SCHEMA['donnees'].items())}).")
    print("Essai à blanc : rien n'a été envoyé. Relancer avec --creer une fois .env rempli.")


def creer(copier):
    sys.path.insert(0, str(DEPOT))
    from baserow import BaserowClient  # nécessite « requests » (pip install requests)

    charger_env()
    verifier_schema()
    espace = os.environ.get("BASEROW_WORKSPACE_ID")
    if not espace:
        sys.exit("BASEROW_WORKSPACE_ID manquant dans .env (python -m baserow.cli workspaces pour le trouver).")
    client = BaserowClient()
    base = client.create_database(int(espace), SCHEMA["base"])
    print(f"Base créée : {base['name']} (id {base['id']})")

    # 1re passe : tables et champs simples (les liens viennent ensuite, une fois toutes les tables créées)
    ids_tables, champs_crees = {}, {}
    for T in SCHEMA["tables"]:
        specs = [champ_baserow(c) for c in T["champs"] if c["type"] != "lien"]
        if copier:   # date d'inscription d'origine conservée (preuve du consentement)
            specs += [{"name": f"{c['nom']} (origine Airtable)", "type": "date", "date_format": "EU",
                       "date_include_time": True, "date_time_format": "24"}
                      for c in T["champs"] if c["type"] == "date_creation"]
        res = client.create_table_with_schema(base["id"], T["nom"], specs)
        ids_tables[T["nom"]] = res["table"]["id"]
        champs_crees[T["nom"]] = {f["name"]: f for f in client.list_fields(res["table"]["id"])}
        print(f"  table {T['nom']} (id {res['table']['id']})")

    # 2e passe : liens entre tables (Baserow crée le champ inverse dans la table liée)
    deja = set()
    for T in SCHEMA["tables"]:
        for c in T["champs"]:
            if c["type"] != "lien":
                continue
            cle = frozenset((T["nom"], c["vers"], c["nom"]))
            if cle in deja:
                continue
            deja.add(cle)
            spec = champ_baserow(c, ids_tables)
            client.create_field(ids_tables[T["nom"]], spec.pop("name"), spec.pop("type"), **spec)
            print(f"  lien {T['nom']}.{c['nom']} → {c['vers']}")
    for nom, tid in ids_tables.items():
        champs_crees[nom] = {f["name"]: f for f in client.list_fields(tid)}

    def options(table, champ, valeur):
        """Valeur d'un choix → identifiant d'option Baserow."""
        f = champs_crees[table].get(champ)
        if f and f.get("type") == "single_select" and isinstance(valeur, str):
            for o in f.get("select_options", []):
                if o["value"] == valeur:
                    return o["id"]
            return None
        return valeur

    # Contenus de départ (épisodes, accroches, stands, paramètres) : seulement si on ne recopie pas Airtable
    if not copier:
        for table, lignes in SCHEMA.get("donnees", {}).items():
            items = [{k: options(table, k, v) for k, v in ligne.items()} for ligne in lignes]
            client.create_rows(ids_tables[table], items)
            print(f"  {len(items)} lignes dans {table}")
        print("Terminé.")
        return

    # Copie depuis Airtable : 1) lignes sans liens, 2) liens recâblés avec la correspondance des identifiants
    import requests

    jeton = os.environ.get("AIRTABLE_TOKEN")
    if not jeton:
        sys.exit("AIRTABLE_TOKEN manquant dans .env (jeton personnel Airtable, lecture seule sur la base).")
    base_at = os.environ.get("AIRTABLE_BASE_ID", "app3Kv7p5WOhut5Un")

    def lire_airtable(table):
        lignes, offset = [], None
        while True:
            params = {"pageSize": 100, **({"offset": offset} if offset else {})}
            r = requests.get(f"https://api.airtable.com/v0/{base_at}/{requests.utils.quote(table)}",
                             headers={"Authorization": f"Bearer {jeton}"}, params=params, timeout=30)
            r.raise_for_status()
            data = r.json()
            lignes += data["records"]
            offset = data.get("offset")
            if not offset:
                return lignes

    correspondance, a_relier = {}, []
    for T in SCHEMA["tables"]:
        simples = {c["nom"]: c for c in T["champs"] if c["type"] not in ("lien", "date_creation")}
        liens = [c["nom"] for c in T["champs"] if c["type"] == "lien"]
        creations = [c["nom"] for c in T["champs"] if c["type"] == "date_creation"]
        enregistrements = lire_airtable(T["nom"])
        for rec in enregistrements:
            valeurs = {k: options(T["nom"], k, v) for k, v in rec["fields"].items() if k in simples}
            for nom in creations:
                valeurs[f"{nom} (origine Airtable)"] = rec["createdTime"]
            ligne = client.create_row(ids_tables[T["nom"]], valeurs)
            correspondance[rec["id"]] = ligne["id"]
            a_relier.append((T["nom"], ligne["id"], {k: rec["fields"].get(k, []) for k in liens}))
        print(f"  {len(enregistrements)} lignes copiées dans {T['nom']}")
    for table, ligne_id, liens in a_relier:
        valeurs = {k: [correspondance[i] for i in v if i in correspondance] for k, v in liens.items() if v}
        if valeurs:
            client.update_row(ids_tables[table], ligne_id, valeurs)
    print("Copie terminée. Vérifier les comptes de lignes, puis supprimer la base Airtable (RGPD chap. V).")


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--creer", action="store_true", help="crée réellement la base dans Baserow")
    p.add_argument("--copier-airtable", action="store_true", help="recopie les lignes de la base Airtable")
    a = p.parse_args()
    if a.creer:
        creer(a.copier_airtable)
    else:
        essai()


if __name__ == "__main__":
    main()
