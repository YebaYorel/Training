# Outils de recherche

Moteur de recherche IA Exa.

## Recherche IA Exa

Moteur de recherche IA de bonne qualité, adapté pour trouver de la documentation
technique, des exemples officiels et des pages pertinentes.

```bash
mcporter call exa.web_search_exa query="requête" numResults=5
mcporter call exa.web_search_exa query="library API code example" numResults=5
```

> ⚠️ Règle YEBA : Exa est un service américain (hors UE). Uniquement des
> requêtes publiques et anonymisées — jamais de nom de client, de stagiaire ni
> de donnée personnelle dans la requête (RGPD, transfert hors UE).

### Cas d'usage

| Situation | Paramètres |
|-----|------|
| Recherche web | `web_search_exa(query: "...", numResults: 5)` |
| Documentation technique / code | `web_search_exa(query: "nom du framework API exemple", numResults: 5)` |

> L'outil `get_code_context_exa` du MCP Exa est obsolète et n'est pas enregistré
> par défaut. Pour les questions de code, utiliser aussi `web_search_exa` ; pour
> chercher précisément dans le contenu d'un dépôt, utiliser la recherche GitHub
> de `dev.md`.

### Points forts

- Très bon sur les contenus en anglais et la documentation technique
- Permet de cibler la documentation officielle et les exemples de code
- Résultats de bonne qualité

## Comparaison avec d'autres outils de recherche

| Outil | Origine | Usage |
|-----|------|---------|
| Exa | agent-reach | Recherche anglophone / technique / code |
| Recherche GitHub | agent-reach (dev.md) | Dépôts / code |
