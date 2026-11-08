import os

from aides import cartes, encadre, flux, tableau

VENTES = [  # entreprise fictive « Ti Marché du Sud », Saint-Louis — rayon fruits et légumes, semaine 46
    ("Lundi", 4820, 4650, 5000, 412), ("Mardi", 4310, 4480, 4800, 371), ("Mercredi", 5140, 4900, 5200, 438),
    ("Jeudi", 4690, 4720, 5000, 401), ("Vendredi", 6380, 6010, 6500, 522), ("Samedi", 8950, 8400, 9000, 690),
    ("Dimanche", 3870, 3950, 4000, 315)]
COMMANDE = [  # produit, stock, ventes moyennes / jour, délai (j), période couverte (j), stock de sécurité
    ("Letchis (kg)", 40, 35, 2, 3, 20), ("Bananes (kg)", 120, 48, 1, 3, 25), ("Ananas Victoria (pièce)", 30, 22, 2, 3, 12),
    ("Tomates (kg)", 55, 30, 1, 3, 15), ("Brèdes mafane (botte)", 10, 18, 1, 2, 8), ("Mangues José (kg)", 0, 25, 2, 3, 12)]

TEXTE_BRUT = """Note à l'attention de Monsieur le Directeur du magasin
Objet : bilan de l'opération « Letchis de la Réunion » - semaine 46
Synthèse
L'opération de mise en avant des letchis a été menée du lundi au dimanche de la semaine 46. Le chiffre d'affaires du rayon fruits et légumes progresse par rapport à l'an dernier, mais reste en dessous de l'objectif fixé. Deux actions correctives sont proposées.
Contexte
Chaque année, la saison des letchis commence fin novembre. Nous avons décidé d'installer une tête de gondole à l'entrée du magasin et de proposer une dégustation le samedi matin.
Résultats
Le chiffre d'affaires de la semaine s'élève à 38 160 euros pour un objectif de 39 500 euros. Il progresse de 2,8 % par rapport à la semaine 46 de l'an dernier. Le samedi représente près d'un quart des ventes de la semaine. Le mardi et le dimanche sont les jours les plus faibles.
Points d'attention
Deux cagettes de letchis ont été livrées abîmées le lundi. Une réserve a été portée sur le bon de livraison. La démarque sur le rayon est en légère hausse.
Propositions
Première proposition : renforcer la présence d'un vendeur au rayon le samedi de 9 heures à 12 heures. Deuxième proposition : tester une offre « panier fraîcheur » le mardi pour dynamiser le jour le plus faible.
Je reste à votre disposition pour en discuter.
Le responsable du rayon fruits et légumes"""


def fichiers(dossier):
    from docx import Document
    from openpyxl import Workbook
    from openpyxl.chart import BarChart, Reference
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.worksheet.datavalidation import DataValidation  # noqa: F401

    entete = PatternFill("solid", fgColor="0B3D4A")
    blanc = Font(name="Arial", size=12, bold=True, color="FFFFFF")
    normal = Font(name="Arial", size=12)
    for corrige in (False, True):
        wb = Workbook()
        ws = wb.active
        ws.title = "1-Ventes S46"
        ws["A1"] = "Ti Marché du Sud (fictif) · Saint-Louis · Rayon fruits et légumes · Semaine 46"
        ws["A1"].font = Font(name="Arial", size=14, bold=True)
        cols = ["Jour", "CA réalisé (€)", "CA N-1 (€)", "Objectif (€)", "Nb tickets", "Écart / objectif (€)",
                "Écart / objectif (%)", "Évolution N/N-1 (%)", "Panier moyen (€)"]
        for j, c in enumerate(cols, 1):
            cell = ws.cell(row=3, column=j, value=c)
            cell.fill, cell.font = entete, blanc
            cell.alignment = Alignment(wrap_text=True, vertical="center")
        for i, (jour, ca, n1, obj, tk) in enumerate(VENTES, 4):
            for j, v in enumerate((jour, ca, n1, obj, tk), 1):
                ws.cell(row=i, column=j, value=v).font = normal
            if corrige:
                ws.cell(row=i, column=6, value=f"=B{i}-D{i}")
                ws.cell(row=i, column=7, value=f"=(B{i}-D{i})/D{i}").number_format = "0.0%"
                ws.cell(row=i, column=8, value=f"=(B{i}-C{i})/C{i}").number_format = "0.0%"
                ws.cell(row=i, column=9, value=f"=B{i}/E{i}").number_format = "0.00"
        ws.cell(row=11, column=1, value="TOTAL").font = Font(name="Arial", size=12, bold=True)
        if corrige:
            for col in "BCDEF":
                ws[f"{col}11"] = f"=SUM({col}4:{col}10)"
            ws["G11"], ws["H11"], ws["I11"] = "=(B11-D11)/D11", "=(B11-C11)/C11", "=B11/E11"
            ws["G11"].number_format = ws["H11"].number_format = "0.0%"
            ws["I11"].number_format = "0.00"
            ws["A13"] = "Part du samedi dans le CA (%)"
            ws["B13"] = "=B9/B11"
            ws["B13"].number_format = "0.0%"
            ch = BarChart()
            ch.title, ch.y_axis.title = "CA réalisé et objectif par jour", "€"
            ch.add_data(Reference(ws, min_col=2, min_row=3, max_row=10), titles_from_data=True)
            ch.add_data(Reference(ws, min_col=4, min_row=3, max_row=10), titles_from_data=True)
            ch.set_categories(Reference(ws, min_col=1, min_row=4, max_row=10))
            ch.width, ch.height = 22, 11
            ws.add_chart(ch, "A15")
        else:
            ws["A13"] = ("Consignes : 1) Calculez les colonnes F à I avec des formules. 2) Calculez la ligne TOTAL (SOMME). "
                         "3) Formatez les % avec 1 décimale. 4) Mise en forme conditionnelle : écarts négatifs en rouge. "
                         "5) Insérez un histogramme CA réalisé / objectif. 6) Calculez la part du samedi dans le CA. "
                         "7) Mise en page : tout sur 1 page A4 paysage, puis aperçu avant impression.")
            ws["A13"].alignment = Alignment(wrap_text=True)
            ws.merge_cells("A13:I17")
        for col, w in zip("ABCDEFGHI", (14, 14, 12, 12, 11, 15, 15, 15, 14)):
            ws.column_dimensions[col].width = w
        ws.row_dimensions[3].height = 48

        w2 = wb.create_sheet("2-Maquette commande")
        w2["A1"] = "MAQUETTE PRÉÉTABLIE (type examen) · Bon de commande fruits et légumes · NE PAS MODIFIER LES CELLULES GRISÉES"
        w2["A1"].font = Font(name="Arial", size=13, bold=True)
        w2["A2"] = "Quantité à commander = ventes moyennes/jour × (délai + période couverte) + stock de sécurité − stock actuel (si résultat < 0 : 0)"
        cols2 = ["Produit", "Stock actuel", "Ventes moy./jour", "Délai livraison (j)", "Période couverte (j)", "Stock sécurité",
                 "Besoin brut", "Quantité à commander"]
        for j, c in enumerate(cols2, 1):
            cell = w2.cell(row=4, column=j, value=c)
            cell.fill, cell.font = entete, blanc
            cell.alignment = Alignment(wrap_text=True)
        gris = PatternFill("solid", fgColor="D9D9D9")
        for i, row in enumerate(COMMANDE, 5):
            for j, v in enumerate(row, 1):
                c = w2.cell(row=i, column=j, value=v)
                c.fill, c.font = gris, normal
            if corrige:
                w2.cell(row=i, column=7, value=f"=C{i}*(D{i}+E{i})+F{i}")
                w2.cell(row=i, column=8, value=f"=MAX(0,G{i}-B{i})")
        w2["A12"] = "Question d’analyse : quel produit présente un risque de rupture immédiat ? Que faites-vous ?"
        if corrige:
            w2["A13"] = ("Mangues José : stock à 0 → rupture déjà en cours ; commander 137 kg, prévenir le responsable, "
                         "vérifier une livraison anticipée, informer l’équipe et adapter l’implantation.")
        for col, w in zip("ABCDEFGH", (26, 12, 14, 14, 14, 12, 12, 16)):
            w2.column_dimensions[col].width = w
        nom = "J2_Exercices_Excel_CORRIGE.xlsx" if corrige else "J2_Exercices_Excel_apprenant.xlsx"
        wb.save(os.path.join(dossier, nom))

    doc = Document()
    for l in TEXTE_BRUT.split("\n"):
        doc.add_paragraph(l)
    doc.add_paragraph("")
    doc.add_paragraph("CONSIGNES (à supprimer à la fin) : 1) Police Arial 11, interligne 1,15. 2) Appliquez le style Titre 1 à "
                      "« Synthèse », « Contexte », « Résultats », « Points d’attention », « Propositions ». 3) Insérez une page de garde, "
                      "puis un sommaire automatique. 4) Insérez un tableau des ventes par jour (données de l’onglet Excel) avec une "
                      "légende. 5) Numérotez les pages (sauf la page de garde). 6) Vérifiez l’orthographe. 7) Exportez en PDF.")
    doc.save(os.path.join(dossier, "J2_Exercice_Word_texte_brut.docx"))


J = {
    "num": 2,
    "date": "Lundi 16 novembre 2026",
    "date_court": "2026-11-16",
    "titre": "Word, Excel, PowerPoint : les outils du manager… et de l’examen",
    "fichiers": fichiers,
    "objectif_general": "Maîtriser les fonctions de Word, Excel et PowerPoint indispensables au manager et aux épreuves du titre MEM "
                        "(étude de cas sur maquettes, dossiers en Arial 11, diaporamas), sur des données réalistes d’un magasin.",
    "objectifs": [
        ("Se rappeler (Bloom 1)", "citer les règles de forme imposées par le RC/RE (police, interligne, nombre de pages et de diapositives)"),
        ("Appliquer (Bloom 3)", "structurer un document Word avec styles, sommaire automatique, tableau, pagination et export PDF"),
        ("Appliquer (Bloom 3)", "calculer dans Excel des écarts, des évolutions en %, un panier moyen, et compléter une maquette sans la casser"),
        ("Analyser (Bloom 4)", "lire un tableau de ventes et repérer le jour fort, le jour faible et l’écart à l’objectif"),
        ("Créer (Bloom 6)", "concevoir 5 diapositives lisibles présentant son établissement (page d’introduction des dossiers)"),
    ],
    "lien_reac": "RC/RE : mise en situation professionnelle sur poste informatique (traitement de texte et tableur, maquettes préétablies, "
                 "impression) ; productions AT3 et AT1 (documents Arial 11 interligne 1,15 et diaporamas). Compétence transversale "
                 "« Communiquer » : rédiger des analyses claires et factuelles pour la hiérarchie.",
    "prerequis": "Savoir allumer un poste, ouvrir un fichier, utiliser souris et clavier. Avoir apporté son CV (J1).",
    "materiel": "Un poste par apprenant avec Microsoft 365 ou LibreOffice ; fichiers J2_Exercices_Excel_apprenant.xlsx et "
                "J2_Exercice_Word_texte_brut.docx copiés sur chaque poste ; imprimante (test d’impression) ; vidéoprojecteur ; "
                "loupe d’écran Windows (touche Windows + « + ») activable pour les personnes malvoyantes.",
    "progression": "Enactif : défi « 60 secondes chrono » et manipulation immédiate des fichiers → Iconique : captures et schémas des menus, "
                   "graphique des ventes → Symbolique : formules, règles de forme du RC/RE → retour enactif : mini-cas chronométré type "
                   "examen sur maquette. Lien spirale : les données de vente préparent le lundi 23/11 (chiffres du commerce).",
    "slides": [
        {"type": "couverture", "titre": "Word, Excel, PowerPoint", "sous_titre": "Les outils du manager… et de l’examen",
         "date": "Lundi 16 novembre 2026", "notes":
         "Ouverture : reprendre les post-it « engagement » du 9/11. Qui a avancé ? Valoriser chaque petite action. "
         "Annoncer : aujourd’hui on travaille sur poste, avec les données d’un magasin fictif de Saint-Louis."},
        {"type": "chiffre", "titre": "Le jour J", "valeur": "4 h", "legende": "d’étude de cas sur ordinateur",
         "source": "Source : RC/RE MEM v09", "notes":
         "Rappel : l’étude de cas se fait avec traitement de texte et tableur, à partir de maquettes préétablies, et on imprime ses "
         "travaux. Celui qui perd 20 minutes à chercher comment faire un pourcentage dans Excel perd des points. Aujourd’hui, on "
         "automatise les gestes pour que le jour J, la tête soit libre pour réfléchir."},
        {"type": "activite", "titre": "Défi : 60 secondes chrono", "genre": "Individuel", "duree": "10 min",
         "items": ["Ouvrir, enregistrer sous", "Copier un tableau", "Calculer une somme"], "notes":
         "Positionnement ludique : 3 mini-défis de 60 secondes. 1) Ouvrir le fichier Excel et l’enregistrer sous « NOM_J2.xlsx » dans "
         "le dossier Documents. 2) Copier le tableau des ventes dans Word. 3) Calculer la somme du CA de la semaine. Chaque apprenant "
         "note ses réussites : 3/3 = autonome, 1-2/3 = à consolider, 0/3 = accompagnement renforcé (binôme avec un autonome). "
         "Accessibilité : proposer la loupe Windows et le zoom (Ctrl + molette)."},
        {"type": "cartes", "titre": "Le programme du jour", "items": [
            ("1 · Word", "dossiers"), ("2 · Excel", "chiffres"), ("3 · PowerPoint", "soutenance"), ("4 · Jour J", "mini-cas")], "notes":
         "Matin : Word puis Excel. Après-midi : PowerPoint puis mini-cas chronométré type examen. Quiz à 15 h 40."},
        {"type": "cartes", "titre": "Les règles du RC/RE", "items": [
            ("Arial 11", "interligne 1,15"), ("AT3", ["12-18 pages", "12-18 diapos"]), ("AT1", ["16-24 pages", "18-24 diapos"])],
         "notes": "Pages comptées hors page de garde, sommaire et annexes. Une page de présentation de l’établissement en ouverture de "
                  "chaque document. Le diaporama AT3 est présenté en 20 minutes, le diaporama AT1 en 25 minutes. Ces règles ne se "
                  "négocient pas : un dossier hors format donne une mauvaise première impression au jury."},
        {"type": "section", "num": "01", "titre": "Word", "sous_titre": "Un dossier pro en 6 gestes", "notes":
         "Ouvrir J2_Exercice_Word_texte_brut.docx : une note « brute », sans aucune mise en forme. Objectif : la transformer en "
         "document professionnel adressé à la hiérarchie."},
        {"type": "etapes", "titre": "Les 6 gestes Word", "items": [
            ("Styles", "Titre 1, Titre 2"), ("Sommaire", "automatique"), ("Pages", "numéros, sauts")], "notes":
         "Geste 1 : appliquer les styles Titre 1 / Titre 2 (onglet Accueil > Styles) au lieu de mettre en gras à la main. "
         "Geste 2 : Références > Table des matières > automatique ; on la met à jour en fin de travail. Geste 3 : Insertion > "
         "Numéro de page ; Ctrl + Entrée pour un saut de page propre. Suite des gestes sur la diapo suivante."},
        {"type": "etapes", "titre": "… et 3 de plus", "items": [
            ("Tableaux", "+ légende"), ("Orthographe", "F7"), ("PDF", "Enregistrer sous")], "notes":
         "Geste 4 : Insertion > Tableau, puis clic droit > Insérer une légende (« Tableau 1 : ventes par jour »). Geste 5 : Révision > "
         "Grammaire et orthographe (F7) ; attention, le correcteur ne voit pas tout (« sa » / « ça »). Geste 6 : Fichier > Enregistrer "
         "sous > PDF : le jury lit un PDF qui ne bouge pas, quel que soit l’ordinateur."},
        {"type": "comparer", "titre": "Mise en forme : avant / après", "gauche": ("Amateur", ["Gras à la main", "Espaces pour aligner", "Pages vides"]),
         "droite": ("Pro", ["Styles de titres", "Tabulations, tableaux", "Sauts de page"]), "notes":
         "Démonstration au vidéoprojecteur : afficher les marques de mise en forme (¶, Ctrl + Maj + 8) pour voir les « bricolages » "
         "(espaces multiples, retours à la ligne en série). C’est souvent un déclic pour les apprenants."},
        {"type": "activite", "titre": "Atelier Word : la note pro", "genre": "Individuel · sur poste", "duree": "45 min",
         "items": ["Arial 11, interligne 1,15", "Styles, sommaire, pages", "Tableau, export PDF"], "notes":
         "Les apprenants suivent les consignes en bas du fichier. Le formateur circule. Les plus rapides : ajouter un en-tête avec le "
         "nom du magasin et la date, et une image de la tête de gondole (image libre de droits, avec texte alternatif : clic droit > "
         "Modifier le texte de remplacement). Évaluation : grille critère 1."},
        {"type": "puces", "titre": "Raccourcis qui sauvent", "items": [
            "Ctrl + S : enregistrer", "Ctrl + Z : annuler", "Ctrl + Entrée : saut de page", "F7 : orthographe"], "notes":
         "Règle d’or de l’examen : Ctrl + S toutes les 5 minutes. Autres raccourcis utiles : Ctrl + C / Ctrl + V (copier / coller), "
         "Ctrl + F (rechercher), Ctrl + P (imprimer), Ctrl + A (tout sélectionner), Windows + flèche (ranger les fenêtres côte à côte)."},
        {"type": "section", "num": "02", "titre": "Excel", "sous_titre": "Faire parler les chiffres", "notes":
         "Pause de 10 minutes vers 10 h 00 avant de commencer Excel. Ouvrir J2_Exercices_Excel_apprenant.xlsx, onglet « 1-Ventes S46 »."},
        {"type": "cartes", "titre": "Excel en 4 idées", "items": [
            ("=", "toute formule"), ("B4-D4", "on vise des cellules"), ("$B$11", "on fige"), ("Ctrl+D", "on recopie")], "notes":
         "1) Une formule commence toujours par « = ». 2) On calcule avec les adresses des cellules, jamais avec les nombres tapés à la "
         "main (sinon, si la donnée change, le résultat est faux). 3) Le symbole $ fige une référence (touche F4) : utile pour diviser "
         "chaque jour par le total. 4) On recopie une formule vers le bas avec la poignée de recopie ou Ctrl + D."},
        {"type": "cartes", "titre": "Les 4 calculs du manager", "items": [
            ("Écart", "réalisé − objectif"), ("Écart %", "écart ÷ objectif"), ("Évolution", "(N − N-1) ÷ N-1"), ("Panier", "CA ÷ tickets")],
         "notes": "Montrer sur le lundi : écart = 4 820 − 5 000 = −180 € ; écart en % = −180 ÷ 5 000 = −3,6 % ; évolution = (4 820 − 4 650) "
                  "÷ 4 650 = +3,7 % ; panier moyen = 4 820 ÷ 412 = 11,70 €. Toujours diviser par la valeur de RÉFÉRENCE (l’objectif, ou "
                  "l’année précédente). Ces calculs seront approfondis lundi 23/11."},
        {"type": "exemple", "titre": "Ti Marché du Sud · S46", "lieu": "Saint-Louis", "lieu_detail": ["Supermarché fictif", "Fruits et légumes"],
         "items": ["CA semaine : 38 160 €", "Objectif : 39 500 €", "N-1 : 37 110 €", "Samedi : 23 % du CA"], "notes":
         "Corrigé : total réalisé 38 160 € ; objectif 39 500 € ; écart −1 340 € soit −3,4 % ; N-1 37 110 €, évolution +2,8 %. "
         "Samedi 8 950 € = 23,5 % du CA. Jour le plus faible : dimanche (3 870 €), mais le mardi est le seul jour de semaine en baisse "
         "par rapport à N-1 avec le jeudi et le dimanche. Panier moyen de la semaine : 38 160 ÷ 3 149 tickets = 12,12 €. "
         "Question au groupe : quelle conclusion pour le manager ? (On progresse vs N-1 mais on rate l’objectif.)"},
        {"type": "etapes", "titre": "Rendre lisible", "items": [
            ("Format %", "1 décimale"), ("Couleurs", "écarts négatifs"), ("Graphique", "histogramme")], "notes":
         "Accueil > Nombre > Pourcentage. Accueil > Mise en forme conditionnelle > Règles de mise en surbrillance > Inférieur à 0 → "
         "texte rouge foncé ET ajouter un signe « − » (la couleur ne doit jamais être seule porteuse de sens : daltonisme). "
         "Insertion > Graphique > Histogramme groupé : CA réalisé et objectif par jour. Un graphique = un message : titre explicite."},
        {"type": "activite", "titre": "Atelier Excel : tableau de bord", "genre": "Individuel · sur poste", "duree": "50 min",
         "items": ["Formules F à I", "Total, %, couleurs", "Graphique, 1 page A4"], "notes":
         "Les consignes sont dans le fichier (cellule A13). Le corrigé (J2_Exercices_Excel_CORRIGE.xlsx) est projeté à la fin. "
         "Pour les plus rapides : calculer la part de chaque jour dans le CA avec une référence figée ($B$11). Évaluation : grille critère 2."},
        {"type": "section", "num": "03", "titre": "PowerPoint", "sous_titre": "Convaincre le jury en 20 minutes", "notes":
         "Après le déjeuner. Démarrer par une question : « Qui s’est déjà endormi devant un PowerPoint ? Pourquoi ? »"},
        {"type": "cartes", "titre": "Une diapo qui marche", "items": [
            ("1 idée", "par diapo"), ("6 mots", "par ligne max"), ("24 pt", "minimum"), ("Contraste", "fort")], "notes":
         "Le diaporama soutient la parole, il ne la remplace pas : si tout est écrit, le jury lit au lieu d’écouter. Le jury peut "
         "compter des personnes malvoyantes ou être assis loin de l’écran. Ce support que vous voyez aujourd’hui respecte ces règles : "
         "il sert d’exemple."},
        {"type": "comparer", "titre": "Diapo ratée / réussie", "gauche": ("Ratée", ["Paragraphes entiers", "Petite police", "Fond chargé"]),
         "droite": ("Réussie", ["Mots-clés", "Un chiffre fort", "Un graphique simple"]), "notes":
         "Montrer un contre-exemple réel (préparé par le formateur) puis sa version corrigée. Règle pour les chiffres : un chiffre clé "
         "en très gros + une phrase courte (« +2,8 % vs N-1 »). Les détails vont dans le document écrit, que le jury a déjà lu."},
        {"type": "etapes", "titre": "Les gestes PowerPoint", "items": [
            ("Masque", "un seul style"), ("Graphique", "collé d’Excel"), ("Présentateur", "notes, minuteur")], "notes":
         "Affichage > Masque des diapositives : on règle police, couleurs et numéro de diapo une seule fois. Copier le graphique Excel, "
         "puis Collage spécial > image (il ne bougera plus). Diaporama > Mode Présentateur : vous voyez vos notes et le minuteur, le "
         "jury voit la diapo. Règle de temps : environ 1 minute par diapositive."},
        {"type": "activite", "titre": "Atelier : mon établissement", "genre": "Individuel · sur poste", "duree": "45 min",
         "items": ["5 diapos maximum", "Qui, où, quoi, combien", "Présenter en 3 min"], "notes":
         "Chaque apprenant crée 5 diapositives présentant SON établissement d’accueil (ou celui qu’il vise) : 1) identité (enseigne, "
         "format, ville) ; 2) organisation (effectif, organigramme simplifié) ; 3) clientèle et concurrence ; 4) son périmètre ; "
         "5) un chiffre clé. C’est l’ébauche de la page d’introduction obligatoire des deux dossiers. RGPD : pas de noms de collègues, "
         "des fonctions ; chiffres internes seulement avec l’accord du tuteur. Passage de 3 volontaires (3 min chacun). Grille critère 4."},
        {"type": "section", "num": "04", "titre": "Le jour J", "sous_titre": "Maquettes préétablies", "notes":
         "Pause de 10 minutes vers 14 h 30 avant le mini-cas."},
        {"type": "cartes", "titre": "Pièges des maquettes", "items": [
            ("Ne pas casser", "les formules"), ("Nom imposé", "enregistrer"), ("Aperçu", "avant impression"), ("Temps", "plan horaire")],
         "notes": "À l’examen, on vous donne des fichiers déjà construits. Ne jamais écrire dans une cellule qui contient une formule "
                  "(cellules souvent grisées ou verrouillées). Respecter le nom de fichier demandé. Toujours vérifier l’aperçu avant "
                  "impression (Ctrl + P) : un tableau coupé sur 3 pages est illisible. Et découper les 4 h dès le début (temps par "
                  "dossier), en gardant 15 minutes pour relire et imprimer."},
        {"type": "activite", "titre": "Mini-cas chronométré", "genre": "Type examen · 30 min", "duree": "30 min",
         "items": ["Onglet 2 : la commande", "Formules, 0 si négatif", "Analyse écrite : 5 lignes"], "notes":
         "Onglet « 2-Maquette commande » : calculer le besoin brut et la quantité à commander avec la formule donnée ; utiliser MAX(0; …) "
         "pour éviter une commande négative. Puis rédiger dans Word 5 lignes d’analyse : quel produit pose problème et que faire. "
         "Corrigé : mangues José à 0 en stock → rupture en cours, commande de 137 kg, alerter le responsable. Lien direct avec l’AT2 "
         "(gérer l’approvisionnement) que l’on verra en 2027."},
        {"type": "cartes", "titre": "Aller plus loin", "items": [
            ("Copilot", "IA dans Office"), ("LibreOffice", "gratuit, libre"), ("TCD", "tableaux croisés"), ("Raccourcis", "gagner du temps")],
         "notes": "Copilot (Microsoft 365) ou une IA comme Le Chat peut écrire une formule à partir d’une phrase (« formule Excel qui "
                  "calcule l’évolution entre B4 et C4 en % ») : utile pour apprendre, mais à l’examen il n’y a pas d’IA. Toujours "
                  "vérifier sur un exemple calculé à la main. RGPD : ne jamais coller dans une IA un fichier contenant des données de "
                  "clients ou de salariés (plannings nominatifs, fichier fidélité). LibreOffice : gratuit, installable chez soi pour "
                  "s’entraîner. Tableau croisé dynamique : pour aller plus loin en analyse des ventes (AT3)."},
        {"type": "activite", "titre": "Quiz : 10 questions", "genre": "Individuel", "duree": "15 min",
         "items": ["10 questions", "Correction ensemble", "Objectif : 7 / 10"], "notes": "Lecture à voix haute possible, temps majoré si aménagement."},
        {"type": "puces", "titre": "À retenir", "items": [
            "Word : styles, sommaire, PDF", "Excel : =, cellules, $", "Diapo : 1 idée, 24 pt", "Examen : Ctrl + S"], "notes":
         "Travail pour lundi 23/11 : finir les 5 diapositives « mon établissement » et refaire l’atelier Excel sans regarder le corrigé."},
        {"type": "question", "titre": "Mon engagement", "texte": "Cette semaine,\nje m’entraîne sur…", "notes":
         "Post-it individuel : un logiciel, une fonction précise. Fin 16 h."},
    ],
    "ressource": [
        ("Pourquoi la bureautique compte autant",
         "<p>Au titre MEM, l’ordinateur n’est pas un détail : l’<b>étude de cas de 4 heures</b> se fait sur poste, avec un traitement de "
         "texte et un tableur, à partir de <b>maquettes préétablies</b> (fichiers déjà construits), et vous imprimez vos travaux. "
         "Vos deux dossiers (AT3 et AT1) et vos deux diaporamas sont aussi produits sur ordinateur.</p>"
         + tableau(["Production", "Règles imposées (RC/RE MEM v09)"], [
             ["Documents écrits", "Arial 11, interligne 1,15 ; pages comptées hors page de garde, sommaire et annexes ; une page de "
              "présentation de l’établissement en introduction"],
             ["Dossier AT3", "12 à 18 pages + diaporama de 12 à 18 diapositives (présentation de 20 minutes)"],
             ["Dossier AT1", "16 à 24 pages + diaporama de 18 à 24 diapositives (présentation de 25 minutes)"],
             ["Étude de cas", "4 h ; traitement de texte et tableur ; impression des travaux"]])
         + encadre("retenir", "<p>Le jour J, la bureautique doit être un <b>réflexe</b>, pour que votre énergie aille à la réflexion "
                   "de manager, pas à la recherche d’un bouton.</p>")),
        ("Word : un dossier professionnel en 6 gestes",
         flux([("Styles", "Titre 1, Titre 2 : jamais de gras à la main pour un titre"), ("Sommaire", "Références > Table des matières"),
               ("Pages", "Insertion > Numéro de page ; Ctrl + Entrée = saut de page"), ("Tableaux", "Insertion > Tableau ; clic droit > Légende"),
               ("Orthographe", "F7 ; relire aussi à voix haute"), ("PDF", "Fichier > Enregistrer sous > PDF")], "Les 6 gestes Word")
         + "<h3>Pas à pas : appliquer Arial 11 et l’interligne 1,15 à tout le document</h3>"
         "<ol><li>Ctrl + A pour tout sélectionner.</li><li>Choisir Arial, taille 11 (onglet Accueil).</li>"
         "<li>Accueil > Paragraphe > Interligne > Options > Multiple : 1,15.</li>"
         "<li>Mieux : clic droit sur le style « Normal » > Modifier > Arial 11, interligne 1,15. Tout le document suit.</li></ol>"
         + encadre("astuce", "<p>Affichez les marques de mise en forme (bouton ¶ ou Ctrl + Maj + 8) : vous verrez les espaces et "
                   "retours à la ligne en trop, qui décalent tout à l’impression.</p>")
         + encadre("piege", "<p>Le sommaire automatique ne se met pas à jour seul : clic droit sur le sommaire > Mettre à jour les "
                   "champs > Mettre à jour toute la table, juste avant d’exporter en PDF.</p>")
         + "<h3>Accessibilité de vos documents</h3><ul><li>Texte alternatif sur chaque image (clic droit > Modifier le texte de "
           "remplacement).</li><li>Titres avec de vrais styles (un lecteur d’écran s’en sert pour naviguer).</li>"
           "<li>Ne jamais faire passer une information uniquement par la couleur.</li></ul>"),
        ("Excel : faire parler les chiffres",
         cartes([("Le signe =", "Toute formule commence par « = »."), ("Les cellules", "On calcule avec B4, D4… jamais avec des nombres tapés."),
                 ("Le $", "F4 fige une cellule : $B$11 ne bouge pas quand on recopie."), ("La recopie", "Poignée en bas à droite, ou Ctrl + D.")], cols=4)
         + "<h3>Les 4 calculs du manager (exemple : lundi, semaine 46)</h3>"
         + tableau(["Calcul", "Formule", "Exemple Excel", "Résultat"], [
             ["Écart à l’objectif (€)", "Réalisé − Objectif", "=B4-D4", "4 820 − 5 000 = <b>−180 €</b>"],
             ["Écart à l’objectif (%)", "(Réalisé − Objectif) ÷ Objectif", "=(B4-D4)/D4", "−180 ÷ 5 000 = <b>−3,6 %</b>"],
             ["Évolution N/N-1 (%)", "(N − N-1) ÷ N-1", "=(B4-C4)/C4", "170 ÷ 4 650 = <b>+3,7 %</b>"],
             ["Panier moyen (€)", "CA ÷ nombre de tickets", "=B4/E4", "4 820 ÷ 412 = <b>11,70 €</b>"]])
         + encadre("retenir", "<p>On divise toujours par la valeur de <b>référence</b> : l’objectif pour un écart, l’année précédente "
                   "pour une évolution.</p>")
         + "<h3>Les fonctions à connaître</h3>"
         + tableau(["Fonction", "À quoi elle sert", "Exemple"], [
             ["SOMME", "Additionner une plage", "=SOMME(B4:B10)"], ["MOYENNE", "Moyenne d’une plage", "=MOYENNE(B4:B10)"],
             ["MAX / MIN", "Plus grande / plus petite valeur", "=MAX(B4:B10)"],
             ["SI", "Afficher selon une condition", "=SI(F4<0;\"Sous objectif\";\"Objectif atteint\")"],
             ["MAX(0;…)", "Éviter un résultat négatif (commande)", "=MAX(0;G5-B5)"],
             ["RECHERCHEX", "Retrouver une information dans une liste", "=RECHERCHEX(A5;Tarifs!A:A;Tarifs!B:B)"]])
         + "<h3>Rendre lisible</h3><ul><li>Format pourcentage avec 1 décimale.</li><li>Mise en forme conditionnelle sur les écarts "
           "négatifs (rouge foncé) et toujours le signe « − » visible.</li><li>Un graphique = un message, avec un titre explicite.</li>"
           "<li>Mise en page : Fichier > Imprimer > « Ajuster la feuille à une page », orientation paysage.</li></ul>"),
        ("Le cas Ti Marché du Sud (données d’exercice)",
         "<p>Entreprise <b>fictive</b> : supermarché de Saint-Louis, rayon fruits et légumes, semaine 46, opération « Letchis de la Réunion ».</p>"
         + tableau(["Jour", "CA réalisé", "CA N-1", "Objectif", "Tickets"], [[j, f"{a:,} €".replace(",", " "), f"{b:,} €".replace(",", " "),
                                                                         f"{c:,} €".replace(",", " "), str(d)] for j, a, b, c, d in VENTES])
         + "<h3>Résultats à retrouver</h3>"
         + tableau(["Indicateur", "Résultat"], [["CA de la semaine", "38 160 €"], ["Objectif", "39 500 €"], ["Écart", "−1 340 € (−3,4 %)"],
                                                ["CA N-1", "37 110 €"], ["Évolution", "+2,8 %"], ["Panier moyen semaine", "12,12 €"],
                                                ["Part du samedi", "23,5 %"]])
         + encadre("ex", "<p><b>Lecture de manager :</b> le rayon progresse par rapport à l’an dernier mais n’atteint pas l’objectif. "
                   "Le samedi pèse près d’un quart des ventes ; le mardi, le jeudi et le dimanche reculent par rapport à N-1. "
                   "Pistes : renfort humain le samedi matin, animation du mardi. C’est exactement le raisonnement attendu en AT3.</p>")),
        ("PowerPoint : convaincre le jury",
         cartes([("1 idée par diapo", "Un titre qui dit le message."), ("6 mots par ligne", "Des mots-clés, pas des phrases."),
                 ("24 pt minimum", "Lisible du fond de la salle."), ("Contraste fort", "Texte foncé sur fond clair, ou l’inverse.")], cols=4)
         + "<h3>Structure conseillée pour vos diaporamas</h3>"
         + flux([("Garde", "titre, nom, date"), ("Sommaire", "3 à 5 parties"), ("Établissement", "identité, chiffres clés"),
                 ("Cœur", "1 compétence = 1 partie, avec preuves"), ("Bilan", "résultats, ce que j’ai appris")])
         + "<h3>Les gestes</h3><ul><li><b>Masque des diapositives</b> (Affichage) : police, couleurs, numéros réglés une seule fois.</li>"
           "<li><b>Graphique</b> : copier depuis Excel, Collage spécial > Image.</li>"
           "<li><b>Mode Présentateur</b> : vos notes et le minuteur sous vos yeux.</li>"
           "<li><b>Temps</b> : environ 1 minute par diapositive ; répétez à voix haute, chronomètre en main.</li></ul>"
         + encadre("jury", "<p>Le jury a déjà lu votre document. Le diaporama doit montrer l’essentiel et des preuves (graphiques, "
                   "photos du rayon, extraits de planning anonymisés), pas réciter le dossier.</p>")),
        ("Le jour J : survivre aux maquettes préétablies",
         tableau(["Piège", "Bon réflexe"], [
             ["Écrire par-dessus une formule", "Repérer les cellules grisées ou verrouillées ; ne saisir que dans les cellules prévues"],
             ["Perdre son travail", "Ctrl + S toutes les 5 minutes ; nom de fichier imposé"],
             ["Impression illisible", "Aperçu (Ctrl + P), ajuster à une page, orientation paysage si besoin"],
             ["Manquer de temps", "Plan horaire dès le début ; 15 minutes gardées pour relire et imprimer"],
             ["Calcul faux non vu", "Vérifier un résultat à la main ou à la calculatrice (ordre de grandeur)"]])
         + "<h3>Mini-cas : la maquette de commande</h3>"
         "<p>Formule donnée : <b>quantité à commander = ventes moyennes par jour × (délai de livraison + période couverte) + stock de "
         "sécurité − stock actuel</b>, et 0 si le résultat est négatif.</p>"
         + tableau(["Produit", "Stock", "Ventes/j", "Délai", "Période", "Sécurité", "Besoin brut", "À commander"], [
             [p, str(s), str(v), str(d), str(pe), str(se), str(v * (d + pe) + se), str(max(0, v * (d + pe) + se - s))]
             for p, s, v, d, pe, se in COMMANDE])
         + encadre("ex", "<p>Les <b>mangues José</b> sont à 0 en stock : la rupture est déjà là. Le manager commande (137 kg), prévient "
                   "son responsable, cherche une livraison anticipée, informe l’équipe et adapte l’implantation en attendant.</p>")),
        ("Aller plus loin avec ces outils",
         tableau(["Outil", "Ce qu’il apporte", "Vigilance"], [
             ["Copilot (Microsoft 365)", "Rédige une formule, résume un document, propose une mise en page", "Pas d’IA à l’examen ; vérifier "
              "chaque formule ; ne pas y mettre de données personnelles"],
             ["Le Chat (Mistral AI)", "Assistant IA d’une entreprise française, explique une formule pas à pas", "Mêmes règles : vérifier, "
              "anonymiser"],
             ["LibreOffice", "Suite gratuite et libre (Writer, Calc, Impress) pour s’entraîner chez soi", "Quelques différences de menus "
              "avec Microsoft Office"],
             ["Tableau croisé dynamique", "Analyse des ventes par rayon, par jour, par produit en quelques clics", "À travailler pour l’AT3"]])
         + encadre("loi", "<p><b>RGPD</b> : un planning nominatif, un fichier de clients fidèles ou un export de caisse avec des noms "
                   "sont des données personnelles. Ne les collez jamais dans une IA en ligne et anonymisez-les dans vos dossiers "
                   "(« Collaborateur A »).<br><b>IA Act</b> (art. 4) : depuis février 2025, les entreprises qui utilisent l’IA doivent "
                   "former leurs équipes à un usage maîtrisé ; savoir en parler est un plus en entretien.</p>")),
        ("Aide-mémoire des raccourcis",
         tableau(["Raccourci", "Action", "Raccourci", "Action"], [
             ["Ctrl + S", "Enregistrer", "Ctrl + Z", "Annuler"], ["Ctrl + C / V", "Copier / coller", "Ctrl + A", "Tout sélectionner"],
             ["Ctrl + Entrée", "Saut de page (Word)", "F7", "Orthographe"], ["F4", "Figer une cellule ($)", "Ctrl + D", "Recopier vers le bas"],
             ["Ctrl + P", "Imprimer / aperçu", "Windows + « + »", "Loupe d’écran"]])),
    ],
    "sources": [
        "RC/RE MEM v09 du 10/12/2025 : modalités de la mise en situation professionnelle et règles des productions (pièce jointe fournie).",
        "Support Microsoft : « Insérer une table des matières », « Fonctions Excel (par ordre alphabétique) » — support.microsoft.com.",
        "Règlement (UE) 2024/1689 (IA Act), article 4 (maîtrise de l’IA) — eur-lex.europa.eu.",
        "Données de vente : entreprise et chiffres fictifs créés pour l’exercice.",
    ],
    "grille": {
        "situation": "Ateliers sur poste : note Word mise en forme, tableau de bord Excel, 5 diapositives « mon établissement », mini-cas chronométré.",
        "criteres": [
            {"critere": "Document Word professionnel", "indicateurs": ["Arial 11, interligne 1,15, styles de titres", "Sommaire automatique, pagination, export PDF"],
             "niveaux": ["Mise en forme manuelle, pas de structure", "Styles partiels, sommaire absent", "Styles, sommaire, pagination corrects", "Document complet, légendes, texte alternatif, PDF propre"]},
            {"critere": "Calculs Excel justes", "indicateurs": ["Formules avec références de cellules", "Écart, évolution, panier moyen exacts"],
             "niveaux": ["Nombres tapés à la main ou faux", "1 ou 2 calculs justes", "Tous les calculs justes", "Justes, $ maîtrisé, vérification de cohérence"]},
            {"critere": "Lisibilité et analyse des chiffres", "indicateurs": ["Formats %, mise en forme conditionnelle, graphique titré", "Conclusion de manager formulée"],
             "niveaux": ["Tableau brut, pas d’analyse", "Mise en forme partielle", "Lisible et graphique pertinent", "Lisible + analyse juste (jour fort/faible, écart, pistes)"]},
            {"critere": "Diaporama « mon établissement »", "indicateurs": ["1 idée par diapo, 24 pt minimum, contraste", "Présentation orale de 3 min"],
             "niveaux": ["Diapos surchargées, illisibles", "Lisible mais trop de texte", "Règles respectées, oral clair", "Règles respectées, oral fluide, RGPD respecté"]},
            {"critere": "Travail sur maquette dans le temps", "indicateurs": ["Formules de la maquette préservées, MAX(0;…) utilisé", "Analyse écrite en 30 min"],
             "niveaux": ["Maquette cassée ou non finie", "Calculs partiels", "Calculs justes dans le temps", "Calculs justes + analyse pertinente + impression vérifiée"]},
        ]},
    "quiz": [
        {"q": "Quelle mise en forme est imposée pour les documents du dossier ?", "choix": ["Calibri 12, interligne 1,5", "Arial 11, interligne 1,15",
                                                                                      "Times 11, interligne simple", "Arial 12, interligne double"], "rep": 1,
         "explication": "Le RC/RE impose Arial 11 et un interligne de 1,15."},
        {"q": "Pour qu’un sommaire se construise automatiquement dans Word, il faut :", "choix": ["mettre les titres en gras", "utiliser les styles Titre 1, Titre 2",
                                                                                            "souligner les titres", "écrire les titres en majuscules"], "rep": 1,
         "explication": "Le sommaire automatique s’appuie sur les styles de titres."},
        {"q": "Quel raccourci insère un saut de page dans Word ?", "choix": ["Ctrl + S", "Ctrl + Entrée", "F7", "Ctrl + P"], "rep": 1,
         "explication": "Ctrl + Entrée insère un saut de page propre, au lieu d’une série de retours à la ligne."},
        {"q": "Par quel symbole commence toute formule Excel ?", "choix": ["+", "=", "$", "#"], "rep": 1, "explication": "Toute formule commence par le signe égal."},
        {"q": "CA réalisé 4 820 €, CA N-1 4 650 €. L’évolution est d’environ :", "choix": ["+170 %", "+3,5 %", "+3,7 %", "−3,7 %"], "rep": 2,
         "explication": "(4 820 − 4 650) ÷ 4 650 = 0,0366, soit +3,7 %. On divise par l’année précédente."},
        {"q": "CA de 4 820 € pour 412 tickets : le panier moyen est de :", "choix": ["8,55 €", "11,70 €", "117 €", "1 170 €"], "rep": 1,
         "explication": "Panier moyen = CA ÷ nombre de tickets = 4 820 ÷ 412 ≈ 11,70 €."},
        {"q": "Dans Excel, à quoi sert le $ dans $B$11 ?", "choix": ["Afficher des euros", "Figer la référence lors de la recopie", "Arrondir", "Protéger le fichier"], "rep": 1,
         "explication": "Le $ (touche F4) fige la ligne et la colonne : la référence ne bouge pas quand on recopie la formule."},
        {"q": "Quelle formule évite une quantité à commander négative ?", "choix": ["=MIN(0;G5-B5)", "=MAX(0;G5-B5)", "=SOMME(G5-B5)", "=SI(G5)"], "rep": 1,
         "explication": "MAX(0;…) renvoie 0 si le résultat est négatif."},
        {"q": "Sur une diapositive destinée au jury, la taille de texte minimale conseillée est :", "choix": ["12 pt", "16 pt", "24 pt", "Peu importe"], "rep": 2,
         "explication": "24 pt minimum pour être lisible de loin, y compris par une personne malvoyante."},
        {"q": "À l’examen, sur une maquette préétablie, il ne faut surtout pas :", "choix": ["enregistrer souvent", "écrire dans une cellule qui contient une formule",
                                                                                         "vérifier l’aperçu avant impression", "respecter le nom de fichier"], "rep": 1,
         "explication": "Écraser une formule casse la maquette et fausse tous les résultats."},
    ],
    "deroule": [
        ("8 h 00 – 8 h 15", "Accueil et retour sur les engagements", "Se remobiliser (Bloom 1)", "Post-it du 9/11 : qui a avancé ? Annonce du programme",
         "Interrogative · symbolique", "Diapo 1, post-it", "Oral"),
        ("8 h 15 – 8 h 30", "Défi « 60 secondes chrono »", "Se positionner (Bloom 3)", "3 mini-défis : enregistrer sous, copier un tableau, somme ; constitution de binômes",
         "Ludique · enactif", "Diapos 2-3, postes", "Diagnostique 0 à 3/3"),
        ("8 h 30 – 8 h 45", "Les règles du RC/RE", "Citer les règles de forme (Bloom 1)", "Arial 11, 1,15, nombre de pages et diapos, durée des présentations",
         "Expositive · symbolique", "Diapos 4-5", "Questions flash"),
        ("8 h 45 – 10 h 00", "S1 · Word : 6 gestes + atelier", "Structurer un document (Bloom 3)",
         "Démonstration des 6 gestes ; avant / après ; atelier « note pro » sur le texte brut ; raccourcis", "Démonstrative puis active · enactif",
         "Diapos 6-11, texte brut .docx", "Grille critère 1"),
        ("10 h 00 – 10 h 10", "Pause", "", "", "", "", ""),
        ("10 h 10 – 10 h 40", "S2 · Excel : les bases", "Écrire une formule juste (Bloom 3)",
         "=, cellules, $, recopie ; 4 calculs du manager démontrés sur le lundi", "Démonstrative · iconique", "Diapos 12-14, classeur apprenant", "Calcul guidé"),
        ("10 h 40 – 11 h 50", "S2 · Atelier tableau de bord", "Calculer et analyser (Bloom 3-4)",
         "Colonnes F à I, totaux, formats, mise en forme conditionnelle, graphique, mise en page ; lecture de manager du cas Ti Marché du Sud",
         "Active · enactif + iconique", "Diapos 15-17, classeur, corrigé projeté", "Grille critères 2 et 3"),
        ("11 h 50 – 12 h 00", "Synthèse matinée", "Reformuler (Bloom 2)", "Ce qui a été difficile ; astuces partagées", "Réflexive", "Tableau", "Oral"),
        ("12 h 00 – 13 h 00", "Pause déjeuner", "", "", "", "", ""),
        ("13 h 00 – 13 h 30", "S3 · PowerPoint : les règles", "Expliquer ce qui rend une diapo efficace (Bloom 2)",
         "« Qui s’est déjà endormi devant un PowerPoint ? » ; 4 règles ; ratée / réussie ; masque, graphique, mode présentateur",
         "Interrogative + démonstrative · iconique", "Diapos 18-21", "Questions"),
        ("13 h 30 – 14 h 30", "S3 · Atelier « mon établissement »", "Concevoir 5 diapositives (Bloom 6)",
         "Création individuelle (45 min) ; 3 présentations volontaires de 3 min avec retours", "Active · enactif", "Diapo 22, postes", "Grille critère 4"),
        ("14 h 30 – 14 h 40", "Pause", "", "", "", "", ""),
        ("14 h 40 – 15 h 20", "S4 · Le jour J + mini-cas", "Travailler sur maquette dans le temps (Bloom 3-4)",
         "Pièges des maquettes (10 min) ; mini-cas chronométré commande + analyse (30 min)", "Simulation · enactif", "Diapos 23-25, onglet 2", "Grille critère 5"),
        ("15 h 20 – 15 h 40", "Correction et aller plus loin", "Transférer (Bloom 2)", "Corrigé projeté ; Copilot, Le Chat, LibreOffice, TCD ; RGPD des fichiers",
         "Expositive · symbolique", "Diapo 26, corrigé", "Auto-correction"),
        ("15 h 40 – 15 h 55", "Quiz 10 questions", "Évaluer (Bloom 1-3)", "Quiz individuel puis correction", "Évaluative", "Quiz", "Sommative 7/10"),
        ("15 h 55 – 16 h 00", "Bilan et engagement", "S’engager (Bloom 3)", "À retenir ; post-it ; annonce du 23/11", "Réflexive", "Diapos 28-30", "Engagement écrit"),
    ],
}
