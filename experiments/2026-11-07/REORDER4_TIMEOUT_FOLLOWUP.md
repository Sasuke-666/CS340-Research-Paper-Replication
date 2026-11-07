# Registered four-thread timeout follow-up

7 November 2026, after inspecting the complete archive of run 42381922637 and
before this follow-up is measured. The previous batch is immutable: all 10
PERIOD invocations on reorder_4 completed, while all 10 compatible serialized
invocations reached the 120-second outer limit after 272–276 printed schedules.
The partial runs have no final buggy-schedule total and are not treated as
complete results. They remain informative evidence of censoring at that limit.

## Fixed design

Run only reorder_4 on a new disposable host, rebuilding both methods' shared
target from the same pinned source and image. Keep the original program/input,
PERIOD driver, author_serialized_abi16 adapter, depth 3, schedule budget 10,000,
internal target timeout and all method settings unchanged. Raise only the outer
driver watchdog from 120 to 240 seconds, which allows longer observation without
changing the underlying scheduler or target program. This is a completion check,
not an experiment to estimate the causal effect of host-independent timing.

Use three paired repetitions in order AB, BA, AB, with PERIOD as A. This meets
the course's minimum while limiting an expensive additional case. The smaller
sample size is explicit; do not represent it as ten repetitions. Do not pool
time or failure observations with the previous host. Report both methods from
this same new batch for the four-thread matched comparison.

Preserve all six calls, including any renewed timeouts or crashes. No further
selection based on favourable results is allowed. Complete runs must satisfy
the same independent raw-log and checksum checks as previous batches. Compare
final explored, first-error and buggy-schedule metrics with the previously
registered Table 2 reference numbers; missing final totals remain missing.
Source/image/binary/driver hashes, compiler/CPU/kernel, command logs, exact ABI
patch, native-key probe and manifests remain required. One build and the IPC
probe are separate from the six scientific invocations. No replay experiment
is planned in this case.

## Runner repair kept separate from measurements

The collector now accepts only directories newly created by the current call,
preventing a failed call from inheriting an earlier call's witness files. This
affects evidence attribution only; no benchmark or schedule logic is modified.
The runner exposes repetition count and outer timeout as recorded parameters;
the defaults remain ten and 120 for historical-design reproduction.
