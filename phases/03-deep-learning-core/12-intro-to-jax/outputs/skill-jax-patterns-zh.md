---
name: skill-jax-patterns
description: JAX 的函数式编程模式——何时以及如何使用 grad、jit、vmap 和 pmap
version: 1.0.0
phase: 3
lesson: 12
tags: [jax, 函数式编程, 自动微分, 编译, 向量化]
---

# JAX 函数式编程模式

JAX 变换纯函数。以下每个模式都遵循一条规则：编写一个接收输入并返回输出的函数，没有任何副作用。然后变换它。

## 四大变换

### grad —— 对函数求导

```python
grads = jax.grad(loss_fn)(params, x, y)
loss, grads = jax.value_and_grad(loss_fn)(params, x, y)
```

使用场景：需要梯度进行优化时。
约束：函数必须返回标量。对于非标量输出，使用 `jax.jacobian`。

### jit —— 编译函数

```python
fast_fn = jax.jit(f)
```

使用场景：当函数将被多次调用且输入形状相同时。
约束：没有依赖被追踪值的 Python 控制流。使用 `jax.lax.cond` 做条件判断，`jax.lax.scan` 做循环。

### vmap —— 向量化函数

```python
batch_fn = jax.vmap(f, in_axes=(None, 0))
```

使用场景：你为一个样本写了函数，现在需要它处理批次数据。
`in_axes` 指定每个参数沿哪个轴批处理。`None` 表示不批处理（广播）。

### pmap —— 跨设备并行化

```python
parallel_fn = jax.pmap(f, axis_name='devices')
```

使用场景：你有多个 GPU/TPU 并希望数据并行。
在函数内部，`jax.lax.pmean(x, 'devices')` 跨设备求平均。

## 组合规则

变换可以组合。顺序很重要：

```python
per_example_grads = jax.jit(jax.vmap(jax.grad(loss_fn), in_axes=(None, 0, 0)))
```

从右往左读：对 loss_fn 求梯度，对样本向量化，编译结果。

有效的组合：
- `jit(grad(f))` -- 编译的梯度计算
- `jit(vmap(f))` -- 编译的批处理计算
- `vmap(grad(f))` -- 逐样本梯度
- `pmap(jit(f))` -- 并行编译计算
- `grad(jit(f))` -- 编译函数的梯度（与 jit(grad(f)) 相同）

## 参数管理模式

JAX 参数是 pytree（嵌套的数组字典）：

```python
params = {
    'layer1': {'w': jnp.zeros((784, 256)), 'b': jnp.zeros(256)},
    'layer2': {'w': jnp.zeros((256, 10)),  'b': jnp.zeros(10)},
}
```

一次性更新所有参数：
```python
params = jax.tree.map(lambda p, g: p - lr * g, params, grads)
```

统计参数量：
```python
n_params = sum(p.size for p in jax.tree.leaves(params))
```

## PRNG Key 管理

JAX 需要显式的随机 key：

```python
key = jax.random.PRNGKey(0)
key, subkey = jax.random.split(key)
noise = jax.random.normal(subkey, shape)
```

多次随机操作时，一次性拆分：
```python
keys = jax.random.split(key, n)
```

绝不重复使用 key。使用前始终先拆分。

## 常见错误

1. **在 jit 内修改数组**：JAX 数组是不可变的。使用 `x.at[i].set(v)` 而非 `x[i] = v`。

2. **在 jit 内使用 Python print**：`print` 在追踪（Tracing）期间而非执行期间运行。使用 `jax.debug.print("{}", x)`。

3. **在 jit 内对被追踪的值使用 Python if/for**：使用 `jax.lax.cond`、`jax.lax.switch`、`jax.lax.scan`、`jax.lax.fori_loop`。

4. **忘记 `.block_until_ready()`**：JAX 使用异步调度。做基准测试时，调用 `.block_until_ready()` 等待实际完成。

5. **重复使用 PRNG key**：两个操作使用相同的 key 会产生相同的「随机」值。始终拆分。

6. **在 jit 编译的函数中使用全局状态**：全局变量在追踪时被捕获。追踪之后的更改不可见。将所有内容作为参数传递。

## 决策清单

1. 函数是否被调用一次以上？添加 `@jax.jit`。
2. 是否需要梯度？用 `jax.grad` 或 `jax.value_and_grad` 包裹。
3. 是否处理一个样本但你有一个批次？用 `jax.vmap` 包裹。
4. 是否有多个设备？用 `jax.pmap` 包裹。
5. 是否使用随机性？显式地线程传递 PRNG key。
6. 是否有基于数组值的 Python 控制流？用 `jax.lax` 原语替换。

## 何时使用 JAX

使用 JAX 的场景：
- 需要逐样本梯度（差分隐私、Fisher 信息）
- 在 TPU 上训练（JAX 是 TPU 的原生框架）
- 需要高阶导数（Hessian 矩阵、Jacobian 矩阵）
- 想要将整个训练步骤编译为单个内核
- 你的团队在 Google DeepMind 或 Anthropic

使用 PyTorch 的场景：
- 想要最大的生态系统（HuggingFace、torchvision、Lightning）
- 调试便利性优先于原始速度
- 使用 NVIDIA GPU 部署，配合 TorchServe/Triton
- 招聘（PyTorch 开发者更多）
- 想在新架构上快速迭代