---
name: skill-vit-patch-and-pos-embed-inspector
description: 验证 ViT 的 patch embedding 和位置编码（Positional Embedding）形状与模型预期序列长度是否匹配
version: 1.0.0
phase: 4
lesson: 14
tags: [vision-transformer, 调试, pytorch]
---

# ViT Patch 与位置编码检查器

最常见的 ViT 移植 bug：将 224x224 预训练的检查点加载到配置为 384x384 的模型中（或反过来）。位置编码的序列长度不对，模型静默地产生垃圾输出。

## 使用场景

- 在非默认分辨率下微调预训练 ViT
- 审查 ViT-B/16 和 ViT-B/32 之间权重迁移为何失败；检查器将标记 patch-size 不匹配，让调用者知道应该切换架构而不是强制迁移
- 调试一个加载无误但训练效果很差的 ViT

## 输入

- `model`：一个已实例化的 ViT `nn.Module`
- `expected_image_size`：模型在生产环境中将处理的 H x W
- `patch_size`：预期的 patch 大小

## 步骤

1. 定位模型内部的 patch embedding 卷积。报告其 `kernel_size`、`stride`、`in_channels`、`out_channels`
2. 计算预期的 patch 数量。对于方形图像：`(image_size / patch_size)^2`。对于矩形：`(H / patch_size) * (W / patch_size)`。要求 `H % patch_size == 0` 且 `W % patch_size == 0`；否则标记并拒绝
3. 定位学习的位置编码。报告其形状 `(1, N, dim)`
4. 比较 `N` 与 `num_patches + 1`（有 CLS token）或 `num_patches`（无 CLS token）。不匹配意味着检查点是在不同分辨率或 patch 大小下预训练的
5. 检查 patch conv 的 `out_channels` 是否等于位置编码的 `dim`
6. 如果模型应该为新分辨率插值位置编码，验证插值工具是否存在（大多数 `timm` ViT 通过 `resize_pos_embed` 自动完成）

## 报告

```
[vit-inspector]
  image_size:          HxW
  patch_size:          <整数>
  num_patches（计算）: <整数>
  patch_conv:          k=<整数>  s=<整数>  in=<整数>  out=<整数>
  pos_embed 形状:      (1, N, dim)
  有 CLS token:        yes | no
  pos_embed N:         <整数>    预期: <整数>
  结论:                ok | 不匹配

[如果不匹配]
  操作:  为新的序列长度重新初始化 pos_embed
  工具:   timm.models.vision_transformer.resize_pos_embed
```

## 规则

- 绝不在无警告的情况下静默插值；将此操作暴露给用户，让他们知道预训练的位置结构可能已经偏移
- 如果 patch_size 不匹配，拒绝推荐插值——切换到正确的架构
- 不要尝试原地修复模型；报告并建议