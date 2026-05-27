---
name: resolution-budget-planner
description: 为混合宽高比的 VLM 工作负载在 square-resize、AnyRes、M-RoPE 和 NaFlex 之间选择，并输出每任务 token 预算计划
version: 1.0.0
phase: 12
lesson: 06
tags: [vlm, patch-n-pack, naflex, anyres, m-rope, token-budget]
---

给定工作负载 — VLM 将看到的图像描述（OCR 文档、图表、UI 截图、自然照片、视频帧）和每请求总 token 预算 — 为每个图像类别选择一种分辨率策略并生成可运行的配置。

生成：

1. 每图像类别策略。对每个声明的类别（OCR、图表、UI、照片、视频帧），从 {square-resize, AnyRes, M-RoPE, NaFlex} 中选择一个。用一句话论证，引用任务对分辨率敏感度。
2. 每张图像 token 预算。包括 min_pixels、max_pixels（Qwen2.5-VL 风格），以及在所选策略下的预期序列长度。标记任何单张图像超过 LLM 上下文 40% 的情况。
3. 批量打包计划。如果请求是批量的，指定使用 `cu_seqlens`（FlashAttn varlen）、密集块对角掩码还是单图像非批量推理。注意当批量宽高比差异超过 2x 时 varlen 带来的 FLOP 节省。
4. 编码器推荐。混合工作负载用 SigLIP 2 NaFlex；智能体 UI 用 Qwen2.5-VL 原生；冻结编码器部署用 CLIP-336 + AnyRes；仅照片路径用原始 ViT at 224。
5. 故障模式警告。所选配置下每张图像的 token 数；在 30 tok/s 预填充下的延迟成本；上下文填充百分比；在典型 OCR 基准上相对于 square-resize 的预期准确率差异。

硬拒绝：
- 为 OCR 或图表任务推荐 square-resize 而不引用用户将损失哪个基准数字。
- 提议产生超过 LLM 上下文容量的 token 的策略。始终按声明的上下文窗口做预算。
- 将 AnyRes 视为通用答案 — 其乘性切块开销可能在单张图像编码完成前就超出 LLM 上下文。

拒绝规则：
- 如果用户的声明 token 预算低于每张图像 256 token，除非是仅照片的语义任务否则拒绝 — 无论多少池化都无法在该预算下恢复 OCR 准确率。
- 如果用户想要密集预测输出（分割、深度）而编码器中未启用 ViT register token，拒绝并指向 DINOv2 / 启用了 register 的 SigLIP 2。
- 如果用户的 LLM 上下文 < 8k 且工作负载包含文档或截图，拒绝并推荐更大的上下文或 OCR 先行流水线。

输出：一页预算计划，包含每类别策略表、批量打包计划、编码器推荐和警告列表。以相关 arXiv 论文结尾作为跟进阅读 — 2307.06304 了解 NaViT，2502.14786 了解 SigLIP 2 / NaFlex，2502.13923 了解 Qwen2.5-VL。