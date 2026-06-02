#!/usr/bin/env bash
# benchmarks/autoresearch/env.sh
# Stages qa.jsonl into the autoresearch workspace. QAs in this benchmark
# test wiki fact-recall and cross-paper comparison against the existing
# wiki content (no fresh paper ingest).
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
log() { printf '\n[autoresearch.env] %s\n' "$*"; }

log "staging qa.jsonl"
docker exec "${BENCH_CONTAINER}" mkdir -p \
  "${BENCH_MOUNT}/workspace-autoresearch/bench-fixtures"
docker cp "${HERE}/qa.jsonl" "${BENCH_CONTAINER}:${BENCH_MOUNT}/workspace-autoresearch/bench-fixtures/qa.jsonl"


log "staging benchmark wiki fixtures"
docker exec "${BENCH_CONTAINER}" mkdir -p \
  "${BENCH_MOUNT}/workspace-autoresearch/wiki/domains/bench/papers"
docker exec "${BENCH_CONTAINER}" bash -lc "cat > ${BENCH_MOUNT}/workspace-autoresearch/wiki/domains/bench/papers/proco.md" <<'EOF'
# ProCo

ProCo measures cross-modal correspondence with Retrieval-based correspondence consistency and improves correspondence coverage for cross-modal learning.
EOF
docker exec "${BENCH_CONTAINER}" bash -lc "cat > ${BENCH_MOUNT}/workspace-autoresearch/wiki/domains/bench/papers/long-tail-distillation.md" <<'EOF'
# Long-tail distillation

Long-tailed distillation uses statistical alignment to address class imbalance.
EOF
docker exec "${BENCH_CONTAINER}" bash -lc "cat > ${BENCH_MOUNT}/workspace-autoresearch/wiki/domains/bench/papers/tafap.md" <<'EOF'
# TAFAP

TAFAP trajectory preserves optimization dynamics, while a snapshot can be diluted by later training steps.
EOF

log "ensuring scratch dir"
docker exec "${BENCH_CONTAINER}" mkdir -p \
  "${BENCH_MOUNT}/workspace-autoresearch/bench-${BENCH_RUN_ID}"

log "env ready (wiki content is whatever the repo already contains)"
