import gen
css=open('style.css').read()
html='<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Catalogue 2026 — YEBA FORMATIONS</title><style>'+css+'</style></head><body>'+''.join(gen.pages(False))+'</body></html>'
open('catalogue.html','w').write(html)
