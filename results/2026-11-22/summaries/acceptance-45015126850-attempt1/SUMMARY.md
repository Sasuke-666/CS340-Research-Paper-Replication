# Independent comparison summary

Batch: `acceptance-45015126850-attempt1`.

Integrity validation: **PASS**.

Values are arithmetic mean ± sample SD. First-error statistics are conditional on a completed trial detecting an error; other metrics use all eligible completed trials.

| Case | Method | Complete / attempts | First error | Schedules | Buggy schedules | Wall time (s) |
|---|---|---:|---:|---:|---:|---:|
| account | author_serialized_abi16 | 3 / 3 | 4.0000 ± 0.0000 (n=3) | 136.0000 ± 0.0000 (n=3) | 49.0000 ± 10.4403 (n=3) | 52.7805 ± 9.7038 (n=3) |
| account | period | 3 / 3 | 10.0000 ± 0.0000 (n=3) | 65.0000 ± 0.0000 (n=3) | 24.6667 ± 0.5774 (n=3) | 26.2351 ± 1.0360 (n=3) |
| lazy01 | author_serialized_abi16 | 3 / 3 | 4.0000 ± 0.0000 (n=3) | 60.0000 ± 0.0000 (n=3) | 16.6667 ± 2.5166 (n=3) | 21.3350 ± 3.4244 (n=3) |
| lazy01 | period | 3 / 3 | 8.0000 ± 0.0000 (n=3) | 39.0000 ± 0.0000 (n=3) | 11.6667 ± 0.5774 (n=3) | 15.1298 ± 0.7118 (n=3) |
| reorder_3 | author_serialized_abi16 | 3 / 3 | 10.0000 ± 0.0000 (n=3) | 30.0000 ± 0.0000 (n=3) | 9.6667 ± 1.5275 (n=3) | 8.1707 ± 1.1587 (n=3) |
| reorder_3 | period | 3 / 3 | 6.0000 ± 0.0000 (n=3) | 27.0000 ± 0.0000 (n=3) | 6.0000 ± 0.0000 (n=3) | 5.2439 ± 0.3520 (n=3) |
| reorder_4 | author_serialized_abi16 | 3 / 3 | 47.0000 ± 0.0000 (n=3) | 384.0000 ± 0.0000 (n=3) | 89.6667 ± 1.5275 (n=3) | 86.0087 ± 15.0419 (n=3) |
| reorder_4 | period | 3 / 3 | 11.3333 ± 2.0817 (n=3) | 100.0000 ± 0.0000 (n=3) | 9.6667 ± 2.0817 (n=3) | 10.0211 ± 2.2133 (n=3) |
| twostage | author_serialized_abi16 | 3 / 3 | 12.3333 ± 14.4338 (n=3) | 33.0000 ± 0.0000 (n=3) | 2.0000 ± 1.0000 (n=3) | 2.0247 ± 0.5756 (n=3) |
| twostage | period | 3 / 3 | 4.0000 ± 0.0000 (n=3) | 33.0000 ± 0.0000 (n=3) | 2.3333 ± 0.5774 (n=3) | 2.2902 ± 0.3570 (n=3) |

## Paired comparisons

Each row uses complete repetition pairs from one case on one matrix-job host.

| Case | Pairs | Schedule reduction (%) | Serialized − PERIOD time (s) | Serialized / PERIOD time |
|---|---:|---:|---:|---:|
| account | 3 | 52.2059 ± 0.0000 (n=3) | 26.5454 ± 9.6086 (n=3) | 2.0127 ± 0.3667 (n=3) |
| lazy01 | 3 | 35.0000 ± 0.0000 (n=3) | 6.2052 ± 2.7567 (n=3) | 1.4054 ± 0.1666 (n=3) |
| reorder_3 | 3 | 10.0000 ± 0.0000 (n=3) | 2.9267 ± 0.9606 (n=3) | 1.5559 ± 0.1723 (n=3) |
| reorder_4 | 3 | 73.9583 ± 0.0000 (n=3) | 75.9876 ± 15.1886 (n=3) | 8.8904 ± 2.4212 (n=3) |
| twostage | 3 | 0.0000 ± 0.0000 (n=3) | -0.2655 ± 0.9266 (n=3) | 0.9236 ± 0.3919 (n=3) |

Detailed paper gaps, diagnostic outcomes, Wilson intervals, paired discordances and provenance are in `summary.json`; every attempted trial is in `all_trials.csv`.

## Limits and integrity findings

- Runtime summaries are per case and batch only. CPU labels are not host identifiers; there is no pooled cross-host speedup.
- Paper gaps are descriptive reproduction gaps. The ABI-adapted released serialized driver has not been proven identical to the historical Table 2 executable.
- Wilson and exact McNemar outputs are optional model-based diagnostics. Independence of repeated trials or pairs is not established by AB/BA ordering; all-hit outcomes do not prove equality. Descriptive counts and mean/sample SD are the primary results.
