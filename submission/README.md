# Final submission documents

Revision: 24 November 2026. The `v1.0` release contains these six frozen files:

| File | Use |
| --- | --- |
| [English report PDF](CS340_PERIOD_Final_Report_20261124.pdf) | Required report submission format |
| [Editable report](CS340_PERIOD_Final_Report_20261124.docx) | Editable Word copy with the same scientific content |
| [Editable presentation](CS340_PERIOD_Final_Presentation_20261124.pptx) | Fourteen English slides with Chinese speaker notes, native tables and chart |
| [Presentation PDF](CS340_PERIOD_Final_Presentation_20261124.pdf) | Portable slide preview and offline fallback |
| [Chinese submission handbook](CS340_Final_Submission_Handbook_20261124.docx) | Editable submission, member preparation and defence guide |
| [Handbook PDF](CS340_Final_Submission_Handbook_20261124.pdf) | Portable copy of the guide |

The [release page](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/releases/tag/v1.0)
also supplies one ZIP with all six documents and the complete tracked repository,
including protocols, failed/censored outcomes and raw evidence. Git metadata,
credentials and compiled benchmark outputs are excluded. `DELIVERY.json` in the
bundle identifies its repository commit and the document hashes.

The manifest `FINAL_RELEASE.json` binds final document bytes to the exact source
revision. From a checkout, verify it with:

```sh
python3 scripts/check_final_submission.py
python3 scripts/package_final_submission.py --output /tmp/CS340_Final_Deliverables_20261124.zip
```

Regenerated reports in `report/export/` are working copies; metadata timestamps
and repository links can differ when generated at another commit. The frozen
files above are the reviewed delivery. Their readable sources remain in
`report/`, `presentation/` and `docs/`. The final documents preserve the generic
assistance statement required by the course and the original authors' credit.

The release gate runs only after both Linux Python checks and the Windows archive
check succeed. It refuses to move an existing `v1.0` tag. Actual validation is
recorded in [the final validation record](../docs/FINAL_VALIDATION_20261124.md).
The [rubric map](../docs/FINAL_SUBMISSION_CHECKLIST.md) separates completed
technical work from course-platform submission, actual presentation and the
remaining course information.
