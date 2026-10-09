---
name: lsf-remotion-maps-maplibre-TECHNIQUE
description: MapLibre 二维地图：Remotion 地图中文参考。
---

# 
MapLibre 二维地图

适用于 MapLibre 样式、路线、标记、标签和二维镜头。地理计算优先 @turf/turf；路线与标记使用 GeoJSON source/layer。默认关闭交互与淡入并保持静态相机。动画由 useCurrentFrame() 驱动；地图加载和逐帧更新用 delayRender()/continueRender() 管理。运动镜头先检查渲染稳定性。

实现本项前阅读 [当前官方接口与示例](upstream/TECHNIQUE.md)，按项目版本核对时间参数、类型和导入。
