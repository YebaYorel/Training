"""Source unique de vérité pour l'action Marilyn Institut — septembre 2026.

Tout document généré lit ses informations ICI. Une donnée corrigée ici est
corrigée partout au prochain `python build_all.py`.

Règle absolue : aucune information n'est inventée. Ce qui n'est pas connu vaut
A_COMPLETER et s'imprime en rouge dans les documents.

Sources :
  [CONV]  Convention C-MAR-2026-01 du 22/09/2026 (Drive, dossier « Marilyn Institut - Formation »)
  [DEV]   Devis D-MAR-2026-01 et D-MAR-2026-02 du 22/09/2026
  [AIR]   Airtable, CATALOGUE FORMATIONS, fiche FOR-0007 (programme, objectifs)
  [AL]    Message d'Aurélien LUMEKA du 27/09/2026
"""
import json
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent
PRIVE = RACINE / "_donnees_personnelles"
SORTIE = RACINE / "livrables"

A_COMPLETER = "⟦À COMPLÉTER⟧"

# --- Organisme -------------------------------------------------------------
ORG = {
    "nom": "YEBA FORMATIONS",
    "dirigeant": "Aurélien LUMEKA",
    "qualite": "directeur",
    "adresse": "9 rue Françoise Châtelain",
    "cp_ville": "97490 Sainte-Clotilde",           # [AL]
    "tel": "06 93 32 24 45",                        # [AL]
    "email": "yebaformations@gmail.com",            # [AL] — prime sur contact@ des anciens documents
    "site": "www.yebaformations.re",
    "siret": "814 622 262 00032",
    "nda": "04973676397",
    "nda_mention": "Déclaration d'activité n° 04973676397 auprès du préfet de région de La Réunion. "
                   "Cet enregistrement ne vaut pas agrément de l'État.",
    "qualiopi": "Certification Qualiopi n° 25FOR02027.1 — catégorie « actions de formation »",  # [AL] mot pour mot
    "tva": "TVA non applicable, article 293 B du CGI.",  # [CONV]
    "ref_handicap": "Aurélien LUMEKA — 9 rue Françoise Châtelain, 97490 Sainte-Clotilde — 06 93 32 24 45 — yebaformations@gmail.com",
}

# --- Client ----------------------------------------------------------------
CLIENT = {
    "raison_sociale": "MARILYN INSTITUT",
    "forme": "SARL",
    "siege": "100 rue du Maréchal Leclerc — 97400 Saint-Denis",
    "siren": "891 617 169",
    "representant": "Sarah MACHON",
    "qualite": "gérante",
    "opco": "OPCO EP",
    "etablissements": {
        "00018": ("MARILYN INSTITUT", "891 617 169 00018", "100 rue du Maréchal Leclerc, 97400 Saint-Denis"),
        "00026": ("L'OR DES ÎLES", "891 617 169 00026", "2 impasse des Citrines, rue des Corbeilles d'Or, 97412 Bras-Panon"),
    },
}

# --- Action ----------------------------------------------------------------
ACTION = {
    "intitule": "Excellence de la relation cliente et vente-conseil en institut",   # [CONV] art. 2
    "reference": "YEBA-MI-2026-01",
    "convention": "C-MAR-2026-01",
    "nature": "Action de formation — article L.6313-1, 1° du code du travail",
    "modalite": "Présentiel, intra-entreprise",
    "duree_h": 7,                                   # [CONV] art. 2 — durée conventionnelle par session
    "horaires": "8h00 – 17h00",                     # [AL] + [CONV]
    "pauses": [("10h00", "10h15"), ("12h00", "13h00"), ("15h00", "15h15")],  # [AL]
    "repas": "Repas à prévoir par chaque participante (pause déjeuner de 12h00 à 13h00).",  # [AL]
    "lieu_nom": "C.R.E.P.S de Saint-Denis — salle « SEYCHELLES »",
    "lieu_adresse": "24 route Philibert Tsiranana — CS 61115 — 97495 La Réunion",  # [AL] mot pour mot
    "formateur": "Aurélien LUMEKA",
    "ratio": "30 % d'apports — 70 % de pratique",
    "prerequis": "Aucun prérequis de niveau. Exercer une activité au contact de la clientèle.",
    "public": "Esthéticiennes, prothésistes ongulaires, praticiennes et personnel d'accueil de MARILYN INSTITUT et de L'OR DES ÎLES.",
}

SESSIONS = {
    1: {"date": "lundi 28 septembre 2026", "date_courte": "28/09/2026", "devis": "D-MAR-2026-01", "groupe": "Groupe 1"},
    2: {"date": "mardi 29 septembre 2026", "date_courte": "29/09/2026", "devis": "D-MAR-2026-02", "groupe": "Groupe 2"},
}

# [AIR] — objectifs opérationnels de la fiche FOR-0007 (Annexe 1 de la convention)
OBJECTIFS = [
    "Appliquer les standards de tenue, de présentation et d'attitude professionnelle définis collectivement dans la Charte d'Image Marilyn.",
    "Conduire le parcours cliente de l'arrivée au départ, en sécurisant les moments de vérité.",
    "Mener une découverte du besoin structurée à l'aide de la méthode S.O.I.N.",
    "Formuler une recommandation complémentaire adaptée, argumentée par le bénéfice et sans pression (méthode P.E.R.L.E.).",
    "Traiter les cinq objections les plus fréquentes sans se justifier ni consentir de remise.",
    "Proposer systématiquement une reprise de rendez-vous en sortie de cabine, selon un standard commun aux deux instituts.",
    "Identifier et exécuter en autonomie les actions à valeur ajoutée pendant les temps creux.",
    "Recevoir une consigne ou une remarque professionnelle en appliquant la séquence Accuser réception / Reformuler / Proposer.",
    "Expliquer sa contribution individuelle au chiffre d'affaires et au remplissage des agendas.",
    "Respecter les règles de collecte et de conservation des données de la fiche cliente (RGPD).",
]

# Déroulé 8h00–17h00 : programme FOR-0007 [AIR], recalé sur les horaires [AL]
# et adapté aux résultats du positionnement (voir fiche Indicateur 8).
# (début, fin, lettre, titre, contenu, pratique_min)
PROGRAMME = [
    ("08h00", "08h30", "", "Accueil & ouverture",
     "Émargement. Consignes de sécurité du C.R.E.P.S. « L'incident » : accueil volontairement raté, puis rejoué aux standards. Mur des ressentis.", 20),
    ("08h30", "09h00", "", "Contrat de la journée",
     "Tour « Je suis / Je fais / Ma fierté ». Le Panier des attentes. Protocole M.A.R.I.L.Y.N. Retour collectif et anonyme du positionnement. RGPD et IA : 5 minutes de transparence.", 15),
    ("09h00", "10h00", "M", "Le Miroir — image professionnelle",
     "Apparence, langage, comportement. Le Photomaton inversé. Livrable : la Charte d'Image Marilyn (10 points votés).", 45),
    ("10h00", "10h15", "", "Pause", "", 0),
    ("10h15", "11h15", "A", "L'Accueil — parcours cliente",
     "Moments de vérité, règle du pic-fin. La Carte du Voyage Cliente. Jeu n°1 « Les 8 Clientes ».", 45),
    ("11h15", "12h00", "R", "Le Ressenti — découvrir le besoin",
     "Méthode S.O.I.N. Jeu n°2 « Les 12 Questions d'Or ». Reformulation. Point RGPD : la fiche cliente.", 30),
    ("12h00", "13h00", "", "Pause déjeuner (repas à prévoir)", "", 0),
    ("13h00", "13h15", "", "Réveil « Les 7 secondes »",
     "Chacune rejoue son accueil en 7 secondes. Debout ou assise, au choix.", 15),
    ("13h15", "14h30", "L", "Le Lien — conseiller sans forcer",
     "Méthode P.E.R.L.E. Jeu n°3 « Bénéfice ou Caractéristique ? ». Le Ring des objections : « c'est cher », « je vais réfléchir »…", 55),
    ("14h30", "15h00", "Y", "« Y revenir » — fidéliser",
     "Taux de reprise de RDV. Atelier « La Phrase qui Rebooke ». Point RGPD : SMS et consentement.", 20),
    ("15h00", "15h15", "", "Pause", "", 0),
    ("15h15", "15h40", "I", "L'Initiative — temps creux",
     "Les 20 Gestes de Valeur. Matrice valeur / effort. Livrable : la Roue des Temps Creux.", 20),
    ("15h40", "16h20", "N", "Nous — équipe et feedback",
     "Méthode A.R.P. Exercice « Le Boomerang ». Jeu n°4 « Les 7 Merveilles de la Beauté » : 10 standards communs.", 30),
    ("16h20", "16h40", "", "Évaluation des acquis",
     "Quiz de 10 questions, en équipes, sur l'écran. Correction commentée.", 15),
    ("16h40", "17h00", "", "Clôture",
     "Ma Promesse Marilyn. Retour au Panier des attentes. Questionnaire de satisfaction. Émargement.", 10),
]

AUTO_ITEMS = [
    "Accueillir une cliente que je ne connais pas",
    "Soigner ma tenue, ma voix, ma posture en permanence",
    "Poser des questions pour comprendre le vrai besoin",
    "Recommander un produit sans avoir l'impression de forcer",
    "Répondre à une cliente qui dit « c'est trop cher »",
    "Proposer le prochain rendez-vous avant qu'elle parte",
    "Occuper utilement un moment sans cliente",
    "Recevoir une remarque sur mon travail sans me braquer",
    "Gérer une cliente mécontente",
    "Parler du chiffre d'affaires et des objectifs de l'institut",
]
QCM_ITEMS = [
    ("q_premiere_impression", "Délai de la première impression (« quelques secondes »)"),
    ("q_caracteristique", "« Contient de l'acide hyaluronique » = caractéristique"),
    ("q_trop_cher", "« C'est trop cher » → demander à quoi elle compare"),
    ("q_un_produit", "Un seul produit complémentaire recommandé en fin de soin"),
    ("q_sante", "Donnée de santé sur la fiche cliente (RGPD art. 9)"),
]


def stagiaires():
    data = json.loads((PRIVE / "stagiaires.json").read_text(encoding="utf-8"))
    return data["stagiaires"]


def par_session(n):
    return [s for s in stagiaires() if s["session"] == n]


def nom_complet(s):
    return f"{s['prenom']} {s['nom']}"


def minutes(h):
    hh, mm = h.split("h")
    return int(hh) * 60 + int(mm)


def bilan_temps():
    """Contrôle du ratio pratique / théorie sur le temps de formation hors déjeuner."""
    total = prat = 0
    for d, f, _l, titre, _c, p in PROGRAMME:
        if titre.startswith("Pause"):
            continue
        duree = minutes(f) - minutes(d)
        total += duree
        prat += p
    return total, prat


def vigilance(cle):
    """Points de vigilance nominatifs — stockés hors Git, dans _donnees_personnelles/vigilance.json."""
    return json.loads((PRIVE / "vigilance.json").read_text(encoding="utf-8"))[cle]
