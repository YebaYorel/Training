#!/usr/bin/env bash
# UserPromptSubmit : à la demande d'Aurélien, rappelle à chaque message
# d'utiliser le skill agent-reach (accès internet) et ses règles YEBA.
cat <<'MSG'
[Rappel automatique — skill agent-reach] Si cette demande nécessite une information d'internet (recherche, veille, lien, plateforme, réglementation, concurrents, marché), utilise le skill `agent-reach` (.claude/skills/agent-reach/SKILL.md) et ses règles YEBA : aucune donnée personnelle ou client envoyée à un service tiers, signaler RGPD / IA Act, citer chaque source par son URL, dire clairement si un canal est bloqué. Réponds en français.
MSG
