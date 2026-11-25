# v1.0.3 复核与交付记录

2026 年 11 月 25 日，组长转述教师已确认本组三人。复核从公开仓库 main 的 `eb2ea3f69034ceca9905e9aebeea8da663af7779` 开始。该提交的 [原检查](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/actions/runs/45482060186) 对应 v1.0.2。

本轮在 macOS 27.2（26B123）、arm64 Apple M5、24 GiB 内存上审查现有归档和文档。基准数据来自各自原宿主，最新的完整构建和调用见 [11 月 22 日验收](VALIDATION_20261122.md)。[交付清单](../submission/FINAL_RELEASE.json)记录本版源码与交付文件的关系，压缩包 DELIVERY.json 记录完整交付提交。


原论文第 8 页 §4.1.3 与第 9 页表 2 已从[作者提供的 PDF](https://wcventure.github.io/pdf/ICSE2022_PERIOD.pdf)核对。五例两方法的 30 个参考值与报告一致，四幅图的误差条均为样本标准差。教师文件的取得范围见[课程依据](COURSE_REQUIREMENTS.md)。

修复前，通用比较解析器可统计测量区间以外的请求；部分汇总目标可通过链接改写既有文件。修订后，解析器检查测量首尾和事件位置，汇总文件先写入临时位置。早期 pilot 的派生 CSV 将有符号差与非负绝对差分列。原始测量、超时记录、成员原始提交与原始命令记录均保留。

`make deliverables` 从报告、手册和演示各自的源生成六份文件。中文手册使用支持简体中文的 LibreOffice 字体；英文报告 PDF 嵌入姓名的八个汉字。ZIP 保留 Git 记录的可执行位。完整交付时，本记录在交付提交补入实际源提交、检查结果和版面核验。
