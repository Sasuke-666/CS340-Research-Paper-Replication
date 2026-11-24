# Instructor requirements and final-week scope

Source: instructor-provided CS340 Research Paper Replication, 5 pages,
Academic Year 2026–2027. The earlier supplied copy was checked on 14 November.
All five pages of the supplied `2609_CS340_Research_Paper_Replication(9).pdf`
were read again on 24 November 2026; the requirements below are unchanged.
Page numbers refer to that source. The separately supplied seven-page
`CS340_Operating_Systems_2609_Course Syllabus(20261116-200257).pdf` was also
read. Its page 5 assigns 20% of the course grade to Paper Presentation; it
does not specify how the three project scores below are combined.

The owner confirmed that 23–29 November is the project's final working week.
The group uses Macau/Beijing time (UTC+08:00) for its 24 November closeout.
This is the current work plan. The project's exact final submission time and
the separate Presentation Instruction still require the course source.
See [the final submission map](FINAL_SUBMISSION_CHECKLIST.md) and
[the Chinese submission and defence guide](MEMBER_ACTIONS_ZH.md) for execution.

## Team and submission scope — page 1

- Four members per group; the teaching team assigns additional members to smaller groups.
- Reproduce one paper from the supplied list.
- Team formation: October 25. No exact closing time is stated.
- Paper changes require a TA request by November 1, 2026.
- Presentation: December 1, tentative.
- Submit group information and the reproduction GitHub repository link via the supplied form.
- Registration form: <https://v.wjx.cn/vm/rZCQLSE.aspx>.
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

## Presentation — page 3

The group delivers a final presentation. Its format, structure and assessment
criteria are assigned to the separate Presentation Instruction. Searches of
the accessible supplied files on 24 November did not locate that document or
a later final-submission notice. The five-page project source gives no
presentation duration, slide count, speaking allocation, language, live-demo
requirement or presentation upload format. The group's rehearsal materials
and ten-minute practice plan are internal preparation choices.

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

## Three external facts to confirm for final delivery

1. **Final submission:** the exact report/repository deadline, upload location,
   any required filenames, and the actual submission receipt after uploading.
2. **Presentation:** the separate Presentation Instruction and the confirmed
   date/session, duration and other stated delivery requirements. December 1
   remains the tentative date printed in the supplied project document.
3. **Group registration:** the recorded group/paper/repository registration and
   the teaching team's fourth-member allocation or permission for the three
   confirmed students. [TEAM.csv](TEAM.csv) records the real known members.

The older uncertainty about the registration closing hour and first calendar
date/timezone of weekly checks remains a historical limitation. It does not
prevent final material preparation. The weekly rule is a meaningful group
push each week; substantive own-account contributions are also required from
every member. The source specifies no per-person weekly quota, PR workflow,
oral sign-off file, extra reviewer form or special teaching-team access setup.
The repository is public. Local hooks and internal review procedures are
implementation choices. Keep registration receipts private where they contain
personal information; a minimal verified status is sufficient for this record.
