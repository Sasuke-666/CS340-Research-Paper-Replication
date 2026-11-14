# Conditional evidence-recovery protocol — 14 November 2026

Status: **activated after observed evidence loss**. The original account job
finished with failure at 08:16:50 UTC. Two final checks at 08:17:33 and
08:18:16 UTC found only the lazy01 artifact; account job-log retrieval returned
404 BlobNotFound. The measurement failure cause and actual invocation count
remain unknown. Complete inspection responses are retained in
[account-evidence-failure](account-evidence-failure/FINAL_OBSERVATION.json).

## Activation condition

Original workflow: `43570556202`.
Original account job: `132373799340`.
Original protocol commit: `bddb831319679c30586d9bbe689fb11b897f1a14`.
Expected artifact name: `period-layout-account-43570556202`.

Activate only after the original workflow/job has finished and its account
artifact cannot be read. Retain the original workflow/job metadata and any
available console log. Record the final outcome, artifact query and actual
inspection time in `ACCOUNT_RECOVERY_ACTIVATION.json` before setting its
`enabled` field to true and publishing this protocol with the workflow.

If the original account evidence becomes readable, use and preserve it; this
recovery is unnecessary. A negative, censored, incomplete or unexpected
scientific result with readable evidence does not activate this protocol.

The recovery decision uses evidence availability, not schedule/error counts or
effect direction. It does not extend a sample until a desired result appears.

## Fixed replacement batch

Run only `account`, with ten paired repetitions in AB/BA order. Use the exact
measurement wrapper and Python runner/helper bytes from the original protocol
commit. The two arms remain `capacity1990` and `capacity3964`; the sole driver
change remains the single array-capacity declaration.

Keep source `cb8deb9a176e5bb292d70d46557dd61dc0e98069`, image
`wcventure/period@sha256:8f47d8b9148f2db579627842026e722d0f205ddeab13e70ee41a8df3dbd59fbc`,
depth 3, schedule budget 10,000, outer timeout 120 seconds, the same private
IPC/PID clean-state procedure and fresh per-invocation calibration.

The new run builds one account binary and uses it for both arms on one new
host. This is a new batch, with its own environment and provenance. It cannot
recover the original host's missing measurements. Preserve the original
evidence-transfer failure alongside it; never replace the old run identity or
claim that the recovery bytes are the old measurements.

The planned denominator remains twenty account workload attempts. Keep every
attempt, build/capability/probe record, timeout, driver failure, source, witness
and manifest. An early setup/control failure leaves later planned trials
unexecuted and explicitly accounted for. No successful-only selection is used.
The completed lazy01 batch stays separate and is not repeated.

## Preservation order

1. Read the activation record and prepare the original pinned runner files.
2. Execute the full predeclared account batch once.
3. Regardless of measurement success, copy its original evidence bytes into a
   fresh repository directory and produce an outer hash manifest. Include the
   activation record and original-run linkage outside the raw account folder.
4. Commit and push this archive with the owner's full name and student ID,
   preserving any concurrent remote work through a fetch/rebase and ordinary
   fast-forward push. Never force-push or overwrite a previous archive.
5. Create one ZIP of the raw evidence and recovery metadata, then upload that
   single ZIP as a second preservation channel. This also runs if Git
   publication fails. The ZIP does not contain credentials or a repository
   `.git` directory.

The Git publication token is supplied only to the final Git publication step.
The measurement container receives no token, credentials, host Docker socket
or authenticated checkout. Its network remains disabled. Source acquisition
and image pulling follow the original wrapper's host-side procedure.

Artifact-upload failure after successful Git publication does not erase the
committed raw evidence. Measurement failure remains visible in the job outcome,
even if both preservation channels succeed. A successful upload alone does not
establish a valid experiment.

## Intended deployment paths

- This file: `experiments/2026-11-14/ACCOUNT_RECOVERY_PROTOCOL.md`
- Activation record: `experiments/2026-11-14/ACCOUNT_RECOVERY_ACTIVATION.json`
- Workflow: `.github/workflows/period-account-recovery.yml`
- Archive helper: `scripts/archive_layout_recovery.py`

This protocol and the observed activation record are published before the
recovery measurements start. The successful original lazy01 evidence is
preserved in its original batch. The original account evidence remains
missing and is not represented as zero attempted or zero failed trials.
