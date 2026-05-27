---
name: web-desktop-harness
description: 构建一个 WebArena/OSWorld 风格的测试夹具，包含基于执行的评估和轨迹效率指标。
version: 1.0.0
phase: 14
lesson: 20
tags: [webarena, osworld, harness, trajectory-efficiency]
---

给定一个目标应用（web 或桌面）和一个带标准轨迹的任务列表，构建一个评估夹具。

生成：

1. 任务定义：`(tid, description, gold_steps, success_predicate, state_reset)`。
2. 运行器：运行智能体，捕获每个动作，记录步骤数 + 耗时 + 成功状态。
3. 轨迹效率指标：`agent_steps / gold_steps`。报告每任务和聚合值。
4. 任务间状态重置——绝不在被前一个任务污染的状态上运行任务。
5. 失败模式分类器：对于每个失败，标记是定位失误（错误元素）还是规划失误（错误动作）。

硬性拒绝：

- 任务间没有状态重置。跨任务污染会使所有分数无效。
- 仅成功率的报告。轨迹效率是 2026 年的标准。
- 仅截图夹具没有 DOM 对等。有些智能体使用 DOM+视觉；除非明确限制表面，否则两者都提供。

拒绝规则：

- 如果任务没有标准轨迹，拒绝。没有它们无法衡量效率。
- 如果应用没有固定到特定版本，拒绝。漂移会使跨运行比较无效。
- 如果智能体有破坏性工具（删除、发布），要求应用的沙箱副本。

输出：`tasks.py`、`runner.py`、`failure_classifier.py`、`report.py`、`README.md`，解释重置策略、标准轨迹来源以及定位-与-规划的分类。结尾的「下一步阅读」指向第 21 课（计算机使用模型）或第 30 课（评估驱动开发）。