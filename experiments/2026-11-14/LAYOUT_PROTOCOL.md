# Registered capacity-layout experiment — 14 November 2026

This protocol is committed before workload measurement. The workflow commit
identifies the exact registration. Outcomes are unknown at registration.

## Question and rationale

The pinned native runtime declares 3,964 elements in each shared key-point
array, while its PERIOD Python driver declares 1,990. Source inspection predicts
misaligned location/order reads, which participate in coverage feedback. The
7 November report disclosed this discrepancy but did not measure its effect.
We ask whether correcting this one driver constant changes enumeration or
failure observations for two programs with large first-failure gaps.

The cases are `CS.account_bad` and `CS.lazy01_bad`, selected before this batch
because their 7 November PERIOD first-failure means were 10.1 and 8.0 compared
with paper values 2 and 3. This is targeted diagnosis, not an unbiased sample
of all workloads. It does not retrospectively change the old results.

## Intervention, controls and execution

- Fixed source: `cb8deb9a176e5bb292d70d46557dd61dc0e98069`.
- Fixed image: `wcventure/period@sha256:8f47d8b9148f2db579627842026e722d0f205ddeab13e70ee41a8df3dbd59fbc`.
- Condition A, `capacity1990`: byte-preserved released `run_PDS.py`.
- Condition B, `capacity3964`: the same file with exactly one declaration changed,
  `SHARE_ARRAY_SIZE = 1990` to `SHARE_ARRAY_SIZE = 3964`.
- No serialized baseline is involved in this experiment. Scheduler code,
  benchmark, native runtime, input and compiled benchmark are identical across
  A and B. Original and amended driver bytes, hashes and diff are retained.
- Each case builds once and runs both conditions on one host. Case jobs may
  use different hosts; all comparisons remain within case and batch.
- Ten paired repetitions per case; odd repetitions use AB and even repetitions
  use BA. Planned total: 40 workload invocations, 20 per case.
- Depth 3, schedule budget 10,000, outer timeout 120 seconds per invocation.
  The driver's internal timeout/calibration behavior remains unchanged.
- Each invocation starts with key 1111 absent inside a private container IPC
  namespace. Cleanup verifies no attachments and removes only that key.
  Processes matching the exact built benchmark path are killed if left over
  after an invocation. Cleanup and any such intervention are recorded.
- Both conditions receive the same clean-state procedure. It is a difference
  from the older measurement batch, so historical-to-new differences cannot
  isolate the capacity intervention. Only this batch's paired arms do so.
- The container uses private PID/IPC namespaces, disabled network, and no
  personal credentials or Docker socket. A separate child probes real-time
  scheduling permission before workload execution.

## ABI validation and evidence

Compile a small declaration-only C++ probe using the exact struct and macros
extracted from the pinned `DBDSFunction.cpp`. Record native `sizeof` and
`offsetof` values; stop if they differ from the registered x86-64 layout:
`sizeof=24008`, `kp=220`, `kpLoc=8148`, `kpOrder=16076`.

A separate synthetic byte-array sentinel check demonstrates how the two Python
capacities decode that observed layout. The sentinel check is explicitly
synthetic; it does not measure benchmark execution or prove a causal effect on
failure discovery. The actual source and compiled-probe command/log are kept.
Generated executables remain outside the retained evidence.

Every trial retains command, timestamps, exit status, timeout state, elapsed
seconds, condition/order, binary hash, freshly created error/timeout witnesses,
and shared-memory reset evidence. The runner's records and hashes are checked
against an independent recount of its raw logs. Source, environment, build and
capability-probe records are separate from the workload denominator.

## Prespecified outcomes and interpretation

Primary outcomes are complete-run explored-schedule totals, error discovery,
first observed failing schedule and buggy-schedule count. Whole-driver time is
secondary. Report arithmetic mean and sample SD with each actual denominator,
plus paired differences where both arms complete. Preserve every planned
attempt and all observed errors, including adverse results.

Timeouts and execution failures remain separate outcomes; missing final totals
do not become zero or a partial prefix. Describe printed schedule-sequence
agreement/differences separately from failure metrics. A printed schedule is a
requested schedule, not an observed memory-operation trace.

If the corrected layout changes results, evidence supports a local effect of
the capacity intervention under this controlled configuration; it does not
establish that the layout mismatch explains every historical discrepancy.
If both arms agree, the mismatch has no observed effect on those metrics in
this sample, while the structural decoder mismatch remains demonstrated.
Neither outcome establishes universal replay determinism. Repeated trials on
one host may be dependent; no independence-based significance claim is planned.

The new study is an extension of the reproduction and a controlled discrepancy
check. It does not replace the depth extension or the original paper tables.

## Reproduction

From the repository root on a disposable x86-64 Linux machine with Docker:

```bash
bash scripts/period_container_layout.sh account results/local-layout-account-001
bash scripts/period_container_layout.sh lazy01 results/local-layout-lazy01-001
```

Use fresh paths. Actual failures are archived before deciding on a separately
registered amendment. This protocol's sample is not increased after viewing
its outcomes to obtain a preferred result.

## Sources

1. Wen et al., *Controlled Concurrency Testing via Periodical Scheduling*,
   ICSE 2022, sections 3.3–3.4 and 4.1.3, Table 2.
   https://wcventure.github.io/pdf/ICSE2022_PERIOD.pdf
2. Pinned driver and runtime:
   https://github.com/wcventure/PERIOD/blob/cb8deb9a176e5bb292d70d46557dd61dc0e98069/tool/DBDS/run_PDS.py
   https://github.com/wcventure/PERIOD/blob/cb8deb9a176e5bb292d70d46557dd61dc0e98069/tool/staticAnalysis/DBDS-INSTRU/llvm-mode/DBDSFunction.cpp
