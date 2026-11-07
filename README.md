# CS340 — PERIOD Research Paper Replication

Operating Systems · Academic Year 2026–2027 · Public course repository

**Selected paper:** *Controlled Concurrency Testing via Periodical Scheduling*
(ICSE 2022). The group confirmed its selection to the project maintainer on
7 November 2026. This is the date of that confirmation.

## Stage progress — 7 November 2026

Read the [expanded English stage report](report/EXPANDED_REPORT.md) for the
current study, claim-by-claim assessment and limitations. The
[historical pilot report](report/PILOT_REPORT.md) remains available with its
original evidence. The overall work is a reduced-scale replication in progress.
The [dated progress record](docs/WEEKLY_PROGRESS.md) separates the actual two
weeks of work, and the [expanded validation record](docs/VALIDATION_EXPANDED_20261107.md)
links the 98-test result and independent evidence audits.

| Evidence batch | Scope | Interpretation and status |
| --- | --- | --- |
| Historical pilot and follow-up | 9 pilot runs, 9 depth-extension runs and 15 fixed-witness replays: **33 test/replay invocations**; six builds and one scheduling probe recorded separately | Selected schedule counts matched the paper; error counts and replay outcomes varied. These observations retain their original scope. |
| Original-driver comparison, run `42380929383` | Five cases, ten planned repetitions per method, with a separate replay diagnostic | Preserve the original `author_serialized` driver failures as failed execution. They are excluded from valid comparison observations and never interpreted as zero detected errors. |
| Compatible-driver study, run `42381922637` | Five cases, ten paired repetitions per case: `period` versus `author_serialized_abi16`; 100 comparison attempts | Archived: **90 complete observations and 10 observations censored at the 120-second outer limit**. All ten censored observations are `reorder_4` with `author_serialized_abi16`. |
| Four-thread completion follow-up, run `42384122902` | `reorder_4` only; three paired repetitions; 240-second outer limit | **6/6 complete and eligible observations; three complete pairs.** Archived and independently audited. The protocol was registered in commit `15ae481` before measurement. |

The five cases are `reorder_3`, `reorder_4`, `account`, `lazy01` and `twostage`.
They cover four program families and 2/3/4 threads. For each case, both methods
use the same built binary, depth 3, schedule budget 10,000 and alternating AB/BA
execution order. The compatible serialized method copies the current driver's
shared-memory interface and four array element types into the authors' older
driver; the serialized scheduling section is preserved. Its explicit label is
`author_serialized_abi16`. Correspondence with the paper's historical Serial
implementation remains a limitation, even where individual counts agree.

The compatible batch contains 80 complete observations across `reorder_3`,
`account`, `lazy01` and `twostage`, plus ten complete PERIOD observations for
`reorder_4`. The ten serialized `reorder_4` attempts all reach the 120-second
outer limit. Thus four cases provide ten complete timing pairs each;
`reorder_4` provides no complete timing pair at this limit. Its censored times
are not substituted as exact completion times, and partial schedule counts are
not used as completed enumeration totals. The separate 40 replay-diagnostic
invocations and five builds are recorded outside the 100 comparison attempts.

The four-thread follow-up preserves the program, input, depth, schedule budget,
drivers and internal timeout. It increases the outer watchdog to 240 seconds
and uses three declared pairs on a new host. Its observations remain a separate
batch; the ten earlier censored observations stay in the archive. Both methods
from the follow-up are used together for its matched comparison.

The two compatible batches contain **96 complete observations (90 + 6)** and
ten censored observations across 106 attempts. The matched analysis has
**43 complete pairs: 40 from four primary cases and three from the four-thread
follow-up**. The ten earlier PERIOD `reorder_4` observations remain in the
primary batch; they are not pooled with the three new observations.

The [audited four-thread summary](results/2026-11-07/summaries/comparison-42384122902/SUMMARY.md)
reports the following values (mean ± sample SD, `n = 3` per method):

| Method | Explored schedules | First failing schedule | Buggy schedules | Whole-driver seconds |
| --- | ---: | ---: | ---: | ---: |
| PERIOD | 100 ± 0 | 9 ± 0 | 12 ± 0 | 21.84 ± 0.50 |
| `author_serialized_abi16` | 384 ± 0 | 47 ± 0 | 86.33 ± 1.15 | 133.96 ± 2.70 |

These are observations from one matched host and declared configuration.
Serial first-failure and buggy-schedule counts differ from the paper
references, so schedule-count agreement alone does not establish full
replication of the historical Serial implementation.

Keep the original-driver and compatible-driver batches separate. Exclude failed
original-driver observations from valid-sample statistics, and retain every
attempt in the evidence record. Comparisons of elapsed time use matched pairs
within one case and batch; separate hosted machines are separate timing scopes.

- [Compatible-driver workflow](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/42381922637) and [its preserved evidence](results/2026-11-07/comparison-42381922637).
- [Original-driver workflow](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/42380929383) and [its preserved evidence](results/2026-11-07/comparison-42380929383).
- [Four-thread follow-up workflow](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/42384122902), [preserved evidence](results/2026-11-07/comparison-42384122902) and [registered protocol](experiments/2026-11-07/REORDER4_TIMEOUT_FOLLOWUP.md).
- [Registered expanded protocol and amendments](experiments/2026-11-07/COMPARISON_PROTOCOL.md) and [compatibility protocol](experiments/2026-11-07/COMPATIBILITY_PROTOCOL.md).
- [Historical pilot evidence manifest](results/2026-11-07/manifest.json): 126 raw files.
- [Pilot workflow](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/42368129299) and [follow-up workflow](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/42369166599).
- [Pilot protocol](experiments/2026-11-07/PROTOCOL.md) and [follow-up protocol](experiments/2026-11-07/FOLLOWUP_PROTOCOL.md).
- [Environment differences](docs/DEVIATIONS.csv), [sources and license](docs/SOURCES.md), [actual contributions](docs/CONTRIBUTIONS.csv) and [academic disclosure](docs/AI_USAGE.md).

## Clone and verify the archived evidence

The repository is public. Read-only cloning requires no collaborator permission.
Local checks and summaries require Git, Make and Python 3.9 or later; they use the
Python standard library. From a new directory:

```bash
git clone https://github.com/Sasuke-666/CS340-Research-Paper-Replication.git
cd CS340-Research-Paper-Replication
git rev-parse HEAD
make check
make audit
```

`make audit` checks the historical pilot/follow-up archive, the original-driver
comparison and the compatible-driver comparison. Its comparison targets also
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
compatible serialized method. The five supported `CASE` values are listed
above. Each selected case plans ten repetitions per method. Use a fresh output
directory for every attempt, including retries. The archived `reorder_4`
serialized attempts reached the 120-second limit; keep any such result as
censored. Save failures and inspect the actual records before reporting
completion. A later study with a different outer limit has its own protocol and
archive and does not replace these observations.

For a complete five-case rerun and an independent summary, use:

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
python3 scripts/export_stage_report.py \
  --source report/EXPANDED_REPORT.md --output report/export
```

The expanded figures are saved under `results/2026-11-07/figures/` as
`expanded_schedule_comparison.svg` and `expanded_paper_gaps.svg`. Checked-in SVGs
can be viewed without installing plotting dependencies. The export command
creates `CS340_PERIOD_Expanded_Report_20261107.docx` and
`CS340_PERIOD_Expanded_Report_20261107.pdf` in `report/export/`; exporting does
not execute experiments or alter observations.

The [separate Chinese member action checklist](docs/MEMBER_ACTIONS_ZH.md) and
[individual review template](docs/reviews/REVIEW_TEMPLATE.md) describe the human
work still requiring actual completion. To create an editable Word checklist:

```bash
python3 scripts/export_member_checklist.py \
  --output report/export/CS340_Member_Action_Checklist_20261107.docx
```


## Repository layout

| Path | Content |
| --- | --- |
| `scripts/`, `Makefile` | Build, run, parse, verify and summarize commands |
| `tests/` | Repository and experiment-helper tests |
| `experiments/2026-11-07/` | Protocols and explicit amendments |
| `results/2026-11-07/` | Separate raw evidence batches, hashes and derived results |
| `report/EXPANDED_REPORT.md` | Current English stage report |
| `report/PILOT_REPORT.md` | Historical pilot report |
| `docs/` | Requirements, sources, deviations, team and review records |
| `presentation/` | Presentation work pending the separate course instructions |

## Team and course commitments

The three confirmed member identities are recorded in [the team table](docs/TEAM.csv):

| Full name | Student ID | GitHub username |
| --- | --- | --- |
| 孙皓扬 | 1240001201 | Sasuke-666 |
| 李扬烁 | 1240001156 | Awaiting member confirmation |
| 何博宇 | 1240000576 | Awaiting member confirmation |

The fourth member remains to be confirmed through the course's group allocation
process. Public repository access is available; each contributor's write access,
registration receipt and individual contribution still need their actual checks.

Every commit message includes the actual responsible student's ID and full name,
including merge and squash messages. Each member uses their own account for
substantive work. The repository must receive meaningful progress each week
before Sunday 23:59; late pushes do not recover missed weeks. The source does
not specify the check timezone, so confirm the course announcement and submit
early using the group's stated local planning time.

A student's independent rerun and group review remain separate human tasks.
Use the [Chinese member action list](docs/MEMBER_ACTIONS_ZH.md),
[individual review template](docs/reviews/REVIEW_TEMPLATE.md) and
[course requirement checklist](docs/COURSE_REQUIREMENTS.md).
Presentation is tentatively 1 December 2026. Its separate rubric and the exact
final-report deadline still require verification. The final report must be in
English and submitted as PDF. This repository records a stage of the project;
the final `v1.0` release follows completion and review.
