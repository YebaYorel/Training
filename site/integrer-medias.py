"""Intègre les médias dans apercu/index.html pour obtenir un fichier unique, lisible hors ligne."""
import base64, pathlib
racine = pathlib.Path(__file__).parent.parent
page = racine / 'apercu' / 'index.html'
html = page.read_text(encoding='utf-8')
types = {'.mp4': 'video/mp4', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.png': 'image/png'}
for f in sorted((racine / 'site' / 'public' / 'media').iterdir()):
    if f.suffix in types:  # le WebM (doublon du MP4) n'est pas intégré : poids inutile
        uri = f'data:{types[f.suffix]};base64,' + base64.b64encode(f.read_bytes()).decode()
        html = html.replace(f'media/{f.name}', uri)
page.write_text(html, encoding='utf-8')
print(page, round(len(html) / 1e6, 2), 'Mo', '— reste « media/ » :', html.count('media/'))
