# PERIOD replication: talk and defence outline

Prepared for group study on 14 November 2026. This is a content outline, not a
fixed slide count, time allocation or claim of completed presentation. Official
presentation requirements remain to be verified. The maintained
[report](../report/EXPANDED_REPORT.md) is authoritative for the latest findings.

## 1. The problem and method

**English message:** Concurrent programs can fail under particular thread
interleavings. PERIOD organizes key operations into execution periods and
systematically explores bounded schedules.

中文讲解：同样的输入，线程以不同顺序访问共享状态，可能得到不同结果。
PERIOD 把关键操作放进有先后关系的 period；前一个 period 结束，后一个才执行。
其实现允许不同线程的操作进入最后一个共同 period。生成器、执行器和反馈分析器
组成循环，已执行路径的信息继续指导搜索。[S1，§2.2、§3]

可用一个自拟的概念例子说明 period 的先后约束：先完成 T0 的指定前缀，再让
T1 的指定前缀运行，最后让剩余工作并行。这个例子只解释机制，不充当本组测量。
如果使用论文原图，应明确标注作者、论文及图号。

## 2. Our two questions

**English messages:**

- C1: Do the selected Table 2 results reproduce with the released implementation?
- C2: Does PERIOD explore fewer schedules than the explicitly adapted serialized
  driver while still exposing the target failure?

中文讲解：C1 对照论文中的首次失败位置、枚举总数和错误调度数。
C2 在相同宿主、程序、输入和已构建二进制上比较两个具体实现。
五案例为 `reorder_3`、`reorder_4`、`account`、`lazy01`、`twostage`，来自四个程序系列。
这是有目的的小规模选择，结论覆盖这批条件。[S2，§1–§3；S3]

序列化方法名称始终使用 `author_serialized_abi16`。原作者旧驱动与当前运行时存在
共享内存接口不兼容，本组按已记录补丁完成最小适配。论文历史 Serial 可执行程序
与这个发布版本的同一性尚未建立。[S2，§5.1；S4]

## 3. Design and evidence accounting

**English message:** Keep attempts, completed observations and matched pairs
separate; preserve every failed or censored attempt.

| Evidence scope | Attempts and completed results | Use in the analysis |
| --- | --- | --- |
| Main compatible comparison | 100 attempts; 90 complete; 10 serialized four-thread outer timeouts | Four cases provide 40 complete pairs; primary PERIOD four-thread values stay in their own batch |
| Registered four-thread follow-up | 6 complete calls at a 240-second outer limit | 3 complete pairs on its follow-up host |
| Combined accounting of those two scopes | 106 attempts, 96 complete calls | 43 complete pairs; timings remain within their case and host |
| Li Yangshuo's separate `account` rerun | 20 complete calls, 10 per method | Independent host corroboration; separate statistics |

说明：一次配对需要同批次的两个条件都完整结束。原批次四线程 PERIOD 的十次结果
仍是完整观测，但没有对应的完整序列化运行，因而不能组成十个完整耗时配对。
增加时限后的三对来自新宿主，两种方法都重新执行。[S2，§2–§5；S5]

新布局诊断按其独立协议和实际归档单列。讲解时使用发布报告中的真实样本数，
保留它与上述比较研究的不同问题和不同条件。
其预先登记提交为 `bddb831`；两个条件都运行 PERIOD，分别使用容量 1,990 和 3,964。
每个案例只有该驱动常数变化，原生运行时和构建好的目标程序相同。
它检验接口布局对行为的影响，未加入新的序列化比较方法。[S8]

原工作流 `43570556202` 的 `lazy01` 有 20 次完整且合格的调用、10 组完整配对。[S12]
原 `account` 作业已终止失败，最终 artifact 列表没有该案例档案，日志端点返回 404；
尝试数、完整数和工作负载失败原因均未知。[S10]
恢复协议先以 `ea273fe4` 发布，再启动 `43575584325`，固定在新宿主另做 `account`
十对，使用新的运行标识并独立分析。[S11]
恢复批次已完成 20 次尝试，全部完整且合格，共十对；Git 归档与备用 ZIP 均已保存。[S13]
它的新观测不能替代原作业的缺失观测，
也不能把原作业的未知尝试数记为零。演示按实际归档分别讲清案例和宿主范围。

## 4. The clearest result

**English message:** PERIOD explored fewer schedules in four of the five
matched cases; one case tied.

| Case | PERIOD | Adapted serialized driver | Reduction |
| --- | ---: | ---: | ---: |
| reorder_3 | 27 | 30 | 10.00% |
| reorder_4 | 100 | 384 | 73.96% |
| account | 65 | 136 | 52.21% |
| lazy01 | 39 | 60 | 35.00% |
| twostage | 33 | 33 | 0.00% |

用报告 Figure 2 展示。四线程行用独立后续批次 n=3，其余行 n=10。
总调度数的样本标准差为零。完整运行均发现目标错误；这些数字支持此范围内的
搜索量减少。[S2，Table 4；S5]

## 5. The discrepancies that matter

**English message:** Matching the schedule count does not guarantee matching
failure observations.

原主批次 `account` 的 PERIOD 首次失败均值为 10.100 ± 0.316，论文参考值为 2，
差 8.100，即 +405.00%。`lazy01` 为 8，对照论文 3。
这两个差异应与成功复现的调度总数一起讲清。[S2，Table 2]

李扬烁独立 `account` 批次的 PERIOD 首次失败位置为 8.8 ± 2.044，调度总数仍为
65 ± 0。序列化方法分别为 4 ± 0 和 136 ± 0。这一新宿主结果提供独立证据，
首次失败位置仍未复现论文的 PERIOD 值 2。宿主、校准和执行环境同时变化，
跨批次差值本身不能单独识别原因。[S6]

本周布局诊断的讲解应按“已观察到的接口差异—只改变的因素—实际结果—允许的结论”
展开。使用对应协议、补丁和原始日志说明控制条件。原 `account` 档案不可用的状态
与新宿主恢复研究分别记录，研究结论以可审计的真实结果为依据。[S8；S10]

`lazy01` 的正式布局对照两臂各十次，均完整且无内外层超时。修正前、后首次失败位置
为 8.500 ± 1.581 与 8.200 ± 0.422；错误调度数为 11.600 ± 0.843 与
9.900 ± 1.912，均为均值 ± 样本标准差。两臂都请求 39 个调度，打印的请求序列一致。
默认反馈哈希从 8 变为 185,480，说明实际反馈读取受到干预；修正后的首次失败仍高于
论文参考值 3。这个案例支持字段解码已对齐、观察到的反馈已改变，同时保留失败发现的
偏差。哈希值是辅助 stdout 证据，其数值变大不表示覆盖率更高。[S12；S2，§8]

`account` 恢复批次也有两臂各十次完整且合格观测。修正前、后首次失败为
10.500 ± 0.850 与 10.200 ± 0.632；错误调度数为 22.900 ± 3.281 与
24.300 ± 1.767。两臂都请求 65 个调度，每个配对的请求序列相同；默认反馈哈希
从 18 变为 196,202。修正后的首次失败仍比论文参考值 2 高 8.2，即 +410.00%。
该恢复批次在新宿主上独立分析，原作业的未知结果继续单列。[S13]

两个案例修正后的首次失败均值配对差都是 -0.300，样本标准差分别为
1.337（`lazy01`）和 1.160（`account`）。错误调度数的配对均值变化分别为
-1.700 与 +1.400，方向不同。可以明确陈述字段解码已对齐、实际反馈哈希改变、
请求枚举不变及首次失败偏差仍在；这些样本不支持统一的效果或性能提升结论。
均值和样本标准差是同案例内的描述性统计，不额外假设同宿主重复运行相互独立。

可以用 `account` 的源码解释“请求调度”和“实际交错”的关系。初值为
`x=1, y=2, z=4`；存款和取款都完成后，余额为 -1，而故意写错的断言要求 -5。
历史日志第二个请求 `[[1,1,1],[0,0,2,2,2]]` 把检查线程和取款线程放在共同的最后
一个 period。取款先获得互斥锁时，检查线程随后能看见两个完成标志并进入错误断言；
检查线程先取得锁时，`withdraw_done` 仍为假，条件分支跳过断言。
这是源码支持的条件解释；确定某一次记录实际走了哪条顺序，还需要验证过的执行轨迹。
它不能充当新批次某次结果的实测原因。[S2，§8.3；S9]

## 6. A controlled extension

**English message:** On the selected `reorder_3` program, depth 2 detected the
known failure while exploring fewer schedules than depth 3.

原深度扩展每个条件运行三次；深度 1、2、3 的枚举数分别为 3、13、27，
发现目标错误的运行数为 0/3、3/3、3/3。深度 2 相对深度 3 少探索 51.85%。
它说明这个程序上的覆盖与搜索成本取舍；深度 1 的未发现结果仅对应这个边界。
更深的设置发现更多触发失败的调度，但没有据此增加“不同缺陷”的数量。[S2，§6]

## 7. Evidence demonstration

选择一个能当场解释的数字，演示“报告—汇总—记录—原始日志—摘要校验”的路径。
建议使用四线程后续批次，因为六条调用及三对关系清晰。[S5；S7]

1. 在报告 Table 4 找到 PERIOD 100 与序列化 384。
2. 打开 `results/2026-11-07/comparison-42384122902/reorder_4/records.json`。
3. 对照 `period_r01.txt` 和 `author_serialized_abi16_r01.txt` 的完成标记与计数。
4. 解释 `(384 - 100) / 384 = 73.96%`，并展示另两对得到相同总数。
5. 说明清单摘要验证文件完整性，独立复算验证统计口径；两者各有用途。

演示现成归档或已准备好的复算命令即可。正式现场运行方式需结合最终展示要求。

## 8. Questions to prepare

| Likely question | Accurate response and evidence |
| --- | --- |
| Why is the conclusion only partially reproduced? | Selected enumeration totals agree; several first-failure positions and buggy counts differ. See report Tables 2–3 and C1 verdict. |
| Is a buggy schedule a distinct bug? | It is a schedule whose execution exposed a failure. Multiple schedules can expose one defect. The report does not count each as a new defect. |
| Does the first failing schedule measure time to bug? | It is a one-based enumeration position. Whole-driver elapsed time includes calibration and other work; time to the first error was not separately measured. |
| Is 120 seconds the serialized completion time? | The ten runs were stopped at the outer bound. Their completion times and final totals are missing; the observed prefixes remain available. |
| Why did the old serialized driver crash? | Source and syscall evidence supports the shared-memory size/type incompatibility; archived probes and the scoped adapter are in report §5.1. |
| Does the adapter prove historical Serial identity? | Its changes are documented and the serialized scheduling section is preserved. Other released-driver differences remain, and the exact historical executable is unverified. |
| Is the result a general speedup? | Timing observations concern the specified implementations within matched cases and hosts. Case totals and host times are not pooled into a universal speedup. |
| Why preserve the replay miss? | The original fixed witness hit 4/5. Later two-setting diagnostics each hit 20/20 per setting and did not explain that miss. These batches retain separate scopes. |
| Does a zero standard deviation prove determinism? | It describes the observed repeated metric. Execution traces and other failure metrics can still vary, and a finite sample does not establish universal behavior. |
| How can identical requested schedules produce different failure observations? | A shared final period can permit different mutex-acquisition orders. The `account` source gives a conditional example; a validated execution trace is required to attribute a particular recorded outcome. See report §8.3 and S9. |
| How is the missing original account archive handled? | The failed job, absent artifact and unavailable logs remain documented. Its attempt/completion counts and failure cause are unknown. A registered recovery uses a new host and keeps its observable results separate. See S10. |
| What did each member do? | Name the actual commits and evidence in `docs/CONTRIBUTIONS.csv`; distinguish submitted work from human review or explanation still awaiting completion. |

## 9. Closing message

**English message:** The selected study supports a bounded reduction in explored
schedules against one adapted released baseline. The capacity correction aligns
the decoded fields and changes observed feedback. First-failure gaps persist in
both audited cases. Our overall verdict is partial reproduction.

结束时展示当前报告、复现命令和证据入口，让听众能检查结论。所用样本、方法和
未解决问题应与最终发布版本一致。

## Sources

- S1. Wen et al. *Controlled Concurrency Testing via Periodical Scheduling*,
  ICSE 2022, DOI: 10.1145/3510003.3510178.
  [Original paper](https://wcventure.github.io/pdf/ICSE2022_PERIOD.pdf),
  sections 2.2 and 3 for the method; Table 2 for paper references.
- S2. [Expanded report](../report/EXPANDED_REPORT.md), with numbered tables,
  figures, scoped verdicts and original data references.
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
