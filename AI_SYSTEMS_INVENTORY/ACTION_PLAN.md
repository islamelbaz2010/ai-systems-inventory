# Action Plan - Tier 1 & Tier 2 Only

Scope: the 10 capabilities marked "Install Immediately" (Tier 1) or "Install Next" (Tier 2)
in `installation_priority.xlsx`. Tier 3 and Tier 4 are explicitly out of scope for this
plan. Optimized for: automation, marketing-agency operations, business systems, AI
workflows, and minimal manual work.

**Priority order note:** Items are ranked by Priority Score (ROI adjusted for complexity),
but the **30-Day Roadmap below sequences by dependency, not raw score** - specifically,
`connect / connect-apps-plugin` (Composio gateway, #10 by score) must be installed
*before* the three Composio-skill items (#3 gmail/slack, #9 github/jira/linear/notion)
can function, even though its standalone Priority Score is lower.

---

## TIER 1

### 1. 51 marketing skills (full marketing bundle)

- **Name:** 51 marketing skills (full marketing bundle)
- **Repository:** claude-skills (alirezarezvani/claude-skills)
- **Why recommended:** Highest Priority Score in the entire inventory (6.0). One install
  delivers the entire marketing domain - AEO, SEO, content, CRO, email, social, pricing -
  with zero dependencies.
- **Business Value:** 8/10
- **Automation Value:** 7/10
- **Estimated Setup Time:** 15-30 minutes
- **Dependencies:** None
- **Required APIs:** None
- **Required Accounts:** Claude Code (already in use)
- **Required Infrastructure:** None - runs entirely inside Claude Code
- **Example Real-World Workflow:** A marketing agency operator runs `/seo-audit` on a new
  client's site, then `/content-creator` to draft a 4-week content calendar, then
  `/social-content` to turn each piece into platform-specific posts - all in one session,
  with no agency retainer.
- **Expected ROI:** 7.5/10 (ROI Score)
- **Priority Order:** **#1**

```bash
/plugin marketplace add alirezarezvani/claude-skills
/plugin install marketing-skills@claude-code-skills
```

---

### 2. Open Design Studio (desktop/web app)

- **Name:** Open Design Studio (desktop/web app)
- **Repository:** open-design (nexu-io/open-design)
- **Why recommended:** Second-highest Priority Score (5.8). Replaces a Canva/Figma
  subscription with a local-first, chat-driven design studio that outputs HTML, decks,
  video, and images directly.
- **Business Value:** 8/10
- **Automation Value:** 6/10
- **Estimated Setup Time:** 20-45 minutes (desktop app) or 30-60 minutes (Docker self-host)
- **Dependencies:** Electron app (desktop) OR Docker + Docker Compose (self-hosted)
- **Required APIs:** None required (optional BYOK LLM key if no local agent CLI detected)
- **Required Accounts:** None for desktop app; optional LLM provider account for BYOK mode
- **Required Infrastructure:** A machine to run the desktop app or Docker container
- **Example Real-World Workflow:** Before a client pitch, generate a branded deck (15
  templates / 36 themes) and a matching landing-page mockup in the same session, using one
  of the 150 bundled Design Systems to guarantee brand consistency - no designer needed.
- **Expected ROI:** 7.2/10 (ROI Score)
- **Priority Order:** **#2**

```bash
# Desktop app (recommended): download from releases page
# OR self-hosted:
cd deploy && cp .env.example .env
echo "OD_API_TOKEN=$(openssl rand -hex 32)" >> .env
docker compose up -d   # http://localhost:7456
```

---

## TIER 2

### 3. Persistent memory hooks (5 lifecycle hooks)

- **Name:** Persistent memory hooks (5 lifecycle hooks)
- **Repository:** claude-mem (thedotmack/claude-mem)
- **Why recommended:** Tied for #3 by Priority Score (4.8). Zero ongoing API cost,
  one-command install, and compounds the value of every other tool by giving Claude
  cross-session memory.
- **Business Value:** 7/10
- **Automation Value:** 8/10
- **Estimated Setup Time:** 10-15 minutes
- **Dependencies:** Node >=20, Bun, SQLite, Chroma vector DB (all installed automatically
  by the installer)
- **Required APIs:** None
- **Required Accounts:** None
- **Required Infrastructure:** Local worker service (runs on localhost, auto-managed)
- **Example Real-World Workflow:** Monday's session establishes a client's brand voice and
  open tasks; Wednesday's session automatically recalls that context without re-explaining
  - Claude picks up exactly where the team left off.
- **Expected ROI:** 6.0/10 (ROI Score)
- **Priority Order:** **#3**

```bash
npx claude-mem install
```

---

### 4. landing-page

- **Name:** landing-page
- **Repository:** claude-skills (alirezarezvani/claude-skills)
- **Why recommended:** Tied for #3 by Priority Score (4.8). Produces a complete,
  conversion-ready landing page in a single file with no build step.
- **Business Value:** 6/10
- **Automation Value:** 6/10
- **Estimated Setup Time:** 5 minutes (bundled with marketing-skills install, Item #1)
- **Dependencies:** None
- **Required APIs:** None
- **Required Accounts:** None
- **Required Infrastructure:** None - outputs a single-file HTML page
- **Example Real-World Workflow:** A new client signs up for a service launch; within the
  same hour, generate a branded single-file HTML landing page (GSAP animations, brand
  palette validated against the client's Design System from Item #8) and deploy it to any
  static host.
- **Expected ROI:** 6.0/10 (ROI Score)
- **Priority Order:** **#4**

```bash
/plugin install product-skills@claude-code-skills
```

---

### 5. gmail-automation / slack-automation

- **Name:** gmail-automation / slack-automation
- **Repository:** awesome-claude-skills (ComposioHQ/awesome-claude-skills)
- **Why recommended:** Tied for #3 by Priority Score (4.8). Automates the two
  highest-frequency daily communication channels - per the inventory notes, a documented
  ~70% reduction in manual comms overhead.
- **Business Value:** 8/10
- **Automation Value:** 9/10
- **Estimated Setup Time:** 20-30 minutes (after Composio gateway, Item #10, is installed)
- **Dependencies:** **Requires Item #10 (connect/connect-apps-plugin) installed first**
- **Required APIs:** Composio API key
- **Required Accounts:** Composio account (dashboard.composio.dev), Gmail account, Slack
  workspace - each authorized via OAuth
- **Required Infrastructure:** None beyond Composio's hosted Tool Router
- **Example Real-World Workflow:** Each morning, Claude triages unread Gmail (drafts
  replies to common client questions, flags urgent items), and posts a daily summary to a
  dedicated Slack channel - without anyone opening their inbox first.
- **Expected ROI:** 6.0/10 (ROI Score)
- **Priority Order:** **#5** (install logically after #10, see roadmap)

```bash
# After connect-apps-plugin is installed and authenticated:
# enable the gmail and slack Composio skills via /connect-apps:list and /connect-apps:setup
```

---

### 6. LLM Council (5-advisor pipeline)

- **Name:** LLM Council (5-advisor pipeline)
- **Repository:** llm-council-skill (tenfoldmarc/llm-council-skill)
- **Why recommended:** Priority Score 4.6. Single-file install, zero dependencies, gives
  instant multi-perspective decision support for high-stakes business calls (per notes:
  "$10k+ decisions, pricing, pivots, hiring").
- **Business Value:** 8/10
- **Automation Value:** 4/10
- **Estimated Setup Time:** 5 minutes
- **Dependencies:** None - Claude Code sub-agents only
- **Required APIs:** None
- **Required Accounts:** None
- **Required Infrastructure:** None
- **Example Real-World Workflow:** Before deciding whether to raise agency retainer prices
  10% across the board, run the decision through the 5-advisor council (each with an
  opposing style) plus anonymous peer review and a chairman synthesis - producing an HTML
  report that documents the reasoning for the final call.
- **Expected ROI:** 5.8/10 (ROI Score)
- **Priority Order:** **#6**

```bash
git clone https://github.com/tenfoldmarc/llm-council-skill ~/.claude/skills/llm-council
# restart Claude Code
```

---

### 7. 16 companion skills (babysit, standup, weekly-digests, etc.)

- **Name:** 16 companion skills (babysit, standup, weekly-digests, etc.)
- **Repository:** claude-mem (thedotmack/claude-mem)
- **Why recommended:** Priority Score 4.4. Turns the memory data from Item #3 into
  recurring reports (standups, weekly digests, project plans) with no manual reporting.
- **Business Value:** 6/10
- **Automation Value:** 7/10
- **Estimated Setup Time:** 0 minutes additional - bundled with Item #3
- **Dependencies:** **Requires Item #3 (Persistent memory hooks) installed first** -
  also needs the worker service + MCP search from that install
- **Required APIs:** None
- **Required Accounts:** None
- **Required Infrastructure:** Same local worker service as Item #3
- **Example Real-World Workflow:** Every Friday, run the weekly-digest companion skill to
  auto-generate a summary of all client work completed that week, pulled directly from
  memory - ready to paste into a client update email.
- **Expected ROI:** 5.5/10 (ROI Score)
- **Priority Order:** **#7**

```bash
# Bundled with claude-mem (Item #3) - no separate install
# Invoke individual companion skills directly, e.g. "run weekly-digest"
```

---

### 8. 150 brand-grade Design Systems (DESIGN.md)

- **Name:** 150 brand-grade Design Systems (DESIGN.md)
- **Repository:** open-design (nexu-io/open-design)
- **Why recommended:** Priority Score 4.4. Pre-built brand contracts (color/type/spacing/
  voice) from Linear, Stripe, Apple, Vercel, etc. - enforces 100% brand compliance on every
  asset generated by Item #2.
- **Business Value:** 6/10
- **Automation Value:** 5/10
- **Estimated Setup Time:** 10 minutes (selecting/adapting one system per brand/client)
- **Dependencies:** Open Design Studio (Item #2) - bundled with it
- **Required APIs:** None
- **Required Accounts:** None
- **Required Infrastructure:** None
- **Example Real-World Workflow:** For each client account, copy the closest-matching
  `design-systems/<brand>/` folder and adjust the palette/voice once - every subsequent
  landing page, deck, or social asset generated for that client automatically inherits the
  brand contract.
- **Expected ROI:** 5.5/10 (ROI Score)
- **Priority Order:** **#8**

```bash
# Bundled with open-design (Item #2)
cp -r open-design/design-systems/<closest-brand> ./my-client-brand
# edit palette/typography/voice in DESIGN.md
```

---

### 9. github-automation / jira-automation / linear-automation / notion-automation

- **Name:** github-automation / jira-automation / linear-automation / notion-automation
- **Repository:** awesome-claude-skills (ComposioHQ/awesome-claude-skills)
- **Why recommended:** Priority Score 4.2. Automates dev/PM tooling - issue triage, PR
  status, sprint updates, Notion page/database syncing - removing recurring manual status
  updates.
- **Business Value:** 7/10
- **Automation Value:** 8/10
- **Estimated Setup Time:** 20-30 minutes per tool (after Composio gateway, Item #10)
- **Dependencies:** **Requires Item #10 (connect/connect-apps-plugin) installed first**
- **Required APIs:** Composio API key (shared with Item #5)
- **Required Accounts:** GitHub, Jira/Linear, and/or Notion accounts - authorized via OAuth
  through Composio
- **Required Infrastructure:** None beyond Composio's hosted Tool Router
- **Example Real-World Workflow:** When a client-facing bug is filed in GitHub, Claude
  automatically creates a linked Linear ticket, updates the project's Notion status page,
  and posts a summary to the team Slack channel (Item #5) - a 4-tool sync done with zero
  manual entry.
- **Expected ROI:** 5.2/10 (ROI Score)
- **Priority Order:** **#9** (install logically after #10, see roadmap)

```bash
# After connect-apps-plugin is installed and authenticated:
# enable github/jira/linear/notion Composio skills via /connect-apps:list and /connect-apps:setup
```

---

### 10. connect / connect-apps-plugin (Composio gateway)

- **Name:** connect / connect-apps-plugin (Composio gateway)
- **Repository:** awesome-claude-skills (ComposioHQ/awesome-claude-skills)
- **Why recommended:** Lowest Priority Score within Tier 2 (4.1, discounted for Medium
  complexity) but the **highest raw ROI Score in the entire inventory (8.2)** and the
  single highest-leverage automation install overall - it is the prerequisite gateway for
  Items #5 and #9.
- **Business Value:** 9/10
- **Automation Value:** 10/10
- **Estimated Setup Time:** 30-60 minutes (account creation, API key, first OAuth
  connections)
- **Dependencies:** None to install; **is itself a dependency for Items #5 and #9**
- **Required APIs:** Composio API key (dashboard.composio.dev)
- **Required Accounts:** Composio account; individual app accounts (Gmail, Slack, GitHub,
  etc.) connected via OAuth as needed
- **Required Infrastructure:** None - Composio's Tool Router is hosted
- **Example Real-World Workflow:** Install once, then progressively turn on Gmail, Slack,
  GitHub, Jira, Linear, Notion, and (later, Tier 3) CRM/Stripe/Shopify connectors - each new
  connector takes ~10 minutes once the gateway is live, rather than a separate integration
  project per app.
- **Expected ROI:** 8.2/10 (ROI Score - highest in the inventory)
- **Priority Order:** **#10 by score, but install EARLY (Week 1) due to its role as a
  dependency for #5 and #9 - see roadmap**

```bash
pip install composio
claude --plugin-dir ./connect-apps-plugin
/connect-apps:setup   # paste API key from dashboard.composio.dev
```

---

# 30-Day Installation Roadmap

Sequencing balances Priority Score with dependency order: the Composio gateway (#10) is
pulled into Week 1 despite its #10 ranking because Items #5 and #9 cannot function without
it, and doing so early avoids a second OAuth-configuration session later.

## Week 1 - Foundation (Marketing Engine + Automation Gateway)

**Install:**
1. **51 marketing skills (full marketing bundle)** - claude-skills (#1)
2. **landing-page** - claude-skills (#4, bundled with #1's marketplace add)
3. **connect / connect-apps-plugin (Composio gateway)** - awesome-claude-skills (#10)

**Why first:** These three require zero or near-zero ongoing infrastructure, and together
they (a) give immediate marketing-agency output capability (SEO, content, CRO, landing
pages) and (b) stand up the automation gateway that Week 2's communication/PM automations
depend on. Starting the Composio account-creation and OAuth process in Week 1 (even before
the dependent skills are configured) avoids it becoming a Week 2 bottleneck.

**Outcome by end of Week 1:** Able to produce full marketing deliverables (audits, content,
landing pages) for any client, and have the Composio gateway authenticated and ready.

---

## Week 2 - Communication & Project Automation

**Install:**
4. **gmail-automation / slack-automation** - awesome-claude-skills (#5, via gateway from
   Week 1)
5. **github-automation / jira-automation / linear-automation / notion-automation** -
   awesome-claude-skills (#9, via gateway from Week 1)
6. **Persistent memory hooks (5 lifecycle hooks)** - claude-mem (#3)

**Why second:** With the Composio gateway live, enabling the communication and PM
connectors is now a ~20-30 minute OAuth click-through per tool rather than a setup project.
claude-mem's memory hooks are added now so that everything done in Weeks 1-2 (client brand
decisions, marketing assets produced, automations configured) is captured from this point
forward.

**Outcome by end of Week 2:** Inbox/Slack triage and dev/PM status syncing run with minimal
manual input; all subsequent work is automatically remembered across sessions.

---

## Week 3 - Design System & Decision Support

**Install:**
7. **Open Design Studio (desktop/web app)** - open-design (#2)
8. **150 brand-grade Design Systems (DESIGN.md)** - open-design (#8, bundled with #7)
9. **LLM Council (5-advisor pipeline)** - llm-council-skill (#6)

**Why third:** Open Design Studio has the highest setup complexity of the Tier 1/2 set
(desktop app or Docker self-host), so it's scheduled once the team is already comfortable
with the Week 1-2 tools and has bandwidth for a slightly longer setup session. LLM Council
is a 5-minute install with no dependencies - added here as a "decision support" capability
to be available for any strategic calls (pricing, hiring, vendor selection) that come up as
the new stack scales.

**Outcome by end of Week 3:** Full design/creative production capability (decks, landing
pages, social assets) with enforced brand consistency, plus a structured decision-support
tool for major calls.

---

## Week 4 - Recurring Operations Layer

**Install:**
10. **16 companion skills (babysit, standup, weekly-digests, etc.)** - claude-mem (#7,
    bundled with Week 2's memory hooks - activate now)

**Why last:** These companion skills depend on having two weeks of memory data already
captured (from Week 2 onward) to produce meaningful standups/digests/reports. Activating
them in Week 4 means the first weekly digest covers real accumulated work rather than an
empty memory store.

**Also in Week 4 - Consolidation (no new installs):**
- Audit all Composio connections from Weeks 1-2 (remove unused scopes, rotate API keys).
- Apply a Design System (Item #8) to each active client/brand.
- Run one real decision through LLM Council to validate the workflow.
- Confirm memory-based companion skills (standup, weekly-digest) are producing useful
  output; tune prompts/cadence as needed.

**Outcome by end of Week 4:** The full Tier 1 + Tier 2 stack (10 capabilities) is installed,
configured, and producing recurring automated output (digests, comms triage, marketing
assets, design system enforcement) with minimal manual intervention going forward.

---

## Summary Table

| Week | Install | Repo | Priority Order |
|------|---------|------|-----------------|
| 1 | 51 marketing skills (full marketing bundle) | claude-skills | #1 |
| 1 | landing-page | claude-skills | #4 |
| 1 | connect / connect-apps-plugin (Composio gateway) | awesome-claude-skills | #10 |
| 2 | gmail-automation / slack-automation | awesome-claude-skills | #5 |
| 2 | github/jira/linear/notion automation | awesome-claude-skills | #9 |
| 2 | Persistent memory hooks (5 lifecycle hooks) | claude-mem | #3 |
| 3 | Open Design Studio (desktop/web app) | open-design | #2 |
| 3 | 150 brand-grade Design Systems (DESIGN.md) | open-design | #8 |
| 3 | LLM Council (5-advisor pipeline) | llm-council-skill | #6 |
| 4 | 16 companion skills (babysit, standup, weekly-digests, etc.) | claude-mem | #7 |
