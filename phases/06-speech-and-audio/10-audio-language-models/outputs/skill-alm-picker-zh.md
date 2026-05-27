---
name: alm-picker
description: 为音频理解任务选择音频-语言模型、基准测试子集、输出模态（文本 vs 语音）和防护措施
version: 1.0.0
phase: 6
lesson: 10
tags: [alm, lalm, qwen-omni, audio-flamingo, gemini-audio, mmau]
---

给定任务（语音 / 声音 / 音乐 / 多音频 / 长音频、输出模态、延迟、许可证），输出：

1. 模型。Qwen2.5-Omni-7B · Qwen3-Omni · SALMONN · Audio Flamingo 3 · AF-Next · LTU · GAMA · Gemini 2.5 Pro (API) · GPT-4o Audio (API)。一句话说明理由。
2. 用于验证的基准测试子集。MMAU-Pro 语音 / 声音 / 音乐 / 多音频 · LongAudioBench · AudioCaps · ClothoAQA。选择与用户任务匹配的维度。
3. 输出模态。仅文本 · 文本 + 语音（Qwen-Omni、GPT-4o Audio）。如需要，为额外的语音解码器做预算。
4. 防护措施。当模型的多音频评分 < 30%（接近随机）时，拒绝需要多音频比较的提示。对于 > 10 分钟的输入，先进行说话人日记化再送入 LALM。
5. 降级策略。何时应回退到专用模型 — Whisper 用于转录、BEATs 用于分类、pyannote 用于日记化。LALM 并非每个子任务的最佳选择。

拒绝在未验证模型在 MMAU-Pro 多音频子集上得分 > 40% 的情况下交付多音频比较任务。拒绝在没有上游日记化的情况下处理长音频（> 10 分钟）。标记任何使用供应商自报数据而未进行独立复验的部署。