# Supplementary evidence audit: account observation provenance and limits

**Prepared by:** 李扬烁, student ID 1240001156, GitHub `barkhorn996`

**Review date:** 14 November 2026, Asia/Shanghai (UTC+08:00)

**Provenance clarification:** 15 November 2026, commit `d907517`.
**Integration decision:** accepted as supplementary evidence review on 16 November 2026; see [the closeout record](../INTEGRATION_20261116.md).

**Reviewed repository state:** `fd0d807f39a9d972dcd4929486d002f53ae4e4f3`
**Scope:** provenance review of the independent account comparison, the original primary account batch, and the 14 November capacity diagnostic

This supplement adds no new workload measurements. It checks the relationships among existing batches, reproduces the reported descriptive statistics from their records, and audits whether the current report states a stronger causal conclusion than the evidence supports. AI assistance performed the requested comparison and drafting; personal oral explanation and member-to-member cross-review remain pending.

## 1. Provenance and contribution boundary

This document is a secondary analysis of already published evidence. It must not be presented as a new account experiment or as independent ownership of the 14 November capacity study.

| Material in this document | Producer and date | Role in PR #3 |
| --- | --- | --- |
| Twenty `account` calls comparing `period` and `author_serialized_abi16` on the WSL2 host | 李扬烁, 8 November 2026; previously submitted in PR #2 and merged into `main` | Primary measurements from the author's earlier independent work; reused here for comparison |
| Original five-case account measurements and summary | Group repository work published 7 November 2026 | Secondary data; inspected and compared, not independently produced in PR #3 |
| Capacity1990 versus capacity3964 protocol, execution, probes, source patch, recovery run and scientific interpretation | Group repository work published 14 November 2026 | Secondary data and prior analysis; cited and audited, not independently produced in PR #3 |
| Paper Table 2 references | Wen et al., ICSE 2022 | External reference values |
| Normalized request-sequence hashing across the member and original batches | Work added in PR #3 using existing raw logs | New analytical check, but no new workload execution |
| Cross-batch descriptive comparison and report-language audit | Work added in PR #3 | Secondary review contribution |

The new work in this PR is therefore limited to evidence organization and independent analysis. It does not claim authorship of the capacity correction, the native-layout probe, the recovery protocol, the recovery run, or their separate scientific conclusions.

PR #3 should be classified as a **supplementary evidence audit** unless the group separately determines that its analytical checks warrant another contribution category. It should not be described as a new experimental extension.

## 2. Questions reviewed

1. Which account metrics agree across the three observation sets?
2. Which differences are controlled within one batch?
3. Which differences arise from multiple simultaneous changes and therefore remain attributionally unresolved?
4. Does the report accurately distinguish structural schedule agreement from failure-observation agreement?
5. Does the report's explanation of the remaining first-failure gap use evidence consistent with the stated limits?

## 3. Observation sets

| Set | Evidence path | Scope | Host and kernel | Methods or conditions |
| --- | --- | --- | --- | --- |
| Independent member rerun | [`1240001156-account-20261108T122201Z-summary/SUMMARY.md`](../../results/member-reruns/1240001156-account-20261108T122201Z-summary/SUMMARY.md) | One `account` case; 20 complete calls; ten pairs | Intel Core i5-14490F; 16 permitted CPUs; WSL2 kernel `6.18.33.2-microsoft-standard-WSL2` | `period` versus `author_serialized_abi16` |
| Original primary batch | [`comparison-42381922637/SUMMARY.md`](../../results/2026-11-07/summaries/comparison-42381922637/SUMMARY.md) | Account is one case in the five-case primary study; ten complete pairs for account | AMD EPYC 9V74; four permitted CPUs; kernel `7.0.0-1017-azure` | `period` versus `author_serialized_abi16` |
| Account capacity recovery | [`layout-recovery-43575584325-account/SUMMARY.md`](../../results/2026-11-14/summaries/layout-recovery-43575584325-account/SUMMARY.md) | One `account` case; 20 complete calls; ten pairs | AMD EPYC 9V45; four permitted CPUs; kernel `7.0.0-1017-azure` | `capacity1990` versus `capacity3964`, both using the PERIOD driver |

All three sets use the same pinned upstream source revision `cb8deb9a176e5bb292d70d46557dd61dc0e98069`, the same pinned container digest, `account_bad`, depth 3, a 10,000-schedule budget, ten pairs and a 120-second invocation limit. These common settings support a comparison of observed outcomes, but they do not make the host scopes interchangeable.

The first two sets compare two different driver implementations. The third set answers a different question: whether one change to the Python driver's key-point-array capacity changes behavior when both arms use the PERIOD scheduler. It is a mechanism diagnostic, not another PERIOD-versus-serialized baseline comparison.

## 4. Recorded results

Values are mean plus or minus sample standard deviation with denominator `n - 1`; every complete arm has `n = 10`. First failure is the one-based schedule-test ordinal at which an assertion is first observed.

| Set | Method or condition | First failure | Explored schedules | Buggy schedules | Whole-driver seconds |
| --- | --- | ---: | ---: | ---: | ---: |
| Independent rerun | `period` | 8.800 ± 2.044 | 65.000 ± 0.000 | 26.400 ± 0.843 | 6.8555 ± 0.1552 |
| Independent rerun | `author_serialized_abi16` | 4.000 ± 0.000 | 136.000 ± 0.000 | 55.900 ± 0.316 | 12.1671 ± 0.3959 |
| Original primary batch | `period` | 10.100 ± 0.316 | 65.000 ± 0.000 | 24.400 ± 2.914 | 23.738 ± 2.356 |
| Original primary batch | `author_serialized_abi16` | 7.700 ± 7.889 | 136.000 ± 0.000 | 49.200 ± 8.217 | 49.317 ± 7.662 |
| Capacity recovery | `capacity1990` with PERIOD | 10.500 ± 0.850 | 65.000 ± 0.000 | 22.900 ± 3.281 | 23.569 ± 3.547 |
| Capacity recovery | `capacity3964` with PERIOD | 10.200 ± 0.632 | 65.000 ± 0.000 | 24.300 ± 1.767 | 24.639 ± 2.040 |

Paper Table 2 provides the following account references:

| Paper method | First failure | Explored schedules | Buggy schedules |
| --- | ---: | ---: | ---: |
| PERIOD | 2 | 65 | 26 |
| Serial | 4 | 136 | 56 |

## 5. What agrees

### 5.1 Structural enumeration

Every account observation set reproduces the paper's two total enumeration counts under the selected implementation labels:

- All PERIOD and capacity-condition observations explore 65 schedules.
- All `author_serialized_abi16` observations explore 136 schedules.

The zero sample SD is a description of these finite repeated outputs, not proof of universal determinism. It supports the narrower claim that the released schedule generator produced the same requested count in every observed repetition.

### 5.2 Independent member batch

The independent batch is closest to two paper reference values:

- Its serialized first failure is 4, exactly the paper's Serial reference.
- Its serialized total is 136, exactly the paper's reference.
- Its serialized buggy-schedule mean is 55.9 versus 56, with nine values of 56 and one value of 55.
- Its PERIOD total is 65, exactly the paper's reference.
- Its PERIOD buggy-schedule mean is 26.4 versus 26.

These agreements support the structural schedule comparison and show a useful independent-host corroboration. They do not establish complete Table 2 replication because the PERIOD first-failure mean is still 8.8 versus 2.

### 5.3 Original primary batch

The original batch also reproduces both total enumeration counts, but its PERIOD first-failure mean is 10.1 and its serialized first-failure distribution is much more dispersed: 7.7 ± 7.889. Its serialized buggy-schedule mean is 49.2 versus the paper's 56.

Thus the cross-host agreement is strongest for the structural schedule totals. Failure-related metrics are sensitive to the concrete run or host scope even when the printed enumeration is identical.

## 6. Printed requests versus failure observations

As an additional check, I normalized ANSI control sequences, extracted the printed `test` lines from all account logs, and hashed the complete ordered sequence in each invocation.

Result:

| Driver family | Independent rerun | Original primary batch | Distinct sequences across both batches |
| --- | --- | --- | ---: |
| PERIOD | One sequence, hash prefix `c4ceaea3afb0` | One sequence, hash prefix `c4ceaea3afb0` | 1 |
| `author_serialized_abi16` | One sequence, hash prefix `06b7fb843aad` | One sequence, hash prefix `06b7fb843aad` | 1 |

The independent PERIOD batch has first failures of 10, 5, 9, 5, 10, 9, 10, 10, 10 and 10 despite these identical printed requests. Its buggy-schedule counts range from 25 to 28. The original batch also retains one PERIOD request sequence, while its observed failure counts range from 18 to 26.

This supports the report's distinction between a requested schedule and the realized execution inside a parallel final period. It also shows why identical explored-schedule totals need not imply identical failure observations.

The result does not identify the realized mutex order in any invocation. The source-level account example in the report remains a conditional mechanism, not a measured trace. A claim that a particular first failure was caused by a particular thread order would require validated instrumentation of that execution.

## 7. What changes across batches

### 7.1 Independent rerun versus original primary batch

The following factors change together:

- Host CPU model and available CPU set
- Host operating system and kernel
- WSL2 versus hosted Linux execution
- Batch-specific calibration and environment
- Independently built but source-identical binaries and driver files

The independent host is therefore a corroborating scope, not a controlled host intervention. Its lower wall times and different failure counts cannot be assigned separately to CPU, kernel, WSL2 scheduling, calibration or another environmental factor.

### 7.2 Original capacities within the 14 November recovery

The diagnosis is controlled differently. Within the recovery batch:

- Both arms use the PERIOD driver.
- The benchmark, native runtime, scheduler, input, depth and budget are fixed.
- The capacity declaration is the only disclosed driver change.
- Both arms start from a verified clean key-1111 state.
- Both arms print the same requested schedule sequence.

The paired corrected-minus-original changes are:

| Metric | Capacity3964 minus capacity1990 |
| --- | ---: |
| Explored schedules | 0.000 ± 0.000 |
| First failure | -0.300 ± 1.160 |
| Buggy schedules | +1.400 ± 4.402 |
| Whole-driver seconds | +1.070 ± 4.323 |

The correction aligns the location and order offsets and changes the observed default feedback hash from 18 to 196,202. It changes internal feedback decoding, but it does not recover the paper's first-failure value and does not produce a uniform improvement in buggy schedules or time.

The capacity diagnostic therefore addresses a real implementation threat. It does not explain the larger first-failure gap between the independent host and the original batch, because those batches differ in multiple host and procedure dimensions.

## 8. Report audit

The reviewed report language is appropriately limited in the relevant sections:

1. It calls the WSL result an **independent host corroboration**, not a replacement for the primary batch.
2. It keeps the WSL account statistics outside the earlier 106-attempt, 96-complete, 43-pair accounting.
3. It states that hardware, kernel and calibration changed together, so the smaller elapsed time does not isolate a causal factor.
4. It separates the capacity correction from PERIOD-versus-serialized comparison.
5. It states that capacity changes feedback decoding and observed outcomes but does not recover the paper's first-failure references.
6. It retains missing original account evidence rather than treating it as zero.
7. It avoids claiming that a buggy schedule is a distinct concurrency defect.
8. It uses whole-driver wall time rather than calling it native execution time or time to first failure.

No material overstatement was found in the report's account discussion. The current qualification that cross-batch differences are descriptive is necessary and should remain in the final PDF.

One wording requirement should continue to be enforced: `author_serialized_abi16` is not proven identical to the paper's historical Serial executable. Its first-failure agreement in the independent batch is encouraging but is not evidence of historical implementation equivalence.

## 9. Findings and conclusion

The evidence supports the following statements:

- The paper's exploration totals of 65 for PERIOD and 136 for the compatible serialized driver reproduce across the independent and original hosted batches.
- The independent serialized run matches the paper's first-failure value 4 and is very close to the paper's buggy-schedule count 56.
- PERIOD's first-failure discrepancy persists on the independent host: 8.8 versus the paper's 2, a signed gap of +6.8 and a relative gap of +340%.
- The 14 November capacity correction changes decoded feedback but does not close the first-failure gap.
- The report's partial-replication verdict remains supported.

The unresolved item is the cause of the PERIOD first-failure discrepancy. Existing evidence supports several possibilities but does not isolate one:

- Actual parallel-period execution order may differ from the abstract printed request.
- Host, kernel, WSL2, CPU affinity and calibration differ across the account batches.
- Released-driver implementation details differ from the paper's historical executable.
- Feedback decoding affects observed behavior, although the capacity correction alone did not remove the gap.

A valid causal test would require a separately registered controlled factor or a verified execution trace. More text-only interpretation should not be used to claim that one of these possibilities has been established.

## 10. Contribution classification

The following classification is provided so that the final contribution record can be accurate:

- **Previously owned experiment:** the 8 November WSL2 account comparison and its 20 complete method calls.
- **Secondary evidence reviewed:** the 7 November original account batch and the 14 November capacity study.
- **New in PR #3:** normalization and hashing of all printed request sequences, cross-batch statistical comparison, and audit of report claims and limits.
- **Not performed independently in PR #3:** capacity source modification, layout probe, synthetic sentinel test, recovery protocol design, recovery measurements, and the conditional mutex-order analysis of the benchmark source.

No result in this document should be used to transfer authorship of the group's 7 November or 14 November experiments to the author of this review.

## 11. Evidence links

- Independent batch: `results/member-reruns/1240001156-account-20261108T122201Z/`
- Independent summary: `results/member-reruns/1240001156-account-20261108T122201Z-summary/`
- Original account batch: `results/2026-11-07/comparison-42381922637/account/`
- Original summary: `results/2026-11-07/summaries/comparison-42381922637/`
- Account capacity recovery: `results/2026-11-14/layout-recovery-43575584325/`
- Capacity summary: `results/2026-11-14/summaries/layout-recovery-43575584325-account/`
- Current scientific review: `docs/LAYOUT_DIAGNOSTIC_REVIEW_20261114.md`
- Current report: `report/EXPANDED_REPORT.md`, sections 3, 7, 8 and 10

Completed by: 李扬烁, 14 November 2026.
