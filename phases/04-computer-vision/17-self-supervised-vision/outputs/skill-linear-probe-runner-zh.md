---
name: skill-linear-probe-runner
description: 为任意冻结编码器和带标注数据集编写完整的线性探针评估
version: 1.0.0
phase: 4
lesson: 17
tags: [自监督, 评估, linear-probe, pytorch]
---

# 线性探针运行器

通过在冻结编码器上训练单个线性分类器来评估其特征。这是每篇自监督论文的标准评估方法。

## 使用场景

- 比较自监督检查点
- 追踪预训练 epoch 中的特征质量
- 判断预训练编码器对于下游任务是否足够好，无需微调

## 输入

- `encoder`：冻结的 `nn.Module`，为每张图像返回固定维度的特征
- `feature_dim`：编码器输出的维度
- `train_dataset`：带标注数据集（图像, 类别 ID）
- `val_dataset`：保留的验证集
- `num_classes`：任务类别数
- `epochs`：ImageNet 规模通常 100，更小数据集 50

## 步骤

1. 设置编码器为 eval 模式，所有参数的 `requires_grad=False`
2. 对训练集和验证集各提取一次特征。存储为 numpy 数组或内存映射文件
3. 在缓存特征上，用 SGD + 余弦调度训练 `nn.Linear(feature_dim, num_classes)`
4. 标准超参数：`lr=0.1`，`momentum=0.9`，`weight_decay=0`，`batch_size=1024`。线性探针对 `lr` 出奇敏感——如果准确率不佳，进行学习率扫描
5. 报告训练结束时验证集上的 top-1 准确率

## 输出模板

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.optim import SGD
from torch.optim.lr_scheduler import CosineAnnealingLR

def extract(encoder, loader, device="cpu"):
    encoder.eval()
    feats, labels = [], []
    with torch.no_grad():
        for x, y in loader:
            f = encoder(x.to(device)).cpu()
            feats.append(f)
            labels.append(y)
    return torch.cat(feats), torch.cat(labels)


def linear_probe(encoder, feature_dim, train_loader, val_loader,
                 num_classes, epochs=50, lr=0.1, device="cpu"):
    for p in encoder.parameters():
        p.requires_grad = False

    f_train, y_train = extract(encoder, train_loader, device)
    f_val, y_val = extract(encoder, val_loader, device)

    head = nn.Linear(feature_dim, num_classes).to(device)
    opt = SGD(head.parameters(), lr=lr, momentum=0.9, weight_decay=0)
    sched = CosineAnnealingLR(opt, T_max=epochs)

    ds = torch.utils.data.TensorDataset(f_train, y_train)
    train_iter = DataLoader(ds, batch_size=1024, shuffle=True)

    best_val = 0.0
    for ep in range(epochs):
        head.train()
        for x, y in train_iter:
            x, y = x.to(device), y.to(device)
            loss = F.cross_entropy(head(x), y)
            opt.zero_grad(); loss.backward(); opt.step()
        sched.step()

        head.eval()
        with torch.no_grad():
            acc = (head(f_val.to(device)).argmax(-1).cpu() == y_val).float().mean().item()
        best_val = max(best_val, acc)
    return best_val
```

## 报告

```
[线性探针]
  encoder:      <名称 + 预训练检查点>
  feature_dim:  <整数>
  epochs:       <整数>
  best_val_top1: <浮点数>
```

## 规则

- 线性探针期间绝不更新编码器权重；那将是微调而非探针
- 预计算特征一次；每个 epoch 重新训练编码器浪费 100 倍计算
- 使用 SGD 加余弦调度且无权重衰减；Adam 在此有时表现不佳
- 每个编码器族至少扫描一次学习率；最优值在不同 SSL 方法间有差异