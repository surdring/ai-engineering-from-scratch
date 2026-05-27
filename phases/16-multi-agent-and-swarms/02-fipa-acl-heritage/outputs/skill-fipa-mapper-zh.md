---
name: fipa-mapper
description: 将任何 2026 年智能体协议规范（MCP、A2A、ACP、ANP、CA-MCP、NLIP 或新协议）映射到 FIPA-ACL 行为动词和交互协议，以判断哪些是真正的新颖性，哪些是重新发明。
version: 1.0.0
phase: 16
lesson: 02
tags: [multi-agent, protocols, FIPA, speech-acts, interoperability]
---

给定一个新的智能体协议规范，生成 FIPA-ACL 映射，使读者能够判断哪些部分是重新发明，哪些是真正的新结构。

生成：

1. **信封映射。** 对规范定义的每种消息类型，指出最接近的 FIPA 行为动词（`inform`、`request`、`query-if`、`query-ref`、`propose`、`accept-proposal`、`reject-proposal`、`cfp`、`subscribe`、`cancel`、`failure`、`not-understood` 或其余约 20 个之一）。如果没有行为动词匹配，精确描述差距。
2. **关联模型。** 规范如何将请求关联到回复，将取消关联到原始请求，将流式事件关联到订阅？与 FIPA 的 `:conversation-id` 和 `:reply-with` 字段进行比较。
3. **内容语言立场。** 规范是要求内容模式（类型化工件、JSON-Schema），接受自然语言，还是保持开放？与 FIPA 的 SL0/SL1 和本体字段进行比较。
4. **交互协议库。** 哪些 FIPA 交互协议可以在该规范之上实现：contract-net、subscribe-notify、request-when、propose-accept？指出实现每个协议所需的消息。
5. **发现模型。** 智能体如何找到对等方和能力（MCP `listTools`、A2A Agent Card、ANP DID + 元协议）？与 FIPA 的目录代理和黄页服务进行比较。
6. **重新发明 vs 新颖性。** 生成一个简表，三列：[FIPA 概念、现代规范等价、变化了什么]。将每行标记为 [重新发明] 或 [新结构]。只有当规范引入了 FIPA 没有的原语时，一行才是「新结构」——去中心化身份、类型化多模态工件和 LLM 可解释内容是常见的候选。

硬性拒绝：

- 任何声称某规范是「革命性」但未展示 FIPA 没有的原语的映射。言语行为理论 + 本体开销是失败模式，而非原语。
- 忽略发现层的框架比较。没有发现的规范是不完整的，而非新颖的。
- 像「协议 X 取代 FIPA」这样的陈述，未解决两个智能体对内容含义产生分歧时会发生什么（语义漂移）。

拒绝规则：

- 如果规范处于预标准化阶段（草稿不足 6 个月，没有公开实现），声明映射是临时的，并标记最可能的三个变化。
- 如果规范是闭源或仅限企业的（某些 ACP 风格），映射已文档化的内容并指出缺口。
- 如果用户仅提供博客文章（没有规范文档），在映射前要求提供规范。

输出：一页简要文档。以一句话总结开头（「协议 X 是 FIPA `request`/`subscribe` 加上 JSON 语法和基于 DID 的发现层。」），然后是上述六节，最后以结尾段回答：「该规范将重新发现 FIPA 的哪个旧失败模式？」