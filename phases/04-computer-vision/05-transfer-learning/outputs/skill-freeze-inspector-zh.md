---
name: skill-freeze-inspector
description: 报告哪些参数可训练、哪些 BatchNorm 层处于评估模式，以及优化器是否实际包含了可训练参数
version: 1.0.0
phase: 4
lesson: 5
tags: [计算机视觉, 迁移学习, 调试, pytorch]
---

# 冻结检查器

迁移学习的 bug 隐藏在三处：应该冻结但未冻结的参数、应该可训练但不可训练的参数，以及在冻结状态变更之前构建的优化器。本技能一次性暴露所有三处问题。

## 使用场景

- 在设置参数子集的 `requires_grad` 之后立即使用
- 在微调运行的第一次训练步骤之前
- 在调用 `freeze_bn_stats` 或任何翻转 BN 模式的辅助函数之后
- 当验证准确率卡在随机水平，你怀疑实际上没有任何参数在训练时

## 输入

- `model`：一个 PyTorch `nn.Module`
- `optimizer`：即将用于训练的优化器
- 可选 `expected_frozen_prefixes`：应该被冻结的参数名称前缀列表（如 `["conv1", "bn1", "layer1"]`）

## 步骤

1. **遍历参数。**对每个 `(name, param)`：
   - 记录 `requires_grad`
   - 记录 `shape` 和 `numel`

2. **遍历模块。**对每个模块：
   - 如果是 BatchNorm，记录其是否处于评估模式，以及其仿射参数是否可训练

3. **检查优化器。**对每个参数组：
   - 将其 `params` 展平为 `id(p)` 的集合
   - 与所有 `requires_grad == True` 的参数的 `id(p)` 集合进行比较

4. **检测四种失败模式：**
   - `leaked_train`：参数 `requires_grad=True` 但未出现在优化器中（梯度被计算但从未被应用）
   - `ghost_train`：参数出现在优化器中但 `requires_grad=False`（优化器状态被浪费；如果之后重新启用 requires_grad 也可能导致 bug）
   - `bn_mismatch`：以下任一情况：(a) BN 层处于训练模式（累积运行统计量）而仿射参数（`weight`、`bias`）被冻结，或 (b) BN 层处于评估模式（冻结统计量）而仿射参数可训练。两种状态都不一致，几乎总是 bug
   - `expected_vs_actual`：`expected_frozen_prefixes` 中列出的任何前缀仍有可训练的参数

## 报告

```
[freeze-inspector]
  模型可训练参数: <N>
  模型冻结参数:   <N>
  处于 eval 模式的 batchnorm 层: <count>
  处于 train 模式的 batchnorm 层: <count>

[优化器覆盖]
  已送入优化器的可训练参数: <M> / <N>
  leaked_train: <参数名称列表>（可训练但不在优化器中）
  ghost_train:  <参数名称列表>（在优化器中但已冻结）

[BN 审计]
  不匹配的层: <名称列表>

[期望检查]
  expected_frozen_prefixes: <...>
  不符合的参数:            <列表>

[结论]
  ok | <一行关于最严重问题的摘要>
```

## 规则

- 仅报告参数名称；绝不打印权重本身
- 每个列表按参数名称字母顺序排序
- 如果优化器覆盖为 100% 且无不匹配，返回 `ok` 并停止
- 对于 `leaked_train`，始终建议在冻结状态变更后重建优化器
- 对于 `ghost_train`，建议移除参数组，或者如果本意是要训练该参数则设置 `requires_grad=True`