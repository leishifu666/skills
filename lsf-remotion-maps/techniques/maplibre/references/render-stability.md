---
name: lsf-remotion-maps-maplibre-render-stability
description: 二维地图渲染稳定性：Remotion 地图中文参考。
---

# 
二维地图渲染稳定性

逐帧改动相机可能让底图细节闪烁。需要平移缩放时，将地图相机固定在最大所需缩放级别，先渲染足够大的底图，再逐帧对画布和投影 HTML 叠层施加相同的 CSS 位移与缩放。限制 WebGL 画布尺寸。
