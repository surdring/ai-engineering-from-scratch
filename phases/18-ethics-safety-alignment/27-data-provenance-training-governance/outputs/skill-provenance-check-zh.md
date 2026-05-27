---
name: provenance-check
description: 对照 California AB 2013 和 EU TDM 退出义务检查训练数据集。
version: 1.0.0
phase: 18
lesson: 27
tags: [data-provenance, ab-2013, tdm-opt-out, legitimate-interest, dpa]
---

给定部署使用的训练数据集，对照 California AB 2013 和 EU TDM 退出检查合规性。

生成：

1. **AB 2013 覆盖。** 填写 12 个字段。标记任何缺失或仅占位符的字段。注意摘要一旦发布即具有约束力。
2. **退出合规。** 数据集是否遵守机器可读的退出信号（robots.txt、C2PA「No AI Training」、TDM.Reservation）？必须具有采集前过滤。
3. **DPA 管辖区映射。** 对数据主体所属的每个管辖区，识别适用的 DPA 和 2025 年正当利益立场（Irish DPC、Cologne Higher Regional Court、Hamburg DPA、UK ICO、Brazilian ANPD）。
4. **不可逆性审计。** 如果数据集包含 PII，有什么遗忘或补救程序？承认没有程序能完全补救训练数据。
5. **溯源链完整性。** 从数据源到训练流水线是否有签名的链？如果数据集是衍生的（抓取 + 过滤），记录衍生过程。

硬性拒绝：
- 任何引用 AB 2013 但没有逐数据集 12 字段摘要的部署。
- 任何不遵守 robots.txt 或等效退出信号的部署。
- 任何假设可以从训练权重中精确移除数据的补救声明。

拒绝规则：
- 如果用户问特定数据集是否「安全可训练」，没有逐管辖区分析则拒绝。
- 如果用户要求通用合规策略，拒绝——各管辖区有实质性差异。

输出：一页检查，填写五个部分，识别最高风险合规缺口，并指出最紧迫的单一补救措施。各引用一次 California AB 2013 和 EU Copyright Directive TDM exception。