# Expanded-study validation — 7 November 2026

This record covers the published expanded analysis and the evidence already
archived by the registered workflows. It records automated checks and document
inspection; it does not assert that a group member has independently rerun or
approved the study.

## Executed checks

| Check | Observed outcome | Preserved evidence |
| --- | --- | --- |
| `python3 -m unittest discover -s tests -q` | 98 tests passed; exit status 0 | [Test output](validation/expanded-20261107/tests.txt) |
| `make audit` | Completed with exit status 0, including archive hashes, raw-log recounts and comparison-summary consistency | [Full audit output](validation/expanded-20261107/evidence-audit.txt) |
| Isolated System V shared-memory reproduction | The larger original-driver request failed with `EINVAL`; the unchecked invalid attachment was demonstrated without accessing the experiment runtime's shared-memory key | [Recorded probe](validation/expanded-20261107/isolated-ipc-reproduction.json), [probe script](../scripts/probe_serial_ipc.py) |
| Complete printed enumeration sequences | Identical printed enumeration lists within each eligible method/case/batch; this does not measure realized runtime event order | [Enumeration audit](../results/2026-11-07/summaries/comparison-42381922637/enumeration_audit.json) |

The comparison summarizer independently checks manifests, command records,
terminal driver summaries, actual sample counts and method labels. It excludes
ineligible observations from completed-run statistics while retaining every
attempt in its exported trial table. Regression tests include censored runs,
missing measurements, incorrect first-failure parsing, corrupt provenance and
the accidental inheritance of a previous invocation's witness files.

## Reconciled denominators

| Evidence | Attempts and interpretation |
| --- | --- |
| Original-driver comparison, `42380929383` | 50 complete PERIOD explorations and 50 original serialized-driver crashes; no complete method pairs. Its 40 replay diagnostics and five builds are separate. |
| Compatible-driver primary study, `42381922637` | 100 attempts: 90 complete and ten outer-timeout censored. Four cases provide 40 complete pairs; the ten complete primary PERIOD four-thread calls have no complete same-batch serialized partners. |
| Registered four-thread follow-up, `42384122902` | Six complete calls, three complete pairs, at a 240-second outer limit. Its host and measurements are kept separate from the primary study. |
| Combined compatible-study accounting | 106 attempts, 96 complete calls and ten censored calls. The matched analysis uses 43 complete pairs: 40 primary pairs and three follow-up pairs. |

The historical pilot, depth extension and saved-witness experiments retain
their own protocols and denominators. Startup failures and the partial
method-selection attempt are preserved and are not pooled with completed
comparisons. The ten censored observations retain their raw prefixes; 120
seconds is a censoring limit rather than an observed completion time.

## Interpretation checks

- The report distinguishes explored schedules, first failing schedule and
  buggy schedules. Buggy schedules are not counts of distinct software defects.
- Means use eligible observations; dispersion uses sample standard deviation.
  Each table states its actual sample size and the applicable evidence batch.
- The released serialized driver required a documented IPC adaptation. Its
  label is `author_serialized_abi16`; correspondence with the paper's historical
  Serial implementation remains a limitation.
- The compatible scheduler explores fewer schedules in four cases and the same
  number in `twostage`. Neither first-failure results nor whole-driver timing
  establish a universal superiority claim.
- Whole-driver timing includes calibration and reporting. Timing comparisons
  remain paired within one case and host batch.
- Later replay diagnostics observed 20/20 hits under each multiplier in each
  diagnostic batch. They do not explain the earlier 4/5 result or demonstrate
  deterministic replay across arbitrary machines.

## Document inspection

The eight-page English Word rendering and five-page Chinese checklist were
inspected page by page. The supplied English PDF uses the corresponding
eight-page Word-to-PDF rendering, preserving the confirmed Chinese names.
The lightweight reproducible exporter was also repaired to embed its fonts;
its eleven-page English PDF was inspected page by page. Tables, figures,
captions and page numbering were intact in the final renderings. The two
English renderers have different pagination but the same scientific content.

## Member verification still required

The [separate member checklist](MEMBER_ACTIONS_ZH.md) assigns a proposed
independent clean-environment rerun, a raw-evidence review and the administrative
checks. Each member must record actual execution, findings and their own
contribution. No member review has been filled in on someone else's behalf.

The [expanded report](../report/EXPANDED_REPORT.md),
[baseline review](SERIAL_BASELINE_REVIEW.md),
[replay review](REPLAY_DIAGNOSTIC_REVIEW.md) and
[dated progress](WEEKLY_PROGRESS.md) preserve the scientific conclusions and
their limits. Continuous checks repeat the applicable audits on the published
commit and produce a source/evidence snapshot with report exports.
