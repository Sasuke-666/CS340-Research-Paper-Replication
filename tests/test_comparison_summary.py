"""Numerical and integrity checks from independent, small raw-log fixtures."""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "summarize_comparison.py"
SPEC = importlib.util.spec_from_file_location("comparison_summary", MODULE)
summary = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(summary)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def raw_log(command, count, failures, elapsed, exit_code=0, complete=True,
            started="2026-11-07T00:00:00+00:00"):
    # Expected values are specified directly by each test, independently of the parser.
    lines = ["Started UTC: " + started, "Command: " + json.dumps(command)]
    if complete:
        error_number = 0
        for ordinal in range(1, count + 1):
            prefix = " for prefix [0, 1]" if ordinal == 2 else ""
            lines.append("\x1b[4;36mtest {:04d}{}:\x1b[0m [[0], [1]]".format(ordinal, prefix))
            if ordinal in failures:
                error_number += 1
                lines.append("\x1b[31m\t[Error Found]: NO.{} assertion failed\x1b[0m".format(error_number))
        lines += ["End Testing!", "Total Error Interleavings: " + str(len(failures)),
                  "Total Timeouts Interleavings: 0", "Round\t0\t\t" + str(count)]
    else:
        lines.append("driver terminated before enumeration")
    lines.append("Runner exit_code={} timed_out=False elapsed_seconds={:.6f}".format(exit_code, elapsed))
    return "\n".join(lines) + "\n"


def refresh_manifest(directory):
    entries = [{"path": str(p.relative_to(directory)), "bytes": p.stat().st_size, "sha256": sha(p)}
               for p in sorted(directory.rglob("*")) if p.is_file() and p.name != "manifest.json"]
    (directory / "manifest.json").write_text(json.dumps({"files": entries}), encoding="utf-8")


def fixture(batch, fail_serial=False, serial="author_serialized_abi16"):
    directory = batch / "twostage"
    (directory / "source").mkdir(parents=True)
    driver_names = {"period": "run_PDS.py", serial: "run_OldPDS_abi16.py" if "abi16" in serial else "run_OldPDS.py"}
    drivers = {}
    for method, name in driver_names.items():
        source = directory / "source" / name
        source.write_text("# independent fixture: " + method + "\n", encoding="utf-8")
        drivers[method] = sha(source)
    environment = {"source_commit": summary.PIN, "binary_sha256": "a"*64,
        "paired_methods_same_built_binary": True, "drivers": drivers,
        "cpu_models": ["fixture CPU"], "cpu_affinity": [0, 1], "platform": "fixture Linux"}
    (directory / "environment.json").write_text(json.dumps(environment), encoding="utf-8")
    # P1,S1,S2,P2; exact expected paired differences are 2 s and 2 s.
    specifications = [(1, "period", 1, 3, [2, 3], 2.0),
                      (1, serial, 2, 6, [3], 4.0),
                      (2, serial, 1, 8, [], 6.0),
                      (2, "period", 2, 4, [1], 4.0)]
    records = []
    for index, (repeat, method, position, count, failures, elapsed) in enumerate(specifications):
        failed = fail_serial and method == serial and repeat == 1
        code = -11 if failed else 0
        if failed:
            elapsed, count, failures = 0.3, 0, []
        command = ["python3", "/source/" + driver_names[method], "-y", "-d", "3", "-f", "10000", "./twostage_bad"]
        name = "{}_r{:02d}.txt".format(method, repeat)
        path = directory / name
        started = "2026-11-07T00:00:{:02d}+00:00".format(index)
        path.write_text(raw_log(command, count, failures, elapsed, code, not failed, started), encoding="utf-8")
        records.append({"case": "twostage", "phase": "comparison", "method": method,
            "repeat": repeat, "position": position, "started_utc": started,
            "exit_code": code, "timed_out": False, "elapsed_seconds": elapsed,
            "log": name, "log_sha256": sha(path), "command": command,
            "schedules": count, "first_error": failures[0] if failures else None,
            "buggy_schedules": None if failed else len(failures), "error_event_count": len(failures),
            "inner_timeouts": 0, "complete_markers": not failed,
            "status": "incomplete" if failed else "complete"})
    (directory / "records.json").write_text(json.dumps(records), encoding="utf-8")
    refresh_manifest(directory)
    return directory


class RawLogTests(unittest.TestCase):
    def test_ansi_prefix_and_event_numbers(self):
        result = summary.parse_raw_log(raw_log(["runner"], 3, [2, 3], 1.25))
        self.assertTrue(result["complete_markers"], result["parse_problems"])
        self.assertEqual((result["schedules"], result["first_error"], result["buggy_schedules"]), (3, 2, 2))
        self.assertEqual(result["runner"]["elapsed_seconds"], 1.25)

    def test_gap_in_schedule_ordinals_is_rejected(self):
        text = raw_log(["runner"], 3, [2], 1.0).replace("test 0003:", "test 0004:")
        result = summary.parse_raw_log(text)
        self.assertFalse(result["complete_markers"])
        self.assertIn("schedule ordinals are not exactly 1..N", result["parse_problems"])

    def test_inconsistent_footer_is_rejected(self):
        text = raw_log(["runner"], 3, [2, 3], 1.0).replace("Error Interleavings: 2", "Error Interleavings: 1")
        self.assertFalse(summary.parse_raw_log(text)["complete_markers"])

    def test_unattributed_error_is_rejected(self):
        text = "[Error Found]: NO.1 assertion failed\n" + raw_log(["runner"], 3, [], 1.0)
        result = summary.parse_raw_log(text)
        self.assertIn("unattributed or repeated error event", result["parse_problems"])

    def test_crash_preserves_null_outcome(self):
        result = summary.parse_raw_log(raw_log(["runner"], 0, [], 0.3, -11, False))
        self.assertEqual(result["runner"]["exit_code"], -11)
        self.assertIsNone(result["first_error"])
        self.assertIsNone(result["buggy_schedules"])
        self.assertFalse(result["complete_markers"])

    def test_replay_target_failure_is_separate_from_wrapper_success(self):
        text = ('Command: ["runner"]\n'
                "case: source.c:80: checkThread: Assertion `0' failed.\n"
                'CS340_REPLAY {"target_returncode": -6, "calibrated_period": 5000, "scale": 1.5}\n'
                'Runner exit_code=0 timed_out=False elapsed_seconds=1.000000\n')
        result = summary.parse_raw_log(text)
        self.assertEqual(result["runner"]["exit_code"], 0)
        self.assertEqual(result["target_observation"]["target_returncode"], -6)
        self.assertTrue(result["expected_assertion"])

    def test_replay_successful_target_does_not_establish_assertion(self):
        text = ('Command: ["runner"]\n'
                'CS340_REPLAY {"target_returncode": 0, "calibrated_period": 5000, "scale": 6.0}\n'
                'Runner exit_code=0 timed_out=False elapsed_seconds=1.000000\n')
        result = summary.parse_raw_log(text)
        self.assertEqual(result["target_observation"]["target_returncode"], 0)
        self.assertFalse(result["expected_assertion"])


class StatisticsTests(unittest.TestCase):
    def test_sample_sd_and_empty_denominators(self):
        result = summary.stats([2, 4])
        self.assertEqual(result["mean"], 3)
        self.assertAlmostEqual(result["sample_sd"], math.sqrt(2))
        self.assertIsNone(summary.stats([])["mean"])
        self.assertIsNone(summary.stats([3])["sample_sd"])

    def test_wilson_and_paired_exact_test(self):
        interval = summary.wilson(20, 20)
        self.assertAlmostEqual(interval["lower_95"], 0.8388748419471806)
        self.assertAlmostEqual(interval["upper_95"], 1.0)
        self.assertAlmostEqual(summary.exact_mcnemar(0, 5), 0.0625)
        self.assertEqual(summary.exact_mcnemar(0, 0), 1.0)

    def test_paper_gaps(self):
        gap = summary.paper_gap(9, 6)
        self.assertEqual(gap["signed_gap"], 3)
        self.assertEqual(gap["relative_gap_pct"], 50)
        self.assertEqual(summary.paper_gap(3, 6)["absolute_gap"], 3)
        self.assertIsNone(summary.paper_gap(None, 6)["relative_gap_pct"])


class BatchTests(unittest.TestCase):
    def run_fixture(self, batch):
        return summary.summarize_batch(batch, expected_repeats=2, expected_cases=("twostage",))

    def test_manual_numeric_recount_and_pairs(self):
        with tempfile.TemporaryDirectory() as temp:
            batch = Path(temp)
            fixture(batch)
            result = self.run_fixture(batch)
            self.assertTrue(result["integrity_ok"], result["integrity_errors"])
            groups = {r["method"]: r for r in result["groups"]}
            period, serial = groups["period"], groups["author_serialized_abi16"]
            self.assertEqual(period["schedules"]["mean"], 3.5)
            self.assertAlmostEqual(period["schedules"]["sample_sd"], math.sqrt(0.5))
            self.assertEqual(period["first_error"]["mean"], 1.5)
            self.assertEqual(serial["first_error"]["n"], 1)
            self.assertEqual(serial["first_error"]["mean"], 3)
            self.assertEqual(serial["detected_n"], 1)
            self.assertEqual(serial["eligible_n"], 2)
            paired = result["paired_comparisons"][0]
            self.assertEqual(paired["n_complete_pairs"], 2)
            self.assertEqual(paired["schedule_reduction_pct"]["mean"], 50)
            self.assertEqual(paired["serial_minus_period_seconds"]["mean"], 2)
            self.assertEqual(paired["serial_minus_period_seconds"]["sample_sd"], 0)
            self.assertEqual(paired["serial_over_period_time_ratio"]["mean"], 1.75)
            self.assertAlmostEqual(paired["serial_over_period_time_ratio"]["sample_sd"], math.sqrt(0.125))

    def test_legacy_failure_is_not_zero_result(self):
        with tempfile.TemporaryDirectory() as temp:
            batch = Path(temp)
            fixture(batch, fail_serial=True, serial="author_serialized")
            result = self.run_fixture(batch)
            self.assertTrue(result["integrity_ok"], result["integrity_errors"])
            serial = next(g for g in result["groups"] if g["method"] == "author_serialized")
            self.assertEqual((serial["attempted_n"], serial["complete_n"], serial["incomplete_n"]), (2, 1, 1))
            self.assertEqual(serial["schedules"]["mean"], 8)
            self.assertEqual(serial["elapsed_seconds"]["mean"], 6)
            self.assertIsNone(serial["first_error"]["mean"])
            self.assertEqual(result["paired_comparisons"][0]["n_complete_pairs"], 1)

    def test_record_hash_is_checked_independently_of_manifest(self):
        with tempfile.TemporaryDirectory() as temp:
            batch = Path(temp)
            directory = fixture(batch)
            path = directory / "period_r01.txt"
            path.write_text(path.read_text(encoding="utf-8") + "extra line\n", encoding="utf-8")
            refresh_manifest(directory)
            result = self.run_fixture(batch)
            self.assertFalse(result["integrity_ok"])
            self.assertTrue(any("record log SHA256 mismatch" in e for e in result["integrity_errors"]))

    def test_manifest_binary_and_order_are_checked(self):
        with tempfile.TemporaryDirectory() as temp:
            batch = Path(temp)
            directory = fixture(batch)
            records_path = directory / "records.json"
            records = json.loads(records_path.read_text())
            records[0]["position"] = 2
            records[0]["binary_sha256"] = "b"*64
            records_path.write_text(json.dumps(records), encoding="utf-8")
            result = self.run_fixture(batch)
            self.assertFalse(result["integrity_ok"])
            self.assertTrue(any("manifest content mismatch" in e for e in result["integrity_errors"]))
            self.assertTrue(any("AB/BA" in e for e in result["integrity_errors"]))
            self.assertTrue(any("binary hash differs" in e for e in result["integrity_errors"]))

    def test_published_summary_is_audited_without_rewriting(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            batch, output = root / "batch", root / "summary"
            fixture(batch)
            result = self.run_fixture(batch)
            summary.write_outputs(result, output)
            summary.check_outputs(result, output)
            path = output / "summary.json"
            published = json.loads(path.read_text(encoding="utf-8"))
            published["groups"][0]["schedules"]["mean"] += 1
            path.write_text(json.dumps(published), encoding="utf-8")
            altered = path.read_bytes()
            with self.assertRaisesRegex(ValueError, "published number differs"):
                summary.check_outputs(result, output)
            self.assertEqual(path.read_bytes(), altered)

    def test_outer_timeout_preserves_observed_prefix_and_excludes_completion_estimate(self):
        with tempfile.TemporaryDirectory() as temp:
            batch = Path(temp)
            directory = fixture(batch)
            records_path = directory / "records.json"
            records = json.loads(records_path.read_text(encoding="utf-8"))
            record = records[1]
            path = directory / record["log"]
            prefix = path.read_text(encoding="utf-8").split("End Testing!")[0]
            path.write_text(prefix + "Runner exit_code=-9 timed_out=True elapsed_seconds=120.000000\n", encoding="utf-8")
            record.update(exit_code=-9, timed_out=True, elapsed_seconds=120.0,
                          buggy_schedules=None, complete_markers=False, status="incomplete", log_sha256=sha(path))
            records_path.write_text(json.dumps(records), encoding="utf-8")
            refresh_manifest(directory)
            result = self.run_fixture(batch)
            self.assertTrue(result["integrity_ok"], result["integrity_errors"])
            serial = next(g for g in result["groups"] if g["method"] == "author_serialized_abi16")
            self.assertEqual(serial["outer_timeout_n"], 1)
            self.assertEqual(serial["eligible_n"], 1)
            self.assertEqual(serial["schedules"]["mean"], 8)
            self.assertEqual(serial["elapsed_seconds"]["mean"], 6)
            observed = serial["incomplete_observations"]
            self.assertEqual(observed["printed_schedules"]["mean"], 6)
            self.assertEqual(observed["observed_first_error"]["mean"], 3)
            self.assertEqual(observed["elapsed_before_stop_seconds"]["mean"], 120)

    def test_cli_case_and_repetition_design_survives_read_only_audit(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            batch, output = root / "batch", root / "summary"
            fixture(batch)
            command = [sys.executable, str(MODULE), str(batch), "--output", str(output),
                       "--cases", "twostage", "--repeats", "2"]
            subprocess.run(command, check=True, capture_output=True, text=True)
            result = json.loads((output / "summary.json").read_text(encoding="utf-8"))
            self.assertEqual(result["design"]["cases"], ["twostage"])
            self.assertEqual(result["design"]["repetitions_per_method"], 2)
            self.assertEqual(result["design"]["expected_comparison_attempts"], 4)
            subprocess.run(command + ["--check"], check=True, capture_output=True, text=True)


if __name__ == "__main__":
    unittest.main()
