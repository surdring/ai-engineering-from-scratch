---
name: skill-image-text-retriever
description: 用任意 CLIP 检查点构建图像嵌入索引；支持通过文本查询和通过图像查询
version: 1.0.0
phase: 4
lesson: 18
tags: [clip, 检索, faiss, 零样本]
---

# 图像-文本检索器

使用 CLIP 嵌入将图像文件夹转化为可搜索索引。

## 使用场景

- 在内部目录上构建零样本图像搜索
- 通过嵌入距离去重近乎相同的图像
- 在没有标注数据集的情况下构建快速「查找相似」组件

## 输入

- `image_folder`：图像文件目录
- `clip_model`：HuggingFace id，如 `openai/clip-vit-base-patch32` 或 `google/siglip-base-patch16-224`
- `index_type`：flat | IVF | HNSW
- `embedding_dim`：从模型推断

## 步骤

1. 加载 CLIP 模型和预处理器
2. 批量编码文件夹中的每张图像。以 (N, D) float32 保存嵌入 + 文件名列表
3. 在嵌入上构建 FAISS 索引。在 L2 归一化向量上使用内积以获得余弦相似度
4. 暴露两个查询接口：
   - `search_by_text(text, k)`——嵌入文本，搜索
   - `search_by_image(image_path, k)`——嵌入图像，搜索

## 输出模板

```python
import os
import glob
import numpy as np
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor
import faiss


class ImageTextRetriever:
    def __init__(self, model_name="openai/clip-vit-base-patch32"):
        self.model = CLIPModel.from_pretrained(model_name).eval()
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.dim = self.model.config.projection_dim
        self.index = None
        self.filenames = []

    @torch.no_grad()
    def _encode_images(self, paths, batch=16):
        embs = []
        for i in range(0, len(paths), batch):
            imgs = [Image.open(p).convert("RGB") for p in paths[i:i + batch]]
            inputs = self.processor(images=imgs, return_tensors="pt")
            out = self.model.get_image_features(**inputs)
            out = out / out.norm(dim=-1, keepdim=True)
            embs.append(out.cpu().numpy())
        return np.concatenate(embs).astype(np.float32)

    @torch.no_grad()
    def _encode_text(self, texts):
        inputs = self.processor(text=texts, return_tensors="pt", padding=True)
        out = self.model.get_text_features(**inputs)
        out = out / out.norm(dim=-1, keepdim=True)
        return out.cpu().numpy().astype(np.float32)

    def build_index(self, folder, index_type="flat"):
        exts = ("*.jpg", "*.jpeg", "*.png", "*.webp", "*.bmp")
        files = []
        for ext in exts:
            files.extend(glob.glob(os.path.join(folder, ext)))
        self.filenames = sorted(files)
        embs = self._encode_images(self.filenames)
        if index_type == "IVF":
            quantizer = faiss.IndexFlatIP(self.dim)
            nlist = min(256, max(4, len(embs) // 32))
            self.index = faiss.IndexIVFFlat(quantizer, self.dim, nlist)
            self.index.train(embs)
        elif index_type == "HNSW":
            self.index = faiss.IndexHNSWFlat(self.dim, 32, faiss.METRIC_INNER_PRODUCT)
        else:
            self.index = faiss.IndexFlatIP(self.dim)
        self.index.add(embs)

    def search_by_text(self, text, k=5):
        q = self._encode_text([text])
        dist, idx = self.index.search(q, k)
        return [(self.filenames[i], float(d)) for d, i in zip(dist[0], idx[0])]

    def search_by_image(self, image_path, k=5):
        q = self._encode_images([image_path])
        dist, idx = self.index.search(q, k)
        return [(self.filenames[i], float(d)) for d, i in zip(dist[0], idx[0])]
```

## 报告

```
[检索器]
  模型:          <名称>
  图像数量:      <整数>
  维度:          <整数>
  索引类型:      flat | IVF | HNSW
  索引大小_mb:   <浮点数>
```

## 规则

- 索引前始终对嵌入进行 L2 归一化；FAISS 内积在归一化向量上等价于余弦相似度
- 对于 < 10 万张图像，`IndexFlatIP`（精确）最简单最快
- 对于 10 万-1000 万，`IndexIVFFlat` 是标准折中方案
- 对于 > 1000 万，使用 HNSW 或乘积量化变体
- 绝不每次查询都重建索引；嵌入一次，搜索多次