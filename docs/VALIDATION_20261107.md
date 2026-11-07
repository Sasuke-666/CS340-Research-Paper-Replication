# Stage verification — 7 November 2026

## Scope and provenance

The starting remote commit was `89a86e4d9b36409d6551d508b368e34512131176`.
The source snapshot was downloaded from successful workflow run `42371001676`,
artifact `13574015225`. Its outer ZIP SHA-256 is
`eff8c2068064c78db31481ecbc3f71b274e51dcff7e2facfb17333dd9955f976`.
After extraction, the local file tree matched remote tree
`2b3600b866756a439517f65b97954cc023e81ac4` exactly. A synthetic local Git commit
was used only for tests and diffs. It is not the parent of any published change.

The original pilot and follow-up artifact ZIPs were separately downloaded.
Their SHA-256 values match the two published values in the stage report. All
126 raw archived files remain byte-for-byte unchanged in this revision.

## Actual checks performed

- Original baseline: 55 unit tests passed.
- Original evidence verifier: 126 files and 40 command logs passed.
- Independent recount: 18 exploration logs, complete planned condition/repetition
  sets, checksums for all 40 command logs and 15 replay outcomes were checked.
  Pilot and extension means/sample standard deviations agree with the published
  CSV tables. Replay results remain 4/5, 5/5 and 5/5; no failed replay was removed.
- New independent parser tests cover missing findings, duplicate schedule numbers,
  missing completion markers, inconsistent totals and sample standard deviation.
- Output-protection regression: three tests failed on the original wrapper; all
  four output-protection tests pass after the repair. These tests use synthetic
  Docker/Git fixtures and are not new PERIOD measurements.
- Combined local suite: 66 tests passed. Run `make check` and `make audit`.
- The original paper's Table 2, PDF page 9, was visually checked: the two PERIOD
  rows are (first, total, buggy) = (6,27,6) and (9,100,12).

The independent checker imports neither the experiment parser nor its statistics
helper. It retains missing first-failure positions as missing. It compares means
and sample standard deviations using the same defined measurement population.

## Repair

Previously the wrapper used `mkdir -p` and reused an existing output directory.
A repeated command could overwrite logs or combine evidence from different runs.
It now rejects an existing output path, including a symbolic link, and creates
its final output directory atomically. Invalid drivers are rejected before output
creation. The archived experiment results have not been regenerated or rewritten.

## Report exports

`make report` creates an English five-page stage PDF and an editable Word document
from `report/PILOT_REPORT.md`, using the existing two figures. The local exports
were rendered and inspected for table/figure placement and text overflow. The
required AI usage statement is present in the printable report itself. The export
script runs no experiment and alters no observation. Output pagination may vary
between Word installations with different font substitution.

The current tracked source contained no commercial assistant product names in the
reviewed baseline. The required generic AI disclosure is retained. Existing Git
history and scientific evidence are preserved; historical disclosures are not
removed or disguised.

## Remaining work that this verification cannot establish

The other members' identities, their own substantive contributions, independent
human understanding/rerunning, teaching-team access to the private repository,
and the group-registration receipt remain unverified. The separate presentation
instructions and exact final-report deadline have not been supplied. No final
`v1.0` tag or final-submission claim is made. The automated review and actual
student roles are disclosed in `AI_USAGE.md` and `CONTRIBUTIONS.csv`.
