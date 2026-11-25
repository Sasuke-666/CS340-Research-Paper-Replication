# CS340 PERIOD 最终提交修订 v1.0.3

本次交付供孙皓扬、李扬烁和何博宇三人提交与答辩使用。组长于 2026 年 11 月 25 日转述了教师对三人组的确认。附件包括英文报告 PDF 和 Word、含中文备注的可编辑 PPTX 和演示 PDF、中文手册 Word 和 PDF，以及完整源码证据 ZIP。课程要求的 v1.0 和后续 v1.0.1、v1.0.2 均保留。

五个案例的 PERIOD 枚举总数与论文一致，与兼容序列化驱动相比四个减少、一个持平。首错位置与触发失败的请求数仍有差异，总体结论为部分复现。历史比较和四线程后续共 106 次尝试、96 次完整、43 对完整配对。深度、容量、成员实验与 11 月 22 日验收分别统计。本次修订没有新增基准调用。

在 ZIP 的 Repository 目录下运行 `python3 scripts/recount_twostage_acceptance.py`，可离线核对报告中三对 twostage 的结果。完整核验可运行 `make check` 和 `make audit`。源码、文档摘要和 Linux／Windows 核验入口见 [本版验证记录](https://github.com/Sasuke-666/CS340-Research-Paper-Replication/blob/v1.0.3/docs/FINAL_VALIDATION_V1_0_3.md)。ZIP 中的 DELIVERY.json 记录交付提交。

本版同步了三人名单、答辩分工和六份文档的生成路径，也修复了归档解析与汇总输出边界。正式提交入口、课程回执及三人的现场讲解按实际课程记录确认。
