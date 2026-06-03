# 委托模板

Main agent 在委托子 agent 时使用 sessions_spawn。以下为各场景的委托要点。

## paper-review

**场景**：论文分析、审稿、找问题、实验设计、Codex 提示词。

### 完整问题分析

目标 agent: paper-review / 超时: 3600 秒

task 消息应包含：

- **论文信息**：标题、Wiki 路径、PDF 路径（Wiki 缺失时必填）、代码仓库（可选）
- **执行要求**：按 S2→S5 顺序执行，输出保存到 outputs/ 目录。S3 问题发现须筛出具体、重要、紧迫的问题，结合 Wiki 和网络补充说明为什么值得处理。
- **上下文**：已读 Wiki 页面（路径列表）、Wiki 关键事实摘要、网络补充来源（arXiv/论文官网/基准/相关论文 URL）、这些来源对重要性/紧迫性的意义、需要回写/入库的新来源候选

完成后建议自动执行 S6 质量评估。

### 单阶段执行

目标 agent: paper-review / 超时: 1800 秒

传递用户原始意图和论文信息。paper-review 会自动判断是否需要补齐前置阶段。前置材料缺失时自动补齐。

### 断点续跑

目标 agent: paper-review / 超时: 3600 秒

标明已完成和待执行阶段，附上下文。阶段间自动衔接。

## autoresearch

**场景**：论文入库、Wiki 整理、知识更新。

目标 agent: autoresearch / 超时: 1800 秒

task 消息应包含：

- **论文信息**：标题、PDF 路径、用户备注
- **执行要求**：按 ingest 流程处理（捕获原文 → 提取元信息 → 创建 paper page → 更新 index.md 和 log.md）
- **结果汇报**：完成后汇报入库位置和 evidence_level

### Wiki 更新

当需要将子 agent 分析结果回写到已有 wiki 页面时：

- **目标页面**：wiki/domains/{domain}/papers/{slug}.md
- **追加内容**：子 agent 的关键发现摘要
- **新检索来源**：本轮新发现的相关论文/项目/基准
- **要求**：保留已有内容，仅追加或更新相关段落

## idea-generate

**场景**：科研 idea 生成。

目标 agent: idea-generate / 超时: 1800 秒

task 消息应包含：

- **用户要求**：领域、方向、约束（如：在联邦学习领域找研究空缺、基于某方法做改进）
- **锚定要求**：每个 idea 必须锚定到某篇论文或 wiki 中同一类型 2-4 篇论文共同暴露的具体痛点。说明：痛点证据、为什么值得现在做、拟解决机制、最小验证实验、预期指标变化和主要风险。
- **上下文**：相关论文、Wiki 路径或领域背景
- **Wiki 回写要求**：列出每个 anchor source、对应 idea ID、应回写的内容，以及本轮新发现需要入库的外部来源

## reviewer

**场景**：审查子 agent 产出质量。

目标 agent: reviewer / 超时: 600 秒 / context: isolated

task 消息应包含：

- **原始任务**：main agent 发给原 subagent 的完整 task
- **被审查对象**：agentId、sessionKey
- **subagent 最终回复**：保留原文
- **产出文件**：路径列表
- **已知约束**：用户要求、benchmark gold_answer/rubric/must_contain、阶段边界、wiki 回写要求等

### 修复提示

当 reviewer 判定 FAIL 时，使用 sessions_send 指向原 sessionKey，消息包含：

- reviewer 的 Fix prompt
- 要求保留已正确完成的部分
- 明确修复了哪些问题
- 给出更新后的完整结果或文件路径

修复后必须再次启动 reviewer 复审。
