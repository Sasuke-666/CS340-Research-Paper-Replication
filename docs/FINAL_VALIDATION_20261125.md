# Final integration validation — 25 November 2026

Dates use Macau/Beijing time (UTC+08:00). This record covers the v1.0.2
integration of PRs #7 and #8, subsequent maintainer fixes and the new document
freeze. Original benchmark measurements and member command transcripts remain
at their recorded dates.

## 1. Inputs and authorship

- Starting final revision: `10ff18acd17d3acd6ccda3d5582c8eecbb496c88` (`v1.0.1`).
- He Boyu PR #7: head `e4db8da35b3e4b298ebd14124830203375e08f74`; submitted
  24 November; normally merged on 25 November as
  `e81bf14524c26dda4de4142ae7e4f7c5ca5d3674`.
- Li Yangshuo PR #8: head `69484e39843a9cb5610246abe35183bfd36fca13`;
  four original member commits submitted 24 November. The integration commit
  preserves that head as a parent and records subsequent fixes as maintainer work.

Original head checks: [PR #7 push](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/45401264915),
[PR #7 merge preview](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/45401333821),
[PR #8 push](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/45415294132),
and [PR #8 merge preview](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/45415308401).
The PR #8 preview used temporary merge `b78c79d42e5f4b9936126862cc057e5b48035675`;
its push run checked `69484e3`. Those runs establish their own revisions.

## 2. Reproduced defects and corrections

| Issue reproduced during review | Correction and targeted verification |
| --- | --- |
| A total/round/runner footer with trailing whitespace could evade position detection, allowing an end marker after the runner footer | Use consistent footer whitespace rules and reject missing positions; valid whitespace remains accepted, invalid order and split footer cases fail |
| The independent acceptance recount ignored test/error events outside the start/end body | Scan both surrounding regions and reject such events; negative tests recompute the changed fixture hash so the parser boundary itself is exercised |
| The validation manifest checked only a leaf symlink and accepted a symlink parent | Check every path component and resolved containment; reject leaf links and parent links to both internal and external directories |
| Two member records labelled the v1.0.1 audit as 22 November, before that release existed | Record the verified 24 November submission date and a 25 November correction note; leave raw transcripts and 22 November measurements unchanged |
| A new contribution row left main inconsistent with the ready v1.0.1 source manifest | Prepare a separate v1.0.2 freeze and check every ready manifest in regular CI |

Five new maintainer test methods produced 13 failing subcases with the old
implementations and passed after the fixes. They supplement the three PR #7
tests and PR #8's parser, metric and manifest checks. Synthetic fixtures add
no research observations.

The retained Windows logs omit checkout SHA, execution time and interpreter
identification. They remain member-submitted local records. Current continuous
checks identify their own checkout and platform; no new Windows benchmark run
or personal oral approval is inferred from either form of evidence.

## 3. Integrated checks

Local integrated checks used Python 3.12.14 with the pinned report dependencies
(`python-docx` 1.2.0, ReportLab 4.4.9 and CairoSVG 2.8.2):

| Check | Observed result |
| --- | --- |
| `make check` | 189 tests, all passed, no skips; tracked-file rules passed |
| `make audit` | Passed all historical, member, capacity, acceptance, report and explanation checks |
| Independent acceptance metrics | 30 comparisons, 10 method groups and 5 paired case rows; JSON, CSV and Markdown outputs reconciled |
| Member validation manifest | 10 files, 45,816 bytes, hashes and sizes verified |
| Historical parser contract | Both parsers agree on 166 complete archived logs; malformed fixture cases remain rejected |
| Raw-record preservation | All 11 original PR #8 command transcripts equal their original Git blobs; experimental results and figure sources retain the baseline bytes |
| Whitespace review | `git -c core.whitespace=cr-at-eol diff --check HEAD` passed; original Windows CRLF logs preserved |

Source freeze `0940ffbebb7556d515c85281adc2a8d87449eb34` passed
[workflow 45479682950](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/45479682950).
Linux Python 3.9 and 3.12, the Python 3.12 report exports, and the native Windows
archived-evidence audit all passed. The new independent acceptance and manifest
checks ran in both platforms. The preparing manifest correctly skipped document
publication. The same commit is the recorded PR #8 integration, with the original
member head preserved as its second parent.

## 4. Document freeze and delivery

All six exports use source `0940ffbebb7556d515c85281adc2a8d87449eb34`.
The English report PDF has 20 pages and the Word rendering has 16. Every page
was visually reviewed. The Word file's 14 tables and 493 cells match the frozen
source; the four figures and 18 captions remain complete. Both formats retain
36 distinct evidence URLs. Contribution Table 13 includes PRs #7 and #8.

The presentation has 14 slides, nine native tables, one native chart with its
embedded workbook, 14 Chinese notes and 47 source URLs. All 14 slide previews
and 14 PDF pages were inspected. Its 39 relationship files resolve all 94 internal
targets. The chart, workbook and chart relationship are byte-identical to v1.0.1.
Only the cover and contribution slide change their displayed text; the other
12 slide XML parts are unchanged. Speaker notes match the frozen source.

The Chinese handbook has three pages in Word and PDF. All pages were checked,
including member duties, rehearsal and the course arrangements still awaiting
confirmation. Its two tables contain 26 cells. Page breaks before member roles
and defence questions keep those sections together; 12 navigation links formerly
using main are fixed to the source commit. Office previews used LibreOffice.

No clipping, overlap or missing text was found in the final page checks. An
initial visual concern about two report captions was resolved by inspecting the
PDF content and full-page renders; no exporter or document defect was confirmed.

[FINAL_RELEASE.json](../submission/FINAL_RELEASE.json) binds the six reviewed
exports and 27 source files to the source commit and source workflow. The ready
manifest is checked before publication. The final repository commit is identified
by the `v1.0.2` tag and by `DELIVERY.json` in the complete ZIP. The publishing
workflow rechecks the source and document bytes, requires passing Linux/Windows
jobs at that delivery commit, and verifies all seven release asset digests.
Earlier v1.0/v1.0.1 tags and assets are retained.

Course registration, submission receipts and personal rehearsal are tracked in
the [closeout record](PROJECT_CLOSEOUT_20261125.md) and require actual course or
student confirmation.
