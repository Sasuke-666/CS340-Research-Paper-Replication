# Review of replay variability and scheduling observations

Review date: 7 November 2026. Source revision:
`wcventure/PERIOD@cb8deb9a176e5bb292d70d46557dd61dc0e98069`.

## Findings supported by the evidence

The original follow-up observed the expected assertion in four of five replays
of the fixed `reorder_3_bad` witness `[[0,2],[2,0],[1,0]]`. The first replay
contained no expected assertion signature and did not reach the outer timeout.
That observation remains part of the evidence. A successful driver exit code
does not establish whether the target reproduced the bug.

Two subsequent diagnostic batches each tested the same witness twenty times
with multiplier 1.5 and twenty times with multiplier 6.0. The observations are
reported separately because the batches used distinct executions and their
environment provenance must remain attached to each batch.

| Batch | Multiplier | Expected assertion | Recorded target return code | Interpretation |
|---|---:|---:|---|---|
| Original follow-up | 1.5 | 4/5 | Not captured separately | One observed replay miss |
| Actions 42380929383 | 1.5 | 20/20 | -6 in all twenty | Miss not reproduced |
| Actions 42380929383 | 6.0 | 20/20 | -6 in all twenty | No observed difference from 1.5 |
| Actions 42381922637 | 1.5 | 20/20 | -6 in all twenty | Miss not reproduced |
| Actions 42381922637 | 6.0 | 20/20 | -6 in all twenty | No observed difference from 1.5 |

Each later batch therefore supplies an **inconclusive sensitivity diagnostic**:
the intervention produced no observed difference in assertion reproduction in
that batch. These observations do not establish deterministic replay, identify
the cause of the earlier miss, or justify replacing the original 4/5 result.
No pooled success rate is used across these batches.

Evidence: the original
[`replay_summary.json`](../results/2026-11-07/replay_summary.json),
[`replay_reorder_3_bad_r1.txt`](../results/2026-11-07/followup/replay_reorder_3_bad_r1.txt),
the `records.json` and `diagnostic_*_r*.txt` files in each run's `reorder_3`
artifact, and the preserved workflow runs
[42380929383](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/42380929383)
and
[42381922637](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/42381922637).
The second batch's counts were checked against its downloaded forty diagnostic
records; they are independent of the compatibility baseline's outcome.

## What the multiplier comparison controls

The registered
[`COMPARISON_PROTOCOL.md`](../experiments/2026-11-07/COMPARISON_PROTOCOL.md)
fixes the source, built target, witness, sample size, timeout, and alternating
condition order within a batch. The diagnostic copy changes the replay
multiplier and prints the calibration and target return code after the child
has terminated. The target binary and instrumentation are unchanged by this
diagnostic. The original comparison driver remains separate.

The multiplier is the intentionally varied setting. Each invocation still
performs its own fresh dry run, following the original driver. Thus paired
trials do not share an identical measured calibration. For example, in batch
42380929383 the recorded calibrated periods ranged from 1,010 to 7,860 under
the default condition and from 1,142 to 9,550 under the expanded condition.
In batch 42381922637 the corresponding ranges were 1,361–6,870 and 1,889–9,340.
These values are recorded driver calibration values, not measured kernel
deadline durations.

Calling 6.0 a fourfold *multiplier* is accurate. Calling every paired execution
a fourfold increase in its actual scheduling deadline would be inaccurate:
the fresh calibration differs, and the runtime selects different formula
branches according to the multiplied input. The experiment tests the two
settings under the original calibration procedure. It does not isolate a
constant absolute time quantum or hold the dry-run measurement fixed.

The retained calibration values and child status make this diagnostic more
informative than checking the outer process return code. Its limited sample
and absence of misses prevent a causal explanation of the earlier miss.

## Mechanism established from the pinned source

1. **Replay remeasures timing.** The driver performs a fresh dry run, reads its
   shared-memory timing field, and applies its small-period adjustment before
   processing the witness. Replay then writes `int(Period * 1.5)` in the
   original implementation. The first witness line stores the yield matrix;
   it does not restore the timing calibration from the original failing run.
   See [`run_PDS.py`, lines 354–396 and 417–442](https://github.com/wcventure/PERIOD/blob/cb8deb9a176e5bb292d70d46557dd61dc0e98069/tool/DBDS/run_PDS.py#L354-L442).

2. **The driver masks the target status at its own exit.** The original replay
   branch calls `process.communicate()` and then `sys.exit()` without passing
   `process.returncode`. An outer exit of zero is consequently compatible
   with a target assertion failure. The diagnostic's post-execution status
   print addresses this observation gap without altering target execution.
   See [`run_PDS.py`, lines 439–442](https://github.com/wcventure/PERIOD/blob/cb8deb9a176e5bb292d70d46557dd61dc0e98069/tool/DBDS/run_PDS.py#L439-L442).

3. **A witness specifies yields at instrumented key points.** The runtime
   configures `SCHED_DEADLINE`, converts its timing input through piecewise
   formulas, and executes the prescribed number of `sched_yield()` calls
   before a key point. This loop contains no acknowledgement that another
   particular thread has reached its next key point. It subsequently records
   the key-point location and an atomic order counter. Source inspection
   therefore distinguishes the requested yield pattern from an observed
   execution trace. Whether this mechanism caused the particular earlier
   miss remains unmeasured.
   See [`DBDSFunction.cpp`, lines 147–240](https://github.com/wcventure/PERIOD/blob/cb8deb9a176e5bb292d70d46557dd61dc0e98069/tool/staticAnalysis/DBDS-INSTRU/llvm-mode/DBDSFunction.cpp#L147-L240),
   [lines 579–602](https://github.com/wcventure/PERIOD/blob/cb8deb9a176e5bb292d70d46557dd61dc0e98069/tool/staticAnalysis/DBDS-INSTRU/llvm-mode/DBDSFunction.cpp#L579-L602),
   and [`sched.h`, lines 95–118](https://github.com/wcventure/PERIOD/blob/cb8deb9a176e5bb292d70d46557dd61dc0e98069/tool/DBDS/sched.h#L95-L118).

The scheduling-policy helper exits after a failed `sched_setattr`; these source
paths do not support a claim of silent policy fallback. The runtime timing
field is populated from a microsecond duration despite a nearby nanosecond
comment. That discrepancy is a source-review observation, with no demonstrated
causal connection to the measured replay miss.

## Shared-memory layout limits on execution-order interpretation

The actual instrumentation source defines `SHARE_MEMORY_THREAD_NUM = 100` and
`SHARE_MEMORY_ARRAY_SIZE = 3964`. The Python PERIOD driver defines array size
1990. Both use the same initial scalar fields and thread-count array, so their
yield-array starting addresses agree. Their subsequent location/order-array
addresses differ.

For the observed Linux x86-64 layout with 8-byte `uint64_t`, 4-byte `unsigned
int`, and 2-byte `uint16_t`, the offsets from the shared-memory base are:

| Field | C++ runtime offset | Python driver offset | Consequence |
|---|---:|---:|---|
| `time` | 0 | 0 | Scalar alignment agrees |
| `N`, `M`, `TestedBounds` | 8, 12, 16 | 8, 12, 16 | Scalar alignment agrees |
| `kpNumArray` | 20 | 20 | Per-thread count start agrees |
| Yield array `kp` | 220 | 220 | Initial yield entries align |
| `kpLoc` | 8,148 | 4,200 | Driver reads the runtime yield array's tail |
| `kpOrder` | 16,076 | 8,180 | Driver starts at runtime `kpLoc[16]` |

The C++ payload ends at byte 24,004; its ordinary 8-byte structure alignment
rounds `sizeof` to 24,008. The Python allocation-size expression requests
12,160 bytes. The exact compiled size should be confirmed by a layout probe
when adding an observer; payload extent and `sizeof` are distinct quantities.

Source evidence:
[`DBDSFunction.cpp`, lines 31–46](https://github.com/wcventure/PERIOD/blob/cb8deb9a176e5bb292d70d46557dd61dc0e98069/tool/staticAnalysis/DBDS-INSTRU/llvm-mode/DBDSFunction.cpp#L31-L46),
[`run_PDS.py`, lines 4–14 and 51–84](https://github.com/wcventure/PERIOD/blob/cb8deb9a176e5bb292d70d46557dd61dc0e98069/tool/DBDS/run_PDS.py#L4-L84).

This mismatch invalidates interpreting the driver's nominal `kpOrderArray`
as the runtime's true order array at this pin. The driver also uses its nominal
location array in coverage calculations; the mismatch is relevant to the
interpretation of that feedback. A demonstrated layout mismatch alone does
not quantify its effect on exploration or establish that it caused variable
assertion counts. This remains a limitation of the preserved primary driver.
Compatibility work on the serialized comparator must not be described as a
repair to this separate PERIOD-driver issue.

The corrected observation offsets are supplied here for future work. **This
review does not claim that either diagnostic batch measured the true runtime
key-point order.** Recorded schedule descriptions and requested yield vectors
are the available scheduling evidence; they are not substitutes for a correctly
decoded runtime trace.

## Interpretation of varying failure counts

In the preserved primary comparisons, identical ordered schedule descriptions
can accompany different assertion counts or a different first failing index.
That establishes variability in the observed outcomes despite the same printed
enumeration. It rules out a change in the printed enumeration as a complete
explanation of those differences. It does not establish identical realized
thread interleavings, identify a particular timing cause, or certify that the
driver's feedback arrays were decoded correctly.

The report should retain both facts: the requested enumeration is repeatable
in the compared logs, while some observed failure outcomes vary. The replay
diagnostic adds that changing the multiplier from 1.5 to 6.0 produced no
observed assertion difference in either new batch. These are bounded findings
with an unresolved cause.

## A narrowly scoped follow-up if the project needs a causal test

No additional experiment is represented as completed here. A useful future
protocol would preserve the same binary, witness, host, and source pin, then
add a parent-only read of shared memory **after** target termination using the
runtime's verified 3964-element layout. It would record the actual calibration,
yield input, child status, key-point locations, and order counters before any
subsequent invocation resets the segment. Runs must remain serial because the
shared-memory key is fixed. An abort may leave an incomplete trace; retain and
label that prefix instead of presenting it as a complete execution.

If outcome variability is observed, compare those correctly decoded traces
before changing timing policy. A separate predeclared comparison could then
hold the absolute timing input constant versus fresh calibration, with balanced
order and all unsuccessful trials retained. That comparison would target the
calibration hypothesis more directly. Even a differing key-point order would
describe instrumented events; it would require the instrumentation locations
to be mapped to source operations before claiming a complete memory-operation
ordering.
