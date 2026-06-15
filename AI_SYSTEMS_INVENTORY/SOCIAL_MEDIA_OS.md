# Social Media Operations Layer

A new layer in the Agency OS, alongside the Memory Layer (claude-mem +
`memory_store.json`) and the Communication Layer (Gmail/Slack via Composio). It
manages client social media accounts across 10 platforms (Instagram, Facebook,
LinkedIn, YouTube, TikTok, X, Pinterest, Bluesky, Threads, Mastodon) via
**OmniSocials** (`agency-os/omnisocials-agent-skills/`).

See `OMNISOCIALS_CAPABILITIES.xlsx` (in `agency-os/omnisocials-agent-skills/`) for the
full capability inventory, `agency-os/SOCIAL_BRIEF.md` for the daily output format,
and `OMNISOCIALS_IMPLEMENTATION_STATUS.md` for current install/connection status.

## Functional Areas

| Area | OmniSocials capability | Agency OS entry point |
|---|---|---|
| Content Publishing | `posts:create-and-publish` | `social_brief.py` recommends; a human/agent runs the publish command after approval |
| Content Scheduling | `posts:create --schedule`, `posts:update` | Weekly content-calendar batch (see Weekly Workflow) |
| Analytics Retrieval | `analytics:post`, `analytics:overview`, `analytics:accounts` | `social_brief.py` ENGAGEMENT METRICS / TOP PERFORMING POSTS |
| Account Management | `accounts:list`, `accounts:get` | Pre-flight check before any posting workflow |
| Cross-Platform Posting | `posts:create` with multiple `--channels` / per-platform media | Weekly content-calendar batch |
| Performance Reporting | `analytics:overview` (7d/30d/custom range) | Monthly KPI rollup (see Monthly Workflow) |

---

## Daily Workflow

Runs every morning, immediately after (or alongside) the Morning Brief.

1. **Run `social_brief.py --source omnisocials`** (or `--source sample` until
   OmniSocials is connected).
2. Pipeline: `accounts:list` (pre-flight) -> `posts:list` -> classify into
   Scheduled / Published / Failed / Draft -> aggregate engagement metrics for
   newly-published posts -> rank top performers -> compile action items.
3. **Output**: the Social Brief (6 sections - see `SOCIAL_BRIEF.md`), printed
   alongside the Morning Brief.
4. **Memory update**: append today's KPI snapshot to
   `memory/social_memory.json.brief_history` (posts published/scheduled/overdue/
   failed/draft, total impressions/engagements, top post ID).
5. **No automatic publishing or scheduling happens in the daily run** - it is
   read-only (`accounts:list`, `posts:list`, `analytics:*`). This matches OmniSocials
   Safety Rules #1-2 (never publish/delete without explicit confirmation).

## Weekly Workflow

Run once per week (e.g. Monday planning session), per client.

1. **Review** the past week's Social Briefs and `memory/social_memory.json` trend
   (posts published, engagement totals, items that required action).
2. **Pull weekly analytics**: `analytics:overview --period 7d` and
   `analytics:accounts` per platform, for the weekly client report.
3. **Plan next week's content calendar**: for each client, decide what to post,
   where (`--channels`), and when.
4. **Stage media**: `media:upload --url ...` for any new creative assets, noting
   returned `media_id`s.
5. **Approval point (see below)**: present the draft calendar to the client/account
   owner before scheduling.
6. **Batch-schedule**: once approved, create the week's posts as `scheduled` via
   `posts:create --schedule ...` (one call per post, confirming channel IDs from
   `accounts:list` first - never guess IDs).
7. **Resolve carry-overs**: address any `failed` posts or `draft` posts flagged in
   "Posts Requiring Action" from the daily briefs during the week.

## Monthly Workflow

Run once per month (client billing-cycle aligned).

1. **Pull monthly analytics**: `analytics:overview --start-date <first-of-month>
   --end-date <last-of-month>` and `analytics:accounts` (follower/subscriber counts)
   per platform, per client.
2. **Compute month-over-month KPIs** from `memory/social_memory.json.brief_history`:
   total impressions, total engagements, posts published vs. scheduled vs. failed,
   follower growth.
3. **Identify top content** of the month (from daily "Top Performing Posts") for the
   client report and for repurposing into next month's calendar.
4. **Webhook health check**: `webhooks:list` - confirm `post.failed` /
   `post.published` webhooks are still active for real-time alerting.
5. **Client report**: compile KPIs, top content, and a forward-looking content plan
   summary (see Reporting Structure below).
6. **Audit connected accounts**: `accounts:list` - confirm no accounts have been
   disconnected (status != `connected`) and reconnect if needed.

---

## Approval Points

Per OmniSocials SKILL.md Safety Rules, the following actions **always require
explicit human confirmation** before the agent proceeds:

| Action | Why it requires approval |
|---|---|
| `posts:create-and-publish` / `posts:publish` | Irreversible - goes public instantly |
| `posts:delete`, `media:delete`, `webhooks:delete` | Irreversible - cannot be undone |
| Weekly content calendar (before `posts:create --schedule` batch) | Client-facing content must be approved before it's queued |
| Draft posts flagged in "Posts Requiring Action" | Drafts represent content awaiting client sign-off by design |
| Pinterest board auto-selection | Agent may auto-pick the first board but must tell the user which one was used |

Everything else (`accounts:list/get`, `posts:list/get`, `media:list`,
`analytics:*`, `webhooks:list/get`, and **creating drafts** without `--schedule` or
publish) is read-only or non-destructive and can run unattended in the Daily
Workflow.

## Automation Opportunities

- **Daily Social Brief** - fully automatable today (read-only), same scheduling
  mechanism as the Morning Brief (`launchd` on macOS).
- **Webhook-driven alerts** - `webhooks:create --events post.published,post.failed`
  feeding into the Communication Layer (Slack) for real-time publish/failure
  notifications, complementing the once-a-day brief.
- **Approved-calendar auto-scheduling** - once a weekly calendar is approved, a
  script can loop `posts:create --schedule ...` for each approved item
  (one-at-a-time, per SKILL.md Safety Rule #7 for bulk operations).
- **Cross-platform repurposing suggestions** - "Top Performing Posts" -> "Recommended
  Next Actions" already auto-generates repurposing prompts; a future iteration could
  draft the repurposed post (still requiring approval to schedule/publish).
- **Monthly KPI report generation** - `memory/social_memory.json.brief_history` +
  `analytics:overview` can be assembled into a client-ready report automatically;
  only the send/delivery step needs human review.

**Not automated by design** (out of scope, matches Agency OS v1 "no Decision Engine"
constraint): content generation/copywriting, creative asset design, and any
publish/delete/schedule action without a human approval step.

## KPI Tracking

Tracked via `memory/social_memory.json.brief_history`, one entry per Social Brief run:

| KPI | Source | Cadence |
|---|---|---|
| Posts published | `posts:list --status published` | Daily |
| Posts scheduled / overdue | `posts:list --status scheduled` (split by `scheduled_at` vs. now) | Daily |
| Posts failed | `posts:list --status failed` | Daily |
| Drafts awaiting approval | `posts:list --status draft` | Daily |
| Impressions / Engagements (daily) | `analytics:post` per published post | Daily |
| Impressions / Engagements / Posts (7d, 30d, custom) | `analytics:overview` | Weekly / Monthly |
| Follower / subscriber counts | `analytics:accounts` | Monthly |
| Top performing post(s) | Ranked by engagements from daily published posts | Daily, rolled up Monthly |

## Reporting Structure

| Report | Audience | Cadence | Contents |
|---|---|---|---|
| **Social Brief** (`SOCIAL_BRIEF.md` format) | Agency owner/team | Daily | Scheduled content, published content, engagement metrics, top performing posts, posts requiring action, recommended next actions |
| **Weekly Planning Summary** | Agency owner/team, per client | Weekly | Past week's KPIs, carry-over action items, proposed content calendar for approval |
| **Monthly Client Report** | Client | Monthly | Month KPIs (impressions, engagements, follower growth), top content, next month's plan |
| **Webhook Alerts** (`post.published`, `post.failed`) | Agency owner/team (via Slack, Communication Layer) | Real-time | Immediate notification of publish success/failure |

---

## Explicitly Out of Scope (this build)

Matches the Agency OS v1 "no Decision Engine / no V4-V5" constraint: no automated
content generation, no automated publishing without approval, no cross-layer Focus
Score / priority ranking beyond the Social Brief's simple "top performers + action
items" list, and no new architecture beyond adding this one layer alongside the
existing Memory and Communication layers.
