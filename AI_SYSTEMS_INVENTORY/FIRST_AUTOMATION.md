# First Automation - Daily Agency Operations Loop

**Built from tools installed in `INSTALL_NOW.md` only:**
1. 51 Marketing Skills bundle (claude-skills)
2. Open Design Studio (open-design)
3. Persistent Memory Hooks (claude-mem)
4. Landing Page Generator (claude-skills)
5. Gmail / Slack Automation (Composio)

No new installs, no new API keys, no new accounts. This document combines the 5 tools
above into one repeatable workflow you run **once per day** (or trigger ad-hoc), covering
marketing agency operations, lead management, internal reporting, and client
communication in a single pass.

---

## Why This Workflow Is the Highest-ROI Combination

Each of the 5 installed tools is useful alone, but they compound when chained:

- **Gmail/Slack automation** is the *input* (new leads, client emails, team questions
  arrive here).
- **Persistent memory** is the *context layer* (remembers each client's brand, status,
  open items - so nothing has to be re-explained).
- **Marketing skills bundle** is the *production engine* (turns a request into an audit,
  copy, or content plan).
- **Landing page generator + Open Design Studio** are the *output layer* (turns a
  production result into a deliverable asset).
- **Slack** is also the *reporting layer* (the daily summary goes back out automatically).

One loop touches all four target areas - marketing ops, leads, reporting, and client
comms - with a single trigger.

---

## The Workflow: "Morning Agency Brief + Auto-Response Loop"

### Trigger
Once a day (recommended: first thing in the morning), or on-demand whenever you say
**"Run the morning brief."**

### Step-by-Step (what Claude does automatically)

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. SCAN (Gmail/Slack automation)                                  │
│    - Read unread Gmail from the last 24 hours                     │
│    - Read unread Slack messages in client/team channels           │
└────────────────────────┬────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. CLASSIFY (Memory + reasoning, no extra tool)                   │
│    Sort each item into one of three buckets:                      │
│    - NEW LEAD  (inbound inquiry, never seen this contact before)  │
│    - CLIENT REQUEST  (existing client asking for work/status)     │
│    - INTERNAL  (team question, FYI, admin)                        │
└────────────────────────┬────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3a. NEW LEAD path           │ 3b. CLIENT REQUEST path             │
│  - Marketing skills bundle: │  - Memory: recall this client's     │
│    draft a tailored reply   │    brand/Design System + open tasks │
│    + run a quick SEO/site   │  - If request = "send me a landing  │
│    audit on their domain    │    page / asset" → Landing Page     │
│    if provided              │    Generator or Open Design Studio  │
│  - Memory: save lead as new │    produces the deliverable         │
│    contact + audit summary  │  - Marketing skills bundle: draft   │
│  - Draft (not send) a Gmail │    the reply email referencing the  │
│    reply with audit findings│    deliverable + next steps          │
│    + a discovery-call CTA   │  - Draft (not send) reply email     │
└────────────────────────┬────┴──────────────┬──────────────────────┘
                          ▼                   ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. REPORT (Slack automation + Memory)                              │
│    Post one "Morning Brief" message to your team Slack channel:   │
│    - X new leads (with names + audit highlights)                  │
│    - Y client requests (with what was drafted/generated)          │
│    - Z internal items needing a human decision                     │
│    - Links/attachments to any generated landing pages/designs      │
│    - Memory is updated so tomorrow's brief only covers what's NEW  │
└─────────────────────────────────────────────────────────────────┘
```

### What Gets Automated vs. What You Still Do

| Action | Automated? | Your Role |
|--------|-----------|-----------|
| Reading inbox/Slack | Fully automated | None |
| Sorting leads vs. clients vs. internal | Fully automated | None |
| SEO/site audit for new leads | Fully automated | None |
| Drafting reply emails | Fully automated (drafts only) | Review + click send |
| Generating landing pages/decks for client requests | Fully automated | Review output |
| Remembering client context across days | Fully automated | None |
| Daily summary to Slack | Fully automated | Read the brief |
| Sending emails | **Manual (by design)** | Approve/send drafts |
| Final decisions on internal items | **Manual (by design)** | Review the 2-3 flagged items |

**Design principle:** Everything that can be drafted, audited, classified, generated, or
summarized is automated. The only manual steps left are the two things that *should*
require a human - approving outbound emails and making judgment calls on internal items -
keeping risk low while removing ~90% of the repetitive work.

---

## How to Run It

### Option 1 - On-demand (start here, no setup)
Simply tell Claude:
> "Run the morning brief: check my unread Gmail and Slack from the last 24 hours, sort
> into new leads / client requests / internal items, draft replies for leads and clients
> using the marketing skills, generate any requested landing pages or designs, save
> everything to memory, and post a summary to the #team Slack channel."

This works immediately with the 5 tools already installed - no scheduling needed.

### Option 2 - Scheduled (once comfortable with Option 1)
Once the on-demand version has run successfully for a few days, ask Claude to set up a
recurring trigger (e.g., a daily hook via claude-mem's companion-skill scheduling, covered
in `ACTION_PLAN.md` Week 4) so the morning brief runs automatically without you asking.
*(This step uses Tier 2 capabilities already on your roadmap - no new tools beyond what's
in this document's scope are required to keep running Option 1 manually in the meantime.)*

---

## Example Run-Through (Realistic Scenario)

**Morning brief input:**
- 2 unread emails: one from "hello@newcafe.com" (never seen before, asking about SEO
  help), one from "client@acmeretail.com" (existing client, asking for a "quick landing
  page for our summer sale")
- 1 Slack message in #team: "Did anyone follow up with the newcafe lead?"

**What happens automatically:**
1. Gmail/Slack automation pulls both emails + the Slack message.
2. Memory check: "newcafe.com" is not in memory → classified as **NEW LEAD**. "acmeretail.com"
   is in memory with a saved Design System → classified as **CLIENT REQUEST**.
3. For the new lead: marketing skills bundle runs a quick SEO audit on newcafe.com,
   drafts a reply email summarizing 3 quick-win findings and offering a discovery call.
   Memory saves "New Cafe - inbound lead, SEO audit sent [date], awaiting reply."
4. For the client request: memory recalls Acme Retail's Design System (brand colors,
   voice). Landing Page Generator produces a "Summer Sale" landing page using that brand
   data. Marketing skills bundle drafts a reply email: "Here's your summer sale landing
   page - [preview], let me know if you'd like any tweaks."
5. The Slack question "Did anyone follow up with the newcafe lead?" is flagged as
   **INTERNAL - needs human reply** (since it's a question directed at the team, not a
   task Claude should resolve unilaterally).
6. Slack #team gets a single Morning Brief message:
   > **Morning Brief**
   > - 🆕 1 new lead: New Cafe (SEO audit sent as draft, 3 quick wins found - review &
   >   send)
   > - 📋 1 client request: Acme Retail summer-sale landing page generated (review &
   >   send to client)
   > - ❓ 1 internal item needs a reply: "Did anyone follow up with the newcafe lead?"
   >   (answer: audit drafted, awaiting your send)

**Your total manual work:** Review and click "send" on 2 draft emails, and reply "yes,
audit drafted - sending now" in Slack. ~5 minutes, down from what would otherwise be a
30-60 minute research + writing + design task.

---

## Next Steps

- Run this workflow daily for one week using Option 1.
- After one week, review what's in memory (`ACTION_PLAN.md` Item #3/#7) and confirm the
  classification (lead vs. client vs. internal) is matching reality - adjust the prompt
  wording if needed.
- Once stable, move to Option 2 (scheduled) and proceed with the remaining Tier 2 items in
  `ACTION_PLAN.md` (Open Design Studio for richer deliverables, GitHub/Jira/Linear/Notion
  automation for internal project tracking, LLM Council for any strategic decisions that
  come out of the morning brief).
