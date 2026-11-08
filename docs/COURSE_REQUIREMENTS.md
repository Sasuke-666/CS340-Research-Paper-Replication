# Instructor requirements and verification status

Source: `2609_CS340_Research_Paper_Replication(1).pdf`, 5 pages, CS340 Operating
Systems, Academic Year 2026–2027. Page numbers below refer to that PDF.

## Team and submission scope — page 1

- Four members per group; the teaching team assigns additional members to smaller groups.
- Reproduce one paper from the supplied list.
- Team formation: October 25. No exact closing time is stated.
- Paper changes require a TA request by November 1, 2026.
- Presentation: December 1, tentative.
- Submit group information and the reproduction GitHub repository link via the supplied form.
- Final report, presentation and Git history are separately assessed out of 100%.
- The document does not state how those three scores are combined.

## Report — pages 2–3

Write in English. Word or LaTeX is allowed; submit PDF.

| Criterion | Weight | Required evidence |
| --- | --- | --- |
| Reproduction results | 30% | Main-claim experiment; stated reduced scale is allowed; Paper vs. Ours with matching metric/setting; at least three runs; mean ± SD; figures and traceable logs |
| Critical analysis | 30% | Verdict for every tested claim; quantified absolute/relative gaps; evidence from controlled re-runs/checks; limitations |
| Reproduction setup | 15% | 1–3 claims linked to paper figures/tables; upstream starting commit; hardware, OS/kernel, compiler/tools; full deviations table |
| Extension | 15% | Motivated new experiment; one factor changed at a time; interpret against the original claim |
| Writing | 10% | Clear structure; numbered/referenced figures and tables; citations; contribution and AI usage statements |

Claim verdicts: supported, partially supported, not supported, inconclusive.
Overall verdict: reproduced, partially reproduced, not reproduced.

## Git history — pages 3–4

- Weekly checks: every Sunday at 23:59, from the project's first week to the final deadline.
- At least one meaningful commit pushed during that week.
- Whitespace-only and typo-only commits do not count.
- Every commit message includes the contributor's student ID and full name.
- Late pushes count only toward the next week; missed weeks cannot be recovered.

| Criterion | Weight |
| --- | --- |
| Weekly commits | 30% |
| Reproducibility and environment | 25% |
| README and code quality | 25% |
| Individual contributions | 10% |
| Commit quality and repository management | 10% |

A clean machine/VM/container must be able to build and run the main experiment
using only README instructions. Pin the OS/kernel/compiler/tool versions, obtain
workloads with scripts, record consequential settings and avoid hard-coded paths.
README must explain purpose, setup, build/run commands, outputs and runtimes.
Include a Makefile or build script when the experiment is implemented. Credit
original code, retain its license, record its starting commit and modified files.
Every member makes substantive commits from their own account. Use `.gitignore`.
Do not commit build outputs, disk images, large traces, credentials or files
larger than 50 MB. Tag the final version `v1.0`.

## Still unresolved

1. Exact team-registration closing time.
2. First calendar date/timezone of weekly Git checks.
3. Exact final-report/final-repository deadline.
4. Separate Presentation Instruction and its grading details.
5. Required GitHub identities and access method for the teaching team.
6. Fourth member or teaching-team assignment, effective member write access,
   and the registration-form receipt. The owner confirmed the PERIOD selection.
   As verified on 8 November, the known handles are `barkhorn996` (Li Yangshuo)
   and `heboyu0714` (He Boyu), already recorded in `TEAM.csv`; their effective
   permissions at inspection were `write` and `read`, respectively. Invitation
   acceptance must be checked separately from public read access.

The repository is public as requested by the owner. Local hooks are an
implementation choice; the teacher does not require them in the supplied document.
