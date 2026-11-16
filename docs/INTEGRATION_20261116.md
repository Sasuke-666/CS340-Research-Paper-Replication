# Member submission closeout — 16 November 2026

## Decision and preserved ownership

The repository owner authorized this closeout after review of the two submitted
heads. PR #4 was merged in `94d0e9b4d16a4cd1907c440f47bcf8242d2c7a72`; PR #3
was merged in `9bb7e6c7d561eafe30d10d01f545c10105d48601`. Both are ordinary
merge commits, retaining all original member commits and authors.

| Member | Accepted scope | Original submissions |
| --- | --- | --- |
| Li Yangshuo / 1240001156 / barkhorn996 | Supplementary account evidence review, cross-batch analysis and provenance clarification; no new measurements or ownership of prior group capacity work | PR #3; `94a35c3`, `d907517`; earlier independent 20-call experiment remains credited through PR #2 |
| He Boyu / 1240000576 / heboyu0714 | Twostage source mechanism, trace evidence table, five fresh fixed-witness replays, verification scripts and Chinese summary | PR #4; `62cbb795`, `6f186ddc`, `c78fd1c`; original run `43681034375` on 15 November |

The author's `new in PR #3` label identifies additional analytical material in
that PR. It does not establish that the scientific observation first originated
there. Prior source, measurements and interpretation retain their attribution.
The five twostage calls are separate from the earlier 106 attempts, 96 complete
explorations and 43 matched pairs; no denominator or historic statistic is changed.
The raw results under `results/` are unchanged by this integration.

## Maintainer changes

README navigation, roster roles, the contribution ledger, weekly progress,
current report and usage disclosures now include the accepted submissions.
The report includes the new witness's actual hardware, wrapper limit and limits
of interpretation; the core verdict remains partially reproduced. Earlier task
suggestions are explicitly marked as historical so accepted work is not reassigned.

The owner-requested integration adds `scripts/audit_member_reviews.py` and ten
synthetic regression tests. This is maintainer verification work, not new student
measurements. The original member runner and classifier remain unchanged.

```sh
make check
make audit
make audit-member-reviews
make report
```

The strict offline check reconstructs the account sequence hashes by stripping
ANSI codes, retaining complete numbered test lines in order, trimming line-end
whitespace, and joining them with LF without a final LF. Both existing batches
supply ten repetitions for each driver: 40 checksummed logs in total. It also
verifies all 12 replay-file checksum entries and requires each of five completed
calls to contain the line-48 funcB assertion after the reproduction marker.
A matching wrapper exit alone is insufficient. Missing assertions, timeouts,
missing checksum coverage and corrupted bytes produce a nonzero exit. Negative
test fixtures are synthetic and excluded from every experimental result.

These checks are included in `make audit` and the Python 3.9/3.12 continuous
checks. `make report` and the export job use revision date 16 November 2026.
Generated files are not tracked; the verification job packages them with source
and evidence as `CS340_Progress_20261116.zip`.

## Dates and boundaries

Member submissions occurred on 14–15 November. Integration occurred on
16 November, with real commit timestamps. No history is rewritten, no force
push is used, and no final `v1.0` tag is created. This maintenance cannot be
backdated to a previous weekly check.

Technical deliverables are accepted within the reviewed evidence scope. Personal
oral explanation, unrecorded human sign-off, the fourth-member arrangement,
registration receipt and final course submission remain outside this closeout.
Required assistance disclosures are retained using generic terminology. This
record does not certify a course grade or another student's personal understanding.

## Local integration verification

The combined pre-edit file tree matched remote merged-main tree
`18c05686e6c8529bc274dd2f49dee34da62958e2` exactly. After the integration edits,
121 unit tests, repository checks and `make audit` completed successfully.
The audit includes both accepted member-review scopes. These are offline checks;
no new target execution or binary rebuild was performed for this closeout.
Final remote checks and exported snapshots are recorded by the corresponding
Repository checks workflow on the published main commit.
