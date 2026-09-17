#!/usr/bin/env python3
"""
Exporte les tables Airtable en CSV, prêts à être importés dans Baserow.

    python migration/export_csv.py                      # les 19 tables
    python migration/export_csv.py --tables "CATALOGUE FORMATIONS"
    python migration/export_csv.py --sans-donnees-perso # exclut les tables de personnes

Pourquoi cette voie
L'import Airtable natif de Baserow réclame les cookies « __Host-airtable-session ».
Ce ne sont pas des identifiants d'API : c'est une SESSION COMPLÈTE. Qui les
détient est vous — toutes vos bases, sans mot de passe ni double authentification,
et sans pouvoir révoquer ce seul accès. Les copier dans un formulaire tiers est
exactement ce qu'un organisme qui forme à la cybersécurité doit refuser.

L'import CSV de Baserow, lui, ne demande rien : vous déposez un fichier.
Le jeton Airtable utilisé ici est en lecture seule et révocable en un clic.

Ce que l'export CSV conserve, et ce qu'il perd
  CONSERVÉ   texte, nombres, montants, dates, cases, sélecteurs, e-mails,
             téléphones, URL — soit l'essentiel des données.
  PERDU      les LIENS entre tables deviennent du texte, les pièces jointes
             ne sont pas transférées, les formules sont figées en valeurs.

C'est la limite de tout import par fichier, pas de ce script. Pour conserver les
relations, il faut la voie API : migration/airtable_vers_baserow.py, qui recrée
les liens en deux passes — elle demande vos identifiants Baserow.

RGPD
Les fichiers produits contiennent des données personnelles de stagiaires. Ils
sont écrits dans migration/export/, dossier ignoré par Git. Ne les committez
jamais, ne les envoyez pas par messagerie non chiffrée, et supprimez-les une
fois l'import vérifié (art. 5.1.e — limitation de la conservation).
Les champs « NE PAS REMPLIR » (art. 9 — données de santé) ne sont jamais
exportés.
"""

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parent
SORTIE = RACINE / "export"
BASE = "appQ2zqc80kkc6MR1"

# Tables contenant des données personnelles de personnes physiques.
# --sans-donnees-perso permet de commencer par le reste, ce qui est la bonne
# façon d'éprouver un import avant d'y verser des données de stagiaires.
TABLES_PERSONNES = {
    "APPRENANTS", "FORMATEURS & PRESTATAIRES", "ENTREPRISES & CLIENTS",
    "INSCRIPTIONS", "PRESENCES & EMARGEMENTS", "EVALUATIONS",
    "STAGES & ALTERNANCES", "MAILING LOG",
}

# Types qu'un CSV ne peut pas porter fidèlement. Exportés en texte lisible,
# avec un avertissement récapitulatif : mieux vaut une perte annoncée qu'une
# colonne silencieusement inexploitable.
TYPES_DEGRADES = {
    "multipleRecordLinks": "lien entre tables → texte",
    "multipleAttachments": "pièce jointe → non transférée",
    "formula": "formule → valeur figée",
    "multipleLookupValues": "valeur liée → texte",
    "rollup": "agrégat → valeur figée",
}


def _appel(url, entetes):
    req = urllib.request.Request(url, headers=entetes)
    for essai in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 429 and essai < 3:
                time.sleep(2 ** essai)
                continue
            sys.exit(f"Airtable a répondu {e.code} : "
                     f"{e.read().decode('utf-8', 'replace')[:300]}")
        except urllib.error.URLError as e:
            if essai < 3:
                time.sleep(2 ** essai)
                continue
            sys.exit(f"Réseau injoignable : {e}")


def aplatir(v):
    """Rend une valeur Airtable lisible dans une cellule de tableur."""
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, dict):
        return v.get("name") or v.get("url") or v.get("text") or ""
    if isinstance(v, list):
        return ", ".join(str(aplatir(x)) for x in v if aplatir(x) != "")
    return v


def main():
    p = argparse.ArgumentParser(description="Airtable → CSV pour Baserow")
    p.add_argument("--tables", help="noms séparés par des virgules")
    p.add_argument("--sans-donnees-perso", action="store_true",
                   help="exclut les tables contenant des données de personnes")
    args = p.parse_args()

    try:
        from dotenv import load_dotenv
        load_dotenv(RACINE.parent / ".env")
    except ImportError:
        pass

    jeton = os.environ.get("AIRTABLE_TOKEN")
    if not jeton:
        sys.exit("AIRTABLE_TOKEN absent. Créez un jeton en LECTURE SEULE sur "
                 "https://airtable.com/create/tokens, puis mettez-le dans .env")
    entetes = {"Authorization": f"Bearer {jeton}"}

    schema = _appel(f"https://api.airtable.com/v0/meta/bases/{BASE}/tables", entetes)
    tables = schema["tables"]

    if args.tables:
        voulues = {t.strip() for t in args.tables.split(",")}
        tables = [t for t in tables if t["name"] in voulues]
    if args.sans_donnees_perso:
        tables = [t for t in tables if t["name"] not in TABLES_PERSONNES]
    if not tables:
        sys.exit("Aucune table à exporter.")

    SORTIE.mkdir(parents=True, exist_ok=True)
    degradations, total_lignes = {}, 0

    for t in tables:
        colonnes = [c for c in t["fields"] if "NE PAS REMPLIR" not in c["name"]]
        exclus = len(t["fields"]) - len(colonnes)

        for c in colonnes:
            if c["type"] in TYPES_DEGRADES:
                degradations.setdefault(TYPES_DEGRADES[c["type"]], 0)
                degradations[TYPES_DEGRADES[c["type"]]] += 1

        lignes, params = [], {"pageSize": 100}
        while True:
            url = (f"https://api.airtable.com/v0/{BASE}/{t['id']}?"
                   + urllib.parse.urlencode(params))
            rep = _appel(url, entetes)
            lignes += rep.get("records", [])
            if not rep.get("offset"):
                break
            params["offset"] = rep["offset"]

        # Nom de fichier sûr : Baserow reprend le nom du fichier comme nom de table.
        nom = "".join(ch if ch.isalnum() or ch in " -_&" else "_" for ch in t["name"])
        chemin = SORTIE / f"{nom}.csv"
        with chemin.open("w", encoding="utf-8-sig", newline="") as f:
            # utf-8-sig : sans cette marque, Excel ouvre les accents en mojibake.
            w = csv.writer(f, quoting=csv.QUOTE_ALL)
            w.writerow([c["name"] for c in colonnes])
            for rec in lignes:
                champs = rec.get("fields", {})
                w.writerow([aplatir(champs.get(c["name"])) for c in colonnes])

        total_lignes += len(lignes)
        marque = f"  ({exclus} champ(s) art. 9 exclu(s))" if exclus else ""
        print(f"  ✓ {t['name'][:34]:34} {len(colonnes):>3} col · {len(lignes):>4} lignes{marque}")

    print(f"\n{len(tables)} fichiers écrits dans {SORTIE}")
    print(f"{total_lignes} lignes au total.")

    if degradations:
        print("\nCe qu'un CSV ne peut pas porter :")
        for quoi, combien in sorted(degradations.items(), key=lambda x: -x[1]):
            print(f"  {combien:>3} colonnes — {quoi}")
        print("\nPour conserver les liens entre tables, utilisez la voie API :")
        print("  python migration/airtable_vers_baserow.py --plan")

    print("\nIMPORT DANS BASEROW")
    print("  1. Base de données → Ajouter une table → Importer un fichier → CSV")
    print("  2. Déposer le fichier. Cocher « Première ligne = en-têtes ».")
    print("  3. Répéter pour chaque fichier.")
    print("  Aucun cookie n'est demandé par cette voie.")

    print("\nRGPD — après vérification de l'import :")
    print(f"  rm -rf {SORTIE}")
    print("  Ces fichiers contiennent des données personnelles (art. 5.1.e).")


if __name__ == "__main__":
    main()
