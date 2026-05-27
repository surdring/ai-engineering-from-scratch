---
name: skill-heatmap-to-coords
description: 编写每个生产级姿态模型都使用的亚像素热力图到坐标的转换程序
version: 1.0.0
phase: 4
lesson: 21
tags: [keypoint, pose, subpixel, inference]
---

# 热力图转坐标

将原始关键点热力图转换为亚像素精度的坐标。这是每个姿态流水线中性价比最高的精度提升手段。

## 使用场景

- 部署基于热力图的关键点模型。
- 基准测试姿态指标 — OKS 对亚像素精度极为敏感。
- 将姿态代码从一个框架移植到另一个框架。

## 输入

- `heatmaps`: `(N, K, H, W)` 张量，来自模型的每个关键点热力图。
- `confidence_threshold`: 丢弃峰值低于此值的关键点。

## 步骤

1. **Argmax** 每个热力图，找到整数峰值位置。
2. **一阶差分偏移** — 从相邻像素估计亚像素偏移。系数 `0.25` 是针对 `sigma >= 1` 的高斯热力图标定的启发式值；对于更精确的亚像素恢复，使用完整的二次拟合（DARK）或高斯拟合。

```
dx = 0.25 * sign(heatmap[y, x+1] - heatmap[y, x-1])
dy = 0.25 * sign(heatmap[y+1, x] - heatmap[y-1, x])
```

对于 DARK / 二次拟合变体，使用局部二次近似：

```
dx = -0.5 * (heatmap[y, x+1] - heatmap[y, x-1])
        / (heatmap[y, x+1] - 2 * heatmap[y, x] + heatmap[y, x-1] + eps)
```

二次拟合在尖锐的热力图上更准确；当热力图有噪声时，基于符号的偏移是更安全的默认选择。

3. **将偏移量加到**整数峰值上。
4. **置信度** — 返回每个关键点的峰值；调用方用于屏蔽低置信度预测。
5. **边界情况** — 当峰值落在某轴上的第一个或最后一个像素时，某一侧的邻居被限制（clamp）；偏移量归零，这是最安全的回退方案。

## 输出模板

```python
import torch

def heatmap_to_coords_subpixel(heatmaps, threshold=0.2):
    N, K, H, W = heatmaps.shape
    flat = heatmaps.reshape(N, K, -1)
    conf, idx = flat.max(dim=-1)
    ys = (idx // W).float()
    xs = (idx % W).float()

    ys_int = ys.long()
    xs_int = xs.long()

    x_minus = (xs_int - 1).clamp(min=0)
    x_plus = (xs_int + 1).clamp(max=W - 1)
    y_minus = (ys_int - 1).clamp(min=0)
    y_plus = (ys_int + 1).clamp(max=H - 1)

    batch_idx = torch.arange(N).view(-1, 1).expand(-1, K)
    kp_idx = torch.arange(K).view(1, -1).expand(N, -1)

    dx_raw = (heatmaps[batch_idx, kp_idx, ys_int, x_plus]
              - heatmaps[batch_idx, kp_idx, ys_int, x_minus])
    dy_raw = (heatmaps[batch_idx, kp_idx, y_plus, xs_int]
              - heatmaps[batch_idx, kp_idx, y_minus, xs_int])
    dx = 0.25 * torch.sign(dx_raw)
    dy = 0.25 * torch.sign(dy_raw)

    at_left = xs_int == 0
    at_right = xs_int == (W - 1)
    at_top = ys_int == 0
    at_bottom = ys_int == (H - 1)
    dx = torch.where(at_left | at_right, torch.zeros_like(dx), dx)
    dy = torch.where(at_top | at_bottom, torch.zeros_like(dy), dy)

    refined_x = xs + dx
    refined_y = ys + dy
    coords = torch.stack([refined_x, refined_y], dim=-1)
    mask = conf >= threshold
    return coords, conf, mask
```

## 报告

```
[subpixel decode]
  keypoints:   K
  threshold:   <浮点数>
  valid_rate:  高于阈值的关键点比例
```

## 规则

- 始终将邻居索引限制（clamp）在有效范围内；边缘关键点的差分偏移为零，但不会崩溃。
- 返回置信度以及坐标，以便调用方可以屏蔽低置信度点。
- 亚像素优化仅在热力图在峰值附近平滑时才有帮助 — 检查训练时是否使用了 sigma >= 1 的高斯目标。
- 对于非常小的热力图分辨率（< 48x48），考虑在提取坐标之前将热力图上采样到完整图像尺寸；亚像素偏移随步长缩放。