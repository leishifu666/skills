---
name: lsf-remotion-maps-maptiler-map-explainer-architecture
description: 地图讲解片架构：Remotion 地图中文参考。
---

# 
地图讲解片架构

地图初始化一次；加载后整理底图、添加源和图层并等待空闲。每帧更新 GeoJSON 或图层样式，等待空闲、触发重绘，再继续 Remotion。河流沿路线显现，各区域在河流到达时触发填色与标签；时长按秒和 fps 换算。几何、标签和样式示例见相邻 assets；数据选择见 map-data-sources.md。
