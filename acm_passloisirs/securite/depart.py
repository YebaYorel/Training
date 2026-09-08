"""Garde de départ : la règle qui REFUSE.

RÈGLE 3 DE L'ARCHITECTURE — « Le serveur refuse ».

Pourquoi ce module existe
-------------------------
Dans la base, le verdict de départ est un champ FORMULE. Une formule calcule
et affiche : elle ne bloque pas l'écriture. Un départ affichant
« BLOQUE - RESTRICTION JUDICIAIRE » peut malgré tout être enregistré, puis
l'écran fermé. C'est une faille reconnue de la couche base (vecteur A4).

Ici, le verdict est RECALCULÉ côté serveur à partir de l'état de la base, et
un verdict non conforme empêche l'écriture. Le client ne transmet jamais le
verdict : il transmet des faits, le serveur juge.

Audit S03 (P0) et test T12 :
« Personne inconnue, autorisation révoquée/expirée, identité non vérifiée ou
rôle animateur ne peuvent produire silencieusement un départ sécurisé. »
« Aucun contournement d'une restriction judiciaire. »
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum

from .autorisation import Demandeur, peut_accorder_derogation


class Verdict(str, Enum):
    CONFORME = "CONFORME"
    IDENTITE_A_CONTROLER = "IDENTITE_A_CONTROLER"
    DEROGATION_TRACEE = "DEROGATION_TRACEE"
    BLOQUE = "BLOQUE"


class DepartRefuse(Exception):
    """Levée quand un départ ne peut pas être enregistré. Porte le motif."""

    def __init__(self, motif: str) -> None:
        super().__init__(motif)
        self.motif = motif


@dataclass(frozen=True)
class LienAutorisation:
    """État d'un lien personne-enfant, tel que lu dans la base."""

    identifiant: str
    id_enfant: str
    droit_recuperation: str  # "Oui" | "Non" | "Sous conditions"
    piece_identite_exigee: bool
    restriction_judiciaire: bool
    valable_du: date | None = None
    valable_jusqu_au: date | None = None
    revoque_le: date | None = None


@dataclass(frozen=True)
class DemandeDepart:
    """Faits transmis par le client. Aucun verdict, aucun drapeau d'autorité."""

    id_enfant: str
    lien: LienAutorisation | None
    identite_verifiee: bool
    #: Le client peut DEMANDER une dérogation ; c'est le serveur qui décide
    #: si le demandeur a le droit de l'accorder.
    derogation_demandee: bool = False
    motif_derogation: str = ""
    personne_declaree_hors_lien: str = ""


@dataclass(frozen=True)
class Decision:
    verdict: Verdict
    motif: str

    @property
    def autorise_ecriture(self) -> bool:
        """Seuls trois verdicts permettent d'enregistrer le départ."""
        return self.verdict in {
            Verdict.CONFORME,
            Verdict.IDENTITE_A_CONTROLER,
            Verdict.DEROGATION_TRACEE,
        }


def _lien_valable(lien: LienAutorisation, aujourd_hui: date) -> str | None:
    """Renvoie le motif d'invalidité, ou None si le lien est valable.

    L'ordre des tests reproduit celui de la base, pour que serveur et
    interface ne se contredisent jamais.
    """
    if lien.restriction_judiciaire:
        return "restriction judiciaire"
    if lien.revoque_le is not None and lien.revoque_le <= aujourd_hui:
        return "autorisation révoquée"
    if lien.droit_recuperation == "Non":
        return "pas de droit de récupération"
    if lien.valable_du is not None and lien.valable_du > aujourd_hui:
        return "autorisation pas encore valable"
    if lien.valable_jusqu_au is not None and lien.valable_jusqu_au < aujourd_hui:
        return "autorisation expirée"
    if lien.droit_recuperation not in {"Oui", "Sous conditions"}:
        return "droit de récupération non renseigné"
    return None


def evaluer(demande: DemandeDepart, demandeur: Demandeur,
            aujourd_hui: date | None = None) -> Decision:
    """Recalcule le verdict côté serveur. Ne présume rien du client."""
    jour = aujourd_hui or date.today()

    # 1. Restriction judiciaire — bloquant absolu, avant toute autre règle.
    #    Aucune dérogation, aucun rôle, aucune circonstance ne la lève.
    if demande.lien is not None and demande.lien.restriction_judiciaire:
        return Decision(Verdict.BLOQUE,
                        "Restriction judiciaire : aucune dérogation possible.")

    # 2. Le lien doit concerner CET enfant.
    #    Audit M05 : « une autorisation valable pour un enfant peut être
    #    appliquée à un autre à tort ».
    if demande.lien is not None and demande.lien.id_enfant != demande.id_enfant:
        return Decision(Verdict.BLOQUE,
                        "Le lien d'autorisation concerne un autre enfant.")

    # 3. Aucun lien : seule une dérogation complète et habilitée peut passer.
    if demande.lien is None:
        if not demande.derogation_demandee:
            return Decision(Verdict.BLOQUE,
                            "Aucun lien d'autorisation pour cet enfant.")
        if not peut_accorder_derogation(demandeur):
            # L'animateur qui remet l'enfant ne peut pas s'auto-autoriser.
            return Decision(Verdict.BLOQUE,
                            "Rôle non habilité à accorder une dérogation.")
        if not demande.motif_derogation.strip():
            return Decision(Verdict.BLOQUE, "Dérogation sans motif.")
        if not demande.personne_declaree_hors_lien.strip():
            return Decision(Verdict.BLOQUE,
                            "Dérogation sans personne déclarée.")
        return Decision(Verdict.DEROGATION_TRACEE,
                        "Dérogation accordée par un responsable habilité, tracée.")

    # 4. Lien présent : sa validité prime.
    invalidite = _lien_valable(demande.lien, jour)
    if invalidite is not None:
        return Decision(Verdict.BLOQUE, f"Autorisation invalide : {invalidite}.")

    # 5. Pièce d'identité exigée mais non contrôlée : blocage.
    if demande.lien.piece_identite_exigee and not demande.identite_verifiee:
        return Decision(Verdict.BLOQUE,
                        "Pièce d'identité exigée et non contrôlée.")

    # 6. « Sous conditions » sans contrôle d'identité : blocage.
    if demande.lien.droit_recuperation == "Sous conditions" and not demande.identite_verifiee:
        return Decision(Verdict.BLOQUE,
                        "Conditions non vérifiées pour ce départ.")

    # 7. Départ conforme ; on distingue le cas « identité non contrôlée alors
    #    qu'elle n'était pas exigée » pour qu'il reste visible et rattrapable.
    if not demande.identite_verifiee:
        return Decision(Verdict.IDENTITE_A_CONTROLER,
                        "Départ autorisé ; identité non contrôlée, à confirmer.")

    return Decision(Verdict.CONFORME, "Départ conforme.")


def exiger_conformite(demande: DemandeDepart, demandeur: Demandeur,
                      aujourd_hui: date | None = None) -> Decision:
    """Point d'entrée des routes d'écriture.

    Lève DepartRefuse si l'enregistrement ne doit pas avoir lieu. Aucune route
    ne doit écrire un départ sans passer par ici.
    """
    decision = evaluer(demande, demandeur, aujourd_hui)
    if not decision.autorise_ecriture:
        raise DepartRefuse(decision.motif)
    return decision
