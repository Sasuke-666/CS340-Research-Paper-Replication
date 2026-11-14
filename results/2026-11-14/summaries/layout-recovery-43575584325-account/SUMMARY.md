# Registered capacity-layout study

Batch: `layout-recovery-43575584325`.

Audited case scope: `account`; planned repetitions per condition: 10.
The denominators below apply to this stated scope only.

Integrity checks: **PASS**.

Actual denominators: `{"complete_pairs": 10, "planned_workload_attempts": 20, "workload_attempts": 20, "workload_complete": 20, "workload_eligible": 20}`.

## Outcomes by case and condition

All values are mean ± sample SD, with actual n. First error is conditional on an observed error.

| Case | Condition | Complete / attempted | Eligible | Schedules | First error | Buggy schedules | Whole-driver seconds |
| --- | --- | ---: | ---: | --- | --- | --- | --- |
| account | capacity1990 | 10 / 10 | 10 | 65.000000 ± 0.000000 (n=10) | 10.500000 ± 0.849837 (n=10) | 22.900000 ± 3.281260 (n=10) | 23.569197 ± 3.546832 (n=10) |
| account | capacity3964 | 10 / 10 | 10 | 65.000000 ± 0.000000 (n=10) | 10.200000 ± 0.632456 (n=10) | 24.300000 ± 1.766981 (n=10) | 24.638909 ± 2.040499 (n=10) |

## Observed outcomes including bounded and incomplete calls

An observed assertion before a timeout or schedule-budget stop remains an observation. Prefix counts are not completed enumeration totals. Error events can repeat the same program defect.

| Case | Condition | Any error observed / intact attempts | Assertion observed | Other error events | Outer / inner timeout trials | Budget reached | Incomplete or censored prefix schedules |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| account | capacity1990 | 10 / 10 | 10 | 0 | 0 / 0 | 0 | unavailable (n=0) |
| account | capacity3964 | 10 / 10 | 10 | 0 | 0 / 0 | 0 | unavailable (n=0) |

## Within-case paired changes

Differences are capacity3964 minus capacity1990. Missing or censored arms are excluded from paired estimates.

| Case | Eligible pairs | Schedule delta | First-error delta | Buggy-schedule delta | Seconds delta | Equal requested sequences |
| --- | ---: | --- | --- | --- | --- | ---: |
| account | 10 | 0.000000 ± 0.000000 (n=10) | -0.300000 ± 1.159502 (n=10) | 1.400000 ± 4.402020 (n=10) | 1.069713 ± 4.322635 (n=10) | 10 / 10 |

## Auxiliary coverage feedback observations

These values are recounted from existing stdout. They are separate from the prespecified primary outcomes and do not establish an executed memory-operation trace.

| Case | Condition | Unique default coverage hashes | Unambiguous observations | Missing or multiple observations |
| --- | --- | --- | ---: | ---: |
| account | capacity1990 | 18 | 10 | 0 |
| account | capacity3964 | 196202 | 10 | 0 |

## Interpretation limits

- Requested schedule hashes describe printed requests, not observed memory-operation traces.
- Synthetic sentinel and native layout probes are excluded from workload denominators.
- The default coverage hash is auxiliary stdout evidence; it is reported only when exactly one such value appears. All values remain in each trial record.
- Capacity can change a local outcome without explaining the historical paper discrepancy.
- Repeated trials on one host may be dependent; descriptive means and sample SD are reported.
- All estimates are withheld if any batch integrity or design check fails.
- A complete driver invocation may end at its schedule budget; bounded completions are excluded from complete-enumeration estimates.
- Binary hashes are captured before each call; executables are not retained in the archive.
