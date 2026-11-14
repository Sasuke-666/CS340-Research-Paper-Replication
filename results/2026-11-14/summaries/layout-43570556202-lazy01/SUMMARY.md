# Registered capacity-layout study

Batch: `layout-43570556202`.

Audited case scope: `lazy01`; planned repetitions per condition: 10.
The denominators below apply to this stated scope only.

Integrity checks: **PASS**.

Actual denominators: `{"complete_pairs": 10, "planned_workload_attempts": 20, "workload_attempts": 20, "workload_complete": 20, "workload_eligible": 20}`.

## Outcomes by case and condition

All values are mean ± sample SD, with actual n. First error is conditional on an observed error.

| Case | Condition | Complete / attempted | Eligible | Schedules | First error | Buggy schedules | Whole-driver seconds |
| --- | --- | ---: | ---: | --- | --- | --- | --- |
| lazy01 | capacity1990 | 10 / 10 | 10 | 39.000000 ± 0.000000 (n=10) | 8.500000 ± 1.581139 (n=10) | 11.600000 ± 0.843274 (n=10) | 10.994348 ± 0.721862 (n=10) |
| lazy01 | capacity3964 | 10 / 10 | 10 | 39.000000 ± 0.000000 (n=10) | 8.200000 ± 0.421637 (n=10) | 9.900000 ± 1.911951 (n=10) | 9.604638 ± 1.607901 (n=10) |

## Observed outcomes including bounded and incomplete calls

An observed assertion before a timeout or schedule-budget stop remains an observation. Prefix counts are not completed enumeration totals. Error events can repeat the same program defect.

| Case | Condition | Any error observed / intact attempts | Assertion observed | Other error events | Outer / inner timeout trials | Budget reached | Incomplete or censored prefix schedules |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| lazy01 | capacity1990 | 10 / 10 | 10 | 0 | 0 / 0 | 0 | unavailable (n=0) |
| lazy01 | capacity3964 | 10 / 10 | 10 | 0 | 0 / 0 | 0 | unavailable (n=0) |

## Within-case paired changes

Differences are capacity3964 minus capacity1990. Missing or censored arms are excluded from paired estimates.

| Case | Eligible pairs | Schedule delta | First-error delta | Buggy-schedule delta | Seconds delta | Equal requested sequences |
| --- | ---: | --- | --- | --- | --- | ---: |
| lazy01 | 10 | 0.000000 ± 0.000000 (n=10) | -0.300000 ± 1.337494 (n=10) | -1.700000 ± 2.002776 (n=10) | -1.389709 ± 1.524520 (n=10) | 10 / 10 |

## Auxiliary coverage feedback observations

These values are recounted from existing stdout. They are separate from the prespecified primary outcomes and do not establish an executed memory-operation trace.

| Case | Condition | Unique default coverage hashes | Unambiguous observations | Missing or multiple observations |
| --- | --- | --- | ---: | ---: |
| lazy01 | capacity1990 | 8 | 10 | 0 |
| lazy01 | capacity3964 | 185480 | 10 | 0 |

## Interpretation limits

- Requested schedule hashes describe printed requests, not observed memory-operation traces.
- Synthetic sentinel and native layout probes are excluded from workload denominators.
- The default coverage hash is auxiliary stdout evidence; it is reported only when exactly one such value appears. All values remain in each trial record.
- Capacity can change a local outcome without explaining the historical paper discrepancy.
- Repeated trials on one host may be dependent; descriptive means and sample SD are reported.
- All estimates are withheld if any batch integrity or design check fails.
- A complete driver invocation may end at its schedule budget; bounded completions are excluded from complete-enumeration estimates.
- Binary hashes are captured before each call; executables are not retained in the archive.
