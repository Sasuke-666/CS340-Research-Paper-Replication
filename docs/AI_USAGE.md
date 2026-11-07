# AI usage statement and verification record

This project used an AI assistant for repository scaffolding, code generation,
experiment planning, execution through development tools, log analysis and draft
technical writing. This statement is retained for the course's required AI
usage disclosure. The original paper and its authors' implementation are cited
separately; their work is not attributed to the group.

| Date | Assistance used | Evidence / affected work | Human contribution and review status |
| --- | --- | --- | --- |
| 2026-10-24 | Prepared project structure, documentation and local checks; assisted repository initialization | Initial commit 1829541 and its files | Owner supplied identity and authorized creation. Independent code review is not recorded. |
| 2026-10-30 | Wrote regression tests, repaired repository-checking defects and prepared continuous checks | Commit 99ec61a; docs/REPOSITORY_CHECKS.md and retained before/after logs | Owner specified and authorized the task. Independent human review remains unrecorded. |
| 2026-11-07 | Prepared the PERIOD protocols and wrappers; initiated hosted experiments; inspected actual logs; computed statistics and drafted the report | Commits bf5e6de and 5970167; experiments/2026-11-07; results/2026-11-07; report/PILOT_REPORT.md | Owner confirmed the selected paper and requested implementation. Group review, explanation and independent rerunning are still required. |
| 2026-11-07, second verification | Independently recounted original logs, reproduced and repaired an evidence-output overwrite risk, added regression tests and exported the existing stage report to PDF/Word | scripts/audit_period_results.py; tests/test_period_output.py; docs/VALIDATION_20261107.md; scripts/export_stage_report.py | Owner requested the work. This automated verification does not replace individual group review or rerunning. |
| 2026-11-07, expanded study | Registered five-case comparisons; diagnosed original serialized-driver IPC failure; prepared a minimal compatibility copy; executed repeated comparisons, a predeclared censored-run completion check, and controlled replay studies; independently audited logs; drafted expanded analysis and a separate member checklist | Comparison protocols, run-specific archives, `report/EXPANDED_REPORT.md`, `docs/MEMBER_ACTIONS_ZH.md` | Requested by the owner. Suggested member assignments are not completed contributions; independent rerun and human review remain pending. |

Experimental measurements come from the archived process output, not invented
values. Automation-generated tests use explicitly synthetic fixtures; those
fixtures are not research observations. The group must check the interpretation,
understand the code and record actual review dates and reviewers before final
submission. No statement here asserts that another member personally executed,
independently authored, or approved work without evidence.

Repository commits made through the owner's authenticated connection identify
that account and the course-required student name/ID. Automated archive commits
identify the automation account and name the requesting owner in the subject;
they must not be counted as another student's independent contribution.

No history was rewritten to remove earlier disclosures. This concise statement
replaces repetitive tool-specific narration in the current document. Exact
historical assistance details and logs remain available in Git history. Any
additional disclosure requested by the instructor takes precedence over this
summary. No final report, final presentation or completed human review is implied.
