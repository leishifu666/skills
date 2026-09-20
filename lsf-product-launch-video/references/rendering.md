# 按帧渲染接入

本技能实测：Remotion / @remotion/bundler / @remotion/renderer 4.0.526，React 19.1.1，Windows，Chrome，FFmpeg。后续安装先核对当前包与文档，不混用 Remotion 包版本。

官方入口：[SSR](https://www.remotion.dev/docs/ssr-node)、[bundle](https://www.remotion.dev/docs/bundle)、[renderStill](https://www.remotion.dev/docs/renderer/render-still)、[renderMedia](https://www.remotion.dev/docs/renderer/render-media)。

## 最小执行链

1. 新建视频产物目录，记录入口、素材、时间线和依赖。现有项目源码按需直接导入。
2. `bundle({entryPoint, webpackOverride})` 生成 bundle。跨目录导入组件时，让 React 和 ReactDOM 指向同一安装，防止 Hook 双实例。
3. `selectComposition({serveUrl,id,inputProps})` 得到尺寸、帧率、时长。把同一 inputProps 传给后续渲染。
4. `renderStill` 输出开头、主要操作、镜头峰值、转场中间和尾帧，检查后再 `renderMedia`。
5. 由 `useCurrentFrame()` 计算 props、相机和文字；音频可用 Remotion Audio，也可由共享事件合成 WAV 后用 FFmpeg 复用视频流封装。
6. 输出 H.264 / yuv420p / AAC MP4，开启 faststart；用 ffprobe 和完整解码确认实际结果。

## 组件契约

- 优先选择 position/value/items 等受控 props；以视频状态驱动，不模拟真实后台完成。
- 若组件依赖图片加载，等待图片可解码后放行帧渲染；不要只等页面加载事件。
- 动画需要主题时在渲染专用浏览器上下文初始化，不改变用户应用的主题默认值。
- 按需带入原有样式；补齐 CSS utility 时列出补齐范围。场景包装、宣传文案、摄影机属于视频，不宣称是原界面的一部分。
- 异步网络、模型请求、用户数据读取在视频渲染中应替换为明确标识的 fixture。

## 实测用例

坤坤魔法图片前后对比：直接导入 `components/shared/BeforeAfterSlider.tsx` 和原 `ThemeProvider`，用受控 position 演示拖动和 5% 键盘步长；图片预览页面的接入由 `ImagePreviewModal.tsx` 与 `MultiImageCompareSlider.tsx` 核对。素材为原创演示图，不是模型生成质量证明。样片记录应保留源码文件 hash、音频报告和实际渲染参数。
