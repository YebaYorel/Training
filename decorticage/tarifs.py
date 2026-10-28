"""Suggestion de prix inter / intra à partir de vos tarifs existants.

Source : export CSV ou XLSX de la base « YEBA FORMATIONS - centre de formation
(adaptable) ». Le logiciel n'appelle PAS Airtable directement :
* Airtable est un service américain (soumis au Cloud Act) → un export
  ponctuel limite l'exposition ; la migration vers Baserow (UE) déjà
  branché dans ce dépôt est recommandée ;
* aucun jeton d'accès Airtable n'est donc stocké sur l'ordinateur.

Le prix n'est JAMAIS publié sans votre validation (voir publication.py).
"""

from __future__ import annotations

import re
import statistics
from pathlib import Path
from typing import Optional

from .extraction import lire_tableau
from .referentiels import normaliser


def _colonne(titres: list[str], *indices: str) -> Optional[str]:
    for t in titres:
        nt = normaliser(t)
        if any(i in nt for i in indices):
            return t
    return None


def _nombre(v) -> Optional[float]:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = re.sub(r"[^\d,.\-]", "", str(v)).replace(",", ".")
    if s.count(".") > 1:
        s = s.replace(".", "", s.count(".") - 1)
    try:
        return float(s)
    except ValueError:
        return None


def charger_tarifs(chemin: Path) -> list[dict]:
    """Normalise les lignes : intitulé, domaine, modalité, heures, prix HT."""
    lignes = lire_tableau(chemin)
    if not lignes:
        return []
    titres = list(lignes[0].keys())
    c_nom = _colonne(titres, "intitul", "formation", "nom", "titre")
    c_prix = _colonne(titres, "prix", "tarif", "montant", "cout")
    c_heures = _colonne(titres, "heure", "duree (h", "nb h")
    c_jours = _colonne(titres, "jour")
    c_mod = _colonne(titres, "modalit", "inter", "intra", "type")
    c_dom = _colonne(titres, "domaine", "categorie", "thematique", "theme", "famille")
    res = []
    for l in lignes:
        prix = _nombre(l.get(c_prix)) if c_prix else None
        heures = _nombre(l.get(c_heures)) if c_heures else None
        if not heures and c_jours:
            j = _nombre(l.get(c_jours))
            heures = j * 7 if j else None
        if not prix or not heures or prix <= 0 or heures <= 0:
            continue
        mod = normaliser(str(l.get(c_mod, ""))) if c_mod else ""
        res.append({
            "intitule": str(l.get(c_nom, "")).strip() if c_nom else "",
            "domaine": str(l.get(c_dom, "")).strip() if c_dom else "",
            "modalite": "intra" if "intra" in mod else ("inter" if "inter" in mod else "inconnue"),
            "heures": heures, "prix": prix, "taux_horaire": prix / heures,
        })
    return res


MOTS_DOMAINE = ["vente", "commerc", "manag", "magasin", "distribution", "relation client", "equipe"]


def suggerer(tarifs: list[dict], heures: float, mots: Optional[list[str]] = None) -> dict:
    """Suggestion argumentée (médianes), jamais publiée sans validation."""
    if not tarifs:
        return {"valide": False, "message": "Aucun tarif importé : importez l'export CSV/XLSX de votre base tarifs."}
    mots = mots or MOTS_DOMAINE
    proches = [t for t in tarifs if any(m in normaliser(t["intitule"] + " " + t["domaine"]) for m in mots)]
    base = proches if len(proches) >= 2 else tarifs
    res = {"valide": False, "base": f"{len(base)} formation(s) de référence"
                                    f"{' du même domaine' if base is proches else ' (tous domaines)'}",
           "heures": heures}
    inter = [t["taux_horaire"] for t in base if t["modalite"] == "inter"]
    intra = [t["taux_horaire"] for t in base if t["modalite"] == "intra"]
    if not inter and not intra:
        inter = [t["taux_horaire"] for t in base]
    if inter:
        th = statistics.median(inter)
        res["inter_taux_horaire"] = round(th, 2)
        res["inter_par_stagiaire"] = round(th * heures, -1)
    if intra:
        th = statistics.median(intra)
        res["intra_taux_horaire"] = round(th, 2)
        res["intra_par_jour_groupe"] = round(th * 7, -1)
        res["intra_total_groupe"] = round(th * heures, -1)
    res["affichage"] = {}
    if "inter_par_stagiaire" in res:
        res["affichage"]["Inter-entreprises (par stagiaire, HT)"] = f"{res['inter_par_stagiaire']:,.0f} €".replace(",", " ")
    if "intra_par_jour_groupe" in res:
        res["affichage"]["Intra-entreprise (par jour, par groupe, HT)"] = f"{res['intra_par_jour_groupe']:,.0f} €".replace(",", " ")
    res["message"] = ("Suggestion calculée sur la médiane de vos taux horaires — à valider ou modifier "
                      "avant toute publication.")
    return res
