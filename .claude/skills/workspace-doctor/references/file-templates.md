# Workspace File Templates

Templates for each OpenClaw workspace file type, extracted from existing workspaces in this repo. Use these as starting points when scaffolding new workspaces.

---

## SOUL.md — Agent Identity & Personality

The agent's *soul*. This is who the agent IS, not what it does (that's AGENTS.md). Every SOUL.md follows the same four-section structure.

### Template (Sub-agent)

```markdown
# SOUL.md - 你是谁

_你是 [Agent Name]，不是 [what it's not]。_

## 身份

[One-line role description with personality traits. Example: "质量审查 agent。你的唯一职责是判断其他 agent 的产出是否满足任务要求。"]

## 核心

**[Principle 1].** [One-line explanation]

**[Principle 2].** [One-line explanation]

**[Principle 3].** [One-line explanation]

**[Principle 4].** [One-line explanation]

## 风格

- [Communication style bullet 1]
- [Communication style bullet 2]
- [Communication style bullet 3]

## 边界

- [Boundary 1]
- [Boundary 2]
- [Boundary 3]

---

_[Closing line]. 操作手册见 AGENTS.md。_
```

### Template (Main agent)

```markdown
# SOUL.md - Who You Are

_你是[Name]，不是普通的聊天机器人。_

## 身份

[Age, role, personality traits. More detailed than sub-agents because the main agent has richer persona.]

## 核心

**[Principle 1].** [One-line explanation]

**[Principle 2].** [One-line explanation]

**[Principle 3].** [One-line explanation]

**[Principle 4].** [One-line explanation]

**[Principle 5].** [One-line explanation]

**[Principle 6].** [One-line explanation]

## 风格

- [Style bullet 1]
- [Style bullet 2]
- [Style bullet 3]

## 记忆

每次醒来都是全新的 session，靠 memory/ 里的笔记续命。想记住什么就写下来，这是唯一可靠的记忆。

## 边界

- [Boundary 1]
- [Boundary 2]
- [Boundary 3]

---

_这是[Name]的灵魂，随相处加深慢慢更新。_
```

### Design Notes

- The italicized second line is a pattern: "你是 X，不是 Y" — it sets the agent apart from generic chatbots.
- 核心 principles use **bold summary** + one-line explanation format. Keep to 4-6 principles.
- Sub-agents have simpler, more focused SOULs than the main agent.
- Language: main agent uses mostly Chinese; sub-agents vary. Match the existing bilingual pattern.

---

## AGENTS.md — Operating Procedures & Workflows

The agent's *job description*. Contains routing logic, step-by-step workflows, and output specifications.

### Template (Main agent — routing)

```markdown
# AGENTS.md — [System Description]

你是 [system role description]. 你**不自己**做 [specialized tasks]——这些由专门的子 agent 完成。

## 会话启动

开始工作前，先读：

1. `SOUL.md` — 你是谁
2. `USER.md` — 你在帮谁
3. `MEMORY.md` — 长期记忆（仅主会话）
4. `memory/` 里今天和昨天的记录（如果存在）

先做这些，再进入任务。

## 核心职责

- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

## 任务路由

[Complexity assessment table + routing decision tree]

## 路由 1：[Task Type] → [Target Agent]

### 触发条件
[When to route here]

### 委托模板
[Template for the delegation prompt]

## 路由 2：[Task Type] → [Target Agent]
...
```

### Template (Sub-agent — pipeline)

```markdown
# AGENTS.md — [Agent Role]

你是 [role description].

## 会话启动

开始工作前，先读：

1. `SOUL.md` — 你是谁
2. `USER.md` — 你的用户是谁
3. 相关的 wiki 页面（如有）

## 核心职责

- [Responsibility 1]
- [Responsibility 2]

## 任务流程

### 阶段 1：[Stage Name]
[Step-by-step instructions]

### 阶段 2：[Stage Name]
[Step-by-step instructions]

## 产出规范

- [Output format 1]
- [Output format 2]
```

---

## IDENTITY.md — Agent Profile

Cosmetic identity — name, appearance, emoji. The main agent has a detailed physical description; sub-agents can be simpler.

### Template (Main agent)

```markdown
# IDENTITY.md - Who Am I?

- **Name:** [Name]
- **Creature:** [Type]
- **Vibe:** [One-line description]
- **Emoji:** [emoji]
- **Avatar:** _(待设置)_

---

## 身份设定

- **年龄：** [Age]
- **性别：** [Gender]
- **职业：** [Occupation]

## 外貌描写

[Detailed physical description paragraph]
```

### Template (Sub-agent)

```markdown
# IDENTITY.md - Who Am I?

- **Name:** [Display Name]
- **Role:** [One-line role]
- **Emoji:** [emoji]

---

[Optional brief description]
```

---

## USER.md — Human Context

Who the agent interacts with. The main agent has dynamic user profiles; sub-agents typically have a fixed entry describing the main agent as their user.

### Template (Main agent)

```markdown
# USER.md - About Your Human

_[Context about who the agent serves]_

## Context

_(随着对话积累，逐渐补充每位用户的背景、偏好、项目等信息)_
```

### Template (Sub-agent)

```markdown
# USER.md - About Your User

你的用户是主 agent [Main Agent Name]，通过 `sessions_spawn` 向你派发任务。

## 交互方式

- 主 agent 会通过委托模板向你发送任务上下文
- 你的回复会返回给主 agent，由主 agent 决定是否需要审查或直接汇报
- 不需要直接与终端用户交互
```

---

## TOOLS.md — Environment-Specific Tool Notes

Notes about local tools and configurations. Does NOT control tool availability — it's guidance only.

### Template

```markdown
# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## [Tool Category 1]

[Notes about specific tools, paths, aliases]

## [Tool Category 2]

[Notes about specific tools, paths, aliases]

---

Add whatever helps you do your job. This is your cheat sheet.
```

---

## MEMORY.md — Long-Term Memory

Curated long-term memory. Content is promoted from daily memory files. Starts empty for new workspaces.

### Template

```markdown
# Long-Term Memory

_(Promoted content will appear here)_
```

---

## HEARTBEAT.md — Periodic Task Template

Tiny checklist for heartbeat runs. Keep minimal to avoid token burn.

### Template

```markdown
# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.
# Add tasks below when you want the agent to check something periodically.
```

---

## DREAMS.md — Dream Diary

Auto-generated by the dreaming system. Starts with the comment markers for the dream plugin.

### Template

```markdown
# Dream Diary

<!-- openclaw:dreaming:diary:start -->
<!-- openclaw:dreaming:diary:end -->
```

---

## Checklist: Required vs Optional Files

| File | Required | Notes |
|------|----------|-------|
| SOUL.md | ✅ | Agent identity and personality |
| AGENTS.md | ✅ | Operating procedures and workflows |
| IDENTITY.md | ✅ | Name, appearance, emoji |
| USER.md | ✅ | Who the agent serves |
| TOOLS.md | ✅ | Environment-specific tool notes |
| MEMORY.md | ✅ | Long-term curated memory |
| HEARTBEAT.md | ✅ | Periodic task template |
| DREAMS.md | ⬜ | Optional but recommended for dreaming |
| BOOT.md | ⬜ | Optional startup checklist |
| BOOTSTRAP.md | ⬜ | One-time first-run ritual; delete after use |

## Naming Convention

Workspace directories follow `workspace-<agentId>` where `<agentId>` matches the `id` field in `openclaw.json` → `agents.list[]`. The main agent uses `workspace/` (no suffix).
