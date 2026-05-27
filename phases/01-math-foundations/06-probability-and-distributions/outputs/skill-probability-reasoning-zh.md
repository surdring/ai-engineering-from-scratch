---
name: skill-probability-reasoning
description: 为给定的机器学习问题选择合适的概率分布
version: 1.0.0
phase: 1
lesson: 6
tags: [概率, 分布, 建模]
---

# 概率分布选择

如何在建模数据、设计损失函数或设置先验时选择正确的分布。

## 决策清单

1. 结果是离散的（类别、计数）还是连续的（测量值、分数）？
2. 结果是有界的（如 [0, 1]）还是无界的？
3. 可能的结果有多少种？两种？k 种？无限种？
4. 数据是对称的还是偏斜的？
5. 事件是独立的还是相关的？
6. 你是在建模比率、计数、比例还是测量值？

## 分布决策树

```
变量是离散的吗？
  是 --> 只有 2 种结果？ --> 伯努利分布 Bernoulli(p)
   |    k 种结果，一次试验？ --> 类别分布 Categorical(p1...pk)
   |    k 种结果，n 次试验？ --> 多项分布 Multinomial(n, p1...pk)
   |    n 次试验中成功次数？ --> 二项分布 Binomial(n, p)
   |    每区间事件计数？ --> 泊松分布 Poisson(lambda)
   |    首次成功前的试验次数？ --> 几何分布 Geometric(p)
   |    r 次成功前的试验次数？ --> 负二项分布 Negative Binomial(r, p)
  否 --> 对称、钟形？ --> 正态分布 Normal(mu, sigma)
      |   正值，右偏？ --> 对数正态分布或指数分布
      |   有界 [0, 1]？ --> Beta 分布 Beta(alpha, beta)
      |   正值，灵活形状？ --> Gamma 分布 Gamma(alpha, beta)
      |   事件间隔时间？ --> 指数分布 Exponential(lambda)
      |   需要厚尾？ --> Student's t 分布或柯西分布
      |   多元、钟形？ --> 多元正态分布
      |   在单纯形上（和为 1）？ --> Dirichlet 分布 Dirichlet(alpha)
```

## 真实 ML 场景到分布的映射

| 场景 | 分布 | 参数 |
|---|---|---|
| 二分类输出 | Bernoulli | p = sigmoid(logit) |
| 多分类输出 | Categorical | p = softmax(logits) |
| 语言模型中的 Token 预测 | 词汇表上的 Categorical | p 来自 softmax |
| 像素强度（归一化） | Beta 或 [0, 1] 上的 Uniform | 取决于图像统计 |
| 文档中的词数 | Poisson | lambda = 平均词数 |
| 用户请求间隔时间 | Exponential | lambda = 请求速率 |
| 测量误差 | Normal | mu = 0, sigma 来自数据 |
| 权重初始化 | Normal 或 Uniform | Kaiming/Xavier 规则 |
| VAE 潜变量空间先验 | Standard Normal | mu = 0, sigma = 1 |
| 比例的贝叶斯先验 | Beta | alpha, beta 来自信念 |
| 类别权重的贝叶斯先验 | Dirichlet | alpha 向量 |
| 回归目标的噪声 | Normal | mu = 0, sigma 估计 |
| 对异常值鲁棒的回归 | Student's t | 低自由度 |
| 持续时间/寿命建模 | Weibull 或 Gamma | 形状和尺度 |
| LDA 中每文档的主题分布 | Dirichlet | alpha < 1 用于稀疏 |

## 分布用错时

- 数据有硬下限时使用正态分布（如价格、距离）。正态分布会给负值分配非零概率。应使用对数正态或 Gamma 分布。
- 方差与均值不同时使用泊松分布。泊松假设均值 = 方差。如果方差 > 均值，使用负二项分布。
- 对多分类问题使用伯努利分布。伯努利严格只用于二分类。k > 2 时使用类别分布。
- 观察值相关时假设独立。时间序列、空间数据和分组数据违反独立性。使用自回归或分层模型。

## 常见错误

- 混淆 PDF 值与概率。PDF 可以超过 1。概率来自对 PDF 在区间上的积分。
- 忘记 softmax 输出是类别概率，而非独立的伯努利概率。它们构造上总和为 1。
- 在有领域知识时使用均匀先验。信息性先验如果选择得当，可以减少方差而不偏倚结果。
- 将对数概率当作概率。对数概率始终为负（或零）。它们不总和为 1。

## 快速参考：分布属性

| 分布 | 支撑集 | 均值 | 方差 | 关键属性 |
|---|---|---|---|---|
| Bernoulli(p) | {0, 1} | p | p(1-p) | 最简单的离散分布 |
| Binomial(n, p) | {0..n} | np | np(1-p) | n 个 Bernoulli 之和 |
| Poisson(lam) | {0, 1, 2, ...} | lam | lam | 均值 = 方差 |
| Normal(mu, s^2) | (-inf, inf) | mu | s^2 | 给定均值/方差下最大熵 |
| Exponential(lam) | [0, inf) | 1/lam | 1/lam^2 | 无记忆性 |
| Beta(a, b) | [0, 1] | a/(a+b) | ab/((a+b)^2(a+b+1)) | Binomial 的共轭 |
| Gamma(a, b) | (0, inf) | a/b | a/b^2 | Poisson 的共轭 |
| Dirichlet(alpha) | 单纯形 | alpha_i/sum | （见公式） | Categorical 的共轭 |