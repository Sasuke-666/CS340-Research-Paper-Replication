# Independent comparison summary

Batch: `1240001156-account-20261108T122201Z`.

Integrity validation: **PASS**.

Values are arithmetic mean ± sample SD. First-error statistics are conditional on a completed trial detecting an error; other metrics use all eligible completed trials.

| Case | Method | Complete / attempts | First error | Schedules | Buggy schedules | Wall time (s) |
|---|---|---:|---:|---:|---:|---:|
| account | author_serialized_abi16 | 10 / 10 | 4.0000 ± 0.0000 (n=10) | 136.0000 ± 0.0000 (n=10) | 55.9000 ± 0.3162 (n=10) | 12.1671 ± 0.3959 (n=10) |
| account | period | 10 / 10 | 8.8000 ± 2.0440 (n=10) | 65.0000 ± 0.0000 (n=10) | 26.4000 ± 0.8433 (n=10) | 6.8555 ± 0.1552 (n=10) |

## Paired comparisons

Each row uses complete repetition pairs from one case on one matrix-job host.

| Case | Pairs | Schedule reduction (%) | Serialized − PERIOD time (s) | Serialized / PERIOD time |
|---|---:|---:|---:|---:|
| account | 10 | 52.2059 ± 0.0000 (n=10) | 5.3117 ± 0.3771 (n=10) | 1.7752 ± 0.0594 (n=10) |

Detailed paper gaps, diagnostic outcomes, Wilson intervals, paired discordances and provenance are in `summary.json`; every attempted trial is in `all_trials.csv`.

## Limits and integrity findings

- No batch archive manifest; individual case manifests are checked.
- Runtime summaries are per case and batch only. CPU labels are not host identifiers; there is no pooled cross-host speedup.
- Paper gaps are descriptive reproduction gaps. The ABI-adapted released serialized driver has not been proven identical to the historical Table 2 executable.
- Wilson and exact McNemar outputs are optional model-based diagnostics. Independence of repeated trials or pairs is not established by AB/BA ordering; all-hit outcomes do not prove equality. Descriptive counts and mean/sample SD are the primary results.
