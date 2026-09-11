#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère le dossier PDF de fonctionnement de la base PASS LOISIRS 2.0.

Destiné à Stan et à son associé : décrit l'architecture réelle de la base,
le résultat du test de charge du 11/09/2026 sur 15 enfants, les défauts
trouvés, ce qui a été réparé, et ce qui reste ouvert.
"""

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, PageBreak,
)

SORTIE = "/home/user/Training/acm_passloisirs/Dossier_Fonctionnement_PASS_LOISIRS_2.0.pdf"

ENCRE = colors.HexColor("#1a1a2e")
ACCENT = colors.HexColor("#0f4c81")
ALERTE = colors.HexColor("#a33")
VERT = colors.HexColor("#1b6b3a")
GRIS = colors.HexColor("#5a5a66")
FOND = colors.HexColor("#f4f5f8")

ss = getSampleStyleSheet()


def st(nom, **kw):
    base = dict(fontName="Helvetica", fontSize=9.5, leading=14, textColor=ENCRE)
    base.update(kw)
    return ParagraphStyle(nom, **base)


S_TITRE = st("t", fontName="Helvetica-Bold", fontSize=23, leading=27, textColor=ACCENT, spaceAfter=4)
S_STITRE = st("st", fontSize=11.5, leading=16, textColor=GRIS, spaceAfter=16)
S_H1 = st("h1", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=ACCENT,
          spaceBefore=16, spaceAfter=7)
S_H2 = st("h2", fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=ENCRE,
          spaceBefore=11, spaceAfter=5)
S_P = st("p", alignment=TA_JUSTIFY, spaceAfter=6)
S_PUCE = st("puce", alignment=TA_JUSTIFY, leftIndent=11, bulletIndent=2, spaceAfter=3)
S_CELL = st("cell", fontSize=8.3, leading=11)
S_CELLB = st("cellb", fontSize=8.3, leading=11, fontName="Helvetica-Bold")
S_NOTE = st("note", fontSize=8.5, leading=12, textColor=GRIS, alignment=TA_JUSTIFY, spaceAfter=6)

flow = []


def h1(txt):
    flow.append(Paragraph(txt, S_H1))


def h2(txt):
    flow.append(Paragraph(txt, S_H2))


def p(txt):
    flow.append(Paragraph(txt, S_P))


def puces(items):
    for it in items:
        flow.append(Paragraph(it, S_PUCE, bulletText="•"))
    flow.append(Spacer(1, 4))


def encadre(titre, txt, couleur=ALERTE):
    t = Table([[Paragraph(f"<b>{titre}</b><br/>{txt}", st("enc", fontSize=9, leading=13))]],
              colWidths=[165 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), FOND),
        ("LINEBEFORE", (0, 0), (0, -1), 2.4, couleur),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    flow.append(t)
    flow.append(Spacer(1, 8))


def tableau(entetes, lignes, largeurs):
    data = [[Paragraph(e, S_CELLB) for e in entetes]]
    for lg in lignes:
        data.append([Paragraph(str(c), S_CELL) for c in lg])
    t = Table(data, colWidths=largeurs, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, FOND]),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#c8ccd4")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    flow.append(t)
    flow.append(Spacer(1, 9))


# En-tête des styles de tableau : largeurs utiles
L = 165 * mm

# ---------------------------------------------------------------- COUVERTURE
flow.append(Spacer(1, 12 * mm))
flow.append(Paragraph("PASS LOISIRS 2.0", S_TITRE))
flow.append(Paragraph(
    "Dossier de fonctionnement de la base de données — accueil collectif de mineurs<br/>"
    "Base <font face='Helvetica-Bold'>appGyK0pp3tlRABVA</font> · saison 2026-2027 · "
    "état au 11 septembre 2026", S_STITRE))

encadre(
    "Ce document décrit une base en mode FICTIF, pas un système mis en service",
    "Le paramètre <b>MODE_DONNEES</b> vaut toujours <b>FICTIF</b>. Toutes les données citées ici "
    "sont des données de recette créées pour éprouver la base, préfixées <b>TEST</b>. "
    "Aucune famille réelle n'y figure. Les cinq automatisations existantes sont en <b>brouillon, "
    "désactivées</b> : aucun courriel ne peut partir en l'état. Ce dossier rend compte d'un test "
    "informatique ; il ne vaut pas certification de conformité, et ne remplace ni un test "
    "d'intrusion, ni une validation juridique par un professionnel.",
    ALERTE)

p("Ce dossier a deux lecteurs : le directeur et son associé. Il décrit comment la base fonctionne "
  "réellement, ce que le test de charge du 11 septembre a cassé, ce qui a été réparé le jour même, "
  "et ce qui reste ouvert avant un usage devant des familles.")

# ---------------------------------------------------------------- 1. RÉSUMÉ
h1("1. Ce qu'il faut retenir en une page")

tableau(
    ["Sujet", "État au 11/09/2026"],
    [
        ["Tarification", "Modèle catalogue + panier. Un jeune peut cumuler mercredis, vacances, sorties, repas et adhésion dans <b>une seule inscription</b>, et son montant est la somme de ses prestations. Plus aucun prix forfaitaire inventé."],
        ["Catalogue", "<b>11 prestations.</b> Les 4 tarifs mercredis sont réels et validés. Les <b>7 autres n'ont pas de prix</b> et sont au statut « À valider » : c'est volontaire, les prix doivent être saisis par la direction."],
        ["Parents", "Modèle Personnes + liens datés. Autorité parentale et qualité de payeur sont <b>deux choses distinctes</b>, et une restriction judiciaire de récupération ne retire pas l'autorité parentale."],
        ["Devis et factures", "Deux tables créées, reprenant les inscriptions sans recopier un seul prix. Acompte, garantie de place, mentions obligatoires et régime de TVA sont portés."],
        ["Acompte", "100 EUR exigibles pour toute inscription VACANCES. Tant qu'il n'est pas encaissé, la place est marquée <b>NON GARANTIE — REMPLACABLE</b>."],
        ["Automatisations", "<b>7 au total, toutes désactivées.</b> 4 héritées, 3 créées ici : envoi du devis, envoi de la facture, relance des impayés."],
        ["Test de charge", "15 enfants, 8 familles, 14 adultes, 28 liens, 15 inscriptions, 16 lignes de prestation. <b>5 défauts trouvés, 5 réparés et re-vérifiés.</b>"],
        ["Verdict", "La base tient le choc sur la tarification, les droits parentaux et les contrôles. Elle <b>n'est pas prête</b> pour le public : prix manquants, aucun blocage technique réel, et un plafond d'enregistrements atteint dès la première saison."],
    ],
    [30 * mm, 135 * mm])

# ---------------------------------------------------------------- 2. ARCHITECTURE
flow.append(PageBreak())
h1("2. Comment la base est construite")

p("La base compte <b>31 tables</b>. Quatre chaînes portent l'essentiel du fonctionnement. "
  "Le principe directeur est simple : <b>aucun montant n'est jamais saisi deux fois</b>. "
  "Un prix vit au catalogue, descend dans une ligne de prestation, remonte dans une inscription, "
  "puis dans un devis et une facture.")

h2("2.1 La chaîne de l'argent")

tableau(
    ["Étape", "Table", "Ce qui s'y passe"],
    [
        ["1", "Tarifs (catalogue)", "Chaque prestation vendable porte son prix 1 enfant et son prix fratrie, son unité, sa catégorie, sa base de quantité et sa version de barème."],
        ["2", "Lignes d'inscription", "Une ligne = une prestation choisie par les parents. La quantité des mercredis est <b>déduite du planning</b>, jamais saisie. 11 contrôles d'anomalie."],
        ["3", "Inscriptions", "Somme des lignes. Priorité de prix : prix contractuel figé, puis tarif manuel, puis catalogue moins réduction."],
        ["4", "Devis", "Regroupe plusieurs jeunes et plusieurs parents. N'invente aucun prix."],
        ["5", "Factures", "Mentions obligatoires, acompte déduit, reste dû, retard, niveau de relance."],
        ["6", "Encaissements → Affectations", "Un paiement est <b>affecté</b> à une inscription précise. Ce passage obligatoire est ce qui évite le double comptage relevé par l'audit."],
    ],
    [12 * mm, 40 * mm, 113 * mm])

h2("2.2 La chaîne des droits parentaux")

p("Une personne est saisie <b>une seule fois</b> dans « Personnes ». Ce qui varie d'un enfant à "
  "l'autre — rôle, autorité parentale, qualité de payeur, droit de récupération, restriction "
  "judiciaire, dates de validité — est porté par le <b>lien</b>, pas par la personne.")

encadre(
    "La distinction juridique la plus importante de la base",
    "Un parent peut être <b>privé du droit de venir chercher l'enfant</b> par décision de justice "
    "tout en restant <b>titulaire de l'autorité parentale</b>. Ce sont deux questions différentes. "
    "La base les traite par deux champs séparés : « Autorisation valable aujourd'hui » juge la "
    "récupération, « Lien actif aujourd'hui » juge la validité générale. Confondre les deux "
    "reviendrait soit à laisser partir un enfant avec un parent interdit, soit à priver un parent "
    "de l'information sur son enfant. Le test a vérifié ce cas (scénario 9).",
    ACCENT)

h2("2.3 Les sept automatisations")

tableau(
    ["Automatisation", "Déclencheur", "État"],
    [
        ["Veille quotidienne", "Cron", "Brouillon"],
        ["Dérogation de départ", "Conditions sur le mouvement", "Brouillon"],
        ["Identité non vérifiée", "Conditions sur le mouvement", "Brouillon"],
        ["Confirmation d'inscription + PDF", "« Confirmation — état » = PRETE A ENVOYER", "Brouillon"],
        ["<b>Envoi du devis aux parents</b>", "« État du devis » = PRET A ENVOYER", "<b>Brouillon, créée le 10/09</b>"],
        ["<b>Envoi de la facture</b>", "« État de la facture » = PRETE A ENVOYER", "<b>Brouillon, créée le 11/09</b>"],
        ["<b>Relance des impayés</b>", "« Relance » contient RELANCE A ENVOYER", "<b>Brouillon, créée le 11/09</b>"],
    ],
    [58 * mm, 72 * mm, 35 * mm])

encadre(
    "Une règle commune à tous les envois : un message par destinataire",
    "Aucune automatisation ne met deux parents en copie du même courriel. Mettre en copie deux "
    "parents séparés <b>révélerait l'adresse de l'un à l'autre</b>. Chaque destinataire reçoit un "
    "message distinct, qui l'appelle par son prénom. L'horodatage d'envoi est toujours posé "
    "<b>avant</b> l'envoi : si l'automatisation échoue en cours de route, elle ne repart pas en boucle.",
    VERT)

h2("2.4 La relance, et ses garde-fous")

p("La relance monte en trois niveaux : rappel bienveillant à J+7, fermeté à J+21, dernier "
  "avertissement à J+45. Trois garde-fous sont écrits dans la règle elle-même, pas dans le "
  "déclencheur :")
puces([
    "la facture doit avoir été <b>envoyée</b> et rester <b>impayée</b> ;",
    "<b>10 jours minimum</b> séparent deux relances ;",
    "après le troisième niveau, la machine <b>s'arrête</b> et passe la main à un humain.",
])
p("Le troisième message propose un échelonnement <i>avant</i> d'évoquer une suspension d'accueil. "
  "Relancer une famille en difficulté tous les jours ne fait pas rentrer l'argent et expose "
  "l'association.")

# ---------------------------------------------------------------- 3. LE TEST
flow.append(PageBreak())
h1("3. Le test de charge du 11 septembre 2026")

p("Quinze enfants ont été créés, tous différents, avec la consigne de mettre la base en difficulté : "
  "fratries, parents séparés, garde exclusive, restriction judiciaire, dossier sans représentant "
  "légal, gratuité, remise aberrante, quantité négative, prestation non tarifée, trop-perçu, "
  "acompte vacances payé et impayé.")

tableau(
    ["Volume créé", "Nombre"],
    [["Familles", "8"], ["Enfants", "15"], ["Adultes (Personnes)", "14"],
     ["Liens personne-enfant", "28"], ["Inscriptions", "15"], ["Lignes de prestation", "16"]],
    [110 * mm, 55 * mm])

h2("3.1 Les quinze scénarios et leur résultat")

tableau(
    ["#", "Scénario", "Attendu", "Obtenu après réparation"],
    [
        ["1", "Aîné d'une fratrie, mercredis journée complète", "39 EUR x 34", "<b>1 326 EUR</b> — conforme"],
        ["2", "2e enfant, tarif fratrie, prix contractuel figé", "37 EUR x 34 figé", "<b>1 258 EUR</b> — seule inscription passée à PRETE A ENVOYER"],
        ["3", "3e enfant, demi-journée sans repas, fratrie", "26 EUR x 34", "<b>884 EUR</b> — conforme"],
        ["4", "Vacances, prix négocié <b>avec</b> motif", "180 EUR, accepté", "180 EUR, bloqué par le catalogue non validé"],
        ["5", "Vacances, prix négocié <b>sans</b> motif", "doit bloquer", "<b>PRIX NEGOCIE SANS MOTIF</b> — bloqué"],
        ["6", "Gratuité totale motivée", "0 EUR sans blocage", "<b>0 EUR</b>, aucune anomalie — conforme"],
        ["7", "Panier mixte mercredis + vacances", "1 326 + 90", "<b>1 416 EUR</b> — le cumul fonctionne"],
        ["8", "Vacances sans acompte", "place non garantie", "acompte 100 EUR exigé, place signalée remplaçable"],
        ["9", "Remise de ligne à 150 %", "doit bloquer", "<b>REMISE HORS BORNES</b> + tarif négatif neutralisé"],
        ["10", "Aucun titulaire de l'autorité parentale", "doit bloquer", "<b>AUCUN TITULAIRE</b> signalé dès l'inscription"],
        ["11", "Vacances, acompte encaissé", "place garantie", "acompte 100 EUR exigé et suivi"],
        ["12", "Vacances, acompte impayé", "remplaçable", "<b>PLACE REMPLACABLE</b> — conforme"],
        ["13", "Prestation sans prix au catalogue", "doit bloquer", "<b>PRESTATION NON TARIFEE</b> — bloqué"],
        ["14", "Quantité négative (-2)", "doit bloquer", "<b>QUANTITE NEGATIVE</b> + montant neutralisé"],
        ["15", "Payeur tiers (grand-mère) sans autorité parentale", "séparation stricte", "payeuse listée, <b>exclue</b> des titulaires"],
    ],
    [7 * mm, 48 * mm, 33 * mm, 77 * mm])

h2("3.2 Les cinq défauts trouvés — et réparés")

encadre(
    "DÉFAUT 1 — le plus grave : de l'argent négatif circulait",
    "Une remise saisie à 150 % produisait un tarif de <b>-663 EUR</b>, une quantité à -2 un tarif de "
    "<b>-50 EUR</b>. Ces montants remontaient jusqu'au solde de la famille et au total du devis : "
    "<b>une erreur de saisie diminuait la dette</b>. L'anomalie était affichée, mais l'argent "
    "circulait quand même.<br/><br/>"
    "<b>Réparé</b> : un tarif négatif ne contribue plus que 0 au montant à facturer, et l'anomalie "
    "reste affichée. Vérifié : Manon passe de -663 EUR à <b>0 EUR</b>, Jade de -50 EUR à <b>0 EUR</b>.",
    ALERTE)

encadre(
    "DÉFAUT 2 — une place garantie sur une erreur de saisie",
    "Le contrôle testait « tarif inférieur ou égal à zéro » et traitait donc un tarif <b>négatif</b> "
    "comme une <b>gratuité</b>. Les deux dossiers ci-dessus affichaient « GARANTIE — inscription "
    "gratuite ».<br/><br/>"
    "<b>Réparé</b> : un tarif négatif ou une anomalie donnent désormais « ANOMALIE — NE PAS "
    "GARANTIR LA PLACE ».",
    ALERTE)

encadre(
    "DÉFAUT 3 — aucune inscription mercredi ne pouvait être confirmée",
    "Le contrôle de planning exigeait que les <b>34 sessions soient reliées une à une</b>. Les neuf "
    "inscriptions mercredi du test étaient toutes bloquées sur « planning à vérifier ». En usage "
    "réel, il aurait fallu relier 34 sessions à la main pour chaque enfant.<br/><br/>"
    "<b>Réparé</b> : le nombre de mercredis engagé vaut preuve de planning ; la divergence n'est "
    "signalée que si des sessions sont effectivement reliées et ne correspondent pas.",
    ALERTE)

encadre(
    "DÉFAUT 4 — le piège du gel de prix",
    "Le tarif final basculait sur le prix figé dès qu'une <b>date</b> de validation était saisie. "
    "Saisir la date sans le montant faisait tomber le tarif à <b>0 EUR en silence</b>.<br/><br/>"
    "<b>Réparé</b> : le gel n'opère que si la date <b>et</b> le montant sont renseignés ; sinon le "
    "calcul continue et l'incohérence est signalée.",
    ALERTE)

encadre(
    "DÉFAUT 5 — un dossier sans représentant légal passait inaperçu",
    "Une inscription pouvait être chiffrée à 1 326 EUR pour un enfant dont <b>aucun adulte</b> ne "
    "détenait l'autorité parentale. Le blocage n'existait qu'au stade du devis, trop tard.<br/><br/>"
    "<b>Réparé</b> : le nombre de titulaires remonte au niveau de l'inscription et déclenche une "
    "anomalie. Vérifié sur le scénario 10.",
    ALERTE)

h2("3.3 Ce que le test a confirmé comme solide")

puces([
    "<b>Le calcul tarifaire</b> : les 34 mercredis, le tarif fratrie, la demi-journée sans repas et le panier mixte tombent tous juste, au centime.",
    "<b>La séparation autorité parentale / payeur</b> : la grand-mère payeuse est bien exclue des titulaires ; la mère à autorité partielle est bien titulaire sans être payeuse.",
    "<b>La restriction judiciaire</b> : le père concerné est bloqué au départ (« NON — RESTRICTION JUDICIAIRE ») tout en restant destinataire de la facture.",
    "<b>Les onze contrôles de ligne</b> : chacun s'est déclenché sur le scénario qui le visait, sans faux positif sur les dossiers sains.",
    "<b>La formule d'appel nominative</b> : « Bonjour Marie et Jean, » se compose correctement pour un couple comme pour un parent seul.",
    "<b>L'acompte vacances</b> : 100 EUR exigés sur les six inscriptions vacances, 0 ailleurs, sans intervention manuelle.",
])

# ---------------------------------------------------------------- 4. LIMITES
flow.append(PageBreak())
h1("4. Ce qui empêche encore un usage devant le public")

encadre(
    "LIMITE 1 — Airtable affiche, mais ne bloque rien",
    "C'est la limite la plus importante du dossier, et elle n'a pas de solution à l'intérieur "
    "d'Airtable. Tous les contrôles décrits ici sont des <b>formules</b> : elles rendent une erreur "
    "<b>visible</b>, elles ne l'<b>empêchent</b> pas. Une personne ayant accès à la table peut "
    "forcer un statut, saisir un prix négocié à 0 EUR avec un motif de complaisance, ou modifier "
    "un droit parental. Le refus réel doit être écrit dans une couche serveur — c'est déjà le cas "
    "pour les départs, dans le module de sécurité. Tant que cette couche n'existe pas pour les "
    "prix et les droits, la base est un outil de pilotage, pas un coffre-fort.",
    ALERTE)

encadre(
    "LIMITE 2 — le plafond d'enregistrements, atteint dès la première saison",
    "Le nombre de jeunes n'est limité par <b>aucun champ</b> de la base. Il est limité par le "
    "forfait Airtable, et aucune modification de structure ne lève ce plafond. L'offre gratuite "
    "s'arrête à <b>1 000 enregistrements par base</b>, l'offre Team à <b>50 000</b>.<br/><br/>"
    "Le calcul par jeune et par saison : 1 enfant + 2 responsables + 1 fiche santé + 1 dossier + "
    "1 inscription + environ 3 lignes + 10 échéances + 10 encaissements + 10 affectations + "
    "<b>34 présences</b>, soit environ <b>75 enregistrements</b>. Le plafond gratuit est donc "
    "franchi vers le <b>treizième enfant</b>. Ce ne sont pas les inscriptions qui saturent : ce "
    "sont les <b>présences</b>. La tarification pèse 3 enregistrements sur 75.",
    ALERTE)

h2("Les points ouverts, par ordre d'urgence")

tableau(
    ["Rang", "Point ouvert", "Qui décide"],
    [
        ["1", "<b>Les 7 prix manquants</b> au catalogue : vacances journée et demi-journées, semaine, sortie, repas, adhésion — tarif 1 enfant et tarif fratrie.", "Direction"],
        ["2", "<b>Le régime de TVA</b> de l'association. Tant qu'il vaut « À DÉTERMINER », aucune facture ne peut partir : c'est une mention obligatoire.", "Expert-comptable"],
        ["3", "<b>La lucrativité au sens fiscal.</b> Un catalogue de prestations tarifées rend l'activité <b>plus visible</b>, pas moins. C'est ce qu'examine la méthode dite des « 4 P ».", "Expert-comptable"],
        ["4", "<b>La numérotation des factures</b> : Airtable ne peut pas garantir une suite chronologique sans trou. Une suppression laisse un trou invisible.", "Couche serveur"],
        ["5", "<b>La fratrie reste manuelle.</b> Cocher « fratrie » pour un enfant unique coûte 2 EUR par mercredi, soit 68 EUR par dossier, invisibles.", "À développer"],
        ["6", "<b>La validation du prix</b> est exigée dossier par dossier (date + montant). C'est un choix défendable, mais il faut le savoir : rien ne part sans geste humain.", "Direction"],
        ["7", "<b>La signature électronique</b> n'est pas branchée. Aucune offre ne réunit gratuité, qualification eIDAS et interface automatique.", "Direction"],
        ["8", "<b>Le cumul obsolète</b> « Tarif dû » subsiste et reste faux. À supprimer après vérification des 26 pages publiées.", "À faire"],
    ],
    [12 * mm, 118 * mm, 35 * mm])

# ---------------------------------------------------------------- 5. RGPD
flow.append(PageBreak())
h1("5. RGPD et IA Act")

h2("5.1 RGPD")

p("<b>Ce qui est traité.</b> Identité des jeunes et des adultes, coordonnées, liens familiaux, "
  "données financières, et — dans une table séparée — des données de santé. Les données de santé "
  "relèvent de l'article 9 et ne sortent jamais vers les rôles opérationnels : l'animateur reçoit "
  "une <b>consigne du jour</b>, jamais le détail médical.")

p("<b>Bases légales.</b> L'inscription et la facturation relèvent de l'<b>exécution du contrat</b> "
  "conclu avec le représentant légal. Le devis relève des <b>mesures précontractuelles</b>. La "
  "conservation des pièces comptables relève de l'<b>obligation légale</b>.")

p("<b>Minimisation.</b> Le catalogue et les lignes de prestation ne contiennent <b>aucune donnée "
  "personnelle en propre</b> : ce sont des prix et des quantités. C'est le lien vers l'inscription "
  "qui les rattache à un mineur. Les champs de notes portent tous l'interdiction explicite d'y "
  "écrire une donnée de santé ou un élément de situation familiale.")

encadre(
    "Le point de vigilance à ne pas manquer",
    "Si vous ajoutez un jour un tarif au quotient familial, stockez une <b>tranche</b>, jamais un "
    "revenu. Un revenu exact est une donnée socio-économique dont la nécessité devra être justifiée, "
    "et dont la durée de conservation devra être fixée séparément.",
    ACCENT)

p("<b>À faire avant la mise en service :</b> mettre à jour le registre des traitements — devis et "
  "factures sont des traitements nouveaux ; réexaminer l'analyse d'impact, exigée par l'audit pour "
  "toute fonction nouvelle ; trancher la qualification hébergement de données de santé, toujours "
  "au statut « À RENSEIGNER » ; renseigner l'entité responsable de traitement, également vide.")

h2("5.2 IA Act")

p("<b>Aucune obligation n'est déclenchée à ce jour.</b> Rien dans la base n'est un système d'IA : "
  "les calculs sont de l'arithmétique et des conditions, les courriels sont des gabarits à trous. "
  "Le paramètre <b>IA_FONCTIONS_ACTIVEES</b> vaut « Aucune ».")

p("Le seuil serait franchi dans trois cas : si le corps d'un courriel était rédigé par un modèle de "
  "langage — il faudrait alors informer les familles ; si un classement automatique des familles "
  "était introduit pour attribuer des places rares — ce serait une décision automatisée au sens de "
  "l'article 22 du RGPD ; si un score de solvabilité était calculé — même analyse, avec une "
  "qualification à mener au titre de l'IA Act.")

# ---------------------------------------------------------------- 6. AVIS
h1("6. Avis franc sur l'état du projet")

p("<b>Ce qui est réellement bon.</b> Le modèle de données est meilleur que ce qu'on trouve "
  "habituellement dans une association de cette taille. La séparation entre l'autorité parentale "
  "et la qualité de payeur, le fait que les droits soient portés par un lien daté et révocable "
  "plutôt que par une case à cocher, le passage obligé des paiements par une table d'affectation : "
  "ce sont des choix d'architecture solides, qui tiendront quand le volume montera. Le test l'a "
  "confirmé sur quinze dossiers volontairement pénibles.")

p("<b>Ce qui doit être dit sans détour.</b> La base ne protège rien par elle-même. Chaque contrôle "
  "décrit dans ce dossier est un panneau, pas une barrière. Tant qu'il n'y a pas de couche serveur "
  "devant, la sécurité repose sur la discipline des personnes qui ont accès à la table. Pour un "
  "accueil de mineurs, avec des données de santé et des restrictions judiciaires, c'est une "
  "situation à corriger avant d'ouvrir au public, pas après.")

p("<b>Le vrai calendrier.</b> Trois choses sont sur le chemin critique, et aucune n'est technique : "
  "les sept prix, le régime de TVA, et la position fiscale de l'association. Tant qu'elles ne sont "
  "pas tranchées, la base ne peut ni facturer ni relancer — et c'est très bien ainsi : elle refuse "
  "plutôt que d'inventer. Le quatrième point, le plafond d'enregistrements, arrivera vers le "
  "treizième enfant : c'est une décision de forfait, ou de migration, à prendre maintenant et non "
  "en cours de saison.")

p("<b>Ce que je recommande.</b> Ne pas ouvrir au public avant d'avoir : saisi les prix, tranché la "
  "TVA, choisi le forfait, et activé les automatisations une par une en les testant sur une adresse "
  "de contrôle. Les automatisations restent en brouillon pour cette raison précise : le jour où "
  "elles passent en service, des courriels partent réellement vers de vraies familles, et une "
  "erreur de gabarit devient publique.")

flow.append(Spacer(1, 6))
encadre(
    "Le jeu de recette doit être supprimé avant la mise en service",
    "Les 96 enregistrements préfixés <b>TEST</b> créés pour ce test — 8 familles, 15 enfants, "
    "14 adultes, 28 liens, 15 inscriptions, 16 lignes — doivent être supprimés avant de basculer "
    "le paramètre MODE_DONNEES sur RÉEL. Les conserver ferait figurer des dossiers fictifs dans les "
    "statistiques, les soldes et les listes d'accueil.",
    ALERTE)

# ---------------------------------------------------------------- PIED
def pied(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GRIS)
    canvas.drawString(22 * mm, 12 * mm,
                      "PASS LOISIRS 2.0 — dossier de fonctionnement — 11/09/2026 — données de recette, mode FICTIF")
    canvas.drawRightString(188 * mm, 12 * mm, "page %d" % doc.page)
    canvas.setStrokeColor(colors.HexColor("#d5d8de"))
    canvas.setLineWidth(0.4)
    canvas.line(22 * mm, 15 * mm, 188 * mm, 15 * mm)
    canvas.restoreState()


doc = BaseDocTemplate(SORTIE, pagesize=A4,
                      leftMargin=22 * mm, rightMargin=22 * mm,
                      topMargin=18 * mm, bottomMargin=20 * mm,
                      title="PASS LOISIRS 2.0 - Dossier de fonctionnement",
                      author="Test informatique du 11/09/2026")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=pied)])
doc.build(flow)
print("PDF genere :", SORTIE)
