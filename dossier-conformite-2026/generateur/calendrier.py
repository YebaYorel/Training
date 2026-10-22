"""Calendrier réel des promotions : jours ouvrés, fériés (dont 20 décembre à La Réunion), fermetures."""
import datetime as dt

from dateutil.easter import easter

from titres import MEM, RPMS, sequence

JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre",
        "octobre", "novembre", "décembre"]

# Proposition de démarrage (à trancher par le dirigeant)
PROMOTIONS = {
    "MEM": {"titre": MEM, "debut": dt.date(2027, 3, 1), "nom": "MEM — Promotion 1"},
    "RPMS": {"titre": RPMS, "debut": dt.date(2027, 9, 6), "nom": "RPMS — Promotion 1"},
}

# Fermeture de fin d'année de l'organisme (proposition)
FERMETURES = [(dt.date(2027, 12, 20), dt.date(2028, 1, 2), "Fermeture de fin d'année")]


def feries(annee):
    p = easter(annee)
    return {
        dt.date(annee, 1, 1): "Jour de l'an",
        p + dt.timedelta(days=1): "Lundi de Pâques",
        dt.date(annee, 5, 1): "Fête du Travail",
        dt.date(annee, 5, 8): "Victoire 1945",
        p + dt.timedelta(days=39): "Ascension",
        p + dt.timedelta(days=50): "Lundi de Pentecôte",
        dt.date(annee, 7, 14): "Fête nationale",
        dt.date(annee, 8, 15): "Assomption",
        dt.date(annee, 11, 1): "Toussaint",
        dt.date(annee, 11, 11): "Armistice",
        dt.date(annee, 12, 20): "Fête de l'abolition de l'esclavage (La Réunion)",
        dt.date(annee, 12, 25): "Noël",
    }


def jour_off(d):
    """Renvoie le motif si le jour n'est pas travaillé, sinon None."""
    if d.weekday() >= 5:
        return "week-end"
    f = feries(d.year)
    if d in f:
        return f[d]
    for debut, fin, motif in FERMETURES:
        if debut <= d <= fin:
            return motif
    return None


def fmt(d, jour=True):
    s = f"{d.day} {MOIS[d.month - 1]} {d.year}"
    return f"{JOURS[d.weekday()]} {s}" if jour else s


def fmt_court(d):
    return f"{d.day:02d}/{d.month:02d}/{d.year}"


def planifier(code):
    """Affecte chaque journée de la séquence à une date réelle. Renvoie (journées, jours sautés)."""
    promo = PROMOTIONS[code]
    seq = sequence(promo["titre"])
    d, out, sautes = promo["debut"], [], []
    for item in seq:
        while jour_off(d):
            if d.weekday() < 5:
                sautes.append((d, jour_off(d)))
            d += dt.timedelta(days=1)
        out.append((d,) + item)
        d += dt.timedelta(days=1)
    return out, sautes


def session_examen(code):
    """Semaine proposée pour la session : la semaine qui suit la dernière journée de formation."""
    jours, _ = planifier(code)
    fin = jours[-1][0]
    lundi = fin + dt.timedelta(days=7 - fin.weekday())
    return lundi, lundi + dt.timedelta(days=4)


def periodes(code):
    """Regroupe les journées consécutives de même lieu : [(lieu, début, fin, nb_jours, modules)]."""
    jours, _ = planifier(code)
    blocs = []
    for d, lieu, m, *_ in jours:
        if blocs and blocs[-1][0] == lieu:
            b = blocs[-1]
            b[2] = d
            b[3] += 1
            if m and m["code"] not in b[4]:
                b[4].append(m["code"])
        else:
            blocs.append([lieu, d, d, 1, [m["code"]] if m else []])
    return blocs


def semaines(code):
    """Regroupe par semaine civile : [(lundi, [(date, lieu, module, titre)])]."""
    jours, _ = planifier(code)
    out = {}
    for d, lieu, m, n, titre, obj in jours:
        lundi = d - dt.timedelta(days=d.weekday())
        out.setdefault(lundi, []).append((d, lieu, m, titre))
    return sorted(out.items())


if __name__ == "__main__":
    for code in PROMOTIONS:
        jours, sautes = planifier(code)
        print(code, "du", fmt(jours[0][0]), "au", fmt(jours[-1][0]), "—", len(jours), "jours")
        for s in sautes:
            print("   sauté :", fmt(s[0]), s[1])
        for b in periodes(code):
            print("  ", b[0], fmt_court(b[1]), "→", fmt_court(b[2]), b[3], "j", b[4])
        print("   session :", session_examen(code))
