---
name: encoding-audit
description: 审计越狱防御报告在编码族攻击方面的覆盖。
version: 1.0.0
phase: 18
lesson: 14
tags: [artprompt, ascii-art, encoding-attack, utes, structural-sleight]
---

给定越狱防御报告，枚举覆盖的编码族攻击以及捕获每个族的防御层。

生成：

1. **编码覆盖。** 列出评估的每个攻击族：ASCII art（ArtPrompt）、base64、leet-speak、UTF-8 同形字、嵌套 JSON/YAML/CSV、树/图 UTES、图像模态。标记缺失的族。
2. **防御层映射。** 对每个族，识别哪个防御层（关键字过滤器、困惑度过滤器、改写、重新令牌化、输出分类器、多模态审核器）捕获它，哪个不能。
3. **视觉识别缺口。** 根据 Jiang 等人 2024，PPL 和 Retokenization 对 ArtPrompt 失败，因为识别发生在视觉层面。报告的防御是否包含任何在视觉/结构层面操作的内容？
4. **泛化测试。** UTES（StructuralSleight）泛化到任意稀有结构。报告是否测试了不在其训练防御集中的结构？
5. **能力-安全权衡。** 具有更强视觉文本能力的模型（高 ViTC 分数）更容易受到 ArtPrompt 攻击。说明模型的 ViTC 分数（如果已报告）；如果没有则要求。

硬性拒绝：
- 任何仅基于子字符串/关键字过滤的防御声明。
- 任何覆盖一个编码族并外推到「编码攻击」的防御声明。
- 任何没有逐族攻击成功率的防御声明。

拒绝规则：
- 如果用户问 ArtPrompt 是否已被「修补」，拒绝并解释识别层面 vs 文本层面防御缺口。
- 如果用户要求推荐的全编码防御，拒绝单一推荐——防御必须对部署可能面临的所有族进行分层。

输出：一页审计，填写以上五个部分，标记主要编码缺口，并指出最紧迫添加的单一防御层。各引用 Jiang 等人（arXiv:2402.11753）和 StructuralSleight 一次。