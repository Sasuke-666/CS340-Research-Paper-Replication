# Independent comparison summary

Batch: `comparison-42380929383`.

Integrity validation: **PASS**.

Values are arithmetic mean ± sample SD. First-error statistics are conditional on a completed trial detecting an error; other metrics use all eligible completed trials.

| Case | Method | Complete / attempts | First error | Schedules | Buggy schedules | Wall time (s) |
|---|---|---:|---:|---:|---:|---:|
| account | author_serialized | 0 / 10 | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| account | period | 10 / 10 | 10.4000 ± 0.6992 (n=10) | 65.0000 ± 0.0000 (n=10) | 25.3000 ± 1.0593 (n=10) | 23.8968 ± 0.9752 (n=10) |
| lazy01 | author_serialized | 0 / 10 | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| lazy01 | period | 10 / 10 | 8.8000 ± 2.2010 (n=10) | 39.0000 ± 0.0000 (n=10) | 10.6000 ± 1.8974 (n=10) | 6.5175 ± 1.0782 (n=10) |
| reorder_3 | author_serialized | 0 / 10 | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| reorder_3 | period | 10 / 10 | 7.4000 ± 4.4272 (n=10) | 27.0000 ± 0.0000 (n=10) | 5.3000 ± 1.3375 (n=10) | 4.7037 ± 0.9931 (n=10) |
| reorder_4 | author_serialized | 0 / 10 | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| reorder_4 | period | 10 / 10 | 9.3000 ± 0.9487 (n=10) | 100.0000 ± 0.0000 (n=10) | 11.8000 ± 0.4216 (n=10) | 21.2199 ± 1.1721 (n=10) |
| twostage | author_serialized | 0 / 10 | NA (n=0) | NA (n=0) | NA (n=0) | NA (n=0) |
| twostage | period | 10 / 10 | 4.0000 ± 0.0000 (n=10) | 33.0000 ± 0.0000 (n=10) | 2.1000 ± 0.3162 (n=10) | 2.3019 ± 0.4224 (n=10) |

## Paired comparisons

Each row uses complete repetition pairs from one case on one matrix-job host.

| Case | Pairs | Schedule reduction (%) | Serialized − PERIOD time (s) | Serialized / PERIOD time |
|---|---:|---:|---:|---:|
| account | 0 | NA (n=0) | NA (n=0) | NA (n=0) |
| lazy01 | 0 | NA (n=0) | NA (n=0) | NA (n=0) |
| reorder_3 | 0 | NA (n=0) | NA (n=0) | NA (n=0) |
| reorder_4 | 0 | NA (n=0) | NA (n=0) | NA (n=0) |
| twostage | 0 | NA (n=0) | NA (n=0) | NA (n=0) |

Detailed paper gaps, diagnostic outcomes, Wilson intervals, paired discordances and provenance are in `summary.json`; every attempted trial is in `all_trials.csv`.

## Limits and integrity findings

- Unmodified serialized failures have no valid scheduler outcome. Historical witnesses/author_serialized copies may be stale PERIOD files; this analysis never uses witness counts or attribution.
- Runtime summaries are per case and batch only. CPU labels are not host identifiers; there is no pooled cross-host speedup.
- Paper gaps are descriptive reproduction gaps. The ABI-adapted released serialized driver has not been proven identical to the historical Table 2 executable.
- Wilson and exact McNemar outputs are optional model-based diagnostics. Independence of repeated trials or pairs is not established by AB/BA ordering; all-hit outcomes do not prove equality. Descriptive counts and mean/sample SD are the primary results.
