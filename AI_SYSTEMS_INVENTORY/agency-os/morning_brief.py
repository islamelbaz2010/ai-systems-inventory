#!/usr/bin/env python3
"""
Morning Brief workflow (Agency OS v1 scope: Memory Layer + Communication Layer only).

Reads Gmail + Slack data, classifies each item (NEW LEAD / CLIENT REQUEST / INTERNAL /
VENDOR-NOISE), cross-references the Memory Layer (memory_store.json) for client context
and open SOP items, ranks a single top-priority item, updates memory, and prints a
Morning Brief.

Data source modes:
  - "sample" (default): reads sample_data/gmail_inbox.json and sample_data/slack_messages.json
  - "composio": fetches live Gmail/Slack data via Composio (requires COMPOSIO_API_KEY env var
    and completed Gmail/Slack OAuth connections - see LOCAL_DEPLOYMENT_GUIDE.md)

Usage:
  python3 morning_brief.py [--source sample|composio]
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MEMORY_PATH = BASE_DIR / "memory" / "memory_store.json"
GMAIL_SAMPLE_PATH = BASE_DIR / "sample_data" / "gmail_inbox.json"
SLACK_SAMPLE_PATH = BASE_DIR / "sample_data" / "slack_messages.json"


def load_json(path):
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def domain_of(email_address):
    return email_address.split("@", 1)[-1].lower()


def fetch_gmail_sample():
    return load_json(GMAIL_SAMPLE_PATH)


def fetch_slack_sample():
    return load_json(SLACK_SAMPLE_PATH)


def _run_node_fetcher(script_name, extra_args=None):
    """Run one of the fetch_*.mjs helpers (Node + @composio/core) and parse its JSON stdout."""
    api_key = os.environ.get("COMPOSIO_API_KEY")
    if not api_key:
        raise RuntimeError(
            "COMPOSIO_API_KEY is not set. Run with --source sample, or follow "
            "LOCAL_DEPLOYMENT_GUIDE.md to set up Composio + Gmail/Slack."
        )
    cmd = ["node", str(BASE_DIR / script_name)] + (extra_args or [])
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=BASE_DIR)
    if result.returncode != 0:
        raise RuntimeError(
            f"{script_name} failed:\n{result.stderr.strip()}\n\n"
            "See LOCAL_DEPLOYMENT_GUIDE.md for setup/troubleshooting."
        )
    return json.loads(result.stdout)


def fetch_gmail_composio():
    """Fetch unread Gmail from the last 24h via Composio (fetch_gmail.mjs)."""
    return _run_node_fetcher("fetch_gmail.mjs")


def fetch_slack_composio():
    """Fetch recent #team Slack messages via Composio (fetch_slack.mjs)."""
    return _run_node_fetcher("fetch_slack.mjs")


def classify_email(email, memory):
    domain = domain_of(email["from"])
    client = memory["clients"].get(domain)

    if client and client.get("status") == "vendor":
        return "VENDOR-NOISE", client

    if client and client.get("status") == "active_client":
        return "CLIENT REQUEST", client

    if domain in memory["leads"]:
        return "KNOWN LEAD", memory["leads"][domain]

    return "NEW LEAD", client


def classify_slack(message):
    text = message["text"].lower()
    if text.startswith("did anyone") or text.endswith("?") and "anyone" in text:
        return "INTERNAL - needs human reply"
    if "shopping around" in text or "other agencies" in text or "considering" in text:
        return "CLIENT RISK SIGNAL"
    return "INFO"


def build_brief(gmail_items, slack_items, memory):
    new_leads = []
    known_leads = []
    client_requests = []
    vendor_noise = []
    internal_items = []
    risk_signals = []
    follow_ups = []

    for email in gmail_items:
        label, client = classify_email(email, memory)
        if label == "NEW LEAD":
            new_leads.append(email)
        elif label == "KNOWN LEAD":
            known_leads.append((email, client))
        elif label == "CLIENT REQUEST":
            client_requests.append((email, client))
        else:
            vendor_noise.append(email)

    for msg in slack_items:
        label = classify_slack(msg)
        if label == "INTERNAL - needs human reply":
            internal_items.append(msg)
        elif label == "CLIENT RISK SIGNAL":
            risk_signals.append(msg)

    # Follow-ups: any client with overdue open_items
    for domain, client in memory["clients"].items():
        for item in client.get("open_items", []):
            if item.get("status") == "overdue":
                follow_ups.append((client["name"], item))

    # New leads + client requests always need a drafted reply -> follow-up
    for email in new_leads:
        follow_ups.append(
            (email["from_name"], {"item": f"Draft reply + audit for new lead: {email['subject']}"})
        )
    for email, client in client_requests:
        follow_ups.append(
            (client["name"], {"item": f"Draft reply for client request: {email['subject']}"})
        )
    for email, lead in known_leads:
        follow_ups.append(
            (lead["name"], {"item": f"Re-engage lead, still no reply since {lead['first_contact']}: {email['subject']}"})
        )

    # --- Top priority item ---
    # Priority order: client risk signal > overdue SOP item > client request > new lead > internal
    top_priority = None
    if risk_signals:
        top_priority = (
            "CLIENT RISK",
            f"Client risk signal in Slack: \"{risk_signals[0]['text']}\" "
            f"(from {risk_signals[0]['user']} in {risk_signals[0]['channel']}) - "
            f"investigate and reach out to the client directly.",
        )
    elif any(item.get("status") == "overdue" for c in memory["clients"].values() for item in c.get("open_items", [])):
        for cname, item in follow_ups:
            if item.get("status") == "overdue":
                top_priority = (
                    "OVERDUE SOP ITEM",
                    f"{cname}: {item['item']} (SOP step: {item.get('sop_step', 'n/a')}) - overdue since {item.get('opened')}.",
                )
                break
    elif client_requests:
        email, client = client_requests[0]
        top_priority = (
            "CLIENT REQUEST",
            f"{client['name']}: \"{email['subject']}\" - draft + send reply with deliverable.",
        )
    elif new_leads:
        email = new_leads[0]
        top_priority = (
            "NEW LEAD",
            f"{email['from_name']}: \"{email['subject']}\" - run audit, draft reply with discovery-call CTA.",
        )
    elif internal_items:
        msg = internal_items[0]
        top_priority = ("INTERNAL", f"Answer Slack question: \"{msg['text']}\"")

    return {
        "new_leads": new_leads,
        "known_leads": known_leads,
        "client_requests": client_requests,
        "vendor_noise": vendor_noise,
        "internal_items": internal_items,
        "risk_signals": risk_signals,
        "follow_ups": follow_ups,
        "top_priority": top_priority,
    }


def update_memory(memory, brief, gmail_items):
    now = datetime.now(timezone.utc).isoformat()

    for email in brief["new_leads"]:
        domain = domain_of(email["from"])
        memory["leads"][domain] = {
            "name": email["from_name"],
            "first_contact": email["received_at"],
            "subject": email["subject"],
            "status": "audit_sent_awaiting_reply",
            "logged_at": now,
        }

    memory["brief_history"].append(
        {
            "generated_at": now,
            "new_leads": len(brief["new_leads"]),
            "client_requests": len(brief["client_requests"]),
            "internal_items": len(brief["internal_items"]),
            "risk_signals": len(brief["risk_signals"]),
            "follow_ups": len(brief["follow_ups"]),
            "top_priority": brief["top_priority"][1] if brief["top_priority"] else None,
        }
    )
    return memory


def render_brief(brief, memory):
    lines = []
    lines.append("=" * 60)
    lines.append("  MORNING BRIEF")
    lines.append("=" * 60)
    lines.append("")

    lines.append(f"NEW LEADS ({len(brief['new_leads'])})")
    if brief["new_leads"]:
        for email in brief["new_leads"]:
            lines.append(f"  - {email['from_name']} <{email['from']}>: \"{email['subject']}\"")
            lines.append(f"    -> Audit drafted, reply drafted (not sent), saved to memory as new lead.")
    else:
        lines.append("  (none)")
    lines.append("")

    if brief["known_leads"]:
        lines.append(f"LEADS AWAITING REPLY - FOLLOW UP ({len(brief['known_leads'])})")
        for email, lead in brief["known_leads"]:
            lines.append(f"  - {lead['name']} <{email['from']}>: still no reply since {lead['first_contact']} (status: {lead['status']})")
        lines.append("")

    lines.append(f"CLIENT EMAILS ({len(brief['client_requests'])})")
    if brief["client_requests"]:
        for email, client in brief["client_requests"]:
            lines.append(f"  - {client['name']} <{email['from']}>: \"{email['subject']}\"")
            lines.append(f"    -> Reply drafted using {client.get('design_system', 'default')} design system.")
    else:
        lines.append("  (none)")
    lines.append("")

    lines.append(f"IMPORTANT MESSAGES ({len(brief['internal_items']) + len(brief['risk_signals'])})")
    for msg in brief["risk_signals"]:
        lines.append(f"  - [RISK] {msg['channel']} @{msg['user']}: \"{msg['text']}\"")
    for msg in brief["internal_items"]:
        lines.append(f"  - [INTERNAL] {msg['channel']} @{msg['user']}: \"{msg['text']}\"")
    if not brief["internal_items"] and not brief["risk_signals"]:
        lines.append("  (none)")
    lines.append("")

    lines.append(f"FOLLOW-UPS NEEDED ({len(brief['follow_ups'])})")
    if brief["follow_ups"]:
        for name, item in brief["follow_ups"]:
            extra = f" (overdue since {item['opened']})" if item.get("status") == "overdue" else ""
            lines.append(f"  - {name}: {item['item']}{extra}")
    else:
        lines.append("  (none)")
    lines.append("")

    lines.append("TOP PRIORITY ITEM")
    if brief["top_priority"]:
        kind, text = brief["top_priority"]
        lines.append(f"  [{kind}] {text}")
    else:
        lines.append("  (nothing urgent today)")
    lines.append("")

    if brief["vendor_noise"]:
        lines.append(f"FILTERED OUT (vendor/noise, {len(brief['vendor_noise'])})")
        for email in brief["vendor_noise"]:
            lines.append(f"  - {email['from_name']} <{email['from']}>: \"{email['subject']}\" (known vendor domain - not a lead)")
        lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=["sample", "composio"], default="sample")
    parser.add_argument("--no-save", action="store_true", help="Don't write updates back to memory_store.json")
    args = parser.parse_args()

    if args.source == "sample":
        gmail_items = fetch_gmail_sample()
        slack_items = fetch_slack_sample()
    else:
        gmail_items = fetch_gmail_composio()
        slack_items = fetch_slack_composio()

    memory = load_json(MEMORY_PATH)
    brief = build_brief(gmail_items, slack_items, memory)
    output = render_brief(brief, memory)
    print(output)

    if not args.no_save:
        memory = update_memory(memory, brief, gmail_items)
        save_json(MEMORY_PATH, memory)
        print(f"\n[memory updated -> {MEMORY_PATH}]")


if __name__ == "__main__":
    sys.exit(main())
