# Final submission and rubric map

Updated 25 November 2026 (Macau/Beijing time). The group leader relayed the
instructor's confirmation that 孙皓扬, 李扬烁 and 何博宇 form the complete
group. The leader designated 23–29 November as the final working week.
The [requirements record](COURSE_REQUIREMENTS.md) identifies the source for
each course requirement and the limits of the available course evidence.

## 1. Final deliverables

| Deliverable | Required outcome | Maintained entry point |
| --- | --- | --- |
| Final report | English PDF with numbered/referenced figures and tables, citations, contribution statement and AI usage statement | [Report source](../report/EXPANDED_REPORT.md), [export instructions](../report/README.md) |
| Final presentation | Group presentation following the separate Presentation Instruction when obtained | [Presentation source and notes](../presentation/SLIDES.md), [delivery instructions](../presentation/README.md) |
| Final repository | Reproducible code/evidence, genuine dated contributions and final version tagged `v1.0` | [README](../README.md), [contributions](CONTRIBUTIONS.csv), [weekly progress](WEEKLY_PROGRESS.md) |

Editable documents, rehearsal timing and additional review maps support group
preparation. The supplied project document fixes the report's PDF format; the
presentation upload format and precise final deadline remain external facts.

## 2. Report evidence against the recorded rubric

| Criterion | Weight | Evidence to inspect |
| --- | ---: | --- |
| Reproduction results | 30% | Report §§1–4: two scoped claims; paper comparison in Tables 2–3; mean and sample SD; explicit n; Figures 1–2; [primary summary](../results/2026-11-07/summaries/comparison-42381922637/SUMMARY.md) and [four-thread follow-up](../results/2026-11-07/summaries/comparison-42384122902/SUMMARY.md) |
| Critical analysis | 30% | Report §§3–5 and §8: C1 partially supported; C2 supported within the stated released-driver comparison; signed/relative gaps, censoring, compatibility probes, failure frequencies, controlled capacity intervention and limits |
| Reproduction setup | 15% | Report §2 and Appendix A: upstream source/image pins, case/host scopes, each driver's depth definition, modified files and the complete consequential [deviations table](DEVIATIONS.csv) |
| Extension | 15% | Report §6: `reorder_3` depth 1/2/3, n=3 per condition, balanced order, fixed input/host/binary and a source-backed interpretation; [archived extension](../results/2026-11-07/followup/) |
| Writing | 10% | Report structure, numbered figures/tables and narrative callouts; references; §10 contribution/usage disclosure; [report audit](../scripts/audit_report.py) and [document validation](FINAL_VALIDATION_V1_0_3.md) |

Overall conclusion: **partially reproduced**. Exact schedule-count agreement
and discrepancies in failure-related observations are both retained. Each
interpretation uses its stated evidence scope. This map records supporting
evidence; the teaching team assigns the mark.

## 3. Repository evidence against the recorded rubric

| Criterion | Weight | Evidence and remaining limits |
| --- | ---: | --- |
| Weekly commits | 30% | [Dated progress](WEEKLY_PROGRESS.md) links GitHub server timestamps for the initial registration stage and one substantive push for each of the five subsequent planning weeks |
| Reproducibility/environment | 25% | README commands, pinned source/dependency image, scripted workloads and host records; [22 November acceptance](VALIDATION_20261122.md#6-subsequent-strict-review-and-live-acceptance) rebuilt all five cases and recorded 30 complete comparisons plus 40 separate diagnostics |
| README/code quality | 25% | README purpose/setup/build/run/output/runtime guidance; [Makefile](../Makefile), [source credit](SOURCES.md), retained upstream license and documented modifications |
| Individual contributions | 10% | [Roster](TEAM.csv), [contribution ledger](CONTRIBUTIONS.csv), report Table 13 and original member-account PRs #1–#8; the [closeout map](PROJECT_CLOSEOUT_20261125.md) distinguishes original measurements, secondary review, tests and maintainer fixes |
| Commit/repository management | 10% | Tracked-file checks, `.gitignore`, preserved history and required [v1.0 release](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/releases/tag/v1.0). Of 68 commits reachable at v1.0.2, [one message](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/commit/9c9af456fd98bfc7e8053fd609f46e4d2e83dd9b) contains the correct student ID but omits the full name. PR #8 establishes its author. The original commit is retained. |

The group weekly-push rule and the per-member substantive-contribution rule
have separate evidence. The assignment adds no per-person weekly quota or
mandatory internal sign-off form. Historical missed checks, if any, cannot be
repaired by relabelling later work.

## 4. Denominators to preserve during final checks

| Scope | Count and interpretation |
| --- | --- |
| Historical compatible comparison and registered four-thread follow-up | 106 attempts, 96 complete calls, 43 complete pairs; ten original outer-timeout prefixes remain censored |
| Independent member `account` host | 20 complete calls, ten pairs, separately analysed |
| Depth-bound extension | Nine calls, three per bound on `reorder_3` |
| Readable capacity diagnostic | Original `lazy01` and recovery `account`: 20 complete calls and ten pairs each; original missing `account` outcomes stay unknown |
| Member `twostage` witness study | Five replays of one selected input, five observed matching assertions |
| Fresh-host acceptance, 22 November | 30 complete eligible comparison calls / 15 pairs, plus 40 complete diagnostic calls and five builds; retained as a separate engineering batch |

The [acceptance receipt](../results/2026-11-22/summaries/acceptance-45015126850-attempt1/acceptance.json)
and [case summaries](../results/2026-11-22/summaries/acceptance-45015126850-attempt1/SUMMARY.md)
preserve the newer host scopes. Whole-driver timing differs from time to first
failure; failure-producing schedules count executions exposing a failure.
Requested schedules and source-derived partial orders keep their stated scope;
a unique measured instruction trace is unavailable.

## 5. Release and course submission

| Item | Evidence and status |
| --- | --- |
| Report, slides and handbook | The [document manifest](../submission/FINAL_RELEASE.json) identifies the document source and six file digests. [Revision validation](FINAL_VALIDATION_V1_0_3.md) identifies the checks for this revision. |
| Release history | The course-required `v1.0` tag identifies the original final submission package. `v1.0.1` revised the prose. `v1.0.2` integrated #7 and #8. `v1.0.3` is the revision for the confirmed group of three. [Release history](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/releases) |
| Course registration | Three-person grouping confirmed, as relayed by the leader. The form showed a closed status on 25 November. A registration receipt for group/paper/repository has not been verified. |
| Upload | Exact deadline, upload route, any required naming convention and a final submission receipt have not been verified. |
| Presentation | The recorded handout gives 1 December as tentative. The separate Presentation Instruction, confirmed slot and duration were unavailable in this review. [Slides](../presentation/SLIDES.md) and the [handbook](MEMBER_ACTIONS_ZH.md) support adjustable practice. Oral delivery and joint rehearsal require the three students themselves. |

The contribution ledger and the PRs distinguish the original measurements
from the member rerun, secondary recounts and maintenance tests. The
[closeout](PROJECT_CLOSEOUT_20261125.md) gives the three members' roles.
