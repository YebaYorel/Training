# Compétence « learnharness » : provenance et règles YEBA

Fichier propre à YEBA FORMATIONS. Il ne fait pas partie de l'œuvre copiée et ne la modifie pas.

- **Source** : https://github.com/amosblomqvist/learnharness, dossier `skills/learnharness/`, application en version
  0.6.0, commit `a63664767ebdd7e5af08f7f501b720e02b2ddc32` (11/11/2026), copiée le 11/11/2026.
- **Auteur et licence** : Amos Blomqvist, licence **AGPL-3.0-only** (fichier `LICENSE` ci-joint, à conserver avec la
  copie). Les fichiers `SKILL.md`, `LICENSE`, `references/` et `scripts/` sont copiés **à l'identique** : en cas de
  modification, il faudrait l'indiquer et garder l'AGPL pour la version modifiée (art. 5). Ce `PROVENANCE.md` et
  `mettre-a-jour.sh` sont des fichiers YEBA séparés.
- **Relu avant installation (11/11/2026)** : trois scripts Python, bibliothèque standard seulement, aucun appel réseau,
  aucune écriture (lecture seule, chemins confinés au dossier de données, contenu HTML neutralisé).
- **Non copié** : l'application elle-même (Electron + Next.js, 1 255 fichiers, 21 Mo). Elle ne tourne pas dans une
  session Claude Code ; elle s'installe sur l'ordinateur depuis https://learnharness.ai ou les « Releases » GitHub. La
  seconde compétence de l'amont, `learnharness-plugins`, n'est pas copiée non plus : elle renvoie à la documentation
  du dépôt complet et ne sert qu'à programmer des extensions.

## À quoi elle sert chez YEBA

Lire, sans jamais le modifier, l'historique d'apprentissage enregistré par l'application LearnHarness : séances,
réponses, niveau de confiance, raisonnements à voix haute, graphe des notions. Exemple : Aurélien se forme à l'IA Act
avec LearnHarness ; Claude lit son historique pour adapter une explication ou un support à ce qu'il maîtrise déjà.

Elle ne sert que là où se trouvent les données : une session Claude Code ouverte sur l'ordinateur où l'application
est installée, ou une copie du dossier de données passée avec `--data-dir`. Dans une session cloud, ce dossier
n'existe pas.

## Garde-fous YEBA (rappel de `CLAUDE.md`)

- **RGPD** : un historique d'apprentissage est un profil personnel (réponses, confiance, raisonnements). Lire
  seulement ce qui sert la demande. Aucun historique de stagiaire sans base légale, information préalable et analyse
  d'impact (AIPD).
- **IA Act** : utiliser LearnHarness avec des stagiaires pour évaluer leurs acquis ou piloter leur parcours relève
  des systèmes à haut risque (annexe III, point 3, b). Changer ainsi la destination de l'outil peut faire de YEBA son
  « fournisseur », avec toutes les obligations correspondantes (art. 25, § 1, c). Usage personnel d'Aurélien
  uniquement, sauf étude de conformité préalable.
- **Souveraineté** : l'application envoie le contexte au fournisseur de modèle choisi. Elle propose une dictée par
  Deepgram (États-Unis) et une recherche web par Tavily, Brave, Exa, Firecrawl ou Ollama, des services hébergés hors
  UE. Réglage YEBA : un modèle local, ou un point d'accès européen compatible OpenAI (à tester) ; dictée et recherche
  web désactivées dès qu'une donnée personnelle de tiers est en jeu.

## Mettre à jour

`bash .claude/skills/learnharness/mettre-a-jour.sh`, puis relire le diff avant de committer : nouveaux imports,
écritures ou appels réseau dans `scripts/` ? Format de données qui change ?
