---
name: sd-toolkit-composer
description: 在 SD / Flux 基础模型上组合 ControlNet、LoRA 和 IP-Adapter
version: 1.0.0
phase: 8
lesson: 08
tags: [controlnet, lora, ip-adapter, diffusion]
---

给定任务（目标图像）、输入（Prompt、参考图像、姿态/深度/涂鸦/分割、主体身份）和基础模型（SDXL、SD3.5、Flux.1-dev），输出：

1. ControlNet 组合。使用哪些 ControlNet（边缘/姿态/深度/涂鸦/分割/线稿/瓦片）、权重多少、顺序如何。权重总和 ≤ 1.5。
2. LoRA 组合。指定的 LoRA、秩、alpha 值。当 alpha > 1.5 或多个 LoRA 针对同一概念时发出警告。
3. IP-Adapter。不使用、普通版或 FaceID 变体；典型权重 0.4-0.8。
4. 文本提示 + 负面提示。关键词顺序、token 预算、负面提示框架。
5. 采样器 + CFG + 种子。Euler A / DPM-Solver++ / LCM；CFG 尺度与基础模型绑定。可复现的种子方案。
6. QA 检查清单。视觉检查 ControlNet 偏移、LoRA 过饱和、IP-Adapter 身份泄露、解剖问题。

拒绝在 SDXL 基础上堆叠 SD 1.5 的 LoRA（维度不匹配）。拒绝以权重 1.0 运行 3 个以上 ControlNet（特征冲突）。标记在用户有 SDXL 或 Flux 的 GPU 预算时仍推荐 SD 1.5。标记用少于 10 张图像训练身份 LoRA 可能过拟合。