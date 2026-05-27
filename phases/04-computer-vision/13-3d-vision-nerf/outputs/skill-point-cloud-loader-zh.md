---
name: skill-point-cloud-loader
description: 为 .ply / .pcd / .xyz 文件编写 PyTorch Dataset，包含正确的归一化、中心化和点采样
version: 1.0.0
phase: 4
lesson: 13
tags: [3d-vision, 点云, 数据加载, pytorch]
---

# 点云加载器

将一个包含 3D 扫描文件的文件夹转化为可训练的 PyTorch `Dataset`。

## 使用场景

- 开始新的点云分类/分割项目
- 在 `.ply`、`.pcd` 和 `.xyz` 格式之间切换
- 调试一个训练无报错但收敛很差的模型；通常是数据加载器的归一化有问题

## 输入

- `data_root`：包含点云文件和可选带标签 CSV 的文件夹
- `file_format`：ply | pcd | xyz | npy
- `num_points`：固定采样大小，通常为 1024 或 2048
- `augmentation`：none | rotate | jitter | mixup

## 归一化策略

每个生产级点云流水线都按以下顺序应用：

1. **中心化**点云：减去质心
2. **缩放**到单位球体：除以到中心的最大距离
3. **采样** `num_points` 个点。如果点云有更多点，使用**最远点采样（FPS）**以获得忠实形状表示，或随机采样以追求速度。如果点更少，则重复点
4. **打乱**点顺序（顺序对模型不重要，但打乱可以打破偶然的顺序依赖）

## 输出模板

```python
import numpy as np
import torch
from torch.utils.data import Dataset

try:
    import open3d as o3d
    HAS_O3D = True
except ImportError:
    HAS_O3D = False

def _read_ply(path):
    if HAS_O3D:
        pc = o3d.io.read_point_cloud(path)
        return np.asarray(pc.points, dtype=np.float32)
    # 退路：最小化的 ascii-ply 读取器
    ...

def _fps(points, k):
    idx = np.zeros(k, dtype=np.int64)
    dist = np.full(len(points), np.inf)
    seed = np.random.randint(len(points))
    idx[0] = seed
    for i in range(1, k):
        dist = np.minimum(dist, ((points - points[idx[i-1]]) ** 2).sum(axis=1))
        idx[i] = int(np.argmax(dist))
    return idx

def normalise(points):
    centre = points.mean(axis=0)
    points = points - centre
    scale = np.max(np.linalg.norm(points, axis=1))
    return points / max(scale, 1e-8)

class PointCloudDataset(Dataset):
    def __init__(self, files, labels, num_points=1024, augment=False):
        self.files = files
        self.labels = labels
        self.num_points = num_points
        self.augment = augment

    def __len__(self):
        return len(self.files)

    def __getitem__(self, i):
        pts = _read_ply(self.files[i])
        pts = normalise(pts)
        if len(pts) >= self.num_points:
            idx = _fps(pts, self.num_points)
            pts = pts[idx]
        else:
            reps = int(np.ceil(self.num_points / len(pts)))
            pts = np.tile(pts, (reps, 1))[:self.num_points]
        # 打乱点顺序以打破任何偶然的依赖（尤其是在平铺点以确定性顺序重复时尤其重要）
        np.random.shuffle(pts)
        if self.augment:
            theta = np.random.uniform(0, 2 * np.pi)
            R = np.array([[np.cos(theta), 0, np.sin(theta)],
                          [0, 1, 0],
                          [-np.sin(theta), 0, np.cos(theta)]], dtype=np.float32)
            pts = pts @ R
            pts = pts + np.random.normal(0, 0.02, pts.shape).astype(np.float32)
        pts = np.ascontiguousarray(pts, dtype=np.float32)
        return torch.from_numpy(pts).transpose(0, 1), int(self.labels[i])
```

## 报告

```
[dataset]
  files:          <N>
  format:         <ply|pcd|xyz|npy>
  points_per_sample: <int>
  normalise:      centre + unit sphere
  sampling:       FPS | random
  augmentation:   <list>
```

## 规则

- 始终先中心化再缩放；交换顺序会改变「单位球体」的含义
- 对于形状任务，优先使用 FPS 而非随机采样；随机采样在分割任务中也可以，因为每个点本来都很重要
- 绝不在评估期间进行数据增强；仅在训练期间
- 如果点云文件包含颜色或法线作为额外通道，扩展 Dataset 返回 `(3 + C, num_points)` 张量，而不仅仅是 xyz