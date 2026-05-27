---
name: skill-cmer-monitor
description: 为生产环境的 VLM 端点配置跨模态错误率（CMER）监控、仪表盘和告警
version: 1.0.0
phase: 4
lesson: 25
tags: [vlm, production, monitoring, hallucination]
---

# CMER 监控器

将跨模态对齐作为一流的生成环境关键绩效指标（KPI）。

## 使用场景

- 部署任何基于图像生成文本的 VLM 端点。
- 调查关于幻觉回复的报告。
- 跟踪输入分布偏移是否降低了模型的对齐质量。

## 输入

- `vlm_output`: 生成的文本。
- `text_confidence`: softmax 后每 token 的平均概率，范围 `[0, 1]`。计算方式为 `exp(mean(log_probs))`。不要传入原始 logits；原始 logits 是无界的，而 `conf_threshold` 依赖于概率值。
- `image_embedding`: 图像的 CLIP 系列嵌入（DINOv3、SigLIP、CLIP）。
- `text_embedding`: 生成文本的 CLIP 系列嵌入。
- 可选的 `prompt_type`: 用于分组的标签（vqa / ocr / captioning / agent）。

## 每请求计算

```python
import torch

def cmer_flag(image_emb, text_emb, text_conf, sim_thr=0.25, conf_thr=0.8):
    if image_emb.shape != text_emb.shape:
        raise ValueError(f"emb shape mismatch: {image_emb.shape} vs {text_emb.shape}")
    image_emb = image_emb / (image_emb.norm() + 1e-8)
    text_emb = text_emb / (text_emb.norm() + 1e-8)
    sim = float((image_emb * text_emb).sum())
    flagged = (text_conf > conf_thr) and (sim < sim_thr)
    return {"sim": sim, "flagged": flagged}
```

嵌入向量是来自独立 CLIP 系列编码器的 1-D PyTorch 张量（`torch.float32`）。如果使用 NumPy 数组，将 `.norm()` 替换为 `np.linalg.norm(...)` 并相应转换输出。

将 `sim`、`text_conf`、`flagged`、`prompt_type`、`timestamp`、`model_version`、`request_id` 存储到你的监控管道（Prometheus、DataDog、OpenTelemetry）中。

## 聚合指标

```
CMER = （窗口内被标记的请求数）/（窗口内总请求数）
```

按端点、prompt_type 和模型版本分别报告。

## 告警阈值

- 基线 CMER：基于 7 天正常流量建立。
- 警告：CMER >= 1.5x 基线持续 1 小时。
- 严重：CMER >= 2x 基线持续 30 分钟，或任何窗口的绝对值 > 15%。

## 仪表盘面板

1. CMER 随时间变化（5 分钟桶，7 天窗口）。
2. 按 prompt_type 分组的 CMER（堆叠柱状图）。
3. 每小时的 `sim` 分布（直方图）。
4. Top 幻觉输出（每天采样 20 个被标记的响应用于人工审查）。

## CMER 飙升时的应对措施

1. 采样被标记的请求。
2. 验证模型版本是否无意中发生了变化。
3. 检查输入分布（新文件格式？新图像来源？不同的压缩方式？）。
4. 将受影响的流量路由到人工审查，直到飙升得以解决。
5. 如果飙升持续，微调或更换模型；不要抑制告警。

## 规则

- 绝不使用 VLM 自身的嵌入来计算 CMER；使用独立的编码器（DINOv3、SigLIP 或 CLIP-L/14）。否则你测量的是模型的内部一致性，而非对齐质量。
- 始终记录原始的 `sim` 值，而不仅仅是 `flagged` 位；在标记率变化之前，下四分位数的分布偏移就能显现。
- 不要在缺少 CMER 监控的情况下部署 VLM 端点；幻觉是主要的生产环境失败模式，没有这个指标就无法被发现。
- 对于敏感领域（医疗、法律、金融），将 `sim_threshold` 提高到 0.35 或更高；标记条件是 `sim < sim_threshold`，更高的阈值会捕获更多输出为潜在偏离实际的 — 对于高风险场景这是正确的默认行为。