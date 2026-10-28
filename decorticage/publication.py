"""Passerelle vers le site internet, toujours soumise à votre accord.

Trois réponses possibles à chaque programme :
* « oui »             → la page est générée dans `site_a_publier/` ;
* « non_redemander »  → rien n'est publié, la question sera reposée ;
* « non_definitif »   → jamais publié, la question n'est plus jamais posée
                        et toute tentative de publication est refusée.
"""

from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
from typing import Optional

from .securite import restreindre_droits

CHOIX = {
    "oui": "Oui, publier sur le site",
    "non_redemander": "Non (me redemander la prochaine fois)",
    "non_definitif": "Non, définitivement (ne jamais publier, ne plus demander)",
}


class PublicationRefusee(PermissionError):
    pass


class RegistrePublication:
    def __init__(self, base: Path) -> None:
        self.fichier = base / "publication.json"

    def _lire(self) -> dict:
        if self.fichier.exists():
            return json.loads(self.fichier.read_text(encoding="utf-8"))
        return {}

    def _ecrire(self, d: dict) -> None:
        tmp = self.fichier.with_suffix(".tmp")
        tmp.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, self.fichier)
        restreindre_droits(self.fichier)

    def statut(self, code: str) -> str:
        return self._lire().get(code, {}).get("statut", "a_demander")

    def doit_demander(self, code: str) -> bool:
        return self.statut(code) in ("a_demander", "non_redemander")

    def decider(self, code: str, choix: str, tarif: Optional[dict] = None) -> None:
        if choix not in CHOIX:
            raise ValueError("Choix inconnu.")
        d = self._lire()
        entree = d.get(code, {"historique": []})
        if entree.get("statut") == "non_definitif":
            raise PublicationRefusee("Ce programme a été refusé définitivement : il ne sera jamais publié.")
        entree["statut"] = choix
        entree["date"] = dt.datetime.now().isoformat(timespec="seconds")
        if tarif is not None:
            entree["tarif"] = tarif
        entree["historique"].append({"date": entree["date"], "choix": choix})
        d[code] = entree
        self._ecrire(d)

    def tarif_valide(self, code: str) -> Optional[dict]:
        return self._lire().get(code, {}).get("tarif")

    def verifier_publiable(self, code: str) -> None:
        s = self.statut(code)
        if s != "oui":
            raise PublicationRefusee(
                "Publication non autorisée : " + ("refus définitif." if s == "non_definitif" else "votre accord est requis."))
