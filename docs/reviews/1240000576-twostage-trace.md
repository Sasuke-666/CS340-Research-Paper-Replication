# Execution evidence for twostage witness 000001_0000004

Archive batch `42381922637`, method `period`, repetition 1, test 4. The worker names below come from the C functions. Rows 2–5 give the partial order required for the assertion in this one-writer, one-reader program. Values in those rows follow from the source and the assertion; the runtime did not print them.

| Step | Actor and source | Shared state or local observation | Evidence |
| ---: | --- | --- | --- |
| 1 | Main, lines 8–13 and 68–94 | Both fields initialize to 0. Main creates A and B with distinct field mutexes. | Source and archived no-argument command. The log reports two workers. |
| 2 | A, lines 19–21 | A writes field 1 = 1 before releasing lock 1. Field 2 still holds its initial 0 at this publication point. | Source-required predecessor of B passing the guard. |
| 3 | B, lines 34–40 | B acquires lock 1 after A releases it, passes the nonzero guard, copies 1 to t1, and releases lock 1. | Required by B reaching line 48 and by field 1 having one nonzero assignment. |
| 4 | B, lines 42–44 | B must read 0 from field 2 before A’s store of 2 at line 24, if that store executes. It retains 0 in t2. | With one writer, field 2 can only be 0 or 2. A sample of 2 would satisfy the check. |
| 5 | B, lines 46–48 | The local comparison evaluates as 0 != 1 + 1. B emits the diagnostic and aborts. | The witness records the diagnostic, function and source line. The numerical substitution is a deduction. |
| 6 | A or main after B samples field 2 | Whether A stores 2 before the process aborts, the shared values at abort, and the exact preemption points are unknown. | No timestamps, per-operation trace or final memory snapshot. |

**Scheduler evidence.** Test 4 requests three periods: two points for ID 0, five for ID 1, then two for ID 0. The yield matrix in the saved witness is the input consumed on replay. Neither file records a total order of realized memory operations. The new five-run evidence repeats the terminal assertion and supplies no additional instruction trace.

[Author source with numbered lines](https://github.com/wcventure/PERIOD/blob/cb8deb9a176e5bb292d70d46557dd61dc0e98069/evaluation/CS/twostage/twostage_bad.c#L8-L106) · [Original log](../../results/2026-11-07/comparison-42381922637/twostage/period_r01.txt#L27-L35) · [Saved witness](../../results/2026-11-07/comparison-42381922637/twostage/witnesses/period/r01/000001_0000004_assertion-failed) · [Fresh replay record](../../results/member-reruns/1240000576-twostage-43681034375/README.md)
