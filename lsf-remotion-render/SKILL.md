---
name: lsf-remotion-render
description: "LSF Remotion 渲染：将 Remotion 合成导出为视频、静帧或逐帧图片。"
version: 4.0.529
---

# LSF Remotion 渲染

## 常规渲染方式

渲染视频：

```
npx remotion render
```

全部选项见：https://www.remotion.dev/docs/cli/render.md

渲染单帧图片：

```
npx remotion still
```

全部选项见：https://www.remotion.dev/docs/cli/still.md

一次将多个视频帧渲染为图片，可使用 `render --frames`：

```
npx remotion render [composition-id] out/frames --frames=0,30,90 --image-format=png
```

更多选项见：https://www.remotion.dev/docs/cli/render.md#--frames

## 透明视频

渲染带透明通道的视频时，阅读[透明视频](./transparent-videos.md)。
