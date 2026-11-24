# Final submission documents

Revision: 24 November 2026. The `v1.0.1` release contains these six reviewed files:

| File | Use |
| --- | --- |
| [English report PDF](CS340_PERIOD_Final_Report_20261124.pdf) | Required report submission format |
| [Editable report](CS340_PERIOD_Final_Report_20261124.docx) | Editable Word copy with the same scientific content |
| [Editable presentation](CS340_PERIOD_Final_Presentation_20261124.pptx) | Fourteen English slides with Chinese speaker notes, native tables and chart |
| [Presentation PDF](CS340_PERIOD_Final_Presentation_20261124.pdf) | Portable slide preview and offline fallback |
| [Chinese submission handbook](CS340_Final_Submission_Handbook_20261124.docx) | Editable submission, member preparation and defence guide |
| [Handbook PDF](CS340_Final_Submission_Handbook_20261124.pdf) | Portable copy of the guide |

The [release page](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/releases/tag/v1.0.1)
also supplies one ZIP with all six documents and the complete tracked repository,
including protocols, failed/censored outcomes and raw evidence. Git metadata,
credentials and compiled benchmark outputs are excluded. `DELIVERY.json` in the
bundle identifies its repository commit and the document hashes.

`FINAL_RELEASE.json` records each document's SHA-256 hash and the source commit
used to produce it. From a checkout, verify the files and build the bundle with:

```sh
python3 scripts/check_final_submission.py
python3 scripts/package_final_submission.py --output /tmp/CS340_Final_Deliverables_20261124.zip
```

This revision improves the report's prose, the slide wording and the Chinese
speaking notes. Tables, experimental results and the scientific conclusion are
unchanged. The initial [v1.0 release](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/releases/tag/v1.0)
remains available.

Readable sources are in `report/`, `presentation/` and `docs/`. Regenerating the
reports creates working copies in `report/export/`; timestamps and evidence
links can differ if exported at another commit. Use the files above for the
reviewed version. The report includes the course-required assistance statement
and credits the original authors.

Publication follows successful Linux Python and Windows archive checks. Existing
tags and published files cannot be replaced by this workflow. The
[validation record](../docs/FINAL_VALIDATION_20261124.md) documents the checks,
and the [rubric map](../docs/FINAL_SUBMISSION_CHECKLIST.md) links the course
criteria to the submitted work.
