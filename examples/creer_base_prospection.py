#!/usr/bin/env python3
"""Crée la base « YEBA – Prospection & Assistant vocal » dans Baserow.

Sept tables, noms de champs alignés sur le workflow n8n
(assistant-vocal/workflow_n8n_assistant_yeba.json) et sur le script
prospection/extraire_entreprises_974.py :

  Formations             catalogue lu par l'assistant vocal
  Inscriptions           demandes d'inscription prises au téléphone
  Demandes sous-traitance  missions proposées par d'autres OF (validation obligatoire)
  Journal des appels     trace minimale de chaque appel
  Prospects Article 4    entreprises 974 issues de l'API Recherche d'entreprises
  Donneurs d'ordre       OF / structures susceptibles de sous-traiter un formateur
  Marchés publics        veille appels d'offres Réunion + océan Indien

RGPD : seules les données strictement utiles sont prévues (pas de date de
naissance, pas de donnée de santé). Le champ « Besoin d'adaptation » ne doit
contenir que ce que la personne choisit de dire (référent handicap), jamais
de diagnostic.

Usage :  python examples/creer_base_prospection.py --workspace <ID>
"""

from __future__ import annotations

import argparse
import json

from dotenv import load_dotenv

from baserow import BaserowClient


def _opts(*values: str) -> list:
    return [{"value": v} for v in values]


SCHEMAS = {
    "Formations": [
        {"name": "Intitulé", "type": "text"},
        {"name": "Domaine", "type": "single_select",
         "select_options": _opts("IA", "RGPD / IA Act", "Vente", "Management", "Soft skills")},
        {"name": "Durée (heures)", "type": "number", "number_decimal_places": 0},
        {"name": "Modalité", "type": "single_select",
         "select_options": _opts("Inter", "Intra", "Distanciel", "Mixte")},
        {"name": "Prochaine session", "type": "date"},
        {"name": "Lieu", "type": "text"},
        {"name": "Prix HT (€)", "type": "number", "number_decimal_places": 0},
        {"name": "Objectifs", "type": "long_text"},
        {"name": "Public et prérequis", "type": "long_text"},
        {"name": "Financements possibles", "type": "long_text"},
        {"name": "Publié", "type": "boolean"},
    ],
    "Inscriptions": [
        {"name": "Nom", "type": "text"},
        {"name": "Entreprise", "type": "text"},
        {"name": "Téléphone", "type": "phone_number"},
        {"name": "Email", "type": "email"},
        {"name": "Formation souhaitée", "type": "text"},
        {"name": "Nombre de participants", "type": "number", "number_decimal_places": 0},
        {"name": "Financement envisagé", "type": "single_select",
         "select_options": _opts("OPCO", "CPF", "Entreprise", "France Travail", "Ne sait pas")},
        {"name": "Besoin d'adaptation", "type": "long_text"},
        {"name": "Statut", "type": "single_select",
         "select_options": _opts("À confirmer", "Confirmée", "Annulée")},
        {"name": "Origine", "type": "single_select",
         "select_options": _opts("Assistant vocal", "Site web", "Email", "Salon")},
        {"name": "Date de la demande", "type": "date", "date_include_time": True},
    ],
    "Demandes sous-traitance": [
        {"name": "Organisme donneur d'ordre", "type": "text"},
        {"name": "Interlocuteur", "type": "text"},
        {"name": "Téléphone", "type": "phone_number"},
        {"name": "Email", "type": "email"},
        {"name": "Thème", "type": "text"},
        {"name": "Dates proposées", "type": "long_text"},
        {"name": "Date début", "type": "date", "date_include_time": True},
        {"name": "Date fin", "type": "date", "date_include_time": True},
        {"name": "Lieu", "type": "text"},
        {"name": "Nombre de stagiaires", "type": "number", "number_decimal_places": 0},
        {"name": "Programme reçu", "type": "boolean"},
        {"name": "Objectifs reçus", "type": "boolean"},
        {"name": "Tarif proposé", "type": "text"},
        {"name": "Statut", "type": "single_select",
         "select_options": _opts("En attente de validation", "Acceptée", "Refusée")},
        {"name": "Jeton de validation", "type": "text"},
        {"name": "Date de la demande", "type": "date", "date_include_time": True},
    ],
    "Journal des appels": [
        {"name": "Identifiant appel", "type": "text"},
        {"name": "Date", "type": "date", "date_include_time": True},
        {"name": "Motif", "type": "single_select",
         "select_options": _opts("Infos formation", "Inscription", "Sous-traitance",
                                 "CGV / mentions légales", "Transfert", "Autre")},
        {"name": "Résumé", "type": "long_text"},
        {"name": "Transféré à Aurélien", "type": "boolean"},
        {"name": "Durée (secondes)", "type": "number", "number_decimal_places": 0},
    ],
    "Prospects Article 4": [
        {"name": "Entreprise", "type": "text"},
        {"name": "SIREN", "type": "text"},
        {"name": "SIRET siège", "type": "text"},
        {"name": "Code NAF", "type": "text"},
        {"name": "Tranche effectif", "type": "text"},
        {"name": "Catégorie", "type": "text"},
        {"name": "Adresse", "type": "text"},
        {"name": "Code postal", "type": "text"},
        {"name": "Commune", "type": "text"},
        {"name": "Dirigeant (personne morale ou fonction)", "type": "text"},
        {"name": "Date de création", "type": "text"},
        {"name": "Site web", "type": "url"},
        {"name": "Email générique", "type": "email"},
        {"name": "Téléphone standard", "type": "phone_number"},
        {"name": "OPCO probable", "type": "text"},
        {"name": "Statut", "type": "single_select",
         "select_options": _opts("À qualifier", "À contacter", "Contacté", "RDV",
                                 "Proposition", "Client", "Opposition RGPD", "Perdu")},
        {"name": "Source de la donnée", "type": "text"},
        {"name": "Date d'information art. 14", "type": "date"},
    ],
    "Donneurs d'ordre": [
        {"name": "Organisme", "type": "text"},
        {"name": "Type", "type": "single_select",
         "select_options": _opts("OF 974", "OF métropole vendant en 974", "CFA",
                                 "Consulaire / public", "Plateforme", "Océan Indien")},
        {"name": "SIREN ou NDA", "type": "text"},
        {"name": "Thèmes", "type": "long_text"},
        {"name": "Qualiopi", "type": "boolean"},
        {"name": "Contact public", "type": "text"},
        {"name": "Site web", "type": "url"},
        {"name": "Statut", "type": "single_select",
         "select_options": _opts("À contacter", "Candidature envoyée", "En discussion",
                                 "Référencé", "Mission obtenue", "Sans suite")},
        {"name": "Source", "type": "text"},
        {"name": "Prochaine action", "type": "date"},
    ],
    "Marchés publics": [
        {"name": "Objet", "type": "text"},
        {"name": "Acheteur", "type": "text"},
        {"name": "Territoire", "type": "single_select",
         "select_options": _opts("Réunion", "Mayotte", "Maurice", "Madagascar",
                                 "Seychelles", "Comores", "National")},
        {"name": "Référence", "type": "text"},
        {"name": "Date limite", "type": "date", "date_include_time": True},
        {"name": "Montant estimé", "type": "text"},
        {"name": "Lien", "type": "url"},
        {"name": "Décision", "type": "single_select",
         "select_options": _opts("À analyser", "Répondre seul", "Répondre en groupement",
                                 "Sous-traitance d'un titulaire", "Pas pour nous")},
        {"name": "Notes", "type": "long_text"},
    ],
}


def main() -> None:
    load_dotenv()
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", type=int, required=True, help="ID du workspace Baserow")
    ap.add_argument("--nom", default="YEBA – Prospection & Assistant vocal")
    args = ap.parse_args()

    client = BaserowClient()
    base = client.create_database(args.workspace, args.nom)
    print(f"Base créée : {base['name']} (id={base['id']})")

    ids = {}
    for table_name, schema in SCHEMAS.items():
        result = client.create_table_with_schema(base["id"], table_name, schema)
        ids[table_name] = result["table"]["id"]
        print(f"  - {table_name} (id={ids[table_name]}, {len(result['fields'])} champs)")

    print("\nIDs à reporter dans le nœud « Config » du workflow n8n :")
    print(json.dumps(ids, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
