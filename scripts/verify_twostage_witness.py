#!/usr/bin/env python3
"""Read archived Git blobs and classify the five fresh twostage replay transcripts."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from statistics import mean, stdev

BASE = "fd0d807f39a9d972dcd4929486d002f53ae4e4f3"
ARCHIVE = "results/2026-11-07/comparison-42381922637/twostage"
WITNESS = "witnesses/period/r01/000001_0000004_assertion-failed"
SIGNATURE = re.compile(r"twostage_bad\.c:48:.*funcB.*Assertion .0. failed")
ANSI = re.compile(r"\x1b\[[\d;]*m")


def blob(name):
    return subprocess.check_output(["git", "show", f"{BASE}:{ARCHIVE}/{name}"])


def archive_results():
    hashes = {e["path"]: e["sha256"] for e in json.loads(blob("manifest.json"))["files"]}

    def checked(name):
        data = blob(name)
        if hashlib.sha256(data).hexdigest() != hashes[name]:
            raise ValueError(f"Archive checksum differs: {name}")
        return data.decode()

    witness = checked(WITNESS)
    if not SIGNATURE.search(witness) or "Bug found!" not in witness:
        raise ValueError("Archived witness lacks the selected assertion")
    records = json.loads(checked("records.json"))
    sequence = None
    for method in ("period", "author_serialized_abi16"):
        trials = sorted((r for r in records if r.get("method") == method and
                         r["phase"] == "comparison"), key=lambda r: r["repeat"])
        if [r["repeat"] for r in trials] != list(range(1, 11)):
            raise ValueError("Incomplete archived repetition set")
        first, counts, seconds = [], [], []
        for r in trials:
            lines = ANSI.sub("", checked(r["log"])).splitlines()
            schedules, failures = [], []
            for line in lines:
                test = re.match(r"^test (\d+): (.+)$", line)
                if test:
                    if int(test[1]) != len(schedules) + 1:
                        raise ValueError("Discontinuous schedule IDs")
                    schedules.append(test[2])
                if "[Error Found]:" in line:
                    if "assertion failed" not in line:
                        raise ValueError("Unexpected error signature")
                    failures.append(len(schedules))
            if (len(schedules), failures[0], len(failures)) != (
                    r["schedules"], r["first_error"], r["buggy_schedules"]):
                raise ValueError(f"Recount disagrees with {r['log']}")
            if len(schedules) != 33 or r["exit_code"] or r["timed_out"] or "End Testing!" not in lines:
                raise ValueError(f"Incomplete run: {r['log']}")
            if r["repeat"] == 1:
                print(method, "r01, failing IDs:", failures, "schedule 4:", schedules[3])
                if sequence is None:
                    sequence = schedules
                else:
                    print("identical r01 printed schedules:", sum(x == y for x, y in zip(sequence, schedules)), "/ 33")
            first.append(failures[0])
            counts.append(len(failures))
            seconds.append(r["elapsed_seconds"])
        print(method, "first failures:", first, "failure counts:", counts)
        for label, values in (("first", first), ("failing", counts), ("seconds", seconds)):
            print(f"  {label}: {mean(values):.3f} +/- {stdev(values):.3f}")
    print("selected witness SHA-256:", hashes[WITNESS])


def replay_results(root):
    hits = 0
    for i in range(1, 6):
        raw = (root / f"replay-{i}.txt").read_bytes().decode()
        rc = int((root / f"replay-{i}.exit").read_text())
        text = ANSI.sub("", raw)
        _, marker, target = text.partition("Perform Reproduction!")
        if rc or not marker:
            result = "timeout" if rc in (124, 137) else "incomplete"
        elif SIGNATURE.search(target) and "Bug found!" in target:
            hits += 1
            result = "matching assertion"
        else:
            result = "no matching assertion observed"
        print(f"replay {i}: driver/wrapper exit={rc}, {result}")
    print(f"target assertion observed in {hits}/5 attempts")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay-dir", type=Path)
    args = parser.parse_args()
    archive_results()
    if args.replay_dir:
        replay_results(args.replay_dir)
