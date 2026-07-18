---
status: accepted
---

# ClawProBench CI matrix 动态扫描 research 全部场景

## Context

[ADR-0002](./0002-clawprobench-fork-target-main.md) 落地时，`.github/workflows/clawprobench.yml` 的 `bench.strategy.matrix` 硬编码了 12 个 curated research scenario（paper_review 主线 7 + idea_generate 主线 5），每条还带一个手写 `timeout`。ADR-0002 原文要求「matrix 分片每 job ≤4 场景」，但实际实现是 **1 scenario = 1 job**（每 job 独立 runner VM + 独立容器，无法跨 job 共享），与「≤4 场景/分片」的措辞不符。

硬编码矩阵有两个维护痛点：

1. **新增/废弃场景需手改 workflow**：fork 在 `scenarios/research/` 下有 170 个 research scenario（全部 `benchmark_status=incubating` + `signal_source=workspace_live`，评 main agent 的 research 产物），但 CI 只跑手挑的 12 个，其余 158 个从不被门控。fork 上游加场景后，本仓库要同步改 YAML include 列表，容易遗漏。
2. **`BENCH_EXPECTED_SCENARIOS` 重复硬编码**：`aggregate` job 把同一份 12 个 id 列表又抄了一遍做覆盖检查（`report_clawprobench.py` warn-only），两处列表必须手动保持一致。

## Decision

把 `bench.strategy.matrix` 从硬编码 12 条 `include` 改为**动态扫描 fork 的 research 全部场景**，新增一个 `discover` job 在 `bench` 之前跑：

- **discover job**（`needs: setup`）：partial clone fork @ `CLAWPROBENCH_PIN`，`grep -rhoE '^id:[[:space:]]+\S+' scenarios/research/` 提取顶层 `id` 字段，`sort -u` 去重，输出三个 step outputs：
  - `matrix`：`{"scenario":["id1",...]}` JSON（bench 用 `fromJSON(...).scenario` 展开）。
  - `scenarios`：逗号分隔列表（aggregate 的 `BENCH_EXPECTED_SCENARIOS` 用，替代硬编码）。
  - `count`：场景数（bench 的 `if: count != '0'` 防御空 matrix）。
- **bench job**：`matrix.scenario: ${{ fromJSON(needs.discover.outputs.matrix).scenario }}`，`timeout-minutes: 60`（统一；fork scenario `timeout_seconds` 均 240–300s，trials=3 约 15min + 容器启动 ~10min，60min 足够，无需 per-scenario）。`workflow_dispatch` 单场景 override 从 bench 的 per-job skip 逻辑上移到 discover（matrix 收窄为单元素），`steps.sel` 仅保留 trials 解析。
- **aggregate job**：`BENCH_EXPECTED_SCENARIOS: ${{ needs.discover.outputs.scenarios }}`，`needs` 加 `discover`。渲染脚本 `report_clawprobench.py` 不改（已读 env，warn-only 覆盖检查对动态列表透明）。

### 为什么用 `grep ^id:` 而非 `run.py --list`

fork `harness/loader.py:200` `scenario_id=raw["id"]` 无变换，YAML 顶层 `id:` 就是 `--scenario` 接受的值。`grep` 零依赖、不起容器、几秒完成；`run.py --list` 需装 fork venv deps 且不输出 timeout。已本地实证：`grep -rhoE '^id:[[:space:]]+\S+' scenarios/research/ | sort -u` 在 pin `5b368ea` 下得到 170 个唯一 `research_` id，0 个异常。

### 安全模型（不变）

- `pull_request`（非 `pull_request_target`）：fork PR 不暴露 secrets，同仓 PR 作者可信。
- discover 与 bench 都用顶层 `env.CLAWPROBENCH_PIN`（fork commit trusted-by-pin，非 PR 可控；`run.py` 在容器内持 `LLM_API_KEY`）。
- `inputs.scenario`/`inputs.trials` 是 `workflow_dispatch`-only（admin-trusted），走 env 路由不内插进 `run:`。matrix 数据来自 fork @ pin 的 YAML，非 PR-body 注入面。

## Consequences

- **覆盖面 12 -> 170**：CI 现在门控 fork 的全部 research 场景。新增/废弃场景自动反映，无需改 workflow。
- **串行时长 ~2-3 天**：`max-parallel:1` 保持（省 LLM 配额优先于速度），170 ×~20min。`concurrency.cancel-in-progress: false`：全套件要跑数天，mid-run push 不能 cancel 回 job 1（否则活跃 PR 上永远跑不完），新 push 排队等当前 run 结束。trade-off：堆叠 push 可能积压多个 run 烧配额，可接受（优于跑不完）。
- **单点动态化**：matrix 与 `BENCH_EXPECTED_SCENARIOS` 同源于 discover，不再有两份手抄列表。
- **discover 成为新 fail-fast 点**：pin 无效或 `scenarios/research/` 消失时 discover 报错退出，不浪费 bench 配额。

## Considered Options

- **保持 curated 12 + 改为每 job ≤4 场景**：ADR-0002 原措辞。但 1:1（每 job 一场景）已是实际实现且更简单（单 job 不超时、artifact 名唯一），回退到多场景/job 反而引入分片边界维护。supersede ADR-0002 的「≤4 场景/分片」措辞。
- **放开 `max-parallel`**：170 并发会瞬间打爆 LLM 配额；用户明确选择保持串行。
- **动态 timeout（读 YAML `timeout_seconds`）**：fork 已有该字段，但 job-level `timeout-minutes` 需整数分钟、且 scenario 实际耗时远低于 60min，统一 60 比动态读更简单且无收益。

## Supersedes

- [ADR-0002](./0002-clawprobench-fork-target-main.md) 中「matrix 分片每 job ≤4 场景」与「curated ~12 场景」措辞：改为动态全量 research 170 + 1:1 matrix。ADR-0002 的其余决策（fork 门控 main agent、删 judge、确定性 custom_check）不受影响。
