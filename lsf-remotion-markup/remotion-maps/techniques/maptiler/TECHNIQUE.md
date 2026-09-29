---
name: lsf-remotion-maps-maptiler-TECHNIQUE
description: MapTiler 地图：Remotion 地图中文参考。
---

# 
MapTiler 地图

MapTiler 适合叠加国界、河流和地点标签。用 @maptiler/sdk 绘制底图、Planet 矢量图层与自定义 GeoJSON。地图只初始化一次，逐帧通过 setData/setPaintProperty 更新；等待 map.once('idle') 后继续。移动镜头优先用固定底图。标签可用定位后的 Interactive.Div；密钥放在 REMOTION_MAPTILER_KEY 环境变量中。
