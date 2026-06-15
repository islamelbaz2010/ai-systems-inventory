// Fetches recent Slack messages from #team via Composio, normalized to the same shape
// as sample_data/slack_messages.json so morning_brief.py can consume either source.
//
// Requires: COMPOSIO_API_KEY env var, and Slack connected via
// `node connect_composio.mjs slack` (connection ID read from memory/connections.json).
//
// Run directly to sanity-check: node fetch_slack.mjs [#channel-name]
// Outputs a JSON array on stdout.

import { Composio } from '@composio/core';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const CONNECTIONS_PATH = path.join(__dirname, 'memory', 'connections.json');
const USER_ID = 'agency-owner';
const CHANNEL_NAME = (process.argv[2] || '#team').replace(/^#/, '');

function loadConnections() {
  if (!fs.existsSync(CONNECTIONS_PATH)) {
    throw new Error(
      `${CONNECTIONS_PATH} not found. Run "node connect_composio.mjs slack" first.`
    );
  }
  return JSON.parse(fs.readFileSync(CONNECTIONS_PATH, 'utf8'));
}

function normalize(rawMessages, channelName, userMap) {
  return rawMessages.map((m, i) => ({
    id: m.ts || `slack-live-${i}`,
    channel: `#${channelName}`,
    user: userMap[m.user] || m.user || m.username || 'unknown',
    text: m.text || '',
    ts: m.ts ? new Date(parseFloat(m.ts) * 1000).toISOString() : new Date().toISOString(),
  }));
}

async function main() {
  const apiKey = process.env.COMPOSIO_API_KEY;
  if (!apiKey) {
    throw new Error('COMPOSIO_API_KEY is not set.');
  }
  const connections = loadConnections();
  if (!connections.slack) {
    throw new Error('Slack is not connected. Run "node connect_composio.mjs slack" first.');
  }

  const composio = new Composio({
  apiKey,
  toolkitVersions: {
    slack: '20250902_00'
  }
});
  const connectedAccountId = connections.slack.connectedAccountId;

  // 1. Resolve channel name -> channel ID
  const channelsResult = await composio.tools.execute('SLACK_LIST_CHANNELS', {
    userId: USER_ID,
    connectedAccountId,
    arguments: { types: 'public_channel,private_channel', limit: 200 },
  });
  const channels = channelsResult?.data?.channels || channelsResult?.data || [];
  const channel = channels.find((c) => c.name === CHANNEL_NAME);
  if (!channel) {
    throw new Error(
      `Channel "#${CHANNEL_NAME}" not found. Available: ${channels.map((c) => c.name).join(', ')}`
    );
  }

  // 2. Fetch recent conversation history for that channel.
  // Verify the exact tool slug/args locally with:
  //   composio.tools.get(USER_ID, { toolkits: ['slack'] }).then(t => console.log(JSON.stringify(t, null, 2)))
  const historyResult = await composio.tools.execute('SLACK_FETCH_CONVERSATION_HISTORY', {
    userId: USER_ID,
    connectedAccountId,
    arguments: { channel: channel.id, limit: 20 },
  });
  const messages = historyResult?.data?.messages || historyResult?.data || [];

  console.log(JSON.stringify(normalize(messages, CHANNEL_NAME, {}), null, 2));
}

main().catch((err) => {
  console.error(`ERROR: ${err.message}`);
  process.exit(1);
});
