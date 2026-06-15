# OmniSocials Implementation Status - Social Media Operations Layer

Covers installation, configuration, and testing of **OmniSocials Agent Skills**
(`github.com/OmniSocials/omnisocials-agent-skills`, MIT, zero-dependency Node CLI +
SKILL.md) and its integration into the Agency OS as the new **Social Media
Operations Layer**.

---

## 1. Summary Table

| Item | Status |
|---|---|
| **Installed** | Yes |
| **Configured** | Yes (API key) |
| **Tested** | Partial - see below |
| **Connected Platforms** | None confirmed yet - blocked by this sandbox's network egress allowlist (see Known Issues) |

---

## 2. Installed (Yes)

- Cloned `github.com/OmniSocials/omnisocials-agent-skills` (public, MIT licensed,
  zero npm dependencies - Node 18+ built-in `fetch` only).
- Copied into `agency-os/omnisocials-agent-skills/`:
  - `scripts/omnisocials.js` - the CLI (single file, no `npm install` required)
  - `skills/omnisocials/SKILL.md` - agent instructions (commands, safety rules,
    platform-specific reference)
  - `skills/omnisocials/CHANGELOG.md`, `.claude-plugin/marketplace.json`,
    `README.md`, `CLAUDE.md`, `LICENSE`, `package.json`
- Verified `node omnisocials-agent-skills/scripts/omnisocials.js --help` and
  `config:show` run correctly with Node v22.22.2 (no install step needed - the CLI
  is a standalone script).

---

## 3. Configured (Yes)

- API key stored in `agency-os/.env` as `OMNISOCIALS_API_KEY` (gitignored - same
  `.env` file already used for `COMPOSIO_API_KEY`, `chmod 600`).
- Per the CLI's config-priority rules (CLI flag > `OMNISOCIALS_API_KEY` env var >
  project config > global config), no `config.json` file was written and nothing
  with the key was committed.
- `config:show` (with `.env` loaded) confirms:
  - Config source: `OMNISOCIALS_API_KEY env var`
  - Base URL: `https://api.omnisocials.com/v1`
  - API key recognized (CLI displays only the first 14 characters, masked with
    `...`, by design)

**Security compliance:**
- API key was never printed in full, never written to any `.md` file, and never
  committed (it lives only in the gitignored `agency-os/.env`).

---

## 4. Tested (Partial)

| Test | Result |
|---|---|
| `config:show` (no network required) | **Pass** - resolves `OMNISOCIALS_API_KEY` from env, correct base URL and source |
| `accounts:list --json` (live API call) | **BLOCKED** - see Known Issues |
| `posts:list`, `analytics:overview`, etc. (live) | Not run - depend on the same blocked network path |
| `social_brief.py --source sample --no-save` | **Pass** - full pipeline runs end-to-end against `sample_data/social_posts.json` + `sample_data/social_accounts.json`; produces all 6 required Social Brief sections |
| `social_brief.py --source sample` (memory write) | **Pass** - appends a KPI snapshot to `memory/social_memory.json.brief_history`; reset to clean baseline (`brief_history: []`) after the test run |
| `social_brief.py --source omnisocials` | Not run - requires the live API connection (same blocker) |

---

## 5. Connected Platforms

**None confirmed.** OmniSocials itself reports which of the 10 platforms
(Instagram, Facebook, LinkedIn, YouTube, TikTok, X, Pinterest, Bluesky, Threads,
Mastodon) are connected via `accounts:list` - this call could not be completed in
this environment (see Known Issues), so platform connection status is unknown until
run on a machine with normal network access.

---

## 6. Known Issues

1. **HARD BLOCKER: This sandbox's network egress allowlist blocks
   `api.omnisocials.com`.** Same class of issue documented for Composio in
   `IMPLEMENTATION_STATUS.md` / `ACTUAL_INSTALLATION_REPORT.md`.
   ```
   curl -sI https://api.omnisocials.com   -> HTTP/2 403, x-deny-reason: host_not_allowed
   ```
   Running `node omnisocials-agent-skills/scripts/omnisocials.js accounts:list --json`
   with the real API key fails because the egress gateway returns a plain-text 403
   ("Host not in allowlist...") instead of JSON, which the CLI then fails to parse.
   This is the egress gateway, not an OmniSocials or code issue - `config:show`
   (no network) works correctly with the same key.

2. **`OMNISOCIALS_CAPABILITIES.xlsx` was built from static analysis** of
   `SKILL.md` and `scripts/omnisocials.js` (command reference, platform support
   matrix, safety rules), not from a live `accounts:list`/API response, because of
   Known Issue #1. The capability descriptions reflect the documented API surface
   accurately, but live response shapes (e.g. exact `analytics:overview` fields)
   are not independently verified.

3. **No real social accounts are connected** - even once network access works, each
   platform (Instagram, Facebook, etc.) must be connected to the client's OmniSocials
   workspace separately (via the OmniSocials web app), the same way Gmail/Slack each
   needed their own OAuth connection through Composio.

---

## 7. Remaining Manual Steps

1. **Run on a machine with unrestricted network access** (same fix as
   `LOCAL_DEPLOYMENT_GUIDE.md` Section recommends for Composio) - e.g. the owner's
   Mac, or fix this environment's egress allowlist to permit `api.omnisocials.com`.
2. **Verify connectivity**: with `.env` loaded,
   `node agency-os/omnisocials-agent-skills/scripts/omnisocials.js accounts:list --json`
   should return the connected accounts for the workspace tied to the provided API
   key.
3. **Connect social platforms** in the OmniSocials web app
   (`app.omnisocials.com/settings`) for each client - Instagram, Facebook, LinkedIn,
   etc. - if not already connected to that workspace.
4. **Run `python3 social_brief.py --source omnisocials`** once accounts are
   connected, to confirm the same classify/aggregate/rank/report pipeline verified
   with sample data works against real posts/analytics.
5. **Set up webhooks** (`webhooks:create --url ... --events
   post.published,post.failed`) once a reachable endpoint exists (e.g. the agency's
   Slack-connected listener), per `SOCIAL_MEDIA_OS.md` Automation Opportunities.
6. **Schedule `social_brief.py`** alongside the Morning Brief via the same
   `launchd` mechanism described in `LOCAL_DEPLOYMENT_GUIDE.md`.

---

## 8. Recommended Next Steps

1. Move OmniSocials connectivity testing to the same local-Mac environment used for
   Composio/Gmail/Slack (per `LOCAL_DEPLOYMENT_GUIDE.md`) - this resolves both
   blockers (Composio and OmniSocials) with one environment change.
2. Once `accounts:list` succeeds, re-run `social_brief.py --source omnisocials` and
   compare its output shape against the sample-data output in
   `agency-os/SOCIAL_BRIEF.md` - adjust field mappings in `social_brief.py` if the
   live API's `posts:list`/`accounts:list` JSON differs from the assumed shape
   (mirrors the troubleshooting note already in `LOCAL_DEPLOYMENT_GUIDE.md` for
   `GMAIL_FETCH_EMAILS`/`SLACK_FETCH_CONVERSATION_HISTORY`).
3. Add `webhooks:create` for `post.published`/`post.failed` once a webhook receiver
   exists, to complement the daily Social Brief with real-time alerts.
4. After 2-4 weeks of `memory/social_memory.json.brief_history` data, build the
   Monthly Client Report described in `SOCIAL_MEDIA_OS.md` from real KPI trends.
5. Keep all publish/schedule/delete actions behind explicit human approval, per
   OmniSocials SKILL.md Safety Rules - no change to that posture is recommended.
