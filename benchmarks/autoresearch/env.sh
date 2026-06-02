#!/usr/bin/env bash
# benchmarks/autoresearch/env.sh
# Stages qa.jsonl into the autoresearch workspace. QAs in this benchmark
# test wiki fact-recall and cross-paper comparison against the existing
# wiki content (no fresh paper ingest).
set -euo pipefail

: "${BENCH_CONTAINER:?must be exported by env_setup.sh}"
: "${BENCH_MOUNT:?must be exported by env_setup.sh}"
: "${BENCH_RUN_ID:=local}"

HERE="$(cd "$(dirname "$0")" && pwd)"
log() { printf '\n[autoresearch.env] %s\n' "$*"; }

log "staging qa.jsonl"
docker exec "${BENCH_CONTAINER}" mkdir -p \
  "${BENCH_MOUNT}/workspace-autoresearch/bench-fixtures"
docker cp "${HERE}/qa.jsonl" "${BENCH_CONTAINER}:${BENCH_MOUNT}/workspace-autoresearch/bench-fixtures/qa.jsonl"

log "ensuring scratch dir"
docker exec "${BENCH_CONTAINER}" mkdir -p \
  "${BENCH_MOUNT}/workspace-autoresearch/bench-${BENCH_RUN_ID}"

log "env ready (wiki content is whatever the repo already contains)"
