---
name: lsf-remotion-transparent-videos
description: "LSF Remotion 透明视频渲染：导出 ProRes 或 WebM 格式的透明视频。"
metadata:
  tags: transparent, alpha, codec, vp9, prores, webm
---

# LSF Remotion 透明视频渲染

Remotion 可以通过两种方式渲染透明视频：ProRes 视频或 WebM 视频。

## 透明 ProRes

适合导入视频编辑软件。

**命令行：**

```bash
npx remotion render --image-format=png --pixel-format=yuva444p10le --codec=prores --prores-profile=4444 MyComp out.mov
```

**Studio 默认设置**（修改后重启 Studio）：

```ts
// remotion.config.ts
import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("png");
Config.setPixelFormat("yuva444p10le");
Config.setCodec("prores");
Config.setProResProfile("4444");
```

**将其设为某个合成的默认导出设置**（通过 calculateMetadata）：

```tsx
import { CalculateMetadataFunction } from "remotion";

const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
}) => {
  return {
    defaultCodec: "prores",
    defaultVideoImageFormat: "png",
    defaultPixelFormat: "yuva444p10le",
    defaultProResProfile: "4444",
  };
};

<Composition
  id="my-video"
  component={MyVideo}
  durationInFrames={150}
  fps={30}
  width={1920}
  height={1080}
  calculateMetadata={calculateMetadata}
/>;
```

## 透明 WebM（VP9）

适合在浏览器中播放。

**命令行：**

```bash
npx remotion render --image-format=png --pixel-format=yuva420p --codec=vp9 MyComp out.webm
```

**Studio 默认设置**（修改后重启 Studio）：

```ts
// remotion.config.ts
import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("png");
Config.setPixelFormat("yuva420p");
Config.setCodec("vp9");
```

**将其设为某个合成的默认导出设置**（通过 calculateMetadata）：

```tsx
import { CalculateMetadataFunction } from "remotion";

const calculateMetadata: CalculateMetadataFunction<Props> = async ({
  props,
}) => {
  return {
    defaultCodec: "vp8",
    defaultVideoImageFormat: "png",
    defaultPixelFormat: "yuva420p",
  };
};

<Composition
  id="my-video"
  component={MyVideo}
  durationInFrames={150}
  fps={30}
  width={1920}
  height={1080}
  calculateMetadata={calculateMetadata}
/>;
```
