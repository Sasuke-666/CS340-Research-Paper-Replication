#!/usr/bin/env bash
# Execute only on a disposable x86_64 Linux machine with Docker access.
set -euo pipefail
repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
out=${1:?Usage: bash scripts/period_container_pilot.sh OUTPUT_DIRECTORY}
driver=${PERIOD_DRIVER:-run_period_pilot.py}
[[ "$driver" == run_period_pilot.py || "$driver" == run_period_followup.py ]] || { echo 'Unsupported experiment driver' >&2; exit 2; }
[[ $(uname -m) == x86_64 ]] || { echo 'Requires x86_64'; exit 2; }
command -v docker >/dev/null || { echo 'Docker is unavailable'; exit 2; }
# Create the final directory atomically. Existing directories, files and symlinks
# are refused before any logs can be overwritten, including an empty directory.
if [[ -e "$out" || -L "$out" ]]; then
  echo 'Output already exists; choose a new evidence directory.' >&2; exit 2
fi
mkdir -p -- "$(dirname -- "$out")"
mkdir -- "$out" || { echo 'Cannot create a fresh evidence directory.' >&2; exit 2; }
out=$(cd -- "$out" && pwd -P)
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
pin=cb8deb9a176e5bb292d70d46557dd61dc0e98069
git clone --quiet https://github.com/wcventure/PERIOD.git "$work/upstream"
git -C "$work/upstream" checkout --quiet --detach "$pin"
[[ $(git -C "$work/upstream" rev-parse HEAD) == "$pin" ]]
# Resolve once; execute the resolved digest, never a second mutable-tag lookup.
image=${PERIOD_IMAGE:-wcventure/period@sha256:8f47d8b9148f2db579627842026e722d0f205ddeab13e70ee41a8df3dbd59fbc}
timeout 420 docker pull "$image" 2>&1 | tee "$out/image_pull.txt"
digest=$(docker image inspect --format '{{index .RepoDigests 0}}' "$image")
[[ "$digest" == *@sha256:* ]] || { echo 'No immutable image digest'; exit 2; }
printf '%s\n' "$digest" > "$out/image_digest.txt"
docker image inspect "$digest" > "$out/image_inspect.json"
printf 'Upstream commit: %s\nStarted UTC: %s\n' "$pin" "$(date -u +%FT%TZ)" > "$out/provenance.txt"
uname -a >> "$out/provenance.txt"
cp "$work/upstream/LICENSE" "$out/upstream_LICENSE.txt"
# No credentials, private .git, host network, or Docker socket are mounted.
# Privileged mode is the authors' documented execution mode, limited to this
# ephemeral runner. Built dependencies come from the recorded image digest.
set +e
timeout 1000 docker run --rm --network none --privileged \
  --mount "type=bind,src=$work/upstream,dst=/pinned,readonly" \
  --mount "type=bind,src=$repo_root/scripts/$driver,dst=/pilot.py,readonly" \
  --mount "type=bind,src=$repo_root/scripts/run_period_pilot.py,dst=/run_period_pilot.py,readonly" \
  --mount "type=bind,src=$out,dst=/evidence" \
  "$digest" bash -c 'set -euo pipefail; cp -a /pinned/. /workdir/PERIOD/; export ROOT_DIR=/workdir/PERIOD; export PATH="$ROOT_DIR/clang+llvm/bin:$PATH"; export LD_LIBRARY_PATH="$ROOT_DIR/clang+llvm/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"; cd "$ROOT_DIR"; clang --version > /evidence/compiler.txt; bash tool/install_staticAnalysis.sh > /evidence/instrumentation_build.txt 2>&1; python3 /pilot.py --root "$ROOT_DIR" --output /evidence' \
  > "$out/container_console.txt" 2>&1
code=$?
set -e
printf '%s\n' "$code" > "$out/container_exit_code.txt"
# Logs contain the original output; keep failure evidence as well.
cat "$out/container_console.txt"
exit "$code"
