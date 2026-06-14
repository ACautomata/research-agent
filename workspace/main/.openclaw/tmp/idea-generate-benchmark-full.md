# Idea Generate Benchmark 设计文档与实测报告

**负责人：** <你的名字>  
**日期：** 2026-06-03  
**版本：** v2.0 · 10 QA · 7 题型全覆盖 · 双路径评分

---

## 一、评测目标

定量评测 `idea-generate` agent 是否稳定产出满足四个硬约束的 research idea cards：

| # | 约束 | 度量方式 |
|---|---|---|
| ① | **有证据锚点** | idea 是否引用输入材料中的具体 limitation / insight（不编造） |
| ② | **可定量比较** | 每个 idea 是否包含具体 metric（如 FPR95、balanced accuracy） |
| ③ | **最小可验证** | 是否附带 minimum validation experiment（自变量 / 控制变量 / 预期结果） |
| ④ | **诚实标注风险** | weak evidence 是否标为 low-confidence，是否写出至少一个 risk |

---

## 二、组件结构

```
benchmarks/idea-generate/
├── benchmark-spec.md              ← 评测规约（题型定义、评分维度、自测流程）
├── seed-qa.md                     ← 10 条 QA 设计稿（详细版）
├── qa.jsonl                       ← CI 直接消费（每行一个 QA JSON）
├── env.sh                         ← Docker 环境准备（fixture 上传）
├── metrics.py                     ← 6 行 shim → 接入公共 run_bench.py
└── self-test-report.md            ← 实测报告（本次交付）
```

**贡献者只需准备三样东西：**

| 文件 | 职责 | 交付 |
|---|---|---|
| `qa.jsonl` | 定义"怎么问 + 怎么判" | ✅ 10 条，7 题型全覆盖 |
| `env.sh` | Docker 环境准备（fixture 上传） | ✅ 已完成 |
| `metrics.py` | 评分计算（6 行模板） | ✅ 接入公共 runner |

---

## 三、QA 题型矩阵

共设计 **7 种题型**，覆盖研究 idea 生成的全部典型场景，**共 10 条 QA**。

| QA ID | 题型 | 输入特征 | 考察能力 | 评分 |
|---|---|---|---|---|
| QA-001 | paper-only | 两篇论文摘要（long-tailed distillation） | 从 limitation 锚定 idea + 指定 metric | rules |
| QA-002 | paper-plus-code | CLIP pipeline，只能改 scoring function | 代码硬约束下的低成本 idea | rules |
| QA-003 | failed-experiment | 蒸馏失败：准确率不升反降 | 基于失败现象诊断 + 生成改进方向 | **agent** |
| QA-004 | weak-evidence | 仅一段摘要，无具体数字 | 诚实标注 low-confidence，不夸大 | **agent** |
| QA-005 | constraint-heavy | 单 GPU / 8h / FedAvg baseline | 资源约束下的可行方案 | rules |
| QA-006 | cross-paper-contradiction | GNN oversmoothing：residual 是否真的有效？ | 识别 split protocol 是矛盾根因 | rules |
| QA-007 | transfer-driven | NLP few-shot → 医疗文本分类 | 评估迁移可行性，识别域差异 | **agent** |
| QA-008 | paper-only | 模型压缩：蒸馏 vs 剪枝，<10MB 边缘部署 | 结合两种方法的优势 | rules |
| QA-009 | constraint-heavy | CPU-only, 2h, 10-task continual learning | 极强约束下的可行方案 | rules |
| QA-010 | cross-paper-contradiction | SSL 评估争议：排名完全颠倒 | 澄清"什么是好的评估协议" | rules |

**题型覆盖率：7/7 ✔️  ·  QA 总数：10  ·  评分方式：rules × 7 · agent × 3**

---

## 四、定量评分体系

### 4.1 双路径评分

```
agent output ──┬── judge: "rules" ──→ 关键词覆盖率（快速、可复现、零 API 开销）
               │
               └── judge: "agent" ──→ reviewer AI 综合评分（语义质量）
                                       └── 失败时自动降级为 rules 兜底
```

### 4.2 规则评分（7 条）

`judge_with_rules()` 从 `gold_answer.must_contain` 提取 10 个关键词，计算候选回答中的覆盖率。

- **评分公式**：score = covered / 10
- **pass 条件**：score ≥ 0.5
- **关键词粒度**：全部为具体词（方法名、约束术语、指标名），避免通用词

### 4.3 AI 评分（3 条）

`judge_with_agent()` 构造 rubric prompt → 发给 `reviewer` agent → 解析 `{"score": 0.6, "rationale": "..."}`。

**每条的 rubric 包含加分项和扣分项：**

| QA | 典型扣分 |
|---|---|
| QA-003 | 提出改模型结构 → **0 分**；risk 笼统 → −0.2；未给 metric 区间 → −0.1 |
| QA-004 | 声称 SOTA → **0 分**；未标 weak evidence → −0.3；Open Questions<3 → −0.1 |
| QA-007 | 简单套用原模板 → −0.3；未讨论长文本开销 → −0.2；未提 API 预算 → −0.1 |

### 4.4 六维 Rubric

| 维度 | 0 分 | 1 分 | 2 分 |
|---|---|---|---|
| **evidence_grounding** | 未引用任何输入证据 | 引用了但泛泛 | 具体引用 limitation/insight |
| **constraint_following** | 违反核心约束 | 部分遵守 | 全部遵守且解释适配原因 |
| **idea_completeness** | 缺少 ≥3 个必填字段 | 缺 1–2 个 | 全部必填字段齐备 |
| **testability** | 无实验或不可执行 | 有实验但缺指标 | 含自变量/控制变量/预期 |
| **risk_honesty** | 弱证据假装确定 | 标了 risk 但笼统 | 具体 risk + 应对策略 |
| **output_usability** | 难以解析或保存 | 可读但缺关键信息 | 结构化、可直接传入后续流程 |

### 4.5 汇总指标

| 指标 | 计算公式 |
|---|---|
| **pass_rate** | passed / total × 100%（每 QA 权重可配，默认 1.0） |
| **avg_score** | Σ(score × weight) / Σ(weight)（加权平均，0–1） |

---

## 五、实测结果

**测试环境：** Windows 10 · deepseek/deepseek-v4-pro · sandbox=off

| QA ID | 题型 | 评分 | 覆盖/关键词 | Score | 结果 | 说明 |
|---|---|---|---|---|---|---|
| QA-001 | paper-only | rules | 8/10 | **0.80** | ✅ PASS | 缺"majority class"、"distillation budget" |
| QA-002 | paper-plus-code | rules | — | — | ❌ SYS_ERR | EPERM 文件 rename 竞态（Windows） |
| QA-003 | failed-experiment | **agent** | 10/10 kw | **~0.85** | ✅ PASS | 引用失败实验数据，mix ratio 数值区间 |
| QA-004 | weak-evidence | **agent** | 10/10 kw | **~0.90** | ✅ PASS | 8 条 Open Questions，I-1 为 baseline 复现 |
| QA-005 | constraint-heavy | rules | 10/10 | **1.00** | ✅ PASS | 7 个 idea 各有时间/指标/代码估算 |
| QA-006 | cross-paper-contradiction | rules | 10/10 | **1.00** | ✅ PASS | 精准识别 split protocol 泄漏为根因 |
| QA-007 | transfer-driven | **agent** | 10/10 kw | **~0.85** | ✅ PASS | 三大组件均判断不可直接复用 |
| QA-008 | paper-only | rules | 9/10 | **0.90** | ✅ PASS | 缺"MobileNet"（用了 ARM Cortex/RPi4 替代） |
| QA-009 | constraint-heavy | rules | 10/10 | **1.00** | ✅ PASS | 每 idea 附带 CPU 时间分解表 |
| QA-010 | cross-paper-contradiction | rules | 10/10 | **1.00** | ✅ PASS | 识别 linear probing vs fine-tuning 排名反转 |

**汇总指标（排除系统错误的 QA-002）：**

| 指标 | 值 |
|---|---|
| 实测条目 | 9 |
| 通过 (pass) | 9（100%） |
| 平均分 (avg_score) | 0.92 |
| 分数区间 | 0.80 ~ 1.00（四级阶梯） |

### v1.0 vs v2.0 评分对比

v1.0 关键词为 5-7 个通用词，导致已测 4 条全满分（无区分度）。v2.0 升级为 10 个具体关键词 + 3 条改用 agent judge：

| QA ID | v1.0 Score | v2.0 Score | 变化说明 |
|---|---|---|---|
| QA-001 | 1.00 (5/5) | **0.80** (8/10) | 加具体词（trajectory matching 等）后区分度出现 |
| QA-002 | SYS_ERR | SYS_ERR | Windows EPERM，需 CI 环境重跑 |
| QA-003 | 1.00 (7/7 rules) | **~0.85** (agent) | 改用 agent，扣分项让评分更精细 |
| QA-004 | 1.00 (5/5 rules) | **~0.90** (agent) | 同等趋势 |
| QA-005 | 1.00 (6/6) | **1.00** (10/10) | 依然全中（agent 产出质量高） |

---

## 六、CI 集成路径

```
PR push → benchmark.yml 触发
  → docker compose up（隔离 openclaw-bench 容器）
  → rsync repo → 容器 /home/node/.openclaw
  → bash benchmarks/idea-generate/env.sh（上传 qa.jsonl + 创建输出目录）
  → python3 benchmarks/idea-generate/metrics.py
       → 逐条 QA: docker exec openclaw agent --agent main
           → main 识别 target_agent="idea-generate"
           → sessions_spawn → idea-generate 执行
           → judge 评分 → 写入 bench-report.json
  → report_pr.py → 更新 PR comment（pass_rate / avg_score / 失败项 Top 5）
```

---

## 七、当前状态与下一步

| 项目 | 状态 |
|---|---|
| benchmark-spec.md（7 种题型定义） | ✅ |
| qa.jsonl（10 条 QA，10 关键词/条） | ✅ |
| seed-qa.md（设计稿） | ✅ |
| env.sh + metrics.py | ✅ |
| self-test-report.md（v2.0 实测） | ✅ |
| 下一步 | QA-002 CI 环境重跑（Windows EPERM 待修复） |
| 下一步 | reviewer agent 正式复审 QA-003/004/007 的扣分项 |
