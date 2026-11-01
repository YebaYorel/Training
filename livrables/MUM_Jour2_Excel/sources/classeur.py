"""Classeur de missions RUN'ATTITUDE auto-corrigé (MUM · Jour 2 · Excel).

    python3 classeur.py <dossier_sortie>

Produit la version stagiaire (cases jaunes vides) et le corrigé formateur (cases remplies,
tous les contrôles à ✔). Fonctionne hors ligne sous Excel 2013+ et LibreOffice Calc :
aucune macro, aucune donnée personnelle, aucun envoi vers un service extérieur.
"""
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

MARINE, OR, NOIR, BLANC, CLAIR = "1B3A6B", "C9AB4C", "121212", "FFFFFF", "EEF2F8"
JAUNE, VERT, ROUGE = "FFF2B3", "C6EFCE", "FFC7CE"
POLICE = "Inter"
fin = Side(style="thin", color="8A97A8")
BORD = Border(left=fin, right=fin, top=fin, bottom=fin)

PRODUITS = [  # réf, produit, quantité, prix unitaire
    ("P01", "T-shirt « 974 »", 24, 19.90), ("P02", "Casquette Piton", 8, 14.50), ("P03", "Tongs Lagon", 35, 9.90),
    ("P04", "Sac en vacoa", 6, 29.00), ("P05", "Vanille Bourbon (3 gousses)", 15, 12.00), ("P06", "Confiture de goyavier", 4, 6.50),
    ("P07", "Café Bourbon pointu 250 g", 9, 18.00), ("P08", "Savon artisanal combava", 40, 5.50), ("P09", "Mug « Piton de la Fournaise »", 12, 11.00),
    ("P10", "Paréo", 18, 22.00), ("P11", "Bob soleil", 3, 13.90), ("P12", "Gourde inox", 27, 21.00)]
PIEGES = {"P03": "35 ", "P08": "'40", "P12": " 27"}          # quantités saisies en texte (Mission 1)
VENTES = [("Lundi", 1245), ("Mardi", 980), ("Mercredi", 1110), ("Jeudi", 1370), ("Vendredi", 1865), ("Samedi", 2640), ("Dimanche", 1520)]
OBJECTIF = 11000
L0 = 6                                                    # première ligne de données
LN = L0 + len(PRODUITS) - 1                               # dernière ligne (17)


def f(cell, size=14, bold=False, color=NOIR, fill=None, align="left", wrap=False, nf=None):
    cell.font = Font(name=POLICE, size=size, bold=bold, color=color)
    cell.alignment = Alignment(horizontal=align, vertical="center", wrap_text=wrap)
    if fill:
        cell.fill = PatternFill("solid", fgColor=fill)
    if nf:
        cell.number_format = nf


def entete(ws, titre, mission, consignes, largeurs):
    for col, w in largeurs.items():
        ws.column_dimensions[col].width = w
    ws.merge_cells("A1:H1"); ws["A1"] = titre; f(ws["A1"], 22, True, BLANC, MARINE)
    ws.row_dimensions[1].height = 36
    ws.merge_cells("A2:H2"); ws["A2"] = mission; f(ws["A2"], 14, True, MARINE, CLAIR, wrap=True)
    ws.row_dimensions[2].height = 40
    ws.merge_cells("A3:H3"); ws["A3"] = consignes; f(ws["A3"], 13, False, NOIR, None, wrap=True)
    ws.row_dimensions[3].height = 58
    ws.sheet_view.zoomScale = 110
    ws.sheet_properties.tabColor = OR


def ligne_titres(ws, row, titres):
    for i, t in enumerate(titres):
        c = ws.cell(row=row, column=i + 1, value=t)
        f(c, 14, True, BLANC, MARINE, "center", True); c.border = BORD
    ws.row_dimensions[row].height = 34


def a_remplir(c, nf=None):
    f(c, 14, False, NOIR, JAUNE, "right", nf=nf); c.border = BORD


def controle(ws, ref, formule):
    c = ws[ref]; c.value = formule
    f(c, 16, True, NOIR, None, "center"); c.border = BORD


def couleurs_controle(ws, plage):
    premiere = plage.split(":")[0]
    ws.conditional_formatting.add(plage, FormulaRule(formula=[f'LEFT({premiere},1)="✔"'], fill=PatternFill("solid", fgColor=VERT)))
    ws.conditional_formatting.add(plage, FormulaRule(formula=[f'LEFT({premiere},1)="✘"'], fill=PatternFill("solid", fgColor=ROUGE)))


def produits(ws, pieges=False, mise_en_forme=True):
    for i, (ref, nom, q, p) in enumerate(PRODUITS):
        r = L0 + i
        valeurs = [ref, nom, PIEGES.get(ref, q) if pieges else q, p]
        for j, v in enumerate(valeurs):
            c = ws.cell(row=r, column=j + 1, value=v)
            if mise_en_forme:
                f(c, 14, nf='#,##0.00 "€"' if j == 3 else None); c.border = BORD
            else:
                c.font = Font(name=POLICE, size=11)


def construire(corrige: bool) -> Workbook:
    wb = Workbook()
    # ------------------------------------------------------------------ Accueil
    ws = wb.active; ws.title = "Accueil"
    entete(ws, "RUN'ATTITUDE · Boutique du Chaudron", "Vous êtes manager de la boutique. La direction régionale vous confie 4 missions, un coffre à ouvrir et un bonus pour la maison.",
           "Règle unique : on écrit seulement dans les cases JAUNES. La colonne « Contrôle » affiche ✔ quand c'est juste, ✘ sinon. "
           "Le score se met à jour tout seul dans la feuille « Tableau de bord ».", {"A": 6, "B": 44, "C": 18, "D": 18, "E": 18, "F": 18, "G": 4, "H": 16})
    for i, (t, d) in enumerate([("Mission 1 · Stock", "Un tableau lisible, des nombres qui en sont"), ("Mission 2 · Valeur", "Valeur, total, moyenne"),
                                ("Mission 3 · Alerte", "Trier, filtrer, décider avec SI"), ("Mission 4 · Erreurs", "####, #VALEUR!, #DIV/0!"),
                                ("Le coffre", "4 codes, 1 coffre : escape game final"), ("Bonus · Ventes", "À la maison : total, moyenne, écart à l'objectif")]):
        ws.cell(row=5 + i, column=1, value=i + 1); ws.cell(row=5 + i, column=2, value=t); ws.merge_cells(start_row=5 + i, start_column=3, end_row=5 + i, end_column=6)
        ws.cell(row=5 + i, column=3, value=d)
        for col in (1, 2, 3):
            f(ws.cell(row=5 + i, column=col), 14, col == 2, MARINE if col == 2 else NOIR, CLAIR if i % 2 == 0 else None)
        ws.row_dimensions[5 + i].height = 26
    ws["B12"] = "Formation YEBA FORMATIONS · Titre professionnel MUM · Jour 2 Excel"; f(ws["B12"], 11, False, "5B6B7C")
    ws["B13"] = "Données fictives. Aucune donnée personnelle. Classeur sans macro, utilisable hors ligne."; f(ws["B13"], 11, False, "5B6B7C")

    # ------------------------------------------------------------------ Mission 1
    ws = wb.create_sheet("Mission 1 · Stock")
    entete(ws, "Mission 1 · Le stock du Chaudron", "La direction veut un état du stock propre et fiable.",
           "1) Mettez l'en-tête en gras sur fond coloré. 2) Ajustez les colonnes. 3) Format € pour les prix. "
           "4) Trois quantités sont enregistrées en TEXTE (alignées à gauche) : retapez-les pour obtenir 12 ✔.",
           {"A": 8, "B": 36, "C": 14, "D": 18, "E": 4, "F": 4, "G": 4, "H": 14})
    for j, t in enumerate(["Réf", "Produit", "Quantité", "Prix unitaire"]):
        ws.cell(row=5, column=j + 1, value=t).font = Font(name=POLICE, size=11)
    ws.cell(row=5, column=8, value="Contrôle"); f(ws["H5"], 14, True, BLANC, MARINE, "center")
    produits(ws, pieges=not corrige, mise_en_forme=corrige)
    for r in range(L0, LN + 1):
        a_remplir(ws.cell(row=r, column=3)) if not corrige else None
        ws.cell(row=r, column=3).fill = PatternFill("solid", fgColor=JAUNE)
        controle(ws, f"H{r}", f'=IF(ISNUMBER(C{r}),"✔","✘")')
    couleurs_controle(ws, f"H{L0}:H{LN}")
    if corrige:
        ligne_titres(ws, 5, ["Réf", "Produit", "Quantité", "Prix unitaire"])

    # ------------------------------------------------------------------ Mission 2
    ws = wb.create_sheet("Mission 2 · Valeur")
    entete(ws, "Mission 2 · La valeur du stock", "La direction veut la valeur du stock, produit par produit et au total.",
           "1) Colonne Valeur : =C6*D6 puis recopiez avec la poignée. 2) Total du stock en E19 avec SOMME. "
           "3) Prix moyen en D20 avec MOYENNE. Le contrôle exige une FORMULE : un nombre tapé à la main donne ✘.",
           {"A": 8, "B": 36, "C": 14, "D": 18, "E": 20, "F": 4, "G": 4, "H": 14})
    ligne_titres(ws, 5, ["Réf", "Produit", "Quantité", "Prix unitaire", "Valeur"])
    ws.cell(row=5, column=8, value="Contrôle"); f(ws["H5"], 14, True, BLANC, MARINE, "center")
    produits(ws)
    for r in range(L0, LN + 1):
        a_remplir(ws[f"E{r}"], '#,##0.00 "€"')
        if corrige:
            ws[f"E{r}"] = f"=C{r}*D{r}"
        controle(ws, f"H{r}", f'=IF(AND(_xlfn.ISFORMULA(E{r}),ROUND(E{r}-C{r}*D{r},2)=0),"✔","✘")')
    ws["D19"] = "Total du stock"; f(ws["D19"], 14, True, MARINE, None, "right")
    ws["C20"] = "Prix moyen"; f(ws["C20"], 14, True, MARINE, None, "right")
    a_remplir(ws["E19"], '#,##0.00 "€"'); a_remplir(ws["D20"], '#,##0.00 "€"')
    if corrige:
        ws["E19"] = f"=SUM(E{L0}:E{LN})"; ws["D20"] = f"=AVERAGE(D{L0}:D{LN})"
    controle(ws, "H19", f'=IF(AND(_xlfn.ISFORMULA(E19),ROUND(E19,2)=ROUND(SUMPRODUCT(C{L0}:C{LN},D{L0}:D{LN}),2)),"✔","✘")')
    controle(ws, "H20", f'=IF(AND(_xlfn.ISFORMULA(D20),ROUND(D20,2)=ROUND(AVERAGE(D{L0}:D{LN}),2)),"✔","✘")')
    couleurs_controle(ws, f"H{L0}:H20")

    # ------------------------------------------------------------------ Mission 3
    ws = wb.create_sheet("Mission 3 · Alerte")
    entete(ws, "Mission 3 · Alerte rupture", "La direction veut voir en un coup d'œil les produits à recommander (seuil : moins de 10).",
           "1) Triez le tableau par quantité croissante (sélectionnez A5:F17). 2) Filtrez quantité < 10. "
           "3) Colonne « À recommander » : Oui ou Non (★ si vous utilisez =SI(C6<10;\"Oui\";\"Non\")). 4) En F19 : le nombre de « Oui » avec NB.SI.",
           {"A": 8, "B": 36, "C": 14, "D": 18, "E": 4, "F": 20, "G": 6, "H": 14})
    ligne_titres(ws, 5, ["Réf", "Produit", "Quantité", "Prix unitaire", "", "À recommander", "★"])
    ws.cell(row=5, column=8, value="Contrôle"); f(ws["H5"], 14, True, BLANC, MARINE, "center")
    produits(ws)
    if corrige:   # le corrigé montre le tableau déjà trié par quantité croissante
        tri = sorted(PRODUITS, key=lambda x: x[2])
        for i, (ref, nom, q, p) in enumerate(tri):
            for j, v in enumerate((ref, nom, q, p)):
                ws.cell(row=L0 + i, column=j + 1, value=v)
    for r in range(L0, LN + 1):
        a_remplir(ws[f"F{r}"]); ws[f"F{r}"].alignment = Alignment(horizontal="center", vertical="center")
        if corrige:
            ws[f"F{r}"] = f'=IF(C{r}<10,"Oui","Non")'
        controle(ws, f"G{r}", f'=IF(_xlfn.ISFORMULA(F{r}),"★","")'); ws[f"G{r}"].font = Font(name=POLICE, size=16, bold=True, color=OR)
        controle(ws, f"H{r}", f'=IF(F{r}="","✘",IF(F{r}=IF(C{r}<10,"Oui","Non"),"✔","✘"))')
    ws["D19"] = "Produits à recommander"; f(ws["D19"], 14, True, MARINE, None, "right")
    a_remplir(ws["F19"])
    if corrige:
        ws["F19"] = f'=COUNTIF(F{L0}:F{LN},"Oui")'
    controle(ws, "H19", f'=IF(AND(ISNUMBER(F19),F19=COUNTIF(C{L0}:C{LN},"<10")),"✔","✘")')
    couleurs_controle(ws, f"H{L0}:H19")
    ws.auto_filter.ref = f"A5:F{LN}"

    # ------------------------------------------------------------------ Mission 4
    ws = wb.create_sheet("Mission 4 · Erreurs")
    entete(ws, "Mission 4 · La chasse aux erreurs", "Le tableau de caisse d'hier ne marche pas. Trois erreurs : trouvez la cause, écrivez-la, corrigez.",
           "Cherchez ####, #VALEUR! et #DIV/0!. Écrivez la cause dans la colonne F, puis réparez. Les ✔ apparaissent quand c'est réparé.",
           {"A": 4, "B": 34, "C": 16, "D": 8 if not corrige else 18, "E": 4, "F": 44, "G": 4, "H": 14})
    ligne_titres(ws, 5, ["", "Indicateur", "Donnée", "Résultat", "", "Cause de l'erreur"])
    ws.cell(row=5, column=8, value="Contrôle"); f(ws["H5"], 14, True, BLANC, MARINE, "center")
    lignes = [("Chiffre d'affaires du jour", 12450, None), ("Quantité de bobs vendus", 12 if corrige else "douze", None),
              ("Prix d'un bob", 13.90, None), ("Valeur des bobs vendus", None, "=C7*C8"), ("Nombre de clients", 415 if corrige else None, None),
              ("Panier moyen", None, "=C6/C10"), ("Chiffre d'affaires affiché", None, "=C6")]
    for i, (lib, don, res) in enumerate(lignes):
        r = 6 + i
        ws[f"B{r}"] = lib; f(ws[f"B{r}"], 14); ws[f"B{r}"].border = BORD
        c = ws[f"C{r}"]; c.value = don
        if res is None:
            a_remplir(c, '#,##0.00 "€"' if r in (6, 8) else None)
        if res:
            ws[f"D{r}"] = res; f(ws[f"D{r}"], 14, True, nf='#,##0.00 "€"', align="right"); ws[f"D{r}"].border = BORD
    ws["D6"] = None
    ws["D12"].number_format = '#,##0.00 "€"'
    for r in (9, 11, 12):
        a_remplir(ws[f"F{r}"]); ws[f"F{r}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    if corrige:
        ws["F9"] = "Texte « douze » dans un calcul → taper 12"; ws["F11"] = "Division par une cellule vide → saisir 415 clients"
        ws["F12"] = "Colonne trop étroite → élargir la colonne D"
    controle(ws, "H9", '=IF(ISERROR(D9),"✘",IF(ROUND(D9,2)=166.8,"✔","✘"))')
    controle(ws, "H11", '=IF(ISERROR(D11),"✘",IF(ROUND(D11,2)=30,"✔","✘"))')
    controle(ws, "H12", '=IF(AND(CELL("width",D12)>=12,LEN(F12)>0),"✔","✘")')
    ws["B14"] = "Remarque formateur : le ✔ de la ligne 12 se met à jour après un recalcul (F9 ou une saisie)."; f(ws["B14"], 11, False, "5B6B7C")
    couleurs_controle(ws, "H9:H12")

    # ------------------------------------------------------------------ Mission 5
    ws = wb.create_sheet("Bonus · Ventes")
    entete(ws, "Bonus à la maison · Les ventes de la semaine", f"Objectif hebdomadaire fixé par la direction : {OBJECTIF:,} €".replace(",", " ") + ". Êtes-vous dans les clous ?",
           "Calculez avec des formules : total, moyenne, meilleur jour (MAX), écart en € (total - objectif), écart en % (écart ÷ objectif). "
           "Puis écrivez en B20 une phrase d'alerte pour la direction, avec une action.",
           {"A": 4, "B": 36, "C": 20, "D": 4, "E": 4, "F": 4, "G": 4, "H": 14})
    ligne_titres(ws, 5, ["", "Jour", "Chiffre d'affaires"])
    ws.cell(row=5, column=8, value="Contrôle"); f(ws["H5"], 14, True, BLANC, MARINE, "center")
    for i, (j, v) in enumerate(VENTES):
        ws[f"B{6 + i}"] = j; ws[f"C{6 + i}"] = v
        f(ws[f"B{6 + i}"], 14); f(ws[f"C{6 + i}"], 14, nf='#,##0 "€"', align="right")
        ws[f"B{6 + i}"].border = ws[f"C{6 + i}"].border = BORD
    calc = [(13, "Total de la semaine", "=SUM(C6:C12)", '#,##0 "€"', "ROUND(C13,2)=ROUND(SUM(C6:C12),2)"),
            (14, "Moyenne par jour", "=AVERAGE(C6:C12)", '#,##0.00 "€"', "ROUND(C14,2)=ROUND(AVERAGE(C6:C12),2)"),
            (15, "Objectif de la semaine", None, '#,##0 "€"', None),
            (16, "Meilleur jour (montant)", "=MAX(C6:C12)", '#,##0 "€"', "C16=MAX(C6:C12)"),
            (17, "Écart à l'objectif (€)", "=C13-C15", '#,##0 "€";-#,##0 "€"', f"ROUND(C17,2)=ROUND(SUM(C6:C12)-{OBJECTIF},2)"),
            (18, "Écart à l'objectif (%)", "=C17/C15", "0.00%", f"ROUND(C18,4)=ROUND((SUM(C6:C12)-{OBJECTIF})/{OBJECTIF},4)")]
    for r, lib, form, nf, test in calc:
        ws[f"B{r}"] = lib; f(ws[f"B{r}"], 14, True, MARINE)
        if form is None:
            ws[f"C{r}"] = OBJECTIF; f(ws[f"C{r}"], 14, True, nf=nf, align="right"); ws[f"C{r}"].border = BORD
            continue
        a_remplir(ws[f"C{r}"], nf)
        if corrige:
            ws[f"C{r}"] = form
        controle(ws, f"H{r}", f'=IF(AND(_xlfn.ISFORMULA(C{r}),{test}),"✔","✘")')
    ws["B19"] = "Phrase d'alerte à la direction :"; f(ws["B19"], 14, True, MARINE)
    ws.merge_cells("B20:G21"); a_remplir(ws["B20"]); ws["B20"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[20].height = 30; ws.row_dimensions[21].height = 30
    if corrige:
        ws["B20"] = "Semaine à 10 730 €, 270 € sous l'objectif (-2,5 %). Mardi est le jour faible : je propose une animation dégustation le mardi."
    controle(ws, "H20", '=IF(LEN(B20)>=40,"✔","✘")')
    couleurs_controle(ws, "H13:H20")

    # ------------------------------------------------------------------ Le coffre
    ws = wb.create_sheet("Le coffre")
    entete(ws, "Le coffre du Chaudron · Escape game", "Chaque code est un résultat de vos missions. Le coffre s'ouvre si les 4 codes sont justes.",
           "Équipe de 3 · 20 minutes · 2 indices maximum (2 minutes de pénalité chacun). Saisissez des nombres entiers.",
           {"A": 4, "B": 58, "C": 18, "D": 4, "E": 4, "F": 4, "G": 4, "H": 14})
    # les codes attendus sont recalculés à partir de données de référence (feuille masquée), jamais écrits en clair
    ref = wb.create_sheet("_ref"); ref.sheet_state = "hidden"
    for i, (r_, nom, q, p) in enumerate(PRODUITS):
        ref.cell(row=i + 1, column=1, value=q); ref.cell(row=i + 1, column=2, value=p)
    for i, (j, v) in enumerate(VENTES):
        ref.cell(row=i + 1, column=3, value=v)
    ref["D1"] = OBJECTIF; ref["E1"] = 12450; ref["F1"] = 415
    codes = [("Code 1 · Nombre de produits à recommander (Mission 3)", 5, 'COUNTIF(_ref!A1:A12,"<10")'),
             ("Code 2 · Valeur totale du stock, arrondie à l'euro (Mission 2)", 2839, "ROUND(SUMPRODUCT(_ref!A1:A12,_ref!B1:B12),0)"),
             ("Code 3 · Panier moyen réparé, en euros (Mission 4)", 30, "ROUND(_ref!E1/_ref!F1,0)"),
             ("Code 4 · Prix moyen des produits, arrondi à l'euro (Mission 2)", 15, "ROUND(AVERAGE(_ref!B1:B12),0)")]
    ligne_titres(ws, 5, ["", "Énigme", "Votre code"])
    ws.cell(row=5, column=8, value="Contrôle"); f(ws["H5"], 14, True, BLANC, MARINE, "center")
    for i, (lib, sol, attendu) in enumerate(codes):
        r = 6 + i
        ws[f"B{r}"] = lib; f(ws[f"B{r}"], 14, wrap=True); ws[f"B{r}"].border = BORD; ws.row_dimensions[r].height = 30
        a_remplir(ws[f"C{r}"], "0")
        if corrige:
            ws[f"C{r}"] = sol
        controle(ws, f"H{r}", f'=IF(AND(ISNUMBER(C{r}),C{r}={attendu}),"✔","✘")')
    couleurs_controle(ws, "H6:H9")
    ws.merge_cells("B11:H13")
    ws["B11"] = '=IF(COUNTIF(H6:H9,"✔")=4,"🔓 COFFRE OUVERT · Bravo l\'équipe !","🔒 Coffre fermé · "&COUNTIF(H6:H9,"✔")&" code(s) juste(s) sur 4")'
    f(ws["B11"], 24, True, BLANC, MARINE, "center")
    ws.conditional_formatting.add("B11", FormulaRule(formula=['COUNTIF($H$6:$H$9,"✔")=4'], fill=PatternFill("solid", fgColor="2E7D32")))

    # ------------------------------------------------------------------ Tableau de bord
    ws = wb.create_sheet("Tableau de bord", 1)
    entete(ws, "Tableau de bord des missions", "Votre score se met à jour à chaque ✔.", "Objectif de la journée : 100 %. Le formateur relève le score à 11h45. Le bonus ne compte pas dans le total.",
           {"A": 4, "B": 30, "C": 14, "D": 14, "E": 14, "F": 30, "G": 4, "H": 4})
    ligne_titres(ws, 5, ["", "Mission", "✔ obtenus", "Sur", "Réussite", "Progression"])
    plages = [("Mission 1 · Stock", f"'Mission 1 · Stock'!H{L0}:H{LN}", 12), ("Mission 2 · Valeur", f"'Mission 2 · Valeur'!H{L0}:H20", 14),
              ("Mission 3 · Alerte", f"'Mission 3 · Alerte'!H{L0}:H19", 13), ("Mission 4 · Erreurs", "'Mission 4 · Erreurs'!H9:H12", 3),
              ("Le coffre", "'Le coffre'!H6:H9", 4), ("Bonus maison · Ventes", "'Bonus · Ventes'!H13:H20", 6)]
    for i, (nom, plage, sur) in enumerate(plages):
        r = 6 + i
        ws[f"B{r}"] = nom; ws[f"C{r}"] = f'=COUNTIF({plage},"✔")'; ws[f"D{r}"] = sur; ws[f"E{r}"] = f"=C{r}/D{r}"
        ws[f"F{r}"] = f'=REPT("█",ROUND(E{r}*10,0))&REPT("░",10-ROUND(E{r}*10,0))'
        for col in "BCDEF":
            f(ws[f"{col}{r}"], 14, col == "B", MARINE if col == "F" else NOIR, CLAIR if i % 2 == 0 else None, "left" if col in "BF" else "center",
              nf="0%" if col == "E" else None)
            ws[f"{col}{r}"].border = BORD
    ws["B13"] = "TOTAL DU MATIN"; ws["C13"] = "=SUM(C6:C10)"; ws["D13"] = "=SUM(D6:D10)"; ws["E13"] = "=C13/D13"
    ws["F13"] = '=REPT("█",ROUND(E13*10,0))&REPT("░",10-ROUND(E13*10,0))'
    for col in "BCDEF":
        f(ws[f"{col}13"], 16, True, BLANC, MARINE, "left" if col in "BF" else "center", nf="0%" if col == "E" else None)
    return wb


if __name__ == "__main__":
    sortie = Path(sys.argv[1]); sortie.mkdir(parents=True, exist_ok=True)
    construire(False).save(sortie / "Classeur_missions_RUNATTITUDE.xlsx")
    construire(True).save(sortie / "Classeur_missions_CORRIGE_FORMATEUR.xlsx")
    print("ok")
