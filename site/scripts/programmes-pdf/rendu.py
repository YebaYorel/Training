"""Mise en page des programmes détaillés YEBA FORMATIONS (PDF).

Reprend la structure du programme « Emailing pro » déposé dans Airtable :
couverture, positionnement, vocabulaire, fiche synoptique, objectifs, déroulé jour par jour,
méthodes et moyens, grille critériée, suivi de la progression, quiz et corrigé, validation,
défi final, annexes. Couleurs YEBA : bleu #1B3A6B, or #C9A84C (jamais en texte sur blanc).
"""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

ICI = Path(__file__).parent
LOGO = ICI.parent.parent / 'public' / 'media' / 'logo-yeba.png'
POLICES = Path('/usr/share/fonts/truetype/liberation')
for nom, fichier in [('L', 'LiberationSans-Regular.ttf'), ('L-B', 'LiberationSans-Bold.ttf'),
                     ('L-I', 'LiberationSans-Italic.ttf'), ('L-BI', 'LiberationSans-BoldItalic.ttf')]:
    pdfmetrics.registerFont(TTFont(nom, str(POLICES / fichier)))
pdfmetrics.registerFontFamily('L', normal='L', bold='L-B', italic='L-I', boldItalic='L-BI')

BLEU = colors.HexColor('#1B3A6B')
OR = colors.HexColor('#C9A84C')
NOIR = colors.HexColor('#121212')
GRIS = colors.HexColor('#4B5563')
ENCART = colors.HexColor('#EAF1FA')
CREME = colors.HexColor('#F7F4EC')
FILET = colors.HexColor('#D5DCE8')
VIGILANCE = colors.HexColor('#FBF3DF')

S = {
    'sur': ParagraphStyle('sur', fontName='L-B', fontSize=9, textColor=BLEU, spaceAfter=10, leading=12),
    'titre': ParagraphStyle('titre', fontName='L-B', fontSize=26, leading=31, textColor=NOIR, alignment=TA_CENTER),
    'soustitre': ParagraphStyle('soustitre', fontName='L', fontSize=13, leading=17, textColor=GRIS, alignment=TA_CENTER, spaceBefore=6),
    'h1': ParagraphStyle('h1', fontName='L-B', fontSize=17, leading=21, textColor=BLEU, spaceBefore=12, spaceAfter=6),
    'h2': ParagraphStyle('h2', fontName='L-B', fontSize=12, leading=15, textColor=BLEU, spaceBefore=8, spaceAfter=4),
    'p': ParagraphStyle('p', fontName='L', fontSize=9.6, leading=13.4, textColor=NOIR, spaceAfter=5),
    'fil': ParagraphStyle('fil', fontName='L-I', fontSize=9.6, leading=13, textColor=NOIR, spaceAfter=6),
    'puce': ParagraphStyle('puce', fontName='L', fontSize=9.6, leading=13.2, textColor=NOIR, leftIndent=12, bulletIndent=2, spaceAfter=2),
    'encart': ParagraphStyle('encart', fontName='L', fontSize=9.6, leading=13.4, textColor=NOIR),
    'cel': ParagraphStyle('cel', fontName='L', fontSize=8, leading=10.2, textColor=NOIR),
    'celb': ParagraphStyle('celb', fontName='L-B', fontSize=8, leading=10.2, textColor=NOIR),
    'tete': ParagraphStyle('tete', fontName='L-B', fontSize=8, leading=10, textColor=colors.white),
    'petit': ParagraphStyle('petit', fontName='L', fontSize=8.4, leading=11, textColor=GRIS),
    'q': ParagraphStyle('q', fontName='L-B', fontSize=9.6, leading=13, textColor=NOIR, spaceBefore=6, spaceAfter=2),
    'rep': ParagraphStyle('rep', fontName='L', fontSize=9.4, leading=12.4, textColor=NOIR, leftIndent=14),
}


class Brut(str):
    """Texte déjà prêt pour Paragraph (balises autorisées)."""


def esc(t):
    return str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def P(t, s='p'):
    return Paragraph(t, S[s])


def puces(items):
    return [Paragraph(esc(i), S['puce'], bulletText='•') for i in items]


def encart(etiquette, texte, fond=ENCART, barre=BLEU):
    t = Table([[Paragraph(f'<b>{esc(etiquette)}</b> {esc(texte)}', S['encart'])]], colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), fond), ('LINEBEFORE', (0, 0), (0, -1), 3.2, barre),
        ('LEFTPADDING', (0, 0), (-1, -1), 12), ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    return KeepTogether([Spacer(1, 4), t, Spacer(1, 6)])


def tableau(entetes, lignes, largeurs, gras_col0=False, zebre=True, pause=None):
    """Tableau à en-tête bleu, lignes alternées crème (comme le modèle)."""
    total = sum(largeurs)
    larg = [170 * mm * l / total for l in largeurs]
    data = [[Paragraph(esc(h), S['tete']) for h in entetes]]
    for ligne in lignes:
        data.append([Paragraph(str(c) if isinstance(c, Brut) else esc(c), S['celb' if (gras_col0 and k == 0) else 'cel'])
                     for k, c in enumerate(ligne)])
    t = Table(data, colWidths=larg, repeatRows=1)
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), BLEU), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.4, FILET), ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5), ('TOPPADDING', (0, 0), (-1, -1), 4.2), ('BOTTOMPADDING', (0, 0), (-1, -1), 4.2),
    ]
    if zebre:
        for i in range(1, len(data)):
            if i % 2 == 0:
                style.append(('BACKGROUND', (0, i), (-1, i), CREME))
    if pause:
        for i, ligne in enumerate(lignes, start=1):
            if pause(ligne):
                style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#EEF2F8')))
    t.setStyle(TableStyle(style))
    return t


class Programme:
    def __init__(self, f):
        self.f = f

    # ---- en-tête et pied de page ----
    def _cadre(self, c, doc):
        f = self.f
        c.saveState()
        w, h = A4
        if doc.page > 1:
            c.setFont('L-B', 7.6)
            c.setFillColor(BLEU)
            c.drawString(20 * mm, h - 13 * mm, f"PROGRAMME DÉTAILLÉ  |  {f['nom'].upper()}")
            c.setStrokeColor(FILET)
            c.setLineWidth(0.6)
            c.line(20 * mm, h - 15.5 * mm, w - 20 * mm, h - 15.5 * mm)
        c.setStrokeColor(FILET)
        c.line(20 * mm, 15 * mm, w - 20 * mm, 15 * mm)
        c.setFont('L', 6.9)
        c.setFillColor(GRIS)
        c.drawString(20 * mm, 11 * mm, f"YEBA FORMATIONS — Aurélien LUMEKA EI — SIRET 814 622 262 00032 — NDA 04973676397 — Qualiopi n° 25FOR02027.1 (actions de formation)")
        c.drawString(20 * mm, 7.6 * mm, f"Réf. {f['ref']} · {f['format_court']} · version du {f['version']}")
        c.setFont('L-B', 8)
        c.drawRightString(w - 20 * mm, 9 * mm, str(doc.page))
        c.restoreState()

    def construire(self, chemin):
        f = self.f
        doc = SimpleDocTemplate(str(chemin), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=22 * mm,
                                bottomMargin=22 * mm, title=f"Programme détaillé — {f['titre']}", author='YEBA FORMATIONS',
                                subject=f"Programme de formation {f['ref']}", creator='YEBA FORMATIONS')
        doc.build(self.contenu(), onFirstPage=self._cadre, onLaterPages=self._cadre)

    # ---- sections ----
    def contenu(self):
        f = self.f
        e = []
        # Couverture
        e.append(Spacer(1, 10 * mm))
        if LOGO.exists():
            e.append(Image(str(LOGO), width=46 * mm, height=46 * mm * 443 / 520))
        e.append(Spacer(1, 10 * mm))
        e.append(P('PROGRAMME DE FORMATION', 'sur'))
        e.append(P(esc(f['nom']), 'titre'))
        e.append(P(esc(f['promesse_titre']), 'soustitre'))
        e.append(Spacer(1, 8 * mm))
        e.append(encart('PROMESSE DU MODULE', f['promesse']))
        e.append(tableau(['Format', 'Durée', 'Pédagogie', 'Validation'],
                         [[f['format_court'], f"{f['heures']} heures ({f['jours']} jour{'s' if f['jours'] > 1 else ''})", '70 % de pratique', f['validation_courte']]],
                         [1, 1, 1, 1], zebre=False))
        e.append(Spacer(1, 6))
        e.append(tableau(['Inter-entreprises', 'Intra-entreprise', 'Effectif'],
                         [[f"{f['inter']} € par jour et par stagiaire", f"{f['intra']} € par jour pour le groupe", '6 à 8 participants (minimum 6, maximum 8)']],
                         [1, 1, 1], zebre=False))
        e.append(Spacer(1, 8))
        e.append(P(f"Public : {esc(f['public_court'])}", 'petit'))
        e.append(P('Prix nets de taxe : TVA non applicable, article 293 B du code général des impôts. Horaires : 08h00–12h00 / 13h00–17h00, deux pauses de 15 minutes (10h00 et 15h00) incluses, soit 8 heures de formation par jour.', 'petit'))
        e.append(P(f"<i>Version du {f['version']} — ce programme est celui du devis ; en intra, il est ajusté aux cas réels de l'entreprise sans modifier les objectifs.</i>", 'petit'))
        e.append(PageBreak())

        n = 1
        # 1. Positionnement
        e.append(P(f'{n}. Positionnement pédagogique', 'h1')); n += 1
        e.append(encart('RECOMMANDATION', f['positionnement']['idee']))
        e.append(P(esc(f['positionnement']['intro'])))
        e += puces(f['positionnement']['points'])
        if f['positionnement'].get('vigilance'):
            e.append(encart('POINT DE VIGILANCE', f['positionnement']['vigilance'], fond=VIGILANCE, barre=OR))

        # 2. Vocabulaire
        e.append(P(f'{n}. Petit vocabulaire pour débuter', 'h1')); n += 1
        e.append(P('Les termes sont introduits au fil de la formation ; ce lexique permet de les expliquer dès leur première apparition.'))
        e.append(tableau(['Terme', 'Explication en langage courant'], f['vocabulaire'], [1, 3], gras_col0=True))

        # 3. Fiche synoptique
        e.append(P(f'{n}. Fiche synoptique', 'h1')); n += 1
        syn = [
            ['Intitulé', f['titre']],
            ['Référence', f['ref']],
            ['Durée', f"{f['heures']} heures en présentiel, sur {f['jours']} journée{'s' if f['jours'] > 1 else ''} de 8 heures (08h00–17h00, pauses de 10h00 et 15h00 incluses, pause méridienne de 12h00 à 13h00 hors temps de formation)"],
            ['Public', f['public']],
            ['Prérequis', f['prerequis']],
            ['Effectif', '6 participants minimum, 8 au maximum — en inter comme en intra'],
            ['Tarifs', f"Inter-entreprises : {f['inter']} € par jour et par stagiaire. Intra-entreprise : {f['intra']} € par jour pour le groupe. Prix nets de taxe (art. 293 B du CGI)."],
            ['Matériel du stagiaire', f['materiel']],
            ['Production attendue', f['production']],
            ['Modalité dominante', 'Démonstrations courtes, ateliers guidés sur la situation réelle du stagiaire, pratique individuelle et revue par les pairs'],
            ['Outils', f['outils']],
            ['Délai d\'accès', '15 jours ouvrés minimum entre l\'inscription et le démarrage (analyse du besoin, test de positionnement, convocation)'],
            ['Financements possibles', f['financements'] + ' — selon les critères de chaque financeur. Formation non éligible au CPF à ce jour.'],
        ]
        e.append(tableau(['Rubrique', 'Proposition'], syn, [1, 3.4], gras_col0=True))

        # 4. Objectifs
        e.append(P(f'{n}. Objectifs pédagogiques et résultats attendus', 'h1')); n += 1
        e.append(P('À la fin de la formation, le stagiaire sera capable de :'))
        e.append(tableau(['Réf.', 'Action', 'Résultat attendu', 'Preuve observable'], f['objectifs'], [0.5, 1.1, 2.6, 2.2]))

        # 5+. Déroulé
        for k, j in enumerate(f['jours_detail'], start=1):
            e.append(PageBreak())
            titre = f"{n}. Déroulé détaillé" + (f" - Jour {k}" if f['jours'] > 1 else '')
            e.append(P(titre + (f" : {esc(j['titre'])}" if j.get('titre') else ''), 'h1')); n += 1
            e.append(P(f"Fil conducteur : {esc(j['fil'])}", 'fil'))
            lignes = [[Brut(f"{esc(h)}<br/>{esc(d)}"), s, c, m, mo] for h, d, s, c, m, mo in j['lignes']]
            e.append(tableau(['Horaire', 'Séquence', 'Objectifs / contenus', 'Méthodes', 'Moyens'], lignes, [0.9, 1.2, 2.5, 1.4, 1.3],
                             pause=lambda l: str(l[1]).lower().startswith('pause')))
            if j.get('livrables'):
                e.append(Spacer(1, 6))
                e.append(encart('LIVRABLES DE LA JOURNÉE', ' · '.join(j['livrables'])))

        # Méthodes et moyens
        e.append(PageBreak())
        e.append(P(f'{n}. Méthodes et moyens pédagogiques', 'h1')); n += 1
        e += puces([
            'Pédagogie active : environ 70 % du temps en manipulation, production ou retour entre pairs ; 30 % d\'apports courts.',
            'Démonstrations courtes selon le protocole « je montre, nous faisons, vous faites ».',
            'Fil rouge : la situation réelle de chaque stagiaire ; un cas fictif réunionnais est fourni pour ne jamais bloquer.',
            'Réactivation : quiz flash, reformulation et rappel des règles en début de séquence.',
            'Différenciation : consignes à trous et démonstrations rejouables pour les débutants ; variantes et défis pour les plus avancés.',
        ] + f.get('methodes_plus', []))
        e.append(P('Moyens à prévoir', 'h2'))
        e += puces(f['moyens'])

        # Grille critériée
        e.append(P(f'{n}. Grille critériée de progression', 'h1')); n += 1
        e.append(P('Échelle commune : 0 = absent ou dangereux ; 1 = fragile ; 2 = opérationnel ; 3 = maîtrisé et justifié. La grille est remise au stagiaire dès l\'ouverture.'))
        e.append(tableau(['Critère', '0 - Non acquis', '1 - En cours', '2 - Acquis', '3 - Maîtrisé'], f['grille'], [1.3, 1, 1, 1.2, 1.2]))
        e.append(encart('SEUIL', f['seuil']))

        # Suivi
        e.append(KeepTogether([P(f'{n}. Suivi de la progression', 'h1'), tableau(['Moment', 'Outil', 'Ce qui est observé', 'Décision pédagogique'], f['suivi'], [1, 1.2, 1.5, 1.6])])); n += 1

        # Quiz
        e.append(PageBreak())
        e.append(P(f'{n}. Quiz d\'évaluation', 'h1'))
        e.append(P('Nom / prénom : ____________________________________'))
        e.append(P('Consigne : répondre individuellement. Une seule réponse sauf mention contraire. Barème : 1 point par question ; réussite à partir de 7/10.'))
        for i, (q, opts, _, _) in enumerate(f['quiz'], start=1):
            bloc = [P(f'{i}. {esc(q)}', 'q')]
            bloc += [P(esc(o), 'rep') for o in opts]
            e.append(KeepTogether(bloc))
        e.append(PageBreak())
        e.append(P('Corrigé et rétroactions', 'h1')); n += 1
        e.append(tableau(['Q', 'Réponse', 'Rétroaction'], [[i, r, rt] for i, (_, _, r, rt) in enumerate(f['quiz'], start=1)], [0.3, 0.8, 4]))

        # Validation
        e.append(P(f'{n}. Compétences acquises et modalités de validation', 'h1')); n += 1
        e.append(tableau(['Compétence validée', 'Preuve attendue', 'Modalité', 'Critère de réussite'], f['validation'], [1.4, 1.5, 1.1, 1.5]))
        e.append(P('Décision finale', 'h2'))
        e += puces([
            f"Validé : quiz ≥ 7/10, production ≥ {f['seuil_points']} et critères essentiels ({f['critiques']}) ≥ 2.",
            'Validé avec réserve : production fonctionnelle mais un élément non essentiel reste à corriger sous 7 jours.',
            'À reprendre : critère essentiel non acquis ou score inférieur au seuil ; remédiation ciblée puis nouvelle preuve.',
        ])
        e.append(encart('SUPERVISION HUMAINE', 'Aucun système d\'IA n\'évalue, ne note, ne classe ni ne sélectionne les stagiaires : la décision est arrêtée par le formateur (règlement (UE) 2024/1689, annexe III, point 3). L\'attestation de fin de formation mentionne les objectifs, la durée et les résultats de l\'évaluation des acquis.'))

        # Défi final
        e.append(P(f'{n}. Défi final - consigne stagiaire', 'h1')); n += 1
        e.append(P(esc(f['defi']['intro'])))
        for i, etape in enumerate(f['defi']['etapes'], start=1):
            e.append(Paragraph(esc(etape), S['puce'], bulletText=f'{i}.'))

        # Annexes
        e.append(PageBreak())
        for k, a in enumerate(f['annexes']):
            lettre = 'ABCDEFG'[k]
            e.append(P(f"Annexe {lettre} - {esc(a['titre'])}", 'h1'))
            if a.get('texte'):
                e.append(P(esc(a['texte'])))
            if a.get('tableau'):
                ent, lig, larg = a['tableau']
                e.append(tableau(ent, lig, larg, gras_col0=True))
            if a.get('puces'):
                e += puces(a['puces'])
            if a.get('encart'):
                e.append(encart(*a['encart']))
        lettre = 'ABCDEFG'[len(f['annexes'])]
        e.append(P(f'Annexe {lettre} - Accessibilité, RGPD et IA Act', 'h1'))
        e.append(P(esc(f['accessibilite'])))
        e += puces([
            'RGPD : seules les données nécessaires à la formation sont collectées (identité, contact professionnel, émargements, résultats) ; information remise à l\'entrée ; aucune donnée de santé n\'est demandée pour un aménagement.',
            'IA Act : les outils d\'IA utilisés en séance sont présentés comme tels (art. 50) ; la formation contribue aux mesures de maîtrise de l\'IA que l\'employeur doit prendre (art. 4).',
            'Exercices : uniquement sur des données fictives ou anonymisées ; aucun document client nominatif n\'est saisi dans un outil d\'IA.',
        ])
        e.append(P('Contact', 'h2'))
        e.append(P('Responsable pédagogique et référent handicap : Aurélien LUMEKA — 0693 32 24 45 — yebaformations@gmail.com — 9 rue Françoise Châtelain, 97490 Sainte-Clotilde, La Réunion. Contact sous 48 h ouvrées, proposition d\'aménagement sous 5 jours ouvrés.'))
        if f.get('sources'):
            e.append(P('Sources et repères', 'h2'))
            e += puces(f['sources'])
            e.append(P(f"Liens consultés le {f['version']}. Ce programme fournit des repères pédagogiques et ne remplace pas un conseil juridique adapté à l'entreprise.", 'petit'))
        return e
