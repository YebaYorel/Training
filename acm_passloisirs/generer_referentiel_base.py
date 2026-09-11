#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère le référentiel complet de la base PASS LOISIRS 2.0, table par table
et champ par champ, à partir du schéma réel exporté depuis Airtable.

Destiné à Stan : comprendre à quoi sert chaque table, chaque champ, ce que la
base fait de fort, et ce qu'il reste à améliorer.
"""

import json
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether,
)

SCHEMA = "/tmp/claude-0/-home-user-Training/8e37fd4f-4098-5af5-a961-7507d0777119/scratchpad/schema.json"
SORTIE = "/home/user/Training/acm_passloisirs/Referentiel_Base_PASS_LOISIRS_2.0.pdf"

ENCRE = colors.HexColor("#16213e")
ACCENT = colors.HexColor("#0f4c81")
ALERTE = colors.HexColor("#a8322d")
VERT = colors.HexColor("#1b6b3a")
OR = colors.HexColor("#8a6d1f")
GRIS = colors.HexColor("#5a5a66")
FOND = colors.HexColor("#f4f5f8")
FONDT = colors.HexColor("#eef1f6")

getSampleStyleSheet()


def st(nom, **kw):
    base = dict(fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=ENCRE)
    base.update(kw)
    return ParagraphStyle(nom, **base)


S_TITRE = st("t", fontName="Helvetica-Bold", fontSize=24, leading=28, textColor=ACCENT, spaceAfter=4)
S_STITRE = st("st", fontSize=11, leading=15.5, textColor=GRIS, spaceAfter=14)
S_PART = st("part", fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=colors.white,
            spaceBefore=4, spaceAfter=4)
S_H1 = st("h1", fontName="Helvetica-Bold", fontSize=14.5, leading=18, textColor=ACCENT,
          spaceBefore=14, spaceAfter=6)
S_H2 = st("h2", fontName="Helvetica-Bold", fontSize=11, leading=14.5, textColor=ENCRE,
          spaceBefore=9, spaceAfter=4)
S_P = st("p", alignment=TA_JUSTIFY, spaceAfter=6)
S_PUCE = st("puce", alignment=TA_JUSTIFY, leftIndent=11, bulletIndent=2, spaceAfter=3)
S_CELL = st("cell", fontSize=7.6, leading=10)
S_CELLB = st("cellb", fontSize=7.6, leading=10, fontName="Helvetica-Bold")
S_CELLH = st("cellh", fontSize=7.8, leading=10, fontName="Helvetica-Bold", textColor=colors.white)
S_TBLDESC = st("td", fontSize=8.6, leading=12, textColor=GRIS, alignment=TA_JUSTIFY, spaceAfter=5)

flow = []
L = 166 * mm


def h1(t):
    flow.append(Paragraph(t, S_H1))


def h2(t):
    flow.append(Paragraph(t, S_H2))


def p(t):
    flow.append(Paragraph(t, S_P))


def puces(items):
    for it in items:
        flow.append(Paragraph(it, S_PUCE, bulletText="•"))
    flow.append(Spacer(1, 4))


def bandeau(titre, sous=""):
    txt = f"<b>{titre}</b>"
    if sous:
        txt += f"<br/><font size=8.5>{sous}</font>"
    t = Table([[Paragraph(txt, st("b", fontSize=15, leading=19, textColor=colors.white,
                                  fontName="Helvetica-Bold"))]], colWidths=[L])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    flow.append(Spacer(1, 6))
    flow.append(t)
    flow.append(Spacer(1, 9))


def encadre(titre, txt, couleur=ALERTE):
    t = Table([[Paragraph(f"<b>{titre}</b><br/>{txt}", st("e", fontSize=8.8, leading=12.5))]],
              colWidths=[L])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), FOND),
        ("LINEBEFORE", (0, 0), (0, -1), 2.6, couleur),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    flow.append(t)
    flow.append(Spacer(1, 8))


def tableau(entetes, lignes, largeurs, garder=False):
    data = [[Paragraph(e, S_CELLH) for e in entetes]]
    for lg in lignes:
        data.append([Paragraph(str(c), S_CELL) for c in lg])
    t = Table(data, colWidths=largeurs, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, FONDT]),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#c4c9d4")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3.5), ("RIGHTPADDING", (0, 0), (-1, -1), 3.5),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    if garder:
        flow.append(KeepTogether(t))
    else:
        flow.append(t)
    flow.append(Spacer(1, 8))


def esc(s):
    if not s:
        return ""
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# Champs dont la description est conservée en entier : ce sont les pivots.
PIVOTS = re.compile(
    r"(ALERTE|CONTR[ÔO]LE|Anomalie|SYNTH[ÈE]SE|FICHE DU JOUR|Place garantie|Relance|"
    r"Titulaire|Acompte exigible|Tarif final|Montant à facturer|État|Etat|Compte Airtable|"
    r"Quantité retenue|Prix unitaire retenu|Autorisation valable|Lien actif|Retard parent|"
    r"Pénalité retard|Allèrgènes)", re.I)


def role(champ):
    d = (champ.get("description") or "").strip()
    if not d:
        return "<i>—</i>"
    d = " ".join(d.split())
    limite = 700 if PIVOTS.search(champ["name"]) else 190
    if len(d) > limite:
        d = d[:limite].rsplit(" ", 1)[0] + "…"
    return esc(d)


TYPES_FR = {
    "singleLineText": "texte", "multilineText": "texte long", "richText": "texte enrichi",
    "email": "courriel", "phoneNumber": "téléphone", "url": "lien", "number": "nombre",
    "currency": "montant", "percent": "pourcentage", "date": "date", "dateTime": "date et heure",
    "checkbox": "case", "singleSelect": "liste", "multipleSelects": "liste multiple",
    "multipleRecordLinks": "LIEN", "formula": "FORMULE", "rollup": "CUMUL",
    "count": "COMPTEUR", "multipleLookupValues": "RECHERCHE", "duration": "durée",
    "rating": "note", "barcode": "code-barres", "multipleAttachments": "pièces jointes",
    "singleCollaborator": "utilisateur", "multipleCollaborators": "utilisateurs",
    "autoNumber": "n° auto", "createdTime": "créé le", "lastModifiedTime": "modifié le",
    "createdBy": "créé par", "lastModifiedBy": "modifié par", "button": "bouton",
}

with open(SCHEMA, encoding="utf-8") as f:
    schema = json.load(f)
TABLES = {t["name"]: t for t in schema["tables"]}
NB_TABLES = len(schema["tables"])
NB_CHAMPS = sum(len(t["fields"]) for t in schema["tables"])

FAMILLES = [
    ("A", "Le socle : ce qui se règle une fois",
     "Les référentiels. On y écrit une valeur une seule fois, et toute la base la lit. "
     "C'est ce qui évite d'avoir un tarif ou un horaire recopié à trente endroits.",
     ["Paramètres", "Tarifs", "Sessions", "Menus", "Activités"]),
    ("B", "Les personnes et leurs droits",
     "Qui est qui, et qui a le droit de faire quoi pour quel enfant. C'est la partie "
     "juridiquement la plus sensible de la base.",
     ["Familles", "Enfants", "Personnes", "Liens personne-enfant",
      "Responsables", "Personnes autorisées"]),
    ("C", "La santé et le dossier administratif",
     "Les données protégées et les pièces obligatoires. Cloisonnées à dessein : "
     "l'animateur reçoit une consigne, jamais un diagnostic.",
     ["Santé", "Dossiers", "Documents", "Documents à fournir"]),
    ("D", "L'inscription et l'argent",
     "De la prestation choisie jusqu'à l'encaissement. Aucun montant n'y est jamais saisi "
     "deux fois : il descend du catalogue et remonte jusqu'à la facture.",
     ["Inscriptions", "Lignes d'inscription", "Devis", "Factures",
      "Échéancier", "Encaissements", "Affectations paiement", "Pénalités & avoirs"]),
    ("E", "La journée d'accueil",
     "Ce qui se passe réellement sur le terrain, heure par heure.",
     ["Présences", "Sorties", "Transmissions parents", "Incidents", "Économat"]),
    ("F", "L'équipe",
     "Les salariés et leur paie. La table la plus sensible de toutes.",
     ["Équipe", "Paie"]),
    ("G", "La conformité et la sécurité",
     "Ce qui permet de prouver, des mois plus tard, ce qui a été fait et par qui.",
     ["Journal d'audit", "Registre des traitements", "Accès, jetons et partages",
      "Incidents de sécurité et violations", "Mouvements de départ"]),
    ("H", "L'entrée dans le parcours",
     "Le premier contact avec une famille.",
     ["Préinscriptions"]),
]

# ------------------------------------------------------------------ COUVERTURE
flow.append(Spacer(1, 10 * mm))
flow.append(Paragraph("PASS LOISIRS 2.0", S_TITRE))
flow.append(Paragraph(
    "Référentiel complet de la base de données — table par table, champ par champ<br/>"
    f"Base <b>appGyK0pp3tlRABVA</b> · <b>{NB_TABLES} tables</b> · <b>{NB_CHAMPS} champs</b> · "
    "7 automatisations · état au 11 septembre 2026", S_STITRE))

encadre(
    "À qui ce document s'adresse, et ce qu'il n'est pas",
    "Ce référentiel est destiné à <b>Stan</b> et à toute personne qui reprendra cette base. "
    "Il décrit ce qui existe réellement : les descriptions de champs reproduites ici sont "
    "celles inscrites dans la base elle-même, pas un commentaire rédigé après coup.<br/><br/>"
    "Il ne s'agit <b>pas</b> d'une attestation de conformité. La base est en mode "
    "<b>FICTIF</b>, les sept automatisations sont en <b>brouillon</b> et aucune donnée réelle "
    "de famille n'y figure. Les limites, y compris celles qui bloquent une mise en service, "
    "sont énoncées sans ménagement en fin de document.",
    ALERTE)

h1("À quoi sert cette base")

p("Un accueil collectif de mineurs traite chaque jour des informations dont la perte ou la fuite "
  "a des conséquences réelles : l'allergie d'un enfant, le nom du parent autorisé à venir le "
  "chercher, l'argent que doit une famille, le salaire d'un animateur. Faire cela au classeur et "
  "au tableur, c'est accepter qu'une information juste existe quelque part sans que personne ne "
  "la voie au bon moment.")

p("Cette base a un objectif simple à énoncer : <b>faire remonter la bonne information à la bonne "
  "personne, au moment où elle doit agir, et refuser de produire un résultat quand les conditions "
  "ne sont pas réunies.</b> Elle affiche « NE PAS SERVIR » à côté d'un enfant dont l'allergie "
  "croise le plat du jour. Elle refuse d'émettre une facture sans régime de TVA renseigné. Elle "
  "signale une place de vacances non garantie faute d'acompte — une place vendable à une autre "
  "famille.")

p("Elle est construite pour trois métiers qui n'ont pas les mêmes besoins ni les mêmes droits : "
  "l'<b>animateur</b>, qui a besoin de gestes et pas de chiffres ; le <b>responsable</b>, qui a "
  "besoin de l'état de sa journée ; le <b>directeur</b>, qui a besoin de savoir où en est sa "
  "structure et ce qui lui coûte de l'argent.")

h1("Comment elle est organisée")

p("Les 36 tables se rangent en huit familles. Deux chaînes portent l'essentiel.")

h2("La chaîne de l'argent")
p("<b>Tarifs</b> (le catalogue) → <b>Lignes d'inscription</b> (le panier d'un jeune) → "
  "<b>Inscriptions</b> (la somme de ses prestations) → <b>Devis</b> → <b>Factures</b> → "
  "<b>Encaissements</b> → <b>Affectations paiement</b>. Le principe tient en une phrase : "
  "<b>un prix vit à un seul endroit</b>, le catalogue, et descend jusqu'à la facture sans jamais "
  "être ressaisi. Le passage obligé par les affectations est ce qui empêche de compter deux fois "
  "le même paiement.")

h2("La chaîne des droits")
p("<b>Personnes</b> (l'identité, saisie une seule fois) → <b>Liens personne-enfant</b> (le droit, "
  "daté et révocable) → <b>Enfants</b> → <b>Mouvements de départ</b>. Le droit est porté par le "
  "<b>lien</b>, jamais par la personne : un même adulte peut être autorisé pour un enfant et pas "
  "pour son frère. C'est ce qui permet de distinguer deux questions que l'on confond souvent, et "
  "dont la confusion est grave.")

encadre(
    "La distinction juridique centrale de cette base",
    "Un parent peut être <b>privé par décision de justice du droit de venir chercher l'enfant</b> "
    "tout en restant <b>titulaire de l'autorité parentale</b>. Ce sont deux questions différentes. "
    "La base les traite par deux champs séparés : « Autorisation valable aujourd'hui » juge la "
    "récupération, « Lien actif aujourd'hui » juge la validité générale du lien. Les confondre "
    "reviendrait soit à laisser partir un enfant avec un parent interdit, soit à priver un parent "
    "de toute information sur son enfant.",
    ACCENT)

# ------------------------------------------------------------------ AUTOMATISATIONS
h1("Les sept automatisations")

p("Toutes sont en <b>brouillon, désactivées</b>. Elles partagent trois règles de conception.")

puces([
    "<b>Une condition unique de déclenchement.</b> Chaque automatisation se déclenche sur un seul champ calculé qui encapsule toutes les exigences. Un déclencheur à six conditions part de travers le jour où l'une d'elles change.",
    "<b>Un message distinct par destinataire.</b> Aucune ne met deux parents en copie du même courriel : mettre en copie deux parents séparés révélerait l'adresse de l'un à l'autre.",
    "<b>L'horodatage est posé avant l'envoi.</b> Si l'automatisation échoue en cours de route, elle ne repart pas en boucle sur les mêmes familles.",
])

tableau(
    ["Automatisation", "Se déclenche quand", "Ce qu'elle fait"],
    [
        ["<b>Envoi du formulaire d'inscription</b>", "« État formulaire » = A ENVOYER, c'est-à-dire dès que l'enfant est saisi et rattaché à un titulaire de l'autorité parentale disposant d'une adresse",
         "Envoie le lien du formulaire à chaque titulaire. <b>C'est le point de départ : Stan tape un nom, la machine fait le reste.</b>"],
        ["<b>Confirmation d'inscription</b>", "« Confirmation — état » = PRETE A ENVOYER, c'est-à-dire inscription validée ET acompte encaissé",
         "Envoie le pack complet : les 5 documents obligatoires en pièces jointes, le contenu du sac, les horaires et le code du portail — tous lus dans les Paramètres."],
        ["<b>Envoi du devis</b>", "« État du devis » = PRET A ENVOYER", "Adresse la proposition chiffrée, détaillée prestation par prestation, avec les conditions d'acompte et leur conséquence."],
        ["<b>Envoi de la facture</b>", "« État de la facture » = PRETE A ENVOYER", "Adresse la facture avec ses mentions obligatoires et le régime de TVA."],
        ["<b>Relance des impayés</b>", "« Relance » contient RELANCE A ENVOYER", "Trois niveaux — rappel, fermeté, dernier avertissement — avec 10 jours minimum entre deux relances et arrêt après le troisième."],
        ["<b>Point du matin (direction)</b>", "Tous les jours à 6h30", "Dix indicateurs de pilotage classés par urgence. Compteurs et liens seulement, jamais un nom."],
        ["<b>Veille quotidienne</b>", "Tous les jours à 7h00", "Capacité dépassée, documents expirés, départs bloqués."],
    ],
    [38 * mm, 52 * mm, 76 * mm])

# ------------------------------------------------------------------ LES TABLES
flow.append(PageBreak())
bandeau("Les 36 tables, champ par champ",
        f"{NB_CHAMPS} champs. Les mentions LIEN, FORMULE, CUMUL, COMPTEUR et RECHERCHE "
        "signalent un champ CALCULÉ : il ne se saisit pas, il se déduit.")

p("<b>Comment lire ces tableaux.</b> La colonne « type » indique si le champ se saisit ou se "
  "calcule. Un champ en majuscules — <b>FORMULE</b>, <b>CUMUL</b>, <b>COMPTEUR</b>, "
  "<b>RECHERCHE</b>, <b>LIEN</b> — n'est jamais tapé à la main : il se met à jour tout seul. "
  "Toucher un champ calculé, c'est casser une chaîne. La colonne « à quoi il sert » reprend la "
  "description inscrite dans la base ; les champs pivots sont donnés en entier, les autres "
  "abrégés.")

for code, titre, intro, noms in FAMILLES:
    flow.append(PageBreak())
    bandeau(f"Famille {code} — {titre}", intro)
    for nom in noms:
        t = TABLES.get(nom)
        if not t:
            continue
        h1(f"{nom}")
        meta = f"<font color='#5a5a66'>Identifiant <b>{t['id']}</b> · {len(t['fields'])} champs</font>"
        flow.append(Paragraph(meta, st("m", fontSize=8, leading=11)))
        desc = (t.get("description") or "").strip()
        if desc:
            flow.append(Paragraph(esc(" ".join(desc.split())), S_TBLDESC))
        else:
            flow.append(Paragraph(
                "<i>Table sans description enregistrée dans la base. À documenter : une table "
                "dont l'objet n'est pas écrit sera mal utilisée par la prochaine personne.</i>",
                S_TBLDESC))
        lignes = []
        for c in t["fields"]:
            nom_c = esc(c["name"])
            typ = TYPES_FR.get(c["type"], c["type"])
            if typ.isupper():
                typ = f"<b>{typ}</b>"
            lignes.append([f"<b>{nom_c}</b>", typ, role(c)])
        tableau(["Champ", "Type", "À quoi il sert"], lignes,
                [40 * mm, 20 * mm, 106 * mm])

# ------------------------------------------------------------------ POINTS FORTS
flow.append(PageBreak())
bandeau("Les points forts", "Ce que cette base fait mieux que ce qu'on trouve habituellement "
                            "dans une structure de cette taille.")

FORTS = [
    ("1. Le prix ne se saisit jamais deux fois",
     "Un tarif vit dans le catalogue, descend dans une ligne de prestation, remonte dans "
     "l'inscription, puis dans le devis et la facture. Changer un prix au catalogue le change "
     "partout. Il n'existe aucun endroit où quelqu'un puisse taper un montant qui contredise un "
     "autre. C'est la différence entre une base et un tableur.", VERT),
    ("2. Le droit est porté par le lien, pas par la personne",
     "Une case « autorisé » cochée sur une personne ne dit ni depuis quand, ni jusqu'à quand, ni "
     "pour quel enfant, ni si une décision de justice est intervenue. Ici, chaque relation adulte-"
     "enfant est datée, révocable, et porte ses propres droits. Un même grand-parent peut être "
     "autorisé pour un petit-fils et pas pour l'autre. Le test l'a vérifié.", VERT),
    ("3. Le croisement automatique du menu et des allergies",
     "Les allergènes des enfants et ceux des menus sont saisis dans la <b>même liste fermée</b> — "
     "les 14 allergènes à déclaration obligatoire du règlement européen. La feuille de présence "
     "affiche alors, toute seule, « NE PAS SERVIR — OEUFS LAIT » à côté de l'enfant concerné. "
     "Une allergie écrite en texte libre ne se croiserait pas. C'est probablement la "
     "fonctionnalité qui protège le plus, au quotidien, un enfant et l'animateur qui le surveille.", VERT),
    ("4. L'argent négatif ne circule plus",
     "Le test a produit des tarifs de -663 EUR et -50 EUR à partir d'une remise à 150 % et d'une "
     "quantité négative. Ces montants remontaient jusqu'au solde des familles : une erreur de "
     "saisie <b>diminuait la dette</b>. Un tarif négatif ne contribue plus que zéro, et l'anomalie "
     "reste affichée. Rien n'est masqué, mais rien de faux ne circule.", VERT),
    ("5. Le refus plutôt que l'invention",
     "Sept prestations n'ont pas de prix : la base <b>refuse</b> de facturer plutôt que d'inventer "
     "un montant. Le régime de TVA n'est pas tranché : la facture <b>refuse</b> de partir. Une "
     "activité aquatique sous-encadrée affiche BLOQUE. Une base qui invente une valeur pour ne "
     "pas rester vide est plus dangereuse qu'une base qui s'arrête.", VERT),
    ("6. La minimisation appliquée pour de vrai",
     "L'animateur voit « ACOMPTE MANQUANT », jamais un euro. Il voit « ne mange ni laitage ni "
     "œuf », jamais le diagnostic. Le courriel du matin au directeur ne transporte que des "
     "compteurs et des liens, jamais un nom d'enfant. Ce n'est pas un principe affiché : c'est "
     "écrit dans les formules.", VERT),
    ("7. Tout envoi laisse une trace",
     "Chaque automatisation écrit au journal d'audit qui a envoyé quoi, à combien de personnes, "
     "et quand — sans recopier le contenu. Six mois plus tard, dans une discussion tendue avec "
     "une famille, cette trace vaut mieux que n'importe quel souvenir.", VERT),
    ("8. Le fuseau horaire est traité correctement",
     "La Réunion est à UTC+4. Les horaires de pointage sont convertis en minutes locales avant "
     "toute comparaison. Un calcul mené en heure universelle aurait décalé tous les pointages de "
     "quatre heures et rendu chaque pénalité de retard contestable.", VERT),
]

for titre, txt, coul in FORTS:
    encadre(titre, txt, coul)

# ------------------------------------------------------------------ AXES
flow.append(PageBreak())
bandeau("Les axes d'amélioration",
        "Classés du plus bloquant au plus confortable. Les trois premiers empêchent une mise en "
        "service devant des familles.")

AXES = [
    ("BLOQUANT 1 — Les fiches de paie ne peuvent pas être étanches sur le forfait gratuit",
     "L'accès « interface seulement » n'existe pas sur le forfait gratuit d'Airtable : il faut au "
     "minimum le forfait Team. Sur le gratuit, donner une interface à un animateur lui donne aussi "
     "la base — donc la table Paie, donc le salaire de ses collègues. Toute la mécanique "
     "d'étanchéité est construite et attend, mais elle <b>ne protège rien tant que le forfait n'a "
     "pas changé</b>. Trois mesures ont été prises en attendant : aucun champ pièce jointe dans la "
     "table Paie (une pièce jointe Airtable est servie par une URL publique qui ignore tous les "
     "filtres), un contrôle qui compare le titulaire du bulletin au compte déclaré dans la fiche "
     "Équipe, et un refus explicite de faire semblant — les six bulletins de test affichent tous "
     "« ETANCHEITE IMPOSSIBLE ». <b>Tant que ce point n'est pas réglé, ne mettez aucun bulletin "
     "réel dans cette base.</b>", ALERTE),
    ("BLOQUANT 2 — Le plafond d'enregistrements est déjà dépassé",
     "Le forfait gratuit s'arrête à 1 000 enregistrements par base ; le jeu de recette en compte "
     "déjà 131 à lui seul. Le calcul par jeune et par saison est d'environ 75 enregistrements, "
     "dont 34 présences. Ce ne sont donc pas les inscriptions qui saturent : ce sont les "
     "<b>présences</b>. Le plafond gratuit serait franchi vers le treizième enfant. Aucune "
     "modification de structure ne lève ce plafond : c'est une décision de forfait, à prendre "
     "avant la saison et non pendant.", ALERTE),
    ("BLOQUANT 3 — Airtable affiche, mais ne bloque pas",
     "Tous les contrôles décrits dans ce document sont des <b>formules</b> : elles rendent une "
     "erreur visible, elles ne l'empêchent pas. Une personne ayant accès à la table peut forcer un "
     "statut, saisir un prix négocié à zéro avec un motif de complaisance, ou modifier un droit "
     "parental. Le refus réel doit être écrit dans une couche serveur — c'est déjà le cas pour les "
     "départs, dans le module de sécurité du dépôt. Tant que cette couche n'existe pas pour les "
     "prix et les droits, la base est un excellent outil de pilotage, pas un coffre-fort.", ALERTE),
    ("4 — Sept prix manquent au catalogue",
     "Vacances journée et demi-journées, semaine, sortie, repas, adhésion : tarif 1 enfant et "
     "tarif fratrie. Tant qu'ils sont vides, aucune inscription vacances n'est facturable. C'est "
     "volontaire — la base refuse d'inventer — mais c'est le premier geste à faire.", OR),
    ("5 — Le régime de TVA n'est pas tranché",
     "Mention obligatoire sur une facture. Tant qu'il vaut « À DÉTERMINER », aucune facture ne "
     "part. À voir avec l'expert-comptable, en même temps que la question plus large de la "
     "lucrativité : un catalogue de prestations tarifées rend l'activité <b>plus visible</b> "
     "fiscalement, pas moins.", OR),
    ("6 — Deux horaires se contredisent",
     "Le paramètre HEURE_FERMETURE vaut 17h30, la règle annoncée aux familles est 18h00. La "
     "pénalité de retard est calculée sur 18h00. Une pénalité fondée sur un horaire différent de "
     "celui du règlement intérieur signé sera contestée, et à juste titre. Le seuil de "
     "déclenchement (paramètre PENALITE_DECLENCHE_A = 2) n'a pas d'unité définie.", OR),
    ("7 — La fratrie reste déclarative",
     "Le drapeau « Fratrie ? » se coche à la main. Rien n'empêche de le cocher pour un enfant "
     "unique : 2 EUR de moins par mercredi, soit 68 EUR par dossier, invisibles. Un contrôle "
     "croisant le nombre d'enfants actifs de la famille corrigerait cela.", OR),
    ("8 — La numérotation des factures n'est pas garantie",
     "Airtable ne peut pas assurer une suite chronologique sans trou : supprimer une facture "
     "laisse un trou invisible. Le contrôle signale un numéro manquant, mais la garantie réelle "
     "exige la couche serveur.", OR),
    ("9 — Les taux d'encadrement sont à paramétrer",
     "Le seuil d'alerte de 12 enfants par animateur est un repère indicatif inscrit dans la "
     "synthèse du jour. Les taux réglementaires réels sont plus stricts pour les moins de six ans "
     "et pour les activités aquatiques. Le champ « Encadrants requis » de chaque activité doit "
     "être renseigné selon la réglementation applicable, activité par activité.", OR),
    ("10 — Les interfaces par rôle restent à compléter",
     "Cinq interfaces par rôle existent depuis les travaux antérieurs. Les pages nouvelles — "
     "journée d'accueil, feuille de présence avec alertes repas, fiche de paie individuelle — "
     "restent à y ajouter. Ce travail n'a de sens qu'une fois le forfait tranché, puisque "
     "l'étanchéité en dépend.", OR),
    ("11 — Le code du portail circule par courriel",
     "Le code 1619 ouvre un accès physique au lieu où se trouvent les enfants. Une fois envoyé, il "
     "vit dans des dizaines de boîtes de réception, y compris celles d'anciennes familles. À "
     "changer au moins à chaque rentrée, et à ne jamais faire figurer dans une interface partagée "
     "publiquement.", OR),
    ("12 — Le jeu de recette doit être purgé",
     "Les 131 enregistrements préfixés TEST doivent disparaître avant de basculer MODE_DONNEES sur "
     "RÉEL. Les conserver fausserait les statistiques, les soldes et les listes d'accueil — et "
     "activer les automatisations en leur présence enverrait une trentaine de courriels de test.", OR),
    ("13 — Trois paramètres de conformité restent vides",
     "L'analyse d'impact (AIPD), la qualification hébergement de données de santé (HDS) et "
     "l'identité du responsable de traitement sont au statut « À RENSEIGNER ». Ce sont des "
     "préalables à une mise en service, pas des formalités de fin de projet.", OR),
]

for titre, txt, coul in AXES:
    encadre(titre, txt, coul)

# ------------------------------------------------------------------ CE QUI A ÉTÉ VÉRIFIÉ
flow.append(PageBreak())
bandeau("Ce qui a été vérifié, et comment",
        "Deux campagnes de test sur données fictives, les 10 et 11 septembre 2026.")

p("La base n'a pas été livrée sur la foi de sa construction : elle a été mise en difficulté "
  "volontairement, sur des scénarios choisis pour la faire échouer.")

tableau(
    ["Campagne", "Ce qui a été éprouvé", "Résultat"],
    [
        ["<b>Test de charge</b><br/>15 enfants, 8 familles, 14 adultes, 28 liens, 15 inscriptions",
         "Fratries, parents séparés, garde exclusive, restriction judiciaire, dossier sans "
         "représentant légal, gratuité, remise à 150 %, quantité négative, prestation non tarifée, "
         "trop-perçu, acompte payé et impayé",
         "<b>5 défauts trouvés, 5 réparés</b> et re-vérifiés le jour même"],
        ["<b>Simulation des trois métiers</b><br/>Stan, un parent de 2 enfants, une animatrice",
         "Croisement menu-allergies, pointage et pénalités, encadrement des activités, étanchéité "
         "des paies, devis familial multi-parents, tableau de bord de direction",
         "<b>4 défauts trouvés</b>, dont une régression introduite par une réparation précédente"],
    ],
    [40 * mm, 76 * mm, 50 * mm])

h2("Les neuf défauts trouvés")

tableau(
    ["#", "Défaut", "État"],
    [
        ["1", "<b>Des montants négatifs remontaient jusqu'au solde des familles</b> : une remise à 150 % produisait -663 EUR et <b>diminuait la dette</b>", "Corrigé"],
        ["2", "Un tarif <b>négatif</b> était traité comme une <b>gratuité</b> : la place était affichée GARANTIE sur une erreur de saisie", "Corrigé"],
        ["3", "Aucune inscription du mercredi ne pouvait être confirmée : le contrôle exigeait de relier les 34 sessions une à une", "Corrigé"],
        ["4", "Saisir une date de validation de prix sans le montant faisait tomber le tarif à <b>0 EUR en silence</b>", "Corrigé"],
        ["5", "Une inscription était chiffrée à 1 326 EUR pour un enfant <b>sans aucun représentant légal</b>, sans alerte", "Corrigé"],
        ["6", "<b>Six enfants pointés, zéro inscription reliée</b> à la journée, aucune alerte : ni assurance vérifiée, ni fiche sanitaire, ni autorisation de départ", "Corrigé"],
        ["7", "<b>Régression d'une réparation précédente</b> : l'anomalie tarifaire écrasait le verdict d'acompte. Le directeur voyait <b>0 place à récupérer au lieu de 5</b>", "Corrigé"],
        ["8", "Écart de 29,60 EUR entre le brut saisi et le brut recalculé sur un bulletin de paie", "Détecté par le contrôle"],
        ["9", "Les six bulletins de paie sont <b>inertes</b> faute de comptes Airtable liés aux salariés", "Structurel — voir bloquant 1"],
    ],
    [7 * mm, 129 * mm, 30 * mm])

encadre(
    "Pourquoi le défaut 7 mérite d'être retenu",
    "Il a été <b>introduit en réparant le défaut 2</b>. Sans la simulation du profil directeur, il "
    "serait passé en production : cinq places de vacances impayées auraient disparu du tableau de "
    "bord, et personne n'aurait su qu'elles étaient revendables. C'est l'argument le plus solide "
    "en faveur du fait de tester une base en jouant les métiers, et pas seulement en relisant les "
    "formules.",
    ACCENT)

h1("Le mot de la fin")

p("Le modèle de données de cette base est meilleur que ce qu'on trouve habituellement dans une "
  "association de cette taille. La séparation entre l'autorité parentale et la qualité de payeur, "
  "les droits portés par un lien daté et révocable, le passage obligé des paiements par une table "
  "d'affectation, le croisement automatique des allergènes : ce sont des choix qui tiendront quand "
  "le volume montera.")

p("Il faut dire aussi, sans détour, ce qui ne va pas. La base <b>ne protège rien par elle-même</b>. "
  "Chaque contrôle décrit ici est un panneau, pas une barrière. Tant qu'il n'y a pas de couche "
  "serveur devant, la sécurité repose sur la discipline des personnes qui ont accès à la table. "
  "Pour un accueil de mineurs, avec des données de santé, des restrictions judiciaires et des "
  "salaires, c'est une situation à corriger avant d'ouvrir au public, pas après.")

p("Trois décisions sont sur le chemin critique, et <b>aucune n'est technique</b> : le forfait, les "
  "sept prix, et la position fiscale de l'association. Tant qu'elles ne sont pas prises, la base "
  "ne peut ni facturer, ni relancer, ni protéger un bulletin de paie — et c'est très bien ainsi : "
  "elle refuse plutôt que d'inventer.")


def pied(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.2)
    canvas.setFillColor(GRIS)
    canvas.drawString(20 * mm, 11.5 * mm,
                      "PASS LOISIRS 2.0 — référentiel de la base — 11/09/2026 — "
                      "36 tables, 631 champs — mode FICTIF")
    canvas.drawRightString(190 * mm, 11.5 * mm, "page %d" % doc.page)
    canvas.setStrokeColor(colors.HexColor("#d5d8de"))
    canvas.setLineWidth(0.4)
    canvas.line(20 * mm, 14.5 * mm, 190 * mm, 14.5 * mm)
    canvas.restoreState()


doc = BaseDocTemplate(SORTIE, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=16 * mm, bottomMargin=19 * mm,
                      title="PASS LOISIRS 2.0 - Referentiel de la base de donnees",
                      author="Referentiel genere depuis le schema reel")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=pied)])
doc.build(flow)
print("PDF genere :", SORTIE)
print("Tables :", NB_TABLES, "| Champs :", NB_CHAMPS)
