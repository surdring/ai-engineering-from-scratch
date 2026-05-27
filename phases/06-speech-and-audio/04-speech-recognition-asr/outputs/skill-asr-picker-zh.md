---
name: asr-picker
description: 为给定的部署目标选择 ASR 模型、解码策略、分块和语言模型融合方式
version: 1.0.0
phase: 6
lesson: 04
tags: [audio, asr, speech-recognition]
---

给定部署目标（语言列表、领域、延迟预算、硬件、离线/流式、音频时长），输出：

1. 模型。Whisper-large-v3-turbo / Parakeet-TDT / Canary-Flash / wav2vec 2.0 / Moonshine。一句话理由。
2. 解码。贪心解码 / 束搜索宽度 / 温度回退 / 语言模型融合权重。理由与质量预算相关。
3. 分块和 VAD。块长度、步长、是否使用 Silero-VAD 或 Whisper 自带的进行门控。
4. 语言策略。强制指定语言 vs 自动语言识别；如何处理跨语言帧。
5. 评估方案。领域测试集上的词错误率（WER）、按说话人覆盖率、静音片段上的幻觉率。

拒绝在没有 VAD 门控的情况下部署长音频 Whisper（静音时容易产生幻觉）。拒绝在未进行文本归一化（小写、标点去除）的情况下报告 WER。标记任何束搜索宽度 > 16 且没有语言模型的情况；原始束搜索在空白符上效果不佳。