#!/usr/bin/env python3
"""Independently audit archived logs and summarize one comparison batch.

This module deliberately imports no measurement-runner parser. Experiment
failures remain visible in all_trials.csv and never become zero-valued results.
Only within-case, within-batch timing pairs are formed; matrix jobs are separate
host scopes even when their CPU model strings happen to match.
"""
import argparse
import collections
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import statistics
import tempfile

PIN = "cb8deb9a176e5bb292d70d46557dd61dc0e98069"
CASES = ("reorder_3", "reorder_4", "account", "lazy01", "twostage")
# ICSE 2022, Table 2: first bug, all schedules, buggy schedules, respectively.
PAPER = {
    "reorder_3": {"period": (6, 27, 6), "serial": (10, 30, 10)},
    "reorder_4": {"period": (9, 100, 12), "serial": (37, 384, 90)},
    "account": {"period": (2, 65, 26), "serial": (4, 136, 56)},
    "lazy01": {"period": (3, 39, 12), "serial": (4, 60, 20)},
    "twostage": {"period": (4, 33, 3), "serial": (4, 33, 3)},
}
METHODS = {"period", "author_serialized", "author_serialized_abi16"}
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def stats(values):
    """Sample SD uses n-1; undefined statistics are JSON null, never zero."""
    values = list(values)
    return {"n": len(values), "mean": statistics.mean(values) if values else None,
            "sample_sd": statistics.stdev(values) if len(values) > 1 else None,
            "min": min(values) if values else None, "max": max(values) if values else None}


def wilson(successes, trials, z=1.959963984540054):
    if not trials:
        return {"successes": successes, "n": 0, "proportion": None,
                "lower_95": None, "upper_95": None}
    p = successes / trials
    denominator = 1 + z*z/trials
    centre = (p + z*z/(2*trials)) / denominator
    radius = z * math.sqrt(p*(1-p)/trials + z*z/(4*trials*trials)) / denominator
    return {"successes": successes, "n": trials, "proportion": p,
            "lower_95": max(0.0, centre-radius), "upper_95": min(1.0, centre+radius)}


def exact_mcnemar(default_only, expanded_only):
    """Two-sided exact conditional binomial test on discordant paired outcomes."""
    n = default_only + expanded_only
    if not n:
        return 1.0
    k = min(default_only, expanded_only)
    coefficient, tail = 1, 1
    for j in range(1, k+1):
        coefficient = coefficient * (n-j+1) // j
        tail += coefficient
    return min(1.0, 2 * tail / (2 ** n))


def parse_raw_log(text):
    """Recover event order, aggregate counters and runner footer from raw text."""
    clean = ANSI.sub("", text)
    ordinals, errors, error_numbers, current = [], [], [], None
    for line in clean.splitlines():
        match = re.fullmatch(r"test\s+(\d+)(?:\s+for prefix\s+[^:]+)?:\s*(.+)", line)
        if match:
            current = int(match.group(1))
            ordinals.append(current)
        if "[Error Found]:" in line:
            errors.append(current)
            number = re.search(r"\[Error Found\]:\s*NO\.(\d+)", line)
            error_numbers.append(int(number.group(1)) if number else None)
    totals = re.findall(r"^Total Error Interleavings:\s*(\d+)\s*$", clean, re.M)
    timeouts = re.findall(r"^Total Timeouts Interleavings:\s*(\d+)\s*$", clean, re.M)
    rounds = re.findall(r"^Round\s+(\d+)\s+(\d+)\s*$", clean, re.M)
    footers = re.findall(r"^Runner exit_code=(-?\d+) timed_out=(True|False) "
                         r"elapsed_seconds=([\d.]+)\s*$", clean, re.M)
    command_lines = re.findall(r"^Command: (.+)$", clean, re.M)
    starts = re.findall(r"^Started UTC: (.+)$", clean, re.M)
    command = None
    if len(command_lines) == 1:
        try:
            command = json.loads(command_lines[0])
        except ValueError:
            pass
    runner = None
    if len(footers) == 1:
        runner = {"exit_code": int(footers[0][0]), "timed_out": footers[0][1] == "True",
                  "elapsed_seconds": float(footers[0][2])}
    problems = []
    if not ordinals:
        problems.append("no enumerated schedules")
    elif ordinals != list(range(1, len(ordinals)+1)):
        problems.append("schedule ordinals are not exactly 1..N")
    if len(totals) != 1:
        problems.append("missing or repeated error-total footer")
    elif int(totals[0]) != len(errors):
        problems.append("error events disagree with error-total footer")
    if any(x is None for x in errors) or len(set(errors)) != len(errors):
        problems.append("unattributed or repeated error event")
    if error_numbers != list(range(1, len(error_numbers)+1)):
        problems.append("error event numbers are not exactly 1..E")
    if len(rounds) != 1 or int(rounds[0][1]) != len(ordinals):
        problems.append("round total disagrees with enumerated schedules")
    if "End Testing!" not in clean:
        problems.append("no end-testing marker")
    inner_timeouts = len(re.findall(r"\[Timeout\s", clean))
    if len(timeouts) != 1 or int(timeouts[0]) != inner_timeouts:
        problems.append("timeout events disagree with timeout-total footer")
    observations = []
    for payload in re.findall(r"^CS340_REPLAY (.+)$", clean, re.M):
        try:
            observations.append(json.loads(payload))
        except ValueError:
            observations.append(None)
    return {
        "schedules": len(ordinals), "first_error": errors[0] if errors else None,
        "buggy_schedules": int(totals[0]) if len(totals) == 1 else None,
        "error_event_count": len(errors), "inner_timeouts": inner_timeouts,
        "complete_markers": not problems, "parse_problems": problems,
        "runner": runner, "command": command,
        "started_utc": starts[0] if len(starts) == 1 else None,
        "target_observation": observations[0] if len(observations) == 1 else None,
        "expected_assertion": bool(re.search(r"Assertion[^\n]*failed", clean)),
    }


def verify_manifest(path, errors):
    """Validate every entry, its byte count and SHA256 without trusting records."""
    entries = {}
    if not path.is_file():
        errors.append("missing manifest: " + str(path))
        return entries
    for entry in load_json(path).get("files", []):
        relative = entry.get("path", "")
        item = path.parent / relative
        if not relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
            errors.append("unsafe manifest path: " + relative)
            continue
        if relative in entries:
            errors.append("duplicate manifest path: " + str(item))
        entries[relative] = entry
        if not item.is_file():
            errors.append("manifest file missing: " + str(item))
        elif item.stat().st_size != entry.get("bytes") or digest(item) != entry.get("sha256"):
            errors.append("manifest content mismatch: " + str(item))
    return entries


def paper_gap(observed, reference):
    if observed is None:
        return {"reference": reference, "signed_gap": None, "absolute_gap": None,
                "relative_gap_pct": None, "absolute_relative_gap_pct": None}
    gap = observed - reference
    return {"reference": reference, "signed_gap": gap, "absolute_gap": abs(gap),
            "relative_gap_pct": 100*gap/reference,
            "absolute_relative_gap_pct": 100*abs(gap)/reference}


def summarize_batch(batch, expected_repeats=10, expected_diagnostics=20, expected_cases=CASES):
    batch = Path(batch).resolve()
    errors, warnings, trials, provenance = [], [], [], {}
    archive = batch / "archive_manifest.json"
    if archive.exists():
        verify_manifest(archive, errors)
    else:
        warnings.append("No batch archive manifest; individual case manifests are checked.")
    record_paths = sorted(batch.glob("*/records.json"))
    if (batch / "records.json").exists():
        record_paths = [batch / "records.json"]
    seen_cases = []
    for record_path in record_paths:
        directory = record_path.parent
        entries = verify_manifest(directory / "manifest.json", errors)
        for required in ("records.json", "environment.json"):
            if required not in entries:
                errors.append(str(directory) + ": manifest omits " + required)
        environment = load_json(directory / "environment.json")
        records = load_json(record_path)
        cases = {r.get("case") for r in records}
        if len(cases) != 1 or None in cases:
            errors.append(str(record_path) + ": ambiguous case identity")
            continue
        case = next(iter(cases))
        seen_cases.append(case)
        if case in provenance:
            errors.append("duplicate case/host scope: " + case)
        binary_hash = environment.get("binary_sha256", "")
        if not HEX64.fullmatch(binary_hash):
            errors.append(case + ": absent or invalid recorded binary SHA256")
        if environment.get("paired_methods_same_built_binary") is not True:
            errors.append(case + ": same-binary pairing was not declared")
        if environment.get("source_commit") != PIN:
            errors.append(case + ": upstream source revision differs from declared pin")
        provenance[case] = {
            "host_scope": batch.name + "/" + case,
            "binary_sha256": binary_hash,
            "binary_hash_validation": "manifest-protected captured hash; executable is not archived",
            "cpu_models": environment.get("cpu_models"),
            "cpu_affinity": environment.get("cpu_affinity"),
            "platform": environment.get("platform"),
            "source_commit": environment.get("source_commit"),
        }
        seen_logs = set()
        for record in records:
            log_name = record.get("log", "")
            path = directory / log_name
            issues = []
            if not log_name or Path(log_name).name != log_name:
                errors.append(case + ": invalid record log name")
                continue
            if log_name in seen_logs:
                issues.append("duplicate command-log reference")
            seen_logs.add(log_name)
            if log_name not in entries:
                issues.append("log absent from case manifest")
            if not path.is_file():
                errors.append(case + "/" + log_name + ": missing log")
                continue
            actual_hash = digest(path)
            if actual_hash != record.get("log_sha256"):
                issues.append("record log SHA256 mismatch")
            if log_name in entries and actual_hash != entries[log_name].get("sha256"):
                issues.append("case manifest log SHA256 mismatch")
            parsed = parse_raw_log(path.read_text(encoding="utf-8", errors="replace"))
            footer = parsed["runner"]
            if footer is None:
                issues.append("missing or repeated runner footer")
            else:
                for key in ("exit_code", "timed_out"):
                    if footer[key] != record.get(key):
                        issues.append("runner/record disagreement: " + key)
                elapsed = record.get("elapsed_seconds")
                if not isinstance(elapsed, (int, float)) or not math.isfinite(elapsed) or elapsed < 0:
                    issues.append("invalid elapsed time")
                elif abs(elapsed - footer["elapsed_seconds"]) > 0.000001:
                    issues.append("runner/record disagreement: elapsed_seconds")
            if parsed["command"] != record.get("command"):
                issues.append("command header/record disagreement")
            if parsed["started_utc"] != record.get("started_utc"):
                issues.append("start-time header/record disagreement")
            if record.get("binary_sha256", binary_hash) != binary_hash:
                issues.append("trial binary hash differs from case binary")
            phase = record.get("phase")
            complete = False
            if phase == "comparison":
                method = record.get("method")
                if method not in METHODS:
                    issues.append("unknown comparison method")
                for key in ("schedules", "first_error", "buggy_schedules", "error_event_count",
                            "complete_markers", "inner_timeouts"):
                    if key in record and record[key] != parsed[key]:
                        issues.append("independent recount disagrees with recorded " + key)
                complete = bool(footer and footer["exit_code"] == 0 and not footer["timed_out"]
                                and parsed["complete_markers"])
                command = record.get("command", [])
                drivers = [Path(x).name for x in command if x.endswith(".py")]
                if len(drivers) != 1:
                    issues.append("ambiguous driver command")
                else:
                    source = directory / "source" / drivers[0]
                    if not source.exists() or digest(source) != environment.get("drivers", {}).get(method):
                        issues.append("archived driver differs from captured driver SHA256")
                if "-d" not in command or command[command.index("-d")+1] != "3":
                    issues.append("unexpected exploration depth")
                if "-f" not in command or command[command.index("-f")+1] != "10000":
                    issues.append("unexpected schedule budget")
            elif phase == "diagnostic":
                obs = parsed["target_observation"]
                complete = bool(footer and footer["exit_code"] == 0 and not footer["timed_out"]
                                and isinstance(obs, dict) and isinstance(obs.get("target_returncode"), int))
                if obs != record.get("target_observation"):
                    issues.append("independent replay observation disagrees with record")
                if parsed["expected_assertion"] != record.get("expected_assertion"):
                    issues.append("independent assertion signature disagrees with record")
                if obs and obs.get("scale") != record.get("scale"):
                    issues.append("replay observation scale differs from condition")
            elif phase != "build":
                issues.append("unknown command phase")
            if phase in ("comparison", "diagnostic"):
                if (record.get("status") == "complete") != complete:
                    issues.append("recorded completion disagrees with independent completion")
                trial = {key: record.get(key) for key in ("case", "phase", "method", "condition", "repeat",
                         "position", "started_utc", "exit_code", "timed_out", "elapsed_seconds", "scale")}
                trial.update({key: parsed[key] for key in ("schedules", "first_error", "buggy_schedules",
                              "error_event_count", "inner_timeouts", "complete_markers", "expected_assertion")})
                observation = parsed["target_observation"] or {}
                trial.update({"target_returncode": observation.get("target_returncode"),
                    "calibrated_period": observation.get("calibrated_period"),
                    "log": str(path.relative_to(batch)), "log_sha256": actual_hash,
                    "host_scope": provenance[case]["host_scope"], "binary_sha256": binary_hash,
                    "complete": complete, "integrity_ok": not issues,
                    "eligible": complete and not issues,
                    "parse_problems": parsed["parse_problems"] if phase == "comparison" else [],
                    "issues": issues})
                trials.append(trial)
            errors.extend(case + "/" + log_name + ": " + issue for issue in issues)
        primary = [r for r in records if r.get("phase") == "comparison"]
        methods = {r.get("method") for r in primary}
        serials = methods - {"period"}
        if len(serials) != 1 or "period" not in methods:
            errors.append(case + ": comparison must contain PERIOD and exactly one serialized variant")
        else:
            serial = next(iter(serials))
            expected_order = [(r, m, pos) for r in range(1, expected_repeats+1)
                for pos, m in enumerate(("period", serial) if r % 2 else (serial, "period"), 1)]
            actual_order = [(r.get("repeat"), r.get("method"), r.get("position")) for r in primary]
            if actual_order != expected_order:
                errors.append(case + ": repetitions or AB/BA execution order differ from protocol")
        diagnostics = [r for r in records if r.get("phase") == "diagnostic"]
        if case == "reorder_3" or diagnostics:
            expected_order = [(r, c, pos) for r in range(1, expected_diagnostics+1)
                for pos, c in enumerate(("default", "expanded") if r % 2 else ("expanded", "default"), 1)]
            actual_order = [(r.get("repeat"), r.get("condition"), r.get("position")) for r in diagnostics]
            if actual_order != expected_order:
                errors.append(case + ": diagnostic repetitions or AB/BA execution order differ from protocol")
        timestamps = [r.get("started_utc", "") for r in records]
        if timestamps != sorted(timestamps):
            errors.append(case + ": record timestamps are not chronological")
    if sorted(seen_cases) != sorted(expected_cases):
        errors.append("case set differs from protocol: " + repr(sorted(seen_cases)))
    groups, pairs, diagnostics_out = [], [], []
    for case in sorted(set(seen_cases)):
        primary = [r for r in trials if r["case"] == case and r["phase"] == "comparison"]
        for method in sorted({r["method"] for r in primary}):
            attempted = [r for r in primary if r["method"] == method]
            eligible = [r for r in attempted if r["eligible"]]
            hits = [r for r in eligible if r["first_error"] is not None]
            incomplete = [r for r in attempted if not r["complete"] and r["integrity_ok"]]
            row = {"case": case, "method": method, "attempted_n": len(attempted),
                   "complete_n": sum(r["complete"] for r in attempted),
                   "eligible_n": len(eligible), "incomplete_n": sum(not r["complete"] for r in attempted),
                   "excluded_integrity_n": sum(not r["integrity_ok"] for r in attempted),
                   "outer_timeout_n": sum(r["timed_out"] is True for r in attempted),
                   "incomplete_observations": {
                       "n": len(incomplete),
                       "interpretation": "Observed prefixes only; these are not completed search totals or completion runtimes.",
                       "printed_schedules": stats(r["schedules"] for r in incomplete),
                       "observed_error_events": stats(r["error_event_count"] for r in incomplete),
                       "observed_first_error": stats(r["first_error"] for r in incomplete if r["first_error"] is not None),
                       "elapsed_before_stop_seconds": stats(r["elapsed_seconds"] for r in incomplete)},
                   "detected_n": len(hits), "first_error_condition": "completed trials with >=1 observed error",
                   "first_error": stats(r["first_error"] for r in hits),
                   "schedules": stats(r["schedules"] for r in eligible),
                   "buggy_schedules": stats(r["buggy_schedules"] for r in eligible),
                   "elapsed_seconds": stats(r["elapsed_seconds"] for r in eligible),
                   "detection_rate": wilson(len(hits), len(eligible)),
                   "exit_codes_all_attempts": dict(collections.Counter(str(r["exit_code"]) for r in attempted)),
                   "host_scope": provenance[case]["host_scope"]}
            reference = PAPER.get(case, {}).get("period" if method == "period" else "serial")
            if reference:
                row["paper_table_2_gaps"] = {metric: paper_gap(row[metric]["mean"], target)
                    for metric, target in zip(("first_error", "schedules", "buggy_schedules"), reference)}
            groups.append(row)
        serials = {r["method"] for r in primary} - {"period"}
        for serial in sorted(serials):
            by_key = {(r["repeat"], r["method"]): r for r in primary if r["eligible"]}
            paired = [(by_key[(i, "period")], by_key[(i, serial)]) for i in range(1, expected_repeats+1)
                      if (i, "period") in by_key and (i, serial) in by_key]
            pairs.append({"case": case, "serial_method": serial, "n_complete_pairs": len(paired),
                "host_scope": provenance[case]["host_scope"],
                "serial_minus_period_seconds": stats(s["elapsed_seconds"]-p["elapsed_seconds"] for p,s in paired),
                "serial_over_period_time_ratio": stats(s["elapsed_seconds"]/p["elapsed_seconds"] for p,s in paired
                                                        if p["elapsed_seconds"] > 0),
                "schedule_reduction_pct": stats(100*(s["schedules"]-p["schedules"])/s["schedules"]
                                                 for p,s in paired if s["schedules"] > 0)})
        diag = [r for r in trials if r["case"] == case and r["phase"] == "diagnostic"]
        if diag:
            condition_rows = []
            for condition in ("default", "expanded"):
                attempted = [r for r in diag if r["condition"] == condition]
                valid = [r for r in attempted if r["eligible"]]
                row = {"condition": condition, "attempted_n": len(attempted), "eligible_n": len(valid),
                       "target_returncodes": dict(collections.Counter(str(r["target_returncode"]) for r in valid)),
                       "nonzero_target_exit": wilson(sum(r["target_returncode"] != 0 for r in valid), len(valid)),
                       "assertion_signature": wilson(sum(r["expected_assertion"] for r in valid), len(valid)),
                       "confirmed_assertion": wilson(sum(r["expected_assertion"] and r["target_returncode"] != 0
                                                          for r in valid), len(valid)),
                       "elapsed_seconds": stats(r["elapsed_seconds"] for r in valid),
                       "calibrated_period": stats(r["calibrated_period"] for r in valid)}
                condition_rows.append(row)
            by_key = {(r["repeat"], r["condition"]): r for r in diag if r["eligible"]}
            counts = collections.Counter()
            for i in range(1, expected_diagnostics+1):
                if (i, "default") in by_key and (i, "expanded") in by_key:
                    a, b = by_key[(i, "default")], by_key[(i, "expanded")]
                    counts[(bool(a["expected_assertion"] and a["target_returncode"] != 0),
                            bool(b["expected_assertion"] and b["target_returncode"] != 0))] += 1
            default_only, expanded_only = counts[(True, False)], counts[(False, True)]
            diagnostics_out.append({"case": case, "conditions": condition_rows,
                "paired_confirmed_assertions": {"n": sum(counts.values()),
                    "both": counts[(True, True)], "neither": counts[(False, False)],
                    "default_only": default_only, "expanded_only": expanded_only,
                    "exact_mcnemar_two_sided_p": exact_mcnemar(default_only, expanded_only)},
                "interpretation": "One fixed witness on one host. Wilson intervals assume an appropriate independent Bernoulli model; exact McNemar assumes independent pairs with exchangeable discordant directions under its null. Sequential repetitions on one host can be dependent. These optional model-based quantities do not establish equality when both conditions always hit. The primary report uses descriptive counts and mean/sample SD."})
    if any(r["method"] == "author_serialized" and not r["complete"] for r in trials):
        warnings.append("Unmodified serialized failures have no valid scheduler outcome. Historical witnesses/author_serialized copies may be stale PERIOD files; this analysis never uses witness counts or attribution.")
    warnings.append("Runtime summaries are per case and batch only. CPU labels are not host identifiers; there is no pooled cross-host speedup.")
    warnings.append("Paper gaps are descriptive reproduction gaps. The ABI-adapted released serialized driver has not been proven identical to the historical Table 2 executable.")
    warnings.append("Wilson and exact McNemar outputs are optional model-based diagnostics. Independence of repeated trials or pairs is not established by AB/BA ordering; all-hit outcomes do not prove equality. Descriptive counts and mean/sample SD are the primary results.")
    if any(r["timed_out"] for r in trials if r["phase"] == "comparison"):
        warnings.append("Outer timeouts are right-censored searches. Their observed schedule/error prefixes are retained separately; they are excluded from completed-search means, paper-total gaps and completed runtime pairs. A timeout after observing an error is not a failure to detect that error.")
    return {"schema_version": 1, "batch": batch.name, "upstream_pin": PIN,
            "design": {"cases": list(expected_cases), "repetitions_per_method": expected_repeats,
                       "expected_comparison_attempts": len(expected_cases)*expected_repeats*2,
                       "diagnostic_pairs_if_reorder_3": expected_diagnostics if "reorder_3" in expected_cases else 0,
                       "order": "Odd repetition PERIOD then serialized; even repetition serialized then PERIOD",
                       "completion_requirement": "All planned attempts accounted for; genuine incomplete outcomes remain admissible and excluded from completed-result estimates",
                       "pooling_scope": "One batch, with paired comparisons confined to each case"},
            "integrity_ok": not errors, "integrity_errors": errors, "warnings": warnings,
            "provenance": provenance, "groups": groups, "paired_comparisons": pairs,
            "diagnostics": diagnostics_out, "trials": trials,
            "denominators": {"comparison_attempts": sum(r["phase"] == "comparison" for r in trials),
                "comparison_complete": sum(r["phase"] == "comparison" and r["complete"] for r in trials),
                "comparison_eligible": sum(r["phase"] == "comparison" and r["eligible"] for r in trials),
                "diagnostic_attempts": sum(r["phase"] == "diagnostic" for r in trials)}}


def write_outputs(summary, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False)+"\n", encoding="utf-8")
    fields = ("case", "phase", "method", "condition", "repeat", "position", "started_utc", "host_scope",
              "binary_sha256", "complete", "integrity_ok", "eligible", "exit_code", "timed_out",
              "elapsed_seconds", "schedules", "first_error", "buggy_schedules", "error_event_count",
              "inner_timeouts", "scale", "target_returncode", "expected_assertion", "calibrated_period",
              "log", "log_sha256", "parse_problems", "issues")
    with (output / "all_trials.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for trial in summary["trials"]:
            row = dict(trial)
            for key in ("parse_problems", "issues"):
                row[key] = "; ".join(row[key])
            writer.writerow(row)
    def cell(value):
        if value["mean"] is None:
            return "NA (n=0)"
        sd = "NA" if value["sample_sd"] is None else "{:.4f}".format(value["sample_sd"])
        return "{:.4f} ± {} (n={})".format(value["mean"], sd, value["n"])
    lines = ["# Independent comparison summary", "", "Batch: `"+summary["batch"]+"`.", "",
             "Integrity validation: **"+("PASS" if summary["integrity_ok"] else "FAIL")+"**.", "",
             "Values are arithmetic mean ± sample SD. First-error statistics are conditional on a completed trial detecting an error; other metrics use all eligible completed trials.", "",
             "| Case | Method | Complete / attempts | First error | Schedules | Buggy schedules | Wall time (s) |",
             "|---|---|---:|---:|---:|---:|---:|"]
    for group in summary["groups"]:
        lines.append("| {} | {} | {} / {} | {} | {} | {} | {} |".format(group["case"], group["method"],
            group["complete_n"], group["attempted_n"], *(cell(group[k]) for k in
                ("first_error", "schedules", "buggy_schedules", "elapsed_seconds"))))
    censored = [group for group in summary["groups"] if group["outer_timeout_n"]]
    if censored:
        lines.extend(["", "## Censored searches", "",
            "Outer timeouts preserve the observed prefix. Its printed schedule count is not the completed search-space size; observations before timeout can still include detected errors.", "",
            "| Case | Method | Outer timeouts | Observed printed schedules (min–max) | Prefixes with an observed first error |",
            "|---|---|---:|---:|---:|"])
        for group in censored:
            observed = group["incomplete_observations"]
            lines.append("| {} | {} | {} | {}–{} | {} / {} |".format(group["case"], group["method"],
                group["outer_timeout_n"], observed["printed_schedules"]["min"], observed["printed_schedules"]["max"],
                observed["observed_first_error"]["n"], observed["n"]))
    lines.extend(["", "## Paired comparisons", "", "Each row uses complete repetition pairs from one case on one matrix-job host.", "",
                  "| Case | Pairs | Schedule reduction (%) | Serialized − PERIOD time (s) | Serialized / PERIOD time |",
                  "|---|---:|---:|---:|---:|"])
    for pair in summary["paired_comparisons"]:
        lines.append("| {} | {} | {} | {} | {} |".format(pair["case"], pair["n_complete_pairs"],
            cell(pair["schedule_reduction_pct"]), cell(pair["serial_minus_period_seconds"]),
            cell(pair["serial_over_period_time_ratio"])))
    lines.extend(["", "Detailed paper gaps, diagnostic outcomes, Wilson intervals, paired discordances and provenance are in `summary.json`; every attempted trial is in `all_trials.csv`.", "", "## Limits and integrity findings", ""])
    lines.extend("- "+x for x in summary["warnings"]+summary["integrity_errors"])
    (output / "SUMMARY.md").write_text("\n".join(lines)+"\n", encoding="utf-8")


def check_outputs(summary, output):
    """Check published tables without rewriting them; allow numerical roundoff."""
    output = Path(output)
    def compare(expected, actual, location="summary"):
        if isinstance(expected, dict) and isinstance(actual, dict):
            if set(expected) != set(actual):
                raise ValueError(location + ": published keys differ")
            for key in expected:
                compare(expected[key], actual[key], location + "/" + str(key))
        elif isinstance(expected, list) and isinstance(actual, list):
            if len(expected) != len(actual):
                raise ValueError(location + ": published list length differs")
            for index, (left, right) in enumerate(zip(expected, actual)):
                compare(left, right, location + "/" + str(index))
        elif (isinstance(expected, (int, float)) and not isinstance(expected, bool)
              and isinstance(actual, (int, float)) and not isinstance(actual, bool)):
            if not math.isclose(expected, actual, rel_tol=1e-12, abs_tol=1e-12):
                raise ValueError(location + ": published number differs")
        elif type(expected) is not type(actual) or expected != actual:
            raise ValueError(location + ": published value differs")
    compare(summary, load_json(output / "summary.json"))
    with tempfile.TemporaryDirectory(prefix="comparison-summary-") as temp:
        write_outputs(summary, temp)
        for name in ("all_trials.csv", "SUMMARY.md"):
            if (Path(temp) / name).read_bytes() != (output / name).read_bytes():
                raise ValueError(name + ": published content differs from independent recount")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path, help="Directory containing one evidence directory per case")
    parser.add_argument("--output", type=Path, help="Summary directory outside raw evidence")
    parser.add_argument("--check", action="store_true", help="Audit existing summaries without modifying them")
    parser.add_argument("--manifest-only", action="store_true", help="Verify bytes of an incomplete/startup archive without requiring scientific samples")
    parser.add_argument("--cases", nargs="+", choices=CASES, default=list(CASES), help="Predeclared case set (default: all five cases)")
    parser.add_argument("--repeats", type=int, default=10, help="Predeclared paired repetitions per case (default: 10)")
    args = parser.parse_args()
    if args.repeats < 1 or len(args.cases) != len(set(args.cases)):
        parser.error("--repeats must be positive and --cases must not contain duplicates")
    if args.manifest_only:
        if args.check or args.output:
            parser.error("--manifest-only cannot be combined with --check or --output")
        paths = sorted(args.batch.rglob("manifest.json"))
        if (args.batch / "archive_manifest.json").exists():
            paths.insert(0, args.batch / "archive_manifest.json")
        if not paths:
            parser.error("no archive or case manifest found")
        errors = []
        count = sum(len(verify_manifest(path, errors)) for path in paths)
        print(json.dumps({"scope": "manifest-only; no complete scientific sample required",
                          "manifest_count": len(paths), "checked_file_entries": count,
                          "integrity_ok": not errors, "integrity_errors": errors}, indent=2))
        return 2 if errors else 0
    if args.output is None:
        parser.error("--output is required for a scientific summary or audit")
    batch, output = args.batch.resolve(), args.output.resolve()
    if output == batch or batch in output.parents:
        parser.error("--output must be outside the immutable raw evidence batch")
    summary = summarize_batch(batch, expected_repeats=args.repeats, expected_cases=args.cases)
    if args.check:
        try:
            check_outputs(summary, output)
        except (ValueError, OSError) as error:
            summary["integrity_ok"] = False
            summary["integrity_errors"].append(str(error))
    else:
        write_outputs(summary, output)
    print(json.dumps({"integrity_ok": summary["integrity_ok"], "denominators": summary["denominators"],
                      "integrity_error_count": len(summary["integrity_errors"]),
                      "integrity_errors": summary["integrity_errors"],
                      "mode": "check" if args.check else "write", "output": str(output)}, indent=2))
    return 0 if summary["integrity_ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
