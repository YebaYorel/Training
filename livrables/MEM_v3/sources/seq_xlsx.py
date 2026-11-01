import json, sys, datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.drawing.image import Image as XLImage
data = json.load(open(sys.argv[1])); L = data["lignes"]
BLEU, OR, CLAIR = "1B3A6B", "C9AB4C", "EEF2F8"
F = Font(name="Inter", size=13); FB = Font(name="Inter", size=13, bold=True)
ENT = Font(name="Montserrat", size=13, bold=True, color="FFFFFF"); TIT = Font(name="Montserrat", size=20, bold=True, color=BLEU)
T = Side(style="thin", color="9AA5B1"); B = Border(left=T, right=T, top=T, bottom=T); RET = Alignment(wrap_text=True, vertical="top")
PHASES = {"Intégration": "FFF3DC", "Mise à niveau": "FFF3DC", "AT1": "E8EEF8", "AT3": "E5F3EA", "AT2": "F6EFD9", "ECF": "FDECEC", "Examen blanc": "FDECEC", "Révision": "EEF2F8", "Productions": "EEF2F8", "Remédiation": "EEF2F8", "Oral": "EEF2F8", "Révisions": "EEF2F8", "Clôture": "FFF3DC"}
def fond(ph):
    for k, v in PHASES.items():
        if ph.startswith(k): return PatternFill("solid", fgColor=v)
    return None
wb = Workbook(); ws = wb.active; ws.title = "Séquençage MEM"
ent = ["N°", "Date", "Mois", "Phase", "Compétence / thème", "Contenu de la session (plan de cours : grande partie → petites parties)", "Fils rouges (numérique, DP, oral)", "Évaluation", "Critères de performance REAC visés", "Épreuve préparée (RE)", "Cumul h"]
larg = [6, 13, 11, 16, 34, 70, 34, 26, 48, 24, 9]
ws["A1"] = "TP Manager d'établissement marchand — séquençage des 48 sessions (lundis, 6 h 30)"; ws["A1"].font = TIT; ws.merge_cells("A1:K1"); ws.row_dimensions[1].height = 34
ws["A2"] = "Ordre AT1 → AT3 → AT2 (la mise en situation de 4 h sur l'AT2 est préparée près de l'examen). Contenus issus du plan de cours décortiqué du REAC (logiciel Pilotage). Hypothèses : fermetures des 21 et 28/12/2026 à confirmer ; lundis fériés exclus."
ws["A2"].font = Font(name="Inter", size=12, italic=True); ws["A2"].alignment = RET; ws.merge_cells("A2:K2"); ws.row_dimensions[2].height = 36
for i, (e, w) in enumerate(zip(ent, larg), 1):
    c = ws.cell(4, i, e); c.font = ENT; c.fill = PatternFill("solid", fgColor=BLEU); c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); c.border = B
    ws.column_dimensions[c.column_letter].width = w
ws.row_dimensions[4].height = 48
MOIS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]
for k, l in enumerate(L):
    r = 5 + k; d = dt.date.fromisoformat(l["date"])
    vals = [l["n"], d, f"{MOIS[d.month - 1]} {d.year}", l["phase"], l["titre"], l["contenu"], l["fil"], l["evaluation"], "\n".join("• " + c for c in l["criteres"]), l["epreuve"], l["cumul"]]
    for i, v in enumerate(vals, 1):
        c = ws.cell(r, i, v); c.font = FB if i in (1, 5) else F; c.alignment = RET; c.border = B
        f = fond(l["phase"])
        if f: c.fill = f
    ws.cell(r, 2).number_format = "dd/mm/yyyy"
    lignes = max(len(str(l["contenu"])) // 62 + l["contenu"].count("\n") + 1, len(l["criteres"]) * 2, 2)
    ws.row_dimensions[r].height = min(409, 17 * lignes + 8)
ws.freeze_panes = "F5"; ws.auto_filter.ref = f"A4:K{4 + len(L)}"
ws.page_setup.orientation = "landscape"; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0; ws.sheet_properties.pageSetUpPr.fitToPage = True
ws.print_title_rows = "4:4"; ws.oddFooter.left.text = "YEBA FORMATIONS — séquençage MEM"; ws.oddFooter.right.text = "Page &P / &N"
try:
    img = XLImage("/home/user/Training/web/pilotage/src/logo_yeba.png"); img.width, img.height = 80, 68; ws.add_image(img, "K1")
except Exception: pass
# Synthèse par phase
s = wb.create_sheet("Synthèse")
s["A1"] = "Répartition des 312 heures"; s["A1"].font = TIT
for i, e in enumerate(["Bloc", "Sessions", "Heures", "% du total"], 1):
    c = s.cell(3, i, e); c.font = ENT; c.fill = PatternFill("solid", fgColor=BLEU); c.border = B
blocs = [("Intégration et mise à niveau", lambda p: p in ("Intégration", "Mise à niveau")), ("AT1 — Manager l'équipe (CP1 à CP4)", lambda p: p.startswith("AT1")), ("AT3 — Performance et rentabilité (CP8 à CP10)", lambda p: p.startswith("AT3")),
         ("AT2 — Dynamique commerciale (CP5 à CP7)", lambda p: p.startswith("AT2")), ("Révisions, remédiation, bilans", lambda p: p.startswith(("Révision", "Remédiation", "Révisions", "Oral", "Clôture"))),
         ("ECF (une par activité type)", lambda p: p.startswith("ECF")), ("Productions et dossier professionnel", lambda p: p.startswith("Productions")), ("Examen blanc", lambda p: p.startswith("Examen blanc"))]
for k, (lib, f) in enumerate(blocs):
    n = sum(1 for l in L if f(l["phase"])); r = 4 + k
    for i, v in enumerate([lib, n, n * 6.5, n / 48], 1):
        c = s.cell(r, i, v); c.font = F; c.border = B
    s.cell(r, 4).number_format = "0%"
r = 4 + len(blocs); s.cell(r, 1, "Total").font = FB; s.cell(r, 2, f"=SUM(B4:B{r-1})").font = FB; s.cell(r, 3, f"=SUM(C4:C{r-1})").font = FB
for col, w in zip("ABCD", [52, 12, 12, 12]): s.column_dimensions[col].width = w
s.cell(r + 2, 1, "Lundis exclus").font = FB
for k, (d, m) in enumerate(data["exclus"].items()): s.cell(r + 3 + k, 1, f"{dt.date.fromisoformat(d).strftime('%d/%m/%Y')} — {m}").font = F
wb.save(sys.argv[2]); print("ok")
