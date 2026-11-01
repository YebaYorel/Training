"""Classeur de traçabilité de la mise à niveau MEM : positionnement → formatives → sommative → remédiation."""
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.drawing.image import Image as XLImage

BLEU, OR, CLAIR, NOIR = "1B3A6B", "C9AB4C", "EEF2F8", "121212"
N = 16  # stagiaires prévus
F = lambda **k: Font(name="Inter", size=14, color=NOIR, **k)
ENT = Font(name="Montserrat", size=14, bold=True, color="FFFFFF")
TIT = Font(name="Montserrat", size=20, bold=True, color=BLEU)
FOND_ENT, FOND_CL, FOND_OR = PatternFill("solid", fgColor=BLEU), PatternFill("solid", fgColor=CLAIR), PatternFill("solid", fgColor=OR)
T = Side(style="thin", color="9AA5B1"); BORD = Border(left=T, right=T, top=T, bottom=T)
RET = Alignment(wrap_text=True, vertical="center")
VERT, ROUGE, ORANGE = PatternFill("solid", fgColor="E5F3EA"), PatternFill("solid", fgColor="FDECEC"), PatternFill("solid", fgColor="FFF3DC")

def feuille(wb, nom, titre, sous, entetes, largeurs, premiere=False):
    ws = wb.active if premiere else wb.create_sheet(nom)
    ws.title = nom
    ws.sheet_view.showGridLines = False
    ws.page_setup.orientation = "landscape"; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.oddFooter.left.text = "YEBA FORMATIONS — traçabilité de la mise à niveau MEM"; ws.oddFooter.right.text = "Page &P / &N"
    ws["A1"] = titre; ws["A1"].font = TIT; ws.row_dimensions[1].height = 34
    ws["A2"] = sous; ws["A2"].font = F(italic=True); ws["A2"].alignment = RET; ws.row_dimensions[2].height = 40
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(entetes)); ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(entetes))
    for i, (e, w) in enumerate(zip(entetes, largeurs), 1):
        c = ws.cell(4, i, e); c.font = ENT; c.fill = FOND_ENT; c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); c.border = BORD
        ws.column_dimensions[c.column_letter].width = w
    ws.row_dimensions[4].height = 58
    ws.freeze_panes = "C5"
    return ws

def ligne(ws, r, n, bande):
    for col in range(1, n + 1):
        c = ws.cell(r, col); c.font = F(); c.border = BORD; c.alignment = RET
        if bande: c.fill = FOND_CL
    ws.row_dimensions[r].height = 26

wb = Workbook()
# ---- Mode d'emploi
ws = feuille(wb, "Mode d'emploi", "Traçabilité de la mise à niveau — TP MEM", "Positionnement (cours 2) → évaluations formatives (cours 2 à 4) → évaluation sommative (cours 4) → remédiation. Preuve Qualiopi : indicateurs 8 (positionnement) et 11 (évaluation des acquis).", ["Étape", "Quand", "Onglet", "Ce que je saisis"], [28, 22, 26, 80], premiere=True)
for i, row in enumerate([
    ("1. Stagiaires", "Cours 1", "Stagiaires", "Un code par stagiaire (S01…). Nom et prénom : seulement si nécessaire (minimisation RGPD)."),
    ("2. Positionnement", "Cours 2, 10h15", "Positionnement", "Niveau de 0 à 3 par domaine : 0 pas commencé, 1 pas encore, 2 avec aide, 3 seul."),
    ("3. Formatives", "Cours 2, 3 et 4", "Formatives", "Scores des quiz et mini-cas ; sauvegarde vérifiée (Oui / Non) à chaque cours."),
    ("4. Sommative", "Cours 4, 14h45", "Sommative", "Points par domaine. Le classeur calcule les % et le statut (Acquis si 70 % ou plus)."),
    ("5. Remédiation", "Cours 5 et 6", "Remédiation", "Pour chaque domaine non acquis : action, binôme, date de réévaluation, résultat."),
    ("6. Synthèse", "Après le cours 4", "Synthèse", "Rien à saisir : tableau de bord du groupe (pour le bilan et l'audit)."),
    ("Conservation", "—", "—", "Données personnelles : accès réservé au formateur et à l'organisme ; durée fixée par l'organisme dans son registre des traitements.")], 5):
    for j, v in enumerate(row, 1): ws.cell(i, j, v)
    ligne(ws, i, 4, i % 2 == 0)
try:
    img = XLImage("/home/user/Training/web/pilotage/src/logo_yeba.png"); img.width, img.height = 104, 89; ws.add_image(img, "E1")
except Exception:
    pass

# ---- Stagiaires
ws = feuille(wb, "Stagiaires", "Liste des stagiaires", "Code obligatoire ; nom et prénom facultatifs. Le binôme d'entraide est fixé après le positionnement.", ["Code", "Nom", "Prénom", "Entreprise d'accueil", "Binôme d'entraide (code)", "Aménagement prévu (oui / non)"], [12, 24, 22, 32, 24, 26])
dv_on = DataValidation(type="list", formula1='"Oui,Non"', allow_blank=True); ws.add_data_validation(dv_on)
for k in range(N):
    r = 5 + k; ws.cell(r, 1, f"S{k + 1:02d}"); ligne(ws, r, 6, k % 2 == 1); dv_on.add(ws.cell(r, 6))

def code_nom(ws, r, k):
    ws.cell(r, 1, f"=Stagiaires!A{5 + k}"); ws.cell(r, 2, f'=IF(Stagiaires!B{5 + k}="","",Stagiaires!B{5 + k}&" "&Stagiaires!C{5 + k})')

# ---- Positionnement
DOM = ["Word", "Excel", "PowerPoint", "Messagerie", "Sauvegarde", "IA"]
ws = feuille(wb, "Positionnement", "Positionnement numérique — cours 2 (évaluation diagnostique)", "0 = pas commencé · 1 = pas encore · 2 = avec aide · 3 = seul. Un domaine à 0 ou 1 = priorité de la mise à niveau.", ["Code", "Stagiaire"] + DOM + ["Moyenne /3", "Domaines prioritaires"], [11, 26, 13, 13, 16, 16, 16, 11, 14, 36])
dv03 = DataValidation(type="whole", operator="between", formula1="0", formula2="3", allow_blank=True, showErrorMessage=True, error="Saisir 0, 1, 2 ou 3"); ws.add_data_validation(dv03)
for k in range(N):
    r = 5 + k; code_nom(ws, r, k)
    for j in range(len(DOM)): dv03.add(ws.cell(r, 3 + j))
    ws.cell(r, 9, f'=IF(COUNT(C{r}:H{r})=0,"",ROUND(AVERAGE(C{r}:H{r}),1))')
    ws.cell(r, 10, "=" + "&".join([f'IF(AND({c}{r}<>"",{c}{r}<2),"{d} ","")' for c, d in zip("CDEFGH", DOM)]))
    ligne(ws, r, 10, k % 2 == 1)
ws.conditional_formatting.add(f"C5:H{4 + N}", CellIsRule(operator="lessThan", formula=["2"], fill=ROUGE))
ws.conditional_formatting.add(f"C5:H{4 + N}", CellIsRule(operator="equal", formula=["3"], fill=VERT))

# ---- Formatives
FORM = [("C2 Quiz /10", 10), ("C2 Sauvegarde vérifiée", None), ("C3 Sauvegarde vérifiée", None), ("C3 Page DP Word /5", 5), ("C3 Mini-cas Excel /5", 5), ("C4 Sauvegarde vérifiée", None), ("C4 Mini-oral /3", 3), ("C4 Demande IA conforme", None)]
ws = feuille(wb, "Formatives", "Évaluations formatives — cours 2 à 4", "Elles servent à progresser, pas à sanctionner. Une case « Non » = on refait avec le binôme au cours suivant.", ["Code", "Stagiaire"] + [f[0] for f in FORM] + ["Remarques"], [11, 26] + [15] * len(FORM) + [34])
dv_on2 = DataValidation(type="list", formula1='"Oui,Non"', allow_blank=True); ws.add_data_validation(dv_on2)
for k in range(N):
    r = 5 + k; code_nom(ws, r, k)
    for j, (lib, mx) in enumerate(FORM):
        c = ws.cell(r, 3 + j)
        if mx is None: dv_on2.add(c)
        else:
            dv = DataValidation(type="decimal", operator="between", formula1="0", formula2=str(mx), allow_blank=True, showErrorMessage=True, error=f"Note entre 0 et {mx}"); ws.add_data_validation(dv); dv.add(c)
    ligne(ws, r, 3 + len(FORM), k % 2 == 1)
ws.conditional_formatting.add(f"C5:{ws.cell(4 + N, 2 + len(FORM)).coordinate}", CellIsRule(operator="equal", formula=['"Non"'], fill=ROUGE))

# ---- Sommative
SOM = [("Word", 20), ("Excel", 25), ("PowerPoint", 20), ("Sauvegarde", 20), ("IA", 15)]
ent = ["Code", "Stagiaire"] + [f"{d} /{m}" for d, m in SOM] + ["Total /100"] + [f"{d} %" for d, _ in SOM] + ["Statut global", "Domaines à remédier"]
ws = feuille(wb, "Sommative", "Évaluation sommative de mise à niveau — cours 4 (60 minutes)", "Seuil d'acquisition : 70 % par domaine. Mêmes consignes, même durée et même barème pour tous.", ent, [11, 26] + [12] * 5 + [12] + [11] * 5 + [17, 34])
for k in range(N):
    r = 5 + k; code_nom(ws, r, k)
    for j, (d, m) in enumerate(SOM):
        c = ws.cell(r, 3 + j); dv = DataValidation(type="decimal", operator="between", formula1="0", formula2=str(m), allow_blank=True, showErrorMessage=True, error=f"Points entre 0 et {m}"); ws.add_data_validation(dv); dv.add(c)
        pc = ws.cell(r, 9 + j); col = c.column_letter
        pc.value = f'=IF({col}{r}="","",{col}{r}/{m})'; pc.number_format = "0%"
    ws.cell(r, 8, f'=IF(COUNT(C{r}:G{r})=0,"",SUM(C{r}:G{r}))')
    ws.cell(r, 14, f'=IF(COUNT(C{r}:G{r})<5,"À compléter",IF(COUNTIF(I{r}:M{r},"<0,7")=0,"Acquis","Remédiation"))'.replace("<0,7", "<0.7"))
    ws.cell(r, 15, "=" + "&".join([f'IF(AND({c}{r}<>"",{c}{r}<0.7),"{d} ","")' for c, (d, _) in zip("IJKLM", SOM)]))
    ligne(ws, r, 15, k % 2 == 1)
ws.conditional_formatting.add(f"I5:M{4 + N}", FormulaRule(formula=['AND(I5<>"",I5<0.7)'], fill=ROUGE))
ws.conditional_formatting.add(f"I5:M{4 + N}", FormulaRule(formula=['AND(I5<>"",I5>=0.7)'], fill=VERT))
ws.conditional_formatting.add(f"N5:N{4 + N}", CellIsRule(operator="equal", formula=['"Remédiation"'], fill=ORANGE))
ws.conditional_formatting.add(f"N5:N{4 + N}", CellIsRule(operator="equal", formula=['"Acquis"'], fill=VERT))

# ---- Remédiation
ws = feuille(wb, "Remédiation", "Plan de remédiation — cours 5 et suivants", "Une ligne par domaine non acquis. Réévaluation sur un exercice équivalent ; le résultat ferme la boucle (preuve de suivi).", ["Code", "Domaine", "Action prévue", "Binôme / appui", "Date de réévaluation", "Résultat", "Commentaire"], [11, 18, 44, 20, 18, 16, 34])
dvd = DataValidation(type="list", formula1='"' + ",".join(d for d, _ in SOM) + '"', allow_blank=True); ws.add_data_validation(dvd)
dvr = DataValidation(type="list", formula1='"Acquis,Encore en cours"', allow_blank=True); ws.add_data_validation(dvr)
for k in range(24):
    r = 5 + k; ligne(ws, r, 7, k % 2 == 1); dvd.add(ws.cell(r, 2)); dvr.add(ws.cell(r, 6)); ws.cell(r, 5).number_format = "dd/mm/yyyy"

# ---- Synthèse
ws = feuille(wb, "Synthèse", "Synthèse du groupe", "Tableau de bord pour le bilan de mise à niveau, le donneur d'ordre et l'audit Qualiopi.", ["Indicateur", "Valeur"], [60, 20])
rows = [("Stagiaires évalués (sommative complète)", f'=COUNTIF(Sommative!N5:N{4 + N},"Acquis")+COUNTIF(Sommative!N5:N{4 + N},"Remédiation")'),
        ("Stagiaires « Acquis » sur les 5 domaines", f'=COUNTIF(Sommative!N5:N{4 + N},"Acquis")'),
        ("Stagiaires en remédiation", f'=COUNTIF(Sommative!N5:N{4 + N},"Remédiation")'),
        ("Taux d'acquisition global", '=IF(B5=0,"",B6/B5)'),
        ("Moyenne du groupe /100", f'=IF(COUNT(Sommative!H5:H{4 + N})=0,"",ROUND(AVERAGE(Sommative!H5:H{4 + N}),1))')]
rows += [(f"Domaine {d} : % de stagiaires au seuil", f'=IF(COUNT(Sommative!{c}5:{c}{4 + N})=0,"",COUNTIF(Sommative!{c}5:{c}{4 + N},">=0.7")/COUNT(Sommative!{c}5:{c}{4 + N}))') for c, (d, _) in zip("IJKLM", SOM)]
rows += [("Moyenne du positionnement initial /3", f'=IF(COUNT(Positionnement!I5:I{4 + N})=0,"",ROUND(AVERAGE(Positionnement!I5:I{4 + N}),1))'),
         ("Remédiations closes « Acquis »", '=COUNTIF(Remédiation!F5:F28,"Acquis")')]
for i, (lib, f) in enumerate(rows):
    r = 5 + i; ws.cell(r, 1, lib); ws.cell(r, 2, f); ligne(ws, r, 2, i % 2 == 1)
    if "%" in lib or "Taux" in lib: ws.cell(r, 2).number_format = "0%"
wb.save(sys.argv[1]); print("ok", sys.argv[1])
