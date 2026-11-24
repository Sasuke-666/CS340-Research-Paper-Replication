# Independent acceptance recount and evidence-parser hardening

**Prepared by:** 李扬烁, student ID 1240001156, GitHub `barkhorn996`

**Audit date:** 22 November 2026, Asia/Shanghai (UTC+08:00)

**Reviewed source revision:** `10ff18acd17d3acd6ccda3d5582c8eecbb496c88`

**Acceptance batch:** `acceptance-45015126850-attempt1`

This work adds no experiment. It independently recounts the completed fresh-host acceptance archive and hardens two raw-log parsers so malformed evidence fails closed. Existing measurements and scientific conclusions are unchanged.

## 1. Independent acceptance recount

The recount reads only the complete ZIP's extracted repository and does not import the acceptance summarizer. It independently checks the outer manifest, record counts, pair structure, execution statuses and raw-log existence.

### 1.1 Archive integrity

| Check | Result |
| --- | ---: |
| Outer manifest entries | 948 |
| Missing files | 0 |
| Byte-count mismatches | 0 |
| SHA-256 mismatches | 0 |
| Recorded command records | 75 |

The 75 command records decompose exactly into:

| Command class | Count |
| --- | ---: |
| Benchmark builds | 5 |
| Comparison invocations | 30 |
| Replay diagnostics | 40 |

### 1.2 Per-case denominators

| Case | Comparison calls | Complete within-case pairs | Diagnostics | Builds |
| --- | ---: | ---: | ---: | ---: |
| `reorder_3` | 6 | 3 | 40 | 1 |
| `reorder_4` | 6 | 3 | 0 | 1 |
| `account` | 6 | 3 | 0 | 1 |
| `lazy01` | 6 | 3 | 0 | 1 |
| `twostage` | 6 | 3 | 0 | 1 |
| **Total** | **30** | **15** | **40** | **5** |

For every comparison and diagnostic record:

- Exit code was 0.
- `timed_out` was false.
- Completed tasks reported status `complete`.
- The referenced raw log existed.

All five build records also had exit code 0 and `timed_out=false`. No nonzero exit, incomplete status, timeout or missing raw-log reference was found.

The repository's independent `check_acceptance.py` agrees:

- Comparison attempts: 30.
- Complete and eligible comparisons: 30.
- Complete pairs: 15.
- Eligible diagnostics: 40.
- Problems: none.
- Acceptance: true.

The independent transcript is in `evidence/1240001156-release-windows-audit-20261124/independent-acceptance-recount.log`.

## 2. Parser robustness review

The existing parsers already rejected missing totals, duplicate schedule ordinals, unattributed errors and inconsistent footer counts. A new adversarial review found additional malformed logs that could still be interpreted as complete:

1. A test or error line inserted after `End Testing!`.
2. Repeated completion, total or round markers where the parser selected one occurrence.
3. An over-budget `test` line whose later error could be attributed to the previous in-budget schedule.
4. Completion markers in an invalid order, such as `End Testing!` moved after the runner footer.

These cases could misattribute an error event or accept a damaged log. They are evidence-integrity risks even if no archived measurement currently exhibits them.

## 3. Parser changes

### 3.1 Live comparison parser

`scripts/run_period_comparison.py` now:

- Requires exactly one `End Testing!` marker.
- Requires exactly one error-total footer.
- Requires exactly one `Round 0` footer.
- Requires `End Testing!`, error total and round footer in the expected order.
- Rejects tests or errors after the end marker.
- Rejects any schedule ordinal greater than the configured budget.
- Continues to reject unattributed errors and non-sequential ordinals.

### 3.2 Independent summarizer parser

`scripts/summarize_comparison.py` now:

- Requires one end marker, one error total, one round footer and one runner footer.
- Requires end, total, round and runner footers in that order.
- Rejects test/error events after the end marker.
- Preserves the existing distinction between a crash prefix and a complete run: a crash still reports its established parse problems and remains ineligible.

## 4. Regression tests

Seven synthetic regression cases were added across:

- `tests/test_period_comparison.py`
- `tests/test_comparison_summary.py`

They cover:

- Error after the end marker.
- Duplicate end or footer markers.
- Schedule beyond the configured budget.
- Error before any test.
- Event after completion.
- Marker-order inversion.

All added fixtures are synthetic and are excluded from experimental results.

## 5. Compatibility with archived evidence

The hardened live parser was applied to 46 complete archived logs from:

- The original account comparison.
- The four-thread follow-up.
- The independent member account batch.

All 46 were still accepted as complete. The full repository audit also remained green, including manifests, report tables, member reviews and acceptance evidence.

Validation results:

- `make check`: **171 tests passed**.
- `make audit`: status 0.
- Integrity checks for historical, member, capacity and acceptance batches: passed.
- Report-table checks: passed.
- Native Windows Python 3.14.7 focused regression check: **34 tests passed**, exit code 0.

The two affected test modules were downloaded from this PR's final source revision and rerun in the existing isolated Windows Python 3.14.7 environment. This closes the cross-platform loop for the parser changes without modifying any archived evidence or experimental result.

Transcripts:

- `evidence/1240001156-release-windows-audit-20261124/parser-hardening-tests.log`
- `evidence/1240001156-release-windows-audit-20261124/parser-hardening-audit.log`
- `evidence/1240001156-release-windows-audit-20261124/windows-focused-tests.log`

## 6. Scope and limits

The independent acceptance recount validates structural completeness and archive integrity. It does not reinterpret the scientific results or replace the acceptance protocol's statistics.

The parser tests are targeted regression cases, not an exhaustive fuzzing campaign. They establish fail-closed behavior for the identified malformed structures and preserve compatibility with existing complete logs.

Completed by: 李扬烁, 22 November 2026.
