"""Autorisation par objet et filtrage des champs en sortie.

RÈGLES 2 ET 4 DE L'ARCHITECTURE :
  - « Autorisation par objet, à chaque requête »
  - « Filtrage en sortie, par rôle »

Vecteurs d'attaque couverts :
  A7 (IDOR) — un identifiant fourni par le client n'est JAMAIS une preuve de
      légitimité. On revérifie systématiquement le lien entre le demandeur et
      l'objet demandé.
  A5/A6 — le serveur ne renvoie que les champs autorisés ; il ne se contente
      pas de les masquer à l'affichage, où un simple outil de développement
      les révélerait.

Correspond à la matrice d'habilitation de l'audit (p. 18) et au contrôle C02 :
« Animateur : finances et médical complet inaccessibles, y compris via liens,
exports et API applicables. »
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Role(str, Enum):
    """Rôles de la matrice d'habilitation de l'audit."""

    DIRECTION = "direction"
    ADMINISTRATIF = "administratif"
    RESPONSABLE_ACM = "responsable_acm"  # habilitation sanitaire
    ANIMATEUR = "animateur"
    COMPTABILITE = "comptabilite"
    PRESTATAIRE = "prestataire"
    PARENT = "parent"  # phase 2


class AccesRefuse(PermissionError):
    """Levée quand un accès est refusé. Ne dit jamais POURQUOI au client."""


#: Champs lisibles par rôle. Tout champ absent de l'ensemble est refusé :
#: liste blanche, jamais liste noire — une liste noire oublie toujours le
#: champ ajouté le mois suivant.
CHAMPS_LISIBLES: dict[Role, frozenset[str]] = {
    Role.ANIMATEUR: frozenset(
        {
            "id",
            "nom_complet",
            "classe",
            "vigilance_sanitaire",  # indicateur binaire, sans détail
            "consigne_operationnelle",  # sans diagnostic ni médicament
            "nage",
            "presence_appel_matin",
            "presence_appel_apres_midi",
            "creneau",
            "personnes_autorisees_libelle",
            "contacts_urgence",
        }
    ),
    Role.RESPONSABLE_ACM: frozenset(
        {
            "id",
            "nom_complet",
            "classe",
            "vigilance_sanitaire",
            "consigne_operationnelle",
            "sante_pai",
            "sante_allergie",
            "sante_regime",
            "sante_traitement",
            "sante_medecin",
            "autorisations",
            "incidents",
            "creneau",
            "contacts_urgence",
        }
    ),
    Role.ADMINISTRATIF: frozenset(
        {
            "id",
            "nom_complet",
            "classe",
            "vigilance_sanitaire",  # l'indicateur, jamais le détail
            "date_naissance",
            "famille",
            "responsables",
            "documents_administratifs",
            "inscriptions",
            "echeancier",
            "statut_paiement",
        }
    ),
    Role.COMPTABILITE: frozenset(
        {
            "id",
            "nom_complet",
            "inscriptions",
            "echeancier",
            "encaissements",
            "affectations",
            "statut_paiement",
            "reste_du",
        }
    ),
    Role.DIRECTION: frozenset(
        {
            "id",
            "nom_complet",
            "classe",
            "date_naissance",
            "famille",
            "responsables",
            "inscriptions",
            "echeancier",
            "encaissements",
            "statut_paiement",
            "reste_du",
            "documents_administratifs",
            "vigilance_sanitaire",
            "consigne_operationnelle",
            "incidents",
            "autorisations",
        }
    ),
    # Le prestataire technique n'a AUCUN champ métier par défaut.
    # Audit p.18 : « Copie générale des dossiers pour développer » = accès à exclure.
    Role.PRESTATAIRE: frozenset({"id"}),
    Role.PARENT: frozenset(
        {
            "id",
            "nom_complet",
            "classe",
            "creneau",
            "inscriptions",
            "echeancier",
            "statut_paiement",
        }
    ),
}

#: Rôles autorisés à consulter le dossier médical complet.
#: Audit S02 : « Valider les habilitations sanitaires. »
ROLES_HABILITATION_SANITAIRE = frozenset({Role.RESPONSABLE_ACM, Role.DIRECTION})

#: Rôles autorisés à accorder une dérogation de départ.
#: Audit S03 : « uniquement via un responsable habilité ». L'animateur qui
#: effectue la remise ne peut pas s'auto-autoriser.
ROLES_DEROGATION_DEPART = frozenset({Role.RESPONSABLE_ACM, Role.DIRECTION})


@dataclass(frozen=True)
class Demandeur:
    """Identité authentifiée. Construite par le serveur, jamais par le client."""

    identifiant: str
    role: Role
    #: Enfants auxquels ce compte est rattaché (parents : liens actifs).
    enfants_rattaches: frozenset[str] = frozenset()
    #: Enfants de la mission du jour (animateurs).
    enfants_mission_du_jour: frozenset[str] = frozenset()


def peut_lire_enfant(demandeur: Demandeur, id_enfant: str) -> bool:
    """L'accès à UN enfant précis, revérifié à chaque requête.

    C'est le cœur de la protection contre l'IDOR (A7) : le fait de connaître
    un identifiant ne confère aucun droit.
    """
    if demandeur.role in {Role.DIRECTION, Role.ADMINISTRATIF, Role.RESPONSABLE_ACM,
                          Role.COMPTABILITE}:
        return True
    if demandeur.role is Role.PARENT:
        return id_enfant in demandeur.enfants_rattaches
    if demandeur.role is Role.ANIMATEUR:
        return id_enfant in demandeur.enfants_mission_du_jour
    return False  # prestataire et tout rôle inconnu : refus


def exiger_lecture_enfant(demandeur: Demandeur, id_enfant: str) -> None:
    """Version impérative : lève AccesRefuse au lieu de renvoyer False.

    Le message reste volontairement neutre. Répondre « cet enfant existe mais
    vous n'y avez pas droit » confirmerait l'existence de l'enregistrement à
    un attaquant qui énumère des identifiants.
    """
    if not peut_lire_enfant(demandeur, id_enfant):
        raise AccesRefuse("Ressource introuvable.")


def filtrer_sortie(demandeur: Demandeur, donnees: dict[str, object],
                   champs_toujours_interdits: frozenset[str] = frozenset()) -> dict[str, object]:
    """Ne conserve que les champs que le rôle a le droit de LIRE.

    Deux filtres successifs, volontairement redondants :
      1. la liste blanche du rôle ;
      2. la liste des champs interdits à tous (défense en profondeur : si un
         champ sensible est ajouté par erreur à une liste blanche, ce second
         filtre le rattrape).
    """
    autorises = CHAMPS_LISIBLES.get(demandeur.role, frozenset())
    return {
        cle: valeur
        for cle, valeur in donnees.items()
        if cle in autorises and cle not in champs_toujours_interdits
    }


def peut_accorder_derogation(demandeur: Demandeur) -> bool:
    """Audit section 16 : dans le kit initial, un booléen `supervisor_override`
    envoyé par le client suffisait à valider un départ avec une personne non
    déclarée et sans contrôle d'identité.

    Ici, la dérogation dépend du RÔLE AUTHENTIFIÉ côté serveur — jamais d'un
    drapeau transmis dans la requête.
    """
    return demandeur.role in ROLES_DEROGATION_DEPART
