# Compétence « watch » : provenance et règles YEBA

- **Source** : https://github.com/bradautomates/claude-video, dossier `skills/watch/`, version 0.3.2,
  commit `03ceb42f7fa2c4439aca01752118044baabffb8f` (25/09/2026), copiée le 11/11/2026.
- **Auteur et licence** : Bradley Bonanno, licence MIT (fichier `LICENSE` ci-joint, à conserver avec la copie).
- **Fichiers** : `SKILL.md` et `scripts/*.py` copiés à l'identique (`build-skill.sh`, outil de développement, non copié).
- **Relu avant installation (11/11/2026)** : commandes lancées sans shell, dossiers de travail isolés, cookies
  uniquement sur demande, aucune télémétrie. Google (Gemini), Groq et OpenAI ne sont contactés que si on configure
  leur clé et leur moteur : ce que la configuration YEBA interdit.

## Configuration YEBA, posée à chaque démarrage par `.claude/hooks/session-start.sh`

`WATCH_ENGINE="local"`, `WATCH_WHISPER_BACKEND="none"` (ou `whisperx`, local, si on l'installe), `WATCH_DETAIL="balanced"`,
dans `~/.config/watch/.env` (droits 0600). Règles d'usage RGPD / IA Act : voir `CLAUDE.md` à la racine du dépôt.

## Mettre à jour

`bash .claude/skills/watch/mettre-a-jour.sh`, puis relire le diff avant de committer (nouvelles adresses réseau ?
nouveau moteur proposé par défaut ?).
