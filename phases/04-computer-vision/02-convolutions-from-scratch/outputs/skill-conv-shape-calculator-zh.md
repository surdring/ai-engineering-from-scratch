---
name: skill-conv-shape-calculator
description: 逐层遍历 CNN 规格，报告每个块的输出形状、感受野和参数量
version: 1.0.0
phase: 4
lesson: 2
tags: [计算机视觉, cnn, 架构, 调试]
---

# 卷积形状计算器

一个用于规划或调试 CNN 的确定性辅助工具。给定输入形状和层规格列表，在不运行模型的情况下追踪形状、感受野和参数量。

## 使用场景

- 设计新 CNN 并希望验证每个降采样落在一个干净的尺寸上
- 阅读论文并将其架构表翻译成代码
- 预训练骨干网络在分类头上因形状不匹配崩溃，你需要知道哪一层改变了空间尺寸
- 在训练之前比较两个骨干网络的参数效率

## 输入

- `input_shape`：`(C, H, W)`
- `layers`：有序的层字典列表。每层支持：
  - `{type: "conv", c_out, k, s, p, groups=1, bias=true}`
  - `{type: "pool", mode: "max"|"avg", k, s, p=0}`
  - `{type: "adaptive_pool", out_h, out_w}`
  - `{type: "flatten"}`
  - `{type: "linear", out_features, bias=true}`

## 步骤

1. **初始化追踪**：`(C, H, W)`，感受野 `1`，有效步幅 `1`，累计参数 `0`

2. **对每一层**，按以下顺序更新：
   - 计算 `C_out`（conv/linear），或保持 `C_in` 不变（pool）
   - 对卷积和池化使用 `(H + 2P - K) / S + 1` 计算空间输出，对自适应池化使用 `out_h/out_w`，对展平操作在进入线性层前输出形状 `(C * H * W, 1, 1)`，线性层输出标量 `1x1`
   - 更新感受野和有效步幅：
     - 卷积/池化：`RF_new = RF_old + (K - 1) * effective_stride`，`effective_stride *= S`
     - 自适应池化：视为具有有效 `S = H_in / out_h`（向下取整）的池化。`RF_new = RF_old + (H_in - 1) * effective_stride_old`；`effective_stride *= S`。注意自适应池化的 RF 等于之前全部空间范围
     - 展平/线性：RF 和有效步幅不再有意义；将其冻结到展平之前的值，并在后续行中省略
   - 计算参数量：
     - 卷积：`C_out * (C_in / groups) * K * K + (有偏置时为 C_out，否则为 0)`
     - 线性：`out_features * in_features + (有偏置时为 out_features，否则为 0)`
     - 池化和展平：0

3. **检测问题**并标记：
   - 非整数输出尺寸（步幅/填充不匹配）
   - 在栈末尾之前 `H_out <= 0`
   - 感受野超过输入尺寸（之后可能存在浪费的计算）
   - 每层参数突然跳跃 10 倍，暗示通道规划有问题

4. **报告**以单表形式呈现：

```
idx  layer                C_in  C_out  K  S  P  H_out  W_out  RF    params     cum_params
1    conv 3x3 s=1 p=1     3     32     3  1  1  224    224    3     896        896
2    conv 3x3 s=2 p=1     32    64     3  2  1  112    112    7     18,496     19,392
3    pool max 2x2         64    64     2  2  0  56     56     11    0          19,392
...
```

5. **摘要行**：最终 `(C, H, W)`，最终感受野，总参数量，警告

## 规则

- 空间尺寸始终返回整数。如果公式产生非整数，标记为错误，不要静默地向下取整
- 当 `groups > 1` 时，验证 `C_in % groups == 0` 且 `C_out % groups == 0`；否则报错
- 对于深度可分离卷积（`groups == C_in`），在 `layer` 列中标注，让读者看到为什么参数量低
- 如果用户提供 BatchNorm 或激活层，忽略它们对形状的影响，但保留参数量（每个 BatchNorm 为 `2 * C`）
- 绝不猜测缺失字段的默认值。每个卷积和池化都必须提供 `k`、`s`、`p`