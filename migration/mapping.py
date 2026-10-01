"""Correspondance des types Airtable → Baserow et conversion des valeurs.

Fonctions PURES (aucun appel réseau) : testables hors ligne.

Principes :
* les champs CALCULÉS (formule, cumul, recherche, comptage) ne sont PAS copiés
  comme valeurs figées : ils doivent être recréés comme formules Baserow, sinon
  ils se désynchroniseraient silencieusement. Ils sont listés dans le rapport ;
* les numéros automatiques et horodatages Airtable sont conservés en valeurs
  (numérotation des factures, historique), car Baserow ne peut pas réécrire
  ses propres champs automatiques ;
* collaborateurs → nom seul (minimisation RGPD : pas d'e-mail ni d'ID).
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Tuple

# Types Airtable non migrés comme données : à recréer en formules Baserow.
COMPUTED_TYPES = {"formula", "rollup", "multipleLookupValues", "lookup", "count"}
# Types sans équivalent utile : ignorés et signalés.
UNSUPPORTED_TYPES = {"button", "aiText", "externalSyncSource"}

_COLORS = {
    "blue": "blue", "cyan": "light-blue", "teal": "green", "green": "green",
    "yellow": "yellow", "orange": "orange", "red": "red", "pink": "red",
    "purple": "dark-blue", "gray": "light-gray",
    # Couleur purement visuelle : une valeur non reconnue n'empêche pas l'import.
}


def baserow_color(airtable_color: Optional[str]) -> str:
    """'greenBright' / 'blueLight2' → couleur Baserow la plus proche."""
    if not airtable_color:
        return "light-gray"
    for prefix, color in _COLORS.items():
        if airtable_color.startswith(prefix):
            return color
    return "light-gray"


def _date_options(af: Dict[str, Any], with_time: bool) -> Dict[str, Any]:
    opts = af.get("options") or {}
    fmt = ((opts.get("dateFormat") or {}).get("name") or "european").lower()
    out: Dict[str, Any] = {
        "date_format": {"us": "US", "iso": "ISO"}.get(fmt, "EU"),
        "date_include_time": with_time,
    }
    if with_time:
        tfmt = (opts.get("timeFormat") or {}).get("name", "24hour")
        out["date_time_format"] = "12" if tfmt == "12hour" else "24"
        tz = opts.get("timeZone")
        if tz and tz not in ("client", "utc"):
            out["date_force_timezone"] = tz
    return out


def plan_field(af: Dict[str, Any]) -> Tuple[Optional[str], Dict[str, Any], str]:
    """Renvoie (type_baserow | None, options, note) pour un champ Airtable.

    type None = champ non créé (calculé ou non pris en charge), `note` explique.
    Les liens (link_row) renvoient l'option spéciale `_linked_table` (ID Airtable)
    à résoudre par l'appelant.
    """
    t = af["type"]
    opts = af.get("options") or {}

    if t in COMPUTED_TYPES:
        return None, {}, "calculé — à recréer en formule Baserow"
    if t in UNSUPPORTED_TYPES:
        return None, {}, "type sans équivalent — ignoré"

    if t in ("singleLineText",):
        return "text", {}, ""
    if t in ("multilineText", "richText"):
        return "long_text", {}, ""
    if t == "email":
        return "email", {}, ""
    if t == "url":
        return "url", {}, ""
    if t == "phoneNumber":
        return "phone_number", {}, ""
    if t == "checkbox":
        return "boolean", {}, ""
    if t in ("number", "currency", "percent"):
        decimals = int(opts.get("precision", 0) or 0)
        note = "pourcentage conservé en fraction (0,5 = 50 %)" if t == "percent" else ""
        if t == "currency":
            decimals = max(decimals, 2)
            note = f"montant ({opts.get('symbol', '€')})"
        return "number", {"number_decimal_places": min(decimals, 10), "number_negative": True}, note
    if t == "autoNumber":
        return "number", {"number_decimal_places": 0}, "numéro automatique Airtable conservé en valeur"
    if t == "rating":
        return "rating", {"max_value": int(opts.get("max", 5) or 5)}, ""
    if t == "duration":
        return "number", {"number_decimal_places": 0}, "durée en secondes"
    if t == "date":
        return "date", _date_options(af, False), ""
    if t == "dateTime":
        return "date", _date_options(af, True), ""
    if t in ("createdTime", "lastModifiedTime"):
        return "date", {"date_format": "EU", "date_include_time": True, "date_time_format": "24"}, \
            "horodatage Airtable conservé en valeur"
    if t in ("singleSelect", "multipleSelects"):
        choices = opts.get("choices") or []
        select_options = [{"value": c["name"], "color": baserow_color(c.get("color"))} for c in choices]
        return ("single_select" if t == "singleSelect" else "multiple_select"), \
            {"select_options": select_options}, ""
    if t == "multipleRecordLinks":
        return "link_row", {"_linked_table": opts.get("linkedTableId")}, ""
    if t == "multipleAttachments":
        return "file", {}, ""
    if t in ("singleCollaborator", "multipleCollaborators", "createdBy", "lastModifiedBy"):
        return "text", {}, "collaborateur → nom seul (minimisation)"
    if t == "barcode":
        return "text", {}, ""
    return None, {}, f"type « {t} » inconnu — ignoré"


def is_empty(value: Any) -> bool:
    return value is None or value == "" or value == [] or value is False


def convert_value(
    af: Dict[str, Any],
    value: Any,
    select_ids: Optional[Dict[str, int]] = None,
    upload: Optional[Callable[[str], Dict[str, Any]]] = None,
) -> Any:
    """Convertit une valeur Airtable (format JSON de l'API) en valeur Baserow.

    Les liens ne sont PAS convertis ici (deuxième passe, après création des lignes).
    Renvoie None pour « ne rien écrire ».
    """
    t = af["type"]
    if value is None:
        return None
    if t == "checkbox":
        return bool(value)
    if t == "singleSelect":
        oid = (select_ids or {}).get(value)
        return oid
    if t == "multipleSelects":
        ids = [(select_ids or {}).get(v) for v in value]
        return [i for i in ids if i is not None]
    if t == "multipleAttachments":
        if upload is None:
            return None
        files = []
        for att in value:
            uploaded = upload(att["url"])
            files.append({"name": uploaded["name"], "visible_name": att.get("filename") or uploaded["name"]})
        return files
    if t in ("singleCollaborator", "createdBy", "lastModifiedBy"):
        return value.get("name") or ""
    if t == "multipleCollaborators":
        return ", ".join(v.get("name", "") for v in value)
    if t == "barcode":
        return value.get("text")
    if t == "rating":
        return int(value)
    if isinstance(value, (dict, list)):
        return None  # forme inattendue : on n'invente rien
    return value


def computed_formula_readable(af: Dict[str, Any], names: Dict[str, str]) -> str:
    """Formule/cumul Airtable rendue lisible ({fldXXX} → {Nom du champ})."""
    opts = af.get("options") or {}
    formula = opts.get("formula")
    if formula:
        for fid, fname in names.items():
            formula = formula.replace("{" + fid + "}", "{" + fname + "}")
        return formula
    parts: List[str] = []
    if opts.get("recordLinkFieldId"):
        parts.append(f"via lien « {names.get(opts['recordLinkFieldId'], opts['recordLinkFieldId'])} »")
    if opts.get("fieldIdInLinkedTable"):
        parts.append(f"champ distant « {names.get(opts['fieldIdInLinkedTable'], opts['fieldIdInLinkedTable'])} »")
    return " ; ".join(parts) or "(configuration non exposée par l'API)"
