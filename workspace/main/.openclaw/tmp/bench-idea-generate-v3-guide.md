# Idea-Generate Benchmark v3.0 变更说明

> **PR:** [#53](https://github.com/ACautomata/research-agent/pull/53) — `bench(idea-generate): v3.0 — 50 QAs, 9 dimensions, 9 task types`
>
> **日期:** 2026-06-07
>
> **作者:** PBemmm

---

## 目录

1. [概述](#概述)
2. [文件变更清单](#文件变更清单)
3. [评估维度（5 → 9）](#评估维度5--9)
4. [任务类型（7 → 9）](#任务类型7--9)
5. [QA 数据集](#qa-数据集)
6. [Judge 模式](#judge-模式)
7. [维度 × 任务类型权重矩阵](#维度--任务类型权重矩阵)
8. [qa.jsonl 格式规范](#qajsonl-格式规范)
9. [已知问题与注意事项](#已知问题与注意事项)

---

## 概述

本轮将 idea-generate benchmark 从 v2.x 的 10 条种子 QA + 简单评分，重构为结构化的 50 条 QA × 9 维 × 9 任务类型的完整评测体系。

### 核心变化

| 项目 | v2.x | v3.0 |
|------|------|------|
| QA 数量 | 10 | 50 |
| 评估维度 | 5 | 9 |
| 任务类型 | 7 | 9 |
| Judge 模式 | 仅 rules | rules + agent |
| 评分依据 | 简单匹配 | `must_contain` + rubric + 维度打分 |

---

## 文件变更清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `benchmarks/idea-generate/qa.jsonl` | **重写** | 10 → 50 条，每条约 1.7 KB，总计 ~84 KB |
| `benchmarks/idea-generate/benchmark-spec.md` | **更新** | 2.7 KB → 11.3 KB，完整描述维度和评分体系 |
| `benchmarks/idea-generate/seed-qa.md` | **删除** | 上游种子记录，已被 qa.jsonl 取代 |
| `benchmarks/idea-generate/self-test-report-template.md` | **删除** | 旧 self-test 模板，不再需要 |
| `benchmarks/idea-generate/env.sh` | ~~误改~~ | 删除了 `bench_force_recreate` 调用，**需恢复为 main 原版** |
| `benchmarks/idea-generate/metrics.py` | **未改动** | 与 main 完全一致 |

> ⚠️ **CI 失败原因**：`env.sh` 误删了容器重建逻辑（`bench_force_recreate`），导致 CI matrix job 无法重新创建已被 setup job 销毁的 Docker 容器。用 main 上的原版 `env.sh` 替换即可修复。

---

## 评估维度（5 → 9）

### 新增 4 个维度

| # | 维度 | 来源 | 解释 |
|---|------|------|------|
| 5 | `falsifiability` 🆕 | good-question #4 | idea 是否说明何种结果会证伪它（can fail） |
| 6 | `importance` 🆕 | good-question #1, Heilmeier | 是否说清楚为什么值得做、谁会受益 |
| 7 | `rival_awareness` 🆕 | good-question #3, Platt | 是否识别竞争性解释，与其他方法区分 |
| 8 | `contribution_positioning` 🆕 | 原创 | 是否正确定位在论文谱系中的位置 |

### 完整 9 维

| # | 维度 | 含义 | 理论来源 |
|---|------|------|----------|
| 1 | `evidence_grounding` | 是否基于输入证据，不编造论文事实；证据 vs 推断标清 | good-question #7 (grounded) |
| 2 | `constraint_following` | 是否遵守代码/数据/计算条件和硬件约束 | good-question #5 (feasible) |
| 3 | `idea_completeness` | 是否包含必需段：机制、最小实验、指标、风险 | good-question #2 (specific) |
| 4 | `testability` | 是否有可执行的最小验证实验和可量化指标 | good-question #5, Platt 强推断 |
| 5 | `falsifiability` 🆕 | 是否说明何种结果会推翻该 idea | good-question #4 (can fail) |
| 6 | `importance` 🆕 | 是否说清价值所在、谁会受益；不只看 novelty | good-question #1, Heilmeier |
| 7 | `rival_awareness` 🆕 | 是否识别竞争性解释，区分自身与他人 | good-question #3, Platt |
| 8 | `contribution_positioning` 🆕 | 正确定位：向后追踪 related work、向前识别 follow-up、诚实评估真实增量 | 本项原创，结合 ARIS + academic-research-skills |
| 9 | `risk_honesty` | 是否诚实披露风险，对低证据推断标注置信度 | good-question #6, ARIS 失败模式 |

### `contribution_positioning` 的 4 个子项

| 子项 | 含义 |
|------|------|
| `backward_trace` | 是否正确引用了输入中的相关论文谱系 |
| `forward_scan` | 是否识别了前方的 follow-up work |
| `delta_honesty` | 在已有工作面前，是否诚实评估 idea 的真实增量 |
| `positioning` | 是否精准定位而非泛泛"combine A and B" |

---

## 任务类型（7 → 9）

### 新增 2 个类型

| 任务类型 🆕 | 含义 | 来源 |
|------------|------|------|
| `assumption-challenge` | 挑战论文或领域的默认假设 → 提出颠覆性 idea | Alvesson & Sandberg (2011) problematization 方法论 |
| `lineage-contextualized` | 在论文谱系中定位 idea（related work + follow-up），agent 须说明其 idea 在谱系中的精确位置和真实增量 | 对应 contribution_positioning 维度 |

### 完整 9 类

| # | task_type | 能力 | 关键约束 |
|---|-----------|------|----------|
| 1 | `paper-only` | 分析论文本体 → 生成 idea | 无代码，依靠文本证据，必须引用论文 limitation |
| 2 | `paper-plus-code` | 有代码边界的低实现 idea | 不能改 backbone / 重型架构，必须给出真实改进 |
| 3 | `failed-experiment-driven` | 从失败实验分析 → 改进方向 | 必须引用失败实验的具体数据，不能凭空提方向 |
| 4 | `weak-evidence` | 弱证据 → 验证假设 | 必须标注 low-confidence，不声称优于 SOTA，优先 baseline 复现 |
| 5 | `constraint-heavy` | 极端资源约束 → 可行方案 | 必须有时间/算力估算，体现 compute constraint |
| 6 | `cross-paper-contradiction` | 识别论文间矛盾 → 解决 idea | 必须明确指出矛盾焦点，提出 controlled re-evaluation |
| 7 | `transfer-driven` | 跨领域迁移评估 → 适配方案 | 必须真实评估可行性而非简单搬用，组件分析可复用性 |
| 8 | `assumption-challenge` 🆕 | 挑战默认假设 → 颠覆性 idea | 必须识别并挑战具体默认假设，不能只做 gap-spotting |
| 9 | `lineage-contextualized` 🆕 | 论文谱系中定位 idea → 贡献评估 | 给定该方向的相关论文谱系，agent 必须说明其 idea 在谱系中的精确位置和真实增量 |

---

## QA 数据集

### 统计

| 指标 | 数值 |
|------|------|
| 总 QA 数 | 50 |
| rules-judged | 29 (58%) |
| agent-judged | 21 (42%) |
| 平均 must_contain 数 | 12 个/QA |
| 覆盖 task_type | 9/9 |
| 覆盖维度 | 9/9 |
| 覆盖领域 | 8（Distillation, OOD Detection, Federated Learning, LLM Reasoning, Spectrum, Autonomous Driving, Cross-Domain, Meta） |

### 分布

| task_type | QA 数 | judge |
|-----------|:-----:|:-----:|
| paper-only | ~6 | rules |
| paper-plus-code | ~5 | agent |
| failed-experiment-driven | ~5 | agent |
| weak-evidence | ~5 | agent |
| constraint-heavy | ~5 | agent |
| cross-paper-contradiction | ~5 | rules |
| transfer-driven | ~5 | rules |
| assumption-challenge | ~7 | agent |
| lineage-contextualized | ~7 | agent/rules |

---

## Judge 模式

| 模式 | 适用场景 | 评分方式 | 使用的 QA |
|------|----------|----------|-----------|
| `rules` | 可量化检查（关键词匹配、维度覆盖） | `judge_with_rules`：检查 `gold_answer.must_contain` | 29 条 |
| `agent` | 需要语义判断的复杂维度 | 由 judge agent 按每个维度的 rubric 打分（0–1），`pass_threshold: 0.5` | 21 条 |

---

## 维度 × 任务类型权重矩阵

9×9 矩阵中，每个 task_type 只在与其相关的维度上加权（★ = 核心维度，★ = 加权维度，无标记 = 基础维度）：

| task_type | evidence | constraint | completeness | testability | falsifiability | importance | rival | contribution_positioning | risk |
|-----------|:--------:|:----------:|:------------:|:-----------:|:--------------:|:----------:|:-----:|:------------------------:|:----:|
| paper-only | ★★ | ★ | ★★ | ★ | ★ | ★ | ★ | ★ | ★ |
| paper-plus-code | ★ | ★★★ | ★★ | ★★ | ★ | ★ | ★ | ★ | ★ |
| failed-experiment | ★★★ | ★★ | ★★ | ★★ | ★ | ★ | ★ | ★ | ★★ |
| weak-evidence | ★★★ | ★ | ★ | ★ | ★ | ★ | ★ | ★ | ★★★ |
| constraint-heavy | ★ | ★★★ | ★★ | ★★★ | ★ | ★ | ★ | ★ | ★★ |
| cross-paper-contradiction | ★★ | ★ | ★★ | ★★ | ★ | ★★★ | ★★★ | ★★ | ★ |
| transfer-driven | ★★ | ★★ | ★★ | ★★ | ★ | ★★ | ★★ | ★★ | ★ |
| assumption-challenge | ★★ | ★ | ★★ | ★ | ★★★ | ★★★ | ★★★ | ★★ | ★★ |
| lineage-contextualized | ★★ | ★ | ★★ | ★★ | ★ | ★★★ | ★★ | ★★★ | ★★ |

---

## qa.jsonl 格式规范

每行一个 JSON，遵循 `benchmarks/_common/qa_schema.json`：

```json
{
  "qa_id": "QA-001",
  "agent": "main",
  "target_agent": "idea-generate",
  "skill": "idea-generate",
  "task_type": "paper-only",
  "input_material": "论文标题、摘要、或 wiki 路径...",
  "question": "具体的 prompt 文本...",
  "gold_answer": {
    "must_contain": ["关键词1", "关键词2", "..."],
    "fields": ["字段1", "字段2"]
  },
  "rubric": "评分标准描述...",
  "rubric_dimensions": [
    "evidence_grounding",
    "constraint_following",
    "idea_completeness",
    "testability",
    "falsifiability",
    "importance",
    "rival_awareness",
    "contribution_positioning",
    "risk_honesty"
  ],
  "pass_threshold": 0.5,
  "judge": "rules",
  "weight": 1.0
}
```

---

## 已知问题与注意事项

### env.sh 误改（阻塞）

`benchmarks/idea-generate/env.sh` 丢失了以下关键代码块：

```bash
# 缺失的代码 —— 必须恢复
if [[ -f "${BENCH_ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  . "${BENCH_ENV_FILE}"
  bench_force_recreate
fi
```

这段代码负责在 CI matrix job 中重建 Docker 容器（setup job 会先销毁容器，各 benchmark job 需要自己重建）。缺失导致 `Bench: idea-generate` 在所有 CI 运行中失败。

**修复方式：** 用 main 分支的原版 `env.sh` 替换当前版本。

### Node.js 20 弃用警告（非阻塞）

CI 中出现的 Node.js 20 deprecation warnings 来自 `actions/download-artifact@v4`、`actions/setup-python@v5` 等，是 GitHub Actions 平台级别的变更，不影响 benchmark 功能，可以后续统一升级。

---

## 与 v2.x 的向后兼容性

- `metrics.py` 未改动，评分逻辑保持一致
- `qa.jsonl` 格式兼容 `benchmarks/_common/qa_schema.json`
- 旧 `seed-qa.md` 内容已整合进新 `qa.jsonl`，无信息丢失
- 新增维度和任务类型对旧 QA 透明（旧 QA 在新维度上默认得基础分）
