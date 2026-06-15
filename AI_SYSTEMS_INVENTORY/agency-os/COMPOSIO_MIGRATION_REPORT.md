# Composio SDK Migration Report

Migration of `connect_composio.mjs` away from the retired
`connectedAccounts.initiate()` endpoint, per `@composio/core`'s own
deprecation error and recommended fix.

---

## 1. What was deprecated

Running `node connect_composio.mjs gmail` (or `slack`/`status`) on a machine
with working Composio connectivity now throws:

```
ComposioLegacyConnectedAccountsEndpointRetiredError:
POST /api/v3/connected_accounts is no longer supported for Composio-managed
OAuth auth configs. Use composio.connectedAccounts.link() instead.
```

This is thrown by `@composio/core` v0.10.0
(`node_modules/@composio/core/dist/index.mjs`) whenever
`connectedAccounts.initiate(userId, authConfigId, options)` is called for an
auth config created with `type: 'use_composio_managed_auth'` (exactly what
`connect_composio.mjs` does). The SDK's own error message prescribes the fix:
replace `initiate()` with `link()`, same call signature, same return shape
(`id`, `redirectUrl`, `status`, and a `waitForConnection(timeout)` method via
the shared `createConnectionRequest()` helper).

## 2. Fix applied to `connect_composio.mjs`

### 2a. Core fix - replace the retired `initiate()` call

```diff
- const connectionRequest = await composio.connectedAccounts.initiate(USER_ID, authConfig.id);
+ const connectionRequest = await composio.connectedAccounts.link(USER_ID, authConfig.id);
```

This change was already applied directly on the Mac (commit `ffbdb80`, "Fix
Composio OAuth flow and SDK compatibility") - the user's local test confirmed
it resolves `ComposioLegacyConnectedAccountsEndpointRetiredError` and the
OAuth flow proceeds. Separately, the same fix was independently verified here
against the SDK source (`connectedAccounts.link()`, `dist/index.mjs`): it
calls `client.link.create({ auth_config_id, user_id })` and returns
`createConnectionRequest(client, connected_account_id,
ConnectedAccountStatuses.INITIATED, redirect_url)` - the identical object
shape the rest of `connect_composio.mjs` already expects
(`connectionRequest.redirectUrl`, `connectionRequest.waitForConnection(120000)`,
`connectedAccount.id`). No downstream code needed to change.

The same Mac commit also added `memory/connections.json` to `.gitignore` and
pinned `toolkitVersions: { slack: '20250902_00' }` in `fetch_slack.mjs` for
SDK compatibility - both outside the scope of this report but consistent with
"migrate to current Composio API, no redesign".

### 2b. Secondary fix - `connectedAccounts.list()` param schema

While inspecting the SDK, found the `status` subcommand was passing an
invalid filter key:

```diff
- const accounts = await composio.connectedAccounts.list({ userId: USER_ID });
+ const accounts = await composio.connectedAccounts.list({ userIds: [USER_ID] });
```

`ConnectedAccountListParamsSchema` (the zod schema validating
`connectedAccounts.list()` input) only recognizes `userIds` (an array). The
old `userId` (singular) key is not part of the schema and was silently
dropped, so `status` was returning **all** connected accounts visible to the
API key rather than just `agency-owner`'s. This is unrelated to the reported
deprecation but directly affects "verify Gmail/Slack connection flow works"
(the `status` command is how connection state is checked), so it was fixed
in the same pass.

## 3. Fetchers - no changes needed

Checked `fetch_gmail.mjs` and `fetch_slack.mjs` for any use of
`connectedAccounts.initiate()`/`.link()`/`.list()`:

```
$ grep -n "connectedAccounts" connect_composio.mjs fetch_gmail.mjs fetch_slack.mjs
connect_composio.mjs:45:    const accounts = await composio.connectedAccounts.list({ userIds: [USER_ID] });
connect_composio.mjs:62:  const connectionRequest = await composio.connectedAccounts.link(USER_ID, authConfig.id);
```

Neither fetcher calls any `connectedAccounts.*` method - both only call
`composio.tools.execute('GMAIL_FETCH_EMAILS' / 'SLACK_LIST_CHANNELS' /
'SLACK_FETCH_CONVERSATION_HISTORY', ...)` using the `connectedAccountId`
already stored in `memory/connections.json`. **No changes required.**

A broader grep of the installed SDK (`dist/index.mjs`) for
`Deprecat|deprecated|Retired` confirms `connectedAccounts.initiate()` is the
only retired API used anywhere in this codebase; the other deprecation
warnings in the SDK relate to the Assistants API, which Agency OS does not
use.

## 4. Verification status

| Check | Result |
|---|---|
| `node --check connect_composio.mjs` | **Pass** - syntax valid |
| SDK source inspection of `link()` return shape vs. `initiate()` usage | **Pass** - identical shape, no downstream changes needed |
| `connectedAccounts.link()` fix (Mac) | **Pass** - already applied and verified on the Mac (commit `ffbdb80`), resolves `ComposioLegacyConnectedAccountsEndpointRetiredError` |
| `node connect_composio.mjs status` (this cloud sandbox) | **Blocked** - `PermissionDeniedError: 403 Host not in allowlist: backend.composio.dev` (pre-existing sandbox egress block, unrelated to this migration - same issue documented in `LOCAL_DEPLOYMENT_STATUS.md`) |
| `node connect_composio.mjs gmail` (this cloud sandbox) | **Blocked** - same egress block, fails before reaching the deprecated/new endpoint either way |
| `connectedAccounts.list({ userIds: [...] })` fix (`status` subcommand) | **Not yet re-run on Mac** - needs confirmation that `status` now scopes to `agency-owner` only |
| Gmail/Slack OAuth flow end-to-end (Mac) | Reported working as of `ffbdb80` for the `link()` fix; re-run after this `userIds` fix to confirm `status` output |

This cloud sandbox cannot reach `backend.composio.dev` at all (independent of
the deprecation fix), so the `userIds` fix could not be exercised here. It is
verified correct via the SDK's `ConnectedAccountListParamsSchema` definition
(`userIds: string[]` is the only recognized user filter key).

## 5. Remaining manual steps (on the Mac)

1. Pull this branch to pick up the `userIds` fix to the `status` subcommand.
2. `node connect_composio.mjs gmail` -> open the printed OAuth URL -> approve
   in browser -> confirm `SUCCESS - gmail connected.` and that
   `memory/connections.json` now has a `gmail` entry.
3. `node connect_composio.mjs slack` -> same, for `slack`.
4. `node connect_composio.mjs status` -> confirm it lists only
   `agency-owner`'s connected accounts (gmail + slack), validating the
   `userIds` fix.
5. `python3 morning_brief.py --source composio --no-save` -> confirm it no
   longer fails with `memory/connections.json not found` and renders real
   Gmail/Slack data.

## 6. Scope

No architectural changes were made. The deprecated-method swap (`initiate()`
-> `link()`) was already applied on the Mac (commit `ffbdb80`); this pass
added one additional one-line fix to `connect_composio.mjs` (the
`connectedAccounts.list()` params schema) and this report. No other files
were modified. No API keys were printed, logged, or committed.
