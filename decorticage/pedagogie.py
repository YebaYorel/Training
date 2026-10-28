"""Moteur pédagogique : Taxonomie de Bloom, processus brunérien, séances.

Principes appliqués (sources citées dans DECORTICAGE.md) :

* **Taxonomie de Bloom révisée** (Anderson & Krathwohl, 2001) : 6 niveaux
  — Se souvenir, Comprendre, Appliquer, Analyser, Évaluer, Créer. Chaque
  objectif commence par un verbe d'action observable.
* **Processus brunérien** (Bruner) :
  - les 3 modes de représentation : *enactif* (agir), *iconique* (image,
    schéma), *symbolique* (mots, concepts, chiffres) ;
  - le curriculum en spirale : on revient sur les notions avec un niveau
    croissant (rappel en début de séance) ;
  - les 6 fonctions d'étayage (Wood, Bruner & Ross, 1976) : enrôlement,
    réduction des degrés de liberté, maintien de l'orientation,
    signalisation des caractéristiques déterminantes, contrôle de la
    frustration, démonstration.

Les objectifs REPRENNENT LES TERMES DU REAC (verbe + objet), simplifiés en
retirant seulement les mots de remplissage. La trace de la phrase d'origine
est conservée dans le tableau.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field

from .referentiels import Competence, Reac, normaliser

# ==========================================================================
# Taxonomie de Bloom révisée — verbes d'action (infinitifs, normalisés)
# ==========================================================================
NIVEAUX_BLOOM = {
    1: "Se souvenir",
    2: "Comprendre",
    3: "Appliquer",
    4: "Analyser",
    5: "Évaluer",
    6: "Créer",
}

VERBES_BLOOM = {
    1: ["identifier", "citer", "nommer", "lister", "reperer", "reconnaitre", "enumerer",
        "connaitre", "recenser", "localiser"],
    2: ["expliquer", "decrire", "distinguer", "illustrer", "interpreter", "reformuler", "situer",
        "resumer", "comprendre", "differencier", "classer", "presenter", "informer", "sensibiliser",
        "ecouter", "echanger"],
    3: ["appliquer", "utiliser", "mettre en oeuvre", "mettre en œuvre", "realiser", "executer",
        "calculer", "transmettre", "renseigner", "receptionner", "faire respecter", "faire appliquer",
        "respecter", "mener", "animer", "conduire", "communiquer", "accompagner", "assurer",
        "participer", "mettre a disposition", "mettre en place", "mettre en avant", "pratiquer",
        "adopter", "deleguer", "accueillir", "conseiller", "traiter", "gerer", "suivre", "tenir",
        "veiller", "remplir", "collecter", "mobiliser", "impliquer", "associer", "partager",
        "fideliser", "valoriser", "encourager", "responsabiliser", "consulter", "cooperer",
        "collaborer", "travailler", "maintenir", "rendre compte", "signaler", "alerter", "adapter",
        "reagir", "etre", "prendre en compte", "integrer", "favoriser", "implanter", "installer",
        "motiver", "federer", "manager", "entretenir", "developper", "corriger", "reajuster",
        "inventorier", "commander", "stocker", "approvisionner", "mettre a jour", "maitriser"],
    4: ["analyser", "comparer", "diagnostiquer", "structurer", "organiser", "hierarchiser",
        "detecter", "examiner", "synthetiser", "anticiper", "identifier les causes", "prioriser",
        "decomposer", "rapprocher", "mesurer", "evaluer la charge", "coordonner", "relier",
        "selectionner", "rechercher", "controler la coherence", "articuler"],
    5: ["evaluer", "controler", "verifier", "justifier", "argumenter", "arbitrer", "valider",
        "juger", "critiquer", "apprecier", "s'assurer", "assurer le suivi", "tester", "auditer"],
    6: ["elaborer", "concevoir", "planifier", "construire", "proposer", "formuler", "preparer",
        "creer", "produire", "definir", "formaliser", "rediger", "imaginer", "ameliorer",
        "optimiser", "contribuer a l'elaboration", "batir", "composer", "etablir", "parametrer"],
}

_INDEX_VERBES = sorted(
    ((v, n) for n, vs in VERBES_BLOOM.items() for v in vs), key=lambda x: -len(x[0])
)


def niveau_bloom(phrase: str) -> int:
    """Niveau de Bloom (1-6) déduit du verbe initial de la phrase."""
    p = normaliser(phrase)
    p = re.sub(r"^(savoir|pouvoir|etre capable de|etre en mesure de)\s+", "", p)
    for verbe, niveau in _INDEX_VERBES:
        if p.startswith(verbe):
            return niveau
    return 3


def verbe_initial(phrase: str) -> str:
    """Le verbe d'action (ou locution verbale) qui ouvre la phrase."""
    mots = phrase.split()
    if not mots:
        return ""
    p = normaliser(phrase)
    for verbe, _ in _INDEX_VERBES:
        if p.startswith(verbe + " ") or p == verbe:
            return " ".join(mots[: len(verbe.split())])
    return mots[0]


# ==========================================================================
# Simplification « mots les plus importants » (en gardant les termes REAC)
# ==========================================================================
_REMPLISSAGE = [
    r"\bde son périmètre\b", r"\bdu périmètre\b", r"\bau sein de l’établissement marchand\b",
    r"\bde l’établissement marchand\b", r"\bdans l’établissement marchand\b",
    r"\bde manière (précise et )?adaptée à la situation\b", r"\bselon la procédure interne\b",
    r"\bde l’enseigne\b", r"\ben vigueur\b", r"\bcourants?\b", r"\bet plus particulièrement\b",
    r"\ble cas échéant\b", r"\bsi nécessaire\b", r"\bnotamment\b", r"\bégalement\b",
]
_MOTS_VIDES = set("""
le la les un une des de du d l à au aux et ou en dans sur pour par avec sans sous son sa ses leur leurs
ce cette ces qui que dont il elle ils elles se sa est sont être a ont plus moins tout tous toute toutes
afin ainsi selon entre vers chez lors cas échéant etc ex notamment également aussi très bien mise
lien liés liées lié liée relatif relative relatives relatifs concernant matière niveau type types
façon manière cadre ensemble différentes différents principales principaux connaissance connaissances
notions fonction fonctions place compte faire œuvre oeuvre rendre auprès face autres autre issues issus
afin cela elles leurs mettre mise place sein travers partir
""".split())

# Familles de mots : relient des formulations différentes d'une même idée
# (ex. « entretien » et « feedback »), pour rattacher chaque savoir-faire à
# la bonne étape du processus.
FAMILLES = [
    {"entreti", "individ", "feedbac", "recadra", "evaluat", "potenti", "progres"},
    {"briefin", "debrief", "reunion", "animer", "animati"},
    {"consign", "informa", "transme", "communi", "procedu", "expliqu", "partage", "message"},
    {"motivat", "stimula", "challen", "team", "federer", "cohesio", "dynamiq", "mobilis", "engagem",
     "fideli", "valoris"},
    {"amelior", "correct", "precon", "solutio", "proposi", "continu", "pdca", "deming", "qualite"},
    {"profess", "formati", "compete", "tutorat", "former", "montee", "develop", "parcour"},
    {"projet", "etapes", "retropl", "hierarc", "jalons"},
    {"handica", "discrim", "inclusi", "amenage", "rqth", "agefiph", "referen"},
    {"plannin", "horaire", "planifi", "charge", "tache", "taches", "absence", "imprevu", "effecti"},
    {"risque", "securit", "prevent", "epi", "tms", "duerp", "hygiene", "qhse", "accident"},
    {"recrute", "candida", "selecti", "poste", "integra", "essai", "accueil", "recrue"},
    {"stock", "stocks", "command", "inventa", "approvi", "recepti", "livrais", "fournis", "rupture"},
    {"merchan", "implant", "lineair", "planogr", "vitrine", "balisag", "operati", "promoti"},
    {"client", "clients", "clientel", "satisfa", "omnican", "crm", "argumen", "vente", "conseil"},
    {"indicat", "tableau", "chiffre", "panier", "transfo", "kpi", "donnees", "reporti", "synthes"},
    {"marge", "rentabi", "couts", "cout", "demarqu", "budget", "economi", "financi"},
    {"ecart", "ecarts", "causes", "analyse", "analyser", "diagnos", "ishikaw", "pareto", "derive"},
    {"gaspill", "dechets", "vrac", "seconde", "reemplo", "ecologi", "rse", "durabil", "environ"},
    {"managem", "manager", "posture", "leaders", "pratiqu", "situati"},
    {"hierarc", "rendre", "alerte", "remonte", "signale"},
]
_FAMILLE_DE = {r: f"#f{i}" for i, fam in enumerate(FAMILLES) for r in fam}


def simplifier(phrase: str, garder_verbe: bool = True) -> str:
    """Raccourcit une phrase du REAC sans changer ses termes clés.

    * retire les compléments de remplissage (« de son périmètre »…) ;
    * retire les parenthèses explicatives longues (garde les sigles courts) ;
    * transforme « Connaissance des X » en « X » (l'objet du savoir).
    """
    s = phrase.strip().rstrip(".")
    s = re.sub(r"^(Connaissance|Connaître|Notions?)\s+(?:sur\s+|des\s+|du\s+|de la\s+|de l’|de\s+|d’)?", "", s,
               flags=re.IGNORECASE)
    s = re.sub(r"\(([^()]{28,})\)", "", s)               # parenthèses longues
    s = re.sub(r"\((ex\.?|par exemple)[^)]*\)", "", s, flags=re.IGNORECASE)
    for motif in _REMPLISSAGE:
        s = re.sub(motif, "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s+,", ",", s)
    s = re.sub(r"\s{2,}", " ", s).strip(" ,;:-")
    if not garder_verbe:
        verbe = verbe_initial(s)
        s = s[len(verbe):].strip()
    return s[:1].upper() + s[1:] if s else s


def _racine(mot: str) -> str:
    m = normaliser(mot)
    m = re.sub(r"[^a-z0-9]", "", m)
    return m[:7]


def mots_cles(phrase: str, maximum: int = 5) -> list[str]:
    """Les mots porteurs de sens d'une phrase (noms, sigles), dans l'ordre."""
    s = simplifier(phrase, garder_verbe=False)
    mots = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿœŒ’'\-]{3,}|[A-Z]{2,}", s)
    retenus: list[str] = []
    vus = set()
    for m in mots:
        m2 = re.sub(r"^(l|d|qu|s|n)[’']", "", m).strip("’'-")
        cle = normaliser(m2)
        if cle in _MOTS_VIDES or cle in vus or len(cle) < 3 or (cle.endswith("ment") and len(cle) > 6):
            continue
        if cle.endswith(("er", "ir")) and not m2.isupper() and cle not in {"manager", "dossier", "fichier"}:
            continue  # verbes à l'infinitif écartés des mots-clés
        vus.add(cle)
        retenus.append(m2 if m2.isupper() else m2.lower())
        if len(retenus) >= maximum:
            break
    return retenus


def _jetons(phrase: str) -> set[str]:
    racines = {_racine(m) for m in re.findall(r"[A-Za-zÀ-ÿœ]{3,}", phrase.replace("’", " "))
               if normaliser(m) not in _MOTS_VIDES}
    return racines | {_FAMILLE_DE[r] for r in racines if r in _FAMILLE_DE}


# ==========================================================================
# Objectif pédagogique à partir d'une ligne REAC
# ==========================================================================
_VERBES_SAVOIRS = [
    (("principe", "règle", "réglementation", "cadre légal", "obligation", "droit", "code du travail",
      "législation", "disposition"), "Expliquer"),
    (("outil", "technique", "méthode", "démarche", "procédure", "étape", "dispositif"), "Décrire"),
    (("indicateur", "ratio", "taux", "terme"), "Expliquer"),
    (("catégorie", "type", "famille", "motif", "forme", "différent", "style"), "Distinguer"),
    (("rôle", "acteur", "enjeu", "environnement", "politique", "stratégie"), "Situer"),
]


def objectif_depuis_savoir(savoir: str) -> str:
    """« Connaissance des techniques d'animation » → « Décrire les techniques d'animation »."""
    objet = simplifier(savoir)
    nobj = normaliser(objet)
    verbe = "Identifier"
    for indices, v in _VERBES_SAVOIRS:
        if any(normaliser(i) in nobj for i in indices):
            verbe = v
            break
    m = re.match(r"^(Connaissance|Connaître|Notions?)\s+(sur\s+|des\s+|du\s+|de la\s+|de l’|de\s+|d’)?",
                 savoir.strip(), re.IGNORECASE)
    art = (m.group(2) or "").strip().lower() if m else ""
    article = {"des": "les", "du": "le", "de la": "la", "de l’": "l’", "sur": "", "de": "", "d’": ""}.get(art, "")
    if objet and article:
        objet = (article + (" " if not article.endswith("’") else "") + objet[0].lower() + objet[1:])
    elif objet:
        objet = objet[0].lower() + objet[1:]
    return f"{verbe} {objet}".strip()


# ==========================================================================
# Bruner : modes de représentation + étayage + activités
# ==========================================================================
MODES_BRUNER = {
    "enactif": "Enactif (agir : mise en situation, manipulation, jeu de rôle)",
    "iconique": "Iconique (voir : schéma, carte mentale, visuel, vidéo)",
    "symbolique": "Symbolique (formaliser : concept, règle, calcul, synthèse écrite)",
}

ETAYAGE = [
    ("Enrôlement", "Accroche : situation vécue / question choc / exemple local"),
    ("Réduction des degrés de liberté", "Consigne courte, une seule tâche à la fois"),
    ("Maintien de l'orientation", "Rappel de l'objectif et du critère de réussite"),
    ("Signalisation des caractéristiques déterminantes", "Points clés mis en évidence (mots-clés REAC)"),
    ("Contrôle de la frustration", "Droit à l'erreur, aide graduée, binôme"),
    ("Démonstration", "Modèle montré par le formateur puis reproduit par le stagiaire"),
]


def mode_bruner(categorie: str, niveau: int) -> str:
    if categorie == "savoir":
        return MODES_BRUNER["iconique"] if niveau <= 2 else MODES_BRUNER["symbolique"]
    if categorie in {"technique", "organisationnel"}:
        return MODES_BRUNER["symbolique"] if niveau in (4, 5) else MODES_BRUNER["enactif"]
    if categorie == "relationnel":
        return MODES_BRUNER["enactif"]
    if categorie == "critere":
        return MODES_BRUNER["enactif"]
    return MODES_BRUNER["iconique"]


# Activités pédagogiques suggérées selon les mots du REAC (ordre = priorité)
ACTIVITES = [
    (("briefing", "débriefing", "réunion"), "Simulation de briefing de 5 min (minuteur) puis débriefing croisé"),
    (("entretien",), "Jeu de rôle en trinôme : manager / collaborateur / observateur avec grille"),
    (("conflit",), "Jeu de rôle « conflit d'équipe » + méthode DESC (Décrire-Exprimer-Spécifier-Conséquences)"),
    (("planning", "plannings", "horaire", "planifier", "rétroplanning", "gantt", "pert"),
     "Atelier tableur : construire le planning d'une semaine avec contraintes (absences, livraison)"),
    (("handicap",), "Étude de cas d'aménagement + mise en situation de simulation (lunettes, gants)"),
    (("discrimin",), "Analyse de situations courtes : discriminant ou non ? (vote, puis règle de droit)"),
    (("risque", "sécurité", "prévention", "tms", "epi", "duerp"),
     "« Chasse aux risques » sur photos de surface de vente + mini-DUERP"),
    (("recrut", "candidat", "fiche de poste", "cv"), "Analyse de 3 CV fictifs avec grille de critères"),
    (("intégration", "tutorat", "période d’essai", "nouvelle recrue"),
     "Construire le parcours d'intégration J1-J30 d'une nouvelle recrue"),
    (("stock", "commande", "inventaire", "approvisionnement", "réception", "livraison"),
     "Cas chiffré sur tableur : calcul de commande (stock, ventes, délai, stock de sécurité)"),
    (("merchandising", "implantation", "planogramme", "linéaire", "vitrine", "balisage"),
     "Atelier planogramme / visite terrain photo d'un rayon + critique"),
    (("client", "accueil", "omnicanal", "crm", "fidélis", "satisfaction"),
     "Parcours client mystère + carte d'expérience client (moments de vérité)"),
    (("argumentaire", "argument", "vente"), "Construire un argumentaire CAP (Caractéristique-Avantage-Preuve) et le jouer"),
    (("marge", "rentabilité", "coût", "démarque", "budget", "économique", "seuil"),
     "Cas chiffré : calcul de marge, démarque et seuil de rentabilité sur tableur"),
    (("indicateur", "chiffre d’affaires", "panier", "transformation", "tableau de bord", "kpi"),
     "Construire un tableau de bord (CA, panier moyen, taux de transformation) N/N-1"),
    (("écart", "analyse", "diagnostic", "ishikawa", "pareto", "cause"),
     "Diagnostic en sous-groupes : Ishikawa (5M) puis Pareto sur un cas réel"),
    (("plan d’actions", "action corrective", "actions correctives", "ajustement"),
     "Bâtir un plan d'actions SMART + tableau de suivi (qui/quoi/quand/indicateur)"),
    (("motivation", "stimulation", "challenge", "team building", "fédérer", "cohésion"),
     "Concevoir un challenge d'équipe (objectif, règles, récompense) et le pitcher"),
    (("compétence", "formation", "progression", "développement professionnel", "potentiel"),
     "Matrice de compétences de l'équipe + plan de formation individualisé"),
    (("communication", "consigne", "écoute", "questionnement"),
     "Exercice « consigne en 3 phrases » + reformulation par le binôme"),
    (("rse", "gaspillage", "déchet", "vrac", "seconde main", "réemploi", "écologique"),
     "Atelier anti-gaspillage : plan de réduction des invendus et valorisation"),
    (("numérique", "digital", "média", "réseaux sociaux", "e-réputation"),
     "Audit d'e-réputation d'une enseigne (avis Google, réseaux sociaux)"),
]

# Pistes d'exemples locaux (La Réunion) à adapter par le formateur — ce sont
# des contextes de travail, pas des données chiffrées.
EXEMPLES_LOCAUX = [
    (("stock", "commande", "approvisionnement", "rupture"),
     "Alerte cyclonique : anticiper la demande (eau, piles, conserves) et les délais de fret maritime"),
    (("livraison", "réception", "fournisseur", "anomalie"),
     "Conteneur arrivé au Port Est avec avaries : contrôler, signaler, réserver"),
    (("marge", "coût", "prix", "rentabilité"),
     "Prix de revient d'un produit importé : achat + fret + octroi de mer → impact sur la marge"),
    (("opération commerciale", "opérations commerciales", "promotion", "événement", "saison"),
     "Opération commerciale calée sur un temps fort local (Grand Raid, fêtes de fin d'année, 20 décembre)"),
    (("planning", "horaire", "imprévu", "absence"),
     "Fermeture anticipée en alerte orange cyclonique : replanifier l'équipe et informer les clients"),
    (("équipe", "intergénérationnelle", "diverse", "motivation", "fédérer"),
     "Équipe multigénérationnelle d'un supermarché de l'Est : motiver jeunes recrues et anciens"),
    (("client", "accueil", "communication"),
     "Accueil d'un client qui s'exprime en créole : adapter son langage et sa posture"),
    (("handicap",), "Accueil d'un client à mobilité réduite un samedi d'affluence en centre commercial"),
    (("risque", "sécurité", "tms", "chaleur"),
     "Mise en rayon en réserve non climatisée en plein été austral : prévenir la fatigue et les TMS"),
    (("gaspillage", "déchet", "vrac", "écologique", "rse"),
     "Fruits et légumes péi en fin de journée : réduire la casse et valoriser les invendus"),
    (("recrut", "intégration", "tutorat"),
     "Renforts saisonniers pour les fêtes : recruter et intégrer en 1 semaine"),
    (("indicateur", "chiffre d’affaires", "panier", "écart", "performance"),
     "Comparer le CA N/N-1 d'un magasin du Sud pendant une période de routes coupées"),
]


def suggestion(table, phrase: str, defaut: str = "") -> str:
    n = normaliser(phrase)
    for mots, texte in table:
        if any(normaliser(m) in n for m in mots):
            return texte
    return defaut


# ==========================================================================
# Construction des séances d'une compétence
# ==========================================================================
@dataclass
class Objectif:
    texte: str                  # objectif reformulé (verbe d'action + objet)
    verbe: str
    niveau: int
    categorie: str              # technique / organisationnel / relationnel / savoir / critere / module
    origine: str                # phrase exacte du REAC
    contenus: list[str] = field(default_factory=list)        # savoirs rattachés (simplifiés)
    mots: list[str] = field(default_factory=list)
    associes: list[str] = field(default_factory=list)        # autres lignes REAC fusionnées
    criteres: list[str] = field(default_factory=list)        # critères RE évalués
    minutes: int = 0
    mode: str = ""
    activite: str = ""
    exemple: str = ""


@dataclass
class Seance:
    titre: str                  # étape du processus REAC (simplifiée)
    origine: str
    objectifs: list[Objectif] = field(default_factory=list)
    minutes: int = 0
    numero: int = 0
    cp: int = 0
    at: int = 0
    sequence: int = 0
    sequence_titre: str = ""
    type_seance: str = "apprentissage"   # apprentissage / evaluation / module


CATEGORIES_SF = [
    ("sf_techniques", "technique"),
    ("sf_organisationnels", "organisationnel"),
    ("sf_relationnels", "relationnel"),
]

ORDRE_CATEGORIE = {"savoir": 0, "technique": 1, "organisationnel": 2, "relationnel": 3, "critere": 4, "module": 5}


def formuler(ligne: str) -> str:
    """Objectif à partir d'une ligne REAC : garde le verbe, simplifie l'objet."""
    if re.match(r"^(Connaissance|Connaître|Notions?)\b", ligne.strip(), re.IGNORECASE):
        return objectif_depuis_savoir(ligne)
    return simplifier(ligne)


def titre_etape(phrase: str) -> str:
    """Titre de séance : l'étape du processus REAC, sans la clause d'introduction."""
    s = phrase.strip()
    m = re.match(r"^(Dans le respect|En collaboration|À partir|A partir|Selon|Sous|En lien|En fonction|"
                 r"Afin|Pour|En tenant|Au regard|En cas)\b[^,]*(,[^,]*)*?,\s+(?=[a-zéèêàâîôû]+(er|ir|re)\b)", s)
    if m:
        s = s[m.end():]
    s = simplifier(s)
    if len(s) > 120:
        coupe = s[:120].rsplit(" ", 1)[0]
        s = coupe.rstrip(",;: ") + "…"
    return s


def construire_seances(cp: Competence, part_evaluation: float = 0.12) -> list[Seance]:
    """Découpe une compétence en séances (= étapes du processus REAC).

    * chaque savoir-faire devient un objectif rattaché à l'étape la plus
      proche (mots communs) ;
    * chaque savoir devient un contenu rattaché à l'objectif le plus proche
      (aucun savoir n'est perdu) ;
    * une séance finale « Entraînement à l'évaluation » reprend chaque
      critère de performance.
    """
    etapes = cp.description or [cp.intitule]
    seances = [Seance(titre=titre_etape(e), origine=e, cp=cp.numero, at=cp.at_numero) for e in etapes]
    jetons_etapes = [_jetons(e) for e in etapes]

    # Pondération IDF : un mot rare (ex. « briefing ») compte plus qu'un mot courant.
    doc_freq = Counter(j for js in jetons_etapes for j in js)

    def score(jetons: set[str], i: int) -> float:
        return sum(1.0 / doc_freq[j] for j in jetons & jetons_etapes[i])

    charge = [0] * len(seances)
    for attr, categorie in CATEGORIES_SF:
        for ligne in getattr(cp, attr):
            j = _jetons(ligne)
            scores = [score(j, i) for i in range(len(seances))]
            meilleur = max(scores) if scores else 0
            if meilleur >= 0.5:
                i = scores.index(meilleur)
            else:
                # savoir-faire transversal (ex. « Utiliser les outils bureautiques ») :
                # placé dans l'étape la moins chargée, parmi les ex-aequo du meilleur score
                candidats = [k for k in range(len(seances)) if scores[k] >= meilleur - 1e-9] or list(range(len(seances)))
                i = min(candidats, key=lambda k: charge[k])
            charge[i] += 1
            niveau = niveau_bloom(ligne)
            texte = formuler(ligne)
            niveau = niveau_bloom(texte)
            obj = Objectif(
                texte=texte, verbe=verbe_initial(texte), niveau=niveau,
                categorie=categorie, origine=ligne, mots=mots_cles(ligne),
                mode=mode_bruner(categorie, niveau),
                activite=suggestion(ACTIVITES, ligne + " " + etapes[i], "Étude de cas guidée puis application en binôme"),
                exemple=suggestion(EXEMPLES_LOCAUX, ligne + " " + etapes[i], ""),
            )
            seances[i].objectifs.append(obj)

    # Étapes restées vides : l'étape elle-même devient l'objectif.
    for s in seances:
        if not s.objectifs:
            niveau = niveau_bloom(s.titre)
            s.objectifs.append(Objectif(
                texte=s.titre, verbe=verbe_initial(s.titre), niveau=niveau, categorie="technique",
                origine=s.origine, mots=mots_cles(s.origine), mode=mode_bruner("technique", niveau),
                activite=suggestion(ACTIVITES, s.origine, "Étude de cas guidée puis application en binôme"),
                exemple=suggestion(EXEMPLES_LOCAUX, s.origine, "")))

    # Savoirs → contenus de l'objectif le plus proche (sur toute la compétence)
    tous = [(si, oi, _jetons(o.origine + " " + seances[si].origine))
            for si, s in enumerate(seances) for oi, o in enumerate(s.objectifs)]
    freq_obj = Counter(j for _, _, js in tous for j in js)
    rotation = 0
    for savoir in cp.savoirs:
        js = _jetons(savoir)
        notes = [sum(1.0 / freq_obj[j] for j in js & jo) for _, _, jo in tous]
        meilleur = max(notes) if notes else 0
        if meilleur > 0:
            k = notes.index(meilleur)
        else:
            k = rotation % len(tous)
            rotation += 1
        si, oi, _ = tous[k]
        seances[si].objectifs[oi].contenus.append(simplifier(savoir))

    # Ordre brunérien (spirale) dans chaque séance : du plus simple au plus complexe
    for s in seances:
        s.objectifs.sort(key=lambda o: (ORDRE_CATEGORIE.get(o.categorie, 9), o.niveau))

    # Séance d'entraînement à l'évaluation (critères de performance du REAC/RE)
    if cp.criteres:
        ev = Seance(titre=f"Entraînement à l'évaluation — {simplifier(cp.intitule)}",
                    origine="Critères de performance du REAC", cp=cp.numero, at=cp.at_numero,
                    type_seance="evaluation")
        for c in cp.criteres:
            ev.objectifs.append(Objectif(
                texte=f"Démontrer que : {c[0].lower() + c[1:]}", verbe="Démontrer", niveau=5,
                categorie="critere", origine=c, criteres=[c], mots=mots_cles(c),
                mode=mode_bruner("critere", 5),
                activite="Mise en situation type examen + auto-évaluation sur la grille du critère",
                exemple=suggestion(EXEMPLES_LOCAUX, c, "")))
        seances.append(ev)
    return seances


# ==========================================================================
# Répartition du temps (en minutes, par pas de 15 min)
# ==========================================================================
PAS = 15


def repartir(total: int, poids: list[float], minimum: int = PAS) -> list[int]:
    """Répartit `total` minutes selon `poids`, par pas de 15 min (plus forts restes)."""
    if not poids:
        return []
    unites = total // PAS
    somme = sum(poids) or 1
    bruts = [unites * p / somme for p in poids]
    base = [max(int(math.floor(b)), minimum // PAS if unites >= len(poids) * (minimum // PAS) else 0) for b in bruts]
    while sum(base) > unites:
        i = max(range(len(base)), key=lambda k: base[k])
        base[i] -= 1
    restes = sorted(range(len(bruts)), key=lambda k: bruts[k] - math.floor(bruts[k]), reverse=True)
    k = 0
    while sum(base) < unites:
        base[restes[k % len(restes)]] += 1
        k += 1
    return [b * PAS for b in base]


def poids_objectif(o: Objectif) -> float:
    """Temps relatif : objectif complexe et riche en contenus = plus de temps."""
    return 1.0 + 0.15 * (o.niveau - 1) + 0.35 * len(o.contenus) + 0.5 * len(o.associes)


def fusionner_si_necessaire(seance: Seance, minutes: int, minimum_par_objectif: int = 30) -> None:
    """Si une séance a trop d'objectifs pour son temps, fusionne les plus proches.

    Rien n'est supprimé : les lignes fusionnées restent visibles dans la
    colonne « Objectifs associés » (traçabilité REAC).
    """
    max_obj = max(1, minutes // minimum_par_objectif)
    while len(seance.objectifs) > max_obj:
        # fusion de deux objectifs voisins de même catégorie, au plus petit poids
        meilleur = None
        for i in range(len(seance.objectifs) - 1):
            a, b = seance.objectifs[i], seance.objectifs[i + 1]
            if a.categorie == b.categorie or meilleur is None:
                p = poids_objectif(a) + poids_objectif(b) + (0 if a.categorie == b.categorie else 5)
                if meilleur is None or p < meilleur[0]:
                    meilleur = (p, i)
        i = meilleur[1]
        a, b = seance.objectifs[i], seance.objectifs.pop(i + 1)
        if b.niveau > a.niveau:  # l'objectif le plus exigeant porte le verbe
            a.texte, b.texte = b.texte, a.texte
            a.verbe, a.niveau, a.origine, b.origine = b.verbe, b.niveau, b.origine, a.origine
        a.associes.append(b.texte if b.origine == b.texte else simplifier(b.origine))
        a.associes.extend(b.associes)
        a.contenus.extend(b.contenus)
        a.criteres.extend(b.criteres)
        for m in b.mots:
            if m not in a.mots and len(a.mots) < 7:
                a.mots.append(m)


def decouper_competence(cp: Competence, minutes_cp: int, part_evaluation: float = 0.12) -> list[Seance]:
    """Séances + durées pour une compétence disposant de `minutes_cp` minutes."""
    seances = construire_seances(cp, part_evaluation)
    eval_s = [s for s in seances if s.type_seance == "evaluation"]
    appr = [s for s in seances if s.type_seance != "evaluation"]
    m_eval = 0
    if eval_s:
        m_eval = max(PAS * 4, int(round(minutes_cp * part_evaluation / PAS)) * PAS)
        m_eval = min(m_eval, minutes_cp // 3 // PAS * PAS)
    m_appr = minutes_cp - m_eval
    durees = repartir(m_appr, [sum(poids_objectif(o) for o in s.objectifs) for s in appr], minimum=PAS * 2)
    for s, d in zip(appr, durees):
        s.minutes = d
    for s in eval_s:
        s.minutes = m_eval
    for s in seances:
        fusionner_si_necessaire(s, s.minutes)
        d_obj = repartir(s.minutes, [poids_objectif(o) for o in s.objectifs])
        for o, d in zip(s.objectifs, d_obj):
            o.minutes = d
        s.objectifs = [o for o in s.objectifs if o.minutes > 0] or s.objectifs[:1]
    return [s for s in seances if s.minutes > 0]


def poids_competences(reac: Reac) -> dict[int, float]:
    """Poids par défaut d'une CP = volume de son contenu REAC (modifiable)."""
    return {cp.numero: float(max(cp.volume(), 1)) for cp in reac.competences}
