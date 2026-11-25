# Instructor requirements and final-week scope

The page references below follow the team's dated reading of the five-page
`2609_CS340_Research_Paper_Replication(9).pdf` (24 November 2026, academic
year 2026–2027) and its earlier review of the seven-page
`CS340_Operating_Systems_2609_Course Syllabus(20261116-200257).pdf`.
The syllabus review records a 20% course weight for Paper Presentation on
page 5. The group has no published weighting for combining the report,
presentation and Git scores. The two original PDFs were not available for
direct inspection in the 25 November Mac handover. The rubric below retains
the team's prior reading and its page references.

On 25 November the group leader relayed the instructor's confirmation that
孙皓扬, 李扬烁 and 何博宇 constitute the complete group. Their IDs and GitHub
accounts are in the [roster](TEAM.csv). The leader designated 23–29 November
as the final working week, using Macau/Beijing time (UTC+08:00). The group
registration receipt, final upload arrangements and presentation notice are
tracked separately in the [submission map](FINAL_SUBMISSION_CHECKLIST.md).

## Team and submission scope — page 1

- The original handout specified four students per group and allocation by
  the teaching team for smaller groups. The instructor's subsequent decision
  for this group, as relayed by the leader, is the three-person roster above.
- Reproduce one paper from the supplied list.
- Team formation was set for 25 October. The handout gave no closing hour.
- Paper changes required a TA request by 1 November 2026.
- The presentation date in the handout was **1 December, tentative**.
- Submit group details and the reproduction repository via the [registration form](https://v.wjx.cn/vm/rZCQLSE.aspx). On 25 November the publicly readable form displayed its title, “课堂小组信息及复现GitHub链接收集问卷”, and the closed status “此问卷处于停止状态，无法作答！” The page supplied neither a closing time nor a receipt for this group.
- The final report, presentation and Git history are separately assessed out of 100%.

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
3. **Group registration:** the receipt or course record showing submission of
   the three members, selected paper and repository. A private receipt may be
   retained by the leader. The instructor's grouping decision is recorded above.

The handout gave no registration closing hour, timezone for weekly checks or
first exact check date. [Weekly progress](WEEKLY_PROGRESS.md) identifies server
evidence by date. The weekly requirement is one meaningful push by the group.
Each member separately needs substantive work from their own account. Internal
rehearsal, review templates and local hooks support the project without creating
additional grading rules.
