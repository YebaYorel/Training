"""Génère, pour chaque formation YEBA du catalogue Airtable, les trois documents :
programme de formation (A4 portrait), livret d'accueil A5 portrait (lecture écran)
et livret d'accueil A4 paysage (impression en livret plié).

Usage : python generer.py [FOR-0004 FOR-0015 ...]
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

from donnees import fiches, incoherences
from livret import construire_a5, imposer
from programme import construire

RACINE = Path(__file__).resolve().parents[2] / 'public' / 'documents'
# Les livrets d'accueil reprennent le modèle du Pack Qualiopi (vendu par YEBA Studio) :
# ils sont remis aux stagiaires inscrits, jamais publiés sur le site ni versionnés.
PRIVE = Path(__file__).resolve().parents[3] / 'livrables-prives' / 'livrets'


def slug(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    return re.sub(r'[^A-Za-z0-9]+', '-', t).strip('-')[:60]


def main(refs=None):
    fs = fiches(refs)
    (RACINE / 'programmes').mkdir(parents=True, exist_ok=True)
    PRIVE.mkdir(parents=True, exist_ok=True)
    index = []
    for f in fs:
        base = f"{f['ref']}_{slug(f['nom'])}"
        prog = RACINE / 'programmes' / f'Programme_{base}.pdf'
        a5 = PRIVE / f'Livret-accueil_{base}_A5-portrait.pdf'
        a4 = PRIVE / f'Livret-accueil_{base}_A4-paysage-impression.pdf'
        construire(f, prog)
        n = construire_a5(f, a5)
        imposer(a5, a4)
        index.append({'ref': f['ref'], 'heures': f['heures'], 'jours': f['jours'], 'pages_livret': n,
                      'programme': prog.relative_to(RACINE.parent).as_posix()})
        print(f"{f['ref']} · {f['heures']} h / {f['jours']} j · livret {n} p. A5")
    if not refs:
        (RACINE / 'index.json').write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding='utf-8')
    print('\nIncohérences relevées (à arbitrer, rien n\'est modifié dans Airtable) :')
    for i in incoherences(fs):
        print(' -', i)


if __name__ == '__main__':
    main(sys.argv[1:] or None)
