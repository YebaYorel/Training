"""Données du lieu de formation : Secrétariat Center (Technor, Saint-Denis).

Sources : informations transmises par le dirigeant le 22/10/2026 (accès, accessibilité,
bus, restauration) ; site lacantoche.re et annuaires en ligne pour La Cantoche et Le Nixon.
Tout ce qui n'a pas pu être confirmé porte la mention « à vérifier ».
"""

NOM = "Secrétariat Center"
ADRESSE = ["Immeuble Rodrigues 2", "7 rue Henri Cornu", "Technopole de La Réunion — Parc Technor", "97490 Saint-Denis (Sainte-Clotilde)"]
SITE = "www.secretariat-center.fr"

ATOUTS = [
    ("Au cœur de Technor", "La technopole de Saint-Denis, entourée de commerces et de services."),
    ("Bien desservi", "Lignes Citalis et Car Jaune à quelques pas."),
    ("À 3 minutes de l'aéroport", "Roland-Garros, en voiture : pratique pour les intervenants et les jurys."),
    ("Accessible", "Entrée, parking, sièges et toilettes accessibles en fauteuil roulant."),
]

EQUIPEMENTS = [
    "Salle de formation équipée : vidéoprojecteur et tableau",
    "Salle de pause",
    "Sanitaires, dont toilettes accessibles en fauteuil roulant",
    "Boissons sur place (environ 2 €) et formules petit-déjeuner (environ 5 €)",
]

ACCESSIBILITE = [
    "Entrée accessible en fauteuil roulant",
    "Places de parking accessibles",
    "Sièges adaptés",
    "Toilettes accessibles en fauteuil roulant",
]

# (arrêt, position, lignes, réseau, destinations)
BUS = [
    ("Parc Technor", "Le plus proche du bâtiment", "26, 27, 29", "Citalis",
     "26 : Bois Rouge – Mairie du Chaudron – Mangoustan – Bibliothèque · 27 : Bretagne Bellevue – Mairie du Chaudron · 29 : Chemin du Plateau – ZAC 2 Moufia"),
    ("Pierre Loti", "À l'entrée de Technor", "29, 31, 32", "Citalis", "Réseau urbain du Nord"),
    ("Technopole", "Sur l'axe principal", "E2, E3, E4", "Car Jaune", "Est (Saint-André, Saint-Benoît) et centre-ville de Saint-Denis"),
]

VOITURE = [
    "Stationnement gratuit dans la rue (places limitées : arriver tôt)",
    "Parking couvert payant à proximité",
    "Places de stationnement accessibles",
    "Aéroport Roland-Garros à environ 3 minutes",
]

# (nom, où, type, prix, accès, remarque, vérifié)
REPAS_A_PIED = [
    ("Secrétariat Center", "Sur place", "Boissons, viennoiseries, petit-déjeuner", "2 € à 5 €", "Sur place",
     "Servi en salle ; idéal pour les pauses de 10 h et 15 h", True),
    ("Camions-bars et snacks du Parc Technor", "Dans le parc", "Sandwichs, salades, barquettes de carry créole", "6 € à 10 €", "À pied",
     "Grande barquette autour de 7 € à 8 € ; l'option rapide des actifs de la zone", True),
    ("La Cantoche", "12 rue Maurice Tomi, Technor", "Cuisine du midi, sur place, à emporter ou en click & collect", "Prix à vérifier", "À pied",
     "Du lundi au vendredi, de 10 h à 15 h (selon son site)", False),
]

REPAS_EN_VOITURE = [
    ("Les Délices du Nord M&M", "Route de la Rivière des Pluies", "Buffet créole à volonté ou barquettes", "20 € à 30 € (barquette dès 7 €)", "3 min en voiture",
     "Bon rapport qualité-prix pour un repas complet", True),
    ("Cap Méchant Buffet Cadjee", "Boulevard du Chaudron", "Grand buffet : caris, rougails, salades, desserts", "Environ 25 €", "3 min en voiture",
     "Service assis, idéal pour un repas de groupe", True),
    ("Le Nixon", "ZAC Foucherolle", "Grillades, cuisine créole et chinoise", "À vérifier", "Distance à vérifier",
     "Ouvert du lundi au samedi, midi et soir (selon sa page publique)", False),
]

CONSEILS = [
    "La pause déjeuner dure 1 heure (12 h – 13 h) : privilégiez les options à pied.",
    "Commandez la veille en click & collect pour gagner du temps.",
    "Repas apporté : il se prend dans la salle de pause, jamais dans la salle de formation.",
    "En période de fortes pluies, renseignez-vous avant de partir : les accès au Chaudron peuvent être ralentis.",
]

VERIF = ("Horaires, lignes et prix susceptibles d'évoluer : à vérifier avant chaque session sur citalis.re, carjaune.re "
         "et auprès des établissements. Les temps de marche ne sont pas garantis.")
