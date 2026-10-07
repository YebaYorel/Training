"""Éléments communs aux programmes : pauses, moyens, suivi, version."""

VERSION = '7 octobre 2026'

PAUSE_MATIN = ('10:00-10:15', '15 min', 'Pause', '-', '-', '-')
DEJEUNER = ('12:00-13:00', '60 min', 'Pause méridienne', 'Hors temps de formation', '-', '-')
PAUSE_APREM = ('15:00-15:15', '15 min', 'Pause', '-', '-', '-')

MOYENS_BASE = [
    'Une salle avec vidéoprojecteur ou écran grand format, paperboard, Wi-Fi stable et prises électriques.',
    'Supports projetés en corps 26 points minimum, contrastes conformes WCAG 2.1 niveau AA ; livret ressource en corps 16 points sur demande.',
    'Grille critériée, fiches outils et livrables remis à chaque stagiaire (papier et numérique).',
]


def suivi_standard(jours, atelier, production):
    lignes = [
        ['Avant l\'entrée', 'Test de positionnement + analyse du besoin', 'Niveau de départ, situation réelle, attentes', 'Constituer les binômes, adapter les exemples et le rythme'],
        ['Début J1', 'Séquence 0 + recueil des attentes', 'Représentations, usages déjà en place', 'Ajuster les démonstrations ; afficher les attentes'],
        ['En séance', atelier, 'Capacité à appliquer la méthode', 'Apporter une consigne à trous ou un cas plus exigeant'],
    ]
    if jours > 1:
        lignes.append(['Début J2' if jours == 2 else 'Début J2 et J3', 'Quiz de réactivation', 'Mémorisation et transfert', 'Revenir sur un point si moins de 70 % de réussite'])
    lignes.append([f'Fin J{jours}', 'Quiz + ' + production, 'Connaissances et compétence intégrée', 'Valider, valider avec réserve ou proposer une reprise'])
    lignes.append(['J+60', 'Questionnaire à froid', 'Usages réellement installés au poste', 'Alimenter l\'amélioration continue du programme'])
    return lignes
