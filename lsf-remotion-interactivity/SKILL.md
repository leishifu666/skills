---
name: lsf-remotion-interactivity
description: LSF Remotion 交互编辑：让合成元素能在 Remotion Studio 中选取、调整样式并编辑关键帧。
version: 4.0.534
github_url: https://github.com/remotion-dev/skills
github_hash: 32b241b97f4e0e4ab61fe9a41b05e6e64503f8c5
---

# LSF Remotion 交互编辑

按特定方式编写 Remotion 标记后，Remotion Studio 就能识别其结构，并提供交互编辑功能：

- 单击选取元素。
- 拖动、缩放和旋转元素。
- 编辑 CSS 样式。
- 编辑关键帧和缓动参数。

如果标记结构太复杂，Studio 无法识别，相关参数会显示为灰色。

## 使用 Interactive 让 HTML 元素可交互

除了 Img（它本身已支持交互）之外，所有 HTML 和 SVG 元素（例如 div）都可以通过 Interactive 变为可交互元素：

```tsx title="Interactive elements"
<Interactive.Div
  name="Greeting card"
  style={{fontSize: 80, padding: 24}}
>
  Hello
</Interactive.Div>
```

这样便可在 Studio 中设置样式和关键帧。请控制元素数量；如果一个组件包含太多元素，时间轴会变得杂乱。

## 文本优先写在元素内部

如果文本是固定的，而且只会用一次，就直接写在可交互元素内，不要先提取成常量。

```tsx title="Inline text"
// 👍 Fixed copy stays editable
<Interactive.Div name="Title">
  LSF Remotion 最佳实践
</Interactive.Div>
```

只有文本会动态变化或需要复用时，才使用属性或变量。

## 给可交互元素设置清楚的名称

为元素添加 name 属性，方便识别。避免动态计算名称，直接写明名称。

```tsx title="Interactive names"
<>
  <Interactive.Div name="Hero title" style={{fontSize: 80}}>
    Launch day
  </Interactive.Div>
  <Img name="Avatar" src="https://remotion.media/image.jpeg" />
  <Video name="Background" src="https://remotion.media/video.mp4" />
  <Sequence name="Title">
    Launch day
  </Sequence>
</>
```

## 将 CSS 样式全部内联

最简单的写法是直接把普通对象传给 style：不要引用常量、展开对象或使用数学表达式。

```tsx title="Interactive example"
<Interactive.Div
  style={{
    fontSize: 80,
    color: 'red',
  }}
>
  Hello World!
</Interactive.Div>
```

```tsx title="❌ Bad for interactivity"
const baseStyle = useMemo(() => {
  return {
    fontSize: 12 // ❌ Non-inline styles are not supported
  }
}, []);

<Interactive.Div
  style={{
    ...baseStyle, // ❌ Spreading is not supported
    color: RED, // ❌ Referring to constants is not supported
    scale: frame * 10 // ❌ Math is not supported
  }}
>
  Hello World!
</Interactive.Div>
```

## 用 interpolate() 制作动画

将 interpolate() 直接写在变化属性上。
输出区间、缓动、外推和 output 属性都要使用固定值。

输入区间还可以使用从 useVideoConfig() 直接解构出的 durationInFrames、fps、width 和 height。支持直接使用这些标识符、与数字相乘（例如 2 * fps 或 fps * 2），以及减去数字（例如 durationInFrames - 1）。

```tsx title="Inline values"
const {fps, durationInFrames} = useVideoConfig();

// 👍 Inline values can be standardized and keyframed
<Interactive.Div
  name="Product card"
  style={{
    color: 'white',
    fontSize: 80,
    scale: interpolate(frame, [0, fps], [0, 1], {
      easing: Easing.spring({damping: 200}),
      output: 'perceptual-scale',
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp'
    }),
    rotate: interpolate(frame, [0, 1 * fps], ['0deg', '20deg'], {
      easing: Easing.spring({damping: 200}),
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp'
    }),
    translate: interpolate(
      frame,
      [durationInFrames - 30, durationInFrames],
      ['0px 0px', '0px 120px'],
      {
        easing: Easing.spring({damping: 200}),
        output: 'perceptual-scale',
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp'
      }
    ),
  }}
/>
```

```tsx title="❌ Bad interactivity"
const translateY = interpolate(frame, [0, 30], [0, 120]); // ❌ Math should be directly in the markup

<Interactive.Div
  name="Product card"
  style={{
    translate: translateY, // ❌ Only inline interpolate() calls are supported,
    rotate: interpolate(frame, [start, start + 10], [0, Math.PI]), // ❌ Cannot use math with arbitrary variables, cannot use constants
    scale: interpolate(anyVariable, [0, 30], [0, 1]) // ❌ Can only interpret the `frame` variable.
  }}
/>
```

## 用 Interactive.Path 保持 SVG 路径可编辑

在 SVG 内使用来自 remotion 的 Interactive.Path，不要使用普通的 path，这样便能在 Studio 中直接编辑路径。

安装 @remotion/paths，以使用路径插值和 Studio 路径关键帧：

```sh
bunx remotion add @remotion/paths
```

如果几何形状是静态的，直接把路径字符串写在 d 属性中，不要提取成常量。

```tsx title="Editable static path"
import {Interactive} from 'remotion';

<Interactive.Svg width={300} height={300} viewBox="0 0 300 300">
  <Interactive.Path
    name="Triangle"
    d="M 40 40 L 260 40 L 150 260 Z"
    fill="#0b84f3"
  />
</Interactive.Svg>
```

### 用内联 interpolatePaths() 变形路径

直接在 d 属性中使用 @remotion/paths 的 interpolatePaths()。
参数依次为当前帧、输入区间、长度相同的路径字符串数组，以及缓动、外推和定格化选项。

按照上文 interpolate() 的输入区间规则，把输出路径、区间和选项都保留为内联值。
如果需要在 Studio 中编辑路径关键帧，不要使用 interpolatePath() API，也不要把插值结果提取到变量中。

```tsx title="Editable path keyframes"
import {interpolatePaths} from '@remotion/paths';
import {Easing, Interactive, useCurrentFrame} from 'remotion';

export const MorphingPath = () => {
  const frame = useCurrentFrame();

  return (
    <Interactive.Svg width={300} height={300} viewBox="0 0 300 300">
      <Interactive.Path
        name="Morphing triangle"
        d={interpolatePaths(
          frame,
          [0, 30, 60],
          [
            'M 40 40 L 260 40 L 150 260 Z',
            'M 40 150 L 150 40 L 260 150 Z',
            'M 40 260 L 150 40 L 260 260 Z',
          ],
          {
            easing: Easing.bezier(0.42, 0, 0.58, 1),
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          },
        )}
        fill="#0b84f3"
      />
    </Interactive.Svg>
  );
};
```

Studio 可以编辑当前帧的路径、添加或移动关键帧，并调整关键帧缓动。路径逐渐显现时使用 strokeDasharray 和 strokeDashoffset。

## 将 scale、translate 和 rotate CSS 属性用于动画

尽量避免使用 transform CSS 属性。优先使用 scale、rotate 和 translate，因为 Studio 只支持交互编辑这三种属性。

## 将合成元数据写成内联值

创建合成时，把 width、height、fps、durationInFrames 和 defaultProps 直接写在定义中，不要使用类型断言。

如果 Composition 或 Still 上的 defaultProps 是内联对象字面量，Props 编辑器就可以把视觉调整保存回代码。

```tsx
// 👍 Static values are in <Composition>, dynamic values are in calculateMetadata()
const calculateMetadata = useMemo(async () => {
  const dimensions = await getDimensions(); // just an example
  return {width: dimensions.width, height: dimensions.height};
});

<Composition
  id="my-video"
  component={MyComponent}
  durationInFrames={150}
  fps={30}
  calculateMetadata={calculateMetadata}
  defaultProps={{title: 'Hello', color: '#0b84ff'}}
/>
```

```tsx title="Negative examples"
const defaultProps = {title: 'Hello', color: '#0b84ff'}; // ❌ Don't extract defaultProps, must be inline
const calculateMetadata = useMemo(() => {
  // ❌ Unnecessary because no calculation is being done,
  return {durationInFrames: 150, fps: 30, width: 1920, height: 1080};
});

<Composition
  id="my-video"
  component={MyComponent}
  calculateMetadata={calculateMetadata}
  defaultProps={{
    title: 'Hello',
  } as Props} // ❌ Don't have type assertions, instead type MyComponent correctly
/>
```

只对动态变化的元数据使用 calculateMetadata()。

## Effect 也应内联

不要预先计算 effects 数组。
这里也遵循 interpolate() 的关键帧规则：输入区间、输出区间、缓动、外推和 output 属性都应使用固定值。

```tsx title="Effects"
// 👍 Parameters are inline and the array shape is stable
<CanvasImage
  src={src}
  width={1280}
  height={720}
  effects={[
    radialProgressiveBlur({
      center: [0.5, 0.5],
      width: 1.2,
      height: 0.8,
      start: 0.2,
      disabled: true,
      rotation: interpolate(frame, [0, 120], [0, 180]),
    }),
  ]}
/>

const center = [0.5, 0.5] as const;
const rotation = frame * 1.5;

<CanvasImage
  src={src}
  width={1280}
  height={720}
  // ❌ Conditional effect is not animateable
  effects={enabled ? [
    radialProgressiveBlur({
      // ❌ Not inline
      center,
      rotation,
    }),
  ] : []}
/>
```

如果某个版本要添加效果，而另一个版本不添加，请分别渲染两个元素。

## 让自定义组件可交互

使用 Interactive.withSchema() 时，在 schema 中包含 Interactive.baseSchema，这样裁剪、可见性等标准时间轴控件仍然可用。

要让自定义组件支持交互，请阅读[让组件支持交互](https://www.remotion.dev/docs/studio/make-component-interactive.md)。

## 视频剪辑

如果 Remotion 组件主要由视频和音频片段组成，请参阅“视频剪辑”指南，了解如何组织标记，使这些片段能在 Remotion Studio 时间轴中交互编辑。

## 当前版本接口

实现前按本次问题读取 [4.0.534 官方接口与示例](references/upstream-current.md)。其中的媒体时间、可编辑节点和合成注册约定更新了旧版实现说明；本地用户改动、授权和交付要求继续适用。
