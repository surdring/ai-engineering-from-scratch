---
name: skill-dcgan-scaffold
description: 根据 z_dim、image_size 和 num_channels 编写完整的 DCGAN 脚手架代码，包括训练循环和样本保存器
version: 1.0.0
phase: 4
lesson: 9
tags: [计算机视觉, gan, dcgan, 脚手架]
---

# DCGAN 脚手架

给定三个参数，生成一个可运行的 DCGAN 项目骨架，其架构尺寸与目标图像分辨率匹配。

## 使用场景

- 在小数据集上启动新的生成实验
- 用可工作的最小示例讲授 DCGAN 基础
- 在同一脚手架上做条件 GAN 的原型开发（标签注入）

## 输入

- `image_size`：32、64 或 128 之一（必须是 2 的幂）
- `num_channels`：1（灰度）或 3（RGB）
- `z_dim`：通常为 64 或 128
- `with_spectral_norm`：是 | 否；默认是

## 架构尺寸

G 中转置卷积块和 D 中步幅卷积块的数量取决于 `image_size`：

| image_size | G 块数 | D 块数 |
|------------|--------|--------|
| 32         | 4      | 4      |
| 64         | 5      | 5      |
| 128        | 6      | 6      |

每增加一个块，G 中空间维度翻倍（D 中减半）。特征数从 32 开始，以 `feat_base * 2^block_index` 方式缩放。

## 输出文件

- `model.py`——生成器 + 判别器类
- `train.py`——训练循环、损失、优化器设置
- `sample.py`——样本网格保存器
- `config.json`——超参数
- `README.md`——10 行快速入门指南

## 报告

```
[脚手架]
  image_size:       <整数>
  num_channels:     <整数>
  z_dim:            <整数>
  spectral_norm:    是 | 否

[架构]
  G 块数:           <N>, 通道数: [列表]
  D 块数:           <N>, 通道数: [列表]
  G 参数（估计）:   <N>
  D 参数（估计）:   <N>

[训练默认值]
  优化器:     Adam(lr=2e-4, betas=(0.5, 0.999))
  批次大小:   64
  epochs:     50
  采样间隔:   每 1 个 epoch

[已写入文件]
  - model.py
  - train.py
  - sample.py
  - config.json
  - README.md
```

## 规则

- 始终在 G 的输出上使用 `nn.Tanh()`，并在训练期间将数据缩放到 [-1, 1]
- 始终在 D 中使用 `LeakyReLU(0.2)`
- 当 `with_spectral_norm == 是` 时，对 D 中的每个卷积层应用 `spectral_norm()`，并从 D 中移除 BatchNorm。在 G 中保留 BatchNorm
- 绝不为 image_size > 128 生成脚手架——DCGAN 在此之上变得不稳定；请引导用户使用 StyleGAN 或扩散模型（Diffusion Model）