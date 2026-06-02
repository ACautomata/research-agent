#!/usr/bin/env bash
# benchmarks/paper-ingest/env.sh
# Stages a tiny test paper into the autoresearch workspace's raw/inbox so the
# autoresearch agent can be told to ingest it.
set -euo pipefail

: "${BENCH_CONTAINER:?must be exported by env_setup.sh}"
: "${BENCH_MOUNT:?must be exported by env_setup.sh}"
: "${BENCH_RUN_ID:=local}"

HERE="$(cd "$(dirname "$0")" && pwd)"
log() { printf '\n[paper-ingest.env] %s\n' "$*"; }

log "staging inbox paper"
TARGET="${BENCH_MOUNT}/workspace-autoresearch/raw/inbox/bench-${BENCH_RUN_ID}"
docker exec "${BENCH_CONTAINER}" mkdir -p "${TARGET}"

# The benchmark carries a fixture string rather than a real PDF; the agent's
# wiki-organizer must handle text-only inputs gracefully.
FIXTURE='---
title: "BenchIngest: A Synthetic Note For Pipeline Testing"
authors: ["Bench Author"]
year: 2026
venue: "BenchConf"
arxiv: "0000.00000"
---
This is a synthetic paper fixture used by the CI benchmark to verify that
the autoresearch agent can ingest a new paper, produce a wiki page at
wiki/domains/bench/papers/benchingest.md, update wiki/index.md, and append
to wiki/log.md.
'
echo "${FIXTURE}" | docker exec -i "${BENCH_CONTAINER}" bash -lc \
  "cat > ${TARGET}/benchingest.md"

log "staging qa.jsonl"
docker exec "${BENCH_CONTAINER}" mkdir -p \
  "${BENCH_MOUNT}/workspace-autoresearch/bench-fixtures"
docker cp "${HERE}/qa.jsonl" "${BENCH_CONTAINER}:${BENCH_MOUNT}/workspace-autoresearch/bench-fixtures/qa.jsonl"

log "env ready"
