"""Chef d'orchestre : documents reçus → analyse → plan → fichiers de sortie."""

from __future__ import annotations

import datetime as dt
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .config import Charte, Identite, Reglages, charger_charte, dossier_donnees, identite_depuis
from .extraction import lire_document
from .planification import Parametres, Plan, construire_plan
from .referentiels import (FicheFranceCompetences, Reac, ReferentielEvaluation, analyser_fiche_fc,
                           analyser_re, analyser_reac, detecter_type)
from .securite import restreindre_droits

SOURCES_PEDAGOGIQUES = [
    "Taxonomie de Bloom révisée : Anderson L. W. & Krathwohl D. R. (2001), A Taxonomy for Learning, "
    "Teaching, and Assessing.",
    "Étayage : Wood D., Bruner J. S. & Ross G. (1976), « The role of tutoring in problem solving », "
    "Journal of Child Psychology and Psychiatry, 17.",
    "Modes de représentation et curriculum en spirale : Bruner J. S. (1966), Toward a Theory of Instruction.",
    "Jours fériés : Code du travail, art. L3133-1 ; 20 décembre à La Réunion : décret n° 83-1003 du 23/11/1983.",
    "Qualiopi : Référentiel national qualité (décret n° 2019-564) — indicateurs 1, 2, 5, 6, 7.",
]


@dataclass
class Contexte:
    reac: Reac
    re: Optional[ReferentielEvaluation]
    fiche: Optional[FicheFranceCompetences]
    plan: Plan
    reglages: Reglages
    charte: Charte
    identite: Identite
    base: Path
    tarif: Optional[dict] = None
    hypotheses: list[str] = field(default_factory=list)
    alertes: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)

    @property
    def titre(self) -> str:
        if self.fiche and self.fiche.intitule:
            return self.fiche.intitule
        return f"TP {self.reac.intitule}"

    @property
    def code(self) -> str:
        return (self.fiche.code if self.fiche and self.fiche.code else self.reac.code_titre) or "SANS-CODE"


def analyser_documents(chemins: list[Path]) -> dict:
    """Lit et classe automatiquement chaque document (REAC, RE/RC, fiche)."""
    res: dict = {"reac": None, "re": None, "fiche": None, "inconnus": [], "noms": {}}
    textes = {}
    for c in chemins:
        texte = lire_document(c)
        type_ = detecter_type(texte)
        textes[c] = (texte, type_)
    for c, (texte, type_) in textes.items():
        if type_ == "REAC":
            res["reac"] = analyser_reac(texte, lire_document(c, nettoyer=False))
            res["noms"]["reac"] = c.name
    for c, (texte, type_) in textes.items():
        if type_ == "RE":
            res["re"] = analyser_re(texte, res["reac"])
            res["noms"]["re"] = c.name
        elif type_ == "FICHE":
            res["fiche"] = analyser_fiche_fc(texte)
            res["noms"]["fiche"] = c.name
        elif type_ == "INCONNU":
            res["inconnus"].append(c.name)
    return res


def _date(s: str) -> Optional[dt.date]:
    s = (s or "").strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def _plages(s: str) -> list[tuple[str, str]]:
    plages = []
    for morceau in re.split(r"[,;]", s or ""):
        m = re.match(r"\s*(\d{1,2}[:h]\d{2})\s*-\s*(\d{1,2}[:h]\d{2})\s*$", morceau)
        if m:
            plages.append((m.group(1).replace("h", ":"), m.group(2).replace("h", ":")))
    return plages


def parametres_depuis(reglages: Reglages, hypotheses: list[str]) -> Parametres:
    debut = _date(reglages.date_debut)
    if not debut:
        debut = dt.date.today() + dt.timedelta(days=(7 - dt.date.today().weekday()))
        hypotheses.append(f"Date de début non fournie : lundi {debut:%d/%m/%Y} retenu par défaut.")
    if reglages.heures_centre <= 0:
        raise ValueError("Indiquez la durée en centre (en heures) : la fiche France Compétences ne la donne pas.")
    fermetures = []
    for morceau in re.split(r"[;\n]", reglages.fermetures or ""):
        m = re.match(r"\s*(\S+?)(?:\.\.(\S+))?\s*(.*)$", morceau)
        if m and _date(m.group(1)):
            a = _date(m.group(1))
            b = _date(m.group(2)) if m.group(2) else a
            fermetures.append((a, b or a, m.group(3).strip() or "fermeture"))
    jours = sorted({int(x) - 1 for x in re.findall(r"[1-7]", reglages.jours or "")}) or [0, 1, 2, 3, 4]
    poids = {int(a): float(b) for a, b in re.findall(r"(\d+)\s*=\s*([\d.]+)", reglages.poids_cp or "")}
    ordre = [int(x) for x in re.findall(r"\d+", reglages.ordre_cp or "")]
    p = Parametres(
        date_debut=debut, heures_centre=reglages.heures_centre,
        creneaux=_plages(reglages.creneaux) or [("08:30", "12:00"), ("13:00", "16:30")],
        pauses=_plages(reglages.pauses), jours_semaine=jours,
        rythme=re.sub(r"[^CEce]", "", reglages.rythme or ""), fermetures=fermetures,
        heures_entreprise=reglages.heures_entreprise, date_examen=_date(reglages.date_examen),
        ordre_cp=ordre, poids_cp=poids, h_accueil=reglages.h_accueil, h_ecf_par_at=reglages.h_ecf_par_at,
        h_dossier_pro=reglages.h_dossier_pro, h_productions=reglages.h_productions,
        h_examen_blanc=reglages.h_examen_blanc, h_bilan=reglages.h_bilan)
    return p


def construire_contexte(analyse: dict, reglages: Reglages, base: Optional[Path] = None,
                        tarif: Optional[dict] = None) -> Contexte:
    base = base or dossier_donnees()
    reac = analyse["reac"]
    if not reac or not reac.competences:
        raise ValueError("Aucun REAC exploitable : le REAC est indispensable (activités types et compétences).")
    hypotheses: list[str] = []
    p = parametres_depuis(reglages, hypotheses)
    plan = construire_plan(reac, analyse["re"], p)
    alertes = list(reac.avertissements)
    if analyse["re"]:
        alertes += analyse["re"].avertissements
    else:
        alertes.append("Pas de RE/RC fourni : l'examen simplifié est construit depuis la fiche France Compétences.")
    if analyse["fiche"]:
        alertes += analyse["fiche"].avertissements
    else:
        alertes.append("Pas de fiche France Compétences : le programme est incomplet (code, certificateur…).")
    if not reglages.heures_entreprise and analyse["re"] and analyse["re"].periode_entreprise:
        m = re.search(r"(\d+)\s*heures pour le titre", " ".join(analyse["re"].periode_entreprise))
        if m:
            reglages.heures_entreprise = float(m.group(1))
            hypotheses.append(f"Période en entreprise : minimum réglementaire de {m.group(1)} h repris du RE.")
    charte = charger_charte(base)
    if not charte.couleurs_validees:
        alertes.append("Couleurs de charte provisoires : saisissez les codes exacts YEBA FORMATIONS (menu Charte).")
    ctx = Contexte(reac=reac, re=analyse["re"], fiche=analyse["fiche"], plan=plan, reglages=reglages,
                   charte=charte, identite=identite_depuis(reglages), base=base, tarif=tarif,
                   hypotheses=hypotheses + p.hypotheses, alertes=alertes)
    ctx.sources = [f"Document source : {v}" for v in analyse.get("noms", {}).values()] + SOURCES_PEDAGOGIQUES
    if ctx.fiche and ctx.fiche.code:
        ctx.sources.insert(0, f"Fiche France Compétences : https://www.francecompetences.fr/recherche/"
                              f"{ctx.fiche.type_fiche.lower()}/{re.sub(r'[^0-9]', '', ctx.fiche.code)}/")
    return ctx


def generer_sorties(ctx: Contexte, dossier: Path) -> dict[str, Path]:
    from .export_autres import (exporter_examen_docx, exporter_ics, exporter_programme_docx,
                                page_programme_html, slug)
    from .export_excel import exporter_classeur

    dossier.mkdir(parents=True, exist_ok=True)
    restreindre_droits(dossier)
    sigle = slug(ctx.reac.sigle or ctx.code)
    sorties = {
        "decorticage": exporter_classeur(ctx, dossier / f"Decorticage_{sigle}.xlsx"),
        "programme": exporter_programme_docx(ctx, dossier / f"Programme_{sigle}.docx"),
        "examen": exporter_examen_docx(ctx, dossier / f"Examen_simplifie_{sigle}.docx"),
        "agenda": exporter_ics(ctx, dossier / f"Planning_{sigle}.ics"),
    }
    page, donnees = page_programme_html(ctx)
    apercu = dossier / f"Apercu_page_site_{sigle}.html"
    apercu.write_text(page, encoding="utf-8")
    sorties["apercu_site"] = apercu
    (dossier / f"programme_{sigle}.json").write_text(json.dumps(donnees, ensure_ascii=False, indent=2),
                                                     encoding="utf-8")
    sorties["programme_json"] = dossier / f"programme_{sigle}.json"
    for p in sorties.values():
        restreindre_droits(p)
    return sorties


def publier_sur_site(ctx: Contexte, base: Optional[Path] = None) -> Path:
    """Écrit la page du programme dans site_a_publier/ — seulement si « Oui »."""
    from .export_autres import page_programme_html, slug
    from .publication import RegistrePublication

    base = base or ctx.base
    reg = RegistrePublication(base)
    reg.verifier_publiable(ctx.code)
    ctx.tarif = reg.tarif_valide(ctx.code) or None
    page, donnees = page_programme_html(ctx)
    cible = base / "site_a_publier" / slug(ctx.titre)
    cible.mkdir(parents=True, exist_ok=True)
    (cible / "index.html").write_text(page, encoding="utf-8")
    (cible / "programme.json").write_text(json.dumps(donnees, ensure_ascii=False, indent=2), encoding="utf-8")
    for f in (cible, cible / "index.html", cible / "programme.json"):
        restreindre_droits(f)
    return cible


def retirer_du_site(titre: str, base: Path) -> bool:
    """Supprime la page générée d'un programme (après un « Non »)."""
    import shutil

    from .export_autres import slug
    from .securite import chemin_dans

    cible = chemin_dans(base / "site_a_publier", slug(titre))
    if cible.exists():
        shutil.rmtree(cible)
        return True
    return False
