# Reproduction plan — provisional

## Planned paper

Controlled Concurrency Testing via Periodical Scheduling (PERIOD), ICSE 2022.
This is paper 4 in the instructor's list (page 4).
Group confirmation: **pending**. Original authors' implementation:
https://github.com/wcventure/PERIOD

## Feasibility gate

Before committing to the final experimental scope:

1. Inspect the upstream paper, README, license and installation requirements.
2. Record the exact upstream commit and actual machine/OS/kernel/compiler versions.
3. Build one original example and run one case tied to a named original table/figure.
4. Preserve commands, exit status, output and any failure diagnosis.
5. Have another member reproduce that case from the written instructions.

No gate above is marked completed by the scaffold. If an obstacle requires
changing paper, apply to the TA within the stated November 1 window.

## Proposed claims, to be finalized against original tables

| Candidate | Proposed question | Required mapping | Current status |
| --- | --- | --- | --- |
| C1 | Does PERIOD reproduce the selected original cases' bug-discovery outcomes and exploration counts? | Exact original table/figure, rows, configurations and definitions | Not yet selected or tested |
| C2 | Are observed mismatches explained by a controlled change of configuration or environment? | C1 plus controlled re-run evidence | Not tested |
| C3, optional | Does a verified baseline comparison support the scoped comparative claim? | Matching baseline implementation, workloads, budget and metric | Baseline not verified |

Select cases before reviewing final outcomes and record the rationale. Do not
silently remove failed or inconvenient cases. A reduced scale must be disclosed.
Do not label the paper's reported numbers as measurements taken by this group.

## Measurement plan

At least three independent runs for the relevant measurements. Use more runs
when feasible and justify the number. Preserve errors and timeouts separately
from successful runs and bug counts. State whether an output is deterministic.
For each run keep: run ID, source commit, case, command, inputs, environment ID,
start/end times, exit code, status, raw-log path and metric definitions.

## Proposed extension

Choose one research question after the first successful run. One possible
proposal is varying thread count in a suitable original test family while
holding its other logic, inputs, hardware, compiler and test budget fixed.
Confirm the chosen points extend the paper, and disclose unsupported assumptions.
No parameterized benchmark or extension result is provided by this scaffold.

## Deliverables

A pinned and documented experiment environment; build/run scripts; actual raw
logs; Paper vs. Ours comparisons; controlled discrepancy checks; one extension;
English PDF report; presentation following the separate instruction; actual
individual contributions; AI disclosure; final `v1.0` tag.
