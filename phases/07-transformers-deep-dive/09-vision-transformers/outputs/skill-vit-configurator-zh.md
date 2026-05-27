---
name: vit-configurator
description: 为新的视觉任务选择 ViT 变体、patch 大小和预训练来源
version: 1.0.0
phase: 7
lesson: 9
tags: [transformers, vit, vision]
---

给定视觉任务（分类 / 分割 / 检测 / 检索）、图像分辨率、数据集大小（标注 + 未标注）和部署目标，输出：

1. 骨干。以下之一：DINOv2 ViT-L/14（检索/分类默认）、SAM 3 编码器（分割）、SigLIP（视觉-语言）、ConvNeXt（延迟敏感）。一句话理由。
2. Patch 大小。224 上的标准分类用 16，DINOv2 用 14，高分辨率的密集预测用 8。标记序列长度 `(H/P)^2 + 1` 和注意力成本 `O(N²)`。
3. 预训练来源。检查点名称。对于小规模标注集（< 1 万）：DINOv2 特征冻结 + 线性探针。对于 > 10 万：微调最后几个块。说明原因。
4. 训练方案。优化器（AdamW）、学习率、数据增强（RandAug、MixUp、Random Erasing）、标签平滑（典型值 0.1）、EMA。
5. 风险提示。数据规模风险（数据太少无法全量微调）、分辨率不匹配（预训练 224 → 部署 1024 而不做位置插值）、缺少 register token（可能损害 DINOv2 特征）。

拒绝推荐在少于 100 万张图像上从头训练 ViT — CNN 基线会更好。拒绝推荐 patch 大小导致序列长度 > 4096 而不明确讨论 Flash Attention + 分层变体（Swin）。标记任何改变输入分辨率但不插值位置嵌入的部署。