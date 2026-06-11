# Shared Skills — 跨 Agent 共享模块

## 用途

将多个 agent 的 SKILL.md 中重复出现的逻辑提取为共享模块，遵循高内聚低耦合原则。

## 目录

| 模块 | 内容 | 使用方 |
|------|------|--------|
| `constraint-rules.md` | 通用约束规则 | spec / tuning / optimizer |
| `missing-info-handling.md` | 缺失信息处理策略 | spec / tuning / optimizer |
| `output-section-framework.md` | 输出文档章节结构规范 | spec / tuning / optimizer |
| `self-check-list.md` | 通用输出前自检项 | spec / tuning / optimizer |
| `checklist-interaction.md` | Checklist 范式交互流程 | tuning / optimizer |

## 使用方式

在 SKILL.md 中引用共享模块：

```markdown
> 参考 [共享约束规则](../../shared/skills/constraint-rules.md) 中的通用约束。
```

高内聚逻辑保留在各自的 SKILL.md 中（如 spec 的输出模板、tuning 的策略参考表、optimizer 的诊断框架）。
