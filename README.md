# CS340 — Research Paper Replication

Operating Systems · Academic Year 2026–2027

## Current status

This repository starts with a reproduction plan, evidence conventions and local
repository checks. **No PERIOD experiment has been run or validated by this
initialization package.** No performance result or claim verdict is asserted.
The planned paper is **Controlled Concurrency Testing via Periodical Scheduling
(PERIOD), ICSE 2022**. Final selection and experiment scope must be confirmed by
the group and recorded in `docs/REPRODUCTION_PLAN.md`.

- Paper: https://wcventure.github.io/pdf/ICSE2022_PERIOD.pdf
- Authors' code: https://github.com/wcventure/PERIOD
- This is the group's reproduction workspace, not the authors' implementation.
- No upstream source, course slides, paper PDFs or credentials are bundled here.

## Course milestones

| Item | Instructor's stated date / rule | Qualification |
| --- | --- | --- |
| Team formation | October 25, 2026 | Exact time is not specified. |
| Request a paper change | By November 1, 2026 | Apply to the TA. |
| Presentation | December 1, 2026 | Tentative date. |
| Repository check | Every Sunday at 23:59 | First specific check date and timezone are not explicitly stated. |
| Final report / final tag | At the final deadline | Exact final submission deadline is not specified in this document. |

Register the group information and reproduction repository link using the course
form: https://v.wjx.cn/vm/rZCQLSE.aspx

Source: `2609_CS340_Research_Paper_Replication(1).pdf`, pp. 1, 3–4.
The repository creator does **not** submit the form or grant instructor access.
The document's original filename is recorded for traceability; it is not included
in this repository.

## Access before registration

The initialization script creates a **private** repository. This is a privacy
choice, not an instructor requirement. The repository owner must arrange access
for all group members and the teaching team, and verify that the teaching team
can inspect it. A private link alone does not establish reviewer access.
Do not infer a GitHub username from a student's or TA's email address.

## Repository map

| Path | Purpose |
| --- | --- |
| `docs/COURSE_REQUIREMENTS.md` | Instructor requirements and open questions |
| `docs/REPRODUCTION_PLAN.md` | Proposed claims, feasibility checks and scope |
| `docs/TEAM.csv` | Verified member identities; never invent missing members |
| `docs/CONTRIBUTIONS.csv` | Actual contributions and evidence references |
| `docs/DEVIATIONS.csv` | Original setting, reproduced setting and reason |
| `docs/AI_USAGE.md` | AI assistance and human verification record |
| `docs/SOURCES.md` | Attribution and upstream licensing obligations |
| `experiments/` | Experiment design and future configurations/scripts |
| `results/logs/` | Actual raw logs once experiments have run |
| `report/` | English report source, ultimately submitted as PDF |
| `presentation/` | Presentation work after separate instructions are obtained |
| `scripts/` | Repository checks and environment capture |
| `.githooks/` | Local commit-identity and staged-file checks |

## Validate the scaffold

Requirements: Git and Python 3.9 or newer.

```sh
python3 scripts/check_repository.py
python3 scripts/capture_environment.py
```

The first command checks tracked files, or scaffold files before Git initialization.
The second prints environment information as JSON without collecting credentials,
usernames, hostnames or environment variables. Inspect its output before saving it.
These commands **do not build or run PERIOD**. There is no validated main
experiment command or runtime estimate yet. Add measured runtimes, expected
outputs and build/run instructions after the first real reproduction run.

## Commits and evidence

Every commit message must contain the actual contributor's student ID and full
name. Use this subject convention:

```text
[STUDENT_ID] Full Name: describe the substantive change
```

The uppercase placeholder above is documentation only and must not be committed
as an actual identity. Each member uses their own GitHub account. See
`CONTRIBUTING.md`. At least one meaningful change must be **pushed during each
week**; local commits and backdated commits cannot repair missed weekly checks.

All reported figures must be traceable to repository logs. Use at least three
runs and report mean ± standard deviation for the measured results required by
the rubric. Distinguish reproducibility checks from claims about statistical
uncertainty; disclose deterministic outputs, failures and timeouts.

The final version must be tagged `v1.0` only when it actually represents the final
submission. Initialization does not create this tag.
