# PERIOD final presentation source

Content revision: 24 November 2026, Macau/Beijing time (v1.0.1). Fourteen slides with English screen text, Chinese speaker notes and source links. See [the presentation guide](README.md) for delivery files and course arrangements.

## Slide 01: PERIOD Replication

### English screen text

- Controlled concurrency testing via periodical scheduling
- CS340 Operating Systems
- Final project presentation, 24 November 2026
- Sun Haoyang  1240001201
- Li Yangshuo  1240001156
- He Boyu  1240000576

### Chinese speaker notes

我们选了 PERIOD 论文中的五个程序，复现其中的调度总数和失败结果，再用控制实验检查实现差异。下面先介绍方法和两项研究问题，再看结果、差距，以及组员提交的独立证据。封面是已确认的三位成员，内容更新到 11 月 24 日。

### Sources

- [Wen et al., ICSE 2022, DOI 10.1145/3510003.3510178](https://wcventure.github.io/pdf/ICSE2022_PERIOD.pdf)
- [Group report, sections 1 and 10](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/v1.0.1/report/EXPANDED_REPORT.md)

## Slide 02: Periods and bounded search

### English screen text

- Shared-state operation order can determine whether a concurrent program fails.
- PERIOD places key operations in successive execution periods.
- Several threads may share the final period.
- Feedback from execution can guide further exploration.

A request sets execution constraints. Threads may still interleave in the final period.

### Chinese speaker notes

同样的输入，线程访问共享变量的先后顺序一变，程序就可能出错。PERIOD 用 period 给关键操作划分执行阶段：前一个阶段完成，后一个阶段才能开始。最后一个 period 可以包含多个线程的剩余工作，所以锁的获取顺序仍可能变化。

驱动先提出调度请求，运行程序，再读取关键点反馈，决定是否继续探索额外切片。理解后面的实验时，要记住这一点：日志里的请求给出了执行约束，具体执行中仍可能出现不同交错。

### Sources

- [Paper, sections 2.2 and 3](https://wcventure.github.io/pdf/ICSE2022_PERIOD.pdf)
- [Group report, section 1](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/v1.0.1/report/EXPANDED_REPORT.md)

## Slide 03: Claims and experimental setup

### English screen text

- C1: Can we reproduce the selected Table 2 counts and failure metrics?
- C2: Under released depth rules, does PERIOD search less and still find the failure?
- Five programs from four families. Depth d=3. Budget 10,000.
- Each pair shares a host and binary. The driver and thread count determine the period bounds.
- Baseline: author_serialized_abi16.

Source cb8deb9. Image sha256:8f47d8b9…59fbc. The report lists full pins and setup differences.

### Chinese speaker notes

我们围绕两个问题做实验。C1 对照论文的枚举总数、首次失败位置和错误调度数。C2 看 PERIOD 能否在找到错误的同时，比适配后的序列化驱动少探索一些调度。

这里的 depth 是发布版驱动的参数 d。PERIOD 遍历的 period 数是 p=2 到 d+1；序列化驱动是 p=N 到 d+N−1，N 是开始枚举时观测到的线程数。取 d=3，三线程的 reorder_3 分别覆盖 2 至 4 和 3 至 5；双线程的 twostage 则都覆盖 2 至 4。两种驱动还保留各自的调度规则，因此 C2 比较的是这两套发布配置，调度器本身的单独效果仍待进一步实验。

代码固定在 cb8deb9，镜像固定到摘要，各批次记录自己的宿主和内核。原序列化驱动的共享内存接口经过最小适配；它与论文当年的可执行程序是否完全相同，现有材料还无法确认。

### Sources

- [Group report, sections 1–2 and Appendix A](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/v1.0.1/report/EXPANDED_REPORT.md)
- [Registered comparison protocol](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/experiments/2026-11-07/COMPARISON_PROTOCOL.md)
- [Compatibility protocol](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/experiments/2026-11-07/COMPATIBILITY_PROTOCOL.md)
- Enumeration bounds in the archived [PERIOD driver](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/8b3102c64214e53782ca0496b61c81f50fb17ff1/results/2026-11-07/comparison-42381922637/reorder_3/source/run_PDS.py#L636-L647) and [serialized driver](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/8b3102c64214e53782ca0496b61c81f50fb17ff1/results/2026-11-07/comparison-42381922637/reorder_3/source/run_OldPDS_abi16.py#L617-L630)

## Slide 04: Attempts, completions and pairs

### English screen text


| Study scope | Attempts | Complete | Complete pairs |
| --- | --- | --- | --- |
| Primary comparison | 100 | 90 | 40 |
| Four-thread follow-up | 6 | 6 | 3 |
| Accounting across both | 106 | 96 | 43 |

Separate evidence: 20 independent-host calls, 40 readable capacity calls and 5 twostage replays.

22 November acceptance: 30 comparisons / 15 pairs, plus 40 diagnostic calls.

### Chinese speaker notes

先看三个数：106 次尝试、96 次完整调用、43 组完整配对。它们来自主批次和四线程后续研究。

主批次有 100 次调用，也就是 50 组计划配对。其中十次四线程序列化调用碰到了 120 秒上限，所以剩下 90 次完整调用，只能组成 40 对。后续研究换用另一个宿主，把上限设为 240 秒，预先固定三对，六次调用全部完成。各案例和宿主仍分别计算统计量。

其他实验各有自己的用途：李扬烁的独立宿主有 20 次，容量诊断有 40 次可读调用，何博宇的见证重放有 5 次。原容量诊断中 account 的实际次数未知。11 月 22 日的新宿主验收又完成了 30 次比较、15 对，另有 40 次诊断；五个案例各用自己的新宿主。这些批次在报告中单独列出。

### Sources

- [Group report, sections 2, 5.2, 7 and 8](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/v1.0.1/report/EXPANDED_REPORT.md)
- [Four-thread completion summary](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/results/2026-11-07/summaries/comparison-42384122902/SUMMARY.md)

## Slide 05: Four cases require fewer schedules

### English screen text


Native editable chart data:

| Program | PERIOD | Serialized ABI16 |
| --- | ---: | ---: |
| reorder_3 | 27 | 30 |
| reorder_4 | 100 | 384 |
| account | 65 | 136 |
| lazy01 | 39 | 60 |
| twostage | 33 | 33 |

Original comparison and four-thread follow-up. Ten pairs per case, except three for reorder_4. Twostage ties at 33.

### Chinese speaker notes

这张图最直观的结果是：四个案例减少了枚举量，twostage 的两种方法都为 33。减少比例依次为 10.00%、73.96%、52.21%、35.00% 和 0%。

每行都比较同一个案例、同一个宿主上的两种方法。四线程这一行使用后续研究的三对，其余四行使用主批次的十对；枚举数的样本标准差都为 0。每次完整调用也都发现了目标错误。因此，在第 3 页说明的配置范围内，C2 得到支持。接下来再看首次失败位置，它回答的是错误在第几个请求被发现。

### Sources

- [Group report, Table 4 and C2 verdict](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/v1.0.1/report/EXPANDED_REPORT.md)
- [Primary comparison summary](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/results/2026-11-07/summaries/comparison-42381922637/SUMMARY.md)
- [Four-thread follow-up summary](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/results/2026-11-07/summaries/comparison-42384122902/SUMMARY.md)

## Slide 06: First failures differ from the paper

### English screen text

- C1 verdict: partially supported

| Case | Paper first failure | PERIOD first failure | Relative gap |
| --- | --- | --- | --- |
| account | 2 | 10.100 ± 0.316 | +405.00% |
| lazy01 | 3 | 8.000 ± 0.000 | +166.67% |
| twostage | 4 | 5.300 ± 4.111 | +32.50% |

Mean ± sample SD, n=10. First failure is an enumeration position.

### Chinese speaker notes

调度总数吻合以后，还要看错误是不是在相近的位置出现。表中是主批次 PERIOD 的三组结果，每组 n=10，写作均值加减样本标准差。

account 有九次在第 10 个请求首次失败，一次在第 11 个；lazy01 十次都在第 8 个。它们与论文参考值 2 和 3 的差距，每次重复都存在。twostage 则有九次在第 4 个、一次在第 17 个，较晚的那一次把均值拉到了 5.300。它的错误调度数九次为 2、一次为 1，也都低于论文的 3。

首次失败位置从 1 开始计数。这些逐次记录能解释均值和波动，但还不能告诉我们某次执行具体在哪一步发生了不同交错。五个程序的探索总数都匹配，而部分失败指标仍有差距，所以 C1 是部分支持，整体结论是部分复现。

### Sources

- [Group report, Table 2 and C1 verdict](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/v1.0.1/report/EXPANDED_REPORT.md)
- [Paper Table 2](https://wcventure.github.io/pdf/ICSE2022_PERIOD.pdf)

## Slide 07: Testing one capacity correction

### English screen text

- The Python reader declares 1,990 elements. The native runtime declares 3,964.

| Field offset, bytes | Native | Capacity 1990 | Capacity 3964 |
| --- | --- | --- | --- |
| kp | 220 | 220 | 220 |
| kpLoc | 8,148 | 4,200 | 8,148 |
| kpOrder | 16,076 | 8,180 | 16,076 |

One driver constant changes within each pair. Target binary and native runtime remain fixed.

### Chinese speaker notes

容量诊断从一个具体的接口问题开始：Python 驱动按 1,990 个元素读取数组，原生运行时却按 3,964 个元素存储。前一个数组长度不一致，后面的字段就会从错误的地址开始读取。

我们在每对实验中只改 Python 驱动的一个容量常数，使用相同的原生运行时、已构建目标、输入和清理程序。编译探针按运行时真实结构测量偏移，表中可以看到修正后的字段已经对齐。原生 sizeof 是 24008 字节，修正映射覆盖 24004 字节，末尾 4 字节是填充。

新诊断的两个条件都使用 fresh IPC。这个流程与历史批次有差别，所以容量的效果要看新实验内部的配对结果。

### Sources

- [Group report, section 8.1 and Table 9](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/v1.0.1/report/EXPANDED_REPORT.md)
- [Registered capacity protocol](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/experiments/2026-11-14/LAYOUT_PROTOCOL.md)

## Slide 08: The correction leaves first-failure gaps

### English screen text


| Case | Paper | Capacity 1990 | Capacity 3964 |
| --- | --- | --- | --- |
| account | 2 | 10.500 ± 0.850 | 10.200 ± 0.632 |
| lazy01 | 3 | 8.500 ± 1.581 | 8.200 ± 0.422 |

- Feedback hashes change; requested sequences stay the same.
- Timing and failure counts change in different directions.

Mean ± sample SD, n=10 per condition. Account uses a separate recovery batch; the original outcomes are unknown.

### Chinese speaker notes

接着看字段对齐后的首次失败位置。表中每种条件都有十次，即 n=10。account 从 10.500 变为 10.200，lazy01 从 8.500 变为 8.200，修正后仍高于论文的 2 和 3。

account 两臂各请求 65 个调度，lazy01 各请求 39 个，配对的请求序列一致。反馈哈希发生了变化，说明修正确实影响了反馈读取；哈希的数值大小不表示覆盖率百分比。错误调度数的配对均值变化分别为 account +1.4、lazy01 −1.7，耗时变化分别为 +1.070 和 −1.390 秒，效果方向并不一致。

这两个案例来自不同宿主。原 account 档案缺失，表中用的是另行登记、在新宿主完成的 20 次恢复调用；原作业的实际结果仍记为未知。

### Sources

- [Group report, Tables 10–12 and section 8.3](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/v1.0.1/report/EXPANDED_REPORT.md)
- [Account recovery summary](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/results/2026-11-14/summaries/layout-recovery-43575584325-account/SUMMARY.md)
- [Original lazy01 summary](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/results/2026-11-14/summaries/layout-43570556202-lazy01/SUMMARY.md)

## Slide 09: Depth controls the observed search

### English screen text


| Depth bound | Explored schedules | Calls finding failure | Buggy schedules |
| --- | --- | --- | --- |
| 1 | 3.000 ± 0.000 | 0/3 | 0.000 ± 0.000 |
| 2 | 13.000 ± 0.000 | 3/3 | 2.000 ± 0.000 |
| 3 | 27.000 ± 0.000 | 3/3 | 5.000 ± 1.732 |

Mean ± sample SD, n=3. Depth 2 explores 51.85% fewer schedules than depth 3.

### Chinese speaker notes

深度扩展只改一个因素：在同一个 reorder_3 二进制和宿主上，把 depth 设为 1、2、3，每种设置三次，并平衡运行顺序。结果是枚举量从 3 增到 13，再增到 27；depth 2 和 3 都在三次运行中找到错误。

九份日志还显示，请求是逐层增加的。depth 1 的 3 个请求和 depth 2 的 13 个请求，都是 depth 3 的 27 个请求的前缀。depth 3 依次包含 p=2 的 3 个、p=3 的 10 个、p=4 的 14 个请求。depth 2 与 3 的六次运行都在第 6 个请求 [[0],[2],[0,1,1]] 首次失败，它位于新增加的三 period 层。

从源码看，两个 setter 依次写 a=1、b=−1，checker 只接受 (0,0) 或 (1,−1)。这个请求把一个 setter 的首个关键点与剩余工作分开，让 checker 有机会读到中间状态 (1,0)。这解释依据的是请求和源码；原记录没有逐条内存操作轨迹。

depth 2 用少 51.85% 的探索量找到了这个已知错误。depth 3 找到更多失败调度，其中可能有多条指向同一个缺陷。depth 1 的 0/3 表示在该边界内没有观察到失败。

### Sources

- [Group report, section 6 and Table 7](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/v1.0.1/report/EXPANDED_REPORT.md)
- [Registered follow-up protocol](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/experiments/2026-11-07/FOLLOWUP_PROTOCOL.md)

## Slide 10: Account on an independent host

### English screen text

- Intel Core i5-14490F, WSL2, 16 permitted CPUs

| Method | First failure | Explored schedules | Buggy schedules |
| --- | --- | --- | --- |
| PERIOD | 8.800 ± 2.044 | 65.000 ± 0.000 | 26.400 ± 0.843 |
| Serialized ABI16 | 4.000 ± 0.000 | 136.000 ± 0.000 | 55.900 ± 0.316 |

Mean ± sample SD, n=10 per method, on the independent host.

### Chinese speaker notes

李扬烁在 11 月 8 日提交了独立 account 宿主的 20 次完整调用，两种方法各十次。换到这台机器后，枚举总数仍是 65 和 136。序列化方法的首次失败位置为 4，与论文参考值一致；PERIOD 的均值是 8.8，仍高于论文的 2。

这给结构上的搜索量比较增加了一份独立宿主证据。CPU、内核、WSL2 和校准都随宿主变化，较短的耗时还无法归结到某一个因素。后续 PR #3 对已有日志补做了序列检查和来源分析，实验调用数仍为原来的 20 次。

### Sources

- [Group report, section 7 and Table 8](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/v1.0.1/report/EXPANDED_REPORT.md)
- [Independent account summary](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/results/member-reruns/1240001156-account-20261108T122201Z-summary/SUMMARY.md)
- [Supplementary account audit](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/docs/reviews/1240001156-account-supplement.md)

## Slide 11: Twostage: a partially published update

### English screen text


| Step | Actor | Event inferred from source and assertion |
| --- | --- | --- |
| 1 | Writer A | Under lock 1: publish field 1 = 1, then unlock. |
| 2 | Reader B | Under lock 1: pass the guard; retain t1 = 1. |
| 3 | Reader B | Under lock 2: sample field 2 = 0 into t2. |
| 4 | Reader B | 0 ≠ 1 + 1; reach the line-48 assertion. |

Source-derived partial order. The witness records the assertion; exact preemption points remain unknown.

### Chinese speaker notes

twostage 的两个字段有关联，却分别由两把锁保护。默认有一个写线程 A 和一个读线程 B，两个字段初值都是 0。A 先在第一把锁下把 data1Value 写成 1，释放锁；如果执行到第 24 行，再在第二把锁下读回这个值，把 data2Value 写成 2。

B 也分两次加锁取样。能到达第 48 行断言，说明它先通过非零检查，保存了 t1=1，随后把第二个字段的旧值 0 存入 t2。即使 A 稍后写入 2，B 已经保存的局部副本仍是 0，于是 0 不等于 1+1，触发断言。

见证中记录的是 funcB 第 48 行的断言，原日志还保存了调度请求。表里的取样值和必要先后可以由源码推出；每次锁操作和确切抢占点没有被逐一记录。

### Sources

- [Twostage source analysis](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/docs/reviews/1240000576-twostage-witness-review.md)
- [Source-derived partial order](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/docs/reviews/1240000576-twostage-trace.md)
- [Archived original C source](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/results/2026-11-07/comparison-42381922637/twostage/source/twostage_bad.c)
- Original [PERIOD request and error](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/8b3102c64214e53782ca0496b61c81f50fb17ff1/results/2026-11-07/comparison-42381922637/twostage/period_r01.txt#L32-L34) and [saved assertion witness](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/8b3102c64214e53782ca0496b61c81f50fb17ff1/results/2026-11-07/comparison-42381922637/twostage/witnesses/period/r01/000001_0000004_assertion-failed#L1-L4)

## Slide 12: Results from fixed-witness replays

### English screen text


| Program and batch | Input | Observed assertion hits |
| --- | --- | --- |
| twostage, 15 November | One archived witness | 5/5 |
| reorder_3, early follow-up | One fixed witness | 4/5 |
| reorder_3, run 42380929383 | Same fixed witness | 20/20 at each multiplier |
| reorder_3, run 42381922637 | Same fixed witness | 20/20 at each multiplier |

22 November acceptance is separate: 30 comparisons / 15 pairs, plus 40 diagnostics.

### Chinese speaker notes

何博宇 11 月 15 日提交的研究，选用了原 twostage 第 1 次 PERIOD 运行、第 4 个请求的见证。五次连续重放都在 Perform Reproduction 标记之后出现 funcB 第 48 行断言，重建二进制的摘要也与原归档一致。因此，这个见证在记录的构建和宿主上五次都重现了错误。

表中还列了 reorder_3 的重放记录：早期为 4/5，后面两个批次都在每种倍率下达到 20/20。早期那一次为什么没有触发，现有诊断仍未解释。

11 月 22 日的验收又做了另一组检查：五个程序共 30 次比较、15 对，其中 twostage 是两种方法各 3 次，共 6 次搜索、3 对；另外 40 次 reorder_3 诊断为两种倍率各 20 次。这些结果与第 4 页的历史 106 次尝试、96 次完整调用、43 对分别统计。

### Sources

- [Twostage replay evidence](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/results/member-reruns/1240000576-twostage-43681034375/README.md)
- [Group report, sections 5.4–5.5 and Table 6](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/v1.0.1/report/EXPANDED_REPORT.md)
- 22 November [per-case comparison summary](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/8b3102c64214e53782ca0496b61c81f50fb17ff1/results/2026-11-22/summaries/acceptance-45015126850-attempt1/SUMMARY.md), [acceptance counts](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/8b3102c64214e53782ca0496b61c81f50fb17ff1/results/2026-11-22/summaries/acceptance-45015126850-attempt1/acceptance.json) and [reorder_3 diagnostic breakdown](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/8b3102c64214e53782ca0496b61c81f50fb17ff1/results/2026-11-22/summaries/acceptance-45015126850-attempt1/summary.json)

## Slide 13: Contributions and evidence trail

### English screen text


| Confirmed contributor | Submitted work |
| --- | --- |
| Sun Haoyang / 1240001201 | Coordinated registered studies, fresh-host acceptance and final integration. |
| Li Yangshuo / 1240001156 | Independent account rerun. Supplementary audit, PR #3. Report traceability, PR #5. |
| He Boyu / 1240000576 | Four-thread audit; twostage source/replays, PR #4; six-log recount and slides, PR #6. |

Offline demonstration: six twostage logs → independent recount → published summary.

### Chinese speaker notes

各成员的贡献可以沿原始提交查到。孙皓扬协调登记实验、组内验收和最终整合；李扬烁提交独立 account 宿主结果、PR #3 的补充审查，以及 PR #5 的报告追溯核对；何博宇提交四线程核数、PR #4 的 twostage 机制和五次重放，再在 PR #6 复算 11 月 22 日组内验收的六份 twostage 日志。PR #6 属于已有数据的复核，原测量仍归于组内验收。实施、执行和写作辅助见报告的使用声明。

演示时运行 scripts/recount_twostage_acceptance.py。先打开序列化的第二份日志：第一个报错跟在 test 0029 后面，所以三个首次失败位置是 4、29、4。均值为 37/3=12.3333，样本标准差为 25/√3=14.4338。运行复算，再对照保存的 summary：每种方法三次搜索，每次 33 个请求。

这条命令读取已有档案，现场无需重新运行实验。提前把源码、日志和 summary 下载到本地，就可以在没有网络时完成演示。

### Sources

- [Group report, section 10 and contribution table](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/v1.0.1/report/EXPANDED_REPORT.md)
- [Contribution record](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/v1.0.1/docs/CONTRIBUTIONS.csv)
- [Li Yangshuo report traceability PR #5](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/5)
- [He Boyu twostage PR #4](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/4)
- [He Boyu independent six-log recount and presentation PR #6](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/6)
- [Six-log recount source](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/v1.0.1/scripts/recount_twostage_acceptance.py)

## Slide 14: Verdict and remaining question

### English screen text

- C1: Partially supported
- C2: Supported within the stated comparison
- Overall: Partially reproduced
- Open question: why do failure observations vary under identical requests?

Verification entry point: make audit

### Chinese speaker notes

我们的结论是部分复现。五个程序的 PERIOD 枚举总数与论文吻合；与适配后的序列化驱动相比，四个案例减少请求数，twostage 持平。首次失败位置和部分失败调度数仍有差距。

容量实验把一个接口问题单独检验了出来：修正后字段对齐、反馈改变，首次失败差距仍然存在。twostage 则给出了一个具体的失败机制，以及选定见证的五次重放记录。接下来最需要补上的证据是经过验证的实际执行轨迹，用它解释相同请求下失败观测为什么变化。仓库中的 make audit 可以复查今天展示的归档数据。

### Sources

- [Group report, verdicts and limitations](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/v1.0.1/report/EXPANDED_REPORT.md)
- [Repository and reproducibility instructions](https://github.com/Sasuke-666/CS340-Research-Paper-Replication)
