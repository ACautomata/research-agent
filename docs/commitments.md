# Inferred Commitments

Source: <https://docs.openclaw.ai/concepts/commitments> (fetched 2026-06-03).

## Overview

Commitments are short-lived follow-up memories that OpenClaw can automatically create when a conversation suggests a future check-in opportunity. They sit between memory and automation, allowing the system to remember conversation-bound obligations and deliver them via heartbeat when due.

## What Are Commitments?

Commitments are inferred follow-ups, not exact reminders. They capture natural follow-up opportunities that arise during conversation but weren't explicitly scheduled by the user.

**Examples include:**

- Mentioning an interview tomorrow → OpenClaw checks in afterward
- Saying you are exhausted → OpenClaw asks later about sleep
- An agent promising to follow up after a change → OpenClaw tracks that open loop

## Lifecycle

1. **Create**: After an agent reply, OpenClaw runs a hidden background extraction pass. High-confidence candidates become stored commitments with:
   - Agent ID and session key
   - Original channel and delivery target
   - Due window
   - Suggested check-in text
   - Metadata for heartbeat decision-making

2. **Track**: Stored commitments remain internal until due. Delivery is scoped to the exact agent and channel where created.

3. **Fulfill**: When due, heartbeat adds the commitment to the turn. The model either sends a natural check-in or replies `HEARTBEAT_OK` to dismiss it.

4. **Release**: Commitments are dismissed, snoozed, or expire. They never replay original conversation text.

**Key constraint**: Commitments cannot echo back in the same moment they were inferred. Due time is clamped to at least one heartbeat interval after creation.

## When to Use Commitments

| Scenario | Approach |
| --- | --- |
| "Remind me at 3 PM" | Scheduled tasks |
| "Ping me in 20 minutes" | Scheduled tasks |
| "I have an interview tomorrow" | Commitments |
| "I was up all night" | Commitments |
| "Follow up if I don't answer" | Commitments |

Exact user requests go to the scheduler. Commitments are **only for inferred follow-ups** — moments where the user didn't ask but the conversation clearly created a useful check-in.

## Configuration

Enable in config:

```bash
openclaw config set commitments.enabled true
openclaw config set commitments.maxPerDay 3
```

Or via `openclaw.json`:

```json
{
  "commitments": {
    "enabled": true,
    "maxPerDay": 3
  }
}
```

- `maxPerDay` defaults to 3 per agent session in a rolling day
- Disable with `openclaw config set commitments.enabled false`

## Managing Commitments

```bash
openclaw commitments
openclaw commitments --all
openclaw commitments --agent main
openclaw commitments --status snoozed
openclaw commitments dismiss cm_abc123
```

## Privacy and Cost

- Extraction uses an LLM pass, adding background model usage after eligible turns
- Stored commitments are local OpenClaw state, not long-term memory
- Pass can read recent exchanges to decide on follow-ups

## Troubleshooting

If follow-ups aren't appearing:

- Confirm `commitments.enabled` is `true`
- Check `openclaw commitments --all` for pending/dismissed/snoozed/expired records
- Verify heartbeat is running for the agent
- Check if `maxPerDay` limit reached
- Remember exact reminders belong to scheduled tasks

## Design Takeaways

- **Inferred ≠ requested.** If a user explicitly asked for a reminder, use cron. Only inferred (sub-textual) follow-ups belong in commitments.
- **Scoped to (agent, channel).** Don't fan a commitment out across channels — context leaks.
- **Bounded noise.** `maxPerDay` is the throttle. Set it conservatively (3 is the default).
- **Fulfilment is conversational.** Heartbeat adds the commitment to the model turn; the model decides whether to actually reach out or reply `HEARTBEAT_OK`.
