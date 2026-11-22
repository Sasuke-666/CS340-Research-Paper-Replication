# Fresh-host acceptance protocol — 22 November 2026

Status: registered before the workflow measurements. The triggering commit is
recorded as `protocol_commit` in each resulting archive manifest.

## Purpose and scope

Verify that the current documented container entry point can obtain its pinned
dependencies, rebuild instrumentation and execute the complete five-case
comparison on fresh disposable hosted Linux machines. The earlier offline
checks verify saved evidence and report consistency; this run tests the live
build/run path. This is an engineering acceptance batch with new host scopes.
It is not an additional sample in the historical paper-replication estimates.

The review found three concrete entry-point defects: the pilot workflow created
an output directory that its wrapper deliberately rejects; bare `make layout`
inherited the unsupported comparison default; and current comparison archiving
unnecessarily downloaded a previously archived historical run. Those defects
are repaired separately. This five-case run exercises the main compatible
comparison path. Regression checks cover the other entry-point corrections;
we do not claim to have rerun the historical pilot or capacity intervention.

## Fixed design

| Setting | Registered value |
| --- | --- |
| Cases | `reorder_3`, `reorder_4`, `account`, `lazy01`, `twostage` |
| Host | One fresh `ubuntu-24.04` x86_64 hosted runner per case; cases remain separate host scopes |
| Upstream commit | `cb8deb9a176e5bb292d70d46557dd61dc0e98069` |
| Image | `wcventure/period@sha256:8f47d8b9148f2db579627842026e722d0f205ddeab13e70ee41a8df3dbd59fbc` |
| Methods | `period` and `author_serialized_abi16`, using the existing unchanged measurement drivers |
| Repetitions | Three paired repetitions per case: AB, BA, AB |
| Comparison parameters | Driver bug depth 3, schedule-request budget 10,000, 240-second outer watchdog per invocation |
| Pairing | Same built benchmark and same host for both methods within each case |
| Isolation | Existing wrapper's private container, privileged runtime, network disabled during execution |
| Additional retained diagnostic | Existing `reorder_3` fixed witness: 20 paired replay repetitions at scales 1.5 and 6.0 |

There are **30 planned comparison invocations, arranged as 15 pairs**, plus
**40 separately counted diagnostic replay invocations** and five benchmark
builds. Instrumentation builds and setup commands are recorded separately.
The existing runner always includes the replay diagnostic for `reorder_3`;
its measurement logic is not edited to reduce the workload. Failures can leave
fewer actual invocations; actual counts must be reported, never inferred from
the planned design. The 240-second watchdog is fixed before execution for all
five cases. It is not changed after seeing results.

## Execution and preservation

The workflow is [period-acceptance.yml](../../.github/workflows/period-acceptance.yml).
It runs on publication of this protocol and also exposes a manual dispatch for
an explicitly separate future attempt. Its case command is:

```bash
bash scripts/period_container_compatible.sh "$STUDY_CASE" "$FRESH_OUTPUT" 3 240
```

The final output directory must not already exist. Every matrix job uploads
whatever evidence exists even if its build or runtime fails. The archive job
also retains the wrapper's outer console and workflow metadata, written only
after the wrapper exits, so setup failures do not require a precreated output
directory. An interrupted or malformed record index is preserved byte-for-byte
with an unknown command count and a parse-error note; it cannot block raw-byte
preservation or count as a successful acceptance. The archive job
copies exact bytes to
`results/2026-11-22/acceptance-RUN_ID-attemptATTEMPT/`, records file sizes and
SHA-256 digests, the protocol commit, run ID and attempt number, and preserves
available cases even when another case fails. Generated summaries live outside
the immutable raw archive. No old workflow artifact is needed.

No automatic rerun or selection of a better outcome is planned. A genuine
failure is kept and documented. A necessary repair and subsequent new attempt
must retain the first attempt and state the changed condition.

## Acceptance criteria

`scripts/check_acceptance.py` independently recounts logs through the existing
summary auditor. Acceptance requires the declared cases and ordering, valid
inner and outer manifests, exact source/image pins, captured build/version
provenance, successful container and benchmark builds, three complete eligible
calls per method and three complete pairs for every case, with no inner timeout
or schedule-budget truncation. All 40 planned
diagnostic calls must have complete eligible process observations. A replay
need not reproduce its assertion to count as a completed observation: its
actual outcome is retained. Missing logs, censored calls or integrity errors
fail acceptance without turning those observations into zero-valued results.

First-failure indices, buggy-request counts and timings are descriptive new-host
observations. Equality to the historical means, a faster runtime or successful
reproduction of every replay is **not** an acceptance criterion. The batch
cannot establish statistical equivalence, a universal performance advantage,
the historical paper binary's identity or anyone else's independent work.

## Relation to course assessment

The supplied rubric explicitly requires a clean-machine build/run path and
traceable evidence. Exercising all five cases with three pairs is our bounded
quality decision, not an additional instructor rule or a predicted score.
Attribution remains with the owner's requested maintenance and disclosed
assistance. Actual member submissions retain their authors and dates.
