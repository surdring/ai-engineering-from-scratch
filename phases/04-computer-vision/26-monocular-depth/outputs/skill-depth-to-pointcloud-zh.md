---
name: skill-depth-to-pointcloud
description: 从深度图构建点云，正确处理相机内参并导出为 .ply 格式
version: 1.0.0
phase: 4
lesson: 26
tags: [depth, point-cloud, 3d, intrinsics]
---

# 深度图转点云

将深度图和彩色图像转换为带纹理的点云，可导出用于可视化或进一步 3D 处理。

## 使用场景

- 将深度预测可视化为实际的 3D 场景。
- 从单张图像引导稀疏 3D 重建。
- 当运动恢复结构（SfM）失败时为 3DGS 训练生成输入。
- 将预测深度与 LiDAR 真实值进行对比。

## 输入

- `depth`: `(H, W)` numpy 数组，深度单位与输出中想要的单位一致（推荐米）。
- `rgb`: `(H, W, 3)` numpy 数组，颜色（uint8 或 float32 [0, 1]）。
- `intrinsics`: `(fx, fy, cx, cy)`，以像素为单位。
- 可选 `depth_scale`: 用于将预测的深度单位转换为米的乘数。

## 流水线

1. **验证** — 在计划包含的所有像素处，深度必须为正且有限。屏蔽无效像素。
2. **提升** — 每个像素：`X = (u - cx) * d / fx`、`Y = (v - cy) * d / fy`、`Z = d`。
3. **与 RGB 配对** — 每个 3D 点从对应像素获取一个 `(r, g, b)` 三元组。
4. **导出** — PLY（通用）、`.xyz`（轻量级）、`.pcd`（Open3D 原生）、`.las`/`.laz`（地理空间）。

## 实现模板

```python
import numpy as np

def depth_to_point_cloud(depth, intrinsics, depth_scale=1.0, min_depth=0.1, max_depth=100.0):
    H, W = depth.shape
    fx, fy, cx, cy = intrinsics
    v, u = np.meshgrid(np.arange(H), np.arange(W), indexing="ij")
    z = depth.astype(np.float32) * depth_scale
    valid = (z > min_depth) & (z < max_depth) & np.isfinite(z)
    x = (u - cx) * z / fx
    y = (v - cy) * z / fy
    points = np.stack([x, y, z], axis=-1)
    return points, valid


def write_ply(path, points, colors=None, valid_mask=None):
    p = points.reshape(-1, 3)
    if valid_mask is not None:
        p = p[valid_mask.flatten()]
    lines = [
        "ply",
        "format ascii 1.0",
        f"element vertex {p.shape[0]}",
        "property float x", "property float y", "property float z",
    ]
    if colors is not None:
        c = colors.reshape(-1, 3).astype(np.uint8)
        if valid_mask is not None:
            c = c[valid_mask.flatten()]
        lines += ["property uchar red", "property uchar green", "property uchar blue"]
    lines.append("end_header")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
        if colors is not None:
            for pt, col in zip(p, c):
                f.write(f"{pt[0]:.4f} {pt[1]:.4f} {pt[2]:.4f} {col[0]} {col[1]} {col[2]}\n")
        else:
            for pt in p:
                f.write(f"{pt[0]:.4f} {pt[1]:.4f} {pt[2]:.4f}\n")
```

## 报告

```
[export]
  input depth shape:  (H, W)
  valid points:       <N> / <H*W>
  output format:      ply | xyz | pcd | las
  coordinate system:  相机坐标系（+X 右, +Y 下, +Z 前）
  scale:              米 | 毫米 | 归一化
```

## 规则

- 始终屏蔽无效深度（零、NaN、inf、饱和值）；包含这些值会在原点产生大量无用点云。
- 对于来自相对深度模型的预测，不要以度量单位导出；在输出文件名前加 `relative_` 以表明坐标约定。
- 保持相机坐标约定一致（OpenCV：+X 右, +Y 下, +Z 前）。如果下游工具期望 OpenGL（+Y 上），则交换符号。
- 对于密集场景（> 1M 点），提供子采样参数；超过 500 MB 的 PLY 文件在各种地方都难以加载。
- 绝不要静默地裁剪深度以产生"合理"的输出；使用带告警的阈值明确裁剪，以便用户知道哪些被丢弃了。