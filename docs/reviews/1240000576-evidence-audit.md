# Evidence review of the four-thread `reorder_4` follow-up

**Submitted by** 何博宇 · 1240000576 · `heboyu0714`  
**Evidence reviewed** 8 November 2026 (UTC+08:00), repository revision `9be5e176116790a40f7e55c2813f4ae8505e0461`.  
**Scope** Archived-log review. At the submitter’s request, an AI assistant read the logs, ran the recount below and drafted this record. Individual oral explanation and independent human sign-off are pending.

The raw logs support the four-thread results in Tables 3–5. In all three matched pairs, PERIOD found the assertion failure by schedule 9 and finished after 100 schedules. The compatible serialized driver first found it at schedule 47 and finished after 384 schedules. No numerical correction to these rows was identified. [Stage report](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/report/EXPANDED_REPORT.md)

## The three completed pairs

The follow-up ran the same four-thread binary on one host at depth 3 with a budget of 10,000 schedules and a 240-second outer time limit. Both builds across the two batches returned 0. Within the follow-up the execution order was PERIOD first, serialized first, then PERIOD first. Each log reached `End Testing!` with zero inner timeouts and a runner footer of `exit_code=0 timed_out=False`. All six comparison calls therefore contribute to the matched statistics. The table uses launch order. [Registered follow-up protocol](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/experiments/2026-11-07/REORDER4_TIMEOUT_FOLLOWUP.md) · [Host and binary](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42384122902/reorder_4/environment.json)

| Pair | Raw log | Explored | First failing ID | Failing schedules | Whole-driver seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | [`period_r01.txt`](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42384122902/reorder_4/period_r01.txt) | 100 | 9 | 12 | 21.278865 |
| 1 | [`author_serialized_abi16_r01.txt`](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42384122902/reorder_4/author_serialized_abi16_r01.txt) | 384 | 47 | 87 | 135.595131 |
| 2 | [`author_serialized_abi16_r02.txt`](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42384122902/reorder_4/author_serialized_abi16_r02.txt) | 384 | 47 | 87 | 135.451399 |
| 2 | [`period_r02.txt`](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42384122902/reorder_4/period_r02.txt) | 100 | 9 | 12 | 22.225299 |
| 3 | [`period_r03.txt`](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42384122902/reorder_4/period_r03.txt) | 100 | 9 | 12 | 22.025956 |
| 3 | [`author_serialized_abi16_r03.txt`](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42384122902/reorder_4/author_serialized_abi16_r03.txt) | 384 | 47 | 85 | 130.840428 |

Log directory: `results/2026-11-07/comparison-42384122902/reorder_4/`. The printed `test` IDs start at one. Each assertion event belongs to the current test ID. Distinct failing IDs count schedules that trigger an assertion, and several such schedules can expose the same defect. A run with no observed failure would have a missing first-failure ID. The distinction between target and driver matters here: every complete driver exited normally after observing target failures.

For example, in [PERIOD run 1](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42384122902/reorder_4/period_r01.txt#L37-L38), the first assertion follows `test 0009`. The footer records `elapsed_seconds=21.278865` ([line 168](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42384122902/reorder_4/period_r01.txt#L168)). The comparison row in [records.json](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42384122902/reorder_4/records.json) with `method=period` and `repeat=1` stores 21.278864712 seconds. Its command was `python3 /workdir/PERIOD/tool/DBDS/run_PDS.py -y -d 3 -f 10000 ./reorder_4_bad`. The code below checks log hashes against both the manifest and the run records, and recounts the events directly from each log.

## Recalculation and report checks

Each cell is the arithmetic mean ± sample standard deviation for three runs. For values x₁, x₂, x₃, the sample variance is the sum of squared deviations from the mean divided by two. Calculations use the unrounded `elapsed_seconds` values in the run records.

| Measure | PERIOD | `author_serialized_abi16` |
| --- | ---: | ---: |
| Explored schedules | 100 ± 0 | 384 ± 0 |
| First failing schedule | 9 ± 0 | 47 ± 0 |
| Failing schedules | 12 ± 0 | 86.333 ± 1.155 |
| Whole-driver time (s) | 21.843 ± 0.499 | 133.962 ± 2.705 |

- **Table 3.** The compatible serialized counts of 87, 87 and 85 give a mean of 259/3 and a sample SD of √(4/3). The registered reference from the paper’s Table 2 for the four-thread Serial case lists first failure 37, explored schedules 384 and failing schedules 90. The exploration total matches. First failure is 10 schedules later (+27.03%), and the mean failing count is 3.667 lower (−4.07%). The follow-up PERIOD counts match the registered PERIOD reference of 9, 100 and 12. [Registered reference values](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/experiments/2026-11-07/COMPARISON_PROTOCOL.md)
- **Table 4.** PERIOD explored 284 fewer schedules in every pair. The reduction relative to the serialized method is (384 − 100) / 384 = **73.96%**.
- **Table 5.** Subtracting PERIOD time from serialized time within each pair gives 114.316266, 113.226100 and 108.814472 seconds. Their **mean ± sample SD is 112.119 ± 2.913 seconds**. The footer measures the entire driver invocation, including calibration, execution and reporting. The first-failure ID gives a position in the enumeration, not an elapsed time. [Follow-up summary](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/summaries/comparison-42384122902/SUMMARY.md)

## The earlier 120-second batch

All ten PERIOD calls below completed (driver exit 0, outer timeout false, 100 schedules, first failure 9). All ten serialized calls reached the outer timeout (exit −9, timeout true). Each serialized log already showed an assertion at schedule 47. The last two columns are counts observed **before interruption**. Final serialized counts and completion times are missing, so this batch contributes zero four-thread timing pairs. Each linked filename is relative to `results/2026-11-07/comparison-42381922637/reorder_4/`. [Primary run records](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42381922637/reorder_4/records.json)

| Pair | Complete PERIOD log | Failing schedules | Censored serialized log | Printed schedule IDs | Observed error events |
| ---: | --- | ---: | --- | ---: | ---: |
| 1 | [period_r01.txt](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42381922637/reorder_4/period_r01.txt) | 12 | [author_serialized_abi16_r01.txt](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42381922637/reorder_4/author_serialized_abi16_r01.txt) | 276 | 61 |
| 2 | [period_r02.txt](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42381922637/reorder_4/period_r02.txt) | 12 | [author_serialized_abi16_r02.txt](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42381922637/reorder_4/author_serialized_abi16_r02.txt) | 276 | 61 |
| 3 | [period_r03.txt](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42381922637/reorder_4/period_r03.txt) | 12 | [author_serialized_abi16_r03.txt](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42381922637/reorder_4/author_serialized_abi16_r03.txt) | 273 | 62 |
| 4 | [period_r04.txt](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42381922637/reorder_4/period_r04.txt) | 12 | [author_serialized_abi16_r04.txt](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42381922637/reorder_4/author_serialized_abi16_r04.txt) | 275 | 62 |
| 5 | [period_r05.txt](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42381922637/reorder_4/period_r05.txt) | 12 | [author_serialized_abi16_r05.txt](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42381922637/reorder_4/author_serialized_abi16_r05.txt) | 272 | 62 |
| 6 | [period_r06.txt](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42381922637/reorder_4/period_r06.txt) | 10 | [author_serialized_abi16_r06.txt](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42381922637/reorder_4/author_serialized_abi16_r06.txt) | 272 | 62 |
| 7 | [period_r07.txt](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42381922637/reorder_4/period_r07.txt) | 12 | [author_serialized_abi16_r07.txt](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42381922637/reorder_4/author_serialized_abi16_r07.txt) | 275 | 61 |
| 8 | [period_r08.txt](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42381922637/reorder_4/period_r08.txt) | 12 | [author_serialized_abi16_r08.txt](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42381922637/reorder_4/author_serialized_abi16_r08.txt) | 272 | 62 |
| 9 | [period_r09.txt](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42381922637/reorder_4/period_r09.txt) | 12 | [author_serialized_abi16_r09.txt](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42381922637/reorder_4/author_serialized_abi16_r09.txt) | 275 | 61 |
| 10 | [period_r10.txt](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42381922637/reorder_4/period_r10.txt) | 12 | [author_serialized_abi16_r10.txt](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42381922637/reorder_4/author_serialized_abi16_r10.txt) | 272 | 62 |

The sixth primary PERIOD run explains why Table 2 reports **11.800 ± 0.632** failing schedules across ten runs, while the follow-up records exactly 12 in each of three runs. Across all five programs, the primary batch had 90 completed calls among 100 attempts: 40 complete pairs plus ten unpaired PERIOD calls. Six further completions contributed three pairs, giving **96 completions in 106 attempts and 43 complete pairs**. [Primary summary](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/summaries/comparison-42381922637/SUMMARY.md)

## What the comparison establishes

The three pairs support a smaller explored schedule set and shorter whole-driver time for PERIOD on this host. Despite identical explored counts, the serialized driver observed 87, 87 and 85 failing schedules. The follow-up used a new host and a longer outer limit. Its three successive pairs cannot establish independence, a generally applicable speedup, or a causal timing effect of extending the limit.

The archive records an AMD EPYC 7763 host with four allowed CPUs, Linux 7.0.0-1017-azure, Ubuntu 18.04.5 container userland, Clang 10, GCC 7.5 and Python 3.6.9. The compatible serialized driver uses an adapted shared-memory interface. The archived diff and metadata confine the edit to IPC helpers and four array element types and report an identical scheduler section. The IPC probe records a successful 12,160-byte request and a rejected 24,300-byte request. The residual location/order-array mismatch limits conclusions about actual execution order. Matching 384 schedules does not establish identity with the paper’s historical Serial executable. Original-driver crashes fall outside these two compatible batches. Only a run’s own logged assertion events count toward its findings. [Environment](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42384122902/reorder_4/environment.json) · [Interface diff](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42384122902/reorder_4/serial_abi16.diff) · [Adapter record](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42384122902/reorder_4/serial_abi16.json) · [IPC probe](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/9be5e176116790a40f7e55c2813f4ae8505e0461/results/2026-11-07/comparison-42384122902/reorder_4/ipc_abi_probe.json)

<details>
<summary>Reproduce the recount and statistics with Python 3</summary>

Run this block from the root of the reviewed revision. It uses only the standard library. It was executed against the archived files from that revision and verified all 26 comparison log hashes. The two run tables and statistics above report the results.

```python
import hashlib
import json
import re
from pathlib import Path
from statistics import mean, stdev

for batch in ("42381922637", "42384122902"):
    root = Path(f"results/2026-11-07/comparison-{batch}/reorder_4")
    manifest = json.loads((root / "manifest.json").read_bytes())
    hashes = {entry["path"]: entry["sha256"] for entry in manifest["files"]}
    records = json.loads((root / "records.json").read_bytes())
    complete = {"period": {}, "author_serialized_abi16": {}}
    for row in records:
        if row["phase"] != "comparison":
            continue
        name = row["log"]
        raw = (root / name).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == hashes[name] == row["log_sha256"]
        log = re.sub(r"\x1b\[[0-9;]*m", "", raw.decode())
        ids, errors = [], []
        for line in log.splitlines():
            match = re.match(r"^test (\d+):", line)
            if match:
                ids.append(int(match[1]))
            if "[Error Found]" in line:
                assert "assertion failed" in line
                errors.append(ids[-1])
        assert ids == list(range(1, len(ids) + 1))
        assert len(ids) == row["schedules"] and len(errors) == row["error_event_count"]
        first = errors[0] if errors else None
        assert first == row["first_error"]
        footer = re.search(r"Runner exit_code=(-?\d+) timed_out=(\w+) elapsed_seconds=([\d.]+)", log)
        assert int(footer[1]) == row["exit_code"] and (footer[2] == "True") == row["timed_out"]
        seconds = row["elapsed_seconds"]
        assert abs(float(footer[3]) - seconds) <= 0.000000501
        if row["timed_out"]:
            assert "End Testing!" not in log and row["buggy_schedules"] is None
            print(batch, name, "censored", len(ids), first, len(errors))
            continue
        assert row["exit_code"] == 0 and "End Testing!" in log
        assert "Total Timeouts Interleavings: 0" in log
        failing = len(set(errors))
        assert failing == row["buggy_schedules"]
        assert re.search(rf"^Total Error Interleavings: {failing}$", log, re.M)
        assert int(re.search(r"^Round\s+0\s+(\d+)$", log, re.M)[1]) == len(ids)
        complete[row["method"]][row["repeat"]] = (len(ids), first, failing, seconds)
        print(batch, name, "complete", len(ids), first, failing, f"{seconds:.6f}")
    for method, runs in complete.items():
        if runs:
            print(method, [(round(mean(v), 6), round(stdev(v), 6))
                           for v in zip(*runs.values())])
    period, serial = complete["period"], complete["author_serialized_abi16"]
    differences = [serial[r][3] - period[r][3] for r in sorted(period.keys() & serial.keys())]
    if differences:
        print("paired seconds", differences, mean(differences), stdev(differences))
```

</details>
