#!/usr/bin/env bash
# On a disposable x86_64 Linux host: bash scripts/replay_twostage.sh FRESH_OUTPUT_DIR
set -euo pipefail
pin=cb8deb9a176e5bb292d70d46557dd61dc0e98069
image=wcventure/period@sha256:8f47d8b9148f2db579627842026e722d0f205ddeab13e70ee41a8df3dbd59fbc
witness_hash=fc55bbedbf9a5469327c9ecbb84465bc1c000745882e2dac476739ce3568d262
if [[ ${1:-} == --inside ]]; then
    exec > /out/container.txt 2>&1
    set -x
    date -u
    cp -a /pin/. /workdir/PERIOD/
    cd /workdir/PERIOD
    export ROOT_DIR=$PWD
    export PATH="$ROOT_DIR/clang+llvm/bin:$PATH"
    export LD_LIBRARY_PATH="$ROOT_DIR/clang+llvm/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
    uname -a
    cat /etc/os-release
    clang --version
    gcc --version
    python3 --version
    getconf _NPROCESSORS_ONLN
    taskset -pc $$
    bash tool/install_staticAnalysis.sh
    cd evaluation/CS/twostage
    sha256sum twostage_bad.c /witness
    bash build.sh
    sha256sum ./twostage_bad "$ROOT_DIR/tool/DBDS/run_PDS.py" ConConfig.twostage_bad
    export PYTHONUNBUFFERED=1
    for i in 1 2 3 4 5; do
        log="/out/replay-$i.txt"
        date -u +%FT%TZ
        code=0
        timeout -k 5s 30s python3 "$ROOT_DIR/tool/DBDS/run_PDS.py" -y -r /witness ./twostage_bad > "$log" 2>&1 || code=$?
        printf '%s\n' "$code" > "/out/replay-$i.exit"
    done
    exit 0
fi
root=$(cd "$(dirname "$0")/.." && pwd)
out=${1:?supply a fresh output directory}
[[ ! -e "$out" ]] || { echo "Output path already exists" >&2; exit 2; }
mkdir -p -- "$out"
out=$(cd "$out" && pwd)
exec > >(tee "$out/host.txt") 2>&1
set -x
date -u
uname -a
[[ $(uname -s) == Linux && $(uname -m) == x86_64 ]]
git -C "$root" rev-parse HEAD
lscpu
docker version
archive="$root/results/2026-11-07/comparison-42381922637/twostage"
witness="$archive/witnesses/period/r01/000001_0000004_assertion-failed"
printf '%s  %s\n' "$witness_hash" "$witness" | sha256sum -c -
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
git -C "$work" init --quiet
git -C "$work" fetch --quiet --depth 1 https://github.com/wcventure/PERIOD.git "$pin"
git -C "$work" checkout --quiet --detach FETCH_HEAD
[[ $(git -C "$work" rev-parse HEAD) == "$pin" ]]
cmp "$archive/source/twostage_bad.c" "$work/evaluation/CS/twostage/twostage_bad.c"
timeout 420s docker pull "$image"
docker image inspect --format '{{.Id}} {{.RepoDigests}}' "$image"
timeout -k 10s 1200s docker run --rm --privileged --network none --hostname period-study \
    --mount "type=bind,src=$work,dst=/pin,readonly" \
    --mount "type=bind,src=$witness,dst=/witness,readonly" \
    --mount "type=bind,src=$root/scripts/replay_twostage.sh,dst=/replay.sh,readonly" \
    --mount "type=bind,src=$out,dst=/out" \
    "$image" bash /replay.sh --inside
