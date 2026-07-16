---
name: literature-query
description: Query and compare literature across papers in the wiki. Runs the curate predicate to search, synthesize, and compare insights with evidence levels. Triggers: 文献查询, 对比论文, 跨论文比较, wiki里有没有, literature query, compare papers, cross-paper.
---

# literature-query — 文献查询与跨论文比较

## 概述

在 wiki 现有内容上做文献查询和跨论文比较。运行 `curate` predicate（lint / compare / query 模式）。

**触发词**: "文献查询", "对比论文", "跨论文比较", "wiki里有没有", "查一下某篇论文", "literature query", "compare papers", "cross-paper"

## 编排（reference predicate）

1. **`curate`** — Wiki 策展、跨论文比较、文献查询（lint / compare / query）

## 步骤

### Step 1: 知识检索（main）
1. 用 `wiki_get` 读取 wiki 索引，定位相关页面。
2. 提取与用户查询相关的关键事实。
3. Wiki 不足时用 browser 补充（arXiv、Scholar），标注来源。

### Step 2: 运行 `curate`
在指定范围内执行查询（`query_type: lint | compare | query`）。把目标论文/关键词、wiki 路径、用户原始问题、已读 wiki 关键事实、网络补充来源传给 `curate`。`curate` 产出引用 `page_id`、标注 `evidence_level`、矛盾点明确标出的结果。

### Step 3: 汇报
向用户呈现结果，附 page paths 和 evidence_level 标签。

## 输入

| Field | Required | Description |
|-------|----------|-------------|
| query | 是 | 自然语言问题或比较请求 |
| papers | 否 | 论文标题、wiki 路径或关键词 |
| dimensions | 否 | 比较轴：methods, datasets, metrics, results |

## 输出

- **query 模式**：结构化回答，带引用、证据等级、缺口
- **compare 模式**：对齐表格，每行带 evidence_level，矛盾标记
- **lint 模式**：Wiki 质量问题 dashboard，按类型分组，带修复建议
