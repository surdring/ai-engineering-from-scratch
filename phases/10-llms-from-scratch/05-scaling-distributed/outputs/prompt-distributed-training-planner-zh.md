---
name: prompt-distributed-training-planner
description: 根据模型大小和可用硬件规划分布式训练运行
version: 1.0.0
phase: 10
lesson: 5
tags: [distributed-training, fsdp, deepspeed, tensor-parallelism, pipeline-parallelism, scaling]
---

# 分布式训练规划器

在规划大规模语言模型的分布式训练运行时，使用此框架确定并行策略、内存预算、通信开销和预期吞吐量。

## 输入要求

提供：
- **模型大小**（以十亿参数计）
- **目标训练 token**（以万亿计）
- **可用 GPU**（类型：A100/H100/H200，数量，互连：NVLink/InfiniBand）
- **GPU 内存**（A100/H100 为 80GB，H200 为 141GB）
- **节点**（每个节点 GPU 数，节点数量）
- **预算约束**（最大美元成本，最大墙钟时间）

## 第一步：内存预算

计算每个组件的每 GPU 内存：

| 组件 | 公式 | FP16 | FP32 |
|-----------|---------|------|------|
| 权重 | params × bytes_per_param | params × 2 | params × 4 |
| Adam 优化器 (m + v) | params × 4 × 2 | 始终 8 字节/参数 | 始终 8 字节/参数 |
| 梯度 | params × bytes_per_param | params × 2 | params × 4 |
| 激活（估算） | seq_len × batch × hidden × layers × 2 | 变化 | 变化 |

如果总量超过 GPU 内存，需要分片。按以下顺序尝试：
1. ZeRO-1（仅分片优化器）— 通信成本最低
2. ZeRO-2（+ 梯度）— 通信成本适中
3. FSDP/ZeRO-3（+ 权重）— 通信成本最高但节省内存最多
4. 如果激活仍过大，添加激活检查点（Activation Checkpointing）
5. 如果单个层不能放进一个 GPU，添加张量并行

## 第二步：并行策略

### 决策树

1. **单个层能放进一个 GPU 吗？**
   - 不能：需要张量并行（TP）。设置 TP = 2、4 或 8（节点内）。
   - 能：跳过张量并行。

2. **完整模型（经过分片后）能放进一个节点的 GPU 中吗？**
   - 不能：需要流水线并行（PP）。设置 PP = 节点数 / 组数。
   - 能：跳过流水线并行。

3. **剩余多少 GPU 用于数据并行（DP）？**
   - DP = total_gpus / (TP × PP)

4. **数据并行组内使用什么分片级别？**
   - 从 FSDP（ZeRO-3）开始。如果通信是瓶颈，降至 ZeRO-2 或 ZeRO-1。

### 典型配置

| 模型大小 | 总 GPU | TP | PP | DP | 分片 |
|-----------|-----------|----|----|-----|----------|
| 7B | 8 | 1 | 1 | 8 | FSDP |
| 13B | 16 | 2 | 1 | 8 | FSDP |
| 70B | 64 | 8 | 1 | 8 | FSDP |
| 70B | 128 | 8 | 2 | 8 | FSDP |
| 405B | 16,384 | 8 | 16 | 128 | FSDP |

## 第三步：通信分析

估算每次训练步的通信量：

- **数据并行（all-reduce）**：每步 2 × gradient_size × (N-1)/N
- **FSDP（all-gather + reduce-scatter）**：每步约 3 × weight_size × (N-1)/N（高于 DP）
- **张量并行（每层 all-reduce）**：每步 2 × activation_size × num_layers（需要 NVLink）
- **流水线并行（点对点）**：每阶段边界 activation_size（最小）

如果通信时间超过计算时间的 20%，策略是通信受限的。解决方案：
- 梯度累积（降低 all-reduce 频率）
- 通信与计算重叠（FSDP 默认如此）
- 增加微批次大小（更好的计算-通信比）
- 切换到通信成本更低的分片阶段

## 第四步：吞吐量和成本估算

**每次训练步的 FLOPS：**
- 前向：约 2 × params × tokens_per_batch
- 反向：约 4 × params × tokens_per_batch（前向的 2 倍）
- 总计：约 6 × params × tokens_per_batch

**训练时间：**
- total_flops = 6 × params × total_tokens
- time_seconds = total_flops / (num_gpus × gpu_tflops × 1e12 × utilization)
- 典型利用率：35-45%（考虑通信、流水线气泡、内存开销）

**成本：**
- total_gpu_hours = num_gpus × time_seconds / 3600
- cost = total_gpu_hours × cost_per_gpu_hour

## 第五步：验证检查清单

启动前：

1. 每 GPU 内存适合硬件限制（留 10% 余量）
2. 有效批次大小匹配目标（per_gpu_batch × DP × gradient_accumulation_steps）
3. 通信-计算比低于 20%
4. 流水线气泡比例低于 15%（足够的微批次）
5. 学习率按有效批次大小缩放
6. 检查点频率考虑故障概率（大规模运行时每 1-2 小时保存一次）
7. 梯度裁剪已设置（大规模模型通常为 1.0）
8. 预热步数与总步数成比例（通常为总数的 0.1-1%）

## 危险信号

- **TP > 8**：跨节点的张量并行（通过 InfiniBand）几乎总是比流水线并行慢
- **流水线段数 > 32**：即使有大量微批次，气泡开销也变得显著
- **有效批次大小 > 10M token**：收益递减，可能损害收敛
- **利用率低于 30%**：通信受限 — 重新评估并行策略
- **13B 以上无激活检查点**：反向传播时会内存不足
- **每 GPU 批次小且无梯度累积**：梯度噪声增加；累积到 256+ 样本的有效批次