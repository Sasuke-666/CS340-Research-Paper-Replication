# PERIOD pilot protocol — 7 November 2026

The group confirmed PERIOD (ICSE 2022) on 7 November 2026. This document is a
prospective protocol, not a statement that any experiment has succeeded.

## Fixed source and scope

Authors' repository: https://github.com/wcventure/PERIOD
Commit: `cb8deb9a176e5bb292d70d46557dd61dc0e98069`.
Paper: https://wcventure.github.io/pdf/ICSE2022_PERIOD.pdf

Selected before execution: the README `test/doubleFree` installation check,
followed by `CS.reorder_3_bad` and `CS.reorder_4_bad` from Table 2 (PDF page 9).
The smoke example is not itself a Table 2 row and will be reported separately.
Selection rationale: validate the installed runtime first, then compare two
small original cases with different thread counts without replacing the
benchmark programs. This is a reduced-scale pilot, not the full 36-program study.

Table 2 reference values (first buggy schedule / total schedules / buggy
schedules): reorder_3 = 6 / 27 / 6; reorder_4 = 9 / 100 / 12. These are published
reference numbers, not measurements from this project. README smoke reference:
3 / 6 / 4. A buggy schedule is not a distinct bug.

## Measurements

Three separate invocations per case; depth bound 3; schedule budget 10,000;
90-second outer limit per invocation. Run sequentially because the upstream
runtime uses a fixed shared-memory key. Record raw stdout/stderr, command,
exit status, start/end UTC, elapsed wall time, first reported buggy schedule,
explored schedule count, error witnesses, and checksums. Preserve failed,
incomplete, timed-out and successful attempts. An exit code of zero alone is
not evidence of successful schedule control or a reproduced scientific claim.

Reference: paper section 4.1.3 uses 10 repetitions, Xeon Silver 4214, Ubuntu
18.04, GCC 7.5 and LLVM 10.0. Our pilot uses 3 repetitions to satisfy the course
minimum, records actual hardware and software, and treats outer time limits,
hosted execution, and dependency-image provenance as explicit deviations.
No cross-machine runtime speedup claim will be made.

## Environment and integrity

Use the authors' Docker image only on an isolated disposable Linux runner.
Resolve its tag to an immutable digest once and record that digest. Overlay the
pinned upstream checkout and rebuild its static-analysis/instrumentation layer.
Compiler, SVF and other installed dependencies remain those in the recorded
image; they are not claimed to be a fully rebuilt 2022 environment. No credentials,
private Git configuration, host network or Docker socket enter the container.
The current local session lacks Docker and CAP_SYS_NICE, so it cannot establish
native PERIOD results; the hosted run is an explicit feasibility test.

## Acceptance and follow-up

Confirm controlled scheduling and inspect actual error witnesses before calling
any Table 2 outcome reproduced. Compare counts with the reference using absolute
and relative differences; report mean and sample standard deviation, including
zero variation when actually observed. A failed build is a failed feasibility
step, not evidence against the paper. A budget-censored result remains censored.

After a valid baseline, the proposed single-factor extension is to vary the
depth bound on one unchanged benchmark; define it before collecting extension
results. No SERIAL or other baseline advantage is claimed until that baseline
has actually been run under matched conditions. Human review and independent
rerunning by a different member remain required. See `docs/AI_USAGE.md` for the
course-required assistance disclosure.
