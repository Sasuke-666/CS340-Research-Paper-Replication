#!/usr/bin/env python3
"""Audit a registered fresh-host comparison acceptance batch without rerunning it."""
import argparse
import json
from pathlib import Path

import summarize_comparison as audit


IMAGE = "wcventure/period@sha256:8f47d8b9148f2db579627842026e722d0f205ddeab13e70ee41a8df3dbd59fbc"
METHODS = {"period", "author_serialized_abi16"}


def assess(batch, summary, cases, repeats, timeout):
    """Add execution-completeness requirements to the scientific integrity audit."""
    batch = Path(batch)
    problems = list(summary["integrity_errors"])
    if not (batch / "archive_manifest.json").is_file():
        problems.append("Missing outer archive manifest")
    expected = len(cases) * repeats * 2
    counts = summary["denominators"]
    for field in ("comparison_attempts", "comparison_complete", "comparison_eligible"):
        if counts[field] != expected:
            problems.append("{}: expected {}, observed {}".format(field, expected, counts[field]))
    groups = summary["groups"]
    expected_groups = {(case, method) for case in cases for method in METHODS}
    if {(row["case"], row["method"]) for row in groups} != expected_groups:
        problems.append("Unexpected case/method groups")
    for row in groups:
        if row["eligible_n"] != repeats:
            problems.append(row["case"] + "/" + row["method"] + ": incomplete eligible sample")
    for row in summary["trials"]:
        if row["phase"] == "comparison" and (row["inner_timeouts"] != 0 or row["schedules"] >= 10000):
            problems.append(row["case"] + "/" + row["log"] + ": inner timeout or schedule-budget truncation")
    pairs = summary["paired_comparisons"]
    if len(pairs) != len(cases) or any(row["n_complete_pairs"] != repeats for row in pairs):
        problems.append("Incomplete within-case method pairs")
    diagnostics = [row for row in summary["trials"] if row["phase"] == "diagnostic"]
    expected_diagnostics = 40 if "reorder_3" in cases else 0
    if len(diagnostics) != expected_diagnostics or any(not row["eligible"] for row in diagnostics):
        problems.append("Incomplete diagnostic process observations")
    for case in cases:
        directory = batch / case
        if not directory.is_dir():
            problems.append(case + ": missing case evidence directory")
            continue
        for name, value in (("upstream_commit.txt", audit.PIN), ("image_digest.txt", IMAGE),
                            ("container_exit_code.txt", "0")):
            path = directory / name
            if not path.is_file() or path.read_text(encoding="utf-8").strip() != value:
                problems.append(case + ": unexpected or absent " + name)
        for name in ("versions.txt", "image_inspect.json", "instrumentation_build.txt"):
            path = directory / name
            if not path.is_file() or path.stat().st_size == 0:
                problems.append(case + ": missing build/version provenance " + name)
        env_path, records_path = directory / "environment.json", directory / "records.json"
        if not env_path.is_file() or not records_path.is_file():
            problems.append(case + ": missing environment or records")
            continue
        environment = json.loads(env_path.read_text(encoding="utf-8"))
        settings = environment.get("comparison_settings", {})
        expected_settings = {"repetitions_per_method": repeats, "outer_timeout_seconds": timeout,
                             "depth": 3, "schedule_budget": 10000}
        if settings != expected_settings:
            problems.append(case + ": environment settings differ from acceptance protocol")
        records = json.loads(records_path.read_text(encoding="utf-8"))
        builds = [row for row in records if row.get("phase") == "build"]
        if len(builds) != 1 or any(row.get("exit_code") != 0 or row.get("timed_out") is not False for row in builds):
            problems.append(case + ": benchmark build did not complete successfully")
        if any(row.get("timeout_seconds") != timeout for row in records if row.get("phase") == "comparison"):
            problems.append(case + ": per-invocation watchdog differs from protocol")
    return {"schema_version": 1, "scope": "Fresh-host engineering acceptance; separate from historical estimates",
            "batch": batch.name, "cases": list(cases), "repeats_per_method": repeats,
            "outer_timeout_seconds": timeout, "accepted": not problems, "problems": problems,
            "comparison_counts": counts, "complete_pairs": sum(row["n_complete_pairs"] for row in pairs),
            "diagnostic_eligible": sum(row["eligible"] for row in diagnostics)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--cases", nargs="+", choices=audit.CASES, default=list(audit.CASES))
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=240)
    args = parser.parse_args()
    if args.repeats < 1 or args.timeout < 1 or len(args.cases) != len(set(args.cases)):
        parser.error("Use positive repeats/timeout and distinct cases")
    batch, output = args.batch.resolve(), args.output.resolve()
    if output == batch or batch in output.parents:
        parser.error("Keep derived output outside the raw archive")
    summary = audit.summarize_batch(batch, expected_repeats=args.repeats, expected_cases=args.cases)
    receipt = assess(batch, summary, args.cases, args.repeats, args.timeout)
    target = output / "acceptance.json"
    if args.check:
        audit.check_outputs(summary, output)
        if json.loads(target.read_text(encoding="utf-8")) != receipt:
            raise ValueError("Acceptance receipt differs from independently audited evidence")
    else:
        audit.write_outputs(summary, output)
        target.write_text(json.dumps(receipt, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    return 0 if receipt["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
