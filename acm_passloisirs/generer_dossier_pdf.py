"""Génère le dossier de conception de la plateforme au format PDF.

Le contenu vit dans ce fichier : le régénérer après modification suffit.
    python3 acm_passloisirs/generer_dossier_pdf.py
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, KeepTogether, PageBreak, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
)

SORTIE = Path(__file__).with_name("Dossier_Plateforme_PASS_LOISIRS_2.0.pdf")

MARINE = colors.HexColor("#123C5A")
AZUR = colors.HexColor("#2E7D9A")
ARDOISE = colors.HexColor("#1F5D78")
ROUGE = colors.HexColor("#B03A2E")
VERT = colors.HexColor("#4A7C3F")
OCRE = colors.HexColor("#B8912F")
GRIS = colors.HexColor("#F2F6F8")
GRIS_BORD = colors.HexColor("#B8C8D2")

S = getSampleStyleSheet()


def style(nom, **kw):
    base = dict(fontName="Helvetica", fontSize=9.2, leading=13, textColor=colors.HexColor("#1A1A1A"))
    base.update(kw)
    return ParagraphStyle(nom, **base)


CORPS = style("corps", alignment=TA_JUSTIFY, spaceAfter=5)
H1 = style("h1", fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=MARINE, spaceBefore=14, spaceAfter=9)
H2 = style("h2", fontName="Helvetica-Bold", fontSize=12, leading=16, textColor=MARINE, spaceBefore=12, spaceAfter=6)
H3 = style("h3", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=ARDOISE, spaceBefore=9, spaceAfter=4)
PUCE = style("puce", alignment=TA_JUSTIFY, leftIndent=10, bulletIndent=2, spaceAfter=3)
MONO = style("mono", fontName="Courier", fontSize=6.5, leading=8.2, textColor=colors.HexColor("#102A36"))
CELL = style("cell", fontSize=7.6, leading=9.6)
CELL_B = style("cellb", fontName="Helvetica-Bold", fontSize=7.6, leading=9.6)
TETE = style("tete", fontName="Helvetica-Bold", fontSize=7.8, leading=9.8, textColor=colors.white)
SRC = style("src", fontSize=7.6, leading=10, textColor=colors.HexColor("#444444"))
TITRE_C = style("titrec", fontName="Helvetica-Bold", fontSize=25, leading=30, textColor=MARINE, alignment=TA_CENTER)
STITRE_C = style("stitrec", fontSize=12.5, leading=17, textColor=AZUR, alignment=TA_CENTER)
PETIT_C = style("petitc", fontSize=9, leading=13, alignment=TA_CENTER, textColor=colors.HexColor("#444444"))

flux: list = []


def p(txt, st=CORPS):
    flux.append(Paragraph(txt, st))


def h1(txt):
    flux.append(Paragraph(txt, H1))
    flux.append(Table([[""]], colWidths=[170 * mm], rowHeights=[1.6],
                      style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), MARINE)])))
    flux.append(Spacer(1, 5))


def h2(txt):
    flux.append(Paragraph(txt, H2))


def h3(txt):
    flux.append(Paragraph(txt, H3))


def puces(items):
    for it in items:
        flux.append(Paragraph(it, PUCE, bulletText="•"))
    flux.append(Spacer(1, 4))


def encadre(txt, couleur, fond):
    t = Table([[Paragraph(txt, style("enc", alignment=TA_JUSTIFY, fontSize=8.8, leading=12.4))]],
              colWidths=[168 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fond),
        ("LINEBEFORE", (0, 0), (0, -1), 3, couleur),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    flux.append(Spacer(1, 4))
    flux.append(t)
    flux.append(Spacer(1, 7))


def alerte(txt):
    encadre(txt, ROUGE, colors.HexColor("#FDF0EE"))


def avis(txt):
    encadre(txt, VERT, colors.HexColor("#F0F6EE"))


def note(txt):
    encadre(txt, OCRE, colors.HexColor("#FDF9E7"))


def schema(txt):
    lignes = [[Paragraph(l.replace(" ", "&nbsp;") or "&nbsp;", MONO)] for l in txt.strip("\n").split("\n")]
    t = Table(lignes, colWidths=[168 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5F7F9")),
        ("BOX", (0, 0), (-1, -1), 0.6, GRIS_BORD),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 0.4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.4),
    ]))
    flux.append(Spacer(1, 4))
    flux.append(t)
    flux.append(Spacer(1, 7))


def tableau(entetes, lignes, largeurs):
    data = [[Paragraph(e, TETE) for e in entetes]]
    for ligne in lignes:
        data.append([Paragraph(c, CELL) for c in ligne])
    t = Table(data, colWidths=[l * mm for l in largeurs], repeatRows=1)
    st = [
        ("BACKGROUND", (0, 0), (-1, 0), MARINE),
        ("GRID", (0, 0), (-1, -1), 0.5, GRIS_BORD),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            st.append(("BACKGROUND", (0, i), (-1, i), GRIS))
    t.setStyle(TableStyle(st))
    flux.append(Spacer(1, 3))
    flux.append(t)
    flux.append(Spacer(1, 8))


# ============================ COUVERTURE ============================
flux.append(Spacer(1, 55 * mm))
flux.append(Paragraph("Plateforme associative", TITRE_C))
flux.append(Paragraph("PASS LOISIRS 2.0", TITRE_C))
flux.append(Spacer(1, 9))
flux.append(Paragraph("Dossier de conception, d'analyse concurrentielle<br/>et de conformité juridique", STITRE_C))
flux.append(Spacer(1, 16))
flux.append(Paragraph("Phase A — Centre névralgique de l'association<br/>"
                      "Phase B — Produit pour les structures de La Réunion et de France", PETIT_C))
flux.append(Spacer(1, 26))
flux.append(Paragraph("Version 1.0 — 8 septembre 2026<br/>Pour Stan Vellard et Aurélien Lumeka", PETIT_C))
flux.append(PageBreak())

# ============================ 0. AVERTISSEMENTS ============================
h1("0. Ce que contient ce document, et ce qu'il ne contient pas")
p("Ce dossier répond à une commande précise : bâtir d'abord un centre de gestion abouti pour "
  "PASS LOISIRS (phase A), puis en faire un produit vendable à d'autres structures (phase B). "
  "Il traite l'architecture, le marché, la tarification, le droit et la fiscalité.")
alerte(
    "<b>Trois limites à connaître avant de lire.</b><br/><br/>"
    "<b>1.</b> Ce document n'est <b>ni un conseil fiscal ni un conseil juridique opposable</b>. Les analyses "
    "fiscales doivent être validées par un expert-comptable ou un avocat fiscaliste avant toute décision. "
    "Les points ouverts sont signalés comme tels.<br/><br/>"
    "<b>2.</b> Le site du BOFIP <b>n'a pas pu être consulté directement</b> : l'accès à bofip.impots.gouv.fr "
    "est bloqué par le proxy réseau de l'environnement de travail. Les références citées proviennent de "
    "résultats de recherche pointant vers les pages officielles ; elles sont exactes en identifiant et en "
    "substance, mais <b>doivent être relues sur le site officiel</b> avant tout usage contractuel.<br/><br/>"
    "<b>3.</b> Les tarifs et fonctionnalités des concurrents <b>évoluent</b>. Ceux cités datent du "
    "8 septembre 2026. Vérifiez-les avant toute communication comparative : une comparaison inexacte est "
    "une pratique commerciale trompeuse.")

# ============================ 1. PHASE A ============================
h1("1. PHASE A — Le centre névralgique de PASS LOISIRS")
h2("1.1 L'objectif")
p("Une base de données unique, complète et fiable, qui permet de gérer une journée d'accueil sans ouvrir "
  "Excel : les bons enfants, les bons montants, les bons accès. C'est le critère de réussite fixé par "
  "l'audit du 7 septembre 2026.")
p("Ce qui est déjà acquis : 26 tables structurées, la sécurité des départs calculée, la chaîne financière "
  "sans double comptage, le registre RGPD, le journal d'audit, cinq interfaces par rôle, quatre "
  "automatisations, et un noyau de sécurité applicative avec 25 contrôles au vert.")

h2("1.2 L'architecture de la phase A")
schema("""
   +--------------------------------------------------------------+
   |                        UTILISATEURS                          |
   |   Direction   Administratif   Responsable ACM   Animateur    |
   +---------------------------+----------------------------------+
                               |  HTTPS + session + MFA
   +---------------------------v----------------------------------+
   |            COUCHE SERVEUR  (FastAPI - deja ecrite)           |
   |  +------------+-------------+------------+----------------+  |
   |  |   config   | autorisation|   depart   |    limites     |  |
   |  |  secrets   | roles/IDOR  |   refuse   | debit/entrees  |  |
   |  +------------+-------------+------------+----------------+  |
   +-------+-----------------------------------+------------------+
           |                                   |
   +-------v---------+                 +-------v----------+
   |   PostgreSQL    |                 |   Stockage S3    |
   |   (manage, UE)  |                 |   (UE, chiffre)  |
   | espace illimite |                 |  pieces jointes  |
   +-------+---------+                 +------------------+
           |
   +-------v------------------------------------------------------+
   |  n8n AUTO-HEBERGE  -  usage INTERNE uniquement (voir 1.5)     |
   |  relances . exports . rapprochements . alertes                |
   +--------------------------------------------------------------+
""")

h2("1.3 Pourquoi quitter Airtable dès la phase A")
p("Airtable a été le bon atelier de conception. Il devient le mauvais outil de production, pour trois "
  "raisons mesurables :")
tableau(
    ["Contrainte", "Effet concret sur PASS LOISIRS"],
    [["Plafond d'enregistrements du plan gratuit (1 000 par base)",
      "37 enfants × 34 mercredis = <b>1 258 présences</b> pour la seule saison des mercredis. Le plafond "
      "est crevé avant Noël, sans compter échéancier, encaissements et documents."],
     ["Pas de permissions par champ ni par table sur les plans accessibles",
      "Les contrôles C02 (cloisonnement des rôles) et C09 (protection des traces) de l'audit restent "
      "<b>hors d'atteinte</b>, quelles que soient les interfaces."],
     ["Facturation par éditeur",
      "Chaque animateur qui doit saisir un pointage devient une licence. Le coût croît avec l'équipe, "
      "pas avec l'usage."]],
    [55, 113])
p("<b>La cible : PostgreSQL managé chez un hébergeur européen.</b> Pas de limite de lignes, contraintes "
  "d'intégrité réelles (clés étrangères, contrôle des montants, unicité anti-doublon), permissions au "
  "niveau du serveur, et coût indépendant du nombre d'utilisateurs.")

h2("1.4 Le rôle exact de Baserow")
p("Baserow répond à la demande « le plus d'espace possible » et à l'exigence de souveraineté. Trois faits :")
puces([
    "<b>Le cœur est sous licence MIT</b> — base de données, automatisations, constructeur d'applications "
    "et tableaux de bord. Usage commercial, modification et redistribution autorisés sans restriction.",
    "<b>La version auto-hébergée n'a aucune limite</b> de lignes, de stockage ni de requêtes API. C'est la "
    "réponse directe à votre besoin d'espace.",
    "<b>Les répertoires premium et enterprise sont propriétaires</b> : journaux d'audit, authentification "
    "unique SAML et gestion fine des rôles ne s'activent qu'avec un abonnement payant par utilisateur.",
])
note("<b>Recommandation nuancée.</b> Baserow est excellent comme <i>outil interne</i> en phase A : il "
     "remplace Airtable sans limite d'espace, sur un cloud européen ou auto-hébergé. Il n'est <b>pas</b> le "
     "bon socle pour le produit de phase B : on ne vend pas une plateforme haut de gamme construite sur une "
     "base sans-code dont on ne maîtrise ni le rythme de version, ni l'ergonomie, ni le modèle de licence "
     "des fonctions de gouvernance. En phase B, l'application est écrite et PostgreSQL est utilisé "
     "directement.")

h2("1.5 n8n — un piège juridique à connaître avant d'investir")
alerte("<b>Point critique.</b> n8n n'est pas un logiciel libre au sens habituel. Il est publié sous "
       "<i>Sustainable Use License</i>, qui restreint l'usage à des « fins internes à l'entreprise ». Deux "
       "usages sont explicitement interdits sans licence commerciale négociée : <b>héberger n8n et faire "
       "payer l'accès</b>, et la <b>marque blanche</b> — proposer n8n sous votre nom à vos clients contre "
       "rémunération. En revanche, la licence <b>autorise</b> l'usage interne illimité, ainsi que la "
       "facturation de prestations de conseil ou de support : construire des workflows n8n pour un client "
       "reste parfaitement légal.")
tableau(
    ["Usage", "Statut", "Ce qu'il faut faire"],
    [["n8n pour automatiser PASS LOISIRS en interne (phase A)", "<b>Autorisé</b>",
      "Rien. Auto-hébergez : c'est conforme et souverain."],
     ["n8n intégré au produit vendu aux autres structures (phase B)", "<b>Interdit</b> sans licence",
      "Négocier une licence commerciale ou <i>embed</i> avec n8n — ou retenir l'alternative ci-dessous."],
     ["Vendre du conseil et des workflows n8n à des clients", "<b>Autorisé</b>",
      "C'est même une offre de service à part entière."]],
    [62, 32, 74])
p("<b>Alternative pour la phase B :</b> les automatisations du produit sont écrites <i>dans</i> "
  "l'application (tâches planifiées côté serveur), et non déléguées à un moteur tiers. C'est plus de "
  "travail au départ, mais cela supprime la dépendance de licence, le coût par client et une surface "
  "d'attaque.")

h2("1.6 RGPD et IA Act en phase A")
p("<b>RGPD.</b> Les huit points ouverts du registre restent bloquants : responsable de traitement, AIPD, "
  "région d'hébergement, contrat de sous-traitance, mécanisme de transfert, qualification HDS, définition "
  "de la fin d'accueil, bases légales des sept finalités. Aucun formulaire public ne peut ouvrir tant que "
  "les bases légales sont à « À QUALIFIER » : sans elles, la notice d'information est littéralement "
  "inécrivable.")
p("<b>IA Act.</b> Aucun composant de la phase A n'est un système d'IA : les calculs de tarif et de planning "
  "sont déterministes, et l'audit rappelle qu'aucune conformité IA Act n'en découle. n8n n'y change rien "
  "tant qu'il n'appelle pas de modèle. Dès qu'un nœud d'IA est ajouté, une qualification est à refaire et "
  "le test d'injection indirecte devient obligatoire.")

h2("1.7 Budget de la phase A")
tableau(
    ["Poste", "Fournisseur (souveraineté UE)", "Ordre de grandeur mensuel"],
    [["Serveur applicatif", "Scaleway (Paris), Clever Cloud, OVHcloud", "15 – 40 €"],
     ["PostgreSQL managé", "Scaleway Database, OVHcloud", "15 – 50 €"],
     ["Stockage objet (pièces jointes)", "Scaleway Object Storage", "1 – 5 €"],
     ["Envoi d'e-mails transactionnels", "Brevo, Scaleway TEM (éditeurs français)", "0 – 25 €"],
     ["n8n auto-hébergé", "sur le serveur applicatif", "0 €"],
     ["Sauvegardes externalisées", "autre région du même hébergeur", "5 – 10 €"],
     ["Nom de domaine", "OVHcloud, Gandi", "≈ 2 €"],
     ["<b>TOTAL PHASE A</b>", "", "<b>40 – 130 € / mois</b>"]],
    [50, 78, 40])
p("Ordres de grandeur au 8 septembre 2026, à vérifier sur les grilles tarifaires : elles évoluent. Si la "
  "qualification HDS conclut à l'obligation d'un hébergeur certifié, compter 200 à 500 €/mois — c'est une "
  "décision budgétaire, pas technique.", SRC)

flux.append(PageBreak())

# ============================ 2. PHASE B ============================
h1("2. PHASE B — Le produit pour les autres structures")
h2("2.1 Le marché réel : qui est déjà là")
p("Le marché se divise en deux mondes qui ne se parlent pas. C'est la donnée stratégique la plus importante "
  "de ce dossier.")

h3("Monde 1 — La gestion associative généraliste")
tableau(
    ["Acteur", "Modèle", "Forces", "Faiblesses"],
    [["<b>HelloAsso</b>", "Outils entièrement gratuits, sans frais ni commission ; contribution volontaire "
      "laissée par le payeur", "Gratuité totale ; notoriété massive ; paiement en ligne intégré",
      "Centré sur le paiement et la collecte ; gestion métier limitée ; aucune verticale enfance-jeunesse"],
     ["<b>AssoConnect</b>", "Sur devis, par palier de contacts",
      "Couverture large : adhérents, dons, compta, site web",
      "Prix opaque et croissant avec la base ; application mobile limitée à l'encaissement ; généraliste, "
      "donc jamais précis sur un métier"],
     ["<b>Yapla</b>", "Gratuit puis ≈ 24 €/mois", "Entrée de gamme accessible",
      "Fonctionnalités métier limitées"],
     ["<b>Pep's Up, Basicompta,<br/>Subventia, HopAsso</b>", "65 à 490 €/an",
      "Bon marché, ciblés (compta, subventions)", "Périmètre étroit ; obligent à empiler plusieurs outils"]],
    [30, 40, 45, 53])

h3("Monde 2 — La gestion enfance / ALSH / périscolaire")
tableau(
    ["Acteur", "Cible", "Forces", "Faiblesses"],
    [["<b>Berger-Levrault</b><br/>(BL.enfance)", "Collectivités",
      "Suite complète petite enfance, périscolaire, ALSH, restauration ; solidité institutionnelle",
      "Conçu pour les mairies ; lourd, cher, long à déployer ; inadapté à une association de 37 enfants"],
     ["<b>AIGA</b> (iNoé)", "Centres de loisirs, centres sociaux, MJC, services jeunesse",
      "Très proche du métier ; conforme aux exigences CAF ; pointage ALSH, périscolaire, cantine",
      "Ergonomie datée ; orienté structures déjà équipées ; peu de souplesse"],
     ["<b>Abelium (Domino),<br/>JVS-Mairistem, Ciril</b>", "Collectivités",
      "Largement déployés ; intégrés aux SI municipaux",
      "Univers collectivité ; procédures d'achat public ; hors de portée d'une petite association"],
     ["<b>Iloïse, AniApps</b>", "ALSH associatifs et municipaux",
      "Plus légers ; portail famille ; en ligne",
      "Notoriété faible ; couverture partielle ; peu ou pas d'ancrage ultramarin"]],
    [30, 33, 50, 55])

avis("<b>Ce que cette carte révèle.</b> Le monde 1 est saturé et son leader est gratuit : attaquer "
     "HelloAsso frontalement est perdu d'avance. Le monde 2 est occupé par des éditeurs qui vendent aux "
     "<b>collectivités</b>, pas aux <b>associations gestionnaires</b>. Entre les deux, il y a un trou : "
     "l'association qui gère un ACM est trop complexe pour HelloAsso et trop petite pour Berger-Levrault. "
     "<b>C'est exactement la place de PASS LOISIRS — et donc votre marché.</b>")

h2("2.2 Les douleurs réelles du secteur associatif")
p("Des chiffres, pas des impressions. Sources en fin de document.")
tableau(
    ["Douleur constatée", "Chiffre", "Réponse produit"],
    [["Fragilité financière", "En 2025, <b>29 %</b> des associations sans salariés et <b>53 %</b> des "
      "associations employeuses jugent leur situation financière difficile ou très difficile",
      "Prix bas, sans engagement, sans coût caché. Une association qui doute doit pouvoir arrêter sans "
      "pénalité."],
     ["Réduction d'activité", "Plus de <b>60 000</b> associations envisageaient de réduire leurs activités",
      "Facturation à l'usage réel (nombre d'adhérents suivis), pas au forfait fixe."],
     ["Érosion du bénévolat", "<b>34 %</b> de Français bénévoles en 2025, contre 38 % en 2019 et 40 % en 2013",
      "Chaque heure administrative économisée est une heure rendue au terrain. C'est l'argument de vente n°1."],
     ["Lourdeur administrative", "Exigences « complexes et chronophages, difficiles à satisfaire pour des "
      "dirigeants non professionnels »",
      "Zéro paramétrage à l'installation. La structure est utilisable le jour de l'inscription."],
     ["Épuisement des dirigeants", "Difficulté à trouver des candidats aux instances, jugées « lourdes, "
      "chronophages et effrayantes en responsabilité »",
      "Le produit porte la conformité (RGPD, traçabilité, sécurité des départs) à la place du dirigeant."],
     ["Contraction des financements", "Ligne « jeunesse et vie associative » réduite de <b>26 %</b> dans le "
      "projet de loi de finances 2026",
      "Un outil qui coûte moins qu'il ne fait économiser, et qui le démontre chiffres à l'appui."]],
    [36, 62, 70])

h2("2.3 Positionnement recommandé")
schema("""
  CE QU'IL NE FAUT PAS FAIRE          CE QU'IL FAUT FAIRE
  --------------------------          ----------------------------------
  " La plateforme de toutes           " Le logiciel des associations qui
    les associations de France "        accueillent des enfants et des jeunes "

  -> face a HelloAsso (gratuit)       -> face a Berger-Levrault et AIGA,
     et AssoConnect (installe)           qui visent les collectivites
  -> aucun avantage distinctif        -> vous avez le metier, un client
  -> budget marketing hors de            pilote, un audit de securite,
     portee d'une equipe de deux         et personne en face a La Reunion

            ELARGIR ENSUITE, PAR CERCLES CONCENTRIQUES
   ACM/periscolaire -> clubs de sport -> centres sociaux -> associations
   (memes besoins : adherents, presence, securite des mineurs, facturation)
""")
p("Les structures que vous citez — SPL, clubs de sport, collectivités — partagent le même noyau "
  "fonctionnel : des adhérents mineurs, des présences à pointer, des responsables légaux à joindre, des "
  "documents à jour et une facturation périodique. <b>Une même base métier les sert toutes</b>, à condition "
  "de commencer par une seule et de la faire parfaitement.")

h2("2.4 Architecture multi-structures")
schema("""
                        +--------------------------+
                        |  SITE PUBLIC (vitrine)   |
                        |  demo . tarifs . contact |
                        +------------+-------------+
                                     |
   +---------------------------------v---------------------------------+
   |                     APPLICATION (une seule)                       |
   |                                                                   |
   |   Chaque requete porte un organisme_id VERIFIE COTE SERVEUR       |
   |   - jamais transmis ni choisi par le navigateur                   |
   |                                                                   |
   |   +----------+  +----------+  +----------+  +----------+          |
   |   | Structure|  | Structure|  | Structure|  | Structure|   ...    |
   |   |    001   |  |    002   |  |    003   |  |    004   |          |
   |   | PASS LOI.|  | Club foot|  |  Centre  |  | Collec-  |          |
   |   |          |  |          |  |  social  |  | tivite   |          |
   |   +----------+  +----------+  +----------+  +----------+          |
   +-------------------------------+-----------------------------------+
                                   |
                    +--------------v--------------+
                    |  PostgreSQL - UNE base      |
                    |  organisme_id sur TOUTES    |
                    |  les tables + Row Level     |
                    |  Security (isolation SQL)   |
                    +-----------------------------+

   TEST D'ISOLATION OBLIGATOIRE avant tout deuxieme client :
   creer deux structures fictives et prouver qu'AUCUN chemin
   - API, export, recherche, piece jointe, e-mail, message d'erreur -
   ne laisse fuir une donnee de l'une vers l'autre.
""")
note("<b>La décision à prendre dès la première ligne de schéma :</b> mettre <font face='Courier'>"
     "organisme_id</font> dans toutes les tables, <i>même avec une seule valeur</i> pendant toute la "
     "phase A. C'est gratuit aujourd'hui et c'est six mois de travail si vous l'ajoutez après.")

h2("2.5 Le socle technique complet")
tableau(
    ["Couche", "Choix recommandé", "Pourquoi"],
    [["Base de données", "PostgreSQL 16+ managé, région UE",
      "Espace illimité, intégrité réelle, Row Level Security pour l'isolation multi-structures"],
     ["API et logique métier", "Python + FastAPI",
      "Le noyau de sécurité est déjà écrit et testé ; performance suffisante ; recrutement facile"],
     ["Interface", "Rendu serveur (Jinja) + HTMX, ou Next.js si équipe étoffée",
      "Rapide sur mobile en 4G ; pas de chaîne de compilation à maintenir ; accessible par construction"],
     ["Fichiers", "Stockage objet UE, servi <b>uniquement</b> par une route serveur",
      "Corrige la faille des URL de pièces jointes consommables hors habilitation"],
     ["E-mails", "Brevo ou Scaleway TEM", "Éditeurs français ; contrat de sous-traitance disponible"],
     ["Authentification", "Sessions serveur + MFA ; SSO plus tard", "Simple, éprouvé, sans dépendance externe"],
     ["Automatisations", "Tâches planifiées <b>dans</b> l'application",
      "Évite la restriction de licence n8n en phase B (voir 1.5)"],
     ["Supervision", "Solution auto-hébergée ou région UE",
      "Les traces d'erreur contiennent des données personnelles"],
     ["Code", "Dépôt privé, propriété de l'entité porteuse", "Exigence de réversibilité de l'audit (G01)"]],
    [34, 58, 76])

h2("2.6 Qualité perçue : ce qui fait « haut de gamme »")
p("Vous citez Airbnb et Amazon. Ce qui rend ces produits crédibles n'est pas le graphisme, c'est la "
  "<b>constance</b>. Traduction concrète et vérifiable :")
tableau(
    ["Exigence", "Critère mesurable"],
    [["Responsive — non négociable", "Tout parcours critique utilisable à une main sur un téléphone de "
      "5 ans, en 4G. Le pointage du mercredi matin se fait debout, pas assis."],
     ["Fluidité", "Moins de 200 ms de réponse serveur sur les pages courantes ; moins de 2 s d'affichage "
      "complet en 4G."],
     ["Intuitivité", "Un animateur qui n'a jamais vu l'outil fait son premier appel sans formation ni "
      "notice. À tester avec une vraie personne, chronomètre en main."],
     ["Accessibilité", "Contraste suffisant, navigation clavier complète, libellés explicites, "
      "compatibilité lecteur d'écran sur les parcours critiques. Référentiel RGAA comme repère technique."],
     ["Zéro paramétrage initial", "Une structure crée son compte et inscrit son premier adhérent en moins "
      "de 15 minutes, sans appel au support."],
     ["Fiabilité", "Sauvegarde quotidienne, restauration testée, page de statut publique, procédure de "
      "secours papier."]],
    [45, 123])
avis("<b>L'accessibilité est votre différenciateur, pas une contrainte.</b> Aurélien Lumeka est référent "
     "handicap en organisme de formation. Aucun concurrent de cette liste n'en fait un argument. Une "
     "plateforme réellement accessible, testée avec des personnes concernées, est à la fois un devoir "
     "moral, un argument commercial et un critère de plus en plus regardé dans les financements publics.")

h2("2.7 Tarification")
p("Trois contraintes croisées : les associations sont fauchées, elles ne récupèrent pas la TVA, et "
  "HelloAsso a habitué le marché à la gratuité.")
alerte("<b>Conséquence fiscale directe sur votre pricing.</b> Une association non assujettie à la TVA "
       "<b>ne récupère pas</b> la TVA qu'elle paie. Un prix affiché hors taxes est donc trompeur pour "
       "elle : son coût réel est le TTC. <b>Affichez systématiquement le prix TTC</b>, avec le HT en "
       "mention secondaire. C'est un signe de respect du client, et cela évite une déception à la "
       "première facture.")
tableau(
    ["Offre", "Cible", "Prix indicatif TTC", "Contenu"],
    [["<b>Découverte</b>", "Toute structure", "0 €",
      "Jusqu'à 15 adhérents. Toutes les fonctions. Pas de carte bancaire. Sert de démonstration réelle, "
      "pas de version amputée."],
     ["<b>Association</b>", "ACM, clubs, centres sociaux", "≈ 29 – 49 € / mois",
      "Jusqu'à 150 adhérents, utilisateurs illimités, portail familles, documents, facturation, sécurité "
      "des départs."],
     ["<b>Structure</b>", "Plusieurs accueils", "≈ 79 – 129 € / mois",
      "Multi-sites, statistiques consolidées, exports comptables, support prioritaire."],
     ["<b>Collectivité</b>", "Communes, SPL", "Sur devis",
      "Marché public, engagements de service, interfaçage SI, hébergement dédié."]],
    [26, 36, 33, 73])
p("<b>Principes de tarification à tenir :</b>")
puces([
    "<b>Facturer les adhérents, jamais les utilisateurs.</b> Faire payer chaque animateur décourage "
    "l'usage — c'est l'erreur d'Airtable transposée. Une structure doit pouvoir donner un accès à tous ses "
    "bénévoles sans y penser.",
    "<b>Aucun coût caché.</b> Pas de frais de mise en service, pas de supplément par module, pas de "
    "facturation à l'export.",
    "<b>Sans engagement, réversibilité incluse.</b> Un export complet et documenté à tout moment. "
    "Paradoxalement, c'est ce qui rassure et fait signer.",
    "<b>Tarif solidaire assumé</b> pour les toutes petites structures : il coûte peu et construit la "
    "réputation, seul canal d'acquisition réaliste dans le milieu associatif.",
])

h2("2.8 Juridique et fiscal — le montage à ne pas rater")
h3("2.8.1 Qui vend ? Le risque de lucrativité de l'association")
alerte("<b>Danger principal du projet.</b> Si l'association PASS LOISIRS commercialise elle-même le "
       "logiciel, elle exerce une activité lucrative. Le régime fiscal de faveur des organismes sans but "
       "lucratif repose sur des conditions strictes ; les dépasser expose l'association aux impôts "
       "commerciaux (impôt sur les sociétés, TVA, cotisation foncière des entreprises) — <b>y compris sur "
       "ses activités associatives</b> si la sectorisation n'est pas correctement organisée.")
p("La franchise des impôts commerciaux suppose <b>trois conditions cumulatives</b> :")
puces([
    "la gestion de l'organisme demeure <b>désintéressée</b> ;",
    "les activités non lucratives restent <b>significativement prépondérantes</b> ;",
    "les recettes d'exploitation encaissées dans l'année au titre des activités lucratives n'excèdent pas "
    "le seuil légal — <b>80 011 € au 1<sup>er</sup> janvier 2025</b>, indexé chaque année sur la prévision "
    "d'inflation de la loi de finances.",
])
p("Le caractère lucratif s'apprécie aussi au regard de la concurrence avec le secteur commercial, selon la "
  "méthode dite <b>des « 4 P »</b> : Produit, Public, Prix, Publicité. Vendre un logiciel à des "
  "collectivités et à des clubs, dans les mêmes conditions qu'un éditeur privé, coche les quatre.")
p("<b>Montage recommandé :</b>")
schema("""
   +-------------------------+         +------------------------------+
   |  ASSOCIATION            |         |  SOCIETE COMMERCIALE         |
   |  PASS LOISIRS           |<--------+  (YEBA FORMATIONS ou         |
   |                         | contrat |   structure ad hoc dediee)   |
   |  . CLIENTE du logiciel  | de      |                              |
   |  . terrain d'experience | presta- |  . edite et vend le produit  |
   |  . reference commerciale| tion    |  . porte la RC professionnelle|
   |  . reste NON LUCRATIVE  |         |  . assume l'IS et la TVA     |
   +-------------------------+         +------------------------------+

   /!\\  La contribution de Stan au produit doit etre FORMALISEE :
        association d'actionnaires, contrat d'apport, ou remuneration.
        Une contribution informelle est une source de conflit certaine
        le jour ou le produit vaut quelque chose.
""")

h3("2.8.2 Votre statut RGPD change")
p("Dès la première structure cliente, le rapport juridique s'inverse :")
tableau(
    ["Phase", "Responsable de traitement", "Votre rôle", "Documents obligatoires"],
    [["A — PASS LOISIRS seul", "L'association", "Sous-traitant (si vous traitez sur instruction)",
      "Contrat article 28 entre vous et l'association"],
     ["B — Produit", "<b>Chaque structure cliente</b>", "Sous-traitant de chacune",
      "Contrat article 28 <b>par client</b>, CGU, CGV, politique de confidentialité, registre des "
      "traitements en tant que sous-traitant, procédure de notification de violation vers vos clients, "
      "garanties de réversibilité"]],
    [30, 36, 40, 62])

h3("2.8.3 Obligations à ne pas oublier")
puces([
    "<b>Assurance responsabilité civile professionnelle</b> couvrant l'édition de logiciel et le préjudice "
    "immatériel. Un défaut qui laisse partir un enfant avec la mauvaise personne n'est pas un incident "
    "informatique.",
    "<b>Mentions légales et identification de l'éditeur</b> sur le site, conformément aux obligations de la "
    "loi pour la confiance dans l'économie numérique.",
    "<b>CGV</b> précisant durée, résiliation, disponibilité, support, propriété des données et modalités de "
    "restitution.",
    "<b>Pas de clause abusive</b> : une clause limitant excessivement votre responsabilité ou verrouillant "
    "les données du client peut être réputée non écrite.",
    "<b>Marché public</b> pour les collectivités : un régime d'achat distinct, avec ses seuils et ses "
    "procédures. À anticiper avant de démarcher une commune.",
    "<b>Qualification HDS</b> si des données de santé sont traitées : à trancher au cas par cas, sans "
    "conclusion automatique dans un sens ou dans l'autre.",
])

h3("2.8.4 IA Act")
p("Aucune fonction d'IA n'est prévue au socle, et les calculs déterministes n'en sont pas. Trois "
  "précautions si vous en ajoutez :")
puces([
    "obligation de <b>transparence</b> : l'utilisateur doit savoir qu'il parle à une IA ;",
    "<b>aucune fonction de profilage, d'admission, de discipline ou de biométrie</b> sur des mineurs sans "
    "une nouvelle qualification complète — c'est le territoire du haut risque ;",
    "un contenu écrit par un utilisateur <b>n'est jamais une instruction</b> : test d'injection indirecte "
    "obligatoire avant activation.",
])

flux.append(PageBreak())

# ============================ 3. FEUILLE DE ROUTE ============================
h1("3. Feuille de route")
schema("""
 MOIS   PHASE                        JALON DE SORTIE (bloquant)
 -----  ---------------------------  ------------------------------------
 0-1    Lever les verrous            8 parametres RGPD renseignes
        (aucun code)                 Matrice de roles signee par Stan
                                     Montage juridique tranche
 -----  ---------------------------  ------------------------------------
 1-3    Fondations techniques        Restauration TESTEE et datee
        PostgreSQL + API + domaine   organisme_id present partout
 -----  ---------------------------  ------------------------------------
 3-4    Pilote ferme, 5 familles     5 cycles complets sans incident
                                     L'equipe prefere l'outil a Excel
 -----  ---------------------------  ------------------------------------
 4-8    PASS LOISIRS complet (37)    Une saison tenue sans Excel
        <- FIN DE LA PHASE A         22 tests metier + 12 controles OK
 -----  ---------------------------  ------------------------------------
 8-12   Industrialisation            Test d'isolation multi-structures
        CGU/CGV/art.28/RC pro        Contrats prets a signer
 -----  ---------------------------  ------------------------------------
 12-15  2 structures pilotes         2 clients payants satisfaits
        (gratuit contre retours)     Support tenu par une personne
 -----  ---------------------------  ------------------------------------
 15-24  Ouverture Reunion            10 a 20 structures
        puis metropole               Rentabilite du poste support
""")
p("<b>Règle absolue :</b> aucun passage au jalon suivant tant que le critère de sortie n'est pas atteint. "
  "C'est le seul garde-fou qui tienne quand la pression commerciale arrive.")

h1("4. Budget consolidé")
tableau(
    ["Palier", "Infrastructure", "Juridique et assurance", "Total annuel indicatif"],
    [["Phase A (PASS LOISIRS)", "500 – 1 600 €",
      "Conseil RGPD + AIPD : 1 500 – 4 000 € (une fois)", "<b>2 000 – 5 600 €</b>"],
     ["Phase B — lancement", "1 200 – 3 000 €",
      "CGU/CGV/art. 28 : 2 000 – 5 000 €<br/>RC pro : 600 – 1 500 €/an", "<b>4 000 – 9 500 €</b>"],
     ["Phase B — 20 clients", "3 000 – 6 000 €",
      "RC pro + veille : 1 500 – 3 000 €/an", "<b>5 000 – 9 000 €</b>"]],
    [40, 34, 56, 38])
p("Hors temps de développement. Ces montants n'incluent ni votre rémunération ni celle de Stan — c'est le "
  "poste le plus lourd, et il doit être arbitré explicitement.", SRC)
p("<b>Seuil de rentabilité indicatif :</b> à 39 € TTC par mois et par structure, 20 structures représentent "
  "environ 9 360 € TTC par an — soit la couverture des coûts d'exploitation, sans rémunération. La "
  "rentabilité réelle commence vers 50 à 80 structures. <b>C'est le chiffre à garder en tête avant "
  "d'annoncer un calendrier.</b>")

flux.append(PageBreak())

# ============================ 5. AVIS ============================
h1("5. Avis franc sur le projet")
p("Vous me demandez mon avis. Le voici, sans enrobage : <b>le projet est solide, l'ambition est mal "
  "calibrée, et une erreur de cadrage vous coûterait un an.</b>")

h2("5.1 Ce qui est solide")
puces([
    "Vous avez un <b>client pilote réel</b> avec un besoin réel. La plupart des projets logiciels démarrent "
    "sans cela et meurent de deviner.",
    "Vous avez un <b>audit de sécurité indépendant</b> déjà réalisé, et ses corrections déjà appliquées. "
    "C'est un actif commercial : aucun concurrent de cette taille ne peut montrer cela.",
    "Vous avez une <b>connaissance métier</b> qui ne s'achète pas : la sécurité des départs, les tarifs "
    "fratrie, l'alternance des mercredis, les pièces obligatoires.",
    "Vous êtes <b>à La Réunion</b>, où aucun éditeur national n'a d'ancrage local. La proximité est un "
    "avantage réel sur ce marché.",
])

h2("5.2 Ce qui est mal calibré")
alerte("<b>La comparaison avec Airbnb et Amazon vous induit en erreur sur la stratégie.</b> Ces "
       "plateformes sont des places de marché à effet de réseau : chaque nouvel utilisateur augmente la "
       "valeur pour tous les autres, ce qui finance une croissance explosive. <b>Un logiciel de gestion "
       "associative n'a aucun effet de réseau.</b> La deuxième association cliente n'apporte rien à la "
       "première. La croissance y est linéaire, portée par la réputation et le support — pas virale. "
       "Viser « la référence de l'associatif en France » avec ce modèle et une équipe de deux, c'est "
       "confondre deux métiers.")
p("<b>Le vrai risque n'est pas technique, il est commercial :</b> HelloAsso est gratuit. Aucune association "
  "ne paiera pour ce que HelloAsso fait déjà pour rien. Votre valeur ne peut donc pas être « gérer une "
  "association » — elle doit être <b>« gérer l'accueil d'enfants mineurs en sécurité et en conformité »</b>, "
  "ce que ni HelloAsso ni AssoConnect ne font, et ce que Berger-Levrault ne vend qu'aux mairies.")

h2("5.3 Ce que je ferais à votre place")
puces([
    "<b>Renoncer à « l'associatif » comme cible et assumer une verticale.</b> « Le logiciel des structures "
    "qui accueillent des enfants. » Plus étroit, donc crédible, donc vendable. On élargit après, jamais "
    "avant.",
    "<b>Ne pas construire le produit avant d'avoir tenu une saison complète</b> avec PASS LOISIRS. Une "
    "saison réelle révèle des cas que douze mois de réunions n'inventeront pas.",
    "<b>Trancher le montage juridique maintenant</b>, pendant que le produit ne vaut rien. Qui possède le "
    "code, qui vend, comment Stan est rémunéré. Ces conversations sont faciles aujourd'hui et impossibles "
    "dans deux ans.",
    "<b>Régler la question n8n avant de l'intégrer au produit.</b> Construire la phase B sur n8n sans "
    "licence commerciale, c'est bâtir sur un terrain qui n'est pas à vous.",
    "<b>Faire de la conformité l'argument de vente, pas une contrainte.</b> Vous construisez le seul outil "
    "du marché qui pourra dire à une association : « voici notre audit, voici notre registre, voici nos "
    "tests de sécurité ». Dans un secteur qui traite des données de mineurs et qui a peur du RGPD, "
    "<b>c'est cela, votre Airbnb.</b>",
])
avis("<b>En une phrase.</b> Vous n'avez pas besoin de devenir la référence de l'associatif français. Vous "
     "avez besoin de devenir <b>la référence des accueils collectifs de mineurs à La Réunion</b> — une "
     "trentaine de structures suffisent à valider le modèle. Si vous y arrivez, la métropole devient une "
     "question d'exécution, pas de pari. Si vous visez la France d'emblée, vous n'aurez ni l'une ni l'autre.")

flux.append(PageBreak())

# ============================ 6. SOURCES ============================
h1("6. Sources")
p("<b>Fiscalité — BOFIP.</b> Références consultées via moteur de recherche le 8 septembre 2026 ; l'accès "
  "direct au site a été bloqué par le proxy réseau. <b>À relire sur bofip.impots.gouv.fr avant tout usage "
  "contractuel.</b><br/>"
  "• BOI-IS-CHAMP-10-50-20-20 — Organismes réalisant des activités lucratives accessoires : franchise<br/>"
  "• BOI-IS-CHAMP-10-50-10-10 — Conditions d'assujettissement des organismes privés<br/>"
  "• BOI-TVA-CHAMP-30-10-30-10 — Organismes sans but lucratif, principes généraux<br/>"
  "• BOI-IF-CFE-10-20-20-20 — Activités sans but lucratif et cotisation foncière des entreprises<br/>"
  "• ACTU-2025-00045 — Mise à jour du montant de la franchise des impôts commerciaux", SRC)
p("<b>Licences logicielles.</b><br/>"
  "• n8n — Sustainable Use License : docs.n8n.io/sustainable-use-license/ ; docs.n8n.io/n8n-community-license<br/>"
  "• Baserow — modèle open-core, licence MIT du cœur : baserow.io/faq ; github.com/baserow/baserow ; "
  "baserow.io/user-docs/self-hosted-licenses", SRC)
p("<b>Marché — gestion enfance et ALSH.</b><br/>"
  "• Berger-Levrault, BL.enfance : berger-levrault.com/fr/produit/bl-enfance/<br/>"
  "• AIGA, iNoé Animation : aiga.fr<br/>"
  "• Iloïse : iloise.net/gamme-iloise/alsh.html — AniApps : aniapps.fr<br/>"
  "• Panorama comparatif : accueildeloisirs.com/logiciel-enfance", SRC)
p("<b>Marché — gestion associative généraliste.</b><br/>"
  "• Comparatifs HelloAsso / AssoConnect / HopAsso : assoft.fr ; tool-advisor.fr ; getapp.fr ; "
  "clictreso.fr ; subventia.ai", SRC)
p("<b>Situation du secteur associatif.</b><br/>"
  "• Associations.gouv.fr — L'opinion des responsables associatifs 2026<br/>"
  "• Recherches &amp; Solidarités — La France bénévole 2026 (avec le soutien de la MAIF)<br/>"
  "• Le Mouvement associatif — Note d'analyse du projet de loi de finances 2026, octobre 2025<br/>"
  "• Sénat — Questions écrites sur les difficultés administratives des bénévoles (2025) et sur les "
  "difficultés du secteur associatif (2026)<br/>"
  "• Institut ISBL — Associations en 2025 : l'urgence d'agir", SRC)
p("<b>Document interne de référence.</b><br/>"
  "• Audit ACM PASS LOISIRS — Sécurité, RGPD, IA Act — 7 septembre 2026, 24 pages (constats S01–S07, "
  "M01–M06, J01–J07, G01–G02 ; tests T01–T22 ; contrôles C01–C12 ; lots L1–L7)", SRC)
flux.append(Spacer(1, 14))
p("Document de travail interne — Version 1.0 du 8 septembre 2026. Les analyses fiscales et juridiques "
  "doivent être validées par un professionnel qualifié avant toute décision engageant l'association ou "
  "la société.", SRC)


# ============================ RENDU ============================
def decor(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(MARINE)
    canvas.rect(0, A4[1] - 12 * mm, A4[0], 12 * mm, stroke=0, fill=1)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.setFillColor(colors.white)
    canvas.drawString(20 * mm, A4[1] - 8 * mm, "PLATEFORME ASSOCIATIVE — PASS LOISIRS 2.0")
    canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 8 * mm, "08.09.2026")
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(20 * mm, 10 * mm, "Dossier de conception — Confidentiel")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "page %d" % doc.page)
    canvas.setStrokeColor(GRIS_BORD)
    canvas.line(20 * mm, 13 * mm, A4[0] - 20 * mm, 13 * mm)
    canvas.restoreState()


doc = BaseDocTemplate(str(SORTIE), pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=18 * mm, bottomMargin=16 * mm,
                      title="Plateforme associative PASS LOISIRS 2.0",
                      author="Dossier de conception")
cadre = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
doc.addPageTemplates([PageTemplate(id="std", frames=[cadre], onPage=decor)])
doc.build(flux)
print(f"PDF genere : {SORTIE}")
