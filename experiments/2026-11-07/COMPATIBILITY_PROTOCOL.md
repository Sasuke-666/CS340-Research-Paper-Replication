# Registered ABI-compatible comparison

7 November 2026. This amendment is registered after inspecting original-driver
failures and before running the adapted baseline. The original registered study
and its complete logs remain archived under run 42380929383. The earlier source
encoding setup failure is run 42380166815. Neither is overwritten.

## Evidence motivating the change

The unmodified old serialized driver terminated with signal 11 before reporting
its first schedule. Source comparison shows its shared-memory arrays and offsets
use 32-bit unsigned integers while the current driver/runtime use 16-bit arrays.
The old requested mapping is 24,300 bytes; the current mapping is 12,160 bytes.
The old driver does not check shmget/shmat failures before memmove. This is an
identified compatibility hypothesis to test with the actual kernel return codes.

## Minimal change

Copy only the current driver's three IPC helper functions (setup/read/write) into
a separate old-driver copy, and change its four array initializers to uint16.
The scheduling/enumeration section from `period_limit = bugDepth + N - 1` onward
must remain byte-identical to the old driver. Save the exact diff and file hashes.
No benchmark, SBPSched implementation, depth bound, input or error oracle is edited.
Call this method `author_serialized_abi16`, not an unmodified historical binary.
The other differences between the two author drivers remain and are disclosed;
wall-clock differences cannot be attributed to enumeration alone.

## Fixed comparison and diagnostic

Repeat the same five cases, ten paired repetitions per method, AB/BA order,
depth 3, 10,000 schedule budget, 120-second comparison limit, original input,
pinned image/source and same binary/host within each case. Use a separate new
batch and do not merge its timing observations with the previous machine batch.
Retain all attempts and incomplete outcomes. Compare against the originally
registered Table 2 numbers without tuning the adapter to those counts.

Repeat the existing 20-pair (1.5 versus 6.0 replay multiplier) diagnostic in the
reorder_3 job. Report it as a separate batch; do not erase or pool the earlier
40 diagnostic calls without disclosing batch/host differences. A diagnostic
that does not reproduce a miss cannot establish its root cause.

After each case, query the actual existing shared-memory key for both requested
sizes without changing its contents. Record errno and the failure sentinel for
an invalid attach, but never dereference an invalid pointer. Retain relevant
original runtime structure definitions alongside the results. This probe is
not a benchmark repetition.

The expected batch contains 100 comparisons, 40 replay diagnostics, five builds
and five separately recorded ABI probes. Actual coverage controls reporting.
Original source licenses and the required assistance disclosure are preserved.

## Runner-label correction before adapted comparisons

Run 42381557337 reached one PERIOD invocation in each case, then stopped on a
runner KeyError because the AB/BA loop still used the old baseline label. Those
five partial measurements and all build logs are preserved separately. The loop
now resolves the configured baseline name and has regression tests for the new
label and invalid method sets. This changes orchestration only, not either
scheduler or the registered experimental conditions. A fresh batch repeats the
full fixed design; partial-batch observations are not silently pooled into it.
