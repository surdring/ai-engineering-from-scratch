---
name: skill-residual-block-reviewer
description: 审查 PyTorch 残差块的跳跃连接正确性、BN 放置、激活顺序和形状对齐
version: 1.0.0
phase: 4
lesson: 3
tags: [计算机视觉, resnet, 代码审查, pytorch]
---

# 残差块审查器

一个专注于 PyTorch `nn.Module` 中实现残差块的审查器。捕获四种几乎涵盖所有残差网络（ResNet）重写错误的错误。

## 使用场景

- 有人写了自定义 BasicBlock 或 Bottleneck，但损失为 NaN 或准确率卡住
- 你正在将一个框架的块移植到另一个框架，想要验证等价性
- 你在审查一个修改 ResNet 内部实现的 PR（预激活、压缩-激励 SE、抗混叠）
- 模型在 CIFAR 大小的输入上运行正常，但在 ImageNet 分辨率上崩溃，因为捷径路径（Shortcut）有误

## 输入

- 一个 PyTorch 类定义，可以是源文本或可导入路径
- 可选 `variant`：`basic` | `bottleneck` | `preact` | `seblock`

## 四项检查

### 1. 捷径形状对齐

对于任何 `stride != 1` 或 `in_channels != out_channels` 的块，捷径路径**必须**是一个形状匹配的模块——通常是 1x1 卷积加 BN。这种情况下裸 `nn.Identity()` 是保证会在前向传播时出现的形状不匹配错误。

诊断：
```
[shortcut]
  detected:  nn.Identity | 1x1 Conv + BN | 1x1 Conv + BN + ReLU | other
  required:  shape-matching Conv if (stride != 1 or in_c != out_c) else Identity
  verdict:   ok | wrong | unnecessarily heavy
```

### 2. BN 相对于加法操作的位置

加法 `out + shortcut(x)` 必须发生在最终 ReLU 之**前**（后激活，原始 ResNet），或者最终 ReLU 必须完全不存在（预激活 ResNet v2）。一个块在主分支上应用 ReLU 然后加上原始捷径路径会产生不对称的激活范围，损害训练。

诊断：
```
[activation order]
  pattern:  post-act (conv-BN-ReLU-conv-BN-add-ReLU) | pre-act (BN-ReLU-conv-BN-ReLU-conv-add) | other
  verdict:  ok | suspect
```

### 3. 卷积层的偏置

紧跟 BatchNorm 的卷积应该设置 `bias=False`。BN 的 beta 已经参数化了偏置，所以额外的卷积偏置浪费参数并可能减慢收敛。

诊断：
```
[bias]
  convs with BN and bias=True: <count>
  recommended fix: set bias=False on those layers
```

### 4. 原地 ReLU 与 autograd

对将被加到捷径路径的张量使用 `nn.ReLU(inplace=True)` 会覆盖残差加法可能仍需的值。标记任何位于不是产生新张量的层之后的原地操作。

诊断：
```
[in-place]
  risky inplace ops: <list>
  fix: inplace=False before the residual add
```

## 报告

```
[block-review]
  variant:       basic | bottleneck | preact | se | other
  shortcut:      ok | wrong | heavy
  activation:    ok | suspect
  bias-bn:       ok | <N> convs need bias=False
  in-place:      ok | <N> risky ops
  summary:       one sentence
```

## 规则

- 不要重写块。仅报告
- 如果块是正确的，全部输出 `ok` 并停止。没有建议
- 如果有多处错误，按以上顺序列出（捷径路径优先，因为它是崩溃的最常见原因）
- 当用户明确指定为故意的预激活或压缩-激励变体时，绝不将其错误标记