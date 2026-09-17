#!/usr/bin/env python3
"""
Génère data/formations.json depuis Airtable pour le site public YEBA FORMATIONS.

    python site/build.py            # régénère le catalogue
    python site/build.py --check    # vérifie sans écrire

Principe : le site est STATIQUE. Aucune clé d'API ne part chez le visiteur,
aucun appel réseau n'est fait depuis son navigateur. Seul ce script parle à
Airtable, sur votre poste, au moment de la génération.

RGPD — le site ne publie que le CATALOGUE FORMATIONS, qui ne contient aucune
donnée personnelle. Les tables APPRENANTS, INSCRIPTIONS, PRESENCES et
EVALUATIONS ne sont jamais lues ici, et ne doivent jamais l'être.
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE_ID = "appQ2zqc80kkc6MR1"
TABLE_CATALOGUE = "tblEYxI7LpLZpBPlo"
TABLE_CONFIG = "tblQJDUCikyk9zCjq"

# ─── Règle de marque blanche ──────────────────────────────────────────────
# Le contrat du donneur d'ordre interdit toute mention de YEBA FORMATIONS sur
# les supports des actions sous-traitées. Publier une de ces fiches sur le site
# YEBA serait une violation contractuelle. Le filtre est donc une LISTE BLANCHE :
# tout ce qui n'est pas explicitement autorisé est exclu, y compris une valeur
# nouvelle ou vide. Ne jamais transformer ceci en liste noire.
MARQUES_PUBLIABLES = {
    "Catalogue YEBA — marque YEBA obligatoire",
    "Client direct — marque YEBA obligatoire",
}
STATUTS_PUBLIABLES = {"Active"}

CHAMPS = [
    "Titre formation", "Type de formation", "Domaine", "Statut",
    "Durée en heures", "Tarif inter HT / jour / personne",
    "Public cible", "Objectifs pédagogiques", "Prérequis",
    "Méthodes pédagogiques", "Financements éligibles",
    "Délai et modalités d'accès", "Accessibilité handicap",
    "Marque / Confidentialité contractuelle",
]

# Mentions sanctionnées, vérifiées à chaque génération : une régression sur ce
# point est un risque juridique, pas un détail de mise en page.
#
# Le contrôle vise l'AFFIRMATION trompeuse, pas le sigle. Écrire « non éligible
# au CPF » est au contraire souhaitable : chercher « cpf » sans regarder ce qui
# le précède bloquerait la mention protectrice en même temps que la faute.
import re

AFFIRMATIONS_CPF = re.compile(
    r"(?<!non )(?<!pas )(?:éligibles?|finançables?|finance[rz]?|utilisable)"
    r"[^.]{0,40}(?:cpf|compte personnel de formation|mon compte formation)"
    r"|(?:cpf|mon compte formation)[^.]{0,30}(?:éligible|accepté|possible)",
    re.IGNORECASE,
)


def _get(path, params=None):
    token = os.environ.get("AIRTABLE_TOKEN")
    if not token:
        sys.exit("AIRTABLE_TOKEN absent. Renseignez-le dans .env (jamais dans Git).")
    url = f"https://api.airtable.com/v0/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Airtable a répondu {e.code} : {e.read().decode('utf-8', 'replace')[:300]}")


def _plat(valeur):
    """Airtable rend les listes de choix sous forme d'objets ; on ne garde que le nom."""
    if isinstance(valeur, dict):
        return valeur.get("name", "")
    if isinstance(valeur, list):
        return [v.get("name", v) if isinstance(v, dict) else v for v in valeur]
    return valeur


def recuperer_formations():
    records, params = [], {"pageSize": 100, "fields[]": CHAMPS}
    while True:
        rep = _get(f"{BASE_ID}/{TABLE_CATALOGUE}", params)
        records += rep.get("records", [])
        offset = rep.get("offset")
        if not offset:
            return records
        params["offset"] = offset


def filtrer(records):
    publiables, exclues = [], []
    for rec in records:
        f = {k: _plat(v) for k, v in rec.get("fields", {}).items()}
        titre = f.get("Titre formation", "").strip()
        marque = f.get("Marque / Confidentialité contractuelle", "")
        statut = f.get("Statut", "")

        if not titre:
            exclues.append(("(fiche sans titre)", "titre vide"))
        elif marque not in MARQUES_PUBLIABLES:
            exclues.append((titre, f"marque « {marque or 'non renseignée'} » non publiable"))
        elif statut not in STATUTS_PUBLIABLES:
            exclues.append((titre, f"statut « {statut or 'non renseigné'} »"))
        else:
            publiables.append({
                "id": rec["id"],
                "titre": titre,
                "domaine": f.get("Domaine", ""),
                "type": f.get("Type de formation", ""),
                "heures": f.get("Durée en heures"),
                "jours": round(f["Durée en heures"] / 7, 1) if f.get("Durée en heures") else None,
                "tarif_jour_personne": f.get("Tarif inter HT / jour / personne"),
                "public": f.get("Public cible", ""),
                "objectifs": f.get("Objectifs pédagogiques", ""),
                "prerequis": f.get("Prérequis", ""),
                "modalites": f.get("Méthodes pédagogiques", []),
                "financements": f.get("Financements éligibles", []),
                "acces": f.get("Délai et modalités d'accès", ""),
                "handicap": bool(f.get("Accessibilité handicap")),
            })
    return publiables, exclues


def controler(formations):
    """Bloque la génération sur les deux fautes qui coûtent le plus cher."""
    erreurs = []
    corpus = json.dumps(formations, ensure_ascii=False)
    for trouve in AFFIRMATIONS_CPF.findall(corpus):
        erreurs.append(
            f"Éligibilité au CPF affirmée (« …{trouve}… »). Aucune formation ne "
            "porte de code RNCP/RS : l'annoncer est une pratique commerciale "
            "trompeuse (code de la consommation, art. L.121-2)."
        )
    for f in formations:
        if not f["objectifs"]:
            erreurs.append(f"« {f['titre'] } » : objectifs pédagogiques vides (RNQ ind. 1).")
        if not f["acces"]:
            erreurs.append(f"« {f['titre'] } » : délai d'accès absent (RNQ ind. 1, mention publique obligatoire).")
    return erreurs


def main():
    check = "--check" in sys.argv
    publiables, exclues = filtrer(recuperer_formations())
    publiables.sort(key=lambda x: x["titre"])

    print(f"Publiables : {len(publiables)}")
    for f in publiables:
        print(f"  ✓ {f['titre']}")
    print(f"\nExclues : {len(exclues)}")
    for titre, motif in exclues:
        print(f"  ✗ {titre} — {motif}")

    erreurs = controler(publiables)
    if erreurs:
        print("\nCONTRÔLE ÉCHOUÉ :")
        for e in erreurs:
            print(f"  ⚠ {e}")
        sys.exit(1)
    print("\nContrôle passé : aucune mention CPF, objectifs et délais d'accès présents.")

    if check:
        print("Mode --check : rien n'a été écrit.")
        return

    sortie = Path(__file__).parent / "data" / "formations.json"
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(
        json.dumps({"formations": publiables}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Écrit : {sortie}")


if __name__ == "__main__":
    main()
