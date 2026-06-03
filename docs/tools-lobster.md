# Lobster — Typed Workflow Runtime

Source: <https://docs.openclaw.ai/tools/lobster> (fetched 2026-06-03).

A typed workflow runtime for OpenClaw with resumable approval gates.

## Overview

Lobster is a workflow shell that lets OpenClaw run multi-step tool sequences as a single, deterministic operation with explicit approval checkpoints.

## Purpose

Lobster moves orchestration into a typed runtime:

- **One call instead of many**: OpenClaw runs one Lobster tool call and gets a structured result.
- **Approvals built in**: Side effects halt the workflow until explicitly approved.
- **Resumable**: Halted workflows return a token; approve and resume without re-running everything.

## How It Works

OpenClaw runs Lobster workflows **in-process** using an embedded runner. No external CLI subprocess is spawned; the workflow engine executes inside the gateway process and returns a JSON envelope directly.

## Installation

Bundled Lobster workflows run in-process; no separate `lobster` binary is required. For standalone CLI, install from the [Lobster repo](https://github.com/openclaw/lobster).

## Enable the Tool

Lobster is an optional plugin tool (not enabled by default).

Recommended (additive, safe):

```json
{
  "tools": {
    "alsoAllow": ["lobster"]
  }
}
```

Or per-agent:

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": {
          "alsoAllow": ["lobster"]
        }
      }
    ]
  }
}
```

## Tool Parameters

### `run`

Run a pipeline in tool mode.

```json
{
  "action": "run",
  "pipeline": "gog.gmail.search --query 'newer_than:1d' | email.triage",
  "cwd": "workspace",
  "timeoutMs": 30000,
  "maxStdoutBytes": 512000
}
```

Run a workflow file with args:

```json
{
  "action": "run",
  "pipeline": "/path/to/inbox-triage.lobster",
  "argsJson": "{\"tag\":\"family\"}"
}
```

### `resume`

Continue a halted workflow after approval.

```json
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

### Optional Inputs

| Parameter | Description |
| --- | --- |
| `cwd` | Relative working directory (must stay within gateway working directory) |
| `timeoutMs` | Abort if exceeded (default: 20000) |
| `maxStdoutBytes` | Abort if output exceeds this size (default: 512000) |
| `argsJson` | JSON string passed to workflow files only |

## Output Envelope

Lobster returns a JSON envelope with one of three statuses:

- `ok` → finished successfully
- `needs_approval` → paused; `requiresApproval.resumeToken` is required to resume
- `cancelled` → explicitly denied or cancelled

## Pattern: CLI + JSON Pipes + Approvals

```bash
inbox list --json
inbox categorize --json
inbox apply --json
```

```json
{
  "action": "run",
  "pipeline": "exec --json --shell 'inbox list --json' | exec --stdin json --shell 'inbox categorize --json' | exec --stdin json --shell 'inbox apply --json' | approve --preview-from-stdin --limit 5 --prompt 'Apply changes?'",
  "timeoutMs": 30000
}
```

## Workflow Files (.lobster)

Lobster can run YAML/JSON workflow files with `name`, `args`, `steps`, `env`, `condition`, and `approval` fields.

```yaml
name: inbox-triage
args:
  tag:
    default: "family"
steps:
  - id: collect
    command: inbox list --json
  - id: categorize
    command: inbox categorize --json
    stdin: $collect.stdout
  - id: approve
    command: inbox apply --approve
    stdin: $categorize.stdout
    approval: required
  - id: execute
    command: inbox apply --execute
    stdin: $categorize.stdout
    condition: $approve.approved
```

Notes:

- `stdin: $step.stdout` and `stdin: $step.json` pass a prior step's output
- `condition` (or `when`) can gate steps on `$step.approved`

## Example: Email Triage

Without Lobster:

```
User: "Check my email and draft replies"
→ openclaw calls gmail.list
→ LLM summarizes
→ User: "draft replies to #2 and #5"
→ LLM drafts
→ User: "send #2"
→ openclaw calls gmail.send
(repeat daily, no memory of what was triaged)
```

With Lobster:

```json
{
  "action": "run",
  "pipeline": "email.triage --limit 20",
  "timeoutMs": 30000
}
```

Returns:

```json
{
  "ok": true,
  "status": "needs_approval",
  "output": [{ "summary": "5 need replies, 2 need action" }],
  "requiresApproval": {
    "type": "approval_request",
    "prompt": "Send 2 draft replies?",
    "items": [],
    "resumeToken": "..."
  }
}
```

User approves → resume:

```json
{
  "action": "resume",
  "token": "<resumeToken>",
  "approve": true
}
```

## JSON-Only LLM Steps (llm-task)

For workflows needing a structured LLM step, enable the optional `llm-task` plugin:

```json
{
  "plugins": {
    "entries": {
      "llm-task": { "enabled": true }
    }
  },
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": { "alsoAllow": ["llm-task"] }
      }
    ]
  }
}
```

### Important Limitation

The bundled Lobster plugin runs workflows in-process. In embedded mode, `openclaw.invoke` does not automatically inherit gateway URL/auth context for nested CLI calls.

Use standalone Lobster CLI when calling `openclaw.invoke` from within workflows.

## Approvals

If `requiresApproval` is present:

- `approve: true` → resume and continue side effects
- `approve: false` → cancel and finalize the workflow

Use `approve --preview-from-stdin --limit N` to attach a JSON preview to approval requests.

## Safety

- **Local in-process only** — workflows execute inside the gateway process
- **No secrets** — Lobster doesn't manage OAuth; it calls OpenClaw tools that do
- **Sandbox-aware** — disabled when the tool context is sandboxed
- **Hardened** — timeouts and output caps enforced by the embedded runner

## Troubleshooting

- `lobster timed out` → increase `timeoutMs`, or split a long pipeline
- `lobster output exceeded maxStdoutBytes` → raise `maxStdoutBytes` or reduce output size
- `lobster returned invalid JSON` → ensure the pipeline runs in tool mode and prints only JSON
- `lobster failed` → check gateway logs for the embedded runner error details

## Design Takeaways (for new features)

- **One typed call > many LLM round-trips** — collapse multi-step tool sequences into a single Lobster run with deterministic steps + JSON pipes.
- **Default to `needs_approval` for any side effect** — preview must be reviewable, and the resume token is the contract.
- **Surface provenance + provenance timestamps** — see Task Flow `Data Provenance` recommendations: `sourceUrl`, `retrievedAt`, `asOf` belong on every collected item.
- **Don't store secrets in Lobster** — it composes tools that already hold OAuth.
- **For nested `openclaw.invoke` calls, use standalone CLI** — embedded mode does not inherit gateway auth context.
