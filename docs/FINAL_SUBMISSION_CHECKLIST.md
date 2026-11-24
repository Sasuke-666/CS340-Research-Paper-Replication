# Final submission and rubric map

Prepared 24 November 2026, Macau/Beijing time (UTC+08:00). The owner confirmed
23–29 November as the final working week. PR #6 is integrated, and `v1.0` is
published. The `v1.0.1` document revision uses the same Linux/Windows checks and
six-document manifest. This map uses the five-page instructor
project document, read in full on 24 November. [The requirements record](COURSE_REQUIREMENTS.md)
distinguishes its clauses from internal preparation choices. Actual publication,
tag and delivery status are recorded in [final validation](FINAL_VALIDATION_20261124.md).

## 1. Final deliverables

| Deliverable | Required outcome | Maintained entry point |
| --- | --- | --- |
| Final report | English PDF, numbered/referenced figures and tables, citations, contribution statement and AI usage statement | [Report source](../report/EXPANDED_REPORT.md), [export instructions](../report/README.md) |
| Final presentation | Group presentation following the separate Presentation Instruction when obtained | [Presentation source and notes](../presentation/SLIDES.md), [delivery instructions](../presentation/README.md) |
| Final repository | Reproducible code/evidence, genuine dated contributions and final version tagged `v1.0` | [README](../README.md), [contributions](CONTRIBUTIONS.csv), [weekly progress](WEEKLY_PROGRESS.md) |

Editable documents, rehearsal timing and additional review maps support group
preparation. The supplied project document fixes the report's PDF format; the
presentation upload format and precise final deadline remain external facts.

## 2. Report evidence against the published rubric

| Criterion | Weight | Evidence to inspect |
| --- | ---: | --- |
| Reproduction results | 30% | Report §§1–4: two scoped claims; paper comparison in Tables 2–3; mean and sample SD; explicit n; Figures 1–2; [primary summary](../results/2026-11-07/summaries/comparison-42381922637/SUMMARY.md) and [four-thread follow-up](../results/2026-11-07/summaries/comparison-42384122902/SUMMARY.md) |
| Critical analysis | 30% | Report §§3–5 and §8: C1 partially supported; C2 supported within the stated released-driver comparison; signed/relative gaps, censoring, compatibility probes, failure frequencies, controlled capacity intervention and limits |
| Reproduction setup | 15% | Report §2 and Appendix A: upstream source/image pins, case/host scopes, each driver's depth definition, modified files and the complete consequential [deviations table](DEVIATIONS.csv) |
| Extension | 15% | Report §6: `reorder_3` depth 1/2/3, n=3 per condition, balanced order, fixed input/host/binary and a source-backed interpretation; [archived extension](../results/2026-11-07/followup/) |
| Writing | 10% | Report structure, numbered figures/tables and narrative callouts; references; §10 contribution/usage disclosure; [report audit](../scripts/audit_report.py) plus actual visual review of the final exports |

Overall conclusion: **partially reproduced**. Exact schedule-count agreement
and discrepancies in failure-related observations are both retained. Each
interpretation uses its stated evidence scope. This map records supporting
evidence; the teaching team assigns the mark.

## 3. Repository evidence against the published rubric

| Criterion | Weight | Evidence and final action |
| --- | ---: | --- |
| Weekly commits | 30% | [Dated progress](WEEKLY_PROGRESS.md) retains earlier push evidence; publish this week's substantive final integration with real identity/date and verify its own workflow |
| Reproducibility/environment | 25% | README commands, pinned source/dependency image, scripted workloads and host records; [22 November acceptance](VALIDATION_20261122.md#6-subsequent-strict-review-and-live-acceptance) rebuilt all five cases and recorded 30 complete comparisons plus 40 separate diagnostics |
| README/code quality | 25% | README purpose/setup/build/run/output/runtime guidance; [Makefile](../Makefile), [source credit](SOURCES.md), retained upstream license and documented modifications |
| Individual contributions | 10% | [Roster](TEAM.csv), [contribution ledger](CONTRIBUTIONS.csv) and original member-account PRs; [PR #6 review](reviews/1240000576-presentation-check-20261122.md) adds secondary verification and rehearsal corrections, with original measurement attribution preserved |
| Commit/repository management | 10% | Meaningful messages with name/student ID; tracked-file checks and `.gitignore`; preserved provenance; actual verified final revision tagged `v1.0` |

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

## 5. Final closeout sequence and actual status

1. PR #6 was normally merged on 24 November as `7941e2b049bf80cddb0b8be723411badedab19b7`.
   Its 22 November member submission date is preserved. The final revision
   repairs archive portability and reconciles the report, slides, contributions
   and revision date.
2. The release checks `make check`, `make audit`, native Windows archive
   verification, and the frozen export/source hashes. Final page/slide review
   and the published revision's own CI results appear in the validation record.
3. The initial release is tagged `v1.0`. The clearer report and presentation
   revision is `v1.0.1`; its `submission/` manifest and bundle record the exact
   source commit and document hashes. Both releases remain available.
4. Submit through the confirmed course route and retain the actual receipt.
   Use [the Chinese guide](MEMBER_ACTIONS_ZH.md) for member preparation and the
   internal ten-minute rehearsal. Personal explanation is established by the
   students' actual participation.

Only three external information groups remain: exact final submission
deadline/route and receipt; the separate presentation instruction and confirmed
session; and group-registration/fourth-member arrangements. The supplied source
lists December 1 as tentative presentation and requires four students, with the
teaching team assigning additional members to smaller groups. The roster records
the three confirmed students. These facts remain explicit while final technical
work proceeds.
