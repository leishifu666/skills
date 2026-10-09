---
name: lsf-remotion-render
description: LSF Remotion 渲染：将 Remotion 合成导出为视频、静帧或逐帧图片。
version: 4.0.534
github_url: https://github.com/remotion-dev/skills
github_hash: 32b241b97f4e0e4ab61fe9a41b05e6e64503f8c5
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

## 当前版本接口

实现前按本次问题读取 [4.0.534 官方接口与示例](references/upstream-current.md)。其中的媒体时间、可编辑节点和合成注册约定更新了旧版实现说明；本地用户改动、授权和交付要求继续适用。
