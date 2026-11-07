# Follow-up protocol — fixed after pilot, before follow-up execution

The first pilot is GitHub Actions run 42368129299, artifact 13571979839.
Its nine runs are retained in full. The three-thread case matched 6/27/6 in all
three runs. The four-thread case explored the same 100 schedule descriptions in
each run but reported first-error positions 13/9/13 and error counts 12/12/8.
The double-free smoke example reported 4/3/4 errors on identical six-schedule
lists. These observations motivate execution/replay checks; they do not establish
a hardware, kernel or implementation root cause.

## Preflight and source control

Use the same pinned source and the first run's immutable image digest:
`wcventure/period@sha256:8f47d8b9148f2db579627842026e722d0f205ddeab13e70ee41a8df3dbd59fbc`.
Before testing, a separate child process attempts SCHED_DEADLINE and records its
return code, errno and observed scheduling policy. Failure stops this study.
The hosted machine is new: do not pool its timings with the first pilot as a
single-machine experiment. Rebuild the benchmarks and record the actual CPU.

## Extension: depth-bound sensitivity

Research question: with the identical three-thread benchmark and binary, how do
bounds 1, 2 and 3 change exploration cost and observed bug discovery? Table 2
reports a depth-3 configuration; the depth-1 and depth-2 configurations are the
proposed extension. This tests configuration sensitivity, not a new scheduler.

Hold machine, input, binary, instrumentation, budget (10,000) and outer timeout
(90 seconds) fixed. Run each depth three times. The predeclared order is
(1,2,3), (3,1,2), (2,3,1), balancing early and late positions. Keep no-bug results
as no-bug-within-bound; they are not proofs of correctness. Preserve all runs.

## Fixed-witness replay

Replay three actual stored pilot witnesses five times each, without editing the
benchmarks. Use the exact pattern line from these original artifact paths:

- `witnesses/reorder_3_bad/out_reorder_3_bad_1/Errors/000001_0000006_assertion-failed`
- `witnesses/reorder_4_bad/out_reorder_4_bad_2/Errors/000001_0000009_assertion-failed`
- `witnesses/df/out_df_1/Errors/000004_0000006_double-free`

Report the expected assertion/double-free signature, timeout, exit status and
raw log separately. The wrapper may return zero after printing a target failure;
its exit status alone is not the bug oracle. These are targeted diagnostics
chosen after observing the pilot, not independent confirmation of the entire
paper. Five successes do not prove universally deterministic replay.
