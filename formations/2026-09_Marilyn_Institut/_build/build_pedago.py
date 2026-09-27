"""Kit à découper, quiz papier + corrigé, grilles critériées nominatives, ressource PDF stagiaire, conducteur formateur.

Corrections apportées au kit du 22/09/2026 :
- retrait de « La Buse » (hôtel du Boucan Canot) et de « session des 3 journées » : la formation a lieu au C.R.E.P.S, sur 1 journée par groupe ;
- jeu n°3 : la carte 4 est bien un BÉNÉFICE (oubliée dans l'ancien corrigé) ;
- jeux MANAGEMENT retirés (autre action, hors convention C-MAR-2026-01) ;
- ajout de 4 jeux issus du positionnement : Ring des objections, Phrases d'appui, Cartes Remarques, cartons-réponses A/B/C.
"""
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

import donnees as D
from docx_lib import Doc, BLEU, GRIS, ROUGE, _shade, fixer_largeurs, _cant_split, HEX_OR_CLAIR
from quiz_data import QUIZ, LETTRES

OUT = D.SORTIE / "04_PEDAGOGIE"


# ============================================================== KIT À DÉCOUPER
def _pointilles(table):
    tblPr = table._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "dashed"); e.set(qn("w:sz"), "8"); e.set(qn("w:space"), "0"); e.set(qn("w:color"), "5A5F6A")
        b.append(e)
    tblPr.append(b)


def cartes(doc, jeu, cartes_, hauteur=6.2, cols=2, taille=16, fond=None):
    """Grille de cartes à découper (traits pointillés). cartes_ = [(entête, titre, texte)]."""
    t = doc.d.add_table(rows=0, cols=cols)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    _pointilles(t)
    for i in range(0, len(cartes_), cols):
        row = t.add_row(); row.height = Cm(hauteur); _cant_split(row)
        for j in range(cols):
            c = row.cells[j]; c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if i + j >= len(cartes_):
                continue
            ent, titre, texte = cartes_[i + j]
            if fond:
                _shade(c, fond)
            p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(f"{jeu} · {ent}"); r.font.size = Pt(10); r.font.color.rgb = GRIS
            if titre:
                p = c.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(titre); r.bold = True; r.font.size = Pt(taille + 3); r.font.color.rgb = BLEU
            for ligne in (texte if isinstance(texte, list) else [texte]):
                p = c.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.line_spacing = 1.1; p.paragraph_format.space_after = Pt(2)
                doc._run(p, ligne, taille)
    larg = doc.largeur / 360000
    fixer_largeurs(t, [larg / cols] * cols)
    fin = doc.d.add_paragraph(); fin.paragraph_format.space_after = Pt(0)


CLIENTES = [
    ("LA PRESSÉE", ["Elle entre en regardant sa montre : « J'ai 40 minutes, pas une de plus. »", ("Piège : bâcler l'accueil pour gagner du temps.", {"i": True})]),
    ("LA SILENCIEUSE", ["Elle répond « oui », « non », « ça va ». Ni enthousiasme, ni plainte.", ("Piège : combler le silence en parlant de soi.", {"i": True})]),
    ("LA COMPARATRICE", ["« À l'institut d'à côté, c'est 15 euros moins cher. »", ("Piège : critiquer le concurrent ou s'excuser du prix.", {"i": True})]),
    ("LA FIDÈLE QUI N'ACHÈTE PAS", ["Elle vient depuis 4 ans, toujours la même prestation, jamais un produit.", ("Piège : ne rien proposer « parce qu'elle n'achète jamais ».", {"i": True})]),
    ("LA MÉCONTENTE", ["Son vernis a tenu 4 jours. Elle le dit fort, dans la salle d'attente.", ("Piège : se défendre, ou dire que c'est de sa faute.", {"i": True})]),
    ("LA PREMIÈRE FOIS", ["Elle n'est jamais venue en institut. Elle ne sait pas où poser ses affaires.", ("Piège : parler avec le vocabulaire du métier.", {"i": True})]),
    ("L'ACCOMPAGNÉE", ["Elle vient avec une amie qui commente tout, ou avec un enfant de 4 ans.", ("Piège : ignorer la personne qui l'accompagne.", {"i": True})]),
    ("LA CLIENTE V.I.P.", ["Elle dépense beaucoup et attend d'être reconnue tout de suite.", ("Piège : la traiter comme les autres… ou trop différemment.", {"i": True})]),
]
QUESTIONS = ["« Qu'est-ce qui vous amène aujourd'hui ? »", "« Comment votre peau réagit-elle depuis notre dernier rendez-vous ? »",
             "« Vous voulez le forfait ou pas ? »", "« Qu'est-ce que vous aimeriez changer en priorité ? »",
             "« Vous avez pris du soleil, on dirait ? »", "« Qu'est-ce que vous utilisez le matin, chez vous ? »",
             "« Vous n'avez toujours pas racheté le sérum ? »", "« Racontez-moi comment se passe votre routine du soir. »",
             "« C'est pour une occasion particulière ? »", "« Vous ne trouvez pas que vos ongles sont abîmés ? »",
             "« Sur une échelle de 1 à 10, où en êtes-vous de votre confort ? »", "« Vous préférez qu'on commence par les mains ou le visage ? »"]
BENEF = ["« Contient 12 % de vitamine C encapsulée. »", "« Vous retrouverez ce teint lumineux dont vous me parliez. »",
         "« Formule sans paraben ni silicone. »", "« Vous n'aurez plus à refaire vos ongles avant votre mariage. »",
         "« Notre marque est fabriquée en France. »", "« Vous gagnerez 10 minutes chaque matin. »",
         "« Flacon de 30 ml avec pompe doseuse. »", "« Vous ne sentirez plus ces tiraillements après la douche. »",
         "« C'est notre meilleure vente du mois. »", "« Vous pourrez enfin porter des sandales sans y penser. »",
         "« Testé sous contrôle dermatologique. »", "« Votre épilation tiendra une semaine de plus. »",
         "« Texture gel-crème à absorption rapide. »", "« Vous éviterez les poils incarnés dont vous vous plaignez. »",
         "« Certifié bio par un organisme indépendant. »", "« Vous n'aurez plus à revenir en urgence entre deux rendez-vous. »",
         "« Disponible en trois teintes. »", "« Vous partirez en vacances sans vous soucier de vos ongles. »",
         "« Notre cabine est équipée d'une table chauffante. »", "« Vous vous réveillerez la peau souple, même en saison sèche. »"]
MERVEILLES = [
    ("AESOP — Australie", ["Le conseiller applique le produit sur la main du client, au lavabo, avant tout discours.", ("À voler : un geste offert à l'arrivée.", {"b": True})]),
    ("LUSH — Royaume-Uni", ["Rien ne se vend sans être touché, senti, essayé.", ("À voler : ne jamais citer un produit sans le faire toucher.", {"b": True})]),
    ("SEPHORA — France", ["Diagnostic gratuit, essai libre, fidélité à paliers visibles.", ("À voler : un diagnostic offert de 5 minutes en fin de soin.", {"b": True})]),
    ("RITZ-CARLTON — hôtellerie", ["Chaque employé peut engager jusqu'à 2 000 $ pour réparer un incident client, sans autorisation.", ("À voler : un geste commercial décidé seule, avec un plafond fixé.", {"b": True})]),
    ("APPLE STORE — monde", ["Cinq étapes connues de toute l'équipe : aborder, sonder, présenter, écouter, conclure.", ("À voler : le même accueil dans les deux instituts.", {"b": True})]),
    ("OMOTENASHI — Japon", ["Le besoin est satisfait avant d'être exprimé : on se souvient du prénom, de la boisson, de la place préférée.", ("À voler : 3 préférences notées sur la fiche.", {"b": True})]),
    ("BASTIEN GONZALEZ — pédicure", ["L'acte le plus banal du métier, ritualisé et nommé, vendu dans les plus grands palaces.", ("À voler : renommer et ritualiser UNE prestation de la carte.", {"b": True})]),
]
OBJECTIONS = [
    ("« C'est cher. »", "Par rapport à quoi ?"),
    ("« Je vais réfléchir. »", "Qu'est-ce qui vous fait hésiter ?"),
    ("« J'en ai déjà un à la maison. »", "Lequel ? Qu'en pensez-vous ?"),
    ("« Je ne suis pas sûre que ça marche sur moi. »", "Qu'est-ce qui vous rassurerait ?"),
    ("« Il faut que j'en parle à mon conjoint. »", "Qu'est-ce qu'il ou elle voudra savoir ?"),
    ("« C'est moins cher sur internet. »", "Revenir au conseil et au suivi"),
    ("« Je n'ai pas le temps de revenir. »", "Quel jour vous arrange le plus ?"),
    ("« La dernière fois, ça n'a pas tenu. »", "Accueillir, écouter, proposer une solution"),
    ("« Je ne mets jamais de crème. »", "Partir de sa routine réelle"),
    ("« Je reviendrai quand j'aurai l'argent. »", "Proposer sans insister, noter le souhait"),
]
APPUI = [
    ("ACCUEILLIR", "« Bonjour [prénom], bienvenue ! Je vous installe ? »"),
    ("OUVRIR", "« Qu'est-ce qui vous ferait plaisir aujourd'hui ? »"),
    ("REFORMULER", "« Si je vous ai bien comprise, vous aimeriez… »"),
    ("RELIER", "« … ce qui veut dire pour vous que… »"),
    ("RECOMMANDER", "« Pour ce que vous m'avez dit, je vous conseille UNE chose : … »"),
    ("ANNONCER LE PRIX", "« Il est à … euros. » (puis silence)"),
    ("OBJECTION", "« Je comprends. Qu'est-ce qui vous fait hésiter ? »"),
    ("REPRENDRE RDV", "« Pour garder ce résultat, on se revoit dans 4 semaines : plutôt mardi ou samedi ? »"),
    ("REMARQUE REÇUE", "« D'accord. Si je comprends bien… Je propose de… »"),
    ("DIRE AU REVOIR", "« Merci [prénom], à très vite ! » (on raccompagne à la porte)"),
]
REMARQUES = [
    ("DOUCE", "« Pense à proposer le prochain rendez-vous, ce matin tu l'as oublié deux fois. »"),
    ("DOUCE", "« Ta cabine n'était pas prête pour la cliente de 14h. »"),
    ("MOYENNE", "« Une cliente m'a dit qu'elle t'avait trouvée pressée. »"),
    ("MOYENNE", "« Tu as recommandé trois produits à la même cliente, elle est partie sans rien. »"),
    ("FERME", "« C'est la troisième fois ce mois-ci que la fiche cliente n'est pas remplie. »"),
    ("FERME", "« Le téléphone ne doit pas être visible en cabine. Je te l'ai déjà dit. »"),
]


def kit():
    doc = Doc("Kit d'exercices à découper", "Vente-conseil — M.A.R.I.L.Y.N. — à imprimer et découper",
              f"Action {D.ACTION['reference']} — 1 jeu par groupe (le même kit sert le lundi et le mardi)", corps=12)
    doc.encadre("Fabrication — 10 minutes", [
        "Imprimer en recto simple, idéalement sur papier 160 g (ou papier ordinaire + plastification pour réutiliser).",
        "Découper le long des traits pointillés : chaque case est une carte (environ 8,5 × 6 cm). Texte en 16 points minimum.",
        "Ranger chaque jeu dans une enveloppe portant son numéro. Prévoir des post-it, un marqueur et un chrono.",
        "Toutes les situations sont fictives : aucune ne décrit une salariée ou une cliente réelle. Consigne en début de jeu : « on ne nomme personne ».",
    ])
    doc.table([["N°", "Jeu", "Séquence", "Durée"],
               ["1", "Les 8 Clientes", "A — Accueil", "20 min"], ["2", "Les 12 Questions d'Or", "R — Ressenti", "15 min"],
               ["3", "Bénéfice ou caractéristique ? (20 cartes)", "L — Lien", "12 min"], ["4", "Le Ring des objections (NOUVEAU)", "L — Lien", "25 min"],
               ["5", "Phrases d'appui (NOUVEAU)", "Toute la journée", "—"], ["6", "Cartes Remarques — Boomerang (NOUVEAU)", "N — Nous", "12 min"],
               ["7", "Les 7 Merveilles de la Beauté", "N — Nous", "18 min"], ["8", "Cartons-réponses A / B / C (NOUVEAU)", "Quiz", "20 min"],
               ["T1-T6", "Trames d'atelier (Photomaton, Charte d'Image, Voyage Cliente, Mes chiffres, Roue des Temps Creux, 10 standards)", "Livrables", "—"]],
              [1.4, 9.4, 4, 2.6], taille=10)
    doc.h1("Jeu n°1 — Les 8 Clientes", nouvelle_page=True)
    doc.p("Chacune tire une carte et joue la cliente 3 minutes ; sa binôme l'accueille. Les autres observent (grille : critères 2 et 3). "
          "Le « piège » est l'axe du débriefing.", taille=11)
    cartes(doc, "JEU 1", [(f"CLIENTE {i + 1}/8", t, x) for i, (t, x) in enumerate(CLIENTES)], hauteur=4.7, taille=14)
    doc.h1("Jeu n°2 — Les 12 Questions d'Or", nouvelle_page=True)
    doc.p("Classer en 3 familles : la question qui OUVRE / qui FERME / qui VEXE. Corrigé en fin de kit.", taille=11)
    cartes(doc, "JEU 2", [(f"QUESTION {i + 1}/12", "", q) for i, q in enumerate(QUESTIONS)], hauteur=3.4, taille=16)
    doc.h1("Jeu n°3 — Bénéfice ou caractéristique ?", nouvelle_page=True)
    cartes(doc, "JEU 3", [(f"CARTE {i + 1}/20", "", q) for i, q in enumerate(BENEF)], hauteur=2.15, taille=14)
    doc.h1("Jeu n°4 — Le Ring des objections", nouvelle_page=True)
    doc.p("Je tire une carte, je réponds en 4 temps : Accueillir · Questionner · Répondre par le bénéfice · Vérifier. 3 rounds de 2 minutes.", taille=11)
    cartes(doc, "JEU 4", [(f"OBJECTION {i + 1}/10", o, "") for i, (o, _) in enumerate(OBJECTIONS)], hauteur=4.3, taille=16, fond=HEX_OR_CLAIR)
    doc.h1("Jeu n°5 — Mes phrases d'appui", nouvelle_page=True)
    doc.p("Cartes à garder en main pendant les jeux de rôle — et à glisser dans la poche de la blouse ensuite. On a le droit de les lire !", taille=11)
    cartes(doc, "PHRASE D'APPUI", [(f"{i + 1}/10", t, x) for i, (t, x) in enumerate(APPUI)], hauteur=4.1, taille=15)
    doc.h1("Jeu n°6 — Cartes Remarques (le Boomerang)", nouvelle_page=True)
    doc.p("Le formateur lit une remarque ; la stagiaire répond en A.R.P. D'abord en binôme. Commencer par les cartes DOUCES.", taille=11)
    cartes(doc, "BOOMERANG", [(f"{i + 1}/6", n, r) for i, (n, r) in enumerate(REMARQUES)], hauteur=5.2, taille=15)
    doc.h1("Jeu n°7 — Les 7 Merveilles de la Beauté", nouvelle_page=True)
    doc.p("Question unique : « Qu'est-ce qu'on installe chez Marilyn dès lundi, sans budget et sans autorisation ? » "
          "Une idée = une action + un responsable + une date.", taille=11)
    cartes(doc, "MERVEILLE", [(f"{i + 1}/7", t, x) for i, (t, x) in enumerate(MERVEILLES)], hauteur=4.9, taille=14)
    doc.p("Sources : J. Michelli, The New Gold Standard, McGraw-Hill, 2008 (Ritz-Carlton) ; C. Gallo, The Apple Experience, McGraw-Hill, 2012 ; "
          "sites officiels des marques citées.", taille=9)
    doc.h1("Jeu n°8 — Cartons-réponses du quiz (un jeu par équipe)", nouvelle_page=True)
    t = doc.d.add_table(rows=1, cols=3); _pointilles(t)
    for j, l in enumerate("ABC"):
        c = t.rows[0].cells[j]; c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER; _shade(c, "1B3A6B")
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(l); r.bold = True; r.font.size = Pt(150); r.font.color.rgb = RGBColor(0xC9, 0xA8, 0x4C)
    t.rows[0].height = Cm(8)
    fixer_largeurs(t, [doc.largeur / 360000 / 3] * 3)
    doc.p("Imprimer cette page 2 fois (une par équipe).", taille=11, italique=True)
    doc.saut()

    # Trames
    doc.h1("T1 — Le Photomaton inversé")
    doc.table([["", "Ce que je CROIS montrer", "Ce que ma binôme VOIT en 3 secondes"],
               ["Mon visage", "", ""], ["Ma posture", "", ""], ["Ma tenue", "", ""], ["Ma voix", "", ""]],
              [3.4, 7, 7], taille=12, hauteur_cm=2.2)
    doc.p("Règle : on décrit un fait visible (« bras croisés »), jamais un jugement (« tu as l'air fermée »).", taille=11, italique=True)
    doc.h1("T2 — La Charte d'Image Marilyn (livrable n°1)", nouvelle_page=True)
    doc.table([["Point", "Notre règle commune (concrète et vérifiable)", "Votes"]] +
              [[x, "", ""] for x in ["Tenue", "Cheveux", "Ongles", "Bijoux", "Chaussures", "Téléphone", "Posture", "Voix", "Mastication", "Regard"]],
              [3.2, 11.4, 2.8], taille=12, hauteur_cm=1.25)
    doc.h1("T3 — La Carte du Voyage Cliente (livrable n°2)", nouvelle_page=True)
    doc.table([["Étape", "🙂", "😐", "☹", "Correctif si ☹"]] +
              [[x, "", "", "", ""] for x in ["1. Prise de RDV", "2. Arrivée, parking", "3. Porte", "4. Accueil", "5. Attente", "6. Vestiaire",
                                             "7. Installation", "8. Soin", "9. Sortie de cabine", "10. Conseil", "11. Encaissement", "12. Au revoir"]],
              [4.6, 1.3, 1.3, 1.3, 8.9], taille=12, hauteur_cm=1.1, centre_cols=(1, 2, 3))
    doc.h1("T4 — Mon agenda, mes chiffres (exemple fictif)", nouvelle_page=True)
    doc.table([["Calcul", "Résultat"],
               ["Prix moyen d'un soin (fictif)", "45 €"], ["Fréquence (toutes les 4 semaines)", "13 visites par an"],
               ["Valeur d'une cliente fidèle sur un an", "13 × 45 € = ........ €"],
               ["1 reprise de RDV de plus par jour × 5 jours × 46 semaines", "........ clientes"],
               ["Mes 3 indicateurs", "Remplissage de mon agenda · taux de reprise de RDV · ventes produits"]],
              [10, 7.4], taille=12, hauteur_cm=1.2)
    doc.h1("T5 — La Roue des Temps Creux (livrable n°4)", nouvelle_page=True)
    doc.table([["", "EFFORT FAIBLE", "EFFORT IMPORTANT"],
               ["VALEUR FORTE", "① À faire d'abord :\n\n\n\n", "② À planifier :\n\n\n\n"],
               ["VALEUR FAIBLE", "③ Si j'ai le temps :\n\n\n\n", "④ À oublier :\n\n\n\n"]],
              [3.8, 6.8, 6.8], taille=12, hauteur_cm=4.8)
    doc.h1("T6 — Nos 10 standards communs (livrable n°5)", nouvelle_page=True)
    doc.table([["N°", "Action (ce qu'on fait)", "Qui", "À partir de quand"]] +
              [[str(i), "" if i < 10 else "Rituel d'équipe (ex. 5 min d'idées par semaine) — proposé à la direction", "", ""] for i in range(1, 11)],
              [1.2, 10.2, 2.6, 3.4], taille=11, hauteur_cm=1.05)
    doc.h1("Corrigés (réservés au formateur)", nouvelle_page=True)
    doc.table([["Jeu", "Corrigé"],
               ["2 — Questions", "OUVRENT : 1, 2, 4, 6, 8, 9, 11. FERMENT : 3, 12 (utiles pour conclure, jamais pour découvrir). VEXENT : 5, 7, 10."],
               ["3 — Bénéfices", "BÉNÉFICES : cartes 2, 4, 6, 8, 10, 12, 14, 16, 18, 20. Les autres : caractéristiques ou preuve sociale (carte 9)."],
               ["4 — Objections", [f"{o} → {p}" for o, p in OBJECTIONS]]],
              [3.5, 13.9], taille=10)
    return doc.enregistrer(OUT / "Kit_exercices_a_decouper_VENTE.docx")


# ================================================================ QUIZ PAPIER
def quiz_papier():
    doc = Doc("Quiz d'évaluation des acquis", "10 questions — une seule bonne réponse — 10 minutes",
              D.ACTION["intitule"], corps=13, mention_eval=True)
    doc.p(("Prénom et nom : ", {"b": True}), ".....................................................   ", ("Date : ", {"b": True}), "......../09/2026")
    doc.p("Cochez UNE case par question. Pas de piège, pas de note négative. Seuil de réussite : 7 / 10. Correction commentée juste après.", taille=12)
    for n, q in enumerate(QUIZ, 1):
        doc.p((f"{n}. {q['q']}", {"b": True, "c": BLEU}), taille=13)
        for k, c in enumerate(q["choix"]):
            doc.p(f"☐  {LETTRES[k]}. {c}", taille=13, apres=1)
    doc.p(("Score : ........ / 10", {"b": True}), taille=14)
    return doc.enregistrer(OUT / "Quiz_papier_feuille_reponse_individuelle.docx")


def quiz_corrige():
    doc = Doc("Quiz — corrigé commenté", "DOCUMENT FORMATEUR — NE PAS DISTRIBUER", D.ACTION["intitule"], corps=11, mention_eval=True)
    lignes = [["N°", "Notion (objectif)", "Réponse", "Argument à donner au groupe"]]
    for n, q in enumerate(QUIZ, 1):
        lignes.append([str(n), f"{q['theme']} (obj. {q['objectif']})", f"{LETTRES[q['bonne']]} — {q['choix'][q['bonne']]}", q["explication"]])
    doc.table(lignes, [1, 3.6, 5, 7.8], taille=9.5)
    doc.h2("Barème et suites données")
    doc.table([["Score", "Appréciation", "Suite donnée"],
               ["9-10", "Acquis — maîtrise", "Peut servir de référente auprès des collègues"],
               ["7-8", "Acquis", "Revoir les notions manquées avec la ressource PDF"],
               ["5-6", "En cours d'acquisition", "Reprise ciblée de 10 minutes en fin de session"],
               ["0-4", "Non acquis", "Point individuel avec le formateur, proposition de consolidation"]], [2.2, 4.6, 10.6], taille=10)
    doc.p("Résultats individuels conservés 3 ans par YEBA FORMATIONS. L'employeur ne reçoit qu'une moyenne de groupe, sans nom. "
          "La correction est faite par le formateur, sans IA.", taille=10)
    return doc.enregistrer(OUT / "Quiz_corrige_commente_FORMATEUR.docx")


# ============================================================ GRILLE CRITÉRIÉE
CRITERES = [
    ("Tenue et attitude professionnelle", "Respecte les 10 points de la Charte d'Image Marilyn co-construite le matin."),
    ("Accueil — 7 premières secondes", "S'interrompt, va vers la cliente, regard, sourire, salue, la nomme si elle est connue."),
    ("Parcours cliente de A à Z", "Prend en charge, annonce le déroulé, accompagne la sortie de cabine, raccompagne."),
    ("Découverte — S.O.I.N.", "Au moins 3 questions ouvertes avant toute proposition ; reformule avec les mots de la cliente."),
    ("Argumentation par le bénéfice", "Présente chaque produit par ce qu'il apporte à CETTE cliente."),
    ("Recommandation — P.E.R.L.E.", "Propose UNE seule chose, reliée à un besoin exprimé ; laisse choisir."),
    ("Prix et objections", "Annonce le prix sans se justifier ni brader ; accueille, questionne, répond, vérifie."),
    ("Reprise de rendez-vous", "Propose systématiquement le prochain RDV avec la formulation standard du groupe."),
    ("Autonomie — temps creux", "Choisit une action utile de la Roue des Temps Creux et sait justifier la priorité."),
    ("Remarque reçue — A.R.P.", "Accuse réception, reformule, propose ; ne se justifie pas, ne coupe pas la parole."),
    ("Contribution aux résultats", "Cite ses 3 indicateurs : remplissage de l'agenda, reprise de RDV, ventes produits."),
    ("Communication et esprit d'équipe", "Transmet une information complète ; ne critique pas une collègue devant une cliente."),
    ("RGPD — fiche cliente", "Ne note aucune donnée de santé inutile ; ne lit pas une fiche à voix haute ; sait expliquer pourquoi on note."),
]


def grille(s):
    se = D.SESSIONS[s["session"]]
    doc = Doc("Grille critériée d'évaluation", f"{D.nom_complet(s)} — session {s['session']} — {se['date']}", D.ACTION["intitule"],
              corps=10, paysage=True, mention_eval=True, compact=True)
    doc.p("Échelle : 0 = non acquis (même après relance) · 1 = en cours (partiel ou après relance) · 2 = acquis (spontané et correct) · "
          "3 = maîtrisé (adapté, et sait l'expliquer). Preuve obligatoire si 0 ou 3. Score sur 39 — seuil 26/39 sans aucun critère à 0.", taille=9.5)
    lignes = [["N°", "Critère", "Ce que je dois voir ou entendre", "0", "1", "2", "3", "Preuve observée / axe de progrès"]]
    for i, (c, ind) in enumerate(CRITERES, 1):
        lignes.append([str(i), c, ind, "☐", "☐", "☐", "☐", ""])
    doc.table(lignes, [0.8, 4.4, 8.6, 0.9, 0.9, 0.9, 0.9, 8.6], taille=8.5, centre_cols=(0, 3, 4, 5, 6))
    doc.table([["Score : ....... / 39", "Résultat : ☐ Acquis   ☐ À consolider", "3 points forts :", "2 axes de progrès :", "Signature du formateur :"],
               ["", "", "", "", ""]], [4, 5.6, 5.8, 5.8, 4.8], taille=9, hauteur_cm=1.4, zebre=False)
    nom = (f"SI_PRESENTE_{s['prenom']}_" if s.get("presence_incertaine") else "") + \
        f"Grille_S{s['session']}_{s['nom'].replace(' ', '_')}_{s['prenom']}.docx"
    return doc.enregistrer(OUT / "Grilles_criteriees" / nom)


# ============================================================ RESSOURCE PDF
def ressource():
    doc = Doc("Ressource stagiaire", "L'essentiel de la journée, à garder et à relire", D.ACTION["intitule"], corps=12)
    doc.p("Ce document reprend tout ce que nous avons vu et pratiqué. Relisez une partie par semaine, et testez une phrase d'appui par jour. "
          "Version en 16 points disponible sur demande.", italique=True, taille=11)
    doc.h1("Le protocole M.A.R.I.L.Y.N. en une page")
    doc.table([["Lettre", "Réflexe", "La phrase à retenir"],
               ["M — Miroir", "Mon image parle avant moi", "Apparence, langage, comportement : les trois se voient en 3 secondes."],
               ["A — Accueil", "Chaque contact est un moment de vérité", "Je m'arrête, je regarde, je souris, bonjour, son prénom."],
               ["R — Ressenti", "Je découvre avant de proposer", "S.O.I.N. : Situer, Observer, Interroger, Nommer."],
               ["I — Initiative", "Un temps creux est un temps utile", "Forte valeur et faible effort d'abord."],
               ["L — Lien", "Je conseille, je ne force pas", "P.E.R.L.E. : UNE recommandation, par le bénéfice."],
               ["Y — Y revenir", "Le prochain RDV se prend avant de partir", "« On se revoit dans 4 semaines : mardi ou samedi ? »"],
               ["N — Nous", "Une remarque est une information", "A.R.P. : Accuser réception, Reformuler, Proposer."]],
              [3.4, 5.6, 8.4], taille=11)

    doc.h1("M — Le Miroir : mon image professionnelle")
    doc.p("L'image professionnelle a trois niveaux : l'apparence (tenue, cheveux, ongles, bijoux, chaussures), le langage "
          "(mots, voix, tutoiement ou vouvoiement) et le comportement (téléphone, posture, regard, mastication).")
    doc.encadre("Le « 7 % – 38 % – 55 % » : attention au mythe", [
        "Albert Mehrabian (Silent Messages, 1971) a étudié des mots isolés exprimant un sentiment, en laboratoire. Il n'a jamais dit que les mots "
        "comptent pour 7 % dans toute conversation.",
        "Ce qu'on peut retenir : quand la voix et le visage contredisent les mots, c'est la voix et le visage qu'on croit. "
        "« Bienvenue » dit avec un visage fermé ne dit pas bienvenue."])
    doc.p(("Ma voix : ", {"b": True}), "débit lent, phrases courtes, sourire qui s'entend, une pause avant le prix.")

    doc.h1("A — L'Accueil : le voyage de la cliente")
    doc.p("Jan Carlzon (Moments of Truth, 1987) appelle « moment de vérité » chaque contact où la cliente se fait un avis. Dans un institut, "
          "on en compte au moins 12 : prise de RDV, arrivée, porte, accueil, attente, vestiaire, installation, soin, sortie de cabine, conseil, "
          "encaissement, au revoir.")
    doc.p(("La règle du pic et de la fin ", {"b": True}), "(Kahneman et al., 1993) : on se souvient surtout du moment le plus fort et du dernier "
          "moment. La sortie de cabine et l'encaissement comptent donc énormément — et ce sont souvent les étapes les plus rapides.")
    doc.p(("Les 7 premières secondes : ", {"b": True}), "je m'arrête · je regarde · je souris · « Bonjour » · son prénom.")

    doc.h1("R — Le Ressenti : découvrir le besoin")
    doc.table([["Lettre", "Je fais", "Exemple"],
               ["S — Situer", "Je comprends le contexte", "« C'est pour une occasion particulière ? »"],
               ["O — Observer", "Je remarque un indice concret", "« Je vois que vos mains sont un peu sèches. »"],
               ["I — Interroger", "Au moins 3 questions ouvertes", "« Racontez-moi votre routine du soir. »"],
               ["N — Nommer", "Je reformule avec SES mots", "« Si je vous ai bien comprise, vous aimeriez… »"]],
              [3.4, 5.6, 8.4], taille=11)
    doc.p("Une question qui ferme trop tôt coûte la vente. Une question qui vexe coûte la vente ET la cliente "
          "(« Vous avez pris du soleil, on dirait ? »).")
    doc.encadre("[RGPD] La fiche cliente", [
        "J'écris ce qui est utile au soin et les préférences de la cliente. Je n'écris jamais un avis sur la personne ni un diagnostic.",
        "Une allergie, une contre-indication, une grossesse sont des données de santé (RGPD, art. 9) : seulement si c'est nécessaire au soin, "
        "accès réservé à l'équipe, jamais lues à voix haute, jamais envoyées par messagerie personnelle.",
        "Si la cliente demande pourquoi : « Pour votre sécurité pendant le soin. »"])

    doc.h1("L — Le Lien : conseiller sans forcer")
    doc.table([["Lettre", "Je fais"],
               ["P — Partir de son besoin", "« Vous m'avez dit que… »"],
               ["E — Expliquer le bénéfice", "« … ce qui veut dire pour vous que… »"],
               ["R — Recommander UNE chose", "La plus utile. Deux produits, ce sont deux doutes."],
               ["L — Laisser choisir", "Je me tais. C'est elle qui décide."],
               ["E — Encaisser sans se justifier", "J'annonce le prix d'une voix stable, sans m'excuser."]],
              [6.4, 11], taille=11)
    doc.p(("Caractéristique ou bénéfice ? ", {"b": True}), "« Contient de la vitamine C » décrit le produit. « Vous retrouverez un teint lumineux » "
          "décrit sa vie à elle. « Meilleure vente du mois » est une preuve sociale, pas un bénéfice.")
    doc.encadre("Promettre juste", [
        "Un cosmétique ne peut pas revendiquer d'effet thérapeutique ni tromper la cliente : on dit « hydrate », « apaise la sensation de tiraillement », "
        "jamais « guérit » ou « soigne l'eczéma » (règlement (CE) n° 1223/2009, art. 20 ; règlement (UE) n° 655/2013)."])
    doc.h2("Les objections : répondre en 4 temps")
    doc.table([["Temps", "Je dis"], ["1. Accueillir", "« Je comprends. »"], ["2. Questionner", "« Par rapport à quoi ? » / « Qu'est-ce qui vous fait hésiter ? »"],
               ["3. Répondre", "Je reviens au bénéfice pour ELLE."], ["4. Vérifier", "« Est-ce que cela répond à votre question ? »"]], [4.4, 13], taille=11)
    doc.table([["Objection", "Première réponse"]] + [[o, p] for o, p in OBJECTIONS], [8, 9.4], taille=11)
    doc.p("Jamais : brader le prix, se justifier sur les charges de l'institut, critiquer un concurrent.", gras=True)

    doc.h1("Y — Y revenir : fidéliser")
    doc.p("Le taux de reprise de rendez-vous (clientes qui reprennent RDV avant de partir ÷ clientes reçues) est l'indicateur n°1 du remplissage "
          "de l'agenda. Mes 3 indicateurs : le remplissage de mon agenda, mon taux de reprise, mes ventes produits.")
    doc.p(("Exemple fictif : ", {"b": True}), "un soin à 45 € toutes les 4 semaines, c'est 13 visites par an, soit 585 € par cliente fidèle.")
    doc.encadre("[RGPD] Les SMS", [
        "Rappel d'un rendez-vous déjà pris : ce n'est pas de la prospection.",
        "Promotion à une cliente existante, pour des soins ou produits analogues : possible si elle en a été informée et peut refuser à chaque "
        "envoi (« STOP »).",
        "Promotion à une personne qui n'est pas cliente : accord préalable obligatoire, par une case jamais pré-cochée "
        "(code des postes et des communications électroniques, art. L.34-5 ; RGPD, art. 6 et 7)."])

    doc.h1("I — L'Initiative : les temps creux")
    doc.p("Classer ses idées selon la valeur et l'effort : d'abord forte valeur et faible effort (rappeler les clientes en retard de RDV, préparer la "
          "cabine suivante, préparer des échantillons, mettre à jour la vitrine).")
    doc.encadre("Check-list 60 secondes entre deux clientes", ["☐ La cabine est prête", "☐ La fiche est à jour", "☐ Le prochain RDV est vérifié",
                                                               "☐ Le produit conseillé est noté", "☐ Je respire"])

    doc.h1("N — Nous : l'équipe et le feedback")
    doc.p("Face à une remarque, on se défend, on se tait, on se justifie… ou on accueille. Seule la dernière réaction fait avancer.")
    doc.p(("A.R.P. : ", {"b": True}), "« D'accord, je note. » → « Si je comprends bien, il faudrait… » → « Je propose de… à partir de… »")
    doc.h1("Mes phrases d'appui")
    doc.table([["Moment", "Phrase"]] + [[t, x] for t, x in APPUI], [5, 12.4], taille=11)
    doc.h1("[IA Act] Photos « avant / après »")
    doc.p("Une photo de cliente ne se publie qu'avec son accord écrit (RGPD). Si l'image est retouchée ou générée par une intelligence artificielle, "
          "cela doit être clairement indiqué (règlement (UE) 2024/1689, art. 50).")
    doc.h1("Sources")
    doc.puces(["J. Carlzon, Moments of Truth, Ballinger, 1987.",
               "D. Kahneman, B. Fredrickson, C. Schreiber, D. Redelmeier, « When more pain is preferred to less », Psychological Science, 1993.",
               "A. Mehrabian, Silent Messages, Wadsworth, 1971.",
               "Règlement (UE) 2016/679 (RGPD), art. 5, 6, 7, 9 ; CNIL, « La prospection commerciale par SMS » (cnil.fr).",
               "Code des postes et des communications électroniques, art. L.34-5.",
               "Règlement (CE) n° 1223/2009 relatif aux produits cosmétiques, art. 20 ; règlement (UE) n° 655/2013.",
               "Règlement (UE) 2024/1689 sur l'intelligence artificielle, art. 50."], taille=10)
    return doc.enregistrer(OUT / "Ressource_stagiaire_complete.docx")


# ============================================================ CONDUCTEUR
def conducteur():
    doc = Doc("Conducteur de séance", "Document formateur — minute par minute", D.ACTION["intitule"], corps=10, paysage=True, compact=True)
    doc.h2("La veille et le jour J — check-list")
    doc.table([["Avant (J-1)", "Le matin (7h30)", "À apporter"],
               [[D.vigilance("conducteur_presence"), D.vigilance("conducteur_groupes"),
                 "☐ Imprimer : émargements, grilles, quiz, positionnement express, droit à l'image, évaluations à chaud", "☐ Découper le kit"],
                ["☐ Vérifier salle SEYCHELLES : vidéoprojecteur, paperboard, chaises à dossier", "☐ Repérer issues de secours et point de rassemblement",
                 "☐ Tester le quiz HTML (sans internet)", "☐ Eau à disposition"],
                ["☐ Ordinateur + adaptateur HDMI", "☐ Clé USB de secours (diaporama en PDF)", "☐ Post-it, marqueurs, panier, chrono",
                 "☐ Livrets d'accueil de secours"]]],
              [8.6, 8.6, 8.6], taille=9, entete=True)
    lignes = [["Horaire", "Séquence", "Déroulé", "Méthode", "Évaluation / preuve"]]
    methodes = {"Accueil & ouverture": "Expérientielle", "Contrat de la journée": "Participative", "Pause": "—",
                "Pause déjeuner (repas à prévoir)": "—", "Évaluation des acquis": "Ludique (équipes)", "Clôture": "Réflexive"}
    preuves = {"Accueil & ouverture": "Émargement matin", "Contrat de la journée": "Positionnement express (matin)",
               "Le Miroir — image professionnelle": "Livrable : Charte d'Image — grille crit. 1",
               "L'Accueil — parcours cliente": "Livrable : Voyage Cliente — grille crit. 2, 3",
               "Le Ressenti — découvrir le besoin": "Grille crit. 4, 13", "Réveil « Les 7 secondes »": "Émargement après-midi",
               "Le Lien — conseiller sans forcer": "Grille crit. 5, 6, 7", "« Y revenir » — fidéliser": "Livrable : Phrase qui Rebooke — crit. 8, 11",
               "L'Initiative — temps creux": "Livrable : Roue — crit. 9", "Nous — équipe et feedback": "Livrable : 10 standards — crit. 10, 12",
               "Évaluation des acquis": "Quiz individuel /10", "Clôture": "Positionnement soir, satisfaction, promesse"}
    for d_, f, l, t, c, p in D.PROGRAMME:
        lignes.append([f"{d_}-{f}", (l + " — " if l else "") + t, c, methodes.get(t, f"Active ({p} min de pratique)"), preuves.get(t, "—")])
    doc.table(lignes, [2.2, 4.8, 10.4, 3.6, 4.8], taille=8.5)
    tot, prat = D.bilan_temps()
    doc.p(f"Temps de formation hors déjeuner : {tot // 60} h {tot % 60:02d} dont {prat} min de pratique, soit {round(prat / tot * 100)} % (engagement contractuel : 70 %).",
          gras=True, taille=10)
    doc.h2("Plans B")
    doc.table([["Situation", "Réponse"],
               ["Groupe de 3 (absence)", "Trinômes : cliente / conseillère / observatrice. Le formateur joue la cliente si besoin."],
               ["Retard important d'une stagiaire", "Émargement avec l'heure réelle d'arrivée ; heures non suivies ni attestées ni facturées à l'OPCO (convention, art. 8)."],
               ["Vidéoprojecteur en panne", "Diaporama en PDF imprimé en A3 pour les séquences clés ; quiz papier par équipes."],
               ["Stagiaire mal à l'aise en jeu de rôle", "Joker, rôle d'observatrice, passage en binôme seulement. Jamais d'obligation devant le groupe."],
               ["Une stagiaire cite une cliente ou une collègue réelle", "Reformuler immédiatement de façon anonyme (RGPD, minimisation)."],
               ["Une stagiaire révèle une difficulté sérieuse (souffrance, conflit, violence)", "Échange individuel, confidentiel, hors du groupe ; orientation (3919, médecine du travail) ; rien dans les grilles."]],
              [7, 18.8], taille=9)
    return doc.enregistrer(OUT / "Conducteur_de_seance_FORMATEUR.docx")


def grille_vierge():
    vierge = {"prenom": "", "nom": "", "session": 1}
    se = D.SESSIONS[1]
    doc = Doc("Grille critériée d'évaluation", "Modèle vierge — Nom : ................................ Date : ......../......../2026",
              D.ACTION["intitule"], corps=10, paysage=True, mention_eval=True, compact=True)
    doc.p("Échelle : 0 = non acquis · 1 = en cours · 2 = acquis · 3 = maîtrisé. Preuve obligatoire si 0 ou 3. "
          "Score sur 39 — seuil 26/39 sans aucun critère à 0.", taille=9.5)
    lignes = [["N°", "Critère", "Ce que je dois voir ou entendre", "0", "1", "2", "3", "Preuve observée / axe de progrès"]]
    for i, (c, ind) in enumerate(CRITERES, 1):
        lignes.append([str(i), c, ind, "☐", "☐", "☐", "☐", ""])
    doc.table(lignes, [0.8, 4.4, 8.6, 0.9, 0.9, 0.9, 0.9, 8.6], taille=8.5, centre_cols=(0, 3, 4, 5, 6))
    return doc.enregistrer(OUT / "Grille_criteriee_VIERGE.docx")


def construire():
    out = [kit(), quiz_papier(), quiz_corrige(), ressource(), conducteur(), grille_vierge()]
    out += [grille(s) for s in D.stagiaires()]
    return out


if __name__ == "__main__":
    for f in construire():
        print(f.relative_to(D.SORTIE))
