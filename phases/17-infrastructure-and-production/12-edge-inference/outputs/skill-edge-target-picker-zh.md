---
name: edge-target-picker
description: 根据设备、模型和延迟预算选择边缘推理目标（Apple ANE、Qualcomm Hexagon、WebGPU/WebLLM、NVIDIA Jetson）及匹配的量化格式。
version: 1.0.0
phase: 17
lesson: 12
tags: [edge, ane, hexagon, webgpu, webllm, jetson, core-ml, qnn, nvfp4]
---

给定部署平台（iOS、Android、浏览器、机器人/汽车/边缘服务器）、模型和延迟/内存预算，生成边缘目标推荐。

生成：

1. **目标。** 指定具体 NPU/GPU（ANE、Hexagon、WebGPU、Jetson Orin Nano / AGX / Thor）。用平台和 2026 运行时覆盖率论证。
2. **带宽上限。** 计算理论解码上限：bandwidth_GB_s / model_size_GB。与用户的 tok/s 需求比较。如果上限低于需求，拒绝或提议更小的模型/更严格的量化。
3. **量化格式。** 选择 Q4 GGUF（浏览器/边缘 CPU）、Core ML INT4 + FP16（ANE）、QNN INT8/INT4（Hexagon）或 NVFP4 + FP8 KV（Jetson Thor / Edge-LLM）。
4. **转换流水线。** 指定确切的转换器（Core ML converter、Qualcomm AI Hub、MLC-LLM for WebLLM、TensorRT-LLM Edge compiler）。
5. **上下文预算。** 说明与权重一起放入设备 RAM 的最大上下文。对长上下文用例，指定 KV 量化（Q4 KV）或拒绝。
6. **后备。** 当设备能力不足或 WebGPU 不可用时（Firefox Android、旧浏览器），指定服务端 API 后备，使用相同的 OpenAI 兼容接口。

硬性拒绝：
- 承诺超过带宽上限的 tok/s。拒绝——物理限制。
- 在 2026 年通过非 Core ML 运行时直接目标 ANE。只有 Core ML 原生暴露 ANE。
- 假设 WebGPU 在所有浏览器上都可用。2026 年覆盖率约 70-75% 移动端；始终指定后备。

拒绝规则：
- 如果模型 > 6 GB 且目标是手机（4-8 GB RAM），拒绝——先提议更小的模型或激进量化。
- 如果请求是 iPhone 上 7B 模型的 128K 上下文，拒绝——设备 RAM 无法容纳，除非使用 Q4 KV 加滑动窗口注意力。
- 如果部署需要 Android 上通过 WebGPU 的长上下文流式传输且用户要求 Firefox 支持，拒绝并要求 Chrome 或服务端后备。

输出：一页计划，指定目标、上限、量化、转换器、上下文预算、后备。以单一指标结尾：目标设备群中最差设备上的观测 tok/s。