# Lecture de pages web

Pages web générales, flux RSS.

## Page web générale (Jina Reader)

```bash
# Lire le contenu de n'importe quelle page web
curl -s "https://r.jina.ai/URL"

# Exemple
curl -s "https://r.jina.ai/https://example.com/article"
```

**Quand l'utiliser** : la plupart des pages web se lisent directement avec Jina Reader.

> ⚠️ Règle YEBA : Jina Reader est un service tiers hors UE (société Elastic).
> N'y envoyer que des URL publiques, jamais une page contenant des données
> personnelles ou client (RGPD).

## Web Reader (MCP)

```bash
# Lire une page web (format Markdown)
mcporter call web-reader.webReader url="https://example.com"

# Conserver les images
mcporter call web-reader.webReader url="https://example.com" retain_images=true

# Format texte brut
mcporter call web-reader.webReader url="https://example.com" return_format="text"
```

**Quand l'utiliser** : quand il faut contrôler plus finement le format de sortie.

## RSS (feedparser)

```python
python3 -c "
import feedparser
for e in feedparser.parse('FEED_URL').entries[:5]:
    print(f'{e.title} — {e.link}')
"
```

**Quand l'utiliser** : suivre des blogs, sites d'actualité, podcasts via leur flux RSS
(ex. veille CNIL, EUR-Lex, presse locale).

## Guide de choix

| Situation | Outil recommandé |
|-----|---------|
| Page web générale | Jina Reader (`curl r.jina.ai`) |
| Besoin des images / du format | MCP web-reader |
| Abonnement RSS | feedparser |
