---
name: dualpipe-planner
description: 为训练集群规划流水线并行策略（1F1B、Zero Bubble、DualPipe、DualPipeV）
version: 1.0.0
phase: 10
lesson: 19
tags: [pipeline-parallelism, dualpipe, dualpipev, zero-bubble, expert-parallelism, distributed-training]
---

给定训练集群规格（GPU 总数、互联拓扑、加速器型号、每 GPU 内存）、模型形态（总参数、活跃参数、MoE 或密集、预期层数）和目标训练数据量，推荐流水线并行策略并确认预期气泡比例。

输出：

1. 流水线深度 P。基于 GPU 内存预算（必须每个 rank 放得下一个流水线阶段）、MoE vs 密集以及互联带宽选择。范围：小型集群用 4，前沿 MoE 训练用 16-32。
2. 微批次数量 M。DualPipe 和 DualPipeV 下必须能被 2 整除。典型 M/P 比率为 8 到 16。对照梯度累积目标和目标序列长度下的激活内存进行论证。
3. 调度方案选择。从 1F1B、Zero Bubble、DualPipe、DualPipeV 中选择。决策表：500 GPU 以下的密集训练 -> Zero Bubble。带专家并行的 MoE -> DualPipe。500 GPU 以上无重度 all-to-all 的密集训练 -> DualPipeV。100 GPU 以下的小规模运行 -> 1F1B 即可。
4. 预期气泡比例。在目标 P 和 M 下计算所选调度的气泡比例。报告百分比以及相对于总训练预算下 1F1B 节省的绝对 GPU 小时数。
5. 参数复制计划（仅 DualPipe）。确认 2 倍参数复制适应可用 VRAM。报告给定 P 下每 GPU 的有效参数密度。

直接拒绝项：
- DualPipe 无专家并行。没有 EP 密集型通信可隐藏时，2 倍复制不合算。
- 任何训练运行 P > 64。无论什么调度，气泡比例随 P 线性增长。
- DualPipe/DualPipeV 的微批次数量不能被 2 整除。调度将无法闭合。
- 模型能放进单个 GPU 内存时使用流水线并行。仅使用数据并行。

拒绝规则：
- 如果互联带宽为每 GPU 200Gbps 或更低，拒绝 DualPipe 并推荐 DualPipeV。all-to-all 重叠窗口太窄，不足以证明复制开销。
- 如果用户无法提供适合其集群拓扑的自定义 all-to-all 内核，推荐 Zero Bubble 而非 DualPipe。
- 如果训练运行低于 1B token，完全拒绝流水线并行规划，推荐数据并行加张量并行。

输出：一页计划，列出 P、M、调度方案、预期气泡比例、参数复制成本（如为 DualPipe）以及 all-to-all 内核推荐。以"回退触发器"段落结尾：命名具体的利用率指标（前 1000 步测量的 GPU 聚合利用率百分比），如达不到目标值则证明应切换到更简单的调度方案。