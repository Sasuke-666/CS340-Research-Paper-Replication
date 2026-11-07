# PERIOD reproduction plan

Paper: Cheng Wen, Mengda He, Bohao Wu, Zhiwu Xu and Shengchao Qin,
*Controlled Concurrency Testing via Periodical Scheduling*, ICSE 2022,
DOI 10.1145/3510003.3510178. Paper 4 in the course list.
The owner confirmed the group's selection on **7 November 2026**. This records
confirmation received on that date, not a newly requested change of paper.

## Scoped questions

| ID | Claim and original location | Scope and measurement | Decision rule |
| --- | --- | --- | --- |
| C1 | Table 2, PDF p. 9: PERIOD detects assertion failures in CS.reorder_3_bad and CS.reorder_4_bad | Original programs; first failing schedule, total explored schedules and buggy schedules, at depth bound 3 and a 10,000-schedule budget | Report each metric and its difference separately. Exact agreement for one row does not establish the entire table. |
| D1 (supplementary diagnostic) | Robustness of saved-witness replay, motivated by the paper introduction/section 3 | Replay one actual saved witness from each selected program and from the separate double-free smoke example | Report actual expected-error signatures in five trials each; do not generalize five trials into universal determinism. |

The authors' double-free README example is an installation smoke check, not a
Table 2 result. SERIAL and other tools have not been run; no comparative speedup
or bug-finding superiority is claimed.

C1 is the single formally scoped paper claim and maps to the two specified
Table 2 rows. D1 is an additional robustness diagnostic, not an independent
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

## Remaining assessed work

All group members must review and understand the experiments, record their own
substantive contributions, and have another member rerun the documented pipeline.
Decide whether to extend the original-case set after reviewing these results;
retain selection rationale and failed attempts. Obtain the separate presentation
instructions, produce the final English PDF and presentation, and tag `v1.0`
only for the final submission. Continue meaningful weekly pushes.
