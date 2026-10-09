---
name: lsf-remotion-maps
description: LSF Remotion 地图动画：为视频选择并实现静态地图、Mapbox、MapLibre、MapTiler 或 CesiumJS 方案。
version: 4.0.534
github_url: https://github.com/remotion-dev/skills
github_hash: 32b241b97f4e0e4ab61fe9a41b05e6e64503f8c5
---

# LSF Remotion 地图动画

根据目标镜头只选择一种实现方案，然后只阅读该方案的 `TECHNIQUE.md`。
每个方案目录都可以独立使用；移除其中一个不会影响其他方案。

## [静态地图](techniques/static-map/TECHNIQUE.md)

- 获取卫星图，将其放入 `<Img>`，再叠加动画。

## [Mapbox](techniques/mapbox/TECHNIQUE.md)

- 需要 Mapbox 密钥。
- 默认地图样式更丰富。
- 缩小视图时可显示为圆形地球。
- 包含埃菲尔铁塔等 3D 建筑。

## [MapLibre](techniques/maplibre/TECHNIQUE.md)

- 不需要 API 密钥，完全免费。
- 不包含 3D 建筑。

## [MapTiler](techniques/maptiler/TECHNIQUE.md)

- 使用 MapTiler。
- 可以在地理要素上方绘制注释，例如边界、河流和地名。

## [CesiumJS](techniques/cesium/TECHNIQUE.md)

- 用于穿越地形和山脉的飞行镜头。
- 提供“飞行模拟器”视角。

## 当前版本接口

实现前按本次问题读取 [4.0.534 官方接口与示例](references/upstream-current.md)。其中的媒体时间、可编辑节点和合成注册约定更新了旧版实现说明；本地用户改动、授权和交付要求继续适用。
