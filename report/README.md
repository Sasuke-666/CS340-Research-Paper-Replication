# English stage report

The maintained source is `PILOT_REPORT.md`. It reports the completed, reduced-scale
7 November experiments and preserves all recorded exceptions. It is not the final
submission.

From the repository root:

```sh
python3 -m pip install -r requirements-report.txt
make report
```

Exports are created in `report/export/` as
`CS340_PERIOD_Stage_Report_20261107.pdf` and
`CS340_PERIOD_Stage_Report_20261107.docx`. The generated files are excluded from
Git and are included in the Python 3.12 verification job's downloadable snapshot.
The report includes the required AI usage statement. Figures, tables and references
are preserved. For scientific provenance, use the Markdown source, raw manifest,
protocols, `make audit` and the archived workflow runs.

Before final submission, obtain the remaining team details, record genuine individual
contributions and review, complete any additional study needed for the selected
claims, and follow the instructor's separately issued deadlines and presentation
requirements. Submit the final report in English as PDF and only then mark the
actual final repository version `v1.0`.
