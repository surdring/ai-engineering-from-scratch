---
name: unified-gen-model-picker
description: 在 Show-o / Transfusion / Emu3 / Janus-Pro 系列之间选择，用于需要多模态理解和生成且使用开放权重的产品
version: 1.0.0
phase: 12
lesson: 14
tags: [show-o, masked-diffusion, unified, t2i, inpainting]
---

给定一个需要统一理解 + 生成（VQA、图像描述、T2I，可选的修复）且具有开放权重约束和延迟预算的产品，选择一个模型系列并输出参考配置。

生成：

1. 系列裁决。Show-o（掩码离散扩散）、Transfusion / MMDiT（连续扩散）、Emu3 / Chameleon（自回归离散）或 Janus-Pro（解耦编码器）。
2. 推理步数预算。Show-o 16 步，Transfusion 20 步，Emu3 1024+ 步。用用户延迟预算论证所选。
3. 修复（Inpainting）支持。Show-o 免费支持；Transfusion 添加掩码通道；Emu3 需要单独微调。为用户标记此项。
4. 分词器选择。对于离散系列，推荐 IBQ / MAGVIT-v2 / SBER；对于连续系列，推荐 SD3 的 VAE。
5. 训练稳定性。双损失（Transfusion）需要权重调优；Show-o 的单损失更简洁。
6. 迁移路径（如果用户业务增长）。当质量成为限制时从 Show-o 迁移到 Transfusion。

硬拒绝：
- 当推理延迟 <10 秒/张图像时提议 Emu3 / Chameleon。对约 1024 个 token 的自回归太慢了。
- 声称 Show-o 在前沿图像质量上与 Transfusion 匹敌。不匹配。分词器是上限。
- 为需要 VQA 的产品推荐 Stable Diffusion。SD 无法推理图像。

拒绝规则：
- 如果用户想要 <2 秒/张图像的生成速度，拒绝 Show-o 并推荐 Stable Diffusion + 单独的 VLM 用于理解。接受多模型复杂性。
- 如果用户想要具有开放权重的「最佳级别质量」，拒绝 Show-o / Emu3 并推荐 Transfusion 系列（MMDiT）或 JanusFlow。
- 如果用户无法提交分词器选择（担心许可、质量上限），拒绝仅离散系列并推荐 Transfusion。

输出：一页选择，包含系列裁决、步数预算、修复支持、分词器推荐、稳定性计划、迁移路径。以 arXiv 2408.12528 (Show-o)、2408.11039 (Transfusion)、2501.17811 (Janus-Pro) 结尾。