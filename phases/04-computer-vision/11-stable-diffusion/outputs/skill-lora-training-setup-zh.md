---
name: skill-lora-training-setup
description: 为自定义数据集编写完整的 LoRA 训练配置，包括标注文本、秩、批次大小和学习率
version: 1.0.0
phase: 4
lesson: 11
tags: [计算机视觉, stable-diffusion, lora, 微调]
---

# LoRA 训练设置

将微调意图描述转化为具体的训练配置，可直接传给 `diffusers` 或 `kohya_ss`。

## 使用场景

- 为特定主题（人物、物体、角色）、风格（艺术家、品牌）或概念（姿势、光影）训练 LoRA
- 用更多数据扩展现有 LoRA
- 调试输出欠拟合或过拟合训练图像的 LoRA 训练

## 输入

- `purpose`：subject | style | concept
- `num_images`：可用训练图像数量
- `base_model`：SD 1.5 | SDXL | SD3 | FLUX
- `gpu_vram_gb`：8 | 12 | 16 | 24 | 48+
- `caption_source`：manual | BLIP2-generated | dataset-native

## 秩（Rank）选择器

| 目的   | Rank  | Alpha    |
|--------|-------|----------|
| 主题   | 8-16  | rank     |
| 风格   | 16-32 | rank * 2 |
| 概念   | 32-64 | rank     |

更高的 rank = 更多容量，在小数据集上有更高的过拟合风险。Alpha 缩放 LoRA 的效果强度；`alpha == rank` 是安全的默认值。风格有记录的例外：`alpha == rank * 2` 提供更强的风格推进效果，代价是风格烙印过深的风险更高——仅在主题保真度不是目标时使用。

## 训练步数目标

- `主题` 包含 5-20 张图像：500-1500 步
- `风格` 包含 30-100 张图像：1500-4000 步
- `概念` 包含 100+ 张图像：4000-10000 步

过犹不及——一个已记忆训练图像的 LoRA 无法泛化。

## 学习率

- 文本编码器 LoRA：SD 1.5 使用 `1e-4`，SDXL 使用 `5e-5`
- U-Net LoRA：SD 1.5 使用 `1e-4`，SDXL 使用 `1e-4`
- FLUX / SD3：Transformer 使用 `5e-5`，文本编码器通常冻结
- 当 `num_images < 15`（主题）或训练超过 3000 步时，学习率减半；小数据集和长训练都受益于更温和的更新

## 调度器

- `cosine_with_warmup`（默认）：在前 5-10% 步进行预热，然后余弦衰减。当 `steps >= 1000` 时使用；衰减尾部产生更锐利的最终样本
- `constant`：仅在极短训练（`steps < 500`）或恢复之前的 LoRA 训练且希望保留当前已学特征而不重新退火时使用

## 标注格式

- 主题：在每个标注文本前附加一个唯一的触发词（"myperson"）。保持触发词罕见，以免覆盖已有概念。避免真实词汇和常见名称
- 风格：在每个标注文本末尾附加一个独特的风格标签（"...in mystyle style"）。标签本身视为一个罕见的触发词——使用 `mystyle`，而不是 `impressionism`，后者已映射到真实概念
- 概念：在每个标注文本中描述概念；不需要触发词。概念本身（如 "low-angle shot"）就是锚点

## 输出配置

```yaml
model:
  base: <base_model HF id>
  precision: fp16 | bf16

lora:
  rank: <int>
  alpha: <int>
  targets: unet.cross_attention  # 和/或 unet.to_q, to_k, to_v, to_out

training:
  steps:          <int>
  batch_size:     <int, 根据 gpu_vram_gb 调整>
  grad_accum:     <int, 通常 >=16 GB 时 1, <=12 GB 时 4>
  learning_rate:  <float>
  optimizer:      AdamW8bit | AdamW
  scheduler:      cosine_with_warmup | constant
  warmup_steps:   <int>
  save_every:     <int>

data:
  images_dir:     <path>
  caption_source: <manual | BLIP2 | native>
  trigger_token:   <string if purpose==subject>
  resolution:      <SD 1.5 用 512, SDXL 用 1024>
  aspect_ratio_bucketing: true
  augmentation:
    flip:          true
    color_jitter:  false

validation:
  prompts:
    - "<trigger> ...测试提示词..."
    - "<trigger> 在不同场景中"
  every_steps: 250
```

## 报告

```
[lora setup]
  目的:     <subject|style|concept>
  基础模型: <model>
  rank:     <int>
  steps:    <int>
  batch:    <int>   grad_accum: <int>
  lr:       <float>
  显存估计: <float> GB
```

## 规则

- 绝不推荐 `rank > 64`；超过此值，LoRA 变为迷你微调，失去其「适配器」特性
- 对于 `num_images < 5`，强烈警告——基于 1-3 张图像的身份 LoRA 总是会过拟合
- 对于 `gpu_vram_gb < 12`，要求使用 AdamW8bit 和梯度检查点
- 如果 `base_model == FLUX` 且 `gpu_vram_gb < 24`，路由到 `schnell` 变体并注明训练较慢
- 绝不跳过验证提示词；没有样本网格的 LoRA 无法评估