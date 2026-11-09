"""Génère les programmes détaillés PDF des formations IA et automatisation.

    python3 site/scripts/programmes-pdf/generer.py [FOR-0002 ...]

Sortie : site/public/programmes/*.pdf (documents publics : programme de formation, RNQ ind. 1).
"""
import importlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from rendu import Programme  # noqa: E402

SORTIE = Path(__file__).parent.parent.parent / 'public' / 'programmes'
REFS = ['FOR-0002', 'FOR-0006', 'FOR-0009', 'FOR-0010', 'FOR-0011', 'FOR-0013', 'FOR-0014', 'FOR-0015']


def main(refs):
    SORTIE.mkdir(parents=True, exist_ok=True)
    index = {}
    for ref in refs:
        f = importlib.import_module('for_' + ref[-4:]).F
        chemin = SORTIE / f['fichier']
        Programme(f).construire(chemin)
        index[ref] = {'fichier': f['fichier'], 'deroule': [
            {'titre': j.get('titre'), 'fil': j['fil'], 'lignes': [list(l) for l in j['lignes']], 'livrables': j.get('livrables', [])}
            for j in f['jours_detail']]}
        print(ref, chemin.stat().st_size // 1024, 'Ko')
    # Déroulé structuré pour le site (même source que le PDF : jamais d'écart entre les deux)
    cible = Path(__file__).parent.parent.parent / 'src' / 'deroules.json'
    existant = json.loads(cible.read_text(encoding='utf-8')) if cible.exists() else {}
    existant.update(index)
    cible.write_text(json.dumps(existant, ensure_ascii=False, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main(sys.argv[1:] or REFS)
