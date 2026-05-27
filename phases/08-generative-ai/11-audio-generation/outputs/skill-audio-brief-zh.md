---
name: audio-brief
description: 将音频需求转化为跨 TTS、音乐和音效的模型 + Prompt + 评估计划
version: 1.0.0
phase: 8
lesson: 11
tags: [audio, tts, music, sfx, codec]
---

给定音频需求（任务：TTS / 音乐 / 音效 / 声音克隆、时长、风格、音色或流派、许可证约束、实时或离线、质量要求），输出：

1. 模型 + 托管。ElevenLabs V3、OpenAI TTS、XTTS v2、Suno v4、Udio、Stable Audio 2.5、MusicGen 3.3B、AudioCraft 2，或 GPT-4o 实时。一句话理由。
2. Prompt 格式。TTS：文本 + 声音 Prompt（3-10 秒样本或声音 ID）+ 情绪/节奏标签。音乐：流派 + 乐器配置 + 情绪 + BPM + 结构标记。音效：拟声词 + 声源 + 时长提示。
3. 编解码器 + 生成器 + 声码器链。指定具体编解码器（Encodec 32 kHz、DAC 44 kHz、自定义）和生成器选择（token 自回归 vs 流匹配）。
4. 种子 + 可复现性。种子固定、版本固定、Prompt 哈希。
5. 评估。TTS 用 MOS（平均意见分）或 A/B 对比、音乐用 CLAP 分数、TTS 转录用 CER、音效用用户听感测试。
6. 防护措施。声音克隆同意 + 水印（PerTh / SynthID-audio）、音乐输出的版权扫描、训练数据政策检查。

拒绝在未经声音所有者核实同意的情况下克隆任何声音（录音带时代"3 秒提示"不是同意）。拒绝交付含未授权参考材料的音乐。标记任何目标 < 200 ms 的实时需求如果不使用流式 token 自回归模型 — 基于扩散的音频在 2026 年无法满足亚 300 ms 的首 token 生成时间（TTFB）。