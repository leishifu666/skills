---
name: lsf-remotion-maps-maptiler-render-stability
description: 二维地图渲染稳定性：Remotion 地图中文参考。
---

# 
二维地图渲染稳定性

逐帧调用 map.jumpTo() 可能让底图闪烁。平移或缩放时保持地图相机静止，按路线生成足够大的底图画布，再逐帧对底图和 HTML 标签施加相同的 CSS 位移与缩放。控制尺寸，避免超过 WebGL 缓冲限制。
