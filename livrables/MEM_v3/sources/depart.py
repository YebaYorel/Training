import sys, os
from docx import Document
from docx.shared import Pt
from openpyxl import Workbook
D = sys.argv[1]
# 1. Document bancal (cours 3) : tapé n'importe comment, volontairement
d = Document()
for t in ["NOTE DE SERVICE", "", "objet : reorganisation des horaires de mise en rayon pendant les fetes", "", "A partir du 1er decembre les livraisons arrivent a 6h00.", "- equipe du matin : 6h00 - 13h00", "- equipe de l'apres midi : 13h00 - 20h00", "- renfort samedi : 9h00 - 17h00",
          "", "LES REGLES", "1) badger a l'arrivee 2) verifier les palettes 3) signaler les ruptures au manager", "", "Qui fait quoi : Marie : fruits et legumes, Paul : epicerie, Lina : boissons", "", "Merci de votre comprehension, la direction"]:
    p = d.add_paragraph(t)
    for r in p.runs: r.font.size = Pt(11); r.font.name = "Times New Roman"
d.save(os.path.join(D, "Cours3_document_bancal.docx"))
# 2. Procédure brute (sommative)
d = Document()
for t in ["Procedure d'ouverture de caisse", "Avant l'ouverture", "Recuperer le fond de caisse aupres du responsable", "Compter le fond de caisse devant le responsable", "Signer la feuille de fond de caisse", "A l'ouverture", "Allumer le terminal", "Se connecter avec son code personnel", "Verifier le TPE avec une transaction test", "En cas de probleme",
          "Prevenir le manager de caisse", "Qui Quoi Quand", "Hote de caisse Compte le fond Avant ouverture", "Manager de caisse Valide le fond Avant ouverture", "Hote de caisse Teste le TPE A l'ouverture"]:
    d.add_paragraph(t)
d.save(os.path.join(D, "Sommative_procedure_a_mettre_en_forme.docx"))
# 3. Ventes du rayon (cours 3)
wb = Workbook(); ws = wb.active; ws.title = "Ventes"
ws.append(["Produit", "Septembre", "Octobre", "Novembre"])
for r in [["Litchis", 320, 410, 980], ["Mangues", 860, 720, 650], ["Ananas Victoria", 540, 600, 720], ["Bananes", 1200, 1150, 1180], ["Litchis séchés", 90, 110, 260], ["Fruits de la passion", 300, 280, 310]]: ws.append(r)
wb.save(os.path.join(D, "Cours3_ventes_rayon.xlsx"))
# 4. CA par rayon d'un magasin de Saint-Louis (cours 3) — données fictives pédagogiques
wb = Workbook(); ws = wb.active; ws.title = "CA par rayon"
ws.append(["Rayon", "CA N-1 (€)", "CA N (€)"])
for r in [["Fruits et légumes", 182000, 195500], ["Épicerie", 245000, 239800], ["Boissons", 158000, 171200], ["Frais", 210500, 224300], ["Droguerie", 96000, 92400], ["Boucherie", 134000, 141900]]: ws.append(r)
ws.append(["Total", None, None]); ws["D1"] = "Évolution"; ws["E1"] = "Part du CA N"
wb.save(os.path.join(D, "Cours3_CA_rayons_Saint-Louis.xlsx"))
# 5. Données de l'évaluation sommative
wb = Workbook(); ws = wb.active; ws.title = "Résultats"
ws.append(["Rayon", "Ventes N-1 (€)", "Ventes N (€)", "Évolution", "Part des ventes N"])
for r in [["Fruits et légumes", 48200, 52100], ["Épicerie", 61300, 59800], ["Boissons", 39500, 44200], ["Frais", 55100, 57900], ["Droguerie", 24800, 23600]]: ws.append(r)
ws.append(["Total"]); ws.append(["Moyenne"])
wb.save(os.path.join(D, "Sommative_donnees_ventes.xlsx"))
print("ok")
