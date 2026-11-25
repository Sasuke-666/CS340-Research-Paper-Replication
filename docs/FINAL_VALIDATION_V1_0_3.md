# v1.0.3 复核与交付记录

2026 年 11 月 25 日，组长转述教师已确认本组三人。复核从公开仓库 main 的 `eb2ea3f69034ceca9905e9aebeea8da663af7779` 开始。该提交的 [原检查](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/45482060186) 对应 v1.0.2。

本轮在 macOS 27.2（26B123）、arm64 Apple M5、24 GiB 内存上审查现有归档和文档。基准数据来自各自原宿主，最新的完整构建和调用见 [11 月 22 日验收](VALIDATION_20261122.md)。[交付清单](../submission/FINAL_RELEASE.json)记录本版源码与交付文件的关系，压缩包 DELIVERY.json 记录完整交付提交。


原论文第 8 页 §4.1.3 与第 9 页表 2 已从[作者提供的 PDF](https://wcventure.github.io/pdf/ICSE2022_PERIOD.pdf)核对。五例两方法的 30 个参考值与报告一致，四幅图的误差条均为样本标准差。教师文件的取得范围见[课程依据](COURSE_REQUIREMENTS.md)。

修复前，通用比较解析器可统计测量区间以外的请求；部分汇总目标可通过链接改写既有文件。修订后，解析器检查测量首尾和事件位置，汇总文件先写入临时位置。早期 pilot 的派生 CSV 将有符号差与非负绝对差分列。原始测量、超时记录、成员原始提交与原始命令记录均保留。

`make deliverables` 从报告、手册和演示各自的源生成六份文件。中文手册使用支持简体中文的 LibreOffice 字体；英文报告 PDF 嵌入姓名的八个汉字。ZIP 保留 Git 记录的可执行位。

## 源提交检查

在干净的 main 源提交 `a1a21dc9c2dee1a5776224dad5e50f40dd2e230d` 上，使用 CPython 3.12.14、GNU Make 3.81、Git 2.54 和仓库锁定的文档依赖。原生 Cairo 从本地库目录加载。LibreOfficeDev 26.8 使用 Noto Sans CJK SC Regular/Bold 字体配置。

| 实际命令 | 范围与结果 |
| --- | --- |
| `make check audit`（项目 Python） | 193 项单元测试全部通过。历史、成员、容量、验收、验证清单及报告统计审计通过。 |
| `python3 scripts/recount_twostage_acceptance.py`（也由 audit 调用） | 六条档案日志，PERIOD 首错 4、4、4；兼容序列化首错 4、29、4，均值 12.3333，样本 SD 14.4338。 |
| `make -j3 deliverables`（项目 Python） | 在 report/export 生成报告、演示和手册的六个文件。 |
| `git diff v1.0.2 a1a21dc9c2dee1a5776224dad5e50f40dd2e230d -- results/ experiments/ docs/reviews/ docs/validation/` | 差异仅为 pilot/summary.csv 的派生差值列；原始测量和成员验证记录逐字节保留。 |
| [源码的 Repository checks](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/45516659321) | Ubuntu Python 3.9、3.12 和 Windows 归档检查通过，源码阶段清单为 preparing。 |

## 逐页和结构复核

英文报告 PDF 共 18 页，Word 另行渲染为 16 页。逐页核对了正文、跨页表头、图表和姓名；四幅图和 14 张表共 493 个数据及表头单元格均与源文档对应。Word 和 PDF 有相同的 36 个不同超链接目标。PDF 作者和贡献处的汉字均用内嵌字体显示。Word 首页一个姓名跨行，三个字与学号均完整。

演示 PDF 和 PPTX 渲染的 14 页逐页检查，正式输出与已检查的参考页逐像素一致。PPTX 的 9 张可编辑表格、1 张原生图表、1 个内嵌工作簿和 14 页中文备注均保留；图表、工作簿字节与旧版一致。49 处备注超链接对应 34 个不同地址，逐一读取均返回 HTTP 200。新源提交链接与历史证据链接分别固定在对应版本。

中文手册的 Word、PDF 均为 3 页。修正本机渲染器的中文字体配置后，PDF 内嵌中文正体和粗体。实际查看三页，并将交付 PDF 与独立 Word 渲染逐页像素对照。22 处 Word 链接对应 20 个不同目标，与 PDF 一致。登记表公开入口显示停止接收，未查询任何答卷，个人回执状态仍待核对。

## 定位交付提交

[六个文件与来源的 SHA-256](../submission/FINAL_RELEASE.json)绑定到上述源提交。交付提交以 [v1.0.3 标签](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/releases/tag/v1.0.3)和 ZIP 中 DELIVERY.json 的 repository_commit 为准。该提交自己的 Repository checks 通过后，发布作业逐项比对六份文件与完整 ZIP 的远端摘要。使用标签所指提交核对 [GitHub 检查记录](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/workflows/repository-checks.yml)。
