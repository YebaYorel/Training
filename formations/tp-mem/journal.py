"""Journal pédagogique des 6 lundis (Word modifiable + PDF) : progression, déroulés, bilans de séance à compléter."""
import importlib
import os
import subprocess
import sys

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
BLEU = RGBColor(0x0B, 0x3D, 0x4A)


def fond(cell, hexa):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hexa)
    tcPr.append(shd)


def table(doc, entetes, lignes, largeurs=None):
    t = doc.add_table(rows=1, cols=len(entetes))
    t.style = "Table Grid"
    t.autofit = False
    for i, h in enumerate(entetes):
        c = t.rows[0].cells[i]
        c.text = ""
        r = c.paragraphs[0].add_run(h)
        r.bold = True; r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF); r.font.size = Pt(10)
        fond(c, "0B3D4A")
    for l in lignes:
        cells = t.add_row().cells
        for i, v in enumerate(l):
            cells[i].text = ""
            r = cells[i].paragraphs[0].add_run(str(v)); r.font.size = Pt(10)
    if largeurs:
        for row in t.rows:
            for i, w in enumerate(largeurs):
                row.cells[i].width = Cm(w)
    return t


def titre(doc, texte, niveau):
    h = doc.add_heading(texte, niveau)
    for r in h.runs:
        r.font.color.rgb = BLEU; r.font.name = "Arial"


def main():
    jours = [importlib.import_module(f"contenus.j{n}").J for n in range(1, 7)]
    doc = Document()
    st = doc.styles["Normal"]; st.font.name = "Arial"; st.font.size = Pt(11)
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width, sec.page_height = sec.page_height, sec.page_width
    for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, m, Cm(1.5))
    doc.core_properties.author = "Formateur TP MEM"
    doc.core_properties.title = "Journal pédagogique TP MEM"

    titre(doc, "Journal pédagogique — TP Manager d’établissement marchand (MEM)", 0)
    doc.add_paragraph("Préparation aux activités-types · 6 lundis du 9 novembre au 14 décembre 2026 · "
                      "8 h 00 – 12 h 00 / 13 h 00 – 16 h 00 (7 h par jour, pauses de 10 min vers 10 h et 14 h 30) · 42 heures au total")
    doc.add_paragraph("Référentiels : REAC et RC/RE du titre professionnel MEM, TP-00136, version 09 du 10/12/2025. "
                      "Démarrage de l’activité-type 1 : 4 ou 11 janvier 2027.")
    titre(doc, "Progression pédagogique d’ensemble (spirale de Bruner)", 1)
    doc.add_paragraph("Logique : on construit d’abord la représentation du métier et de l’examen (J1), puis les outils transversaux "
                      "(bureautique J2, chiffres J3, communication J4, méthodes J5, règles J6). Chaque lundi reprend le trio "
                      "« équipe – commerce – chiffres » à un niveau plus élevé, et suit la séquence enactif → iconique → symbolique → "
                      "retour enactif.")
    table(doc, ["Date", "Thème", "Objectif général", "Activités phares (pédagogie active)"], [
        [j["date"], j["titre"], j["objectif_general"],
         " · ".join(s["titre"] for s in j["slides"] if s["type"] == "activite" and not s["titre"].startswith("Quiz"))] for j in jours],
        [3.2, 6.5, 9.5, 7.3])
    doc.add_paragraph()
    titre(doc, "Suivi global du groupe", 2)
    table(doc, ["Date", "Effectif présent (nombre)", "Moyenne du quiz / 10", "Moyenne grille / 20", "Adaptations accessibilité mises en place"],
          [[j["date"], "", "", "", ""] for j in jours], [4, 4, 4, 4, 10.5])
    doc.add_paragraph("RGPD : ce journal ne contient aucun nom d’apprenant ni donnée de santé. Les besoins d’aménagement sont suivis "
                      "nominativement par le référent handicap de l’organisme, dans son propre registre sécurisé. Conservation : "
                      "durée prévue par l’organisme pour les preuves Qualiopi (indicateurs 11 et 26 notamment).").runs[0].font.size = Pt(9)

    for j in jours:
        doc.add_page_break()
        titre(doc, f"{j['date']} — {j['titre']}", 1)
        doc.add_paragraph(f"Objectif général : {j['objectif_general']}")
        for niv, o in j["objectifs"]:
            doc.add_paragraph(f"{niv} : {o}", style="List Bullet")
        doc.add_paragraph(f"Lien avec le référentiel : {j['lien_reac']}")
        doc.add_paragraph(f"Prérequis : {j['prerequis']}")
        doc.add_paragraph(f"Matériel : {j['materiel']}")
        doc.add_paragraph(f"Progression : {j['progression']}")
        titre(doc, "Déroulé pédagogique", 2)
        table(doc, ["Horaire", "Séquence", "Objectif (Bloom)", "Contenu et activités", "Méthode · Bruner", "Supports", "Évaluation"],
              [list(d) for d in j["deroule"]], [2.4, 3.2, 3.5, 7, 3, 3.2, 3.2])
        titre(doc, "Bilan de séance (à compléter le jour même)", 2)
        table(doc, ["Rubrique", "Observations"], [
            ["Effectif présent / prévu", ""], ["Résultats du quiz (moyenne, min, max)", ""], ["Grille critériée : critères les mieux / moins réussis", ""],
            ["Ce qui a bien fonctionné", ""], ["Ce qui est à ajuster (contenu, timing, activité)", ""],
            ["Écarts au déroulé prévu et raisons", ""], ["Adaptations accessibilité réalisées", ""],
            ["Incidents, réclamations, retours des apprenants", ""], ["Suite à donner (lundi suivant, tuteurs, référent handicap)", ""]], [8, 18.5])
    chemin = os.path.join(ICI, "sortie", "Journal_pedagogique_TP_MEM.docx")
    doc.save(chemin)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", os.path.dirname(chemin), chemin],
                   capture_output=True, check=True)
    print(chemin)


if __name__ == "__main__":
    main()
