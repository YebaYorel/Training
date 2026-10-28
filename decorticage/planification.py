"""Planification : de la durée totale au déroulé jour par jour, heure par heure.

Étapes :
1. répartition des heures entre modules transverses (accueil, ECF, dossier
   professionnel, examen blanc, bilan) et compétences (pondération REAC) ;
2. découpage de chaque compétence en séances et objectifs (module pédagogie) ;
3. génération des créneaux réels (jours de centre, horaires, pauses, jours
   fériés de La Réunion, fermetures, rythme d'alternance) ;
4. placement séquentiel des objectifs dans les créneaux.

Jours fériés : Code du travail art. L3133-1 + 20 décembre (abolition de
l'esclavage à La Réunion, décret n° 83-1003 du 23 novembre 1983).
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from typing import Optional

from .pedagogie import (NIVEAUX_BLOOM, PAS, Objectif, Seance, decouper_competence, mode_bruner,
                        poids_competences, repartir)
from .referentiels import Reac, ReferentielEvaluation

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre",
        "octobre", "novembre", "décembre"]
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


# ==========================================================================
# Calendrier
# ==========================================================================
def paques(annee: int) -> dt.date:
    """Dimanche de Pâques (algorithme de Meeus/Jones/Butcher)."""
    a, b, c = annee % 19, annee // 100, annee % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    mois = (h + l_ - 7 * m + 114) // 31
    jour = ((h + l_ - 7 * m + 114) % 31) + 1
    return dt.date(annee, mois, jour)


def jours_feries_reunion(annee: int) -> dict[dt.date, str]:
    p = paques(annee)
    return {
        dt.date(annee, 1, 1): "Jour de l'An",
        p + dt.timedelta(days=1): "Lundi de Pâques",
        dt.date(annee, 5, 1): "Fête du Travail",
        dt.date(annee, 5, 8): "Victoire 1945",
        p + dt.timedelta(days=39): "Ascension",
        p + dt.timedelta(days=50): "Lundi de Pentecôte",
        dt.date(annee, 7, 14): "Fête nationale",
        dt.date(annee, 8, 15): "Assomption",
        dt.date(annee, 11, 1): "Toussaint",
        dt.date(annee, 11, 11): "Armistice 1918",
        dt.date(annee, 12, 20): "Fête de l'abolition de l'esclavage (La Réunion)",
        dt.date(annee, 12, 25): "Noël",
    }


def _hm(s: str) -> int:
    h, m = s.strip().replace("h", ":").split(":")
    return int(h) * 60 + int(m or 0)


def fmt_hm(minutes: int) -> str:
    return f"{minutes // 60:02d}h{minutes % 60:02d}"


def fmt_duree(minutes: int) -> str:
    h, m = divmod(int(minutes), 60)
    return f"{h} h {m:02d}" if m else f"{h} h"


@dataclass
class Parametres:
    date_debut: dt.date
    heures_centre: float
    creneaux: list[tuple[str, str]] = field(default_factory=lambda: [("08:30", "12:00"), ("13:00", "16:30")])
    pauses: list[tuple[str, str]] = field(default_factory=lambda: [("10:15", "10:30"), ("14:45", "15:00")])
    jours_semaine: list[int] = field(default_factory=lambda: [0, 1, 2, 3, 4])   # 0 = lundi
    rythme: str = ""            # ex. « CCEE » : 2 semaines centre / 2 semaines entreprise (répété)
    fermetures: list[tuple[dt.date, dt.date, str]] = field(default_factory=list)
    feries: bool = True
    heures_entreprise: float = 0
    date_examen: Optional[dt.date] = None
    ordre_cp: list[int] = field(default_factory=list)
    poids_cp: dict[int, float] = field(default_factory=dict)
    # Modules transverses (heures) — modifiables
    h_accueil: float = 7
    h_ecf_par_at: float = 3.5
    h_dossier_pro: float = 14
    h_productions: float = 21
    h_examen_blanc: float = 0          # 0 = durée des épreuves du RE arrondie
    h_bilan: float = 3.5
    part_evaluation_cp: float = 0.12
    max_minutes_seance: int = 420     # au-delà, une séance est scindée en parties
    hypotheses: list[str] = field(default_factory=list)

    def minutes_par_jour(self) -> int:
        return sum(b - a for a, b in _fenetres(self))


def _fenetres(p: Parametres) -> list[tuple[int, int]]:
    """Fenêtres d'enseignement d'une journée (créneaux moins les pauses)."""
    fenetres = []
    pauses = sorted((_hm(a), _hm(b)) for a, b in p.pauses)
    for a, b in p.creneaux:
        debut, fin = _hm(a), _hm(b)
        curseur = debut
        for pa, pb in pauses:
            if debut <= pa < fin:
                if pa > curseur:
                    fenetres.append((curseur, pa))
                curseur = max(curseur, pb)
        if fin > curseur:
            fenetres.append((curseur, fin))
    return fenetres


def jour_ouvre(p: Parametres, jour: dt.date, debut_rythme: dt.date) -> tuple[bool, str]:
    if jour.weekday() not in p.jours_semaine:
        return False, "jour non travaillé en centre"
    if p.feries:
        f = jours_feries_reunion(jour.year).get(jour)
        if f:
            return False, f"férié : {f}"
    for a, b, motif in p.fermetures:
        if a <= jour <= b:
            return False, motif or "fermeture"
    if p.rythme:
        semaine = ((jour - (debut_rythme - dt.timedelta(days=debut_rythme.weekday()))).days // 7)
        if p.rythme[semaine % len(p.rythme)].upper() != "C":
            return False, "semaine en entreprise"
    return True, ""


def creneaux_disponibles(p: Parametres, minutes_requises: int, limite_jours: int = 1500):
    """Génère (date, début, fin) jusqu'à couvrir `minutes_requises`."""
    fenetres = _fenetres(p)
    if not fenetres:
        raise ValueError("Aucun créneau horaire valide : vérifiez les horaires et les pauses.")
    total = 0
    jour = p.date_debut
    for _ in range(limite_jours):
        if jour_ouvre(p, jour, p.date_debut)[0]:
            for a, b in fenetres:
                yield jour, a, b
                total += b - a
                if total >= minutes_requises:
                    return
        jour += dt.timedelta(days=1)


# ==========================================================================
# Modules transverses (hors compétences)
# ==========================================================================
def _obj(texte: str, niveau: int, activite: str, categorie: str = "module", criteres=None) -> Objectif:
    from .pedagogie import mots_cles, verbe_initial
    return Objectif(texte=texte, verbe=verbe_initial(texte), niveau=niveau, categorie=categorie,
                    origine=texte, mots=mots_cles(texte), mode=mode_bruner("technique", niveau),
                    activite=activite, criteres=list(criteres or []))


def module_accueil(reac: Reac, re_: Optional[ReferentielEvaluation]) -> Seance:
    s = Seance(titre="Accueil, présentation du titre et positionnement", origine="Module d'accueil",
               type_seance="module")
    s.objectifs = [
        _obj("Identifier le déroulé de la formation, les règles de vie et les interlocuteurs", 1,
             "Tour de table + livret d'accueil + règlement intérieur"),
        _obj(f"Situer les {len(reac.activites)} activités types et {len(reac.competences)} compétences du titre", 2,
             "Carte mentale collective du titre (AT → CP)"),
        _obj("Décrire les épreuves de l'examen et le dossier professionnel", 2,
             "Présentation de la fiche « Examen simplifié »"),
        _obj("Évaluer ses acquis de départ (positionnement)", 5,
             "Test de positionnement + entretien individuel (adaptations handicap si besoin)"),
    ]
    return s


def module_ecf(at_num: int, at_titre: str, criteres: list[str]) -> Seance:
    s = Seance(titre=f"ECF — Évaluation en cours de formation AT{at_num}", origine=at_titre,
               type_seance="evaluation", at=at_num)
    s.objectifs = [
        _obj(f"Démontrer les compétences de l'AT{at_num} en situation type examen", 5,
             "Étude de cas chronométrée sur le modèle de l'épreuve", "critere", criteres),
        _obj("Analyser ses résultats et fixer ses axes de progrès", 4,
             "Correction collective + auto-positionnement sur les critères"),
    ]
    return s


def module_productions(re_: Optional[ReferentielEvaluation]) -> list[Seance]:
    seances = []
    dp = Seance(titre="Dossier professionnel (DP) : rédaction accompagnée",
                origine="Arrêté du 22 décembre 2015 — dossier professionnel", type_seance="module")
    dp.objectifs = [
        _obj("Sélectionner les exemples de pratique professionnelle par activité type", 4,
             "Atelier : du vécu en entreprise à l'exemple rédigé (méthode STAR)"),
        _obj("Rédiger les exemples de pratique professionnelle du DP", 6,
             "Rédaction guidée + relecture croisée"),
        _obj("Vérifier la complétude du DP avant la session", 5, "Check-list de conformité"),
    ]
    seances.append(dp)
    if re_ and (re_.documents or re_.productions):
        prod = Seance(titre="Productions d'examen : documents et diaporamas", origine="Référentiel d'évaluation",
                      type_seance="module")
        prod.objectifs = [
            _obj(f"Construire le plan du document : {d}", 6, "Plan détaillé validé par le formateur")
            for d in re_.documents if "Mise en forme" not in d
        ] + [
            _obj(f"Concevoir le diaporama : {d}", 6, "Atelier diaporama : 1 idée = 1 diapositive")
            for d in re_.diaporamas
        ] + [
            _obj("S'entraîner à la présentation orale et au questionnement du jury", 3,
                 "Oral blanc filmé + grille d'auto-évaluation"),
        ]
        seances.append(prod)
    return seances


def module_examen_blanc(re_: Optional[ReferentielEvaluation]) -> Seance:
    s = Seance(titre="Examen blanc dans les conditions de la session", origine="Référentiel d'évaluation",
               type_seance="evaluation")
    if re_ and re_.epreuves:
        s.objectifs = [_obj(f"Réaliser l'épreuve « {e.modalite} » ({e.duree})", 5,
                            "Conditions réelles : temps, consignes, jury simulé", "critere")
                       for e in re_.epreuves]
    else:
        s.objectifs = [_obj("Réaliser les épreuves dans les conditions de la session", 5,
                            "Conditions réelles", "critere")]
    return s


def module_bilan() -> Seance:
    s = Seance(titre="Bilan de formation et préparation à la session", origine="Module de clôture",
               type_seance="module")
    s.objectifs = [
        _obj("Évaluer l'atteinte des objectifs de la formation", 5, "Questionnaire de satisfaction + bilan individuel"),
        _obj("Préparer la logistique et le mental du jour de l'examen", 3, "Check-list J-1 / Jour J"),
    ]
    return s


# ==========================================================================
# Construction du plan complet
# ==========================================================================
@dataclass
class Plan:
    seances: list[Seance] = field(default_factory=list)
    lignes: list[dict] = field(default_factory=list)      # déroulé créneau par créneau
    minutes_cp: dict[int, int] = field(default_factory=dict)
    minutes_modules: dict[str, int] = field(default_factory=dict)
    date_fin: Optional[dt.date] = None
    jours_exclus: list[tuple[dt.date, str]] = field(default_factory=list)
    avertissements: list[str] = field(default_factory=list)


def _scinder(seance: Seance, maximum: int) -> list[Seance]:
    if seance.minutes <= maximum or len(seance.objectifs) < 2:
        return [seance]
    parties, courante, total = [], [], 0
    for o in seance.objectifs:
        if courante and total + o.minutes > maximum:
            parties.append(courante)
            courante, total = [], 0
        courante.append(o)
        total += o.minutes
    if courante:
        parties.append(courante)
    if len(parties) == 1:
        return [seance]
    resultat = []
    for i, objs in enumerate(parties, 1):
        s = Seance(titre=f"{seance.titre} (partie {i}/{len(parties)})", origine=seance.origine,
                   objectifs=objs, minutes=sum(o.minutes for o in objs), cp=seance.cp, at=seance.at,
                   type_seance=seance.type_seance)
        resultat.append(s)
    return resultat


def construire_plan(reac: Reac, re_: Optional[ReferentielEvaluation], p: Parametres) -> Plan:
    plan = Plan()
    total = int(round(p.heures_centre * 60 / PAS)) * PAS
    if total <= 0:
        raise ValueError("La durée en centre doit être supérieure à 0 heure.")

    # --- 1. modules transverses
    m_exam = p.h_examen_blanc * 60
    if not m_exam:
        m_exam = sum(e.minutes for e in (re_.epreuves if re_ else [])) or 7 * 60
        m_exam = -(-m_exam // PAS) * PAS
    modules = {
        "accueil": p.h_accueil * 60,
        "ecf": p.h_ecf_par_at * 60 * len(reac.activites),
        "dossier": p.h_dossier_pro * 60,
        "productions": p.h_productions * 60 if (re_ and (re_.documents or re_.productions)) else 0,
        "examen": m_exam,
        "bilan": p.h_bilan * 60,
    }
    modules = {k: int(round(v / PAS)) * PAS for k, v in modules.items()}
    if sum(modules.values()) > total * 0.4:
        plan.avertissements.append(
            "Les modules transverses dépassent 40 % de la durée : ils ont été réduits proportionnellement.")
        facteur = total * 0.4 / sum(modules.values())
        modules = {k: int(v * facteur / PAS) * PAS for k, v in modules.items()}
    plan.minutes_modules = modules
    reste = total - sum(modules.values())

    # --- 2. compétences
    ordre = p.ordre_cp or [c.numero for at in reac.activites for c in reac.competences if c.at_numero == at.numero]
    ordre += [c.numero for c in reac.competences if c.numero not in ordre]
    poids = poids_competences(reac)
    poids.update({k: v for k, v in p.poids_cp.items() if v > 0})
    durees = repartir(reste, [poids[n] for n in ordre], minimum=PAS * 8)
    plan.minutes_cp = dict(zip(ordre, durees))

    # --- 3. séquences dans l'ordre pédagogique
    sequences: list[tuple[str, list[Seance]]] = []
    acc = module_accueil(reac, re_)
    acc.minutes = modules["accueil"]
    sequences.append(("Accueil et positionnement", [acc]))
    at_vus = []
    for n in ordre:
        cp = reac.competence(n)
        seances = decouper_competence(cp, plan.minutes_cp[n], p.part_evaluation_cp)
        sequences.append((f"CP{cp.numero} — {cp.intitule}", seances))
        # ECF à la fin de chaque AT (après sa dernière compétence dans l'ordre)
        at = cp.at_numero
        restantes = [m for m in ordre[ordre.index(n) + 1:] if reac.competence(m).at_numero == at]
        if not restantes and at not in at_vus and modules["ecf"]:
            at_vus.append(at)
            at_obj = reac.activite(at)
            crit = [c for x in reac.competences if x.at_numero == at for c in x.criteres]
            ecf = module_ecf(at, at_obj.intitule if at_obj else "", crit)
            ecf.minutes = modules["ecf"] // max(len(reac.activites), 1)
            sequences.append((f"ECF AT{at}", [ecf]))
    prods = module_productions(re_)
    prods[0].minutes = modules["dossier"]
    if len(prods) > 1:
        prods[1].minutes = modules["productions"]
    sequences.append(("Dossier professionnel et productions d'examen", [s for s in prods if s.minutes]))
    ex = module_examen_blanc(re_)
    ex.minutes = modules["examen"]
    bil = module_bilan()
    bil.minutes = modules["bilan"]
    sequences.append(("Examen blanc et bilan", [s for s in (ex, bil) if s.minutes]))

    # --- 4. numérotation, durées des objectifs des modules, scission des longues séances
    num_seance = 0
    for num_seq, (titre_seq, seances) in enumerate(sequences, 1):
        finales = []
        for s in seances:
            if s.type_seance == "module" or not any(o.minutes for o in s.objectifs):
                for o, d in zip(s.objectifs, repartir(s.minutes, [1.0] * len(s.objectifs))):
                    o.minutes = d
            finales.extend(_scinder(s, p.max_minutes_seance))
        for s in finales:
            num_seance += 1
            s.numero, s.sequence, s.sequence_titre = num_seance, num_seq, titre_seq
            plan.seances.append(s)

    # --- 5. placement dans le calendrier
    file = [(s, o) for s in plan.seances for o in s.objectifs if o.minutes > 0]
    a_placer = sum(o.minutes for _, o in file)
    cumul = 0
    idx, reste_obj = 0, file[0][1].minutes if file else 0
    deja_commence = set()
    for jour, debut, fin in creneaux_disponibles(p, a_placer):
        curseur = debut
        while curseur < fin and idx < len(file):
            s, o = file[idx]
            duree = min(reste_obj, fin - curseur)
            cle = id(o)
            cumul += duree
            plan.lignes.append({
                "date": jour, "debut": curseur, "fin": curseur + duree, "minutes": duree,
                "seance": s, "objectif": o, "suite": cle in deja_commence,
                "cumul": cumul, "pourcentage": cumul / a_placer if a_placer else 0,
            })
            deja_commence.add(cle)
            curseur += duree
            reste_obj -= duree
            if reste_obj <= 0:
                idx += 1
                if idx < len(file):
                    reste_obj = file[idx][1].minutes
        if idx >= len(file):
            break
    plan.date_fin = plan.lignes[-1]["date"] if plan.lignes else None
    if idx < len(file):
        plan.avertissements.append("Calendrier insuffisant : toutes les séances n'ont pas pu être placées.")

    # jours exclus (fériés, fermetures) sur la période réelle
    if plan.date_fin:
        jour = p.date_debut
        while jour <= plan.date_fin:
            ok, motif = jour_ouvre(p, jour, p.date_debut)
            if not ok and motif not in ("jour non travaillé en centre", "semaine en entreprise"):
                plan.jours_exclus.append((jour, motif))
            jour += dt.timedelta(days=1)
    if p.date_examen and plan.date_fin and plan.date_fin >= p.date_examen:
        plan.avertissements.append(
            f"La fin des cours ({plan.date_fin:%d/%m/%Y}) dépasse la date d'examen "
            f"({p.date_examen:%d/%m/%Y}) : revoir le calendrier ou la durée.")
    return plan


def libelle_bloom(o: Objectif) -> str:
    return f"{o.niveau} - {NIVEAUX_BLOOM[o.niveau]}"
