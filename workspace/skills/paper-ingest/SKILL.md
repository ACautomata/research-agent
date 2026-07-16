---
name: paper-ingest
description: Lightly ingest a paper into the wiki and verify quality. Runs the ingest predicate (create wiki page) then the curate predicate (lint for consistency). Triggers: 入库, ingest paper, add to wiki, 文献笔记, 整理这篇论文.
---

# paper-ingest — 论文入库 + 质量校验

## 概述

把一篇论文轻量入库到 wiki 并校验质量：先运行 `ingest` predicate 创建结构化论文页面，再运行 `curate` predicate 做 lint。两个 predicate 都把完整产出写进 wiki。

**触发词**: "入库", "ingest paper", "add to wiki", "文献笔记", "整理这篇论文"

## 编排（reference predicate）

1. **`ingest`** — PDF → 结构化 wiki 论文页面（11 节，证据可追溯）
2. **`curate`** — 对新入库页面做质量 lint（frontmatter、evidence_level、Results 数字、孤立链接、矛盾、index）

## 步骤

### Pre-check
1. 用 `wiki_search` 检查已有条目。如已存在且用户未要求重新入库则跳过。
2. 验证用户提供了 PDF 路径或 URL，否则询问。
3. 记录论文元数据供下游使用。

### Step 1: 运行 `ingest`
将论文入库。完成后获取入库位置（wiki page path）和 `evidence_level`。

### Step 2: 运行 `curate`（lint 模式）
对新入库页面执行质量检查。获取 lint report。

### Step 3: 汇报
- **Curate 通过**：汇报 wiki 路径、evidence_level、关键元数据。建议下一步（`paper-read` 深读、`literature-query` 跨论文比较、`brainstorm` 生成 idea）。
- **Curate 发现阻塞问题**：汇报问题，不自动重跑 `ingest`。

## 输入

| Field | Required | Description |
|-------|----------|-------------|
| PDF path or URL | 是 | 绝对路径或可访问 URL |
| Title | 推荐 | 缺省时从 PDF 提取 |
| User notes | 否 | 关注区域或特殊指令 |
