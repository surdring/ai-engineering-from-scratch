---
name: skill-inference-optimization
description: 诊断和优化 LLM 推理服务的吞吐量、延迟和成本
version: 1.0.0
phase: 10
lesson: 12
tags: [inference, kv-cache, batching, speculative-decoding, vllm, optimization]
---

# LLM 推理优化模式

两个阶段：预填充（Prefill，计算密集型，可并行）和解码（Decode，内存密集型，串行）。每个优化针对其中一个或两个。

```
请求 -> 预填充（处理 Prompt）-> 解码（生成 token）-> 响应
              |                            |
         计算密集型                   内存密集型
         优化：融合、                 优化：批处理、
         前缀缓存                     量化、推测
```

## 决策框架

### 第一步：识别瓶颈

测量你工作负载的 ops:byte 比率：

| ops:byte | 受限于 | 如何优化 |
|----------|-------|-----------------|
| < 50 | 内存 | 量化 KV 缓存，增大批次 |
| 50-200 | 过渡期 | 两者都重要，从批处理开始 |
| > 200 | 计算 | 内核融合、张量并行、FP8 |

### 第二步：选择引擎

- **默认**：vLLM（最广模型支持、PagedAttention、OpenAI 兼容 API）
- **多轮对话/结构化输出**：SGLang（RadixAttention 前缀缓存、受限解码）
- **NVIDIA 最大吞吐量**：TensorRT-LLM（内核融合、H100 上 FP8）

### 第三步：按顺序应用优化

1. **KV 缓存** -- 始终开启，无副作用
2. **连续批处理** -- 始终开启，无副作用（vLLM/SGLang 默认支持）
3. **前缀缓存** -- 如有共享系统提示则启用（大多数聊天机器人有）
4. **量化** -- KV 缓存 INT8/FP8 减少内存 2-4 倍，质量损失最小
5. **推测式解码** -- 延迟比吞吐量更重要时添加
6. **张量并行** -- 模型放不进单个 GPU 时分拆到多个 GPU

## KV 缓存内存公式

```
per_token = 2 × num_layers × num_kv_heads × head_dim × bytes_per_param
total = per_token × sequence_length × num_concurrent_users
```

常用模型快速参考（BF16）：

| 模型 | 每 token | 100 用户 @ 4K |
|-------|-----------|----------------|
| Llama 3 8B | 32 KB | 12.5 GB |
| Llama 3 70B | 320 KB | 125 GB |
| Llama 3 405B | 504 KB | 197 GB |

## 推测式解码检查清单

- 草稿模型应比目标小 5-10 倍（例如 8B 草稿配 70B 目标）
- 接受率 > 70% 才有意义加速
- 在可预测文本上最佳（代码、结构化输出、自然语言）
- 在创意/采样密集型任务上最差（低温度有帮助）
- 大多数工作负载：EAGLE > 草稿-目标 > n-gram

## 常见错误

- 以 batch=1 运行解码（内存受限，GPU 计算 95% 空闲）
- 分配连续 KV 缓存块（使用 PagedAttention，接近零浪费）
- 80% 请求共享相同系统提示时忽略前缀缓存
- 为模型权重过度分配 GPU 内存，KV 缓存无剩余空间
- 只测吞吐量不测延迟（10 秒 TTFT 的高吞吐量无意义）
- 高温度下使用推测式解码（接受率降至 50% 以下）

## 监控检查清单

- 首 token 到时间（TTFT）：预填充延迟，交互式使用目标 < 500ms
- Token 间延迟（ITL）：解码速度，流式传输目标 < 50ms
- 吞吐量（tokens/秒）：所有并发用户总计
- KV 缓存利用率：已分配缓存的使用百分比
- 批次利用率：每次迭代填充的批次槽位百分比
- 队列深度：等待批次槽位的请求数