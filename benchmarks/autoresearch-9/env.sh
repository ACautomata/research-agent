#!/usr/bin/env bash
# Shard of autoresearch benchmark.
set -euo pipefail

: "${BENCH_CONTAINER:?must be exported by env_setup.sh}"
: "${BENCH_MOUNT:?must be exported by env_setup.sh}"
: "${BENCH_RUN_ID:=local}"

HERE="$(cd "$(dirname "$0")" && pwd)"
PARENT="$(cd "${HERE}/../autoresearch" && pwd)"
# shellcheck disable=SC1090
. "${PARENT}/_env_shared.sh"
