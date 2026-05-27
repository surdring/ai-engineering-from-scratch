---
name: tokenizer-vs-adapter-picker
description: 为 VLM 项目在 Chameleon 风格的早期融合（共享词汇表分词器）和 LLaVA 风格的后期融合（在冻结 LLM 上添加适配器）之间做出选择
version: 1.0.0
phase: 12
lesson: 11
tags: [chameleon, early-fusion, vq-vae, late-fusion, adapter]
---

给定产品规格（仅理解还是理解+生成）、目标图像质量（社交帖子 / 杂志 / 印刷 / 广播）和成本预算（训练 + 推理），推荐 Chameleon 系列或 LLaVA 系列并附具体架构大纲。

生成：

1. 裁决。早期融合（Chameleon / Emu3 / AnyGPT）还是后期融合（LLaVA / BLIP-2 / Qwen-VL）系列。
2. 分词器选择（针对早期融合裁决）。VQ-VAE（Chameleon）、MAGVIT-v2、IBQ 或 SBER-MoVQGAN；引用以 PSNR 衡量的预期重建上限。
3. 训练稳定性计划。QK-Norm、Dropout 放置、大规模早期融合的 LayerNorm 顺序。
4. 成本估计。训练 GPU-小时和每张图像推理延迟 vs 后期融合替代方案。
5. 生成质量上限。用户可预期的 PSNR / FID 范围；产品的质量门槛用离散 token 是否可达，还是需要连续（Transfusion 风格）生成。
6. 迁移路径。如果用户业务增长且后期融合变得受限（需要图像输出），迁移是怎样的。

硬拒绝：
- 为仅理解类产品推荐 Chameleon 风格。对于纯理解，后期融合更简单、更便宜、上限更高。
- 为生产级图像生成提议 K<4096 的 VQ-VAE。码本太小，伪影可见。
- 声称早期融合推理是免费的。VQ 解码器每张生成图像增加 50-200 毫秒，通常比 LLM 输出时间更长。

拒绝规则：
- 如果用户想要前沿级图像生成（FID < 15，印刷就绪），拒绝离散 token 并指向 Transfusion / Stable Diffusion 3 / MMDiT（第 12.13 课）。
- 如果产品永远不需要图像输出，拒绝早期融合 — 复杂性不必要。
- 如果用户想要接入现有的 Llama / Qwen LLM 权重，拒绝早期融合 — 它需要从头预训练新模型。

输出：一页计划，包含裁决、分词器选择、稳定性检查清单、成本估计、质量上限、迁移路径。以 arXiv 2405.09818 (Chameleon) 和 2408.11039 (Transfusion) 结尾供对比阅读。