---
name: vad-tuner
description: 为语音智能体选择 VAD 模型、阈值、静音延迟、预滚动和轮流发言检测策略
version: 1.0.0
phase: 6
lesson: 14
tags: [vad, silero, cobra, turn-detection, flush-trick]
---

给定工作负载（消费级 / 呼叫中心 / 边缘 / 无障碍；噪声特征；语言组合；延迟），输出：

1. VAD。Silero VAD（默认）· Cobra（商业级准确率）· pyannote 分割（日记化级别）· WebRTC VAD（旧版/轻量）。一句话说明理由。
2. 参数。阈值（0.3-0.5）、最短语音（200-300 ms）、静音延迟（400-800 ms）、预滚动（250-500 ms）。
3. 语义轮流发言检测。启用（LiveKit 轮流检测器或自定义 MLP）或不启用。理由与预期的用户语音模式相关。
4. Flush 技巧。启用（如果 STT 支持 — Kyutai / Deepgram）或不启用。预期的延迟节省。
5. 防护。拒绝短于最短时长的语音片段；始终保留预滚动；限制每用户的静音延迟覆盖；如果 VAD 服务宕机则 fail-open（将所有内容视为语音）。

拒绝在生产中使用纯能量 VAD — 噪声太大。拒绝零静音延迟 — 会打断用户。拒绝在有专用 Silero 可用时使用基于 Whisper 的 VAD（更慢且准确率更低）。