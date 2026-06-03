# Task Flow

Source: <https://docs.openclaw.ai/automation/taskflow> (fetched 2026-06-03).

## Overview

Task Flow serves as the flow orchestration substrate positioned above background tasks. It handles durable multi-step flows featuring their own state, revision tracking, and sync semantics, while individual tasks function as the unit of detached work.

## Purpose

Task Flow enables workflows spanning multiple sequential or branching steps requiring durable progress tracking across gateway restarts. For single background operations, a plain task remains sufficient.

## When to Use

| Scenario | Recommendation |
| --- | --- |
| Single background job | Plain task |
| Multi-step pipeline (A then B then C) | Task Flow (managed) |
| Observe externally created tasks | Task Flow (mirrored) |
| One-shot reminder | Cron job |

## Sync Modes

### Managed Mode

Task Flow owns the lifecycle end-to-end. It creates tasks as flow steps, drives them to completion, and advances the flow state automatically.

**Example progression:**

```
Flow: weekly-report
  Step 1: gather-data     → task created → succeeded
  Step 2: generate-report → task created → succeeded
  Step 3: deliver         → task created → running
```

### Mirrored Mode

Task Flow observes externally created tasks and maintains flow state synchronization without owning task creation. This proves valuable when tasks originate from cron jobs, CLI commands, or other sources and you require a unified progress view as a flow.

## Durable State and Revision Tracking

Each flow persists its own state and tracks revisions, enabling progress to survive gateway restarts. Revision tracking facilitates conflict detection when multiple sources attempt to advance the same flow concurrently. The flow registry employs SQLite with bounded write-ahead-log maintenance, incorporating periodic and shutdown checkpoints to prevent unbounded `registry.sqlite-wal` sidecar files on long-running gateways.

## Cancel Behavior

`openclaw tasks flow cancel` establishes a sticky cancel intent on the flow. Active tasks within the flow get cancelled, and no new steps initiate. The cancel intent persists across restarts, ensuring a cancelled flow remains cancelled even if the gateway restarts before all child tasks terminate.

## CLI Commands

```bash
# List active and recent flows
openclaw tasks flow list

# Show details for a specific flow
openclaw tasks flow show <lookup>

# Cancel a running flow and its active tasks
openclaw tasks flow cancel <lookup>
```

| Command | Description |
| --- | --- |
| `openclaw tasks flow list` | Displays tracked flows with status and sync mode |
| `openclaw tasks flow show <id>` | Inspects one flow by flow id or lookup key |
| `openclaw tasks flow cancel <id>` | Cancels a running flow and its active tasks |

## Reliable Scheduled Workflow Pattern

For recurring workflows such as market intelligence briefings, treat the schedule, orchestration, and reliability checks as separate layers:

1. Use Scheduled Tasks for timing
2. Use a persistent cron session when the workflow builds on prior context
3. Use Lobster for deterministic steps, approval gates, and resume tokens
4. Use Task Flow to track the multi-step run across child tasks, waits, retries, and gateway restarts

**Example cron configuration:**

```bash
openclaw cron add \
  --name "Market intelligence brief" \
  --cron "0 7 * * 1-5" \
  --tz "America/New_York" \
  --session session:market-intel \
  --message "Run the market-intel Lobster workflow. Verify source freshness before summarizing." \
  --announce \
  --channel slack \
  --to "channel:C1234567890"
```

**Session strategy:**

- Use `session:<id>` when the recurring workflow needs deliberate history, previous run summaries, or standing context
- Use `isolated` when each run should start fresh and all required state is explicit in the workflow

**Example workflow definition:**

```yaml
name: market-intel-brief
steps:
  - id: preflight
    command: market-intel check --json
  - id: collect
    command: market-intel collect --json
    stdin: $preflight.json
  - id: summarize
    command: market-intel summarize --json
    stdin: $collect.json
  - id: approve
    command: market-intel deliver --preview
    stdin: $summarize.json
    approval: required
  - id: deliver
    command: market-intel deliver --execute
    stdin: $summarize.json
    condition: $approve.approved
```

## Design Recommendations

### Preflight Checks

Place reliability checks before the LLM summary step:

- Browser availability and profile choice (managed state via `openclaw` or signed-in Chrome via `user`)
- API credentials and quota for each source
- Network reachability for required endpoints
- Required tools enabled for the agent (lobster, browser, llm-task)
- Failure destination configured for cron to ensure preflight failures are visible

### Data Provenance

Include these fields for every collected item:

```json
{
  "sourceUrl": "https://example.com/report",
  "retrievedAt": "2026-04-24T12:00:00Z",
  "asOf": "2026-04-24",
  "title": "Example report",
  "content": "..."
}
```

Have the workflow reject or mark stale items before summarization. The LLM step should receive only structured JSON and should be asked to preserve `sourceUrl`, `retrievedAt`, and `asOf` in its output. Use LLM Task when a schema-validated model step inside the workflow is needed.

### Package Reuse

For reusable team or community workflows, package the CLI, `.lobster` files, and setup notes as a skill or plugin, then publish through ClawHub. Keep workflow-specific guardrails in that package unless the plugin API lacks a needed generic capability.

## Relationship to Tasks

Flows coordinate tasks rather than replace them. A single flow may drive multiple background tasks over its lifetime. Use `openclaw tasks` to inspect individual task records and `openclaw tasks flow` to inspect the orchestrating flow.
