---
name: benchmark
description: Run a QA benchmark and score it through the judge subagent. Main runs each question itself (using its predicate skills), then spawns judge for quality-gated scoring. Triggers: run benchmark, run eval, 跑 benchmark, 评估, benchmark 评测, QA 测评.
---

# benchmark — benchmark 执行与评分

## 概述

执行 QA benchmark 并评分。main 自己跑每条 QA（按需用 predicate skill），候选答案收集后 spawn `judge` 子 agent 做质量门评分。**judge 是本系统唯一 spawn 的子 agent**，保持评分独立性。

**触发词**: "run benchmark", "run eval", "跑 benchmark", "评估", "benchmark 评测", "QA 测评"

## 编排（predicate + spawn judge）

1. main 自己执行每条 QA（按需用 `ingest`/`extract`/`critic` 等 predicate skill）
2. **spawn `judge`** — 独立质量门，对候选答案评分

## 步骤

### Step 1: 加载 benchmark 规格
读取 `benchmarks/<name>/qa.jsonl`。每条含 `question`、`gold_answer`(可选)、`must_contain`(可选)、`rubric`(可选)、`pass_threshold`(可选)。

### Step 2: 执行 QA
对每条 QA，main 按正常任务路由处理问题（按需用 predicate skill）。收集候选答案（最终 reply 文本）。

### Step 3: spawn `judge` 评分
根据 gold_answer、must_contain、rubric、pass_threshold 评估候选答案。judge 输出 VERDICT、SCORE (0.00-1.00)、rationale。FAIL 时提供 fix prompt。

### Step 4: 处理 judge 结论
- **PASS**：记录分数，计入 pass_rate
- **FAIL**：可选发回重试（每 QA 最多 1 次），重试后重新评分
- **NEEDS_HUMAN_REVIEW**：标记待人工关注

### Step 5: 汇总和报告
- `pass_rate` = 通过数 / 总数
- `avg_score` = 所有分数均值
- 输出 `bench-report.json`（顶层含 `pass_rate` 和 `avg_score`）
- 向用户呈现含逐条分解的摘要

## 输入

**命名 benchmark 运行**：benchmark 名称（匹配 `benchmarks/` 下目录）；可选 QA 索引（默认全部）。

**Ad-hoc 评估**：问题文本、候选答案、评估标准（gold_answer/must_contain/rubric/pass_threshold 任意组合）。

## 输出

`bench-report.json`:

```json
{
  "benchmark": "{name}",
  "pass_rate": 0.00,
  "avg_score": 0.00,
  "items": [
    {"index": 0, "verdict": "PASS|FAIL|NEEDS_HUMAN_REVIEW", "score": 0.00, "summary": "..."}
  ]
}
```
