#!/usr/bin/env bash
# benchmarks/arch-optimization/env.sh
set -euo pipefail
: "${BENCH_CONTAINER:?}"
: "${BENCH_MOUNT:?}"
: "${BENCH_RUN_ID:=local}"
HERE="$(cd "$(dirname "$0")" && pwd)"
. "${HERE}/_env_shared.sh" 2>/dev/null || true
