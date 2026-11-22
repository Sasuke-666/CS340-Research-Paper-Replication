# English stage report

The maintained source is [EXPANDED_REPORT.md](EXPANDED_REPORT.md), revised on
**22 November 2026**. Its canonical revision date is [REVISION_DATE](REVISION_DATE).
It extends the earlier [PILOT_REPORT.md](PILOT_REPORT.md), which remains an
unchanged historical report. The current report
includes the five-case matched comparison, original-driver failures, compatibility
repair, replay diagnostics, the earlier single-factor depth study, the separately
audited member-host rerun, and the preregistered capacity-layout diagnostic. A
complete setup-deviation table is included in the report itself. It is a
stage report incorporating the 16 November member integration and the
22 November report traceability audit, with all measurements retaining their
actual dates and separate scopes. Final submission follows the instructor's
confirmed submission instructions.

From the repository root:

```sh
python3 -m pip install -r requirements-report.txt
make report
```

Exports are created in `report/export/` as
`CS340_PERIOD_Expanded_Report_20261122.pdf` and
`CS340_PERIOD_Expanded_Report_20261122.docx`. The date in each default filename
and footer comes from `REVISION_DATE`; an inconsistent explicit export date is
rejected. The generated files are excluded from
Git and are included in the Python 3.12 verification job's downloadable snapshot.
Use the [repository-checks run](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/workflows/repository-checks.yml)
for the revision being reviewed and compare the downloaded `SNAPSHOT.json`
commit and report revision with that run.
The report includes the required AI usage statement. Figures, tables and references
are preserved. For scientific provenance, use the maintained source, raw manifests,
protocols, `make audit` and the archived workflow runs. The current validation
record is [VALIDATION_20261122.md](../docs/VALIDATION_20261122.md).
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

Before final submission, confirm the remaining team and registration details,
deadline, submission portal and separate presentation instructions. The current
report and contribution records identify the accepted work and its evidence.
Any further study should address a specific unresolved question under a recorded
design. Submit the verified final report in English as PDF and tag the actual
final repository version `v1.0`.

The separate Chinese member task list is maintained in
[MEMBER_ACTIONS_ZH.md](../docs/MEMBER_ACTIONS_ZH.md); its Word/PDF copies are for task assignment and do not
replace the English academic report. The editable review template is
[REVIEW_TEMPLATE.md](../docs/reviews/REVIEW_TEMPLATE.md).
