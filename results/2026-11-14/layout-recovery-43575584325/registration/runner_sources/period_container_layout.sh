#!/usr/bin/env bash
# Registered capacity-only comparison on an isolated disposable x86_64 host.
set -euo pipefail
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
case_name=${1:?case required}; out=${2:?fresh evidence directory required}
repetitions=${3:-10}; comparison_seconds=${4:-120}
[[ "$repetitions" =~ ^[1-9][0-9]*$ && "$comparison_seconds" =~ ^[1-9][0-9]*$ ]] || exit 2
case "$case_name" in account|lazy01) ;; *) exit 2;; esac
[[ $(uname -m) == x86_64 ]] || exit 2
command -v docker >/dev/null
[[ ! -e "$out" && ! -L "$out" ]] || { echo 'Output exists; refusing to overwrite'; exit 2; }
mkdir -p -- "$(dirname -- "$out")"; mkdir -- "$out"; out=$(cd "$out" && pwd -P)
work=$(mktemp -d)
finish() {
  code=$?
  trap - EXIT
  printf '%s\n' "$code" > "$out/wrapper_exit_code.txt"
  rm -rf -- "$work"
  exit "$code"
}
trap finish EXIT
pin=cb8deb9a176e5bb292d70d46557dd61dc0e98069
image=wcventure/period@sha256:8f47d8b9148f2db579627842026e722d0f205ddeab13e70ee41a8df3dbd59fbc
printf '%s\n' "$pin" > "$out/upstream_commit.txt"
printf '%s\n' "$image" > "$out/image_digest.txt"
git clone -q https://github.com/wcventure/PERIOD.git "$work/upstream" > "$out/source_clone.txt" 2>&1
git -C "$work/upstream" checkout -q --detach "$pin" >> "$out/source_clone.txt" 2>&1
[[ $(git -C "$work/upstream" rev-parse HEAD) == "$pin" ]]
timeout 420 docker pull "$image" > "$out/image_pull.txt" 2>&1
docker image inspect "$image" > "$out/image_inspect.json"
set +e
# Docker's default PID mode creates a private namespace; do not use host PID mode.
timeout 3000 docker run --rm --network none --ipc private --privileged --hostname period-layout \
 --env CS340_PRIVATE_STUDY_CONTAINER=1 \
 --mount "type=bind,src=$work/upstream,dst=/pinned,readonly" \
 --mount "type=bind,src=$root/scripts/run_period_layout.py,dst=/layout.py,readonly" \
 --mount "type=bind,src=$root/scripts/run_period_comparison.py,dst=/run_period_comparison.py,readonly" \
 --mount "type=bind,src=$root/scripts/run_period_pilot.py,dst=/run_period_pilot.py,readonly" \
 --mount "type=bind,src=$out,dst=/evidence" \
 "$image" bash -c 'set -euo pipefail; cp -a /pinned/. /workdir/PERIOD/; export ROOT_DIR=/workdir/PERIOD; export PATH="$ROOT_DIR/clang+llvm/bin:$PATH"; export LD_LIBRARY_PATH="$ROOT_DIR/clang+llvm/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"; cd "$ROOT_DIR"; { uname -a; clang --version; gcc --version; python3 --version; } > /evidence/versions.txt; cp /layout.py /evidence/measurement_runner.py; bash tool/install_staticAnalysis.sh > /evidence/instrumentation_build.txt 2>&1; python3 /layout.py --case "$1" --output /evidence --repetitions "$2" --comparison-timeout "$3"' bash "$case_name" "$repetitions" "$comparison_seconds" \
 > "$out/container_console.txt" 2>&1
code=$?; set -e
printf '%s\n' "$code" > "$out/container_exit_code.txt"
cat "$out/container_console.txt"
exit "$code"
