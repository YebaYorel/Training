"""Classeur Excel du décorticage — paysage, gros caractères, charte graphique.

Choix d'accessibilité (public malvoyant, impression) :
* police 14 pt minimum, titres 22 pt, fort contraste (texte sombre sur fond
  clair, en-têtes blancs sur couleur primaire) ;
* orientation paysage, ajusté à la largeur d'une page, en-têtes répétés à
  chaque page imprimée, volets figés à l'écran ;
* texte renvoyé à la ligne et hauteur de ligne calculée : aucun mot coupé ;
* le logo est une image indépendante : un clic + « Suppr » suffit pour le
  retirer. Aucune signature ni mention d'outil dans le fichier.
"""

from __future__ import annotations

import datetime as dt
from collections import OrderedDict, defaultdict
from pathlib import Path

from openpyxl import Workbook
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

from .pedagogie import ETAYAGE, NIVEAUX_BLOOM
from .planification import JOURS, MOIS, fmt_duree, fmt_hm
from .programme import construire_examen, construire_programme
from .securite import ecrire_cellule, texte_cellule


class Style:
    def __init__(self, charte):
        self.c = charte
        t = charte.taille_texte
        self.police = charte.police
        self.normal = Font(name=self.police, size=t, color=charte.couleur_texte)
        self.gras = Font(name=self.police, size=t, bold=True, color=charte.couleur_texte)
        self.entete = Font(name=self.police, size=t + 1, bold=True, color="FFFFFF")
        self.titre = Font(name=self.police, size=charte.taille_titre, bold=True, color=charte.couleur_primaire)
        self.sous_titre = Font(name=self.police, size=t + 3, bold=True, color=charte.couleur_secondaire)
        self.fond_entete = PatternFill("solid", fgColor=charte.couleur_primaire)
        self.fond_clair = PatternFill("solid", fgColor=charte.couleur_claire)
        self.fond_accent = PatternFill("solid", fgColor=charte.couleur_secondaire)
        fin = Side(style="thin", color="9AA5B1")
        self.bord = Border(left=fin, right=fin, top=fin, bottom=fin)
        self.retour = Alignment(wrap_text=True, vertical="top")
        self.centre = Alignment(wrap_text=True, vertical="center", horizontal="center")


def _lignes_necessaires(texte, largeur_col: float, taille: int) -> int:
    if texte is None:
        return 1
    s = str(texte)
    # caractères par ligne ≈ largeur de colonne × 11 / taille de police (police proportionnelle)
    par_ligne = max(4.0, largeur_col * 11.0 / taille * 0.95)
    total = 0
    for morceau in s.split("\n"):
        mots = morceau.split(" ")
        lignes, courant = 1, 0
        for m in mots:
            L = len(m) + 1
            if courant + L > par_ligne and courant > 0:
                lignes += 1
                courant = L
            else:
                courant += L
        total += lignes
    return total


class Feuille:
    """Petit utilitaire pour écrire des tableaux lisibles."""

    def __init__(self, wb: Workbook, nom: str, style: Style, largeurs: list[float], titre: str = "",
                 sous_titre: str = "", ident_nom: str = ""):
        self.ws = wb.create_sheet(nom[:31])
        self.s = style
        self.largeurs = largeurs
        for i, w in enumerate(largeurs, 1):
            self.ws.column_dimensions[get_column_letter(i)].width = w
        self.ligne = 1
        ws = self.ws
        ws.sheet_view.showGridLines = False
        ws.sheet_view.zoomScale = 90
        ws.page_setup.orientation = "landscape"
        ws.page_setup.paperSize = ws.PAPERSIZE_A4
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.print_options.horizontalCentered = True
        ws.page_margins.left = ws.page_margins.right = 0.4
        ws.page_margins.top = ws.page_margins.bottom = 0.5
        ws.oddFooter.right.text = "Page &P / &N"
        ws.oddFooter.right.size = 12
        if ident_nom:
            ws.oddFooter.left.text = ident_nom.replace("&", "&&")
            ws.oddFooter.left.size = 12
        if titre:
            self.titre(titre, sous_titre)

    def titre(self, texte: str, sous_titre: str = ""):
        ws = self.ws
        fin = get_column_letter(len(self.largeurs))
        ws.merge_cells(f"A{self.ligne}:{fin}{self.ligne}")
        c = ws.cell(self.ligne, 1)
        ecrire_cellule(c, texte)
        c.font = self.s.titre
        c.alignment = Alignment(vertical="center", wrap_text=True)
        ws.row_dimensions[self.ligne].height = self.s.c.taille_titre * 2.0
        self.ligne += 1
        if sous_titre:
            ws.merge_cells(f"A{self.ligne}:{fin}{self.ligne}")
            c = ws.cell(self.ligne, 1)
            ecrire_cellule(c, sous_titre)
            c.font = self.s.sous_titre
            c.alignment = Alignment(vertical="center", wrap_text=True)
            ws.row_dimensions[self.ligne].height = (self.s.c.taille_texte + 3) * 1.8
            self.ligne += 1
        self.ligne += 1

    def entetes(self, valeurs: list[str], repeter: bool = True, figer: bool = True):
        r = self.ligne
        largeurs = self._fusion_fin(r, len(valeurs))
        for i, v in enumerate(valeurs, 1):
            c = self.ws.cell(r, i)
            ecrire_cellule(c, v)
            c.font, c.fill, c.alignment, c.border = self.s.entete, self.s.fond_entete, self.s.centre, self.s.bord
        h = max(_lignes_necessaires(v, largeurs[i - 1], self.s.c.taille_texte + 1) for i, v in enumerate(valeurs, 1))
        self.ws.row_dimensions[r].height = h * (self.s.c.taille_texte + 1) * 1.6 + 10
        if repeter:
            self.ws.print_title_rows = f"{r}:{r}"
        if figer:
            self.ws.freeze_panes = self.ws.cell(r + 1, 1)
        self.debut_tableau = r
        self.ligne += 1

    def _fusion_fin(self, r: int, nb: int) -> list[float]:
        """Si la ligne a moins de valeurs que de colonnes, la dernière cellule
        s'étend jusqu'au bord (pas de colonnes vides). Retourne les largeurs utiles."""
        largeurs = list(self.largeurs[:nb])
        if 0 < nb < len(self.largeurs):
            self.ws.merge_cells(start_row=r, start_column=nb, end_row=r, end_column=len(self.largeurs))
            largeurs[-1] = sum(self.largeurs[nb - 1:])
        return largeurs

    def rangee(self, valeurs: list, bande: bool = False, gras: bool = False, fond=None, hauteur_min: float = 0):
        r = self.ligne
        nb_lignes = 1
        largeurs = self._fusion_fin(r, len(valeurs))
        for i, v in enumerate(valeurs, 1):
            c = self.ws.cell(r, i)
            if isinstance(v, CellRichText):
                c.value = v
                texte = "".join(str(b) for b in v)
            else:
                ecrire_cellule(c, v)
                texte = v
            c.font = self.s.gras if gras else self.s.normal
            c.alignment = self.s.retour
            c.border = self.s.bord
            if fond is not None:
                c.fill = fond
            elif bande:
                c.fill = self.s.fond_clair
            nb_lignes = max(nb_lignes, _lignes_necessaires(texte, largeurs[i - 1], self.s.c.taille_texte))
        self.ws.row_dimensions[r].height = max(hauteur_min, min(409, nb_lignes * self.s.c.taille_texte * 1.42 + 8))
        self.ligne += 1
        return r

    def vide(self, n: int = 1):
        self.ligne += n

    def paragraphe(self, texte: str, police=None, fond=None):
        fin = get_column_letter(len(self.largeurs))
        r = self.ligne
        self.ws.merge_cells(f"A{r}:{fin}{r}")
        c = self.ws.cell(r, 1)
        ecrire_cellule(c, texte)
        c.font = police or self.s.normal
        c.alignment = self.s.retour
        if fond is not None:
            c.fill = fond
        n = _lignes_necessaires(texte, sum(self.largeurs) * 0.85, self.s.c.taille_texte)
        self.ws.row_dimensions[r].height = min(409, n * self.s.c.taille_texte * 1.45 + 8)
        self.ligne += 1


def _objectif_riche(style: Style, verbe: str, texte: str) -> CellRichText:
    """Verbe d'action Bloom en gras et en couleur d'accent (« mise en exergue »)."""
    t = texte_cellule(texte)
    if verbe and t.lower().startswith(verbe.lower()):
        reste = t[len(verbe):]
        debut = t[:len(verbe)]
    else:
        debut, reste = "", t
    blocs = []
    if debut:
        blocs.append(TextBlock(InlineFont(rFont=style.police, sz=style.c.taille_texte, b=True,
                                          color=style.c.couleur_secondaire), debut.upper()))
    blocs.append(TextBlock(InlineFont(rFont=style.police, sz=style.c.taille_texte, color=style.c.couleur_texte),
                           reste))
    return CellRichText(blocs)


def _ajouter_logo(ws, chemin_logo: Path, ancre: str = "A1", hauteur_px: int = 70):
    from openpyxl.drawing.image import Image as XLImage
    img = XLImage(str(chemin_logo))
    ratio = hauteur_px / max(img.height, 1)
    img.height = hauteur_px
    img.width = int(img.width * ratio)
    img.anchor = ancre
    ws.add_image(img)


# ==========================================================================
# Export principal
# ==========================================================================
def exporter_classeur(ctx, chemin: Path) -> Path:
    reac, re_, fiche, plan = ctx.reac, ctx.re, ctx.fiche, ctx.plan
    st = Style(ctx.charte)
    nom_org = ctx.identite.nom_affiche(ctx.charte)
    logo = ctx.charte.chemin_logo(ctx.base) if ctx.identite.logo_autorise() else None
    titre_formation = (fiche.intitule if fiche and fiche.intitule else f"TP {reac.intitule}").strip()
    code = fiche.code if fiche and fiche.code else (reac.code_titre or "")

    wb = Workbook()
    wb.remove(wb.active)
    # Propriétés du fichier : aucune signature d'outil
    wb.properties.creator = nom_org or ""
    wb.properties.lastModifiedBy = nom_org or ""
    wb.properties.title = f"Décorticage — {titre_formation}"
    wb.properties.description = ""
    wb.properties.keywords = ""

    total_min = sum(l["minutes"] for l in plan.lignes)

    # ------------------------------------------------------------------ Accueil
    f = Feuille(wb, "Accueil", st, [34, 40, 34, 40], ident_nom=nom_org)
    if logo:
        f.ws.row_dimensions[1].height = 60
        _ajouter_logo(f.ws, logo, "A1", 70)
        f.ligne = 2
    f.titre(f"Décorticage pédagogique — {titre_formation}",
            " • ".join(x for x in [code, f"Niveau {reac.niveau}" if reac.niveau else "", nom_org] if x))
    infos = [
        ("Durée en centre", fmt_duree(total_min)),
        ("Période", f"du {plan.lignes[0]['date']:%d/%m/%Y} au {plan.date_fin:%d/%m/%Y}" if plan.lignes else "—"),
        ("Activités types", str(len(reac.activites))),
        ("Compétences", str(len(reac.competences))),
        ("Séances", str(len(plan.seances))),
        ("Jours de formation", str(len({l['date'] for l in plan.lignes}))),
        ("REAC", f"{reac.sigle} {reac.code_titre} — millésime {reac.millesime} du {reac.date_validation}".strip()),
        ("Période en entreprise", fmt_duree(ctx.reglages.heures_entreprise * 60) if ctx.reglages.heures_entreprise else "voir Examen"),
    ]
    for i in range(0, len(infos), 2):
        ligne = []
        for k, v in infos[i:i + 2]:
            ligne += [k, v]
        r = f.rangee(ligne + [""] * (4 - len(ligne)))
        for col in (1, 3):
            f.ws.cell(r, col).font = st.gras
            f.ws.cell(r, col).fill = st.fond_clair
    f.vide()
    f.paragraphe("Sommaire (cliquer pour ouvrir)", st.sous_titre)
    sommaire = ["Décorticage", "Planning détaillé", "Planning par jour", "Synthèses", "Programme",
                "Examen simplifié", "Couverture critères", "Suivi journalier", "Préparation PowerPoint",
                "Paramètres et sources"]
    for nom in sommaire:
        r = f.ligne
        f.ws.merge_cells(f"A{r}:D{r}")
        c = f.ws.cell(r, 1)
        c.value = f"→ {nom}"
        c.hyperlink = f"#'{nom}'!A1"
        c.font = Font(name=st.police, size=st.c.taille_texte + 1, color=st.c.couleur_primaire, underline="single")
        f.ws.row_dimensions[r].height = 26
        f.ligne += 1
    f.vide()
    f.paragraphe("Légende — Taxonomie de Bloom (verbe d'action en COULEUR et MAJUSCULES dans les tableaux)",
                 st.sous_titre)
    for n, lib in NIVEAUX_BLOOM.items():
        f.rangee([f"Niveau {n}", lib, {1: "identifier, citer", 2: "expliquer, décrire", 3: "appliquer, utiliser",
                                        4: "analyser, organiser", 5: "évaluer, contrôler", 6: "élaborer, planifier"}[n]],
                 bande=n % 2 == 0)
    if plan.avertissements or ctx.alertes:
        f.vide()
        f.paragraphe("Points à vérifier", st.sous_titre)
        for a in plan.avertissements + ctx.alertes:
            f.paragraphe(f"⚠ {a}")

    # ------------------------------------------------------------- Décorticage
    larg = [24, 8, 26, 38, 14, 34, 9]
    f = Feuille(wb, "Décorticage", st, larg, f"Décorticage — {titre_formation}",
                "Activités types et compétences : termes exacts du REAC. Objectifs : verbe d'action (Bloom) + mots clés du REAC.",
                nom_org)
    f.entetes(["Activité type · Compétence (REAC)", "N°", "Étape du processus (REAC)", "Objectif pédagogique",
               "Bloom · Bruner", "Contenus (savoirs REAC)", "Durée"])
    cp_prec = None
    bande = False
    for s in plan.seances:
        for k, o in enumerate(s.objectifs):
            if s.cp != cp_prec:
                bande = not bande
                cp_prec = s.cp
            cp = reac.competence(s.cp) if s.cp else None
            contenus = "\n".join(f"• {c}" for c in o.contenus)
            if o.associes:
                contenus = ("Aussi : " + " ; ".join(o.associes) + ("\n" + contenus if contenus else ""))
            f.rangee([
                (f"AT{s.at} · CP{cp.numero} — {cp.intitule}" if k == 0 else f"AT{s.at} · CP{cp.numero}")
                if cp else (s.sequence_titre if k == 0 else "Module"),
                f"S{s.numero}",
                s.titre if k == 0 else "",
                _objectif_riche(st, o.verbe, o.texte),
                f"{o.niveau} - {NIVEAUX_BLOOM[o.niveau]}\n{o.mode.split(' (')[0]}",
                contenus,
                fmt_duree(o.minutes),
            ], bande=bande)
    f.ws.auto_filter.ref = f"A{f.debut_tableau}:{get_column_letter(len(larg))}{f.ligne - 1}"

    # ------------------------------------------------------- Planning détaillé
    larg = [18, 15, 8, 7, 29, 40, 13, 11, 13]
    f = Feuille(wb, "Planning détaillé", st, larg, f"Planning heure par heure — {titre_formation}",
                "Chaque ligne = un créneau réel (pauses exclues). Colonne « Réalisé » : liste déroulante.",
                nom_org)
    f.entetes(["Date · semaine", "Horaire", "Durée", "CP", "Séance", "Objectif pédagogique",
               "Cumul · % avancé", "Réalisé ?", "Observations"])
    dv = DataValidation(type="list", formula1='"Oui,Partiel,Non,Reporté"', allow_blank=True)
    f.ws.add_data_validation(dv)
    jour_prec = None
    bande = False
    for l in plan.lignes:
        s, o = l["seance"], l["objectif"]
        if l["date"] != jour_prec:
            bande = not bande
            jour_prec = l["date"]
        d = l["date"]
        r = f.rangee([
            f"{JOURS[d.weekday()][:3].capitalize()} {d:%d/%m/%Y}\nSem. {d.isocalendar()[1]}",
            f"{fmt_hm(l['debut'])} – {fmt_hm(l['fin'])}",
            fmt_duree(l["minutes"]), f"CP{s.cp}" if s.cp else "—",
            f"S{s.numero} — {s.titre}", _objectif_riche(st, o.verbe, o.texte + (" (suite)" if l["suite"] else "")),
            f"{fmt_duree(l['cumul'])}\n{l['pourcentage']:.0%}", "", ""], bande=bande)
        dv.add(f.ws.cell(r, 8))
    f.ws.auto_filter.ref = f"A{f.debut_tableau}:{get_column_letter(len(larg))}{f.ligne - 1}"

    # ---------------------------------------------------------- Planning par jour
    larg = [16, 12, 8, 16, 70, 12, 12]
    f = Feuille(wb, "Planning par jour", st, larg, "Séances prévues par jour", "", nom_org)
    f.entetes(["Date", "Jour", "Sem.", "Mois", "Séances et objectifs du jour", "Heures", "Cumul"])
    par_jour: "OrderedDict[dt.date, list]" = OrderedDict()
    for l in plan.lignes:
        par_jour.setdefault(l["date"], []).append(l)
    cumul = 0
    for i, (d, ls) in enumerate(par_jour.items()):
        minutes = sum(x["minutes"] for x in ls)
        cumul += minutes
        seances = OrderedDict()
        for x in ls:
            seances.setdefault(x["seance"].numero, (x["seance"], []))[1].append(x)
        texte = "\n".join(
            f"S{s.numero} — {s.titre} ({fmt_hm(xs[0]['debut'])}-{fmt_hm(xs[-1]['fin'])})"
            for s, xs in seances.values())
        f.rangee([d.strftime("%d/%m/%Y"), JOURS[d.weekday()].capitalize(), d.isocalendar()[1],
                  f"{MOIS[d.month - 1].capitalize()} {d.year}", texte, fmt_duree(minutes), fmt_duree(cumul)],
                 bande=i % 2 == 1)

    # ----------------------------------------------------------------- Synthèses
    larg = [46, 16, 16, 14, 12, 38]
    f = Feuille(wb, "Synthèses", st, larg, "Synthèses : par activité type, compétence, mois et semaine", "", nom_org)
    f.paragraphe("Par activité type et compétence", st.sous_titre)
    f.entetes(["Activité type / Compétence", "Début", "Fin", "Heures", "% du total", "Séances"], repeter=False, figer=False)
    lignes_cp = defaultdict(list)
    for l in plan.lignes:
        lignes_cp[(l["seance"].at, l["seance"].cp, l["seance"].sequence_titre if not l["seance"].cp else "")].append(l)
    for at in reac.activites:
        ls_at = [l for l in plan.lignes if l["seance"].at == at.numero]
        if ls_at:
            m = sum(l["minutes"] for l in ls_at)
            f.rangee([f"AT{at.numero} — {at.intitule}", ls_at[0]["date"].strftime("%d/%m/%Y"),
                      ls_at[-1]["date"].strftime("%d/%m/%Y"), fmt_duree(m), f"{m / total_min:.1%}",
                      str(len({l['seance'].numero for l in ls_at}))], gras=True, fond=st.fond_clair)
        for n in at.competences:
            ls = [l for l in plan.lignes if l["seance"].cp == n]
            if ls:
                m = sum(l["minutes"] for l in ls)
                f.rangee([f"   CP{n} — {reac.competence(n).intitule}", ls[0]["date"].strftime("%d/%m/%Y"),
                          ls[-1]["date"].strftime("%d/%m/%Y"), fmt_duree(m), f"{m / total_min:.1%}",
                          str(len({l['seance'].numero for l in ls}))])
    autres = [l for l in plan.lignes if not l["seance"].cp]
    if autres:
        m = sum(l["minutes"] for l in autres)
        f.rangee(["Modules transverses (accueil, ECF, DP, examen blanc, bilan)", "", "", fmt_duree(m),
                  f"{m / total_min:.1%}", str(len({l['seance'].numero for l in autres}))], gras=True, fond=st.fond_clair)
    f.rangee(["TOTAL", plan.lignes[0]["date"].strftime("%d/%m/%Y") if plan.lignes else "",
              plan.date_fin.strftime("%d/%m/%Y") if plan.date_fin else "", fmt_duree(total_min), "100 %",
              str(len(plan.seances))], gras=True, fond=st.fond_accent)
    f.vide()
    f.paragraphe("Par mois", st.sous_titre)
    f.entetes(["Mois", "Jours de formation", "Heures", "Cumul", "% avancé", "Compétences travaillées"], repeter=False, figer=False)
    mois = OrderedDict()
    for l in plan.lignes:
        mois.setdefault((l["date"].year, l["date"].month), []).append(l)
    cumul = 0
    for i, ((a, m_), ls) in enumerate(mois.items()):
        mn = sum(l["minutes"] for l in ls)
        cumul += mn
        cps = sorted({l["seance"].cp for l in ls if l["seance"].cp})
        f.rangee([f"{MOIS[m_ - 1].capitalize()} {a}", str(len({l['date'] for l in ls})), fmt_duree(mn),
                  fmt_duree(cumul), f"{cumul / total_min:.0%}", ", ".join(f"CP{c}" for c in cps) or "Modules"],
                 bande=i % 2 == 1)
    f.vide()
    f.paragraphe("Par semaine", st.sous_titre)
    f.entetes(["Semaine", "Du … au …", "Heures", "Cumul", "% avancé", "Séances"], repeter=False, figer=False)
    sem = OrderedDict()
    for l in plan.lignes:
        iso = l["date"].isocalendar()
        sem.setdefault((iso[0], iso[1]), []).append(l)
    cumul = 0
    for i, ((a, w), ls) in enumerate(sem.items()):
        mn = sum(l["minutes"] for l in ls)
        cumul += mn
        nums = sorted({l["seance"].numero for l in ls})
        f.rangee([f"S{w} — {a}", f"{ls[0]['date']:%d/%m} → {ls[-1]['date']:%d/%m}", fmt_duree(mn),
                  fmt_duree(cumul), f"{cumul / total_min:.0%}", f"S{nums[0]} à S{nums[-1]}" if len(nums) > 1 else f"S{nums[0]}"],
                 bande=i % 2 == 1)

    # ----------------------------------------------------------------- Programme
    intitule, sections = construire_programme(reac, re_, fiche, plan, ctx.reglages, ctx.tarif)
    f = Feuille(wb, "Programme", st, [30, 36, 48, 14, 12, 12], ident_nom=nom_org)
    if logo:
        f.ws.row_dimensions[1].height = 60
        _ajouter_logo(f.ws, logo, "A1", 70)
        f.ligne = 2
    f.titre(f"Programme de formation — {intitule}", nom_org)
    for sec in sections:
        f.paragraphe(sec.titre, st.sous_titre)
        for p in sec.paragraphes:
            f.paragraphe(p)
        for p in sec.puces:
            f.paragraphe(f"•  {p}")
        if sec.tableau:
            f.entetes(sec.tableau[0], repeter=False, figer=False)
            for i, row in enumerate(sec.tableau[1:]):
                f.rangee(row, bande=i % 2 == 1)
        f.vide()
    f.paragraphe(f"Mise à jour : {dt.date.today():%d/%m/%Y}")

    # --------------------------------------------------------- Examen simplifié
    ex = construire_examen(reac, re_, fiche)
    f = Feuille(wb, "Examen simplifié", st, [32, 18, 50, 52], ident_nom=nom_org)
    if logo:
        f.ws.row_dimensions[1].height = 60
        _ajouter_logo(f.ws, logo, "A1", 70)
        f.ligne = 2
    f.titre(f"L'examen en clair — {titre_formation}",
            f"Durée totale pour le candidat : {ex['duree_totale']}" if ex["duree_totale"] else "")
    f.paragraphe("PARTIE 1 — Les épreuves", st.sous_titre)
    if len(ex["partie1"]) > 1:
        f.entetes(ex["partie1"][0], repeter=False, figer=False)
        for i, row in enumerate(ex["partie1"][1:]):
            f.rangee(row, bande=i % 2 == 1)
    for c in ex["consignes"]:
        f.paragraphe(f"•  {c}")
    f.vide()
    f.paragraphe("PARTIE 2 — Ce que le jury attend, compétence par compétence", st.sous_titre)
    f.entetes(["Compétence", "Évaluée par", "Ce qu'il faut savoir faire (critères en clair)", "À préparer avant l'examen"],
              repeter=False, figer=False)
    for i, b in enumerate(ex["partie2"]):
        prod = ""
        if b["production"]:
            prod = f"Partie de document ({b['production']['pages']}) :\n" + "\n".join(
                f"• {t}" for t in b["production"]["themes"])
        f.rangee([b["cp"], "\n".join(b["epreuves"]) or "—", "\n".join(f"✔ {a}" for a in b["attendus"]), prod],
                 bande=i % 2 == 1)

    # -------------------------------------------------------- Couverture critères
    f = Feuille(wb, "Couverture critères", st, [30, 62, 40, 18],
                "Couverture des critères d'évaluation", "Chaque critère du REAC/RE est relié aux séances qui le travaillent.",
                nom_org)
    f.entetes(["Compétence", "Critère de performance / d'évaluation", "Séances", "Statut"])
    for cp in reac.competences:
        for crit in cp.criteres:
            seances = [s for s in plan.seances if any(crit in o.criteres for o in s.objectifs)]
            ecf = [s for s in plan.seances if s.type_seance == "evaluation" and not s.cp and s.at == cp.at_numero]
            couvre = ", ".join(f"S{s.numero}" for s in seances + ecf)
            f.rangee([f"CP{cp.numero} — {cp.intitule}", crit, couvre or "—", "Couvert ✔" if couvre else "À COUVRIR ✖"],
                     fond=None if couvre else st.fond_accent)

    # ---------------------------------------------------------- Suivi journalier
    larg = [14, 9, 80, 30, 18]
    f = Feuille(wb, "Suivi journalier", st, larg, "Suivi journalier — texte prêt à reprendre",
                "Le texte du jour est pré-rédigé à partir du décorticage. Ajustez seulement ce qui a changé.", nom_org)
    f.entetes(["Date", "Heures", "Ce qui a été fait aujourd'hui (pré-rédigé)", "Écarts / adaptations", "Émargement vérifié"])
    for i, (d, ls) in enumerate(par_jour.items()):
        objs = list(OrderedDict.fromkeys(x["objectif"].texte for x in ls))
        seances = list(OrderedDict.fromkeys(f"S{x['seance'].numero} « {x['seance'].titre} »" for x in ls))
        cps = sorted({x["seance"].cp for x in ls if x["seance"].cp})
        texte = (f"Séance(s) {', '.join(seances)}"
                 + (f" — {', '.join(f'CP{c}' for c in cps)}" if cps else "")
                 + ". Objectifs travaillés : " + " ; ".join(o[0].lower() + o[1:] for o in objs) + ".")
        f.rangee([d.strftime("%d/%m/%Y"), fmt_duree(sum(x["minutes"] for x in ls)), texte, "", ""], bande=i % 2 == 1)

    # ---------------------------------------------------- Préparation PowerPoint
    larg = [8, 30, 36, 40, 38]
    f = Feuille(wb, "Préparation PowerPoint", st, larg, "Trame de diaporama par séance",
                "Étayage de Bruner : la trame suit les 6 fonctions de tutelle (Wood, Bruner & Ross, 1976).", nom_org)
    f.entetes(["N°", "Titre de la séance", "Diapositives clés (mots-clés REAC)", "Déroulé (étayage brunérien)",
               "Exercices et exemples"])
    for i, s in enumerate(plan.seances):
        diapos = "\n".join(f"• {o.verbe.upper()} : {', '.join(o.mots[:4])}" for o in s.objectifs[:8])
        modes = sorted({o.mode.split(" (")[0] for o in s.objectifs})
        diapos += "\nModes : " + ", ".join(modes)
        exemple = next((o.exemple for o in s.objectifs if o.exemple), "")
        activite = next((o.activite for o in s.objectifs if o.activite), "")
        mots = list(dict.fromkeys(m for o in s.objectifs for m in o.mots))[:6]
        deroule = "\n".join([
            f"1. {ETAYAGE[0][0]} : {exemple or 'question d’accroche sur le vécu en entreprise'}",
            f"2. {ETAYAGE[1][0]} : une consigne, une tâche — « {s.objectifs[0].texte} »",
            f"3. {ETAYAGE[2][0]} : rappel de l'objectif et du critère de réussite",
            f"4. {ETAYAGE[3][0]} : {', '.join(mots)}",
            f"5. {ETAYAGE[4][0]} : binôme, aide graduée, droit à l'erreur",
            f"6. {ETAYAGE[5][0]} : {activite or 'modèle montré puis reproduit'}",
        ])
        exo = "\n".join(dict.fromkeys(x for o in s.objectifs for x in (o.activite, o.exemple) if x))
        f.rangee([f"S{s.numero}", f"{s.titre}\n({fmt_duree(s.minutes)})", diapos, deroule, exo], bande=i % 2 == 1)

    # ----------------------------------------------------- Paramètres et sources
    f = Feuille(wb, "Paramètres et sources", st, [44, 100], "Paramètres, hypothèses et sources", "", nom_org)
    f.entetes(["Paramètre", "Valeur"], repeter=False, figer=False)
    r = ctx.reglages
    params = [
        ("Durée en centre (h)", f"{r.heures_centre:g}"), ("Date de début", r.date_debut), ("Jours de centre", r.jours),
        ("Créneaux", r.creneaux), ("Pauses (exclues des heures)", r.pauses), ("Rythme d'alternance", r.rythme or "aucun"),
        ("Fermetures", r.fermetures or "aucune"), ("Jours fériés", "La Réunion (dont 20 décembre), automatiques"),
        ("Accueil / ECF par AT / DP / Productions / Examen blanc / Bilan (h)",
         f"{r.h_accueil:g} / {r.h_ecf_par_at:g} / {r.h_dossier_pro:g} / {r.h_productions:g} / "
         f"{r.h_examen_blanc:g} (0 = durée du RE) / {r.h_bilan:g}"),
        ("Pondération des compétences", r.poids_cp or "automatique (volume du REAC)"),
    ]
    for k, v in params:
        f.rangee([k, v])
    if plan.jours_exclus:
        f.rangee(["Jours exclus du calendrier", "\n".join(f"{d:%d/%m/%Y} — {m}" for d, m in plan.jours_exclus)])
    for h in ctx.hypotheses:
        f.rangee(["HYPOTHÈSE À CONFIRMER", h], fond=st.fond_accent)
    f.vide()
    f.paragraphe("Sources", st.sous_titre)
    for s in ctx.sources:
        f.paragraphe(f"•  {s}")

    wb.active = 0
    chemin.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(chemin))
    _effacer_signature_outil(chemin)
    return chemin


def _effacer_signature_outil(chemin: Path) -> None:
    """openpyxl inscrit son nom dans docProps/app.xml : on le remplace par un libellé neutre."""
    import os
    import zipfile

    tmp = chemin.with_suffix(".tmp")
    with zipfile.ZipFile(chemin) as src, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
        for info in src.infolist():
            donnees = src.read(info.filename)
            if info.filename == "docProps/app.xml":
                donnees = (b'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/'
                           b'extended-properties"><Application>Microsoft Excel</Application></Properties>')
            dst.writestr(info, donnees)
    os.replace(tmp, chemin)

