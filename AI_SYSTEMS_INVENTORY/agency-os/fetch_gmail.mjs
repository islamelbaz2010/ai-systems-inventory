// Fetches unread Gmail from the last 24h via Composio, normalized to the same shape
// as sample_data/gmail_inbox.json so morning_brief.py can consume either source.
//
// Requires: COMPOSIO_API_KEY env var, and a Gmail account connected via
// `node connect_composio.mjs gmail` (connection ID read from memory/connections.json).
//
// Run directly to sanity-check: node fetch_gmail.mjs
// Outputs a JSON array on stdout.

import { Composio } from '@composio/core';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const CONNECTIONS_PATH = path.join(__dirname, 'memory', 'connections.json');
const USER_ID = 'agency-owner';

function loadConnections() {
  if (!fs.existsSync(CONNECTIONS_PATH)) {
    throw new Error(
      `${CONNECTIONS_PATH} not found. Run "node connect_composio.mjs gmail" first.`
    );
  }
  return JSON.parse(fs.readFileSync(CONNECTIONS_PATH, 'utf8'));
}

function normalize(rawMessages) {
  return rawMessages.map((m, i) => ({
    id: m.messageId || m.id || `gmail-live-${i}`,
    from: (m.sender || m.from || '').replace(/.*<(.+)>/, '$1'),
    from_name: (m.sender || m.from || '').replace(/<.*>/, '').trim() || m.sender,
    subject: m.subject || '(no subject)',
    body: m.messageText || m.snippet || m.body || '',
    received_at: m.messageTimestamp || m.date || new Date().toISOString(),
    thread_id: m.threadId || m.thread_id || m.id,
  }));
}

async function main() {
  const apiKey = process.env.COMPOSIO_API_KEY;
  if (!apiKey) {
    throw new Error('COMPOSIO_API_KEY is not set.');
  }
  const connections = loadConnections();
  if (!connections.gmail) {
    throw new Error('Gmail is not connected. Run "node connect_composio.mjs gmail" first.');
  }

  const composio = new Composio({ apiKey });

  // Verify the exact tool slug/args locally with:
  //   composio.tools.get(USER_ID, { toolkits: ['gmail'] }).then(t => console.log(JSON.stringify(t, null, 2)))
  // GMAIL_FETCH_EMAILS is the documented slug as of @composio/core ^0.10 (see LOCAL_DEPLOYMENT_GUIDE.md step 8).
  const result = await composio.tools.execute('GMAIL_FETCH_EMAILS', {
    userId: USER_ID,
    connectedAccountId: connections.gmail.connectedAccountId,
    arguments: {
      query: 'newer_than:1d',
      max_results: 20,
    },
  });

  const messages = result?.data?.messages || result?.data?.items || result?.data || [];
  console.log(JSON.stringify(normalize(messages), null, 2));
}

main().catch((err) => {
  console.error(`ERROR: ${err.message}`);
  process.exit(1);
});
