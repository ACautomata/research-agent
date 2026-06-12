# paper-pipeline

## 概述 / Overview

End-to-end deep paper analysis and validation. Orchestrates up to 7 subagents in a linear chain from ingestion to quality audit. Supports three execution modes:

- **full（默认）**: S1(ingest) → S1b(curate lint) → S2(extract) → S3(critic) → S4(design) → S5(spec) → S6(audit) — 新论文入库+全流程分析
- **post-ingest**: S2(extract) → S3(critic) → S4(design) → S5(spec) → S6(audit) — 跳过 S1，论文已在 wiki 中
- **ingest-only**: S1(ingest) → curate (lint) — 仅创建 wiki 条目，不深入分析

**Trigger words**: "完整分析", "full pipeline", "deep review", "S1-S6", "全流程分析", "paper pipeline", "端到端审稿", "分析这篇", "analyze this paper", "帮我看这篇论文"

**Auto-trigger signals（无需关键词）**: 任何 PDF 路径、arxiv URL、论文标题+作者引用、或附带论文的 GitHub 仓库链接。检测到这些信号时，默认走 **full 模式**，除非用户明确限定范围。

## 应用场景 / Scenario

Deep paper analysis and validation. User provides a paper (PDF/URL) and receives a complete chain: wiki entry, experiment extraction, problem critique, validation design, implementation spec, and quality audit.

## Subagent 调用链 / Agent Chain

| # | Agent | Stage | Role |
|---|-------|-------|------|
| 1 | **ingest** | S1 | Paper PDF ingestion, structured wiki page creation |
| 2 | **curate** | S1b | Quality lint on newly created wiki page（论文已存在时跳过） |
| 3 | **extract** | S2 | Deep experiment extraction from paper text |
| 4 | **critic** | S3 | Reviewer-perspective problem and claim analysis |
| 5 | **design** | S4 | Validation experiment design for identified problems |
| 6 | **spec** | S5 | Implementation spec and claude-code task prompt generation |
| 7 | **audit** | S6 | Cross-stage quality auditing and consistency check |

## 编排步骤 / Orchestration Steps

### Pre-pipeline: Mode Detection

Before launching any stage, determine the execution mode:

1. **Check wiki** using `wiki_search` for the paper (by title / arxiv ID / DOI)
2. **Determine mode:**
   - Paper **not in wiki** → default to `full` mode (S1 → S1b → S2 → S3 → S4 → S5 → S6)
   - Paper **already in wiki** → default to `post-ingest` mode (S2 → S3 → S4 → S5 → S6)，告知用户 "这篇论文已入库，从实验提取开始分析"
   - User **explicitly said** "入库" / "ingest only" / "只看摘要" / "大概看一眼" → `ingest-only` mode (S1 → curate)
   - User **explicitly said** "不入库" / "skip wiki" / "只分析" → `post-ingest` mode
3. **Record mode** in the task context passed to orchestrate

### Per-stage spawn pattern

Each stage follows the same pattern: spawn, wait, verify output, proceed.

**S1 — ingest** | Timeout: 900s (15 min)
- `sessions_spawn(agentId: "ingest", task: "将以下论文入库。标题：{title}。PDF路径：{path}。按 Capture→Extract→Create Paper Page→Update Index 流程执行。", mode: "run", runTimeoutSeconds: 900)`
- Output: Wiki page path, raw source path, evidence_level (inline reply)
- Gate: Wiki page >= 100 lines, at least one numeric result

**S1b — curate (post-ingest lint)** | Timeout: 600s (10 min)
- **仅当 S1 创建了新 wiki 页面时执行**（论文已存在时跳过此阶段）
- `sessions_spawn(agentId: "curate", task: "对新入库的论文页面执行质量检查。目标页面：{S1 output wiki path}。检查 frontmatter 完整性、evidence_level 准确性、Results 数值、孤立链接、index.md 条目正确性。输出 lint report。不修改 raw sources。", mode: "run", runTimeoutSeconds: 600)`
- Output: Lint report (pass/fail, findings)
- Gate: **非阻塞** — lint 发现的问题记录但不中断后续阶段。仅页面完全缺失时才 halt。

**S2 — extract** | Timeout: 1800s (30 min)
- `sessions_spawn(agentId: "extract", task: "对以下论文执行实验深度提取（S2）。标题：{title}。Wiki页面：{page_id}（使用 wiki_get 读取）。使用 paper-experiment-deep-extractor skill。在 reply 中直接返回完整 12 节实验提取文档（## 0–## 11）。", mode: "run", runTimeoutSeconds: 1800)`
- Input: Wiki path from S1, PDF as fallback
- Output: Inline reply containing full 12-section experiment extraction
- Gate: Reply contains all 12 sections (## 0–## 11) per extract skill template

**S3 — critic** | Timeout: 1200s (20 min)
- `sessions_spawn(agentId: "critic", task: "对以下论文执行审稿式问题分析（S3）。标题：{title}。Wiki页面：{page_id}（使用 wiki_get 读取）。S2 实验提取文档如下（从上游 agent 的 reply 中传递）：\n{S2 reply content}", mode: "run", runTimeoutSeconds: 1200)`
- Input: Wiki path, S2 experiment doc (inline)
- Output: Inline reply containing full problem analysis
- Gate: >= 1 concrete problem with evidence traceability

**S4 — design** | Timeout: 1200s (20 min)
- `sessions_spawn(agentId: "design", task: "对以下论文执行验证实验设计（S4）。标题：{title}。Wiki页面：{page_id}（使用 wiki_get 读取）。S3 问题分析文档如下（从上游 agent 的 reply 中传递）：\n{S3 reply content}。在 reply 中直接返回完整 10 节验证实验设计文档（## 0–## 9）", mode: "run", runTimeoutSeconds: 1200)`
- Input: Wiki path, S3 problem doc (inline)
- Output: Inline reply containing full validation experiment design
- Gate: Reply contains all 10 sections (## 0–## 9) per design skill template; each experiment maps to an S3 problem with expected results

**S5 — spec** | Timeout: 600s (10 min)
- `sessions_spawn(agentId: "spec", task: "生成 claude-code 任务提示词（S5）。代码仓库：{repo, optional}。S3 问题分析：\n{S3 reply content}\n\nS4 验证设计：\n{S4 reply content}", mode: "run", runTimeoutSeconds: 600)`
- Input: S3 + S4 outputs (inline), optional code repo
- Output: Inline reply containing full claude-code task prompt
- Gate: File-level specific, no unfilled placeholders

**S6 — audit** | Timeout: 600s (10 min)
- `sessions_spawn(agentId: "audit", task: "执行流水线质量审计（S6）。以下是 S2-S5 的完整产出内容：\n\n=== S2 实验提取 ===\n{S2 reply}\n=== S3 问题分析 ===\n{S3 reply}\n=== S4 验证设计 ===\n{S4 reply}\n=== S5 Codex 提示词 ===\n{S5 reply}", mode: "run", runTimeoutSeconds: 600)`
- Input: All S2-S5 inline reply content
- Output: Inline reply containing full audit report
- Gate: Covers all 6 audit dimensions; blocking issues are actionable

### Error Handling

- **Stage fails**: Log failure, inform user with stage + error detail. Offer retry or checkpoint resume.
- **S1b (curate lint) issues**: Record findings, continue pipeline. Only halt if page is completely missing.
- **S1→S2 chain broken**: If ingest failed but paper text is available (e.g., user pasted abstract), skip to S2 with available text.
- **Checkpoint resume**: Record completed stages **with the full inline Markdown content for each completed stage**, not only summaries or session keys. Store this checkpoint in the main session/memory or a wiki note that can be retrieved after the original session ends. When `Start stage` is S3 or later, verify that every prerequisite stage's full content is available; if any required upstream content is missing, ask the user to provide it or rerun the missing stage before continuing. Pass recovered completed output content inline and resume from the requested stage.
- **Quality gate failure**: Re-spawn same agent with previous output attached + fix instructions. One retry per stage max.

## 输入规范 / Input Specification

| Field | Required | Description |
|-------|----------|-------------|
| Paper title | Yes | Full paper title |
| PDF path or URL | Yes | Absolute path or accessible URL |
| Code repo | No | Local path or remote URL |
| User notes | No | Focus areas, constraints, questions |
| Start stage | No | Default S1; set to "S3" etc. for checkpoint resume |
| Execution mode | No | `full` (default) / `post-ingest` / `ingest-only`。由 mode detection 自动判定 |

## 输出规范 / Output Specification

Each stage returns its full output as inline reply text (Markdown). The orchestrator passes content between stages by embedding upstream reply text into downstream task parameters.

| Stage | Agent | Content |
|-------|-------|---------|
| S1 | ingest | Wiki page path, evidence_level |
| S1b | curate | Lint report (pass/fail, findings) |
| S2 | extract | Structured experiment extraction (12-section Markdown) |
| S3 | critic | Prioritized problem and claim analysis (8-section Markdown) |
| S4 | design | Validation experiment designs (10-section Markdown) |
| S5 | spec | Ready-to-use claude-code task prompt (Markdown) |
| S6 | audit | Cross-stage quality audit report (Markdown) |

User receives: top 3 problems, priority validation experiments, audit verdict, next steps.

## 示例 / Examples

### Example 1: Full pipeline (auto-detected)

User sends: "https://arxiv.org/abs/2401.01234 这篇论文关于对比学习"（无触发词）

1. Main 检测到 arXiv URL 信号 → 自动判断为 full mode。2. Check wiki: no entry. 3. Spawn **ingest** (S1). Wiki page created. 4. Spawn **curate** (S1b). Lint passes. 5. Spawn **extract** (S2). Receive full experiment extraction inline. 6. Spawn **critic** (S3) with S2 content embedded. 7. Spawn **design** (S4) with S3 content embedded. 8. Spawn **spec** (S5) with S3+S4 content embedded. 9. Spawn **audit** (S6) with S2-S5 content embedded. 10. Report summary.

### Example 1b: Paper already in wiki

User sends: "帮我看下 Attention Is All You Need 的实验设计"

1. Main detects paper reference. 2. Check wiki: entry exists at `wiki/papers/attention-is-all-you-need.md`. 3. Mode = `post-ingest`. 4. Tell user "这篇论文已入库，从实验提取开始分析". 5. Spawn **extract** (S2). Continue through S6.

### Example 2: Checkpoint resume

User: "从S3继续分析 attention-is-all-you-need"

1. Retrieve the checkpoint containing the full S2 inline Markdown (not just a summary or session key). 2. If full S2 content is missing, ask the user to paste it or rerun S2. 3. Spawn **critic** (S3) with wiki + full S2 content inline. 4. Continue S4-S6 normally, recording each full stage reply in the checkpoint.
