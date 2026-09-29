---
name: lsf-remotion-maps-cesium-3d-flyover-architecture
description: 三维飞行镜头架构：Remotion 地图中文参考。
---

# 
三维飞行镜头架构

地图实例只初始化一次，禁用无关控件并设置 preserveDrawingBuffer。按模式加载地形和影像或城市 3D Tiles。用平滑地理路径计算逐帧相机位置、朝向与俯仰，并设定地形高度和安全距离。Remotion 每帧手动驱动 Cesium 完整渲染，等待瓦片稳定后继续；参数示例见同目录 assets。
