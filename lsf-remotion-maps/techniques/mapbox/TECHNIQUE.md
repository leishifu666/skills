---
name: lsf-remotion-maps-mapbox-TECHNIQUE
description: Mapbox 二维地图：Remotion 地图中文参考。
---

# 
Mapbox 二维地图

用户指定 Mapbox 或需要其样式时使用，需访问令牌。地理计算优先 @turf/turf；路线、点和标签使用 GeoJSON source 与图层。默认保持相机静止，关闭交互和淡入；运动镜头前先阅读稳定性说明。动画由 useCurrentFrame() 驱动，加载和逐帧更新用 delayRender()/continueRender() 管理。
