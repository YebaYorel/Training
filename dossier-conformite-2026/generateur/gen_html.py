"""Documents mis en page en HTML puis imprimés en PDF par Chromium (même méthode que le livret Marilyn).

- LIEU-01 : fiche « Votre lieu de formation » (A4), à présenter aux financeurs et aux stagiaires.
- LIV-MEM / LIV-RPMS : livrets d'accueil A5 (lecture écran) et A4 paysage (impression en livret plié).
"""
import html
import json
import re
import subprocess
import tempfile
from pathlib import Path

from pypdf import PageObject, PdfReader, PdfWriter, Transformation

import lieu as L
from calendrier import MOIS, PROMOTIONS, fmt, fmt_court, periodes, planifier, session_examen
from lib import HORAIRES, ORGANISME, RACINE, SORTIE
from titres import DUREE_JOUR, MEM, RPMS, heures, heures_centre

O, H = ORGANISME, HORAIRES
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
FONTS = RACINE / "assets" / "fonts"
LOGO_CLAIR = RACINE / "assets" / "logo" / "logo_yeba_fond_clair_1000.png"
LOGO_BLEU = RACINE / "assets" / "logo" / "logo_yeba_fond_bleu_transparent.png"
DOCS_OFFICIELS = RACINE / "sources" / "airtable_documents_officiels.json"
e = html.escape

CSS_BASE = f"""
@font-face {{ font-family: 'Montserrat'; src: url('file://{FONTS}/Montserrat-latin.woff2') format('woff2'); font-weight: 100 900; }}
@font-face {{ font-family: 'Inter'; src: url('file://{FONTS}/Inter-Regular.otf'); font-weight: 400; }}
@font-face {{ font-family: 'Inter'; src: url('file://{FONTS}/Inter-Medium.otf'); font-weight: 500; }}
@font-face {{ font-family: 'Inter'; src: url('file://{FONTS}/Inter-SemiBold.otf'); font-weight: 600; }}
@font-face {{ font-family: 'Inter'; src: url('file://{FONTS}/Inter-Bold.otf'); font-weight: 700; }}
:root {{ --bleu: #1B3A6B; --or: #C9A84C; --noir: #121212; --gris: #5A5F6A; --fond: #F7F7F5; --bleu-clair: #E8EEF7; }}
* {{ box-sizing: border-box; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ margin: 0; font-family: 'Inter', Arial, sans-serif; color: var(--noir); line-height: 1.35; hyphens: none; overflow-wrap: normal; }}
h1, h2, h3, .titre {{ font-family: 'Montserrat', Arial, sans-serif; color: var(--bleu); }}
table {{ border-collapse: collapse; width: 100%; }}
th {{ background: var(--bleu); color: #fff; text-align: left; font-weight: 600; }}
tr:nth-child(even) td {{ background: var(--bleu-clair); }}
td, th {{ vertical-align: top; }}
td:first-child {{ font-weight: 600; color: var(--bleu); }}
.encadre {{ background: var(--bleu-clair); border-left: 4px solid var(--or); padding: 8px 12px; margin: 8px 0; }}
.badge {{ display: inline-block; min-width: 2.2em; padding: 1px 7px; border-radius: 10px; font-weight: 700; text-align: center; }}
.citalis {{ background: var(--bleu); color: #fff; }}
.carjaune {{ background: var(--or); color: var(--noir); }}
.note {{ color: var(--gris); }}
ul {{ padding-left: 1.2em; margin: 4px 0; }}
li {{ margin: 2px 0; }}
"""


def _chrome(html_txt, pdf_out):
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "doc.html"
        src.write_text(html_txt, encoding="utf-8")
        pdf_out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        "--allow-file-access-from-files", f"--print-to-pdf={pdf_out}", f"file://{src}"],
                       check=True, capture_output=True, timeout=180)
    return pdf_out


def _textes_pages(pdf):
    out = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
    return out.split("\f")


def imposer_livret(pdf_a5, pdf_a4):
    """Imposition en livret : feuilles A4 paysage, recto-verso, pliées au centre."""
    r = PdfReader(str(pdf_a5))
    n = len(r.pages)
    assert n % 4 == 0, n
    w = float(r.pages[0].mediabox.width)
    h = float(r.pages[0].mediabox.height)
    out = PdfWriter()
    for i in range(n // 4):
        for gauche, droite in ((n - 2 * i, 2 * i + 1), (2 * i + 2, n - 2 * i - 1)):
            face = PageObject.create_blank_page(width=2 * w, height=h)
            face.merge_transformed_page(r.pages[gauche - 1], Transformation())
            face.merge_transformed_page(r.pages[droite - 1], Transformation().translate(tx=w, ty=0))
            out.add_page(face)
    with open(pdf_a4, "wb") as f:
        out.write(f)
    return pdf_a4


def _table(entetes, lignes, classes=None):
    th = "".join(f"<th>{e(x)}</th>" for x in entetes)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in l) + "</tr>" for l in lignes)
    return f"<table class='{classes or ''}'><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>"


def _badge(ligne, reseau):
    cls = "carjaune" if reseau == "Car Jaune" else "citalis"
    return " ".join(f"<span class='badge {cls}'>{e(x.strip())}</span>" for x in ligne.split(","))


def _bus_html():
    lignes = [[e(arret) + f"<br><span class='note'>{e(pos)}</span>", _badge(l, res), e(res), e(dest)] for arret, pos, l, res, dest in L.BUS]
    return _table(["Arrêt", "Lignes", "Réseau", "Direction"], lignes, "bus")


def _repas_html(liste):
    lignes = []
    for nom, ou, typ, prix, acces, rem, ok in liste:
        v = "" if ok else " <span class='note'>(à vérifier)</span>"
        lignes.append([f"{e(nom)}<br><span class='note'>{e(ou)}</span>", f"{e(typ)}<br><span class='note'>{e(rem)}</span>{v}",
                       f"<b>{e(prix)}</b>", e(acces)])
    return _table(["Où", "Quoi", "Prix", "Accès"], lignes, "repas")


def _bloc_marque():
    return (f"<b>{O['nom']}</b> — {O['dirigeant']}, entrepreneur individuel (EI), directeur · {O['siege_court']} · "
            f"Tél. {O['tel']} · {O['mail']} · SIRET {O['siret']} · {O['nda_mention']} · Certification Qualiopi n° {O['qualiopi']} "
            f"({O['qualiopi_categories']}) — {O['certificateur']}. Référent handicap : {O['dirigeant']}. "
            "Document conçu avec l'assistance d'un système d'IA générative (règlement (UE) 2024/1689, art. 50), vérifié et validé par un humain.")


# --------------------------------------------------------------------------- LIEU-01
def fiche_lieu():
    tuiles = "".join(f"<div class='tuile'><div class='t'>{e(t)}</div><div>{e(d)}</div></div>" for t, d in L.ATOUTS)
    css = CSS_BASE + """
    @page { size: A4; margin: 0; }
    body { font-size: 10.5pt; }
    .page { width: 210mm; height: 297mm; position: relative; overflow: hidden; break-after: page; }
    .page:last-child { break-after: auto; }
    .bandeau { background: var(--bleu); color: #fff; padding: 12mm 14mm 9mm; display: flex; align-items: center; gap: 10mm; border-bottom: 3mm solid var(--or); }
    .bandeau img { height: 30mm; }
    .bandeau h1 { color: #fff; font-size: 24pt; margin: 0; line-height: 1.1; }
    .bandeau .sous { color: var(--or); font-family: 'Montserrat'; font-weight: 600; font-size: 13pt; margin-top: 3mm; }
    .corps { padding: 7mm 14mm 0; }
    h2 { font-size: 14pt; margin: 6mm 0 2.5mm; padding-bottom: 1.5mm; border-bottom: 1.2mm solid var(--or); }
    .adresse { display: flex; gap: 6mm; align-items: stretch; }
    .carte { flex: 1; border: 0.4mm solid var(--bleu); border-radius: 3mm; padding: 4mm 5mm; }
    .carte .t { font-family: 'Montserrat'; font-weight: 700; color: var(--bleu); font-size: 12pt; margin-bottom: 1.5mm; }
    .tuiles { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm; flex: 1.3; }
    .tuile { background: var(--bleu-clair); border-top: 1.2mm solid var(--or); border-radius: 2mm; padding: 2.5mm 3.5mm; font-size: 9.5pt; }
    .tuile .t { font-family: 'Montserrat'; font-weight: 700; color: var(--bleu); font-size: 10pt; }
    table { font-size: 9.5pt; } td, th { padding: 2mm 2.5mm; }
    .deux { display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; }
    .pied { position: absolute; bottom: 0; left: 0; right: 0; background: var(--bleu); color: #fff; font-size: 7pt; padding: 3mm 14mm; line-height: 1.35; }
    .pied b { color: var(--or); }
    .num { position: absolute; bottom: 14mm; right: 14mm; color: var(--gris); font-size: 8pt; }
    """
    adresse = "<br>".join(e(x) for x in L.ADRESSE)
    p1 = f"""
    <div class='page'>
      <div class='bandeau'><img src='file://{LOGO_BLEU}' alt='Logo YEBA FORMATIONS'>
        <div><h1>Votre lieu de formation</h1><div class='sous'>{e(L.NOM)} · Technor · Saint-Denis</div></div></div>
      <div class='corps'>
        <div class='adresse'>
          <div class='carte'><div class='t'>Adresse</div>{adresse}<br><span class='note'>{e(L.SITE)}</span>
            <div class='t' style='margin-top:3mm'>Horaires de formation</div>{e(H['journee'])}<br>Pauses {e(H['pauses'])}<br>Déjeuner 12 h 00 – 13 h 00</div>
          <div class='tuiles'>{tuiles}</div>
        </div>
        <h2>Venir en bus</h2>
        {_bus_html()}
        <p class='note'>Arrêt le plus proche : <b>Parc Technor</b>. Plans et horaires : citalis.re et carjaune.re.</p>
        <h2>Venir en voiture ou en avion</h2>
        <ul>{''.join(f'<li>{e(x)}</li>' for x in L.VOITURE)}</ul>
      </div>
      <div class='num'>1 / 2</div>
      <div class='pied'>{_bloc_marque()}</div>
    </div>"""
    p2 = f"""
    <div class='page'>
      <div class='corps' style='padding-top:12mm'>
        <h2 style='margin-top:0'>Où manger le midi — à pied</h2>
        {_repas_html(L.REPAS_A_PIED)}
        <h2>Pour un repas assis — à quelques minutes en voiture</h2>
        {_repas_html(L.REPAS_EN_VOITURE)}
        <div class='encadre'><b>Nos conseils pour la pause de 12 h à 13 h</b><ul>{''.join(f'<li>{e(x)}</li>' for x in L.CONSEILS)}</ul></div>
        <div class='deux'>
          <div><h2>Sur place</h2><ul>{''.join(f'<li>{e(x)}</li>' for x in L.EQUIPEMENTS)}</ul></div>
          <div><h2>Accessibilité</h2><ul>{''.join(f'<li>{e(x)}</li>' for x in L.ACCESSIBILITE)}</ul>
            <p>Besoin d'un aménagement ? Contactez le référent handicap, {e(O['dirigeant'])}, au {e(O['tel'])} : aucun diagnostic n'est demandé.</p></div>
        </div>
        <p class='note'>{e(L.VERIF)}</p>
      </div>
      <div class='num'>2 / 2</div>
      <div class='pied'>{_bloc_marque()}</div>
    </div>"""
    doc = f"<!doctype html><html lang='fr'><head><meta charset='utf-8'><title>Votre lieu de formation</title><style>{css}</style></head><body>{p1}{p2}</body></html>"
    return _chrome(doc, SORTIE / "06_Organisme" / "LIEU-01_Votre_lieu_de_formation.pdf")


# --------------------------------------------------------------------------- Livrets
def _ri_officiel():
    docs = {d["ref"]: d for d in json.loads(DOCS_OFFICIELS.read_text(encoding="utf-8"))}
    texte = docs["YEBA-DOC-04"]["contenu"].split("ACCUSÉ DE RÉCEPTION")[0]
    out = []
    for ligne in texte.split("\n")[4:]:
        ligne = ligne.strip()
        if not ligne:
            continue
        if re.match(r"^(TITRE|Article)", ligne):
            out.append(f"<h3>{e(ligne)}</h3>")
        else:
            out.append(f"<p>{e(ligne)}</p>")
    return "\n".join(out)


def _sections_livret(t):
    code = t["code"]
    jours, _ = planifier(code)
    s1, s2 = session_examen(code)
    pers = periodes(code)
    mods = {m["code"]: m for m in t["modules"]}
    S = []

    def sec(titre, corps, saut=True):
        S.append((titre, corps, saut))

    sec("Bienvenue", f"""
      <p>Vous entrez en formation pour préparer le <b>{e(t['intitule'].lower())}</b>, un titre de <b>niveau 5</b> délivré par le ministère du Travail.</p>
      <p>Pendant environ six mois, vous allez <b>alterner le centre et l'entreprise</b> : {heures_centre(t)} heures avec nous, {t['pae']} heures sur le terrain.
      Les dossiers que vous présenterez au jury se construiront à partir de ce que vous vivrez en entreprise.</p>
      <p>Ici, pas de cours magistral : des cas réunionnais, des jeux, des mises en situation, et un module sur l'intelligence artificielle que vous utiliserez dès demain.</p>
      <p>Lisez ce livret avant votre premier jour et gardez-le : il vous accompagnera toute l'année.</p>
      <p>Je me réjouis de vous accueillir.<br><b>{e(O['dirigeant'])}</b><br>Directeur de YEBA FORMATIONS, formateur</p>""")
    sec("Vos interlocuteurs", f"""
      <p><b>YEBA FORMATIONS</b> est un organisme de formation réunionnais, créé en 2021, spécialisé en vente, management, relation client et intelligence artificielle.
      Il est <b>certifié Qualiopi</b> (n° {e(O['qualiopi'])}).</p>
      {_table(['Rôle', 'Interlocuteur'], [['Formateur', e(O['dirigeant'])], ['Référent pédagogique', e(O['dirigeant'])], ['Référent handicap', e(O['dirigeant'])],
             ['Suivi administratif', e(O['dirigeant'])], ['Vos délégués', 'Élus entre la 20e et la 40e heure'],
             ['Si un fait concerne le directeur', 'Défenseur des droits ou DEETS de La Réunion']])}
      <div class='encadre'><b>Contact</b><br>Tél. : <b>{e(O['tel'])}</b><br>E-mail : <b>{e(O['mail'])}</b></div>""")
    sec("La formation en bref", _table(["Élément", "Détail"], [
        ["Titre", f"{e(t['intitule'])} — {e(t['rncp'])}, niveau 5"],
        ["Public", e(t["public"])],
        ["Durée", f"{heures_centre(t)} h en centre + {t['pae']} h en entreprise"],
        ["Dates", f"du {e(fmt(jours[0][0]))} au {e(fmt(jours[-1][0]))}"],
        ["Examen", f"semaine du {fmt_court(s1)} (à confirmer)"],
        ["Horaires", f"{e(H['journee'])} ; pauses {e(H['pauses'])} ; déjeuner 12 h – 13 h"],
        ["Lieu", "Secrétariat Center, Immeuble Rodrigues 2, 7 rue Henri Cornu, Parc Technor, Saint-Denis"],
        ["Groupe", "10 stagiaires"],
    ]))
    obj = "".join(f"<h3>{e(c)} — {e(lib)}</h3><ul>" + "".join(f"<li>{e(m['intitule'])}</li>" for m in t["modules"] if m["bloc"] == c) + "</ul>"
                  for c, bc, lib, ep in t["blocs"])
    sec("Ce que vous saurez faire", f"<p>À la fin du parcours, vous serez capable de :</p>{obj}"
        "<div class='encadre'>En plus du titre : <b>l'intelligence artificielle au service du métier</b>, utilisée de façon sûre et conforme.</div>")
    frise = "".join(
        f"<div class='etape {'centre' if l == 'Centre' else 'ent'}'><div class='d'>{fmt_court(a)} → {fmt_court(b)}</div>"
        f"<div class='l'>{'Au centre' if l == 'Centre' else 'En entreprise'} · {nb * DUREE_JOUR} h</div>"
        f"<div>{e(', '.join(mods[c]['intitule'] for c in ms)) if ms else 'Mise en pratique avec votre tuteur'}</div></div>"
        for l, a, b, nb, ms in pers)
    frise += (f"<div class='etape exam'><div class='d'>Semaine du {fmt_court(s1)}</div><div class='l'>Examen</div>"
              "<div>Session de validation du titre (date à confirmer)</div></div>")
    sec("Votre année en un coup d'œil", f"<div class='frise'>{frise}</div>")
    par_mois = {}
    for d, lieu_, m, *_ in jours:
        cle = (d.year, d.month)
        par_mois.setdefault(cle, {"c": 0, "e": 0, "m": []})
        if lieu_ == "Centre":
            par_mois[cle]["c"] += 1
            if m["code"] not in par_mois[cle]["m"]:
                par_mois[cle]["m"].append(m["code"])
        else:
            par_mois[cle]["e"] += 1
    lignes = [[f"{MOIS[mo - 1].capitalize()} {a}", f"{v['c']} j" if v["c"] else "—", f"{v['e']} j" if v["e"] else "—",
               e(", ".join(mods[c]["intitule"] for c in v["m"])) or "Entreprise"] for (a, mo), v in sorted(par_mois.items())]
    sec("Le calendrier mois par mois", _table(["Mois", "Centre", "Entreprise", "Au programme"], lignes)
        + "<p class='note'>Jours fériés et fermeture de fin d'année déjà retirés. Le détail jour par jour vous est remis séparément.</p>")
    sec("Le titre et l'examen", _table(["Bloc", "Comment il est évalué"], [[f"{c}<br><span class='note'>{e(lib)}</span>", e(ep)] for c, bc, lib, ep in t["blocs"]])
        + f"<p><b>Durée de l'épreuve :</b> {e(t['session'])}.</p><p><b>À préparer avant l'examen :</b></p><ul>"
        + "".join(f"<li>{e(p)}</li>" for p in t["productions"] if "VÉRIFIER" not in p) + "</ul>")
    sec("La période en entreprise", f"""
      <p>Elle est <b>obligatoire</b> pour passer l'examen : <b>{t['pae']} heures minimum</b>.</p>
      <ul><li>Nous vous aidons à trouver votre structure d'accueil.</li>
      <li>Une convention est signée avant le premier jour.</li>
      <li>Votre tuteur vous confie des activités liées au titre.</li>
      <li>Nous appelons ou rencontrons votre tuteur à mi-période.</li>
      <li>Vous recueillez les éléments de vos dossiers d'examen, sans aucun nom de client ni de salarié.</li>
      <li>Une attestation vous est remise le dernier jour : gardez-la, le jury la demande.</li></ul>""")
    sec("Méthodes pédagogiques", """<ul>
      <li><b>Pratique d'abord</b> : études de cas réunionnais, jeux de rôle, ateliers, défis en équipe.</li>
      <li><b>Projet fil rouge</b> relié à votre période en entreprise.</li>
      <li><b>Diaporama accessible</b> : mots-clés, très grands caractères, fort contraste.</li>
      <li><b>D'abord en binôme, puis en groupe</b> : personne ne joue devant le groupe sans s'être entraîné.</li>
      <li><b>Supports numériques</b> remis après chaque module ; version en 16 points sur demande.</li></ul>""")
    sec("Évaluation et suivi", _table(["Quand ?", "Comment et pourquoi ?"], [
        ["Avant", "Positionnement : connaître votre point de départ et adapter le parcours"],
        ["Chaque module", "Évaluation en cours de formation : le jury en tient compte"],
        ["Mi-parcours", "Entretien individuel de bilan"],
        ["Avant l'examen", "Épreuves blanches avec des professionnels"],
        ["Fin", "Questionnaire de satisfaction"],
        ["À 3 et 6 mois", "Questionnaires de suivi et d'insertion"]]))
    sec("Documents remis", """<p><b>Avant l'entrée</b></p><ul><li>La convocation, le programme et ce livret</li>
      <li>Le règlement intérieur et son avenant, la politique de confidentialité, la charte IA</li>
      <li>La convention ou le contrat de formation</li></ul>
      <p><b>Pendant</b></p><ul><li>Les conventions de période en entreprise</li><li>Les attestations mensuelles de présence</li></ul>
      <p><b>À la fin</b></p><ul><li>L'attestation de fin de formation (code du travail, art. L.6353-1)</li>
      <li>Le certificat de réalisation, transmis au financeur</li></ul>""")
    sec("Règles de vie", _table(["Règle", "Ce qui est attendu"], [
        ["Ponctualité", "Arriver à l'heure ; signer soi-même la feuille de présence, matin et après-midi"],
        ["Absence, retard", "Prévenir avant 8 h 30 ; justificatif sous 48 heures"],
        ["Téléphone", "En mode silencieux ; utilisé seulement pour une activité demandée"],
        ["Respect", "Bienveillance, écoute, aucun propos discriminant"],
        ["Confidentialité", "Ce qui est dit en formation reste en formation"],
        ["Photos, vidéos", "Interdites sans l'accord écrit des personnes concernées"],
        ["Intelligence artificielle", "Aucune donnée personnelle dans un outil non validé ; usage déclaré dans vos dossiers d'examen"],
        ["Repas", "Dans la salle de pause, jamais dans la salle de formation"],
        ["Tabac, alcool", "Tabac, vapotage et alcool interdits"]]))
    sec("Tolérance zéro", f"""<p>YEBA FORMATIONS applique une <b>tolérance zéro</b> face aux violences sexistes et sexuelles, au harcèlement et aux discriminations.</p>
      <div class='encadre'><b>Vous êtes victime ou témoin ?</b><ul>
      <li>Parlez-en au formateur, {e(O['dirigeant'])}.</li>
      <li>Si les faits le concernent : Défenseur des droits (09 69 39 00 00) ou DEETS de La Réunion.</li>
      <li>Écoute : 3919 (gratuit, anonyme).</li><li>Danger immédiat : 17 ou 112 ; par SMS : 114.</li></ul></div>
      <p>Chaque signalement est traité sous 48 heures, en toute confidentialité. Aucune représaille contre une personne de bonne foi.</p>""")
    sec("Infos pratiques", _table(["Sujet", "Information"], [
        ["Adresse", "Secrétariat Center<br>Immeuble Rodrigues 2, 7 rue Henri Cornu<br>Parc Technor — 97490 Saint-Denis"],
        ["Arrivée", "Présentez-vous à 7 h 50 : la formation commence à 8 h 00 précises"],
        ["Horaires", f"Matin {e(H['matin'])}<br>Après-midi {e(H['apres_midi'])}"],
        ["Pauses", "10 h 00 – 10 h 15 et 15 h 00 – 15 h 15"],
        ["Déjeuner", "12 h 00 – 13 h 00 : voir « Où manger le midi »"],
        ["Sur place", "Salle de pause, boissons (environ 2 €), vidéoprojecteur, tableau"],
        ["À apporter", "De quoi écrire, une clé USB ; un ordinateur portable si vous en avez un"],
        ["Cyclone", "Alerte orange : la session est suspendue, rentrez chez vous. Alerte rouge : aucun déplacement. Report sans frais."]]))
    sec("Venir au centre", f"{_bus_html()}<p class='note'>Arrêt le plus proche : <b>Parc Technor</b>. Plans et horaires : citalis.re et carjaune.re.</p>"
        f"<h3>En voiture</h3><ul>{''.join(f'<li>{e(x)}</li>' for x in L.VOITURE)}</ul>")
    sec("Où manger le midi", f"<h3>À pied</h3>{_repas_html(L.REPAS_A_PIED)}<h3>À quelques minutes en voiture</h3>{_repas_html(L.REPAS_EN_VOITURE)}"
        f"<div class='encadre'><ul>{''.join(f'<li>{e(x)}</li>' for x in L.CONSEILS[:3])}</ul></div><p class='note'>{e(L.VERIF)}</p>")
    sec("Handicap et accessibilité", f"""<p>Vous avez un besoin particulier, lié ou non à un handicap : vue, audition, mobilité, concentration, santé ? Contactez le <b>référent handicap</b>, avant l'entrée si possible.</p>
      <div class='encadre'><b>Référent handicap</b><br>{e(O['dirigeant'])}<br>{e(O['tel'])} · {e(O['mail'])}</div>
      <ul><li>Vous n'avez <b>pas à indiquer de raison</b> ni de diagnostic : seul le besoin d'aménagement est utile.</li>
      <li><b>Le lieu</b> : entrée, parking, sièges et toilettes accessibles en fauteuil roulant.</li>
      <li><b>Sur demande</b> : supports en 16 points, place près de l'écran, pauses, rythme adapté.</li>
      <li><b>Examen</b> : des aménagements d'épreuve peuvent être demandés ; nous vous accompagnons dans la démarche.</li>
      <li>Votre information reste <b>confidentielle</b>.</li></ul>""")
    sec("Vos données (RGPD)", _table(["Données", "Pourquoi ?", "Durée"], [
        ["Identité, coordonnées, émargements, attestations", "Organiser la formation et l'examen, justifier sa réalisation auprès du financeur. Contrat et obligation légale.", "5 ans après la fin"],
        ["Évaluations, dossiers d'examen", "Mesurer les acquis, présenter le titre. Obligation légale.", "5 ans après la fin"],
        ["Questionnaires de satisfaction", "Améliorer les formations. Intérêt légitime.", "2 ans"],
        ["Besoin d'aménagement", "Adapter la formation. Seul l'aménagement est noté, jamais la raison.", "Fin du parcours"],
        ["Photo, vidéo", "Uniquement les usages que vous acceptez. Consentement.", "Durée choisie"]])
        + f"<p>Destinataires : financeur, DEETS et jury du titre, entreprise d'accueil (convention). Aucune donnée vendue. "
          f"Vos droits : écrivez à {e(O['mail'])} (réponse sous un mois) ; vous pouvez saisir la CNIL.</p>")
    sec("IA et évaluation", """<div class='encadre'><b>Transparence sur l'usage de l'IA</b><ul>
      <li>Certains supports ont été conçus avec l'aide d'une intelligence artificielle, puis vérifiés et validés par le formateur (règlement européen sur l'IA, art. 50).</li>
      <li><b>Aucune IA ne note, ne classe ni n'évalue les stagiaires</b> : la correction est faite par le formateur, et l'examen par un jury de professionnels.</li>
      <li>Aucune décision vous concernant n'est prise de façon automatisée (RGPD, art. 22).</li>
      <li>Vos dossiers d'examen restent votre travail personnel : déclarez tout usage d'un outil d'IA.</li></ul></div>""")
    sec("Avis et réclamations", f"""<ul><li>Votre avis compte : questionnaire en fin de parcours, puis à 3 et 6 mois.</li>
      <li>Réclamation : à l'oral au formateur, à vos délégués, ou par e-mail à {e(O['mail'])}.</li>
      <li><b>Accusé de réception sous 48 heures ouvrées</b>, réponse motivée sous 15 jours ouvrés.</li>
      <li>Chaque réclamation donne lieu, si elle est fondée, à une action corrective.</li></ul>""")
    sec("Aides et rémunération", """<ul>
      <li><b>Demandeur d'emploi</b> : votre conseiller France Travail vous informe du maintien de votre allocation ou d'une rémunération de formation.</li>
      <li><b>Moins de 26 ans</b> : la Mission Locale peut vous accompagner (contrat d'engagement jeune).</li>
      <li><b>Région Réunion</b> : rémunération des stagiaires de la formation professionnelle selon votre situation (à vérifier avec votre conseiller).</li>
      <li><b>Garde d'enfants</b> : renseignez-vous auprès de la CAF.</li>
      <li><b>Handicap</b> : Agefiph et Cap emploi.</li></ul>
      <div class='encadre'>Une difficulté d'argent, de transport ou de garde ? <b>Parlez-en tôt</b> : la plupart des abandons s'évitent quand on en parle à temps.</div>""")
    sec("Numéros utiles", _table(["Service", "Numéro"], [
        ["Votre formateur", e(O["tel"])], ["SAMU — urgence médicale", "15"], ["Pompiers", "18"], ["Police — gendarmerie", "17"],
        ["Numéro d'urgence européen", "112"], ["Urgence par SMS (surdité)", "114"], ["Violences Femmes Info", "3919"], ["Défenseur des droits", "09 69 39 00 00"]]))
    sec("Règlement intérieur", """<p class='note'>Avenant pour les parcours certifiants (RI-06), qui prime sur le règlement général pour les points suivants :</p><ul>
      <li><b>Horaires</b> : 8 h 00 – 12 h 00 et 13 h 00 – 16 h 00.</li>
      <li><b>Lieu</b> : Secrétariat Center ; consignes d'évacuation présentées le premier jour.</li>
      <li><b>Délégués</b> : élection obligatoire (formation de plus de 500 heures).</li>
      <li><b>Période en entreprise</b> : le règlement de l'entreprise s'applique aussi ; la règle la plus protectrice prévaut.</li>
      <li><b>Dossiers d'examen</b> : travail personnel ; usage de l'IA déclaré ; aucune donnée personnelle de l'entreprise.</li></ul>
      <p class='note'>Règlement intérieur général YEBA-DOC-04 :</p>""" + f"<div class='ri'>{_ri_officiel()}</div>")
    sec("Attestation de remise", f"""<p>Je soussigné(e), stagiaire du parcours « {e(t['intitule'])} » organisé par YEBA FORMATIONS, atteste avoir reçu, lu et compris ce livret d'accueil,
      le règlement intérieur et son avenant, et la notice d'information sur mes données, et m'engage à respecter le règlement intérieur.</p>
      <table class='sign'><tr><th>Le stagiaire</th><th>Pour YEBA FORMATIONS</th></tr>
      <tr><td>Nom et prénom :<br><br>Date :<br><br>Signature :<br><br><br></td><td>{e(O['dirigeant'])}, directeur<br><br>Date :<br><br>Signature :<br><br><br></td></tr></table>
      <p class='note'>Un exemplaire séparé est signé le premier jour et conservé au dossier (Qualiopi, indicateur 9).</p>""")
    sec("Mon plan de progression", "<p>À compléter avec le formateur au bilan de mi-parcours.</p>" + "".join(
        f"<div class='cadre'><b>{e(x)}</b></div>" for x in ("Mon projet professionnel", "Mes points forts", "Ce que je veux progresser",
                                                          "Mon entreprise d'accueil et mon tuteur", "Mes trois engagements jusqu'à l'examen")))
    return S


def livret(t, notes_extra=0, numeros=None):
    sections = _sections_livret(t)
    for _ in range(notes_extra):
        sections.append(("Mes notes", "<div class='lignes'></div>", True))
    titre_pied = f"Livret d'accueil – TP {t['court']}"
    sommaire = "".join(
        f"<div class='som'><span>{i}.&nbsp; {e(s)}</span><span class='pts'></span><span>{(numeros or {}).get(s, '')}</span></div>"
        for i, (s, _, _) in enumerate([x for x in sections if x[0] != "Mes notes"], 1))
    css = CSS_BASE + f"""
    @page {{ size: 148mm 210mm; margin: 17mm 12mm 14mm;
      @top-left {{ content: 'YEBA FORMATIONS'; font-family: Montserrat; font-weight: 700; font-size: 6.5pt; color: #1B3A6B; border-bottom: 0.3mm solid #C9A84C; vertical-align: bottom; padding-bottom: 1.5mm; }}
      @top-right {{ content: "{titre_pied.replace(chr(39), '’')}"; font-family: Inter; font-size: 6.5pt; color: #5A5F6A; border-bottom: 0.3mm solid #C9A84C; vertical-align: bottom; padding-bottom: 1.5mm; }}
      @bottom-center {{ content: counter(page); font-family: Inter; font-size: 7.5pt; color: #5A5F6A; }} }}
    @page couverture {{ margin: 0; @top-left {{ content: none; border: none; }} @top-right {{ content: none; border: none; }} @bottom-center {{ content: none; }} }}
    body {{ font-size: 10.5pt; }}
    .couv, .dos {{ page: couverture; height: 209mm; width: 148mm; overflow: hidden; text-align: center; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 14mm; break-after: page; }}
    .couv img {{ width: 62mm; }}
    .couv .k {{ font-family: Montserrat; font-weight: 600; font-size: 7.5pt; letter-spacing: 0.08em; color: var(--bleu); margin-top: 8mm; }}
    .couv h1 {{ font-size: 17pt; margin: 3mm 0; line-height: 1.2; }}
    .couv .filet {{ width: 30mm; height: 0.6mm; background: var(--or); margin: 4mm auto; }}
    .couv p {{ margin: 1mm 0; font-size: 9pt; }}
    .couv .slogan {{ font-family: Montserrat; font-weight: 300; color: var(--gris); font-size: 11pt; margin-top: 10mm; }}
    .dos {{ break-before: page; break-after: auto; font-size: 7.5pt; }}
    .dos img {{ width: 34mm; margin-bottom: 5mm; }}
    h1.s {{ font-size: 14pt; margin: 0 0 4mm; padding-bottom: 1.5mm; border-bottom: 0.6mm solid var(--or); }}
    h3 {{ font-size: 10pt; margin: 3mm 0 1.5mm; }}
    section {{ break-before: page; }}
    section.suite {{ break-before: auto; margin-top: 6mm; }}
    table {{ font-size: 9.8pt; margin: 2mm 0; }} td, th {{ padding: 1.5mm 2mm; }}
    tr {{ break-inside: avoid; }}
    .som {{ display: flex; gap: 2mm; font-size: 9.4pt; padding: 0.55mm 0; border-bottom: 0.2mm solid #d9dde6; }}
    .som .pts {{ flex: 1; }}
    .som span:last-child {{ font-weight: 700; color: var(--bleu); min-width: 6mm; text-align: right; }}
    .frise {{ border-left: 1mm solid var(--or); padding-left: 4mm; }}
    .etape {{ margin: 0 0 2mm; padding: 1.5mm 3mm; border-radius: 2mm; break-inside: avoid; font-size: 9.2pt; line-height: 1.25; }}
    .etape .d {{ font-weight: 700; color: var(--bleu); font-size: 8.5pt; }}
    .etape .l {{ font-family: Montserrat; font-weight: 700; font-size: 9.5pt; }}
    .etape.centre {{ background: var(--bleu-clair); }}
    .etape.ent {{ background: #FBF6E9; }}
    .etape.exam {{ background: var(--bleu); color: #fff; }} .etape.exam .d, .etape.exam .l {{ color: var(--or); }}
    .ri {{ font-size: 10pt; line-height: 1.3; }} .ri h3 {{ font-size: 10.5pt; margin: 2.5mm 0 0.5mm; }} .ri p {{ margin: 0 0 1.2mm; }}
    .cadre {{ border: 0.3mm solid var(--bleu); border-radius: 2mm; height: 25mm; padding: 2mm 3mm; margin: 3mm 0; }}
    .lignes {{ height: 160mm; background: repeating-linear-gradient(to bottom, transparent 0, transparent 8.5mm, #c8cdd8 8.5mm, #c8cdd8 8.8mm); }}
    table.sign td {{ height: 40mm; }}
    """
    s1, _ = session_examen(t["code"])
    jours, _ = planifier(t["code"])
    corps = [f"""<div class='couv'><img src='file://{LOGO_CLAIR}' alt='Logo YEBA FORMATIONS'>
      <div class='k'>LIVRET D'ACCUEIL DU STAGIAIRE</div><h1>{e(t['intitule'])}</h1><div class='filet'></div>
      <p>Titre professionnel de niveau 5 — {e(t['rncp'])}</p><p><b>{e(PROMOTIONS[t['code']]['nom'])}</b></p>
      <p>Du {fmt_court(jours[0][0])} au {fmt_court(jours[-1][0])} · {heures_centre(t)} h en centre + {t['pae']} h en entreprise</p>
      <p>Secrétariat Center · Parc Technor · Saint-Denis</p><p style='margin-top:8mm'>Stagiaire : ......................................................</p>
      <div class='slogan'>Apprendre, grandir, réussir</div></div>""",
             f"<section><h1 class='s'>Sommaire</h1>{sommaire}</section>"]
    n = 0
    for titre, html_corps, saut in sections:
        if titre != "Mes notes":
            n += 1
            corps.append(f"<section><h1 class='s'>{n}. {e(titre)}</h1>{html_corps}</section>")
        else:
            corps.append(f"<section><h1 class='s'>Mes notes</h1>{html_corps}</section>")
    corps.append(f"""<div class='dos'><img src='file://{LOGO_CLAIR}' alt='Logo YEBA FORMATIONS'>
      <p><b>YEBA FORMATIONS</b><br>{e(O['siege_court'])}<br>{e(O['tel'])} · {e(O['mail'])}</p>
      <p>SIRET {e(O['siret'])}<br>{e(O['nda_mention'])}<br>Certification Qualiopi n° {e(O['qualiopi'])} — {e(O['qualiopi_categories'])}.<br>Référent handicap : {e(O['dirigeant'])}.</p>
      <p>Livret remis avant l'entrée en formation (code du travail, art. L.6353-8). Version du 22 octobre 2026. Version en 16 points sur simple demande.</p>
      <p class='note'>Document conçu par le formateur avec l'assistance d'un système d'IA générative (règlement (UE) 2024/1689, art. 50), vérifié et validé par un humain.</p></div>""")
    doc = f"<!doctype html><html lang='fr'><head><meta charset='utf-8'><title>{e(titre_pied)}</title><style>{css}</style></head><body>{''.join(corps)}</body></html>"
    return doc, [s for s, _, _ in sections if s != "Mes notes"]


def livrets(t):
    dossier = SORTIE / f"02_{t['code']}"
    a5 = dossier / f"LIV-{t['code']}_Livret_accueil_A5_lecture_ecran.pdf"
    # 1er passage : pagination ; 2e : numéros du sommaire ; 3e : pages de notes pour atteindre un multiple de 4
    doc, titres = livret(t)
    _chrome(doc, a5)
    numeros = {}
    pages = _textes_pages(a5)
    for i, txt in enumerate(pages, 1):
        if i == 1 or "Sommaire" in txt:
            continue  # couverture et sommaire
        for k, s in enumerate(titres, 1):
            if s not in numeros and re.search(rf"^\s*{k}\.\s+{re.escape(s)}", txt, re.M):
                numeros[s] = i
    total = len(PdfReader(str(a5)).pages)
    extra = (-total) % 4
    doc, _ = livret(t, notes_extra=extra, numeros=numeros)
    _chrome(doc, a5)
    total = len(PdfReader(str(a5)).pages)
    if total % 4:
        doc, _ = livret(t, notes_extra=extra + (-total) % 4, numeros=numeros)
        _chrome(doc, a5)
    a4 = imposer_livret(a5, dossier / f"LIV-{t['code']}_Livret_accueil_A4_impression_livret_plie.pdf")
    manquants = [s for s in titres if s not in numeros]
    return [a5, a4], manquants


def tout():
    out = [fiche_lieu()]
    for t in (MEM, RPMS):
        f, manquants = livrets(t)
        if manquants:
            print("Sommaire incomplet", t["code"], manquants)
        out += f
    return out


if __name__ == "__main__":
    for f in tout():
        print(f.name, len(PdfReader(str(f)).pages), "pages")
