"""Documents PDF et Excel d'une formation YEBA FORMATIONS, à partir d'un module `contenu.py` privé.

Produit : ressource du stagiaire (et sa version en corps 16), évaluation de 10 questions (stagiaire et
corrigé de l'évaluateur), grille critériée, guide de l'animateur (déroulé minute par minute, notes de
chaque diapo, jeux et corrigés), cartes de jeu à imprimer, déroulé .xlsx.
Charte : site/scripts/documents-pdf/charte.py (Montserrat + Atkinson Hyperlegible, conçue pour les malvoyants).
`marque=False` : aucune trace de YEBA FORMATIONS (sous-traitance en marque blanche).
"""
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE / 'site' / 'scripts' / 'documents-pdf'))

from charte import (BLEU, BLEU_NUIT, CREME, FILET, FOND, GRIS, LEGAL, LOGO, LOGO_RATIO, NOIR, OR, OR_FOND,  # noqa: E402
                    ENTREPRISE, esc, propre, styles)
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import A4, landscape  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, KeepTogether, PageBreak, PageTemplate,  # noqa: E402
                                Paragraph, Spacer, Table, TableStyle)

BLANC = colors.white


def net(t):
    """Signes absents des polices de la charte → équivalents lisibles."""
    return (propre(t).replace('⏩', '[compressible]').replace('🔁', '(spirale)').replace('≠', 'différent de')
            .replace('▸', '•'))


class Doc(BaseDocTemplate):
    def __init__(self, chemin, c, titre_doc, paysage=False, marque=True):
        self.taille = landscape(A4) if paysage else A4
        super().__init__(str(chemin), pagesize=self.taille, leftMargin=16 * mm, rightMargin=16 * mm, topMargin=21 * mm,
                         bottomMargin=19 * mm, title=f"{titre_doc} — {c.META['titre']}",
                         author='YEBA FORMATIONS' if marque else 'Formateur', subject=c.META['ref'],
                         creator='YEBA FORMATIONS' if marque else 'Formateur')
        self.c, self.titre_doc, self.marque = c, titre_doc, marque
        cadre = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id='c', leftPadding=0, rightPadding=0)
        self.addPageTemplates([PageTemplate(id='p', frames=[cadre], onPage=self.decor)])

    def decor(self, cv, doc):
        w, h = self.taille
        cv.saveState()
        if self.marque:
            cv.drawImage(str(LOGO), 16 * mm, h - 16 * mm, width=13 * mm, height=13 * mm * LOGO_RATIO, mask='auto')
        cv.setFont('M-B', 8.5)
        cv.setFillColor(BLEU)
        cv.drawRightString(w - 16 * mm, h - 11 * mm, net(f"{self.titre_doc.upper()} · {self.c.META['ref']}"))
        cv.setFont('A', 8.5)
        cv.setFillColor(GRIS)
        cv.drawRightString(w - 16 * mm, h - 15 * mm, net(self.c.META['titre']))
        cv.setStrokeColor(OR)
        cv.setLineWidth(0.8)
        cv.line(16 * mm, h - 17.5 * mm, w - 16 * mm, h - 17.5 * mm)
        cv.setStrokeColor(FILET)
        cv.setLineWidth(0.6)
        cv.line(16 * mm, 13 * mm, w - 16 * mm, 13 * mm)
        cv.setFont('A', 7.5)
        cv.setFillColor(GRIS)
        if self.marque:
            cv.drawString(16 * mm, 9 * mm, LEGAL)
        cv.drawString(16 * mm, 5.5 * mm, net(f"Version {self.c.META['version']} du {self.c.META['date_maj']} · document conçu avec "
                                             "l'assistance d'une IA, vérifié et validé par le formateur"))
        cv.setFont('M-B', 9)
        cv.setFillColor(BLEU)
        cv.drawRightString(w - 16 * mm, 7 * mm, str(doc.page))
        cv.restoreState()


class Mise:
    """Petits constructeurs de blocs, liés à un jeu de styles (corps normal ou corps 16)."""

    def __init__(self, base, largeur):
        self.S = styles(base)
        self.L = largeur
        self.base = base

    def P(self, t, s='p'):
        return Paragraph(net(t), self.S[s])

    def puces(self, items):
        return [Paragraph(net(i), self.S['puce'], bulletText='•') for i in items]

    def h1(self, t):
        bar = Table([[self.P(esc(t), 'h1')]], colWidths=[self.L])
        bar.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, -1), 1.4, OR), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                                 ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]))
        return [CondPageBreak(45 * mm), bar, Spacer(1, 4)]

    def encart(self, titre, texte, fond=FOND, barre=BLEU):
        return KeepTogether([Spacer(1, 4), self.encart_table(titre, texte, fond, barre), Spacer(1, 6)])

    def encart_table(self, titre, texte, fond=FOND, barre=BLEU):
        """Encadré nu (sans KeepTogether) : à utiliser à l'intérieur d'un bloc déjà insécable."""
        t = Table([[self.P(f'<b>{esc(titre)}</b>', 'encart')], [self.P(texte, 'encart')]], colWidths=[self.L])
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), fond), ('LINEBEFORE', (0, 0), (0, -1), 3.5, barre),
                               ('LEFTPADDING', (0, 0), (-1, -1), 12), ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                               ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5)]))
        return t

    def tableau(self, entetes, lignes, largeurs=None, gras0=True, fonds_lignes=None):
        n = len(entetes)
        largeurs = largeurs or [1] * n
        tot = sum(largeurs)
        cel = lambda x, k: x if not isinstance(x, str) else self.P(x, 'celb' if (gras0 and k == 0) else 'cel')
        data = [[self.P(esc(h), 'tete') for h in entetes]] + [[cel(x, k) for k, x in enumerate(l)] for l in lignes]
        t = Table(data, colWidths=[self.L * x / tot for x in largeurs], repeatRows=1)
        st = [('BACKGROUND', (0, 0), (-1, 0), BLEU), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LINEBELOW', (0, 1), (-1, -1), 0.5, FILET),
              ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5), ('TOPPADDING', (0, 0), (-1, -1), 4),
              ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]
        st += [('BACKGROUND', (0, i), (-1, i), CREME) for i in range(2, len(data), 2)]
        for i, f in (fonds_lignes or {}).items():
            st.append(('BACKGROUND', (0, i), (-1, i), f))
        t.setStyle(TableStyle(st))
        return t

    def vide(self, entetes, n):
        return KeepTogether([Spacer(1, 4), self.vide_table(entetes, n), Spacer(1, 6)])

    def vide_table(self, entetes, n):
        data = [[self.P(esc(h), 'tete') for h in entetes]] + [[''] * len(entetes) for _ in range(n)]
        t = Table(data, colWidths=[self.L / len(entetes)] * len(entetes), rowHeights=[None] + [12 * mm] * n)
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), BLEU), ('GRID', (0, 1), (-1, -1), 0.6, FILET),
                               ('BOX', (0, 0), (-1, -1), 0.6, FILET)]))
        return t

    def blocs(self, liste):
        out = []
        for b in liste:
            k = b[0]
            if k == 'h1':
                out += self.h1(b[1])
            elif k == 'h2':
                out += [CondPageBreak(30 * mm), self.P(esc(b[1]), 'h2')]
            elif k == 'p':
                out.append(self.P(b[1]))
            elif k == 'puces':
                out += self.puces(b[1])
            elif k == 'table':
                out += [Spacer(1, 3), self.tableau(b[1], b[2]), Spacer(1, 6)]
            elif k == 'encart':
                out.append(self.encart(b[1], b[2]))
            elif k == 'plus':
                out.append(self.encart('Pour aller plus loin', b[1], fond=OR_FOND, barre=OR))
            elif k == 'analogie':
                out.append(self.encart("C'est comme…", f"{b[1]}<br/><b>Où l'analogie s'arrête :</b> {b[2]}", fond=FOND, barre=OR))
            elif k == 'vide':
                out.append(self.vide(b[1], b[2]))
            elif k == 'saut':
                out.append(PageBreak())
        return out

    def couverture(self, c, sous, marque=True):
        e = [Spacer(1, 18 * mm)]
        if marque:
            from reportlab.platypus import Image
            e.append(Image(str(LOGO), width=46 * mm, height=46 * mm * LOGO_RATIO))
            e.append(Spacer(1, 10 * mm))
        bloc = Table([[self.P(esc(sous.upper()), 'sur')], [self.P(esc(c.META['titre']), 'titre_blanc')],
                      [self.P(esc(c.META['sous_titre']), 'sous_or')]], colWidths=[self.L])
        bloc.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), BLEU_NUIT), ('LEFTPADDING', (0, 0), (-1, -1), 16),
                                  ('RIGHTPADDING', (0, 0), (-1, -1), 16), ('TOPPADDING', (0, 0), (0, 0), 16),
                                  ('BOTTOMPADDING', (0, -1), (-1, -1), 18), ('LINEBELOW', (0, -1), (-1, -1), 3, OR)]))
        e += [bloc, Spacer(1, 8 * mm)]
        m = c.META
        e.append(self.tableau(['Référence', 'Durée', 'Horaires', 'Version'],
                              [[m['ref'], m['duree'], m['horaires'], f"{m['version']} du {m['date_maj']}"]], gras0=False))
        e.append(Spacer(1, 4 * mm))
        e.append(self.P(f"<b>Public :</b> {esc(m['public'])}"))
        e.append(self.P(f"<b>Prérequis :</b> {esc(m['prerequis'])}"))
        if marque:
            e.append(Spacer(1, 6 * mm))
            e.append(self.P(f"{ENTREPRISE['nom']} — {ENTREPRISE['dirigeant']} · déclaration d'activité n° {ENTREPRISE['nda']} "
                            f"(cet enregistrement ne vaut pas agrément de l'État) · certification Qualiopi n° {ENTREPRISE['qualiopi']} "
                            "au titre des actions de formation.", 'petit'))
        e.append(PageBreak())
        return e


# --------------------------------------------------------------------------------------------- RESSOURCE
def ressource(c, r, chemin, base=11.4, marque=True):
    doc = Doc(chemin, c, 'Ressource du stagiaire' + (' · corps 16' if base >= 15 else ''), marque=marque)
    m = Mise(base, doc.width)
    e = m.couverture(c, 'Ressource du stagiaire', marque)
    e += m.h1('Mode d\'emploi') + m.blocs(r.MODE_EMPLOI)
    e += m.h1('Vos objectifs') + [m.P("À l'issue de la journée, vous serez capable de :")]
    e += m.puces([f"<b>{o['code']}</b> — {esc(o['enonce'])}" for o in c.OBJECTIFS])
    e.append(PageBreak())
    e += m.blocs(r.CHAPITRES)
    e.append(PageBreak())
    e += m.h1('Glossaire') + [m.tableau(['Mot', 'Définition'], [[a, b] for a, b in r.GLOSSAIRE], [1, 3])]
    e.append(PageBreak())
    e += m.h1('Annexe 1 — Modèle de fiche du registre')
    e.append(m.tableau(['Rubrique', 'À remplir'], [[x, ''] for x in ['Responsable et contact', 'Finalité', 'Personnes concernées',
                                                                      'Catégories de données', 'Destinataires', 'Transferts hors UE et garanties',
                                                                      'Durée de conservation', 'Mesures de sécurité']], [1, 2.3]))
    e += m.h1("Annexe 2 — Modèle de charte d'usage de l'IA (une page)")
    e.append(m.tableau(['Rubrique', 'Texte à compléter'], [[a, b] for a, b in r.CHARTE_MODELE], [1, 3]))
    e.append(PageBreak())
    e += m.h1('Annexe 3 — Fiche réflexe « Violation de données » (à afficher)')
    e.append(m.tableau(['Étape', 'Que faire'], [[a, b] for a, b in r.FICHE_REFLEXE], [1, 3]))
    e += m.h1("Annexe 4 — Mon plan d'action à 90 jours")
    e.append(m.vide(['Échéance', 'Action', 'Qui ?', 'Fait le'], 4))
    e += m.h1('Sources')
    e += m.puces([f"{esc(t)}{(' — ' + esc(u)) if u else ''}" for t, u in c.SOURCES])
    e.append(Spacer(1, 6))
    e.append(m.P("Ce livret a été conçu avec l'assistance d'un système d'IA générative (règlement (UE) 2024/1689, art. 50), vérifié et "
                 "validé par le formateur, qui en assume la responsabilité. Aucun système d'IA n'évalue, ne note ni ne sélectionne les "
                 "stagiaires. Version en corps 16 points et fichier lisible par lecteur d'écran sur simple demande.", 'petit'))
    doc.build(e)


# --------------------------------------------------------------------------------------------- ÉVALUATION
def quiz(c, chemin, corrige=False, marque=True):
    doc = Doc(chemin, c, 'Corrigé de l\'évaluateur' if corrige else 'Évaluation finale', marque=marque)
    m = Mise(12, doc.width)
    e = m.h1('Évaluation des acquis — 10 questions' + (' — CORRIGÉ' if corrige else ''))
    if corrige:
        e.append(m.encart('Consignes pour l\'évaluateur',
                          "Seuil de réussite : 7 sur 10. Questions 6 et 10 : réponses ouvertes, barème indiqué. La correction et la décision "
                          "sont humaines : aucun outil d'IA ne note les stagiaires (IA Act, annexe III, point 3). Reporter le score sur la "
                          "grille critériée de chaque stagiaire."))
        e.append(m.tableau(['Q', 'Objectif', 'Niveau de Bloom', 'Réponse'],
                           [[str(q['n']), q['obj'], q['bloom'], q['rep']] for q in c.QUIZ], [0.5, 1, 1.5, 2], gras0=False))
        e.append(Spacer(1, 8))
    else:
        e.append(m.vide(['Nom et prénom', 'Session (date, lieu)'], 1))
        e.append(m.P("15 minutes · seul · documents fermés. Entourez UNE réponse, ou répondez en quelques lignes pour les questions 6 et 10. "
                     "Temps majoré d'un tiers sur demande, sans justification."))
    for q in c.QUIZ:
        bloc = [m.P(f"<b>Question {q['n']}</b> <font color='#5B6678'>({q['obj']} · {q['bloom']})</font>", 'h3'), m.P(esc(q['q']))]
        if q['choix']:
            bloc += m.puces([f"<b>{'ABCD'[i]}.</b> {esc(x)}" for i, x in enumerate(q['choix'])])
        elif not corrige:
            bloc += [Spacer(1, 3), m.vide_table(['Votre réponse'], 2)]
        if corrige:
            bloc += [Spacer(1, 3), m.encart_table(f"Réponse : {q['rep']}", esc(q['expl']), fond=OR_FOND, barre=OR)]
        bloc.append(Spacer(1, 5))
        e.append(KeepTogether(bloc))
    if not corrige:
        e.append(m.vide(['Score (rempli par le formateur)', 'Signature du formateur'], 1))
    doc.build(e)


def grille(c, chemin, marque=True):
    doc = Doc(chemin, c, 'Grille critériée', paysage=True, marque=marque)
    m = Mise(10.4, doc.width)
    e = m.h1('Grille critériée d\'évaluation des acquis — une grille par stagiaire')
    e.append(m.vide(['Stagiaire', 'Session (dates, lieu)', 'Formateur', 'Évaluation finale (sur 10)'], 1))
    e.append(Spacer(1, 5))
    entetes = ['Objectif'] + c.NIVEAUX_GRILLE + ['Niveau atteint']
    lignes = [[f"{code} — {nom}"] + desc + [''] for code, nom, desc in c.GRILLE]
    t = m.tableau(entetes, lignes, [1.25, 1.35, 1.45, 1.55, 1.55, 0.85])
    e.append(t)
    e.append(Spacer(1, 6))
    e.append(m.encart('Règle de validation', c.REGLE_VALIDATION))
    e.append(m.tableau(['Décision du formateur', 'Date', 'Signature'], [['□ Objectifs atteints   □ Objectifs partiellement atteints   □ Non atteints', '', '']],
                       [3, 1, 1.4], gras0=False))
    doc.build(e)


# --------------------------------------------------------------------------------------------- GUIDE ANIMATEUR
def guide(c, chemin, marque=True):
    doc = Doc(chemin, c, "Guide de l'animateur", paysage=True, marque=marque)
    m = Mise(10, doc.width)
    e = m.h1("Guide de l'animateur — tout ce qu'il faut pour animer la journée")
    meta = c.META
    e.append(m.tableau(['Référence', 'Durée', 'Horaires', 'Pauses', 'Effectif', 'Version'],
                       [[meta['ref'], meta['duree'], meta['horaires'], meta['pauses'], meta['effectif'], f"{meta['version']} du {meta['date_maj']}"]],
                       [0.8, 0.9, 1.2, 2.6, 0.9, 0.9], gras0=False))
    e.append(Spacer(1, 6))
    e.append(m.P(f"<b>Public :</b> {esc(meta['public'])} <b>Prérequis :</b> {esc(meta['prerequis'])} <b>Matériel :</b> {esc(meta['materiel'])}"))
    e += m.h1('1. Objectifs opérationnels (Mager) et tableau de Bloom')
    e.append(m.tableau(['Code', 'À l\'issue de la formation, le stagiaire sera capable de…', 'Condition', 'Critère de réussite', 'Bloom', 'Connaissance'],
                       [[o['code'], o['enonce'], o['condition'], o['critere'], o['bloom'], o['connaissance']] for o in c.OBJECTIFS],
                       [0.45, 3, 1.6, 1.8, 0.8, 1]))
    niveaux = ['Mémoriser', 'Comprendre', 'Appliquer', 'Analyser', 'Évaluer', 'Créer']
    types = ['Factuelle', 'Conceptuelle', 'Procédurale', 'Métacognitive']
    e.append(Spacer(1, 6))
    e.append(m.tableau(['Connaissance'] + niveaux, [[t] + [c.BLOOM_TABLE.get((t, n), '') for n in niveaux] for t in types]))
    nb = sum(1 for o in c.OBJECTIFS if o['bloom'] in ('Appliquer', 'Analyser', 'Évaluer', 'Créer'))
    e.append(m.P(f"Règle YEBA : au moins 50 % des objectifs au niveau « Appliquer » ou au-dessus. Ici : {nb} sur {len(c.OBJECTIFS)}.", 'petit'))
    e += m.h1('2. Alignement pédagogique (Biggs) : chaque objectif a une activité ET une évaluation')
    e.append(m.tableau(['Objectif', 'Niveau', 'Activité qui l\'entraîne', 'Évaluation qui le mesure'],
                       [[o['code'], o['bloom'], o['activite'], o['evaluation']] for o in c.OBJECTIFS], [0.6, 0.8, 3, 2.4]))
    e += m.h1('3. Progression en spirale (Bruner)')
    e.append(m.tableau(['Demi-journée', 'Horaires', 'Séquence', 'Objectifs', 'Tour de spirale'], [list(x) for x in c.PROGRESSION], [0.8, 0.9, 2, 0.7, 2.6]))
    e.append(Spacer(1, 6))
    e.append(m.tableau(['Notion', 'Enactif (agir)', 'Iconique (voir)', 'Symbolique (texte)', 'Tours de spirale', 'Étayage', 'Désétayage'],
                       [list(x) for x in c.BRUNER], [1.1, 1.3, 1.3, 1.1, 1.6, 1.2, 1.2]))
    e.append(PageBreak())
    e += m.h1('4. Déroulé minute par minute')
    lignes, fonds = [], {}
    for i, (deb, dur, seq, obj, meth, form, stag, sup, trace) in enumerate(c.DEROULE, start=1):
        h, mi = map(int, deb.split(':'))
        fin = h * 60 + mi + dur
        horaire = f"{deb.replace(':', 'h')}<br/>{fin // 60:02d}h{fin % 60:02d}"
        lignes.append([horaire, f"{dur} min", seq, obj, meth, form, stag, sup, trace])
        if seq in ('PAUSE', 'DÉJEUNER'):
            fonds[i] = OR_FOND
    e.append(m.tableau(['Horaire', 'Durée', 'Séquence', 'Obj.', 'Méthode', 'Formateur', 'Stagiaires', 'Supports', 'Trace / évaluation'],
                       lignes, [0.62, 0.55, 1.3, 0.62, 0.95, 2.1, 1.7, 1.1, 1.2], fonds_lignes=fonds))
    total = sum(d[1] for d in c.DEROULE if d[2] != 'DÉJEUNER')
    e.append(m.P(f"Contrôle : {total} minutes de formation, pauses de 15 minutes comprises, soit {total / 60:g} heures ; déjeuner hors temps de formation.", 'petit'))
    e.append(PageBreak())
    e += m.h1('5. Notes de l\'animateur, diapo par diapo')
    for i, d in enumerate(c.DIAPOS, start=1):
        titre = d.get('titre', '')
        e.append(KeepTogether([m.P(f"<b>Diapo {i} — {esc(titre)}</b>", 'h3'), m.P(esc(d.get('notes', '')))]))
    e.append(PageBreak())
    e += m.h1('6. Matériel des jeux et corrigés')
    for cle in ('boite', 'bases', 'feu', 'vrai_faux'):
        j = c.JEUX[cle]
        e.append(m.P(f"<b>{esc(j['titre'])}</b>", 'h2'))
        e.append(m.tableau(['Carte', 'Réponse', 'Explication'], [list(x) for x in j['cartes']], [2.6, 1, 2.6]))
    e.append(m.P(f"<b>{esc(c.FORMULAIRE['titre'])}</b>", 'h2'))
    e.append(m.tableau(['Champ', 'Garder ?'], [[a, 'Oui' if b else 'Non : à barrer'] for a, b in c.FORMULAIRE['champs']], [2, 1]))
    e.append(m.P('<b>La pêche aux indices</b>', 'h2'))
    for msg in c.PECHE:
        e.append(KeepTogether([m.P(f"<b>{esc(msg['titre'])}</b>", 'h3'), m.P(esc(msg['texte']).replace('\n', '<br/>')),
                               m.P('<b>Indices :</b> ' + ' · '.join(esc(x) for x in msg['indices']))]))
    e.append(m.P(esc(c.PECHE_REGLE), 'petit'))
    e.append(m.P('<b>Exercice de crise « 72 heures »</b>', 'h2'))
    e.append(m.encart('Scénario (à lire au groupe)', esc(c.CRISE['scenario'])))
    e.append(m.tableau(['Moment', 'Alerte à injecter'], [list(x) for x in c.CRISE['alertes']], [1, 3]))
    e += [Spacer(1, 4), m.P('<b>Attendus et pièges</b>', 'h3')] + m.puces([esc(x) for x in c.CRISE['attendus']])
    e += m.h1('7. Plan B, adaptations et accessibilité')
    e.append(m.tableau(['Situation', 'Réponse prévue'], [list(x) for x in c.PLAN_B], [1, 3]))
    e += [Spacer(1, 4)] + m.puces([esc(x) for x in c.ADAPTATIONS])
    e += m.h1('8. Indicateurs Qualiopi couverts et réflexes RGPD / IA Act')
    e.append(m.tableau(['Pièce', 'Indicateurs'], [
        ['Programme : objectifs, durée, prérequis, modalités, accessibilité', '1, 5, 6'],
        ['Positionnement d\'entrée', '4, 8'],
        ['Déroulé, supports, ressource', '6, 10'],
        ['Évaluation finale, grille critériée', '11'],
        ['Adaptations liées au handicap', '26'],
        ['Satisfaction à chaud et à froid, amélioration', '30, 32'],
    ], [3, 1]))
    e += m.puces(["<b>RGPD</b> : exemples fictifs uniquement ; aucune donnée réelle de stagiaire dans les supports ; besoins d'aménagement "
                  "recueillis sans diagnostic (art. 9) ; questionnaires conservés selon la politique de l'organisme.",
                  "<b>IA Act</b> : supports conçus avec l'assistance d'une IA (transparence) ; la correction et la décision de réussite "
                  "restent humaines (annexe III, point 3)."])
    e += m.h1('Sources')
    e += m.puces([f"{esc(t)}{(' — ' + esc(u)) if u else ''}" for t, u in c.SOURCES])
    doc.build(e)


# --------------------------------------------------------------------------------------------- CARTES
def cartes(c, chemin, marque=True):
    """Cartes de jeu à découper : corps 16 minimum, une carte = une case de 2 × 4 par page A4."""
    doc = Doc(chemin, c, 'Cartes de jeu à imprimer', marque=marque)
    m = Mise(16, doc.width)
    e = []
    for cle in ('boite', 'bases', 'feu', 'vrai_faux'):
        j = c.JEUX[cle]
        e += m.h1(j['titre'])
        textes = [x[0] for x in j['cartes']]
        rangs = [textes[i:i + 2] + [''] * (2 - len(textes[i:i + 2])) for i in range(0, len(textes), 2)]
        data = [[m.P(f"<b>{esc(t)}</b>", 'pc') if t else '' for t in r] for r in rangs]
        t = Table(data, colWidths=[doc.width / 2] * 2, rowHeights=[48 * mm] * len(data))
        t.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.8, FILET), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                               ('LEFTPADDING', (0, 0), (-1, -1), 10), ('RIGHTPADDING', (0, 0), (-1, -1), 10)]))
        e += [t, PageBreak()]
    e += m.h1('Les 6 affiches des bases légales (une par page en A4 paysage, ou à recopier au tableau)')
    e += m.puces(['Contrat', 'Obligation légale', 'Intérêt légitime', 'Consentement', 'Intérêts vitaux', "Mission d'intérêt public"])
    e += m.h1('Cartons VRAI / FAUX (un de chaque par stagiaire)')
    t = Table([[m.P('<b>VRAI</b>', 'pc'), m.P('<b>FAUX</b>', 'pc')]], colWidths=[doc.width / 2] * 2, rowHeights=[60 * mm])
    t.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.8, FILET), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    e.append(t)
    doc.build(e)


# --------------------------------------------------------------------------------------------- EXCEL
def deroule_xlsx(c, chemin):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = Workbook()
    ws = wb.active
    ws.title = 'Déroulé'
    ws.append([f"{c.META['ref']} — {c.META['titre']} · {c.META['duree']} · {c.META['horaires']} · version {c.META['version']} du {c.META['date_maj']}"])
    ws['A1'].font = Font(name='Montserrat', bold=True, size=13, color='1B3A6B')
    ws.append([])
    ent = ['Début', 'Fin', 'Durée (min)', 'Séquence', 'Objectif', 'Méthode', 'Activité du formateur', 'Activité des stagiaires', 'Supports', 'Trace / évaluation']
    ws.append(ent)
    for cell in ws[3]:
        cell.font = Font(bold=True, color='FFFFFF')
        cell.fill = PatternFill('solid', fgColor='1B3A6B')
        cell.alignment = Alignment(wrap_text=True, vertical='center')
    fin_ligne = Side(style='thin', color='D5DCE8')
    for deb, dur, seq, obj, meth, form, stag, sup, trace in c.DEROULE:
        h, mi = map(int, deb.split(':'))
        fin = h * 60 + mi + dur
        ws.append([deb, f"{fin // 60:02d}:{fin % 60:02d}", dur, seq, obj, meth, form, stag, sup, trace])
        r = ws.max_row
        for cell in ws[r]:
            cell.alignment = Alignment(wrap_text=True, vertical='top')
            cell.border = Border(bottom=fin_ligne)
            if seq in ('PAUSE', 'DÉJEUNER'):
                cell.fill = PatternFill('solid', fgColor='F6EFD9')
    ws.append([])
    ws.append(['', 'Total formation (min)', f'=SUMIF(D4:D{ws.max_row - 1},"<>DÉJEUNER",C4:C{ws.max_row - 1})'])
    for col, w in zip('ABCDEFGHIJ', [8, 8, 10, 30, 9, 18, 48, 40, 26, 28]):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = 'A4'
    ws.page_setup.orientation = 'landscape'
    ws.page_setup.fitToWidth = 1
    wb.save(chemin)
