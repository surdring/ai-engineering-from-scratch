---
name: skill-3dgs-export-router
description: 根据下游查看器或引擎，选择正确的 3DGS 导出格式（.ply / .splat / glTF KHR_gaussian_splatting / USD）
version: 1.0.0
phase: 4
lesson: 22
tags: [3d-gaussian-splatting, export, glTF, OpenUSD, pipeline]
---

# 3DGS 导出路由器

将下游目标映射到正确的 3DGS 文件格式。节省数小时的"无法加载"调试时间。

## 使用场景

- 训练完 3DGS 场景后，在分享到内容流水线之前。
- 在研究级（.ply）和生产级（glTF / USD）格式之间做选择。
- 流水线交接：拍摄团队 -> 3DGS 工程师 -> 游戏设计师 / VFX 艺术家 / Web 开发者。

## 输入

- `target_engine`: unreal | unity | omniverse | blender | vision_pro | three_js | babylon_js | cesium | playcanvas | supersplat
- `priority`: portability | file_size | quality_preservation
- `include_sh_degree`: 0 | 1 | 2 | 3

## 格式决策

| 目标 | 推荐格式 | 原因 |
|--------|--------------------|-----|
| Unreal Engine（虚拟制片） | Volinga 插件或 glTF KHR_gaussian_splatting | 原生 Unreal SDK 路径 |
| Unity（XR / 游戏） | .ply 通过 Aras-P Unity-GaussianSplatting 插件 | 社区标准 Unity 流水线 |
| NVIDIA Omniverse、Pixar 工具 | OpenUSD 26.03 (UsdVolParticleField3DGaussianSplat) | 原生 USD prim 类型 |
| Apple Vision Pro | OpenUSD 26.03 | visionOS 2.x 原生支持 |
| Blender | .ply + KIRI Engine 插件 | 社区插件读取原始 splats |
| Three.js Web 查看器 | glTF KHR_gaussian_splatting 或 .splat | 浏览器标准，配合 `GaussianSplats3D` 使用 |
| Babylon.js V9+ | glTF KHR_gaussian_splatting | V9 新增原生支持 |
| Cesium（CesiumJS 1.139+、Cesium for Unreal 2.23+） | glTF KHR_gaussian_splatting | 已发布明确支持 |
| PlayCanvas | .splat | PlayCanvas 原生量化格式 |
| SuperSplat（编辑器） | .ply 或 .splat | 导入 + 导出 |

## 量化权衡

- `.ply` 全精度：文件最大，无损，任何查看器都能读取。
- `.splat`：小 4-8 倍，SH3 系数有轻微质量损失，PlayCanvas 生态标准。
- glTF KHR：通过 EXT_meshopt_compression 可配置；兼容性最高且文件最小。
- USD：通过 USDZ 打包压缩；Apple 流水线中最小的文件。

## 输出报告

```
[export plan]
  target:         <引擎>
  format:         <名称>
  sh degree:      <0|1|2|3>
  compression:    <none|meshopt|quantisation|usdz>
  expected size:  <MB>
  compatible with: <查看器列表>

[pipeline]
  1. source: <来自训练的 .ply>
  2. optional: SuperSplat 清理步骤
  3. convert: <工具 + CLI 或 API 调用>
  4. package: <.gltf / .glb / .usd / .usdz / .splat / .ply>
  5. validate: <查看器完整性检查>
```

## 规则

- 绝不要静默地剥离 SH3 系数 — 这会明显改变镜面反射效果。
- 如果 `priority == file_size`，推荐 `.splat` 或带 meshopt 的 glTF；提示质量损失。
- 对于 Apple 平台，2026 年优先使用 USD / USDZ 而非 glTF；USDZ 在 visionOS 上有一等支持。
- 如果目标查看器的 3DGS 支持处于标准发布前（2026 年 2 月之前），推荐 `.ply` 和查看器的自定义加载器；Khronos 标准 glTF 尚不会被识别。
- 在交接之前，始终在至少一个查看器中验证导出的文件；量化过程中可能发生静默损坏。