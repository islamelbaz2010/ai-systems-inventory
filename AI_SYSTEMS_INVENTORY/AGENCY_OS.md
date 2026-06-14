# Agency OS - A Complete Operating System Built on 5 Installed Tools

**Built entirely from the tools in `INSTALL_NOW.md`:**
1. 51 Marketing Skills bundle (claude-skills) - the **production engine**
2. Open Design Studio (open-design) - the **creative engine**
3. Persistent Memory Hooks (claude-mem) - the **memory layer**
4. Landing Page Generator (claude-skills) - the **fast-output engine**
5. Gmail / Slack Automation (Composio) - the **communication layer**

No new installs, accounts, or API keys required beyond what's already configured. This
document arranges those 5 tools into 10 functional systems that together form a working
"Agency OS" - reducing the owner's day-to-day involvement to review/approval decisions
only.

---

## System Map (10 Components)

```
                         ┌─────────────────────────────┐
                         │      MEMORY LAYER (3)        │
                         │  (claude-mem - the "brain")  │
                         └───────────▲──────▲───────────┘
                                      │      │
        ┌─────────────────────────────┘      └─────────────────────────────┐
        │                                                                     │
┌───────▼────────┐   ┌────────────────┐   ┌─────────────────┐   ┌───────────▼─────────┐
│  COMMUNICATION  │──▶│ LEAD MANAGEMENT │──▶│ CLIENT MANAGEMENT│──▶│ CONTENT PRODUCTION   │
│   LAYER (9)     │   │      (1)        │   │       (2)        │   │        (3)           │
│ Gmail/Slack     │   │                 │   │                  │   │ Marketing skills +   │
│ automation      │   │                 │   │                  │   │ Open Design + Landing│
└───────▲────────┘   └────────┬────────┘   └────────┬─────────┘   └──────────┬───────────┘
        │                      │                     │                         │
        │                      ▼                     ▼                         ▼
        │             ┌─────────────────────────────────────────────────────────┐
        │             │              TASK MANAGEMENT (7)                          │
        │             │     (tracked in memory; flagged for approval)             │
        │             └────────────────────────┬───────────────────────────────┘
        │                                       │
        │                                       ▼
        │             ┌─────────────────────────────────────────────────────────┐
        │             │            INTERNAL OPERATIONS (4)                        │
        │             │     (process/standard checks, recurring tasks)            │
        │             └────────────────────────┬───────────────────────────────┘
        │                                       │
        │                                       ▼
        │             ┌─────────────────────────────────────────────────────────┐
        └────────────▶│              REPORTING (5)                                │
                       │   Daily/weekly summaries → Slack                          │
                       └────────────────────────┬───────────────────────────────┘
                                                  │
                                                  ▼
                       ┌─────────────────────────────────────────────────────────┐
                       │           EXECUTIVE DASHBOARD (6)                          │
                       │   (owner's single view: pending approvals + KPIs)          │
                       └─────────────────────────────────────────────────────────┘

                       ┌─────────────────────────────────────────────────────────┐
                       │           AUTOMATION LAYER (10)                            │
                       │  (the triggers/scheduling that connect all of the above)   │
                       └─────────────────────────────────────────────────────────┘
```

---

## 1. Lead Management

**Built from:** Gmail/Slack automation (intake) + Marketing skills bundle (qualification/
audit) + Memory layer (dedup/tracking)

**What it does:**
- Detects new inbound contacts (emails from addresses not in memory).
- Runs an automatic SEO/website audit on the lead's domain (if provided) using the
  marketing skills bundle.
- Drafts a personalized outreach/reply referencing the audit findings.
- Saves the lead profile (name, source, audit summary, status) to memory.

**Data Flow:**
`Gmail (new email) → Memory (check if known contact) → [if new] Marketing Skills (audit +
draft reply) → Memory (save lead record) → Reporting (added to daily brief)`

**Trigger Events:**
- New unread email from an unrecognized sender (run on the daily brief, see Automation
  Layer)
- Manual: "Qualify this lead: [email/domain]"

**Manual Approval Points:**
- Sending the drafted outreach email (owner or designated team member clicks send)
- Marking a lead as "qualified" vs. "not a fit" if the audit reveals a mismatch (e.g.,
  wrong industry, no budget signals)

---

## 2. Client Management

**Built from:** Memory layer (client profiles/brand data) + Open Design Studio (brand-
consistent asset generation) + Gmail/Slack automation (status updates)

**What it does:**
- Maintains a persistent profile per client in memory: brand colors/voice (linked to an
  Open Design "Design System"), active projects, open requests, last contact date.
- When a client emails/Slacks a request, recalls their profile automatically (no
  re-explaining brand guidelines).
- Routes "send me an asset" requests to Content Production (system 3).

**Data Flow:**
`Gmail/Slack (client message) → Memory (recall client profile + Design System) → Content
Production (generate asset using recalled brand data) → Communication Layer (draft reply
with asset) → Memory (update project status)`

**Trigger Events:**
- Inbound message from a known client domain/contact
- Manual: "Update [Client]'s profile" or "Show me [Client]'s status"

**Manual Approval Points:**
- Sending the reply with the generated asset
- Any scope change requests (e.g., client asks for something outside the agreed
  deliverables) get flagged, not auto-actioned

---

## 3. Content Production

**Built from:** Marketing skills bundle (copy/strategy) + Open Design Studio (visual
assets) + Landing Page Generator (fast single-page output)

**What it does:**
- Three production paths depending on request type:
  - **Copy/strategy** (SEO audits, ad copy, email sequences, social posts) →
    Marketing skills bundle
  - **Visual assets** (decks, social graphics, prototypes) → Open Design Studio, using
    the client's saved Design System from memory
  - **Landing pages** (single-page sites, campaign pages) → Landing Page Generator,
    brand-validated against the client's palette

**Data Flow:**
`Task Management (production request) → Memory (pull client brand/Design System) →
[Marketing Skills | Open Design | Landing Page Generator] → Output (file/preview) →
Client Management (attach to client record) → Communication Layer (deliver to client)`

**Trigger Events:**
- New client request classified as "needs a deliverable" (from Lead/Client Management)
- Manual: "Create [asset type] for [client] about [topic]"
- Internal: recurring content calendar items (e.g., "weekly blog post" - tracked in Task
  Management)

**Manual Approval Points:**
- Final review of generated content/design before it's sent to the client (quality
  control gate - this is the single most important approval point in the whole system)

---

## 4. Internal Operations

**Built from:** Memory layer (process state) + Gmail/Slack automation (internal comms) +
Marketing skills bundle (operational skills like process-mapping where applicable)

**What it does:**
- Tracks recurring internal processes (e.g., "every new client gets a Design System
  created within 48 hours," "every lead gets an audit within 24 hours").
- Flags items that have stalled (e.g., a lead audit was promised but not sent after 24
  hours) by comparing memory timestamps against expected SLAs.
- Surfaces internal Slack questions/requests that need a human decision (vs. ones Claude
  can resolve via the other systems).

**Data Flow:**
`Memory (scan for items past SLA) → Internal Operations (flag stalled items) → Reporting
(included in daily brief) → Executive Dashboard (escalated if unresolved >X days)`

**Trigger Events:**
- Daily brief run (scans memory for SLA breaches)
- Internal Slack message directed at "the team" with no clear owner

**Manual Approval Points:**
- Reassigning or resolving flagged/stalled items (a human decides priority, not Claude)

---

## 5. Reporting

**Built from:** Memory layer (data source) + Gmail/Slack automation (delivery channel)

**What it does:**
- Produces a **daily brief** (new leads, client requests handled, content produced,
  flagged internal items) posted to a team Slack channel.
- Produces a **weekly digest** (aggregated from 7 days of memory: leads converted, content
  pieces shipped, client satisfaction signals from email tone/sentiment, recurring
  bottlenecks).
- All reports are generated FROM memory - no manual data entry.

**Data Flow:**
`Memory (all activity logged throughout the day/week) → Reporting (summarize) →
Communication Layer (post to Slack) → Executive Dashboard (weekly digest feeds the KPI
view)`

**Trigger Events:**
- Daily: end-of-day or start-of-day brief
- Weekly: Friday/Monday digest covering the prior 7 days

**Manual Approval Points:**
- None required for reading reports - they are informational. (Optional: owner can flag a
  report item for follow-up, which creates a Task Management item.)

---

## 6. Executive Dashboard

**Built from:** Reporting (weekly digest) + Memory layer (aggregated KPIs) + Communication
Layer (single delivery point)

**What it does:**
- A single weekly Slack message (or pinned memory summary) the owner reads in under 5
  minutes, containing:
  - Leads in pipeline (new / qualified / unresponsive)
  - Client deliverables shipped this week
  - Open approval items still waiting on the owner
  - Any SLA breaches from Internal Operations
  - One-line "health check" per active client (last contact date, sentiment)

**Data Flow:**
`Memory (full week of activity) → Reporting (weekly digest) → Executive Dashboard (owner-
facing summary, prioritized by what needs the owner's attention) → Communication Layer
(delivered to owner's Slack DM or a dedicated #exec channel)`

**Trigger Events:**
- Weekly (recommended: Monday morning)
- On-demand: "Give me the executive summary right now"

**Manual Approval Points:**
- This is the owner's primary control point - it's where all pending approvals from
  systems 1-4 surface in one place, so the owner never has to dig through Slack/Gmail
  individually.

---

## 7. Task Management

**Built from:** Memory layer (task state storage) - no new tool, this is a *pattern*
layered on top of memory

**What it does:**
- Every action that requires human approval (send email, approve design, resolve internal
  item) is written to memory as a "pending task" with: description, related
  client/lead, generated draft/asset reference, and timestamp.
- Tasks are surfaced in Reporting (daily brief) and Executive Dashboard (weekly), and
  cleared from memory once the owner confirms completion (e.g., "sent," "approved,"
  "done").

**Data Flow:**
`[Any system 1-4] (creates approval-needed item) → Task Management (logged in memory as
pending) → Reporting/Dashboard (surfaced) → Owner action → Task Management (marked
complete in memory)`

**Trigger Events:**
- Any time a system generates output that requires sending/approval
- Manual: "What's still pending?"

**Manual Approval Points:**
- This system *is* the approval-tracking mechanism - every manual approval point listed in
  systems 1-6 flows through here.

---

## 8. Memory Layer

**Built from:** Persistent Memory Hooks (claude-mem) - this is the foundational tool all
other systems read/write to.

**What it does:**
- Stores: client profiles + Design Systems, lead records, content/asset history, task
  status, SLA timestamps, and report history.
- Every other system (1-7, 9-10) reads from and writes to this layer - it's the shared
  "database" with no separate database software required.

**Data Flow:**
`All systems ↔ Memory (read/write on every interaction)`

**Trigger Events:**
- Continuous (automatic via claude-mem's lifecycle hooks - every session is captured)

**Manual Approval Points:**
- None - memory capture is fully automatic. (Privacy note: use `<private>` tags for any
  information that shouldn't be stored, per claude-mem's documentation.)

---

## 9. Communication Layer

**Built from:** Gmail/Slack Automation (Composio)

**What it does:**
- Single intake point (Gmail + Slack) for all external (lead/client) and internal (team)
  communication.
- Single delivery point for all outputs (draft replies, reports, dashboards).
- Acts as the "nervous system" connecting the owner/team to all 9 other systems.

**Data Flow:**
`External world (leads, clients) ↔ Gmail/Slack ↔ [Lead Mgmt | Client Mgmt | Reporting |
Dashboard] ↔ Memory`

**Trigger Events:**
- Any new email or Slack message (continuous monitoring, or polled during the daily brief)

**Manual Approval Points:**
- Sending drafted emails/Slack messages (the actual "send" action is always manual - see
  Content Production and Lead/Client Management)

---

## 10. Automation Layer

**Built from:** Combination of all 5 tools, orchestrated via the **Morning Agency Brief**
workflow from `FIRST_AUTOMATION.md`, extended into a full daily/weekly cycle.

**What it does:**
- Defines *when* each system runs:
  - **Continuous:** Memory capture (system 8)
  - **Daily:** Lead Management scan, Client Management request handling, Content
    Production for time-sensitive requests, Internal Operations SLA check, Reporting
    (daily brief)
  - **Weekly:** Reporting (digest) → Executive Dashboard
  - **On-demand:** Any system can be manually triggered by the owner at any time

**Data Flow:**
`Automation Layer (schedule/trigger) → [any of systems 1-9] → Memory (log result) →
Reporting/Dashboard (surface result)`

**Trigger Events:**
- Daily brief (morning, per `FIRST_AUTOMATION.md`)
- Weekly digest (Monday)
- Ad-hoc owner commands ("run the morning brief now," "give me the executive summary")

**Manual Approval Points:**
- None for triggering - automation runs on schedule or on command. All approvals happen
  downstream in Task Management (system 7).

---

## Manual Approval Points - Consolidated List

These are the **only** points where the owner (or a designated team member) must act.
Everything else runs automatically:

1. Sending drafted outreach emails to new leads (System 1)
2. Marking leads qualified/disqualified after audit review (System 1)
3. Sending drafted replies + generated assets to clients (System 2, 3)
4. Approving scope changes requested by clients (System 2)
5. Final quality-control review of generated content/designs before delivery (System 3)
6. Resolving flagged internal/SLA-breach items (System 4)
7. Clearing completed tasks from the pending list (System 7)

**Everything else** - reading inbox/Slack, classifying messages, running audits, drafting
replies, generating content/designs, updating memory, producing reports - is fully
automated.

---

## Expected Time Savings (per week, single-operator agency)

| System | Manual time before | Time after Agency OS | Savings |
|--------|--------------------|-----------------------|---------|
| Lead Management (intake + audit + draft outreach) | ~3-5 hrs/wk | ~30 min/wk (review/send only) | ~3.5 hrs |
| Client Management (status recall, brand re-explaining) | ~2-3 hrs/wk | ~15 min/wk | ~2.5 hrs |
| Content Production (drafts, decks, landing pages) | ~6-10 hrs/wk | ~1-2 hrs/wk (QC review) | ~7 hrs |
| Internal Operations (status checks, follow-ups) | ~1-2 hrs/wk | ~15 min/wk | ~1.5 hrs |
| Reporting (compiling updates) | ~2-3 hrs/wk | ~0 (auto-generated) | ~2.5 hrs |
| Executive Dashboard (owner status check-ins) | ~1-2 hrs/wk | ~5 min/wk | ~1.5 hrs |
| **Total** | **~15-25 hrs/wk** | **~2-3 hrs/wk** | **~12-22 hrs/wk** |

These ranges are directional estimates based on typical small-agency workloads, not
measured benchmarks - actual savings depend on lead volume and number of active clients.

---

## Expected ROI

- **51 Marketing Skills bundle** (ROI Score 7.5/10) and **connect-apps/Gmail-Slack
  automation** (ROI Score 6.0-8.2/10) are the two highest-value components, per
  `master_inventory.xlsx` - both are core to this system (Content Production and
  Communication Layer).
- **Open Design Studio** (ROI Score 7.2/10) replaces a recurring Canva/Figma subscription
  and/or freelance design spend - direct cost offset in addition to time savings.
- **Persistent Memory** (ROI Score 6.0/10) has no direct revenue line but is the
  multiplier that makes every other system context-aware - without it, Client Management
  and Reporting would require manual re-entry, eroding most of the other systems' savings.
- **Combined**, recovering ~12-22 hours/week at even a conservative $50/hr value of owner
  time represents **$600-$1,100/week (~$2,400-$4,400/month)** in time value, against an
  initial setup cost of a few hours and zero ongoing tool spend beyond what's already
  installed (Composio's free tier covers Gmail/Slack for typical agency volumes; check
  Composio's pricing if volume is very high).

---

## Implementation Order

Builds directly on `ACTION_PLAN.md`'s 30-Day Roadmap - this is the *system assembly*
order once the 5 tools are installed (Week 1 of that roadmap):

1. **Memory Layer (8)** - must be live first; every other system depends on it.
2. **Communication Layer (9)** - Gmail/Slack must be connected before Lead/Client
   Management can have an intake point.
3. **Content Production (3)** - stand up Marketing Skills + Landing Page Generator +
   Open Design Studio as standalone capabilities (already done in `INSTALL_NOW.md`).
4. **Lead Management (1)** - first end-to-end loop: new email → audit → draft → memory.
   Run for a few days using `FIRST_AUTOMATION.md`'s "Morning Brief" before adding more.
5. **Client Management (2)** - add client profiles + Design Systems to memory for each
   active client; extend the morning brief to handle client requests.
6. **Task Management (7)** - formalize the "pending approvals" pattern in memory once
   Lead + Client Management are generating approval items daily.
7. **Internal Operations (4)** - add SLA tracking once there's enough memory history (1-2
   weeks) to define realistic SLAs.
8. **Reporting (5)** - daily brief should already exist from step 4; add the weekly digest
   once 1+ week of data exists.
9. **Executive Dashboard (6)** - layer on top of Reporting once weekly digests are
   stable and useful.
10. **Automation Layer (10)** - convert the on-demand "morning brief" into a scheduled
    trigger only after steps 1-9 have run reliably on-demand for at least one week.

This order mirrors `ACTION_PLAN.md` Weeks 1-4: Week 1 installs the tools and stands up
Memory + Communication (steps 1-2 here); Weeks 2-3 build out Content Production, Lead, and
Client Management (steps 3-5); Week 4 formalizes Task Management, Internal Operations,
Reporting, and the Executive Dashboard (steps 6-9), with full Automation (step 10)
beginning in Month 2.

---

## Future Expansion Opportunities (Tier 3/4 - Not Built Yet)

These are explicitly **out of scope** for this document but represent natural next steps
once Agency OS (built on the 5 installed tools) is running smoothly - all are already
catalogued in `master_inventory.xlsx` / `installation_priority.xlsx`:

- **GitHub/Jira/Linear/Notion automation** (Tier 2, not yet installed) - would extend
  Internal Operations (4) and Task Management (7) into a full project-management sync,
  removing the need to manually track tasks in memory once volume grows.
- **16 companion skills** (Tier 2, claude-mem) - would directly automate the Reporting (5)
  layer's standup/digest generation rather than relying on prompted summaries.
- **150 brand-grade Design Systems** (Tier 2, open-design) - would formalize Client
  Management's (2) brand-profile step with pre-built templates instead of ad-hoc Design
  System creation.
- **LLM Council** (Tier 2) - would plug into the Executive Dashboard (6) as an on-demand
  "second opinion" for any major decision the dashboard surfaces (e.g., "should we raise
  this client's retainer?").
- **CRM automation (HubSpot/Salesforce/Pipedrive)** (Tier 3) - would replace memory-based
  lead tracking (System 1) with a proper CRM once lead volume exceeds what memory-based
  tracking can handle cleanly.
- **Stripe/Shopify automation** (Tier 3) - would extend Client Management (2) and
  Reporting (5) to include revenue/billing data in the Executive Dashboard.

None of these are required for Agency OS to function - they are upgrade paths once the
core 10-system loop (built entirely on the 5 installed tools) proves out.

---

## Quality Control Summary

The entire design optimizes for **reducing owner involvement while maintaining quality**
via one principle: **automate generation and classification, keep approval and final
review manual.** The 7 consolidated approval points (above) are deliberately positioned at
the only places where errors would be costly (sending something to a client/lead,
committing to scope, or making a strategic call) - everything upstream of those points
(reading, sorting, drafting, generating, summarizing) carries no external risk if imperfect,
because a human reviews before anything leaves the system.
