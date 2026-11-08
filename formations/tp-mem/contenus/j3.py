import os

from aides import cartes, encadre, flux, pyramide, tableau

PRODUITS = [  # produit, PA HT, PV HT, taux de TVA (La Réunion)
    ("Tongs (paire)", 6.00, 10.00, 0.085), ("Ballon de foot", 9.50, 19.90, 0.085), ("Gourde isotherme", 7.20, 14.40, 0.085),
    ("Mangues (kg)", 2.10, 3.50, 0.021), ("Rhum arrangé 70 cl", 11.00, 18.50, 0.085), ("Pain (baguette)", 0.45, 0.90, 0.021)]
INDIC = [  # indicateur, octobre 2026, octobre 2025
    ("Entrées en magasin", 12400, 13100), ("Nombre de tickets", 2480, 2489), ("CA HT (€)", 148800, 141800),
    ("Articles vendus", 4464, 4231), ("Heures travaillées", 1240, 1210)]


def fichiers(dossier):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    ent, blanc = PatternFill("solid", fgColor="0B3D4A"), Font(name="Arial", size=12, bold=True, color="FFFFFF")
    for corrige in (False, True):
        wb = Workbook()
        ws = wb.active
        ws.title = "1-Prix et marges"
        ws["A1"] = "Sport Évasion (fictif) · calculs de prix · TVA La Réunion : 8,5 % (normal) / 2,1 % (réduit)"
        ws["A1"].font = Font(name="Arial", size=13, bold=True)
        cols = ["Produit", "PA HT", "PV HT", "TVA", "PV TTC", "Marge unitaire", "Taux de marge", "Taux de marque", "Coefficient"]
        for j, c in enumerate(cols, 1):
            x = ws.cell(row=3, column=j, value=c); x.fill, x.font = ent, blanc
        for i, (p, pa, pv, t) in enumerate(PRODUITS, 4):
            for j, v in enumerate((p, pa, pv, t), 1):
                ws.cell(row=i, column=j, value=v)
            ws.cell(row=i, column=4).number_format = "0.0%"
            if corrige:
                ws.cell(row=i, column=5, value=f"=C{i}*(1+D{i})").number_format = "0.00"
                ws.cell(row=i, column=6, value=f"=C{i}-B{i}").number_format = "0.00"
                ws.cell(row=i, column=7, value=f"=F{i}/B{i}").number_format = "0.0%"
                ws.cell(row=i, column=8, value=f"=F{i}/C{i}").number_format = "0.0%"
                ws.cell(row=i, column=9, value=f"=E{i}/B{i}").number_format = "0.00"
        for col, w in zip("ABCDEFGHI", (24, 10, 10, 8, 10, 14, 14, 14, 12)):
            ws.column_dimensions[col].width = w
        w2 = wb.create_sheet("2-Indicateurs magasin")
        w2["A1"] = "Sport Évasion (fictif) · Saint-Pierre · octobre 2026 vs octobre 2025"
        w2["A1"].font = Font(name="Arial", size=13, bold=True)
        for j, c in enumerate(["Donnée", "Oct. 2026", "Oct. 2025", "Évolution %"], 1):
            x = w2.cell(row=3, column=j, value=c); x.fill, x.font = ent, blanc
        for i, (k, a, b) in enumerate(INDIC, 4):
            w2.cell(row=i, column=1, value=k); w2.cell(row=i, column=2, value=a); w2.cell(row=i, column=3, value=b)
            if corrige:
                w2.cell(row=i, column=4, value=f"=(B{i}-C{i})/C{i}").number_format = "0.0%"
        calc = [("Taux de transformation", "=B5/B4", "=C5/C4", "0.0%"), ("Panier moyen (€)", "=B6/B5", "=C6/C5", "0.00"),
                ("Articles par ticket (UPT)", "=B7/B5", "=C7/C5", "0.00"), ("Prix moyen article (€)", "=B6/B7", "=C6/C7", "0.00"),
                ("CA par heure travaillée (€)", "=B6/B8", "=C6/C8", "0.00")]
        for i, (k, f1, f2, fmt) in enumerate(calc, 10):
            w2.cell(row=i, column=1, value=k).font = Font(name="Arial", bold=True)
            if corrige:
                for col, f in ((2, f1), (3, f2)):
                    w2.cell(row=i, column=col, value=f).number_format = fmt
                w2.cell(row=i, column=4, value=f"=(B{i}-C{i})/C{i}").number_format = "0.0%"
        w2.column_dimensions["A"].width = 30
        for c in "BCD":
            w2.column_dimensions[c].width = 14
        w3 = wb.create_sheet("3-Rentabilité")
        lignes = [("CA HT octobre (€)", 148800), ("Taux de marque moyen", 0.40), ("Démarque constatée (€, prix de vente)", 2976),
                  ("Stock début de mois (€, prix d’achat)", 98000), ("Stock fin de mois (€, prix d’achat)", 102000), ("Jours dans le mois", 31)]
        for i, (k, v) in enumerate(lignes, 2):
            w3.cell(row=i, column=1, value=k); w3.cell(row=i, column=2, value=v)
        w3["B3"].number_format = "0%"
        res = [("Marge brute (€)", "=B2*B3", "0"), ("Taux de démarque", "=B4/B2", "0.0%"), ("Coût d’achat des ventes (€)", "=B2-B10", "0"),
               ("Stock moyen (€)", "=(B5+B6)/2", "0"), ("Rotation du stock sur le mois", "=B12/B13", "0.00"),
               ("Couverture de stock (jours)", "=B13/(B12/B7)", "0.0")]
        for i, (k, f, fmt) in enumerate(res, 10):
            w3.cell(row=i, column=1, value=k).font = Font(name="Arial", bold=True)
            if corrige:
                w3.cell(row=i, column=2, value=f).number_format = fmt
        w3.column_dimensions["A"].width = 40
        w3.column_dimensions["B"].width = 16
        if not corrige:
            for sh, cell in ((ws, "A11"), (w2, "A16"), (w3, "A17")):
                sh[cell] = "Consigne : complétez les cellules vides avec des FORMULES (voir la ressource du jour, fiche formules)."
                sh[cell].alignment = Alignment(wrap_text=True)
        wb.save(os.path.join(dossier, "J3_Calculs_commerciaux_" + ("CORRIGE" if corrige else "apprenant") + ".xlsx"))


J = {
    "num": 3,
    "date": "Lundi 23 novembre 2026",
    "date_court": "2026-11-23",
    "titre": "Les chiffres du commerce sans peur : prix, marges et indicateurs du manager",
    "fichiers": fichiers,
    "objectif_general": "Calculer et interpréter sans erreur les prix (HT, TTC), les marges et les indicateurs commerciaux et de rentabilité "
                        "utilisés au quotidien par le MEM, socle des activités-types 2 et 3.",
    "objectifs": [
        ("Se rappeler (Bloom 1)", "énoncer les formules du prix TTC, de la marge, des taux de marge et de marque, du coefficient"),
        ("Comprendre (Bloom 2)", "expliquer la différence entre taux de marge et taux de marque, et pourquoi on ne les confond pas"),
        ("Appliquer (Bloom 3)", "calculer panier moyen, taux de transformation, UPT, démarque, rotation et couverture de stock"),
        ("Analyser (Bloom 4)", "interpréter l’évolution d’un tableau d’indicateurs et en déduire la cause probable d’un écart"),
        ("Évaluer (Bloom 5)", "juger de la pertinence d’une décision de prix au regard de la marge (jeu du marché forain)"),
    ],
    "lien_reac": "AT3 : Analyser la performance commerciale (CA, panier moyen, tickets, taux de transformation, fréquentation) ; Analyser "
                 "la rentabilité (taux de marge brute, démarque, rotation, coût du personnel rapporté au CA). AT2 : Gérer l’approvisionnement "
                 "(stocks, couverture). RC/RE : dossier AT3 partie 1 et 2.",
    "prerequis": "J2 : savoir écrire une formule Excel simple. Calculatrice (celle du téléphone suffit).",
    "materiel": "Postes avec Excel ou LibreOffice ; fichier J3_Calculs_commerciaux_apprenant.xlsx ; calculatrices ; billets et pièces factices "
                "(ou jetons) pour le jeu du marché forain ; 4 enveloppes « fournisseur » préparées ; étiquettes prix vierges.",
    "progression": "Enactif : jeu du marché forain (acheter, fixer un prix, vendre, compter la marge) AVANT toute formule → Iconique : "
                   "schéma « l’escalier du prix » et pyramide des indicateurs → Symbolique : formules, fiche mémo → retour enactif : "
                   "tableau de bord Excel du magasin et diagnostic. Spirale : on réutilise les ventes du J2 et on prépare l’AT3.",
    "slides": [
        {"type": "couverture", "titre": "Les chiffres sans peur", "sous_titre": "Prix · Marges · Indicateurs", "date": "Lundi 23 novembre 2026",
         "notes": "Désamorcer l’angoisse des maths : « Aujourd’hui, pas de mathématiques compliquées : quatre opérations et des pourcentages. "
                  "Si vous savez rendre la monnaie, vous saurez faire. » Retour sur les engagements du 16/11."},
        {"type": "question", "titre": "Défi d’ouverture", "texte": "+ 10 % puis − 10 %…\non revient au prix de départ ?", "notes":
         "Vote à main levée. Réponse : NON. 100 € + 10 % = 110 € ; 110 € − 10 % = 99 €. Le pourcentage s’applique toujours à une base "
         "différente. Accroche idéale : les pourcentages sont la première source d’erreur des managers… et du jury qui piège."},
        {"type": "cartes", "titre": "Le programme du jour", "items": [
            ("1 · Le marché", "jeu"), ("2 · Les prix", "HT, TTC, marges"), ("3 · Les indicateurs", "ventes"), ("4 · Rentabilité", "stocks, démarque")],
         "notes": "On joue d’abord, on formalise ensuite. Fin de journée : diagnostic complet d’un magasin fictif."},
        {"type": "section", "num": "01", "titre": "Le marché forain", "sous_titre": "On vend avant de calculer", "notes":
         "Mise en place du jeu (voir diapo suivante). Matériel : jetons, enveloppes fournisseur, étiquettes."},
        {"type": "activite", "titre": "Jeu : le marché forain", "genre": "4 équipes · 4 stands", "duree": "40 min",
         "items": ["J’achète au fournisseur", "Je fixe mon prix", "Je vends, je compte"], "notes":
         "4 équipes = 4 stands du marché de Saint-Paul (fictif) : letchis, ananas Victoria, vanille, samoussas. Chaque équipe reçoit "
         "une enveloppe fournisseur : prix d’achat HT, quantité, frais. Elle fixe un prix de vente TTC (TVA 2,1 % pour l’alimentaire). "
         "Le formateur joue les clients avec des cartes « client » : certains comparent les prix, d’autres achètent en quantité. "
         "3 tours de 8 minutes. Après chaque tour, l’équipe calcule ce qu’elle a gagné. À la fin : quelle équipe a fait le plus de "
         "CHIFFRE D’AFFAIRES ? Laquelle a fait le plus de MARGE ? Ce ne sont pas les mêmes : c’est le message clé de la journée."},
        {"type": "comparer", "titre": "CA ou marge ?", "gauche": ("Chiffre d’affaires", ["Ce qui entre", "Prix × quantité", "Flatteur"]),
         "droite": ("Marge", ["Ce qui reste", "Prix − coût d’achat", "Ce qui fait vivre"]), "notes":
         "Debriefing du jeu : l’équipe qui a cassé les prix a vendu beaucoup mais gagné peu. Phrase à retenir : « Le chiffre d’affaires "
         "flatte, la marge fait vivre. » Le MEM suit les deux (AT3 : performance commerciale ET rentabilité)."},
        {"type": "section", "num": "02", "titre": "Les prix", "sous_titre": "HT, TTC, marge, coefficient", "notes": "Pause de 10 minutes vers 10 h."},
        {"type": "etapes", "titre": "L’escalier du prix", "items": [("PA HT", "prix d’achat"), ("PV HT", "+ marge"), ("PV TTC", "+ TVA")],
         "notes": "On monte l’escalier : prix d’achat hors taxes, on ajoute la marge, on obtient le prix de vente hors taxes ; on ajoute la "
                  "TVA, on obtient le prix de vente TTC payé par le client. La TVA n’appartient pas au magasin : il la reverse à l’État. "
                  "Donc la marge se calcule TOUJOURS en hors taxes."},
        {"type": "chiffre", "titre": "TVA à La Réunion", "valeur": "8,5 %", "legende": "taux normal · 2,1 % taux réduit",
         "source": "Source : Code général des impôts, art. 296", "notes":
         "Spécificité DOM : à La Réunion, le taux normal de TVA est de 8,5 % (contre 20 % en métropole) et le taux réduit de 2,1 % "
         "(alimentaire notamment). L’octroi de mer, une taxe sur les marchandises importées propre aux DOM, pèse aussi sur les prix : "
         "il est inclus dans le coût d’achat. Piège à l’examen : l’étude de cas peut se situer en métropole (20 %) : lire l’énoncé. "
         "Vérifier les taux en vigueur sur impots.gouv.fr avant la séance."},
        {"type": "cartes", "titre": "Les 2 formules de base", "items": [
            ("TTC", "HT × (1 + TVA)"), ("HT", "TTC ÷ (1 + TVA)")], "t_titre": 40, "t_texte": 34, "notes":
         "Exemple : des tongs à 10,00 € HT → 10 × 1,085 = 10,85 € TTC. Inversement, un ballon affiché 21,59 € TTC → 21,59 ÷ 1,085 = "
         "19,90 € HT. Piège : on ne retire PAS 8,5 % du TTC (21,59 − 8,5 % = 19,75 € : faux)."},
        {"type": "cartes", "titre": "Marge : 2 taux", "items": [
            ("Taux de marge", ["marge ÷ PA HT", "regarde l’achat"]), ("Taux de marque", ["marge ÷ PV HT", "regarde la vente"])],
         "t_titre": 34, "t_texte": 30, "notes":
         "Exemple des tongs : PA HT 6 €, PV HT 10 €, marge 4 €. Taux de marge = 4 ÷ 6 = 66,7 %. Taux de marque = 4 ÷ 10 = 40 %. "
         "Même marge, deux pourcentages différents : il faut TOUJOURS préciser lequel on utilise. En grande distribution, on parle "
         "surtout de taux de marque (« taux de marge brute » sur le CA). Moyen mnémotechnique : marQue → Que l’on vend (prix de vente)."},
        {"type": "chiffre", "titre": "Le coefficient", "valeur": "× 1,81", "legende": "PV TTC ÷ PA HT (tongs)", "notes":
         "Coefficient multiplicateur = PV TTC ÷ PA HT = 10,85 ÷ 6 = 1,81. Il permet de fixer un prix de vente très vite : PA HT × "
         "coefficient = PV TTC. Les enseignes fixent souvent un coefficient par famille de produits."},
        {"type": "activite", "titre": "Le juste prix péi", "genre": "Par équipes · ardoises", "duree": "25 min",
         "items": ["Je calcule le TTC", "Je trouve la marge", "Le plus juste gagne"], "notes":
         "Le formateur affiche un produit et son prix d’achat HT ; les équipes calculent sur ardoise. Séries : 1) Gourde : PV HT 14,40 € "
         "→ TTC ? (15,62 €). 2) Rhum arrangé : PA 11 €, PV HT 18,50 € → marge, taux de marque ? (7,50 € ; 40,5 %). 3) Mangues : PA "
         "2,10 € le kg, taux de marque visé 40 % → PV HT ? (PV HT = PA ÷ (1 − 0,40) = 3,50 €). 4) Baguette : PV TTC 0,92 € → HT ? (0,90 €). "
         "Puis travail individuel sur l’onglet « 1-Prix et marges » du fichier Excel."},
        {"type": "section", "num": "03", "titre": "Les indicateurs", "sous_titre": "Le tableau de bord du manager", "notes": ""},
        {"type": "etapes", "titre": "Du passant au client", "items": [("Entrées", "fréquentation"), ("Tickets", "achats"), ("CA", "€ encaissés")],
         "notes": "Le parcours qui explique tout le CA : des gens entrent (fréquentation), certains achètent (tickets), chacun dépense "
                  "un certain montant (panier moyen). CA = entrées × taux de transformation × panier moyen. Si le CA baisse, il faut "
                  "savoir LEQUEL de ces trois leviers a bougé : c’est l’analyse de performance attendue au dossier AT3."},
        {"type": "cartes", "titre": "Les 4 ratios clés", "items": [
            ("Transformation", "tickets ÷ entrées"), ("Panier moyen", "CA ÷ tickets"), ("UPT", "articles ÷ tickets"), ("Prix moyen", "CA ÷ articles")],
         "notes": "Taux de transformation : sur 100 personnes qui entrent, combien achètent ? Panier moyen : combien dépense un client. "
                  "UPT (unités par ticket, ou indice de vente) : combien d’articles par client. Prix moyen article. Leviers : transformation "
                  "= accueil, conseil, disponibilité des produits ; panier = vente additionnelle, montée en gamme ; UPT = produits "
                  "complémentaires (le ballon + la pompe)."},
        {"type": "exemple", "titre": "Sport Évasion · octobre", "lieu": "Saint-Pierre", "lieu_detail": ["Magasin de sport", "fictif"],
         "items": ["Entrées : − 5,3 %", "Transformation : 20 %", "Panier : 60 €", "CA : + 4,9 %"], "notes":
         "Corrigé : entrées 12 400 vs 13 100 (−5,3 %) ; tickets 2 480 vs 2 489 ; taux de transformation 20,0 % vs 19,0 % ; panier moyen "
         "60,00 € vs 56,97 € (+5,3 %) ; UPT 1,80 vs 1,70 ; CA 148 800 € vs 141 800 € (+4,9 %). Lecture : moins de monde entre, mais "
         "l’équipe transforme mieux et vend plus par client. Hypothèses : travaux sur le parking ou concurrence (externe) ; formation "
         "à la vente additionnelle (interne). Le bon réflexe : distinguer causes internes et externes, comme demandé au dossier AT3."},
        {"type": "activite", "titre": "Atelier : tableau de bord", "genre": "Individuel · Excel", "duree": "35 min",
         "items": ["Onglet 2 : 5 ratios", "Évolutions en %", "3 lignes d’analyse"], "notes":
         "Les apprenants complètent l’onglet « 2-Indicateurs magasin » puis écrivent 3 lignes d’analyse : ce qui progresse, ce qui "
         "recule, une hypothèse de cause. Correction projetée avec le fichier CORRIGE."},
        {"type": "section", "num": "04", "titre": "La rentabilité", "sous_titre": "Marge, démarque, stock", "notes": "Après la pause de 14 h 30."},
        {"type": "cartes", "titre": "Les 4 ratios de rentabilité", "items": [
            ("Marge brute", "CA × taux de marque"), ("Démarque", "pertes ÷ CA"), ("Rotation", "ventes ÷ stock moyen"), ("Productivité", "CA ÷ heures")],
         "notes": "Démarque : produits volés, cassés, périmés, erreurs de prix ou de réception. Connue (on la constate : casse, DLC) et "
                  "inconnue (révélée à l’inventaire : vol, erreurs). Rotation : combien de fois le stock « tourne » ; un stock qui dort "
                  "coûte (place, argent immobilisé, risque de démarque). Productivité : CA par heure travaillée, ou masse salariale ÷ CA."},
        {"type": "chiffre", "titre": "Démarque : l’effet loupe", "valeur": "2 %", "legende": "de démarque = 5 % de la marge perdue (marque 40 %)",
         "notes": "Calcul : CA 148 800 € ; démarque 2 976 € = 2 % du CA. Marge brute 59 520 € (40 %). La démarque représente 5 % de la "
                  "marge : chaque euro perdu se paie sur ce qui reste, pas sur le CA. Exemple frappant : pour compenser un vol de 30 € "
                  "à 40 % de marque, il faut vendre 75 € de plus."},
        {"type": "cartes", "titre": "Le stock en 2 chiffres", "items": [
            ("Stock moyen", "(début + fin) ÷ 2"), ("Couverture", "stock ÷ ventes / jour")], "t_titre": 36, "t_texte": 30, "notes":
         "Sport Évasion : stock moyen = (98 000 + 102 000) ÷ 2 = 100 000 € au prix d’achat. Coût d’achat des ventes du mois = 148 800 × "
         "0,60 = 89 280 €. Rotation sur le mois = 0,89. Couverture = 100 000 ÷ (89 280 ÷ 31) ≈ 35 jours : le magasin a 35 jours de "
         "ventes en stock. Est-ce trop ? Ça dépend du secteur : énorme pour des fruits, normal pour du textile de sport."},
        {"type": "activite", "titre": "Diagnostic du magasin", "genre": "En binôme", "duree": "35 min",
         "items": ["Onglet 3 : rentabilité", "1 force, 1 faiblesse", "2 actions chiffrées"], "notes":
         "Les binômes complètent l’onglet « 3-Rentabilité » puis préparent une mini-note à leur responsable (3 parties : constat, causes "
         "possibles, 2 propositions chiffrées). C’est le format exact du dossier AT3 en miniature. 2 binômes présentent en 2 minutes."},
        {"type": "puces", "titre": "Pièges classiques", "items": [
            "Marge calculée en TTC", "Marge et marque confondues", "Mauvaise base de %", "Points et % mélangés"], "notes":
         "Points de pourcentage : un taux de transformation qui passe de 19 % à 20 % progresse de 1 POINT (et de 5,3 %). À l’oral devant "
         "le jury, dire « +1 point » est un signe de maîtrise."},
        {"type": "activite", "titre": "Quiz : 10 questions", "genre": "Individuel · calculatrice", "duree": "15 min",
         "items": ["10 questions", "Calculatrice autorisée", "Objectif : 7 / 10"], "notes": "Lecture à voix haute possible."},
        {"type": "puces", "titre": "À retenir", "items": ["Marge en hors taxes", "Marque = sur la vente", "CA = entrées × transfo × panier", "Démarque : effet loupe"],
         "notes": "Annonce du 30/11 : la communication du manager (consignes, briefing, écoute). Travail : apprendre la fiche mémo des formules."},
        {"type": "question", "titre": "Mon engagement", "texte": "Cette semaine, je relève\n3 chiffres de mon magasin", "notes":
         "Avec l’accord du tuteur : CA, panier moyen, fréquentation d’une journée. Données de l’entreprise : ne pas les diffuser hors du groupe."},
    ],
    "ressource": [
        ("Pourquoi les chiffres sont au cœur du métier",
         "<p>Le MEM n’est pas comptable, mais il <b>pilote</b> son périmètre avec des chiffres : il les collecte, vérifie qu’ils sont "
         "fiables, les compare (à l’objectif, à l’an dernier), détecte les écarts, en cherche les causes et propose des actions "
         "(REAC, AT3). Le jury de l’AT3 vous questionnera sur ces indicateurs pendant 40 minutes.</p>"
         + encadre("retenir", "<p><b>Le chiffre d’affaires flatte, la marge fait vivre.</b> Un manager suit toujours les deux.</p>")
         + encadre("def", "<p><b>Pourcentage</b> : une part de 100. 25 % de 80 € = 80 × 25 ÷ 100 = 20 €. <b>Évolution en %</b> = (nouvelle "
                   "valeur − ancienne) ÷ ancienne. <b>Point de pourcentage</b> : différence entre deux taux (19 % → 20 % = +1 point).</p>")
         + encadre("piege", "<p>+10 % puis −10 % ne ramène pas au départ : 100 → 110 → 99. Une remise de 20 % puis de 10 % ne fait pas "
                   "30 % mais 28 % (100 → 80 → 72).</p>")),
        ("Les prix : HT, TTC et TVA à La Réunion",
         flux([("PA HT", "prix d’achat hors taxes (coût du produit, octroi de mer et frais inclus)"), ("+ marge", "ce que gagne le magasin"),
               ("PV HT", "prix de vente hors taxes"), ("+ TVA", "reversée à l’État"), ("PV TTC", "prix payé par le client")], "L’escalier du prix")
         + tableau(["Taux de TVA à La Réunion", "Valeur", "Exemples"], [["Taux normal", "8,5 %", "Articles de sport, textile, boissons alcoolisées"],
                                                                    ["Taux réduit", "2,1 %", "Produits alimentaires (sauf exceptions)"]])
         + "<p class='petit'>En métropole : 20 % (normal), 5,5 % et 10 % (réduits). Lisez toujours le taux donné dans l’énoncé.</p>"
         + tableau(["Je cherche", "Formule", "Exemple"], [["PV TTC", "PV HT × (1 + taux)", "10,00 × 1,085 = 10,85 €"],
                                                       ["PV HT", "PV TTC ÷ (1 + taux)", "21,59 ÷ 1,085 = 19,90 €"],
                                                       ["Montant de TVA", "PV TTC − PV HT", "10,85 − 10,00 = 0,85 €"]])
         + encadre("piege", "<p>Pour passer du TTC au HT, on <b>divise</b> par 1,085 ; on ne retire pas 8,5 %.</p>")),
        ("Marge, taux de marge, taux de marque, coefficient",
         tableau(["Notion", "Formule", "Exemple : tongs (PA HT 6 €, PV HT 10 €)"], [
             ["Marge brute unitaire", "PV HT − PA HT", "10 − 6 = <b>4 €</b>"],
             ["Taux de marge", "Marge ÷ PA HT × 100", "4 ÷ 6 = <b>66,7 %</b>"],
             ["Taux de marque", "Marge ÷ PV HT × 100", "4 ÷ 10 = <b>40 %</b>"],
             ["Coefficient multiplicateur", "PV TTC ÷ PA HT", "10,85 ÷ 6 = <b>1,81</b>"],
             ["PV HT à partir d’un taux de marque visé", "PA HT ÷ (1 − taux de marque)", "6 ÷ (1 − 0,40) = <b>10 €</b>"]])
         + cartes([("Taux de marge", "On regarde l’ACHAT : « sur ce que j’ai payé, je gagne 66,7 % »."),
                   ("Taux de marque", "On regarde la VENTE : « sur ce que je vends, 40 % me reste ». MarQue = Que l’on vend.")], cols=2)
         + encadre("ex", "<p>Rhum arrangé artisanal : PA HT 11 €, PV HT 18,50 €. Marge 7,50 € ; taux de marge 68,2 % ; taux de marque "
                   "40,5 % ; PV TTC 20,07 € ; coefficient 1,82.</p>")),
        ("Les indicateurs de performance commerciale",
         pyramide([("CA", "le résultat"), ("Panier moyen × tickets", "comment il se forme"), ("Entrées × taux de transformation", "d’où viennent les tickets")],
                  "CA = entrées × taux de transformation × panier moyen")
         + tableau(["Indicateur", "Formule", "Ce qu’il dit", "Leviers du manager"], [
             ["Fréquentation", "Nombre d’entrées (compteur)", "L’attractivité du magasin", "Vitrine, animations, communication locale"],
             ["Taux de transformation", "Tickets ÷ entrées × 100", "La capacité à faire acheter", "Accueil, conseil, produits disponibles, attente en caisse"],
             ["Panier moyen", "CA ÷ tickets", "Ce que dépense un client", "Vente additionnelle, montée en gamme"],
             ["UPT (indice de vente)", "Articles ÷ tickets", "Le nombre d’articles par client", "Produits complémentaires, implantation"],
             ["Prix moyen article", "CA ÷ articles", "Le niveau de gamme vendu", "Mise en avant, conseil"],
             ["Évolution N/N-1", "(N − N-1) ÷ N-1", "La tendance", "Comparer la même période (saisonnalité)"]])
         + "<h3>Cas Sport Évasion (fictif), Saint-Pierre, octobre</h3>"
         + tableau(["Indicateur", "Oct. 2026", "Oct. 2025", "Évolution"], [
             ["Entrées", "12 400", "13 100", "−5,3 %"], ["Tickets", "2 480", "2 489", "−0,4 %"], ["CA HT", "148 800 €", "141 800 €", "+4,9 %"],
             ["Taux de transformation", "20,0 %", "19,0 %", "+1 point"], ["Panier moyen", "60,00 €", "56,97 €", "+5,3 %"],
             ["UPT", "1,80", "1,70", "+5,9 %"], ["CA par heure travaillée", "120,00 €", "117,19 €", "+2,4 %"]])
         + encadre("ex", "<p><b>Lecture de manager :</b> moins de clients entrent (−5,3 %), mais l’équipe transforme mieux (+1 point) et "
                   "vend plus par client. Causes possibles : externes (travaux, concurrence, météo) pour la fréquentation ; internes "
                   "(formation à la vente additionnelle) pour le panier. Action : agir sur la fréquentation (animation, vitrine) "
                   "sans perdre la qualité de vente.</p>")),
        ("Les indicateurs de rentabilité",
         tableau(["Indicateur", "Formule", "Exemple Sport Évasion"], [
             ["Marge brute", "CA HT × taux de marque (ou CA HT − coût d’achat des ventes)", "148 800 × 40 % = 59 520 €"],
             ["Taux de démarque", "Démarque ÷ CA × 100", "2 976 ÷ 148 800 = 2,0 %"],
             ["Stock moyen", "(Stock début + stock fin) ÷ 2", "(98 000 + 102 000) ÷ 2 = 100 000 €"],
             ["Coût d’achat des ventes", "CA HT − marge brute", "148 800 − 59 520 = 89 280 €"],
             ["Rotation du stock", "Coût d’achat des ventes ÷ stock moyen", "89 280 ÷ 100 000 = 0,89 sur le mois"],
             ["Couverture de stock (jours)", "Stock moyen ÷ (coût d’achat des ventes ÷ jours)", "100 000 ÷ 2 880 ≈ 35 jours"],
             ["Productivité", "CA ÷ heures travaillées", "148 800 ÷ 1 240 = 120 € / heure"]])
         + encadre("retenir", "<p><b>L’effet loupe de la démarque :</b> avec 40 % de taux de marque, une perte de 30 € de marchandise "
                   "oblige à vendre 75 € de plus pour retrouver la même marge (30 ÷ 0,40).</p>")
         + cartes([("Démarque connue", "Casse, produits périmés, erreurs constatées : on la mesure au fil de l’eau."),
                   ("Démarque inconnue", "Vol, erreurs de réception ou de prix : révélée par l’inventaire.")], cols=2)),
        ("Méthode d’analyse d’un écart (préparation AT3)",
         flux([("Constater", "chiffre, période, référence"), ("Mesurer", "écart en € et en %"), ("Expliquer", "causes internes / externes"),
               ("Vérifier", "croiser les sources, le terrain"), ("Proposer", "actions chiffrées à la hiérarchie")])
         + tableau(["Causes internes (je peux agir)", "Causes externes (je dois m’adapter)"], [
             ["Ruptures, implantation, effectif insuffisant, accueil", "Météo, cyclone, vacances scolaires, concurrence"],
             ["Erreurs de prix, démarque, formation de l’équipe", "Travaux, grève, hausse des coûts (fret, énergie)"]])
         + encadre("jury", "<p>Phrase type attendue : « Le CA du rayon recule de 4 % par rapport à N-1 ; la fréquentation est stable mais le "
                   "taux de transformation perd 2 points, en lien avec 6 jours de rupture sur les produits phares. Je propose… »</p>")),
        ("Fiche mémo des formules",
         tableau(["Je cherche…", "Formule"], [
             ["PV TTC", "PV HT × (1 + taux de TVA)"], ["PV HT", "PV TTC ÷ (1 + taux de TVA)"], ["Marge unitaire", "PV HT − PA HT"],
             ["Taux de marge", "Marge ÷ PA HT"], ["Taux de marque", "Marge ÷ PV HT"], ["Coefficient", "PV TTC ÷ PA HT"],
             ["PV HT avec taux de marque visé", "PA HT ÷ (1 − taux de marque)"], ["Évolution", "(N − N-1) ÷ N-1"],
             ["Écart à l’objectif", "(Réalisé − objectif) ÷ objectif"], ["Taux de transformation", "Tickets ÷ entrées"],
             ["Panier moyen", "CA ÷ tickets"], ["UPT", "Articles ÷ tickets"], ["Taux de démarque", "Démarque ÷ CA"],
             ["Stock moyen", "(SI + SF) ÷ 2"], ["Rotation", "Coût d’achat des ventes ÷ stock moyen"],
             ["Couverture (jours)", "Stock ÷ ventes moyennes par jour"], ["Productivité", "CA ÷ heures travaillées"]])),
        ("Le jeu du marché forain (règles pour réviser chez soi)",
         "<p>4 stands (letchis, ananas Victoria, vanille, samoussas). Chaque équipe connaît son prix d’achat HT et fixe un prix de vente "
         "TTC (TVA 2,1 %). Après chaque tour : CA HT = ventes TTC ÷ 1,021 ; marge = CA HT − coût d’achat des produits vendus. L’équipe "
         "gagnante est celle qui a la plus forte <b>marge</b>, pas le plus fort CA.</p>"
         + encadre("loi", "<p><b>Droit</b> : les prix doivent être affichés TTC et lisibles pour le consommateur (Code de la consommation, "
                   "art. L112-1). <b>RGPD</b> : les chiffres d’un fichier client (achats nominatifs) sont des données personnelles ; pour "
                   "analyser des ventes, on utilise des données agrégées.</p>")),
    ],
    "sources": [
        "REAC et RC/RE MEM v09 du 10/12/2025 : compétences de l’AT3 et contenu attendu du dossier (pièces jointes).",
        "Code général des impôts, article 296 (taux de TVA dans les départements d’outre-mer) — legifrance.gouv.fr ; à vérifier sur impots.gouv.fr avant chaque session.",
        "Code de la consommation, article L112-1 (information sur les prix) — legifrance.gouv.fr.",
        "Données Sport Évasion et Ti Marché du Sud : entreprises et chiffres fictifs créés pour les exercices.",
    ],
    "grille": {
        "situation": "Jeu du marché forain, atelier Excel (prix, indicateurs, rentabilité) et mini-note de diagnostic en binôme.",
        "criteres": [
            {"critere": "Calcul des prix HT / TTC", "indicateurs": ["Applique le bon taux (8,5 % / 2,1 %)", "Divise par (1 + taux) pour retrouver le HT"],
             "niveaux": ["Erreurs systématiques", "Juste dans un sens seulement", "Justes dans les deux sens", "Justes, rapides, explique la logique"]},
            {"critere": "Marge, taux de marge, taux de marque", "indicateurs": ["Calcule en hors taxes", "Distingue les deux taux"],
             "niveaux": ["Confond les notions", "Marge juste, taux confondus", "Tous justes", "Justes + calcule un PV à partir d’un taux visé"]},
            {"critere": "Indicateurs commerciaux", "indicateurs": ["Transformation, panier, UPT exacts", "Évolutions en % et en points"],
             "niveaux": ["Formules fausses", "2 indicateurs justes", "Tous justes", "Justes + décompose le CA en ses 3 leviers"]},
            {"critere": "Indicateurs de rentabilité", "indicateurs": ["Démarque, stock moyen, rotation, couverture", "Explique l’effet loupe"],
             "niveaux": ["Non traités", "Partiels", "Justes", "Justes + interprétation selon le secteur"]},
            {"critere": "Analyse et proposition", "indicateurs": ["Distingue causes internes et externes", "Propose 2 actions chiffrées"],
             "niveaux": ["Aucune analyse", "Constat sans causes", "Causes + actions", "Analyse structurée, actions chiffrées et réalistes"]},
        ]},
    "quiz": [
        {"q": "Un article coûte 20,00 € HT. À La Réunion (taux normal), son prix TTC est :", "choix": ["21,70 €", "24,00 €", "20,85 €", "21,85 €"], "rep": 0,
         "explication": "20 × 1,085 = 21,70 €."},
        {"q": "Un article est affiché 32,55 € TTC (TVA 8,5 %). Son prix HT est :", "choix": ["29,78 €", "30,00 €", "29,79 €", "31,00 €"], "rep": 1,
         "explication": "32,55 ÷ 1,085 = 30,00 €. On divise, on ne retire pas 8,5 %."},
        {"q": "PA HT 6 €, PV HT 10 €. Le taux de marque est :", "choix": ["66,7 %", "40 %", "4 %", "60 %"], "rep": 1, "explication": "Marge 4 € ÷ PV HT 10 € = 40 %."},
        {"q": "Avec les mêmes chiffres, le taux de marge est :", "choix": ["40 %", "60 %", "66,7 %", "150 %"], "rep": 2, "explication": "Marge 4 € ÷ PA HT 6 € = 66,7 %."},
        {"q": "La marge se calcule toujours :", "choix": ["en TTC", "en hors taxes", "TVA comprise", "selon le magasin"], "rep": 1,
         "explication": "La TVA est reversée à l’État : elle n’entre pas dans la marge."},
        {"q": "1 000 entrées, 220 tickets : le taux de transformation est :", "choix": ["2,2 %", "22 %", "45 %", "78 %"], "rep": 1, "explication": "220 ÷ 1 000 = 22 %."},
        {"q": "CA de 13 200 € pour 220 tickets : le panier moyen est :", "choix": ["60 €", "16,7 €", "600 €", "6 €"], "rep": 0, "explication": "13 200 ÷ 220 = 60 €."},
        {"q": "Un taux de transformation passe de 19 % à 20 %. On dit qu’il progresse de :", "choix": ["1 %", "1 point", "20 %", "0,1 point"], "rep": 1,
         "explication": "+1 point de pourcentage (soit +5,3 % en évolution relative)."},
        {"q": "Stock début 98 000 €, stock fin 102 000 €. Le stock moyen est :", "choix": ["200 000 €", "4 000 €", "100 000 €", "102 000 €"], "rep": 2,
         "explication": "(98 000 + 102 000) ÷ 2 = 100 000 €."},
        {"q": "Avec un taux de marque de 40 %, pour compenser un vol de 30 €, il faut vendre en plus :", "choix": ["30 €", "42 €", "75 €", "12 €"], "rep": 2,
         "explication": "30 ÷ 0,40 = 75 € : c’est l’effet loupe de la démarque."},
    ],
    "deroule": [
        ("8 h 00 – 8 h 20", "Accueil et défi d’ouverture", "Lever l’appréhension (Bloom 2)", "Engagements du 16/11 ; défi « +10 % puis −10 % » ; programme",
         "Interrogative · enactif", "Diapos 1-3", "Vote, oral"),
        ("8 h 20 – 9 h 10", "S1 · Jeu du marché forain", "Découvrir CA et marge en les vivant (Bloom 3)",
         "4 stands, enveloppes fournisseur, 3 tours de vente, calcul des gains à chaque tour", "Ludique · enactif", "Diapo 4-5, jetons, enveloppes", "Observation"),
        ("9 h 10 – 9 h 30", "S1 · Débriefing CA / marge", "Expliquer la différence (Bloom 2)", "Classement CA vs marge ; « le CA flatte, la marge fait vivre »",
         "Interrogative · iconique", "Diapo 6", "Reformulation"),
        ("9 h 30 – 10 h 00", "S2 · L’escalier du prix, TVA péi", "Calculer HT / TTC (Bloom 3)", "Escalier du prix ; TVA 8,5 % / 2,1 % ; 2 formules ; pièges",
         "Expositive · iconique → symbolique", "Diapos 7-10", "Calculs guidés"),
        ("10 h 00 – 10 h 10", "Pause", "", "", "", "", ""),
        ("10 h 10 – 10 h 40", "S2 · Marge, marque, coefficient", "Distinguer les taux (Bloom 2-3)", "Exemple des tongs ; moyen mnémotechnique ; coefficient",
         "Démonstrative · symbolique", "Diapos 11-12", "Questions"),
        ("10 h 40 – 12 h 00", "S2 · Le juste prix péi + Excel onglet 1", "Appliquer (Bloom 3)", "4 séries par équipes sur ardoise ; puis onglet « 1-Prix et marges »",
         "Ludique puis active · enactif", "Diapo 13, ardoises, classeur", "Grille critères 1-2"),
        ("12 h 00 – 13 h 00", "Pause déjeuner", "", "", "", "", ""),
        ("13 h 00 – 13 h 40", "S3 · Les indicateurs commerciaux", "Calculer et décomposer le CA (Bloom 3)",
         "Du passant au client ; 4 ratios ; cas Sport Évasion lu ensemble", "Expositive participative · iconique", "Diapos 14-17", "Questions"),
        ("13 h 40 – 14 h 30", "S3 · Atelier tableau de bord", "Analyser une évolution (Bloom 4)", "Onglet 2 : ratios, évolutions, 3 lignes d’analyse ; correction",
         "Active · symbolique", "Diapo 18, classeur, corrigé", "Grille critère 3"),
        ("14 h 30 – 14 h 40", "Pause", "", "", "", "", ""),
        ("14 h 40 – 15 h 00", "S4 · Rentabilité", "Expliquer marge, démarque, rotation (Bloom 2)", "4 ratios ; effet loupe ; stock moyen et couverture",
         "Expositive · iconique", "Diapos 19-22", "Questions"),
        ("15 h 00 – 15 h 35", "S4 · Diagnostic en binôme", "Évaluer et proposer (Bloom 4-5)", "Onglet 3 + mini-note (constat, causes, 2 actions chiffrées) ; 2 présentations",
         "Active · enactif + symbolique", "Diapos 23-24, classeur", "Grille critères 4-5"),
        ("15 h 35 – 15 h 55", "Quiz 10 questions", "Évaluer (Bloom 1-3)", "Quiz avec calculatrice puis correction", "Évaluative", "Quiz", "Sommative 7/10"),
        ("15 h 55 – 16 h 00", "Bilan et engagement", "S’engager (Bloom 3)", "À retenir ; relever 3 chiffres de son magasin", "Réflexive", "Diapos 26-28", "Engagement"),
    ],
}
