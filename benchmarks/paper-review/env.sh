#!/usr/bin/env bash
# benchmarks/paper-review/env.sh
# Stages the paper-review seed QA and the FedAux fixture paper into the
# container so the paper-review sub-agent has both the prompts and the
# materials available when the agent runs.
set -euo pipefail

: "${BENCH_CONTAINER:?must be exported by env_setup.sh}"
: "${BENCH_MOUNT:?must be exported by env_setup.sh}"
: "${BENCH_RUN_ID:=local}"

HERE="$(cd "$(dirname "$0")" && pwd)"
QA_SRC="${HERE}/qa.jsonl"
MATERIALS_SRC="${HERE}/materials"
[[ -f "${QA_SRC}" ]] || { echo "missing ${QA_SRC} (run build_qa.py first)" >&2; exit 1; }

log() { printf '\n[paper-review.env] %s\n' "$*"; }

# Bring up a fresh openclaw-bench container for this benchmark so fixtures
# and runtime state from a previous benchmark cannot leak in.
if [[ -f "${BENCH_ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  . "${BENCH_ENV_FILE}"
  bench_force_recreate
fi

log "staging qa.jsonl"
docker exec "${BENCH_CONTAINER}" mkdir -p \
  "${BENCH_MOUNT}/workspace-paper-review/bench-fixtures"
docker cp "${QA_SRC}" "${BENCH_CONTAINER}:${BENCH_MOUNT}/workspace-paper-review/bench-fixtures/qa.jsonl"

if [[ -d "${MATERIALS_SRC}" ]]; then
  log "staging materials (${MATERIALS_SRC})"
  docker exec "${BENCH_CONTAINER}" mkdir -p \
    "${BENCH_MOUNT}/workspace-paper-review/bench-fixtures/materials"
  tar -C "${MATERIALS_SRC}" -cf - . | \
    docker cp - "${CONTAINER:-${BENCH_CONTAINER}}:${BENCH_MOUNT}/workspace-paper-review/bench-fixtures/materials/" \
    || docker exec "${BENCH_CONTAINER}" bash -lc \
        "rm -rf ${BENCH_MOUNT}/workspace-paper-review/bench-fixtures/materials && mkdir -p ${BENCH_MOUNT}/workspace-paper-review/bench-fixtures/materials"
  for f in "${MATERIALS_SRC}"/*; do
    [[ -f "$f" ]] || continue
    docker cp "$f" "${BENCH_CONTAINER}:${BENCH_MOUNT}/workspace-paper-review/bench-fixtures/materials/$(basename "$f")"
  done
fi

log "ensuring output dir"
docker exec "${BENCH_CONTAINER}" mkdir -p \
  "${BENCH_MOUNT}/workspace-paper-review/outputs/bench-${BENCH_RUN_ID}"

# ---------------------------------------------------------------------------
# Wiki import: call main agent to import the MD materials into the wiki.
# The agent must confirm "导入成功"; otherwise we write a failure marker
# that metrics.py picks up and the benchmark scores 0.
# ---------------------------------------------------------------------------

# Clean stale marker from a previous run
rm -f "${HERE}/.wiki-import-failed"

log "staging MD materials into autoresearch inbox"
WIKI_INBOX="${BENCH_MOUNT}/workspace-autoresearch/raw/inbox/bench-${BENCH_RUN_ID}"
docker exec "${BENCH_CONTAINER}" mkdir -p "${WIKI_INBOX}"
for f in "${MATERIALS_SRC}"/*.md; do
  [[ -f "$f" ]] || continue
  docker cp "$f" "${BENCH_CONTAINER}:${WIKI_INBOX}/$(basename "$f")"
done

log "calling main agent to import materials into wiki"
IMPORT_SESSION="wiki-import-${BENCH_RUN_ID}-$$"
IMPORT_PROMPT=$'请将以下两份论文材料导入 wiki。\n\n材料位于 workspace-autoresearch/raw/inbox/bench-'"${BENCH_RUN_ID}"$'/ 目录下：\n1. 16556_Personalized_Subgraph_Fe.md — FedAux (Personalized Subgraph Federated Learning) 论文全文\n2. fedaux_experiment_deep_extraction.md — FedAux 实验提取文档\n\n请使用 autoresearch 子 agent 的 ingest 流程将这两份材料导入 wiki。\n\n完成后请逐个文件汇报导入状态：\n- 成功则回复「导入成功」并列出 wiki 页面路径\n- 失败则回复「导入失败」并说明原因'

IMPORT_RAW=$(docker exec -i \
  -e "MINIMAX_API_KEY" -e "MINIMAX_BASE_URL" \
  "${BENCH_CONTAINER}" openclaw agent \
  --agent main \
  --message "${IMPORT_PROMPT}" \
  --json --local \
  --session-key "${IMPORT_SESSION}" \
  --timeout 600 \
  2>/dev/null) || IMPORT_RAW=""

# Extract agent text from JSON payloads
IMPORT_TEXT=$(printf '%s' "${IMPORT_RAW}" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    texts = []
    for key_path in [('payloads',), ('result', 'payloads')]:
        d = data
        for k in key_path:
            d = d.get(k, {}) if isinstance(d, dict) else {}
        if isinstance(d, list):
            texts.extend(p.get('text','') for p in d if isinstance(p, dict) and p.get('text'))
    out = '\n'.join(t for t in texts if t)
    if out.strip():
        print(out)
except Exception:
    pass
" 2>/dev/null) || IMPORT_TEXT=""

if [[ -n "${IMPORT_TEXT}" ]] && echo "${IMPORT_TEXT}" | grep -q "导入成功"; then
  log "wiki import succeeded"
else
  log "FATAL: wiki import failed — agent did not confirm success"
  touch "${HERE}/.wiki-import-failed"
  log "failure marker written; benchmark will score 0"
fi

log "env ready"
