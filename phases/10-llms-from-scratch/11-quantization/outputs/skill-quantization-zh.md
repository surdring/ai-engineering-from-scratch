---
name: skill-quantization
description: 根据硬件、质量和延迟约束选择部署 LLM 的量化策略
version: 1.0.0
phase: 10
lesson: 11
tags: [quantization, inference, deployment, optimization, fp8, int4, int8, gptq, awq, gguf]
---

# 量化决策框架

在部署语言模型时，使用此框架选择正确的数字格式、量化方法和质量验证策略。

## 输入要求

提供：
- **模型**（名称、参数数量、原始精度）
- **目标硬件**（GPU 型号/VRAM、CPU、Apple Silicon、边缘设备）
- **延迟目标**（tokens/秒、首 token 到达时间）
- **质量底线**（最大可接受困惑度增加、基准偏移）
- **服务模式**（批次大小、最大上下文长度、并发用户）

## 快速选择

| 你的情况 | 格式 | 方法 | 预期质量损失 |
|---------------|--------|--------|----------------------|
| H100 GPU，最大吞吐量 | FP8 E4M3 | Native H100 casting | < 0.1% |
| A100/A10，需要 2 倍吞吐 | INT8 | LLM.int8() 或 SmoothQuant | < 0.5% |
| 单 24GB GPU，70B 模型 | INT4 | AWQ 或 GPTQ | 1-3% |
| MacBook / Apple Silicon | INT4 GGUF | Q4_K_M（via llama.cpp） | 1-2% |
| 移动/边缘设备 | INT4 或 INT3 | QAT + 设备特定 | 2-5% |
| 最大压缩，可接受部分损失 | INT2 | QuIP# 或 AQLM | 5-15% |
| 训练（混合精度） | BF16 + FP32 累加 | 原生框架支持 | 0% |

## 按组件的精度选择

并非所有张量都应得到相同处理。

| 组件 | 安全下限 | 推荐 | 避免 |
|-----------|-------------|-------------|-------|
| FFN 权重 | INT4 | INT4 (AWQ/GPTQ) | INT2 无 QAT |
| 注意力权重 | INT4 | INT8 或 FP8 | INT2 |
| 嵌入层 | INT8 | FP16（保持原样） | INT4 |
| 输出头 | INT8 | FP16（保持原样） | INT4 |
| KV 缓存 | FP8 | FP8 或 INT8 | 长上下文用 INT4 |
| 注意力 logits | FP16 | FP16 或 BF16 | INT8 |
| 激活值（推理） | INT8 | FP8 或 INT8 | INT4 |

## 方法对比

### GPTQ
- **适用场景**：GPU 推理，需要 Hugging Face 兼容模型
- **校准数据**：128 个示例，每个 2048 token
- **耗时**：A100 上 70B 约 30-60 分钟
- **工具**：`auto-gptq`、`exllama`、`exllamav2`
- **优势**：经过充分测试，Hugging Face 上有巨大模型库
- **劣势**：比 AWQ 应用慢，在某些模型上质量略低于 AWQ

### AWQ
- **适用场景**：GPU 推理，需要最佳的每比特质量
- **校准数据**：128 个示例
- **耗时**：A100 上 70B 约 15-30 分钟
- **工具**：`autoawq`、`vLLM`（原生支持）
- **优势**：最佳 INT4 质量，快速应用，vLLM 集成
- **劣势**：模型库比 GPTQ 小

### GGUF
- **适用场景**：CPU 推理、Apple Silicon、llama.cpp 生态
- **变体**：Q2_K、Q3_K_S/M/L、Q4_K_S/M、Q5_K_S/M、Q6_K、Q8_0、F16
- **推荐默认值**：Q4_K_M（最佳质量/大小平衡）
- **工具**：`llama.cpp`、`ollama`、`LM Studio`
- **优势**：自包含文件、混合精度、庞大生态
- **劣势**：对 GPU 并非最优（为 CPU/Metal 设计）

### SmoothQuant
- **适用场景**：GPU 上 INT8，需要权重和激活值同时量化
- **核心思想**：通过逐通道缩放将量化难度从激活值迁移到权重
- **工具**：`smoothquant`、`TensorRT-LLM`
- **优势**：实现 W8A8（权重和激活值均为 INT8），2 倍加速
- **劣势**：仅 INT8，不扩展到 INT4

## 质量验证协议

量化后，部署前验证：

1. **困惑度测试**。在 WikiText-2 或你的领域语料上计算。增量 < 0.5 是优秀，0.5-1.0 是良好，> 2.0 是有问题。

2. **基准扫描**。运行 MMLU（通用）、GSM8K（数学）、HumanEval（代码）。数学和代码对精度损失最敏感。

3. **输出对比**。从原始模型和量化模型分别生成 100 个回答。使用 LLM 作为裁判计算胜率。目标：量化模型在 > 90% 的提示上胜出或持平。

4. **延迟测量**。在批次大小为 1 和目标批次大小下测量 tokens/秒。验证加速是否值得质量损失。

5. **长上下文测试**。如果服务长上下文（> 4K token），在最大上下文长度下测试。KV 缓存量化误差随序列长度累积。

## 内存预算计算器

```
权重内存（GB）= 参数（B）× bits / 8 / 1.073741824
每 token KV 缓存（MB）= 2 × num_layers × d_model × bits / 8 / 1048576
上下文 KV 缓存（GB）= kv_per_token × max_context_length / 1024
激活内存（GB）~ 1-4 GB（相对固定，取决于批次大小）
总计 = 权重内存 + KV 缓存 + 激活内存 + 开销（10-20%）
```

Llama 3 70B INT4、32K 上下文示例：
- 权重：70B × 4 / 8 / 1.07 = 32.6 GB
- KV 缓存（FP16）：2 × 80 × 8192 × 16 / 8 / 1e9 × 32768 = ~40 GB
- KV 缓存（FP8）：~20 GB
- 总计（FP8 KV）：~55 GB（适合单张 80GB A100）

## 常见错误

| 错误 | 为何失败 | 修复 |
|---------|-------------|-----|
| 将嵌入层量化为 INT4 | 第一层错误会通过整个模型放大 | 嵌入层保持 FP16 或 INT8 |
| 对 INT4 使用每张量缩放因子 | 一个异常行会破坏所有行的精度 | 使用逐通道或逐组缩放因子 |
| 未校准 GPTQ/AWQ | 没有代表性数据时缩放因子错误 | 使用 128 个领域内示例 |
| 所有层相同位宽 | 首尾层更敏感 | 混合精度：首尾层用更高位宽 |
| 在超长上下文时量化 KV 缓存 | 误差随序列长度平方累积 | KV 缓存用 FP8，不用 INT4 |
| 跳过质量验证 | 某些模型量化效果差（尤其边界处） | 始终运行困惑度 + 任务评估 |

## 部署方案

### 方案 1：vLLM with AWQ（GPU 服务器）
```
pip install vllm autoawq
vllm serve model-awq --quantization awq --dtype half --max-model-len 8192
```

### 方案 2：llama.cpp with GGUF（MacBook）
```
./llama-server -m model.Q4_K_M.gguf -c 4096 -ngl 99
```

### 方案 3：TensorRT-LLM with FP8（H100）
```
trtllm-build --model_dir model --output_dir engine --dtype float16 --use_fp8
```