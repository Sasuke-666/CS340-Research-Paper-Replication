# Sources, attribution and version record

1. Instructor-provided `2609_CS340_Research_Paper_Replication(1).pdf`, academic
   year 2026–2027. Pages 1–4 define milestones, report and repository criteria.
   The course PDF and slides are not redistributed.
2. Wen, C., He, M., Wu, B., Xu, Z. and Qin, S. (2022). *Controlled Concurrency
   Testing via Periodical Scheduling*. ICSE 2022. DOI: 10.1145/3510003.3510178.
   https://wcventure.github.io/pdf/ICSE2022_PERIOD.pdf
   Table 2 (PDF p. 9) supplies the selected reference counts; section 4.1.3
   (PDF p. 8) supplies the original experiment settings. The PDF is not bundled.
3. Authors' implementation: https://github.com/wcventure/PERIOD
   Starting commit: `cb8deb9a176e5bb292d70d46557dd61dc0e98069`.
   The runner downloads this public source at that commit. Benchmark source is
   not edited. Its instrumentation/static-analysis layer is rebuilt from this
   checkout; installed compiler/SVF dependencies come from the recorded image.
4. Authors' container: `wcventure/period:stable`, resolved during the first pilot
   to `wcventure/period@sha256:8f47d8b9148f2db579627842026e722d0f205ddeab13e70ee41a8df3dbd59fbc`.
   Subsequent scripts default to that digest. See the archived image inspection,
   compiler output and environment records. A digest pins image contents, not
   the host kernel or CPU. Do not identify it as a fresh build of every original
   2022 dependency.
5. Upstream license: the complete MIT notice copied from the pinned checkout is
   retained as `results/2026-11-07/pilot/upstream_LICENSE.txt`, and again with the
   follow-up. Other dependencies retain their own licenses; no blanket license
   is assigned to them or to the group's future work.

## Project additions

Project-owned additions are the scripts under `scripts/`, workflow files,
experiment protocols, tests, analysis documents and measurement records.
The `scripts/period_container_pilot.sh` overlay restores the pinned source over
an existing dependency image; it rebuilds the original analysis/instrumentation
layer but does not modify benchmark logic. Generated bitcode/executables remain
inside the disposable container and are not committed. No original library,
compiler binary, disk image or credentials are redistributed.

The wrapper uses a fixed `/workdir/PERIOD` location inside the container because
that is the authors' installed layout. Host paths are derived from the repository
location and the chosen output directory; no student's home directory is required.

## Serialized baseline adaptation

`scripts/run_period_compatible.py` creates `run_OldPDS_abi16.py` from the pinned
authors' source. Only three IPC functions and four array element types are
backported from `run_PDS.py`; the serialized enumeration section is required to
remain byte-identical. Every measured case preserves `serial_abi16.diff`, the
original/adapted SHA-256 values, and both source files. The method is always
identified as `author_serialized_abi16`. The paper does not identify the precise
script/version of its Serial baseline, so historical identity is not asserted.

The current Python drivers use 1,990-element location/order arrays while the C
runtime uses 3,964. The minimal adaptation preserves this upstream convention;
internal actual-order traces are not inferred from those mismatched offsets.
`scripts/probe_serial_ipc.py` is a separate isolated syscall demonstration, not
a scheduler implementation or a benchmark repetition.

## Controlled capacity diagnostic on 14 November

`scripts/run_period_layout.py` preserves the released `run_PDS.py` and creates
`run_PDS_layout3964.py` by changing only `SHARE_ARRAY_SIZE = 1990` to `3964`.
The native runtime and benchmark source are unchanged. Each case retains the
exact one-line patch and original/revised source hashes. A declaration-only
compiled probe extracts the actual runtime structure's size and offsets; its
separate synthetic sentinel demonstration is excluded from workload results.
The new wrapper resets private IPC state for both conditions and preserves
all attempted calls. These new-state controls are separate from the old study.

The upstream driver SHA-256 is
`c6ed1312f61f7ec739e3dcead0086e0265d37f07bd88ef64d6588d3ff61a8e8f`;
the one-constant revision is
`3b2c8422de8654b2dbbb3730b4c7f289566768f4edaf3ead13ab4b24b3cf801d`;
the unchanged native runtime is
`6e5001f8a79851f24f3074b4a6d84cf2550b52b947946f8a330f8877e44e4f61`.
Hashes refer to exact bytes, including line endings. The raw source and license
are part of each archived case. See the
[registered protocol](../experiments/2026-11-14/LAYOUT_PROTOCOL.md).

The original account job finished unsuccessfully without an accessible result
artifact or job log. Its final API responses are preserved in
[the original evidence-loss record](../experiments/2026-11-14/account-evidence-failure/FINAL_OBSERVATION.json).
The [recovery protocol](../experiments/2026-11-14/ACCOUNT_RECOVERY_PROTOCOL.md),
registered at `ea273fe4`, extracts all four measurement wrapper/helper files
byte-for-byte from `bddb831`. Its archive separately retains those runner
sources, their hashes, the activation record and the new batch identity.
Only evidence preservation changes: Git publication precedes the backup upload.
