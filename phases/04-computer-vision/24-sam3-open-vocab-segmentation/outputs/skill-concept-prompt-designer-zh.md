---
name: skill-concept-prompt-designer
description: 将用户表述转化为格式良好的 SAM 3 概念提示，包含拆分、消歧和回退策略
version: 1.0.0
phase: 4
lesson: 24
tags: [sam3, open-vocab, prompt-engineering, segmentation]
---

# 概念提示设计器

SAM 3 的准确性很大程度上取决于概念提示的表述方式。本技能将自由形式的用户表述规范化为 SAM 3 易于处理的提示。

## 使用场景

- 构建接受自然语言物体查询的用户界面。
- 通过 API 暴露 SAM 3，上游调用方发送的是完整句子。
- 调试 SAM 3 匹配效果差的问题 — 通常是因为提示格式不当，而非模型问题。

## 输入

- `utterance`: 原始用户字符串。
- `context`: 可选的领域提示（如 "监控"、"医疗"、"零售"）。
- `max_concepts`: 每个表述最多提取的概念数；默认 5。

## SAM 3 偏好的规则

- **简短的名词短语，而非句子。** `"cat"` 优于 `"there is a cat"`。
- **具体名词。** `"skateboard"` 优于 `"thing to ride on"`。
- **修饰语紧邻名词之前。** `"red car"` 优于 `"car that is red"`。
- **小写。** SAM 3 具有鲁棒性，但经验上小写输入略好。
- **单数或复数。** 两者均可；当预期有多个实例时复数更有利。

## 步骤

1. **按常见分隔符分词** — 逗号、分号、"and"、"or"、"&"。
2. **删除填充前缀** — "find"、"show me"、"segment"、"detect"、"locate"、"a"、"an"、"the"。
3. **仅保留可视的介词修饰语** — `"striped red umbrella"` 保留，`"umbrella from yesterday"` 不保留（`"from yesterday"` 不在图像中）。
4. **使用可选的 `context` 对冲突进行消歧**：
   - `"window"` 在监控上下文中 -> `"building window"`。
   - `"window"` 在医疗上下文中 -> 通常为错误；建议用户澄清。
5. **回退**：如果拆分后得到的概念数为零且表述包含至少一个具体名词，则回退到精确字符串。如果无法提取具体名词，则不输出概念 — 仅返回警告并请用户澄清（参见规则）。
6. **上限为 `max_concepts`。** 如果提取的概念数超过调用方要求的数量，保留前 `max_concepts` 个（按表述顺序），其余在 `dropped` 下输出，原因为 `"exceeded max_concepts"`。这可以在用户粘贴长串枚举时保持延迟可控。

## 输出格式

```
[designed prompts]
  utterance:    <原始表述>
  concepts:     ["concept_1", "concept_2", ...]
  dropped:      ["filler_1", ...]
  warnings:     ["概念过于抽象", "可能匹配多个类别", ...]

[sam3 calls]
  对每个概念运行: sam3.detect(image, concept)
  合并输出，每个检测带不同的概念标签。
```

## 示例

```
输入:  "can you find me a cat or two dogs?"
输出: ["cat", "dogs"]
丢弃: ["can you find me", "a", "or two", "?"]
说明: "dogs" 保留复数，因为表述中说 "two dogs" — 保留了复数提示。

输入:  "segment the big red truck and the blue sedan"
输出: ["big red truck", "blue sedan"]
丢弃: ["segment", "the", "and"]

输入:  "thing near the door"
输出: ["door"]
警告: ["'thing' 对 SAM 3 来说过于抽象；回退到 'door'"]

输入:  "striped red umbrella, green hat, pink balloon"
输出: ["striped red umbrella", "green hat", "pink balloon"]
```

## 规则

- 绝不要向 SAM 3 传递超过 8 个单词的句子 — 超过此长度准确率会下降。
- 当表述中不包含可提取的具体名词时，不运行 SAM 3；返回警告并请用户澄清。
- 不要按引号内的标点符号分割；如果带引号，将 `"black and white cat"` 保留为一个概念。
- 始终记录原始表述和派生概念，以便生产环境调试。