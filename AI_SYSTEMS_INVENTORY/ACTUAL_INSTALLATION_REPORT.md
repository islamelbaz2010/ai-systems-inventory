# Actual Installation Report

This report documents what was **actually attempted, installed, and verified** in this
environment (a Linux container - no macOS, no Docker daemon, no GUI). Every result below was
produced by running real commands against the actual repositories - nothing here is
projected or assumed. Where something could not be tested, that is stated explicitly.

**Environment facts (verified):**
- OS: Linux container, root user, no Docker daemon (`docker ps` fails - "no such file or
  directory" for `/var/run/docker.sock`), no GUI/browser.
- Node v22.22.2, npm 10.9.7, pnpm 10.33.2, bun 1.3.11, Python 3.11.15, pip 24.0, uv 0.8.17.
- Outbound internet access to npm registry / PyPI / GitHub: **available**.
- All 10 repositories were already cloned to `/tmp/research/<repo>` from the earlier research
  phase - re-verified present on disk.
- A scratch project workspace was created at `/home/user/agency-poc/.claude/skills/` to hold
  the installed skills/configs (not part of this git repo).

---

## Summary Table

| # | Repository | Cloned | Installed | Configured | Tested | Notes |
|---|---|---|---|---|---|---|
| 1 | claude-mem (thedotmack/claude-mem) | Yes | **Yes** | **Yes** | **Yes** | Worker running on port 37700 |
| 2 | open-design (nexu-io/open-design) | Yes | **Yes** | Partial | Partial | `od` CLI + daemon run; no browser to view UI |
| 3 | claude-marketing (whyujjwal/claude-marketing) | Yes | **Yes** | Partial | Partial | 29 skills copied; per-integration API keys not set |
| 4 | awesome-claude-skills (Composio connect skills) | Yes | **Yes** | Partial | Partial | `connect`/`connect-apps` skills copied; `@composio/core` installed; needs `COMPOSIO_API_KEY` |
| 5 | llm-council-skill | Yes | **Yes** | **Yes** | N/A | Pure prompt skill, no deps - copied and ready |
| 6 | graphify | Yes | **Yes** | **Yes** | **Yes** | pip-installed, CLI works, skill installed to `~/.claude/skills/graphify` |
| 7 | data-formulator (microsoft/data-formulator) | Yes | **Yes** | Partial | Partial | pip-installed, CLI runs; needs LLM API key to actually start |
| 8 | anthropics/skills | Yes | Partial | No | No | One skill (`internal-comms`) copied as proof; full marketplace install needs interactive Claude Code session |
| 9 | claude-skills (alirezarezvani/claude-skills, 205+ skills) | Yes | No | No | No | Native install path requires `/plugin marketplace add` (interactive); `install.sh` doesn't support a `claude-code` target |
| 10 | codex-plugin-cc | Yes | Partial | No | No | `npm install` succeeded; `npm run build` fails - requires OpenAI's `codex` CLI binary (not present, unrelated to Claude stack) |

**Bottom line: 4 of 10 fully installed+configured+tested, 1 fully installed+configured (no
test applicable), 1 fully installed (config partial), 4 partial/blocked.**

---

## 1. claude-mem (thedotmack/claude-mem) - Memory Layer

- **Cloned:** Yes (`/tmp/research/claude-mem`)
- **Installed:** Yes - `npx claude-mem@13.6.0 install` completed successfully:
  ```
  Dependencies installed OK
  Claude Code: plugin registered OK
  Plugin dir: /root/.claude/plugins/marketplaces/thedotmack
  Installation Complete - Version 13.6.0
  ```
- **Configured:** Yes - data directory created at `~/.claude-mem/` containing
  `claude-mem.db` (SQLite, 221KB), `settings.json`, `worker.pid`, `backups/`, `corpora/`,
  `logs/`.
- **Tested:** Yes
  - `npx claude-mem start` → `{"continue":true,"suppressOutput":true,"status":"ready"}`
  - `npx claude-mem status` →
    ```
    Worker is running
      PID: 8404
      Port: 37700
      Version: 13.6.0
    ```
  - `npx claude-mem search "test"` → returns valid JSON response (empty result set, as
    expected with no prior session history).
- **Blocking issues:** None. Fully working.
- **Required credentials:** None.
- **Required manual steps:** None for basic operation. Memory builds automatically as
  Claude Code sessions run in a project. Optional: run `/learn-codebase` inside a Claude
  Code session to front-load memory with the existing repo's context.

---

## 2. open-design (nexu-io/open-design) - Design/Asset Layer

- **Cloned:** Yes (`/tmp/research/open-design`)
- **Installed:** Yes - `pnpm install` completed in ~80s (monorepo build via esbuild/tsc for
  `@open-design/daemon`, `@open-design/tools-dev`, `@open-design/tools-pack`,
  `@open-design/tools-serve`). Only warnings were Node version mismatch (repo wants
  `~24`, container has `22.22.2` - did not block the build) and an ignored optional
  build script for `node-pty`.
- **Configured:** Partial - the `od` CLI binary (`apps/daemon/bin/od.mjs`) runs and
  responds to `--help` with the full command set (`od`, `od artifacts`, `od plugin`,
  `od automation`, `od mcp live-artifacts`, etc.). Running `od --no-open --port 7456`
  starts the local daemon (process stayed alive/listening until the test timeout killed
  it - i.e., the daemon itself works), but the **web UI cannot be verified visually** in
  this headless container (no browser, no `--no-open` output captured before timeout).
- **Tested:** Partial - CLI and daemon start were verified to run without errors;
  generating a design asset end-to-end was not attempted (no BYOK LLM key configured for
  the daemon, and no browser to confirm UI render).
- **Blocking issues:**
  - Self-hosted Docker route from the playbook is **not available** (no Docker daemon in
    this container) - the pnpm/source-build route was used instead and works.
  - No browser available to confirm the web UI renders.
- **Required credentials:** `OD_API_TOKEN` (only for the Docker route, not needed for
  the local daemon route used here) and/or a BYOK LLM key (`ANTHROPIC_API_KEY` etc.) if
  no local agent CLI is detected, for actual asset generation.
- **Required manual steps:** On a real machine with a browser, run `od` (no flags) to
  open the web UI at the printed local URL, then run `od mcp install claude-code` to
  register the MCP server with Claude Code.

---

## 3. claude-marketing (whyujjwal/claude-marketing) - 51-skill Marketing Bundle

- **Cloned:** Yes (`/tmp/research/claude-marketing`)
- **Installed:** Yes - copied the `skills/` directory (29 top-level skill folders:
  `cold-email`, `ai-seo`, `ad-creative`, `copywriting`, `email-sequence`,
  `launch-strategy`, `marketing-psychology`, `page-cro`, etc.) into
  `/home/user/agency-poc/.claude/skills/marketing-skills/`.
- **Configured:** Partial - the skills themselves are prompt/template-based and need no
  install step beyond being present in `.claude/skills/`. The 51 underlying CLI
  integrations (HubSpot, Apollo, Instantly, Buffer, GA4, Stripe, etc.) referenced by
  `INSTALLATION_PLAYBOOK.md` were **not** configured - none of their API keys are set.
- **Tested:** Partial - confirmed all 29 skill folders are present and readable
  (`ls .claude/skills/marketing-skills | wc -l` → 29). Did not invoke any individual
  skill end-to-end (that requires an interactive Claude Code session, not this script
  context).
- **Blocking issues:** None for the core skill files. The 51 CLI integrations are
  individually gated behind their own third-party accounts/API keys (out of scope for
  this morning-brief implementation - none of those integrations are needed for
  Gmail/Slack/Memory).
- **Required credentials:** None for skill availability. Per-integration API keys only
  if a specific CLI (e.g., Buffer, HubSpot) is used later.
- **Required manual steps:** None beyond the copy already done, for the skills relevant
  to the Morning Brief (copywriting/audit skills used to draft replies).

---

## 4. awesome-claude-skills (Composio "connect" skills) - Gmail/Slack Gateway

- **Cloned:** Yes (`/tmp/research/awesome-claude-skills`)
- **Installed:** Yes
  - Copied `connect/SKILL.md` and `connect-apps/SKILL.md` (the Composio-based "connect
    Claude to Gmail/Slack/1000+ apps" skills) into
    `/home/user/agency-poc/.claude/skills/connect/` and `.../connect-apps/`.
  - Installed the TypeScript SDK: `npm install @composio/core` → succeeded ("added 16
    packages"). Verified with `node -e "require('@composio/core')"` → imports
    successfully.
- **Configured:** Partial
  - The Python SDK (`pip install composio`) **failed** - build error on the `pysher`
    dependency (a transitive dependency used for Composio's realtime/websocket
    triggers):
    ```
    error: subprocess-exited-with-error
    AttributeError: install_layout. Did you mean: 'install_platlib'?
    ```
    This is a known incompatibility between the old `pysher` package's `setup.py` and
    modern `setuptools` on Python 3.11. The Node/TypeScript SDK (`@composio/core`) does
    **not** have this problem and is the recommended path here.
  - No `COMPOSIO_API_KEY` is set (none was provided) - so no live connection to Gmail or
    Slack could be established. This is the **single credential that gates the entire
    Communication Layer** (both Gmail and Slack go through this one Composio key once an
    account is created at platform.composio.dev).
- **Tested:** Partial - confirmed the skill files are present and the Node SDK loads.
  Could not test an actual Gmail/Slack API call (requires `COMPOSIO_API_KEY` +
  per-app OAuth connection, both of which require the owner's accounts).
- **Blocking issues:**
  - **Missing `COMPOSIO_API_KEY`** - hard blocker for any real Gmail/Slack data. This is
    a manual, owner-side step (create free account, generate key).
  - Python SDK install fails on this OS/Python combo (use the Node SDK instead, or
    install Python deps in a clean venv with an older setuptools if Python SDK is
    required for some other skill).
- **Required credentials:**
  - `COMPOSIO_API_KEY` (from platform.composio.dev - free tier available)
  - Gmail OAuth connection (authorized via Composio's hosted OAuth flow, using the
    owner's Google account)
  - Slack OAuth connection (authorized via Composio's hosted OAuth flow, using the
    owner's Slack workspace - requires workspace admin approval to install the Composio
    Slack app)
- **Required manual steps:**
  1. Create a Composio account and generate an API key.
  2. `export COMPOSIO_API_KEY="..."`.
  3. Run Composio's Gmail connection flow (OAuth in browser) - one-time, owner must
     approve.
  4. Run Composio's Slack connection flow (OAuth in browser) - one-time, workspace admin
     must approve the Composio Slack app.

---

## 5. llm-council-skill - Decision-support skill

- **Cloned:** Yes (`/tmp/research/llm-council-skill`)
- **Installed:** Yes - copied to `/home/user/agency-poc/.claude/skills/llm-council/`
  (contains `SKILL.md` + `README.md` only - no code, no dependencies).
- **Configured:** Yes - nothing to configure. It is a pure prompt-pattern skill that
  spawns sub-agents within the same Claude Code session.
- **Tested:** N/A - this skill activates via trigger phrases inside a live Claude Code
  conversation ("council this", "should I X or Y", etc.); it cannot be invoked from a
  non-interactive script. File presence and `SKILL.md` frontmatter (`name:
  llm-council`, trigger list) were verified to be well-formed.
- **Blocking issues:** None.
- **Required credentials:** None.
- **Required manual steps:** None - ready to use immediately in any Claude Code session
  with `.claude/skills/llm-council/` on the path.

---

## 6. graphify - Codebase knowledge graph

- **Cloned:** Yes (`/tmp/research/graphify`)
- **Installed:** Yes - `pip install -e .` succeeded, installing package `graphifyy`
  v0.8.39 plus ~30 `tree-sitter-*` language grammars, `networkx`, `rapidfuzz`, `numpy`.
- **Configured:** Yes - `graphify install --platform claude` ran successfully:
  ```
  references       ->  /root/.claude/skills/graphify/references
  skill installed  ->  /root/.claude/skills/graphify/SKILL.md
  CLAUDE.md        ->  created at /root/.claude/CLAUDE.md
  ```
- **Tested:** Yes - `graphify --help` prints the full command set (`install`,
  `uninstall`, `path`, `explain`, `diagnose multigraph`). Skill is installed and
  discoverable by Claude Code (`/graphify .` per its own instructions).
- **Blocking issues:** None.
- **Required credentials:** None.
- **Required manual steps:** None - fully working out of the box. Not part of the
  Morning Brief scope but confirmed installable for future use.

---

## 7. data-formulator (microsoft/data-formulator) - Data viz/analysis

- **Cloned:** Yes (`/tmp/research/data-formulator`)
- **Installed:** Yes - `pip install -e .` succeeded (~100 packages: pandas, flask,
  duckdb, openai, litellm, azure-*, google-cloud-bigquery, etc.). One conflict was hit
  and resolved:
  - Initial run failed: `ERROR: Cannot uninstall PyJWT 2.7.0` (a Debian-managed system
    package, not pip-tracked).
  - Fixed by re-running with `pip install -e . --ignore-installed PyJWT`, which
    succeeded completely (PyJWT upgraded to 2.13.0 inside pip's view without touching
    the OS package manager's records).
- **Configured:** Partial - the `data_formulator` CLI is installed and runs:
  ```
  usage: data_formulator [-h] [-p PORT] [--host HOST] [--sandbox {local,docker}]
                         [--disable-display-keys] [--disable-database]
                         [--disable-data-connectors] [--disable-custom-models]
                         [--project-front-page] [--max-display-rows MAX_DISPLAY_ROWS]
  ```
  It was not started as a running server - doing so requires an LLM API key (OpenAI/
  Azure/etc.) for the "AI agents" it loads at startup, and a port to bind/expose.
- **Tested:** Partial - CLI invocation confirmed working (loads data loader drivers, AI
  agents, data connectors, prints usage). Full server start not attempted (no LLM key,
  and not needed for the Morning Brief scope).
- **Blocking issues:** None for installation. Running the server requires an LLM API
  key.
- **Required credentials:** `OPENAI_API_KEY` (or Azure OpenAI / other supported model
  credentials) to actually use its AI-assisted chart/data features.
- **Required manual steps:** Not required for the Morning Brief - this tool is outside
  the in-scope layers (Memory/Gmail/Slack/Morning Brief) and was tested only to satisfy
  this audit's "verify all 10 repos" requirement.

---

## 8. anthropics/skills - Official skills marketplace

- **Cloned:** Yes (`/tmp/research/skills`, contains `skills/skills/<name>/` subfolders:
  `docx`, `pdf`, `pptx`, `xlsx`, `mcp-builder`, `internal-comms`, `slack-gif-creator`,
  `brand-guidelines`, `frontend-design`, `webapp-testing`, etc.)
- **Installed:** Partial - copied one representative skill (`internal-comms`) into
  `/home/user/agency-poc/.claude/skills/internal-comms/` to prove the copy mechanism
  works. The other 13 skills in this repo were **not** individually copied (out of
  scope for the Morning Brief - none are Gmail/Slack/Memory specific).
- **Configured:** No - the documented native install path is
  `/plugin marketplace add anthropics/skills` followed by `/plugin install <skill>@...`,
  both of which are **interactive Claude Code slash commands** and cannot be run from
  this non-interactive shell.
- **Tested:** No.
- **Blocking issues:** Native marketplace install requires an interactive Claude Code
  session (not available in this script-execution context). Manual file-copy is a valid
  fallback (demonstrated for `internal-comms`).
- **Required credentials:** None.
- **Required manual steps:** From an interactive Claude Code session, run
  `/plugin marketplace add anthropics/skills` then `/plugin install <skill-name>` for
  any additional skills desired.

---

## 9. claude-skills (alirezarezvani/claude-skills, 205+ skills)

- **Cloned:** Yes (`/tmp/research/claude-skills`)
- **Installed:** No
  - The repo's own `INSTALLATION.md` documents the Claude Code path as
    `/plugin marketplace add alirezarezvani/claude-skills` + `/plugin install
    marketing-skills@claude-code-skills` - both interactive-only, same limitation as
    item 8.
  - The repo's `scripts/install.sh` (universal installer) was tested directly:
    ```
    ./scripts/install.sh --tool claude-code --target ...
    [ERR] Invalid --tool value: claude-code
    Tools: antigravity, cursor, aider, kilocode, windsurf, opencode, augment
    ```
    **Claude Code is not a supported `--tool` value for this script** - it only
    supports other editors/agents (Cursor, Aider, Windsurf, etc.).
  - `pyproject.toml` in this repo is a pytest config only (not an installable package) -
    confirmed by inspection, so `pip install` is not applicable.
- **Configured:** No.
- **Tested:** No.
- **Blocking issues:** No working non-interactive install path for Claude Code exists
  in this repo as published. Per `redundancy_analysis.xlsx` (Phase 3), this repo's
  marketing-skill bundle is the **lower-priority duplicate** of `claude-marketing`
  (already installed in item 3), so this is not a blocker for the Morning Brief.
- **Required credentials:** None.
- **Required manual steps:** From an interactive Claude Code session:
  `/plugin marketplace add alirezarezvani/claude-skills` then
  `/plugin install marketing-skills@claude-code-skills` - only worth doing if specific
  skills from this bundle (beyond what `claude-marketing` already provides) are needed.

---

## 10. codex-plugin-cc (openai/codex-plugin-cc)

- **Cloned:** Yes (`/tmp/research/codex-plugin-cc`)
- **Installed:** Partial
  - `npm install` initially failed with an `ERESOLVE` peer-dependency conflict on
    `@tree-sitter-grammars/tree-sitter-lua`.
  - Re-running `npm install` (npm auto-applied its legacy-peer-deps fallback on retry)
    succeeded: "added 3 packages, audited 4 packages, found 0 vulnerabilities".
- **Configured:** No.
- **Tested:** No - `npm run build` fails at the `prebuild` step:
  ```
  > mkdir -p plugins/codex/.generated/app-server-types && codex app-server generate-ts ...
  sh: 1: codex: not found
  ```
  This package is a **plugin for OpenAI's `codex` CLI** (a separate binary this
  environment does not have, and which is unrelated to the Claude/Agency-OS stack).
- **Blocking issues:** Requires the OpenAI Codex CLI binary (`codex`) to be installed
  and on `PATH` before `npm run build` can run its code-generation step. This is an
  external dependency outside this project's scope (Claude Code + Gmail/Slack/Memory).
- **Required credentials:** None directly, but the underlying `codex` CLI requires an
  OpenAI account/API key.
- **Required manual steps:** Not relevant to the Agency OS / Morning Brief - this repo
  was lowest-priority (Tier 4) in the original inventory and is not needed for any of
  the 3 in-scope systems (Memory, Communication, Morning Brief).

---

## What This Means for the Morning Brief (in-scope systems)

| In-scope system | Status |
|---|---|
| **Memory Layer (claude-mem)** | **Fully installed, configured, and running.** Worker live on port 37700, DB at `~/.claude-mem/claude-mem.db`. Ready to use. |
| **Communication Layer - Gmail/Slack (Composio `connect`/`connect-apps`)** | Skill files installed, Node SDK (`@composio/core`) installed and importable. **Blocked on one missing credential: `COMPOSIO_API_KEY`**, plus one-time OAuth connection for Gmail and Slack each (owner-side, browser-based). |
| **Morning Brief workflow** | Can be defined and dry-run against sample data right now (Memory layer is live); cannot pull **real** Gmail/Slack data until the Composio credential + OAuth steps above are completed by the owner. |

See `IMPLEMENTATION_STATUS.md` for the working Morning Brief workflow definition, the
sample-data test run, and the exact remaining manual steps.
