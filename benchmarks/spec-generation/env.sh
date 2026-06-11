#!/usr/bin/env bash
# benchmarks/spec-generation/env.sh
# Spec-generation benchmark — tests spec agent's ability to generate claude-code prompts.
set -euo pipefail

: "${BENCH_CONTAINER:?must be exported by env_setup.sh}"
: "${BENCH_MOUNT:?must be exported by env_setup.sh}"
: "${BENCH_RUN_ID:=local}"

HERE="$(cd "$(dirname "$0")" && pwd)"

# Delegate to shared env.
. "${HERE}/_env_shared.sh" 2>/dev/null || true
