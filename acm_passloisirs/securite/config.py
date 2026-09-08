"""Chargement des secrets et de la configuration de sécurité.

RÈGLE 1 DE L'ARCHITECTURE — « Le secret ne quitte jamais le serveur ».

Ce module est volontairement strict : il REFUSE DE DÉMARRER si un secret
obligatoire est absent, plutôt que de se rabattre sur une valeur par défaut.
Un défaut silencieux en sécurité est pire qu'un arrêt bruyant : il donne
l'apparence du fonctionnement.

Vecteur d'attaque couvert (A1) : un jeton d'API placé dans le code d'une page
web se lit en quelques secondes et donne l'intégralité de la base — santé,
adresses, pièces judiciaires — sans authentification et sans trace exploitable.
Le jeton n'existe donc QUE dans l'environnement du serveur.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field


class ErreurConfiguration(RuntimeError):
    """Levée quand la configuration de sécurité est incomplète ou dangereuse."""


#: Secrets sans lesquels l'application n'a pas le droit de démarrer.
SECRETS_OBLIGATOIRES = (
    "ACM_JETON_BASE",  # accès à la base de données
    "ACM_CLE_SESSION",  # signature des cookies de session
)

#: Longueur minimale d'une clé de session. En dessous, la signature est
#: attaquable hors ligne par force brute sur du matériel courant.
LONGUEUR_MIN_CLE = 32


@dataclass(frozen=True)
class ConfigurationSecurite:
    """Configuration validée. Immuable : personne ne la modifie en cours de route."""

    jeton_base: str
    cle_session: str
    origines_autorisees: tuple[str, ...]
    duree_session_minutes: int = 30
    cookie_securise: bool = True
    fuseau: str = "Indian/Reunion"
    #: Champs qui ne doivent JAMAIS être sérialisés vers un client, quel que
    #: soit son rôle. Filet de sécurité de dernier recours, en complément du
    #: filtrage par rôle (voir autorisation.py).
    champs_toujours_interdits: frozenset[str] = field(
        default_factory=lambda: frozenset(
            {
                "detail_restriction",
                "preuve_restriction",
                "alerte_sante_detail",
                "precision_allergie",
                "precision_medicale",
                "precision_traitement",
                "medecin",
                "tel_medecin",
            }
        )
    )

    def masquer(self) -> dict[str, str]:
        """Représentation sûre pour les journaux : aucun secret en clair.

        Utilisée au démarrage pour tracer la configuration sans la divulguer.
        """
        return {
            "jeton_base": _empreinte(self.jeton_base),
            "cle_session": _empreinte(self.cle_session),
            "origines_autorisees": ",".join(self.origines_autorisees),
            "duree_session_minutes": str(self.duree_session_minutes),
            "cookie_securise": str(self.cookie_securise),
        }


def _empreinte(secret: str) -> str:
    """Empreinte non réversible, pour identifier un secret sans le révéler.

    Permet de vérifier « le serveur utilise bien le jeton que j'ai tourné »
    sans jamais écrire le jeton dans un journal ou un ticket.
    """
    import hashlib

    return "sha256:" + hashlib.sha256(secret.encode("utf-8")).hexdigest()[:12]


def charger(environnement: dict[str, str] | None = None) -> ConfigurationSecurite:
    """Charge et VALIDE la configuration. Lève ErreurConfiguration si dangereuse."""
    env = environnement if environnement is not None else dict(os.environ)

    manquants = [nom for nom in SECRETS_OBLIGATOIRES if not env.get(nom, "").strip()]
    if manquants:
        raise ErreurConfiguration(
            "Secrets obligatoires absents : "
            + ", ".join(manquants)
            + ". Le serveur ne démarre pas sans eux — c'est voulu. "
            "Renseignez-les en variables d'environnement, jamais dans le dépôt."
        )

    cle_session = env["ACM_CLE_SESSION"].strip()
    if len(cle_session) < LONGUEUR_MIN_CLE:
        raise ErreurConfiguration(
            f"ACM_CLE_SESSION fait {len(cle_session)} caractères ; "
            f"{LONGUEUR_MIN_CLE} au minimum sont exigés. Une clé courte se "
            "casse hors ligne, et une session forgée vaut un accès complet."
        )

    origines_brutes = env.get("ACM_ORIGINES_AUTORISEES", "").strip()
    origines = tuple(o.strip() for o in origines_brutes.split(",") if o.strip())
    if not origines:
        raise ErreurConfiguration(
            "ACM_ORIGINES_AUTORISEES est vide. Refuser par défaut : une liste "
            "d'origines vide vaut mieux qu'un caractère générique, qui "
            "autoriserait n'importe quel site à appeler l'API depuis le "
            "navigateur d'un utilisateur authentifié."
        )
    if "*" in origines:
        raise ErreurConfiguration(
            "ACM_ORIGINES_AUTORISEES contient « * ». Interdit : cela laisse "
            "n'importe quel site déclencher des requêtes authentifiées."
        )

    cookie_securise = env.get("ACM_COOKIE_SECURISE", "1").strip() not in {"0", "false", "False"}
    if not cookie_securise and env.get("ACM_ENVIRONNEMENT", "production") == "production":
        raise ErreurConfiguration(
            "Cookies non sécurisés interdits en production : la session "
            "circulerait en clair et serait interceptable."
        )

    return ConfigurationSecurite(
        jeton_base=env["ACM_JETON_BASE"].strip(),
        cle_session=cle_session,
        origines_autorisees=origines,
        duree_session_minutes=int(env.get("ACM_DUREE_SESSION_MINUTES", "30")),
        cookie_securise=cookie_securise,
    )


#: En-têtes de sécurité appliqués à TOUTES les réponses.
#: `default-src 'none'` interdit par défaut tout chargement externe : c'est la
#: posture « refus par défaut » appliquée au navigateur.
EN_TETES_SECURITE = {
    "Content-Security-Policy": (
        "default-src 'none'; script-src 'self'; style-src 'self'; "
        "img-src 'self' data:; connect-src 'self'; form-action 'self'; "
        "frame-ancestors 'none'; base-uri 'none'"
    ),
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Cache-Control": "no-store",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
}
