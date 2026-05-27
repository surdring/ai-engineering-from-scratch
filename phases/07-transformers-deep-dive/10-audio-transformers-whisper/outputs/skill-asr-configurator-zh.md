---
name: asr-configurator
description: 为新的语音流水线选择 ASR 模型（Whisper 变体 / Moonshine / faster-whisper）和解码参数
version: 1.0.0
phase: 7
lesson: 10
tags: [transformers, whisper, asr, speech]
---

给定语音任务（转录 / 翻译 / 流式 / 端侧）、语言、音频特征（噪声、口音、时长）以及延迟/质量目标，输出：

1. 模型选择。以下之一：faster-whisper large-v3-turbo（默认生产选择）、whisper large-v3（最高质量，多语言）、whisper medium（中级）、Moonshine base（边缘设备）、distil-whisper（2× 更快的英语）。一句话理由。
2. 量化。int8_float16（CPU 默认）、float16（GPU 默认）、fp32（研究）。标记 VRAM 影响。
3. 解码。束搜索宽度（典型值 5，流式用 1）、温度回退计划、log-prob 阈值、无声阈值、VAD 门控开启/关闭。
4. 分块。30 秒固定窗口 vs 流式分块（通常 10 秒带 2 秒重叠）+ 基于 VAD 的分割。记录重叠部分的后合并策略。
5. 后处理。时间戳对齐（WhisperX 强制对齐）、标点恢复、说话人日记化（pyannote）。标记哪些是任务所需的。

拒绝为生产环境推荐原始 OpenAI Whisper（参考实现）— `faster-whisper` 速度快 4 倍且输出相同。拒绝在没有 VAD 的情况下交付流式 ASR，除非有说明文档。标记任何在输入可能多说话人时的单说话人假设。