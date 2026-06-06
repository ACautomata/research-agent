# Main Agent 调用 paper-review 子 agent 的模板

本文件保存 main agent 通过 `sessions_spawn` / `sessions_send` 委托 paper-review 子 agent
时的 4 个常用场景模板，以及调用前的 9 项关键约定。这些模板来自 `AGENTS.md` 的
"Main Agent 调用此 Subagent 的方式"段落，原本散落在 `AGENTS.md` 中；为保持
`AGENTS.md` 简洁、只描述 agent 自身行为，将调用侧的样例抽出到本文件。

调用 paper-review 子 agent 时，按目标场景复制对应模板，填入 `{}` 占位符即可。

## 场景 1：完整流程（推荐）

```
sessions_spawn(
  agentId: "paper-review",
  task: """对以下论文执行完整的问题分析流程。

## 论文信息
- 标题：{论文标题}
- Wiki路径：{autoresearch wiki 中的路径，如 /workspace/shared/memory-wiki/domains/federated-learning/papers/xxx.md}
- PDF路径：{PDF文件绝对路径或URL，Wiki缺失时必填}
- 代码仓库：{可选，本地绝对路径}

## 执行要求
按 S2→S3→S4→S5 顺序执行，每个阶段完成后将输出保存到
workspace 下的 `outputs/{论文简称}/` 目录。

各阶段输出文件命名：
- {论文简称}-experiment.md
- {论文简称}-problem.md
- {论文简称}-validation.md
- {论文简称}-codex-prompt.md

注意：Wiki 条目由 autoresearch 子 agent 维护，不需要重新整理。
如果 Wiki 路径未提供，请在 /workspace/shared/memory-wiki/ 中自动搜索。
全流程完成后，建议自动执行 S6 质量评估。""",
  mode: "run",
  runTimeoutSeconds: 3600
)
```

## 场景 2：单阶段执行

```
sessions_spawn(
  agentId: "paper-review",
  task: """只执行 S3 paper-review-style-problem-analyzer。

## 已有材料
- 论文标题：{论文标题}
- Wiki条目：{autoresearch wiki 路径 或 outputs中的wiki路径}
- 实验提取：{S2输出文件路径}

## 执行要求
基于以上材料生成审稿式问题分析文档，
输出到 `outputs/{论文简称}/{论文简称}-problem.md`。

只做问题分析，不做实验设计和提示词生成。""",
  mode: "run",
  runTimeoutSeconds: 1800
)
```

## 场景 3：断点续跑

```
sessions_spawn(
  agentId: "paper-review",
  task: """继续之前未完成的流程。

## 已完成
- Wiki条目：{路径，来自autoresearch或outputs}
- S2 实验提取：{路径}

## 待执行
继续执行 S3→S4→S5，阶段间自动衔接。

## 上下文
之前因为 {原因} 中断，所有已有输出在 outputs 目录中。""",
  mode: "run",
  runTimeoutSeconds: 3600
)
```

## 场景 4：仅质量审计

```
sessions_spawn(
  agentId: "paper-review",
  task: """对已有产出执行 S6 paper-pipeline-quality-auditor。

## 待评估文件
- outputs/{论文简称}/{论文简称}-wiki.md（来自autoresearch）
- outputs/{论文简称}/{论文简称}-experiment.md
- outputs/{论文简称}/{论文简称}-problem.md
- outputs/{论文简称}/{论文简称}-validation.md
- outputs/{论文简称}/{论文简称}-codex-prompt.md

只评估，不修改原文件。""",
  mode: "run"
)
```

## 关键约定

调用本 agent 之前，main agent 应确认以下约定，避免参数缺失或上下文不足：

| 约定 | 说明 |
|------|------|
| **Wiki 来源** | 优先使用 autoresearch 知识库中的 wiki；main agent 应尽量传递 wiki 路径 |
| **Wiki 查找** | 若未提供 wiki 路径，本 agent 会在 `/workspace/shared/memory-wiki/` 中自动搜索（沙箱内）；非沙箱环境下回落到 `~/.openclaw/wiki/main/` |
| **PDF 路径** | Wiki 缺失时的兜底方案；必须是 Gateway 可访问的绝对路径或可公网访问的 URL |
| **代码仓库** | 只在 S5 需要；如果无仓库，S5 生成通用框架性提示词 |
| **输出位置** | 默认输出到 `outputs/{论文简称}/` 目录 |
| **超时设置** | S2–S3 各约 10–30 分钟；S4–S5 约 15–45 分钟；全流程建议 3600s+ |
| **进度追踪** | main agent 可用 `subagents(action: "list")` 查看子任务状态 |
| **结果获取** | `mode: "run"` 子任务完成后自动通知 main agent |
| **断点续跑** | 已完成的阶段输出文件保存在 outputs 目录，后续阶段直接读取 |
