# Registered expanded comparison and replay diagnostic

Registered 7 November 2026 before this batch's measurements. The previous pilot
and follow-up remain unchanged. This new study is not retroactively assigned to
an earlier week. This is a reduced-scale study, not the full paper evaluation.

## Questions and predefined sample

C2: On matched original workloads, does the authors' parallel-ending scheduler
explore fewer schedules than their serialized driver while detecting failures?
C1 extension: Do the paper's selected Table 2 counts replicate beyond reorder?
D2: Is replay behavior sensitive to its calibrated scheduling-period multiplier?

The fixed selection is CS.reorder_3_bad, CS.reorder_4_bad, CS.account_bad,
CS.lazy01_bad and CS.twostage_bad. It covers four program families and 2/3/4
threads. Reorder retains continuity with the pilot; the other families broaden
coverage with modest published schedule counts. This is a purposeful sample,
not a random sample of all concurrency programs. No failed case will be dropped.

## Baseline implementation and measurements

Use the unmodified authors' run_PDS.py and run_OldPDS.py from upstream commit
cb8deb9a176e5bb292d70d46557dd61dc0e98069. Source inspection shows SBPMESched and a
mixed final period in run_PDS, versus SBPSched and period_limit = bugDepth + N - 1
in run_OldPDS. The latter is called `author_serialized` until source review and
checks against the paper's Serial counts establish the scoped correspondence.
The paper does not name this script. Matching numbers alone do not prove exact
identity with the unpublished experimental checkout; retain that limitation.
No invented baseline or replacement schedule enumerator is allowed.

Same source, built binary, workload, host and image for each paired comparison.
Use depth 3 and schedule budget 10,000; outer limit 120 seconds per invocation.
Each case has ten repetitions per method (20 calls). Alternate method order
AB/BA; run serially within a case because the shared-memory key is fixed.
Cases may use separate disposable hosted machines: do not pool absolute times
across cases or compare directly with the paper's workstation times.

Report first failing schedule, explored schedules, buggy schedules, incomplete
runs, inner/outer timeouts and elapsed whole-driver time. Preserve missing first
failures as missing. Calculate mean and sample SD only over explicitly reported
complete observations; list denominators and all incomplete trials. Do not infer
bugs from workflow return code alone. Save source, compiler, CPU, kernel, image,
commands, raw logs, binary/driver hashes and bounded error witnesses.

Table 2 reference triples (first,total,buggy), transcribed from PDF page 9:
reorder_3: PERIOD (6,27,6), Serial (10,30,10).
reorder_4: PERIOD (9,100,12), Serial (37,384,90).
account: PERIOD (2,65,26), Serial (4,136,56).
lazy01: PERIOD (3,39,12), Serial (4,60,20).
twostage: PERIOD (4,33,3), Serial (4,33,3).
Source: https://wcventure.github.io/pdf/ICSE2022_PERIOD.pdf, sections 4.1.3/4.2 and Table 2.

## Controlled replay diagnostic

After the reorder_3 comparison, use the unchanged built binary and the fixed
previously observed witness [[0,2],[2,0],[1,0]]. Compare original replay multiplier
1.5 with 6.0 (fourfold), twenty paired repetitions, alternating AB/BA order.
A diagnostic copy of the driver changes only this multiplier and adds a
post-execution parent-process print of calibration and target return code.
Save the exact patch. The comparison drivers remain unmodified.

The dry-run calibration is measured anew in each invocation, as in the original
runtime, and is retained. A changed failure rate would support sensitivity to
this configuration in this environment; it would not alone identify the root
cause of the previous pilot miss. An unchanged rate or failure to reproduce the
miss is an inconclusive diagnostic, not proof of deterministic replay.

## Evidence and publication

The expected study has 100 comparison and 40 diagnostic calls, plus five builds.
Completion is determined from actual records. All failures remain in the archive.
Each case uploads an artifact; a separate non-privileged archive job commits
only bounded source/log evidence and a checksum index to a new run-ID directory.
Automation commits identify the requesting owner and do not count as another
member's personal contribution. Required assistance disclosure remains in docs/AI_USAGE.md.
No final tag or final-grade claim is made. Group review is a separate task.

## Execution amendment on 7 November 2026

Attempt 42380166815 stopped before any benchmark was built or measured because
Python 3.6 used an ASCII locale while reading the original UTF-8 source.
The separate archive step then rejected original upstream trailing whitespace.
Both issues are corrected by explicit UTF-8 source/evidence I/O and retaining
verbatim upstream bytes in the archive. The case set, methods, order, budgets,
repetitions and diagnostic conditions are unchanged. Failed-attempt artifacts
remain linked and will be archived alongside the successful batch; none are
counted as experimental repetitions. This amendment precedes new measurements.
