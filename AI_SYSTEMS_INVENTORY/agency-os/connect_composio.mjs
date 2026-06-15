// Connects Gmail and Slack via Composio's managed OAuth.
// Requires COMPOSIO_API_KEY in the environment (from https://platform.composio.dev/).
//
// Usage:
//   node connect_composio.mjs gmail   -> prints a Google OAuth URL, then waits for you to approve it
//   node connect_composio.mjs slack   -> prints a Slack OAuth URL, then waits for you to approve it
//   node connect_composio.mjs status  -> lists current connected accounts
//
// On success, the connected account ID is appended to connections.json so
// morning_brief.py can use it.

import { Composio } from '@composio/core';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const CONNECTIONS_PATH = path.join(__dirname, 'memory', 'connections.json');
const USER_ID = 'agency-owner';

function loadConnections() {
  if (fs.existsSync(CONNECTIONS_PATH)) {
    return JSON.parse(fs.readFileSync(CONNECTIONS_PATH, 'utf8'));
  }
  return {};
}

function saveConnections(data) {
  fs.writeFileSync(CONNECTIONS_PATH, JSON.stringify(data, null, 2));
}

async function main() {
  const apiKey = process.env.COMPOSIO_API_KEY;
  if (!apiKey) {
    console.error('ERROR: COMPOSIO_API_KEY is not set.');
    console.error('Get a free key at https://platform.composio.dev/ then run:');
    console.error('  export COMPOSIO_API_KEY="your-key-here"');
    process.exit(1);
  }

  const composio = new Composio({ apiKey });
  const toolkit = process.argv[2];

  if (toolkit === 'status') {
    const accounts = await composio.connectedAccounts.list({ userIds: [USER_ID] });
    console.log(JSON.stringify(accounts, null, 2));
    return;
  }

  if (toolkit !== 'gmail' && toolkit !== 'slack') {
    console.error('Usage: node connect_composio.mjs <gmail|slack|status>');
    process.exit(1);
  }

  console.log(`Creating a Composio-managed auth config for "${toolkit}"...`);
  const authConfig = await composio.authConfigs.create(toolkit, {
    type: 'use_composio_managed_auth',
  });
  console.log(`Auth config created: ${authConfig.id}`);

  console.log(`Initiating connection for "${toolkit}" (user: ${USER_ID})...`);
  const connectionRequest = await composio.connectedAccounts.link(USER_ID, authConfig.id);

  console.log('');
  console.log('=========================================================');
  console.log(`OPEN THIS URL IN YOUR BROWSER TO AUTHORIZE ${toolkit.toUpperCase()}:`);
  console.log('');
  console.log(connectionRequest.redirectUrl);
  console.log('');
  console.log('=========================================================');
  console.log('Waiting up to 120 seconds for you to complete the authorization...');

  try {
    const connectedAccount = await connectionRequest.waitForConnection(120000);
    console.log('');
    console.log(`SUCCESS - ${toolkit} connected.`);
    console.log(`Connected account ID: ${connectedAccount.id}`);

    const connections = loadConnections();
    connections[toolkit] = {
      connectedAccountId: connectedAccount.id,
      authConfigId: authConfig.id,
      userId: USER_ID,
      connectedAt: new Date().toISOString(),
    };
    saveConnections(connections);
    console.log(`Saved to ${CONNECTIONS_PATH}`);
  } catch (err) {
    console.error('');
    console.error(`Connection did not complete: ${err.message}`);
    console.error('Re-run this command after opening the URL above and approving access.');
    process.exit(1);
  }
}

main();
