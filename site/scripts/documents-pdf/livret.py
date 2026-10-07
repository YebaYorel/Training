"""Livret d'accueil du stagiaire : A5 portrait (lecture écran) + A4 paysage imposé (impression en livret plié).

Structure et textes communs repris du livret modèle du dirigeant ; règlement intérieur = YEBA-DOC-04 (en vigueur).
"""
import json
import re
from pathlib import Path

import pymupdf
from reportlab.lib import colors
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, Image, KeepTogether, PageBreak, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle)

from charte import BLEU, CREME, ENTREPRISE, FILET, FOND, GRIS, LOGO, LOGO_RATIO, NOIR, OR, OR_FOND, esc, propre, styles
from memos import MEMOS

S = styles(9.6)
W, H = A5
M = 14 * mm
L = W - 2 * M
VERSION = '7 octobre 2026'
DOC04 = Path(__file__).parent.parent.parent / 'airtable' / 'documents-brut.json'


def P(t, s='p'):
    return Paragraph(propre(t), S[s])


def puces(items):
    return [Paragraph(propre(i), S['puce'], bulletText='•') for i in items]


class Titre(Paragraph):
    """Titre de rubrique repéré pour le sommaire."""

    def __init__(self, texte, rubrique=True):
        super().__init__(propre(texte), S['h1'])
        self.rubrique = texte if rubrique else None


def titre(t, rubrique=True):
    return [Titre(esc(t), rubrique), Table([['']], colWidths=[L], rowHeights=[2], style=[('LINEABOVE', (0, 0), (-1, -1), 1.3, OR)]), Spacer(1, 6)]


class Brut(str):
    """Texte déjà balisé (pas d'échappement)."""


def tableau(entetes, lignes, largeurs):
    tot = sum(largeurs)
    data = [[P(esc(h), 'tete') for h in entetes]] + [[P(c if isinstance(c, Brut) else esc(c), 'celbleu' if k == 0 else 'cel')
                                                      for k, c in enumerate(l)] for l in lignes]
    t = Table(data, colWidths=[L * x / tot for x in largeurs], repeatRows=1)
    st = [('BACKGROUND', (0, 0), (-1, 0), BLEU), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LINEBELOW', (0, 1), (-1, -1), 0.5, FILET),
          ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5), ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]
    st += [('BACKGROUND', (0, i), (-1, i), CREME) for i in range(2, len(data), 2)]
    t.setStyle(TableStyle(st))
    return t


def encart(texte, fond=FOND, barre=BLEU):
    t = Table([[P(texte, 'encart')]], colWidths=[L])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), fond), ('LINEBEFORE', (0, 0), (0, -1), 3, barre),
                           ('LEFTPADDING', (0, 0), (-1, -1), 9), ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    return t


def pastilles(items):
    """Liste numérotée à pastilles or (objectifs)."""
    lignes = []
    for i, t in enumerate(items, start=1):
        chip = Table([[P(f'<font name="M-XB" color="#0B1830">{i}</font>', 'pc')]], colWidths=[6 * mm], rowHeights=[6 * mm])
        chip.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), OR), ('ROUNDEDCORNERS', [9, 9, 9, 9]), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                  ('TOPPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0)]))
        lignes.append([chip, P(esc(t))])
    t = Table(lignes, colWidths=[9 * mm, L - 9 * mm])
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
    return t


def cadre_ecriture(titre_cadre, hauteur):
    t = Table([[P(f'<b>{esc(titre_cadre)}</b>', 'cel')], ['']], colWidths=[L], rowHeights=[None, hauteur])
    t.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.8, BLEU), ('BACKGROUND', (0, 0), (-1, 0), FOND), ('LEFTPADDING', (0, 0), (-1, -1), 6)]))
    return [t, Spacer(1, 6)]


def reglement_interieur():
    data = json.loads(DOC04.read_text(encoding='utf-8'))['records']
    texte = next(r['fields']['fldcNJ4MDGkK3uDKb'] for r in data if r['fields'].get('fldFfYg5S7zrqgROf') == 'YEBA-DOC-04')
    texte = texte.split('ACCUSÉ DE RÉCEPTION')[0]
    out = []
    for l in texte.split('\n')[4:]:
        l = l.strip()
        if not l:
            continue
        if l.startswith('TITRE'):
            t = l.capitalize()
            t = re.sub(r'^(Titre) ([ivx]+)\b', lambda m: f'{m.group(1)} {m.group(2).upper()}', t)
            out.append(P(esc(t), 'h2'))
        elif l.startswith('Article'):
            out.append(P(esc(l), 'h3'))
        elif l.startswith('•'):
            out += puces([esc(l.lstrip('• '))])
        else:
            out.append(P(esc(l)))
    return out


def contenu(f, sommaire):
    e = []
    nom_court = f['nom']
    duree = f"{f['jours']} jour{'s' if f['jours'] > 1 else ''} · {f['heures']} heures de formation"
    # ---- Couverture ----
    e += [Spacer(1, 14 * mm), Image(str(LOGO), width=46 * mm, height=46 * mm * LOGO_RATIO), Spacer(1, 9 * mm),
          P('LIVRET D\'ACCUEIL DU STAGIAIRE', 'sur_couv'), Spacer(1, 5), P(esc(f['nom']), 'titre_couv'), Spacer(1, 3),
          P(esc(f['promesse']), 'pc'), Spacer(1, 8 * mm)]
    infos = Table([[P(f"<b>{duree}</b>", 'pc')], [P('08h00 – 17h00 · 7 heures de formation par jour', 'pc')],
                   [P('Dates et lieu : précisés dans votre convocation', 'pc')], [P(f"Réf. {f['ref']} · Présentiel", 'petitc')]], colWidths=[L])
    infos.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), FOND), ('LINEABOVE', (0, 0), (-1, 0), 2.5, OR), ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
    e += [infos, Spacer(1, 10 * mm), P('Stagiaire : ......................................................', 'pc'), Spacer(1, 12 * mm),
          P('<font name="M-SB" color="#1B3A6B" size="11">Apprendre, grandir, réussir</font>', 'pc'), PageBreak()]

    # ---- Sommaire ----
    e += titre('Sommaire', rubrique=False)
    lignes = [[P(esc(t), 'cel'), P(f'<b>{p}</b>', 'cel')] for t, p in sommaire] or [[P('…', 'cel'), P('', 'cel')]]
    som = Table(lignes, colWidths=[L - 12 * mm, 12 * mm])
    som.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, -1), 0.4, FILET), ('ALIGN', (1, 0), (1, -1), 'RIGHT'), ('TOPPADDING', (0, 0), (-1, -1), 2.2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2)]))
    e += [som, PageBreak()]

    n = [0]

    def rub(t):
        n[0] += 1
        return [CondPageBreak(55 * mm)] + titre(f'{n[0]}. {t}')

    e += rub('Bienvenue')
    e += [P(f"Vous allez suivre la formation <b>« {esc(f['nom'])} »</b> : {esc(f['promesse'][0].lower() + f['promesse'][1:])}."),
          P('Cette formation a été construite pour votre métier, à partir de vos réponses au questionnaire de positionnement. Ici, pas de cours magistral : <b>70 % de pratique</b>, des ateliers, des mises en situation en petit groupe, et des outils que vous utiliserez dès le lendemain.'),
          P('Lisez ce livret avant la session et gardez-le : il vous accompagnera aussi après la formation.'),
          Spacer(1, 4), P('Je me réjouis de vous accueillir.'), P(f"<b>{ENTREPRISE['dirigeant']}</b><br/>Directeur de YEBA FORMATIONS, formateur")]

    e += rub('Vos interlocuteurs')
    e.append(P('<b>YEBA FORMATIONS</b> est un organisme de formation réunionnais, créé en 2021, spécialisé en vente, management, relation client et intelligence artificielle. Il est <b>certifié Qualiopi</b> (n° 25FOR02027.1) au titre de la catégorie <b>actions de formation</b>.'))
    e.append(tableau(['Rôle', 'Interlocuteur'], [['Formateur', 'Aurélien LUMEKA'], ['Référent pédagogique', 'Aurélien LUMEKA'], ['Référent handicap', 'Aurélien LUMEKA'],
                                                 ['Suivi administratif', 'Aurélien LUMEKA'], ['Si un fait concerne le formateur', 'Votre responsable dans l\'entreprise ou votre financeur ; le Défenseur des droits (09 69 39 00 00)']], [1.1, 1.6]))
    e += [Spacer(1, 6), KeepTogether(encart(f"<b>Contact</b><br/>Tél. : {ENTREPRISE['tel']}<br/>E-mail : {ENTREPRISE['email']}<br/>Site : {ENTREPRISE['site']}"))]

    e += rub('La formation en bref')
    e.append(tableau(['Élément', 'Détail'], [
        ['Intitulé', f['titre']], ['Public', re.split(r'\n', f['public'])[0]], ['Prérequis', re.split(r'\n', f['prerequis'])[0]],
        ['Modalité', f"Présentiel, {f['type'].lower() if f['type'] else 'inter ou intra-entreprise'}, groupe de 6 à 8 personnes"],
        ['Durée', duree], ['Dates', 'Précisées dans votre convocation'],
    ], [0.9, 2]))
    e += [Spacer(1, 6), P('La journée en pratique', 'h2'), tableau(['Élément', 'Détail'], [
        ['Horaires', Brut('8h00 – 17h00 · 7 heures de formation<br/>Pause : 10h00 – 10h15<br/>Déjeuner : 12h00 – 13h00<br/>Pause : 15h00 – 15h15')],
        ['Lieu', 'Précisé dans votre convocation, envoyée au plus tard 7 jours avant la session'],
        ['Matériel', f['materiel']], ['Formateur', 'Aurélien LUMEKA'],
        ['Financement', ', '.join(f['financements']) + ' — selon votre situation'],
        ['Rémunération', 'Salarié : votre rémunération est maintenue par votre employeur'],
    ], [0.9, 2])]

    e += rub('Objectifs')
    e.append(P('<b>À la fin de la formation, vous serez capable de :</b>'))
    e.append(pastilles([o[2] for o in f['objectifs']]))

    e += rub('Programme')
    for k, j in enumerate(f['deroule'], start=1):
        tj = (f"Jour {k}" if len(f['deroule']) > 1 else 'La journée') + (f" — {j['titre']}" if j.get('titre') else '')
        lignes = []
        for c in j['creneaux']:
            corps = f'<i>{esc(c["titre"])}</i>' if c['pause'] else f'<b>{esc(c["titre"])}</b>' + ''.join(f'<br/>• {esc(p)}' for p in c['points'][:4])
            lignes.append([c['h'].replace('–', ' – '), Brut(corps)])
        e += [CondPageBreak(45 * mm), P(esc(tj), 'h2'), tableau(['Horaire', 'Séquence'], lignes, [0.75, 2.25]), Spacer(1, 4)]

    e += rub('Méthodes pédagogiques')
    e += puces(['30 % d\'apports, 70 % de pratique : ateliers, jeux de rôle en binôme, cas pratiques, retours personnalisés.',
                'Cas pratiques tirés du quotidien des entreprises réunionnaises, avec des entreprises et des clients fictifs : aucune personne réelle n\'est citée.',
                'Diaporama accessible : mots-clés, très grands caractères, fort contraste.',
                'D\'abord en binôme, puis en groupe : personne ne passe devant le groupe sans s\'être entraîné. Droit au joker.',
                'Ressource PDF complète remise après la session.'])

    e += rub('Évaluation et suivi')
    e.append(tableau(['Quand ?', 'Comment et pourquoi ?'], [
        ['Avant', 'Questionnaire de positionnement : connaître votre point de départ et adapter la formation'],
        ['Pendant', 'Observation pendant les ateliers, avec une grille critériée remise dès l\'ouverture'],
        ['En fin de formation', 'Mise en situation notée et quiz de 10 questions (réussite à partir de 7/10)'],
        ['17h00, dernier jour', 'Questionnaire de satisfaction « à chaud »'],
        ['À 30 jours (J+30)', 'Questionnaire « à froid » : ce qui a changé au quotidien'],
    ], [0.9, 2]))

    e += rub('Documents remis')
    e.append(tableau(['Quand ?', 'Documents'], [
        ['Avant la session', 'La convocation ; ce livret d\'accueil, avec le programme, le règlement intérieur et la notice sur vos données ; la fiche de droit à l\'image (facultative)'],
        ['Après la session', 'L\'attestation de fin de formation : objectifs, nature, durée et résultats de l\'évaluation (code du travail, art. L.6353-1) ; la ressource PDF de la formation'],
        ['À votre employeur ou financeur', 'Les feuilles d\'émargement signées par demi-journée ; le certificat de réalisation'],
    ], [0.9, 2]))

    e += rub('Règles de vie')
    e.append(P('Le règlement intérieur complet figure en fin de livret. En résumé :'))
    e.append(tableau(['Règle', 'Ce qui est attendu'], [
        ['Ponctualité', 'Arriver à l\'heure ; signer soi-même la feuille de présence, matin et après-midi'],
        ['Absence, retard', 'Prévenir le formateur et votre responsable au plus tôt'],
        ['Téléphone', 'En mode silencieux ; utilisé seulement pour une activité demandée'],
        ['Respect', 'Bienveillance, écoute, aucune moquerie ni propos discriminant'],
        ['Confidentialité', 'Ce qui est dit en formation reste en formation'],
        ['Photos, vidéos', 'Interdites sans l\'accord écrit des personnes concernées'],
        ['Sécurité', 'Suivre les consignes du lieu d\'accueil ; signaler tout accident ou danger'],
        ['Tabac, alcool', 'Tabac, vapotage et alcool interdits dans les locaux'],
    ], [0.9, 2]))

    e += rub('Tolérance zéro')
    e.append(P('YEBA FORMATIONS applique une <b>tolérance zéro</b> face aux violences sexistes et sexuelles, au harcèlement et aux discriminations.'))
    e.append(encart('<b>Vous êtes victime ou témoin ?</b><br/>• Parlez-en au formateur, Aurélien LUMEKA, pendant ou après la session.<br/>• Si les faits concernent le formateur : adressez-vous à votre responsable ou au Défenseur des droits.<br/>• Écoute : <b>3919</b> (gratuit, anonyme).<br/>• Danger immédiat : <b>17</b> ou <b>112</b> ; par SMS : <b>114</b>.', OR_FOND, OR))
    e.append(Spacer(1, 4))
    e.append(P('Chaque signalement est traité <b>sous 48 heures</b>, en toute <b>confidentialité</b>. Aucune personne qui signale des faits de bonne foi, ou qui en témoigne, ne peut subir de représailles.'))

    e += rub('Infos pratiques')
    e.append(tableau(['Sujet', 'Information'], [
        ['Adresse', 'Indiquée dans votre convocation'], ['Arrivée', 'Présentez-vous à 7h50 : la formation commence à 8h00 précises'],
        ['Transport', 'Par vos propres moyens. Le trajet relève de la législation sur les accidents de trajet.'],
        ['Déjeuner', 'De 12h00 à 13h00, pris hors de la salle de formation'], ['À apporter', f"De quoi écrire. {f['materiel']}."],
        ['Tenue', 'Professionnelle ou confortable. Activités assises ou debout, au choix.'],
    ], [0.9, 2]))

    e += rub('Handicap et accessibilité')
    e.append(P('Vous avez un besoin particulier, lié ou non à un handicap : vue, audition, mobilité, concentration, santé ? Contactez le référent handicap, avant la session si possible.'))
    e.append(encart(f"<b>Référent handicap : Aurélien LUMEKA</b><br/>{ENTREPRISE['adresse']}<br/>{ENTREPRISE['tel']} · {ENTREPRISE['email']}"))
    e.append(Spacer(1, 4))
    e += puces(['Vous n\'avez pas à indiquer de raison ni de diagnostic : seul le besoin d\'aménagement est utile.',
                'Déjà prévu pour tout le groupe : supports en grands caractères, activités assises ou debout au choix, pauses, consignes à l\'oral et à l\'écrit.',
                'Sur demande : supports en 16 points, place près de l\'écran, évaluation orale, rythme adapté, temps majoré.',
                'Votre information reste confidentielle : elle n\'est pas transmise à votre employeur sans votre accord.'])

    e += rub('Vos données (RGPD)')
    e.append(P(f"<b>Responsable du traitement :</b> YEBA FORMATIONS, représentée par son directeur, Aurélien LUMEKA ({ENTREPRISE['email']})."))
    e.append(tableau(['Données', 'Pourquoi ? Base légale', 'Durée'], [
        ['Identité, fonction, émargements, attestation', 'Organiser la formation et justifier sa réalisation. Contrat et obligation légale.', '3 ans (plus si la loi l\'impose)'],
        ['Positionnement, grille, quiz, plan d\'action', 'Adapter la formation, mesurer les acquis. Obligation légale (L.6353-1).', '3 ans'],
        ['Questionnaires de satisfaction', 'Améliorer les formations. Intérêt légitime.', '3 ans'],
        ['Besoin d\'aménagement', 'Adapter la formation. Seul l\'aménagement est noté, jamais la raison.', 'Fin de la session'],
        ['Photo, vidéo', 'Uniquement les usages que vous cochez. Votre consentement.', 'Durée choisie'],
    ], [1, 1.5, 0.8]))
    e.append(Spacer(1, 4))
    e += puces(['Votre employeur reçoit votre présence, votre attestation et le certificat ; vos réponses individuelles au positionnement ne lui sont pas transmises.',
                'L\'organisme certificateur Qualiopi et les services de contrôle de l\'État, uniquement en cas d\'audit ou de contrôle.',
                'Les prestataires techniques de YEBA FORMATIONS, liés par contrat. Outils hébergés de préférence dans l\'Union européenne ; tout transfert hors UE est encadré (RGPD, art. 44 et suivants).',
                'Aucune donnée n\'est vendue ni utilisée à des fins publicitaires.',
                f"Vos droits : accès, rectification, effacement, limitation, opposition, retrait du consentement. Écrivez à {ENTREPRISE['email']} : réponse sous un mois. Vous pouvez aussi saisir la CNIL (www.cnil.fr)."])

    e += rub('IA et évaluation')
    e.append(encart('<b>Transparence sur l\'usage de l\'IA</b><br/>Certains supports de cette formation ont été conçus avec l\'aide d\'une intelligence artificielle générative, puis vérifiés et validés par le formateur (règlement européen sur l\'IA, art. 50).'))
    e.append(Spacer(1, 4))
    e += puces(['Aucune IA ne note, ne classe ni n\'évalue les stagiaires : la correction est faite par le formateur.',
                'Aucune décision vous concernant n\'est prise de façon automatisée (RGPD, art. 22).',
                'Vous pouvez demander l\'explication de votre résultat et le contester auprès du formateur.'])

    e += rub('Avis et réclamations')
    e += puces(['Votre avis compte : questionnaire de satisfaction en fin de formation, puis questionnaire « à froid » à 30 jours (J+30).',
                f"Réclamation : oralement au formateur, ou par e-mail à {ENTREPRISE['email']}.",
                'Accusé de réception sous 48 heures ouvrées, réponse motivée sous 15 jours ouvrés (règlement intérieur, art. 24).',
                'Chaque avis et chaque réclamation sont analysés pour améliorer nos formations.'])

    e += rub('Numéros utiles')
    e.append(tableau(['Service', 'Numéro'], [['Votre formateur', ENTREPRISE['tel']], ['SAMU — urgence médicale', '15'], ['Pompiers', '18'],
                                             ['Police — gendarmerie', '17'], ['Numéro d\'urgence européen', '112'], ['Urgence par SMS (surdité)', '114'],
                                             ['Violences Femmes Info', '3919'], ['Défenseur des droits', '09 69 39 00 00']], [1.8, 1]))

    e += rub('Mémo des méthodes')
    e.append(tableau(['Méthode', 'Les étapes'], MEMOS.get(f['ref'], []), [0.9, 2]))

    e += [PageBreak()] + titre(f'{n[0] + 1}. Règlement intérieur')
    n[0] += 1
    e.append(P('Réf. YEBA-DOC-04 — applicable aux stagiaires (code du travail, art. L.6352-3 à L.6352-5 et R.6352-1 à R.6352-15).', 'petit'))
    e += reglement_interieur()

    e += [PageBreak()] + rub('Attestation de remise')
    e.append(P(f"Je soussigné(e), stagiaire de l'action « {esc(f['titre'])} » organisée par YEBA FORMATIONS, atteste avoir reçu, lu et compris ce livret d'accueil, le <b>règlement intérieur</b> et la <b>notice d'information sur mes données</b>, et m'engage à respecter le règlement intérieur."))
    e.append(Spacer(1, 6))
    sig = Table([[P('<b>Le stagiaire</b><br/>Nom et prénom :<br/><br/>Date :<br/><br/>Signature :', 'cel'),
                  P('<b>Pour YEBA FORMATIONS</b><br/>Aurélien LUMEKA, directeur<br/><br/>Date :<br/><br/>Signature :', 'cel')]], colWidths=[L / 2, L / 2], rowHeights=[48 * mm])
    sig.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.8, BLEU), ('INNERGRID', (0, 0), (-1, -1), 0.8, BLEU), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 6), ('TOPPADDING', (0, 0), (-1, -1), 6)]))
    e += [sig, Spacer(1, 6), P('Un exemplaire séparé de cette attestation est signé le jour J et conservé au dossier de la session (Qualiopi, indicateur 9).', 'petit')]

    e += [PageBreak()] + rub('Mon plan d\'action')
    e.append(P('À compléter en fin de formation, puis à relire avec votre responsable.'))
    for t in ['Ce que je retiens de la formation', 'Ce que j\'applique dès demain', 'Quand, avec qui, et comment je mesure mon progrès', 'Ma première action dans les 30 jours']:
        e += cadre_ecriture(t, 24 * mm)
    return e


def notes():
    return [PageBreak()] + titre('Mes notes', rubrique=False) + [Table([['']] * 22, colWidths=[L], rowHeights=[7 * mm] * 22, style=[('LINEBELOW', (0, 0), (-1, -1), 0.4, FILET)])]


def quatrieme():
    lignes = [f"<b>YEBA FORMATIONS</b>", '9 rue Françoise Châtelain', '97490 Sainte-Clotilde — La Réunion',
              f"{ENTREPRISE['tel']} · {ENTREPRISE['email']}", ENTREPRISE['site'], '', f"SIRET {ENTREPRISE['siret']}",
              f"Déclaration d'activité n° {ENTREPRISE['nda']} auprès du préfet de région de La Réunion. Cet enregistrement ne vaut pas agrément de l'État.",
              f"Certification Qualiopi n° {ENTREPRISE['qualiopi']} — catégorie « actions de formation ».", 'Référent handicap : Aurélien LUMEKA.', '',
              f'Livret remis avant l\'entrée en formation (code du travail, art. L.6353-8). Version du {VERSION}. Version en 16 points sur simple demande.',
              'Document conçu avec l\'assistance d\'un système d\'IA générative (règlement (UE) 2024/1689, art. 50), vérifié et validé par un humain.']
    return [PageBreak(), Spacer(1, 40 * mm), Image(str(LOGO), width=30 * mm, height=30 * mm * LOGO_RATIO), Spacer(1, 8)] + [P(l, 'petitc') if l else Spacer(1, 6) for l in lignes]


class Doc(BaseDocTemplate):
    def __init__(self, chemin, f):
        super().__init__(str(chemin), pagesize=A5, leftMargin=M, rightMargin=M, topMargin=17 * mm, bottomMargin=15 * mm,
                         title=f"Livret d'accueil — {f['titre']}", author='YEBA FORMATIONS', subject=f"Livret d'accueil {f['ref']}", creator='YEBA FORMATIONS')
        self.f = f
        self.rubriques = []
        self.dernier = 0
        cadre = Frame(M, self.bottomMargin, L, self.height, id='c', leftPadding=0, rightPadding=0)
        self.addPageTemplates([PageTemplate(id='p', frames=[cadre], onPage=self.decor)])

    def afterFlowable(self, fl):
        if isinstance(fl, Titre) and fl.rubrique:
            self.rubriques.append((fl.rubrique, self.page))

    def decor(self, c, doc):
        p = doc.page
        if p == 1 or (self.dernier and p == self.dernier):
            return
        c.saveState()
        c.setFont('M-XB', 6.8)
        c.setFillColor(BLEU)
        c.drawString(M, H - 9 * mm, 'YEBA FORMATIONS')
        c.setFont('A', 6.8)
        c.setFillColor(GRIS)
        c.drawRightString(W - M, H - 9 * mm, f"Livret d'accueil – {self.f['nom']}")
        c.setStrokeColor(OR)
        c.setLineWidth(0.7)
        c.line(M, H - 10.8 * mm, W - M, H - 10.8 * mm)
        c.setFont('M-B', 7.5)
        c.setFillColor(BLEU)
        (c.drawString if p % 2 == 0 else c.drawRightString)(M if p % 2 == 0 else W - M, 8 * mm, str(p))
        c.restoreState()


def construire_a5(f, chemin):
    # 1er passage : pagination des rubriques et nombre de pages
    d = Doc(chemin, f)
    d.build(contenu(f, []))
    sommaire = d.rubriques
    d = Doc(chemin, f)
    d.build(contenu(f, sommaire))
    pages = d.page
    # Total multiple de 4 (livret plié) : pages « Mes notes » puis 4e de couverture
    k = 1
    while (pages + k + 1) % 4:
        k += 1
    d = Doc(chemin, f)
    d.dernier = pages + k + 1
    d.build(contenu(f, d.rubriques or sommaire) + sum([notes() for _ in range(k)], []) + quatrieme())
    return d.page


def imposer(a5, a4):
    """A5 × N → A4 paysage, ordre de pliage (cahier unique, piqûre à cheval)."""
    src = pymupdf.open(str(a5))
    n = src.page_count
    assert n % 4 == 0, n
    out = pymupdf.open()
    lw, lh = 841.89, 595.28
    for i in range(n // 2):
        gauche, droite = (n - 1 - i, i) if i % 2 == 0 else (i, n - 1 - i)
        page = out.new_page(width=lw, height=lh)
        page.show_pdf_page(pymupdf.Rect(0, 0, lw / 2, lh), src, gauche)
        page.show_pdf_page(pymupdf.Rect(lw / 2, 0, lw, lh), src, droite)
    out.set_metadata({**src.metadata, 'title': src.metadata.get('title', '') + ' — impression livret A4 paysage'})
    out.save(str(a4))
    return out.page_count
