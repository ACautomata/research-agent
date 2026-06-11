---
name: tuning
description: 调参优化编排 skill。Main 将调参任务委托给 orchestrate，orchestrate 派发给 tuning agent。
---

# tuning

## 概述 / Overview

调参优化任务编排。当用户需要对算法代码进行超参优化时，main 将任务委托给 orchestrate，由 orchestrate 派发给 tuning agent。

**Trigger words**: "调参", "tuning", "超参数优化", "hyperparameter", "参数调优", "优化参数", "搜索参数"

## 应用场景 / Scenario

- 用户有代码仓库，需要对模型超参数进行系统优化
- 需要确定最优的搜索策略和搜索空间
- 需要在有限预算内找到最佳参数组合

## 编排步骤 / Orchestration Steps

### Step 1: Main 初步分析

Main 先了解用户需求，确认以下信息：
1. 目标代码仓库路径
2. 调参目标（精度/延迟/参数量）
3. 已有配置文件（如有）
4. 计算预算（如有）

### Step 2: 委托 orchestrate

```
sessions_spawn(
  agentId: "orchestrate",
  task: "调参优化任务",
  ...
)
```

### Step 3: Orchestrate 派发 tuning

Orchestrate 将任务派发给 tuning agent：
```
T1(tuning: 分析代码 → 生成调参方案)
```

### Step 4: Main 接收结果 + Judge 审查

- Main 接收 tuning 的调参方案
- 派发 judge 审查方案质量
- 向用户汇报

## 路由规则

| 用户意图 | 编排层 | Worker | Skill |
|---------|--------|--------|-------|
| 调参优化 | orchestrate | tuning | skills/tuning/ |
