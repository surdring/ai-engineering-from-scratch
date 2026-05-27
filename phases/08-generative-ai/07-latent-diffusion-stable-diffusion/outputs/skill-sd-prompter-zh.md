---
name: sd-prompter
description: 为给定的 Prompt、风格和质量要求配置 Stable Diffusion / Flux 推理
version: 1.0.0
phase: 8
lesson: 07
tags: [stable-diffusion, flux, latent-diffusion]
---

给定 Prompt、目标风格和质量要求（快速预览 / 作品集质量 / 印刷级），输出：

1. 模型 + 检查点。SD 1.5（旧版工具）、SDXL-base + refiner、SDXL-Turbo（快速）、SD3.5-Large、Flux.1-dev（最佳开源）、Flux.1-schnell（快速开源），或托管 API（DALL-E 3、Imagen 4、Midjourney v7）。一句话理由。
2. 采样器。Euler A（创意）、DPM-Solver++ 2M Karras（稳定）、LCM（快速），或流匹配采样器（SD3/Flux）。含步数。
3. CFG 尺度。Turbo / LCM 用 0，Flux 用 3-4，SDXL 用 5-7，SD1.5 用 7-10。记录权衡关系。
4. 附加组件。ControlNet（姿态、深度、边缘、分割）、IP-Adapter（参考图像）、LoRA（风格或主体）、SD3+ 的 T5 开关。
5. 负面提示。显式空字符串 vs 填充内容（瑕疵、低质量、错误解剖）区别很大；两者都需指定。

拒绝 SDXL+ 使用 CFG > 10（输出饱和）。拒绝在非旧版检查点上使用 > 50 采样步数（质量在 30 步已趋于平缓）。拒绝混用不同基础模型训练的 LoRA（SD 1.5 的 LoRA 用于 SDXL 会静默失效）。标记任何生成逼真人物的请求，必须提醒 NSFW、深度伪造和版权政策。