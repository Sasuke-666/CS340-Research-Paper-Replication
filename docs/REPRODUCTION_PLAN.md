# Historical PERIOD pilot plan — 7 November 2026

This document preserves the initial pilot's questions and proposed next steps.
The later five-case comparison, adapted baseline, member studies and capacity
diagnostic are defined in the
[current report](../report/EXPANDED_REPORT.md),
[comparison protocol](../experiments/2026-11-07/COMPARISON_PROTOCOL.md),
[compatibility protocol](../experiments/2026-11-07/COMPATIBILITY_PROTOCOL.md) and
[capacity protocol](../experiments/2026-11-14/LAYOUT_PROTOCOL.md).
Use [MEMBER_ACTIONS_ZH.md](MEMBER_ACTIONS_ZH.md) for the current group plan and
[WEEKLY_PROGRESS.md](WEEKLY_PROGRESS.md) for actual delivery dates.

Paper: Cheng Wen, Mengda He, Bohao Wu, Zhiwu Xu and Shengchao Qin,
*Controlled Concurrency Testing via Periodical Scheduling*, ICSE 2022,
DOI 10.1145/3510003.3510178. Paper 4 in the course list.
The owner confirmed the group's selection on **7 November 2026**. This records
confirmation received on that date, not a newly requested change of paper.

## Questions scoped for the pilot

| ID | Claim and original location | Scope and measurement | Decision rule |
| --- | --- | --- | --- |
| C1 | Table 2, PDF p. 9: PERIOD detects assertion failures in CS.reorder_3_bad and CS.reorder_4_bad | Original programs; first failing schedule, total explored schedules and buggy schedules, at depth bound 3 and a 10,000-schedule budget | Report each metric and its difference separately. Exact agreement for one row does not establish the entire table. |
| D1 (supplementary diagnostic) | Robustness of saved-witness replay, motivated by the paper introduction/section 3 | Replay one actual saved witness from each selected program and from the separate double-free smoke example | Report actual expected-error signatures in five trials each; do not generalize five trials into universal determinism. |

The authors' double-free README example is an installation smoke check, not a
Table 2 result. At the pilot stage, SERIAL and other tools had not yet been run;
the pilot made no comparative speedup or bug-finding superiority claim.

C1 was the pilot's single formally scoped paper claim and mapped to the two
specified Table 2 rows. D1 was an additional robustness diagnostic, not an independent
claim that the original paper reports a particular replay success rate.

## Execution and extension

Upstream source is pinned to `cb8deb9a176e5bb292d70d46557dd61dc0e98069`.
The executable pipeline and budgets are documented in
[`PROTOCOL.md`](../experiments/2026-11-07/PROTOCOL.md).
The first pilot used three invocations per case. All nine runs are retained.

After observing variation in the smoke and four-thread cases, a separate
[`FOLLOWUP_PROTOCOL.md`](../experiments/2026-11-07/FOLLOWUP_PROTOCOL.md) was fixed
before running targeted diagnostics. It changes only the depth bound (1, 2, 3)
on the unchanged three-thread binary, with three balanced-order repetitions per
setting. This is a configuration-sensitivity extension, not a new scheduling
algorithm. Replay checks use exact pattern lines from the first pilot.

## Evidence and interpretation

Read [`PILOT_REPORT.md`](../report/PILOT_REPORT.md) for measured outcomes and
verdicts, `results/2026-11-07/` for raw evidence and hashes, and
`docs/DEVIATIONS.csv` for environment and scope differences.
Report mean and sample standard deviation; preserve null first-error positions
for runs with no failure. A successful workflow is operational evidence only.
An assertion or sanitizer signature establishes a target failure; no detected
failure within a bound does not establish correctness.

## Next steps proposed at the pilot stage

The group proposed studying the results, tracing table values to raw evidence
and arranging an independent member rerun before deciding whether to broaden
the original-case set. Those were internal quality steps; subsequent work and
the completed independent rerun are recorded in the current links above.
Retain the original selection rationale, failed attempts and measurement dates.

The published requirements include substantive contributions from each member's
own account, meaningful weekly pushes, a final English PDF, a presentation
following the separate instruction and a final `v1.0` tag. Current registration,
team-allocation and final-submission information still requires the actual
course evidence identified in [COURSE_REQUIREMENTS.md](COURSE_REQUIREMENTS.md).
