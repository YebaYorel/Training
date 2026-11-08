---
name: omniroute
description: Accès aux 46 skills d'OmniRoute (diegosouzapw/OmniRoute, MIT) — passerelle IA multi-fournisseurs (routage, quotas, cache, compression, clés API, CLI). Utiliser uniquement si Aurélien a installé un serveur OmniRoute et demande de le piloter, ou parle d'« OmniRoute ».
---

# OmniRoute (skills en réserve)

Les 46 skills OmniRoute sont rangés dans `.claude/reserve/omniroute/` (copie
figée au commit `3ee8039`, licence MIT) au lieu d'être chargés à chaque session.
Ils ne servent qu'avec un serveur OmniRoute installé : les charger d'office
aurait alourdi chaque session pour rien.

## Utilisation

1. Lister les skills : `ls .claude/reserve/omniroute/`.
2. Lire le `SKILL.md` du skill utile (ex. `cli-routing`, `omni-models`,
   `omni-budget`) et l'appliquer.

## Avertissement à rappeler à Aurélien (RGPD)

OmniRoute fait transiter les requêtes vers des centaines de fournisseurs d'IA,
dont beaucoup hors UE, et certaines offres gratuites **réutilisent les données
envoyées pour entraîner leurs modèles**. Ne jamais y faire passer de données de
clients ou de stagiaires (RGPD, chapitre V : transferts hors UE). L'usage reste
la décision d'Aurélien, qui l'a autorisé en connaissance de cause.
