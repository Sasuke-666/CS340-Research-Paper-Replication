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
| 2026-11-08 | Prepared a disposable Ubuntu WSL2 and Docker environment, completed the `account` comparison with ten repetitions per method, preserved the failed image-pull attempt and all successful raw logs, independently audited the summary, and drafted the member review | `docs/reviews/1240001156-clean-run.md`; `results/member-reruns/1240001156-account-20261108T122201Z`; network-failure attempt `1240001156-account-20261108T113548Z` | Requested by member Li Yangshuo and submitted through that member's account. Personal explanation and cross-review remain pending. |
| 2026-11-08, four-thread member review | Recounted archived logs and drafted the four-thread evidence review at the member's request | `docs/reviews/1240000576-evidence-audit.md`; member commit `b02adef5d66f6dd3cee6c6215338ac0792d9bb0f` | Submitted through He Boyu's own account. Personal explanation and sign-off remain unrecorded. |
| 2026-11-08, repository integration | Verified submitted evidence, corrected two source references and overstrong causal wording, integrated member PRs, reconciled contribution records and used generic assistance terminology | PRs #1 and #2; `docs/CONTRIBUTIONS.csv`; `docs/WEEKLY_PROGRESS.md` | Owner authorized integration. Original member authors and commits are preserved; this automated check is not a new member experiment or a claim of human sign-off. |
| 2026-11-14, controlled diagnostic and report revision | Prepared and published the capacity-only protocol and runner, initiated the registered hosted study, independently recounted raw evidence, added member-batch verification, revised the report and complete deviations table, prepared the editable rehearsal presentation, registered a separately scoped recovery after the original account evidence was unavailable, and exported revised documents | Registrations `bddb831` and `ea273fe4`; workflows `43570556202` and `43575584325`; `experiments/2026-11-14`; run-specific results; `docs/VALIDATION_20261114.md` | Owner requested current-stage completion and stronger quality. All observed failures and incomplete calls remain reported. This work does not certify another member's independent execution, personal explanation or human approval. |

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
