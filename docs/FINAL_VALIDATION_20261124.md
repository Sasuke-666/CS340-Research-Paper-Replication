# Final integration and validation, 24 November 2026

The owner identified 23–29 November as the final working week and requested
completion of the repository, report and presentation. The supplied instructor
requirements were read again in full. The technical delivery uses the final
`v1.0` release; course submission and the actual oral presentation are separate
events. All dates below describe actions that actually occurred.

## 1. Accepted member work

PR #6, submitted through He Boyu's own account on 22 November, was normally
merged on 24 November as `7941e2b049bf80cddb0b8be723411badedab19b7`.
Its two original member commits and authors were retained. An independent
review matched all six raw twostage logs and their published statistics. The
52-line Linux transcript excerpt matched the actual workflow job, while the
reported Windows failure could be reproduced from the original implementation.
The review adds no new measurement. See [the member report](reviews/1240000576-presentation-check-20261122.md)
and [retained transcript](reviews/1240000576-audit-20261122.txt).

## 2. Portability and release repairs

Comparison and capacity-summary paths now use forward slashes on every host.
Derived JSON/Markdown outputs use UTF-8 and LF. Original evidence bytes remain
strictly checked; changing their line endings still fails their manifests.
The new `windows-archive-audit` job disables checkout conversion and runs the
archive audits with native Python. Fresh benchmark execution remains scoped to
the README's x86_64 Linux/Docker environment.

`make audit` now includes the member's independent twostage recount. The report
exporter accepts the final revision marker and writes consistent final document
titles, metadata, filenames and headers. The final document manifest checks
required files, paths, sizes, SHA-256 hashes and source identity. The release
job waits for the Linux and Windows checks and cannot move an existing tag.

## 3. Scientific and document scope

The final report preserves all historical numeric tables and adds the N=2
exception to the drivers' depth-to-period mapping. The 22 November engineering
acceptance is reported separately: 30 complete comparisons / 15 pairs, plus 40
diagnostics and five builds. No new workload is launched in this final revision.

The main comparison still accounts for 106 attempts, 96 complete calls and 43
complete pairs. Independent member evidence, depth extension, both readable
capacity batches and the selected witness replays keep their distinct scopes.
The unavailable original account capacity batch remains unknown.

The fourteen-slide presentation and Chinese handbook use one classroom archive
demonstration: `python3 scripts/recount_twostage_acceptance.py`. It confirms
serialized twostage first failures 4, 29, 4, with mean 12.3333 and sample SD
14.4338. Source-derived necessary ordering stays distinct from a measured
instruction trace. Report/slide contribution statements include all six PRs.

## 4. Verification ledger

Local source validation on 24 November completed all 162 unit tests with
zero failures and zero skips, with the pinned report dependencies installed.
`make audit` passed, including the historical evidence checks, comparison/member
summaries, both readable capacity batches, member reviews, acceptance receipt,
six-log recount and report traceability. The report checker bound 321 table
cells (236 numeric/missing-value cells), 18 unique captions and four figures.
The explanation audit checked 66 files, 61 complete logs and nine depth runs.
`git diff --check` passed.

Visual review inspected every page of the 20-page English PDF, every page of the
16-page Word rendering, all 14 slide previews and 14 presentation-PDF pages,
and every page of the three-page Chinese handbook. Tables, figures, names,
notes, references and dates were legible without clipping or overlap. The
presentation contains nine editable native tables, one native chart with its
workbook, 14 Chinese notes and 44 source links. PDF/Word evidence hyperlinks
were retained. Word and presentation conversion used LibreOffice; no native
Microsoft Office or in-person rehearsal is claimed.

The source-freeze workflow result and the subsequent frozen-document manifest
are recorded below after publication. The final document release runs the same
Linux/Windows gates again at its exact commit before creating `v1.0` and
publishing its six documents and complete ZIP. This gate cannot move an existing
tag or replace mismatched published assets.

## 5. Course-facing actions

The remaining external facts are the exact final submission route/deadline and
receipt, the separate presentation instructions and actual session, and the
registration/fourth-member arrangement. The visible roster has three confirmed
members. The supplied project PDF gives a tentative 1 December presentation.
The release does not assert a portal upload, personal rehearsal or final mark.

Current files and final assets use generic assistance terminology. Original
contributions, experiment dates, upstream credit and earlier history remain
preserved. The [rubric map](FINAL_SUBMISSION_CHECKLIST.md) links every published
report and repository criterion to its evidence.
