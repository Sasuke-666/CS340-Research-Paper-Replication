#!/usr/bin/env python3
"""Audit the registered capacity study from immutable source and raw logs.

The raw-log decoder is shared with the independent comparison auditor, never
with the measurement runner. Requested schedules are not execution traces.
"""
import argparse
import ast
import collections
import csv
import datetime
import difflib
import hashlib
import json
import math
from pathlib import Path
import re
import tempfile

from summarize_comparison import ANSI, parse_raw_log, stats

PIN = "cb8deb9a176e5bb292d70d46557dd61dc0e98069"
PINNED_DRIVER_SHA256 = "c6ed1312f61f7ec739e3dcead0086e0265d37f07bd88ef64d6588d3ff61a8e8f"
PINNED_RUNTIME_SHA256 = "6e5001f8a79851f24f3074b4a6d84cf2550b52b947946f8a330f8877e44e4f61"
CASES = ("account", "lazy01")
CONDITIONS = ("capacity1990", "capacity3964")
DRIVERS = dict(zip(CONDITIONS, ("run_PDS.py", "run_PDS_layout3964.py")))
LAYOUT = {"sizeof": 24008, "offsets": dict(zip(
    ("time", "N", "M", "TestedBounds", "kpNumArray", "kp", "kpLoc", "kpOrder"),
    (0, 8, 12, 16, 20, 220, 8148, 16076)))}
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
METRICS = ("schedules", "first_error", "buggy_schedules", "elapsed_seconds")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path, errors, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        errors.append(path.name + ": cannot read JSON (" + type(error).__name__ + ")")
        return {} if default is None else default


def safe_path(root, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise ValueError("unsafe evidence path")
    path = root / relative
    if any(item.is_symlink() for item in (path, *path.parents) if item != root.parent):
        raise ValueError("evidence path contains a symlink")
    return path


def verify_manifest(path, errors):
    entries = {}
    manifest = read_json(path, errors)
    files = manifest.get("files", []) if isinstance(manifest, dict) else []
    if not isinstance(files, list) or not files:
        errors.append(path.name + ": empty or invalid manifest")
        return entries
    for entry in files:
        if not isinstance(entry, dict):
            errors.append(path.name + ": invalid manifest entry")
            continue
        relative = entry.get("path")
        try:
            item = safe_path(path.parent, relative)
            if relative in entries:
                raise ValueError("duplicate manifest path")
            entries[relative] = entry
            if not item.is_file():
                raise ValueError("manifest file missing")
            if type(entry.get("bytes")) is not int or item.stat().st_size != entry["bytes"] or digest(item) != entry.get("sha256"):
                raise ValueError("manifest content mismatch")
        except (ValueError, OSError) as error:
            errors.append(str(relative) + ": " + str(error))
    return entries


def required_file(directory, name, manifest, errors):
    if name not in manifest:
        errors.append(name + ": absent from manifest")
    try:
        path = safe_path(directory, name)
        # Source and log hashes identify archived bytes; text-mode reading would
        # silently normalize the pinned native source's CRLF line endings.
        return path.read_bytes().decode("utf-8")
    except (OSError, ValueError) as error:
        errors.append(name + ": cannot read evidence (" + type(error).__name__ + ")")
        return ""


def validate_sources(directory, environment, manifest, errors):
    original = required_file(directory, "source/run_PDS.py", manifest, errors)
    corrected = required_file(directory, "source/run_PDS_layout3964.py", manifest, errors)
    runtime = required_file(directory, "source/DBDSFunction.cpp", manifest, errors)
    hashes = {"capacity1990": hashlib.sha256(original.encode()).hexdigest(),
              "capacity3964": hashlib.sha256(corrected.encode()).hexdigest()}
    runtime_hash = hashlib.sha256(runtime.encode()).hexdigest()
    if hashes["capacity1990"] != PINNED_DRIVER_SHA256:
        errors.append("original driver differs from the pinned upstream bytes")
    if runtime_hash != PINNED_RUNTIME_SHA256:
        errors.append("native runtime differs from the pinned upstream bytes")
    anchor = "SHARE_ARRAY_SIZE = 1990"
    if original.count(anchor) != 1 or corrected != original.replace(anchor, "SHARE_ARRAY_SIZE = 3964", 1):
        errors.append("driver conditions differ beyond the one registered capacity declaration")
    if environment.get("drivers") != hashes:
        errors.append("captured driver hashes disagree with archived sources")
    patch = required_file(directory, "capacity.diff", manifest, errors)
    expected_patch = "".join(difflib.unified_diff(original.splitlines(True), corrected.splitlines(True),
                               fromfile="upstream/run_PDS.py", tofile="adapted/run_PDS_layout3964.py"))
    if patch != expected_patch:
        errors.append("capacity.diff disagrees with archived source comparison")
    for name in ("capacity_change.json", "runtime_layout.json", "synthetic_decode_probe.json", "source/runtime_layout_probe.cpp"):
        required_file(directory, name, manifest, errors)
    change = read_json(directory / "capacity_change.json", errors)
    if (change.get("original_sha256") != hashes["capacity1990"] or
            change.get("adapted_sha256") != hashes["capacity3964"] or change.get("runtime_sha256") != runtime_hash):
        errors.append("capacity change metadata hash disagreement")
    layout = read_json(directory / "runtime_layout.json", errors)
    if layout.get("observed_layout") != LAYOUT or layout.get("runtime_source_sha256") != runtime_hash:
        errors.append("compiled native layout or runtime provenance differs from protocol")
    probe_source = directory / "source/runtime_layout_probe.cpp"
    if not probe_source.is_file() or layout.get("probe_source_sha256") != digest(probe_source):
        errors.append("compiled probe source hash disagreement")
    else:
        probe_text = probe_source.read_text(encoding="utf-8")
        # The declaration-only probe is generated after text-mode source reading.
        # Normalize line endings only for this semantic declaration comparison.
        structures = re.findall(r"typedef struct Sched_Info\s*\{.*?\}\s*sched_info;", runtime.replace("\r\n", "\n"), re.S)
        if len(structures) != 1 or probe_text.count(structures[0]) != 1:
            errors.append("layout probe does not contain the actual runtime structure")
        for name, value in (("SHARE_MEMORY_THREAD_NUM", 100), ("SHARE_MEMORY_ARRAY_SIZE", 3964)):
            declaration = r"(?m)^#define\s+" + name + r"\s+" + str(value) + r"\s*$"
            if len(re.findall(declaration, runtime)) != 1 or len(re.findall(declaration, probe_text)) != 1:
                errors.append("layout probe macro differs from pinned runtime: " + name)
    # Native layout and the synthetic decoder are separate evidence types.
    sentinel = read_json(directory / "synthetic_decode_probe.json", errors)
    expected = {"capacity1990": (101, 202), "capacity3964": (202, 303)}
    for condition, values in expected.items():
        observed = sentinel.get("conditions", {}).get(condition, {})
        if (observed.get("decoded_location"), observed.get("decoded_order")) != values:
            errors.append("synthetic sentinel decoding disagreement: " + condition)
    return {"driver_sha256": hashes, "runtime_sha256": runtime_hash,
            "native_layout": layout.get("observed_layout"),
            "synthetic_decode_scope": "Synthetic sentinel evidence; excluded from workload counts"}


def check_reset(reset, errors, label):
    if not isinstance(reset, dict):
        errors.append(label + ": missing cleanup record")
        return
    if reset.get("key_absent") is not True or reset.get("post_shmget") != -1 or reset.get("post_errno") != 2:
        errors.append(label + ": shared-memory key absence was not verified")
    previous = reset.get("previous_shmid")
    if type(previous) is not int:
        errors.append(label + ": invalid previous segment identifier")
    elif previous >= 0:
        row = reset.get("previous_segment")
        if not isinstance(row, dict) or str(row.get("nattch")) != "0" or str(row.get("shmid")) != str(previous) or str(row.get("key")) != "1111":
            errors.append(label + ": prior shared-memory attachments or identity are not verified")
    elif previous != -1 or reset.get("previous_errno") != 2 or reset.get("previous_segment") is not None:
        errors.append(label + ": previous lookup failed for an unexpected reason")
    killed = reset.get("killed_target_pids")
    if not isinstance(killed, list) or any(type(x) is not int or x < 1 for x in killed):
        errors.append(label + ": invalid target cleanup PID record")


def normalize_budget_boundary(text, budget=10000):
    """Decode the pinned driver's unexecuted budget+1 print, preserving its count.

    The driver prints the next ordinal before checking its budget. On stopping,
    that unfinished label is followed by End Testing! instead of a request.
    This is a bounded completion, not a (budget+1)th target execution.
    """
    clean = ANSI.sub("", text)
    totals = re.findall(r"(?m)^Round\s+(\d+)\s+(\d+)\s*$", clean)
    reported = int(totals[0][1]) if len(totals) == 1 else None
    sentinel = r"(?m)^test[ \t]+0*" + str(budget + 1) + r"(?:[ \t]+for prefix[ \t]+[^:\r\n]+)?:[ \t]*End Testing![ \t]*$"
    matches = re.findall(sentinel, clean)
    recognized = len(matches) == 1 and reported == budget + 1
    if recognized:
        clean = re.sub(sentinel, "End Testing!", clean)
        clean = re.sub(r"(?m)^Round\s+(\d+)\s+" + str(budget + 1) + r"\s*$",
                       lambda match: "Round " + match.group(1) + " " + str(budget), clean)
    return clean, reported, recognized


def parse_layout_log(text, budget=10000):
    normalized, reported, sentinel = normalize_budget_boundary(text, budget)
    result = parse_raw_log(normalized)
    result.update(reported_round_total=reported, unexecuted_budget_sentinel=sentinel,
                  budget_reached=reported is not None and reported >= budget)
    return result


def schedule_sequence(text):
    sequence = []
    clean, _, _ = normalize_budget_boundary(text)
    for ordinal, prefix, schedule in re.findall(r"(?m)^test[ \t]+(\d+)(?:[ \t]+for prefix[ \t]+([^:\r\n]+))?:[ \t]*(.+)$", clean):
        value = ast.literal_eval(schedule)
        prefix_value = ast.literal_eval(prefix) if prefix else []
        if not isinstance(value, list) or not isinstance(prefix_value, list):
            raise ValueError("non-list requested schedule")
        sequence.append([int(ordinal), prefix_value, value])
    canonical = json.dumps(sequence, separators=(",", ":"), ensure_ascii=True)
    return sequence, hashlib.sha256(canonical.encode()).hexdigest()


def valid_time(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def check_command_record(directory, record, manifest, errors):
    name = record.get("log", "")
    text = required_file(directory, name, manifest, errors)
    actual_hash = hashlib.sha256(text.encode()).hexdigest()
    if actual_hash != record.get("log_sha256"):
        errors.append(name + ": log hash differs from record")
    parsed = parse_layout_log(text) if record.get("phase") == "layout" else parse_raw_log(text)
    footer = parsed["runner"]
    if footer is None:
        errors.append(name + ": missing or repeated runner footer")
    else:
        if footer["exit_code"] != record.get("exit_code") or footer["timed_out"] != record.get("timed_out"):
            errors.append(name + ": process outcome disagrees with raw footer")
        if not valid_time(record.get("elapsed_seconds")) or abs(record["elapsed_seconds"] - footer["elapsed_seconds"]) > 1e-6:
            errors.append(name + ": elapsed time disagrees with raw footer")
    if parsed["command"] != record.get("command") or parsed["started_utc"] != record.get("started_utc"):
        errors.append(name + ": command or start timestamp disagrees with raw header")
    try:
        start = datetime.datetime.fromisoformat(record["started_utc"])
        finish = datetime.datetime.fromisoformat(record["finished_utc"])
        if start.tzinfo is None or finish.tzinfo is None or finish < start:
            raise ValueError("invalid timestamp interval")
    except (KeyError, TypeError, ValueError):
        errors.append(name + ": invalid or missing timestamp interval")
    return parsed, text, actual_hash


def summarize_batch(batch, expected_cases=CASES, expected_repeats=10):
    batch = Path(batch).resolve()
    errors, trials, provenance, sequences = [], [], {}, {}
    archive_errors = []
    archive_entries = (verify_manifest(batch / "archive_manifest.json", archive_errors)
                       if (batch / "archive_manifest.json").exists() else {})
    errors.extend("archive: " + item for item in archive_errors)
    record_paths = [batch / "records.json"] if (batch / "records.json").exists() else sorted(batch.glob("*/records.json"))
    seen_cases = []
    for record_path in record_paths:
        directory = record_path.parent
        local = []
        manifest = verify_manifest(directory / "manifest.json", local)
        for required in ("records.json", "environment.json", "planned_trials.json"):
            required_file(directory, required, manifest, local)
        records = read_json(record_path, local, [])
        environment = read_json(directory / "environment.json", local)
        if not isinstance(records, list) or any(not isinstance(r, dict) for r in records):
            errors.append(directory.name + ": invalid records list")
            continue
        cases = {r.get("case") for r in records}
        case = next(iter(cases)) if len(cases) == 1 else None
        if case not in expected_cases or case in seen_cases:
            errors.append(directory.name + ": unknown, duplicate, or ambiguous case identity")
            continue
        seen_cases.append(case)
        if environment.get("source_commit") != PIN or environment.get("same_built_binary") is not True:
            local.append("source pin or same-binary declaration differs from protocol")
        binary_hash = environment.get("binary_sha256", "")
        if not isinstance(binary_hash, str) or not HEX64.fullmatch(binary_hash):
            local.append("absent or invalid benchmark binary SHA256")
        expected_settings = {"depth": 3, "schedule_budget": 10000, "repetitions_per_condition": expected_repeats,
                             "outer_timeout_seconds": 120}
        if any(environment.get("settings", {}).get(k) != v for k, v in expected_settings.items()):
            local.append("captured settings differ from the registered design")
        source_check = validate_sources(directory, environment, manifest, local)
        provenance[case] = {"host_scope": batch.name + "/" + case, "binary_sha256": binary_hash,
                            "cpu_models": environment.get("cpu_models"), "cpu_affinity": environment.get("cpu_affinity"),
                            "platform": environment.get("platform"), "manifest_file_count": len(manifest), **source_check}
        preparation = [r.get("phase") for r in records if r.get("phase") != "layout"]
        if preparation != ["layout_probe_build", "layout_probe", "deadline_probe", "build"]:
            local.append("preparation phases differ from the registered sequence")
        primary = [r for r in records if r.get("phase") == "layout"]
        expected_order = [(repeat, condition, position) for repeat in range(1, expected_repeats + 1)
                          for position, condition in enumerate(CONDITIONS if repeat % 2 else CONDITIONS[::-1], 1)]
        declared = read_json(directory / "planned_trials.json", local, [])
        if declared != [{"phase": "layout", "case": case, "repeat": repeat, "position": position, "condition": condition}
                        for repeat, condition, position in expected_order]:
            local.append("saved planned trial roster differs from the registered design")
        if [(r.get("repeat"), r.get("condition"), r.get("position")) for r in primary] != expected_order:
            local.append("planned trial identities or AB/BA order differ from protocol")
        timestamps = [r.get("started_utc", "") for r in records]
        if timestamps != sorted(timestamps):
            local.append("command timestamps are not chronological")
        logs = [r.get("log") for r in records]
        if len(set(logs)) != len(logs):
            local.append("more than one record refers to the same log")
        for record in records:
            issues = []
            parsed, text, actual_hash = check_command_record(directory, record, manifest, issues)
            phase = record.get("phase")
            if phase != "layout":
                if not parsed["runner"] or parsed["runner"]["exit_code"] != 0 or parsed["runner"]["timed_out"]:
                    issues.append("preparation command failed or timed out")
                if phase in ("layout_probe", "deadline_probe"):
                    try:
                        values = [json.loads(line) for line in text.splitlines() if line.startswith("{")]
                        if len(values) != 1:
                            raise ValueError("one observation required")
                        if phase == "layout_probe" and values[0] != LAYOUT:
                            raise ValueError("native layout observation mismatch")
                        if phase == "deadline_probe" and (values[0].get("sched_setattr_return") != 0 or values[0].get("observed_policy") != 6):
                            raise ValueError("real-time scheduling capability not established")
                    except (ValueError, AttributeError):
                        issues.append("invalid " + str(phase) + " raw observation")
                local.extend(record.get("log", "") + ": " + issue for issue in issues)
                continue
            condition = record.get("condition")
            if condition not in CONDITIONS:
                issues.append("unknown layout condition")
            command = parsed["command"] or []
            if (len(command) != 8 or Path(command[0]).name not in ("python3", "python3.6") or
                    Path(command[1]).name != DRIVERS.get(condition) or
                    command[2:] != ["-y", "-d", "3", "-f", "10000", "./" + case + "_bad"]):
                issues.append("workload command differs from the declared condition or parameters")
            if record.get("binary_sha256") != binary_hash or record.get("timeout_seconds") != 120:
                issues.append("trial binary or timeout differs from captured design")
            for metric in ("schedules", "first_error", "buggy_schedules", "error_event_count", "inner_timeouts", "complete_markers", "budget_reached"):
                if record.get(metric) != parsed[metric]:
                    issues.append("independent recount disagrees with recorded " + metric)
            footer = parsed["runner"]
            complete = bool(footer and footer["exit_code"] == 0 and not footer["timed_out"] and parsed["complete_markers"])
            if record.get("status") != ("complete" if complete else "incomplete"):
                issues.append("recorded completion disagrees with independent completion")
            reset_name = record.get("reset_log", "")
            reset_text = required_file(directory, reset_name, manifest, issues)
            if hashlib.sha256(reset_text.encode()).hexdigest() != record.get("reset_log_sha256"):
                issues.append("pre-trial reset hash disagrees with record")
            try:
                reset = json.loads(reset_text)
            except ValueError:
                reset = None
            check_reset(reset, issues, "before trial")
            check_reset(record.get("cleanup_after"), issues, "after trial")
            sequence, sequence_hash = [], None
            sequence_payload_complete = True
            try:
                sequence, sequence_hash = schedule_sequence(text)
            except (ValueError, SyntaxError):
                sequence_payload_complete = False
                if complete:
                    issues.append("requested schedule payload cannot be decoded in a complete invocation")
                # A killed process can leave the last printed request truncated.
                # Keep the raw ordinal prefix and observed failures, but do not
                # manufacture a requested-sequence hash from incomplete bytes.
            labels = re.findall(r"\[Error Found\]:\s*NO\.\d+\s+([^\x1b\r\n]+)", text)
            if labels != record.get("error_labels"):
                issues.append("error label record differs from raw log")
            coverage_hashes = [int(value) for value in re.findall(r"(?m)^coverage_hashID:[ \t]*(-?\d+)[ \t]*$", ANSI.sub("", text))]
            trial = {key: record.get(key) for key in ("case", "condition", "repeat", "position", "started_utc",
                     "finished_utc", "exit_code", "timed_out", "elapsed_seconds", "binary_sha256")}
            trial.update({key: parsed[key] for key in ("schedules", "first_error", "buggy_schedules", "error_event_count", "inner_timeouts")})
            trial.update(log=str((directory / record["log"]).relative_to(batch)), log_sha256=actual_hash,
                         complete=complete, eligible=False, integrity_ok=not issues, issues=issues,
                         schedule_sequence_sha256=sequence_hash, error_labels=sorted(set(labels)),
                         assertion_error_events=sum(label.strip() == "assertion failed" for label in labels),
                         other_error_events=sum(label.strip() != "assertion failed" for label in labels),
                         coverage_hash_ids=coverage_hashes,
                         default_coverage_hash_id=coverage_hashes[0] if len(coverage_hashes) == 1 else None,
                         coverage_hash_observation_count=len(coverage_hashes),
                         schedule_payload_complete=sequence_payload_complete,
                         prefix_schedule_count=sum(bool(row[1]) for row in sequence) if sequence_payload_complete else None,
                         cleanup_killed_before=len(reset.get("killed_target_pids", [])) if isinstance(reset, dict) else None,
                         cleanup_killed_after=len(record.get("cleanup_after", {}).get("killed_target_pids", [])),
                         budget_reached=parsed["budget_reached"], reported_round_total=parsed["reported_round_total"],
                         unexecuted_budget_sentinel=parsed["unexecuted_budget_sentinel"],
                         parse_problems=parsed["parse_problems"])
            sequences[trial["log"]] = sequence
            trials.append(trial)
            local.extend(trial["log"] + ": " + issue for issue in issues)
        errors.extend(case + ": " + issue for issue in local)
    if sorted(seen_cases) != sorted(expected_cases):
        errors.append("observed case set differs from protocol")
    # A batch with a broken design or corrupted provenance cannot supply estimates.
    for trial in trials:
        trial["eligible"] = bool(not errors and trial["complete"] and trial["integrity_ok"]
                                 and trial["inner_timeouts"] == 0 and not trial["budget_reached"])
    groups, pairs = [], []
    for case in expected_cases:
        case_trials = [r for r in trials if r["case"] == case]
        for condition in CONDITIONS:
            rows = [r for r in case_trials if r["condition"] == condition]
            eligible = [r for r in rows if r["eligible"]]
            observed = [r for r in rows if r["integrity_ok"] and not errors]
            censored = [r for r in observed if not r["eligible"]]
            group = {"case": case, "condition": condition, "planned_n": expected_repeats, "attempted_n": len(rows),
                     "missing_n": max(0, expected_repeats - len(rows)), "complete_n": sum(r["complete"] for r in rows),
                     "eligible_n": len(eligible), "outer_timeout_n": sum(r["timed_out"] is True for r in rows),
                     "inner_timeout_trials_n": sum(r["inner_timeouts"] > 0 for r in rows),
                     "budget_censored_n": sum(r["budget_reached"] for r in rows),
                     "bounded_complete_n": sum(r["complete"] and r["budget_reached"] for r in rows),
                     "detected_n": sum(r["first_error"] is not None for r in eligible),
                     "observed_detection_n": sum(r["first_error"] is not None for r in observed),
                     "observed_detection_denominator": len(observed),
                     "observed_assertion_trials_n": sum(r["assertion_error_events"] > 0 for r in observed),
                     "observed_assertion_error_events": sum(r["assertion_error_events"] for r in observed),
                     "observed_other_error_events": sum(r["other_error_events"] for r in observed),
                     "observed_error_label_trial_counts": dict(sorted(collections.Counter(label for r in observed for label in r["error_labels"]).items())),
                     "default_coverage_hash_ids": sorted(set(r["default_coverage_hash_id"] for r in observed if r["default_coverage_hash_id"] is not None)),
                     "default_coverage_observed_n": sum(r["default_coverage_hash_id"] is not None for r in observed),
                     "ambiguous_or_missing_coverage_n": sum(r["default_coverage_hash_id"] is None for r in observed),
                     "censored_or_incomplete_prefix": {"n": len(censored),
                         "interpretation": "Observed schedule requests and error events before stopping; not complete enumeration totals",
                         "printed_schedule_count": stats(r["schedules"] for r in censored),
                         "error_event_count": stats(r["error_event_count"] for r in censored),
                         "first_observed_error": stats(r["first_error"] for r in censored if r["first_error"] is not None)},
                     "first_error_condition": "eligible complete trials with an observed error; missing stays null",
                     "schedule_sequence_hashes": dict(sorted(collections.Counter(r["schedule_sequence_sha256"] for r in eligible).items()))}
            for metric in METRICS:
                group[metric] = stats(r[metric] for r in eligible if r[metric] is not None)
            groups.append(group)
        keyed = {(r["repeat"], r["condition"]): r for r in case_trials if r["eligible"]}
        matched = [(keyed[(repeat, CONDITIONS[0])], keyed[(repeat, CONDITIONS[1])]) for repeat in range(1, expected_repeats + 1)
                   if (repeat, CONDITIONS[0]) in keyed and (repeat, CONDITIONS[1]) in keyed]
        pair = {"case": case, "host_scope": batch.name + "/" + case, "n_complete_pairs": len(matched),
                "delta_orientation": "capacity3964 minus capacity1990", "same_requested_sequence_pairs": 0,
                "sequence_comparisons": [], "detection_pairs": {"both": 0, "capacity1990_only": 0, "capacity3964_only": 0, "neither": 0}}
        for metric in METRICS:
            pair[metric + "_delta"] = stats(b[metric] - a[metric] for a, b in matched if a[metric] is not None and b[metric] is not None)
        for a, b in matched:
            same = a["schedule_sequence_sha256"] == b["schedule_sequence_sha256"]
            pair["same_requested_sequence_pairs"] += same
            left, right = sequences[a["log"]], sequences[b["log"]]
            difference = next((i + 1 for i, (x, y) in enumerate(zip(left, right)) if x != y), None)
            if difference is None and len(left) != len(right):
                difference = min(len(left), len(right)) + 1
            pair["sequence_comparisons"].append({"repeat": a["repeat"], "equal": same, "first_differing_ordinal": difference})
            detected = (a["first_error"] is not None, b["first_error"] is not None)
            pair["detection_pairs"][{(True, True): "both", (True, False): "capacity1990_only", (False, True): "capacity3964_only", (False, False): "neither"}[detected]] += 1
        pairs.append(pair)
    return {"schema_version": 1, "batch": batch.name, "upstream_pin": PIN, "integrity_ok": not errors,
            "integrity_errors": errors, "design": {"cases": list(expected_cases), "repetitions_per_condition": expected_repeats,
                "conditions": list(CONDITIONS), "expected_workload_attempts": len(expected_cases) * expected_repeats * 2,
                "order": "Odd repetition AB; even repetition BA", "same_host_scope": "Within one case and batch only",
                "eligible_rule": "Complete, intact provenance/design, no inner/outer timeout, no schedule-budget censoring"},
            "denominators": {"planned_workload_attempts": len(expected_cases) * expected_repeats * 2,
                "workload_attempts": len(trials), "workload_complete": sum(r["complete"] for r in trials),
                "workload_eligible": sum(r["eligible"] for r in trials), "complete_pairs": sum(p["n_complete_pairs"] for p in pairs)},
            "provenance": provenance, "groups": groups, "paired_comparisons": pairs, "trials": trials,
            "warnings": ["Requested schedule hashes describe printed requests, not observed memory-operation traces.",
                "Synthetic sentinel and native layout probes are excluded from workload denominators.",
                "The default coverage hash is auxiliary stdout evidence; it is reported only when exactly one such value appears. All values remain in each trial record.",
                "Capacity can change a local outcome without explaining the historical paper discrepancy.",
                "Repeated trials on one host may be dependent; descriptive means and sample SD are reported.",
                "All estimates are withheld if any batch integrity or design check fails.",
                "A complete driver invocation may end at its schedule budget; bounded completions are excluded from complete-enumeration estimates.",
                "Binary hashes are captured before each call; executables are not retained in the archive."],
            "archive_manifest_file_count": len(archive_entries)}


def write_outputs(summary, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    fields = ("case", "condition", "repeat", "position", "started_utc", "finished_utc", "exit_code", "timed_out",
              "complete", "eligible", "integrity_ok", "schedules", "first_error", "buggy_schedules", "inner_timeouts",
              "elapsed_seconds", "schedule_sequence_sha256", "schedule_payload_complete", "prefix_schedule_count", "cleanup_killed_before",
              "cleanup_killed_after", "assertion_error_events", "other_error_events", "budget_reached",
              "reported_round_total", "unexecuted_budget_sentinel", "default_coverage_hash_id",
              "coverage_hash_observation_count", "binary_sha256", "log", "log_sha256", "issues")
    with (output / "all_trials.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in summary["trials"]:
            value = {key: row.get(key) for key in fields}
            value["issues"] = "; ".join(row["issues"])
            if valid_time(value["elapsed_seconds"]):
                value["elapsed_seconds"] = format(value["elapsed_seconds"], ".9f")
            writer.writerow(value)
    def cell(value):
        if value["mean"] is None:
            return "unavailable (n=0)"
        return "{:.6f} ± {} (n={})".format(value["mean"], "undefined" if value["sample_sd"] is None else "{:.6f}".format(value["sample_sd"]), value["n"])
    lines = ["# Registered capacity-layout study", "", "Batch: `" + summary["batch"] + "`.", "",
             "Audited case scope: " + ", ".join("`" + case + "`" for case in summary["design"]["cases"]) +
             "; planned repetitions per condition: " + str(summary["design"]["repetitions_per_condition"]) + ".",
             "The denominators below apply to this stated scope only.", "",
             "Integrity checks: **" + ("PASS" if summary["integrity_ok"] else "FAIL; estimates withheld") + "**.", "",
             "Actual denominators: `" + json.dumps(summary["denominators"], sort_keys=True) + "`.", "",
             "## Outcomes by case and condition", "", "All values are mean ± sample SD, with actual n. First error is conditional on an observed error.", "",
             "| Case | Condition | Complete / attempted | Eligible | Schedules | First error | Buggy schedules | Whole-driver seconds |",
             "| --- | --- | ---: | ---: | --- | --- | --- | --- |"]
    for group in summary["groups"]:
        lines.append("| {} | {} | {} / {} | {} | {} | {} | {} | {} |".format(group["case"], group["condition"], group["complete_n"], group["attempted_n"], group["eligible_n"], *(cell(group[m]) for m in METRICS)))
    lines += ["", "## Observed outcomes including bounded and incomplete calls", "",
              "An observed assertion before a timeout or schedule-budget stop remains an observation. Prefix counts are not completed enumeration totals. Error events can repeat the same program defect.", "",
              "| Case | Condition | Any error observed / intact attempts | Assertion observed | Other error events | Outer / inner timeout trials | Budget reached | Incomplete or censored prefix schedules |",
              "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |"]
    for group in summary["groups"]:
        lines.append("| {} | {} | {} / {} | {} | {} | {} / {} | {} | {} |".format(
            group["case"], group["condition"], group["observed_detection_n"], group["observed_detection_denominator"],
            group["observed_assertion_trials_n"], group["observed_other_error_events"], group["outer_timeout_n"],
            group["inner_timeout_trials_n"], group["budget_censored_n"], cell(group["censored_or_incomplete_prefix"]["printed_schedule_count"])))
    lines += ["", "## Within-case paired changes", "", "Differences are capacity3964 minus capacity1990. Missing or censored arms are excluded from paired estimates.", "",
              "| Case | Eligible pairs | Schedule delta | First-error delta | Buggy-schedule delta | Seconds delta | Equal requested sequences |",
              "| --- | ---: | --- | --- | --- | --- | ---: |"]
    for pair in summary["paired_comparisons"]:
        lines.append("| {} | {} | {} | {} | {} | {} | {} / {} |".format(pair["case"], pair["n_complete_pairs"], *(cell(pair[m + "_delta"]) for m in METRICS), pair["same_requested_sequence_pairs"], pair["n_complete_pairs"]))
    lines += ["", "## Auxiliary coverage feedback observations", "",
              "These values are recounted from existing stdout. They are separate from the prespecified primary outcomes and do not establish an executed memory-operation trace.", "",
              "| Case | Condition | Unique default coverage hashes | Unambiguous observations | Missing or multiple observations |",
              "| --- | --- | --- | ---: | ---: |"]
    for group in summary["groups"]:
        lines.append("| {} | {} | {} | {} | {} |".format(group["case"], group["condition"],
            ", ".join(str(value) for value in group["default_coverage_hash_ids"]) or "unavailable",
            group["default_coverage_observed_n"], group["ambiguous_or_missing_coverage_n"]))
    lines += ["", "## Interpretation limits", ""] + ["- " + item for item in summary["warnings"]]
    if summary["integrity_errors"]:
        lines += ["", "## Integrity findings", ""] + ["- " + item for item in summary["integrity_errors"]]
    (output / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def check_outputs(summary, output):
    output = Path(output)
    def compare(a, b):
        if isinstance(a, dict) and isinstance(b, dict):
            return set(a) == set(b) and all(compare(a[k], b[k]) for k in a)
        if isinstance(a, list) and isinstance(b, list):
            return len(a) == len(b) and all(compare(x, y) for x, y in zip(a, b))
        if type(a) in (int, float) and type(b) in (int, float):
            return math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12)
        return type(a) is type(b) and a == b
    if not compare(summary, json.loads((output / "summary.json").read_text(encoding="utf-8"))):
        raise ValueError("published summary differs from independent recount")
    with tempfile.TemporaryDirectory(prefix="layout-audit-") as temp:
        write_outputs(summary, temp)
        for name in ("all_trials.csv", "SUMMARY.md"):
            if (Path(temp) / name).read_bytes() != (output / name).read_bytes():
                raise ValueError(name + ": published content differs from independent recount")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cases", choices=CASES, nargs="+", default=list(CASES))
    parser.add_argument("--repeats", type=int, default=10)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.repeats < 1 or len(args.cases) != len(set(args.cases)):
        parser.error("Positive repetitions and unique cases required")
    batch, output = args.batch.resolve(), args.output.resolve()
    if output == batch or batch in output.parents:
        parser.error("Summary output must be outside immutable raw evidence")
    summary = summarize_batch(batch, args.cases, args.repeats)
    if args.check:
        try:
            check_outputs(summary, output)
        except (ValueError, OSError) as error:
            summary["integrity_ok"] = False
            summary["integrity_errors"].append(str(error))
    else:
        write_outputs(summary, output)
    print(json.dumps({key: summary[key] for key in ("integrity_ok", "denominators", "integrity_errors")}, indent=2))
    return 0 if summary["integrity_ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
