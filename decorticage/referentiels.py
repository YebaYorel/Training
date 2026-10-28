"""Analyse des référentiels : REAC, RE/RC, fiche France Compétences (RNCP ou RS).

Les REAC et RE des titres professionnels du ministère du Travail suivent une
structure normalisée (« FICHE ACTIVITÉ TYPE N° », « FICHE COMPÉTENCE
PROFESSIONNELLE N° », « Critères de performance », « 1 - Savoir-faire
techniques »…). Le parseur s'appuie sur ces repères : il fonctionne pour
tous les titres professionnels qui respectent ce gabarit, pas seulement MEM.

Les Activités-types et Compétences sont reprises MOT POUR MOT : elles ne
sont jamais reformulées (elles « ne bougent pas »).
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import asdict, dataclass, field
from typing import Optional


# ==========================================================================
# Modèle de données
# ==========================================================================
@dataclass
class Competence:
    numero: int
    intitule: str
    at_numero: int = 0
    description: list[str] = field(default_factory=list)   # étapes du processus
    contexte: str = ""
    criteres: list[str] = field(default_factory=list)
    sf_techniques: list[str] = field(default_factory=list)
    sf_organisationnels: list[str] = field(default_factory=list)
    sf_relationnels: list[str] = field(default_factory=list)
    savoirs: list[str] = field(default_factory=list)

    def volume(self) -> int:
        return (len(self.sf_techniques) + len(self.sf_organisationnels)
                + len(self.sf_relationnels) + len(self.savoirs) + len(self.criteres))


@dataclass
class ActiviteType:
    numero: int
    intitule: str
    description: str = ""
    competences: list[int] = field(default_factory=list)


@dataclass
class Reac:
    intitule: str = ""
    sigle: str = ""
    niveau: str = ""
    code_titre: str = ""
    millesime: str = ""
    date_validation: str = ""
    activites: list[ActiviteType] = field(default_factory=list)
    competences: list[Competence] = field(default_factory=list)
    transversales: list[str] = field(default_factory=list)
    avertissements: list[str] = field(default_factory=list)

    def competence(self, numero: int) -> Optional[Competence]:
        return next((c for c in self.competences if c.numero == numero), None)

    def activite(self, numero: int) -> Optional[ActiviteType]:
        return next((a for a in self.activites if a.numero == numero), None)


@dataclass
class Epreuve:
    modalite: str
    duree: str
    minutes: int
    competences: list[int] = field(default_factory=list)
    detail: str = ""


@dataclass
class PartieProduction:
    """Une partie d'un document à produire avant l'examen (ex. dossier AT3)."""
    competence: str
    pages: str
    themes: list[tuple[str, list[str]]] = field(default_factory=list)


@dataclass
class ReferentielEvaluation:
    epreuves: list[Epreuve] = field(default_factory=list)
    duree_totale: str = ""
    periode_entreprise: list[str] = field(default_factory=list)
    productions: list[PartieProduction] = field(default_factory=list)
    documents: list[str] = field(default_factory=list)     # consignes de forme
    diaporamas: list[str] = field(default_factory=list)
    avertissements: list[str] = field(default_factory=list)


@dataclass
class Bloc:
    code: str
    intitule: str
    competences: list[str] = field(default_factory=list)
    evaluation: str = ""


@dataclass
class FicheFranceCompetences:
    code: str = ""                 # RNCP41853 ou RS1234
    type_fiche: str = ""           # RNCP ou RS
    intitule: str = ""
    etat: str = ""
    niveau: str = ""
    nsf: list[str] = field(default_factory=list)
    formacodes: list[str] = field(default_factory=list)
    rome: list[str] = field(default_factory=list)
    certificateur: str = ""
    date_debut: str = ""
    date_echeance: str = ""
    objectifs: str = ""
    activites_visees: str = ""
    competences_attestees: str = ""
    modalites_evaluation: str = ""
    blocs: list[Bloc] = field(default_factory=list)
    secteurs: list[str] = field(default_factory=list)
    emplois: list[str] = field(default_factory=list)
    prerequis_entree: str = ""
    prerequis_validation: str = ""
    voies_acces: list[tuple[str, bool]] = field(default_factory=list)
    correspondances: list[str] = field(default_factory=list)
    statistiques: list[dict] = field(default_factory=list)
    duree_formation: str = ""      # rarement indiquée sur la fiche
    avertissements: list[str] = field(default_factory=list)


def en_dict(obj) -> dict:
    return asdict(obj)


# ==========================================================================
# Outils texte
# ==========================================================================
_LIAISONS_FIN = re.compile(
    r"(,|;|:|\(|\bde|\bdu|\bdes|\bet|\bla|\ble|\bles|\bà|\bau|\baux|\ben|\bun|\bune|\bpar|"
    r"\bpour|\bsur|\bavec|\bd’|\bl’|\bd'|\bl'|\bou|\bdans|\bson|\bsa|\bses|\bleur|\bleurs|-)$",
    re.IGNORECASE,
)


def normaliser(s: str) -> str:
    """Minuscules, sans accents, espaces simplifiés (pour comparer)."""
    s = unicodedata.normalize("NFKD", s.replace("’", "'")).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s.lower()).strip()


def _parentheses_ouvertes(s: str) -> bool:
    return s.count("(") > s.count(")")


def joindre_items(lignes: list[str]) -> list[str]:
    """Recolle les lignes coupées par la mise en page en items complets.

    Un item d'une liste REAC commence par une majuscule ; une ligne qui
    commence par une minuscule, ou qui suit une ligne finissant par un mot
    de liaison ou une parenthèse ouverte, est la suite de l'item précédent.
    """
    items: list[str] = []
    for brute in lignes:
        ligne = brute.strip()
        if not ligne:
            continue
        ligne = re.sub(r"^-\s+", "", ligne)
        suite = bool(items) and (
            ligne[0].islower()
            or ligne[0] in "(…)."
            or _LIAISONS_FIN.search(items[-1])
            or _parentheses_ouvertes(items[-1])
        )
        if suite:
            items[-1] = f"{items[-1]} {ligne}"
        else:
            items.append(ligne)
    return [re.sub(r"\s+", " ", i).strip().rstrip(".").strip() for i in items]


def decouper_phrases(lignes: list[str]) -> list[str]:
    """Découpe une description en étapes (phrases) du processus."""
    blocs: list[str] = []
    for brute in lignes:
        ligne = brute.strip()
        if not ligne:
            continue
        if blocs and (ligne[0].islower() or _LIAISONS_FIN.search(blocs[-1])
                      or _parentheses_ouvertes(blocs[-1])):
            blocs[-1] += " " + ligne
        else:
            blocs.append(ligne)
    phrases: list[str] = []
    for bloc in blocs:
        for p in re.split(r"(?<=[.!?])\s+(?=[A-ZÀÂÉÈÊÎÔÛÇ])", bloc):
            p = p.strip().rstrip(".").strip()
            if len(p) > 3:
                phrases.append(p)
    return phrases


def _section(texte: str, debut: str, fins: list[str]) -> str:
    """Texte entre le motif `debut` et le premier des motifs `fins`."""
    m = re.search(debut, texte, re.IGNORECASE | re.MULTILINE)
    if not m:
        return ""
    reste = texte[m.end():]
    positions = [mm.start() for f in fins if (mm := re.search(f, reste, re.IGNORECASE | re.MULTILINE))]
    return reste[: min(positions)] if positions else reste


# ==========================================================================
# REAC
# ==========================================================================
_RE_FICHE_AT = re.compile(r"^FICHE ACTIVIT[ÉE] TYPE N°\s*(\d+)\s*$", re.MULTILINE)
_RE_FICHE_CP = re.compile(r"^FICHE COMP[ÉE]TENCE PROFESSIONNELLE N°\s*(\d+)\s*$", re.MULTILINE)
_RE_FIN_CP = re.compile(
    r"^(FICHE DES COMP[ÉE]TENCES TRANSVERSALES|FICHE COMP[ÉE]TENCES TRANSVERSALES|Glossaire)",
    re.MULTILINE | re.IGNORECASE,
)
_SOUS_SECTIONS = [
    ("sf_techniques", r"^\s*1\s*[-–]\s*Savoir-faire techniques"),
    ("sf_organisationnels", r"^\s*2\s*[-–]\s*Savoir-faire organisationnels"),
    ("sf_relationnels", r"^\s*3\s*[-–]\s*Savoir-faire relationnels"),
    ("savoirs", r"^\s*4\s*[-–]\s*Savoirs"),
]


def _titre_multiligne(lignes: list[str], arret: str) -> tuple[str, list[str]]:
    titre = []
    i = 0
    while i < len(lignes) and not re.match(arret, lignes[i], re.IGNORECASE):
        if lignes[i].strip():
            titre.append(lignes[i].strip())
        i += 1
    return re.sub(r"\s+", " ", " ".join(titre)).strip(), lignes[i:]


def _parser_competence(numero: int, bloc: str) -> Competence:
    lignes = bloc.splitlines()
    intitule, reste = _titre_multiligne(lignes, r"^Description de la comp")
    texte = "\n".join(reste)
    cp = Competence(numero=numero, intitule=intitule)

    desc = _section(texte, r"^Description de la comp.*$", [r"^Contexte\(s\) professionnel"])
    cp.description = decouper_phrases(desc.splitlines())
    ctx = _section(texte, r"^Contexte\(s\) professionnel.*$", [r"^Crit[èe]res de performance"])
    cp.contexte = re.sub(r"\s+", " ", ctx).strip()
    crit = _section(texte, r"^Crit[èe]res de performance\s*$", [r"^Savoir-faire techniques, savoir", r"^\s*1\s*[-–]"])
    cp.criteres = joindre_items(crit.splitlines())

    for i, (attr, motif) in enumerate(_SOUS_SECTIONS):
        fins = [m for _, m in _SOUS_SECTIONS[i + 1:]] + [r"^FICHE ", r"\Z"]
        contenu = _section(texte, motif + r".*$", fins)
        setattr(cp, attr, joindre_items(contenu.splitlines()))
    return cp


def _infos_cartouche(texte: str, reac: Reac) -> None:
    m = re.search(r"\b([A-Z]{2,6})\s+(?:REAC|RE|RC)\s+(TP-\d{5})\s+(\d{1,2})\s+(\d{2}/\d{2}/\d{4})", texte)
    if m:
        reac.sigle, reac.code_titre, reac.millesime, reac.date_validation = m.groups()
    m = re.search(r"DU TITRE PROFESSIONNEL\s*\n\s*(.+?)\s*\n", texte)
    if m:
        reac.intitule = m.group(1).strip()
    m = re.search(r"\bNiveau\s+(\d)\b", texte)
    if m:
        reac.niveau = m.group(1)


def analyser_reac(texte_brut: str, texte_avec_cartouche: Optional[str] = None) -> Reac:
    """Analyse le texte d'un REAC et retourne sa structure complète."""
    reac = Reac()
    _infos_cartouche(texte_avec_cartouche or texte_brut, reac)

    # --- Activités types
    positions_at = list(_RE_FICHE_AT.finditer(texte_brut))
    premiere_cp = _RE_FICHE_CP.search(texte_brut)
    for idx, m in enumerate(positions_at):
        fin = positions_at[idx + 1].start() if idx + 1 < len(positions_at) else (
            premiere_cp.start() if premiere_cp else len(texte_brut))
        bloc = texte_brut[m.end():fin]
        intitule, _ = _titre_multiligne(bloc.splitlines(), r"^D[ée]finition")
        at = ActiviteType(numero=int(m.group(1)), intitule=intitule)
        at.description = re.sub(r"\s+", " ", _section(
            bloc, r"^D[ée]finition.*$", [r"^R[ée]glementation", r"^Liste des comp"])).strip()
        at._liste_cp = joindre_items(_section(  # type: ignore[attr-defined]
            bloc, r"^Liste des comp[ée]tences professionnelles.*$", [r"^Comp[ée]tences transversales"]).splitlines())
        reac.activites.append(at)

    # --- Compétences professionnelles
    positions_cp = list(_RE_FICHE_CP.finditer(texte_brut))
    fin_globale = _RE_FIN_CP.search(texte_brut, positions_cp[-1].end()) if positions_cp else None
    for idx, m in enumerate(positions_cp):
        fin = positions_cp[idx + 1].start() if idx + 1 < len(positions_cp) else (
            fin_globale.start() if fin_globale else len(texte_brut))
        reac.competences.append(_parser_competence(int(m.group(1)), texte_brut[m.end():fin]))

    # --- Rattachement CP → AT (par l'intitulé exact listé dans chaque fiche AT)
    for at in reac.activites:
        for libelle in getattr(at, "_liste_cp", []):
            cle = normaliser(libelle)[:45]
            for cp in reac.competences:
                if normaliser(cp.intitule)[:45] == cle:
                    cp.at_numero = at.numero
                    if cp.numero not in at.competences:
                        at.competences.append(cp.numero)
        if hasattr(at, "_liste_cp"):
            del at._liste_cp  # type: ignore[attr-defined]

    # --- Compétences transversales
    trans = _section(texte_brut, r"^Comp[ée]tences transversales de l.emploi\s*$", [r"^Niveau et/ou", r"^FICHE"])
    reac.transversales = joindre_items(trans.splitlines())

    # --- Contrôles de cohérence (signalés, jamais inventés)
    if not reac.activites:
        reac.avertissements.append("Aucune fiche « Activité type » trouvée : ce document est-il bien un REAC ?")
    if not reac.competences:
        reac.avertissements.append("Aucune fiche « Compétence professionnelle » trouvée.")
    for cp in reac.competences:
        if not cp.at_numero:
            reac.avertissements.append(f"CP{cp.numero} non rattachée à une activité type : vérifier.")
        if not cp.criteres:
            reac.avertissements.append(f"CP{cp.numero} : critères de performance introuvables.")
    return reac


# ==========================================================================
# Référentiel d'évaluation (RE) / de certification (RC)
# ==========================================================================
_MODALITES = [
    "Mise en situation professionnelle",
    "Présentation d'un projet réalisé en amont de la session",
    "Questionnement à partir de production(s)",
    "Questionnaire professionnel",
    "Entretien technique",
    "Entretien final",
    "Entretien technique final",
]
_RE_DUREE = re.compile(r"(\d{1,2})\s*h\s*(\d{2})\s*min")


def _minutes(s: str) -> int:
    m = _RE_DUREE.search(s)
    return int(m.group(1)) * 60 + int(m.group(2)) if m else 0


def analyser_re(texte: str, reac: Optional[Reac] = None) -> ReferentielEvaluation:
    """Analyse un RE (référentiel d'évaluation) ou RC (référentiel de certification)."""
    re_ = ReferentielEvaluation()
    norm = texte.replace("'", "’")

    tableau = _section(norm, r"^\s*3\.1\.?\s*Modalités d’évaluation des compétences et organisation de l’épreuve",
                       [r"^Informations complémentaires", r"^3\.2\."])
    if not tableau:
        tableau = _section(norm, r"^Modalités d’évaluation des compétences et organisation de l’épreuve\s*$",
                           [r"^Informations complémentaires", r"^3\.2\."])
    if not tableau:
        re_.avertissements.append("Tableau des modalités d'évaluation introuvable.")
    # Repère chaque modalité + durée dans l'ordre du tableau.
    motif_modalite = re.compile(
        r"^\s*(?:-\s*)?(Mise en situation|Entretien technique|Questionnaire|Questionnement à partir|"
        r"Entretien final|Présentation d’un projet)", re.MULTILINE)
    debuts = list(motif_modalite.finditer(tableau))
    titres_cp = [(cp.numero, normaliser(cp.intitule)[:40]) for cp in (reac.competences if reac else [])]
    for i, m in enumerate(debuts):
        morceau = tableau[m.start(): debuts[i + 1].start() if i + 1 < len(debuts) else len(tableau)]
        tete = normaliser(morceau.lstrip(" -"))
        nom = next((x for x in _MODALITES if tete.startswith(normaliser(x)[:18])), m.group(1))
        duree_m = _RE_DUREE.search(morceau)
        if "sans objet" in normaliser(morceau[:200]) and not duree_m:
            continue
        ep = Epreuve(modalite=nom, duree=duree_m.group(0) if duree_m else "",
                     minutes=_minutes(morceau))
        morceau_norm = normaliser(morceau)
        ep.competences = [n for n, t in titres_cp if t and t in morceau_norm]
        ep.detail = re.sub(r"\s+", " ", morceau).strip()[:1500]
        re_.epreuves.append(ep)
    m = re.search(r"Durée totale de l’épreuve pour le candidat\s*:?\s*(\d{1,2}\s*h\s*\d{2}\s*min)", norm)
    if m:
        re_.duree_totale = m.group(1)

    per = _section(norm, r"^Période en entreprise\s*:?\s*$", [r"^Production\s*:?\s*$", r"^La période en entreprise est incluse"])
    re_.periode_entreprise = [l.lstrip("- ").strip() for l in joindre_items(per.splitlines()) if l]

    # Productions : « Cette partie … se réfère à la compétence « X » » + thèmes numérotés
    motif_partie = re.compile(
        r"Cette partie comporte (entre \d+ et \d+ pages)\.\s*Elle se réfère à la compétence\s*«\s*(.+?)\s*»",
        re.DOTALL)
    vus = set()
    parties = list(motif_partie.finditer(norm))
    for i, m in enumerate(parties):
        comp = re.sub(r"\s+", " ", m.group(2)).strip()
        if normaliser(comp) in vus:
            continue  # le RE répète parfois les consignes en annexe
        vus.add(normaliser(comp))
        fin = parties[i + 1].start() if i + 1 < len(parties) else len(norm)
        corps = norm[m.end():fin]
        coupe = re.search(r"^(Diaporama relatif|Document relatif|Précisions pour|\d\.\d\.)", corps, re.MULTILINE)
        if coupe:
            corps = corps[:coupe.start()]
        partie = PartieProduction(competence=comp, pages=m.group(1))
        courant = None
        for ligne in corps.splitlines():
            ligne = ligne.strip()
            t = re.match(r"^(\d)\.\s+(.+?)\s*:?\s*$", ligne)
            if t:
                courant = (t.group(2).rstrip(" :"), [])
                partie.themes.append(courant)
            elif ligne.startswith("- ") and courant is not None:
                courant[1].append(ligne[2:].strip())
            elif courant is not None and courant[1] and ligne and ligne[0].islower():
                courant[1][-1] += " " + ligne
        re_.productions.append(partie)

    for m in re.finditer(r"Ce document comporte (entre \d+ et \d+ pages)[^.]*\.", norm):
        avant = norm[max(0, m.start() - 300):m.start()]
        act = re.findall(r"Document relatif à l’activité\s*«\s*(.+?)\s*»", avant, re.DOTALL)
        lib = re.sub(r"\s+", " ", act[-1]) if act else "Document"
        ligne = f"{lib} : {m.group(1)}"
        if ligne not in re_.documents:
            re_.documents.append(ligne)
    for m in re.finditer(r"diaporama de (\d+ à \d+ diapositives)", norm):
        avant = norm[max(0, m.start() - 400):m.start()]
        act = re.findall(r"Diaporama relatif à l’activité\s*«\s*(.+?)\s*»", avant, re.DOTALL)
        lib = re.sub(r"\s+", " ", act[-1]) if act else "Diaporama"
        ligne = f"{lib} : {m.group(1)}"
        if ligne not in re_.diaporamas:
            re_.diaporamas.append(ligne)
    m = re.search(r"police (Arial \d+, interligne [\d,]+)", norm)
    if m:
        re_.documents.append(f"Mise en forme imposée : {m.group(1)}")
    return re_


# ==========================================================================
# Fiche France Compétences (RNCP ou RS)
# ==========================================================================
_TITRES_FC = [
    "L'essentiel", "Certificateur(s)", "Résumé de la certification", "Objectifs et contexte de la certification",
    "Activités visées", "Compétences attestées", "Modalités d'évaluation", "Blocs de compétences",
    "Description des modalités d'acquisition", "Secteur d’activité et type d’emploi", "Secteurs d’activités",
    "Type d'emplois accessibles", "Code(s) ROME", "Références juridiques", "Voie d’accès",
    "Le cas échant, prérequis à l’entrée en formation", "Le cas échéant, prérequis à l’entrée en formation",
    "Le cas échant, prérequis à la validation de la certification",
    "Le cas échéant, prérequis à la validation de la certification", "Pré-requis disctincts",
    "Voie d’accès à", "Liens avec d’autres certifications", "Base légale", "Statistiques",
    "Pour plus d’informations", "Lien internet vers le descriptif",
]


def _entre(texte: str, debut: str, fins: list[str]) -> str:
    i = texte.find(debut)
    if i < 0:
        return ""
    reste = texte[i + len(debut):]
    positions = [p for f in fins if (p := reste.find(f)) > 0]
    return (reste[:min(positions)] if positions else reste).strip(" :\n")


def analyser_fiche_fc(texte: str) -> FicheFranceCompetences:
    """Analyse une fiche RNCP ou RS téléchargée depuis francecompetences.fr."""
    t = texte.replace("'", "’").replace("’", "’")
    f = FicheFranceCompetences()
    m = re.search(r"\b((RNCP|RS)\s?\d{3,6})\b", t)
    if m:
        f.code, f.type_fiche = m.group(1).replace(" ", ""), m.group(2)
        apres = t[m.end():m.end() + 30]
        e = re.match(r"\s*(Active|Inactive)", apres)
        f.etat = e.group(1) if e else ""
    m = re.search(r"Répertoire (?:national des certifications professionnelles|spécifique)\s+(.+?)\n", t)
    if m:
        f.intitule = m.group(1).strip()
    m = re.search(r"\b(Niveau \d)\b", t)
    if m:
        f.niveau = m.group(1)
    zone = _entre(t, "Code(s) NSF", ["Date de début"])
    f.nsf = re.findall(r"(\d{3}[a-z]\s*:\s*[^\n]+)", zone)
    f.formacodes = [x.strip() for x in re.findall(r"(?:^|\s)(\d{5}\s*:\s*[^\n]+)", zone)]
    m = re.search(r"(\d{2}-\d{2}-\d{4})\s*\n?\s*parcours certifiants", t) or \
        re.search(r"parcours certifiants\s*(\d{2}-\d{2}-\d{4})", t)
    if m:
        f.date_debut = m.group(1)
    m = re.search(r"Date d’échéance\s*\n?\s*(?:de l’enregistrement\s*)?(\d{2}-\d{2}-\d{4})", t)
    if m:
        f.date_echeance = m.group(1)
    bloc_cert = _entre(t, "Certificateur(s)", ["Résumé de la certification", "Objectifs et contexte"])
    morceaux = []
    for ligne in bloc_cert.splitlines():
        ligne = re.sub(r"\b\d{5,}\b|\b\d\b|(?<!\w)-(?!\w)", " ", ligne)
        ligne = re.sub(r"\b(Nom légal|Siret|Nom|Site|commercial|internet)\b", " ", ligne).strip()
        if ligne:
            morceaux.append(ligne)
    f.certificateur = re.sub(r"\s+", " ", " ".join(morceaux)).replace("L’ ", "L’").replace("L' ", "L'").strip()

    f.objectifs = _entre(t, "Objectifs et contexte de la certification", ["Activités visées"])
    f.activites_visees = _entre(t, "Activités visées", ["Résumé de la certification", "Compétences attestées"])
    f.activites_visees = f.activites_visees.replace("Résumé de la certification", "").strip()
    f.objectifs = re.sub(r"\s*\n\s*", " ", f.objectifs).strip()
    f.competences_attestees = _entre(t, "Compétences attestées", ["Modalités d’évaluation"])
    f.modalites_evaluation = _entre(t, "Modalités d’évaluation :", ["Blocs de compétences", f"{f.code}BC01"])

    # Blocs de compétences
    blocs = list(re.finditer(rf"^({re.escape(f.code)}BC\d{{2}})\s*-\s*(.+?)$", t, re.MULTILINE)) if f.code else []
    vus = set()
    for i, m in enumerate(blocs):
        code = m.group(1)
        if code in vus:
            continue
        fin = blocs[i + 1].start() if i + 1 < len(blocs) else t.find("Description des modalités d’acquisition")
        corps = t[m.end(): fin if fin > m.end() else len(t)]
        intitule = m.group(2).strip()
        suite = corps.splitlines()[1] if len(corps.splitlines()) > 1 else ""
        if suite and suite[0].islower():
            intitule += " " + suite.strip()
        comps = [re.sub(r"\s+", " ", c).strip() for c in re.findall(r"^-\s*(.+?)$", corps, re.MULTILINE)]
        comps = [c for c in comps if not c.lower().startswith(("pendant", "d’un", "d'un"))]
        if len(comps) < 1:
            continue
        vus.add(code)
        duree = re.search(r"Durée totale de l’épreuve pour le candidat\s*:\s*(\d{2} h \d{2} min)", corps)
        f.blocs.append(Bloc(code=code, intitule=intitule, competences=comps,
                            evaluation=duree.group(1) if duree else ""))
    # Compléter les compétences des blocs depuis « Compétences attestées » (plus propre)
    _completer_blocs(f)

    f.secteurs = [s.lstrip("- ").strip() for s in _entre(t, "Secteurs d’activités :", ["Type d’emplois", "Type d'emplois"]).splitlines() if s.strip().startswith("-")]
    f.emplois = [s.lstrip("- ").strip() for s in _entre(t, "accessibles :", ["Code(s) ROME"]).splitlines() if s.strip().startswith("-")]
    f.rome = re.findall(r"([A-Z]\d{4}\s*-\s*.+)", t)
    f.rome = list(dict.fromkeys(r.strip() for r in f.rome))
    pre = re.search(r"prérequis à l’entrée en formation\s*:\s*(.*?)\n\s*Le cas éch[ée]?ant, prérequis à la validation", t, re.DOTALL)
    f.prerequis_entree = re.sub(r"\s+", " ", pre.group(1)).strip() if pre else ""
    val = re.search(r"prérequis à la validation de la certification\s*:\s*(.*?)(Pré-requis disctincts|Pré-requis distincts|Voie d’accès à)", t, re.DOTALL)
    if val:
        txt = re.sub(r"^[A-Z]\d{4}\s*-.*$", "", val.group(1), flags=re.MULTILINE)
        txt = txt.replace("Voie d’accès", "")
        f.prerequis_validation = re.sub(r"\s+", " ", txt).strip()

    curseur = t.find("Voie d’accès à")
    if curseur >= 0:
        for voie, cle in [
            ("Après un parcours de formation sous statut d’élève ou d’étudiant", "Après un parcours"),
            ("En contrat d’apprentissage", "En contrat"),
            ("Après un parcours de formation continue", "Après un parcours"),
            ("En contrat de professionnalisation", "En contrat de"),
            ("Par candidature individuelle", "Par candidature"),
            ("Par expérience (VAE)", "Par expérience"),
        ]:
            i = t.find(cle, curseur)
            if i < 0:
                continue
            mx = re.search(r"\bX\b(\s*-\s*-)?", t[i:i + 250])
            if mx:
                # « X - - » : case « Non » cochée et ni jury ni date → voie fermée
                f.voies_acces.append((voie, not bool(mx.group(1))))
            curseur = i + len(cle)

    zone = _entre(t, "Liens avec d’autres certifications", ["Base légale"])
    noms = {}
    for code, nom in re.findall(r"(RNCP\d{5})\s+-\s+((?:BTS|TP|BUT|BP|CAP|Licence|Titre|Bac)[^\n]*?)(?=\s+RNCP\d|\n|$)", zone):
        noms.setdefault(code, nom.strip())
    propre = f.code
    blocs_ext: dict[str, list[str]] = {}
    for code_bc in re.findall(r"(RNCP\d{5})(BC\d{2})", zone):
        if code_bc[0] != propre:
            blocs_ext.setdefault(code_bc[0], [])
            if code_bc[1] not in blocs_ext[code_bc[0]]:
                blocs_ext[code_bc[0]].append(code_bc[1])
    for code, bcs in blocs_ext.items():
        nom = noms.get(code, "")
        f.correspondances.append(
            f"{code}{(' – ' + nom) if nom else ''} : correspondance partielle (blocs {', '.join(sorted(bcs))}) "
            "— intitulé complet à vérifier sur la fiche")

    stats = _entre(t, "Statistiques :", ["Lien internet", "Pour plus"])
    for mm in re.finditer(r"^(20\d{2})\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$", stats, re.MULTILINE):
        f.statistiques.append({
            "annee": mm.group(1), "certifies": mm.group(2), "vae": mm.group(3),
            "insertion_6_mois": mm.group(4), "metier_6_mois": mm.group(5), "metier_2_ans": mm.group(6)})
    for mm in re.finditer(r"^(20\d{2})\s+(\d{4,5})(\d)\s+(\d+)\s+(\d+)\s+(\d+)\s*$", stats, re.MULTILINE):
        # ligne collée par le PDF (ex. « 2022 15334 73 62 74 ») : signalée, non devinée
        f.avertissements.append(
            f"Statistiques {mm.group(1)} : colonnes collées dans le PDF (« {mm.group(0).strip()} ») — "
            "vérifier sur francecompetences.fr avant publication.")

    dur = re.search(r"Durée (?:totale )?(?:de la )?formation\s*:?\s*([\d\s]+heures?)", t, re.IGNORECASE)
    if dur:
        f.duree_formation = dur.group(1).strip()
    else:
        f.avertissements.append(
            "La fiche France Compétences n'indique pas de durée de formation : la durée en centre "
            "doit être fixée par la convention avec l'organisme (ou par vous).")
    if not f.prerequis_entree:
        f.avertissements.append(
            "Aucun prérequis d'entrée indiqué sur la fiche : à définir par l'organisme "
            "(information obligatoire du programme, Qualiopi indicateur 1).")
    return f


def _completer_blocs(f: FicheFranceCompetences) -> None:
    """Rapproche chaque bloc de la liste « Compétences attestées » (plus fiable)."""
    if not f.competences_attestees:
        return
    groupes: list[tuple[str, list[str]]] = []
    for ligne in f.competences_attestees.splitlines():
        ligne = ligne.strip()
        if not ligne:
            continue
        if ligne.startswith("-"):
            if groupes:
                groupes[-1][1].append(ligne.lstrip("- ").rstrip(".").strip())
        elif groupes and groupes[-1][1] and ligne[0].islower():
            groupes[-1][1][-1] += " " + ligne
        else:
            groupes.append((ligne, []))
    for bloc in f.blocs:
        for titre, comps in groupes:
            if normaliser(titre)[:35] == normaliser(bloc.intitule)[:35] and comps:
                bloc.competences = comps
                bloc.intitule = titre
    if not f.blocs:
        for i, (titre, comps) in enumerate(groupes, 1):
            f.blocs.append(Bloc(code=f"{f.code}BC{i:02d}", intitule=titre, competences=comps))


# ==========================================================================
# Détection automatique du type de document
# ==========================================================================
def detecter_type(texte: str) -> str:
    """Retourne 'REAC', 'RE', 'FICHE' ou 'INCONNU'."""
    debut = normaliser(texte[:3000])
    if "referentiel emploi activites competences" in debut or "fiche competence professionnelle" in normaliser(texte[:60000]):
        if "referentiel d'evaluation" not in debut and "referentiel de certification" not in debut:
            return "REAC"
    if "referentiel d'evaluation" in debut or "referentiel de certification" in debut:
        return "RE"
    if "francecompetences" in normaliser(texte) or "code de la fiche" in debut:
        return "FICHE"
    return "INCONNU"
