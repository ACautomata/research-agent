---
name: paper-audit
description: Quality-gate audit of a paper's analysis outputs (extract/critic/design/spec) for structure, boundaries, and cross-stage consistency. Runs the audit predicate. Triggers: 质量审计, paper-audit, 审计产出, 流水线审计, 检查这些产出.
---

# paper-audit — 分析链质量审计

## 概述

对一段论文分析链的产出（`extract` / `critic` / `design` / `spec`）做质量门审计：结构完整性、阶段边界、跨阶段一致性。运行 `audit` predicate（只读评估，不修改产出）。

**触发词**: "质量审计", "paper-audit", "审计产出", "流水线审计", "检查这些产出"

## 编排（reference predicate）

1. **`audit`** — 对 extract/critic/design/spec 产出做只读质量审计，产出审计报告（写回 wiki）

## 步骤

### Pre-check
确认 wiki 里存在待审计的产出（至少 `extract`；critic/design/spec 视链长度而定）。用 `wiki_search` 定位。

### Step 1: 运行 `audit`
对已有产出执行质量审计。`audit` 读取 wiki 产出，按 6 个维度（结构完整性、字段覆盖、阶段边界、缺失信息标注、证据强度分级、跨阶段一致性）评估，产出审计报告并 write back。完成后获取审计结论。

### Step 2: 汇报
呈现：必须修复项（阻塞下游）、建议改进项、总体可用性结论。附 wiki 路径。

## 输入

| Field | Required | Description |
|-------|----------|-------------|
| 论文（wiki page） | 是 | 待审计产出的论文 |
| 审计范围 | 否 | 默认全部已有阶段；可指定子集 |
