"""Programme de formation A4 — même structure pour toutes les formations (modèle « Programme Formation Détaillé »)."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, Image, KeepTogether, PageTemplate, Paragraph, Spacer,
                                Table, TableStyle)

from charte import BLEU, BLEU_NUIT, CREME, ENTREPRISE, FILET, FOND, GRIS, LEGAL, LOGO, LOGO_RATIO, NOIR, OR, OR_FOND, esc, propre, styles

S = styles(10.4)
L = A4[0] - 36 * mm  # largeur utile
VERSION = '07/10/2026'


def P(t, s='p'):
    return Paragraph(propre(t), S[s])


def puces(items, style='puce'):
    return [Paragraph(propre(esc(i)), S[style], bulletText='•') for i in items]


def titre_section(n, texte):
    chip = Table([[Paragraph(f'<font name="M-XB" color="#0B1830">{n}</font>', S['pc'])]], colWidths=[8.5 * mm], rowHeights=[8.5 * mm])
    chip.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), OR), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                              ('ROUNDEDCORNERS', [4, 4, 4, 4]), ('TOPPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]))
    t = Table([[chip, P(esc(texte), 'h1')]], colWidths=[11 * mm, L - 11 * mm])
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                           ('LINEBELOW', (0, 0), (-1, -1), 1.2, OR), ('BOTTOMPADDING', (0, 0), (-1, -1), 4), ('TOPPADDING', (0, 0), (-1, -1), 0)]))
    return [CondPageBreak(40 * mm), Spacer(1, 6), t, Spacer(1, 6)]


def encart(texte, fond=FOND, barre=BLEU):
    t = Table([[P(texte, 'encart')]], colWidths=[L])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), fond), ('LINEBEFORE', (0, 0), (0, -1), 3.5, barre),
                           ('LEFTPADDING', (0, 0), (-1, -1), 12), ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                           ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8)]))
    return t


def tableau(entetes, lignes, largeurs, gras0=True):
    tot = sum(largeurs)
    data = [[P(esc(h), 'tete') for h in entetes]] + [
        [c if not isinstance(c, str) else P(esc(c), 'celb' if (gras0 and k == 0) else 'cel') for k, c in enumerate(l)] for l in lignes]
    t = Table(data, colWidths=[L * x / tot for x in largeurs], repeatRows=1)
    st = [('BACKGROUND', (0, 0), (-1, 0), BLEU), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LINEBELOW', (0, 1), (-1, -1), 0.5, FILET),
          ('LEFTPADDING', (0, 0), (-1, -1), 6), ('RIGHTPADDING', (0, 0), (-1, -1), 6), ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5)]
    st += [('BACKGROUND', (0, i), (-1, i), CREME) for i in range(2, len(data), 2)]
    t.setStyle(TableStyle(st))
    return t


def paragraphes(texte):
    out = []
    for bloc in texte.split('\n'):
        b = bloc.strip()
        if not b:
            continue
        if b.startswith('•'):
            out += puces([b.lstrip('• ')])
        else:
            # Intitulés en capitales (« ÉVALUATION FORMATIVE : … ») mis en gras, sans majuscules criardes
            b = esc(b)
            import re
            m = re.match(r'^([A-ZÀ-ÜŒ\' ’\-]{6,}?)\s*:\s*(.*)$', b)
            if m:
                tete = m.group(1).strip().capitalize()
                b = f'<b>{tete} :</b> {m.group(2)}'
            out.append(P(b))
    return out


def tuiles(f):
    donnees = [
        ('DURÉE', f"{f['heures']} heures", f"{f['jours']} jour{'s' if f['jours'] > 1 else ''} · 7 h par jour"),
        ('EFFECTIF', '6 à 8', 'participants, inter et intra'),
        ('INTER', f"{eur(f['inter'])} €", 'par jour et par stagiaire'),
        ('INTRA', f"{eur(f['intra'])} €", 'par jour pour le groupe'),
    ]
    cel = [[P(l, 'tuile_l'), P(v, 'tuile_v'), P(s_, 'tuile_s')] for l, v, s_ in donnees]
    cartes = []
    for c in cel:
        t = Table([[c[0]], [c[1]], [c[2]]], colWidths=[L / 4 - 4 * mm])
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), FOND), ('LINEABOVE', (0, 0), (-1, 0), 2.5, OR),
                               ('LEFTPADDING', (0, 0), (-1, -1), 8), ('TOPPADDING', (0, 0), (-1, -1), 2.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5)]))
        cartes.append(t)
    g = Table([cartes], colWidths=[L / 4] * 4)
    g.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 4 * mm), ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    return g


def contenu(f):
    e = []
    brouillon = f['statut'] != 'Active'
    # Bandeau titre
    logo = Image(str(LOGO), width=30 * mm, height=30 * mm * LOGO_RATIO)
    carte_logo = Table([[logo]], colWidths=[38 * mm], rowHeights=[33 * mm])
    carte_logo.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.white), ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('ROUNDEDCORNERS', [8, 8, 8, 8])]))
    texte = [P('PROGRAMME DE FORMATION' + (' · VERSION DE TRAVAIL' if brouillon else ''), 'sur'), P(esc(f['nom']), 'titre_blanc'),
             P(esc(f['promesse']), 'sous_or'), Spacer(1, 4),
             P(f"Réf. {f['ref']} · {esc(f['type'] or 'Inter et intra-entreprise')} · Présentiel", 'blanc')]
    band = Table([[carte_logo, texte]], colWidths=[44 * mm, L - 44 * mm])
    band.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), BLEU), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                              ('LEFTPADDING', (0, 0), (-1, -1), 10), ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                              ('TOPPADDING', (0, 0), (-1, -1), 12), ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                              ('LINEBELOW', (0, 0), (-1, -1), 3, OR), ('ROUNDEDCORNERS', [10, 10, 0, 0])]))
    e += [band, Spacer(1, 8), tuiles(f), Spacer(1, 4)]
    if brouillon:
        e.append(encart('<b>Formation en développement :</b> ce programme est une version de travail, non publiée au catalogue.', OR_FOND, OR))

    n = 0

    def sec(t):
        nonlocal n
        n += 1
        return titre_section(n, t)

    e += sec('Public visé')
    e += paragraphes(f['public'])

    e += sec('Objectifs de la formation')
    e.append(P(f"<b>{esc(f['promesse'])}.</b>"))
    e.append(P('À l\'issue de la formation, le participant sera en capacité de :'))
    for code, verbe, texte, crit in f['objectifs']:
        ligne = f'<b>{code}</b>{" · " + esc(verbe) if verbe else ""} — {esc(texte)}'
        if crit:
            ligne += f'<br/><font color="#3F4A5C" size="8.8">Critère de réussite : {esc(crit)}</font>'
        e.append(Paragraph(propre(ligne), S['puce'], bulletText='›'))

    e += sec('Outils de mesure des écarts')
    e.append(tableau(['Moment', 'Outil', 'Ce qui est mesuré'], [
        ['Avant', 'Test de positionnement et analyse du besoin', 'Le niveau de départ, la situation réelle et les attentes du participant'],
        ['Pendant', 'Grille critériée remise dès l\'ouverture', 'L\'acquisition de chaque objectif, atelier par atelier'],
        ['Fin de formation', 'Mise en situation notée + quiz de 10 questions (seuil 7/10)', 'Les compétences opérationnelles acquises'],
        ['Après', 'Questionnaire de satisfaction à chaud, puis à froid à J+30', 'La mise en pratique réelle au poste de travail'],
    ], [1, 1.6, 2.4]))

    e += sec('Prérequis')
    e += paragraphes(f['prerequis'])

    e += sec('Durée et horaires')
    e.append(tableau(['Élément', 'Détail'], [
        ['Durée', f"{f['jours']} jour{'s' if f['jours'] > 1 else ''} — {f['heures']} heures de formation (7 heures par jour)"],
        ['Horaires', '08h00 – 12h00 et 13h00 – 17h00'],
        ['Pauses', 'Deux pauses de 15 minutes, à 10h00 et à 15h00 ; pause méridienne de 12h00 à 13h00'],
        ['Délai d\'accès', '15 jours ouvrés minimum entre l\'inscription et le démarrage'],
        ['Modalité', f"Présentiel — {esc(f['type'] or 'inter ou intra-entreprise')}"],
    ], [1, 3.6]))

    e += sec('Contenu pédagogique')
    for k, j in enumerate(f['deroule'], start=1):
        titre_j = f"Jour {k}" + (f" — {j['titre']}" if j.get('titre') else '') if len(f['deroule']) > 1 else ('La journée' + (f" — {j['titre']}" if j.get('titre') else ''))
        bloc = [P(esc(titre_j), 'h2')]
        lignes = []
        for c in j['creneaux']:
            if c['pause']:
                lignes.append([P(c['h'].replace('–', ' – '), 'celbleu'), P(f'<i>{esc(c["titre"])}</i>', 'cel')])
            else:
                corps = f'<b>{esc(c["titre"])}</b>' + ''.join(f'<br/>• {esc(p)}' for p in c['points'])
                lignes.append([P(c['h'].replace('–', ' – '), 'celbleu'), P(corps, 'cel')])
        t = Table([[P('Horaire', 'tete'), P('Séquence et contenus', 'tete')]] + lignes, colWidths=[27 * mm, L - 27 * mm], repeatRows=1)
        st = [('BACKGROUND', (0, 0), (-1, 0), BLEU), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LINEBELOW', (0, 1), (-1, -1), 0.5, FILET),
              ('LEFTPADDING', (0, 0), (-1, -1), 6), ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5)]
        st += [('BACKGROUND', (0, i), (-1, i), FOND) for i, c in enumerate(j['creneaux'], start=1) if c['pause']]
        t.setStyle(TableStyle(st))
        e += [CondPageBreak(60 * mm)] + bloc + [t, Spacer(1, 6)]

    e += sec('Méthodes pédagogiques')
    e += puces([
        'Méthode active et participative : 30 % d\'apports, 70 % de pratique sur la situation réelle de chaque participant.',
        'Démonstrations en temps réel sur grand écran, puis « je montre, nous faisons, vous faites ».',
        'Ateliers en binôme et en sous-groupe, mises en situation, jeux de rôle et cas pratiques réunionnais fictifs.',
        'Quiz interactifs et réactivation en début de séquence ; feedback individualisé.',
        'Évaluation formative tout au long de la formation et évaluation sommative en fin de parcours.',
    ])

    e += sec('Moyens et techniques pédagogiques')
    e += puces([
        'Salle équipée : vidéoprojecteur ou écran grand format, paperboard, connexion internet, prises électriques.',
        'Diaporama accessible : mots-clés, très grands caractères (corps 26 minimum), contrastes conformes WCAG 2.1 AA.',
        'Supports imprimés et numériques, fiches outils, grille critériée remise à chaque participant.',
        f"Matériel du stagiaire : {f['materiel']}.",
    ])

    e += sec('Évaluation')
    e += paragraphes(f['evaluation'])
    e.append(Spacer(1, 3))
    e.append(encart('<b>Supervision humaine.</b> Aucun système d\'intelligence artificielle n\'évalue, ne note ni ne classe les participants : la décision est prise par le formateur (règlement (UE) 2024/1689, annexe III ; RGPD, art. 22). Une attestation de fin de formation est remise à chaque participant : objectifs, nature, durée et résultats de l\'évaluation des acquis (code du travail, art. L.6353-1).'))

    e += sec('Accès et handicap')
    e += paragraphes(f['acces'])
    e += paragraphes(f['adaptations'])

    e += sec('Lieu')
    e += puces([
        'En présentiel.',
        'Le lieu est communiqué dans la convocation, envoyée au plus tard 7 jours avant le début de la session : hôtel, espace de séminaire ou de coworking en inter ; locaux de l\'entreprise cliente en intra.',
    ])

    e += sec('Tarifs et financements')
    e.append(tableau(['Formule', 'Tarif', 'Effectif'], [
        ['Inter-entreprises', f"{eur(f['inter'])} € par jour et par stagiaire", '6 participants minimum, 8 au maximum'],
        ['Intra-entreprise', f"{eur(f['intra'])} € par jour pour le groupe", '6 participants minimum, 8 au maximum'],
    ], [1.2, 1.8, 1.8]))
    e.append(P('Prix nets de taxe : TVA non applicable, article 293 B du code général des impôts.', 'petit'))
    e.append(Spacer(1, 4))
    e.append(P('<b>Financements possibles</b>, selon les critères de chaque financeur : ' + esc(', '.join(f['financements'])) + '.'))
    e.append(P('<b>Certification :</b> aucune certification RNCP ou RS n\'est visée à ce jour ; cette formation n\'est donc pas éligible au CPF.'))

    e += sec('Inscription')
    e += puces([
        'Pré-inscription : feuille d\'inscription et fiche de motivation ; signalement de tout besoin d\'aménagement, sans justificatif médical.',
        'Entretien individuel ou collectif : analyse des attentes et des prérequis.',
        'Positionnement : test de positionnement pour mesurer les écarts de compétences initiaux.',
        'Contractualisation : devis, puis convention (entreprise) ou contrat (particulier) signé avant le démarrage.',
        'Documents remis avant l\'entrée : programme, livret d\'accueil, règlement intérieur, information sur les données personnelles.',
    ])

    e += sec('Conditions d\'utilisation')
    e.append(P('Le stagiaire s\'engage à respecter les horaires, à n\'utiliser son téléphone qu\'en pause ou à la demande du formateur, à signer les feuilles d\'émargement par demi-journée (obligatoires pour le financement), à ne pas transmettre les supports de cours à des fins commerciales ou de prêt, et à adopter une attitude respectueuse envers les autres et le matériel.'))

    e += sec('Pourquoi choisir YEBA FORMATIONS')
    e.append(P('Une pédagogie centrée sur l\'humain, un cadre d\'exception et une expertise terrain reconnue. Nous ne formons pas des robots, nous formons des humains augmentés.'))

    e += sec('Responsable de la formation — contact — référent handicap')
    contact = Table([[P(f"<b>{ENTREPRISE['dirigeant']}</b><br/>Responsable pédagogique et référent handicap<br/>"
                        f"{ENTREPRISE['tel']} · {ENTREPRISE['email']}<br/>{ENTREPRISE['adresse']}<br/>{ENTREPRISE['site']}", 'encart')]], colWidths=[L])
    contact.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), OR_FOND), ('LINEBEFORE', (0, 0), (0, -1), 3.5, OR),
                                 ('LEFTPADDING', (0, 0), (-1, -1), 12), ('TOPPADDING', (0, 0), (-1, -1), 9), ('BOTTOMPADDING', (0, 0), (-1, -1), 9)]))
    e.append(KeepTogether([contact]))
    e.append(Spacer(1, 8))
    e.append(P('Document conçu avec l\'assistance d\'un système d\'IA générative (règlement (UE) 2024/1689, art. 50), vérifié et validé par le responsable pédagogique. Version en corps 16 sur simple demande.', 'petit'))
    return e


class Doc(BaseDocTemplate):
    def __init__(self, chemin, f):
        super().__init__(str(chemin), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=20 * mm, bottomMargin=20 * mm,
                         title=f"Programme de formation — {f['titre']}", author='YEBA FORMATIONS', subject=f"Programme {f['ref']}",
                         creator='YEBA FORMATIONS')
        self.f = f
        cadre = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id='c', leftPadding=0, rightPadding=0)
        self.addPageTemplates([PageTemplate(id='p', frames=[cadre], onPage=self.decor)])

    def decor(self, c, doc):
        w, h = A4
        c.saveState()
        if doc.page > 1:
            c.drawImage(str(LOGO), 18 * mm, h - 15 * mm, width=13 * mm, height=13 * mm * LOGO_RATIO, mask='auto')
            c.setFont('M-B', 7.8)
            c.setFillColor(BLEU)
            c.drawRightString(w - 18 * mm, h - 10.5 * mm, f"PROGRAMME DE FORMATION · {self.f['nom'].upper()}")
            c.setStrokeColor(OR)
            c.setLineWidth(0.8)
            c.line(18 * mm, h - 16.5 * mm, w - 18 * mm, h - 16.5 * mm)
        c.setStrokeColor(FILET)
        c.setLineWidth(0.6)
        c.line(18 * mm, 14 * mm, w - 18 * mm, 14 * mm)
        c.setFont('A', 7)
        c.setFillColor(GRIS)
        c.drawString(18 * mm, 10 * mm, LEGAL)
        c.drawString(18 * mm, 6.6 * mm, f"Réf. {self.f['ref']} · Mise à jour du document le : {VERSION}")
        c.setFont('M-B', 8.5)
        c.setFillColor(BLEU)
        c.drawRightString(w - 18 * mm, 8 * mm, str(doc.page))
        c.restoreState()


def eur(v):
    return f"{int(v):,}".replace(',', '\xa0') if v not in (None, '') else '—'


def construire(f, chemin):
    Doc(chemin, f).build(contenu(f))
