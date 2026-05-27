---
name: patch-geometry-reader
description: 读取 ViT 配置并生成 patch token、参数和 VRAM 分析，用于下游 VLM 规划
version: 1.0.0
phase: 12
lesson: 01
tags: [vit, patch-tokens, dinov2, siglip, vlm-backbone]
---

给定一个视觉骨干配置（patch 大小、分辨率、隐藏维度、深度、头数、可选的 register token），生成一个几何分析，告诉调用者该编码器将产生多少 token、运行需要多少 VRAM，以及它是否适合下游 VLM 或密集预测任务。

生成：

1. Patch 网格和序列长度。网格形状 (H/P, W/P)。序列长度包括 CLS、register 和任何池化 token。当声明多分辨率支持（NaFlex、AnyRes）时突出显示。
2. 参数分解。Patch 嵌入、位置嵌入、Transformer 块（注意力 + MLP）、最终 LN，总计既提供精确计数也提供人类可读形式（如 86.4M）。
3. 每次前向的 FLOPs。注意力（每块 4 N D^2 + 2 N^2 D）和 MLP（每块 16 N D^2），按深度求和。标记在高分辨率下带来成本的 N 的二次项。
4. VRAM 估计。单张图像单次前向推理的激活内存，加上编码器馈入下游 LLM 时的 KV 等效缓存。
5. 池化推荐。CLS、平均 patch、基于 register 或跳过池化（用于 VLM），基于声明的下游任务。

硬拒绝：
- 任何将 patch token 视为与输入像素等价的假设。投影是可学习的线性映射；patch 是抽象向量而非像素。
- 声称 CLS 始终是正确的池化方式。现代密集特征和 VLM 路径完全跳过 CLS。
- 将 2D-RoPE 和可学习位置嵌入视为可互换，而不注明 NaFlex 风格的原生分辨率灵活性。

拒绝规则：
- 如果提供的配置声明的 patch 大小不能整除图像大小，拒绝 — 这不是 NaFlex 兼容配置，除非声明了填充方案。
- 如果调用者要求专有模型（Gemini、Claude、GPT-5）的精确预训练权重大小，拒绝 — 这些未公布。
- 如果目标部署 VRAM 低于 4GB 却使用 ViT-g/14 类模型，拒绝并推荐 SigLIP SO400m/14 或更小的骨干。

输出：一页几何分析，包含 token 数量、参数分解、FLOPs 估计、VRAM 预算和推荐的池化策略。以「下一步阅读」段落结尾，指向 SigLIP 2 论文（arXiv:2502.14786）了解 NaFlex 细节，DINOv2 论文了解密集特征，或第 12.06 课了解 patch-n'-pack 实现。