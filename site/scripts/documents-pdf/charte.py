"""Charte graphique YEBA FORMATIONS pour les documents PDF (programmes, livrets d'accueil).

Bleu #1B3A6B, or #C9A84C (jamais en texte sur fond blanc : filets, pastilles, fonds), noir #121212.
Titres Montserrat, texte Atkinson Hyperlegible (police conçue pour les personnes malvoyantes).
"""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ICI = Path(__file__).parent
LOGO = ICI / 'logo-yeba-doc.png'  # logo fourni par le dirigeant (fond transparent), réduit à 420 px pour alléger les PDF
LOGO_RATIO = 657 / 771

for nom, f in [('M-SB', 'Montserrat-SemiBold'), ('M-B', 'Montserrat-Bold'), ('M-XB', 'Montserrat-ExtraBold'),
               ('A', 'Atkinson-Regular'), ('A-B', 'Atkinson-Bold'), ('A-I', 'Atkinson-Italic'), ('A-BI', 'Atkinson-BoldItalic')]:
    pdfmetrics.registerFont(TTFont(nom, str(ICI / 'polices' / f'{f}.ttf')))
pdfmetrics.registerFont(TTFont('DJ', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFontFamily('A', normal='A', bold='A-B', italic='A-I', boldItalic='A-BI')
pdfmetrics.registerFontFamily('M-B', normal='M-B', bold='M-XB', italic='M-B', boldItalic='M-XB')

BLEU = colors.HexColor('#1B3A6B')
BLEU_NUIT = colors.HexColor('#0B1830')
OR = colors.HexColor('#C9A84C')
OR_CLAIR = colors.HexColor('#E3C979')
NOIR = colors.HexColor('#121212')
GRIS = colors.HexColor('#3F4A5C')
GRIS_CLAIR = colors.HexColor('#5B6678')
FOND = colors.HexColor('#EEF2F8')
CREME = colors.HexColor('#F7F4EC')
FILET = colors.HexColor('#D5DCE8')
OR_FOND = colors.HexColor('#F6EFD9')

ENTREPRISE = {
    'nom': 'YEBA FORMATIONS', 'dirigeant': 'Aurélien LUMEKA',
    'adresse': '9 rue Françoise Châtelain, 97490 Sainte-Clotilde — La Réunion',
    'tel': '06 93 32 24 45', 'email': 'yebaformations@gmail.com', 'site': 'www.yebaformations.re',
    'siret': '814 622 262 00032', 'nda': '04973676397', 'qualiopi': '25FOR02027.1',
}
LEGAL = (f"YEBA FORMATIONS — Aurélien LUMEKA EI — SIRET {ENTREPRISE['siret']} — NDA {ENTREPRISE['nda']} "
         f"— Qualiopi n° {ENTREPRISE['qualiopi']} (actions de formation)")


def styles(base=10.4):
    """Jeu de styles ; `base` = corps du texte (10,4 pt en A4, 9,6 pt en A5)."""
    k = base / 10.4
    st = lambda nom, **kw: ParagraphStyle(nom, **kw)
    return {
        'p': st('p', fontName='A', fontSize=base, leading=base * 1.42, textColor=NOIR, spaceAfter=4 * k),
        'pc': st('pc', fontName='A', fontSize=base, leading=base * 1.42, textColor=NOIR, alignment=TA_CENTER),
        'petit': st('petit', fontName='A', fontSize=base * 0.82, leading=base * 1.15, textColor=GRIS),
        'petitc': st('petitc', fontName='A', fontSize=base * 0.82, leading=base * 1.15, textColor=GRIS, alignment=TA_CENTER),
        'puce': st('puce', fontName='A', fontSize=base, leading=base * 1.38, textColor=NOIR, leftIndent=13 * k, bulletIndent=2 * k, spaceAfter=2.5 * k),
        'h1': st('h1', fontName='M-XB', fontSize=base * 1.5, leading=base * 1.85, textColor=BLEU, spaceBefore=10 * k, spaceAfter=3 * k),
        'h2': st('h2', fontName='M-B', fontSize=base * 1.12, leading=base * 1.4, textColor=BLEU, spaceBefore=8 * k, spaceAfter=3 * k),
        'h3': st('h3', fontName='M-B', fontSize=base * 0.98, leading=base * 1.3, textColor=NOIR, spaceBefore=4 * k, spaceAfter=2 * k),
        'cel': st('cel', fontName='A', fontSize=base * 0.88, leading=base * 1.2, textColor=NOIR),
        'celb': st('celb', fontName='A-B', fontSize=base * 0.88, leading=base * 1.2, textColor=NOIR),
        'celbleu': st('celbleu', fontName='M-B', fontSize=base * 0.82, leading=base * 1.14, textColor=BLEU),
        'tete': st('tete', fontName='M-B', fontSize=base * 0.82, leading=base * 1.1, textColor=colors.white),
        'encart': st('encart', fontName='A', fontSize=base, leading=base * 1.42, textColor=NOIR),
        'blanc': st('blanc', fontName='A', fontSize=base, leading=base * 1.4, textColor=colors.white),
        'titre_blanc': st('titre_blanc', fontName='M-XB', fontSize=base * 2.4, leading=base * 2.8, textColor=colors.white),
        'sous_or': st('sous_or', fontName='M-SB', fontSize=base * 1.15, leading=base * 1.5, textColor=OR_CLAIR),
        'sur': st('sur', fontName='M-B', fontSize=base * 0.78, leading=base, textColor=OR_CLAIR, spaceAfter=4),
        'titre_couv': st('titre_couv', fontName='M-XB', fontSize=base * 1.85, leading=base * 2.25, textColor=BLEU, alignment=TA_CENTER),
        'sur_couv': st('sur_couv', fontName='M-B', fontSize=base * 0.8, leading=base * 1.1, textColor=GRIS, alignment=TA_CENTER),
        'tuile_v': st('tuile_v', fontName='M-XB', fontSize=base * 1.25, leading=base * 1.45, textColor=BLEU, alignment=TA_LEFT),
        'tuile_l': st('tuile_l', fontName='M-B', fontSize=base * 0.72, leading=base * 0.95, textColor=GRIS_CLAIR),
        'tuile_s': st('tuile_s', fontName='A', fontSize=base * 0.82, leading=base * 1.1, textColor=GRIS),
    }


def esc(t):
    return str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def propre(t):
    """Remplace les quelques signes absents des polices de la charte."""
    return (str(t).replace('→', '›').replace('≥', '⩾').replace('⩾', 'au moins ').replace('☐', '□')
            .replace('✓', '•').replace(' ', ' '))
