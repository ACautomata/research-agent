# OpenClaw Design References

Local snapshots of key OpenClaw automation / orchestration concepts. **Consult these before designing new features** in this repo (new agents, skills, subagents, scheduled work, event-driven behaviour, approval flows, multi-step pipelines).

These are reference docs — not project source. Keep them updated when the upstream pages change. The official, authoritative source is <https://docs.openclaw.ai/>.

## When to read what

| You're designing… | Read first |
| --- | --- |
| A new subagent or skill | `automation-overview.md` (decision guide), `standing-orders.md` (authority & escalation) |
| A scheduled or recurring job | `automation-overview.md`, `automation-taskflow.md` (durable multi-step flows) |
| A one-shot reminder or follow-up | `commitments.md` (inferred) vs `automation-overview.md` → Scheduled Tasks (exact) |
| An event-driven side effect (e.g. on `/new`, `/reset`, message received) | `hooks.md` (internal hooks) |
| A multi-step pipeline that needs resumable approvals and structured output | `tools-lobster.md` (typed workflow runtime), `automation-taskflow.md` (durable orchestration) |
| Routine monitoring that doesn't need exact timing | `automation-overview.md` → Heartbeat section |

## Index

- [`automation-overview.md`](automation-overview.md) — quick decision guide, how the 6 mechanisms fit together, when to use which
- [`automation-taskflow.md`](automation-taskflow.md) — Task Flow (managed / mirrored modes, durable state, cron + lobster pattern)
- [`tools-lobster.md`](tools-lobster.md) — Lobster: typed workflow runtime, `.lobster` files, approval gates, resume tokens
- [`commitments.md`](commitments.md) — Inferred Commitments: short-lived follow-up memories via heartbeat
- [`standing-orders.md`](standing-orders.md) — Standing Orders: permanent operating authority in `AGENTS.md`
- [`hooks.md`](hooks.md) — Internal Hooks: event-driven scripts (command, session, message, gateway lifecycle)

## Maintenance

- Source URLs are at the top of each file.
- When adding a new agent/skill/cron/hook, cross-check the design against at least one of these references.
- When the OpenClaw docs change materially, refresh the corresponding local file (a `git log` on `docs/` is a useful audit trail).
