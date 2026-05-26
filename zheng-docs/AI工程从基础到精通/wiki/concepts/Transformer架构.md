# Transformer 架构

## 知识库中的位置

Transformer 是当代 AI 的基石架构：

- [[../07-transformers-deep-dive/01_why-transformers]] — 为什么 Transformer 取代了 RNN/LSTM
- [[../07-transformers-deep-dive/02_self-attention-from-scratch]] — Self-Attention
- [[../07-transformers-deep-dive/03_multi-head-attention]] — 多头注意力
- [[../07-transformers-deep-dive/04_positional-encoding]] — 位置编码：Sinusoidal、RoPE、ALiBi
- [[../07-transformers-deep-dive/05_full-transformer]] — 完整 Transformer 实现
- [[../07-transformers-deep-dive/06_bert-masked-language-modeling]] — BERT：编码器架构
- [[../07-transformers-deep-dive/07_gpt-causal-language-modeling]] — GPT：解码器架构
- [[../07-transformers-deep-dive/08_t5-bart-encoder-decoder]] — T5/BART：编码器-解码器
- [[../07-transformers-deep-dive/11_mixture-of-experts]] — MoE：稀疏激活专家模型
- [[../07-transformers-deep-dive/12_kv-cache-flash-attention]] — KV Cache + Flash Attention
- [[../07-transformers-deep-dive/13_scaling-laws]] — Scaling Laws：计算最优分配
- [[../07-transformers-deep-dive/14_build-a-transformer-capstone]] — 综合实践

## 三大范式

| 类型 | 代表模型 | 用途 |
|------|----------|------|
| Encoder-only | BERT, RoBERTa | 理解任务（分类、NER、语义分析） |
| Decoder-only | GPT, LLaMA, Claude | 生成任务（文本生成、对话） |
| Encoder-Decoder | T5, BART | 翻译、摘要 |

## 关键创新时间线

1. **2017** — "Attention Is All You Need" 提出 Transformer
2. **2018** — BERT + GPT 双星闪耀
3. **2019** — GPT-2 展示 Scaling 潜力
4. **2020** — GPT-3 确立 Scaling Laws
5. **2021** — Vision Transformer (ViT)，MoE (Switch Transformer)
6. **2022** — Chinchilla Scaling Laws，Flash Attention
7. **2023** — LLaMA 开源，RoPE 成为标配，GQA/MQA
8. **2024** — DeepSeek-V3 (MoE)，Mamba/SSM 挑战注意力
9. **2025+** — NSA (Native Sparse Attention)，Differential Attention

## 跨阶段关联

- Transformer 的 Self-Attention 来自 [[concepts/注意力机制]]
- Decoder-only 架构是 [[concepts/大语言模型LLM]] 的标准
- ViT 将 Transformer 引入 [[concepts/计算机视觉]]
- MoE 架构是 [[concepts/推理优化]] 的关键技术
- Scaling Laws 指导 [[concepts/模型训练范式]]