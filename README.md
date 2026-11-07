# CS340 — PERIOD Research Paper Replication

Operating Systems · Academic Year 2026–2027

**Selected paper:** *Controlled Concurrency Testing via Periodical Scheduling*
(ICSE 2022). The group selection was confirmed to the project maintainer on
7 November 2026. This records the received confirmation, not a change of paper.

## Measured progress — 7 November 2026

The project has completed a reduced-scale pilot on two original Table 2 cases,
a separate double-free smoke test, a single-factor depth-bound extension and
fixed-witness replay checks. **33 test/replay invocations** were recorded:
9 pilot runs, 9 extension runs and 15 replays. Six builds and one scheduling
capability probe are recorded separately.

Read the [English stage report](report/PILOT_REPORT.md). Its verdict is **partial
replication within the stated scope**: explored-schedule counts match the selected
paper rows, while some error counts and replay outcomes vary between runs.
No unrun comparison with SERIAL or other tools is claimed.

- [Exact evidence and hashes](results/2026-11-07/manifest.json): 126 raw files.
- [Pilot execution](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/42368129299).
- [Controlled follow-up and archive](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/42369166599).
- [Protocols](experiments/2026-11-07/PROTOCOL.md) and [follow-up protocol](experiments/2026-11-07/FOLLOWUP_PROTOCOL.md).
- [Environment differences](docs/DEVIATIONS.csv), [sources and license](docs/SOURCES.md),
  [contributions](docs/CONTRIBUTIONS.csv), and [academic disclosure](docs/AI_USAGE.md).

## Verify the archived results without Docker

Requirements: Git and Python 3.9 or later; the checks and summaries use only the
Python standard library. Clone this private repository using your own authorized
account, change to its root, and run:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
python3 scripts/verify_period_evidence.py
python3 scripts/summarize_period.py results/2026-11-07/pilot
python3 scripts/summarize_followup.py
```

Expected verification: 126 manifest files and 40 command logs verified; fixed
replay signatures 4/5 for reorder_3_bad, 5/5 for reorder_4_bad and 5/5 for df.
The summary writes CSV and JSON using mean and sample standard deviation.
Null values remain null; a missed failure is never turned into a zero-valued
first-failure position. Unit-test fixtures are synthetic and are not experiments.

## Rebuild and run the experiments

Use an isolated, disposable **x86_64 Linux machine** with Git, Bash, GNU timeout,
Docker, network access for public downloads, and permission to run Docker.
The authors' runtime needs real-time scheduling privileges. The script uses
`--privileged` only on that disposable machine, without a network, host Docker
socket, private Git checkout or credentials inside the experiment container.
Do not run this workflow on a production computer or mount personal directories.

```sh
# Build and run three repetitions of each pilot case.
make pilot EVIDENCE_DIR=results/local-pilot-001

# Build and run the controlled extension and fixed-witness replays.
make followup EVIDENCE_DIR=results/local-followup-001
```

Use a fresh output directory each time. Both targets clone the exact original
source commit and rebuild its analysis/instrumentation layer and benchmarks.
They preserve commands, stdout/stderr, exit status, timing, image identity and
checksums. Generated binaries and bitcode stay in the disposable container.

Source pin: `cb8deb9a176e5bb292d70d46557dd61dc0e98069`.
Image pin: `wcventure/period@sha256:8f47d8b9148f2db579627842026e722d0f205ddeab13e70ee41a8df3dbd59fbc`.
Container: Ubuntu 18.04.5, Clang 10.0.0 and Python 3.6.9 in the recorded runs.
The host kernel and CPU are recorded rather than pinned by Docker. The observed
kernel was 7.0.0-1017-azure with two permitted CPUs; the follow-up host identified
AMD EPYC 7763. See the report for the resulting limits on comparisons.

Observed whole-driver pilot runtimes were 7.757 ± 1.042 s (smoke),
7.335 ± 0.204 s (three threads), and 17.475 ± 3.508 s (four threads), excluding
container pull/build. These are observations, not runtime guarantees. Each pilot
or extension invocation has a 90-second outer limit, each replay 20 seconds,
and each build 180 seconds. A zero workflow exit is not itself a bug verdict.

Both PERIOD workflows can now be dispatched manually and produce downloadable
evidence. The completed 7 November jobs have already been archived in Git;
future dispatches do not overwrite those historical files. Use a new batch
directory and updated protocol for a new study.

To regenerate the figures, use an isolated Python environment with
`pip install -r requirements-figures.txt`, then run
`python3 scripts/plot_period_results.py`. The checked-in SVG figures can be
viewed without installing plotting dependencies.

## Repository layout

| Path | Content |
| --- | --- |
| `scripts/`, `Makefile` | Rebuild/run, parse, verify and summarize commands |
| `tests/` | Repository and experiment-helper tests |
| `experiments/2026-11-07/` | Protocols fixed before their respective runs |
| `results/2026-11-07/` | Raw pilot/follow-up evidence, hashes, derived summaries and figures |
| `report/PILOT_REPORT.md` | English stage report with scope, results, analysis and extension |
| `docs/` | Course requirements, source/deviation records and team/review information |
| `presentation/` | Presentation materials to be prepared using the separate instructions |

## Course commitments and remaining human work

Every commit message must include the actual contributor's student ID and full
name. Each member must use their own account for genuine substantive work.
The repository must receive meaningful progress each week before Sunday 23:59;
late pushes do not repair missed weeks. The supplied document does not specify
the check timezone. Submit early in Macau local time and confirm announcements.

The current known member is recorded in `docs/TEAM.csv`; other identities,
teaching-team access and the registration receipt still need verification.
A second member's independent rerun and group review have not been recorded.
See [the review checklist](docs/REVIEW_CHECKLIST.md). Presentation is tentatively
1 December 2026. The separate presentation rubric and exact final-report deadline
remain to be obtained. The final report must be in English and submitted as PDF.
This is a stage report, not the final submission; no `v1.0` tag has been created.
