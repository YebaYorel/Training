#!/usr/bin/env python3
"""Fiche entreprise gratuite pour la prospection YEBA (remplace Pappers).

Source : API officielle « Recherche d'entreprises » (DINUM / annuaire-entreprises
.data.gouv.fr), gratuite, sans clé, données INSEE Sirene + RNE, hébergée en France.
Doc : https://recherche-entreprises.api.gouv.fr/docs/

Usage :
    python scripts/fiche_entreprise.py "Nom de l'entreprise" [--dep 974] [--json]

RGPD : on ne lit que des données PUBLIQUES de personnes morales. Le nom du
dirigeant est une donnée personnelle publique (RNE) : il sert seulement à
personnaliser la salutation, jamais à constituer un fichier de personnes.
Si l'entreprise a fait opposition à la prospection (`opposition_diffusion_
commerciale`), le script le signale : NE PAS la prospecter.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request

API = "https://recherche-entreprises.api.gouv.fr/search"

# Tranches d'effectif INSEE (code -> libellé)
TRANCHES = {
    "NN": "non employeur", "00": "0 salarié", "01": "1 ou 2", "02": "3 à 5",
    "03": "6 à 9", "11": "10 à 19", "12": "20 à 49", "21": "50 à 99",
    "22": "100 à 199", "31": "200 à 249", "32": "250 à 499", "41": "500 à 999",
    "42": "1 000 à 1 999", "51": "2 000 à 4 999", "52": "5 000 à 9 999",
    "53": "10 000 et plus",
}

# OPCO probable selon la section NAF (indicatif : l'OPCO réel dépend de la
# convention collective, à confirmer avec le client).
OPCO_PAR_SECTION = {
    "A": "OCAPIAT", "C": "OPCO 2i / OCAPIAT (agroalimentaire)", "F": "Constructys",
    "G": "OPCOMMERCE (commerce) / OPCO Mobilités (auto)", "H": "OPCO Mobilités",
    "I": "AKTO (hôtellerie-restauration)", "J": "Atlas", "K": "Atlas", "L": "AKTO / Atlas",
    "M": "Atlas / OPCO EP", "N": "AKTO (propreté, sécurité) / OPCO EP",
    "P": "Uniformation / Akto", "Q": "OPCO Santé / Uniformation", "S": "OPCO EP / AKTO",
}


def chercher(nom: str, departement: str | None) -> list[dict]:
    params = {"q": nom, "per_page": 5, "etat_administratif": "A"}
    if departement:
        params["departement"] = departement
    url = f"{API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "fiche-entreprise/1.0"})
    for essai in range(3):  # l'API limite à ~7 requêtes/s ; coupures réseau possibles
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.load(r).get("results", [])
        except OSError:
            if essai == 2:
                raise
            time.sleep(2 * (essai + 1))
    return []


def fiche(r: dict) -> dict:
    s = r.get("siege") or {}
    dirigeants = []
    for d in r.get("dirigeants") or []:
        nom = " ".join(x for x in (d.get("prenoms"), d.get("nom")) if x) or d.get("denomination")
        if nom and "commissaire" not in (d.get("qualite") or "").lower():
            dirigeants.append(f"{nom} ({d.get('qualite') or 'dirigeant'})")
    section = r.get("section_activite_principale") or ""
    return {
        "nom": r.get("nom_complet"),
        "siren": r.get("siren"),
        "siret_siege": s.get("siret"),
        "naf": r.get("activite_principale"),
        "section_naf": section,
        "effectif": TRANCHES.get(r.get("tranche_effectif_salarie") or "", "non renseigné"),
        "categorie": r.get("categorie_entreprise"),
        "adresse": s.get("adresse"),
        "date_creation": r.get("date_creation"),
        "dirigeants": dirigeants,
        "opco_probable": OPCO_PAR_SECTION.get(section, "à confirmer (convention collective)"),
        "opposition_prospection": bool(r.get("opposition_diffusion_commerciale")),
        "diffusion_restreinte": r.get("statut_diffusion") not in (None, "O"),
        "etablissements_ouverts": r.get("nombre_etablissements_ouverts"),
        "source": f"annuaire-entreprises.data.gouv.fr/entreprise/{r.get('siren')}",
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("nom")
    p.add_argument("--dep", default="974", help="département (974 par défaut ; '' = toute la France)")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    res = [fiche(r) for r in chercher(a.nom, a.dep or None)]
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0 if res else 1
    if not res:
        print("Aucune entreprise active trouvée. Essayer sans --dep ou avec le SIREN.")
        return 1
    for f in res:
        alerte = "  ⚠ OPPOSITION À LA PROSPECTION : NE PAS CONTACTER" if f["opposition_prospection"] else ""
        print(f"{f['nom']} — SIREN {f['siren']} — NAF {f['naf']} — {f['effectif']}{alerte}")
        print(f"   {f['adresse']} | dirigeant(s) : {', '.join(f['dirigeants']) or 'non diffusé'}")
        print(f"   OPCO probable : {f['opco_probable']} | source : {f['source']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
