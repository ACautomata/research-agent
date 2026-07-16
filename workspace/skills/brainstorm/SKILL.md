---
name: brainstorm
description: Generate evidence-grounded research ideas. Runs curate (build literature context) then ideate (structured idea cards anchored to named pain points). Triggers: brainstorm ideas, research ideas, generate ideas, research directions, find research gaps, 科研 idea, 研究思路, 头脑风暴.
---

# brainstorm — 研究 idea 生成

## 概述

基于 wiki 证据生成研究 idea：运行 `curate` predicate 准备精选文献上下文，再运行 `ideate` predicate 生成结构化 idea card。每个 idea 锚定到命名痛点，非空想。

**触发词**: "brainstorm ideas", "research ideas", "generate ideas", "research directions", "find research gaps", "科研 idea", "研究思路", "头脑风暴"

## 编排（reference predicate）

1. **`curate`** — Wiki 策展、跨论文比较，为 idea 生成准备精选上下文
2. **`ideate`** — 基于上下文生成证据支撑的 idea card

## 步骤

### Step 0: Pre-flight
用 `wiki_get` 读取 wiki 索引和相关领域页面。不足时 browser 搜索 arXiv/Scholar。收集 page ID、摘要、缺口组成上下文包。

### Step 1: 运行 `curate`
为 idea 生成准备精选上下文摘要：跨论文比较（方法、数据集、指标、evidence_level）、lint 报告（矛盾、缺口、过时 claim）、文献摘要（局限性、未来工作信号、未验证 claim）、缺口列表（2-4 篇同类论文集群的具体痛点）。每个 claim 引用 page_id。

### Step 2: 运行 `ideate`
从精选上下文生成 idea card：5-10 张，每张锚定到论文或 2-4 篇论文集群并命名痛点。含痛点证据、why now、提议机制、最小验证实验、预期指标、风险。去重，弱 card 标 `low-confidence`。

### Step 3: 呈现和回写
1. 向用户呈现 idea 摘要表和详细 card。
2. 如有 wiki 回写候选，运行 `curate` 更新 wiki。
3. 建议下一步（跑实验、深挖、入库更多论文）。

## 输入

| Field | Required | Description |
|-------|----------|-------------|
| Domain / topic | 否 | idea 生成范围，缺省全部 wiki 论文 |
| Paper list | 否 | 指定论文（标题、wiki 路径、URL） |
| Constraints | 否 | 方法、数据集、问题、时间范围 |

最少需要 domain/topic 或至少一个论文引用。都没有则询问用户。

## 输出

1. **Idea 摘要表** 供快速浏览
2. **详细 idea card** 含完整证据链和验证计划
3. **Wiki 更新通知**
4. **下一步建议**
