# Local Deployment Guide - Morning Brief on macOS

The cloud sandbox used to build this proof of concept has a network egress allowlist that
blocks `*.composio.dev` (see `IMPLEMENTATION_STATUS.md`, Blocker #1), so Gmail/Slack OAuth
cannot complete there. **Everything below runs on your own Mac**, which has normal,
unrestricted internet access - the only thing the cloud build prepared is the code in
`AI_SYSTEMS_INVENTORY/agency-os/`.

This guide takes you from a clean Mac to a working Morning Brief running on your real
Gmail and Slack.

---

## 1. Node.js Requirements

- **Node.js 18 or newer** (the Composio SDK and `claude-mem` both target modern Node).

Check what you have:
```bash
node -v
npm -v
```

If you don't have Node, install it via [nodejs.org](https://nodejs.org/) (LTS installer,
.pkg) or via Homebrew:
```bash
brew install node
```

---

## 2. Python Requirements

- **Python 3.10+** (macOS ships with Python 3 already; 3.11+ recommended).

Check:
```bash
python3 --version
pip3 --version
```

If missing or too old:
```bash
brew install python@3.11
```

No additional Python packages are required for `morning_brief.py` itself - it only uses
the standard library (`json`, `subprocess`, `argparse`, `datetime`, `pathlib`).

---

## 3. Installation Commands

```bash
# 1. Clone the repo (or pull latest if you already have it)
git clone https://github.com/islamelbaz2010/ai-systems-inventory.git
cd ai-systems-inventory/AI_SYSTEMS_INVENTORY/agency-os

# 2. Install the Node dependency (Composio SDK)
npm install

# 3. (Optional but recommended) Install claude-mem - the Memory Layer
npx claude-mem@13.6.0 install
npx claude-mem@13.6.0 start
npx claude-mem@13.6.0 status   # should show "Worker is running" on port 37700
```

`npm install` reads the already-committed `package.json` (`@composio/core`) and creates
`node_modules/` locally - this directory and `package-lock.json` are gitignored, so this
step must be run on your Mac.

---

## 4. Environment Variables

Create a `.env` file in `agency-os/` (already gitignored, will not be committed):

```bash
cd ai-systems-inventory/AI_SYSTEMS_INVENTORY/agency-os
cat > .env << 'EOF'
COMPOSIO_API_KEY=your-composio-api-key-here
EOF
chmod 600 .env
```

Before running any of the scripts below, load it into your shell:
```bash
set -a && source .env && set +a
```

(Or add that line to your `~/.zshrc` / `~/.bash_profile` if you want it always loaded -
just make sure `.env` itself is never committed.)

| Variable | Required | Where it comes from |
|---|---|---|
| `COMPOSIO_API_KEY` | Yes | Step 5 below (platform.composio.dev) |

No other environment variables are required for the in-scope systems (Memory,
Communication, Morning Brief).

---

## 5. Composio Setup

1. Go to **https://platform.composio.dev/** and sign up (free tier is sufficient).
2. Go to **Settings → API Keys** and create a new key.
3. Put it in `agency-os/.env` as shown in section 4.

This one key is the gateway for **both** Gmail and Slack - you do not need separate keys
per service.

---

## 6. Gmail OAuth Setup

From `agency-os/` (with `.env` loaded per section 4):

```bash
node connect_composio.mjs gmail
```

What happens:
1. The script creates a Composio-managed Gmail auth config (no need to register your own
   Google Cloud OAuth app - Composio provides a managed one).
2. It prints a URL like:
   ```
   OPEN THIS URL IN YOUR BROWSER TO AUTHORIZE GMAIL:
   https://accounts.google.com/o/oauth2/v2/auth?...
   ```
3. **Open that URL in your browser**, sign in with the Gmail account the agency should
   monitor, and approve the requested read-mail scopes.
4. The script polls for up to 120 seconds and, on success, prints:
   ```
   SUCCESS - gmail connected.
   Connected account ID: ca_xxxxxxxx
   ```
   and writes this to `agency-os/memory/connections.json`.

If it times out before you finish approving, just re-run `node connect_composio.mjs
gmail` - it's safe to repeat.

---

## 7. Slack OAuth Setup

```bash
node connect_composio.mjs slack
```

Same flow as Gmail:
1. Prints a Slack OAuth URL.
2. **Open it in your browser**, choose the workspace, and approve. If you are not a
   workspace admin, an admin will need to approve the Composio Slack app for the
   workspace the first time any member connects it.
3. On success, the connection is saved to `agency-os/memory/connections.json` under
   `"slack"`.

Check both connections any time with:
```bash
node connect_composio.mjs status
```

---

## 8. How to Run `morning_brief.py` Locally

### 8a. Sanity-check the raw fetchers first

```bash
set -a && source .env && set +a

node fetch_gmail.mjs   # should print a JSON array of recent emails
node fetch_slack.mjs   # should print a JSON array of recent #team messages
```

**Important:** the exact Composio tool slugs used inside `fetch_gmail.mjs`
(`GMAIL_FETCH_EMAILS`) and `fetch_slack.mjs` (`SLACK_LIST_CHANNELS`,
`SLACK_FETCH_CONVERSATION_HISTORY`) were written against Composio's documented API but
**could not be executed/verified in the cloud sandbox** (network blocked - see
`IMPLEMENTATION_STATUS.md`). On your Mac, with real network access, if either command
errors with something like "tool not found" or "unknown action":

1. Run this once to list the real available actions for your connected account:
   ```bash
   node -e "
   import('@composio/core').then(async ({Composio}) => {
     const c = new Composio({apiKey: process.env.COMPOSIO_API_KEY});
     const tools = await c.tools.get('agency-owner', { toolkits: ['gmail'] });
     console.log(JSON.stringify(tools.map(t => t.slug), null, 2));
   });
   "
   ```
   (swap `'gmail'` for `'slack'` for the Slack action list)
2. Update the `composio.tools.execute('GMAIL_FETCH_EMAILS', ...)` /
   `'SLACK_FETCH_CONVERSATION_HISTORY'` lines in `fetch_gmail.mjs` / `fetch_slack.mjs` to
   match the slug names your account actually has. The rest of the pipeline
   (normalization, classification, memory, ranking, report) does not need to change.

### 8b. Run the full Morning Brief against real data

```bash
python3 morning_brief.py --source composio
```

This will:
1. Call `fetch_gmail.mjs` and `fetch_slack.mjs` (real Gmail/Slack data via Composio).
2. Classify each item against `memory/memory_store.json` (new lead / client request /
   vendor noise / known lead awaiting reply / internal Slack question / client-risk
   signal).
3. Print the Morning Brief (new leads, client emails, important messages, follow-ups
   needed, top priority item).
4. Update `memory/memory_store.json` so tomorrow's run remembers today's leads.

To test without modifying memory:
```bash
python3 morning_brief.py --source composio --no-save
```

To go back to the sample-data demo at any time:
```bash
python3 morning_brief.py --source sample
```

### 8c. Update `memory/memory_store.json` for your real clients

The shipped `memory_store.json` contains placeholder clients (`acmeretail.com`,
`brightdental.com`, `vendorco.com`) used for the sample-data demo. Edit this file to
reflect your real clients/vendors before running against real Gmail, e.g.:

```json
"clients": {
  "yourclient.com": {
    "name": "Your Client",
    "status": "active_client",
    "design_system": "...",
    "open_items": [],
    "last_positive_contact": "2026-06-01"
  },
  "knownvendor.com": {
    "name": "Some Vendor",
    "status": "vendor",
    "note": "Excluded from lead classification"
  }
}
```

Any sender domain not listed here is treated as a **new lead**.

---

## 9. How to Schedule It Daily on macOS

Use `launchd` (the macOS-native scheduler - more reliable than `cron` for GUI/login
sessions).

1. Create a wrapper script `agency-os/run_morning_brief.sh`:
   ```bash
   #!/bin/bash
   cd "$(dirname "$0")"
   set -a
   source .env
   set +a
   /usr/bin/python3 morning_brief.py --source composio >> morning_brief.log 2>&1
   ```
   ```bash
   chmod +x run_morning_brief.sh
   ```

2. Create `~/Library/LaunchAgents/com.agencyos.morningbrief.plist`:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
     "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
     <key>Label</key>
     <string>com.agencyos.morningbrief</string>
     <key>ProgramArguments</key>
     <array>
       <string>/bin/bash</string>
       <string>/Users/YOURNAME/ai-systems-inventory/AI_SYSTEMS_INVENTORY/agency-os/run_morning_brief.sh</string>
     </array>
     <key>StartCalendarInterval</key>
     <dict>
       <key>Hour</key>
       <integer>7</integer>
       <key>Minute</key>
       <integer>0</integer>
     </dict>
     <key>StandardOutPath</key>
     <string>/tmp/morningbrief.out.log</string>
     <key>StandardErrorPath</key>
     <string>/tmp/morningbrief.err.log</string>
   </dict>
   </plist>
   ```
   Replace `/Users/YOURNAME/...` with the real absolute path.

3. Load it:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.agencyos.morningbrief.plist
   ```

4. Test it immediately without waiting for 7am:
   ```bash
   launchctl start com.agencyos.morningbrief
   cat /tmp/morningbrief.out.log
   ```

5. To stop/remove:
   ```bash
   launchctl unload ~/Library/LaunchAgents/com.agencyos.morningbrief.plist
   ```

**Posting to Slack instead of (or in addition to) a log file** is a follow-up step: add a
`SLACK_SEND_MESSAGE` call (same Composio Slack connection) at the end of
`render_brief()` in `morning_brief.py`, passing the rendered text. This was not done in
this build (out of scope per the original "Morning Brief = read + report" definition,
and untestable without the real Slack connection) but is a small, mechanical addition
once you're running locally.

---

## 10. Verification Steps

Run through these in order on your Mac:

1. **Node/Python versions**
   ```bash
   node -v   # >= 18
   python3 --version  # >= 3.10
   ```

2. **Dependencies installed**
   ```bash
   cd agency-os && npm install && ls node_modules/@composio/core
   ```

3. **claude-mem running** (Memory Layer)
   ```bash
   npx claude-mem@13.6.0 status
   # Expect: "Worker is running" with a PID and Port: 37700
   ```

4. **Composio key set**
   ```bash
   set -a && source .env && set +a
   node connect_composio.mjs status
   # Should not error with "COMPOSIO_API_KEY is not set"
   ```

5. **Gmail connected**
   ```bash
   node fetch_gmail.mjs | head -20
   # Should print real email JSON, not an error
   ```

6. **Slack connected**
   ```bash
   node fetch_slack.mjs | head -20
   # Should print real #team message JSON, not an error
   ```

7. **End-to-end Morning Brief on sample data** (always works, no credentials needed -
   regression check that the classify/memory/rank/report logic still works):
   ```bash
   python3 morning_brief.py --source sample --no-save
   ```

8. **End-to-end Morning Brief on real data**
   ```bash
   python3 morning_brief.py --source composio
   ```
   Confirm the output contains:
   - NEW LEADS - any senders not in `memory_store.json`
   - CLIENT EMAILS - senders matching an `active_client` domain
   - IMPORTANT MESSAGES - flagged Slack items
   - FOLLOW-UPS NEEDED - aggregated action list
   - TOP PRIORITY ITEM - exactly one ranked item

9. **Memory persistence**
   ```bash
   cat memory/memory_store.json | python3 -m json.tool | grep -A3 brief_history
   ```
   Should show a new entry with today's timestamp after step 8.

10. **(Optional) Scheduled run**
    ```bash
    launchctl start com.agencyos.morningbrief
    cat /tmp/morningbrief.out.log
    ```

If steps 1-7 pass but 8 fails with a Composio "tool not found" type error, see the
troubleshooting note in section 8a - the action slug names need to be confirmed against
your live Composio account and adjusted in `fetch_gmail.mjs` / `fetch_slack.mjs`.
