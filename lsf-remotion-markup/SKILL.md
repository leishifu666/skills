---
name: lsf-remotion-markup
description: "LSF Remotion 标记最佳实践：编写视频合成、动画、媒体、效果和排版。"
version: 4.0.529
---

# LSF Remotion React 标记最佳实践

本技能说明如何编写 Remotion React 标记。若任务与标记编写无关，请改用 LSF Remotion 最佳实践。

## 保留用户已有改动

用户可能在对话之外编辑代码。如果发现意外变化，先保留原样；必要时再向用户确认。

## 通用规则

使用 useCurrentFrame() 和 interpolate() 驱动动画。
CSS transition 或 animation 无法正确渲染，需要改写。
Tailwind 动画类也无法正确渲染，需要改写。

使用 Easing.bezier() 和 Easing.spring() 调整动画节奏。

按照 LSF Remotion 交互编辑最佳实践组织标记。

```tsx
import { useCurrentFrame, Easing, interpolate, Interactive } from "remotion";

export const FadeIn = () => {
  const frame = useCurrentFrame();

  return (
    <Interactive.Div
      name="Title"
      style={{
        opacity: interpolate(frame, [0, 2 * fps], [0, 1], {
          extrapolateRight: "clamp",
          extrapolateLeft: "clamp",
          easing: Easing.bezier(0.16, 1, 0.3, 1),
        }),
      }}
    >
      Hello World!
    </Interactive.Div>
  );
};
```

把 interpolate() 直接写在 style 属性中。
使用 scale、translate 和 rotate CSS 属性，不要使用 transform。

```tsx
// 👍 Inline editable keyframes and transform shorthands
style={{
  scale: interpolate(frame, [0, 100], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.spring({damping: 200}),
    output: 'perceptual-scale' // For `scale` animations, use "output: 'perceptual-scale'"
  }),
  translate: interpolate(frame, [0, 100], ["0px 0px", "100px 100px"], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.spring({damping: 200}),
  }),
  rotate: interpolate(frame, [0, 100], ["20deg", "90deg"], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.spring({damping: 200}),
  }),
}}

// 👎 Non-inline values and transform strings become harder to edit in Studio
const scale = interpolate(frame, [0, 100], [0, 1]);

style={{
  transform: `scale(${scale})`,
}}
```

## 资源文件

把资源放在项目根目录的 public/ 文件夹中。
使用 staticFile() 引用该文件夹中的资源。

## 媒体组件

使用来自 @remotion/media 的 Video 和 Audio 添加视频、音频。
使用 CanvasImage 添加图片。
要添加动画 GIF、APNG、WebP 或 AVIF，请使用 AnimatedImage；如果不用 Chrome，则使用 @remotion/gif。
对 public/ 中的文件使用 staticFile()，也可以直接传入远程 URL：

```tsx
import { Audio, Video } from "@remotion/media";
import { staticFile, CanvasImage, AnimatedImage } from "remotion";

export const MyComposition = () => {
  return (
    <>
      <Video src={staticFile("video.mp4")} style={{ opacity: 0.5 }} />
      <Audio src={staticFile("audio.mp3")} />
      <CanvasImage
        src={staticFile("logo.png")}
        style={{ width: 100, height: 100 }}
      />
      <Video src="https://remotion.media/video.mp4" />
      <AnimatedImage src={staticFile('nyancat.gif')} />
    </>
  );
};
```

## 场景示例

```tsx
import {
  AbsoluteFill,
  Easing,
  Interactive,
  interpolate,
  useCurrentFrame,
  useVideoConfig
} from "remotion";

export const Empty = () => {
  const {fps} = useVideoConfig();
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      name="Scene"
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'white'
      }}
    >
      <Interactive.Div
        name="Title"
        style={{
          opacity: interpolate(frame, [1 * fps, 2 * fps], [0, 1], {
            extrapolateRight: "clamp",
            extrapolateLeft: "clamp",
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
          fontSize: 88
        }}
      >
        Title
      </Interactive.Div>
      <Interactive.Div
        name="Subtitle"
        style={{
          opacity: interpolate(frame, [2 * fps, 3 * fps, 8 * fps, 10 * fps], [0, 1, 1, 0], {
            extrapolateRight: "clamp",
            extrapolateLeft: "clamp",
            easing: [Easing.bezier(0.16, 1, 0.3, 1), Easing.linear, Easing.bezier(0.16, 1, 0.3, 1)],
          }),
          fontSize: 32
        }}
      >
        Subtitle
      </Interactive.Div>
    </AbsoluteFill>
  );
}
```

## 延迟显示与裁剪

大多数组件支持以下属性，包括 AbsoluteFill、Interactive.*、Img、AnimatedImage、CanvasImage、HtmlInCanvas、Solid、来自 remotion 的 Sequence、来自 @remotion/media 的 Video 和 Audio、Gif 等。

### from

```tsx
<Img from={1 * fps} {/* ... */}/>
<Video from={1 * fps} {/* ... */}/>
<Interactive.Div from={1 * fps} {/* ... */}/>
```

元素从什么时候开始显示。

### durationInFrames

```tsx
<Img durationInFrames={20 * fps} {/* ... */}/>
<Interactive.Div durationInFrames={20 * fps} {/* ... */}/>
```

图层持续播放的帧数。
对于媒体，请传入媒体自身的自然时长，例如：Video 的 durationInFrames 应等于 29.322 * fps。

### trimBefore

适合需要延后启动内部时钟的组件：

```tsx
// Trim away first 2 seconds of footage
<Video trimBefore={2 * fps} {/* ... */} />

// `useCurrenFrame()` for children starts at `10 * fps`
<Sequence trimBefore={10 * fps} {/* ... */} />
```

### 替代方案

如果组件不支持这些属性，可用来自 remotion 的 Sequence 包裹它。

- layout="absolute-fill" 让 Sequence 的行为与 AbsoluteFill 相同。
- layout="none" 表示无包装元素的“无头”模式。

## 地图

需要在视频中加入地图时，阅读[LSF Remotion 地图动画](./remotion-maps/REFERENCE.md)，或加载 lsf-remotion-maps。

## 文本高亮和注释

文本高亮、标记、圆圈、下划线、删除线、划掉效果和方框，参阅 [text-highlights.md](text-highlights.md)。

## 多场景视频

计划连续展示多个场景时，参阅 [multi-scene-video.md](multi-scene-video.md)。

## 关联合成

如果某个场景或图层组需要独立且可编辑的时间轴，请参阅 [connected-compositions.md](connected-compositions.md)。多场景视频中的重要场景优先采用这种结构。

## 旁白

要用 ElevenLabs TTS 为 Remotion 合成添加 AI 旁白，参阅 [voiceover.md](voiceover.md)。

## 嵌入视频

高级视频嵌入用法（裁剪、音量、速度、循环和音调）参阅 [embedding-videos.md](embedding-videos.md)。

## 嵌入音频

高级音频用法（裁剪、音量、速度和音调）参阅 [audio.md](audio.md)。

## 视频剪辑

要在 Remotion Studio 中建立可编辑的视频时间轴，参阅 [video-editing.md](video-editing.md)。

## 裁切

需要裁切组件可见区域时，参阅 [cropping.md](cropping.md)。

## 转场

场景转场模式参阅 [transitions.md](transitions.md)。

## 动态模糊

要添加动态模糊或运动轨迹，请阅读 [motion-blur.md](motion-blur.md)，了解推荐的 HTML-in-canvas 方案、预览要求和替代方法。

## 视觉与像素效果

制作视觉效果时，先判断 CSS/HTML 是否足够，还是需要 shader。优先顺序如下：

1. 使用常规 HTML、CSS 或其他 Web 技术。
2. 直接对元素应用效果（例如 Video、Img），或用 [HtmlInCanvas](html-in-canvas.md) 包装内容；它也支持 effects：

- 使用 [effects.md](effects.md) 中列出的效果。
- 没有合适预设时，可按 [effects.md](effects.md) 使用自定义 createEffect()。

## 3D 内容

使用 Three.js 和 React Three Fiber 在 Remotion 中制作 3D 内容，参阅 [3d.md](3d.md)。

## 音效

需要音效时，阅读 [sfx.md](sfx.md)。

## 音频可视化

要显示频谱条、波形或随低音变化的效果，请阅读 [audio-visualization.md](audio-visualization.md)。

## 字幕

处理字幕时，使用 LSF Remotion 最佳实践路由到当前可用的 Remotion 文档指导。

## Google Fonts

在 Remotion 中加载字体时，推荐使用 Google Fonts；方法见 [google-fonts.md](google-fonts.md)。

## 本地字体

加载本地字体的方法见 [local-fonts.md](local-fonts.md)。

## GIF

在 Remotion 时间轴上同步显示 GIF，参阅 [gifs.md](gifs.md)。

## 高级图片用法

图片尺寸和位置、动态图片路径及获取图片尺寸的方法见 [images.md](images.md)。

## Lottie 动画

在 Remotion 中嵌入 Lottie 动画，参阅 [lottie.md](lottie.md)。

## 时间控制

interpolate() 的更多用法见 [timing.md](timing.md)。

## 参数化视频

要通过 Zod schema 让合成可配置，参阅 [parameters.md](parameters.md)。

## 测量 DOM 节点

测量 DOM 元素尺寸的方法见 [measuring-dom-nodes.md](measuring-dom-nodes.md)。

## 测量文本

测量文本尺寸、让文本适配容器并检查溢出，参阅 [measuring-text.md](measuring-text.md)。

## 使用 FFmpeg

裁切视频或检测静音等操作需要使用 FFmpeg；更多信息见 [ffmpeg.md](ffmpeg.md)。

## 静音检测

需要检测并裁掉视频或音频中的静音片段时，参阅 [silence-detection.md](silence-detection.md)。

## 动态时长、尺寸和数据

动态设置合成时长、尺寸和属性，参阅 [calculate-metadata.md](calculate-metadata.md)。

## 高级合成

定义静帧、文件夹、默认属性和嵌套合成，参阅 [compositions.md](compositions.md)。要在 Studio 中进入某个场景自己的时间轴，请使用 [connected-compositions.md](connected-compositions.md)。

## 高级序列编排

更多延迟、裁剪和限制素材时长的用法，参阅 [sequencing.md](sequencing.md)。

## 安装模块

使用 npx remotion add 安装与当前版本匹配的新包：

```
npx remotion add @remotion/media
```

该命令适用于 @remotion/*、mediabunny、@mediabunny/*、zod 和 @huggingface/transformers。

## 视觉检查

需要检查画面时，打开 Remotion Studio 进行交互式预览。
也可以通过渲染查看一帧或多帧图片。
