---
name: finetuning-pipeline
description: 运行可复现的数据到 SFT 到 DPO 到服务的微调流水线，包含消融实验、量化和 2026 Model Openness Framework 模型卡。
version: 1.0.0
phase: 19
lesson: 07
tags: [capstone, fine-tuning, axolotl, trl, dpo, grpo, vllm, eagle-3, mof]
---

给定基础模型（Llama 3.3 8B、Qwen3 14B 或 Gemma 3 12B）和任务特定数据集，构建一条命令即产出服务端点和可复现模型卡的流水线。

构建计划：

1. 数据阶段：Datatrove 去重、Nemotron-CC 风格质量过滤、Presidio PII 脱敏、种子 train/val 分割。
2. 污染检查：对照 MMLU-Pro、MT-Bench-v2、RewardBench-2 的 MinHashLSH。重叠则拒绝。
3. SFT：Axolotl v0.8，ZeRO-3、Flash Attention 3、打包序列、2-3 epoch 在 8xH100 上。
4. 偏好调优：TRL 0.15 DPO（或带可验证奖励的 GRPO）1 个 epoch，beta 扫描。
5. 量化：GPTQ-INT4-Marlin + AWQ-INT4 + GGUF-Q4_K_M。
6. 部署：vLLM 0.7 配合 EAGLE-3 推测解码（通过 Red Hat Speculators 或 SGLang SpecForge 的草稿头）。K8s 部署，HPA 监控队列等待。
7. 评估：lm-evaluation-harness、RewardBench-2、MT-Bench-v2、MMLU-Pro，覆盖基础/SFT-only/SFT+DPO/SFT+GRPO。
8. 安全：Llama Guard 4 通过率、ShieldGemma-2 输出过滤器。
9. 2026 Model Openness Framework 下的模型卡，包含数据、训练、评估、安全、可复现性章节。

评估标准：

| 权重 | 标准 | 测量方式 |
|:-:|---|---|
| 25 | 相较基础的评估增量 | MMLU-Pro、MT-Bench-v2、任务特定基准的测量增益 |
| 20 | 流水线可复现性 | 一条命令用相同种子重跑产出匹配哈希 |
| 20 | 数据卫生 | 去重率、PII 脱敏覆盖、污染检查绿灯 |
| 20 | 部署效率 | batch 1/8/32 的 tokens/s、EAGLE-3 接受率、$/1M tokens |
| 15 | 模型卡 + 安全评估 | 2026 MOF 完整性 + Llama Guard 4 通过率 |

硬性拒绝：
- 跳过 MinHash 污染检查的流水线。将 MMLU-Pro 泄露到训练中是经典的评估作弊失败模式。
- 没有种子或 YAML 附件的训练运行。可复现性是硬性要求。
- 没有 EAGLE-3 或等效推测解码配置的部署。基线 tokens/s 不是 2026 的标准。
- 缺失安全评估。每个微调都需要附带 Llama Guard 4 通过率。

拒绝规则：
- 拒绝发布声称基准分数而不附带 lm-eval-harness 提交 SHA 的模型卡。
- 拒绝在许可证禁止衍生模型的数据上微调。MOF 对数据许可进行评级。
- 拒绝在不测量评估矩阵上质量损失的情况下交付量化模型。

输出：包含流水线编排器、Llama 3.3 8B + 一个替代基础模型的 YAML、SFT 和 DPO W&B run logs、量化产物、部署端点、三基准评估矩阵、安全评估、2026 MOF 模型卡的仓库，以及记录你捕获并修复的三大数据卫生问题的 write-up。