---
name: checkpointing-planner
description: 根据训练配置和 HBM 预算选择每层激活重计算策略（无/选择性/全量/卸载）
version: 1.0.0
phase: 10
lesson: 34
tags: [gradient-checkpointing, activation-recomputation, selective-checkpoint, fsdp-offload, training-memory]
---

给定训练配置（层数 L、隐藏维度大小 d、序列长度 S、微批次 B、每值数据类型字节数、注意力内核、张量并行度 TP、流水线并行度 PP、如果是 MoE 则还有专家并行度 EP）以及除去权重和优化器状态后的每 rank HBM 预算，输出：

1. 每层策略。对栈中每种层类型（嵌入、注意力、FFN、MoE 专家、归一化、输出头）选择无（none）、选择性（selective）、全量（full）或卸载（offload）。当 S 超过 4096 时注意力默认使用选择性；残差流和归一化默认使用无；仅当该层激活的 PCIe 传输时间测量值小于其重计算时间测量值时，FFN 使用卸载。
2. 分段大小 k。如果使用全量检查点，均匀层成本下 k 取 round(sqrt(L))，激活内存占主导的预算下用更小的 k。报告额外 FLOP 百分比为前向 FLOPs 的 (1/k)。
3. FlashAttention 交互。确认注意力内核是否已经重计算 softmax。如果是，选择性注意力检查点收益很小，降级为无。按名称声明内核（FlashAttention-2/3、xFormers memory-efficient、vanilla）。
4. TP/PP 计划。TP 方面，列出重计算时需要 gather 或 rescatter 的激活，以及每步增加的通信字节数。PP 方面，确认哪些流水线阶段被端到端检查点化，以便反向微批次在回流前释放激活内存。
5. 预算计算。预测应用策略前后的激活内存（每 rank MB）。预测 FLOP 开销占 fwd+bwd 的百分比。拒绝任何无法在留有 10% 余量的 HBM 预算内适配的计划。

拒绝仅通过选择性注意力就能关闭预算的情况下全量检查点每一层；分析显示全量的 FLOP 开销是选择性的数倍，节省相同内存，且确切比率与工作负载相关。拒绝当某层在目标 PCIe 链路上的激活传输时间测量值超过其重计算时间测量值时使用卸载；重计算胜出。拒绝 FP8 训练中"到处检查点"若所选框架不保存 amax 快照；重计算会漂移缩放因子并静默破坏梯度。

示例输入：「L=64，d=8192，S=8192，B=1，bf16，FlashAttention-3，TP=8，PP=4，每 rank HBM 预算 32 GB（除去权重），MoE 含 8 个专家且 EP=8。」

示例输出：
- 每层策略：注意力选择性，FFN 无，MoE 专家全量，嵌入无，输出头卸载。
- 分段大小：仅 MoE 应用全量，k=8；专家路径 FLOP 开销 12%，其他 0。
- FlashAttention 交互：FA-3 已重计算 softmax；选择性在层包装器而非内核内。
- TP/PP 计划：重计算时注意力输入的 TP gather，每步额外通信 0.3 GB；PP 每阶段将其正向全部检查点化；PP 阶段 3 保留其激活用于最后反向。
- 预算计算：无策略时激活 38 GB，有策略时 11 GB。总 FLOP 开销占 fwd+bwd 的 7.5%。