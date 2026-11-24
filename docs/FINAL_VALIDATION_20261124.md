# Final integration and validation, 24 November 2026

The owner identified 23–29 November as the final working week and requested
completion of the repository, report and presentation. The supplied instructor
requirements were read again in full. The technical delivery uses the final
`v1.0` release, followed by the `v1.0.1` document revision in section 6.
Course submission and the oral presentation have their own completion records.

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

## 4. Verification of v1.0

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

Source freeze `d64fe8001b8f4f7caae5d4606902a66430ffddd9` was published on
24 November. [Its workflow 45350993838](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/45350993838)
completed successfully: Linux Python 3.9 and 3.12 repository checks, the report
export checks on Python 3.12, and native Windows archived-evidence verification.
The source-only commit correctly skipped document publication because it had
no final manifest. This supplies revision-specific evidence for the Windows
path/newline repair, without claiming Windows benchmark execution.

The [v1.0 manifest](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/v1.0/submission/FINAL_RELEASE.json) binds all six reviewed
documents to this source commit and the exact source-file bytes. Original Git
history and upstream credit were preserved.

Frozen-document commit `7634e7e381983d5092f9a3e764d0b84f2e4263b7` passed
the Linux/Windows checks in [run 45351419681](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/45351419681).
Its publishing job created [v1.0](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/releases/tag/v1.0)
on 24 November at 15:53:40 UTC+8, with the six documents and complete ZIP.
The workflow cannot move an existing tag or replace mismatched assets.
`DELIVERY.json` and the manifest record the source, repository and document
identities independently of the download filename.

## 5. Course-facing actions

The remaining external facts are the exact final submission route/deadline and
receipt, the separate presentation instructions and actual session, and the
registration/fourth-member arrangement. The visible roster has three confirmed
members. The supplied project PDF gives a tentative 1 December presentation.
The release does not assert a portal upload, personal rehearsal or final mark.

The [rubric map](FINAL_SUBMISSION_CHECKLIST.md) links every published report and
repository criterion to its evidence.

## 6. Document revision v1.0.1

The report paragraphs now follow the experiment and its interpretation more
directly. The slide text is shorter, and the Chinese notes are written for oral
delivery. The README puts reading and reproduction instructions before the
historical studies. This revision changes no measurements or member attribution.

Compared with `c2f41f89d8b1dd9a777602ddff651d78acd068bc`, all 116 report
table lines, 18 caption lines and four figure references are unchanged. Fixed
historical source links are unchanged; current document links use `v1.0.1`.
The README's thirteen command blocks are also unchanged.

Local source checks passed all 164 unit tests with no failures or skips, using
the pinned report dependencies. `make audit` passed, including the 321 bound
report cells and the explanation check's 66 source/log files. The added release
tests verify that a document patch publishes separately while preserving the
existing `v1.0` tag and all its assets. A preparing manifest skips publication;
only a ready, verified document manifest can trigger it.
