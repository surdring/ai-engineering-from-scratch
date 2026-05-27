---
name: img2img-chooser
description: 根据配对/非配对数据、领域特异性和延迟预算选择图像到图像转换方法
version: 1.0.0
phase: 8
lesson: 04
tags: [pix2pix, img2img, conditional]
---

给定任务描述（源领域、目标领域、数据可用性 — 配对/非配对/N 个样本、延迟预算、质量要求），输出：

1. 方法。Pix2Pix（配对，窄领域）、Pix2PixHD（配对，高分辨率）、CycleGAN（非配对）、SPADE（分割到图像），或基于 SD3 / Flux.1 的 ControlNet 变体（通用，开放领域）。
2. 训练数据规格。最少配对数量、分辨率、数据增强、许可证考虑。
3. 架构。G（U-Net 深度、通道宽度）、D（PatchGAN 感受野、谱归一化）、损失权重（对抗、L1、VGG 感知损失）。
4. 推理延迟。单张消费级 GPU（RTX 4090、M3 Max）上的目标毫秒数/图像，分辨率权衡。
5. 评估。与留出配对数据的 LPIPS、5k 样本上的 FID、任务特定指标（分割任务用 mIoU、超分辨率用 PSNR）、人工偏好。

拒绝在数据非配对时推荐 Pix2Pix — 应推荐 CycleGAN 或 ControlNet。拒绝在少于 500 对且无数据增强/预训练建议的情况下训练配对模型。标记任何说"任意文本提示"的需求 — 这些需要扩散模型 + ControlNet，而非配对 GAN。