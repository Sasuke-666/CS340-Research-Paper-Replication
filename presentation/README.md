# Final presentation materials

Content revision: 25 November 2026, Macau/Beijing time (v1.0.2).

[SLIDES.md](SLIDES.md) contains the fourteen slides, with concise English text,
Chinese speaker notes and sources for each slide. The [talk and defence
outline](TALK_OUTLINE.md) explains the results in more detail and includes an
offline demonstration. Use the [expanded report](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/v1.0.2/report/EXPANDED_REPORT.md)
for the full analysis and experimental details.

## Presentation files

The editable PowerPoint and its PDF preview are available through
[submission/](../submission/README.md):

- `CS340_PERIOD_Final_Presentation_20261125.pptx`
- `CS340_PERIOD_Final_Presentation_20261125.pdf`

The deck has fourteen slides, nine editable data tables and one native chart.
Chinese explanations and evidence links are in the speaker notes. The
[v1.0.2 release](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/releases/tag/v1.0.2)
packages these files with the report and member handbook. The
[validation record](../docs/FINAL_VALIDATION_20261125.md) documents the export
and visual review. Current report and contribution links use `v1.0.2`;
references to historical protocols and measurements retain their fixed commits
and original dates.

## Talk sequence and demonstration

The talk begins with periodical scheduling and the two claims, C1 and C2. It
then presents the five-case comparison, explains the failure metrics that differ
from the paper, and examines the capacity correction and depth extension.
The final sections cover the independent account host, twostage's failure
mechanism and the member reviews.

Slide 13 follows six twostage acceptance logs from raw output to the reported
statistics. The [talk outline](TALK_OUTLINE.md) gives the files and the read-only
command. The serialized first-failure positions 4, 29 and 4 yield a mean of
12.3333 and a sample SD of 14.4338. This demonstration can run offline after the
repository is downloaded.

## Results and their scope

The overall verdict is **partially reproduced**. C1 is **partially supported**:
selected enumeration totals match, while several failure metrics differ. C2 is
**supported within the stated comparison**: PERIOD explores fewer schedules in
four cases and ties in twostage.

Depth d follows each released driver's rule. PERIOD enumerates p=2 through
d+1; the serialized driver enumerates p=N through d+N−1, where N is the thread
count observed at enumeration setup. At d=3, two-thread twostage uses 2–4
periods in both drivers. The ranges differ for N>2, and other driver differences
also remain. C2 concerns these released configurations.

Keep the following studies separate when presenting their numbers:

- The main comparison and four-thread follow-up contain 106 attempts,
  96 complete calls and 43 complete pairs. The independent account host adds
  its own 20 calls, and the capacity diagnostic has 40 readable calls.
- The capacity diagnostic uses 20 complete eligible calls and ten pairs from
  [the original lazy01 batch](../results/2026-11-14/summaries/layout-43570556202-lazy01/SUMMARY.md)
  and another 20 calls and ten pairs from
  [the account recovery](../results/2026-11-14/summaries/layout-recovery-43575584325-account/SUMMARY.md).
  The [original account archive was unavailable](../experiments/2026-11-14/account-evidence-failure/FINAL_OBSERVATION.json),
  so its denominator remains unknown. Correcting the reader aligns the native
  field offsets in both cases; the first-failure gaps remain.
- Twostage's 5/5 result describes five replays of one selected witness on the
  recorded build and host. Earlier reorder_3 studies have separate results
  of 4/5 and 20/20 per setting.
- The 22 November acceptance contains 30 complete comparisons and 15 pairs
  across five case hosts, plus 40 witness diagnostics. Its n=3 summaries are
  separate from the historical estimates. PR #6 recounts six of these existing
  comparison calls and contributes a secondary analysis. PR #7 adds synthetic recount tests;
  PR #8 adds independent audit and parser checks. Neither adds measurement calls.

Use mean and sample SD with the actual n, and compare times within their case
and host. A coverage hash's magnitude has no coverage-percentage meaning.
The twostage table gives a necessary partial order inferred from the source and
matching assertion. The recorded yield matrix specifies scheduling input;
the unique instruction trace remains unknown.

## Course arrangements and preparation

The project document refers to a separate Presentation Instruction, which is
absent from the inspected materials. The tentative presentation date is
1 December 2026. Confirm the actual date, duration, slide limit, speaking
allocation and submission format against that instruction. Fourteen slides is
the current content choice. The cover lists the three confirmed contributors;
the fourth-member arrangement still needs confirmation.

Use the [member handbook](../docs/MEMBER_ACTIONS_ZH.md) to prepare individual
explanations and handovers. Describe contributions and assistance consistently
with report section 10. Record rehearsal, personal participation and course
submission when they actually occur. The [final submission
checklist](../docs/FINAL_SUBMISSION_CHECKLIST.md) tracks the remaining course
actions.
