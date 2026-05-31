# 时间序列基础

> Past performance does predict future results -- if you check for stationarity first.

#phase-02-ml-fundamentals #ml #time-series #build-it #use-it #python #foundation

## 1. 核心理念

### 时间序列解决了什么问题？

- 你有按时间排序的数据：日销售额、每小时温度、每分钟 CPU 使用率、周股价
- 你想**预测下一个值**、下一天、下一周、下一季度
- 但标准 ML 的工具（随机分割、交叉验证、特征矩阵输入）在时间数据上全部失效

### 时间序列 vs 标准 ML 的根本差异

标准 ML 假设数据是 **i.i.d.**（独立同分布）：

| 假设 | 标准 ML | 时间序列的现实 |
|------|---------|--------------|
| **独立性** | 样本之间无关 | 今天的值**依赖**昨天的值 |
| **同分布** | 所有样本来自同一分布 | 12 月的销售分布和 3 月完全不同 |

**后果**：用随机 80/20 分割在时间序列上可能得到 95% 准确率（虚假），而向前走验证只给 55%（真实）。

## 2. 深入设计哲学

### 2.1 时间序列分解

```
Observed[t] = Trend[t] + Seasonality[t] + Residual[t]
```

| 成分 | 含义 | 例子 |
|------|------|------|
| **趋势** | 长期方向（上/下/平） | 营收年增长 10% |
| **季节** | 固定周期重复模式 | 12 月零售额飙升 |
| **残差** | 去除趋势和季节后的随机波动 | 某天突然多卖 5 台空调 |

### 2.2 平稳性（Stationarity）

**定义**：序列的统计性质（均值、方差、自相关结构）不随时间变化。

**为什么重要**：非平稳序列的均值在漂移。模型在 1 月学到均值，2 月数据已有不同均值 → 系统性错误。

**检查方法**：
1. **滚动统计**：计算滑动窗口内的均值/标准差，如果漂移则是非平稳
2. **ADF 检验**：零假设为「非平稳」，p < 0.05 则拒绝零假设

**修复方法 —— 差分**：

```
diff[t] = value[t] - value[t-1]
```

示例：原始 `[100, 102, 106, 112, 120]` → 一阶 `[2, 4, 6, 8]` → 二阶 `[2, 2, 2]`（平稳）

### 2.3 自相关（Autocorrelation）

- **ACF**：衡量 time=t 与 time=t-k 的相关性，k 为滞后阶数
- **ACF 告诉你**：序列的记忆长度（ACF 何时归零）、季节性（ACF 在 lag=12 有尖峰）、选多少个滞后特征
- **PACF**：剔除中间变量的间接影响，比 ACF 更「纯净」

### 2.4 滞后特征（Lag Features）—— 桥接时间序列与监督学习

将 1D 序列转为 (n - n_lags) × n_lags 特征矩阵：

```
[10, 12, 14, 13, 15]

lag_2  lag_1  target
  10     12     14
  12     14     13
  14     13     15
```

**特征类型**：

| 特征类型 | 示例 | 作用 |
|---------|------|------|
| 滞后值 | value[t-1], value[t-2] | 基础记忆 |
| 滚动统计 | 过去 7 天均值/标准差 | 近期趋势和波动 |
| 日历特征 | 星期几、是否节假日 | 周期性规律 |
| 差分值 | value[t-1] - value[t-2] | 变化方向 |
| 比值特征 | 当前值 / 滚动均值 | 偏离程度 |

**目标对齐陷阱**：target 必须是 time=t，特征必须只用 time≤t-1。如果误用 time=t 的值作为特征 → 完美预测器 → 完全无用的模型。

### 2.5 向前走验证（Walk-Forward Validation）

**时间序列唯一诚实的评估方法**：

```
Fold 1: Train [1月-3月] → Test [4月]
Fold 2: Train [1月-4月] → Test [5月]
Fold 3: Train [1月-5月] → Test [6月]
```

- **扩展窗口**：训练数据随 fold 增长（旧数据仍相关时用）
- **滑动窗口**：训练数据固定大小（世界变化快时用）

### 2.6 ARIMA 直觉

ARIMA(p, d, q) 的三个参数：

| 参数 | 含义 | 如何选 |
|------|------|--------|
| p | 用过去 p 个值预测 | PACF 截尾处 |
| d | 差分阶数使平稳 | 差分到 ADF 通过为止 |
| q | 用过去 q 个误差修正 | ACF 截尾处 |

## 3. 横向对比

### 3.1 方法选型对比

| 场景 | 推荐方法 |
|------|---------|
| 单变量短期预测 | ARIMA / 指数平滑 |
| 强季节性单变量 | SARIMA / Prophet |
| 有大量外部特征 | 滞后特征 + 梯度提升（**最强起点**） |
| 成百上千相关序列 | LightGBM + 序列 ID |
| 长序列复杂模式 | LSTM / Temporal Fusion Transformer |
| 快速基线 | 季节性朴素（预测值 = 去年同期） |

### 3.2 Build It vs Use It

| 你手写的 | sklearn/statsmodels 提供的 |
|---------|---------------------------|
| `walk_forward_split()` | `TimeSeriesSplit(n_splits)` |
| `make_lag_features()` | `pd.DataFrame.shift()` 或手动 |
| `SimpleAR.fit()` + `np.linalg.lstsq` | `Ridge(alpha=1.0).fit()` |
| `mse()` / `mae()` | `sklearn.metrics.mean_squared_error` / `mean_absolute_error` |
| (无) ARIMA 的 MA 部分 | `statsmodels.tsa.arima.model.ARIMA` |

**框架替我们做了三件事**：
1. **数值稳定性**：`Ridge` 用 SVD 分解 + L2 正则，比手动 `lstsq` 更鲁棒
2. **复杂参数估计**：ARIMA 的 MA 组件需要最大似然估计
3. **集成验证**：`TimeSeriesSplit` 与 `cross_val_score` 联动

## 4. Build It：从零实现

### 4.1 合成数据生成

```python
def make_synthetic_series(n=500, seed=42):
    rng = np.random.RandomState(seed)
    t = np.arange(n, dtype=float)
    trend = 0.05 * t
    seasonality = 10 * np.sin(2 * np.pi * t / 30)
    noise = rng.normal(0, 2, n)
    series = 50 + trend + seasonality + noise
    return series
```

体现 `时间序列 = 趋势 + 季节 + 噪声` 的分解公式。

### 4.2 滞后特征创建

```python
def make_lag_features(series, n_lags):
    n = len(series)
    X = np.full((n, n_lags), np.nan)
    for lag in range(1, n_lags + 1):
        X[lag:, lag - 1] = series[:-lag]
    valid_mask = ~np.isnan(X).any(axis=1)
    return X[valid_mask], series[valid_mask]
```

前 `n_lags` 行因历史不足被过滤。

### 4.3 SimpleAR 模型（自回归 = 线性回归 + 滞后特征）

```python
class SimpleAR:
    def __init__(self, n_lags=5):
        self.n_lags = n_lags
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        X_b = np.column_stack([np.ones(len(X)), X])
        theta = np.linalg.lstsq(X_b, y, rcond=None)[0]
        self.bias = theta[0]
        self.weights = theta[1:]
        return self

    def predict(self, X):
        return X @ self.weights + self.bias

    def fit_series(self, series):
        X, y = make_lag_features(series, self.n_lags)
        return self.fit(X, y)

    def forecast(self, last_values, n_steps):
        if len(last_values) < self.n_lags:
            raise ValueError(...)
        history = list(last_values[-self.n_lags:])
        predictions = []
        for _ in range(n_steps):
            features = np.array(history[-self.n_lags:]).reshape(1, -1)
            pred = self.predict(features)[0]
            predictions.append(pred)
            history.append(pred)
        return np.array(predictions)
```

**递归多步预测**：第 1 步用真实历史，之后用预测值替代 → 误差逐级累积。

### 4.4 向前走分割

```python
def walk_forward_split(n_samples, n_splits=5, min_train=50):
    if n_samples <= min_train:
        return
    step = max(1, (n_samples - min_train) // n_splits)
    for i in range(n_splits):
        train_end = min_train + i * step
        test_end = min(train_end + step, n_samples)
        if train_end >= n_samples:
            break
        yield slice(0, train_end), slice(train_end, test_end)
```

### 4.5 平稳性检查

```python
def check_stationarity(series, window=50):
    n = len(series)
    rolling_mean = np.zeros(n)
    rolling_std = np.zeros(n)
    for i in range(n):
        start = max(0, i - window + 1)
        segment = series[start:i + 1]
        rolling_mean[i] = segment.mean()
        rolling_std[i] = segment.std() if len(segment) > 1 else 0.0

    first_half_mean = series[:n // 2].mean()
    second_half_mean = series[n // 2:].mean()
    first_half_var = series[:n // 2].var()
    second_half_var = series[n // 2:].var()

    mean_shift = abs(first_half_mean - second_half_mean)
    var_ratio = max(first_half_var, second_half_var) / max(min(first_half_var, second_half_var), 1e-10)
    is_stationary = mean_shift < 0.5 * series.std() and var_ratio < 2.0
    return rolling_mean, rolling_std, is_stationary
```

### 4.6 自相关函数

```python
def autocorrelation(series, max_lag=20):
    n = len(series)
    mean = series.mean()
    var = series.var()
    acf = np.zeros(max_lag + 1)
    for k in range(max_lag + 1):
        if k >= n:
            break
        cov = np.mean((series[:n - k] - mean) * (series[k:] - mean)) if k < n else 0
        acf[k] = cov / var if var > 0 else 0.0
    return acf
```

### 4.7 评估指标

```python
def mse(y_true, y_pred): return np.mean((y_true - y_pred) ** 2)
def mae(y_true, y_pred): return np.mean(np.abs(y_true - y_pred))
def mape(y_true, y_pred):
    mask = y_true != 0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
```

### 4.8 Demo 函数链

```
demo_stationarity()              → 验证差分使非平稳变平稳
demo_autocorrelation()           → 验证周季节性（lag=7,14 有尖峰）
demo_lag_features()              → 展示 1D→2D 转换 + AR 权重
demo_walk_forward()              → 5 折向前走验证
demo_random_vs_walk_forward()    → 随机分割 vs 向前走（核心对比）
demo_lag_comparison()            → 不同滞后数的效果
demo_forecasting()               → 多步预测误差分析
```

## 5. Use It：框架实现

### 5.1 sklearn + 滞后特征

```python
from sklearn.linear_model import Ridge
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import TimeSeriesSplit

X, y = make_lag_features(series, n_lags=10)

# 单折
for train_idx, test_idx in TimeSeriesSplit(n_splits=5).split(X):
    model = Ridge(alpha=1.0)
    model.fit(X[train_idx], y[train_idx])
    predictions = model.predict(X[test_idx])

# 或者交叉验证
scores = cross_val_score(model, X, y, cv=TimeSeriesSplit(n_splits=5))
```

### 5.2 statsmodels ARIMA

```python
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(train_series, order=(5, 1, 2))
fitted = model.fit()
forecast = fitted.forecast(steps=30)
```

## 6. 注意事项与常见陷阱

### 时间序列六宗罪

| 陷阱 | 原因 | 修复 |
|------|------|------|
| 随机分割 | 习惯标准 ML | 永远用向前走 |
| 使用未来特征 | 特征对齐出错 | 审计每个特征的时间戳 |
| 对季节性过拟合 | 模型背下日历模式 | 测试集留出整个季节周期 |
| 忽略量纲变化 | 绝对值模式 vs 比例模式 | 建模百分比变化 |
| 滞后特征太多 | 「越多越好」错觉 | 用 ACF 确定范围 |
| 不做差分 | 「模型自己会学」 | 线性模型必须预处理 |

### 多步预测策略

| 策略 | 做法 | 优点 | 缺点 |
|------|------|------|------|
| 递归 | 单步预测，用预测值继续 | 一个模型 | 误差累积 |
| 直接 | 每个 horizon 一个模型 | 无误差累积 | 样本少，不共享信息 |
| 多输出 | 一个模型输出所有 horizon | 信息共享 | 需模型支持多输出 |

### 评估原则

- **MAE**：单位直观，适合业务解释
- **RMSE**：对大误差惩罚更重，适合模型优化
- **MAPE**：无量纲，可跨序列比较（值为 0 时未定义）
- **永远和简单基线比较**：季节性朴素预测是最低标准

## 7. 可复用产物

[prompt-time-series-advisor](file:///d:/workspace/github-projects/ai-engineering-from-scratch/phases/02-ml-fundamentals/15-time-series/outputs/prompt-time-series-advisor.md)

该 Prompt 系统化地帮助你：
1. 理解问题（目标、horizon、频率、外部特征）
2. 检查常见陷阱（时间分割、未来特征、平稳性、季节性）
3. 推荐方法（按场景匹配）
4. 特征工程清单（滞后值、滚动统计、差分值、日历特征）
5. 评估协议（Walk-forward + MAE/MAPE/RMSE + 基线对比）

## 8. 自测回顾

### 课前测评

**Q1**：为什么随机训练/测试分割对时间序列无效？
- 正确：随机分割会把未来数据泄漏到训练集，让模型作弊
- 核心概念：时间顺序必须被尊重

**Q2**：平稳性意味着什么？
- 正确：序列的统计性质（均值、方差、自相关）不随时间变化
- 核心概念：大多数预测方法假设平稳性

### 课后测评

**Q3**：差分的目的是什么？
- 正确：建模前后值的变化来移除趋势，使序列平稳
- 公式：diff[t] = value[t] - value[t-1]

**Q4**：lag-3 特征是什么？
- 正确：y[t-3] —— 3 个时间步前的值
- 核心概念：滞后特征将时间序列转为监督学习

**Q5**：向前走验证为什么比 k-fold CV 更好？
- 正确：尊重时间顺序，只用过去训练、用未来测试，防止前瞻偏差
- 核心概念：时间序列唯一诚实的评估方法

---

*教学日期：2026-05-31 | 关联课程：[[Phase2-LinearRegression]]、[[Phase2-ModelEvaluation]]*