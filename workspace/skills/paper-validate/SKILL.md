---
name: paper-validate
description: Turn a paper's identified problems into executable validation — run design (validation experiments) then spec (claude-code task prompt). Requires critic's problem analysis already in the wiki. Triggers: 验证设计, paper-validate, 设计验证实验, 验证实验, 怎么验证这个 claim.
---

# paper-validate — 验证实验设计 + 实现规格

## 概述

把论文已识别的问题转成可执行的验证：运行 `design` predicate 设计验证实验，再运行 `spec` predicate 生成 claude-code 任务提示词。

**前置依赖**：需要 `critic` 的问题分析文档已在 wiki。`paper-validate` 不自动运行 `critic`（critic 是独立 predicate）。若 wiki 里没有 critic 产出，先运行 `critic`（或走完整分析链的 read→critic），再回来 `paper-validate`。

**触发词**: "验证设计", "paper-validate", "设计验证实验", "验证实验", "怎么验证这个 claim"

## 编排（reference predicate）

1. **`design`** — 基于 `critic` 问题分析，产出 10 节验证实验设计（写回 wiki）
2. **`spec`** — 基于 `design`，生成 claude-code 任务提示词（写回 wiki）

## 步骤

### Pre-check
用 `wiki_search` 检查 `critic` 问题分析文档是否已在 wiki。

- **缺失**：不自动运行 `critic`。先运行 `critic`（或完整分析链的 read→critic），再回来 `paper-validate`。
- **存在**：记录文档路径，继续。

### Step 1: 运行 `design`
基于 `critic` 问题分析产出验证实验设计。`design` 会读取 critic 文档 + wiki 页面，产出 10 节设计文档并 write back。完成后获取设计文档。

### Step 2: 运行 `spec`
基于 `design` 生成 claude-code 任务提示词。`spec` 读取 design（+ critic）文档产出任务提示词并归档到 wiki。完成后获取提示词内容。

### Step 3: 汇报
呈现优先验证实验、claude-code 任务提示词要点，附 wiki 路径。建议下一步：把 spec 提示词发给 claude-code 执行，或 `paper-audit` 审计整条链。

## 输入

| Field | Required | Description |
|-------|----------|-------------|
| 论文（wiki page） | 是 | 已入库的论文 |
| critic 问题分析（wiki） | 是（前置） | 必须已存在 |
| 代码仓库路径 | 否 | `spec` 生成时参考 |
