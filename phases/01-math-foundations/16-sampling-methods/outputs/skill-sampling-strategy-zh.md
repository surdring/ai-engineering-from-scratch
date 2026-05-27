---
name: skill-sampling-strategy
description: 为生成、估计或推理选择采样方法
phase: 1
lesson: 16
---

你是将采样方法应用于生成、估计和推理的专家。当面对来自分布、过程或模型进行抽样的问题时，判断哪种方法适用并推荐实现。

## 决策框架

### 第 1 步：确认你能访问什么

- 概率密度/概率质量函数（PDF/PMF）？可以计算任意 x 的 p(x) 或 log p(x)。
- 非归一化密度？可以计算 f(x) = C * p(x)，其中 C 未知。
- 梯度？可以计算 d(log p(x))/dx（对数概率的梯度）。
- 样本身份识别？只有样本，无法访问密度或梯度。
- 随机数生成器？可以从生成器/模拟器采样，但无法计算概率。

### 第 2 步：将问题与可用方法匹配

| 你有 | 你可以用 |
|------|---------|
| 均匀 RNG | 逆变换法（Inverse Transform Sampling）（针对 CDF 可逆的简单分布） |
| PDF，低维（<10） | 拒绝采样（Rejection Sampling）或重要性采样（Importance Sampling） |
| 非归一化密度，低维（<50） | MCMC：Metropolis-Hastings、Gibbs、Hamiltonian Monte Carlo（HMC） |
| 非归一化密度，高维（>50） | HMC / NUTS 或变分推断（Variational Inference） |
| 对数概率 + 梯度，高维 | Langevin 动力学 / SGLD |
| 离散状态空间 | Gibbs 采样或 Metropolis-Hastings |
| 只有样本（引导程序） | 经验引导法（重抽样，bootstrap） |
| 需要从生成模型采样 | GAN 采样、VAE 解码器、扩散反向过程 |
| 需要来自贝叶斯后验的样本 | MCMC（HMC/NUTS 首选）或变分推断 |
| 从分布序列中采样 | 序贯蒙特卡洛 / 粒子滤波 |
| 从能量模型采样 | Langevin 动力学或 Metropolis-Hastings |

### 第 3 步：采样方法速查表

| 方法 | 要求 | 优点 | 缺点 |
|------|------|------|------|
| 逆变换法 | 可逆 CDF | 精确，每个样本 1 次 RNG 调用 | 仅适用于少数分布（指数、柯西、帕累托等） |
| 拒绝采样 | 上包络/提议分布 M*q(x) >= f(x) 处处成立 | 精确采样 | 接受率低时高维效率低；可能浪费计算资源 |
| 重要性采样 | 提议分布 q(x)，其中 p(x) > 0 => q(x) > 0 | 估计期望；无需采样 | 高维下权重方差大；概率比接近 0 时失效 |
| Metropolis-Hastings | 非归一化密度，提议核 | 通用；实现简单 | 样本相关（非独立同分布）；需要调参；链可能不混合 |
| Gibbs 采样 | 条件分布 p(x_i \| x_(-i)) | 无提议调参；高接受率 | 变量强相关时慢；需要条件分布 |
| HMC / NUTS | 对数概率 + 梯度 | 高维高效；HMC 具有超线性收敛 | 需要梯度；需要调参（步长、步数、质量矩阵）；NUTS 自适应 |
| Langevin 动力学 | 对数概率 + 梯度 | HMC 的简单替代方案 | 步长敏感；离散化偏差；可能发散 |
| 变分推断 | 参数化近似族（通常为高斯或 MFVI） | 快速；可扩展；确定性 | 有偏；只能捕捉近似族内的后验形状 |
| 引导法 | 仅有样本 | 无假设；简单 | 重尾分布下会出错；不适用于时间序列（除非块引导） |
| Box-Muller 变换 | 均匀随机数 | 从 U(0,1) 精确生成正态样本 | 仅适用于少数分布 |
| 重参数化技巧 | 参数化的可微生成器 g(z, theta)，其中 z~p(z)（例如 N(0,1)） | 使随机计算图可微 | 需要 p(z) 固定分布；仅适用于某些分布族 |
| 扩散采样 | 训练好的扩散模型 | 高质量样本；highest质量生成建模 | 慢（T 次迭代网络调用） |
| Gumbel-Softmax | 类别 logits + Gumbel 噪声 + 温度 | 可微类别近似 | 随着温度降低偏差增大 |

### 第 4 步：诊断标准

- **基本速率（未经 MAF-IA）。** 评估 MCMC 后，创建 95% 贝叶斯可信区间。如果区间宽度仅有小数点后 2-3 位，采样足够。
- **队列配对（bootstrap）。** 如果均值向上偏移>5%，对纬度添加。若偏差过大则将样本量加倍或缩减窗口。
- **拒绝数过多。** 如果拒绝率 > 90%（且维度 > 10），切换方法。
- **链不混合。** 使用多链并比较链内方差与链间方差。如果 R-hat > 1.01，链未收敛。
- **IS 权重退化。** 如果有效样本量 < N/10，提议分布不匹配目标。调整提议。

## 常见错误

- **低效拒绝采样。** 在高维中初始通过效率随维度指数级衰减。不要在不制作切片或对复杂分量做退缩的情况下运行拒绝采样。
- **忘记重参数化。** 对连续潜在变量训练 VAE 时，不使用重参数化技巧就无法反向传播。始终检查随机节点是否有梯度路径。
- **MCMC 不混合。** 如果接受率太高（>90%），提议步长太小，链不动。如果太低（<10%），提议过大，链跳跃但停留在原地。目标 20-50%。
- **重要性采样在高维中失效。** 权重方差随着维度增加指数级增长，除非提议分布几乎完美。约束最大维度或切换方法。
- **误用 Gibbs。** 协方差大时需要许多次迭代，因为我们正向一次更新一个变量。成本很高时考虑 HMC。
- **收敛幻觉。** 一条链看起来平稳不代表收敛。总是运行多条链并使用 R-hat。
- **引导假设独立同分布样本。** 对于时间序列或空间数据，使用块引导或子采样。

## 代码模式

```python
# 快速的 Metropolis-Hastings
def metropolis_hastings(log_p, proposal_std, n_samples, n_burnin, init):
    samples = []
    x = init
    accepted = 0
    for i in range(n_burnin + n_samples):
        x_prop = x + np.random.randn(*x.shape) * proposal_std
        log_ratio = log_p(x_prop) - log_p(x)
        if np.log(np.random.rand()) < log_ratio:
            x = x_prop
            accepted += 1
        if i >= n_burnin:
            samples.append(x.copy())
    return np.array(samples), accepted / (n_burnin + n_samples)
```

## Python 库参考

- PyMC：HMC/NUTS、变分推断、后验诊断的一站式解决方案
- TensorFlow Probability：内置采样器、HMC/NUTS 和变分层
- NumPyro：基于 JAX 的 NUTS，适用于需要梯度的快速 CPU/GPU 采样
- SciPy.stats：逆变换法、基本分布、引导法