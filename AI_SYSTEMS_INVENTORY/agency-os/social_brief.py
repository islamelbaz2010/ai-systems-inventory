#!/usr/bin/env python3
"""
Social Brief workflow (Social Media Operations Layer, Agency OS).

Reads post/account data from OmniSocials (or sample data), summarizes scheduled
content, published content, engagement metrics, top performing posts, posts
requiring action, and recommended next actions. Updates memory/social_memory.json
with a KPI snapshot for month-over-month tracking.

Data source modes:
  - "sample" (default): reads sample_data/social_posts.json and
    sample_data/social_accounts.json
  - "omnisocials": calls omnisocials-agent-skills/scripts/omnisocials.js
    (requires OMNISOCIALS_API_KEY env var) for posts:list and accounts:list

Usage:
  python3 social_brief.py [--source sample|omnisocials]
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MEMORY_PATH = BASE_DIR / "memory" / "social_memory.json"
POSTS_SAMPLE_PATH = BASE_DIR / "sample_data" / "social_posts.json"
ACCOUNTS_SAMPLE_PATH = BASE_DIR / "sample_data" / "social_accounts.json"
OMNISOCIALS_CLI = BASE_DIR / "omnisocials-agent-skills" / "scripts" / "omnisocials.js"

TOP_PERFORMERS_COUNT = 2


def load_json(path):
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def fetch_posts_sample():
    return load_json(POSTS_SAMPLE_PATH)


def fetch_accounts_sample():
    return load_json(ACCOUNTS_SAMPLE_PATH)


def _run_omnisocials_cli(args):
    """Run the OmniSocials CLI with --json and parse its stdout."""
    if not os.environ.get("OMNISOCIALS_API_KEY"):
        raise RuntimeError(
            "OMNISOCIALS_API_KEY is not set. Run with --source sample, or set "
            "OMNISOCIALS_API_KEY (see agency-os/omnisocials-agent-skills/skills/omnisocials/SKILL.md)."
        )
    cmd = ["node", str(OMNISOCIALS_CLI)] + args + ["--json"]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=BASE_DIR)
    if result.returncode != 0:
        raise RuntimeError(
            f"omnisocials {' '.join(args)} failed:\n{result.stderr.strip() or result.stdout.strip()}\n\n"
            "See OMNISOCIALS_IMPLEMENTATION_STATUS.md for setup/troubleshooting."
        )
    return json.loads(result.stdout)


def fetch_posts_omnisocials():
    result = _run_omnisocials_cli(["posts:list", "--limit", "50"])
    data = result.get("data", result)
    return data.get("posts", data) if isinstance(data, dict) else data


def fetch_accounts_omnisocials():
    result = _run_omnisocials_cli(["accounts:list"])
    data = result.get("data", result)
    return data.get("accounts", data) if isinstance(data, dict) else data


def now_utc():
    return datetime.now(timezone.utc)


def parse_iso(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def build_brief(posts, accounts):
    now = now_utc()

    scheduled_upcoming = []
    scheduled_overdue = []
    published = []
    failed = []
    drafts = []

    for post in posts:
        status = post.get("status")
        if status == "scheduled":
            scheduled_at = parse_iso(post["scheduled_at"])
            if scheduled_at < now:
                scheduled_overdue.append(post)
            else:
                scheduled_upcoming.append(post)
        elif status == "published":
            published.append(post)
        elif status == "failed":
            failed.append(post)
        elif status == "draft":
            drafts.append(post)

    # --- Engagement metrics (aggregate across published posts) ---
    totals = {"impressions": 0, "engagements": 0, "likes": 0, "comments": 0, "shares": 0}
    for post in published:
        analytics = post.get("analytics", {})
        for key in totals:
            totals[key] += analytics.get(key, 0)

    # --- Top performing posts (by engagements) ---
    top_performing = sorted(
        published, key=lambda p: p.get("analytics", {}).get("engagements", 0), reverse=True
    )[:TOP_PERFORMERS_COUNT]

    # --- Posts requiring action ---
    posts_requiring_action = []
    for post in failed:
        posts_requiring_action.append(
            (post, f"Fix and resubmit (failed: {post.get('error', 'unknown error')})")
        )
    for post in scheduled_overdue:
        posts_requiring_action.append(
            (post, f"Missed schedule (was due {post['scheduled_at']}) — investigate and republish or reschedule")
        )
    for post in drafts:
        posts_requiring_action.append(
            (post, "Awaiting client approval before scheduling")
        )

    # --- Recommended next actions ---
    recommended_next_actions = []
    for post, reason in posts_requiring_action:
        recommended_next_actions.append(f"{post['client']}: {reason} — \"{post['content']}\"")

    for post in top_performing:
        eng = post.get("analytics", {}).get("engagements", 0)
        recommended_next_actions.append(
            f"{post['client']}: Repurpose top performer (\"{post['content']}\", {eng} engagements) "
            f"across other connected platforms."
        )

    if not recommended_next_actions:
        recommended_next_actions.append("Nothing urgent — continue with the planned content calendar.")

    return {
        "scheduled_upcoming": scheduled_upcoming,
        "scheduled_overdue": scheduled_overdue,
        "published": published,
        "failed": failed,
        "drafts": drafts,
        "totals": totals,
        "top_performing": top_performing,
        "posts_requiring_action": posts_requiring_action,
        "recommended_next_actions": recommended_next_actions,
        "accounts": accounts,
    }


def update_memory(memory, brief):
    now = now_utc().isoformat()
    top_post = brief["top_performing"][0] if brief["top_performing"] else None

    memory["brief_history"].append(
        {
            "generated_at": now,
            "posts_published": len(brief["published"]),
            "posts_scheduled": len(brief["scheduled_upcoming"]),
            "posts_overdue": len(brief["scheduled_overdue"]),
            "posts_failed": len(brief["failed"]),
            "posts_draft": len(brief["drafts"]),
            "total_impressions": brief["totals"]["impressions"],
            "total_engagements": brief["totals"]["engagements"],
            "top_post_id": top_post["id"] if top_post else None,
        }
    )
    return memory


def render_brief(brief):
    lines = []
    lines.append("=" * 60)
    lines.append("  SOCIAL BRIEF")
    lines.append("=" * 60)
    lines.append("")

    lines.append(f"SCHEDULED CONTENT ({len(brief['scheduled_upcoming'])})")
    if brief["scheduled_upcoming"]:
        for post in brief["scheduled_upcoming"]:
            channels = ", ".join(post["channels"])
            lines.append(
                f"  - {post['client']} [{post['type']}] on {channels} at {post['scheduled_at']}: \"{post['content']}\""
            )
    else:
        lines.append("  (none)")
    lines.append("")

    lines.append(f"PUBLISHED CONTENT ({len(brief['published'])})")
    if brief["published"]:
        for post in brief["published"]:
            channels = ", ".join(post["channels"])
            a = post.get("analytics", {})
            lines.append(
                f"  - {post['client']} [{post['type']}] on {channels}, published {post['published_at']}: \"{post['content']}\""
            )
            lines.append(
                f"    -> impressions: {a.get('impressions', 0)}, engagements: {a.get('engagements', 0)}, "
                f"likes: {a.get('likes', 0)}, comments: {a.get('comments', 0)}, shares: {a.get('shares', 0)}"
            )
    else:
        lines.append("  (none)")
    lines.append("")

    t = brief["totals"]
    lines.append("ENGAGEMENT METRICS (across published posts above)")
    lines.append(
        f"  Impressions: {t['impressions']}  |  Engagements: {t['engagements']}  |  "
        f"Likes: {t['likes']}  |  Comments: {t['comments']}  |  Shares: {t['shares']}"
    )
    lines.append("")

    lines.append(f"TOP PERFORMING POSTS ({len(brief['top_performing'])})")
    if brief["top_performing"]:
        for post in brief["top_performing"]:
            a = post.get("analytics", {})
            lines.append(
                f"  - {post['client']}: \"{post['content']}\" — {a.get('engagements', 0)} engagements "
                f"({a.get('impressions', 0)} impressions)"
            )
    else:
        lines.append("  (none)")
    lines.append("")

    lines.append(f"POSTS REQUIRING ACTION ({len(brief['posts_requiring_action'])})")
    if brief["posts_requiring_action"]:
        for post, reason in brief["posts_requiring_action"]:
            lines.append(f"  - {post['client']}: \"{post['content']}\" — {reason}")
    else:
        lines.append("  (none)")
    lines.append("")

    lines.append("RECOMMENDED NEXT ACTIONS")
    for action in brief["recommended_next_actions"]:
        lines.append(f"  - {action}")
    lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=["sample", "omnisocials"], default="sample")
    parser.add_argument("--no-save", action="store_true", help="Don't write updates back to memory/social_memory.json")
    args = parser.parse_args()

    if args.source == "sample":
        posts = fetch_posts_sample()
        accounts = fetch_accounts_sample()
    else:
        posts = fetch_posts_omnisocials()
        accounts = fetch_accounts_omnisocials()

    brief = build_brief(posts, accounts)
    output = render_brief(brief)
    print(output)

    if not args.no_save:
        memory = load_json(MEMORY_PATH)
        memory = update_memory(memory, brief)
        save_json(MEMORY_PATH, memory)
        print(f"\n[memory updated -> {MEMORY_PATH}]")


if __name__ == "__main__":
    sys.exit(main())
