# paper-ingest

## 概述 / Overview

Two-stage pipeline to ingest a paper into the research wiki and verify quality: ingest creates the wiki page, curate lints for consistency.

**When used standalone** (user explicitly limits scope): Trigger words: "入库", "ingest paper", "add to wiki", "文献笔记", "整理这篇论文".

**When used as an auto-chain starter**: After successful ingest+curate, automatically chains into paper-pipeline S2-S6 for deep analysis — unless the user explicitly said "只看摘要" / "大概看一眼" / "只入库". This is the default behavior for all research materials without explicit scope limitation.

## 应用场景 / Scenario

Add a paper (PDF or URL) to the research wiki. Produces a verified, linted wiki entry with correct metadata and evidence levels.

## Subagent 调用链 / Agent Chain

1. **ingest** — PDF ingestion, text extraction, structured wiki page creation
2. **curate** — Quality linting, metadata verification, cross-page consistency check

## 编排步骤 / Orchestration Steps

### Pre-check (main agent)

1. Use `wiki_search` to check for existing entry. Skip if already present unless user requests re-ingest.
2. Validate user provided a PDF path or URL. If neither, ask.
3. Record paper metadata for downstream context.

### Step 1: Spawn ingest

```
sessions_spawn(
  agentId: "ingest",
  task: """将以下论文入库。

## 论文信息
- 标题：{title}
- PDF路径：{pdf_path_or_url}
- 用户备注：{user_notes, if any}

## 执行要求
按 Capture → Extract → Create Paper Page → Update Index 流程处理。
完成后汇报入库位置和 evidence_level。""",
  mode: "run",
  runTimeoutSeconds: 1800
)
```

Input: user-provided title, PDF/URL, optional notes. Output: wiki page path, evidence_level. Timeout: 1800s.

### Step 2: Spawn curate

After ingest completes, before reporting to user:

```
sessions_spawn(
  agentId: "curate",
  task: """对新入库页面执行质量检查。

## 目标页面
{ingest output: wiki page path}

## 检查范围
1. frontmatter 完整性（title, authors, year, venue, evidence_level）
2. evidence_level 与实际阅读深度一致
3. Results 是否包含具体数字
4. 孤立链接、矛盾 claim、index.md 条目正确性

输出 lint report。不修改 raw sources。""",
  mode: "run",
  runTimeoutSeconds: 600
)
```

Input: ingest inline reply. Output: lint report (pass/fail, findings). Timeout: 600s.

### Step 2b: Auto-chain into paper-pipeline (conditional)

After curate passes, check whether to auto-chain into the full paper analysis pipeline:

**Auto-chain conditions（任一满足即自动衔接）:**
- 原始任务上下文来自自动检测（用户未说触发词，只是发送了论文材料）
- 任务上下文包含 `mode: "unified"` 或 `chain_to_pipeline: true`
- 用户意图为"论文资料自动处理"

**Standalone conditions（不衔接，仅入库）:**
- 用户明确说 "入库" / "ingest only" / "只看摘要" / "大概看一眼" / "不要分析"
- 任务上下文明确 `mode: "ingest-only"`
- curate 发现 blocking issues 且 S1 需重做

**If auto-chaining:**
- DO NOT report ingest results to user yet
- Proceed to spawn paper-pipeline S2-S6 stages (extract → critic → design → spec → audit)
- Pass the wiki page path from S1 and the paper title as context
- The final pipeline report will include all stages

**If standalone:**
- Proceed to Step 3 (report ingest results to user with suggestions for next steps)

### Step 3: Report to user

**Standalone mode:**
- **Curate passes**: Report wiki path, evidence_level, key metadata. Suggest next steps (paper-review, idea-generate, cross-paper compare).
- **Curate finds blocking issues**: Report issues to user. Do not auto-re-spawn ingest.

**Auto-chain mode（pipeline continues）:**
- Record ingest results silently; the final pipeline report will include all stages.
- Only report to user after the full pipeline (S2-S6) completes.

### Error handling

| Stage | Failure | Action |
|-------|---------|--------|
| ingest | PDF unreadable | Ask user for alternative source |
| ingest | Extract insufficient | Suggest manual abstract entry |
| curate | Blocking lint issues | Report to user, await instruction |

### Quality gate

The curate stage is the quality gate for this skill — no separate `reviewer` spawn. For stricter review (benchmark scoring), spawn `reviewer` separately.

## 输入规范 / Input Specification

| Field | Required | Description |
|-------|----------|-------------|
| PDF path or URL | Yes | Absolute path or accessible URL |
| Title | Recommended | Extracted from PDF if omitted |
| User notes | Optional | Focus areas or special instructions |

## 输出规范 / Output Specification

User receives:

```
✅ 论文已入库并通过质量检查
📁 Wiki 页面：{path}
📊 Evidence level：{level}
🔍 Curate：{N} 项通过 / {M} 个建议
💡 下一步：paper-review / idea-generate / curate compare
```

## 示例 / Examples

**Example 1**: User: "帮我把 /workspace/raw/sources/2024-01-15-mhkc.pdf 入库"
→ 用户明确说"入库"，standalone mode。Pre-check (not in wiki) → spawn ingest (1800s) → page created → spawn curate (600s) → 0 blocking, 1 suggestion → report success, suggest next steps.

**Example 2**: User: "入库 https://arxiv.org/abs/2401.01234，重点看实验设计"
→ 用户同时说了"入库"和"重点看"——完整入库后根据"重点看实验设计"衔接 pipeline。Pre-check → spawn ingest with user note → page created → spawn curate → auto-chain into S2(extract) with focus on experiment design → continue S3-S6.

**Example 3**: User: "https://arxiv.org/abs/2401.01234 这篇论文怎么样"
→ 用户未说触发词，自动检测 arXiv URL 信号 → auto-chain mode。Pre-check → spawn ingest → spawn curate → auto-chain into S2-S6。完整 pipeline 结束后统一汇报。

**Example 4**: User: "只看摘要，帮我把这篇入库 /papers/new-paper.pdf"
→ 用户明确说"只看摘要" → standalone mode (ingest-only)。不衔接 pipeline。
