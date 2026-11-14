# Controlled shared-memory layout diagnostic: scientific review

Review date: 14 November 2026. Source revision:
`wcventure/PERIOD@cb8deb9a176e5bb292d70d46557dd61dc0e98069`.

**Evidence status:** the `lazy01` artifact has been downloaded and independently
checked. The original `account` job ended with `failure` at 08:16:50 UTC.
The completed run's artifact list contained only `lazy01` when checked at
08:18:16 UTC, and the account job-log endpoint returned `404 BlobNotFound`.
The original account plan contains twenty invocations; their actual attempt
count, completion count and scientific outcomes remain unknown. The separately
registered account evidence-transfer recovery completed all twenty calls and
has also passed independent review. It remains a separate case/host batch.
The forty readable calls comprise twenty original `lazy01` calls and twenty
recovery `account` calls; they do not reconstruct the missing original calls.

## 1. Question, design and evidence boundary

The [registered protocol](../experiments/2026-11-14/LAYOUT_PROTOCOL.md) was
published in commit `bddb831319679c30586d9bbe689fb11b897f1a14`, before
[workflow 43570556202](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/43570556202)
measured the workloads. It targets a concrete limitation of the earlier study:
the released Python driver declares 1,990 array elements, whereas its native
runtime declares 3,964. The array length determines the locations from which
the driver reads key-point identifiers and execution-order values.

Both arms use the PERIOD driver. `capacity1990` preserves its released bytes;
`capacity3964` changes exactly one declaration to the native runtime's capacity.
The benchmark, native runtime, scheduler code, input, depth 3 and budget 10,000
are unchanged within a case. Each case builds once and plans ten AB/BA pairs
on one host, with a 120-second outer timeout per invocation. This experiment
does not introduce new serialized-baseline measurements.

Each invocation receives the same clean-state procedure in a disposable
container with private IPC and PID namespaces. Cleanup is confined to key
1111 and processes whose executable path matches the built target. The record
verifies key absence and, before removal, zero attachments. Both arms receive
this procedure. Historical-to-new differences cannot isolate the capacity
intervention because the earlier batch used a different cleanup procedure and
host. The relevant controlled comparison is between arms within this batch.

## 2. Structural mechanism and its verification

The probe compiles the actual pinned native struct and macros into a small
declaration-only C++ program. The observed x86-64 structure size is 24,008
bytes. Its field offsets are compared with the two Python declarations below.

| Field | Native runtime offset | Capacity 1990 offset | Capacity 3964 offset |
| --- | ---: | ---: | ---: |
| Key-point counts | 20 | 20 | 20 |
| Yield array | 220 | 220 | 220 |
| Key-point locations | 8,148 | 4,200 | 8,148 |
| Key-point order | 16,076 | 8,180 | 16,076 |

The old location read starts inside the native yield array; its order read
starts at the native location array's seventeenth element. The corrected
capacity aligns both reads. The driver requests a payload ending at byte
24,004; the native structure's four trailing padding bytes account for the
24,008-byte allocation. No field needs those padding bytes.

A separate synthetic sentinel check fills each native array with a distinct
constant. The old reader obtains yield/location values where location/order
values are expected; the corrected reader obtains the intended fields. The
sentinel check is labelled synthetic and excluded from workload counts. It
demonstrates the decoder relationship, not a benchmark execution or the cause
of a particular missed assertion.

The actual driver uses `kpLocArray` in `calculate_coverage_hashID`; that value
is subsequently consulted when selecting additional key-point slices for
exploration. This gives the source-level path through which the decoder
discrepancy could affect search. Whether that path changes a particular
workload's requested schedules is a separate empirical question.

The byte-level source identities are:

| Source | SHA-256 |
| --- | --- |
| Released driver | `c6ed1312f61f7ec739e3dcead0086e0265d37f07bd88ef64d6588d3ff61a8e8f` |
| Capacity-corrected driver | `3b2c8422de8654b2dbbb3730b4c7f289566768f4edaf3ead13ab4b24b3cf801d` |
| Native runtime | `6e5001f8a79851f24f3074b4a6d84cf2550b52b947946f8a330f8877e44e4f61` |

The runtime hash is computed from raw bytes. Its source uses CRLF line endings;
text-mode normalization would change the digest without changing the code.

## 3. Verified lazy01 measurements

Artifact `14103948940` has ZIP SHA-256
`21762deda8eb2a07783655a03ee359886968b08c53e69d3d1cb521eb2b2e1f75`,
matching the workflow's published upload digest. All 300 entries in the
per-case manifest passed independent byte-count and SHA-256 checks. A separate
raw-log recount reproduced all twenty schedule/error observations. All 215
preserved error witnesses contain an assertion-failure signature.

The preserved case is available in the
[original raw archive](../results/2026-11-14/layout-43570556202/lazy01/).
Its [generated audit summary](../results/2026-11-14/summaries/layout-43570556202-lazy01/SUMMARY.md)
passes the independent verifier and reports the same counts and paired
differences. The root archive manifest contains 304 verified entries; the
workload denominators below apply only to the twenty readable `lazy01` trials.

Both arms completed 10/10 invocations. No inner timeout, outer timeout or
schedule-budget stop occurred. No leftover target process required killing.
The host reported an AMD EPYC 9V74 processor, affinity `[0,1,2,3]`, host kernel
7.0.0-1017-azure, Ubuntu 18.04.5 container userland and Python 3.6.9.

Values below are mean and sample standard deviation, with denominator `n-1`.
The paired column subtracts the original-capacity observation from the
corrected-capacity observation for each matching repetition.

| Metric | Capacity 1990, n=10 | Capacity 3964, n=10 | Paired corrected minus original, n=10 |
| --- | ---: | ---: | ---: |
| Explored schedules | 39.000 ± 0.000 | 39.000 ± 0.000 | 0.000 ± 0.000 |
| First failing schedule | 8.500 ± 1.581 | 8.200 ± 0.422 | −0.300 ± 1.337 |
| Buggy schedules | 11.600 ± 0.843 | 9.900 ± 1.912 | −1.700 ± 2.003 |
| Whole-driver seconds | 10.994 ± 0.722 | 9.605 ± 1.608 | −1.390 ± 1.525 |

All twenty printed requested-schedule sequences are identical. The raw logs
print one default coverage hash per invocation: **8** for every original
capacity run, and **185,480** for every corrected-capacity run. The feedback
reading changes in actual driver execution, while this case's requested
enumeration remains unchanged. No prefix-exploration schedule is printed.
All runs report three threads and a maximum of two key points per thread, far
below either capacity bound.

The paper's first-failure reference for this case is 3. The corrected mean
remains 8.2, a gap of +5.2 schedules (+173.33%). The source-level layout repair
does not recover that reference in this sample. It also produces fewer
observed buggy schedules than the original-capacity arm. The reported shorter
whole-driver time is accompanied by that adverse failure-count observation;
it does not establish a general improvement in effectiveness.

These are descriptive observations from sequential pairs on one host. No
independence assumption or significance claim is made. Whole-driver time
includes calibration, target execution and reporting; time to the first
failure was not separately measured. A buggy-schedule count describes failing
executions, not distinct defects. The repeated assertion signatures confirm
the target failure type but do not identify the realized memory-operation
order that led to each outcome.

## 4. Verified account recovery measurements

The [recovery protocol](../experiments/2026-11-14/ACCOUNT_RECOVERY_PROTOCOL.md)
was published in commit `ea273fe4b6e49bd1f8f5c5b7c964c02aaf22d144`
before [workflow 43575584325](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/43575584325).
It retained the fixed twenty-call plan on a new host, using the four original
measurement wrapper/helper files from `bddb831`. The activation followed
the original completed job and the two evidence-availability checks. No
original account numerical result was available to guide that decision.

The recovery measurement step completed successfully at 08:32:30 UTC.
The complete original output was published through ordinary Git history at
08:32:44 UTC, before the secondary ZIP artifact finished uploading at
08:32:46 UTC. The retained Git archive provides the raw measurements, and
the completed workflow also records the secondary ZIP artifact. The
[raw recovery archive](../results/2026-11-14/layout-recovery-43575584325/)
and [generated audit summary](../results/2026-11-14/summaries/layout-recovery-43575584325-account/SUMMARY.md)
retain their original-run linkage.

All 571 root-manifest entries and 557 case-manifest entries passed independent
byte-count and SHA-256 checks. All four archived runner sources were compared
byte for byte with `git show bddb831:<original path>` and with the registration
hashes; all agree. The archived released driver, capacity-corrected driver and
native runtime reproduce the three source digests in section 2. Direct byte
comparison confirms that the capacity declaration is their only driver
difference. The recovery probe reproduces all native offsets and the
24,008-byte structure size.

Both arms completed 10/10 invocations, with ten eligible pairs. No inner or
outer timeout, budget stop, or other error type occurred. The before/after
cleanup records verify that key 1111 was absent; no residual target process
required killing. The same built executable was used throughout the case,
with SHA-256
`28c4d2d994766f67735fe83905e65e34afdea7586b6f8e7cd33189e621ac2b0d`.
The host reported an AMD EPYC 9V45 processor and affinity `[0,1,2,3]`, with
the same recorded kernel, container userland and Python version as section 3.

A separate raw-log recount reproduced every schedule and error observation.
All **472** preserved witnesses contain the expected target assertion,
`balance == (x - y) - z`: 229 in the original-capacity arm and 243 in the
corrected-capacity arm. Each of the twenty invocations observes this assertion.
These are repeated failing schedules of the known defect.

| Metric | Capacity 1990, n=10 | Capacity 3964, n=10 | Paired corrected minus original, n=10 |
| --- | ---: | ---: | ---: |
| Explored schedules | 65.000 ± 0.000 | 65.000 ± 0.000 | 0.000 ± 0.000 |
| First failing schedule | 10.500 ± 0.850 | 10.200 ± 0.632 | −0.300 ± 1.160 |
| Buggy schedules | 22.900 ± 3.281 | 24.300 ± 1.767 | +1.400 ± 4.402 |
| Whole-driver seconds | 23.569 ± 3.547 | 24.639 ± 2.040 | +1.070 ± 4.323 |

All twenty complete printed requested-schedule sequences are identical.
The default feedback hash is **18** in every original-capacity invocation and
**196,202** in every corrected-capacity invocation. No prefix-exploration
schedule is printed. The paper's first-failure reference is 2; the corrected
mean remains 10.2, a gap of +8.2 schedules (+410.00%). The capacity correction
does not close that gap on this host.

Account's corrected arm observes more failing schedules and a longer average
whole-driver time. Lazy01's corrected arm observes fewer failing schedules
and a shorter average time. These mixed directions support no general claim
of faster execution or greater failure yield. The two cases retain separate
hosts and denominators. All contrasts are descriptive; no independence
assumption or significance claim is made. The successful recovery supplies
new account evidence and does not determine why the original attempt failed.

## 5. Account: a conditional source-level explanation

The following illustration uses the pinned source and a requested schedule
present in the earlier study and every recovery invocation. It separates the
printed request from the realized execution order within a parallel period.

`account_bad.c` creates `check_result`, `deposit` and `withdraw` in that order.
The native creation handshake assigns sequential thread identifiers, mapped
to zero-based scheduler indices. The earlier log's second requested schedule
is `[[1,1,1],[0,0,2,2,2]]`. Its final period permits the checker and withdrawal
thread to run in parallel after the deposit thread's assigned operations.

If withdrawal obtains the mutex and completes before the checker, the checker
can observe both completion flags and enter the deliberately incorrect
assertion. If the checker obtains the mutex first, it can observe
`withdraw_done == 0` and skip that assertion. The request itself therefore
permits different assertion outcomes inside its parallel final period.

This source-based, conditional example explains why identical printed requests
need not uniquely determine realized execution. No correctly decoded actual
execution trace was collected for these observations. The example does not
establish which mutex order occurred in any recorded invocation or prove the
cause of a particular historical miss. Such a causal attribution would require
an observed trace and a separately designed control.

## 6. Conclusions and original account evidence loss

The structural decoder mismatch is verified, and the capacity correction
aligns the location/order fields. In both completed case batches, actual
default feedback hashes change while the complete requested enumeration
remains unchanged. The first-failure gaps remain substantial. Buggy-schedule
counts and whole-driver time change in mixed directions across cases. This
field-offset correction is insufficient to recover the paper's first-failure
references in these controlled samples. The observations do not establish
the shared-memory layout as the sole cause of the historical discrepancy.

The original `account` workload step ended with `failure` at 07:30:52 UTC;
its preservation step began at 07:30:58 UTC. The job metadata later marked
the job completed with `failure` at 08:16:50 UTC, while the step metadata
still labelled preservation as in progress. The full workflow reached its
final failed state, and two subsequent artifact queries returned only the
completed `lazy01` artifact. The account log endpoint returned `404
BlobNotFound` both times. These records establish unavailable account evidence
after the original run ended. They do not identify the measurement failure
as a timeout, incomplete enumeration or a runner defect.

The unavailable original account attempts contribute no numerical outcome to
the tables. Twenty invocations were planned; the actual trial count is
unknown and must not be reported as a measured zero. The recovery satisfied
the separately registered evidence-transfer condition, retained the same
fixed twenty-invocation plan, and reports its own host and results in section
4. Its activation depended on evidence availability. Historical
paper-versus-ours tables remain unchanged.

The [final observation](../experiments/2026-11-14/account-evidence-failure/FINAL_OBSERVATION.json)
and the [retained API responses](../experiments/2026-11-14/account-evidence-failure/)
document the original missing-evidence scope. The
[account recovery protocol](../experiments/2026-11-14/ACCOUNT_RECOVERY_PROTOCOL.md)
defines the separate fixed sample and preserves its original-run linkage.

## Sources and review entry points

1. [Registered protocol](../experiments/2026-11-14/LAYOUT_PROTOCOL.md) and
   [measurement workflow](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/43570556202).
2. [Pinned PERIOD driver](https://github.com/wcventure/PERIOD/blob/cb8deb9a176e5bb292d70d46557dd61dc0e98069/tool/DBDS/run_PDS.py),
   especially its array declaration, shared-memory reads and coverage handling.
3. [Pinned coverage helper](https://github.com/wcventure/PERIOD/blob/cb8deb9a176e5bb292d70d46557dd61dc0e98069/tool/DBDS/external_def.py)
   and [native runtime](https://github.com/wcventure/PERIOD/blob/cb8deb9a176e5bb292d70d46557dd61dc0e98069/tool/staticAnalysis/DBDS-INSTRU/llvm-mode/DBDSFunction.cpp).
4. [Pinned account benchmark](https://github.com/wcventure/PERIOD/blob/cb8deb9a176e5bb292d70d46557dd61dc0e98069/evaluation/CS/account/account_bad.c)
   and [earlier account raw log](../results/2026-11-07/comparison-42381922637/account/period_r01.txt).
5. Wen et al., *Controlled Concurrency Testing via Periodical Scheduling*,
   ICSE 2022, Table 2 and sections 3.2–3.4:
   https://wcventure.github.io/pdf/ICSE2022_PERIOD.pdf
6. [Original account evidence-transfer final observation](../experiments/2026-11-14/account-evidence-failure/FINAL_OBSERVATION.json)
   and [separate account recovery protocol](../experiments/2026-11-14/ACCOUNT_RECOVERY_PROTOCOL.md).
7. [Recovery raw measurements and registration](../results/2026-11-14/layout-recovery-43575584325/)
   and [independent account summary](../results/2026-11-14/summaries/layout-recovery-43575584325-account/SUMMARY.md).
