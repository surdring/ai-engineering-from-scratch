---
name: ner-picker
description: 为给定的命名实体识别（NER）提取任务选择合适的方法
version: 1.0.0
phase: 5
lesson: 06
tags: [nlp, ner, extraction]
---

给定任务描述（领域、标签集、语言、延迟、数据量），输出：

1. 方法。基于规则 + 词典、CRF、BiLSTM-CRF 或 Transformer 微调。
2. 起始模型。命名（spaCy 模型 ID，如 `en_core_web_sm` / `en_core_web_trf`；Hugging Face 检查点 ID，如 `dslim/bert-base-NER`；或"自定义，从头训练"）。
3. 标注策略。BIO、BILOU 或基于 span 的标注。一句话说明理由。
4. 评估。使用 `seqeval`。始终报告实体级 F1，绝不报告 token 级。

当标注样本少于 500 时，除非用户已有预训练领域模型（如医学领域的 BioBERT），否则拒绝推荐微调 Transformer。标记嵌套实体需要基于 span 或多轮模型。如果用户提到"生产规模"且使用开箱即用的 CoNLL-2003 标签，要求进行词典审计。