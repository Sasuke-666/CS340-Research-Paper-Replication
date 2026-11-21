# Final report traceability audit

**Prepared by:** 李扬烁, student ID 1240001156, GitHub `barkhorn996`

**Audit date:** 22 November 2026, Asia/Shanghai (UTC+08:00)

**Audited revision:** `be8688609e9da8aeb0e1eeaf5a60d115486ed1bf`

**Scope:** source-level traceability of selected final-report tables and figures

This audit introduces no experiment. It checks whether representative report values can be traced from the Markdown table to the generated summary, machine-readable records and raw command logs. It also checks whether numbered tables and figures are explicitly referenced in the report narrative.

## 1. Verification method

The following repository checks were run from a clean checkout of the audited revision:

```sh
make check
make audit
```

`make check` completed all 121 tests and the repository-file validation successfully. `make audit` returned status 0 and verified the main comparison, the compatible-driver recovery, the independent member batch, both capacity batches, member-review hashes and the retained historical evidence.

For each selected result, the audit compared:

1. The value printed in `report/EXPANDED_REPORT.md`.
2. The corresponding group entry or paired comparison in `summary.json`.
3. The per-trial fields in `records.json` or `all_trials.csv`.
4. At least one raw log or a manifest-checked primary record.

## 2. Numerical traceability

### 2.1 Table 4: account schedule reduction

The report states that the account comparison reduced explored schedules by `52.21%` relative to the compatible serialized driver.

Trace:

| Step | Evidence | Value |
| --- | --- | ---: |
| Report | `report/EXPANDED_REPORT.md`, Table 4 | 52.21% |
| Summary | `results/2026-11-07/summaries/comparison-42381922637/summary.json`, account `schedule_reduction_pct` | 52.2058823529412 |
| Pair count | Same summary object | n = 10 |
| Per-trial counts | `results/2026-11-07/comparison-42381922637/account/records.json` | PERIOD 65; serialized 136 in every complete trial |
| Raw logs | `period_r01.txt` and `author_serialized_abi16_r01.txt` driver Round/Total summaries, checked against sequential test records | 65 and 136 explored schedules |
| Calculation | `(136 - 65) / 136 × 100` | 52.20588235294117% |

The report's `52.21%` is the correct two-decimal rounding.

### 2.2 Table 5: account paired elapsed time

The report states a paired whole-driver difference of `25.579 ± 8.536` seconds for serialized minus PERIOD.

Trace:

| Step | Evidence | Value |
| --- | --- | ---: |
| Report | `report/EXPANDED_REPORT.md`, Table 5 | 25.579 ± 8.536 |
| Summary | Primary `summary.json`, account `serial_minus_period_seconds` | 25.5789615377 ± 8.53643350476536 |
| Pair count | Same summary object | n = 10 |
| Per-trial source | Primary `records.json`, `elapsed_seconds` | Ten complete pairs |

The report uses the correct rounding. The metric name also correctly states that time is a paired whole-driver difference, not native target execution time.

### 2.3 Table 8: independent account rerun

The independent batch reports:

| Metric | Report value | Summary value | Result |
| --- | ---: | ---: | --- |
| PERIOD first failure | 8.800 ± 2.044 | 8.8 ± 2.0439612956 | Match after rounding |
| PERIOD schedules | 65.000 ± 0.000 | 65 ± 0 | Match |
| PERIOD buggy schedules | 26.400 ± 0.843 | 26.4 ± 0.8432740427 | Match after rounding |
| PERIOD seconds | 6.855 ± 0.155 | 6.8554669299 ± 0.1551686177 | Match after rounding |
| Serialized first failure | 4.000 ± 0.000 | 4 ± 0 | Match |
| Serialized schedules | 136.000 ± 0.000 | 136 ± 0 | Match |
| Serialized buggy schedules | 55.900 ± 0.316 | 55.9 ± 0.3162277660 | Match after rounding |
| Serialized seconds | 12.167 ± 0.396 | 12.1671447103 ± 0.3959229090 | Match after rounding |

Additional checks:

- The report's paired time difference `5.312 ± 0.377` matches `5.3116777804 ± 0.3771073598`.
- The PERIOD first-failure gap `+6.800` is `8.8 - 2`.
- The relative gap `+340.00%` is `6.8 / 2 × 100`.
- The period buggy-count gap `+0.400` and relative gap `+1.54%` are correct.
- The serialized buggy-count gap `-0.100` and relative gap `-0.18%` are correct.

The raw evidence is in `results/member-reruns/1240001156-account-20261108T122201Z/`. The checked-in `manifest.json` and `make audit` verify its hashes and summary.

### 2.4 Table 11: controlled account capacity results

The report lists:

| Condition | First failure | Schedules | Buggy schedules | Seconds |
| --- | ---: | ---: | ---: | ---: |
| capacity1990 | 10.500 ± 0.850 | 65.000 ± 0.000 | 22.900 ± 3.281 | 23.569 ± 3.547 |
| capacity3964 | 10.200 ± 0.632 | 65.000 ± 0.000 | 24.300 ± 1.767 | 24.639 ± 2.040 |

These values match the group records in:

`results/2026-11-14/summaries/layout-recovery-43575584325-account/summary.json`

The report's A/B first-failure gaps from the paper value 2 are also correct:

- `10.5 - 2 = +8.5`, or `425%`.
- `10.2 - 2 = +8.2`, or `410%`.

The summary retains `n = 10` in each condition and ten complete pairs. The forty readable capacity calls are kept separate from the earlier 106/96/43 comparison accounting.

### 2.5 Table 13: contribution provenance

The account-review row in Table 13 identifies the original independent work as PR #2 and the later supplementary review as PR #3. It does not assign ownership of the group's 7 November or 14 November measurements to this member.

The current main history contains the corresponding original commits and merge commits:

- Original independent account work: `8ce522d`, `9f30843`.
- Supplementary evidence review: `94a35c3`, `d907517`.
- Main integrations: `c35bd0e`, `9bb7e6c`.

The contribution wording is consistent with those commit boundaries.

## 3. Table and figure citation audit

The course requirements ask for numbered figures and tables that are referenced in the report text. The audited revision had captions for every numbered table and figure, but several items lacked a nearby narrative callout rather than relying on the caption alone.

This PR adds concise narrative references for:

- Figures 1, 2, 3 and 4.
- Tables 6, 7, 8, 10, 11, 12, 13 and A1.

No numerical value, table row, figure source, sample denominator or interpretation was changed by these additions.

## 4. Findings

### Numerical findings

No numerical mismatch was found in the four selected quantitative checks:

- Table 4 account reduction.
- Table 5 account paired elapsed time.
- Table 8 independent-host account statistics and paper gaps.
- Table 11 controlled capacity statistics and paired changes.

### Provenance findings

No provenance error was found in the audited contribution row. The report distinguishes the independent member measurements from the later secondary audit.

### Reporting-language findings

The report continues to use appropriately limited language:

- Schedule-count agreement is not equated with full replication.
- A buggy schedule is not described as a distinct defect.
- Whole-driver time is not described as native target execution time.
- First-failure position is not described as time to failure.
- Host-dependent timing and failure differences are not assigned to one cause.
- The adapted serialized driver is not claimed to be identical to the paper's historical Serial executable.

## 5. Changes submitted by this audit

1. Added this traceability record.
2. Added explicit narrative callouts for the tables and figures identified above in `report/EXPANDED_REPORT.md`.
3. Made no experimental, statistical or environmental changes.

## 6. Export verification

After the narrative callouts were added, the report exporter completed successfully and produced:

- `report/export/CS340_PERIOD_Expanded_Report_20261116.docx`
- `report/export/CS340_PERIOD_Expanded_Report_20261116.pdf`

The generated PDF has 17 A4 pages, uses `595.28 × 841.89` points on every page, contains 52,120 extracted text characters and has no blank pages. It embeds four images on four different pages, matching the four numbered figures in the source. The PDF text contains the explicit callouts for Figures 1–4 and Tables 6, 7, 8, 10, 11, 12, 13 and A1; the Table 7 callout wraps across a line in the rendered document but remains present.

The PDF was also rendered to page images to exercise the rendering pipeline. Final human visual review of the official submission export remains required because the course presentation format may still change.

## 7. Limitations

This audit samples representative values rather than retyping or rechecking every number in every table. The repository-wide automated audits cover all retained evidence and generated summaries. Visual judgment of typography and figure legibility is not replaced by these structural checks.

Completed by: 李扬烁, 22 November 2026.

## Maintainer integration note, 22 November 2026

PR #5 was merged in `7ba2d8f966fcaa1dd13e32d5cc4ee662df59d340` with the original member commit preserved. The raw-log locator in section 2.1 was clarified during integration: schedule totals occur in the driver summaries and test records. Wrapper footers record process status and elapsed time. This correction changes no measurement or original audit date.
