# English final report

The maintained source is [EXPANDED_REPORT.md](EXPANDED_REPORT.md), revised on
**24 November 2026**. Its canonical revision date is [REVISION_DATE](REVISION_DATE).
It extends the earlier [PILOT_REPORT.md](PILOT_REPORT.md), which remains an
unchanged historical report. The current report
includes the five-case matched comparison, original-driver failures, compatibility
repair, replay diagnostics, the earlier single-factor depth study, the separately
audited member-host rerun, the preregistered capacity-layout diagnostic and the
22 November fresh-host engineering acceptance. The final revision incorporates
PR #6's independent six-log twostage recount and presentation review. A complete
setup-deviation table is included in the report. All measurements retain their
actual dates and separate scopes; the new acceptance and secondary review do
not change the historical comparison tables or their denominators. Course
submission follows the instructor's confirmed instructions.

From the repository root:

```sh
python3 -m pip install -r requirements-report.txt
make report
```

Exports are created in `report/export/` as
`CS340_PERIOD_Final_Report_20261124.pdf` and
`CS340_PERIOD_Final_Report_20261124.docx`. The date in each default filename
and footer comes from `REVISION_DATE`; an inconsistent explicit export date is
rejected. Regenerated working copies in `report/export/` are excluded from
Git and are included in the Python 3.12 verification job's downloadable snapshot.
The visually checked final copies are frozen in [submission/](../submission/README.md)
and distributed with `v1.0`.
Use the [repository-checks run](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/workflows/repository-checks.yml)
for the revision being reviewed and compare the downloaded `SNAPSHOT.json`
commit and report revision with that run.
The report includes the required AI usage statement. Figures, tables and references
are preserved. For scientific provenance, use the maintained source, raw manifests,
protocols, `make audit` and the archived workflow runs. The current validation
record is [FINAL_VALIDATION_20261124.md](../docs/FINAL_VALIDATION_20261124.md).
[VALIDATION_20261122.md](../docs/VALIDATION_20261122.md),
[INTEGRATION_20261116.md](../docs/INTEGRATION_20261116.md) and
[VALIDATION_20261114.md](../docs/VALIDATION_20261114.md) retain their historical
scope. The [course requirements](../docs/COURSE_REQUIREMENTS.md) give the
published criteria and unresolved course information; the
[14 November evidence review](../docs/QUALITY_REVIEW_20261114.md) records the
earlier assessment and repairs. Current work and remaining tasks are in
[MEMBER_ACTIONS_ZH.md](../docs/MEMBER_ACTIONS_ZH.md).

The lightweight PDF exporter embeds its fonts and uses the confirmed members'
romanized names; the editable Word file retains their Chinese names. Exporting
that Word file to PDF preserves the Chinese names when the installed document
renderer has the corresponding CJK fonts. Pagination can differ between these
two rendering paths; the scientific content and student IDs are the same.

The final repository handoff is identified by `v1.0`. Check its commit against
the verification run and snapshot before using the exported PDF. The
[final submission checklist](../docs/FINAL_SUBMISSION_CHECKLIST.md) separates
prepared deliverables from the remaining course actions: team/registration
confirmation, the exact deadline and portal, and the separate presentation
instructions. The report records accepted technical work and assistance;
personal explanation, human sign-off, formal submission and actual presentation
must be recorded from events that occur. The final report is submitted in
English as PDF.

The separate Chinese member task list is maintained in
[MEMBER_ACTIONS_ZH.md](../docs/MEMBER_ACTIONS_ZH.md); its Word/PDF copies are for task assignment and do not
replace the English academic report. The editable review template is
[REVIEW_TEMPLATE.md](../docs/reviews/REVIEW_TEMPLATE.md).
