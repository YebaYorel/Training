"""Contenus « Programme de formation » et « Examen simplifié ».

Un seul constructeur pour tous les formats (Excel, Word, page web) : le
même texte partout, donc aucune incohérence entre le classeur et le site.

Le programme reprend les informations obligatoires ou attendues par le
Référentiel national qualité (Qualiopi, critère 1 — indicateurs 1 et 2 :
information du public sur les prestations, délais, modalités, tarifs,
accessibilité, indicateurs de résultats).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

from .pedagogie import simplifier
from .planification import fmt_duree
from .referentiels import FicheFranceCompetences, Reac, ReferentielEvaluation, normaliser

A_COMPLETER = "À compléter"


@dataclass
class Section:
    titre: str
    paragraphes: list[str] = field(default_factory=list)
    puces: list[str] = field(default_factory=list)
    tableau: list[list[str]] = field(default_factory=list)   # 1re ligne = en-têtes


def construire_programme(reac: Reac, re_: Optional[ReferentielEvaluation],
                         fiche: Optional[FicheFranceCompetences], plan, reglages,
                         tarif: Optional[dict] = None) -> tuple[str, list[Section]]:
    f = fiche or FicheFranceCompetences()
    intitule = (f.intitule or (f"TP - {reac.intitule}" if reac.intitule else "")).strip() or A_COMPLETER
    sections: list[Section] = []

    ident = Section("Identification de la certification")
    ident.tableau = [["Élément", "Information"]] + [[a, b] for a, b in [
        ("Intitulé", intitule),
        ("Code France Compétences", f.code or A_COMPLETER),
        ("Niveau", f.niveau or (f"Niveau {reac.niveau}" if reac.niveau else A_COMPLETER)),
        ("Certificateur", f.certificateur or A_COMPLETER),
        ("Code(s) NSF", " ; ".join(f.nsf) or A_COMPLETER),
        ("Formacode(s)", " ; ".join(f.formacodes) or A_COMPLETER),
        ("Code(s) ROME", " ; ".join(f.rome) or A_COMPLETER),
        ("Enregistrement valable jusqu'au", f.date_echeance or A_COMPLETER),
    ]]
    sections.append(ident)

    obj = Section("Objectifs de la formation")
    if f.objectifs:
        obj.paragraphes.append(f.objectifs)
    obj.puces = [f"AT{a.numero} — {a.intitule}" for a in reac.activites]
    sections.append(obj)

    pub = Section("Public et prérequis")
    pub.puces = [
        f"Public : {reglages.public or A_COMPLETER}",
        f"Prérequis : {reglages.prerequis or f.prerequis_entree or 'Aucun prérequis réglementaire indiqué sur la fiche — à définir par l’organisme (test de positionnement recommandé)'}",
    ]
    voies = [v for v, ok in f.voies_acces if ok]
    if voies:
        pub.puces.append("Voies d'accès : " + " ; ".join(voies))
    sections.append(pub)

    duree = Section("Durée, rythme et lieu")
    h_centre = sum(l["minutes"] for l in plan.lignes) if plan else 0
    duree.puces = [
        f"Durée en centre : {fmt_duree(h_centre)}" if h_centre else f"Durée en centre : {A_COMPLETER}",
        f"Période en entreprise : {fmt_duree(reglages.heures_entreprise * 60)}" if reglages.heures_entreprise
        else "Période en entreprise obligatoire (voir « Validation »)",
        f"Dates : du {plan.lignes[0]['date']:%d/%m/%Y} au {plan.date_fin:%d/%m/%Y}" if plan and plan.lignes
        else f"Dates : {A_COMPLETER}",
        f"Horaires : {reglages.creneaux}",
        f"Lieu : {reglages.lieu or A_COMPLETER}",
        f"Délai d'accès : {reglages.delai_acces or A_COMPLETER}",
    ]
    sections.append(duree)

    contenu = Section("Contenu de la formation (par compétence)")
    contenu.tableau = [["Bloc / Activité type", "Compétence", "Contenus clés", "Durée"]]
    for at in reac.activites:
        for n in at.competences:
            cp = reac.competence(n)
            seances = [s for s in plan.seances if s.cp == n and s.type_seance != "evaluation"] if plan else []
            titres = list(dict.fromkeys(re.sub(r" \(partie \d+/\d+\)$", "", s.titre) for s in seances))
            minutes = plan.minutes_cp.get(n, 0) if plan else 0
            courts = [t if len(t) <= 70 else t[:70].rsplit(" ", 1)[0] + "…" for t in titres]
            contenu.tableau.append([f"AT{at.numero} — {at.intitule}", f"CP{cp.numero} — {cp.intitule}",
                                    "\n".join(f"• {t}" for t in courts) or simplifier(cp.intitule),
                                    fmt_duree(minutes) if minutes else ""])
    if plan:
        for cle, lib in [("accueil", "Accueil et positionnement"), ("ecf", "Évaluations en cours de formation (ECF)"),
                         ("dossier", "Dossier professionnel"), ("productions", "Productions d'examen"),
                         ("examen", "Examen blanc"), ("bilan", "Bilan")]:
            if plan.minutes_modules.get(cle):
                contenu.tableau.append(["Modules transverses", lib, "", fmt_duree(plan.minutes_modules[cle])])
    sections.append(contenu)

    peda = Section("Modalités pédagogiques et moyens")
    peda.puces = [
        reglages.modalites_pedagogiques,
        "Objectifs formulés selon la taxonomie de Bloom ; progression en spirale (démarche brunérienne)",
        "Supports projetés à fort contraste, police agrandie (accessibilité)",
    ]
    sections.append(peda)

    evalu = Section("Modalités d'évaluation et de certification")
    if re_ and re_.epreuves:
        evalu.tableau = [["Épreuve", "Durée", "Compétences évaluées"]] + [
            [e.modalite, e.duree, ", ".join(f"CP{n}" for n in e.competences) or "Toutes (échange sur le DP)"]
            for e in re_.epreuves]
        if re_.duree_totale:
            evalu.paragraphes.append(f"Durée totale de l'épreuve pour le candidat : {re_.duree_totale}")
    elif f.modalites_evaluation:
        evalu.paragraphes.append(f.modalites_evaluation)
    evalu.puces = ["Évaluations en cours de formation (ECF) à la fin de chaque activité type",
                   "Validation totale (titre) ou partielle par blocs de compétences (CCP)"]
    sections.append(evalu)

    if f.blocs:
        blocs = Section("Blocs de compétences (validation partielle possible)")
        blocs.tableau = [["Code", "Bloc", "Compétences"]] + [
            [b.code, b.intitule, " • ".join(b.competences)] for b in f.blocs]
        sections.append(blocs)

    access = Section("Accessibilité aux personnes en situation de handicap")
    access.paragraphes.append(
        "Formation accessible : aménagements possibles du parcours et des épreuves "
        "(guide d'aménagement des sessions d'examen du ministère du Travail). "
        f"Référent handicap : {reglages.referent_handicap or A_COMPLETER}.")
    sections.append(access)

    deb = Section("Débouchés et suite de parcours")
    deb.puces = (f.emplois[:15] or [A_COMPLETER])
    if f.correspondances:
        deb.paragraphes.append("Équivalences partielles : " + " | ".join(f.correspondances))
    sections.append(deb)

    if f.statistiques:
        st = Section("Indicateurs de résultats (France Compétences)")
        st.tableau = [["Année", "Certifiés", "Dont VAE", "Insertion globale 6 mois (%)",
                       "Dans le métier 6 mois (%)", "Dans le métier 2 ans (%)"]] + [
            [s["annee"], s["certifies"], s["vae"], s["insertion_6_mois"], s["metier_6_mois"], s["metier_2_ans"]]
            for s in f.statistiques]
        st.paragraphes.append(f"Source : fiche {f.code} — francecompetences.fr (statistiques nationales).")
        sections.append(st)

    prix = Section("Tarif")
    if tarif and tarif.get("valide"):
        prix.puces = [f"{k} : {v}" for k, v in tarif.get("affichage", {}).items()]
    else:
        prix.puces = ["Sur devis — nous consulter (prise en charge OPCO, CPF, France Travail selon éligibilité)"]
    sections.append(prix)
    return intitule, sections


# ==========================================================================
# Examen simplifié
# ==========================================================================
_IRREGULIERS = {
    "transmis": "transmettre", "transmise": "transmettre", "transmises": "transmettre", "mis": "mettre",
    "mise": "mettre", "mises": "mettre", "fait": "faire", "faite": "faire", "faites": "faire",
    "pris": "prendre", "prise": "prendre", "prises": "prendre", "suivi": "suivre", "suivie": "suivre",
    "suivis": "suivre", "suivies": "suivre", "prévu": "prévoir", "prévue": "prévoir", "prévus": "prévoir",
    "prévues": "prévoir", "tenu": "tenir", "tenue": "tenir", "tenus": "tenir", "maintenu": "maintenir",
    "obtenu": "obtenir", "rendu": "rendre", "rendus": "rendre", "conduit": "conduire", "conduite": "conduire",
    "fournies": "fournir", "fourni": "fournir", "fournis": "fournir", "remplis": "remplir", "rempli": "remplir",
    "répartie": "répartir", "réparti": "répartir", "réparties": "répartir", "établi": "établir",
    "établis": "établir", "définis": "définir", "défini": "définir", "définie": "définir",
}
_ADJECTIFS = {"efficace", "pertinente", "pertinent", "pertinents", "pertinentes", "cohérentes", "cohérente",
              "cohérent", "réalistes", "réaliste", "claire", "clair", "claires", "fiables", "fiable",
              "individualisés", "adaptée", "adaptées", "adaptés", "adapté", "conforme", "conformes", "structurée"}


def _infinitif(mot: str):
    m = mot.lower().strip(";.")
    virgule = m.endswith(",")
    m = m.rstrip(",")
    res = None
    if m in _IRREGULIERS:
        res = _IRREGULIERS[m]
    elif m in _ADJECTIFS and not m.startswith("adapt"):
        return None
    else:
        for fin, rempl in (("ées", "er"), ("és", "er"), ("ée", "er"), ("é", "er")):
            if m.endswith(fin) and len(m) > len(fin) + 2:
                res = m[: -len(fin)] + rempl
                break
    return (res + ",") if (res and virgule) else res


_LOCUTIONS = ("en compte", "en œuvre", "en place", "en avant", "en évidence")
_ADVERBES_FIN = {"et fiables": "de manière fiable", "et fiable": "de manière fiable"}


def criteres_en_clair(critere: str) -> str:
    """Critère du jury → action à réaliser, en clair.

    « Les besoins humains sont anticipés et adaptés… » → « Anticiper et adapter les besoins humains… ».
    Si la phrase ne suit pas ce modèle, elle est gardée telle quelle (aucune invention).
    """
    c = critere.strip().rstrip(".")
    m = re.match(r"^(Les|Le|La|L’|Une|Un|Des)\s*(.+?)\s+(?:sont|est)\s+(.+)$", c)
    if not m or re.search(r"\b(font|fait|permet|répond|tient|respecte|correspond|prennent|valorisent)\b", m.group(2)):
        return c
    article = {"Les": "les", "Le": "le", "La": "la", "L’": "l’", "Un": "un", "Une": "une", "Des": "des"}[m.group(1)]
    sujet, attribut = m.group(2).strip(), m.group(3)
    # seconde proposition : « … et les difficultés sont remontées à la hiérarchie »
    second = ""
    m2 = re.match(r"^(.*?)\s+et\s+((?:les|le|la|l’|des)\s*.+?\s+(?:sont|est)\s+.+)$", attribut)
    if m2:
        attribut = m2.group(1)
        conv = criteres_en_clair(m2.group(2)[0].upper() + m2.group(2)[1:])
        if conv != m2.group(2)[0].upper() + m2.group(2)[1:]:
            second = " et " + conv[0].lower() + conv[1:]
        else:
            attribut = m2.group(1) + " et " + m2.group(2)
    mots = attribut.split()
    verbes, i = [], 0
    while i < len(mots):
        inf = _infinitif(mots[i])
        if not inf:
            break
        i += 1
        suite = " ".join(mots[i:i + 2])
        if suite in _LOCUTIONS:
            inf += " " + suite
            i += 2
        verbes.append(inf)
        if i < len(mots) and mots[i] == "et" and i + 1 < len(mots) and _infinitif(mots[i + 1]):
            i += 1
        elif not mots[i - 1].endswith(","):
            break
    if not verbes:
        return c
    verbes = [v.rstrip(",") for v in verbes]
    tete = verbes[0] if len(verbes) == 1 else ", ".join(verbes[:-1]) + " et " + verbes[-1]
    reste = " ".join(mots[i:])
    for fin, rempl in _ADVERBES_FIN.items():
        if reste.endswith(fin):
            reste = reste[: -len(fin)].rstrip() + " " + rempl
    liaison = "" if article.endswith("’") else " "
    return (f"{tete[0].upper() + tete[1:]} {article}{liaison}{sujet} {reste}".strip() + second).replace("  ", " ")


def construire_examen(reac: Reac, re_: Optional[ReferentielEvaluation],
                      fiche: Optional[FicheFranceCompetences]) -> dict:
    """Partie 1 : tableau des épreuves. Partie 2 : attendus par compétence, en clair."""
    partie1 = [["Épreuve", "Durée", "Compétences évaluées", "Comment ça se passe (en bref)"]]
    if re_ and re_.epreuves:
        for e in re_.epreuves:
            comps = "\n".join(f"CP{n} — {simplifier(reac.competence(n).intitule)}" for n in e.competences
                              if reac.competence(n)) or "Échange avec le jury (dossier professionnel)"
            partie1.append([e.modalite, e.duree, comps, resume_epreuve(e.modalite, e.detail)])
    elif fiche and fiche.blocs:
        for b in fiche.blocs:
            partie1.append([f"Bloc {b.code}", b.evaluation, "\n".join(b.competences), ""])

    partie2 = []
    prod_par_cp = {}
    for p in (re_.productions if re_ else []):
        prod_par_cp[normaliser(p.competence)[:30]] = p
    for cp in reac.competences:
        bloc = {"cp": f"CP{cp.numero} — {cp.intitule}", "at": cp.at_numero,
                "epreuves": [e.modalite for e in (re_.epreuves if re_ else []) if cp.numero in e.competences],
                "attendus": [criteres_en_clair(c) for c in cp.criteres], "production": None}
        cle = normaliser(cp.intitule)[:30]
        p = prod_par_cp.get(cle) or next((v for k, v in prod_par_cp.items()
                                           if k[:18] == cle[:18]), None)
        if p:
            bloc["production"] = {"pages": p.pages, "themes": [t for t, _ in p.themes]}
        partie2.append(bloc)
    consignes = []
    if re_:
        consignes = re_.documents + re_.diaporamas + re_.periode_entreprise[:1]
    return {"partie1": partie1, "partie2": partie2, "consignes": consignes,
            "duree_totale": re_.duree_totale if re_ else ""}


def resume_epreuve(modalite: str, detail: str) -> str:
    n = normaliser(modalite)
    d = normaliser(detail)
    if n.startswith("mise en situation"):
        return ("Étude de cas écrite sur ordinateur (traitement de texte + tableur), à partir d'un dossier "
                "papier et de modèles numériques. Travaux imprimés et corrigés par le jury."
                if "etude de cas" in d else "Mise en situation professionnelle devant le jury.")
    if n.startswith("entretien technique"):
        return "Préparation sans jury, puis présentation des travaux et échange avec le jury (cas pratiques possibles)."
    if n.startswith("questionnement"):
        return ("Présentation des documents et diaporamas préparés AVANT l'examen, puis questions du jury "
                "(simulations possibles).")
    if n.startswith("entretien final"):
        return "Échange avec le jury, y compris sur le dossier professionnel."
    if n.startswith("questionnaire"):
        return "Questionnaire écrit."
    return ""
