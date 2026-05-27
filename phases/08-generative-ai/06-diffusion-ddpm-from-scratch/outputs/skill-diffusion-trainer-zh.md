---
name: diffusion-trainer
description: 配置扩散模型训练：调度器、预测目标、采样器和评估计划
version: 1.0.0
phase: 8
lesson: 06
tags: [diffusion, ddpm, training]
---

给定数据集概况（模态、分辨率、数据集大小）、计算预算（GPU 小时、VRAM 底线）和质量要求（FID 目标或下游用途），输出：

1. 调度器。线性、余弦（Nichol），或 sigmoid。步数 T（DDPM 基线用 1000；更快变体用 256）。
2. 预测目标。epsilon、v-prediction，或 x_0。理由与分辨率和调度中各阶段的信噪比相关。
3. 架构。像素扩散用 U-Net 深度 + 通道宽度，隐空间扩散用 DiT，视频用 3D U-Net / DiT。包含时间嵌入方案（正弦 + MLP、FiLM，或 AdaLN）。
4. 采样器。DDIM（20-50 步）、DPM-Solver++（10-20）、Euler-A（创意生成），或蒸馏 1-4 步。包含引导尺度（CFG w）推荐。
5. 评估计划。FID / KID / CLIP-score / 人工偏好，含样本数量（FID 需 ≥ 10k），CFG w 的扫描方案。

拒绝在 >= 256×256 分辨率上推荐像素空间扩散训练，因为隐空间扩散以 1/16 的 FLOPs 实现相同质量。拒绝交付没有 CFG 的条件生成模型 — 条件模型的无条件零样本采样通常会产生退化的结果。标记任何 beta_T > 0.1 的调度器可能在训练中产生饱和或不稳定。