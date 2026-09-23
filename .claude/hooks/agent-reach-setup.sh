#!/usr/bin/env bash
# SessionStart : installe (ou réutilise) le CLI Agent-Reach, épinglé sur un
# commit vérifié. Idempotent, ne bloque jamais la session en cas d'échec.
set -u
COMMIT="a19a171fa980a0785849596492e0af4db800c82f"
VENV="${HOME}/.agent-reach/venv"
BIN="${VENV}/bin"

if [ ! -x "${BIN}/agent-reach" ] || ! grep -q "${COMMIT}" "${VENV}/.commit" 2>/dev/null; then
  mkdir -p "${HOME}/.agent-reach"
  { python3 -m venv "${VENV}" \
    && "${BIN}/pip" install -q --disable-pip-version-check \
         "git+https://github.com/Panniantong/Agent-Reach.git@${COMMIT}" \
    && echo "${COMMIT}" > "${VENV}/.commit"; } >/dev/null 2>&1 \
    || { echo "Agent-Reach : installation impossible (réseau ?). Le skill reste lisible mais les commandes échoueront."; exit 0; }
fi

# yt-dlp a besoin d'un runtime JS pour YouTube (recommandation de `agent-reach doctor`)
if command -v node >/dev/null 2>&1; then
  mkdir -p "${HOME}/.config/yt-dlp"
  grep -qxF -- '--js-runtimes node' "${HOME}/.config/yt-dlp/config" 2>/dev/null \
    || printf '%s\n' '--js-runtimes node' >> "${HOME}/.config/yt-dlp/config"
fi

# Rendre agent-reach / yt-dlp disponibles dans les commandes Bash de la session
[ -n "${CLAUDE_ENV_FILE:-}" ] && echo "export PATH=\"${BIN}:\$PATH\"" >> "${CLAUDE_ENV_FILE}"
echo "Agent-Reach prêt (${BIN}/agent-reach, commit ${COMMIT:0:7}). Vérifier les canaux : agent-reach doctor"
exit 0
