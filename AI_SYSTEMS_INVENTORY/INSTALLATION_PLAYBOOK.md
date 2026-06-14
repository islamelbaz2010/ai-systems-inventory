# Installation Playbook

Per-repository setup guide for the recommended tools in this inventory, ordered to match
`installation_priority.xlsx` (highest-priority repos first). Each section covers
Installation, Dependencies, Configuration, Environment Variables, Verification Steps,
Troubleshooting, and Maintenance Notes.

---

## 1. claude-marketing (whyujjwal/claude-marketing)

**Why first:** Highest combined priority score (51-skill marketing bundle = 6.0) - the fastest
path to marketing/automation leverage for a business owner.

### Installation
```bash
cd your-project/
git clone https://github.com/whyujjwal/claude-marketing.git .claude-marketing
mkdir -p .claude/commands
cp .claude-marketing/.claude/commands/* .claude/commands/
cp -r .claude-marketing/skills .claude/skills
```

### Dependencies
- Node.js 18+ (required for the 51 CLI integrations; the CLIs themselves are zero-dependency)
- No Python dependencies

### Configuration
- Each CLI integration lives under `.claude-marketing/cli/<tool>` - review `README.md` per tool
  before wiring it into a workflow.
- Start with 1-2 integrations (e.g. cold-email + SEO audit) rather than configuring all 51 at once.

### Environment Variables
Set one variable per connected platform you actually use, in the convention `{TOOL_NAME}_API_KEY`:
- `HUBSPOT_API_KEY`, `APOLLO_API_KEY`, `INSTANTLY_API_KEY`, `BUFFER_API_KEY`, `GA4_API_KEY`, `STRIPE_API_KEY`, etc.
Store these in a local `.env` (never commit it) and load via your shell profile or a dotenv loader.

### Verification Steps
1. Run `/cold-email+` (or any installed skill) and confirm it loads without missing-dependency errors.
2. Test one CLI integration end-to-end (e.g. `buffer` post creation) with a sandbox/test account first.
3. Confirm `.claude/commands` contains the expected slash commands (`ls .claude/commands`).

### Troubleshooting
- "Command not found" → re-run the `cp` steps; commands must live under `.claude/commands` in
  the *current* project, not globally.
- API auth errors → double-check the env var naming convention (`{TOOL_NAME}_API_KEY`) exactly
  matches what each CLI script expects (check the CLI's own `--help`).
- Node version errors → confirm `node -v` is 18+; use `nvm install 18` if needed.

### Maintenance Notes
- This is a **snapshot release** (Feb 2026, no ongoing updates) - pin the commit you cloned and
  periodically check the upstream repo for a maintained fork before depending on it long-term.
- Budget 1-2 hours for initial multi-CLI configuration; do this once, not per-project.

---

## 2. open-design (nexu-io/open-design)

**Why second:** Highest single-item priority (5.8) - local-first design platform that produces
HTML/video/deck/image assets and feeds 22+ coding agents.

### Installation
```bash
# Desktop App (recommended, zero config)
# Download from releases page for your OS (macOS .dmg / Windows / Linux)

# Or self-hosted via Docker
cd deploy
cp .env.example .env
echo "OD_API_TOKEN=$(openssl rand -hex 32)" >> .env
docker compose up -d
# Access at http://localhost:7456
```

### Dependencies
- Docker + Docker Compose (self-hosted route)
- Or: Node 24 + pnpm 10.33 (source build): `pnpm install`
- One-line MCP install once running: `od mcp install <agent>`

### Configuration
- Design systems (150 bundled) live under the app's design-system library - browse and pick
  2-3 relevant to your brand before generating assets.
- BYOK (bring your own key) mode: paste an LLM API key + endpoint in Settings if you don't have
  a local agent CLI (Claude Code, Cursor, Copilot) already installed.

### Environment Variables
- `OD_API_TOKEN` - required for self-hosted Docker deployment (generate with `openssl rand -hex 32`)
- Optional BYOK keys: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `AZURE_*`, `GOOGLE_API_KEY` - only
  needed if no local agent CLI is detected.

### Verification Steps
1. Open `http://localhost:7456` (self-hosted) or launch the desktop app.
2. Run `od mcp install claude-code` and confirm the MCP server appears in Claude Code's MCP list.
3. Generate one test artifact (e.g. a simple landing page) and confirm it renders.

### Troubleshooting
- Docker container won't start → check `.env` was copied from `.env.example` and `OD_API_TOKEN` is set.
- MCP server not detected by agent → restart the agent after running `od mcp install`.
- No local agent detected and no BYOK key set → generation will fail; set a BYOK key or install
  Claude Code/Cursor locally.

### Maintenance Notes
- Extremely active project (v0.10.0, 141 PRs/2 weeks) - update regularly via `docker compose pull`
  or desktop auto-update; review changelogs since the plugin/design-system API surface is evolving fast.

---

## 3. claude-mem (thedotmack/claude-mem)

**Why third:** Persistent cross-session memory (priority 4.8) - compounds the value of every
other tool by giving Claude continuity across sessions.

### Installation
```bash
# Primary (recommended) - Claude Code plugin marketplace
npx claude-mem install

# Gemini CLI support
npx claude-mem install --ide gemini-cli
```

### Dependencies
- Node.js (npx)
- SQLite + Chroma (bundled/managed by the worker service - no manual DB setup)

### Configuration
- Main config file: `~/.claude-mem/settings.json` (auto-created with sensible defaults on first run)
- Adjust retention/compression settings here if memory grows large.

### Environment Variables
- `DO_NOT_TRACK` - set to disable telemetry/observation-compression calls if privacy is a concern.
- Use `<private>` tags in conversation to exclude sensitive content from memory compression.

### Verification Steps
1. After install, restart Claude Code and run a short session, then start a new session and
   confirm prior context is retrievable via the `mem-search` / `search` MCP tool.
2. Open the web viewer at `http://localhost:37777` and confirm the memory stream populates.
3. Check `~/.claude-mem/settings.json` exists.

### Troubleshooting
- Stale worker process / port conflicts → v13.5.6+ self-heals via PID liveness checks; if stuck,
  kill the process on port 37777 and restart Claude Code.
- "Ghost" or fabricated memories → v13.6.0+ includes fabrication detection; update to latest if
  you see hallucinated observations.

### Maintenance Notes
- Very active (daily releases) - run `npx claude-mem install` periodically to pick up the latest
  worker fixes. The 16 companion skills (standup, weekly-digest, etc.) are optional - install
  incrementally as needed.

---

## 4. claude-skills (alirezarezvani/claude-skills)

**Why fourth:** Largest strategy/operations library (345 skills) - install bundles incrementally,
starting with the c-level/executive entry point.

### Installation
```bash
/plugin marketplace add alirezarezvani/claude-skills
/plugin install c-level-skills@claude-code-skills        # 66 skills - start here
/plugin install marketing-skills@claude-code-skills      # 46 skills
/plugin install engineering-skills@claude-code-skills    # 51 skills
/plugin install engineering-advanced-skills@claude-code-skills  # 78 advanced skills
```

### Dependencies
- None - all 579 Python tools are stdlib-only, zero `pip install` required.

### Configuration
- No global config needed. Each skill is self-contained under its `SKILL.md`.
- For non-Claude-Code agents: use `./scripts/install.sh --tool <name>` (Cursor, Aider, Windsurf,
  Kilo Code) or the dedicated installer (`codex-install.sh`, `gemini-install.sh`, `vibe-install.sh`).

### Environment Variables
- None required for core skills.

### Verification Steps
1. `/plugin list` and confirm the installed bundles appear.
2. Invoke one skill from each bundle (e.g. `/ceo-advisor`, `/seo-audit` would come from
   marketing-skills) and confirm it responds.
3. Run `--help` on any bundled Python tool to confirm stdlib-only execution.

### Troubleshooting
- Plugin not found after `marketplace add` → run `/plugin marketplace update alirezarezvani/claude-skills`.
- Skill conflicts with claude-marketing (overlapping marketing skills) → see `redundancy_analysis.xlsx`;
  prefer claude-marketing's versions for SEO/cold-email, claude-skills for strategy/pricing.

### Maintenance Notes
- Active release cycle (v2.9.0+, semantic versioning) - re-run `/plugin marketplace update` monthly.
- Run the included `engineering/skill-security-auditor` skill before installing additional
  third-party skill bundles into the same project.

---

## 5. awesome-claude-skills (ComposioHQ/awesome-claude-skills)

**Why fifth:** Connects Claude to 832 SaaS apps (CRM, email, Slack, GitHub, Notion, Stripe,
Shopify) - the automation backbone once core skills are in place.

### Installation
```bash
# Install Composio core
pip install composio

# Claude Code native plugin
claude --plugin-dir ./connect-apps-plugin

# Authenticate
/connect-apps:setup   # paste API key from dashboard.composio.dev
```

### Dependencies
- Python (for `pip install composio`)
- A free or paid Composio account (dashboard.composio.dev)

### Configuration
- After `/connect-apps:setup`, use `/connect-apps:list` (or equivalent) to see which app
  integrations are available, then enable only the ones you actively use (Gmail, Slack,
  GitHub, Notion, Stripe, Shopify, Google Sheets/Drive/Airtable/Dropbox first).
- The 4 official Anthropic document skills (docx/pdf/pptx/xlsx) bundled here are duplicates -
  skip them and use `anthropics/skills` instead (see redundancy_analysis.xlsx).

### Environment Variables
- `COMPOSIO_API_KEY` - obtained from dashboard.composio.dev, set during `/connect-apps:setup`.
- Per-app OAuth tokens are managed by Composio after you authorize each app in its dashboard.

### Verification Steps
1. `/connect-apps:setup` completes without error and lists connected apps.
2. Run one automation (e.g. "list my unread Gmail" or "create a Notion page") and confirm it executes.
3. Confirm document skills are NOT duplicated - if both this and anthropics/skills are installed,
   verify only one docx/pdf/pptx/xlsx skill set is active.

### Troubleshooting
- OAuth/auth failures → re-authorize the specific app in the Composio dashboard; tokens expire
  periodically.
- "Skill not found" for community skills → installation varies per skill (copy folder / npm
  install / git clone+symlink) - check that specific skill's README.

### Maintenance Notes
- Composio is a vendor dependency - monitor for pricing/API changes. Community skills vary in
  quality; prefer the official Anthropic and Composio-maintained entries.

---

## 6. llm-council-skill (tenfoldmarc/llm-council-skill)

**Why sixth:** Single-file, near-zero-friction decision-support tool (priority 4.6) for
high-stakes business decisions.

### Installation
```bash
git clone https://github.com/tenfoldmarc/llm-council-skill ~/.claude/skills/llm-council
```
Then restart Claude Code.

### Dependencies
- None beyond Claude Code itself (single SKILL.md file).

### Configuration
- No configuration required. Optional: review the SKILL.md to adjust the 5 advisor personas
  to match your industry/decision domains.

### Environment Variables
- None.

### Verification Steps
1. Restart Claude Code, then invoke the skill (e.g. ask Claude to "run an LLM Council review of
   this decision").
2. Confirm it produces 5 distinct advisor perspectives + anonymous peer review + chairman synthesis.

### Troubleshooting
- Skill not triggering → confirm the file landed at `~/.claude/skills/llm-council/SKILL.md` and
  Claude Code was fully restarted (not just reloaded).

### Maintenance Notes
- Community snapshot (v1.0, single file) - low maintenance burden, but no upstream updates
  expected. Re-clone only if you customize the personas and want to merge upstream improvements.

---

## 7. anthropics/skills (anthropics/skills)

**Why seventh:** Official, highest-quality reference skills (docx/pdf/pptx/xlsx, mcp-builder,
skill-creator) - lower business-impact priority but foundational for building everything else.

### Installation
```bash
/plugin marketplace add anthropics/skills
```
Then install:
- `document-skills@anthropic-agent-skills` (docx/pdf/pptx/xlsx - production document tools)
- `example-skills@anthropic-agent-skills` (skill-creator, mcp-builder, web-artifacts-builder, etc.)

### Dependencies
- None beyond Claude Code plugin marketplace support.

### Configuration
- No configuration required - these are reference implementations that work out of the box.

### Environment Variables
- None.

### Verification Steps
1. `/plugin list` shows both `document-skills` and `example-skills`.
2. Ask Claude to generate a `.docx` or `.xlsx` file and confirm the document-skills path is used.
3. Run `skill-creator` once to confirm it scaffolds a new SKILL.md correctly.

### Troubleshooting
- Conflicts with awesome-claude-skills' duplicated docx/pdf/pptx/xlsx skills → uninstall/disable
  the awesome-claude-skills copies (see redundancy_analysis.xlsx, Phase 3).

### Maintenance Notes
- Anthropic-maintained, Apache 2.0 - update via `/plugin marketplace update anthropics/skills`
  whenever the Agent Skills spec changes. This is the canonical reference - prefer it over any
  third-party copy.

---

## 8. graphify (safishamsi/graphify)

**Why eighth:** Knowledge-graph extraction for codebases - high AI-workflow value but more
relevant to engineering-heavy operations than day-to-day business tasks.

### Installation
```bash
# Recommended (uv puts graphify on PATH automatically)
uv tool install graphifyy

# Alternatives
pipx install graphifyy
pip install graphifyy

# Register with Claude Code
graphify install
```

### Dependencies
- `uv` (recommended) or `pipx`/`pip`
- No API key needed for code-only extraction (runs offline via tree-sitter)
- API key needed only for docs/image/video extraction backends

### Configuration
- `.graphifyignore` (same syntax as `.gitignore`) to exclude paths from extraction.
- Manifest stored at `~/.graphify/manifest.json`.
- `GRAPHIFY_MAX_WORKERS` - optional, auto-computed AST parallelism.
- `GRAPHIFY_MAX_OUTPUT_TOKENS` - optional, raise for very large/dense codebases (e.g. 32768).

### Environment Variables (only if using non-code backends)
- `ANTHROPIC_API_KEY` (--backend claude), `GEMINI_API_KEY`/`GOOGLE_API_KEY` (--backend gemini),
  `OPENAI_API_KEY` (--backend openai), `DEEPSEEK_API_KEY`, `MOONSHOT_API_KEY`,
  `AZURE_OPENAI_API_KEY` + `AZURE_OPENAI_ENDPOINT`, `OLLAMA_BASE_URL`/`OLLAMA_MODEL` (local),
  AWS credentials (--backend bedrock).

### Verification Steps
1. `graphify install` completes and registers with Claude Code.
2. Run `graphify extract` in a project and confirm a knowledge graph is generated.
3. Run `graphify query`/`explain`/`path` against the generated graph.

### Troubleshooting
- Command not on PATH after `pip install` → use `uv tool install` or `pipx install` instead,
  which manage PATH automatically.
- Extraction fails for docs/images → confirm the relevant backend API key env var is set.

### Maintenance Notes
- Extremely active (daily releases) - re-run `uv tool upgrade graphifyy` periodically. YC-backed
  company, expect rapid API changes for now.

---

## 9. data-formulator (microsoft/data-formulator)

**Why ninth:** BI/data-visualization app - high quality but narrower use case (analytics-heavy
workflows specifically).

### Installation
```bash
# uv (recommended)
uv tool install data_formulator
# or
pip install data_formulator
python -m data_formulator
```

### Dependencies
- Python 3.10+
- `uv` (recommended) or pip

### Configuration
- Runs in demo mode with no configuration.
- For LLM-powered features, copy `.env.template` to `.env` and add provider keys.

### Environment Variables
- At least one LLM provider key: `OPENAI_API_KEY` (gpt-4/gpt-5.x), or equivalent for other
  supported providers - set in `.env`.

### Verification Steps
1. `python -m data_formulator` launches a local web UI.
2. Load a sample dataset and generate one chart via natural-language prompt.
3. Confirm at least one of the 15+ data connectors (CSV/Excel at minimum) loads data successfully.

### Troubleshooting
- LLM features fail silently → confirm `.env` exists and the correct provider key is set.
- Connector errors for enterprise data sources → check the specific connector's setup docs
  (these require additional credentials per source).

### Maintenance Notes
- Actively maintained by Microsoft Research (v0.7.0 beta, CI/CD, 123 test files) - update via
  `uv tool upgrade data_formulator` periodically. Beta status - expect breaking changes between
  minor versions.

---

## 10. codex-plugin-cc (openai/codex-plugin-cc)

**Why last:** Lowest business-value score - useful as a secondary code-review tool but not core
to business operations/automation/marketing goals.

### Installation
```bash
# 1. Add the OpenAI marketplace
/plugin marketplace add openai/codex-plugin-cc

# 2. Install the plugin
/plugin install codex@openai-codex

# 3. Reload plugins
/reload-plugins
```

### Dependencies
- Requires an OpenAI account/API access for the Codex agent bridge.

### Configuration
- No additional config beyond the plugin install - commands like `/codex:review` and
  `/codex:adversarial-review` become available immediately.

### Environment Variables
- OpenAI API credentials as required by the Codex agent (set per OpenAI's standard
  `OPENAI_API_KEY` convention).

### Verification Steps
1. `/plugin list` shows `codex@openai-codex`.
2. Run `/codex:review` on a small file and confirm a review response is returned.
3. Run `/codex:status` / `/codex:result` / `/codex:cancel` to confirm the task-management commands work.

### Troubleshooting
- Commands not appearing → run `/reload-plugins` again after install.
- Auth errors → confirm OpenAI API key/account has Codex access enabled.

### Maintenance Notes
- Stable snapshot (v1.0.4) - single-commit release, OpenAI-backed but treat as low-frequency
  update cadence. Optional install - skip if you don't already use OpenAI's Codex agent.

---

## General Notes

- Install in the order above (1 → 10) to front-load highest-ROI tools first.
- After each install, run the Verification Steps before moving to the next tool - this avoids
  compounding configuration issues across overlapping tools (especially the document-skills and
  marketing-skill duplicates flagged in `redundancy_analysis.xlsx`).
- Keep all API keys in a single `.env` file (gitignored) per project rather than scattered
  shell exports, to make audits and rotations easier.
