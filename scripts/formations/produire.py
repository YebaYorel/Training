"""Produit le pack complet d'une formation à partir de son dossier privé.

    python scripts/formations/produire.py livrables-prives/formations/FOR-0003

Le dossier contient `contenu.py` (diapos, objectifs, déroulé, évaluation, grille, jeux) et `ressource.py`
(livret du stagiaire). Sorties dans le même dossier ; rien n'est écrit dans le dépôt Git.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parents[1]
sys.path.insert(0, str(ICI))

import deck  # noqa: E402
import documents  # noqa: E402

SKILL = RACINE / '.claude' / 'skills' / 'yeba-powerpoint' / 'scripts'


def charger(chemin, nom):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(dossier):
    d = Path(dossier).resolve()
    c = charger(d / 'contenu.py', 'contenu')
    r = charger(d / 'ressource.py', 'ressource')
    ref, marque = c.META['ref'], c.META.get('marque', True)
    brut = d / 'brut.pptx'
    deck.construire(c.DIAPOS, brut, f"{ref} — {c.META['titre']}", marque=marque)
    sections = [i + 1 for i, s in enumerate(c.DIAPOS) if s['type'] == 'section']
    forts = ['--diapo', '1:prisme', '--diapo', f'{len(c.DIAPOS)}:prisme']
    if len(sections) > 3:
        forts += ['--diapo', f'{sections[len(sections) // 2]}:revelation']
    sortie = d / f'{ref}_Support-stagiaires.pptx'
    subprocess.run([sys.executable, SKILL / 'transitions.py', brut, sortie, '--defaut', 'morph', *forts], check=True, capture_output=True)
    subprocess.run([sys.executable, SKILL / 'transitions.py', brut, d / f'{ref}_Support-sans-animation.pptx', '--defaut', 'aucune'],
                   check=True, capture_output=True)
    brut.unlink()
    verif = subprocess.run([sys.executable, SKILL / 'verifier_accessibilite.py', sortie], capture_output=True, text=True)
    print(verif.stdout.strip().splitlines()[-1])
    if verif.returncode:
        print(verif.stdout)
        raise SystemExit('Accessibilité : erreurs à corriger')
    documents.ressource(c, r, d / f'{ref}_Ressource-stagiaire.pdf', marque=marque)
    documents.ressource(c, r, d / f'{ref}_Ressource-stagiaire_corps16.pdf', base=16, marque=marque)
    documents.quiz(c, d / f'{ref}_Evaluation-10-questions_stagiaire.pdf', marque=marque)
    documents.quiz(c, d / f'{ref}_Evaluation-10-questions_corrige-evaluateur.pdf', corrige=True, marque=marque)
    documents.grille(c, d / f'{ref}_Grille-critériée.pdf', marque=marque)
    documents.guide(c, d / f'{ref}_Guide-animateur.pdf', marque=marque)
    documents.cartes(c, d / f'{ref}_Cartes-de-jeu.pdf', marque=marque)
    documents.deroule_xlsx(c, d / f'{ref}_Deroule-minute-par-minute.xlsx')
    for f in sorted(d.glob(f'{ref}_*')):
        print(f'{f.stat().st_size // 1024:>6} Ko  {f.name}')


if __name__ == '__main__':
    main(sys.argv[1])
