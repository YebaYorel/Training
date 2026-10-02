"""Conversion d'heures entre La Réunion et le fuseau d'un interlocuteur.

Tient compte des heures d'été / d'hiver (base IANA, via zoneinfo) : La Réunion est à
UTC+4 toute l'année, mais l'écart avec Paris passe de 2 h (été) à 3 h (hiver).

Usage :
    python assistant/outils/fuseau.py 2026-11-12 14:00 Europe/Paris
        → 14:00 à La Réunion = 11:00 à Paris (Europe/Paris)
    python assistant/outils/fuseau.py 2026-11-12 09:00 Europe/Paris --depuis
        → 09:00 à Paris = 12:00 à La Réunion
    python assistant/outils/fuseau.py --liste
"""
import argparse
import sys
from datetime import datetime
from zoneinfo import ZoneInfo, available_timezones

REUNION = "Indian/Reunion"
RACCOURCIS = {
    "paris": "Europe/Paris", "metropole": "Europe/Paris", "maurice": "Indian/Mauritius",
    "mayotte": "Indian/Mayotte", "madagascar": "Indian/Antananarivo", "dubai": "Asia/Dubai",
    "inde": "Asia/Kolkata", "montreal": "America/Toronto", "chine": "Asia/Shanghai",
    "guadeloupe": "America/Guadeloupe", "martinique": "America/Martinique", "guyane": "America/Cayenne",
    "nouvelle-caledonie": "Pacific/Noumea", "tahiti": "Pacific/Tahiti", "londres": "Europe/London",
    "new-york": "America/New_York", "afrique-du-sud": "Africa/Johannesburg",
}


def zone(nom):
    nom = RACCOURCIS.get(nom.lower(), nom)
    if nom not in available_timezones():
        raise SystemExit(f"Fuseau inconnu : {nom}. Exemple : Europe/Paris, ou un raccourci (--liste).")
    return nom


def convertir(jour, heure, autre, depuis_autre=False):
    src, dst = (autre, REUNION) if depuis_autre else (REUNION, autre)
    dt = datetime.fromisoformat(f"{jour}T{heure}").replace(tzinfo=ZoneInfo(src))
    return dt, dt.astimezone(ZoneInfo(dst))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("jour", nargs="?", help="AAAA-MM-JJ")
    ap.add_argument("heure", nargs="?", help="HH:MM")
    ap.add_argument("fuseau", nargs="?", help="fuseau IANA de l'interlocuteur ou raccourci")
    ap.add_argument("--depuis", action="store_true", help="l'heure donnée est celle de l'interlocuteur")
    ap.add_argument("--liste", action="store_true", help="afficher les raccourcis")
    a = ap.parse_args()
    if a.liste:
        for k, v in RACCOURCIS.items():
            print(f"  {k:<20} {v}")
        return 0
    if not (a.jour and a.heure and a.fuseau):
        ap.error("jour, heure et fuseau sont requis")
    autre = zone(a.fuseau)
    src, dst = convertir(a.jour, a.heure, autre, a.depuis)
    lieu_src, lieu_dst = ("l'interlocuteur", "La Réunion") if a.depuis else ("La Réunion", "l'interlocuteur")
    print(f"{src:%d/%m/%Y %H:%M} ({lieu_src}, {src.tzinfo}, UTC{src:%z}) "
          f"= {dst:%d/%m/%Y %H:%M} ({lieu_dst}, {dst.tzinfo}, UTC{dst:%z})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
