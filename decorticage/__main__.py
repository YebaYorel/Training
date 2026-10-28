"""Point d'entrée : `python -m decorticage` (interface) ou sous-commandes.

    python -m decorticage                 → ouvre l'interface dans le navigateur
    python -m decorticage generer --reac REAC.pdf --re RE.pdf --fiche RNCP.pdf \
        --heures 455 --debut 2027-01-04 --sortie ./sorties
    python -m decorticage audit           → contrôle de sécurité (+ --corriger)
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def main(argv=None) -> int:
    if os.name == "posix":
        os.umask(0o077)   # tout fichier créé par le logiciel est privé (vous seul)
    parser = argparse.ArgumentParser(prog="decorticage", description="Décorticage pédagogique de titres professionnels")
    sous = parser.add_subparsers(dest="commande")

    p_ui = sous.add_parser("interface", help="ouvrir l'interface (par défaut)")
    p_ui.add_argument("--port", type=int, default=0)
    p_ui.add_argument("--sans-navigateur", action="store_true")

    p_gen = sous.add_parser("generer", help="générer sans interface")
    p_gen.add_argument("--reac", required=True, type=Path)
    p_gen.add_argument("--re", type=Path)
    p_gen.add_argument("--fiche", type=Path)
    p_gen.add_argument("--heures", required=True, type=float, help="durée en centre (heures)")
    p_gen.add_argument("--debut", required=True, help="date de début AAAA-MM-JJ")
    p_gen.add_argument("--jours", default="1,2,3,4,5")
    p_gen.add_argument("--rythme", default="")
    p_gen.add_argument("--creneaux", default="08:30-12:00, 13:00-16:30")
    p_gen.add_argument("--pauses", default="10:15-10:30, 14:45-15:00")
    p_gen.add_argument("--fermetures", default="")
    p_gen.add_argument("--commanditaire", default="", help="autre centre : masque YEBA FORMATIONS")
    p_gen.add_argument("--sortie", required=True, type=Path)

    p_aud = sous.add_parser("audit", help="contrôle de sécurité")
    p_aud.add_argument("--corriger", action="store_true")

    a = parser.parse_args(argv)
    if a.commande in (None, "interface"):
        from .app import lancer
        lancer(port=getattr(a, "port", 0), ouvrir=not getattr(a, "sans_navigateur", False))
        return 0
    if a.commande == "generer":
        from .config import Reglages
        from .moteur import analyser_documents, construire_contexte, generer_sorties
        docs = [x for x in (a.reac, a.re, a.fiche) if x]
        r = Reglages(heures_centre=a.heures, date_debut=a.debut, jours=a.jours, rythme=a.rythme,
                     creneaux=a.creneaux, pauses=a.pauses, fermetures=a.fermetures, commanditaire=a.commanditaire)
        ctx = construire_contexte(analyser_documents(docs), r)
        for k, v in generer_sorties(ctx, a.sortie).items():
            print(f"{k:16} {v}")
        for x in ctx.alertes + ctx.plan.avertissements + ctx.hypotheses:
            print(f"! {x}")
        return 0
    if a.commande == "audit":
        from . import audit
        from .config import dossier_donnees
        base = dossier_donnees()
        if a.corriger:
            audit.corriger(base)
        ok = True
        for r in audit.auditer(base):
            ok &= r["ok"]
            print(f"[{'OK' if r['ok'] else '!!'}] {r['controle']} — {r['detail']}")
        return 0 if ok else 1
    return 1


if __name__ == "__main__":
    sys.exit(main())
