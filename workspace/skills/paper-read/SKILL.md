---
name: paper-read
description: Deeply read a paper in one continuous flow — ingest it into the wiki, then extract a structured 12-section experiment analysis. Triggers: 深读论文, 精读这篇, paper-read, deep read, 实验精读, 读透这篇论文.
---

# paper-read — 论文深读（入库 + 实验提取）

## 概述

一次性深读一篇论文：先运行 `ingest` predicate 入库，再运行 `extract` predicate 做深度实验提取。两个 predicate 都把完整产出写进 wiki；main 是唯一 context，连续传递，无 cross-agent handoff。

**触发词**: "深读论文", "精读这篇", "paper-read", "deep read", "实验精读", "读透这篇论文"

## 编排（reference predicate）

1. **`ingest`** — PDF → 结构化 wiki 论文页面
2. **`extract`** — 基于 wiki 页面 + 论文原文，产出 12 节实验提取文档（写回 wiki）

## 步骤

### Pre-check
用 `wiki_search` 检查论文是否已入库。如已入库且页面完整，可直接跳到 Step 2；否则先 Step 1。

### Step 1: 运行 `ingest`
将论文入库。完成后获取 wiki page path。若已入库，直接用已有 page。

### Step 2: 运行 `extract`
对入库论文执行实验深度提取。`extract` 会读取 wiki 页面（和 PDF fallback）产出 12 节文档并 write back 到 wiki。完成后获取实验提取文档内容。

### Step 3: 汇报
呈现实验提取的关键发现（主结果、消融、现象、证据充分性），附 wiki 路径。建议下一步：`critic`（问题分析）、`paper-validate`（验证设计）。

## 输入

| Field | Required | Description |
|-------|----------|-------------|
| PDF path or URL | 是 | 绝对路径或可访问 URL |
| Title | 推荐 | 缺省时从 PDF 提取 |
| Wiki page（已入库时） | 否 | 已有 page 可跳过 `ingest` |
