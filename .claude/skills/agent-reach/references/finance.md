# Cotations financières (Xueqiu)

Cotations boursières, recherche et contenus populaires de Xueqiu (plateforme
chinoise). Les cours peuvent être différés ; ce n'est pas un conseil en
investissement.

## Vérifier d'abord l'état

```bash
agent-reach doctor --json
```

Si `xueqiu.active_backend` est renseigné, utiliser ce backend ; la valeur `null`
signifie seulement que Doctor n'a pas vérifié le contenu en direct. Xueqiu
exige une session connectée ou un cookie minimal : une erreur HTTP 400 ne veut
pas dire que l'action n'existe pas.

## OpenCLI (prioritaire si une session Chrome connectée existe sur le poste)

```bash
# Vérifier la session actuelle
opencli xueqiu whoami -f yaml

# Recherche d'actions et cours en temps réel
opencli xueqiu search "NVIDIA" -f yaml
opencli xueqiu stock NVDA -f yaml

# Contenus et actions populaires
opencli xueqiu hot -f yaml
opencli xueqiu hot-stock -f yaml

# Voir toutes les commandes en lecture seule
opencli xueqiu --help
```

OpenCLI réutilise uniquement une session de navigateur déjà ouverte et
contrôlée par l'utilisateur. Ne jamais lancer `opencli xueqiu login`
automatiquement ; sans session existante, demander à l'utilisateur de se
connecter dans Chrome, ou d'importer explicitement le cookie minimal :

```bash
agent-reach configure --from-browser chrome --platform xueqiu
```

Cette configuration lit et enregistre uniquement `xq_a_token`, sans collecter
les cookies d'autres plateformes.

> ⚠️ Règle YEBA : plateforme chinoise, hors UE — accord explicite d'Aurélien
> requis avant toute configuration de cookie.

## Validation et gestion des échecs

- Succès = nom, code, cours de l'action ou liste de contenus non vide ; un code
  de sortie 0 avec des champs vides n'est pas un succès.
- HTTP 400 = en général un problème de session/cookie, pas un code action inexistant.
- Si `whoami` réussit mais `stock`/`hot` échouent : signaler un problème
  d'adaptateur ou d'API de la plateforme, pas un défaut de connexion.
