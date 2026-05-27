---
name: speaker-verifier
description: 设计说话人验证或说话人日记化流水线，包含模型选择、注册协议和阈值调优
version: 1.0.0
phase: 6
lesson: 06
tags: [audio, speaker, verification, diarization]
---

给定目标（验证 vs 识别 vs 日记化、领域、声道、威胁模型）和数据（用于阈值调优的小时数、说话人数量、注册音频预算），输出：

1. 嵌入器。ECAPA-TDNN / WavLM-SV / ReDimNet / x-vector。说明理由。
2. 注册协议。音频片段数、最小时长、噪声门控、声道匹配。
3. 评分。余弦相似度 / PLDA；是否使用 AS-norm；参考人群规模。
4. 阈值。目标 FAR（欺诈风险）或 EER；调优集规模。
5. 防伪防御。防伪模型（AASIST、RawNet2）、活体挑战，或重放检测。

拒绝任何没有防伪前端的欺诈级别的部署。拒绝在未报告评估集、声道和音频时长分布的情况下发布 EER。标记在不同领域间固定余弦阈值而不重新调优的做法。