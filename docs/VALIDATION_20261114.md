# Third-week verification receipt — 14 November 2026

This receipt records observed checks and distinguishes evidence integrity from
experimental success. Dates are Macau/Beijing local time unless marked UTC.
The starting repository revision was
`0dc19a89cfe82439ebffa78e8f8bdd6c2201f7bb`. The new experiment was registered in
`bddb831319679c30586d9bbe689fb11b897f1a14` before its first workload execution.

## 1. Scientific scope and immutable history

The original compatible comparisons retain 106 attempts, 96 complete calls,
ten censored calls and 43 matched pairs across separately scoped batches. The
member's WSL2 `account` batch retains 20 complete calls and ten pairs. Neither
is replaced by the third-week experiment. Original failures, partial attempts,
replay exceptions, member authors and commit dates remain intact.

The [layout protocol](../experiments/2026-11-14/LAYOUT_PROTOCOL.md) specifies
two cases, ten AB/BA pairs per case, one driver-capacity declaration changed,
unchanged native runtime/benchmark, fresh private IPC state for both arms,
depth 3, budget 10,000 and a 120-second outer limit. The
[study workflow](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/43570556202)
is also dated evidence of a substantive push in the 9–15 November week.

## 2. Verification commands and interpretation

Run from the repository root:

```sh
make check
make audit
make audit-member
make audit-layout
git diff --check
```

`make check` completed 111 synthetic regression tests and the repository file
rules check. Thirteen new tests cover the capacity-only source intervention,
native layout extraction, state controls and independent layout evidence audit.
They include wrong or missing condition records, manifest/log corruption,
changed source or binary hashes, live IPC attachments, CRLF source bytes,
censored prefixes, the driver's unexecuted budget-limit label and published
summary consistency. Synthetic tests never enter experimental statistics.

The local 111-test run was repeated successfully after the summary auditor
was hardened for terminated schedule-output payloads. The synthetic fixtures
remain separate from measured data.

The member audit reconstructs the ten-pair design and all metrics from the
original logs, validates 880 manifest entries and checks the maintained summary
without rewriting it. The default audit and both continuous-check Python
versions now include this batch and the new layout study.

The original layout workflow archived the lazy01 case. Its case-specific
summary validates 304 outer-manifest entries and 300 case-manifest entries,
with 20 complete eligible calls and ten pairs. Its separate raw and summary
scopes are maintained in `make audit-layout`. Original account evidence loss
and the subsequently registered recovery are recorded in
[the final availability observation](../experiments/2026-11-14/account-evidence-failure/FINAL_OBSERVATION.json)
and [recovery protocol](../experiments/2026-11-14/ACCOUNT_RECOVERY_PROTOCOL.md).
The unavailable original account actual count remains unknown.

The separate account recovery completed successfully. Its independently checked
summary validates 571 outer-manifest entries and 557 case-manifest entries,
20 complete eligible calls and ten pairs. All four archived measurement
wrapper/helper files match their exact `bddb831` originals, and the actual
measurement-runner copy matches too. The two readable scopes contain 215
lazy01 and 472 account target-assertion witness files. Both have no recorded
inner/outer timeout, budget censoring or other error type. Every paired
requested sequence matches within its case. The
[recovery run](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/43575584325)
finished successfully at 08:32:48 UTC, after Git archive commit `8fbc34d` and
successful backup upload.

The recovery registration's
[remote repository checks](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/43575584256)
passed on `ea273fe4b6e49bd1f8f5c5b7c964c02aaf22d144`. That revision predates the
final independent-summary additions; this is a specifically scoped earlier
remote check, not a claim about an untested later revision.

The final local `make check`, `make audit` and `git diff --check` all completed
with exit status zero after both formal layout summaries were produced. The
full audit includes all maintained historical comparison summaries, failed-setup
manifests, the member rerun and both new case scopes. Later workflow maintenance
adds an eight-minute limit to the Git publication step; the already completed
recovery remains tied to its originally registered workflow revision. No
measurement source, sample, raw log or historical result was changed by that
transport-only safeguard.

## 3. Report and course-evidence closure

The revised English report contains the paper-linked C1/C2 verdicts, original
paper-versus-observed tables, the depth extension, an independent-host section,
the new diagnostic and a complete setup-deviation table in Appendix A.
Contributions and the required generic assistance statement reflect the dated
submissions. See the [criteria mapping](QUALITY_REVIEW_20261114.md) and
[actual contribution record](CONTRIBUTIONS.csv).

The [member checklist](MEMBER_ACTIONS_ZH.md) credits completed work and identifies
the course-information items requiring actual confirmation. The
[talk outline](../presentation/TALK_OUTLINE.md) gives a source-backed explanation,
demonstration sequence and likely questions. No presentation duration, final
deadline or fourth member is invented.

The delivered English PDF has 16 pages and the Word export renders to 14
pages. Every page was visually inspected; the larger-font Figure 4 was checked
again after its final revision. Tables 10–12, all four figures, the continued
deviation table and reference hyperlinks are readable. Numeric report tables
were checked against the independently audited JSON, including every sample
size, paired difference and absolute/relative paper gap.

The editable English rehearsal presentation contains twelve slides, seven
native tables, two native charts with two embedded workbooks, and Chinese
speaker notes with sources on all twelve slides. All slides were rendered by
an independent office renderer and visually checked. The package, embedded
workbooks and metadata passed recursive XML/ZIP integrity and terminology
checks. The three-page Chinese member checklist was also rendered and checked;
its numbered actions remain separate paragraphs and its source links are
clickable. These delivered files are dated preparation materials, not a claim
that the instructor's separate presentation rubric or member rehearsal is
already complete.

The final relative-link audit checked 34 Markdown files, including 159 relative
references resolving to 63 unique local targets, with no missing target or
fragment errors. These checks use the final source documents and preserve the
archived raw measurements.

## 4. Current terminology and historical scope

A byte-level check of current maintained files and all three remote branch
heads found no specific assistance-product names. The required generic usage
statement remains. Old reachable history contains two commit messages and
three distinct earlier file blobs with historical product wording. Those
objects retain their original identities and dates; the current-tree check
does not claim that old history was erased. Member commits and weekly push
evidence remain available.

## 5. Limits of this receipt

Automated checks establish the stated file, arithmetic and procedural properties.
They do not certify personal understanding, a student's independent authorship,
oral presentation quality or an instructor's grade. Final `v1.0` tagging and
submission remain tied to the actual final version and verified course details.
