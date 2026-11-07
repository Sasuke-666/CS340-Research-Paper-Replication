# Independent comparison summary

Batch: `comparison-42384122902`.

Integrity validation: **PASS**.

Values are arithmetic mean ± sample SD. First-error statistics are conditional on a completed trial detecting an error; other metrics use all eligible completed trials.

| Case | Method | Complete / attempts | First error | Schedules | Buggy schedules | Wall time (s) |
|---|---|---:|---:|---:|---:|---:|
| reorder_4 | author_serialized_abi16 | 3 / 3 | 47.0000 ± 0.0000 (n=3) | 384.0000 ± 0.0000 (n=3) | 86.3333 ± 1.1547 (n=3) | 133.9623 ± 2.7046 (n=3) |
| reorder_4 | period | 3 / 3 | 9.0000 ± 0.0000 (n=3) | 100.0000 ± 0.0000 (n=3) | 12.0000 ± 0.0000 (n=3) | 21.8434 ± 0.4989 (n=3) |

## Paired comparisons

Each row uses complete repetition pairs from one case on one matrix-job host.

| Case | Pairs | Schedule reduction (%) | Serialized − PERIOD time (s) | Serialized / PERIOD time |
|---|---:|---:|---:|---:|
| reorder_4 | 3 | 73.9583 ± 0.0000 (n=3) | 112.1189 ± 2.9132 (n=3) | 6.1357 ± 0.2189 (n=3) |

Detailed paper gaps, diagnostic outcomes, Wilson intervals, paired discordances and provenance are in `summary.json`; every attempted trial is in `all_trials.csv`.

## Limits and integrity findings

- Runtime summaries are per case and batch only. CPU labels are not host identifiers; there is no pooled cross-host speedup.
- Paper gaps are descriptive reproduction gaps. The ABI-adapted released serialized driver has not been proven identical to the historical Table 2 executable.
- Wilson and exact McNemar outputs are optional model-based diagnostics. Independence of repeated trials or pairs is not established by AB/BA ordering; all-hit outcomes do not prove equality. Descriptive counts and mean/sample SD are the primary results.
