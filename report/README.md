# English final report

[EXPANDED_REPORT.md](EXPANDED_REPORT.md) is the current report, revised on
25 November 2026. The reviewed PDF and editable Word copy are in
[submission/](../submission/README.md). Release `v1.0.2` records PRs #7 and #8 and the final validation repairs.
Experimental measurements, numerical result tables and scientific conclusions
retain their original scope. The `v1.0` and `v1.0.1` releases and [PILOT_REPORT.md](PILOT_REPORT.md)
remain available as earlier versions.

## Read the report

The report follows two questions: how closely the selected PERIOD results match
the paper, and how its search compares with the released serialized driver.
It then examines the original-driver failure, censored runs and variable failure
observations. The depth-bound extension, independent member-host rerun, controlled
capacity diagnostic and 22 November acceptance each have their own samples and
host records. Appendix A collects the setup differences. The final sections
record contributions, references and the required usage statement.

Use the [final submission checklist](../docs/FINAL_SUBMISSION_CHECKLIST.md) to
match the evidence to the course criteria. The [validation record](../docs/FINAL_VALIDATION_20261125.md)
documents this integration. Earlier checks remain in
[24 November final validation](../docs/FINAL_VALIDATION_20261124.md),
[22 November validation](../docs/VALIDATION_20261122.md),
[16 November integration](../docs/INTEGRATION_20261116.md),
[14 November validation](../docs/VALIDATION_20261114.md) and
[the 14 November evidence review](../docs/QUALITY_REVIEW_20261114.md).

## Regenerate PDF and Word

From the repository root:

```sh
python3 -m pip install -r requirements-report.txt
make report
```

The exporter writes these working copies to `report/export/`:

- `CS340_PERIOD_Final_Report_20261125.pdf`
- `CS340_PERIOD_Final_Report_20261125.docx`

[REVISION_DATE](REVISION_DATE) controls the default filenames and footer date;
an explicit date that disagrees with it is rejected. Working exports are ignored
by Git. The Python 3.12 [repository-checks job](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/workflows/repository-checks.yml)
includes them in its downloadable snapshot. `SNAPSHOT.json` identifies the commit
and report revision, so use the run for the version being reviewed. The frozen
files in `submission/` are the copies checked for delivery.

The PDF exporter embeds its fonts and uses the members' confirmed romanized
names. Word retains their Chinese names. Converting Word to PDF also preserves
those names when the renderer has the required CJK fonts. The two paths can
paginate differently; their scientific content and student IDs are the same.

For reproduction and numerical checks, start with the repository README,
registered protocols, raw manifests and `make audit`. Report formatting alone
does not verify a result.

## Prepare the submission

The course requires the report in English as a PDF. Confirm the exact deadline,
portal and any naming rule from the course notice, then retain the upload receipt.
The [course requirements](../docs/COURSE_REQUIREMENTS.md) and
[Chinese member handbook](../docs/MEMBER_ACTIONS_ZH.md) list the remaining group
registration and presentation arrangements. The handbook supports task assignment
and rehearsal; the English report is the academic submission. An editable
[review template](../docs/reviews/REVIEW_TEMPLATE.md) is also available.
