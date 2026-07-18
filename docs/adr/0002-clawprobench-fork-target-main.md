---
status: accepted
---

# 用 ClawProBench fork 替换自搓 benchmark，门控 main agent

## Context

main agent 是单 agent 自动化科研系统（见 [ADR-0001](./0001-single-main-agent-two-layer-skills.md)）。CI 要评的是**main agent 的产物**（`openclaw.json` + `workspace/skills/`），不是泛化 model leaderboard。旧自搓 `benchmarks/_common/` harness 已门控 main（`run_bench.py:7` "every benchmark task calls only the `main` agent"），但维护负担重、无统一 grading 生态。原样 ClawProBench（仓库 `ACautomata/ClawResearchBench`，产品名 ClawProBench）按 `--model` 新建 `ocb6-<model>-<uuid>` 临时 agent（`live_harness.py:1560`）且 `_replace_workspace_contents` 清空 workspace（`:674`）--评的是 model 能力而非 main agent，且会抹掉 main agent workspace。

## Decision

fork ClawProBench 到 `ACautomata/ClawResearchBench` 的 `fork/target-main` 分支（**不进 research-agent git 树**，CI `git clone` 钉定 commit SHA），改造 `harness/live_harness.py` + `run.py` 让它门控指定 agent（`--agent` 默认 `main`）并复用其 workspace：

- **跳过 `_create_agent`**（其首步 `openclaw agents delete <id> --force` 会删 target agent）--无条件安全硬约束，与隔离状态无关。
- **跳过 `_replace_workspace_contents` 整体清空**--改为把场景 `workspace_seed_dir` 的 fixture stage 进 main workspace 子目录（`materials/`/`outputs/`），不抹 main agent workspace。
- **门控 `_delete_agent`**--trial 间不删 main（`--cleanup-agents` 默认关 + runner `delete_agent` 门控）。
- `--model` 改 optional，从 `openclaw.json` 的 `agents.defaults.model.primary` 自动读 main 的 model（`minimax/MiniMax-M3`），仅记录用；result slug 用 `main`。**注意**：`benchmarks/_common/env_setup.sh` 会把 `agents.defaults.model.primary` patch 成 `LLM_MODEL`（未配 secret 时默认 `minimax/MiniMax-M2.7`），fork bootstrap 必须显式 pin `LLM_MODEL=minimax/MiniMax-M3`（或跳过该 patch），否则会静默评 M2.7 而非 main 的 M3。
- CI 在既有 `openclaw-bench` 容器内跑 `run.py`（state=`/home/node/.openclaw`=main agent 真实 state；`_uses_isolated_state()=False`，三个 seed 函数全 no-op，零污染--仅指 config/auth seed 不污染，不含 trial 间 workspace 状态）。**注意**：bench 容器默认 `OPENCLAW_PLUGINS_ENABLED=false`（`docker/docker-compose.bench.yml:57` / `env_setup.sh:495`），但 main 的 research skills 依赖 plugin 支撑的 wiki 工具（`wiki_apply`/`wiki_search`，见 ingest/design/paper-validate 等），fork bootstrap 必须显式启用所需 plugins（至少 memory-wiki），否则 `workspace_live` 场景无法创建/读取被 custom_check 打分的 wiki 产物。
- **trial 间隔离**：fork `main` 的 target-agent runner 在每个 trial 前快照 main workspace 与配置的 `memory-wiki` vault，并在 grading 后按基线恢复（若 vault 原本不存在则删除 trial 创建的 vault）。因此 `wiki_apply`、`materials/` 与声明的场景产物不会泄漏给 trial 2/3，`pass@3` / `pass^3` 保持独立 trial 的统计语义。research-agent CI 默认跟踪 fork `main`；fork 的变更必须先通过该隔离回归。
- 跑 **research 精选子集**：研究场景 `benchmark_status=incubating`、不在 active profile，`--benchmark-status all` 只是状态过滤器（让 incubating 场景可入选），单独用会跑远超预算的场景。fork 必须叠加显式 `--scenario` ID 列表 / research tag / 自定义 profile 才能限定到 ~12 场景（paper_review 主线 ~7 + idea_generate 主线 ~5）；trials=3 保 `pass@3` 语义；matrix 分片每 job ≤4 场景，`max-parallel:1`。
- PR 评论用**新渲染器**读 `result_main_<ts>.json`（FinalScore/pass@3/outcomes）+ **复用旧 `report_pr.py` 的 gh api upsert**（MARKER + base delta）。**注意**：`report_pr.py` 仅存在于 `benchmarks/_common/`，清理批次删 `_common` 前必须先把它迁移到本仓库 `scripts/`（或 fork 仓库），否则新渲染器失去 PR comment upsert 路径。
- **fork 跑通后删除 judge + 删旧 `benchmarks/_common/`**（收尾清理批次，独立 commit，避免未验证就动 main agent config）：改 `openclaw.json` + 删 `judge.py` + 更新 CLAUDE.md/CONTEXT.md；**同步清理 runtime 指令**--`workspace/AGENTS.md` 的 spawn-judge 段、`workspace/skills/benchmark/SKILL.md`（frontmatter `description` 与正文均让 main spawn judge 评分）改为确定性 custom_check 或删该 skill，否则会 spawn 已删的 judge agent；**先迁移 `report_pr.py`**（见上条）再删 `_common`。
- **本地与 CI 共用单一 bootstrap 脚本**（clone fork @ SHA + 起容器 + 容器内 `run.py` + 渲染）。

## Why

换用 ClawProBench 成熟确定性 grading 生态（`custom_checks/*.py` + `harness/scoring.py` + scenarios YAML + FinalScore/pass@3）替代自搓 harness；门控 main agent 是 fork 的必要修改（原样评 model 不评 main agent、且清空 workspace）；删 judge 因 ADR-0001「仅因 benchmark CI 强制要求保留」的前提被确定性 `custom_check` 取代，保留即孤儿、违背单 agent 收缩方向。

## Consequences

- **双仓库分工**：fork 代码改动在 `ClawResearchBench`/`fork/target-main`；CI workflow / CONTEXT.md / ADR / main agent config / 删 judge 在 research-agent。上游 ClawProBench 升级需手动 rebase fork 分支。
- **失去**旧 `benchmarks/_common/` 的 send->watch->logs 编排（被 ClawProBench `live_harness` 取代）；judge LLM 评判能力删除（确定性 `custom_check` 替代，若未来需 LLM 评判须重建 agent）。
- **local bootstrap 脚本**是 Q2=clone 的代价（research-agent 无 `scripts/` 目录，需新建）。
- 执行时机：fork 代码改造 -> CI 跑通 research 子集 -> 验证 FinalScore -> 删 judge + 旧 `benchmarks/_common/`（收尾批次，避免未验证就动 main agent config）。

## Considered Options

- **原样 ClawProBench（不 fork）**：评 model 不评 main agent，且清空 workspace，不可行。
- **新建独立 `ACautomata/ClawProBench-fork` 仓库**：与 Q2=clone 无额外收益，且需两仓库同步上游。
- **改本仓库 main**：fork 改动与上游 leaderboard/场景混杂，rebase 痛苦，本仓库不再是干净镜像。
- **保留 judge**：孤儿，与 ADR-0001「仅因 CI 保留」前提矛盾，留下困惑。
