---
name: lsf-remocn
description: >
  使用 remocn 为 Remotion 视频安装动画和时间轴驱动的 UI 组件。
  适用于场景编排、动画、转场、背景、界面模拟，以及按钮、对话框和命令菜单等基础组件。
  即使用户未提及 remocn，只要任务需要精致的 Remotion 视频，也应考虑使用。
---

# LSF Remocn 视频组件

remocn 提供适用于 Remotion 的可复制组件。组件通过 shadcn 安装到项目的 components/remocn/，安装后代码由项目自行维护。

## 查询在线组件目录

组件目录会持续变化，本地不保留完整副本。每次挑选组件都先读取：

https://remocn.dev/llms-components.txt

目录按类别列出组件，包含用途、避免场景、自然时长、风格、层级、依赖和完整文档链接。先筛选候选项，再读取选中组件的文档。组件文档 URL 以 .md 结尾，例如：

~~~text
https://remocn.dev/docs/typography/blur-out-up.md
https://remocn.dev/docs/transitions/whip-pan.md
https://remocn.dev/docs/ui/components/dialog.md
~~~

不要凭组件名猜 URL 路径。使用可用的网页读取工具或 curl 获取资料。网络不可用时说明限制并停止，不要猜属性、默认值或时长；属性名猜错会导致构建失败，时长猜错可能让动画被截断。

## 安装

先准备 Remotion 项目，例如运行 npx create-video@latest。通过命名空间安装：

~~~bash
shadcn add @remocn/blur-out-up
~~~

项目的 components.json 需配置 registries。也可从 https://remocn.dev/r/<name>.json 安装。组件依赖通过 registryDependencies 自动安装，例如安装 @remocn/typewriter 时也会安装 @remocn/remocn-ui 和 @remocn/caret。共享核心库 @remocn/remocn-ui 提供时间轴折叠 hook、主题上下文和颜色计算，大多数 UI 基础组件会依赖它，通常不需要手动安装。

## 两类组件

- **动画组件（remocn）**：文字动画、转场、背景、界面模拟、品牌与社交卡片、完整场景。按帧驱动，常见属性包括 speed；文字组件还可能提供 fontSize、color、fontWeight。
- **UI 基础组件（remocn-ui）**：时间轴驱动的 shadcn 风格按钮、对话框、选择框、命令菜单和提示框等。通过 state、style、variant、size、theme 控制状态，不接受 speed。

先看目录中的 Tier 标记，再读取该组件的文档。不要把动画组件属性套用到 UI 基础组件。

## 动画组件约定

每个组件的 Props 类型和可选属性以对应文档为准。speed 通常表示时间倍率，默认值通常为 1；文字组件常见字号、颜色和字重属性。转场组件通常导出小写工厂函数，返回 TransitionPresentation，通过 TransitionSeries.Transition 的 presentation 属性传入，再用 linearTiming 或 springTiming 设置时长。

部分名为转场的组件其实负责完整场景编排，例如 slide-swap 和 spring-settle，它们接收 scenes 数组并管理整个时间线。需按组件文档确认类型。

UI 基础组件使用状态属性，例如 open/closed，不依赖 speed。对话框、警告对话框和抽屉等模态组件需与触发元素组合，结构按组件示例实现。

## Remotion 动画 API

~~~tsx
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateRight: "clamp",
});
const scale = spring({
  fps,
  frame,
  config: { damping: 12, mass: 1, stiffness: 100 },
});

// 使用确定性随机值，不要使用 Math.random()
import { random } from "@remotion/random";
const jitter = random(`seed-${frame}`);
~~~

## 场景与时间线

~~~tsx
import { Sequence, Series } from "remotion";

<Sequence from={30} durationInFrames={60}>
  <Typewriter text="npm install remocn" />
</Sequence>

<Series>
  <Series.Sequence durationInFrames={60}><SceneA /></Series.Sequence>
  <Series.Sequence durationInFrames={60}><SceneB /></Series.Sequence>
</Series>
~~~

## 画布和时长

- 默认画布为 1280×720、30 fps；组件通常按这个画幅设计。
- 目录中的 Length 表示组件自身动画的自然时长，不是整段场景的时长。转场组件的 Length 通常作为 linearTiming 或 springTiming 的时长；其他动画的 Length 表示动画完成帧。Sequence 至少应覆盖这个时长，并按需要增加停留时间。
- 标为 state-driven 的组件由 state 属性控制状态，本身没有固定动画时长。
- 按品牌选择目录中的 vibe 标签。paper 风格使用约每秒 10 个姿态的量化节奏、手写和墨迹效果；优先与同风格组件搭配，不要混入平滑动画体系。

## 设计默认值

自行新增的文字、场景框架和卡片应克制：使用正常字距和句式大小写、纯色文字与轻微阴影。不要无缘由添加装饰性字距、全大写、渐变文字或发光阴影。组件本身若以某种效果为特色，例如 tracking-in 或社交卡片渐变，不要移除该效果。

设计细则见：
- https://remocn.dev/docs/craft/design-defaults.md
- https://remocn.dev/docs/craft/motion-principles.md
- https://remocn.dev/docs/craft/anti-patterns.md

## 常见问题

- 终端滚动按离散步骤移动，不要给滚动本身加弹簧或缓动。
- 分栏布局在宽度动画时设置 overflow: hidden，避免内容溢出。
- 光标闪烁按帧计算，例如 Math.floor(frame / 15) % 2 === 0，不使用 interval。
- 静态资源放在 public/，通过 staticFile('cursor.svg') 加载，不要直接导入。
- 社交卡片离线时使用空 avatarUrl 或 coverUrl 触发渐变占位，不要依赖运行时抓取网络图片。

通用 Remotion 规则（确定性随机数、避免 setInterval、优先动画 transform、渲染前加载字体）见 lsf-remotion-best-practices。

## 完整视频的制作方式

不要堆砌组件，要围绕一个故事组织视频。

1. **选择策略**：决定复用模板、组合现有组件还是新建组件，见 references/anatomy.md。
2. **安排镜头**：产品演示可按钩子、定位、产品展示、功能、证据、行动号召组织；最后两拍可按内容省略。
3. **选择配方**：references/archetypes/index.md 会导向各类视频的镜头节奏、内容字段、时长选项和组件建议。
4. **为每拍选组件**：从在线目录查找，匹配品牌 vibe，并依据组件 Length 安排 Sequence。
5. **检查质量**：只保留一个强调色、易读文字和真实内容；避免光晕与机械罗列功能。

## 参考入口

本地制作说明：
- references/anatomy.md：模板、组件组合和新建组件的取舍；产品演示结构与质量标准。
- references/archetypes/index.md：各类视频配方索引。

在线组件资料：
- https://remocn.dev/llms-components.txt：组件目录，查询时从这里开始。
- https://remocn.dev/docs/<section>/<name>.md：单个组件的完整说明。
- https://remocn.dev/docs/craft/design-defaults.md：设计默认值与令牌。
- https://remocn.dev/docs/craft/motion-principles.md：动画原则。
- https://remocn.dev/docs/craft/anti-patterns.md：常见生成问题。
- https://remocn.dev/llms.txt：完整文档索引。
