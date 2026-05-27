---
name: skill-mot-evaluator
description: 编写完整的 MOTA / IDF1 / HOTA 评估框架，与真实标注轨迹进行对比
version: 1.0.0
phase: 4
lesson: 27
tags: [mot, evaluation, tracking, metrics]
---

# MOT 评估器

将跟踪器的输出封装到标准的 MOTA/IDF1/HOTA 流水线中，以便与文献进行公平比较。

## 使用场景

- 在 MOT17 / MOT20 / DanceTrack / SportsMOT 上对新跟踪器进行基准测试。
- 在自己拍摄的视频上对比 ByteTrack、BoT-SORT、SAM 2。
- 为论文或 PR 描述生成可复现的数值。

## 输入

- `predictions`: 每帧的 `(track_id, x, y, w, h, confidence)` 元组列表。
- `ground_truth`: 每帧的 `(gt_id, x, y, w, h)` 元组列表。
- `iou_threshold`: 通常 MOTA 用 0.5；HOTA 使用扫描方式。
- `evaluator`: `py-motmetrics`（MOTA、IDF1）或 `TrackEval`（HOTA）。

## 输出格式约定

`py-motmetrics` 和 `TrackEval` 都期望特定的磁盘格式：

```
# predictions.txt
<frame>,<track_id>,<x>,<y>,<w>,<h>,<confidence>,-1,-1,-1

# ground_truth.txt
<frame>,<gt_id>,<x>,<y>,<w>,<h>,1,-1,-1,-1
```

帧从 1 开始编号，边界框格式为 (x, y, w, h)，而非 (x1, y1, x2, y2)。格式转换是大多数集成 bug 的来源。

## 步骤

1. 将跟踪器的输出转换为 MOT Challenge 文本格式。
2. 对两个文件分别运行 `py-motmetrics.io.loadtxt`。
3. 使用 `mm.metrics.create().compute()` 计算 MOTA + IDF1。
4. 对于 HOTA，使用相同文件调用 `TrackEval` 并设置 `Metrics: HOTA`。
5. 将结果保存为 JSON 供仪表盘使用。

## 实现概要

```python
import motmetrics as mm

def evaluate_mota_idf1(pred_path, gt_path):
    gt = mm.io.loadtxt(gt_path, fmt="mot15-2D")
    pred = mm.io.loadtxt(pred_path, fmt="mot15-2D")
    acc = mm.utils.compare_to_groundtruth(gt, pred, dist="iou", distth=0.5)
    metrics = mm.metrics.create().compute(
        acc, metrics=["num_frames", "mota", "motp", "idf1", "idp", "idr", "num_switches"]
    )
    return metrics


def write_mot_txt(predictions, path):
    with open(path, "w") as f:
        for frame_idx, detections in enumerate(predictions, start=1):
            for tid, x, y, w, h, conf in detections:
                f.write(f"{frame_idx},{tid},{x:.2f},{y:.2f},{w:.2f},{h:.2f},{conf:.3f},-1,-1,-1\n")
```

## 报告

```
[mot evaluation]
  frames:     <整数>
  gt tracks:  <整数>
  pred tracks: <整数>

[metrics]
  MOTA:       <浮点数>
  MOTP:       <浮点数>
  IDF1:       <浮点数>
  IDP/IDR:    <浮点数/浮点数>
  ID switches: <整数>
  HOTA:       <浮点数>  （来自 TrackEval）
```

## 规则

- 输出文本文件中的帧始终从 1 开始编号；MOT 工具链期望如此。
- 在写入之前将 (x1, y1, x2, y2) 转换为 (x, y, w, h)。
- 在现代比较中不要只报告 MOTA；应包含 IDF1 和 HOTA。
- 注意 MOT17 上的私有检测与公共检测 — 它们是分开评估的，混合使用会虚高分数。
- 记录每个序列的分数；汇总分数会掩盖在单个困难序列上的失败。