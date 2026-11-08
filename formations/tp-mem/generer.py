"""Génère, pour chaque lundi : PowerPoint, ressource apprenant, grille critériée,
quiz (apprenant + corrigé), déroulé pédagogique ; puis le journal pédagogique.

    python generer.py            # tous les jours
    python generer.py 1 3        # seulement J1 et J3
"""
import importlib
import os
import subprocess
import sys

from aides import e, tableau
from moteur_pptx import Deck

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, "sortie")
TRANSITIONS = os.path.join(ICI, "..", "..", ".claude", "skills", "yeba-powerpoint", "scripts", "transitions.py")

CSS = """
body { font-family: Arial, Helvetica, sans-serif; font-size: 13pt; line-height: 1.5; color: #111;
       text-align: left; margin: 0; }
h1 { font-size: 24pt; color: #0B3D4A; margin: 0 0 4mm; line-height: 1.2; }
h2 { font-size: 18pt; color: #0B3D4A; border-bottom: 3px solid #E0A800; padding-bottom: 2mm;
     margin: 9mm 0 4mm; page-break-after: avoid; }
h3 { font-size: 15pt; color: #0B3D4A; margin: 6mm 0 2mm; page-break-after: avoid; }
p, li { margin: 0 0 2.5mm; }
.couv { background: #102A33; color: #fff; padding: 14mm 12mm; border-radius: 4mm; margin-bottom: 8mm; }
.couv h1 { color: #FFC845; font-size: 28pt; }
.couv .st { font-size: 16pt; color: #fff; font-weight: bold; }
.couv .meta { color: #7FE0D0; font-size: 13pt; margin-top: 4mm; }
.schema { margin: 5mm 0; page-break-inside: avoid; }
figcaption { font-size: 11.5pt; color: #333; margin-top: 2mm; font-style: normal; }
.flux { display: flex; align-items: stretch; gap: 2mm; }
.etape { flex: 1; background: #E8F4F6; border: 2px solid #0B3D4A; border-radius: 3mm; padding: 3mm;
         display: flex; flex-direction: column; gap: 1mm; font-size: 11.5pt; }
.etape b { font-size: 12.5pt; color: #0B3D4A; }
.etape .num { background: #0B3D4A; color: #fff; width: 8mm; height: 8mm; border-radius: 50%;
              display: flex; align-items: center; justify-content: center; font-weight: bold; }
.fl { display: flex; align-items: center; font-size: 18pt; color: #0B3D4A; }
.cartes { display: grid; gap: 3mm; }
.cartes.c2 { grid-template-columns: 1fr 1fr; } .cartes.c3 { grid-template-columns: 1fr 1fr 1fr; }
.cartes.c4 { grid-template-columns: 1fr 1fr 1fr 1fr; }
.carte { background: #F4F6F8; border-left: 5px solid #0B3D4A; border-radius: 2mm; padding: 3mm;
         display: flex; flex-direction: column; gap: 1mm; font-size: 11.5pt; }
.carte b { color: #0B3D4A; font-size: 12.5pt; }
.enc { border-radius: 3mm; padding: 3mm 5mm; margin: 4mm 0; page-break-inside: avoid; border: 2px solid; }
.enc .et { font-weight: bold; margin-bottom: 1mm; font-size: 13pt; }
.retenir { background: #FFF6D6; border-color: #B88700; } .ex { background: #E6F7F3; border-color: #157A68; }
.piege { background: #FDECEC; border-color: #B3261E; } .loi { background: #EEF0FF; border-color: #3B4CB8; }
.jury { background: #F1F1F1; border-color: #444; } .astuce { background: #EAF5FF; border-color: #1C5D99; }
.def { background: #F7F1FF; border-color: #6A3FB0; }
table { border-collapse: collapse; width: 100%; margin: 3mm 0; font-size: 11.5pt; page-break-inside: auto; }
th { background: #0B3D4A; color: #fff; text-align: left; padding: 2mm; }
td { border: 1px solid #8A9AA0; padding: 2mm; vertical-align: top; }
tr { page-break-inside: avoid; }
.pyr { display: flex; flex-direction: column; align-items: center; gap: 1.5mm; }
.niv { background: #0B3D4A; color: #fff; text-align: center; padding: 2.5mm; border-radius: 2mm; font-size: 11.5pt; }
.niv b { color: #FFC845; }
.mat-wrap { display: flex; gap: 2mm; align-items: center; }
.axe-y { writing-mode: vertical-rl; transform: rotate(180deg); font-weight: bold; color: #0B3D4A; }
.axe-x { text-align: center; font-weight: bold; color: #0B3D4A; margin-top: 1mm; }
.mat { display: grid; grid-template-columns: 1fr 1fr; gap: 2mm; }
.case { background: #E8F4F6; border: 2px solid #0B3D4A; border-radius: 2mm; padding: 3mm; font-size: 11.5pt;
        display: flex; flex-direction: column; }
.case b { color: #0B3D4A; }
.q { page-break-inside: avoid; margin: 0 0 5mm; padding: 3mm 4mm; border: 1.5px solid #8A9AA0; border-radius: 2mm; }
.q .choix { list-style: none; padding-left: 2mm; }
.q .choix li::before { content: "☐  "; }
.rep { background: #E6F7F3; border-left: 5px solid #157A68; padding: 2mm 3mm; margin-top: 2mm; }
.niveaux td { width: 18%; } .niveaux td:first-child { width: 28%; }
.champ { border: 1.5px solid #8A9AA0; min-height: 14mm; border-radius: 2mm; margin: 1mm 0 4mm; }
.petit { font-size: 11pt; color: #333; }
.saut { page-break-before: always; }
.der td:first-child { white-space: nowrap; }
"""


def page(titre, corps, paysage=False):
    o = ' data-orientation="paysage"' if paysage else ""
    taille = "@page { size: A4 landscape; }" if paysage else "@page { size: A4; }"
    return (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{e(titre)}</title>'
            f'<style>{taille}{CSS}</style></head><body{o}>{corps}</body></html>')


def entete(J, quoi):
    return (f'<div class="couv"><div class="meta">TP Manager d’établissement marchand (MEM) · Préparation aux activités-types</div>'
            f'<h1>{e(quoi)}</h1><div class="st">{e(J["titre"])}</div>'
            f'<div class="meta">{e(J["date"])} · 8 h 00 – 12 h 00 / 13 h 00 – 16 h 00 · 7 heures</div></div>')


def objectifs_html(J):
    lis = "".join(f"<li><b>{e(n)}</b> — {e(o)}</li>" for n, o in J["objectifs"])
    return (f'<h2>Objectifs de la journée</h2><p><b>Objectif général :</b> {e(J["objectif_general"])}</p>'
            f'<p>À la fin de la journée, vous serez capable de :</p><ul>{lis}</ul>'
            f'<p class="petit"><b>Lien avec le référentiel (REAC TP-00136 v09) :</b> {e(J["lien_reac"])}</p>')


def ressource(J):
    corps = entete(J, "Ressource apprenant") + objectifs_html(J)
    sommaire = "".join(f"<li>{e(t)}</li>" for t, _ in J["ressource"])
    corps += f"<h2>Sommaire</h2><ol>{sommaire}</ol>"
    for t, h in J["ressource"]:
        corps += f"<h2>{e(t)}</h2>{h}"
    if J.get("sources"):
        corps += "<h2>Sources</h2><ul>" + "".join(f"<li class='petit'>{s}</li>" for s in J["sources"]) + "</ul>"
    return page(f"J{J['num']} Ressource apprenant", corps)


def grille(J):
    g = J["grille"]
    corps = entete(J, "Grille critériée d’évaluation")
    corps += (f'<p><b>Situation évaluée :</b> {e(g["situation"])}</p>'
              '<p><b>Nom / prénom :</b> ………………………………………… &nbsp; <b>Date :</b> ……………… &nbsp; <b>Évaluateur :</b> ………………………</p>'
              '<p class="petit">Barème : chaque critère est noté de 0 à 4 (0 = non observé · 1 = non acquis · 2 = en cours · 3 = acquis · 4 = maîtrisé). Total sur 20. '
              'Seuil de réussite conseillé : 12/20 et aucun critère à 0.</p>')
    lignes = []
    for i, c in enumerate(g["criteres"], 1):
        ind = "<br>".join("• " + e(x) for x in c["indicateurs"])
        niv = [e(x) for x in c["niveaux"]]
        lignes.append([f"<b>{i}. {e(c['critere'])}</b><br><span class='petit'>{ind}</span>"] + niv + ["/4"])
    corps += tableau(["Critère et indicateurs", "1 · Non acquis", "2 · En cours", "3 · Acquis", "4 · Maîtrisé", "Note"], lignes, "niveaux")
    corps += ('<p><b>Total :</b> ……… / 20</p><p><b>Points forts :</b></p><div class="champ"></div>'
              '<p><b>Axes de progrès :</b></p><div class="champ"></div>'
              '<p><b>Auto-évaluation de l’apprenant (ce que je retiens / ce que je dois retravailler) :</b></p><div class="champ"></div>')
    return page(f"J{J['num']} Grille critériée", corps, paysage=True)


def quiz(J, corrige):
    corps = entete(J, "Quiz de fin de journée — " + ("CORRIGÉ formateur" if corrige else "version apprenant"))
    if not corrige:
        corps += "<p><b>Nom / prénom :</b> ………………………………………… &nbsp; Durée : 15 minutes. Une seule bonne réponse par question, sauf mention contraire.</p>"
    lettres = "ABCD"
    score = 0
    for i, q in enumerate(J["quiz"], 1):
        ch = "".join(f"<li>{lettres[k]}. {e(c)}</li>" for k, c in enumerate(q["choix"]))
        bloc = f'<div class="q"><p><b>Question {i}.</b> {e(q["q"])}</p><ul class="choix">{ch}</ul>'
        if corrige:
            rep = q["rep"] if isinstance(q["rep"], list) else [q["rep"]]
            bloc += (f'<div class="rep"><b>Réponse : {", ".join(lettres[r] for r in rep)}</b> — {e(q["explication"])}</div>')
        bloc += "</div>"
        corps += bloc
        score += 1
    corps += f"<p><b>Score :</b> ……… / {score}</p>"
    return page(f"J{J['num']} Quiz {'corrige' if corrige else 'apprenant'}", corps)


def deroule_table(J):
    lignes = []
    for d in J["deroule"]:
        lignes.append([f"<b>{e(d[0])}</b>", f"<b>{e(d[1])}</b><br><span class='petit'>{e(d[2])}</span>", e(d[3]),
                       e(d[4]), e(d[5]), e(d[6])])
    return tableau(["Horaire", "Séquence · objectif (niveau Bloom)", "Contenu et activités", "Méthode · mode (Bruner)",
                    "Supports", "Évaluation"], lignes, "der")


def deroule(J):
    corps = entete(J, "Déroulé pédagogique minute par minute")
    corps += objectifs_html(J)
    corps += (f"<p><b>Public :</b> {e(J.get('public', 'Groupe TP MEM, niveau 5, en début de parcours.'))}</p>"
              f"<p><b>Prérequis :</b> {e(J['prerequis'])}</p>"
              f"<p><b>Matériel :</b> {e(J['materiel'])}</p>"
              f"<p><b>Progression (spirale de Bruner) :</b> {e(J['progression'])}</p>")
    corps += "<h2>Déroulé</h2>" + deroule_table(J)
    corps += ("<h2>Adaptations accessibilité (à ajuster selon les besoins déclarés)</h2><ul>"
              "<li>Support projeté en 32 pt minimum, fort contraste, mots-clés ; ressource en Arial 13 pt, interligne 1,5, alignée à gauche.</li>"
              "<li>Envoyer le .pptx et la ressource la veille aux apprenants concernés (lecture zoomée, synthèse vocale).</li>"
              "<li>Consignes données à l’oral ET à l’écrit ; reformulation par un apprenant.</li>"
              "<li>Temps majoré (+ 1/3) pour le quiz si un aménagement est prévu ; quiz lisible à l’oral.</li>"
              "<li>Placement : proche de l’écran pour la malvoyance, face au formateur pour la lecture labiale.</li></ul>")
    return page(f"J{J['num']} Deroule pedagogique", corps, paysage=True)


def pptx(J, dossier):
    d = Deck(f"TP MEM · {J['titre']}", J["date"])
    for s in J["slides"]:
        d.ajouter(s)
    brut = os.path.join(dossier, "_brut.pptx")
    final = os.path.join(dossier, f"J{J['num']}_Support_formateur.pptx")
    d.enregistrer(brut)
    n = len(J["slides"])
    forts = [f"{i+1}:prisme" for i, s in enumerate(J["slides"]) if s["type"] == "section"][:3]
    args = [sys.executable, TRANSITIONS, brut, final, "--defaut", "fondu"]
    for f in forts:
        args += ["--diapo", f]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout, r.stderr)
        os.replace(brut, final)
    else:
        os.remove(brut)
    return final, n


def generer(num):
    J = importlib.import_module(f"contenus.j{num}").J
    dossier = os.path.join(SORTIE, f"J{num}_{J['date_court']}")
    os.makedirs(dossier, exist_ok=True)
    if J.get("fichiers"):
        J["fichiers"](dossier)
    f, n = pptx(J, dossier)
    print("PPTX", f, n, "diapositives")
    paires = []
    for nom, html in [("Ressource_apprenant", ressource(J)), ("Grille_criteriee", grille(J)),
                      ("Quiz_apprenant", quiz(J, False)), ("Quiz_corrige", quiz(J, True)),
                      ("Deroule_pedagogique", deroule(J))]:
        h = os.path.join(dossier, f"J{num}_{nom}.html")
        with open(h, "w", encoding="utf-8") as fh:
            fh.write(html)
        paires += [h, h[:-5] + ".pdf"]
    subprocess.run(["node", os.path.join(ICI, "rendu_pdf.js")] + paires, check=True)
    for h in paires[::2]:
        os.remove(h)
    return J


if __name__ == "__main__":
    nums = [int(x) for x in sys.argv[1:]] or [1, 2, 3, 4, 5, 6]
    sys.path.insert(0, ICI)
    for k in nums:
        generer(k)
