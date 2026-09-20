# GSAP 连续镜头与确定性渲染

已在坤坤魔法 26 秒、多功能试跑中使用 GSAP 3.15.0 + Remotion 4.0.526。以下为工程方法，不是书中原文，也不意味着参考视频使用了同样的库。

## 先指定继承对象

每一对相邻镜头填四个值：`carryObject`、`exitState`、`entryState`、`focus`。例如中心模板卡 → 输入附件；输入容器 → 结果窗口；结果窗口 → 画布中心节点。没有继承对象时选择有理由的遮挡或切镜，不为炫酷任意旋转整个页面。

1. 给继承对象一个连续状态，包含 x/y/width/height/radius/opacity
2. 新旧内容放同一外壳，旧内容先退 4–8 帧，外壳开始变形，新内容晚进 6–12 帧；具体值按片子调整
3. 相机追随正在操作的区域；大动作后回到可读状态
4. 指针分接近、抓取、移动、释放，拖动时保持与被抓取对象的位置关系
5. 只在入场或落位短暂用回弹；实际阅读期间稳定
6. 标题和画面作为整体配重，输入框较矮时标题靠近，结果展开时标题同步腾出位置

## GSAP 驱动数据，Remotion 只画帧

### 输入特写与回到操作全景

为镜头状态建独立的 GSAP timeline，记录 `scale`、`focusX/focusY` 和目标屏幕位置。先测真实展开后的输入区域，不围绕整个页面中心盲目缩放。

- 页面/输入栏展开完成后推进，起始可试 1 → 1.3–1.5 倍；倍率按实际裁切调整，不作为所有镜头统一参数
- 打字期间保持主镜头稳定；只有文字超出安全区才做缓慢跟随，不逐字放大缩小
- 输入完成保留阅读停顿，再拉回到能同时看清参数、模型选择器与生成按钮的景别
- 模型菜单开启后检查浮层位置，不能让裁切将候选项挡在画外；镜头停稳后再选择
- 镜头层与产品组件层分开，缩放整组内容不重排真实 UI，按钮尺寸与 hover 行为保持原状

若镜头层 transform-origin 固定在左上角，局部焦点 `(fx, fy)` 映射到屏幕 `(tx, ty)`，使用平移 `x = tx - scale * fx`、`y = ty - scale * fy`，保证缩放与焦点位置一致。若外层还有偏移，先统一坐标系再计算。起止关键帧之间通过 GSAP 插值，检查文本、菜单与光标的裁切。

键入与音效读取同一事件表；真实组件用输入事件驱动，不直接按字符进度修改 DOM 或 setter。离线回放按固定事件时间重建，中文区分组词、提交和粘贴，不能冒称逐汉字插入等于真实输入法。声音变体在事件表中固定；按 [输入音效规则](segment-editing-and-typing.md#输入框与打字声音) 安排短组、停顿和提交。

```js
const state = {x: 960, y: 650, width: 1000, height: 220};
const timeline = gsap.timeline({paused: true});
timeline.addLabel('expand', event.frame / fps);
timeline.to(state, {
  y: 580, width: 960, height: 720,
  duration: event.durationFrames / fps,
  ease: 'power3.inOut',
}, 'expand');
const frames = [];
for (let f = 0; f < durationFrames; f++) {
  timeline.time(f / fps, false);
  frames.push({x: state.x, y: state.y, width: state.width, height: state.height});
}
timeline.kill();
gsap.ticker.sleep();
// Save frames as JSON; render frames[useCurrentFrame()] in the video.
```

不要把 GSAP 的内部 `_gsap` 缓存序列化。使用白名单属性，或过滤它。数据采样不依赖浏览器 raf、计时器、播放速度或截图顺序。图片素材仍需等待加载，组件主题/样式仍需注入。

## 验证

- 对同一工程连续采样两次，JSON 哈希一致
- 检查每次形状交接前后与中间帧；相同对象中心/尺寸应连续
- 画面音效使用同一 event，不手工重复维护两份时间点
- 查看静止镜头完整画幅以及缩略图，检查整体重心；细节放大镜头另查裁切
- 成片解码后再抽帧，不仅检查预渲染图
- GSAP 只负责执行，不能拿“用了 GSAP”当作视觉质量的验收结论

按片段开发时，画面区间仍可连续排列；为每处交接导出前后余量，由主时间线统一采样共享相机或继承对象，不能让两段各自归零再拼。交接字段和抽查范围见 [片段制作与拼接](segment-editing-and-typing.md#片段制作与拼接)。
