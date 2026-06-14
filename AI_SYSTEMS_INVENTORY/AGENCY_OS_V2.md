# Agency OS V2 - Revenue, SOP & KPI Layers + True Owner Dashboard

This is an upgrade to `AGENCY_OS.md` (10 systems built on the 5 tools from
`INSTALL_NOW.md`). V2 adds three new layers and replaces the original Executive Dashboard
(System 6) with a true owner-facing dashboard.

**Constraint carried forward:** the 3 new layers are designed to run primarily on the 5
tools already installed (Memory, Communication, Marketing Skills, Open Design, Landing
Page Generator). Where a capability would be meaningfully stronger with a Tier 3 add-on
(e.g., Stripe automation for the Revenue Layer), that's called out explicitly as a
**Future Expansion** - not a requirement to use this V2 design today.

---

## 11. Revenue Layer

### Purpose
Give the owner a continuously-updated picture of money coming in (and expected to come
in) without manually checking invoices, bank accounts, or asking the team "did that client
pay yet?"

### Inputs
- Gmail: invoice emails, payment confirmation emails, payment reminder threads (read via
  Communication Layer, System 9)
- Memory: client records (System 2) - contract value, billing cadence, retainer vs.
  project-based
- Owner/team manual updates: "Acme Retail paid the March retainer" (logged via Slack, read
  by Communication Layer)

### Outputs
- A **revenue ledger inside memory**: per client, per month - expected amount, status
  (invoiced / paid / overdue), last update date
- Flags for overdue payments (no payment-confirmation email found within X days of an
  invoice email)
- A rolled-up "Monthly Recurring Revenue" (MRR) figure derived from active retainer
  clients in memory

### Automation Opportunities
- Auto-detect invoice-sent and payment-received emails via Gmail automation and log them
  to the revenue ledger in memory - no manual entry for the common case.
- Auto-flag a client as "payment overdue" if an invoice was logged but no payment
  confirmation appears within the client's normal payment window (learned from memory
  history).
- Auto-include revenue status in the daily brief and Reporting (System 5) whenever a
  payment is received or becomes overdue.

### Approval Points
- **Marking an invoice as "paid" based on an ambiguous email** (e.g., a forwarded receipt
  that doesn't clearly match a client) - owner/team confirms the match.
- **Any "overdue" flag that triggers an automated reminder email to a client** - the
  reminder is drafted, never sent automatically (protects the client relationship).
- **Changes to a client's billing cadence or contract value in memory** - always
  owner-confirmed, since this feeds MRR calculations.

### Metrics
- Monthly Recurring Revenue (MRR) - sum of active retainer values in memory
- Outstanding/overdue invoice total (across all clients)
- Average days-to-payment per client (historical, from memory)
- Revenue by client (top 3 by value - useful for prioritizing client attention)

### Data Flow
`Gmail (invoice/payment emails) → Communication Layer → Revenue Layer (classify: invoice
sent / payment received) → Memory (update revenue ledger) → Reporting (daily brief if
status changed) → Executive Dashboard (MRR + overdue summary)`

### Business Impact
Removes the owner from "who owes us money" tracking entirely for the common case (email
confirms payment), while keeping a human in the loop for anything ambiguous or for
client-facing reminders. Directly supports the Executive Dashboard's "How much money is
coming in?" question.

**Future Expansion:** Stripe/Shopify automation (Tier 3, `master_inventory.xlsx`) would
replace email-based detection with direct payment-processor data - more accurate, no
email-parsing ambiguity. Not required for V2 to function.

---

## 12. SOP Layer (Standard Operating Procedures)

### Purpose
Encode the agency's repeatable processes (how a new lead is handled, how a client
onboarding works, how content gets produced and reviewed) as memory-stored, checkable
checklists - so Claude (and any new hire) follows the same process every time, without the
owner re-explaining it.

### Inputs
- Owner-authored SOP definitions (one-time setup): e.g., "New Lead SOP: 1) run audit, 2)
  draft reply, 3) save to memory, 4) flag for send within 24h"
- Memory: current state of any in-progress item (lead, client request, content piece)
- Outputs from Systems 1-4 (Lead/Client Management, Content Production, Internal
  Operations) - each step's completion is checked against the relevant SOP

### Outputs
- A **process-compliance record** in memory: for each lead/client/content item, which SOP
  steps are done vs. pending vs. skipped
- Alerts when a step is skipped or overdue relative to the SOP's expected timing
- A library of reusable SOPs (New Lead, New Client Onboarding, Content Request, Monthly
  Reporting) that any of the other 12 systems can reference

### Automation Opportunities
- Every time Lead Management (System 1) or Content Production (System 3) completes a
  step, automatically check it off against the relevant SOP in memory - no separate
  tracking tool needed.
- Auto-generate a "process health" note in the daily brief if any item has skipped/overdue
  SOP steps (feeds Internal Operations, System 4).
- New SOPs can be added by the owner simply describing the process once in plain English
  - Claude stores it as a checklist template in memory for future reuse.

### Approval Points
- **Defining or changing an SOP** - always owner-initiated (Claude doesn't invent new
  mandatory processes on its own).
- **Marking an SOP step as "intentionally skipped"** (vs. "overdue") - requires a human
  judgment call, since skipping a step might be correct for an edge case.

### Metrics
- SOP compliance rate (% of steps completed on-time across all active items)
- Most-frequently-skipped SOP step (signals a process that may need redesign)
- Average time-to-complete per SOP (e.g., "New Lead SOP" average completion time)

### Data Flow
`Owner (defines SOP once) → Memory (SOP template stored) → Systems 1-4 (complete steps) →
SOP Layer (checks steps against template) → Memory (compliance record) → Reporting
(process health) → Executive Dashboard (flags if compliance drops)`

### Business Impact
This is what makes the Agency OS **scalable beyond the owner's personal habits** - any
process the owner does consistently gets captured once and then enforced automatically,
which is essential before adding team members or expanding client volume. It directly
reduces the owner's role from "doing the process" to "occasionally updating the process
definition."

---

## 13. KPI Layer

### Purpose
Turn the raw activity logged across all other layers (Lead Management, Client Management,
Content Production, Revenue, SOP) into a small set of trend-tracked numbers the owner can
glance at weekly to know if the business is healthy, growing, or has a problem - without
digging through memory or Slack history.

### Inputs
- Memory: full activity history from all other systems (leads logged, content shipped,
  revenue ledger, SOP compliance)
- Time-series data: weekly snapshots of each metric (stored in memory as a running log)

### Outputs
- A **weekly KPI snapshot** stored in memory (so trends over time are computable)
- Trend indicators (up/down/flat vs. prior week and prior 4-week average) for each KPI
- The KPI snapshot feeds directly into the redesigned Executive Dashboard (below)

### Automation Opportunities
- Every weekly digest (Reporting, System 5) automatically computes and stores the KPI
  snapshot - no manual data pulls.
- Trend flags (e.g., "leads down 30% vs. 4-week average") are computed automatically and
  surfaced in the dashboard's "What should the owner focus on today?" section.
- KPI definitions themselves can be extended over time (owner says "also track X") and
  the KPI Layer starts logging it from memory going forward.

### Approval Points
- **Adding/removing a tracked KPI** - owner-initiated.
- **Interpreting a trend as "needs action"** - the KPI Layer flags trends, but deciding
  *what to do* about a downward trend is always the owner's call (surfaced via the
  dashboard, not auto-acted-on).

### Core KPIs Tracked
1. **New leads this week** (from Lead Management)
2. **Lead → client conversion rate** (rolling 4/12-week)
3. **Content pieces shipped this week** (from Content Production)
4. **MRR + revenue trend** (from Revenue Layer)
5. **SOP compliance rate** (from SOP Layer)
6. **Client health** (days since last positive contact per client, from Client
   Management/memory)
7. **Owner time spent on approvals this week** (count of Task Management items completed
   - a direct measure of "owner involvement," which this whole system aims to minimize)

### Data Flow
`Memory (all activity) → KPI Layer (weekly aggregation + trend calc) → Memory (KPI
snapshot log, time-series) → Reporting (weekly digest includes KPI summary) → Executive
Dashboard (KPI trends + focus recommendations)`

### Business Impact
Converts "the system is running" into "the business is healthy" - the KPI Layer is the
translation layer between operational activity (which the owner shouldn't need to see in
detail) and business outcomes (which the owner absolutely needs visibility into). KPI #7
(owner time on approvals) directly measures whether the Agency OS is achieving its core
goal of minimal owner involvement.

---

## Redesigned Executive Dashboard (System 6, V2)

The original Executive Dashboard (V1) was a generic weekly summary. V2 redesigns it as a
**single Slack message, delivered every Monday morning (and available on-demand)**, that
answers six specific owner questions in order. Each question maps to one or more of the
13 systems (10 original + 3 new).

### Dashboard Structure

```
═══════════════════════════════════════════════════════
  OWNER DASHBOARD - Week of [date]
═══════════════════════════════════════════════════════

💰 MONEY COMING IN
   MRR: $X,XXX (▲/▼ $XXX vs last month)
   Paid this week: $X,XXX across N clients
   Overdue: $X,XXX (Client A - 12 days overdue)
   [Source: Revenue Layer]

📋 ACTIVE LEADS
   New this week: N
   In progress (audit/outreach sent, awaiting reply): N
   Conversion rate (4-wk): X%
   [Source: Lead Management + KPI Layer]

⚠️ CLIENTS NEEDING ATTENTION
   - Client B: no contact in 14 days (health flag)
   - Client C: requested scope change, awaiting your decision
   - Client D: payment overdue 12 days
   [Source: Client Management + Revenue Layer + SOP Layer]

🚧 BLOCKED TASKS
   - 3 draft emails awaiting send (Lead Mgmt)
   - 1 design awaiting QC review (Content Production)
   - 1 SOP step overdue: "New Cafe" onboarding Design System (SOP Layer)
   [Source: Task Management + SOP Layer]

🎯 OPPORTUNITIES
   - Client E mentioned wanting "more social content" in last email -
     potential upsell (flagged from Communication Layer)
   - 2 leads from last week never replied - re-engagement opportunity
   - SOP Layer: "Content Request" SOP completes 30% faster than 4 weeks
     ago - capacity may exist for 1-2 more clients
   [Source: Client Mgmt + Lead Mgmt + SOP Layer + KPI Layer]

👉 FOCUS TODAY
   1. Approve/send the 3 pending lead outreach emails (5 min)
   2. Decide on Client C's scope change request (10 min)
   3. Follow up personally with Client D on overdue payment (relationship-
      sensitive, not automated)
   [Source: Task Management, ranked by KPI Layer + Revenue Layer urgency]
═══════════════════════════════════════════════════════
```

### How Each Question Is Answered

| Owner Question | Answered By | Layers Involved |
|---|---|---|
| How much money is coming in? | "MONEY COMING IN" section - MRR, payments this week, overdue | Revenue Layer (11), KPI Layer (13) |
| How many leads are active? | "ACTIVE LEADS" section - counts + conversion rate | Lead Management (1), KPI Layer (13) |
| Which clients need attention? | "CLIENTS NEEDING ATTENTION" - health flags, scope changes, overdue payments | Client Management (2), Revenue Layer (11), SOP Layer (12) |
| What tasks are blocked? | "BLOCKED TASKS" - pending approvals + overdue SOP steps | Task Management (7), SOP Layer (12) |
| What opportunities exist? | "OPPORTUNITIES" - upsell signals, re-engagement, capacity | Client Mgmt (2), Lead Mgmt (1), SOP Layer (12), KPI Layer (13) |
| What should the owner focus on today? | "FOCUS TODAY" - ranked, time-boxed action list | Task Management (7) ranked by Revenue (11) + KPI (13) urgency |

### Data Flow (Full V2 Dashboard)

```
Memory (8) ──────────────────────────────────────────────────┐
   │  (revenue ledger, lead records, client profiles,         │
   │   SOP compliance, KPI snapshots, pending tasks)           │
   ▼                                                            │
Revenue Layer (11) ──┐                                          │
Lead Mgmt (1) ───────┤                                          │
Client Mgmt (2) ─────┼──▶ KPI Layer (13) ──▶ Reporting (5) ──▶ Executive Dashboard (6, V2)
SOP Layer (12) ──────┤        (weekly trend calc)   (digest)        (Monday Slack message)
Task Mgmt (7) ───────┘                                                       │
                                                                              ▼
                                                                  Communication Layer (9)
                                                                  (delivered to owner)
```

### Approval Points (Dashboard-Specific)
- The dashboard itself requires **no approval to generate or send** - it's read-only
  information for the owner.
- However, every item in "BLOCKED TASKS" and "FOCUS TODAY" *is* an approval point from
  another layer, now surfaced in one place. The dashboard doesn't create new approval
  points - it **aggregates existing ones** so the owner has one place to act, instead of
  hunting across Gmail/Slack/memory.

---

## V2 Implementation Order (Extends `AGENCY_OS.md` Steps 1-10)

1. **Revenue Layer (11)** - add after Client Management (V1 step 5) is stable, since it
   depends on client records already existing in memory. ~1 week of Gmail-based invoice/
   payment tracking before trusting the MRR figure.
2. **SOP Layer (12)** - add once Lead Management and Content Production (V1 steps 3-4)
   have run for 2+ weeks - you need real examples of "how we currently do it" before
   encoding an SOP.
3. **KPI Layer (13)** - add last, once Revenue and SOP layers have at least 2-4 weeks of
   data to compute meaningful trends (a single data point has no trend).
4. **Executive Dashboard V2** - redesign the dashboard only after Revenue, SOP, and KPI
   layers are all producing data - otherwise sections of the dashboard will be empty.

**Recommended timing:** V1 (Weeks 1-4 per `ACTION_PLAN.md`) → run V1 for 4-6 weeks to
build up memory history → then implement V2 layers in the order above over 2-3 additional
weeks. Attempting V2 before V1 has real history will produce an empty/inaccurate dashboard.

---

## Business Impact Summary (V2 vs V1)

| | V1 (AGENCY_OS.md) | V2 (this document) |
|---|---|---|
| Owner sees | Activity summary (what got done) | Business health (money, leads, risks, opportunities, focus) |
| Revenue visibility | None | MRR, overdue tracking, payment trends |
| Process consistency | Implicit (whatever Claude does each time) | Explicit SOPs, compliance tracked |
| Trend awareness | None (point-in-time only) | Week-over-week KPI trends |
| Owner's weekly Monday task | Read activity report (~5 min) | Read prioritized focus list + act on 1-3 ranked items (~15-20 min) |
| Scalability | Works for owner-only operations | Foundation for adding team members (SOPs become onboarding docs) |

V2 keeps the V1 principle intact - **automate generation/classification, keep approval and
strategic judgment manual** - while adding the financial and process visibility a growing
agency needs without increasing the owner's day-to-day workload (the Monday dashboard
remains a single message).
