---
name: lsf-remotion-maps-cesium-3d-troubleshooting
description: Cesium 三维渲染排查：Remotion 地图中文参考。
---

# 
Cesium 三维渲染排查

独立无头浏览器可能只显示星空而不绘制地球。应在 Remotion 渲染循环内手动驱动 Cesium，逐帧调用完整 viewer.render()，不要只调用 scene.render()。禁用默认循环，等待瓦片和场景完成；排查 WebGL、密钥、跨域请求与 preserveDrawingBuffer。
