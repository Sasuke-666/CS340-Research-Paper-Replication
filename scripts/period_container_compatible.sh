#!/usr/bin/env bash
# Run only on an isolated disposable x86_64 Linux host.
set -euo pipefail
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
case_name=${1:?case required}; out=${2:?fresh evidence directory required}
case "$case_name" in reorder_3|reorder_4|account|lazy01|twostage) ;; *) exit 2;; esac
[[ $(uname -m) == x86_64 ]] || exit 2
command -v docker >/dev/null
[[ ! -e "$out" && ! -L "$out" ]] || { echo 'Output exists'; exit 2; }
mkdir -p -- "$(dirname -- "$out")"; mkdir -- "$out"; out=$(cd "$out" && pwd -P)
work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
pin=cb8deb9a176e5bb292d70d46557dd61dc0e98069
image=wcventure/period@sha256:8f47d8b9148f2db579627842026e722d0f205ddeab13e70ee41a8df3dbd59fbc
git clone -q https://github.com/wcventure/PERIOD.git "$work/upstream"
git -C "$work/upstream" checkout -q --detach "$pin"
[[ $(git -C "$work/upstream" rev-parse HEAD) == "$pin" ]]
timeout 420 docker pull "$image" > "$out/image_pull.txt" 2>&1
docker image inspect "$image" > "$out/image_inspect.json"
printf '%s\n' "$pin" > "$out/upstream_commit.txt"
printf '%s\n' "$image" > "$out/image_digest.txt"
set +e
timeout 2200 docker run --rm --network none --privileged --hostname period-study \
 --mount "type=bind,src=$work/upstream,dst=/pinned,readonly" \
 --mount "type=bind,src=$root/scripts/run_period_compatible.py,dst=/compatible.py,readonly" \
 --mount "type=bind,src=$root/scripts/run_period_comparison.py,dst=/run_period_comparison.py,readonly" \
 --mount "type=bind,src=$root/scripts/run_period_pilot.py,dst=/run_period_pilot.py,readonly" \
 --mount "type=bind,src=$out,dst=/evidence" \
 "$image" bash -c 'set -euo pipefail; cp -a /pinned/. /workdir/PERIOD/; export ROOT_DIR=/workdir/PERIOD; export PATH="$ROOT_DIR/clang+llvm/bin:$PATH"; export LD_LIBRARY_PATH="$ROOT_DIR/clang+llvm/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"; cd "$ROOT_DIR"; { uname -a; clang --version; gcc --version; python3 --version; } > /evidence/versions.txt; grep -R -n "kpNumArray\|SHARE_ARRAY_SIZE" tool/staticAnalysis/DBDS-INSTRU --include="*.h" --include="*.cpp" --include="*.c" > /evidence/runtime_abi_source.txt || true; bash tool/install_staticAnalysis.sh > /evidence/instrumentation_build.txt 2>&1; python3 /compatible.py --case "$1" --output /evidence' bash "$case_name" \
 > "$out/container_console.txt" 2>&1
code=$?; set -e
printf '%s\n' "$code" > "$out/container_exit_code.txt"
cat "$out/container_console.txt"
exit "$code"
