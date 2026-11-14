# English stage report

The maintained source is `EXPANDED_REPORT.md`. It extends the earlier
`PILOT_REPORT.md`, which remains an unchanged historical report. The new report
includes the five-case matched comparison, original-driver failures, compatibility
repair, replay diagnostics, the earlier single-factor depth study, the separately
audited member-host rerun, and the preregistered capacity-layout diagnostic. A
complete setup-deviation table is included in the report itself. It is a
stage report; final submission requires actual group review and the instructor's
final instructions.

From the repository root:

```sh
python3 -m pip install -r requirements-report.txt
make report
```

Exports are created in `report/export/` as
`CS340_PERIOD_Expanded_Report_20261114.pdf` and
`CS340_PERIOD_Expanded_Report_20261114.docx`. The generated files are excluded from
Git and are included in the Python 3.12 verification job's downloadable snapshot.
The report includes the required AI usage statement. Figures, tables and references
are preserved. For scientific provenance, use the maintained source, raw manifests,
protocols, `make audit` and the archived workflow runs. The dated verification
receipt is `docs/VALIDATION_20261114.md`; the course-criteria mapping is
`docs/QUALITY_REVIEW_20261114.md`.

The lightweight PDF exporter embeds its fonts and uses the confirmed members'
romanized names; the editable Word file retains their Chinese names. Exporting
that Word file to PDF preserves the Chinese names when the installed document
renderer has the corresponding CJK fonts. Pagination can differ between these
two rendering paths; the scientific content and student IDs are the same.

Before final submission, obtain the remaining team details, record genuine individual
contributions and review, complete any additional study needed for the selected
claims, and follow the instructor's separately issued deadlines and presentation
requirements. Submit the final report in English as PDF and only then mark the
actual final repository version `v1.0`.

The separate Chinese member task list is maintained in
`docs/MEMBER_ACTIONS_ZH.md`; its Word/PDF copies are for task assignment and do not
replace the English academic report. The editable review template is
`docs/reviews/REVIEW_TEMPLATE.md`.
