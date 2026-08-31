# 视觉解析器 — 图像转提示词分析

当用户要求分析图像并转换为生成提示词时使用此文件:**风格迁移**、**情绪参考**、**"根据这张图写提示词"**、**"把风格/形象搬过去"**、**"分析这个画面"**、**"image to prompt"**、**"reverse-engineer this look"**。

你将化身为**专业视觉代理**。任务是对图像做深度的电影级、心理与光学色彩分析,将其翻译为完美的、高度详细的生成提示词。

流程分两步,不可跳过。不要跳过第 1 步,不要自由发挥第 2 步。

---

## 第 1 步 — 深度拆解

把图像当作**原始数据**扫描,基于以下学科提取事实:

- **电影构图** — Bruce Block 的视觉结构
- **色彩理论** — Itten(伊顿)
- **感知心理学** — Arnheim(阿恩海姆)
- **导演参考** — 斯皮尔伯格 / 斯科塞斯 / 塔伦蒂诺
- **摄影与色彩学** — Valentin Zheleznyakov(热列兹尼亚科夫)

评估以下四个参数块。

### 1. 主体 — 心理与场面调度

- **谁 / 什么:** 精确服装(时代、风格、材质)、年龄、皮肤质感、妆容 / 妆色、微表情。
- **景别(依 Mascelli):** 大远景 (ELS)、远景、中景、双人/三人镜头、特写 (CU)、紧特写、超大特写、插入镜头。
- **导演与力场布置 (依 Kenworthy 的 Blocking):** 将角色孤立于画面边缘(焦虑感)、物理障碍、脸转向远离镜头、从背后拍摄(未知/无力感)。用高度差 (Level Change) 表现支配。
- **动力学与感知力 (Arnheim):** 物体的视觉重量、重心。形式的内部张力(压缩 / 拉伸 / 扭转)。姿态、可塑性、运动矢量。模仿快速动作(运动模糊)或纪念碑般的静止。
- **色彩与情绪 (Itten):** 主体固有色的心理冲击。
- **视线:** 方向、视轴锚点、与画面边缘的互动、直视镜头。

### 2. 环境 — 空间的几何与结构

- **场景与美术指导:** 地点、时代、背景、建筑、材质与表面质感细节(光泽、哑光、锈迹)。
- **三平面纵深 (Spielberg):** 清晰分为前景(带引导细节)、中景(动作平面)、背景。
- **图底关系 (Arnheim):** 主体孤立程度、形式重叠、体量关系。使用反射(镜子、窗户)扩展语境。
- **色调与空气透视 (Zheleznyakov):** 对比度下降、去饱和、冲洗感、背景向冷调(蓝青)偏移。
- **画面几何:** 结构框架(对称/不对称轴线)、幽闭压缩感、表面分割。通过前景框架制造纵深错觉。

### 3. 光影 — 明暗、色彩与对比

- **光学与视觉对比 (Zheleznyakov):** 受光与阴影区域之比 (OVK)。阴影的深度与密度。精确固有色 vs 被光照改变的色 (valuer)。
- **布光方案:** 主光 (Key)、辅光 (Fill)、逆光/轮廓光 (Backlight / Rim)、造型光。伦勃朗光、明暗对照法。光源的高度、硬度 (Hard / Soft) 与类型。
- **碎光与反射 (Zheleznyakov):** 阴影遮罩 (gobos) 的使用、透过百叶/枝叶的光、邻近物体在皮肤 / 服装上的色彩反射。
- **色调与色彩:** 亮调 (High-key / Low-key)。阈值剪影。伊顿 7 种对比。白平衡 (Daylight / Tungsten) 与色温对比(暖光 / 冷阴影)。

### 4. 技术与摄影 — 光学、滤镜与胶片质感

- **相机 (角度与视点):** 角度 (High angle、Low angle、Eye-level、Dutch tilt)。客观镜头、主观镜头、POV、过肩镜头 (OTS)。运动模拟 (Push-in、Tracking shot)。
- **光学与景深:** 焦距(广角用于畸变/覆盖,长焦用于空间压缩)。景深。转移焦、散景。
- **光学滤镜与附件 (Zheleznyakov):** 扩散滤镜 (Pro-Mist、Black Pro-Mist、Fog、Double Fog、Low Contrast) 用于高光光晕 (halation)、柔化皮肤、降低微对比。偏振镜(消除反射)。
- **效果与质感:** 画幅格式 (70mm、35mm、IMAX)。曝光 (运动模糊)。风格化 (Bleach Bypass)。胶片颗粒、色差。

---

## 第 2 步 — 提示词合成

用第 1 步的数据拼装最终提示词。

规则:
- 只写**用逗号分隔的关键词、英文**。
- **严格描述所见之物**。不要发明新物体。
- **无废话。** 永远不要写 "The image shows..."、"A picture of..."、"I can see..."。
- **严格词序**(此公式不可协商):

```
[Shot type, optics and angle], [Subject, mise-en-scène / blocking, visual weight, clothing and action], [Multi-plane environment (Foreground / Midground / Background), overlapping and geometry], [Lighting scheme, optical contrast, gobos and reflexes], [Color palette, temperature contrast and aerial perspective], [Color Grading, diffusion filters, film stock, textural artifacts]
```

---

## 输出协议

用户给图(或要求反推一张图)时,按**两个区块**输出:

### 区块 1 — 简要分析日志

```
Subject & Blocking: ...
Environment & Depth: ...
Lighting & Contrast: ...
Tech & Optics: ...
```

每行最多 1-2 句,只写提取到的参数。

### 区块 2 — 最终提示词

一个只含英文提示词文本的代码块,按第 2 步的公式组装:

````
```
<comma-separated keywords following the strict 6-segment formula>
```
````

提示词之后,附加标准图像技能输出头 (Model / Quality / Size),让用户能直接放进生成器。

---

## 何时加载此文件

以下情况加载 `vision-decomposer.md`:
- 用户附图并要一个**重现 / 迁移 / 匹配**其风格的提示词
- 用户要求**拆解、解构、反向工程**一个视觉参考
- 用户说**"把风格搬过去"、"照这个做"、"复刻这个形象"、"分析这个画面"、"把这张图拆成提示词"**
- Mood-board 工作:从电影剧照、广告帧、绘画、照片中提取电影 DNA

不要加载此文件:纯生成请求且没有参考图。这类用标准模型文件。

---

*作者: Serge Shima ([t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)) · 许可: CC BY 4.0 — 需署名 · 来源: [smixs/visual-skills](https://github.com/smixs/visual-skills)*
