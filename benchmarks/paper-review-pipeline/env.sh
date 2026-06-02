#!/usr/bin/env bash
# benchmarks/paper-review-pipeline/env.sh
# Reuses the paper-review benchmark fixtures. The 5-stage pipeline is run
# against the same FedAux paper, so the agent just needs a clean output dir
# and a marker for which pipeline run id is active.
set -euo pipefail

RUNTIME_ENV="${BENCH_ENV_FILE:-$(cd "$(dirname "$0")/../.." && pwd)/.bench-runtime/bench-runtime-env.sh}"
if [[ -f "${RUNTIME_ENV}" ]]; then
  # shellcheck disable=SC1090
  . "${RUNTIME_ENV}"
fi

: "${BENCH_CONTAINER:?must be exported by env_setup.sh}"
: "${BENCH_MOUNT:?must be exported by env_setup.sh}"
: "${BENCH_RUN_ID:=local}"

HERE="$(cd "$(dirname "$0")" && pwd)"
log() { printf '\n[paper-review-pipeline.env] %s\n' "$*"; }

log "ensuring output dir for full pipeline"
docker exec "${BENCH_CONTAINER}" mkdir -p \
  "${BENCH_MOUNT}/workspace-paper-review/outputs/bench-${BENCH_RUN_ID}/pipeline"

log "staging qa.jsonl + materials"
docker exec "${BENCH_CONTAINER}" mkdir -p \
  "${BENCH_MOUNT}/workspace-paper-review/bench-fixtures"
docker cp "${HERE}/qa.jsonl" "${BENCH_CONTAINER}:${BENCH_MOUNT}/workspace-paper-review/bench-fixtures/pipeline-qa.jsonl"
for f in "${HERE}/../paper-review/materials/"*; do
  [[ -f "$f" ]] || continue
  docker exec "${BENCH_CONTAINER}" mkdir -p \
    "${BENCH_MOUNT}/workspace-paper-review/bench-fixtures/materials"
  docker cp "$f" "${BENCH_CONTAINER}:${BENCH_MOUNT}/workspace-paper-review/bench-fixtures/materials/$(basename "$f")"
done

log "env ready"
