# PERIOD rehearsal presentation source

Revised 22 November 2026, Macau/Beijing time. Fourteen total slides. English screen text and Chinese speaker notes. Official presentation duration, speaking allocation and format remain to be confirmed. These instructions specify content and do not certify a completed presentation.

## Slide 01: PERIOD Replication

### English screen text

- Controlled concurrency testing via periodical scheduling
- CS340 Operating Systems
- Rehearsal draft, 22 November 2026
- Sun Haoyang  1240001201
- Li Yangshuo  1240001156
- He Boyu  1240000576

### Chinese speaker notes

本组复现PERIOD论文中五个程序的指定结果，并通过控制实验研究实现差异。今天先解释方法与两项主张，再展示复现结果、差异及成员独立证据。三位姓名对应已确认成员；正式讲解时长与分工仍以课程通知为准。本稿用于排练。

### Sources

- [Wen et al., ICSE 2022, DOI 10.1145/3510003.3510178](https://wcventure.github.io/pdf/ICSE2022_PERIOD.pdf)
- [Group report, sections 1 and 10](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/2de378771adbeeced2709f9bc4ca436799848197/report/EXPANDED_REPORT.md)

## Slide 02: Periods and bounded search

### English screen text

- Concurrent failures depend on the order of shared-state operations.
- PERIOD assigns key operations to successive execution periods.
- The mixed final period can contain work from several threads.
- Execution feedback can guide further exploration.

A requested schedule constrains execution. The realized order still needs evidence.

### Chinese speaker notes

同一输入下，不同线程访问共享数据的顺序会影响是否触发错误。PERIOD将关键操作安排到有先后约束的period中。其实现允许最后一个period包含多个线程，实际锁获取顺序仍可能有变化。生成器提出请求，程序执行后反馈关键点信息，驱动再决定是否探索额外切片。后面需要一直区分请求调度和实际执行。

### Sources

- [Paper, sections 2.2 and 3](https://wcventure.github.io/pdf/ICSE2022_PERIOD.pdf)
- [Group report, section 1](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/2de378771adbeeced2709f9bc4ca436799848197/report/EXPANDED_REPORT.md)

## Slide 03: Claims and experimental setup

### English screen text

- C1: Do the selected Table 2 counts and failure metrics reproduce?
- C2: Under released depth rules, does PERIOD reduce search and still find failure?
- Five programs from four families. Depth d=3. Budget 10,000.
- Baseline: author_serialized_abi16. Different period bounds. Same case host and binary.

Source cb8deb9. Image sha256:8f47d8b9…59fbc. Full pins and deviations appear in the report.

### Chinese speaker notes

C1同时比较枚举总数、首次失败位置和错误调度数。C2比较两个发布版驱动各自深度规则下的配置：PERIOD遍历period数p=2到d+1，序列化驱动遍历p=N到d+N−1，N为枚举开始时观测到的线程数。三线程d=3时，两者分别覆盖p=2、3、4与p=3、4、5。因此数值相同的depth并不对应相同的绝对period边界，保留的驱动差异也使本比较无法把效果单独归因于调度器。源代码固定在cb8deb9，镜像固定到摘要，每批次另记录宿主和内核。原序列化接口需要最小适配，其历史可执行程序同一性仍未证明。结论限于五个选定程序和上述配置。

### Sources

- [Group report, sections 1–2 and Appendix A](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/2de378771adbeeced2709f9bc4ca436799848197/report/EXPANDED_REPORT.md)
- [Registered comparison protocol](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/experiments/2026-11-07/COMPARISON_PROTOCOL.md)
- [Compatibility protocol](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/experiments/2026-11-07/COMPATIBILITY_PROTOCOL.md)

## Slide 04: Attempts, completions and pairs

### English screen text


| Study scope | Attempts | Complete | Complete pairs |
| --- | --- | --- | --- |
| Primary comparison | 100 | 90 | 40 |
| Four-thread follow-up | 6 | 6 | 3 |
| Accounting across both | 106 | 96 | 43 |

Separate evidence: 20 independent-host calls, 40 readable capacity calls and 5 twostage replays.

### Chinese speaker notes

主批次100次驱动调用等于50组计划方法配对。十次四线程序列化调用到达120秒上限，因此90次完整调用只能提供40组完整配对。后续研究在另一个宿主用240秒上限固定运行三对，六次都完整。106、96、43是这两项研究的记账总数，统计仍按案例与宿主分别报告。李的20次独立宿主、布局诊断40次可读调用、何的5次重放都使用各自分母。原布局account实际次数未知。

### Sources

- [Group report, sections 2, 5.2, 7 and 8](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/2de378771adbeeced2709f9bc4ca436799848197/report/EXPANDED_REPORT.md)
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

Explored schedules. n=10 pairs per case, except reorder_4 n=3. Twostage ties at 33.

### Chinese speaker notes

五行均为同案例同宿主的比较，两种发布驱动各自使用第3页说明的depth到period映射。四线程使用独立完成研究的三对，其余四案例使用十对，每行枚举数的样本标准差为0。减少比例依次是10.00%、73.96%、52.21%、35.00%、0%。每次完整调用均发现目标错误。这支持限定配置内的C2，调度总数的减少不能直接推导首次失败更早或所有程序更快。

### Sources

- [Group report, Table 4 and C2 verdict](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/2de378771adbeeced2709f9bc4ca436799848197/report/EXPANDED_REPORT.md)
- [Primary comparison summary](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/results/2026-11-07/summaries/comparison-42381922637/SUMMARY.md)
- [Four-thread follow-up summary](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/results/2026-11-07/summaries/comparison-42384122902/SUMMARY.md)

## Slide 06: Failure metrics retain substantial gaps

### English screen text

- C1 verdict: partially supported

| Case | Paper first failure | PERIOD first failure | Relative gap |
| --- | --- | --- | --- |
| account | 2 | 10.100 ± 0.316 | +405.00% |
| lazy01 | 3 | 8.000 ± 0.000 | +166.67% |
| twostage | 4 | 5.300 ± 4.111 | +32.50% |

Mean ± sample SD, n=10. First failure is an enumeration position.

### Chinese speaker notes

这里展示原主批次PERIOD的三个代表性首次失败差距，数值是均值加减样本标准差，每行n=10。account有九次在第10个请求首次失败、一次在第11个，lazy01十次均在第8个，说明它们相对论文2和3的偏移在每次重复中都存在。twostage有九次在第4个、一次在第17个，单次较晚发现使均值升到5.300；错误调度数则九次为2、一次为1，均低于论文的3。首次失败指一基的枚举位置。频数帮助解释均值与离散程度，不能确定延迟所对应的真实执行顺序。五个程序的探索总数全部匹配，首次失败和部分错误调度数仍有偏差，所以总体保持部分复现。

### Sources

- [Group report, Table 2 and C1 verdict](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/2de378771adbeeced2709f9bc4ca436799848197/report/EXPANDED_REPORT.md)
- [Paper Table 2](https://wcventure.github.io/pdf/ICSE2022_PERIOD.pdf)

## Slide 07: A controlled capacity correction

### English screen text

- The Python reader declares 1,990 elements. The native runtime declares 3,964.

| Field offset, bytes | Native | Capacity 1990 | Capacity 3964 |
| --- | --- | --- | --- |
| kp | 220 | 220 | 220 |
| kpLoc | 8,148 | 4,200 | 8,148 |
| kpOrder | 16,076 | 8,180 | 16,076 |

One driver constant changes within each pair. Target binary and native runtime remain fixed.

### Chinese speaker notes

驱动读取共享内存时，数组容量不同使后续字段错位。新实验只改变Python驱动的一个容量常数，两臂使用相同原生运行时、已构建目标、输入及清理程序。编译探针使用原生真实结构，证实修正后的使用字段偏移匹配。原生sizeof为24008，修正映射覆盖24004，末尾4字节是填充。新诊断共同采用fresh IPC，与旧批次相比还有流程差异，所以因果比较限定在新实验每对内部。

### Sources

- [Group report, section 8.1 and Table 9](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/2de378771adbeeced2709f9bc4ca436799848197/report/EXPANDED_REPORT.md)
- [Registered capacity protocol](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/experiments/2026-11-14/LAYOUT_PROTOCOL.md)

## Slide 08: The correction leaves first-failure gaps

### English screen text


| Case | Paper | Capacity 1990 | Capacity 3964 |
| --- | --- | --- | --- |
| account | 2 | 10.500 ± 0.850 | 10.200 ± 0.632 |
| lazy01 | 3 | 8.500 ± 1.581 | 8.200 ± 0.422 |

- Feedback hashes change. Requested sequences remain equal.
- Timing and failure-yield changes have mixed directions.

Mean ± sample SD, n=10 per condition. Original account outcomes remain unknown. Recovery is separate.

### Chinese speaker notes

每种条件n=10，表中是首次失败均值与样本标准差。account两臂65个请求，lazy01两臂39个请求，配对请求序列相同。反馈哈希改变，表明实际读取反馈受到影响；哈希数字大小没有覆盖率百分比意义。错误调度数的配对变化account为+1.4、lazy01为−1.7；耗时变化分别+1.070和−1.390秒，方向不同。两批来自不同host。原account档案缺失，恢复的20次另列，不能补成原作业的实测次数。

### Sources

- [Group report, Tables 10–12 and section 8.3](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/2de378771adbeeced2709f9bc4ca436799848197/report/EXPANDED_REPORT.md)
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

这项单因素扩展在同一reorder_3二进制和宿主上，只改变深度1、2、3，每个条件三次，顺序平衡。九份日志均显示嵌套请求前缀：depth 1的3个请求、depth 2的13个请求均是depth 3的27个请求的前缀。depth 3依次包含p=2的3个、p=3的10个、p=4的14个请求。depth 2与3的六次运行都在第6个请求[[0],[2],[0,1,1]]首次失败，位于新增加的三period层。源码中两个setter依次写a=1和b=−1，checker只接受(0,0)或(1,−1)；该请求将一个setter的首个关键点与剩余工作分开，并将checker放在两者之间，允许观察中间状态(1,0)。这是请求顺序和源码支持的机制解释，原记录没有逐条内存操作的真实轨迹。深度2三次均找到已知错误，相对深度3减少51.85%的探索。深度3的更多失败调度仍可能对应同一个缺陷。深度1的未发现结果只描述该边界内的观察。

### Sources

- [Group report, section 6 and Table 7](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/2de378771adbeeced2709f9bc4ca436799848197/report/EXPANDED_REPORT.md)
- [Registered follow-up protocol](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/experiments/2026-11-07/FOLLOWUP_PROTOCOL.md)

## Slide 10: Independent account host corroboration

### English screen text

- Intel Core i5-14490F, WSL2, 16 permitted CPUs

| Method | First failure | Explored schedules | Buggy schedules |
| --- | --- | --- | --- |
| PERIOD | 8.800 ± 2.044 | 65.000 ± 0.000 | 26.400 ± 0.843 |
| Serialized ABI16 | 4.000 ± 0.000 | 136.000 ± 0.000 | 55.900 ± 0.316 |

Mean ± sample SD, n=10 per method. Keep this host separate from the primary batch.

### Chinese speaker notes

李扬烁11月8日的独立account宿主提供20次完整调用，每种方法十次。结构枚举仍为65和136。序列化首次失败4与论文参考值一致，PERIOD的8.8仍高于2。跨批次CPU、内核、WSL2和校准共同变化，耗时更短不能归因于单一因素。后续PR #3补充序列检查和来源范围说明，使用旧证据进行新分析，未增加实验调用数。

### Sources

- [Group report, section 7 and Table 8](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/2de378771adbeeced2709f9bc4ca436799848197/report/EXPANDED_REPORT.md)
- [Independent account summary](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/results/member-reruns/1240001156-account-20261108T122201Z-summary/SUMMARY.md)
- [Supplementary account audit](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/docs/reviews/1240001156-account-supplement.md)

## Slide 11: Twostage: a partially published update

### English screen text


| Step | Actor | Source-required observation |
| --- | --- | --- |
| 1 | Writer A | Publish field 1 = 1 under lock 1. |
| 2 | Reader B | Pass the guard and retain local t1 = 1. |
| 3 | Reader B | Sample field 2 = 0 before its update. |
| 4 | Reader B | Check 0 ≠ 1 + 1 and reach the assertion. |

Source-derived necessary partial order. Exact preemption points remain unknown.

### Chinese speaker notes

twostage默认一个写线程A和一个读线程B，两个字段用不同锁保护。A先发布字段1=1，B随后通过非零检查保存t1=1，再在第二把锁下读到字段2旧值0，最终断言失败。这里是源代码和断言共同限定的必要偏序。原日志并未记录每个操作的时间戳或唯一锁顺序；A可能在B取样后、程序终止前写入字段2。图表中不要将推断标成观测轨迹。

### Sources

- [Twostage source analysis](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/docs/reviews/1240000576-twostage-witness-review.md)
- [Source-derived partial order](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/docs/reviews/1240000576-twostage-trace.md)
- [Archived original C source](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/results/2026-11-07/comparison-42381922637/twostage/source/twostage_bad.c)

## Slide 12: Replay evidence keeps its own scope

### English screen text


| Program and batch | Input | Observed assertion hits |
| --- | --- | --- |
| twostage, 15 November | One archived witness | 5/5 |
| reorder_3, early follow-up | One fixed witness | 4/5 |
| reorder_3, run 42380929383 | Same fixed witness | 20/20 at each multiplier |
| reorder_3, run 42381922637 | Same fixed witness | 20/20 at each multiplier |

These are separate studies. Later diagnostics leave the earlier reorder_3 miss unexplained.

### Chinese speaker notes

何博宇用原twostage第1次PERIOD运行第4个请求的见证，进行五次预先固定的重放。全部在Perform Reproduction标记之后出现相同funcB第48行断言。重建二进制的记录摘要与原归档相同，驱动返回0本身不能证明目标失败。该结果只覆盖此输入、此build和host。下面保留不同程序reorder_3的早期4/5与两个后续批次，每个后续批次的两种倍率分别20/20。早期漏报的原因仍未解释。

### Sources

- [Twostage replay evidence](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/be8688609e9da8aeb0e1eeaf5a60d115486ed1bf/results/member-reruns/1240000576-twostage-43681034375/README.md)
- [Group report, sections 5.4–5.5 and Table 6](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/2de378771adbeeced2709f9bc4ca436799848197/report/EXPANDED_REPORT.md)

## Slide 13: Contributions and evidence trail

### English screen text


| Confirmed contributor | Submitted work |
| --- | --- |
| Sun Haoyang / 1240001201 | Registered comparisons and diagnostics. Integrated evidence, audits and reports. |
| Li Yangshuo / 1240001156 | Independent account rerun. Supplementary audit, PR #3. Report traceability, PR #5. |
| He Boyu / 1240000576 | Four-thread evidence audit. Twostage source analysis and five witness replays, PR #4. |

Original contributions and assistance statements appear in report section 10.

### Chinese speaker notes

按实际提交范围说明贡献。孙皓扬组织协议、研究与整合；李扬烁贡献独立account宿主，并在PR #3做二次证据审查，在PR #5核对报告数值与引用；何博宇贡献四线程核数和twostage机制及五次重放。检查同一批数据可以形成有效审查贡献，应与原始测量归属区分。实施、执行和写作辅助详见报告使用声明。演示可以选报告Table 4的65与136，沿summary、records、原日志Round/Total行追溯，再展示make audit实际结果。

### Sources

- [Group report, section 10 and contribution table](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/2de378771adbeeced2709f9bc4ca436799848197/report/EXPANDED_REPORT.md)
- [Contribution record](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/2de378771adbeeced2709f9bc4ca436799848197/docs/CONTRIBUTIONS.csv)
- [Li Yangshuo report traceability PR #5](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/5)
- [He Boyu twostage PR #4](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/4)

## Slide 14: Verdict and remaining question

### English screen text

- C1: Partially supported
- C2: Supported within the stated comparison
- Overall: Partially reproduced
- Remaining question: why do failure observations vary under identical requests?

Verification entry point: make audit

### Chinese speaker notes

结论集中在证据允许的范围：五个程序的PERIOD枚举总数匹配，四个案例相对明确适配的序列化驱动减少请求数，一个持平；首次失败和部分失败调度数存在偏差。容量修正验证了一个接口问题并改变反馈，但差距保留。twostage给出一个具体缺陷的必要偏序和选定见证的五次重放证据。下一步因果定位需要验证过的真实执行轨迹。展示结束时给出仓库与make audit入口，听众可复查已有证据。

### Sources

- [Group report, verdicts and limitations](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/2de378771adbeeced2709f9bc4ca436799848197/report/EXPANDED_REPORT.md)
- [Repository and reproducibility instructions](https://github.com/Sasuke-666/CS340-Research-Paper-Replication)
