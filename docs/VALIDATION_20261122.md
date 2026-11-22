# Report traceability and current-stage validation

Date: 22 November 2026, Macau/Beijing time (UTC+8).
Integration baseline: `7ba2d8f966fcaa1dd13e32d5cc4ee662df59d340`.
The owner requested completion and stronger quality of the current stage.
Sections 1–5 describe the earlier traceability closeout, which added no measured
workload. Section 6 records the subsequent stricter review and separately
registered live acceptance work. Historical archived results are unchanged.

## 1. Accepted member work

[PR #5](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/5)
was checked at the submitted head `7ac3a655edf0bb872d1f457fc2911ab41b4424a7`.
Both workflow runs attached to that head (`44922732227`, `44922750477`) passed
in Python 3.9 and 3.12. The normal merge preserved Li Yangshuo's authorship.
The member audit is secondary verification and narrative reference improvement.
The maintainer clarified its raw-log locator: schedule totals come from driver
Round/Total summaries and sequential test records, not the wrapper footer.
No value or member submission date was changed.

The report, contribution record and current member checklist now include PR #5
and the already accepted PR #3/#4 studies. Prior dated contribution rows retain
their original status. Current technical acceptance is distinct from an
unrecorded personal explanation or formal course submission.

## 2. Automatic report traceability

`make audit` runs the existing raw-file, comparison, member, layout and replay
checks, then `scripts/audit_report.py`. `make audit-report` runs the last check
alone. It relies on separately audited summaries for the relevant bindings;
use the full audit to verify underlying archived bytes and recounts.

| Binding | Actual checked scope |
| --- | --- |
| Tables 2–5 | Paper-reference gaps, rounded means/sample SD, stable schedule counts, sample sizes and within-host paired differences |
| Tables 6–7 | Historical raw-log recount for replay/depth, separately scoped replay multiplier diagnostics, missing first failure and detection denominators |
| Table 8 | Independent WSL2 account sample, ten calls per method |
| Table 9 | Native and decoder field offsets in both separately archived cases |
| Table 10 | Original missing account denominator stays Unknown; readable lazy01 and recovery account remain separate |
| Tables 11–12 | Capacity-condition samples and paired B-minus-A effects on each case host |
| Captions and source | 18 unique numbered captions with narrative references, four local figure paths, current revision date |

The successful output reports **11 quantitative tables**, **321 bound cells**,
of which **236 are numeric or missingness cells**. The declared coverage does
not include every prose assertion, the original paper's accuracy, Table 6's
interpretation column, the semantic content of Tables 1/13/A1, plotted SVG
geometry or final document layout. Those remain separate review tasks.

Thirteen report regression tests exercise changed means/SD/gaps, altered n,
reversed differences, Unknown/Not observed replaced by zero, relabelled batches,
changed replay counts, wrong native offsets, missing/duplicate captions,
missing narrative callouts including ranges, invalid image paths, invalid
summary provenance and stale revision dates. Fixtures are synthetic and are
never research observations. During integration, an added range callout exposed
a test assumption about a unique reference. The test was repaired to remove
all prose callouts while preserving captions; the audit was not weakened.

## 3. Export consistency and documentation

`report/REVISION_DATE` is the canonical revision date. Its ISO date must match
the report header. Both English report formats and the Chinese checklist use
that date in their default filename/footer. An inconsistent explicit `--date`
is rejected. Makefile and continuous checks call the same export entry points.
`make deliverables` creates the report and checklist using pinned document
libraries. Historical measurement dates remain unchanged.

The initial phrase "100 comparisons" was clarified to 100 driver invocations,
arranged as 50 planned method pairs. The evidence remains 90 complete primary
calls plus six complete follow-up calls, 43 complete pairs in separate host
scopes, and ten censored primary calls. The independent account study, two
readable capacity batches and five twostage replays keep their own denominators.

The 14-slide rehearsal source includes English screen text, Chinese notes and
sources for each slide. It explains the necessary twostage partial order and
the five selected-witness assertions without claiming a unique measured trace.
The official presentation format still requires the separate course instruction.

## 4. Verification performed

| Check | Observed result |
| --- | --- |
| Complete unittest suite | 134 tests passed, including 13 report regressions |
| Full evidence audit | Passed; original checksums, independently recounted records and maintained summaries unchanged |
| Report table/caption/date check | Passed with the declared 321-cell coverage |
| English report export | PDF 17 pages; editable Word rendered as 15 pages in the available office renderer |
| Chinese member checklist | Editable Word rendered as two pages; both pages visually checked |
| English PDF and Word visual review | All 17 PDF pages and all 15 rendered Word pages checked at full size; figures/captions together, tables readable, Appendix A repeats its table header across pages, long source links fit |
| Historical commit identity scan at integration baseline | All 49 reachable subjects contain a recorded member's full name and student ID |

The published revision's workflow result is verified separately at delivery.
Document pagination can differ between the
editable Word version and the independently laid-out PDF. Both are exported
from the same maintained report source.

The repository workflow runs the complete tests and evidence/report checks on
Python 3.9 and 3.12. The Python 3.12 job also exports and packages tracked source,
evidence and documents. Its `SNAPSHOT.json` identifies the exact commit and
report revision. Use the run attached to the published commit in
[Repository checks](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/workflows/repository-checks.yml)
to inspect its actual status and download the matching snapshot. Earlier green
runs do not establish the status of a later revision.

## 5. Course alignment and remaining external items

All five pages of the latest supplied five-page course project document were
checked again. The [requirements record](COURSE_REQUIREMENTS.md) preserves the
stated report/Git criteria and identifies the separate presentation rubric as
unavailable. This revision strengthens numerical traceability, referenced
figures/tables, accurate contribution attribution, reproducible exports and
substantive progress during 16–22 November. It does not assign a predicted mark.

The group still needs the actual registration receipt and fourth-member
allocation, final submission deadline/portal and formal presentation guidance.
Members must prepare their own explanation of the submitted work. Final PDF
submission and `v1.0` tagging belong to the actual verified final version.

## 6. Subsequent strict review and live acceptance

The owner's follow-up requested reasonable grading-risk inference and concrete
improvements. The supplied rubric remains the source of official requirements.
The choice of a concise reviewer entry point, deeper distribution/mechanism
explanations and this bounded acceptance design is the group's quality decision.
No score or unannounced instructor rule is inferred as fact.

Three actual defects were found beyond the earlier offline checks. The pilot
workflow precreated an output directory that the wrapper rejects; the layout
Make target inherited `reorder_3`, although only account/lazy01 are supported;
and the compatible-comparison archive unconditionally downloaded an old run
whose bytes are already in Git. Fixes preserve output non-overwrite, choose
target-specific defaults and archive only the current run's artifacts.

The report now distinguishes bug depth from absolute period count and limits
C2 to the released driver configurations. It explains persistent and occasional
first-failure shifts using actual frequency counts and connects the nested
depth extension to the selected request and benchmark source. These additions
use existing checksummed evidence; no actual instruction trace is reconstructed.
`scripts/audit_report_explanations.py`, included in `make audit-report` and
`make audit`, independently checks 66 files (61 logs and five source/configuration
files), then recounts the five failure-index distributions and all nine depth
extension sequences. Explicit checks remain active with Python optimization.
This verifies the source facts supporting those passages; it does not bind
arbitrary natural-language claims or prove a causal execution trace.

The [fresh-host protocol](../experiments/2026-11-22/ACCEPTANCE_PROTOCOL.md)
is registered before measurement. It plans 30 comparison calls (15 pairs),
40 separate replay calls and five benchmark builds across five case hosts.
Its acceptance check requires integrity, complete observations, explicit
provenance and no inner timeout or schedule-budget truncation. It does not
require historical timing/failure metrics to match. The actual workflow result
and archive will be recorded after the run; this registration is not a pass.
