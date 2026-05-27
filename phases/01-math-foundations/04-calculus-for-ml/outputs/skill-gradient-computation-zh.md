---
name: skill-gradient-computation
description: 计算常见机器学习损失函数的梯度，并选择正确的求导方式
version: 1.0.0
phase: 1
lesson: 4
tags: [微积分, 梯度, 反向传播]
---

# 机器学习中的梯度计算

计算神经网络中使用的损失函数、激活函数和层操作的梯度的实用参考。

## 决策清单

1. 函数是否由简单的基本运算（幂、exp、log、三角函数）组合而成？使用解析导数配合链式法则。
2. 函数是否为自定义或黑盒操作？使用数值微分：`(f(x+h) - f(x-h)) / (2h)`，其中 h = 1e-7。
3. 函数是否由 PyTorch/JAX 中的张量操作构建而成？交给自动微分处理。用数值检查验证。
4. 是否需要标量损失关于权重矩阵的梯度？通过计算图逐节点应用链式法则。
5. 是否存在不可微操作（argmax、rounding、sampling）？使用直通估计器（Straight-Through Estimator）或重参数化技巧（Reparameterization Trick）。

## 各方法适用场景

| 方法 | 适用场景 | 代价 |
|---|---|---|
| 解析法（手推） | 简单函数，验证自动微分输出 | 运行时零成本 |
| 数值法（有限差分） | 调试、梯度检查、黑盒函数 | n 个参数需要 2n 次前向传播 |
| 自动微分（Autograd） | 任何可微计算图（默认选择） | 一次反向传播 |
| 符号法（SymPy、Mathematica） | 为论文推导闭式梯度 | 仅编译时 |

## 快速参考：常见导数

| 函数 | f(x) | f'(x) | ML 上下文 |
|---|---|---|---|
| MSE 损失 | (1/n) sum(y_hat - y)^2 | (2/n)(y_hat - y) | 回归 |
| 交叉熵（二分类） | -(y log(p) + (1-y) log(1-p)) | p - y（sigmoid 之后） | 二分类 |
| 交叉熵（多分类） | -log(p_true_class) | p - one_hot(y)（softmax 之后） | 多分类 |
| Sigmoid | 1 / (1 + e^(-x)) | sigma(x) * (1 - sigma(x)) | 输出门控、二分类输出 |
| Tanh | (e^x - e^(-x)) / (e^x + e^(-x)) | 1 - tanh(x)^2 | 隐藏层激活（旧式） |
| ReLU | max(0, x) | x > 0 时为 1，x < 0 时为 0 | 默认隐藏层激活 |
| Leaky ReLU | max(0.01x, x) | x > 0 时为 1，x < 0 时为 0.01 | 避免死亡神经元 |
| GELU | x * Phi(x) | Phi(x) + x * phi(x) | Transformer |
| Softmax_i | e^(x_i) / sum(e^(x_j)) | i=j 时 s_i(1-s_i)，i!=j 时 -s_i*s_j | 输出层（Jacobian 矩阵） |
| Log-softmax | x_i - log(sum(e^(x_j))) | 第 i 项为 1 - softmax(x_i) | 数值稳定的交叉熵 |
| 线性层 | y = Wx + b | dL/dW = dL/dy * x^T, dL/db = dL/dy | 每一层 |
| L2 正则化 | lambda * sum(w^2) | 2 * lambda * w | 权重衰减 |
| L1 正则化 | lambda * sum(\|w\|) | lambda * sign(w) | 稀疏性 |

## 常见错误

- 忘记批次平均损失（MSE、交叉熵）中的 1/n 因子。梯度会按批次大小缩放。
- 将 softmax 梯度当作向量计算，实际上它是一个 Jacobian 矩阵。对于交叉熵 + softmax 的组合，梯度简化为 (p - y)，避免了完整的 Jacobian 计算。
- 以错误的顺序应用链式法则。从损失向后推导：dL/dW = dL/dy * dy/dW。
- 数值微分时 h 太大（h = 0.1）或太小（h = 1e-15）。float64 下使用 h = 1e-7。
- 忘记 ReLU 在 x = 0 处的梯度未定义。实践中设为 0 或 0.5。

## 梯度检查方法

```
对于每个参数 w:
  numeric_grad = (loss(w + h) - loss(w - h)) / (2h)
  auto_grad = 反向传播得到的值
  relative_error = |numeric - auto| / max(|numeric|, |auto|, 1e-8)
  assert relative_error < 1e-5
```

相对误差超过 1e-3 说明有问题。在 1e-5 到 1e-3 之间需要调查。