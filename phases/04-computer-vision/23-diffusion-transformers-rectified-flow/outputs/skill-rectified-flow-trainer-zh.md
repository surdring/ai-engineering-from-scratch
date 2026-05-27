---
name: skill-rectified-flow-trainer
description: 编写完整的修正流（Rectified Flow）训练循环，包含 AdaLN DiT 和 Euler 采样
version: 1.0.0
phase: 4
lesson: 23
tags: [diffusion, rectified-flow, DiT, training]
---

# 修正流训练器

编写一个干净、最小化的训练循环，可以在任何图像张量数据集上成功训练一个带修正流的小型 DiT。

## 使用场景

- 在小规模上复现 SD3 / FLUX 训练目标。
- 在相同数据上对比修正流与 DDPM 的效果。
- 为非标准领域（医疗、卫星）构建自定义修正流模型。

## 输入

- `model`: 一个 `nn.Module`，接受 `(x, t)` 并返回预测速度。
- `dataset`: 模型域中干净图像的可迭代对象。
- `optimizer`: AdamW，参数为 `lr=1e-4`、`weight_decay=0.01`、`betas=(0.9, 0.99)`。
- `scheduler`: 带预热的余弦调度，默认 1000 预热步。

## 训练步骤

```python
def rectified_flow_train_step(model, x0, optimizer, device):
    model.train()
    x0 = x0.to(device)
    n = x0.size(0)
    t = torch.rand(n, device=device)                     # [0, 1] 上的均匀分布
    epsilon = torch.randn_like(x0)
    x_t = (1 - t[:, None, None, None]) * x0 + t[:, None, None, None] * epsilon
    target_v = epsilon - x0                              # 速度目标
    pred_v = model(x_t, t)
    loss = F.mse_loss(pred_v, target_v)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss.item()
```

## 采样（Euler 方法）

```python
@torch.no_grad()
def sample(model, shape, steps=20, device="cpu"):
    model.eval()
    x = torch.randn(shape, device=device)
    dt = 1.0 / steps
    t = torch.ones(shape[0], device=device)
    for _ in range(steps):
        v = model(x, t)
        x = x - dt * v
        t = t - dt
    return x
```

## 技巧

- 使用 `torch.rand` 均匀 `t`；对 `t` 进行 logit-normal 或 SD3 风格的加权采样略有帮助，但不是入门的必要条件。
- 模型权重的指数滑动平均（EMA）是常规做法；使用衰减系数 0.9999 维护 `ema_model`。
- 条件模型的分类器自由引导（CFG）：训练时以 10% 的概率将条件替换为空/空嵌入；推理时混合 `v_uncond + w * (v_cond - v_uncond)`，`w` 通常在 3-5 左右。
- 对于 LDM 风格训练（FLUX、SD3），整个循环在 VAE 潜在空间中运行；上述的干净 `x0` 实际上是 `VAE.encode(image)`。
- 在 32x32 玩具数据集上的典型收敛：2000-5000 步。在真实潜在 SD3 训练上：数十万步。

## 报告

```
[rectified flow training]
  steps:        <整数>
  final loss:   <浮点数>
  ema decay:    <浮点数>
  vae?:         yes | no
  cfg dropout:  <比例>

[sampling]
  default steps: 20
  schnell / turbo target: 4
  full quality reference: 50+（仅用于对比参考）
```

## 规则

- 绝不要在 RGB `uint8` 数据上以图像空间速度目标训练修正流；先归一化到零均值、单位方差。
- 始终按时间步桶记录训练损失；如果早期时间步（接近 0）的损失高于晚期时间步（接近 1），速度参数化可能连接有误。
- 不要在同一训练循环中混合使用修正流速度目标和 DDPM 噪声目标；选择其中一个。
- 在 Ampere+ GPU 上使用 bfloat16 训练；float16 在修正流中有时会因为速度幅值产生 NaN 梯度。