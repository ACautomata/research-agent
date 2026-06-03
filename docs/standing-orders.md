# Standing Orders

Source: <https://docs.openclaw.ai/automation/standing-orders> (fetched 2026-06-03).

## What Are Standing Orders?

Standing orders grant an agent **permanent operating authority** for defined programs. Rather than prompting the agent for each task, you define programs with clear scope, triggers, and escalation rules — enabling autonomous execution within defined boundaries.

## Purpose

**Without standing orders:**

- Every task requires prompting
- Agent remains idle between requests
- Routine work gets forgotten or delayed
- Human becomes the bottleneck

**With standing orders:**

- Agent executes autonomously within defined boundaries
- Routine work happens on schedule
- Human involvement only for exceptions and approvals
- Agent fills idle time productively

## How to Create Them

Standing orders are defined in agent workspace files. The recommended approach includes them directly in `AGENTS.md` (auto-injected every session) or in a dedicated `standing-orders.md` file referenced from `AGENTS.md`.

Each program specifies:

1. **Scope** — What the agent is authorized to do
2. **Triggers** — When to execute (schedule, event, or condition)
3. **Approval gates** — What requires human sign-off before acting
4. **Escalation rules** — When to stop and ask for help

## Anatomy of a Standing Order

```markdown
## Program: Weekly Status Report

**Authority:** Compile data, generate report, deliver to stakeholders
**Trigger:** Every Friday at 4 PM (enforced via cron job)
**Approval gate:** None for standard reports. Flag anomalies for human review.
**Escalation:** If data source is unavailable or metrics look unusual (>2σ from norm)

### Execution steps

1. Pull metrics from configured sources
2. Compare to prior week and targets
3. Generate report in Reports/weekly/YYYY-MM-DD.md
4. Deliver summary via configured channel
5. Log completion to Agent/Logs/

### What NOT to do

- Do not send reports to external parties
- Do not modify source data
- Do not skip delivery if metrics look bad - report accurately
```

## Scheduling with Cron Jobs

Standing orders define **what** the agent is authorized to do. Cron jobs define **when** it happens. Together:

```
Standing Order: "You own the daily inbox triage"
    ↓
Cron Job (8 AM daily): "Execute inbox triage per standing orders"
    ↓
Agent: Reads standing orders → executes steps → reports results
```

Example cron job command:

```bash
openclaw cron add \
  --name daily-inbox-triage \
  --cron "0 8 * * 1-5" \
  --tz America/New_York \
  --timeout-seconds 300 \
  --announce \
  --channel imessage \
  --to "+1XXXXXXXXXX" \
  --message "Execute daily inbox triage per standing orders. Check mail for new alerts. Parse, categorize, and persist each item. Report summary to owner. Escalate unknowns."
```

## Execute-Verify-Report Pattern

Every task should follow this loop:

1. **Execute** — Do the actual work
2. **Verify** — Confirm the result is correct
3. **Report** — Tell the owner what was done

```markdown
### Execution rules

- Every task follows Execute-Verify-Report. No exceptions.
- "I'll do that" is not execution. Do it, then report.
- "Done" without verification is not acceptable. Prove it.
- If execution fails: retry once with adjusted approach.
- If still fails: report failure with diagnosis. Never silently fail.
- Never retry indefinitely - 3 attempts max, then escalate.
```

## Multi-Program Architecture

For agents managing multiple concerns, organize standing orders as separate programs with clear boundaries:

```markdown
## Program 1: [Domain A] (Weekly)

...

## Program 2: [Domain B] (Monthly + On-Demand)

...

## Program 3: [Domain C] (As-Needed)

...

## Escalation Rules (All Programs)

- [Common escalation criteria]
- [Approval gates that apply across programs]
```

Each program should have its own trigger cadence, approval gates, and clear boundaries.

## Best Practices

### Do

- Start with narrow authority and expand as trust builds
- Define explicit approval gates for high-risk actions
- Include "What NOT to do" sections
- Combine with cron jobs for reliable time-based execution
- Review agent logs weekly
- Update standing orders as needs evolve

### Avoid

- Granting broad authority on day one
- Skipping escalation rules
- Relying on verbal instructions
- Mixing concerns in a single program
- Skipping cron job enforcement

## Design Takeaways (for new subagents / skills)

- **Standing order = persistent authority** — agent reads it every session, no need to re-prompt.
- **Scope + trigger + approval + escalation** — every program needs all four. Missing any one of them is the bug.
- **Pair every standing order with cron** — standing order says *what* is allowed, cron says *when* it fires.
- **Multi-program boundaries** — if a subagent grows to handle >1 distinct program, split the subagent (per repo `CLAUDE.md` "Single minimal function per subagent").
- **Execute-Verify-Report** — never report without verification; never silently fail.
