# CS340 PERIOD final submission v1.0.2

Final report and presentation revision: 25 November 2026.

This release integrates the two member submissions made on 24 November and
closes the remaining issues found in their review. The study covers five
programs, a depth-bound extension, controlled capacity diagnostics and independent
member work. Its conclusion remains **partially reproduced**.

## Changes in this revision

- Preserves He Boyu's PR #7: three synthetic regressions for the twostage recount.
- Preserves Li Yangshuo's PR #8: release/Windows verification, independent
  acceptance metrics, stricter parsers and a validation evidence manifest.
- Adds maintainer fixes for footer whitespace/order, events outside the accepted
  test body and symbolic-link parent directories. Five targeted test methods
  exercise the reproduced boundary cases.
- Clarifies two audit date labels using the verified 24 November submission
  date. Original transcripts remain unchanged, with their execution scope
  stated separately from the exact-revision continuous checks.
- Runs the independent metric and manifest audits in `make audit` and Linux/
  Windows CI. Every ready final manifest is checked for source drift.
- Updates the report, fourteen-slide presentation, Chinese handbook and dated
  contribution map. The six documents and complete ZIP share one verified
  source and delivery manifest.

No new benchmark measurements were made for this revision. The historical
numeric results, raw evidence and study denominators retain their original
scope. The `v1.0` and `v1.0.1` tags and assets remain available unchanged.

## Download and reproduce

The six individual files are attached. The complete ZIP contains the same
documents, the tracked repository and raw evidence without Git metadata.
Read `Repository/README.md` in that bundle, or clone the repository at `v1.0.2`.

`make check` validates the maintained code and repository rules. `make audit`
recounts preserved evidence and verifies the report and validation records.
The main experiments use the README's pinned x86_64 Linux/Docker procedure.

The 22 November fresh-host acceptance has its own 30 complete comparison calls,
15 pairs, 40 separate diagnostic calls and five successful builds. It does not
replace the historical 106 attempts, 96 complete calls and 43 complete pairs.
The independent member run, depth extension, capacity batches and five fixed-
witness replays retain their own denominators.

The [closeout record](../docs/PROJECT_CLOSEOUT_20261125.md) identifies each
member's verified work. The [validation record](../docs/FINAL_VALIDATION_20261125.md)
identifies the source, tests, document review and delivery checks. Course
registration, submission and presentation arrangements are recorded when their
actual confirmations are available.
