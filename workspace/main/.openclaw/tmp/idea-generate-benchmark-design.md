# Idea Generate Benchmark 设计文档

**负责人：** &lt;你的名字&gt;  
**日期：** 2026-06-03  
**版本：** v1.1（10 QAs · 7 题型 · 双路径评分）

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
└── self-test-report-template.md   ← 自测报告模板
```

**贡献者只需准备三样东西：**

| 文件 | 职责 | 本次交付 |
|---|---|---|
| `qa.jsonl` | 定义"怎么问 + 怎么判" | ✅ 10 条，覆盖 7 种题型 |
| `env.sh` | 定义运行环境（fixture 上传） | ✅ 已完成 |
| `metrics.py` | 定义评分计算（6 行模板） | ✅ 接入公共 runner |

---

## 三、QA 题型矩阵

共设计 **7 种题型**，覆盖研究 idea 生成的全部典型场景。**全部已实现，共 10 条 QA。**

| QA ID | 题型 | 输入特征 | 考察能力 | 评分 |
|---|---|---|---|---|
| QA-001 | paper-only | 两篇论文摘要（long-tailed distillation） | 从 limitation 锚定 idea + 指定 metric | rules |
| QA-002 | paper-plus-code | CLIP pipeline，只能改 scoring function | 代码硬约束下的低成本 idea | rules |
| QA-003 | failed-experiment | 蒸馏失败：准确率不升反降 | 基于失败现象诊断 + 生成改进方向 | rules |
| QA-004 | weak-evidence | 仅一段摘要，无具体数字 | 诚实标注 low-confidence，不夸大 | rules |
| QA-005 | constraint-heavy | 单 GPU / 8h / FedAvg baseline | 资源约束下的可行方案 | rules |
| QA-006 | cross-paper-contradiction | GNN oversmoothing：residual 是否真的有效？ | 识别 split protocol 是矛盾根因 | rules |
| QA-007 | transfer-driven | NLP few-shot → 医疗文本分类 | 评估迁移可行性，识别域差异 | **agent** ★ |
| QA-008 | paper-only | 模型压缩：蒸馏 vs 剪枝，<10MB 边缘部署 | 结合两种方法的优势 | rules |
| QA-009 | constraint-heavy | CPU-only, 2h, 10-task continual learning | 极强约束下的可行方案 | rules |
| QA-010 | cross-paper-contradiction | SSL 评估争议：排名完全颠倒 | 澄清"什么是好的评估协议" | **agent** ★ |

**题型覆盖率：7/7 ✔️**  
**QA 总数：10 条**  
**评分方式：rules × 8 · agent × 2**

---

## 四、定量评分体系

### 4.1 双路径评分

```
agent output ──┬── judge: "rules" ──→ 关键词覆盖率（快速、可复现）
               │
               └── judge: "agent" ──→ reviewer AI 综合评分（语义质量）
                                       └── 失败时自动降级为 rules 兜底
```

### 4.2 规则评分（8 条）

`judge_with_rules()` 从 `gold_answer.must_contain` 提取关键词列表，计算候选回答中的覆盖率：

- **评分公式**：score = covered / required
- **pass 条件**：score ≥ pass_threshold（默认 0.5）
- **适用场景**：结构完整性、硬约束合规、必填字段检查
- **优点**：零 API 开销、完全可复现、毫秒级

### 4.3 AI 评分（2 条）

`judge_with_agent()` 构造 rubric prompt → 发给 `reviewer` agent → 解析 JSON 评分：

```
你是 Reviewer agent。按 rubric 严格打分，只返回 JSON：
{"score": 0.6, "rationale": "..."}

QA: {question}
RUBRIC: {rubric}
CANDIDATE: {agent_output}
```

- **评分公式**：reviewer 返回 0–1 分 + rationale
- **适用场景**：需判断语义质量的维度（迁移可行性评估、协议设计质量）
- **兜底策略**：reviewer 不可用时自动降级为 rules 评分

### 4.4 六维 Rubric（每条 QA 均适用）

| 维度 | 0 分 | 1 分 | 2 分 |
|---|---|---|---|
| **evidence_grounding** | 未引用任何输入证据 | 引用了但泛泛 | 具体引用 limitation/insight |
| **constraint_following** | 违反核心约束 | 部分遵守 | 全部遵守且解释适配原因 |
| **idea_completeness** | 缺少 ≥3 个必填字段 | 缺 1–2 个 | 全部必填字段齐备 |
| **testability** | 无实验或不可执行 | 有实验但缺指标 | 含自变量/控制变量/预期 |
| **risk_honesty** | 弱证据假装确定 | 标了 risk 但笼统 | 具体 risk + 应对策略 |
| **output_usability** | 难以解析或保存 | 可读但缺关键信息 | 结构化、可直接传入后续流程 |

### 4.5 汇总指标

每条 QA 跑完后输出 `bench-report.json`，CI 自动汇总为 PR comment 中的两个核心指标：

| 指标 | 计算公式 |
|---|---|
| **pass_rate** | passed / total × 100%（每 QA 权重可配，默认 1.0） |
| **avg_score** | Σ(score × weight) / Σ(weight)（加权平均，0–1） |

---

## 五、CI 集成路径

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

## 六、当前状态与下一步

| 项目 | 状态 |
|---|---|
| benchmark-spec.md（7 种题型定义） | ✅ |
| qa.jsonl（10 条 QA） | ✅ |
| seed-qa.md（设计稿） | ✅ |
| env.sh + metrics.py | ✅ |
| self-test-report | ⚠️ 模板完成，待填入实测数据 |
| 下一步 | 本地自测 10 条 QA → 填充报告 |
