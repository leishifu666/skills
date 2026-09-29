---
name: lsf-remotion-maps-mapbox-render-stability
description: 二维地图渲染稳定性：Remotion 地图中文参考。
---

# 
二维地图渲染稳定性

逐帧调用 map.jumpTo() 可能造成底图细节闪烁。需要移动地图时，按路线渲染足够大的固定底图，保持地图相机不动，再对画布和 HTML 叠层应用相同的 CSS translate 和 scale。尺寸须符合 WebGL 缓冲限制，不要盲目放大数倍。
