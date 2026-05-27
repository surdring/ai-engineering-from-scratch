---
name: prompt-gpt-architecture-analyzer
description: 分析任何 GPT 风格 Transformer 模型的架构选择
version: 1.0.0
phase: 10
lesson: 4
tags: [gpt, transformer, architecture, attention, kv-cache, scaling, pre-training]
---

# GPT 架构分析器

在评估技术报告、模型卡片或训练日志中的 GPT 风格模型时，使用此框架拆解架构并识别设计权衡。

## 分析协议

### 1. 参数分配分解

计算每个组件的精确参数数量：

- **Token 嵌入**：vocab_size × embed_dim
- **位置嵌入**：max_seq_len × embed_dim
- **每块注意力**：4 × embed_dim × embed_dim（Q、K、V、输出投影）
- **每块 FFN**：2 × embed_dim × ff_dim + embed_dim + ff_dim（两个线性层 + 偏置）
- **每块 LayerNorm**：4 × embed_dim（两个归一化层，各有缩放 + 偏置）
- **最终 LayerNorm**：2 × embed_dim
- **输出头**：vocab_size × embed_dim（若与 token 嵌入权重绑定则为 0）

标记任何单个组件超过总参数 40% 的情况。小模型中嵌入矩阵占主导，大模型中注意力和 FFN 占主导。

### 2. 注意力设计分析

评估注意力配置：

- **头维度**：embed_dim / num_heads。标准为 64（GPT-2）或 128（Llama 3）。低于 32 限制每头表达能力，高于 128 浪费计算且收益很小。
- **每层头数**：更多头 = 更多样化的注意力模式，但 KV 缓存需要更多内存。
- **分组查询注意力（GQA）**：模型是否在多个 Q 头之间共享 K/V 头？Llama 3 使用 GQA，32 个 Q 头配 8 个 KV 头。这使 KV 缓存减少 4 倍。
- **上下文长度**：最大位置嵌入。RoPE 允许超出训练长度进行外推，绝对位置嵌入则不能。

### 3. 内存预算

在模型的最大上下文长度下进行推理：

- **权重（FP16）**：total_params × 2 字节
- **KV 缓存（FP16）**：2 × num_layers × num_kv_heads × head_dim × max_seq_len × 2 字节
- **激活值**：batch_size × seq_len × embed_dim × 2 字节 × num_layers（近似）

标记 KV 缓存超过权重内存的情况。这发生在长上下文模型（128K+）上，表明模型在解码阶段是内存受限的。

### 4. 计算概况

- **预填充每 token FLOPS**：约 2 × total_params（每参数一次矩阵乘法，前向传播）
- **解码每 token FLOPS**：与预填充相同但在单个 token 上
- **预填充瓶颈**：计算受限（GPU TFLOPS）
- **解码瓶颈**：内存受限（GPU 内存带宽）
- **算术强度**：每字节内存访问的 FLOPS。低于 100 = 内存受限。

### 5. 缩放决策

对照已知缩放法则评估：

- **Chinchilla 最优**：对给定的计算预算 C，最优模型大小 N 和 token 数 D 满足 N ~ D（大致相等缩放）。7B 模型需要约 140B token。
- **Llama 3 过度训练**：Meta 用 15T token 训练 Llama 3 8B（Chinchilla 最优的 100 倍）。在更多数据上过度训练小模型产生更好的每 token 推理成本。
- **宽度 vs 深度**：对相同参数数量，更深模型（更多层）通常比更宽模型（更大 embed_dim）样本效率更高。

## 危险信号

- **FFN 比例不是 4 倍**：标准是 ff_dim = 4 × embed_dim。Llama 使用 8/3 × embed_dim 配合 SwiGLU。偏离应有理由。
- **无权重绑定**：除非 vocab_size 相对 embed_dim 非常大，否则输出头应与 token 嵌入共享权重。
- **13B 以上无 GQA**：13B 以上模型没有分组查询注意力将产生过大 KV 缓存。
- **长上下文无 RoPE**：绝对位置嵌入不能超出训练长度外推。目标 32K+ 上下文的模型应使用旋转嵌入。
- **学习率对模型大小来说过高**：更大模型需要更低峰值学习率。GPT-2 Small 使用 6e-4，Llama 3 405B 使用 8e-5。

## 输出格式

1. **参数表**：逐组件参数数量及百分比
2. **内存预算**：最大上下文长度下的权重、KV 缓存和激活内存
3. **计算概况**：A100/H100 上的预填充和解码吞吐量估算
4. **设计评估**：模型做得对的地方以及非标准之处
5. **缩放结论**：模型大小是否与训练数据相匹配