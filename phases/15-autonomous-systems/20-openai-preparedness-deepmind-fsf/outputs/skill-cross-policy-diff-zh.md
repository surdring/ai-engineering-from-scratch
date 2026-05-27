---
name: cross-policy-diff
description: 使用 OpenAI Preparedness Framework v2、Anthropic RSP v3.0 和 DeepMind FSF v3 作为参考，对特定能力进行跨策略比较。
version: 1.0.0
phase: 15
lesson: 20
tags: [preparedness-framework, fsf, rsp, cross-policy, scaling-policy]
---

给定一个特定的前沿能力（例如「长时间范围自主」、「自主复制与适应」、「R&D 自动化」），生成跨策略差异文档，展示三个框架各自如何分类该能力以及触发了哪些缓解措施。

生成：

1. **OpenAI PF v2 分类。** Tracked 或 Research。如果 Tracked，指出 Capabilities + Safeguards Report 的触发条件。如果 Research，注意策略语言是「潜在」缓解措施。
2. **Anthropic RSP v3.0 分类。** 哪个阈值（ASL-3、AI R&D-4、硬编码禁止）？哪种缓解（肯定案例、安全 + 部署）？确认承诺在 Anthropic 单边层还是行业建议层。
3. **DeepMind FSF v3 分类。** 哪个领域（Cyber、Bio、ML R&D、CBRN）？哪个 CCL 或跟踪能力级别？是否调用欺骗对齐监控？
4. **收敛总结。** 三个策略对该能力的严重性是否一致，还是存在有意义的差异？哪个分类最严格，哪个最宽松？
5. **测量依赖。** 每个分类都依赖能力测量。指出如何测量该能力以及哪个评估提供商（METR、Apollo、内部、第三方）拥有该测量。

硬性拒绝：
- 基于公告语言相似性而未提供文档级证据的跨策略一致声明。
- 任何不能指向源文档具体条款的分类。
- 将「Research Category」（OpenAI）视为等同于「Tracked Category」——它们有不同的操作后果。

拒绝规则：
- 如果用户不能提供每个分类的源文档段落，拒绝并要求先提供引用。
- 如果用户将策略存在视为实践中缓解的证据，拒绝并要求具体缓解措施触发的证据。
- 如果声称某框架「覆盖」了某能力但该词未出现在文档中，拒绝并要求具体的条款引用。

输出格式：

返回差异文档，包含：
- **能力定义**（一句话）
- **OpenAI PF v2 行**（分类、触发条件、源条款）
- **Anthropic RSP v3.0 行**（分类、触发条件、单边-vs-建议）
- **DeepMind FSF v3 行**（领域、CCL / TCL、欺骗对齐参与情况）
- **收敛总结**（一致之处 + 有意义的分歧）
- **测量归属**（评估提供商、评估频率）
- **读者建议**（最严格、最宽松，附理由）