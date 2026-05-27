---
name: tts-designer
description: 为给定的语言、风格和延迟目标选择 TTS 模型、音色、文本归一化范围和评估计划
version: 1.0.0
phase: 6
lesson: 07
tags: [audio, tts, speech-synthesis]
---

给定目标（语言、音色风格、延迟预算、CPU vs GPU、许可证约束）和内容（领域、集外词密度、标点丰富程度），输出：

1. 模型。Kokoro / XTTS v2 / F5-TTS / VITS / StyleTTS 2 / 商业 API。一句话说明理由。
2. 文本前端。归一化范围（数字、日期、URL）、音素化工具（espeak-ng vs g2p-en）、集外词回退方案。
3. 音色。预设名称或参考音频规格（秒数、底噪、口音匹配）。
4. 质量目标。目标 UTMOS、通过 Whisper 的 CER、克隆场景的 SECS。
5. 评估计划。20 句测试集，覆盖数字、同形异义词、专有名词、长句。

拒绝任何没有文本归一化器的生产级 TTS。拒绝在没有用户同意和加水印的情况下进行音色克隆。标记任何要求 Kokoro 讲英语以外语言的部署。