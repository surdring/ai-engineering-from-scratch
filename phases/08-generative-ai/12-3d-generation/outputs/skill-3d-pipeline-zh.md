---
name: 3d-pipeline
description: 根据输入类型、输出格式和用例选择 3D 生成或重建流水线
version: 1.0.0
phase: 8
lesson: 12
tags: [3d, gaussian-splatting, nerf, mesh]
---

给定输入（文本 Prompt / 单张图像 / 少量图像 / 照片拍摄 / 视频）、目标输出（网格 / 高斯泼溅 / NeRF / 点云）和用例（实时渲染、游戏引擎、AR/VR、影视），输出：

1. 流水线。(a) 多视图扩散 + 3D 拟合（SV3D、CAT3D + 3DGS），(b) 直接单次生成（LRM、TripoSR、InstantMesh），(c) 文本到网格 + PBR（Meshy 4、Rodin Gen-1.5、Hunyuan3D 2.0），(d) 照片拍摄 + 3DGS（Gsplat、Postshot、Scaniverse）。
2. 基础模型 + 托管。指定模型 + 开源/托管。包含商业用途的许可证相关性。
3. 迭代预算。首次输出的预期时间、迭代成本、精炼策略。
4. 拓扑 + 材质。需要重新网格化？PBR 通道需求（反照率、粗糙度、金属度、法线）？UV 布局自动还是手动？
5. 评估。留出视图上的 SSIM、CLIP 分数、网格水密性、多边形数量、纹理分辨率。
6. 平台目标。Unity / Unreal / Blender / Web（three.js / Babylon）/ AR（USDZ / glb）。

拒绝在没有网格转换步骤的情况下将 3DGS 直接交付到游戏引擎（大多数引擎原生不支持渲染泼溅）。拒绝为复杂铰接角色使用文本到 3D — 应用支持骨骼绑定的流水线。标记任何 NeRF-only 输出且下游工具无法渲染 NeRF（大多数 DCC 工具）的情况。