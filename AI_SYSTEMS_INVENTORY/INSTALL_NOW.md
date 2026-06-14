# Install Now - Top 5 Highest-Impact Capabilities (macOS)

This guide is written for a **non-developer business owner** using a Mac. Every step is
something you can do by copying and pasting commands - no coding knowledge required.

You'll need:
- A Mac with macOS
- Claude Code already installed (if you're reading this inside Claude Code, you have it)
- About 2-3 hours total, spread across the steps below (you do NOT need to do this all at
  once)

**Order matters.** Do these in order 1 → 5. Item #5 depends on a setup step that's easiest
to do once, so it's listed last but explained fully.

---

## How to Open Terminal (you'll need this for items #3 and #5)

1. Press `Cmd + Space` to open Spotlight Search.
2. Type `Terminal` and press `Enter`.
3. A black or white window with text will open. This is where you'll paste commands.
4. To paste a command, copy it from this document, click inside the Terminal window, then
   press `Cmd + V`, then press `Enter` to run it.

---

# 1. 51 Marketing Skills (Full Marketing Bundle)

**What it does:** Gives Claude an entire marketing department's worth of skills - SEO
audits, content creation, ad copy, email sequences, social posts, pricing strategy - all
in one install.

### Exact Installation Commands

Run these **inside Claude Code** (type them directly into your Claude Code chat window,
not Terminal):

```
/plugin marketplace add alirezarezvani/claude-skills
```

Wait for it to finish, then run:

```
/plugin install marketing-skills@claude-code-skills
```

### Dependencies
None.

### API Keys Required
None.

### Accounts Required
None - works with your existing Claude Code account.

### Estimated Setup Time
10-15 minutes.

### Verification Steps
1. In Claude Code, type:
   ```
   /plugin list
   ```
2. Confirm `marketing-skills@claude-code-skills` appears in the list with a status of
   "installed" or "enabled."
3. Ask Claude: *"Run a quick SEO audit of [your website URL]."* Confirm it produces a
   structured audit (not an error message).

### Common Errors
- **"Marketplace not found"** → Double-check you typed `alirezarezvani/claude-skills`
  exactly (no extra spaces). Re-run the `/plugin marketplace add` command.
- **"Plugin install failed"** → Run `/plugin marketplace update alirezarezvani/claude-skills`
  and then retry the install command.
- **Nothing happens after pasting** → Make sure you're typing into the Claude Code chat
  box, not Terminal - this step does NOT use Terminal.

### Success Criteria
You can ask Claude to run any marketing task (SEO audit, write ad copy, create a social
media post) and it responds with real, structured output - not "I don't have that skill."

---

# 2. Open Design Studio (Desktop App)

**What it does:** A design tool that replaces Canva/Figma for most needs - generates
landing pages, presentation decks, social graphics, and videos from a simple chat
description, using 150 pre-built professional design templates.

### Exact Installation Commands

No Terminal needed for this one.

1. Open your web browser and go to the Open Design GitHub releases page:
   `https://github.com/nexu-io/open-design/releases`
2. Find the latest release at the top of the page.
3. Under "Assets," download the file ending in `.dmg` that matches your Mac:
   - `open-design-<version>-arm64.dmg` if you have an Apple Silicon Mac (M1/M2/M3/M4)
   - `open-design-<version>-x64.dmg` if you have an Intel Mac
   - *(Not sure which chip? Click the Apple menu → About This Mac. It will say "Apple"
     or "Intel" under the chip name.)*
4. Once downloaded, double-click the `.dmg` file in your Downloads folder.
5. Drag the "Open Design" icon into the "Applications" folder when prompted.
6. Open your Applications folder and double-click "Open Design" to launch it.

### Dependencies
None - it's a self-contained desktop app.

### API Keys Required
None for basic use. (Optional: if you want to use your own OpenAI/Anthropic account
instead of the built-in option, you can add that key later in Settings - skip this for
now.)

### Accounts Required
None to start.

### Estimated Setup Time
15-20 minutes (mostly download time).

### Verification Steps
1. Launch the app from your Applications folder.
2. If macOS shows a warning like "Open Design can't be opened because it is from an
   unidentified developer," go to **System Settings → Privacy & Security**, scroll down,
   and click **"Open Anyway"** next to the Open Design entry. Then try opening it again.
3. Once open, you should see a chat-style interface with a sidebar of design templates.
4. Type a simple request like *"Create a landing page for a coffee shop"* and confirm it
   generates a preview.

### Common Errors
- **"App is damaged and can't be opened"** → Re-download the `.dmg` file (the download may
  have been interrupted) and try again.
- **App won't open due to security warning** → Use the "Open Anyway" step above. This is
  normal for apps not distributed through the Mac App Store.
- **Blank/white screen on launch** → Quit the app completely (Cmd+Q) and reopen it. If it
  persists, restart your Mac and try again.

### Success Criteria
The app opens, shows the chat interface, and successfully generates a design (landing
page, deck, or image) when you describe what you want in plain English.

---

# 3. Persistent Memory Hooks (claude-mem)

**What it does:** Gives Claude long-term memory across sessions, so you don't have to
re-explain your business, brand, or ongoing projects every time you start a new
conversation.

### Exact Installation Commands

This step uses **Terminal** (see "How to Open Terminal" above).

1. First, check if you have Node.js installed. Paste this into Terminal and press Enter:
   ```
   node -v
   ```
   - If you see a version number like `v20.x.x` or higher, you're good - skip to step 3.
   - If you see "command not found," continue to step 2.

2. Install Node.js (only if step 1 said "command not found"):
   - Go to `https://nodejs.org` in your browser.
   - Click the button to download the "LTS" version for macOS.
   - Open the downloaded `.pkg` file and follow the installer prompts (click Continue/Agree/
     Install, enter your Mac password when asked).
   - Once finished, close and reopen Terminal, then run `node -v` again to confirm it now
     shows a version number.

3. Install claude-mem by pasting this into Terminal and pressing Enter:
   ```
   npx claude-mem install
   ```
   - You may see a prompt asking to confirm installing a package - type `y` and press
     Enter.
   - This will take a few minutes the first time.

4. Restart Claude Code completely (quit and reopen it) once the install finishes.

### Dependencies
- Node.js version 20 or higher (installed in step 2 above if needed)
- Everything else (SQLite, Chroma database) is installed automatically by the command above

### API Keys Required
None.

### Accounts Required
None.

### Estimated Setup Time
15-30 minutes (longer if Node.js needs to be installed first).

### Verification Steps
1. After restarting Claude Code, start a new conversation and tell Claude something
   memorable, e.g. *"My company is called Acme Co. and our brand colors are navy and
   gold."*
2. Close that conversation and start a brand new one.
3. Ask: *"What are my brand colors?"* If memory is working, Claude recalls "navy and gold"
   without you repeating it.
4. Optional: open `http://localhost:37777` in your browser - you should see a memory
   dashboard with your recent conversation logged.

### Common Errors
- **"npx: command not found"** → Node.js wasn't installed correctly. Repeat step 2, then
  reopen Terminal and try again.
- **Install hangs for a long time** → Press `Ctrl + C` to cancel, close Terminal, reopen
  it, and run `npx claude-mem install` again.
- **Claude doesn't remember anything after restart** → Make sure you fully quit Claude Code
  (Cmd+Q, not just closing the window) and reopened it after the install finished.
- **Port 37777 won't load in browser** → This is optional/cosmetic - memory still works
  even if the dashboard doesn't load. Try restarting your Mac if you want the dashboard.

### Success Criteria
Information you tell Claude in one session is automatically available in a brand-new
session, without you repeating it.

---

# 4. Landing Page Generator (landing-page skill)

**What it does:** Generates a complete, ready-to-publish landing page (single file, with
animations and your brand colors) from a short description - no web developer needed.

### Exact Installation Commands

Run this **inside Claude Code**:

```
/plugin install product-skills@claude-code-skills
```

*(Note: This uses the same marketplace you already added in Step 1. If you get an error
saying the marketplace isn't found, first run `/plugin marketplace add
alirezarezvani/claude-skills` again, then retry this command.)*

### Dependencies
None (requires Step 1's marketplace to already be added).

### API Keys Required
None.

### Accounts Required
None.

### Estimated Setup Time
5 minutes.

### Verification Steps
1. Run `/plugin list` in Claude Code and confirm `product-skills@claude-code-skills`
   appears as installed.
2. Ask Claude: *"Create a landing page for [your business name] offering [your main
   service]. Use the brand colors [color 1] and [color 2]."*
3. Confirm Claude produces a single HTML file you can open in your browser by
   double-clicking it.

### Common Errors
- **"Plugin not found"** → The marketplace from Step 1 wasn't added. Run:
  ```
  /plugin marketplace add alirezarezvani/claude-skills
  ```
  then retry the install command above.
- **Generated page looks broken when opened** → Make sure you're opening the `.html` file
  by double-clicking it (it should open in your web browser), not opening it as a text
  file.

### Success Criteria
You can describe a landing page in plain English and receive a finished `.html` file that
opens correctly in your web browser and looks professional.

---

# 5. Gmail / Slack Automation (via Composio Connector)

**What it does:** Lets Claude read, draft, send, and organize your Gmail, and post/read
messages in Slack - automating your daily inbox and team-communication triage.

This is the most involved step because it requires creating a free account with a service
called **Composio**, which is what securely connects Claude to your Gmail and Slack. Take
your time with this one - once it's done, it's done for good.

### Exact Installation Commands

**Part A - Create your Composio account and get your API key**

1. In your browser, go to `https://dashboard.composio.dev`
2. Sign up for a free account (you can use your Google account to sign up faster).
3. Once logged in, look for a section called "API Keys" (usually in account/profile
   settings).
4. Click "Create API Key" (or it may already show a default key).
5. Copy this key - you'll paste it in Part C. Treat it like a password; don't share it
   publicly.

**Part B - Install the Composio connector tools**

This step uses **Terminal**.

1. Check if Python is installed by pasting this into Terminal:
   ```
   python3 --version
   ```
   - macOS comes with Python pre-installed, so you should see a version number like
     `Python 3.x.x`. If you see "command not found," install Python from
     `https://www.python.org/downloads/` (download the macOS installer, open it, and
     follow the prompts), then reopen Terminal.

2. Install Composio by pasting this into Terminal and pressing Enter:
   ```
   pip3 install composio
   ```

**Part C - Connect the plugin and authorize Gmail/Slack**

3. In Claude Code, run:
   ```
   /connect-apps:setup
   ```
4. When prompted, paste the Composio API key you copied in Part A, then press Enter.
5. Claude will give you a link (or links) to authorize Gmail and Slack. Click each link -
   it will open your browser and ask you to log into Gmail / Slack and click "Allow."
6. Once both show as "Connected," you're done.

### Dependencies
- Python 3 (pre-installed on most Macs; install from python.org if missing)
- The `composio` Python package (installed via `pip3 install composio` above)

### API Keys Required
- **Composio API key** - free, obtained from dashboard.composio.dev (Part A above)

### Accounts Required
- **Composio account** (free) - dashboard.composio.dev
- **Gmail account** - the one you want Claude to manage
- **Slack workspace** - the one you want Claude to post/read in (you'll need permission to
  authorize apps in this workspace; if you're not the workspace admin, ask them to approve
  the connection request)

### Estimated Setup Time
45-60 minutes (mostly account creation and OAuth click-throughs).

### Verification Steps
1. In Claude Code, ask: *"Show me my 5 most recent unread emails."* Confirm Claude returns
   real subject lines from your actual inbox (not an error).
2. Ask: *"Post 'Testing automation setup' to the #general Slack channel."* Confirm the
   message actually appears in Slack.
3. If both of those work, the connection is fully live.

### Common Errors
- **"pip3: command not found"** → Python wasn't installed correctly. Re-download from
  python.org, run the installer fully (including any "Install Certificates.command" step
  it mentions), then reopen Terminal.
- **`/connect-apps:setup` says "plugin not found"** → The Composio plugin needs to be
  loaded first. Ask Claude (or check the awesome-claude-skills documentation) for the exact
  `claude --plugin-dir` command for your install, then retry `/connect-apps:setup`.
- **Authorization link doesn't work / "redirect error"** → Make sure you're logged into
  the correct Gmail account / Slack workspace in your browser before clicking the
  authorization link. Try opening the link in an incognito/private window if it fails.
- **"Connected" but Claude says it can't access Gmail/Slack** → Go back to
  dashboard.composio.dev, check that both Gmail and Slack show a green "Connected" status,
  and re-run `/connect-apps:setup` if either shows red/disconnected.
- **Slack admin blocks the app** → If your Slack workspace requires admin approval for new
  apps, ask your workspace admin to approve the "Composio" app request - it will appear in
  their Slack admin notifications.

### Success Criteria
Claude can read your real Gmail inbox and post real messages to your real Slack workspace
when asked, without any further setup steps.

---

## What's Next

Once these 5 are working, see `ACTION_PLAN.md` for the remaining Tier 2 items (companion
memory skills, design system templates, GitHub/Jira/Linear/Notion automation, and LLM
Council) and the full 30-Day Roadmap. Do not move on to anything in Tier 3 or Tier 4 yet -
those are covered in `installation_priority.xlsx` for later, on-demand installs.
