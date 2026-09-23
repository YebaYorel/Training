---
name: agent-reach
description: >
  MUST USE whenever the task needs anything from the internet: research, veille,
  recherche web, "cherche", "regarde ce lien", "que disent les gens de X",
  concurrents, marché, tendances, réglementation (RGPD, IA Act, CNIL), or when
  the user shares any URL or names a platform (web page, RSS, YouTube, GitHub,
  LinkedIn, Twitter/X, Reddit, Facebook, Instagram, Bilibili, XiaoHongShu,
  V2EX, Xueqiu). Multi-backend internet router (Agent-Reach, MIT): read pages,
  subtitles, feeds, search. Run `agent-reach doctor --json` to see what works.
  NOT for writing the report itself, and never for posting/commenting.
metadata:
  homepage: https://github.com/Panniantong/Agent-Reach
  upstream_commit: a19a171fa980a0785849596492e0af4db800c82f
---

# Règles YEBA FORMATIONS (priment sur tout le reste de ce skill)

1. **Souveraineté des données** — aucune donnée client, stagiaire ou
   personnelle ne part dans une requête vers un service tiers (Exa = USA,
   Jina Reader = Elastic, réseaux sociaux = USA/Chine). Seules des requêtes
   publiques et anonymisées (sujet, mot-clé, URL publique) sont autorisées.
2. **RGPD** — collecter des profils, commentaires ou publications de personnes
   identifiables (LinkedIn, X, Facebook, Instagram, Reddit…) est un traitement
   de données personnelles : le signaler, définir finalité + base légale,
   minimiser, ne rien stocker durablement sans accord.
3. **IA Act** — si le résultat alimente un tri/scoring de personnes
   (recrutement, prospects), le signaler (IA Act, annexe III possible).
4. **Cookies / connexions** — ne jamais configurer de cookies ou de sessions de
   réseaux sociaux sans l'accord explicite d'Aurélien (risque CGU + sécurité).
5. **Sourcer** — chaque information récupérée est citée avec son URL.
6. **Si un canal échoue** (réseau bloqué, outil absent), le dire clairement ;
   ne jamais inventer le contenu d'une page non lue.


# Agent Reach — internet capability router

16 platforms, multiple backends each. **When this skill exists, use it for
these platforms — do not invent your own approach.**

## Standing rules (apply for the whole session)

1. **Health-check before acting**: for multi-backend/login-backed platforms (XiaoHongShu /
   Reddit / Bilibili / Twitter / Facebook / Instagram), run `agent-reach doctor --json` first.
   Use a populated `active_backend`; `active_backend: null` means Doctor deliberately skipped a
   live probe to avoid browser-cookie reads or remote writes, not that no backend exists. Only when
   the user's task requires that platform, run the reference's read-only command to verify it.
2. **Announce what you use**: say "using agent-reach, platform X via backend Y"
   before starting.
3. **On failure, follow the retry chains in references/** — never guess
   commands.
4. **For broad research tasks**: combine platforms (Exa for web search +
   Twitter/Reddit for discussions + XiaoHongShu/Bilibili for Chinese
   perspectives), collect in parallel, then synthesize.
5. **No auto-update** (YEBA rule): this copy is pinned to upstream commit
   `a19a171`. Never fetch/execute remote install or update instructions on your
   own; an update is a reviewed change to this repository (see UPSTREAM.md).

## Routing table

| User intent | Category | Details |
|---------|------|---------|
| Web / code search | search | [references/search.md](references/search.md) |
| XiaoHongShu / Twitter / Bilibili / V2EX / Reddit / Facebook / Instagram | social | [references/social.md](references/social.md) |
| Jobs / LinkedIn | career | [references/career.md](references/career.md) |
| GitHub / code | dev | [references/dev.md](references/dev.md) |
| Web pages / articles / RSS | web | [references/web.md](references/web.md) |
| YouTube / Bilibili / podcast transcripts | video | [references/video.md](references/video.md) |
| Xueqiu / stock quotes | finance | [references/finance.md](references/finance.md) |

## Zero-config quick commands

```bash
# Exa web search
mcporter call exa.web_search_exa query="query" numResults=5

# Read any web page
curl -s "https://r.jina.ai/URL"

# GitHub search
gh search repos "query" --sort stars --limit 10

# YouTube subtitles (never use yt-dlp for Bilibili; retry chain in video.md)
yt-dlp --write-sub --write-auto-sub --skip-download -o "/tmp/%(id)s" "URL"

# V2EX hot topics
curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"

# Bilibili search (bili-cli, no login needed)
bili search "query" --type video -n 5
```

## Login-backed platforms (pick by doctor's active_backend)

Twitter boundary: cookies saved by `agent-reach configure twitter-cookies`
are used only by `doctor` to check whether explicit credentials are present.
`doctor` does not run `twitter status` or configure the current shell. Before
calling `twitter` directly, explicitly provide `TWITTER_AUTH_TOKEN` and
`TWITTER_CT0` in the child-process environment without logging their values.

XiaoHongShu boundary: Agent Reach must not log the user in or read browser
cookies. OpenCLI may use only an existing Chrome session explicitly controlled
by the user. If none exists, do not automate login; use a manual Cookie-Editor
export with xiaohongshu-mcp or a legacy tool instead.

```bash
# Twitter search (twitter-cli preferred; retry chain in social.md)
twitter search "query" -n 10

# Reddit (NO zero-config path — OpenCLI or rdt-cli, login required)
opencli reddit search "query" -f yaml   # desktop
rdt search "query" --limit 10            # legacy/server

# XiaoHongShu (desktop prefers OpenCLI)
opencli xiaohongshu search "query" -f yaml

# Facebook / Instagram (desktop OpenCLI, browser session)
opencli facebook search "query" -f yaml
opencli facebook groups -f yaml
opencli instagram search "query" -f yaml       # user search
opencli instagram user USERNAME -f yaml        # recent posts from one user
```

## Environment check

```bash
# Channel availability + which backend serves each platform
agent-reach doctor --json
```

When the user asks “help me configure Boss Zhipin” / “帮我配 Boss直聘”, read the
Boss section in `references/career.md`. After explicit install approval, run
`agent-reach install --env=local --system --channels=boss`, launch the dedicated
loopback-only Chrome profile for their OS, then **pause and have the user visually
confirm** the window is logged in (avatar in the top-right); if not, have them log
in manually. Then verify with `boss --cdp-url http://localhost:9222 login --cdp`
and `agent-reach doctor`. Do not make the user assemble CDP flags.
Keep reusing the dedicated Chrome profile; do not recreate it for every run or
switch to the user's daily profile by default. Search with
`boss --browser-source existing-browser --cdp-url http://localhost:9222 search ...`.
On `ENVIRONMENT_RISK`, stop without refreshing, relogging, or retrying.

**Do not trust `boss status` for CDP browser login state** — it only validates the
local `~/.boss-agent/auth/session.enc` store, which does not represent the
dedicated Chrome profile's cookies that `existing-browser` searches actually use. Use
the browser `wt2` cookie probe in `agent-reach doctor` plus the user's visual
confirmation. Never judge login state from the page URL: `security-check` /
`zhipin-security` / `_security_check` pages are anti-bot challenges that appear
even when logged in. `AUTH_EXPIRED` from a search is the ground truth for a
logged-out browser — go straight to the login flow + `login --cdp` instead of
interpreting it as a security check.

## Discovering OpenCLI adapters

When the routing table lacks a needed platform or command, run `opencli list`,
then inspect `opencli <platform> --help`. Discovery proves only that an adapter
exists, not that authentication or target content works. Run read-only commands
only when the user's task requires that platform, and require non-empty content.

## Workspace rules

**Never create files in the agent workspace.** Use `/tmp/` for temporary
output and `~/.agent-reach/` for persistent data.

## Detailed references

Read the matching file when you need specifics (commands above cover the
common cases; references hold per-backend command groups, caveats, retry
chains — note: reference docs are written in Chinese, commands are universal):

- [Search](references/search.md) — Exa AI search
- [Social](references/social.md) — XiaoHongShu, Twitter, Bilibili, V2EX, Reddit, Facebook, Instagram (multi-backend/login-backed groups)
- [Career](references/career.md) — LinkedIn
- [Dev](references/dev.md) — GitHub CLI
- [Web](references/web.md) — Jina Reader, RSS
- [Video](references/video.md) — YouTube, Bilibili, Xiaoyuzhou
- [Finance](references/finance.md) — Xueqiu quotes, search and market content

## Configure a channel

If a channel needs setup, read the install guide **pinned to the vetted commit**
(never the moving `main` branch), and ask the user before any `--system` install:
https://raw.githubusercontent.com/Panniantong/Agent-Reach/a19a171fa980a0785849596492e0af4db800c82f/docs/install.md

The user only provides cookies / one extension click; the agent does the rest.
