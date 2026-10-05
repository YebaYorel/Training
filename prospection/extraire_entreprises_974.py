#!/usr/bin/env python3
"""Extraction des entreprises actives de La Réunion (974) depuis l'API publique
« Recherche d'entreprises » (DINUM / annuaire-entreprises.data.gouv.fr).

Gratuite, sans clé, données SIRENE (INSEE) + RNE (INPI). Hébergement État
français. Limite d'usage indicative : 7 requêtes/seconde, 25 résultats/page.

Deux modes :
  entreprises  → cibles « Article 4 IA Act » (TPE-PME, par code NAF / effectif)
  organismes   → organismes de formation du 974 (donneurs d'ordre en sous-traitance)

Exemples :
  python prospection/extraire_entreprises_974.py entreprises \
      --naf 46.65Z 46.69B 69.20Z 68.31Z --effectifs 03 11 12 21 -o prospects_974.csv
  python prospection/extraire_entreprises_974.py entreprises --section M N \
      --effectifs 11 12 21 22 -o services_974.csv
  python prospection/extraire_entreprises_974.py organismes -o of_974.csv
  # + envoi direct dans Baserow (table « Prospects Article 4 » ou « Donneurs d'ordre »)
  python prospection/extraire_entreprises_974.py entreprises --naf 46.65Z \
      --baserow-table 123

Tranches d'effectif INSEE : 00=0 · 01=1-2 · 02=3-5 · 03=6-9 · 11=10-19 ·
12=20-49 · 21=50-99 · 22=100-199 · 31=200-249 · 32=250-499.

RGPD (à lire) :
  - Les données d'entreprise (raison sociale, SIREN, adresse du siège) ne sont
    pas des données personnelles. En revanche le NOM D'UN DIRIGEANT PERSONNE
    PHYSIQUE et un entrepreneur individuel (EI) le sont.
  - Par défaut, le script ne conserve que la FONCTION du dirigeant personne
    physique (ex. « Gérant »), pas son nom (minimisation, art. 5.1.c).
    --avec-noms-dirigeants les conserve : vous devrez alors informer chaque
    personne au plus tard au premier contact (art. 14 RGPD : source = API
    Recherche d'entreprises / SIRENE-RNE) et respecter son opposition (art. 21).
  - Les entrepreneurs individuels sont exclus par défaut (leur dénomination
    est leur nom). --inclure-ei pour les garder.
  - Respectez les diffusions restreintes SIRENE : l'API les masque déjà ;
    ne cherchez pas à les reconstituer.
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from typing import Any, Dict, Iterator, List

import requests

API = "https://recherche-entreprises.api.gouv.fr/search"
PER_PAGE = 25
PAUSE = 0.2  # ≈ 5 requêtes/s, sous la limite de 7/s
SOURCE = "API Recherche d'entreprises (SIRENE/RNE) – recherche-entreprises.api.gouv.fr"

COLONNES = [
    "Entreprise", "SIREN", "SIRET siège", "Code NAF", "Tranche effectif",
    "Catégorie", "Adresse", "Code postal", "Commune",
    "Dirigeant (personne morale ou fonction)", "Date de création",
    "Qualiopi", "Source de la donnée",
]


def _pages(params: Dict[str, Any], max_pages: int) -> Iterator[Dict[str, Any]]:
    session = requests.Session()
    page = 1
    while page <= max_pages:
        q = dict(params, page=page, per_page=PER_PAGE)
        for attempt in range(4):
            r = session.get(API, params=q, timeout=30)
            if r.status_code == 429:
                time.sleep(2 ** attempt)
                continue
            r.raise_for_status()
            break
        else:
            raise RuntimeError("API saturée (429) – réessayez plus tard")
        data = r.json()
        for item in data.get("results", []):
            yield item
        if page >= data.get("total_pages", 0):
            return
        page += 1
        time.sleep(PAUSE)


def _dirigeant(item: Dict[str, Any], avec_noms: bool) -> str:
    for d in item.get("dirigeants") or []:
        qualite = d.get("qualite") or ""
        if d.get("type_dirigeant") == "personne morale":
            return f"{d.get('denomination', '')} ({qualite})".strip()
        if avec_noms:
            nom = f"{d.get('prenoms', '')} {d.get('nom', '')}".strip()
            return f"{nom} ({qualite})".strip()
        return qualite
    return ""


def _ligne(item: Dict[str, Any], avec_noms: bool) -> Dict[str, Any]:
    siege = item.get("siege") or {}
    complements = item.get("complements") or {}
    return {
        "Entreprise": item.get("nom_raison_sociale") or item.get("nom_complet", ""),
        "SIREN": item.get("siren", ""),
        "SIRET siège": siege.get("siret", ""),
        "Code NAF": item.get("activite_principale", ""),
        "Tranche effectif": item.get("tranche_effectif_salarie") or "",
        "Catégorie": item.get("categorie_entreprise") or "",
        "Adresse": siege.get("adresse", ""),
        "Code postal": siege.get("code_postal", ""),
        "Commune": siege.get("libelle_commune", ""),
        "Dirigeant (personne morale ou fonction)": _dirigeant(item, avec_noms),
        "Date de création": item.get("date_creation", ""),
        "Qualiopi": "oui" if complements.get("est_qualiopi") else "",
        "Source de la donnée": SOURCE,
    }


def _est_ei(item: Dict[str, Any]) -> bool:
    nature = str(item.get("nature_juridique") or "")
    return nature.startswith("1")  # 1000 = entrepreneur individuel


def collecter(args: argparse.Namespace) -> List[Dict[str, Any]]:
    base = {"departement": "974", "etat_administratif": "A"}
    if args.effectifs:
        base["tranche_effectif_salarie"] = ",".join(args.effectifs)

    requetes: List[Dict[str, Any]] = []
    if args.mode == "organismes":
        requetes.append(dict(base, est_organisme_formation="true"))
    elif args.naf:
        requetes += [dict(base, activite_principale=n) for n in args.naf]
    elif args.section:
        requetes += [dict(base, section_activite_principale=s) for s in args.section]
    else:
        sys.exit("Précisez --naf ou --section (le 974 compte des dizaines de milliers d'unités).")

    vus, lignes = set(), []
    for params in requetes:
        n = 0
        for item in _pages(params, args.max_pages):
            if item.get("siren") in vus:
                continue
            if _est_ei(item) and not args.inclure_ei:
                continue
            vus.add(item.get("siren"))
            lignes.append(_ligne(item, args.avec_noms_dirigeants))
            n += 1
        print(f"{params}: {n} entreprises", file=sys.stderr)
    return lignes


def vers_baserow(lignes: List[Dict[str, Any]], table_id: int) -> None:
    from dotenv import load_dotenv
    from baserow import BaserowClient

    load_dotenv()
    client = BaserowClient()
    champs = {f["name"] for f in client.list_fields(table_id)}
    rows = [{k: v for k, v in l.items() if k in champs and v != ""} for l in lignes]
    for i in range(0, len(rows), 200):  # 200 = maximum de l'endpoint batch
        client.create_rows(table_id, rows[i:i + 200])
    print(f"{len(rows)} lignes envoyées dans la table Baserow {table_id}", file=sys.stderr)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["entreprises", "organismes"])
    ap.add_argument("--naf", nargs="*", help="Codes NAF, ex. 46.65Z 69.20Z")
    ap.add_argument("--section", nargs="*", help="Sections NAF, ex. G M N")
    ap.add_argument("--effectifs", nargs="*", help="Tranches INSEE, ex. 03 11 12 21")
    ap.add_argument("--max-pages", type=int, default=40, help="40 pages × 25 = 1000 par requête")
    ap.add_argument("--avec-noms-dirigeants", action="store_true")
    ap.add_argument("--inclure-ei", action="store_true")
    ap.add_argument("-o", "--output", default="extraction_974.csv")
    ap.add_argument("--baserow-table", type=int)
    args = ap.parse_args()

    lignes = collecter(args)
    with open(args.output, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=COLONNES, delimiter=";")
        w.writeheader()
        w.writerows(lignes)
    print(f"{len(lignes)} lignes → {args.output}", file=sys.stderr)

    if args.baserow_table:
        vers_baserow(lignes, args.baserow_table)


if __name__ == "__main__":
    main()
