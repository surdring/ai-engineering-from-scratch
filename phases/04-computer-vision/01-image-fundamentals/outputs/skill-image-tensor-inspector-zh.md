---
name: skill-image-tensor-inspector
description: 检查任意图像形状的张量或数组，报告数据类型、布局、值域范围，以及它看起来是原始像素、归一化还是标准化状态
version: 1.0.0
phase: 4
lesson: 1
tags: [计算机视觉, 调试, 预处理, 张量]
---

# 图像张量检查器

一个诊断技能，适用于视觉流水线中任何持有图像形状数组、需要确切知道它处于何种状态的时候。

## 使用场景

- 预训练模型返回垃圾预测，你怀疑预处理有问题
- 在 OpenCV 和 torchvision 之间迁移流水线，通道顺序不明确
- 从多个框架堆叠层，批次轴总是出现在错误位置
- 调试损失卡在 `log(num_classes)` 的训练循环

## 输入

- `x`：任意 2-D、3-D 或 4-D 类数组（NumPy、PyTorch、JAX）
- 可选 `expected`：用于对照检查的不变量字典，如 `{"layout": "CHW", "range": "standardized"}`

## 步骤

1. **解析后端**——检测 `x` 是 NumPy、Torch 还是 JAX。转换为 NumPy 进行检查但不修改原始数据。

2. **分类秩（Rank）**：
   - rank 2 -> 单通道图像 (H, W)
   - rank 3 -> 如果最后一轴为 1、3 或 4 且严格小于其他两轴，则为 `HWC`；否则 `CHW`
   - rank 4 -> 如果第 1 轴在 {1, 3, 4} 中**且**第 2 轴或第 3 轴大于 16，则优先 `NCHW`；否则优先 `NHWC`。纯轴-1 检查会将小图像 NHWC 批次如 `(3, 4, 224, 3)` 误分类
   - 始终将模棱两可的情况（如 `(1, 3, 3, 3)`）标记为 `ambiguous` 而非猜测；需要调用者提供 `expected`

3. **分类数据类型和值域范围**：
   - `uint8` 在 [0, 255] -> `raw`
   - `float*` 且 min >= 0 且 max <= 1.01 -> `normalized`
   - `float*` 且 min < 0 且 |mean| < 0.5 且 0.5 <= std <= 1.5 -> `standardized`
   - 其他 -> `unusual`，打印直方图

4. **逐通道统计**——报告每通道的均值和标准差。如果数组看起来是标准化的，与 ImageNet 均值/标准差比较，输出匹配置信度。

5. **报告**格式如下：

```
[inspector]
  backend:   numpy | torch | jax
  rank:      2 | 3 | 4
  layout:    HW | HWC | CHW | NHWC | NCHW
  dtype:     <dtype>
  shape:     <shape>
  range:     raw | normalized | standardized | unusual
  min/max:   <min> / <max>
  per-channel mean: [ ... ]
  per-channel std:  [ ... ]
  likely source:    camera | PIL | OpenCV | torchvision | random init
  likely target:    display | training | inference
```

6. **根据 `likely target` 推荐下一步操作**：
   - `display`：转置到 HWC，钳位，转换为 uint8
   - `training`：使用数据集统计量进行标准化，转置到 CHW，添加批次轴
   - `inference`：精确匹配模型卡中的不变量

## 规则

- 绝不修改输入。仅输出诊断信息
- 如果提供了 `expected`，对每个不匹配标记 `[expected X got Y]`
- 当布局或通道顺序不明确时，明确指出静默失败风险
- 一次推荐一个操作，而非一系列选项