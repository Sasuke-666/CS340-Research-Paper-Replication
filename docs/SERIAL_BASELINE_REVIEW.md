# Serialized baseline: source, compatibility and interpretation review

Review date: 2026-11-07. Upstream revision: `cb8deb9a176e5bb292d70d46557dd61dc0e98069`.

## 1. What the released baseline represents

The paper defines SERIAL as a version of PERIOD using the serialized scheduler. Section 3.2.1 describes serialized periods, and Section 4.2 evaluates the parallel scheduler against that baseline. The published SCTBench experiment uses depth 3, a 10,000-schedule budget and ten invocations per program. Table 2 distinguishes the ordinal of the first failing schedule, the total schedules explored and the number of schedules exhibiting a bug. Those are separate outcomes; an invocation that crashes before enumeration has no observed value for any of them. [1]

At the pinned revision, `run_OldPDS.py` calls the authors' `SBPSched` implementation in `sbp_sched.py`. Its enumeration starts at the observed thread count and sets `period_limit = bugDepth + N - 1`. The released parallel driver `run_PDS.py` calls `SBPMESched`, starts at two periods and uses `period_limit = bugDepth + 1`. These source relationships support using the old driver as the released serialized comparison. The release does not establish that this exact driver and runtime combination is the executable used to produce the historical table. Report it as the **authors' released serialized driver**, with the compatibility amendment stated explicitly. [2–4]

The five selected cases belong to the CS suite within SCTBench. They cover different program patterns; they do not constitute five independent benchmark suites. `twostage_bad` provides the useful two-thread control: the paper reports the same 33 total schedules for both methods. [1,5]

| CS program | PERIOD first / total / buggy | Paper SERIAL first / total / buggy |
|---|---:|---:|
| `reorder_3_bad` | 6 / 27 / 6 | 10 / 30 / 10 |
| `reorder_4_bad` | 9 / 100 / 12 | 37 / 384 / 90 |
| `account_bad` | 2 / 65 / 26 | 4 / 136 / 56 |
| `lazy01_bad` | 3 / 39 / 12 | 4 / 60 / 20 |
| `twostage_bad` | 4 / 33 / 3 | 4 / 33 / 3 |

Reference values are transcribed from Table 2, including its distinction between first-error and total-schedule counts. A reproduced total does not establish that first-error position or buggy-schedule count also matches. [1]

## 2. The original-driver failure and its evidence

The preserved batch [`comparison-42380929383`](../results/2026-11-07/comparison-42380929383/) contains 100 comparison invocations. Independent recounting of its archived logs validates all 50 PERIOD invocations and finds all 50 unmodified serialized invocations incomplete, with driver exit code `-11` before any schedule is printed. Their outcomes remain missing. The roughly subsecond duration of a failed driver is excluded from successful-method runtime comparisons.

The shared-memory declarations give a specific compatibility explanation:

| Component | Key-point element width | Python array capacity | Requested or allocated bytes |
|---|---:|---:|---:|
| Original serialized Python driver | 32 bits | 1,990 | 24,300 requested |
| Current parallel Python driver | 16 bits | 1,990 | 12,160 requested |
| Current native instrumentation runtime | 16 bits | 3,964 | 24,008 allocated, including native struct alignment |

The native runtime creates System V shared memory at key `1111` using `sizeof(sched_info)`. The old driver requests a larger segment at that existing key. Its unchecked `shmget`/`shmat` results can lead to an invalid address being passed to `memmove`. Both Python drivers retain a 1,990-element constant, while the native runtime declares 3,964 elements. These values follow directly from the pinned sources. [2,3,6]

The local isolated API-mechanism probe is preserved in [`ipc-mechanism-probe.json`](validation/expanded-20261107/ipc-mechanism-probe.json). It used a separate segment and removed that segment afterward. It established the size-mismatch mechanism without treating a local probe as a crash stack from the hosted run. The amended hosted batch additionally writes `ipc_abi_probe.json` against the actual runtime key: the 12,160-byte request succeeds, the 24,300-byte request returns `-1` with `errno=22`, and an invalid attachment returns the failure sentinel. Together, source inspection, the failed raw logs and the runtime probe support the compatibility diagnosis.

The failed batch also has an evidence-collection defect: after a serialized invocation produced no output directory, the original collector could copy the previous PERIOD directory as a serialized witness. Files under its `witnesses/author_serialized` directories have unreliable attribution. Preserve those historical files but exclude them from baseline claims. The independent summary uses measurement logs and their checksums; it never infers a failure count from the witness directory.

## 3. Scope of the ABI amendment

[`run_period_compatible.py`](../scripts/run_period_compatible.py) constructs `run_OldPDS_abi16.py` by copying exactly the shared-memory function block from the current parallel driver and replacing four global `ctypes` array initializers with their 16-bit forms. The copied block contains shared-memory setup, reading and schedule writing. It records the source hashes and exact patch as `serial_abi16.json` and `serial_abi16.diff`. The comparison label is `author_serialized_abi16`.

The construction checks unique block anchors and verifies that the original serialized enumeration section, beginning with its `bugDepth + N - 1` limit, remains byte-identical. The following behavior is preserved: `SBPSched`, serialized period bounds, enumeration order, depth rules, calibration and execution logic outside the shared-memory block. A new batch is required after the amendment; the original failure batch remains independently auditable.

The amendment deliberately follows the current author's Python ABI, including its 1,990-element convention. It does not repair the remaining 1,990-versus-3,964 layout difference. The key-point count and yield arrays have matching initial offsets, but location and order arrays begin at different offsets in Python and the native runtime. That difference could affect coverage-related behavior. It limits claims of complete runtime equivalence and should remain a documented issue for future work. Altering only the serialized branch to 3,964 would introduce an additional difference in this controlled comparison. [2,3,6]

The released parallel and serialized drivers also differ outside scheduler selection. Examples include stderr handling, short-runtime scaling, fallback calibration, prefix handling and parts of later exploration. The present study compares two released driver configurations under a shared binary and environment. It does not isolate the scheduler as the sole cause of every runtime or bug-detection difference. The schedule-count comparison is interpreted alongside the observed raw enumeration and the paper's structural prediction.

## 4. What the independent summary validates

Run the independent parser from the repository root, with an output directory outside the immutable evidence batch:

```sh
python3 scripts/summarize_comparison.py results/2026-11-07/comparison-RUN_ID --output results/2026-11-07/summaries/comparison-RUN_ID
python3 -m unittest discover -s tests -p test_comparison_summary.py -v
```

`make summarize` regenerates the archived summaries. `make audit` independently recounts both comparison batches and checks their published JSON, CSV and Markdown without modifying them. Startup and partial-run archives receive manifest-only byte verification; their interrupted phases are not required to satisfy the complete scientific sample design. The same comparison audit runs in repository CI.

The parser reads every raw command log independently of the runner's parser. It verifies per-file manifest sizes and SHA256 values, each record's log hash, footer exit and timing values, command identity, contiguous schedule and error ordinals, final error and timeout totals, completion markers, driver-source hashes, captured binary-hash consistency and the prescribed repetition order. It requires ten AB/BA repetitions per comparison method and twenty AB/BA pairs for the fixed-witness diagnostic. The primary adapted batch includes ten censored reorder_4 invocations; their observed first error at schedule 47 is retained separately from missing final totals. A separately registered three-pair follow-up uses a 240-second outer watchdog and remains a separate host scope. A genuine incomplete run remains an experiment outcome; an integrity disagreement fails validation.

The binary is intentionally absent from the evidence archive. The summary can verify that its captured hash is well formed, protected by the environment-file manifest and consistent across any record-level hashes. It cannot recompute the executable hash from a binary that was not retained. The measurement process records that each case's two methods execute the same built binary.

`all_trials.csv` preserves every attempted comparison and diagnostic invocation. `summary.json` gives eligible sample sizes, arithmetic means, sample standard deviations, first-error detection denominators, signed and absolute paper gaps, and paired schedule/time differences. `SUMMARY.md` provides a readable table. Incomplete invocations and null first-error values do not become zeros. First-error means are explicitly conditional on completed invocations that detected an error.

The measured wall time covers the complete driver invocation, including startup and calibration as well as exploration. Timing pairs are formed only within a case and batch. Matrix cases may run on different hosts; even identical CPU model strings do not establish host identity. No cross-case or cross-host wall-time speedup is pooled. Schedule counts may be compared across cases with each case clearly identified.

For the fixed-witness extension, the summary distinguishes the target process's nonzero return code from the expected assertion signature. A wrapper's successful return alone does not establish reproduction. Descriptive counts and mean/sample SD are the primary report outputs. Optional Wilson intervals assume an appropriate independent Bernoulli model; the exact McNemar calculation assumes independent paired observations and the corresponding null model for discordant directions. Sequential executions on one host may be dependent. When both conditions hit in every trial, these quantities do not establish equivalence or demonstrate a benefit from extending the replay window.

## References

1. Wen et al. *Controlled Concurrency Testing via Periodical Scheduling*. ICSE 2022, Sections 3.2.1 and 4.1–4.2, Table 2. [Author manuscript](https://wcventure.github.io/pdf/ICSE2022_PERIOD.pdf). DOI: [10.1145/3510003.3510178](https://doi.org/10.1145/3510003.3510178).
2. Authors' pinned [serialized driver](https://github.com/wcventure/PERIOD/blob/cb8deb9a176e5bb292d70d46557dd61dc0e98069/tool/DBDS/run_OldPDS.py).
3. Authors' pinned [parallel driver](https://github.com/wcventure/PERIOD/blob/cb8deb9a176e5bb292d70d46557dd61dc0e98069/tool/DBDS/run_PDS.py).
4. Authors' pinned [serialized scheduler](https://github.com/wcventure/PERIOD/blob/cb8deb9a176e5bb292d70d46557dd61dc0e98069/tool/DBDS/sbp_sched.py) and [parallel scheduler](https://github.com/wcventure/PERIOD/blob/cb8deb9a176e5bb292d70d46557dd61dc0e98069/tool/DBDS/sbp_sched_mixed_end.py).
5. Authors' pinned [CS benchmark directory](https://github.com/wcventure/PERIOD/tree/cb8deb9a176e5bb292d70d46557dd61dc0e98069/evaluation/CS).
6. Authors' pinned [native shared-memory runtime](https://github.com/wcventure/PERIOD/blob/cb8deb9a176e5bb292d70d46557dd61dc0e98069/tool/staticAnalysis/DBDS-INSTRU/llvm-mode/DBDSFunction.cpp).
