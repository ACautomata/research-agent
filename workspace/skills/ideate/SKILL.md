---
name: ideate
description: Generate evidence-grounded research idea cards; each anchors to a named pain point. Triggers: 生成 idea, brainstorm ideas, research ideas, 研究思路, 研究方向, idea 生成.
---

# ideate — 研究 idea 生成

## Mission

将论文、wiki 上下文、实验记录和项目约束转化为有证据支撑、结构化、可比较、可验证的研究 idea card。

每个 idea 必须锚定到一篇具体论文 / wiki 页面，或一个 2–4 篇同类论文组成的、暴露具体痛点的集群。没有命名痛点的宽泛方向标签不是有效的 idea card。

## When to use

- 用户请求"brainstorm ideas""生成研究 idea""找研究方向"
- 需要从已有论文 / wiki 证据生成可验证的研究机会

不要用于：wiki 查询 / 比较（`curate`）、论文问题分析（`critic`）。

## 核心工作流

1. 将请求标准化为 Idea Generation Brief（参考 `references/brief-template.md`）
2. 从 wiki 页面、论文、实验记录构建上下文摘要
3. 提取每篇论文的上下文和局限性 / 未来工作信号
4. 将跨论文发现综合为机会桶
5. 生成 5–10 张候选 idea card
6. 去重，保留每个集群中最强的变体
7. 验证每张 card 的必填字段和证据链
8. 在 reply 中内联返回完整 idea card
9. 收到用户反馈后，产出版本化的跟进

## 输入（Idea Generation Brief）

- `research_topic`（必需，可从论文标题或用户上下文推断）
- `target_task`、`current_baseline`、`available_data`、`available_code`
- `available_compute`、`preferred_metrics`、`hard_constraints`
- `known_failures`、`desired_risk_level`

缺失字段保守推断并标注为假设。仅当没有研究主题、没有证据材料或硬约束无法解决时才追问。

生成前确认上下文充分性：至少有论文材料、wiki 页面或实验记录之一可用。否则向调用者报告证据不足，不强行生成空洞的通用 idea。

## 生成策略

使用 `references/generation-strategies.md`：gap-driven, contradiction-driven, transfer-driven, failure-driven, ablation-driven, metric-driven, constraint-driven。

## Hard Rules

1. 每个 idea 以证据为基础
2. 每个 idea 锚定到一篇具体论文 / wiki 页面或 2–4 篇同类论文集群；显式命名来源
3. `target_problem` 必须是具体痛点，不是宽泛研究领域或方法族标签
4. 每个 idea 包含最小验证实验
5. 每个 idea 命名至少一个预期变化的指标
6. 每个 idea 标识一个风险或失败模式
7. 弱支撑 idea 标记为 `low-confidence`
8. 优先 5–10 个高信号 idea，而非冗长嘈杂列表
9. 不声称论文说了什么除非出现在来源中
10. 准备 idea 供人工审查或下游评估；不在 skill 内宣布最终赢家

## 输出结构

最终 reply 中内联返回完整 recommended-ideas.md（详见 `references/output-spec.md`，paper demo 场景见 `references/paper-demo-output-spec.md`），附简短摘要：处理论文数、推荐 idea 数、wiki writeback candidates。

每张 Idea Card 遵循 `references/idea-card-template.md`：

```text
idea_id:
title:
one_sentence_hypothesis:
anchor_sources:
target_problem:
mechanism:
paper_insight_or_limitation:
evidence_chain:
minimum_experiment:
expected_metric_change:
implementation_scope:
risks:
confidence:
recommendation_reason:
wiki_writeback:
```

## 完成门禁

- 5–10 张 idea card，每张锚定到命名痛点、含最小验证实验 + 预期指标 + 风险
- 去重后保留每个集群最强变体
- 弱支撑 idea 标记 `low-confidence`
