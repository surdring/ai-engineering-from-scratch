---
name: vae-trainer
description: 为给定数据集和下游用途指定 VAE 架构、隐变量大小、beta 调度和评估计划
version: 1.0.0
phase: 8
lesson: 02
tags: [vae, latent, generative]
---

给定数据集概况（模态、分辨率、数据集大小）和下游用途（仅重建、采样，或作为隐空间扩散 / token 自回归模型的输入编码器），输出：

1. 变体。普通 VAE、beta-VAE、VQ-VAE、RVQ（残差），或 NVAE。一句话理由，与模态和下游用途相关。
2. 架构。编码器/解码器拓扑（卷积下采样因子、通道宽度、隐藏维度、注意力块）。适用时提及公开参考权重（`sd-vae-ft-ema`、EnCodec、DAC、WAN-VAE）。
3. 隐变量维度。空间和通道维度。每样本总比特数。与原始数据的压缩比。
4. Beta 调度。预热爬坡、最终值、以及 free-bits 阈值（如适用）。
5. 评估计划。重建 MSE / SSIM / PSNR、每维度 KL、活跃维度数、后验崩塌告警阈值、`q(z|x)` 与先验之间的 Frechet 距离。

拒绝在训练开始时使用 beta > 0.5 的 VAE（后验崩塌）。拒绝将普通高斯 VAE 用作图像的最终生成器 — 它会模糊；应将其用作扩散或流匹配模型的隐变量编码器。标记任何码本使用率低于 20% 的 VQ-VAE 为码本重置策略配置不当。