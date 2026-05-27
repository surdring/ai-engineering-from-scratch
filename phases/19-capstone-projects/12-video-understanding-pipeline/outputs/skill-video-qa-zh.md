---
name: video-qa
description: 构建视频理解流水线，具有场景分割、多向量索引、时序定位和带时间戳的引用。
version: 1.0.0
phase: 19
lesson: 12
tags: [capstone, video, multimodal, gemini, qwen-vl, molmo, transnet, qdrant]
---

给定 100 小时视频，构建摄取流水线和查询系统，用 (start, end) 时间戳加帧预览回答自然语言问题。

构建计划：

1. 摄取视频（YouTube URL 或 MP4）；按需下采样到 720p。
2. 使用 TransNetV2 或 PySceneDetect 的场景分割；输出 `[{scene_id, start_ms, end_ms, keyframe_path}]`。
3. Whisper-v3-turbo（faster-whisper）ASR，产生词级别时间戳；逐场景切片。
4. Gemini 2.5 Pro 或 Qwen3-VL-Max 或 Molmo 2 的 VLM 字幕；输出字幕 + 帧嵌入。
5. Qdrant multi-vector 索引，每场景三个命名向量（caption_emb、frame_emb、transcript_emb）和 payload {video_id, scene_id, start_ms, end_ms, keyframe_url}。
6. 查询：三个并行密集查询；reciprocal rank fusion 合并；top-k=5 场景。
7. 时序定位（TimeLens adapter 或 VideoITG）在 top 场景内细化 (start, end)。
8. VLM 综合（Gemini 2.5 Pro），带 query + top-3 场景片段 + 转录；要求 `(video_id, start_ms, end_ms)` 引用。
9. 在 ActivityNet-QA、NeXT-GQA 上加 100 查询手动标记自定义集上评估。报告总体准确率和逐问题类别（描述性、计数、动作类型）。

评估标准：

| 权重 | 标准 | 测量方式 |
|:-:|---|---|
| 25 | 时序定位 IoU | 保留定位集上的 IoU |
| 20 | QA 准确率 | NeXT-GQA 和 100 查询自定义集 |
| 20 | 摄取吞吐 | 每美元索引的视频小时数 |
| 20 | UI 和引用 UX | 时间戳链接、缩略图条、跳转到帧 |
| 15 | 幻觉率 | 计数和动作类型准确率单独报告 |

硬性拒绝：
- 每场景池化单一向量的流水线。多向量是类别区分能显示的必要条件。
- 没有 (start, end) 引用的答案。
- 报告一个总体准确率而不分解计数/动作子集。
- 不直接接收场景帧的 VLM 综合（仅文本输入失去视觉锚定）。

拒绝规则：
- 拒绝提供许可证来源不清晰的视频；要求每个 video_id 上的许可标签。
- 拒绝在超过测量吞吐的摄取速率下声称「实时」响应。
- 拒绝将计数/动作幻觉数字隐藏在总体准确率数字内。

输出：包含场景分割 + ASR + 字幕流水线、多向量 Qdrant 集合、时序定位适配器、带时间戳深度链接的 Next.js 15 查看器、三基准评估结果（ActivityNet-QA、NeXT-GQA、custom）的仓库，以及指出你观察到的三大计数或动作类型失败类别和减少每个的检索或综合更改的 write-up。