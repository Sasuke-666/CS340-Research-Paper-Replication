"""Small independent evidence fixtures for real layout-audit failure modes."""
import difflib
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import summarize_layout as audit

ORIGINAL = "# synthetic fixture driver\nSHARE_ARRAY_SIZE = 1990\nscheduler_unchanged = True\n"
CORRECTED = "# synthetic fixture driver\nSHARE_ARRAY_SIZE = 3964\nscheduler_unchanged = True\n"
RUNTIME = ("#define SHARE_MEMORY_THREAD_NUM 100\n#define SHARE_MEMORY_ARRAY_SIZE 3964\n"
           "typedef struct Sched_Info { int synthetic_fixture; } sched_info;\n")


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def manifest(directory):
    write_json(directory / "manifest.json", {"files": [
        {"path": path.relative_to(directory).as_posix(), "bytes": path.stat().st_size,
         "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        for path in sorted(directory.rglob("*")) if path.is_file() and path.name != "manifest.json"]})


def reset():
    return {"key_absent": True, "post_shmget": -1, "post_errno": 2,
            "previous_shmid": -1, "previous_errno": 2, "previous_segment": None, "killed_target_pids": []}


def fixture(batch, incomplete=False):
    directory = batch / "account"
    source = directory / "source"
    source.mkdir(parents=True)
    for name, text in (("run_PDS.py", ORIGINAL), ("run_PDS_layout3964.py", CORRECTED),
                       ("DBDSFunction.cpp", RUNTIME), ("runtime_layout_probe.cpp", RUNTIME)):
        (source / name).write_text(text, encoding="utf-8")
    (directory / "capacity.diff").write_text("".join(difflib.unified_diff(
        ORIGINAL.splitlines(True), CORRECTED.splitlines(True),
        fromfile="upstream/run_PDS.py", tofile="adapted/run_PDS_layout3964.py")), encoding="utf-8")
    write_json(directory / "capacity_change.json", {"original_sha256": sha(ORIGINAL),
               "adapted_sha256": sha(CORRECTED), "runtime_sha256": sha(RUNTIME)})
    write_json(directory / "runtime_layout.json", {"observed_layout": audit.LAYOUT,
               "runtime_source_sha256": sha(RUNTIME), "probe_source_sha256": sha(RUNTIME)})
    write_json(directory / "synthetic_decode_probe.json", {"conditions": {
        "capacity1990": {"decoded_location": 101, "decoded_order": 202},
        "capacity3964": {"decoded_location": 202, "decoded_order": 303}}})
    write_json(directory / "environment.json", {"source_commit": audit.PIN, "same_built_binary": True,
        "binary_sha256": "a" * 64, "settings": {"depth": 3, "schedule_budget": 10000,
            "repetitions_per_condition": 2, "outer_timeout_seconds": 120},
        "drivers": {"capacity1990": sha(ORIGINAL), "capacity3964": sha(CORRECTED)},
        "cpu_models": ["synthetic fixture CPU"], "cpu_affinity": [0], "platform": "synthetic fixture Linux"})
    records = []

    def add(phase, command, payload, elapsed=0.1, timed_out=False, **metadata):
        ordinal = len(records)
        started = "2026-11-14T00:{:02d}:00+00:00".format(ordinal)
        finished = "2026-11-14T00:{:02d}:30+00:00".format(ordinal)
        name = phase + "_" + str(ordinal) + ".txt"
        code = -9 if timed_out else 0
        text = ("Started UTC: " + started + "\nCommand: " + json.dumps(command) + "\n" + payload +
                "\nRunner exit_code={} timed_out={} elapsed_seconds={:.6f}\n".format(code, timed_out, elapsed))
        (directory / name).write_text(text, encoding="utf-8")
        record = {"phase": phase, "case": "account", "command": command, "started_utc": started,
                  "finished_utc": finished, "log": name, "log_sha256": sha(text), "exit_code": code,
                  "timed_out": timed_out, "elapsed_seconds": elapsed, **metadata}
        records.append(record)

    add("layout_probe_build", ["g++", "fixture.cpp"], "")
    add("layout_probe", ["fixture-layout"], json.dumps(audit.LAYOUT))
    add("deadline_probe", ["python3", "-c", "fixture"], json.dumps({"sched_setattr_return": 0, "observed_policy": 6}))
    add("build", ["bash", "build.sh"], "")
    # AB/BA, with manually chosen B-A deltas: +2s, +2s and -1 first-error index.
    settings = [(1, "capacity1990", 1, 3.0), (1, "capacity3964", 2, 5.0),
                (2, "capacity3964", 1, 7.0), (2, "capacity1990", 2, 5.0)]
    write_json(directory / "planned_trials.json", [{"phase": "layout", "case": "account", "repeat": r,
               "condition": c, "position": p} for r, c, p, _ in settings])
    for repetition, condition, position, elapsed in settings:
        timed_out = incomplete and repetition == 1 and condition == "capacity3964"
        first = 2 if condition == "capacity1990" else 1
        lines = ["coverage_hashID: " + ("17" if condition == "capacity1990" else "23")]
        for number in range(1, 4):
            lines.append("test {:04d}: [[0], [1]]".format(number))
            if number == first:
                lines.append("[Error Found]: NO.1 assertion failed")
        if not timed_out:
            lines += ["End Testing!", "Total Error Interleavings: 1", "Total Timeouts Interleavings: 0", "Round 0 3"]
        reset_name = "{}_r{}_reset.json".format(condition, repetition)
        write_json(directory / reset_name, reset())
        add("layout", ["python3", "/source/" + audit.DRIVERS[condition], "-y", "-d", "3", "-f", "10000", "./account_bad"],
            "\n".join(lines), elapsed, timed_out, condition=condition, repeat=repetition, position=position,
            binary_sha256="a" * 64, timeout_seconds=120, schedules=3, first_error=first,
            buggy_schedules=None if timed_out else 1, error_event_count=1, inner_timeouts=0,
            budget_reached=False,
            complete_markers=not timed_out, status="incomplete" if timed_out else "complete",
            error_labels=["assertion failed"], reset_log=reset_name,
            reset_log_sha256=audit.digest(directory / reset_name), cleanup_after=reset())
    write_json(directory / "records.json", records)
    manifest(directory)
    return directory


class LayoutAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.batch = Path(self.temp.name) / "batch"
        # Tiny fixtures have their own explicit source pins; production pins remain fixed.
        self.pins = patch.multiple(audit, PINNED_DRIVER_SHA256=sha(ORIGINAL), PINNED_RUNTIME_SHA256=sha(RUNTIME))
        self.pins.start()
        self.addCleanup(self.pins.stop)

    def summarize(self):
        return audit.summarize_batch(self.batch, ("account",), 2)

    def test_manual_pairs_and_read_only_published_check(self):
        fixture(self.batch)
        result = self.summarize()
        self.assertTrue(result["integrity_ok"], result["integrity_errors"])
        pair = result["paired_comparisons"][0]
        self.assertEqual(pair["elapsed_seconds_delta"], {"n": 2, "mean": 2.0, "sample_sd": 0.0, "min": 2.0, "max": 2.0})
        self.assertEqual(pair["first_error_delta"]["mean"], -1)
        self.assertEqual(pair["same_requested_sequence_pairs"], 2)
        self.assertEqual(result["groups"][0]["default_coverage_hash_ids"], [17])
        self.assertEqual(result["groups"][1]["default_coverage_hash_ids"], [23])
        out = Path(self.temp.name) / "summary"
        audit.write_outputs(result, out)
        audit.check_outputs(result, out)
        (out / "SUMMARY.md").write_text("altered", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "published content"):
            audit.check_outputs(result, out)
        self.assertEqual((out / "SUMMARY.md").read_text(), "altered")

    def test_missing_trial_and_wrong_condition_fail_closed(self):
        directory = fixture(self.batch)
        records = json.loads((directory / "records.json").read_text())
        records.pop()
        records[-1]["condition"] = "capacity1990"
        write_json(directory / "records.json", records)
        manifest(directory)
        result = self.summarize()
        self.assertFalse(result["integrity_ok"])
        self.assertEqual(result["denominators"]["workload_attempts"], 3)
        self.assertEqual(result["denominators"]["workload_eligible"], 0)
        self.assertTrue(any("AB/BA" in item for item in result["integrity_errors"]))

    def test_raw_log_corruption_is_detected_without_rewriting(self):
        directory = fixture(self.batch)
        path = directory / "layout_4.txt"
        path.write_text(path.read_text().replace("assertion failed", "driver crashed"))
        result = self.summarize()
        self.assertFalse(result["integrity_ok"])
        self.assertTrue(any("hash" in item or "manifest content mismatch" in item for item in result["integrity_errors"]))
        self.assertIn("driver crashed", path.read_text())
        self.assertEqual(result["denominators"]["workload_eligible"], 0)

    def test_cleaned_manifest_cannot_hide_binary_or_source_change(self):
        directory = fixture(self.batch)
        records = json.loads((directory / "records.json").read_text())
        records[4]["binary_sha256"] = "b" * 64
        write_json(directory / "records.json", records)
        path = directory / "source/run_PDS_layout3964.py"
        path.write_text(CORRECTED + "scheduler_unchanged = False\n")
        manifest(directory)
        result = self.summarize()
        self.assertFalse(result["integrity_ok"])
        self.assertTrue(any("one registered capacity" in item for item in result["integrity_errors"]))
        self.assertTrue(any("trial binary" in item for item in result["integrity_errors"]))
        self.assertEqual(result["denominators"]["complete_pairs"], 0)

    def test_attached_segment_cannot_be_declared_clean(self):
        directory = fixture(self.batch)
        records = json.loads((directory / "records.json").read_text())
        path = directory / records[4]["reset_log"]
        data = reset()
        data.update(previous_shmid=4, previous_errno=0, previous_segment={"key": "1111", "shmid": "4", "nattch": "1"})
        write_json(path, data)
        records[4]["reset_log_sha256"] = audit.digest(path)
        write_json(directory / "records.json", records)
        manifest(directory)
        result = self.summarize()
        self.assertFalse(result["integrity_ok"])
        self.assertTrue(any("attachments" in item for item in result["integrity_errors"]))
        self.assertEqual(result["denominators"]["workload_eligible"], 0)

    def test_timeout_prefix_is_retained_and_not_zero_filled(self):
        directory = fixture(self.batch, incomplete=True)
        records = json.loads((directory / "records.json").read_text())
        timed_out = next(record for record in records if record["timed_out"])
        path = directory / timed_out["log"]
        path.write_text(path.read_text().replace("test 0003: [[0], [1]]", "test 0003: [[0], [1"))
        timed_out["log_sha256"] = audit.digest(path)
        write_json(directory / "records.json", records)
        manifest(directory)
        result = self.summarize()
        self.assertTrue(result["integrity_ok"], result["integrity_errors"])
        self.assertEqual(result["denominators"]["workload_attempts"], 4)
        self.assertEqual(result["denominators"]["workload_complete"], 3)
        self.assertEqual(result["denominators"]["workload_eligible"], 3)
        self.assertEqual(result["denominators"]["complete_pairs"], 1)
        stopped = next(row for row in result["trials"] if row["timed_out"])
        self.assertEqual(stopped["schedules"], 3)
        self.assertIsNone(stopped["buggy_schedules"])
        self.assertFalse(stopped["eligible"])
        self.assertFalse(stopped["schedule_payload_complete"])
        self.assertIsNone(stopped["schedule_sequence_sha256"])
        corrected = next(group for group in result["groups"] if group["condition"] == "capacity3964")
        self.assertEqual(corrected["observed_detection_n"], 2)
        self.assertEqual(corrected["observed_assertion_trials_n"], 2)
        self.assertEqual(corrected["censored_or_incomplete_prefix"]["printed_schedule_count"]["mean"], 3)

    def test_crlf_source_hashes_preserve_exact_bytes(self):
        directory = fixture(self.batch)
        original = ORIGINAL.replace("\n", "\r\n")
        corrected = CORRECTED.replace("\n", "\r\n")
        runtime = RUNTIME.replace("\n", "\r\n")
        for name, data in (("run_PDS.py", original), ("run_PDS_layout3964.py", corrected), ("DBDSFunction.cpp", runtime)):
            (directory / "source" / name).write_bytes(data.encode())
        patch_text = "".join(difflib.unified_diff(original.splitlines(True), corrected.splitlines(True),
                             fromfile="upstream/run_PDS.py", tofile="adapted/run_PDS_layout3964.py"))
        (directory / "capacity.diff").write_bytes(patch_text.encode())
        environment = json.loads((directory / "environment.json").read_text())
        environment["drivers"] = {"capacity1990": sha(original), "capacity3964": sha(corrected)}
        write_json(directory / "environment.json", environment)
        write_json(directory / "capacity_change.json", {"original_sha256": sha(original), "adapted_sha256": sha(corrected), "runtime_sha256": sha(runtime)})
        write_json(directory / "runtime_layout.json", {"observed_layout": audit.LAYOUT,
                   "runtime_source_sha256": sha(runtime), "probe_source_sha256": sha(RUNTIME)})
        manifest(directory)
        with patch.multiple(audit, PINNED_DRIVER_SHA256=sha(original), PINNED_RUNTIME_SHA256=sha(runtime)):
            result = self.summarize()
        self.assertTrue(result["integrity_ok"], result["integrity_errors"])
        self.assertNotEqual(sha(runtime), sha(RUNTIME))

    def test_budget_label_is_not_an_executed_schedule(self):
        # Pinned source prints ordinal 4 before the budget=3 guard, then exits.
        # Only three schedule requests exist; the raw Round footer still says 4.
        text = ("Started UTC: 2026-11-14T00:00:00+00:00\nCommand: [\"python3\"]\n"
                "test 0001: [[0], [1]]\ntest 0002: [[1], [0]]\n"
                "[Error Found]: NO.1 assertion failed\n"
                "test 0003: [[0, 1]]\ntest 0004: End Testing!\n"
                "Total Error Interleavings: 1\nTotal Timeouts Interleavings: 0\nRound 0 4\n"
                "Runner exit_code=0 timed_out=False elapsed_seconds=1.000000\n")
        parsed = audit.parse_layout_log(text, budget=3)
        self.assertTrue(parsed["complete_markers"], parsed["parse_problems"])
        self.assertTrue(parsed["budget_reached"])
        self.assertTrue(parsed["unexecuted_budget_sentinel"])
        self.assertEqual(parsed["schedules"], 3)
        self.assertEqual(parsed["reported_round_total"], 4)
        self.assertEqual(parsed["first_error"], 2)
        wrong = audit.parse_layout_log(text.replace("Round 0 4", "Round 0 5"), budget=3)
        self.assertFalse(wrong["complete_markers"])


if __name__ == "__main__":
    unittest.main()
