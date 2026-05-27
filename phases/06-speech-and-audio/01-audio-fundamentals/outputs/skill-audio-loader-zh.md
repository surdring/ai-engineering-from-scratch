---
name: audio-loader
description: 根据目标模型的预期验证原始音频文件并安全重采样
version: 1.0.0
phase: 6
lesson: 01
tags: [audio, speech, preprocessing]
---

给定一个音频文件（路径、声道数、采样率、位深度、编解码器）和目标模型（ASR / TTS / 分类器，具有要求的采样率和声道数），输出：

1. 不匹配项。列出文件与目标不一致的每个维度（采样率、声道数、最小时长、削波检查）。
2. 重采样方案。源采样率、目标采样率、重采样库（`torchaudio.transforms.Resample` 或 `librosa.resample`）、抗混叠滤波器类型。
3. 声道方案。单声道折叠策略（平均值 vs 仅左声道），或当模型支持时保留多声道直通。
4. 归一化。峰值归一化 vs RMS 归一化，dBFS 目标值，削波保护。
5. 验证代码片段。加载文件、执行变换、并断言最终数组匹配 `(target_sr, dtype, channel_count, range)` 的 Python 代码。

拒绝在没有抗混叠滤波器的情况下进行降采样。拒绝在没有重建滤波器的情况下进行超过 2 倍的上采样。标记任何削波峰值超过 ±0.999 或直流偏移超过 ±0.01 的输入文件。