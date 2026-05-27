---
name: skill-ctc-decoder
description: 从头编写贪心解码和束搜索（Beam Search）CTC 解码器，包含长度归一化
version: 1.0.0
phase: 4
lesson: 19
tags: [ocr, ctc, decoding, sequence-models]
---

# CTC 解码器

为 CTC 输出编写两种解码程序：贪心解码（快速）和束搜索（在噪声输入上效果更好）。

## 使用场景

- 在自定义 CRNN 输出上运行 OCR 推理。
- 针对不同解码器对预训练 OCR 模型进行基准测试。
- 在不引入 ctcdecode 的情况下实现简单的束搜索解码。

## 输入

- `log_probs`: (T, N, C) 词表上的对数 softmax 概率（按约定索引 0 = blank）。
- `vocab`: C 个字符的列表。
- `beam_width`（仅束搜索）：通常为 5-10。

## 贪心解码器

```python
def greedy_ctc_decode(log_probs, vocab, blank=0):
    preds = log_probs.argmax(dim=-1).transpose(0, 1).cpu().tolist()
    out = []
    for seq in preds:
        decoded = []
        prev = None
        for idx in seq:
            if idx != prev and idx != blank:
                decoded.append(vocab[idx])
            prev = idx
        out.append("".join(decoded))
    return out
```

## 束搜索解码器

```python
import heapq
import math

def beam_ctc_decode(log_probs, vocab, beam_width=5, blank=0):
    T, N, C = log_probs.shape
    lp = log_probs.cpu()
    results = []
    for n in range(N):
        beams = {("",): (0.0, -math.inf)}  # (前缀元组) -> (p_blank, p_nonblank)
        for t in range(T):
            logits_t = lp[t, n]
            new_beams = {}
            for prefix, (p_b, p_nb) in beams.items():
                for c in range(C):
                    p = logits_t[c].item()
                    if c == blank:
                        nb = p_b + p
                        nnb = p_nb + p
                        upd = new_beams.get(prefix, (-math.inf, -math.inf))
                        new_beams[prefix] = (
                            _logsumexp(upd[0], _logsumexp(nb, nnb)),
                            upd[1],
                        )
                    else:
                        last = prefix[-1] if prefix else ""
                        char = vocab[c]
                        if char == last:
                            # 情况1：保持在相同前缀上（从 p_nb 折叠）
                            upd = new_beams.get(prefix, (-math.inf, -math.inf))
                            new_beams[prefix] = (upd[0], _logsumexp(upd[1], p_nb + p))
                            # 情况2：通过 blank 分隔的重复来扩展前缀（"a_a" -> "aa"）
                            new_prefix = prefix + (char,)
                            upd = new_beams.get(new_prefix, (-math.inf, -math.inf))
                            new_beams[new_prefix] = (upd[0], _logsumexp(upd[1], p_b + p))
                        else:
                            new_prefix = prefix + (char,)
                            upd = new_beams.get(new_prefix, (-math.inf, -math.inf))
                            nb = _logsumexp(p_b, p_nb) + p
                            new_beams[new_prefix] = (upd[0], _logsumexp(upd[1], nb))
            beams = dict(heapq.nlargest(
                beam_width,
                new_beams.items(),
                key=lambda kv: _logsumexp(kv[1][0], kv[1][1]),
            ))
        best = max(beams.items(), key=lambda kv: _logsumexp(kv[1][0], kv[1][1]))[0]
        results.append("".join(best))
    return results


def _logsumexp(a, b):
    if a == -math.inf: return b
    if b == -math.inf: return a
    m = max(a, b)
    return m + math.log(math.exp(a - m) + math.exp(b - m))
```

## 规则

- 在 PyTorch 的 `nn.CTCLoss` 中，按约定 blank 索引为 0。
- 束搜索在低置信度输入上能提升准确率；在干净输入上的提升小于 1% CER。
- 永远不要将束宽度裁剪到 5 以下；精度-延迟的权衡在低于此值时趋于平坦。
- 在延迟预算紧张时使用束搜索，降级为贪心解码；在大多数生产 OCR 数据上质量损失很小。
- 对于大词表（CJK 有 3000+ 字符），改用 `ctcdecode`（C++）而非上述纯 Python 版本；Python 束搜索很快就会成为瓶颈。