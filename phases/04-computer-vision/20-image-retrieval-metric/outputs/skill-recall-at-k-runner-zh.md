---
name: skill-recall-at-k-runner
description: 编写一个干净的 recall@K 评估框架，支持训练/验证/检索库划分和规范的数据契约
version: 1.0.0
phase: 4
lesson: 20
tags: [retrieval, evaluation, recall, faiss]
---

# Recall@K 运行器

将一个包含查询图像和检索库图像及标签的文件夹转化为可复现的 recall@K 数值。

## 使用场景

- 新骨干网络的首次检索基准测试。
- 跨微调轮次跟踪嵌入质量。
- 在同一数据集上比较两个检索系统。

## 输入

- `query_images`: 路径列表。
- `gallery_images`: 路径列表（查询可能与检索库重叠，也可能不重叠）。
- `query_labels`, `gallery_labels`: 类别或实例 ID。
- `encoder_fn`: 可调用对象 `image -> embedding`（预计算或实时计算）。
- `ks`: 列表，如 `[1, 5, 10]`。

## 步骤

1. 对每个检索库图像编码一次。保存为 numpy 数组。
2. 对每个查询图像编码。
3. 对两组嵌入向量进行 L2 归一化。
4. 对于每个查询，计算与所有检索库项的相似度。
5. 按降序排序，取前 max(ks) 个。
6. 对于每个 K，检查前 K 个检索库项中是否有任何一个与查询的标签相同。
7. 报告 `recall@K = 在前 K 个结果中至少有一个正确邻居的查询比例`。

## 输出模板

```python
import numpy as np
from sklearn.preprocessing import normalize

def encode_all(images, encoder_fn, batch=32):
    out = []
    for i in range(0, len(images), batch):
        embs = encoder_fn(images[i:i + batch])
        out.append(embs)
    return np.concatenate(out)


def recall_at_k(query_emb, gallery_emb, q_labels, g_labels,
                ks=(1, 5, 10), query_ids=None, gallery_ids=None):
    if len(query_emb) == 0 or len(gallery_emb) == 0:
        return {f"recall@{k}": 0.0 for k in ks}

    g_label_set = set(g_labels.tolist())
    keep = np.array([lbl in g_label_set for lbl in q_labels])
    if not keep.any():
        return {f"recall@{k}": 0.0 for k in ks}

    q_emb_f = query_emb[keep]
    q_lab_f = q_labels[keep]
    q_id_f = query_ids[keep] if query_ids is not None else None

    q = normalize(q_emb_f)
    g = normalize(gallery_emb)
    sims = q @ g.T

    if q_id_f is not None and gallery_ids is not None:
        self_mask = q_id_f[:, None] == gallery_ids[None, :]
        sims = np.where(self_mask, -np.inf, sims)

    top_k_max = min(max(ks), g.shape[0])
    if top_k_max <= 0:
        return {f"recall@{k}": 0.0 for k in ks}

    top = np.argpartition(-sims, top_k_max - 1, axis=1)[:, :top_k_max]
    sorted_top = np.take_along_axis(
        top, np.argsort(-sims[np.arange(len(q))[:, None], top], axis=1), axis=1
    )
    out = {}
    for k in ks:
        k_eff = min(k, top_k_max)
        hits = np.any(g_labels[sorted_top[:, :k_eff]] == q_lab_f[:, None], axis=1)
        out[f"recall@{k}"] = float(hits.mean())
    return out


def evaluate(query_images, query_labels, gallery_images, gallery_labels, encoder_fn, ks=(1, 5, 10)):
    q_emb = encode_all(query_images, encoder_fn)
    g_emb = encode_all(gallery_images, encoder_fn)
    return recall_at_k(q_emb, g_emb, np.array(query_labels), np.array(gallery_labels), ks)
```

## 报告

```
[evaluation]
  num queries:   <整数>
  num gallery:   <整数>
  embedding_dim: <整数>

[recall]
  recall@1:  <浮点数>
  recall@5:  <浮点数>
  recall@10: <浮点数>
```

## 规则

- 在计算相似度之前对嵌入向量进行归一化；在归一化向量上使用 FAISS IndexFlatIP 等价于余弦相似度。
- 当查询的真实标签不在检索库中时，排除该查询；否则 recall 会被不必要地限制在 1 以下。
- 如果查询和检索库重叠，从查询自身的前 K 个结果中排除查询本身，否则你测量的是自相似度而非检索效果。
- 对于 `num_queries > 10,000`，对相似度矩阵乘法进行分批处理以避免内存溢出（OOM）。