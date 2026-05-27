---
name: generative-model-chooser
description: 为给定的任务和预算选择生成模型家族、骨干网络和托管替代方案
version: 1.0.0
phase: 8
lesson: 01
tags: [generative, taxonomy]
---

给定任务描述（模态、领域、延迟预算、计算预算、条件信号），输出：

1. 模型家族。显式可解（Explicit-tractable）、显式近似（VAE / 扩散模型）、隐式（GAN）、分数/流匹配，或 token 自回归。一句话理由，与模态 + 延迟相关。
2. 骨干 + 开源参考。一个用户今天就能微调的预训练开源权重模型（如 Stable Diffusion 3、Flux.1-dev、AudioCraft 2、StyleGAN3、3D 高斯泼溅）。
3. 托管替代方案。三个生产 API，按质量 / 成本 / 延迟权衡排序（fal.ai、Replicate、Stability、Runway、Veo、Kling、ElevenLabs 等）。
4. 失败模式。所选家族的已知病态（模式崩塌、暴露偏差、采样器漂移、分词器伪影、CLIP-score 博弈）。
5. 预算。单 A100 上的大致训练小时数、每样本推理成本、VRAM 底线。

拒绝在任务需要似然评分时推荐 GAN。拒绝为高分辨率实时场景推荐像素级自回归。标记任何已有开源骨干覆盖该领域时仍建议"从头训练"的推荐。