### AdaBoost sklearn 1.8.0 兼容性修复记录

#### 1. 问题背景
在运行 `phases/02-ml-fundamentals/11-ensemble-methods/code/ensembles.py` 脚本时，由于当前环境使用的 scikit-learn 版本为 1.8.0，`AdaBoostClassifier` 的 API 发生了变更，导致原有代码抛出兼容性异常，脚本无法正常执行。

#### 2. 根因分析
在 scikit-learn 1.8.0 中，`AdaBoostClassifier` 移除了 `algorithm` 参数（原用于指定 `"SAMME"` 或 `"SAMME.R"`）。新版本默认且仅支持 SAMME 算法的实现逻辑，继续显式传入 `algorithm="SAMME"` 会触发 `TypeError`。

#### 3. 修复方案
通过 `sed` 命令对源码进行原地替换，移除已废弃的 `algorithm="SAMME"` 参数。

**执行指令：**
```bash
sed -i 's/ada_sk = AdaBoostClassifier(n_estimators=50, random_state=42, algorithm="SAMME")/ada_sk = AdaBoostClassifier(n_estimators=50, random_state=42)/' phases/02-ml-fundamentals/11-ensemble-methods/code/ensembles.py
```

**验证修改：**
```bash
grep -n "AdaBoostClassifier" phases/02-ml-fundamentals/11-ensemble-methods/code/ensembles.py
```
确认输出第 479 行已更新为 `ada_sk = AdaBoostClassifier(n_estimators=50, random_state=42)`，且 import 语句未受影响。

#### 4. 验证结果
使用 `uv run --active` 重新执行脚本，所有模块均成功运行，无报错。关键指标如下：

| 模块 | 关键指标 | 结果 |
| :--- | :--- | :--- |
| AdaBoost (Scratch) | Test Accuracy (n=50) | 0.838 |
| Gradient Boosting | Test MSE (n=100) | 0.3073 |
| Bagging Classifier | Accuracy (20 trees) | 0.863 |
| Stacking Ensemble | Meta-learner Accuracy | 0.838 |
| **sklearn AdaBoost** | **Test Accuracy** | **0.880** |
| sklearn Random Forest | Test Accuracy | 0.890 |
| sklearn GBM | Test Accuracy | 0.910 |

#### 5. 结论与建议
-   **修复状态**：✅ 已完成。sklearn 1.8.0 兼容性问题已彻底解决。
-   **后续注意**：若项目中其他文件仍使用了 `AdaBoostClassifier(algorithm=...)`，需按相同方式批量清理。建议在项目依赖中明确锁定 scikit-learn 版本，或在代码中加入版本判断以兼顾新旧 API。