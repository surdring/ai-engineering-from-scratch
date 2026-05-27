---
name: video-brief
description: 将视频需求转化 2026 年视频生成器的模型 + Prompt + 镜头计划
version: 1.0.0
phase: 8
lesson: 10
tags: [video, diffusion, sora, veo, kling]
---

给定视频需求（时长、宽高比、风格、主体、摄影计划、音频需求、保真度要求、预算），输出：

1. 模型 + 托管。Sora、Veo 3、Kling 2.1、Runway Gen-3、Pika 2.0、CogVideoX、HunyuanVideo、WAN 2.2，或 Mochi-1。一句话理由，与时程/质量/许可证相关。
2. Prompt 框架。(a) 摄影语言（远景、跟拍、推轨、升降、手持），(b) 主体 + 动作，(c) 灯光 + 风格，(d) 负面提示或风格开关。Sora 目标 50-150 个 token，Runway 目标 20-60 个。
3. 镜头计划。单片段 vs 拼接多镜头、关键帧或首帧锚点、每镜头的 I2V vs T2V。
4. 种子 + 可复现性。每镜头种子、版本固定、工具仓库。
5. QA 检查清单。逐帧检查闪烁、身份一致性、物理违规、水印合规。
6. 音频。Veo 3 原生支持，否则外加（ElevenLabs、Suno 或授权音轨 + 口型同步）。

拒绝承诺在免费层上生成 > 10 秒 1080p 的连续运动（Pika/Kling/Runway 上限 10 秒；更长的运行需要拼接）。拒绝在无授权的情况下生成真实人物的肖像。标记任何暗示 2026 年实时 4K 生成的需求 — 当前最佳是托管端点上每 6 秒 1080p 片段约需 30 秒生成时间。