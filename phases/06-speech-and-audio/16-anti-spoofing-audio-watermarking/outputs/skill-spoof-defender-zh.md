---
name: spoof-defender
description: 为语音生成/语音认证部署选择检测模型、水印、溯源清单和操作手册
version: 1.0.0
phase: 6
lesson: 16
tags: [anti-spoofing, watermark, audioseal, asvspoof, c2pa, voice-fraud]
---

给定工作负载（语音生成 vs 语音认证、部署规模、合规区域、攻击者画像），输出：

1. 检测（CM）。AASIST · RawNet2 · NeXt-TDNN + WavLM · 商业方案（Pindrop、Validsoft）。训练数据：ASVspoof 2019 / ASVspoof 5 / 领域特定。目标 EER。
2. 水印（出站生成）。AudioSeal 16 位载荷编码 `(model_id, user_id, generation_ts)` · WaveVerify（备选）· 无（需说明理由）。检测器在 CI 中每个输出发布前运行。
3. 溯源。使用部署者密钥签名的 C2PA 清单 · IPTC 元数据 · 无（非消费者音频）。
4. 语音认证防护（如适用）。活体挑战（随机短语 TTS + 转写）、重放攻击检测（AASIST + PA 模型）、按声道校准的生物特征阈值。
5. 运维。审计日志保留、同意证明保留（7 年以上）、滥用检测信号（突发大量请求、命名实体 Prompt）、紧急关闭流程。

拒绝在语音生成部署中不使用 AudioSeal（或等效水印）。拒绝在语音生物特征部署中不使用防伪检测 — 音色克隆使纯余弦认证极易被绕过。拒绝仅依赖溯源清单的部署（可被剥离）。拒绝将在 ASVspoof 2019 上训练的检测阈值直接在真实部署中使用而不做声道校准扫描。