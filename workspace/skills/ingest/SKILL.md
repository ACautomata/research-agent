---
name: ingest
description: Ingest a paper PDF into the wiki as an evidence-traceable paper page. Triggers: 入库, ingest paper, add to wiki, 文献笔记, 整理这篇论文.
---

# ingest — 论文 PDF → 结构化 wiki 页面

## Mission

将研究论文 PDF 转化为符合 wiki 规范的结构化论文页面，确保每条 claim 可追溯到原始来源。这是研究 wiki 的唯一入库入口。

## When to use

- 新论文 PDF 需要加入 wiki
- 用户请求"入库这篇论文""加入 wiki""整理这篇论文"
- `raw/inbox/` 中有待处理的论文

不要用于：文献查询、跨论文比较、wiki 质量审计（那是 `curate`）。

## 核心原则

- Raw sources 不可变；不修改 `raw/` 下原始文件
- Wiki 受证据约束，不发明不存在的知识；每条持久 claim 追溯到论文页章节和原始来源
- 区分证据等级：`abstract-only` / `skimmed` / `full-paper` / `reproduced`

## 语言

- Wiki 内容默认中文
- 保留原始论文标题、作者、DOI、arXiv、代码链接的原文
- Raw sources 保持原文不变

## 职责边界

**做：**

- 捕获 raw source（PDF），规范命名移入 `raw/sources/`
- 提取全文到 `raw/sources/`
- 按论文页模板创建结构化 wiki 页面
- 更新 wiki 索引和日志
- 产出通过 `wiki_apply` 写入 wiki

**不做：**

- 不回答文献查询 / 跨论文比较 / wiki 质量 lint（那是 `curate`）
- 不做实验深度提取（那是 `extract`）

## 输入

| Field | Required | Description |
|-------|----------|-------------|
| `pdf_path` | 是 | 源 PDF 路径（`raw/inbox/` 或 `raw/sources/`）或可访问 URL |
| `target_domain` | 推荐 | 论文所属领域子树 |
| `evidence_level` | 否 | 基于 PDF 访问程度（全文提取成功默认 `full-paper`）|

## 执行流程（Capture → Extract → Create → Index）

### 1. Capture
捕获 raw source，规范命名移入 `raw/sources/`。验证文件存在、可读、非空。失败重试一次。

### 2. Extract
提取全文到 `raw/sources/`。验证文本长度足够、包含论文结构。失败尝试替代方法一次。

### 3. Create Paper Page
用 `wiki_apply` 按论文页模板（见 `references/page-templates.md`）创建论文页面。填写全部通用 frontmatter 与论文专属 frontmatter（`paper.*`、`classification.*`、`evidence_level`）。包含全部 11 节：Citation, One-Sentence Contribution, Problem Setting, Method, Experiments, Results, Limitations, Reusable Claims, Connections, Open Questions, Provenance。

### 4. Update Index
用 `wiki_apply` 更新 wiki 索引和日志（追加式）。

## 完成门禁

- 一个 raw source 已捕获、一份全文已提取
- 一个论文页面已通过 wiki 工具创建（**>= 100 行**、有 `evidence_level`、Results 有具体数字）
- Wiki 索引和日志已更新

## 质量规则

遵循 `references/wiki-conventions.md` 的命名、索引、日志、链接规范。此外：

- 不编造 claim——每条 claim 追溯到论文页章节
- Experiments 必须包含数据集大小、baseline 名称、训练设置（架构/backbone/优化器/lr/batch/epoch/硬件）、评估协议、消融
- Results 必须为每个 main claim 包含具体数字（如 "AUROC 95.12% vs. MCM 86.05%"，不用"显著优于 baseline"）
- 缺失信息标注"原文未报告"
- 更新已有页面优先于创建重复页面
