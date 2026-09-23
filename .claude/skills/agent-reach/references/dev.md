# Outils de développement

GitHub CLI

## GitHub (gh CLI)

Outil officiel en ligne de commande de GitHub : dépôts, Issues, PR, Actions,
Releases et accès à l'API.

```bash
# Authentification
gh auth login
gh auth status

# Recherche
gh search repos "requête" --sort stars --limit 10
gh search code "requête" --language python

# Dépôts
gh repo view owner/repo
gh repo clone owner/repo
gh repo create my-repo --private
gh repo fork owner/repo
gh repo fork owner/repo --clone
gh repo sync owner/repo

# Issues
gh issue list -R owner/repo --state open
gh issue view 123 -R owner/repo
gh issue create -R owner/repo --title "Titre" --body "Contenu"

# Pull Requests
gh pr list -R owner/repo --state open
gh pr view 123 -R owner/repo
gh pr create -R owner/repo --title "Titre" --body "Contenu"
gh pr checks 123 --repo owner/repo

# Actions / CI
gh run list --repo owner/repo --limit 10
gh run view <run-id> --repo owner/repo
gh run view <run-id> --repo owner/repo --log-failed
gh workflow list --repo owner/repo

# Releases
gh release list -R owner/repo
gh release create v1.0.0

# API
gh api /user
gh api repos/owner/repo

# Sortie JSON
gh issue list --repo owner/repo --json number,title --jq '.[] | "\(.number): \(.title)"'
```

> Dans l'environnement Claude Code web, `gh` n'est pas disponible : utiliser
> les outils GitHub MCP (`mcp__github__*`) à la place.

## Guide de choix

| Outil | Origine | Usage |
|-----|------|------|
| gh CLI | agent-reach | Opérations Git / GitHub |
| MCP GitHub | Claude Code | Lire dépôts, issues, PR sans `gh` |
