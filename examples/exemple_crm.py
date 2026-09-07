#!/usr/bin/env python3
"""Exemple concret : construit un mini-CRM prospection pour YEBA FORMATIONS.

Montre comment Claude Code (ou vous) enchaîne les appels : base -> table +
schéma -> lignes. Adapté au contexte réunionnais (TPE-PME).

Usage :  python examples/exemple_crm.py --workspace <ID>
"""

from __future__ import annotations

import argparse

from dotenv import load_dotenv

from baserow import BaserowClient


def main() -> None:
    load_dotenv()
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", type=int, required=True, help="ID du workspace Baserow")
    args = ap.parse_args()

    client = BaserowClient()

    # 1) Base
    base = client.create_database(args.workspace, "CRM Prospection")
    print(f"Base créée : {base['name']} (id={base['id']})")

    # 2) Table + schéma complet
    schema = [
        {"name": "Entreprise", "type": "text"},
        {"name": "Secteur", "type": "single_select",
         "select_options": [{"value": "Tourisme"}, {"value": "BTP"},
                            {"value": "Commerce"}, {"value": "Services"}]},
        {"name": "Contact", "type": "text"},
        {"name": "Email", "type": "email"},
        {"name": "Téléphone", "type": "phone_number"},
        {"name": "Statut", "type": "single_select",
         "select_options": [{"value": "À contacter"}, {"value": "En discussion"},
                            {"value": "Proposition"}, {"value": "Client"},
                            {"value": "Perdu"}]},
        {"name": "Besoin IA/RGPD", "type": "long_text"},
        {"name": "Budget estimé (€)", "type": "number", "number_decimal_places": 0},
    ]
    result = client.create_table_with_schema(base["id"], "Prospects", schema)
    table_id = result["table"]["id"]
    print(f"Table créée : Prospects (id={table_id}) avec {len(result['fields'])} champs")

    # 3) Quelques lignes d'exemple
    client.create_rows(table_id, [
        {"Entreprise": "Hôtel Lagon", "Secteur": "Tourisme", "Contact": "M. Payet",
         "Email": "contact@exemple.re", "Statut": "À contacter",
         "Besoin IA/RGPD": "Automatiser les réponses aux avis clients",
         "Budget estimé (€)": 4000},
        {"Entreprise": "BTP Océan Indien", "Secteur": "BTP", "Contact": "Mme Hoarau",
         "Statut": "En discussion",
         "Besoin IA/RGPD": "Audit RGPD + workflow devis", "Budget estimé (€)": 6000},
    ])
    print("2 prospects insérés. CRM prêt.")


if __name__ == "__main__":
    main()
