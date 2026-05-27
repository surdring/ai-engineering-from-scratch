---
name: skill-noise-schedule-designer
description: 给定 T 和目标损坏水平，生成线性、余弦或 sigmoid 的 beta 调度表，以及 SNR 曲线图
version: 1.0.0
phase: 4
lesson: 10
tags: [计算机视觉, 扩散, 噪声调度, 训练]
---

# 噪声调度设计器

beta 调度表控制每个扩散步骤保留多少信号。糟糕的调度表会限制训练效率和所有下游决策的样本质量。

## 使用场景

- 开始新的扩散训练并选择 T 和 beta
- 调试产生模糊样本（调度表过于激进）或无法学习结构（调度表过于温和）的扩散模型
- 比较不同论文中报告的调度表设计

## 输入

- `T`：时间步数，通常为 100-1000
- `type`：linear | cosine | sigmoid
- `target_alpha_bar_final`：在 t=T 时保留的信号比例，默认 0.001（99.9% 损坏）
- 可选 `image_resolution`——更大的图像受益于更慢的损坏调度表（余弦或偏移调度表）

## 调度公式

### 线性（Linear）
```
beta_t = beta_start + (beta_end - beta_start) * (t - 1) / (T - 1)
```
默认值：beta_start=1e-4, beta_end=0.02（DDPM 论文）。

### 余弦（Cosine，Nichol & Dhariwal, 2021）
```
alpha_bar_t = cos^2((t/T + s) / (1 + s) * pi/2)
beta_t = 1 - alpha_bar_t / alpha_bar_{t-1}
```
s = 0.008。更长时间保留信号；在低步数下表现更佳。

### Sigmoid
```
alpha_bar_t = 1 / (1 + exp(k * (t/T - 0.5)))
```
k = 6 到 12。良好的折中方案；一些 SDXL 变体使用。

## 步骤

1. 根据公式计算 betas
2. 预计算 `alphas`、`alphas_cumprod`、`sqrt_alphas_cumprod`、`sqrt_one_minus_alphas_cumprod`
3. 计算 SNR_t = alpha_bar_t / (1 - alpha_bar_t)；生成 SNR 随时间变化的摘要
4. 验证 `alphas_cumprod[T-1]` 是否在 `target_alpha_bar_final` 的 10% 以内；否则调整 beta_end（线性）、s（余弦）或 k（sigmoid）并重试
5. 报告三个检查点：
   - `t=T*0.25`——早期损坏
   - `t=T*0.5`——中途
   - `t=T*0.75`——接近最终

## 报告

```
[调度表]
  类型:    <名称>
  T:       <整数>
  beta_start: <浮点数>   beta_end: <浮点数>

[信号保留]
  t=0.25T:  alpha_bar=<X>  SNR=<X>
  t=0.5T:   alpha_bar=<X>  SNR=<X>
  t=0.75T:  alpha_bar=<X>  SNR=<X>
  t=T:      alpha_bar=<X>  SNR=<X>

[警告]
  - <如果 alpha_bar 在 0.75T 之前崩溃>
  - <如果 beta_end 在对数 SNR 中产生 NaN>
```

## 规则

- 绝不生成任何 `alpha_bar_t <= 0` 的调度表；将低于 1e-5 的值钳制并警告
- 余弦是低步数采样（< 30 步）的默认推荐
- 线性是 `quality_target == research` 的默认推荐——DDPM 基线使用线性调度表报告
- 当 `image_resolution > 256` 时，建议使用偏移调度表（Chen, 2023）以在高分辨率下保留更多信号