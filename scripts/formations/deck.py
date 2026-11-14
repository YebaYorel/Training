"""Fabrique de diaporamas de formation YEBA FORMATIONS (python-pptx).

Le contenu (privé) est décrit dans un module `contenu.py` hors du dépôt ; ce fichier
ne contient que la mise en forme. Règles appliquées (skill yeba-powerpoint) :
titres >= 40 pt, texte >= 28 pt, mots-clés seulement, contraste >= 7:1 visé,
aucune ligne ne traverse un texte, texte alternatif sur chaque image, 16:9.

    construire(diapos, sortie, marque=True, titre_fichier="...")

`marque=False` : aucune trace de YEBA FORMATIONS (sous-traitance en marque blanche).
"""
import random
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

RACINE = Path(__file__).resolve().parents[2]
LOGO = RACINE / 'site' / 'scripts' / 'documents-pdf' / 'logo-yeba-doc.png'

BLEU, OR, NOIR, BLANC = '1B3A6B', 'C9AB4C', '121212', 'FFFFFF'
FOND_CLAIR = 'EEF2F8'
DECOR = '2F5FA8'          # néon bleu décoratif (jamais pour du texte)
NIVEAUX = {               # couleur de fond, couleur du texte (contraste >= 7:1)
    'interdit': ('8E1B1B', BLANC), 'haut': ('8A4500', BLANC),
    'transparence': (OR, NOIR), 'minimal': ('1E5E3A', BLANC),
}
TITRE, TEXTE = 'Montserrat', 'Inter'
L, H = Inches(13.333), Inches(7.5)
LARGEUR_CAR = 0.62        # même hypothèse que verifier_accessibilite.py


def rgb(h):
    return RGBColor.from_string(h)


def taille_pour(mots, largeur_emu, voulu, mini=28, marge_pt=16):
    """Plus grande taille <= voulu pour que le mot le plus long tienne dans la zone."""
    long = max((len(m) for t in mots for m in t.split()), default=1)
    utile = Emu(largeur_emu).pt - marge_pt
    t = voulu
    while t > mini and long * t * LARGEUR_CAR > utile:
        t -= 2
    if long * t * LARGEUR_CAR > utile:
        raise ValueError(f'Mot trop long pour la zone : {mots}')
    return t


class Deck:
    def __init__(self, marque=True):
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = L, H
        self.marque = marque
        self.layout = self.prs.slide_layouts[5]  # « Titre seul » : un vrai titre pour les lecteurs d'écran

    # ------------------------------------------------------------------ outils
    def _diapo(self, fond):
        s = self.prs.slides.add_slide(self.layout)
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = rgb(fond)
        return s

    def _titre(self, s, texte, couleur, gauche=Inches(0.75), haut=Inches(0.42), larg=Inches(10.9),
               haut_zone=Inches(1.15), taille=40, align=PP_ALIGN.LEFT):
        t = s.shapes.title
        t.left, t.top, t.width, t.height = gauche, haut, larg, haut_zone
        t.name = '!!titre'
        tf = t.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.text = texte
        p = tf.paragraphs[0]
        p.alignment = align
        r = p.runs[0]
        r.font.name, r.font.bold = TITRE, True
        r.font.size = Pt(taille_pour([texte], larg, taille, mini=40))
        r.font.color.rgb = rgb(couleur)
        return t

    def _texte(self, s, x, y, w, h, lignes, couleur, taille=30, gras=False, police=TEXTE,
               align=PP_ALIGN.LEFT, ancre=MSO_ANCHOR.TOP, nom=None, interligne=1.1, espace=8):
        bx = s.shapes.add_textbox(x, y, w, h)
        if nom:
            bx.name = nom
        tf = bx.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = ancre
        tf.margin_left = tf.margin_right = Inches(0.08)
        lignes = [lignes] if isinstance(lignes, str) else list(lignes)
        t = taille_pour(lignes, w, taille)
        for i, ligne in enumerate(lignes):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            p.line_spacing = interligne
            p.space_after = Pt(espace)
            r = p.add_run()
            r.text = ligne
            r.font.name, r.font.size, r.font.bold = police, Pt(t), gras
            r.font.color.rgb = rgb(couleur)
        return bx

    def _forme(self, s, kind, x, y, w, h, fond, nom=None, contour=None):
        f = s.shapes.add_shape(kind, x, y, w, h)
        f.fill.solid()
        f.fill.fore_color.rgb = rgb(fond)
        if contour:
            f.line.color.rgb = rgb(contour)
            f.line.width = Pt(2)
        else:
            f.line.fill.background()
        f.shadow.inherit = False
        if nom:
            f.name = nom
        return f

    def _carte(self, s, x, y, w, h, lignes, fond, couleur, taille=30, gras=True, nom=None, align=PP_ALIGN.CENTER):
        c = self._forme(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fond, nom=nom)
        c.adjustments[0] = 0.12
        tf = c.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_right = Inches(0.15)
        lignes = [lignes] if isinstance(lignes, str) else list(lignes)
        t = taille_pour(lignes, w - Inches(0.3), taille, marge_pt=4)
        for i, ligne in enumerate(lignes):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            r = p.add_run()
            r.text = ligne
            r.font.name = TITRE if (gras and i == 0) else TEXTE
            r.font.size, r.font.bold = Pt(t if i == 0 else max(28, t - 2)), gras and i == 0
            r.font.color.rgb = rgb(couleur)
        return c

    def _logo(self, s, x=None, y=None, h=Inches(0.75), sur_fond_sombre=False):
        if not self.marque:
            return
        w = int(h * 420 / 358)
        x = L - w - Inches(0.35) if x is None else x
        y = H - h - Inches(0.25) if y is None else y
        if sur_fond_sombre:   # pastille blanche : le logo fourni n'est jamais modifié ni recoloré
            p = self._forme(s, MSO_SHAPE.ROUNDED_RECTANGLE, x - Inches(0.12), y - Inches(0.1),
                            w + Inches(0.24), h + Inches(0.2), BLANC, nom='!!pastille-logo')
            p.adjustments[0] = 0.2
        pic = s.shapes.add_picture(str(LOGO), x, y, height=h)
        pic.name = '!!logo'
        pic._element.xpath('./p:nvPicPr/p:cNvPr')[0].set('descr', 'Logo YEBA FORMATIONS : trois montagnes en réseau')
        return pic

    def _badge(self, s, objectif, fond_diapo):
        """Rappel de l'objectif en coin de diapo (étayage : maintien de l'orientation)."""
        if not objectif:
            return
        b = self._forme(s, MSO_SHAPE.OVAL, L - Inches(1.45), Inches(0.5), Inches(1.0), Inches(1.0), OR, nom='!!badge')
        tf = b.text_frame
        tf.margin_left = tf.margin_right = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = objectif
        r.font.name, r.font.size, r.font.bold = TITRE, Pt(28), True
        r.font.color.rgb = rgb(NOIR)

    def _barre(self, s, couleur=OR):
        self._forme(s, MSO_SHAPE.RECTANGLE, Inches(0.38), Inches(0.62), Inches(0.12), Inches(0.75), couleur, nom='!!barre')

    def _reseau(self, s, x0, y0, w, h, graine, n=16, couleur_points=OR, couleur_liens=DECOR):
        """Motif « réseau de points reliés » (Cyber-Garage), confiné à une zone sans texte."""
        rnd = random.Random(graine)
        pts = [(x0 + int(rnd.random() * w), y0 + int(rnd.random() * h)) for _ in range(n)]
        for i, (xa, ya) in enumerate(pts):
            voisins = sorted(pts[:i] + pts[i + 1:], key=lambda q: (q[0] - xa) ** 2 + (q[1] - ya) ** 2)[:2]
            for xb, yb in voisins:
                c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, xa, ya, xb, yb)
                c.line.color.rgb = rgb(couleur_liens)
                c.line.width = Pt(1.25)
                c.name = 'decor-lien'
        for i, (x, y) in enumerate(pts):
            d = Inches(0.16) if i % 4 else Inches(0.24)
            self._forme(s, MSO_SHAPE.OVAL, x - d // 2, y - d // 2, d, d, couleur_points if i % 3 else DECOR, nom='decor-point')

    @staticmethod
    def _notes(s, notes):
        if notes:
            s.notes_slide.notes_text_frame.text = notes

    # ------------------------------------------------------------------ modèles
    def couverture(self, d):
        s = self._diapo(NOIR)
        self._reseau(s, Inches(8.9), Inches(0.5), Inches(4.0), Inches(4.2), graine=7, n=18)
        self._titre(s, d['titre'], BLANC, haut=Inches(2.2), larg=Inches(8.0), haut_zone=Inches(2.3), taille=44)
        if d.get('sous_titre'):
            self._texte(s, Inches(0.75), Inches(4.6), Inches(8.0), Inches(1.0), d['sous_titre'], OR, taille=30, gras=True, police=TITRE)
        if d.get('bas'):
            self._texte(s, Inches(0.75), Inches(5.8), Inches(7.6), Inches(1.2), d['bas'], BLANC, taille=28)
        self._logo(s, x=Inches(0.85), y=Inches(0.55), h=Inches(1.2), sur_fond_sombre=True)
        self._notes(s, d.get('notes'))

    def section(self, d):
        s = self._diapo(BLEU)
        self._reseau(s, Inches(9.2), Inches(3.9), Inches(3.6), Inches(3.0), graine=int(d.get('num', 1)) * 11, n=12)
        self._texte(s, Inches(0.75), Inches(1.0), Inches(3.0), Inches(2.0), str(d['num']), OR, taille=96, gras=True,
                    police=TITRE, nom='!!numero')
        self._titre(s, d['titre'], BLANC, haut=Inches(3.0), larg=Inches(8.2), haut_zone=Inches(1.4), taille=48)
        if d.get('sous_titre'):
            self._texte(s, Inches(0.75), Inches(4.5), Inches(8.2), Inches(1.6), d['sous_titre'], BLANC, taille=30)
        self._badge(s, d.get('objectif'), BLEU)
        self._notes(s, d.get('notes'))

    def mots(self, d):
        """1 à 4 mots-clés en cartes, sur fond blanc."""
        s = self._diapo(BLANC)
        self._barre(s)
        self._titre(s, d['titre'], BLEU)
        self._badge(s, d.get('objectif'), BLANC)
        items = d['mots']
        n = len(items)
        marge, ecart = Inches(0.75), Inches(0.3)
        par_ligne = 2 if n == 4 else n          # 4 cartes : grille 2 × 2, pour que les mots longs tiennent
        rangs = (n + par_ligne - 1) // par_ligne
        larg = (L - 2 * marge - (par_ligne - 1) * ecart) // par_ligne
        haut = Inches(3.4) if rangs == 1 else Inches(1.72)
        for i, it in enumerate(items):
            lignes = it if isinstance(it, (list, tuple)) else [it]
            fond, coul = (BLEU, BLANC) if (i + i // par_ligne) % 2 == 0 else (FOND_CLAIR, BLEU)
            x = marge + (i % par_ligne) * (larg + ecart)
            y = Inches(1.95) + (i // par_ligne) * (haut + Inches(0.18))
            self._carte(s, x, y, larg, haut, lignes, fond, coul, taille=d.get('taille', 32), nom=f'!!carte{i}')
        if d.get('pied'):
            self._texte(s, marge, Inches(5.75), Inches(10.5), Inches(1.0), d['pied'], NOIR, taille=28)
        self._logo(s)
        self._notes(s, d.get('notes'))

    def liste(self, d):
        """Liste de 3 à 5 mots-clés numérotés (pas de phrases)."""
        s = self._diapo(BLANC)
        self._barre(s)
        self._titre(s, d['titre'], BLEU)
        self._badge(s, d.get('objectif'), BLANC)
        y = Inches(1.85)
        pas = min(Inches(1.0), (Inches(5.1)) // max(1, len(d['items'])))
        for i, it in enumerate(d['items']):
            pastille = self._forme(s, MSO_SHAPE.OVAL, Inches(0.8), y + Inches(0.08), Inches(0.72), Inches(0.72), BLEU, nom=f'!!puce{i}')
            tf = pastille.text_frame
            tf.margin_left = tf.margin_right = 0
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            r = p.add_run()
            r.text = str(i + 1) if not d.get('symboles') else d['symboles'][i]
            r.font.name, r.font.size, r.font.bold = TITRE, Pt(28), True
            r.font.color.rgb = rgb(BLANC)
            self._texte(s, Inches(1.8), y, Inches(10.3), pas, it, NOIR, taille=d.get('taille', 32 if len(d['items']) <= 5 else 28),
                        ancre=MSO_ANCHOR.MIDDLE)
            y += pas
        self._logo(s)
        self._notes(s, d.get('notes'))

    def chiffre(self, d):
        s = self._diapo(NOIR)
        self._reseau(s, Inches(9.6), Inches(0.4), Inches(3.3), Inches(2.4), graine=len(d['chiffre']) * 5, n=10)
        self._texte(s, Inches(0.75), Inches(1.4), Inches(8.6), Inches(2.3), d['chiffre'], OR, taille=110, gras=True,
                    police=TITRE, nom='!!chiffre')
        self._titre(s, d['titre'], BLANC, haut=Inches(3.8), larg=Inches(11.5), haut_zone=Inches(1.3), taille=40)
        if d.get('source'):
            self._texte(s, Inches(0.75), Inches(5.3), Inches(10.0), Inches(0.9), d['source'], BLANC, taille=28)
        self._logo(s, sur_fond_sombre=True)
        self._notes(s, d.get('notes'))

    def activite(self, d):
        """Jeu, atelier, exercice de crise : fond noir, étiquette or."""
        s = self._diapo(NOIR)
        self._carte(s, Inches(0.75), Inches(0.45), Inches(3.3), Inches(0.9), d.get('etiquette', 'JEU'), OR, NOIR, taille=30,
                    nom='!!etiquette')
        self._titre(s, d['titre'], BLANC, haut=Inches(1.5), larg=Inches(11.0), haut_zone=Inches(1.2), taille=44)
        y = Inches(2.95)
        for i, c in enumerate(d['consignes'][:4]):
            self._texte(s, Inches(0.95), y, Inches(8.6), Inches(0.85), f'{i + 1}. {c}', BLANC, taille=30, ancre=MSO_ANCHOR.MIDDLE)
            y += Inches(0.9)
        if d.get('duree'):
            self._carte(s, Inches(9.9), Inches(3.1), Inches(2.8), Inches(1.9), ['Durée', d['duree']], BLEU, BLANC, taille=32,
                        nom='!!duree')
        self._badge(s, d.get('objectif'), NOIR)
        self._notes(s, d.get('notes'))

    def oral(self, d):
        """Évaluation formative à voix haute (main levée, cartes)."""
        s = self._diapo(BLEU)
        self._carte(s, Inches(0.75), Inches(0.45), Inches(4.2), Inches(0.9), 'À VOIX HAUTE', OR, NOIR, taille=30, nom='!!etiquette')
        self._titre(s, d['titre'], BLANC, haut=Inches(1.5), larg=Inches(11.2), haut_zone=Inches(1.3), taille=42)
        items = d['items']
        n = len(items)
        marge, ecart = Inches(0.75), Inches(0.25)
        larg = (L - 2 * marge - (n - 1) * ecart) // n
        for i, it in enumerate(items):
            self._carte(s, marge + i * (larg + ecart), Inches(3.2), larg, Inches(2.6), it, BLANC, BLEU, taille=30, nom=f'!!carte{i}')
        self._badge(s, d.get('objectif'), BLEU)
        self._notes(s, d.get('notes'))

    def analogie(self, d):
        s = self._diapo(BLANC)
        self._barre(s)
        self._titre(s, d['titre'], BLEU)
        self._badge(s, d.get('objectif'), BLANC)
        self._carte(s, Inches(0.75), Inches(1.95), Inches(5.6), Inches(3.4), ['C\'est comme…', d['image']], BLEU, BLANC, taille=34,
                    nom='!!carte0')
        self._carte(s, Inches(6.75), Inches(1.95), Inches(5.85), Inches(3.4), ['Limite', d['limite']], FOND_CLAIR, BLEU, taille=30,
                    nom='!!carte1')
        if d.get('pied'):
            self._texte(s, Inches(0.75), Inches(5.65), Inches(10.6), Inches(1.0), d['pied'], NOIR, taille=28)
        self._logo(s)
        self._notes(s, d.get('notes'))

    def exemple(self, d):
        """Exemple saisissant réunionnais : lieu + 3 mots."""
        s = self._diapo(FOND_CLAIR)
        self._barre(s, BLEU)
        self._titre(s, d['titre'], BLEU)
        self._badge(s, d.get('objectif'), FOND_CLAIR)
        # largeur calculée sur le texte : un nom composé (Saint-Pierre) ne doit jamais se couper au trait d'union
        larg_lieu = max(Inches(4.4), Inches((len(d['lieu']) * 30 * LARGEUR_CAR + 40) / 72))
        self._carte(s, Inches(0.75), Inches(1.9), larg_lieu, Inches(1.1), d['lieu'], BLEU, BLANC, taille=30, nom='!!lieu')
        y = Inches(3.25)
        for i, m in enumerate(d['mots'][:3]):   # puce = petit carré or (forme décorative, pas un caractère)
            self._forme(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.85), y + Inches(0.33), Inches(0.24), Inches(0.24), OR, nom=f'puce{i}')
            self._texte(s, Inches(1.25), y, Inches(10.5), Inches(0.9), m, NOIR, taille=32, gras=(i == len(d['mots'][:3]) - 1),
                        ancre=MSO_ANCHOR.MIDDLE)
            y += Inches(0.95)
        self._logo(s)
        self._notes(s, d.get('notes'))

    def etapes(self, d):
        s = self._diapo(BLANC)
        self._barre(s)
        self._titre(s, d['titre'], BLEU)
        self._badge(s, d.get('objectif'), BLANC)
        n = len(d['etapes'])
        marge, ecart = Inches(0.5), Inches(0.25)
        larg = (L - 2 * marge - (n - 1) * ecart) // n
        for i, e in enumerate(d['etapes']):
            x = marge + i * (larg + ecart)
            self._carte(s, x, Inches(1.95), larg, Inches(0.95), str(i + 1), OR, NOIR, taille=36, nom=f'!!num{i}')
            lignes = e if isinstance(e, (list, tuple)) else [e]
            self._carte(s, x, Inches(3.05), larg, Inches(2.7), lignes, BLEU if i % 2 == 0 else FOND_CLAIR,
                        BLANC if i % 2 == 0 else BLEU, taille=30, nom=f'!!carte{i}')
        if d.get('pied'):
            self._texte(s, marge, Inches(5.95), Inches(10.6), Inches(0.9), d['pied'], NOIR, taille=28)
        self._logo(s)
        self._notes(s, d.get('notes'))

    def niveaux(self, d):
        """Les 4 niveaux de l'IA Act : couleur + mot (la couleur n'est jamais seule)."""
        s = self._diapo(BLANC)
        self._barre(s)
        self._titre(s, d['titre'], BLEU)
        self._badge(s, d.get('objectif'), BLANC)
        marge, ecart = Inches(0.75), Inches(0.25)
        larg = (L - 2 * marge - ecart) // 2          # grille 2 × 2 : les mots longs ne sont jamais coupés
        haut = Inches(2.15)
        for i, (cle, mot, ex) in enumerate(d['niveaux']):
            fond, coul = NIVEAUX[cle]
            x = marge + (i % 2) * (larg + ecart)
            y = Inches(1.85) + (i // 2) * (haut + Inches(0.2))
            self._carte(s, x, y, larg, haut, [mot, ex], fond, coul, taille=32, nom=f'!!carte{i}')
        self._logo(s)
        self._notes(s, d.get('notes'))

    def frise(self, d):
        s = self._diapo(BLANC)
        self._barre(s)
        self._titre(s, d['titre'], BLEU)
        self._badge(s, d.get('objectif'), BLANC)
        n = len(d['jalons'])
        marge, ecart = Inches(0.6), Inches(0.18)
        larg = (L - 2 * marge - (n - 1) * ecart) // n
        for i, (date, quoi) in enumerate(d['jalons']):
            x = marge + i * (larg + ecart)
            self._carte(s, x, Inches(1.95), larg, Inches(1.5), date, BLEU, BLANC, taille=28, nom=f'!!date{i}')
            self._carte(s, x, Inches(3.6), larg, Inches(2.5), quoi, FOND_CLAIR, NOIR, taille=28, gras=False, nom=f'!!quoi{i}')
        if d.get('pied'):
            self._texte(s, marge, Inches(6.25), Inches(10.6), Inches(0.8), d['pied'], NOIR, taille=28)
        self._logo(s)
        self._notes(s, d.get('notes'))

    def fin(self, d):
        s = self._diapo(NOIR)
        self._reseau(s, Inches(8.8), Inches(3.6), Inches(4.0), Inches(3.4), graine=99, n=14)
        self._titre(s, d['titre'], BLANC, haut=Inches(2.0), larg=Inches(8.0), haut_zone=Inches(1.5), taille=48)
        if d.get('lignes'):
            self._texte(s, Inches(0.75), Inches(3.7), Inches(7.8), Inches(2.6), d['lignes'], OR, taille=30, gras=True)
        self._logo(s, x=Inches(0.85), y=Inches(0.55), h=Inches(1.1), sur_fond_sombre=True)
        self._notes(s, d.get('notes'))

    def enregistrer(self, sortie, titre, auteur):
        cp = self.prs.core_properties
        cp.title, cp.author, cp.last_modified_by = titre, auteur, auteur
        cp.subject, cp.keywords = 'Support de formation', 'formation; accessibilité'
        cp.comments = ('Support conçu avec l\'assistance d\'un système d\'IA générative (règlement (UE) 2024/1689, art. 50), '
                       'vérifié et validé par le formateur, qui en assume la responsabilité.')
        self.prs.save(sortie)


def construire(diapos, sortie, titre, marque=True):
    d = Deck(marque=marque)
    for spec in diapos:
        getattr(d, spec['type'])(spec)
    auteur = 'YEBA FORMATIONS — Aurélien LUMEKA' if marque else 'Formateur'
    d.enregistrer(sortie, titre, auteur)
    return len(diapos)
