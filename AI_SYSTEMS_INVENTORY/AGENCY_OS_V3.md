# Agency OS V3 - The Decision Engine

This is an upgrade to `AGENCY_OS_V2.md` (13 systems: the original 10 from `AGENCY_OS.md`
plus Revenue, SOP, and KPI layers). V3 adds **System 14: the Decision Engine** - the layer
that turns all the data the other 13 systems collect into a small number of ranked,
actionable decisions.

**Critical distinction from Reporting (5) and the Executive Dashboard (6):** those systems
*describe* what happened. The Decision Engine *prioritizes what to do next*. Reporting
answers "what happened this week?" - the Decision Engine answers "out of everything that's
true right now, what matters most?"

No new tools required - the Decision Engine is a reasoning/scoring layer built entirely on
data already flowing through Memory (8) from the other 13 systems.

---

## 14. Decision Engine

### Purpose

Continuously answer six standing questions by scoring and ranking every active item
(lead, client, task, opportunity) in memory - so the owner's attention is always directed
at the single highest-leverage thing, never at a list they have to triage themselves.

This layer behaves like a **combined COO (operational prioritization - what's at risk,
what's blocked, what needs resourcing) and Chief of Staff (executive framing - what
deserves the owner's specific attention today, filtered for relevance and urgency)**.

### Inputs

The Decision Engine reads from every other layer - it produces nothing new on its own,
only synthesizes:

| Source Layer | What's Read |
|---|---|
| Lead Management (1) | Lead records: source, audit results, outreach status, time since last contact, response history |
| Client Management (2) | Client profiles: contract value, last contact date, sentiment signals, open requests |
| Content Production (3) | In-progress/completed deliverables, time-in-queue, QC status |
| Internal Operations (4) | SLA breach flags |
| Revenue Layer (11) | MRR, payment status per client, overdue amounts and durations |
| SOP Layer (12) | Compliance records, step completion times, skipped steps |
| KPI Layer (13) | Weekly/4-week trend data for all tracked KPIs |
| Task Management (7) | All pending approval items, age of each item |

### Outputs

1. **Daily Decision Brief** (feeds the Dashboard's "FOCUS TODAY" section) - the top 1-3
   ranked actions for today, each with a one-line "why this, why now"
2. **Standing Answers** to the six core questions (recomputed daily, available on-demand)
3. **Escalation flags** - items that have crossed a threshold and need owner attention
   regardless of the daily ranking
4. **A priority-scored backlog** - everything else, ranked but not surfaced unless asked
   ("show me everything")

---

## The Six Standing Questions - Decision Rules & Priority Scoring

Each question below has: (a) the data inputs used, (b) the scoring formula, (c) how ties
are broken, and (d) what triggers escalation outside the normal daily ranking.

### 1. What should the owner focus on today?

**This is the meta-question** - its answer is the *union* of the top-ranked item from
each of questions 2-6 below, further ranked against each other using a single combined
score:

```
Focus Score = (Business Impact × Urgency × Confidence) / Owner Effort Required
```

Where:
- **Business Impact** (1-10): derived from Revenue Layer (contract value / MRR at stake)
  or KPI Layer (effect on conversion rate, etc.)
- **Urgency** (1-10): how quickly the situation degrades if not acted on (e.g., overdue
  payment compounds daily; a lead going cold over 1 week has lower daily urgency)
- **Confidence** (0.0-1.0): how certain the Decision Engine is that this is the right
  call (lower confidence items get surfaced as "FYI" rather than "do this")
- **Owner Effort Required** (1-10): estimated minutes/10 (e.g., a 5-minute approval = 0.5;
  a 50-minute strategic decision = 5)

**Decision Rule:** Surface the top 1-3 items by Focus Score where Confidence >= 0.6.
Items with Confidence < 0.6 are never put in "FOCUS TODAY" - they go to "OPPORTUNITIES"
or "FYI" instead, since low-confidence recommendations as direct instructions erode trust
in the system.

**Tie-breaking:** If two items have similar Focus Scores, prefer the one with the higher
**Urgency** (time-sensitive beats important-but-not-urgent, on the theory that important
items will simply re-rank higher tomorrow if not addressed, while urgent items may not
get a second chance).

### 2. What is the highest ROI action available?

**Inputs:** Revenue Layer (potential revenue impact), KPI Layer (potential conversion/
efficiency impact), Content Production (effort required for the action)

**Scoring:**
```
Action ROI = Estimated Value Created / Estimated Effort (owner minutes)
```

Examples of "Estimated Value Created":
- Sending a drafted proposal to a qualified lead with high audit-fit score → value =
  expected contract value × lead-close probability (see Question 4)
- Approving a generated upsell pitch for an existing client → value = estimated upsell MRR
- Resolving a blocked SOP step that's holding up 3 other items → value = unblocked
  downstream value (sum of blocked items' value)

**Decision Rule:** Recompute the full backlog's Action ROI daily; the single highest-ROI
action (above a minimum value threshold, e.g., >$50 estimated value) is always a candidate
for "FOCUS TODAY," subject to the Confidence >= 0.6 gate above.

### 3. Which client is most at risk?

**Inputs:** Client Management (last contact date, sentiment), Revenue Layer (payment
status), SOP Layer (whether onboarding/process steps were completed on schedule)

**Scoring (Client Risk Score, 0-100):**
```
Risk Score = (Days Since Last Positive Contact × 2)
            + (Overdue Payment Days × 3)
            + (SOP Steps Skipped/Overdue for this client × 10)
            + (Negative Sentiment Signal? +20 : 0)
            + (Contract Value Weight: Risk Score × (Contract Value / Average Contract Value))
```

The **Contract Value Weight** ensures that risk to a high-value client is amplified - a
mildly-at-risk $5,000/mo client outranks a severely-at-risk $200/mo client.

**Decision Rule:** Any client with Risk Score > 50 is escalated immediately (see
Escalation Logic). Clients with Risk Score 25-50 appear in "CLIENTS NEEDING ATTENTION" on
the dashboard but don't escalate outside the normal cycle.

### 4. Which lead is most likely to close?

**Inputs:** Lead Management (audit results - does the lead have a clear, addressable
problem the agency solves?), response history (did they reply to outreach?), source
quality (referral vs. cold inbound, tracked in memory over time as a learned signal)

**Scoring (Lead Close-Probability, 0.0-1.0):**
```
Close Probability = Base Rate (from KPI Layer's historical conversion rate)
                   × Response Multiplier (replied=1.5, no reply yet=1.0, unresponsive
                     after 2 follow-ups=0.3)
                   × Audit-Fit Multiplier (audit found 3+ addressable issues=1.3,
                     1-2=1.0, 0=0.6)
                   × Source Multiplier (referral=1.4, inbound=1.0, cold=0.7 - learned
                     from memory's historical close rates by source)
```

**Decision Rule:** The lead with the highest Close Probability AND no pending action
(i.e., not already waiting on the owner) is surfaced as "highest-probability lead" in
Question 6 (opportunities) or directly in "FOCUS TODAY" if it requires an owner action
(e.g., "this lead replied positively - approve the proposal").

### 5. What task is creating the biggest bottleneck?

**Inputs:** Task Management (age of pending items), SOP Layer (which steps are blocked
across multiple items), Content Production (queue depth)

**Scoring (Bottleneck Score):**
```
Bottleneck Score = (Number of Downstream Items Blocked) × (Average Age of Blocked Items
                    in days) × (Average Value of Blocked Items)
```

A single pending approval that's blocking 3 client deliverables (each worth $X) scores
much higher than 3 independent low-value pending items.

**Decision Rule:** The highest Bottleneck Score item is always evaluated for "FOCUS
TODAY" - clearing a true bottleneck has outsized leverage (it unblocks multiple downstream
items at once), so it gets a Focus Score boost via the "Business Impact" term (Question
1) equal to the sum of unblocked value, not just its own value.

### 6. What opportunity deserves immediate attention?

**Inputs:** Communication Layer (upsell signals detected in client emails - e.g., "we're
also thinking about X"), KPI Layer (capacity signals - e.g., SOPs completing faster,
suggesting bandwidth for more clients), Lead Management (re-engagement candidates - leads
gone cold but with high original audit-fit)

**Scoring (Opportunity Score):**
```
Opportunity Score = Potential Value × Recency (signals decay over time - an upsell hint
                     from 3 weeks ago is worth less than one from yesterday) × Strategic
                     Fit (does this match the agency's stated focus areas in the SOP
                     Layer's service-offering definitions?)
```

**Decision Rule:** Opportunities require **Confidence >= 0.7** (higher bar than other
questions) before appearing in "FOCUS TODAY," because acting on a misread opportunity
signal (e.g., misinterpreting a casual comment as a buying signal) has a relationship cost.
Below 0.7, opportunities appear in the dashboard's "OPPORTUNITIES" section as FYI items
only.

---

## Escalation Logic

Escalation means: **bypass the daily ranking cycle and notify the owner immediately**
(via Slack, Communication Layer) rather than waiting for the next Daily Decision Brief.

| Trigger | Threshold | Action |
|---|---|---|
| Client Risk Score | > 50 | Immediate Slack alert: "[Client] is at risk - [top contributing factor]. Recommend: [action]." |
| Overdue payment | > 14 days | Immediate alert, separate from general risk - cash flow is time-sensitive |
| Bottleneck Score | Blocks >= 3 downstream items | Immediate alert: "[Task] is blocking 3 deliverables worth $X total - resolving this unblocks the most value available today" |
| SOP compliance | Drops below 70% for any active SOP, sustained 2+ weeks | Weekly alert (not immediate) - flagged in Weekly Review, not urgent enough for same-day interruption |
| High-confidence opportunity | Confidence >= 0.85 AND Potential Value > 2× average client MRR | Immediate alert - large opportunities decay fastest and have the highest regret-if-missed |
| Lead close probability | Crosses from <0.5 to >=0.7 (e.g., a cold lead suddenly replies positively) | Immediate alert - "hot lead" status changes are time-sensitive |

**Design principle:** Escalations are rare by design. If escalations are firing more than
~2-3 times per week, the thresholds are miscalibrated (too sensitive) and should be
reviewed in the Monthly Review (below) - frequent interruptions defeat the "minimal owner
attention" goal.

---

## Approval Requirements

The Decision Engine **never takes action itself** - it only ranks, scores, and
recommends. Every approval requirement from Systems 1-13 (consolidated list in
`AGENCY_OS.md`, extended by Revenue/SOP layers in V2) still applies. The Decision Engine
adds exactly one new approval type:

- **"Accept this recommendation" vs. "Dismiss/reprioritize"** - when the Decision Engine
  surfaces a "FOCUS TODAY" item, the owner can:
  1. **Act on it** (which triggers the underlying approval from the relevant system, e.g.,
     "send this email")
  2. **Dismiss it** ("not now, deprioritize") - the Decision Engine logs this and adjusts
     that item's Urgency decay rate so it doesn't resurface at the same priority tomorrow
     without a real change in underlying data
  3. **Reprioritize** ("actually, focus on X instead") - the Decision Engine logs the
     owner's manual override; if overrides happen repeatedly for similar item types, this
     is flagged in the Monthly Review as a sign the scoring weights need adjustment

This makes the Decision Engine **self-correcting**: owner dismissals and overrides are
themselves data that refines future scoring (see Monthly Review).

---

## Dashboard Integration

The Decision Engine replaces the *ranking logic* behind the V2 dashboard's "FOCUS TODAY"
and "OPPORTUNITIES" sections - the dashboard's visual structure from V2 stays the same, but
the content is now driven by the scoring model above rather than a simple chronological or
category-based list.

### Updated Dashboard Flow

```
Memory (8) → [Lead Mgmt, Client Mgmt, Revenue, SOP, KPI, Task Mgmt - all 13 prior systems]
                              │
                              ▼
                    DECISION ENGINE (14)
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
    Daily Decision Brief   Escalation Flags   Priority-Scored Backlog
            │                 │                 │
            ▼                 ▼                 ▼
    "FOCUS TODAY"      Immediate Slack    "show me everything"
    (Dashboard)         alert (any time)   (on-demand, full list)
```

### Dashboard Section Changes from V2

| Dashboard Section | V2 Source | V3 Source |
|---|---|---|
| 💰 MONEY COMING IN | Revenue Layer (raw numbers) | Unchanged - factual reporting |
| 📋 ACTIVE LEADS | Lead Mgmt (raw counts) | Unchanged - factual reporting, + highlight from Q4 (highest close-probability lead) |
| ⚠️ CLIENTS NEEDING ATTENTION | Client Mgmt + Revenue + SOP (raw flags) | Now ranked by Risk Score (Q3) - highest-risk client listed first, with score shown |
| 🚧 BLOCKED TASKS | Task Mgmt (raw list, by age) | Now ranked by Bottleneck Score (Q5) - the task unblocking the most value listed first |
| 🎯 OPPORTUNITIES | Various (unranked) | Now ranked by Opportunity Score (Q6), filtered to Confidence >= 0.7 |
| 👉 FOCUS TODAY | Task Mgmt items by urgency | **Now the Decision Engine's top 1-3 Focus Score items (Q1)** - the headline change in V3 |

**New dashboard line** (added at the top, before "MONEY COMING IN"):

```
🧭 TODAY'S #1 PRIORITY: [single highest Focus Score item]
   Why: [one-line reasoning citing the specific score components]
   Action: [exact action - "approve," "send," "decide," "review"]
   Estimated time: [X minutes]
```

This single line is designed so that **a busy owner who reads nothing else still gets the
one thing that matters most today** - everything below it is supporting detail.

---

## Weekly Review Process

**When:** Every Monday, as part of the existing Executive Dashboard delivery (V2's
schedule - no new cadence introduced).

**What happens automatically (no owner time required):**
1. Decision Engine recomputes all six standing-question scores using the past week's data.
2. Compares this week's "FOCUS TODAY" picks against what the owner actually did (accepted/
   dismissed/overrode) - logs the hit rate (% of recommendations accepted as-is).
3. Updates the Lead Close-Probability model's "Base Rate" using the actual conversions
   from the past week (the model gets more accurate over time as more data accumulates).
4. Surfaces any sustained escalation triggers (SOP compliance trend, see Escalation Logic
   table) that didn't warrant a same-day alert but should be reviewed weekly.

**What the owner does (target: <5 minutes):**
- Reads the dashboard (per V2/V3 structure above) - this IS the weekly review from the
  owner's perspective. No separate "review meeting" is required.
- Optionally: dismiss/reprioritize any items, which feeds back into next week's scoring
  (per Approval Requirements above).

---

## Monthly Review Process

**When:** First Monday of each month, as an **extended** version of the weekly dashboard
- same delivery channel (Slack), longer content.

**What happens automatically:**
1. **Recommendation accuracy report**: hit rate of "FOCUS TODAY" recommendations over the
   past month (% accepted vs. dismissed vs. overridden), broken down by question type
   (Q1-Q6) - identifies which scoring models are working well vs. need recalibration.
2. **Scoring weight review**: if overrides cluster around a specific item type (e.g., the
   owner consistently reprioritizes away from "highest ROI action" toward "client risk"
   items), the Decision Engine proposes an adjusted weighting (e.g., increase the weight
   of Client Risk Score relative to Action ROI in the Focus Score formula) - **proposed,
   not auto-applied** (requires owner approval per Approval Requirements).
3. **Escalation calibration check**: if escalations fired 0 times in the month, thresholds
   may be too conservative (real risks going unflagged); if >8 times, too sensitive
   (alert fatigue). Both are reported with a suggested threshold adjustment.
4. **KPI Layer cross-check** (from V2): monthly trends in MRR, conversion rate, SOP
   compliance, and "owner time on approvals" (KPI #7) - the last one is the direct measure
   of whether the Decision Engine is achieving its goal of minimal owner attention. A
   rising trend in owner-time-on-approvals despite the Decision Engine being active is the
   single most important signal that something needs to change.

**What the owner does (target: 15-20 minutes, once a month):**
- Reviews the recommendation accuracy report and approves/rejects proposed scoring weight
  changes.
- Reviews escalation calibration and approves/rejects threshold adjustments.
- Optionally: redefines or adds SOPs (SOP Layer, V2) based on patterns noticed in the
  monthly data - e.g., "every time we get a referral lead, close probability is high -
  let's create a 'Referral Lead Fast-Track' SOP."

---

## Why This Behaves Like a Combined COO + Chief of Staff

| Role | What They'd Normally Do | Decision Engine Equivalent |
|---|---|---|
| **COO** | Monitor operations, identify bottlenecks, ensure processes run smoothly, flag operational risks | Bottleneck Score (Q5), Client Risk Score (Q3), SOP compliance escalations |
| **Chief of Staff** | Filter information reaching the executive, prioritize the executive's calendar/attention, frame decisions with context | Focus Score (Q1) ranking, Confidence gating (low-confidence items don't reach the owner), "Today's #1 Priority" framing |
| **Both combined** | Translate "everything happening in the business" into "here's what you, specifically, need to do, and why" | The entire Decision Engine output - daily brief + escalations + weekly/monthly reviews |

---

## Implementation Order (Extends V1 + V2)

V3 should be implemented **last**, after V1 (Systems 1-10) and V2 (Systems 11-13, dashboard
redesign) have been running long enough to produce:
- At least 4-8 weeks of lead conversion history (for Question 4's Base Rate)
- At least 4 weeks of KPI trend data (for Question 1's Urgency calibration)
- At least one full SOP cycle per service type (for Question 5's bottleneck detection)

**Steps:**
1. Stand up the six scoring formulas using existing historical memory data (retroactive
   scoring - no waiting required once V1+V2 data exists).
2. Run the Decision Engine in "shadow mode" for 1-2 weeks: it computes recommendations but
   they're shown alongside (not replacing) the V2 dashboard, so the owner can compare.
3. Once recommendations look reasonable (owner accepts most of them in shadow mode),
   switch the dashboard's "FOCUS TODAY" and "OPPORTUNITIES" sections to Decision-Engine-
   driven (full V3 dashboard).
4. Begin the Weekly Review process (automatic from week 1 of full V3).
5. First Monthly Review occurs after 4 full weeks of full-V3 operation.

---

## Business Impact Summary (V3 vs V2)

| | V2 | V3 |
|---|---|---|
| Owner's role | Read activity + revenue summary, act on a list of pending items | Read ONE prioritized recommendation + supporting context, act on it |
| How items are ordered | By category (leads, clients, tasks, opportunities) | By cross-cutting Focus Score - the single most important thing regardless of category |
| Risk detection | Flagged when thresholds crossed | Proactively scored and ranked continuously; escalates only the truly urgent |
| System improves over time? | No - same logic every week | Yes - Weekly Review updates close-probability model; Monthly Review recalibrates scoring weights based on owner feedback |
| Closest human-role analogy | A good executive assistant (organizes information) | A COO + Chief of Staff (organizes information AND tells you what to do about it) |

V3 completes the transition from "a system that tells the owner what happened" (V1
Reporting) to "a system that tells the owner what to do" (V3 Decision Engine) - while
preserving every approval gate from V1 and V2, so the increase in leverage does not come
at the cost of control.
