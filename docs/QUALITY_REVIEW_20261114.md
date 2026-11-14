# Course-evidence review for the third project week

Review date: 14 November 2026, using the task's Macau/Beijing planning date.
Baseline inspected: `0dc19a89cfe82439ebffa78e8f8bdd6c2201f7bb`.
This document records a repository review. It does not certify a student's
personal review, assign a predicted mark, or establish an unverified deadline.
Later implementation and validation records should be read alongside it.

The baseline findings in sections 2–3 explain why changes were selected.
Section 6 records their current disposition, so an old finding is not an open
task after its repair has been implemented and verified.

## 1. Basis and calendar

The criterion mapping below uses [COURSE_REQUIREMENTS.md](COURSE_REQUIREMENTS.md),
the repository's page-referenced transcription of the instructor-provided
five-page project document. The original
`2609_CS340_Research_Paper_Replication(1).pdf` supplied by the owner was reread
during this update. The transcription matches its weekly Sunday check, commit
identity, English PDF submission, report weights, single-factor extension and
assistance-disclosure requirements.
The course PDF is not redistributed. Current course-platform announcements,
the registration receipt and the separate presentation rubric remain unavailable;
those sources must settle later changes and unresolved submission details.

The third full week after the 25 October formation deadline is 9–15 November.
The baseline's latest commit was published on 8 November. Its first two weeks
have dated evidence in [WEEKLY_PROGRESS.md](WEEKLY_PROGRESS.md); that prior work
does not itself establish substantive progress in the third week. The new
protocol and execution code were published as
[`bddb831`](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/commit/bddb831319679c30586d9bbe689fb11b897f1a14).
The [push-triggered study run](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/43570556202)
was created on 14 November at 15:19:28 UTC+08:00. This server-side timestamp
supports publication of substantive third-week work independently of the
editable local commit date. Its experiment outcomes are assessed separately
from the fact of that publication. The course
requires at least one meaningful group push during each week and gives Sunday
23:59 as the check time without identifying a timezone in the transcribed
source. This review uses local dates for planning and does not add a requirement
that every member commit every week.

## 2. Report criteria: evidence and remaining work

| Course criterion | Weight | Evidence already present at the inspected revision | Work with useful scoring value |
| --- | ---: | --- | --- |
| Reproduction results | 30% | Five original programs; ten primary repetitions per condition; separately registered three-pair four-thread completion study; paper-versus-observed tables, sample SD and raw logs | Preserve the 106/96/43 attempted/complete/matched distinction; present the submitted independent `account` host as a separate corroboration, with its own sample and limits |
| Critical analysis | 30% | Separate C1/C2 verdicts, quantified gaps, original IPC failure diagnosis, preserved censoring, printed-sequence checks and inconclusive replay diagnostic | Investigate one unresolved discrepancy with a declared, controlled question; distinguish implementation-level findings from claims about the historical paper executable |
| Reproduction setup | 15% | Pinned upstream revision and container digest; per-batch hardware/kernel/compiler; protocol chronology; [deviations table](DEVIATIONS.csv) | Keep new diagnostic or host settings explicit; add each consequential deviation and avoid pooling host timings |
| Extension | 15% | Balanced single-factor depth-bound study, three runs per level, linked to the search/coverage question | State exactly which variable changes in any new extension and which mechanism it tests; retain the established depth study as a separately scoped result |
| Writing | 10% | English report, numbered tables and figures, paper/code citations, contribution and generic assistance statements | Add a concise mechanism explanation; reconcile newly submitted evidence and current dates; regenerate and visually check the final PDF/Word outputs |

The five-case study supports selected local claims. The report's overall
**partially reproduced** verdict follows the documented first-failure and
buggy-schedule discrepancies. A reduced scope is allowed by the course source;
scope must remain explicit. More runs alone do not resolve the causal questions.

## 3. Repository criteria: evidence and remaining work

| Course criterion | Weight | Evidence already present | Remaining check or improvement |
| --- | ---: | --- | --- |
| Weekly commits | 30% | Initial preparation, first full week and second full week have genuine dated changes; second-week server-side push checks are linked | Publish this week's substantive implementation/analysis with its actual date and preserve remote verification |
| Reproducibility and environment | 25% | Pinned source/image, isolated Docker execution, source and binary hashes, raw manifests, independent summaries; one member submitted a clean-host rerun | Include the merged member batch in the default archive audit and continuous checks; retain failed setup attempts |
| README and code quality | 25% | Build/run/audit/report commands, runtime limits, tests and maintained source | Reconcile stale permission/task statements and make the current study entry point clear; verify that documented commands cover every maintained result |
| Individual contributions | 10% | Li Yangshuo's PR #2 and He Boyu's PR #1 are merged with their original authors and substantive commits preserved | Keep actual work and assistance accurately attributed; personal understanding and any later human review require the members' own completion |
| Commit quality and management | 10% | All inspected subjects include the responsible student's full name and ID; meaningful merge history and ignored generated outputs | Preserve author history; use a final `v1.0` tag only for the actual final version, after final requirements and materials are settled |

### Concrete maintenance findings at the baseline

1. `make audit` and the comparison audit target cover the 7 November archives.
   They do not yet include the merged member `account` batch, although it has a
   checked-in summary and 880 manifest entries. Its verification needs the
   explicit single-case design, `--cases account --repeats 10`, and summary
   comparison mode.
2. The end of README still describes contributors' write access and individual
   contributions as needing checks, while its opening section records the
   successful submissions and integration. Current-state wording should agree.
3. The member action list contains a clearly labelled earlier snapshot, but
   subsequent unchecked action items still repeat that He Boyu has read-only
   access and both assigned submissions are absent. Completed tasks belong in
   the completed section; historical snapshots should remain dated history.
4. The assistance statement has an empty line inside its table before the last
   two rows. Removing that formatting defect restores a single readable table
   while preserving the disclosure.
5. The report exporter and source-snapshot filename still carry the initial
   stage date. New output names and titles should identify the actual revised
   study without changing the dates of old observations.

## 4. Member evidence already completed

Li Yangshuo, 李扬烁, 1240001156 (`barkhorn996`), submitted a separate WSL2
`account` batch: 20 complete method calls, ten per method, a retained failed
image-pull attempt, environment metadata and the review at
[1240001156-clean-run.md](reviews/1240001156-clean-run.md). Commits `8ce522d`
and `9f30843` reached main through PR #2 and merge `c35bd0e`.

He Boyu, 何博宇, 1240000576 (`heboyu0714`), submitted
[1240000576-evidence-audit.md](reviews/1240000576-evidence-audit.md), including
executable recounting of 26 four-thread logs and separate treatment of the ten
censored runs. Commit `b02adef5` reached main through PR #1 and merge `ff254d8`.

These completed submissions should not be reassigned as though missing.
Subsequent cross-review is useful group quality work. The supplied instructor
text does not make oral sign-off or a particular cross-review file an additional
Git-history rule. Original contribution records and the generic assistance
statement are retained in [CONTRIBUTIONS.csv](CONTRIBUTIONS.csv) and
[AI_USAGE.md](AI_USAGE.md).

## 5. Items requiring external information or real participation

The repository cannot independently establish the fourth member or the teaching
team's allocation, the submitted group-registration receipt, the first weekly
check date/timezone, the exact final-report deadline, the final submission
portal, or the separate presentation rubric. These items need the actual
course communication or registration evidence.

The existing experiments support preparing an accurate explanation and a
defence outline now. Duration, slide count, required speaking allocation and
presentation grading should remain unspecified until their source is supplied.
Each member must personally understand and explain the work attributed to them.
No automated audit can record that personal completion on their behalf.

## 6. Current disposition of the findings

| Finding or improvement | Implemented result and evidence |
| --- | --- |
| Merged member archive absent from the default audit | `make audit-member` now verifies the submitted single-case batch with ten repeats per method and checks its saved summary. All 20 calls and 880 manifest entries passed; the target is included in `make audit` and continuous checks. See [Makefile](../Makefile) and [member summary](../results/member-reruns/1240001156-account-20261108T122201Z-summary/SUMMARY.md). |
| Independent host evidence mentioned only in the contribution discussion | The report now has a separate independent-host section and Table 8, with mean ± sample SD, the paired timing difference, paper gaps and host limits. The 20 calls remain outside the 106-attempt primary/follow-up accounting. |
| Full deviations available only as a repository CSV | Report Appendix A places the complete consequential differences inside the report source for inclusion in the submitted PDF; the maintained CSV remains the detailed machine-readable source. |
| Method explanation too compressed | The report explains the execution periods, final parallel period and feedback-guided exploration before the measurements. A source-backed [talk outline](../presentation/TALK_OUTLINE.md) explains the questions, findings and evidence demonstration. |
| Completed member work repeated as current pending tasks | [MEMBER_ACTIONS_ZH.md](MEMBER_ACTIONS_ZH.md) now separates completed submissions, current review suggestions and genuine course-information gaps; historical snapshots remain linked. Both existing member PRs and author identities are preserved. |
| Inconsistent README access/task statements | The current README identifies the integrated submissions and presents the separate third-week study. Course information still needing verification is explicitly separated. |
| Broken assistance-statement table | [AI_USAGE.md](AI_USAGE.md) retains the required generic disclosure as a continuous table. No completed personal sign-off is inferred. |
| Initial-stage filenames on revised outputs | The report exporter, member-checklist exporter and workflow snapshot names now use the 14 November revision date; historical measurement dates remain unchanged. Output rendering is verified at final publication. |
| Uninvestigated native/Python array-capacity mismatch | The [registered layout protocol](../experiments/2026-11-14/LAYOUT_PROTOCOL.md), actual native declaration probe and two independently audited case/host samples test the single capacity intervention. Each available case has 20 complete eligible calls and ten pairs. The field alignment and feedback change are verified; first-failure gaps persist. |
| Presentation preparation limited to a short checklist | A twelve-slide editable English rehearsal draft now follows the source-backed outline, with seven native tables, two native data charts, Chinese speaker notes and per-slide source links. It includes the original/recovery distinction and actual diagnostic results. Official presentation requirements remain an external information item. |

The original layout study's [formal `lazy01` summary](../results/2026-11-14/summaries/layout-43570556202-lazy01/SUMMARY.md)
has 20 complete, eligible invocations and ten complete pairs. Its 304-entry
outer manifest and 300-entry case manifest passed verification. The corrected
reader changes the observed default feedback hash while both arms request
39 schedules. Its first-failure mean remains 8.200 ± 0.422 against the paper's
reference of 3. This controlled result narrows the interpretation of the layout
repair and adds substantive critical analysis. The same workflow's `account` job has
terminated with a failure status. Two final artifact listings contain no
downloadable `account` archive, and its job-log endpoint returns 404. The
[final observation record](../experiments/2026-11-14/account-evidence-failure/FINAL_OBSERVATION.json)
preserves that evidence-availability failure. The original `account` attempt
count, completion count and workload-failure cause remain unknown. Missing
measurements are not zero observations.

The activated [recovery protocol](../experiments/2026-11-14/ACCOUNT_RECOVERY_PROTOCOL.md)
was published in `ea273fe4` before
[recovery run 43575584325](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/43575584325).
It specified one fixed `account` batch on a new host, preserving the original
runner bytes and predeclared ten pairs. The recovery archive was preserved by
both Git and a backup ZIP. Its [formal summary](../results/2026-11-14/summaries/layout-recovery-43575584325-account/SUMMARY.md)
passes with 20 attempted, complete and eligible calls, ten pairs, 571 verified
outer-manifest entries and 557 case-manifest entries. Both arms request 65
schedules. The corrected first-failure mean is 10.200 ± 0.632, compared with
the paper's reference of 2. The two cases' buggy-schedule changes have opposite
signs, so the report makes no uniform effectiveness-improvement claim.

The recovery retains its own run identity and paired analysis. Its observations
cannot supply the missing original denominator. The original `lazy01` sample
and recovered `account` sample remain distinct case/host scopes. The earlier
106/96/43 accounting and the independent member's 20 calls remain unchanged.

The actual study outcomes and evidence-availability failure are incorporated
into the current report and presentation materials. Publication verification is
recorded in [VALIDATION_20261114.md](VALIDATION_20261114.md). The remaining
course/user-dependent items are precisely those in section 5.

## 7. Review conclusion

The baseline contains substantial reproducible experimental work and genuine
member-account submissions. The strongest third-week work is a controlled
investigation of a remaining limitation, supported by current archive checks
and an updated explanation of what the evidence establishes. Routine formatting
repairs help readability; they do not substitute for that substantive progress.

Full marks remain an instructor decision across the separately assessed report,
presentation and repository. This mapping identifies evidence and actual gaps
without treating proposed internal milestones as instructor deadlines.
