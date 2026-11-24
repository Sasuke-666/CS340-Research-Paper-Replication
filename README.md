# CS340 — PERIOD Research Paper Replication

Operating Systems · Academic Year 2026–2027

We reproduced selected experiments from *Controlled Concurrency Testing via
Periodical Scheduling* (ICSE 2022). The study asks whether PERIOD recovers the
paper's schedule counts and failure-discovery results, and how it compares with
the authors' released serialized driver on five small concurrent programs.

Our conclusion is **partially reproduced**. The selected schedule counts agree
with the paper, and PERIOD explores fewer schedules in four of the five cases
under our stated driver settings. Failure-discovery results differ. The report
examines those differences through a depth-bound extension, a controlled
shared-memory capacity change and independent member checks.

## Start here

| To do | Entry point |
| --- | --- |
| Read the findings | [English report](report/EXPANDED_REPORT.md), especially §§1–4 for results, §5 for discrepancies, §6 for the extension and §8 for the capacity study |
| Download the final documents | [Report, presentation and Chinese handbook](submission/README.md), or the [complete v1.0.2 bundle](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/releases/tag/v1.0.2) |
| Check the archived evidence | [Clone and run the offline checks](#clone-and-verify-the-archived-evidence); no Docker workload is needed |
| Run a new experiment | [Linux/Docker instructions](#independently-rebuild-and-run-a-comparison), including settings and expected runtime |
| Prepare the presentation | [Fourteen-slide source](presentation/SLIDES.md), [Chinese speaking notes and questions](presentation/TALK_OUTLINE.md), [member preparation](docs/MEMBER_ACTIONS_ZH.md) |
| Check course requirements and contributions | [Rubric map](docs/FINAL_SUBMISSION_CHECKLIST.md), [actual contributions](docs/CONTRIBUTIONS.csv), [weekly progress](docs/WEEKLY_PROGRESS.md) and [course requirements](docs/COURSE_REQUIREMENTS.md) |

## Final documents — 25 November 2026

The final report records all eight member pull requests. He Boyu's
[PR #7](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/7)
adds three synthetic-log regression tests for the twostage recount. Li Yangshuo's
[PR #8](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/8)
adds release and Windows checks, independent acceptance metrics and parser
integrity checks. Maintainer review closes three further parser/path boundary
cases and clarifies the dates and scope of the retained validation records.

The [v1.0.2 revision](submission/README.md) contains the English report in PDF
and Word, an editable fourteen-slide presentation and PDF, and a Chinese
submission handbook in Word and PDF. The `v1.0` and `v1.0.1` releases remain
available. Each version records its document hashes and source commit in
`submission/FINAL_RELEASE.json`; publication follows Linux and Windows checks.
The [closeout record](docs/PROJECT_CLOSEOUT_20261125.md) maps the completed work
to its contributors. The [validation record](docs/FINAL_VALIDATION_20261125.md)
records the checks for this revision. These changes add no benchmark samples.

The latest fresh-host run was completed on **22 November**.
[Run 45015126850](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/45015126850)
rebuilt all five cases and produced **30 complete comparison calls, 15 complete
method pairs, 40 complete diagnostic calls and five successful builds**.
The [acceptance receipt](results/2026-11-22/summaries/acceptance-45015126850-attempt1/acceptance.json)
accounts for all 948 archived evidence files. No comparison reached an inner
timeout, outer timeout or schedule-budget limit. This engineering check has
its own [case and host records](results/2026-11-22/summaries/acceptance-45015126850-attempt1/SUMMARY.md);
the historical studies below keep their original samples.

## Clone and verify the archived evidence

Local checks require Git, Make and Python 3.9 or later. The evidence audits use
the Python standard library and read the archived files without running the
benchmarks. Start from a new directory:

```bash
git clone https://github.com/Sasuke-666/CS340-Research-Paper-Replication.git
cd CS340-Research-Paper-Replication
git rev-parse HEAD
make check
make audit
```

`make audit` checks the historical pilot/follow-up archive, the original-driver
comparison, the compatible-driver comparison, the independent member batch
and the controlled layout diagnostic, plus the completed fresh-host acceptance.
Its comparison targets also
verify startup-failure manifests and compare checked-in summaries against an
independent recount without rewriting them. The historical archive has 126
manifest files and 40 command logs; its recorded fixed replay signatures were
4/5 for `reorder_3_bad`, 5/5 for `reorder_4_bad` and 5/5 for `df`.

The comparison summarizer recounts raw logs, checks manifests and records
complete and incomplete observations. Its outputs are `summary.json`,
`all_trials.csv` and `SUMMARY.md`. Use the explicit command below for the
separate archived three-pair follow-up.

The required `--output` location must be outside the raw evidence batch. This
example creates a fresh temporary directory and preserves the archived bytes:

```bash
SUMMARY_ROOT=$(mktemp -d)
python3 scripts/summarize_comparison.py \
  results/2026-11-07/comparison-42380929383 \
  --output "$SUMMARY_ROOT/original-driver"
printf 'Summary directory: %s\n' "$SUMMARY_ROOT/original-driver"
```

Audit the archived compatible batch separately. Its observed comparison
denominators are 100 attempted, 90 complete and 10 outer-timeout censored:

```bash
COMPATIBLE_SUMMARY_ROOT=$(mktemp -d)
python3 scripts/summarize_comparison.py \
  results/2026-11-07/comparison-42381922637 \
  --output "$COMPATIBLE_SUMMARY_ROOT/compatible-driver"
printf 'Summary directory: %s\n' "$COMPATIBLE_SUMMARY_ROOT/compatible-driver"
```

Audit the archived four-thread follow-up with its declared single-case,
three-pair sample; the observed denominator is six complete comparison calls:

```bash
FOLLOWUP_SUMMARY_ROOT=$(mktemp -d)
python3 scripts/summarize_comparison.py \
  results/2026-11-07/comparison-42384122902 \
  --cases reorder_4 --repeats 3 \
  --output "$FOLLOWUP_SUMMARY_ROOT/reorder4-followup"
```

Read the reported denominators and integrity findings before using the tables.
Means and sample standard deviations use explicitly eligible observations;
missing first failures stay missing. The summary does not turn execution
failures into valid zero-error results. Unit-test fixtures are synthetic test
inputs and are separate from measured experiments.

The report audit checks Tables 2–12 against those records, including sample
sizes, means, sample standard deviations, signed differences and missing values.
It also checks 18 numbered captions, their references in the text and four figure
paths. The explanation audit checks 66 source/log files and recounts failure
frequencies, depth layers and nested request prefixes. These checks cover the
recorded data and references; visual review is recorded separately for the
exported documents. Synthetic regression fixtures are kept out of the results.

## Windows archive verification

Native Windows supports the read-only evidence checks. Preserve archived bytes
when cloning, since Git line-ending conversion changes their recorded digests:

```powershell
git clone -c core.autocrlf=false https://github.com/Sasuke-666/CS340-Research-Paper-Replication.git
cd CS340-Research-Paper-Replication
$env:PYTHONUTF8 = "1"
python scripts/check_acceptance.py results/2026-11-22/acceptance-45015126850-attempt1 --output results/2026-11-22/summaries/acceptance-45015126850-attempt1 --check
python scripts/recount_twostage_acceptance.py
```

The CI job `windows-archive-audit` also checks the historical comparison, layout,
independent member evidence and report. Fresh benchmark builds and executions
use the documented x86_64 Linux/Docker environment below. The member's original
Windows failure transcript remains preserved in [PR #6's audit record](docs/reviews/1240000576-audit-20261122.txt).

## Independently rebuild and run a comparison

Use an isolated, disposable **x86_64 Linux machine** with Git, Bash, GNU timeout,
Make, Python 3.9 or later, Docker and permission to run Docker. Public downloads
require network access. The authors' runtime requires real-time scheduling
privileges. The experiment uses a privileged container on the disposable host;
its runtime network is disabled and it receives no personal credentials or host
Docker socket. Record the actual host kernel, CPU and available resources.

From the cloned repository root, run one independent `account` batch:

```bash
uname -a
docker version
git rev-parse HEAD
EVIDENCE_PATH="results/local-account-$(date -u +%Y%m%dT%H%M%SZ)"
make comparison CASE=account EVIDENCE_DIR="$EVIDENCE_PATH"
printf 'Evidence directory: %s\n' "$EVIDENCE_PATH"
```

`make comparison` calls `scripts/period_container_compatible.sh`, using the
compatible serialized method. Supported `CASE` values are `reorder_3`,
`reorder_4`, `account`, `lazy01` and `twostage`. Each selected case plans ten
repetitions per method. Use a fresh output
directory for every attempt, including retries. The archived `reorder_4`
serialized attempts reached the 120-second limit; keep any such result as
censored. Save failures and inspect the actual records before reporting
completion. A later study with a different outer limit has its own protocol and
archive and does not replace these observations.

To repeat the measurement design of the **22 November five-case acceptance**,
use three pairs and a 240-second watchdog explicitly. These are the exact
wrapper arguments exercised by its successful fresh-host workflow:

```bash
ACCEPTANCE_ROOT="results/local-acceptance-$(date -u +%Y%m%dT%H%M%SZ)"
for STUDY_CASE in reorder_3 reorder_4 account lazy01 twostage; do
  if bash scripts/period_container_compatible.sh "$STUDY_CASE" \
    "$ACCEPTANCE_ROOT/$STUDY_CASE" 3 240; then
    printf 'Completed case: %s\n' "$STUDY_CASE"
  else
    printf 'Incomplete case; preserve and inspect: %s\n' "$STUDY_CASE" >&2
  fi
done
ACCEPTANCE_SUMMARY=$(mktemp -d)
python3 scripts/summarize_comparison.py "$ACCEPTANCE_ROOT" --repeats 3 \
  --output "$ACCEPTANCE_SUMMARY/acceptance"
```

This local loop runs cases sequentially on the reader's machine, with a fresh
container per case. The hosted acceptance assigned a separate fresh machine
to each case. Both use the same host and built binary within each method pair;
separate local case directories do not imply separate physical hosts.
The local command reproduces each case's measurement settings and independent
recounting. The hosted workflow additionally archives the outer console, workflow provenance
and a full-batch manifest, then applies the strict acceptance gate. A local
integrity-only summary is not a complete acceptance receipt: inspect completion,
timeouts and budget status as specified in the [protocol](experiments/2026-11-22/ACCEPTANCE_PROTOCOL.md).
In the recorded acceptance, the six comparison calls per case took approximately
40.2 seconds (`reorder_3`), 288.1 (`reorder_4`), 237.0 (`account`),
109.4 (`lazy01`) and 12.9 (`twostage`) in total on each respective host.
Allow additional time for downloads, instrumentation, builds and the separate
40-call `reorder_3` diagnostic. New-machine times can differ substantially.

To repeat the original ten-pair, 120-second five-case design, use:

```bash
COMPARISON_ROOT="results/local-comparison-$(date -u +%Y%m%dT%H%M%SZ)"
for STUDY_CASE in reorder_3 reorder_4 account lazy01 twostage; do
  make comparison CASE="$STUDY_CASE" EVIDENCE_DIR="$COMPARISON_ROOT/$STUDY_CASE"
done
LOCAL_SUMMARY_ROOT=$(mktemp -d)
python3 scripts/summarize_comparison.py "$COMPARISON_ROOT" \
  --output "$LOCAL_SUMMARY_ROOT/comparison"
```

The loop preserves all case attempts even if one fails. Inspect the summary's
integrity findings and each case's command logs. A driver or workflow return
code alone does not establish a target assertion failure. The `reorder_3` case
also runs the registered fixed-witness replay diagnostic; report those results
separately from comparison repetitions.

To independently repeat the registered four-thread completion check, preserve
its three paired repetitions and 240-second outer limit:

```bash
NEW_DIR="results/local-reorder4-240s-$(date -u +%Y%m%dT%H%M%SZ)"
bash scripts/period_container_compatible.sh reorder_4 "$NEW_DIR" 3 240
FOLLOWUP_LOCAL_SUMMARY=$(mktemp -d)
python3 scripts/summarize_comparison.py "$NEW_DIR" \
  --cases reorder_4 --repeats 3 \
  --output "$FOLLOWUP_LOCAL_SUMMARY/reorder4-followup"
```

The wrapper's default settings remain ten repetitions and 120 seconds. The
explicit parameters above reproduce the separately registered follow-up design.
The archived six calls took about 7.8 minutes of whole-driver time in total;
allow additional time for image download, build and instrumentation. Runtime on
a new host may differ.

To repeat the historical experiments, use fresh directories:

```bash
make pilot EVIDENCE_DIR=results/local-pilot-001
make followup EVIDENCE_DIR=results/local-followup-001
```

Each target clones the pinned upstream source, rebuilds its instrumentation and
benchmarks, and records commands, stdout/stderr, exit status, timing, image
identity and checksums. Generated binaries and bitcode stay in the disposable
container. Compatible runs additionally preserve `serial_abi16.diff`, source
hashes and the shared-memory probe. The known runtime/driver array-layout limits
remain part of the study's limitations.

Source pin: `cb8deb9a176e5bb292d70d46557dd61dc0e98069`.

Image pin: `wcventure/period@sha256:8f47d8b9148f2db579627842026e722d0f205ddeab13e70ee41a8df3dbd59fbc`.

The recorded container uses Ubuntu 18.04.5, Clang 10.0.0 and Python 3.6.9.
Container Python and the local audit Python are separate environments. Docker
pins the userland image; the host kernel and CPU are recorded per batch. The
historical runs recorded kernel 7.0.0-1017-azure and two permitted CPUs; the
historical follow-up host identified AMD EPYC 7763. The 240-second four-thread
follow-up also used AMD EPYC 7763, with four permitted CPUs, kernel
7.0.0-1017-azure, Clang 10.0.0, GCC 7.5 and container Python 3.6.9. Consult each
batch's environment files for its actual hardware and compiler versions.

The historical exploration/replay/build outer limits were 90/20/180 seconds.
The primary expanded comparison has a 120-second outer limit; the separate
four-thread completion follow-up uses 240 seconds. Whole-driver elapsed time
includes calibration and reporting. Its interpretation differs
from native target execution time and from the paper's workstation timings.

## Reproduce the controlled layout diagnostic

Use the same disposable x86_64 Linux and Docker prerequisites as above. Each
case builds once and runs twenty invocations serially. The two capacity conditions
alternate AB/BA. Each invocation has a 120-second watchdog; the wrapper bounds
the container phase at 3,000 seconds and the image pull at 420 seconds. Actual
elapsed time depends on the host and download cache. Do not run inside a shared
container with other workloads using IPC key 1111.

```bash
LAYOUT_ROOT="results/local-layout-$(date -u +%Y%m%dT%H%M%SZ)"
for STUDY_CASE in account lazy01; do
  bash scripts/period_container_layout.sh "$STUDY_CASE" "$LAYOUT_ROOT/$STUDY_CASE"
done
LAYOUT_SUMMARY_ROOT=$(mktemp -d)
python3 scripts/summarize_layout.py "$LAYOUT_ROOT" \
  --output "$LAYOUT_SUMMARY_ROOT/layout"
```

Inspect the actual denominator and any integrity findings. Native structure and
scheduling probes are separate from workload counts. Synthetic decoder sentinels
are explicitly labelled. Every raw file is retained, including a failed or
censored attempt. The one-constant change and fresh IPC controls are recorded
with source hashes and per-invocation cleanup logs. Requested schedule sequences
are compared independently; they do not provide an actual memory-operation trace.
The historical experiments retain their original source and state behavior.

For the archived 14 November evidence, `make audit-layout` checks two explicit
case scopes: [original lazy01](results/2026-11-14/summaries/layout-43570556202-lazy01/SUMMARY.md)
and [recovery account](results/2026-11-14/summaries/layout-recovery-43575584325-account/SUMMARY.md).
The original account scope has twenty planned invocations and unknown actual
counts. Its absence is not a zero-detection observation. Recovery was triggered
by evidence availability, before any recovery outcomes were known.

## Regenerate figures and export Word/PDF

Use a Python environment with the figure and report dependencies. The expanded
comparison plot uses the separately audited primary and four-thread follow-up
summaries now preserved in the repository. The script requires their declared
complete samples and valid evidence checks. The four-thread comparison is labelled `n = 3`; the other four cases
use `n = 10`. Historical figures retain their original data.

```bash
python3 -m pip install -r requirements-figures.txt -r requirements-report.txt
python3 scripts/plot_period_results.py
python3 scripts/summarize_comparison.py \
  results/2026-11-07/comparison-42381922637 \
  --output results/2026-11-07/summaries/comparison-42381922637
python3 scripts/summarize_comparison.py \
  results/2026-11-07/comparison-42384122902 \
  --cases reorder_4 --repeats 3 \
  --output results/2026-11-07/summaries/comparison-42384122902
python3 scripts/plot_comparison_results.py
make audit-layout
python3 scripts/plot_layout_results.py
make deliverables
```

The expanded figures are saved under `results/2026-11-07/figures/` as
`expanded_schedule_comparison.svg` and `expanded_paper_gaps.svg`. Checked-in SVGs
can be viewed without installing plotting dependencies. The separately scoped
capacity study produces `results/2026-11-14/figures/layout_comparison.svg`, using
only its independently audited summary and displaying actual metric denominators.
The export command
creates `CS340_PERIOD_Final_Report_20261125.docx` and
`CS340_PERIOD_Final_Report_20261125.pdf` in `report/export/`; exporting does
not execute experiments or alter observations.

The [Chinese handbook](docs/MEMBER_ACTIONS_ZH.md) covers submission and member
preparation. To export its editable Word copy:

```bash
make checklist
```

Export names and dates come from `report/REVISION_DATE`, currently 2026-11-25,
and must match the report header. Report evidence links point to the exporting
checkout's exact commit when Git metadata is available. The files in
`report/export/` are working exports; reviewed release copies are in
`submission/`.

## Archived studies and member work

The group confirmed the paper selection to the maintainer on 7 November 2026.
The [weekly record](docs/WEEKLY_PROGRESS.md) gives the dates of subsequent work.
The table below separates the experiments used in the report.

| Evidence batch | Sample and outcome | Record |
| --- | --- | --- |
| Historical pilot and follow-up | Nine pilot runs, nine depth-extension runs and fifteen witness replays: 33 invocations; six builds and one scheduling probe counted separately | [Pilot report](report/PILOT_REPORT.md), [126-file manifest](results/2026-11-07/manifest.json), [follow-up protocol](experiments/2026-11-07/FOLLOWUP_PROTOCOL.md) |
| Original serialized driver, 7 November | Driver failures prevented a valid method comparison; failed attempts are retained and excluded from valid-sample statistics | [Run 42380929383](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/42380929383), [archive](results/2026-11-07/comparison-42380929383) |
| Compatible-driver comparison, 7 November | Five cases, ten planned pairs per case: 100 attempts, 90 complete calls and ten serialized `reorder_4` calls censored at 120 seconds | [Protocol](experiments/2026-11-07/COMPARISON_PROTOCOL.md), [run 42381922637](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/42381922637), [summary](results/2026-11-07/summaries/comparison-42381922637/SUMMARY.md) |
| Four-thread completion follow-up, 7 November | Three `reorder_4` pairs on a new host with a 240-second limit; all six calls complete | [Registered protocol](experiments/2026-11-07/REORDER4_TIMEOUT_FOLLOWUP.md), [run 42384122902](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/42384122902), [summary](results/2026-11-07/summaries/comparison-42384122902/SUMMARY.md) |
| Li Yangshuo's independent `account` run, 8 November | Twenty complete calls and ten pairs on one WSL2 host | [Member review](docs/reviews/1240001156-clean-run.md), [batch summary](results/member-reruns/1240001156-account-20261108T122201Z-summary/SUMMARY.md) |
| Capacity diagnostic, 14 November | Original `lazy01` and recovery `account`: twenty complete calls and ten pairs each, on separate hosts; the original `account` outcomes remain unknown | [Protocol](experiments/2026-11-14/LAYOUT_PROTOCOL.md), [lazy01 summary](results/2026-11-14/summaries/layout-43570556202-lazy01/SUMMARY.md), [recovery account summary](results/2026-11-14/summaries/layout-recovery-43575584325-account/SUMMARY.md) |
| He Boyu's selected twostage witness, 15 November | Five fresh replays, all reaching the selected assertion | [Replay archive](results/member-reruns/1240000576-twostage-43681034375/README.md), [source analysis](docs/reviews/1240000576-twostage-witness-review.md) |

### Main comparison

The five cases are `reorder_3`, `reorder_4`, `account`, `lazy01` and `twostage`:
four program families with two, three or four threads. Each method pair uses
the same built binary, depth 3 and a 10,000-schedule budget, with AB/BA execution
order. Each driver uses its own depth definition: PERIOD searches periods
2 through d+1; the serialized driver searches N through d+N−1 for N threads.
[Report §2](report/EXPANDED_REPORT.md#2-experimental-setup-and-registered-design)
explains this distinction and the two-thread case where the ranges coincide.
The comparison method, `author_serialized_abi16`, copies the current
driver's shared-memory interface and four array element types into the authors'
older serialized driver. Its scheduling section is preserved. The
[compatibility protocol](experiments/2026-11-07/COMPATIBILITY_PROTOCOL.md)
documents this change and the limits of comparison with the paper's historical
Serial implementation.

The compatible study and four-thread follow-up together contain **106 attempts,
96 complete calls and 43 complete pairs**: forty pairs from the four primary
cases and three from the follow-up. At the original 120-second limit,
`reorder_4` has ten complete PERIOD calls and no complete serialized call, so it
provides no complete timing pair. Those censored prefixes remain in the archive;
their partial schedule counts are not used as finished enumeration totals.
The separate forty replay-diagnostic calls and five builds are outside the
100 comparison attempts.

The four-thread follow-up uses a longer outer watchdog and a new host, retaining
the program, input, depth, schedule budget, drivers and internal timeout. Its
means and sample standard deviations (`n = 3` per method) are:

| Method | Explored schedules | First failing schedule | Buggy schedules | Whole-driver seconds |
| --- | ---: | ---: | ---: | ---: |
| PERIOD | 100 ± 0 | 9 ± 0 | 12 ± 0 | 21.84 ± 0.50 |
| `author_serialized_abi16` | 384 ± 0 | 47 ± 0 | 86.33 ± 1.15 | 133.96 ± 2.70 |

Serial's first-failure position and buggy-schedule count differ from the paper.
Schedule-count agreement therefore supports only part of the reproduction.
Elapsed times are compared within a case and host; the earlier PERIOD calls
are not pooled with the follow-up.

### Capacity diagnostic

The [registered intervention](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/commit/bddb831319679c30586d9bbe689fb11b897f1a14)
changes one Python array-capacity constant from 1990 to 3964. Native runtime and
benchmark code are unchanged. Each case uses the same binary and host for both
conditions, fresh private IPC state and ten AB/BA pairs.

[Run 43570556202](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/43570556202)
archived twenty complete `lazy01` calls. Its `account` job failed, and neither
the raw artifact nor the job log was available after two final checks. The
[observations](experiments/2026-11-14/account-evidence-failure/FINAL_OBSERVATION.json)
record that uncertainty. A separate
[recovery protocol](experiments/2026-11-14/ACCOUNT_RECOVERY_PROTOCOL.md), committed
as `ea273fe4` before
[run 43575584325](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/43575584325),
fixed twenty new `account` calls using the same measurement bytes on a new host.
Recovery results keep their own sample; the unavailable original results remain
unknown.

The original lazy01 archive has 304 manifest entries and recovery account has
571; all pass the hash audit. The capacity change alters the observed feedback
hash while preserving the requested schedules: 39 for lazy01 and 65 for account.
Corrected first-failure positions are 8.200 ± 0.422 and 10.200 ± 0.632,
respectively, against paper references 3 and 2. Timing and failure-yield changes
have mixed directions. Report Tables 10–12 and Figure 4 explain what this
intervention resolves and which discrepancies remain.

### Member contributions

All eight member PRs are integrated with their original authors and dates:

- Li Yangshuo's [PR #2](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/2)
  contributes the independent account experiment, including the initial image-
  pull failure, environment records and raw logs. [PR #3](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/3)
  adds a [secondary account review](docs/reviews/1240001156-account-supplement.md),
  and [PR #5](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/5)
  checks report traceability and adds missing narrative references.
  [PR #8](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/8)
  audits the release and Windows analysis path, independently recounts the
  acceptance metrics, and adds parser and validation-manifest checks.
- He Boyu's [PR #1](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/1)
  recounts 26 four-thread logs and treats the ten censored attempts separately.
  [PR #4](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/4)
  contributes twostage source analysis, a [necessary-order table](docs/reviews/1240000576-twostage-trace.md),
  a [Chinese explanation](docs/reviews/1240000576-twostage-summary-zh.md) and five
  fresh witness replays. [PR #6](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/6)
  checks the final twostage statistics and presentation.
  [PR #7](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/7)
  protects the recount with three synthetic regression cases.

`make audit` verifies the independent account batch's 880 manifest entries and
twenty logs. `make audit-member-reviews` checks forty account request sequences,
all twelve new witness-file checksums and the selected assertion after the
reproduction marker in each replay. A missing assertion, timeout or checksum
mismatch fails the check. The [integration record](docs/INTEGRATION_20261116.md)
and [contribution ledger](docs/CONTRIBUTIONS.csv) distinguish the members' work
from maintainer verification.

`make audit-validation` independently checks the acceptance metrics and the
member validation manifest. It is included in `make audit` and Linux/Windows
continuous checks. The [closeout record](docs/PROJECT_CLOSEOUT_20261125.md)
distinguishes original measurements, secondary review, tests and later
maintenance, with links to the actual submissions.

## Repository layout

| Path | Content |
| --- | --- |
| `scripts/`, `Makefile` | Build, run, parse, verify and summarize commands |
| `tests/` | Repository and experiment-helper tests |
| `experiments/2026-11-07/`, `experiments/2026-11-14/` | Protocols and explicit amendments |
| `results/2026-11-07/`, `results/2026-11-14/`, `results/member-reruns/` | Separate raw evidence batches, hashes and derived results |
| `report/EXPANDED_REPORT.md` | Final English report source |
| `report/PILOT_REPORT.md` | Historical pilot report |
| `docs/` | Requirements, sources, deviations, team and review records |
| `presentation/` | English slide content, Chinese speaker notes and defence outline |
| `submission/` | Frozen final documents, content manifest and release notes |

## Team and course commitments

The three confirmed member identities are recorded in [the team table](docs/TEAM.csv):

| Full name | Student ID | GitHub username |
| --- | --- | --- |
| 孙皓扬 | 1240001201 | Sasuke-666 |
| 李扬烁 | 1240001156 | barkhorn996 |
| 何博宇 | 1240000576 | heboyu0714 |

The fourth member remains to be confirmed through the course's group allocation
process. Both member accounts had verified write access on 8 November, and all eight
member submissions are integrated. The registration receipt
and any later course allocation still need their actual evidence.

Every commit message includes the actual responsible student's ID and full name,
including merge and squash messages. Each member uses their own account for
substantive work. The repository must receive meaningful progress each week
before Sunday 23:59; late pushes do not recover missed weeks. The source does
not specify the check timezone, so confirm the course announcement and submit
early using the group's stated local planning time.

The submitted independent rerun is complete. Each member's own understanding and
any new review still require actual participation. Use the [Chinese member action list](docs/MEMBER_ACTIONS_ZH.md),
[individual review template](docs/reviews/REVIEW_TEMPLATE.md) and
[course requirement checklist](docs/COURSE_REQUIREMENTS.md).
Presentation is tentatively 1 December 2026. Its separate rubric and the exact
final-report deadline still require verification. The final report must be in
English and submitted as PDF. The initial final submission is tagged
`v1.0`; the prose revision is `v1.0.1` and the final member integration is
`v1.0.2`. The release links provide
the reviewed documents and complete source/evidence bundles. The course portal receipt and oral presentation
remain actions for the registered members.
