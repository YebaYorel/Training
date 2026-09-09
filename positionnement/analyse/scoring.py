#!/usr/bin/env python3
"""Moteur d'analyse des tests de positionnement — YEBA FORMATIONS.

Un seul moteur pour toutes les formations : le contenu vit dans
``referentiels.json``, jamais dans le code. Ajouter une formation = ajouter une
entrée JSON.

Usage
-----
    python scoring.py --formation FOR-0001 --reponses reponses.json
    python scoring.py --autotest          # jeu d'essai intégré

Le fichier de réponses est une liste d'objets ::

    [{"ref_inscription": "INS-00042",
      "auto": {"B1": 2, "B2": 1, ...},
      "qcm":  {"C1": "b", "C2": "c", ...},
      "ouvertes": {"D1": "...", "D2": "...", "D3": "..."},
      "amenagement": false}]

Aucune donnée nominative n'entre ici : seule la référence d'inscription
circule (minimisation, RGPD art. 5.1.c).
"""

from __future__ import annotations

import argparse
import json
import statistics
from dataclasses import dataclass, field
from pathlib import Path

REFERENTIELS = Path(__file__).with_name("referentiels.json")

NIVEAUX = ("Découverte", "Intermédiaire", "Avancé")
DECISIONS = ("APPUYER", "AJUSTER", "ALLÉGER", "DIFFÉRENCIER")

# En deçà de ce nombre de répondants, l'écart-type d'un domaine reflète surtout
# le hasard de la composition du groupe : les décisions automatiques ne sont
# plus lisibles seules et la synthèse le signale.
SEUIL_ECART_TYPE_FIABLE = 6


def charger_referentiel(code_formation: str, chemin: Path = REFERENTIELS) -> dict:
    donnees = json.loads(chemin.read_text(encoding="utf-8"))
    if code_formation not in donnees:
        disponibles = ", ".join(k for k in donnees if not k.startswith("_"))
        raise KeyError(
            f"Formation {code_formation} absente du référentiel. "
            f"Disponibles : {disponibles}"
        )
    referentiel = donnees[code_formation]
    referentiel["_seuils"] = donnees["_meta"]["seuils"]
    referentiel["_ponderation"] = donnees["_meta"]["ponderation_niveau_global"]
    return referentiel


# --------------------------------------------------------------------------
# Niveau individuel
# --------------------------------------------------------------------------

@dataclass
class ResultatIndividuel:
    ref_inscription: str
    auto: dict[str, float]          # par domaine, 0-100
    reel: dict[str, float]          # par domaine, 0-100
    calibration: dict[str, float]   # auto - reel
    niveau_global: str
    score_global: float
    amenagement: bool = False
    ouvertes: dict[str, str] = field(default_factory=dict)
    incomplet: bool = False

    def alertes_calibration(self, seuils: dict) -> list[tuple[str, str]]:
        """Domaines où le stagiaire se trompe sur lui-même."""
        sur, sous = seuils["calibration_surestimation"], seuils["calibration_sousestimation"]
        signaux = []
        for domaine, ecart in self.calibration.items():
            if ecart > sur:
                signaux.append((domaine, "surestimation"))
            elif ecart < sous:
                signaux.append((domaine, "sous-estimation"))
        return signaux


def scorer_individu(reponse: dict, referentiel: dict) -> ResultatIndividuel:
    domaines = list(referentiel["domaines"])
    auto_items, qcm = referentiel["auto_items"], referentiel["qcm"]

    auto_brut = {d: [] for d in domaines}
    for item, domaine in auto_items.items():
        valeur = reponse.get("auto", {}).get(item)
        if valeur is not None:
            auto_brut[domaine].append(int(valeur))

    reel_brut = {d: [] for d in domaines}
    for question, config in qcm.items():
        donnee = reponse.get("qcm", {}).get(question)
        if donnee is not None:
            juste = str(donnee).strip().lower() == config["correct"]
            reel_brut[config["domaine"]].append(1 if juste else 0)

    attendu_auto = len(auto_items)
    attendu_qcm = len(qcm)
    fournis = sum(len(v) for v in auto_brut.values()) + sum(len(v) for v in reel_brut.values())
    incomplet = fournis < (attendu_auto + attendu_qcm)

    # Un domaine sans aucune réponse vaut 0 : ne pas répondre n'est pas
    # équivalent à maîtriser. Le drapeau `incomplet` signale le cas au relecteur.
    auto = {d: (sum(v) / (3 * len(v)) * 100 if v else 0.0) for d, v in auto_brut.items()}
    reel = {d: (sum(v) / len(v) * 100 if v else 0.0) for d, v in reel_brut.items()}
    calibration = {d: round(auto[d] - reel[d], 1) for d in domaines}

    p = referentiel["_ponderation"]
    score_global = (
        p["reel"] * statistics.fmean(reel.values())
        + p["auto"] * statistics.fmean(auto.values())
    )

    s = referentiel["_seuils"]
    if score_global < s["niveau_decouverte_max"]:
        niveau = NIVEAUX[0]
    elif score_global < s["niveau_intermediaire_max"]:
        niveau = NIVEAUX[1]
    else:
        niveau = NIVEAUX[2]

    return ResultatIndividuel(
        ref_inscription=reponse.get("ref_inscription", "INCONNU"),
        auto={d: round(v, 1) for d, v in auto.items()},
        reel={d: round(v, 1) for d, v in reel.items()},
        calibration=calibration,
        niveau_global=niveau,
        score_global=round(score_global, 1),
        amenagement=bool(reponse.get("amenagement", False)),
        ouvertes=reponse.get("ouvertes", {}),
        incomplet=incomplet,
    )


# --------------------------------------------------------------------------
# Niveau groupe
# --------------------------------------------------------------------------

def decider(moyenne: float, ecart_type: float, seuils: dict) -> str:
    """Décision pédagogique pour un domaine.

    L'hétérogénéité prime : un groupe éclaté se gère d'abord par la
    différenciation, quel que soit son niveau moyen.
    """
    if ecart_type >= seuils["groupe_differencier_sigma_min"]:
        return "DIFFÉRENCIER"
    if moyenne < seuils["groupe_appuyer_max"]:
        return "APPUYER"
    if moyenne < seuils["groupe_ajuster_max"]:
        return "AJUSTER"
    if ecart_type < seuils["groupe_alleger_sigma_max"]:
        return "ALLÉGER"
    return "AJUSTER"


def synthetiser_groupe(resultats: list[ResultatIndividuel], referentiel: dict) -> dict:
    if not resultats:
        raise ValueError("Aucune réponse à analyser.")

    domaines = list(referentiel["domaines"])
    seuils = referentiel["_seuils"]
    synthese = {}

    for domaine in domaines:
        scores = [r.reel[domaine] for r in resultats]
        moyenne = statistics.fmean(scores)
        ecart_type = statistics.pstdev(scores) if len(scores) > 1 else 0.0
        synthese[domaine] = {
            "libelle": referentiel["domaines"][domaine]["libelle"],
            "poids_heures": referentiel["domaines"][domaine]["poids_heures"],
            "moyenne": round(moyenne, 1),
            "ecart_type": round(ecart_type, 1),
            "decision": decider(moyenne, ecart_type, seuils),
        }

    reallocation = proposer_reallocation(synthese)

    return {
        "nb_reponses": len(resultats),
        "domaines": synthese,
        "reallocation_minutes": reallocation,
        "repartition_niveaux": {
            niveau: sum(1 for r in resultats if r.niveau_global == niveau)
            for niveau in NIVEAUX
        },
        "amenagements": [r.ref_inscription for r in resultats if r.amenagement],
        "incomplets": [r.ref_inscription for r in resultats if r.incomplet],
    }


def proposer_reallocation(synthese: dict) -> dict:
    """Transfère du temps des domaines ALLÉGER vers les domaines APPUYER.

    On libère 40 % du volume d'un domaine allégé — jamais davantage : le module
    reste traité et évalué, comme l'exige l'engagement porté au programme
    (Qualiopi ind. 5 et 6). On ne supprime rien, on redistribue.
    """
    liberables = {
        d: round(v["poids_heures"] * 60 * 0.4)
        for d, v in synthese.items()
        if v["decision"] == "ALLÉGER"
    }
    total = sum(liberables.values())
    if not total:
        return {}

    beneficiaires = sorted(
        (d for d, v in synthese.items() if v["decision"] in ("APPUYER", "DIFFÉRENCIER")),
        key=lambda d: synthese[d]["moyenne"],
    )
    if not beneficiaires:
        return {}

    # Le domaine le plus faible reçoit le plus : poids inverse de la moyenne.
    poids = [100 - synthese[d]["moyenne"] + 1 for d in beneficiaires]
    somme = sum(poids)
    plan = {f"-{d}": -m for d, m in liberables.items()}
    for domaine, p in zip(beneficiaires, poids):
        plan[f"+{domaine}"] = round(total * p / somme)
    return plan


# --------------------------------------------------------------------------
# Rendu
# --------------------------------------------------------------------------

def rendre_synthese_groupe(groupe: dict, referentiel: dict, code: str) -> str:
    lignes = [
        f"# Synthèse de positionnement — {referentiel['titre']} ({code})",
        "",
        f"**{groupe['nb_reponses']} réponse(s) analysée(s).**",
        "",
    ]
    if groupe["nb_reponses"] < SEUIL_ECART_TYPE_FIABLE:
        lignes += [
            f"> ⚠️ **Moins de {SEUIL_ECART_TYPE_FIABLE} réponses : l'écart-type "
            "n'est pas interprétable.** Une seule personne atypique suffit à "
            "faire basculer un domaine en « DIFFÉRENCIER ». Lire ici les "
            "moyennes et les profils individuels, pas les décisions "
            "automatiques.",
            "",
        ]
    lignes += [
        "| Domaine | Moyenne | Écart-type | Décision |",
        "|---|---:|---:|---|",
    ]
    for domaine, v in groupe["domaines"].items():
        lignes.append(
            f"| **{domaine}** — {v['libelle']} | {v['moyenne']} | "
            f"{v['ecart_type']} | **{v['decision']}** |"
        )

    lignes += ["", "## Répartition des niveaux", ""]
    for niveau, n in groupe["repartition_niveaux"].items():
        lignes.append(f"- {niveau} : **{n}**")

    if groupe["reallocation_minutes"]:
        lignes += ["", "## Réallocation de temps proposée", ""]
        for cle, minutes in groupe["reallocation_minutes"].items():
            sens = "libérées de" if minutes < 0 else "ajoutées à"
            lignes.append(f"- {abs(minutes)} min {sens} **{cle[1:]}**")
        lignes.append("")
        lignes.append(
            "> Les modules allégés restent traités et évalués : seule la "
            "profondeur change, jamais le périmètre annoncé au programme."
        )

    if groupe["amenagements"]:
        lignes += [
            "",
            "## Aménagements à prévoir",
            "",
            f"{len(groupe['amenagements'])} stagiaire(s) ont signalé un besoin "
            "d'aménagement : " + ", ".join(groupe["amenagements"]),
            "",
            "> Contacter chaque personne **avant** la session. Ne consigner que "
            "le besoin exprimé, jamais la cause médicale (RGPD art. 9).",
        ]

    if groupe["incomplets"]:
        lignes += [
            "",
            "## À vérifier",
            "",
            "Réponses incomplètes (extraction papier douteuse ou formulaire "
            "partiel) — **à relire avant validation** : "
            + ", ".join(groupe["incomplets"]),
        ]

    lignes += [
        "",
        "---",
        "",
        "> Synthèse produite par un outil automatisé. **Elle n'a aucune valeur "
        "tant qu'elle n'est pas relue et validée par le responsable "
        "pédagogique.** Aucune décision concernant un stagiaire ne repose sur "
        "ce document seul.",
    ]
    return "\n".join(lignes)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

JEU_ESSAI = [
    {  # débutant lucide
        "ref_inscription": "INS-00001",
        "auto": {"B1": 0, "B2": 1, "B3": 0, "B4": 1, "B5": 1, "B6": 1, "B7": 0, "B8": 1},
        "qcm": {"C1": "a", "C2": "c", "C3": "a", "C4": "b", "C5": "a", "C6": "b",
                "C7": "a", "C8": "c", "C9": "b", "C10": "a", "C11": "b", "C12": "b"},
        "ouvertes": {"D1": "Rédiger mes devis plus vite."},
    },
    {  # surestimation nette : se croit expert, échoue
        "ref_inscription": "INS-00002",
        "auto": {"B1": 3, "B2": 3, "B3": 3, "B4": 3, "B5": 3, "B6": 3, "B7": 3, "B8": 3},
        "qcm": {"C1": "a", "C2": "a", "C3": "b", "C4": "a", "C5": "a", "C6": "b",
                "C7": "a", "C8": "a", "C9": "b", "C10": "a", "C11": "a", "C12": "b"},
        "amenagement": True,
    },
    {  # avancé
        "ref_inscription": "INS-00003",
        "auto": {"B1": 3, "B2": 3, "B3": 2, "B4": 3, "B5": 3, "B6": 2, "B7": 3, "B8": 3},
        "qcm": {"C1": "b", "C2": "c", "C3": "a", "C4": "b", "C5": "c", "C6": "a",
                "C7": "b", "C8": "c", "C9": "a", "C10": "c", "C11": "b", "C12": "a"},
    },
    {  # sous-estimation : sait faire, n'ose pas le dire
        "ref_inscription": "INS-00004",
        "auto": {"B1": 1, "B2": 0, "B3": 1, "B4": 1, "B5": 0, "B6": 1, "B7": 1, "B8": 0},
        "qcm": {"C1": "b", "C2": "c", "C3": "a", "C4": "b", "C5": "c", "C6": "a",
                "C7": "b", "C8": "c", "C9": "a", "C10": "c", "C11": "b", "C12": "a"},
    },
]


def autotest() -> int:
    ref = charger_referentiel("FOR-0001")
    resultats = [scorer_individu(r, ref) for r in JEU_ESSAI]
    seuils = ref["_seuils"]
    echecs = []

    r2 = resultats[1]
    if not any(t == "surestimation" for _, t in r2.alertes_calibration(seuils)):
        echecs.append("INS-00002 aurait dû être détecté en surestimation")
    if r2.niveau_global != "Découverte":
        echecs.append(f"INS-00002 : niveau {r2.niveau_global}, attendu Découverte")

    r3 = resultats[2]
    if r3.niveau_global != "Avancé":
        echecs.append(f"INS-00003 : niveau {r3.niveau_global}, attendu Avancé")
    if any(abs(v) > 25 for v in r3.calibration.values()):
        echecs.append("INS-00003 aurait dû être calibré")

    r4 = resultats[3]
    if not any(t == "sous-estimation" for _, t in r4.alertes_calibration(seuils)):
        echecs.append("INS-00004 aurait dû être détecté en sous-estimation")

    groupe = synthetiser_groupe(resultats, ref)
    if groupe["amenagements"] != ["INS-00002"]:
        echecs.append(f"aménagements : {groupe['amenagements']}, attendu ['INS-00002']")
    if not all(v["decision"] in DECISIONS for v in groupe["domaines"].values()):
        echecs.append("décision hors du vocabulaire autorisé")

    print(rendre_synthese_groupe(groupe, ref, "FOR-0001"))
    print("\n" + "=" * 70)
    for r in resultats:
        signaux = r.alertes_calibration(seuils) or [("—", "calibré")]
        détail = ", ".join(f"{d}:{t}" for d, t in signaux)
        print(f"{r.ref_inscription}  {r.score_global:>5} pts  "
              f"{r.niveau_global:<14} {détail}")
    print("=" * 70)

    if echecs:
        print("\nAUTOTEST EN ÉCHEC :")
        for e in echecs:
            print(f"  - {e}")
        return 1
    print("\nAUTOTEST OK — 5 vérifications passées.")
    return 0


def main() -> int:
    parseur = argparse.ArgumentParser(description=__doc__)
    parseur.add_argument("--formation", help="code catalogue, ex. FOR-0001")
    parseur.add_argument("--reponses", type=Path, help="fichier JSON des réponses")
    parseur.add_argument("--autotest", action="store_true", help="jeu d'essai intégré")
    args = parseur.parse_args()

    if args.autotest:
        return autotest()
    if not (args.formation and args.reponses):
        parseur.error("--formation et --reponses sont requis (ou --autotest)")

    ref = charger_referentiel(args.formation)
    reponses = json.loads(args.reponses.read_text(encoding="utf-8"))
    resultats = [scorer_individu(r, ref) for r in reponses]
    print(rendre_synthese_groupe(synthetiser_groupe(resultats, ref), ref, args.formation))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
