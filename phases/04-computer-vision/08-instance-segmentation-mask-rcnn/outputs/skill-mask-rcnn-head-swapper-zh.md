---
name: skill-mask-rcnn-head-swapper
description: 生成针对自定义 num_classes 替换 torchvision Mask R-CNN 中边界框头和掩码头所需的确切代码
version: 1.0.0
phase: 4
lesson: 8
tags: [计算机视觉, mask-rcnn, 微调, torchvision]
---

# Mask R-CNN 头部替换器

专门为 Mask R-CNN 生成头部替换样板代码。以下模板假设 `model.roi_heads.box_predictor` 和 `model.roi_heads.mask_predictor` 存在，这仅适用于 `maskrcnn_resnet50_fpn` 和 `maskrcnn_resnet50_fpn_v2`。Faster R-CNN 有边界框预测器但没有掩码预测器；RetinaNet 使用 `RetinaNetHead` 且根本没有 `roi_heads`——这两者需要不同的技能。

## 使用场景

- 在自定义类别集上微调 `maskrcnn_resnet50_fpn` 或 `maskrcnn_resnet50_fpn_v2`
- 将 COCO 上训练的 Mask R-CNN 检查点迁移到非 COCO 类别数
- 调试因 `cls_score.out_features` 或 `mask_predictor` 不匹配而崩溃的 Mask R-CNN 训练

## 适用范围之外

- `fasterrcnn_*`——没有 `mask_predictor`。仅替换 `box_predictor`；使用单独的 Faster R-CNN 头部替换方案
- `retinanet_*`——没有 `roi_heads`；分类头和回归头位于 `model.head.classification_head` 和 `model.head.regression_head` 下。使用 RetinaNet 专用技能
- `keypointrcnn_*`——使用 `keypoint_predictor` 而非 `mask_predictor`

## 输入

- `model_name`：torchvision 检测模型构造函数，如 `maskrcnn_resnet50_fpn_v2`
- `num_classes`：包含背景。一个 4 目标类别的数据集意味着 `num_classes=5`
- `freeze`：`backbone`、`backbone_fpn` 或 `none` 之一

## 步骤

1. 导入模型构造函数和两个预测器类（`FastRCNNPredictor`、`MaskRCNNPredictor`）
2. 加载默认权重预训练模型
3. 用新的 `FastRCNNPredictor(in_features, num_classes)` 替换 `model.roi_heads.box_predictor`
4. 用新的 `MaskRCNNPredictor(in_features_mask, hidden_layer=256, num_classes)` 替换 `model.roi_heads.mask_predictor`
5. 应用请求的冻结策略
6. 打印确认块，列出每个模块的可训练参数

## 输出代码模板

```python
from torchvision.models.detection import {MODEL_NAME}, {MODEL_WEIGHTS}
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor

def build_model(num_classes={NUM_CLASSES}):
    model = {MODEL_NAME}(weights={MODEL_WEIGHTS}.DEFAULT)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    in_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
    model.roi_heads.mask_predictor = MaskRCNNPredictor(in_features_mask, 256, num_classes)

    {FREEZE_BLOCK}

    return model
```

其中 `{FREEZE_BLOCK}` 为：

- `none` -> 空
- `backbone` ->
  ```python
  for p in model.backbone.parameters():
      p.requires_grad = False
  ```
- `backbone_fpn` ->
  ```python
  for p in model.backbone.parameters():
      p.requires_grad = False
  # FPN 参数位于 backbone.fpn 内部
  ```

## 报告

```
[头部替换]
  模型:          <MODEL_NAME>
  num_classes:   <N>（包含背景）
  冻结策略:      <选择>
  可训练参数量:  <N>
  总参数量:      <N>
```

## 规则

- 绝不推荐不包含背景的 `num_classes`；始终提醒用户
- 始终尽可能使用 torchvision 检测模型的 `_v2` 变体；它们比旧版本的预训练权重更好
- 不要在本技能中实例化模型——生成代码块，让用户自行运行
- 如果用户在超过 10,000 张图像的数据集上请求 `freeze backbone`，建议他们也考虑微调骨干网络