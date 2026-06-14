# Post-Implementation Audit - 30-Day Review Template & Methodology

## Important Note on This Document

This document is a **template and data-collection methodology**, not a completed audit.
As of this writing, the Agency OS (V1-V3, defined in `AGENCY_OS.md`,
`AGENCY_OS_V2.md`, `AGENCY_OS_V3.md`) has been **designed but not yet operated for 30
days** - there is no real usage history in memory to analyze yet.

Producing a "real" audit with fabricated numbers would defeat the stated goal:
**"optimization based on real behavior, not assumptions."** Instead, this document
provides:

1. The exact data sources and queries to run against `claude-mem` after 30 days of real
   operation
2. The structure every section of the final audit must follow
3. A worked **illustrative example** (clearly marked as hypothetical) showing what
   "good" findings look like, so the format is ready to use the moment real data exists

**To produce the real audit:** run this template against the Memory Layer (System 8) and
KPI Layer (System 13) after 30 consecutive days of `FIRST_AUTOMATION.md` / Agency OS
operation, replacing every `[DATA]` placeholder with actual figures.

---

## Data Sources for the Real Audit

| Section | Memory Query / Source |
|---|---|
| Most/Least Used Automations | Count of invocations per system (1-14) logged in memory's activity history, last 30 days |
| False Positives | Items the Decision Engine (14) or Lead/Client classification (Systems 1-2) flagged, that the owner subsequently dismissed/corrected (logged via the "Dismiss/Reprioritize" mechanism in V3) |
| False Negatives | Items the owner had to manually raise/handle that the system never flagged (requires owner to log these via a simple "the system missed this" note - the one piece of data collection that can't be fully automated) |
| Bad/Good Recommendations | Decision Engine's monthly "recommendation accuracy report" (V3 Monthly Review) - acceptance vs. dismissal vs. override rates per question type (Q1-Q6) |
| Time Actually Saved | KPI #7 ("owner time spent on approvals") compared against the V1 baseline estimate in `AGENCY_OS.md`'s Expected Time Savings table |
| Processes Still Manual | SOP Layer (12) compliance records - any SOP step consistently marked "owner did this manually" rather than completed by an automated system |
| New Bottlenecks | Decision Engine's Bottleneck Score (Q5) history - items with sustained high scores that weren't present in the original `AGENCY_OS.md` design |
| Recommended Improvements/Removals/Automations | Synthesis of all of the above, cross-referenced against `master_inventory.xlsx` for any Tier 3/4 capability that would address a recurring gap |

---

## Audit Structure (Complete This After 30 Days)

### 1. Most Used Automations

List the systems (1-14) ranked by invocation count over 30 days, with a one-line note on
why each is/isn't surprising given the original design intent.

```
| Rank | System | Invocations (30d) | Expected? |
|------|--------|--------------------|-----------|
| 1    | [DATA] | [DATA]             | [DATA]    |
| 2    | [DATA] | [DATA]             | [DATA]    |
...
```

**Illustrative example (hypothetical):**
> Communication Layer (9) and Memory Layer (8) are used on every single interaction by
> design (continuous), so they're excluded from ranking - this section ranks the
> *discretionary* systems (1-7, 11-14). In a typical first month, Lead Management (1) and
> Content Production (3) are usually the most-invoked discretionary systems, since they
> map to the highest-frequency daily activities (new emails, content requests).

---

### 2. Least Used Automations

Same ranking, inverted - systems invoked rarely or never in 30 days.

**Illustrative example (hypothetical):**
> The SOP Layer (12) and KPI Layer (13) are often the least-invoked in month 1, simply
> because they require 2-4 weeks of history to produce meaningful output (per
> `AGENCY_OS_V2.md`'s implementation order) - low usage here in month 1 is *expected*, not
> a problem. A genuinely concerning "least used" finding would be a System 1-4 capability
> (e.g., Open Design Studio) that was installed but never invoked despite relevant
> requests existing in the inbox - that would indicate either a workflow gap (the system
> doesn't know to use it) or a training gap (the owner doesn't know it's available).

---

### 3. False Positives

Cases where the system flagged/acted on something it shouldn't have (e.g., classified a
non-lead as a lead, flagged a healthy client as "at risk," escalated something that wasn't
urgent).

```
| Date | System | What Was Flagged | Why It Was Wrong | Correction Made |
|------|--------|-------------------|--------------------|-------------------|
| [DATA] | [DATA] | [DATA] | [DATA] | [DATA] |
```

**Illustrative example (hypothetical):**
> A vendor's automated "your invoice is ready" email gets classified as a "new lead"
> because the sender wasn't in memory yet. **Correction:** add a rule to Lead Management
> (1) that excludes senders matching known vendor/service-provider domains (a short
> deny-list in memory) before the new-lead classification runs.

---

### 4. False Negatives

Cases where something needed attention but the system never surfaced it - the owner had
to notice it manually.

```
| Date | What Was Missed | Which System Should Have Caught It | Why It Was Missed |
|------|-------------------|----------------------------------------|---------------------|
| [DATA] | [DATA] | [DATA] | [DATA] |
```

**Illustrative example (hypothetical):**
> A client mentioned in a casual Slack message (not email) that they were "considering
> other agencies" - a major Client Risk signal (System 12/14) - but the Risk Score (V3,
> Q3) only reads sentiment from Gmail, not Slack DMs. **Fix:** extend Client Management
> (2) and the Risk Score's sentiment input to include Slack messages, not just email.

---

### 5. Bad Recommendations

Decision Engine (14) "FOCUS TODAY" items that, in hindsight, were not actually the right
priority - logged via the V3 "Dismiss/Reprioritize" mechanism.

```
| Date | Recommended Action | What Owner Did Instead | Why the Recommendation Was Wrong |
|------|----------------------|---------------------------|--------------------------------------|
| [DATA] | [DATA] | [DATA] | [DATA] |
```

**Illustrative example (hypothetical):**
> Decision Engine recommended "follow up with Lead X" (high Close Probability score)
> ahead of "respond to Client Y's scope-change request" (lower Focus Score due to
> Confidence < 0.6 on the ambiguous request). The owner correctly prioritized Client Y -
> existing-client retention should generally outrank new-lead pursuit when both are
> time-sensitive. **Fix:** in the Monthly Review (V3), increase the Business Impact
> weighting for existing-client items relative to new-lead items in the Focus Score
> formula - existing revenue at risk is generally higher-stakes than potential new
> revenue.

---

### 6. Good Recommendations

The inverse - "FOCUS TODAY" items the owner accepted as-is, especially any that the owner
notes they "wouldn't have caught on their own."

```
| Date | Recommended Action | Outcome | Value Created |
|------|----------------------|----------|------------------|
| [DATA] | [DATA] | [DATA] | [DATA] |
```

**Illustrative example (hypothetical):**
> Decision Engine flagged an overdue-payment escalation (Revenue Layer, V2) for a client
> 15 days past due - the owner hadn't checked invoices that week and would likely have
> missed it for several more days. Payment was collected the same day after a direct
> follow-up. **Value created:** ~2 weeks of cash-flow delay avoided, ~zero owner time
> spent finding the issue (system found it).

---

### 7. Time Actually Saved

Compare actual KPI #7 ("owner time on approvals," V2/V3) data against the V1 baseline
estimate.

```
| System | V1 Estimated Savings (hrs/wk) | Actual Owner Time Spent (hrs/wk) | Actual Savings |
|--------|-------------------------------|-------------------------------------|------------------|
| Lead Management (1) | ~3.5 | [DATA] | [DATA] |
| Client Management (2) | ~2.5 | [DATA] | [DATA] |
| Content Production (3) | ~7 | [DATA] | [DATA] |
| Internal Operations (4) | ~1.5 | [DATA] | [DATA] |
| Reporting (5) | ~2.5 | [DATA] | [DATA] |
| Executive Dashboard (6) | ~1.5 | [DATA] | [DATA] |
| **Total** | **~12-22** | **[DATA]** | **[DATA]** |
```

**Note:** `AGENCY_OS.md`'s original estimates were explicitly labeled "directional, not
measured" - this section is where they get replaced with real numbers. A large gap
between estimated and actual (in either direction) should be investigated: if actual
savings are much lower, look for "Processes Still Manual" (section 9) explaining why; if
much higher, the V1 estimate was conservative and can be revised upward for future
planning.

---

### 8. Processes Still Manual

Direct from SOP Layer (12) compliance records - any step that's *supposed* to be automated
per the Agency OS design but is, in practice, still done by the owner/team every time.

```
| Process / SOP Step | Designed To Be Automated By | Why It's Still Manual |
|------------------------|--------------------------------|---------------------------|
| [DATA] | [DATA] | [DATA] |
```

**Illustrative example (hypothetical):**
> "Final QC review before sending generated content to clients" (Content Production,
> System 3) is, by design, the *one* manual approval point in that system - finding it
> here is expected and correct, not a gap. A genuinely concerning finding would be
> something like "drafting the lead-outreach email" still being done manually because the
> marketing-skills-bundle output quality wasn't trusted - that indicates a prompt/quality
> issue to fix, not a permanent manual step.

---

### 9. New Bottlenecks

Decision Engine Bottleneck Score (Q5) items with sustained high scores over the 30-day
period that weren't anticipated in the original `AGENCY_OS.md` design.

```
| Bottleneck | First Appeared | Sustained Score | Root Cause | Anticipated in V1-V3 Design? |
|------------|-------------------|---------------------|---------------|----------------------------------|
| [DATA] | [DATA] | [DATA] | [DATA] | [DATA] |
```

**Illustrative example (hypothetical):**
> "Design System creation for new clients" (V2 expansion item, `150 brand-grade Design
> Systems`) becomes a bottleneck if client onboarding volume exceeds 1-2/week and each new
> Design System still requires ~30 min of manual brand-palette setup. **Root cause:** the
> 150 pre-built templates cover common brand archetypes well, but bespoke brands still
> need manual adaptation. This was *not* explicitly flagged as a bottleneck risk in V1-V3.

---

### 10. Recommended Improvements

Synthesis - changes to existing systems (1-14) based on sections 3-9 above. Each
improvement should cite which finding(s) motivated it.

```
| Improvement | Motivated By | Affected System(s) | Effort to Implement |
|----------------|------------------|------------------------|--------------------------|
| [DATA] | [DATA] | [DATA] | [DATA] |
```

---

### 11. Recommended Removals

Capabilities from `INSTALL_NOW.md`/`ACTION_PLAN.md` that, after 30 days, are not earning
their setup/maintenance cost - i.e., genuinely unused (section 2) with no expected
ramp-up justification.

```
| Capability | Usage (30d) | Setup/Maintenance Cost | Recommendation |
|----------------|----------------|----------------------------|---------------------|
| [DATA] | [DATA] | [DATA] | [DATA] |
```

**Guardrail:** Do not recommend removing anything that's part of the Memory (8) or
Communication (9) layers - these are foundational and their value is structural, not
measured by direct invocation count. This section should focus on optional/Tier 2 add-ons
only (e.g., if "150 brand-grade Design Systems" went entirely unused because all clients
have bespoke brands, that's a candidate for removal/deprioritization - but Memory itself
being "low usage" by some naive metric would be a misread of its role).

---

### 12. Recommended Automations (New)

Based on sections 4 (false negatives), 8 (manual processes), and 9 (new bottlenecks),
identify specific new automations - prefer ones achievable with capabilities already in
`master_inventory.xlsx` (Tier 3, on-demand) before recommending anything not yet
catalogued.

```
| New Automation | Addresses | Source Capability (if exists in inventory) | Tier |
|--------------------|---------------|--------------------------------------------------|---------|
| [DATA] | [DATA] | [DATA] | [DATA] |
```

**Illustrative example (hypothetical):**
> If section 9's "Design System creation bottleneck" materializes, the recommended
> automation is to pre-generate Design Systems for the agency's 3-5 most common client
> archetypes (e.g., "SaaS startup," "local service business," "e-commerce") during a quiet
> week, so onboarding becomes "pick the closest match" instead of "create from scratch" -
> this uses only the already-installed Open Design Studio (no new Tier capability needed).
> If false negatives in section 4 (Slack-based sentiment) recur, the recommended
> automation is extending the existing gmail/slack-automation skill's scope (already
> installed, Tier 2) to include sentiment scanning of client Slack channels - no new
> capability required, just an expanded prompt/scope for an existing one.

---

## How to Run This Audit

1. **Set a reminder** for 30 days after Agency OS V1 implementation begins (per
   `ACTION_PLAN.md` Week 1 start date).
2. **On day 30**, ask Claude: *"Run the Post-Implementation Audit using
   POST_IMPLEMENTATION_AUDIT.md as the template - pull 30 days of memory data and fill in
   every [DATA] placeholder with real figures."*
3. Claude will query the Memory Layer (8) and KPI Layer (13) for the relevant counts,
   timestamps, and Decision Engine logs (if V3 is active) or note where V3 isn't active
   yet and adjust sections 5-6 accordingly (those sections require the Decision Engine).
4. Review sections 10-12 (Improvements, Removals, New Automations) as the actionable
   output - these become the input to the next Monthly Review (`AGENCY_OS_V3.md`).
5. **Repeat monthly** thereafter - the Monthly Review process in `AGENCY_OS_V3.md` already
   covers ongoing recalibration; this 30-day audit is most valuable as the *first* one,
   establishing the baseline that V3's monthly cadence will build on.

---

## Why No Fabricated Data Is Included

Every illustrative example above is explicitly labeled "(hypothetical)" and describes
*plausible categories of findings* based on the system design (e.g., "the SOP Layer will
have low usage in month 1 because it needs 2-4 weeks of history" follows directly from
`AGENCY_OS_V2.md`'s own implementation-order guidance, not from invented usage stats).
Presenting invented numbers (e.g., "saved 14.3 hours this month") as if they were measured
would violate the explicit goal of this audit - "optimization based on real behavior, not
assumptions" - by adding a *new* layer of assumption disguised as data. This template is
designed to be filled in with one command once real data exists.
