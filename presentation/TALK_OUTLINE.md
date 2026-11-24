# PERIOD replication: talk and defence outline

Content revision: 25 November 2026, Macau/Beijing time (v1.0.2).
Use this outline with the [fourteen slides](SLIDES.md). It explains the results
in Chinese, gives concise English messages and provides an offline demonstration
and answers to likely questions. The [report](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/v1.0.2/report/EXPANDED_REPORT.md)
contains the full analysis. Confirm the official duration and speaking
arrangements before choosing how much of the material to present.

## 1. The problem and method

**English message:** Concurrent failures depend on thread interleavings.
PERIOD groups key operations into execution periods and explores bounded
schedules systematically.

同样的输入，线程访问共享变量的顺序一变，程序就可能出错。PERIOD 用 period
给关键操作划分执行阶段：前一个阶段完成，后一个阶段才能开始。最后一个
period 可以容纳多个线程的剩余操作。驱动提出调度请求、运行程序、读取反馈，
再决定后续探索；已执行路径的信息因此能够参与下一步搜索。[S1，§2.2、§3]

解释 period 时，可以用一个概念例子：先运行 T0 的指定前缀，再运行 T1 的指定
前缀，最后让剩余工作并行。注明这是机制示意；若展示论文原图，标明作者、论文
和图号。

## 2. Our two questions

**English messages:**

- C1: Can we reproduce the selected Table 2 results with the released implementation?
- C2: Under the released drivers' respective depth rules, does PERIOD search
  fewer schedules than the adapted serialized driver and still expose the failure?

C1 对照三个指标：首次失败位置、枚举总数和错误调度数。C2 把两种方法放在
同一个宿主、程序、输入和已构建二进制上比较。选取的五个案例是 `reorder_3`、
`reorder_4`、`account`、`lazy01` 和 `twostage`，来自四个程序系列；结论适用于
这组有目的选取的小规模样本。[S2，§1–§3；S3]

depth 是发布版驱动的 bug-depth 参数 d。PERIOD 遍历 p=2 到 d+1，序列化驱动
遍历 p=N 到 d+N−1，N 是开始枚举时观测到的线程数。例如，三线程取 d=3，
两种驱动分别覆盖 2、3、4 和 3、4、5 个 period；双线程 twostage 则都覆盖
2、3、4。C2 比较的是这两套发布配置，包括它们保留的驱动差异。要单独判断
调度器的效果，还需要进一步控制实验。[S2，§2]

序列化方法在图表中统一标为 `author_serialized_abi16`。原作者旧驱动与当前
运行时的共享内存接口不兼容，本组按记录的补丁做了最小适配。这个发布版本与
论文当年的 Serial 可执行程序是否完全相同，现有材料还无法确认。[S2，§5.1；S4]

## 3. Design and evidence accounting

**English message:** Report attempts, completed calls and matched pairs
separately. Failed and censored attempts remain part of the record.

| Evidence scope | Attempts and completed results | Use in the analysis |
| --- | --- | --- |
| Main compatible comparison | 100 attempts; 90 complete; 10 serialized four-thread outer timeouts | Four cases provide 40 complete pairs; primary PERIOD four-thread values stay in their own batch |
| Registered four-thread follow-up | 6 complete calls at a 240-second outer limit | 3 complete pairs on its follow-up host |
| Combined accounting of those two scopes | 106 attempts, 96 complete calls | 43 complete pairs; timings remain within their case and host |
| Li Yangshuo's separate `account` rerun | 20 complete calls, 10 per method | Independent host corroboration; separate statistics |
| Readable capacity diagnostic | 40 complete calls across two case/host scopes | 10 complete pairs per case; separate statistics |
| He Boyu's `twostage` witness study | 5 completed replays of one selected input | Separate build/host observation; no paired exploration design |
| 22 November engineering acceptance | 30 complete comparison calls; 40 additional diagnostic calls | 15 comparison pairs across five separate case hosts; independent n=3 summaries |

一次完整配对需要同批次的两个条件都完整结束。主批次的四线程 PERIOD 虽有
十次完整观测，对应的十次序列化调用却都超时，所以这一部分没有完整耗时配对。
后续研究在新宿主上把外层时限增加到 240 秒，两种方法重新各运行三次，形成
三对完整结果。[S2，§2–§5；S5]

容量诊断研究另一个问题：读取接口的布局是否影响运行结果。它先以 `bddb831`
登记协议，再在每个案例内比较容量 1,990 和 3,964。两个条件都运行 PERIOD，
只改驱动中的容量常数，原生运行时和已构建目标保持相同。[S8]

原工作流 `43570556202` 中，`lazy01` 有 20 次完整且合格的调用、10 对。[S12]
原 `account` 作业失败后，最终 artifact 列表中没有它的档案，日志端点返回 404。
因此，这个作业的尝试数、完整数和工作负载失败原因都记为未知。[S10]
恢复协议 `ea273fe4` 发布后，新的 `43575584325` 在另一宿主固定运行 `account`
十对。20 次调用全部完整且合格，结果同时保存为 Git 归档和备用 ZIP。[S11；S13]
原作业的缺失结果与恢复批次分列，未知尝试数也继续记为未知。

11 月 22 日验收先以 `2de3787` 登记，再执行 `45015126850` attempt 1。
五个程序各在新宿主运行两种方法，每种三次，共 30 次、15 对；另有 40 次
reorder_3 固定见证诊断，两种倍率各 20 次。所有比较都完整结束，无内外层超时
或预算截断。这说明构建和执行入口在记录环境中通过了验收。它使用自己的
n=3 汇总，与历史 106/96/43 分列；未来换宿主后的失败位置仍可能变化。[S17]

## 4. The clearest result

**English message:** PERIOD explored fewer schedules in four of the five
matched cases; twostage tied.

| Case | PERIOD | Adapted serialized driver | Reduction |
| --- | ---: | ---: | ---: |
| reorder_3 | 27 | 30 | 10.00% |
| reorder_4 | 100 | 384 | 73.96% |
| account | 65 | 136 | 52.21% |
| lazy01 | 39 | 60 | 35.00% |
| twostage | 33 | 33 | 0.00% |

展示报告 Figure 2。四线程这一行来自后续批次，n=3；其余各行 n=10。总调度数的
样本标准差都为零，每次完整运行也都发现了目标错误。这是 C2 最直接的依据：
在这组比较条件下，四个案例用较少的请求完成了搜索。[S2，Table 4；S5]

## 5. The discrepancies that matter

**English message:** The exploration totals match the paper, while several
failure metrics still differ.

主批次 `account` 的 PERIOD 首次失败均值为 10.100 ± 0.316，论文参考值为 2，
差 8.100，即 +405.00%。`lazy01` 的均值为 8，论文为 3。报告把这些差距与
匹配的枚举总数一起呈现。[S2，Table 2]

看逐次记录，更容易理解这些均值。account 有九次在第 10 个请求首次失败，
一次在第 11 个；lazy01 十次都在第 8 个。它们与论文的偏移每次都存在。
twostage 有九次在第 4 个、一次在第 17 个，较晚的那次把均值拉到 5.300。
它的错误调度数九次为 2、一次为 1，十次都低于论文的 3。频数说明了重复观测
怎样构成均值和波动，具体执行顺序仍需轨迹证据解释。[S2，§3]

李扬烁独立 `account` 批次的 PERIOD 首次失败位置为 8.8 ± 2.044，调度总数仍是
65 ± 0；序列化方法分别为 4 ± 0 和 136 ± 0。这台宿主支持相同的搜索量比较，
PERIOD 的首次失败位置仍高于论文的 2。CPU、内核、校准和执行环境同时变化，
所以跨批次差值还无法归结到某一个因素。[S6]

### What changed in the capacity experiment?

11 月 14 日的诊断先定位字段偏移，再只改变容量常数，最后看运行结果。
对应协议、补丁和日志给出了控制条件。这里要用原 `lazy01` 批次和恢复的
`account` 批次分别说明结果。[S8；S10]

`lazy01` 两臂各十次，全部完整且无内外层超时。修正前、后首次失败位置为
8.500 ± 1.581 和 8.200 ± 0.422；错误调度数为 11.600 ± 0.843 和
9.900 ± 1.912，均为均值 ± 样本标准差。两臂各请求 39 个调度，打印的序列相同。
默认反馈哈希从 8 变为 185,480，说明修正确实影响了反馈读取。修正后的首次
失败仍高于论文的 3。哈希是辅助 stdout 记录，其大小没有覆盖率百分比的含义。
[S12；S2，§8]

`account` 恢复批次也有两臂各十次完整且合格的观测。修正前、后首次失败为
10.500 ± 0.850 和 10.200 ± 0.632；错误调度数为 22.900 ± 3.281 和
24.300 ± 1.767。两臂各请求 65 个调度，每对请求序列相同；默认反馈哈希从
18 变为 196,202。修正后的首次失败仍比论文的 2 高 8.2，即 +410.00%。
这些数值都来自恢复宿主，原 account 作业的结果仍然未知。[S13]

两个案例的首次失败位置配对均值差都是 -0.300，样本标准差分别为
1.337（`lazy01`）和 1.160（`account`）。错误调度数的配对均值差分别为
-1.700 和 +1.400。可以据此得出：字段解码已对齐、反馈哈希改变、请求枚举保持
相同，而首次失败差距仍在；失败数量的变化方向因案例而异。这里使用同案例内的
描述性统计，同宿主重复运行是否独立还没有额外证据。

### Why can the same request lead to different observations?

`account` 提供了一个具体例子。初值是 `x=1, y=2, z=4`，存款和取款都完成后，
余额为 -1，故意写错的断言却要求 -5。历史日志的第二个请求
`[[1,1,1],[0,0,2,2,2]]` 把检查线程和取款线程放在同一个最后 period。
如果取款先获得互斥锁，检查线程随后就会看到两个完成标志，进入错误断言；
如果检查线程先获得锁，`withdraw_done` 仍为假，条件分支会跳过断言。
源码允许这两条执行路径。要判断某次记录实际走了哪一条，还需要经过验证的
执行轨迹。[S2，§8.3；S9]

### Twostage source mechanism and the member replay

**English message:** Separate field locks let the reader observe a partially
published update. The source and assertion identify a necessary partial order.

默认输入只有一个写线程 A 和一个读线程 B。A 在第一把锁下写入字段 1=1，
解锁后再在第二把锁下更新字段 2。B 通过第一个字段的非零检查，保存 t1=1，
再读取第二个字段。到达第 48 行断言，说明 B 保存了 t2=0，违反 t2=t1+1。
这就是由源码和断言推出的必要偏序。A 是否在 B 取样后、断言终止前已经写入 2，
原记录没有给出答案。因此，表格标为“source-derived partial order”。[S14]

何博宇选择主批次 PERIOD 第 1 次运行、第 4 个请求的错误见证，在 11 月 15 日的
新宿主上连续重放五次，五次都在重放标记之后出现 funcB 第 48 行断言。
重建目标的记录哈希与原归档一致。输入是见证第一行的 yield 矩阵，后面的历史
报错文字不传给目标程序；是否触发断言要检查实际输出，单看驱动返回 0 不够。
[S14；S15]

这五次重放描述这个输入在记录构建和宿主上的结果，单独计数。reorder_3 早期
的 4/5 和后来两批每种倍率 20/20 也各自保留；早期那一次为什么未触发，仍没有
得到解释。它们与 twostage 使用不同程序和输入。[S2，§5.4–§5.5]

## 6. A controlled extension

**English message:** On `reorder_3`, depth 2 detected the known failure while
exploring fewer schedules than depth 3.

深度扩展每种条件运行三次。depth 1、2、3 的枚举数分别为 3、13、27，发现错误的
运行数为 0/3、3/3、3/3；depth 2 比 depth 3 少探索 51.85%。这展示了该程序上的
搜索成本与覆盖范围取舍。depth 1 的结果表示这个边界内未观察到失败；较深设置
中的多条失败调度也可能指向同一个缺陷。[S2，§6]

九份日志呈现出相同的嵌套结构：3 个 depth-1 请求和 13 个 depth-2 请求，都是
27 个 depth-3 请求的前缀。depth 3 依次包含 3 个两 period、10 个三 period、
14 个四 period 请求。depth 2 和 3 的六次运行都在第 6 个请求
`[[0],[2],[0,1,1]]` 首次失败，位于新增的三 period 层。

源码中的 setter 依次写 `a=1`、`b=-1`，checker 只接受 `(0,0)` 或 `(1,-1)`。
这个请求分开一个 setter 的首个关键点和剩余工作，让 checker 有机会在中间
读取 `(1,0)`。解释依据是请求顺序和源码，原记录没有逐条内存操作轨迹。[S2，§6]

## 7. Evidence demonstration

用 11 月 22 日验收中的六份 twostage 日志，展示一个统计值怎样从原始输出算出来。
演示与 Slide 13 一致。提前下载这些文件，现场就不依赖网络。[S17–S18]

1. 打开[验收范围记录](../results/2026-11-22/summaries/acceptance-45015126850-attempt1/acceptance.json)。先定位 twostage：它占这批 30 次比较中的 6 次；11 月 15 日的 5 次单见证重放另列。
2. 打开 [twostage records.json](../results/2026-11-22/acceptance-45015126850-attempt1/twostage/records.json)，确认两种方法各三次、三个配对和 240 秒外层上限。
3. 在[序列化第二份日志](../results/2026-11-22/acceptance-45015126850-attempt1/twostage/author_serialized_abi16_r02.txt)中，找到 `test 0029` 后第一个 `[Error Found]`。`NO.1` 是报错序号，对应的请求位置为 29。
4. 另外两次首次失败位置都是 4。三个数 4、29、4 给出均值 `37/3 = 12.3333`，样本标准差 `25/√3 = 14.4338`。三次都枚举了 33 个请求，每次完整搜索可能触发多个失败请求。
5. 运行下面的复算命令，再对照[独立汇总](../results/2026-11-22/summaries/acceptance-45015126850-attempt1/SUMMARY.md)。文件摘要检查完整性，从日志重算则检查统计口径。

从仓库根目录运行：

```sh
python3 scripts/recount_twostage_acceptance.py
```

命令核对六份原始日志、完成状态和六项已发布统计。PERIOD 首次失败位置为
4、4、4；序列化为 4、29、4；两种方法的枚举均值都是 33。输出还列出每份日志的
失败请求 ID。整个演示只读归档，现场无需重放见证或启动新工作负载。时间较短时，
讲第 3–5 步即可，其他文件留作答疑。项目级 `make audit` 则可复查全部归档研究，
检查日期与原实验日期分别记录。

### Contribution attribution

孙皓扬组织实验协议、组内测量、仓库整合和报告。李扬烁提交独立 account 宿主
结果，随后在 PR #3 补充序列与来源审查，在 PR #5 核对报告追溯路径和正文图表
引用。何博宇提交四线程核数，在 PR #4 提交 twostage 源码、偏序说明和五次重放，
再在 PR #6 复算组内验收的六份日志并修改展示内容。

11 月 24 日，何博宇在 PR #7 提交三项合成日志回归测试：完整日志的指标计数、
同一请求的重复报错按一个失败调度计数，以及摘要匹配但缺少结束标记时拒绝接收。
李扬烁在 PR #8 提交 v1.0.1 发布与原生 Windows 核验、验收档案独立重算、
解析器加固和验证证据清单。其独立脚本复算原有 30 次比较，并对照 JSON、CSV
和 Markdown 汇总。两项 PR 均未新增实验调用。[S19–S20]

最终整合中的校验边界修复与日期校正，另列为孙皓扬授权的维护工作。原成员提交
和整合修改保留各自的提交记录，原始测量仍属于对应的实验批次。

贡献按原始 PR 和提交记录说明。二次审查与原始测量分别归属，实施、执行和写作
辅助见报告使用声明；个人讲解情况以成员实际参与为准。[S2，§10；S14–S20]

准备时可这样分工：孙皓扬讲研究问题、控制设计和各批次样本；李扬烁讲独立宿主
和数字追溯；何博宇讲 twostage 的必要偏序和六日志复算。每个人都练习回答
“观察到了什么、还有什么不清楚、证据在哪里”。发言和交叉复核完成后，再记录
实际参与者与日期。

## 8. Questions to prepare

| Likely question | Accurate response and evidence |
| --- | --- |
| Why is the conclusion only partially reproduced? | Selected enumeration totals agree; several first-failure positions and buggy counts differ. See report Tables 2–3 and C1 verdict. |
| Is a buggy schedule a distinct bug? | It is a schedule whose execution exposed a failure. Multiple schedules can expose one defect. The report does not count each as a new defect. |
| Does the first failing schedule measure time to bug? | It is a one-based enumeration position. Whole-driver elapsed time includes calibration and other work; time to the first error was not separately measured. |
| Is 120 seconds the serialized completion time? | The ten runs were stopped at the outer bound. Their completion times and final totals are missing; the observed prefixes remain available. |
| Why did the old serialized driver crash? | Source and syscall evidence supports the shared-memory size/type incompatibility; archived probes and the scoped adapter are in report §5.1. |
| Does depth 3 impose the same period bound on both drivers? | PERIOD enumerates p=2 through d+1; the released serialized driver enumerates p=N through d+N−1. Three threads at d=3 give 2–4 versus 3–5 periods; two-thread twostage gives 2–4 for both. C2 concerns the released configurations. See report §2. |
| Does the adapter prove historical Serial identity? | Its changes are documented and the serialized scheduling section is preserved. Other released-driver differences remain, and the exact historical executable is unverified. |
| Is the result a general speedup? | Timing observations concern the specified implementations within matched cases and hosts. Case totals and host times are not pooled into a universal speedup. |
| Why preserve the replay miss? | The original fixed witness hit 4/5. Later two-setting diagnostics each hit 20/20 per setting and did not explain that miss. These batches retain separate scopes. |
| Does a zero standard deviation prove determinism? | It describes the observed repeated metric. Execution traces and other failure metrics can still vary, and a finite sample does not establish universal behavior. |
| How can identical requested schedules produce different failure observations? | A shared final period can permit different mutex-acquisition orders. The `account` source gives a conditional example; a validated execution trace is required to attribute a particular recorded outcome. See report §8.3 and S9. |
| How is the missing original account archive handled? | The failed job, absent artifact and unavailable logs remain documented. Its attempt/completion counts and failure cause are unknown. A registered recovery uses a new host and keeps its observable results separate. See S10. |
| What did each member do? | Name the actual commits and evidence in [the contribution record](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/v1.0.2/docs/CONTRIBUTIONS.csv); distinguish submitted work from human review or explanation still awaiting completion. |
| Is the twostage table an observed instruction trace? | It gives a source-derived necessary partial order and the observed assertion. Exact preemption points, a unique lock order and final shared-state values remain unknown. See S14. |
| What does the twostage 5/5 replay result establish? | Five consecutive calls replayed the selected witness and produced the matching assertion on the recorded build and host. It supplies no unconditional or cross-host reliability guarantee. See S15. |
| Does the account supplementary review claim new measurements? | PR #3 analyses existing evidence and adds request-sequence checks. PR #5 audits report traceability and improves narrative figure/table callouts. Their contribution scopes remain separate from original measurements. See S16. |
| Is the 22 November acceptance part of the original 106/96/43 accounting? | It is a separate registered engineering batch: 30 complete comparisons, 15 pairs and 40 additional diagnostics on new hosts. Historical statistics are unchanged. See S17. |
| Did PR #6 produce six new twostage runs? | It independently recounts six already archived acceptance calls and improves the presentation. The original group acceptance and the member's secondary review have separate attribution. See S18. |
| Did PRs #7 and #8 add measurements? | PR #7 adds three synthetic-log regression tests. PR #8 checks release and Windows evidence, recounts the existing acceptance archive, and strengthens parsers and evidence provenance. Original measurement counts remain unchanged. Integration repairs have separate attribution. See S19–S20. |

## 9. Closing message

**English message:** PERIOD explored fewer schedules in four of our five cases
against the adapted released baseline. Correcting the capacity aligned the
fields and changed the feedback, but first-failure gaps remained in both cases.
Our overall verdict is partial reproduction.

结束时给出报告、复现命令和证据入口。听众可以沿同一条路径检查今天展示的结果，
也能看到仍待解释的问题。

## Sources

- S1. Wen et al. *Controlled Concurrency Testing via Periodical Scheduling*,
  ICSE 2022, DOI: 10.1145/3510003.3510178.
  [Original paper](https://wcventure.github.io/pdf/ICSE2022_PERIOD.pdf),
  sections 2.2 and 3 for the method; Table 2 for paper references.
- S2. [Expanded report](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/v1.0.2/report/EXPANDED_REPORT.md), with numbered tables,
  figures, scoped verdicts and original data references at the `v1.0.2` revision.
- S3. [Registered comparison protocol](../experiments/2026-11-07/COMPARISON_PROTOCOL.md).
- S4. [Compatibility protocol](../experiments/2026-11-07/COMPATIBILITY_PROTOCOL.md)
  and [source/attribution record](../docs/SOURCES.md).
- S5. [Four-thread follow-up summary](../results/2026-11-07/summaries/comparison-42384122902/SUMMARY.md).
- S6. [Member account rerun](../docs/reviews/1240001156-clean-run.md)
  and [its summary](../results/member-reruns/1240001156-account-20261108T122201Z-summary/SUMMARY.md).
- S7. [Four-thread evidence review](../docs/reviews/1240000576-evidence-audit.md).
- S8. [Registered one-factor layout protocol](../experiments/2026-11-14/LAYOUT_PROTOCOL.md),
  published as `bddb831` before the measurements, and
  [the study workflow](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/43570556202).
- S9. [Archived original account source](../results/2026-11-07/comparison-42381922637/account/source/account_bad.c),
  [its historical requested-schedule log](../results/2026-11-07/comparison-42381922637/account/period_r01.txt),
  and the conditional source explanation in the
  [diagnostic review](../docs/LAYOUT_DIAGNOSTIC_REVIEW_20261114.md).
- S10. [Original account evidence-availability failure](../experiments/2026-11-14/account-evidence-failure/FINAL_OBSERVATION.json).
- S11. [Fixed account recovery protocol](../experiments/2026-11-14/ACCOUNT_RECOVERY_PROTOCOL.md)
  and [its observed activation basis](../experiments/2026-11-14/ACCOUNT_RECOVERY_ACTIVATION.json),
  published as `ea273fe4` before
  [recovery run 43575584325](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/43575584325).
- S12. [Audited lazy01 layout summary](../results/2026-11-14/summaries/layout-43570556202-lazy01/SUMMARY.md),
  original run `43570556202`, 20 complete calls and ten complete pairs.
- S13. [Audited account recovery summary](../results/2026-11-14/summaries/layout-recovery-43575584325-account/SUMMARY.md),
  new-host run `43575584325`, 20 complete calls and ten complete pairs.
- S14. [Twostage source and assertion analysis](../docs/reviews/1240000576-twostage-witness-review.md)
  and [source-derived partial order](../docs/reviews/1240000576-twostage-trace.md),
  submitted in [PR #4](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/4).
- S15. [Five-call twostage replay record](../results/member-reruns/1240000576-twostage-43681034375/README.md),
  original measurement run `43681034375`, 15 November 2026.
- S16. [Supplementary account provenance audit](../docs/reviews/1240001156-account-supplement.md),
  [PR #3](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/3), and
  [PR #5 report traceability audit](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/5),
  submitted 22 November 2026, Macau/Beijing time.
- S17. [Registered fresh-host acceptance protocol](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/2de378771adbeeced2709f9bc4ca436799848197/experiments/2026-11-22/ACCEPTANCE_PROTOCOL.md)
  and [independent acceptance receipt](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/8b3102c64214e53782ca0496b61c81f50fb17ff1/results/2026-11-22/summaries/acceptance-45015126850-attempt1/acceptance.json),
  original run `45015126850`, attempt 1, 22 November 2026.
- S18. [He Boyu's six-log recount and presentation review](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/2aea86e1f35fdd8f2b482aec5f4b65b0568f0c9a/docs/reviews/1240000576-presentation-check-20261122.md)
  and [PR #6](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/6),
  submitted 22 November and integrated 24 November 2026; secondary analysis of the group acceptance archive.
- S19. [He Boyu's synthetic twostage regression tests](../tests/test_recount_twostage_acceptance.py)
  and [PR #7](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/7),
  submitted 24 November 2026. Three synthetic fixtures test recount semantics and incomplete-log rejection.
- S20. Li Yangshuo's [release and Windows audit](../docs/validation/1240001156-release-windows-audit-20261124.md),
  [acceptance parser review](../docs/validation/1240001156-acceptance-parser-hardening-20261124.md),
  [independent metrics and evidence manifest](../docs/validation/1240001156-evidence-chain-20261124.md),
  and [PR #8](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/pull/8),
  submitted 24 November 2026. These audits verify existing evidence and keep original measurement ownership.
