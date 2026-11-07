# Independent comparison summary

Batch: `comparison-42381922637`.

Integrity validation: **PASS**.

Values are arithmetic mean ± sample SD. First-error statistics are conditional on a completed trial detecting an error; other metrics use all eligible completed trials.

| Case | Method | Complete / attempts | First error | Schedules | Buggy schedules | Wall time (s) |
|---|---|---:|---:|---:|---:|---:|
| account | author_serialized_abi16 | 10 / 10 | 7.7000 ± 7.8888 (n=10) | 136.0000 ± 0.0000 (n=10) | 49.2000 ± 8.2165 (n=10) | 49.3170 ± 7.6616 (n=10) |
| account | period | 10 / 10 | 10.1000 ± 0.3162 (n=10) | 65.0000 ± 0.0000 (n=10) | 24.4000 ± 2.9136 (n=10) | 23.7380 ± 2.3559 (n=10) |
| lazy01 | author_serialized_abi16 | 10 / 10 | 7.2000 ± 7.0048 (n=10) | 60.0000 ± 0.0000 (n=10) | 17.7000 ± 4.7152 (n=10) | 16.8881 ± 4.1186 (n=10) |
| lazy01 | period | 10 / 10 | 8.0000 ± 0.0000 (n=10) | 39.0000 ± 0.0000 (n=10) | 12.0000 ± 0.0000 (n=10) | 11.4851 ± 0.4335 (n=10) |
| reorder_3 | author_serialized_abi16 | 10 / 10 | 10.1000 ± 0.3162 (n=10) | 30.0000 ± 0.0000 (n=10) | 9.8000 ± 0.9189 (n=10) | 9.5526 ± 0.8272 (n=10) |
| reorder_3 | period | 10 / 10 | 6.1000 ± 0.3162 (n=10) | 27.0000 ± 0.0000 (n=10) | 6.0000 ± 0.0000 (n=10) | 5.8550 ± 0.3241 (n=10) |
| reorder_4 | author_serialized_abi16 | 0 / 10 | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| reorder_4 | period | 10 / 10 | 9.0000 ± 0.0000 (n=10) | 100.0000 ± 0.0000 (n=10) | 11.8000 ± 0.6325 (n=10) | 20.7245 ± 0.9983 (n=10) |
| twostage | author_serialized_abi16 | 10 / 10 | 4.0000 ± 0.0000 (n=10) | 33.0000 ± 0.0000 (n=10) | 2.2000 ± 0.4216 (n=10) | 2.6522 ± 0.3776 (n=10) |
| twostage | period | 10 / 10 | 5.3000 ± 4.1110 (n=10) | 33.0000 ± 0.0000 (n=10) | 1.9000 ± 0.3162 (n=10) | 2.6635 ± 0.2958 (n=10) |

## Censored searches

Outer timeouts preserve the observed prefix. Its printed schedule count is not the completed search-space size; observations before timeout can still include detected errors.

| Case | Method | Outer timeouts | Observed printed schedules (min–max) | Prefixes with an observed first error |
|---|---|---:|---:|---:|
| reorder_4 | author_serialized_abi16 | 10 | 272–276 | 10 / 10 |

## Paired comparisons

Each row uses complete repetition pairs from one case on one matrix-job host.

| Case | Pairs | Schedule reduction (%) | Serialized − PERIOD time (s) | Serialized / PERIOD time |
|---|---:|---:|---:|---:|
| account | 10 | 52.2059 ± 0.0000 (n=10) | 25.5790 ± 8.5364 (n=10) | 2.1077 ± 0.4543 (n=10) |
| lazy01 | 10 | 35.0000 ± 0.0000 (n=10) | 5.4030 ± 3.8525 (n=10) | 1.4638 ± 0.3469 (n=10) |
| reorder_3 | 10 | 10.0000 ± 0.0000 (n=10) | 3.6976 ± 0.9251 (n=10) | 1.6375 ± 0.1797 (n=10) |
| reorder_4 | 0 | NA (n=0) | NA (n=0) | NA (n=0) |
| twostage | 10 | 0.0000 ± 0.0000 (n=10) | -0.0113 ± 0.4388 (n=10) | 1.0077 ± 0.1817 (n=10) |

Detailed paper gaps, diagnostic outcomes, Wilson intervals, paired discordances and provenance are in `summary.json`; every attempted trial is in `all_trials.csv`.

## Limits and integrity findings

- Runtime summaries are per case and batch only. CPU labels are not host identifiers; there is no pooled cross-host speedup.
- Paper gaps are descriptive reproduction gaps. The ABI-adapted released serialized driver has not been proven identical to the historical Table 2 executable.
- Wilson and exact McNemar outputs are optional model-based diagnostics. Independence of repeated trials or pairs is not established by AB/BA ordering; all-hit outcomes do not prove equality. Descriptive counts and mean/sample SD are the primary results.
- Outer timeouts are right-censored searches. Their observed schedule/error prefixes are retained separately; they are excluded from completed-search means, paper-total gaps and completed runtime pairs. A timeout after observing an error is not a failure to detect that error.
