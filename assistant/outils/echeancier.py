"""Échéancier des abonnements et prévisionnel des règlements.

Lit la table « CHARGES & ABONNEMENTS » (export CSV d'Airtable, ou JSON) et calcule,
pour le mois demandé (par défaut : le mois prochain), chaque prélèvement attendu et le
total à provisionner. Aucune donnée personnelle : uniquement des services et des montants.

Usage :
    python assistant/outils/echeancier.py abonnements.csv              # mois prochain
    python assistant/outils/echeancier.py abonnements.json --mois 2026-11
    python assistant/outils/echeancier.py abonnements.csv --sur 3      # 3 mois de prévisionnel

Colonnes attendues (noms de la table Airtable) : « Nom du service », « Coût »,
« Fréquence » (Mensuel / Annuel / Ponctuel), « Prochain renouvellement », « Statut ».
"""
import argparse
import calendar
import csv
import json
import sys
from datetime import date, datetime
from zoneinfo import ZoneInfo

FUSEAU = ZoneInfo("Indian/Reunion")


def lire_date(txt):
    txt = (txt or "").strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(txt[:10], fmt).date()
        except ValueError:
            continue
    return None


def lire_montant(v):
    if isinstance(v, (int, float)):
        return float(v)
    txt = str(v or "").replace("€", "").replace(" ", "").replace(" ", "").replace(",", ".")
    try:
        return float(txt)
    except ValueError:
        return None


def ajouter_mois(d, n):
    m = d.month - 1 + n
    a, m = d.year + m // 12, m % 12 + 1
    return date(a, m, min(d.day, calendar.monthrange(a, m)[1]))


def charger(chemin):
    if chemin.endswith(".json"):
        with open(chemin, encoding="utf-8") as f:
            data = json.load(f)
        # accepte une liste de lignes, ou la réponse brute de l'API Airtable ({"records": [{"fields": …}]})
        if isinstance(data, dict):
            data = [r.get("fields", r) for r in data.get("records", [])]
        return data
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def occurrences(ligne, debut, fin):
    """Dates de prélèvement de la ligne comprises entre debut et fin (inclus)."""
    d = lire_date(ligne.get("Prochain renouvellement"))
    freq = (ligne.get("Fréquence") or "").strip().lower()
    if not d:
        return []
    pas = {"mensuel": 1, "annuel": 12}.get(freq)
    if pas is None:  # ponctuel ou inconnu : une seule échéance
        return [d] if debut <= d <= fin else []
    res, k = [], 0
    while True:
        x = ajouter_mois(d, k * pas)
        if x > fin:
            return res
        if x >= debut:
            res.append(x)
        k += 1


def echeancier(lignes, annee, mois, nb_mois=1):
    debut = date(annee, mois, 1)
    fin_d = ajouter_mois(debut, nb_mois - 1)
    fin = date(fin_d.year, fin_d.month, calendar.monthrange(fin_d.year, fin_d.month)[1])
    sorties, a_verifier = [], []
    for l in lignes:
        if (l.get("Statut") or "Actif").strip() != "Actif":
            continue
        nom = l.get("Nom du service") or "(sans nom)"
        cout = lire_montant(l.get("Coût"))
        if cout is None or not lire_date(l.get("Prochain renouvellement")):
            a_verifier.append(nom)
            continue
        for d in occurrences(l, debut, fin):
            sorties.append((d, nom, cout, l.get("Fréquence") or ""))
    sorties.sort()
    return sorties, a_verifier


def euros(x):
    return f"{x:,.2f} €".replace(",", " ").replace(".", ",")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fichier")
    ap.add_argument("--mois", help="AAAA-MM (par défaut : le mois prochain, heure de La Réunion)")
    ap.add_argument("--sur", type=int, default=1, help="nombre de mois du prévisionnel (défaut 1)")
    a = ap.parse_args()
    if a.mois:
        annee, mois = map(int, a.mois.split("-"))
    else:
        prochain = ajouter_mois(datetime.now(FUSEAU).date().replace(day=1), 1)
        annee, mois = prochain.year, prochain.month
    sorties, a_verifier = echeancier(charger(a.fichier), annee, mois, a.sur)
    print(f"ÉCHÉANCIER — à partir de {mois:02d}/{annee} sur {a.sur} mois\n")
    total, par_mois = 0.0, {}
    for d, nom, cout, freq in sorties:
        print(f"  {d:%d/%m/%Y}  {nom:<35} {euros(cout):>12}  ({freq})")
        total += cout
        par_mois[(d.year, d.month)] = par_mois.get((d.year, d.month), 0) + cout
    if not sorties:
        print("  Aucun prélèvement attendu sur la période.")
    print()
    for (y, m), t in sorted(par_mois.items()):
        print(f"  Total {m:02d}/{y} : {euros(t)}")
    print(f"\n  TOTAL À PROVISIONNER : {euros(total)}")
    if a_verifier:
        print("\n  ⚠ Lignes ignorées (coût ou date manquant) : " + ", ".join(a_verifier))
    return 0


if __name__ == "__main__":
    sys.exit(main())
