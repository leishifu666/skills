# 演示幻灯片

面向演示与路演的专业幻灯片视觉。

## 设计原则

### 一页一个观点
不要组合无关概念。观众对视觉的记忆力是 65%,而听到的内容仅 10%。

### 内容限制
- 每页最多 5 个要点
- 文本块 15-20 词
- 标题 + 列表**或**段落,不要同时

### 排版
```
标题: 44-54 pt, bold
副标题: 28-36 pt, medium
正文: 18-24 pt, regular (最小 18 保证可读)

字体: sans-serif 为主 (Inter, Helvetica, Roboto)
Serif 仅用于强调
```

### 对比与颜色
- 最多 3-4 色 (主色 + 2-3 强调色)
- 一种中性背景 (white/black/gray)
- 对比度最低 4.5:1
- 黑底避免纯白 #fff — 用 #f5f5f5

### 留白
- 内容要能呼吸
- 非对称布局 (2/3 + 1/3) 比居中布局更有动感
- 太挤就拆成两页

### 视觉一致性
- 一种风格: 照片**或**插画**或**极简图形
- 混用 = 视觉混乱
- 只用高清图,每张图都强化观点

### 检查清单
```
☐ 一页 = 一个观点
☐ 最多 5 个要点
☐ 标题 44-54pt,正文 18-24pt
☐ 3-4 色,高对比
☐ 留白充足
☐ 高清视觉,统一风格
```

---

## 页面类型

### Hero 标题页 (暗色)
```
Create dramatic title slide for [CONTEXT] presentation.

Background: Gradient from [DARK hex] to #0a0a0a.
Atmospheric: subtle mist at lower edge.

Typography:
"[MAIN TITLE]" in extra bold, white, extremely large, upper third
"[SUBTITLE]" in thin, muted, 5x smaller, below

Mood: Confident, premium
Format: 16:9
```

### 数据可视化
```
Create data slide for [CONTEXT] presentation.

Background: Dark gradient [hex] to [hex].

Hero number: "[METRIC]" in bold, [ACCENT], center
Trend: [up/down arrow] in [green/red]
Supporting: 3-4 smaller metrics below

Chart: [TYPE] showing [DATA]

Mood: Analytical, impactful
Format: 16:9
```

### 对比页 (亮色)
```
Create comparison slide for [CONTEXT].

Background: Off-white #fafafa to #f0efed.

Split layout:
Left: "[OPTION A]" with details
Right: "[OPTION B]" with details

Emphasis: Right side accent bar #3b82f6

Mood: Clear, objective
Format: 16:9
```

### 洞察/问题页
```
Create insight slide for [CONTEXT].

Background: Clean off-white.

Focal: "[KEY MESSAGE]" in bold, centered
Supporting: "[CONTEXT]" smaller, below
Emphasis bar: [ACCENT] strip with data point

Mood: Clarity, focus
Format: 16:9
```

### 流程/时间轴
```
Create process slide for [CONTEXT].

Flow: [HORIZONTAL/VERTICAL]
Stages: [1]→[2]→[3]→[4]
Each: icon + "[LABEL]" + description
Connectors: arrows in [ACCENT]

Format: 16:9
```

## 排版

**层级:**
- Hero: "Extremely large, dominating upper third"
- 主级: "Large, commanding"
- 次级: "3-5x smaller than hero"
- 页脚: "Minimal"

**字重:** thin | regular | medium | bold | extra bold
**位置:** "upper third"、"left aligned 10% margin"、"centered"

## 色彩系统

**暗色调色板:**
- 近黑: #0a0a0a、#121212
- 深色调: #0d3d2d、#1a2a3a
- 文字: #ffffff、#e0e0e0

**亮色调色板:**
- 米白: #fafafa、#f8f9fa
- 暖灰: #f5f5f4
- 文字: #1a1a1a、#374151

**数据色彩:**
- 正向: #22c55e
- 负向: #dc2626
- 强调: #3b82f6

## 氛围效果

- "Subtle gradient haze"
- "White mist at ground level"
- "Soft vignette darkening edges"
- "Noise texture for premium feel"

---

## 布局系统

通用排版规则。适用于任何视觉风格。

---

### 便当格 (Bento Grid)

不同尺寸块组成的模块化系统。

**核心规则:**
- 父容器带明确的模块边界
- 层级: 重要内容 → 大块,次要内容 → 小块
- 最多 9 块 (否则过载)
- 统一间距 (标准 16px)
- 关联内容归入同一块

**块形:** 宽/扁 (hero) | 窄/高 (列表) | 方块 (图标)

**网格:**
```
3-block:           6-block:             9-block:
┌───────┬───┐     ┌───┬───┬───┐       ┌─────┬───┬───┐
│ HERO  │SEC│     │ S │ S │ S │       │HERO │MED│ S │
├───────┴───┤     ├───┴───┼───┤       ├──┬──┴───┼───┤
│  FOOTER   │     │ CHART │LST│       │S │ MED  │ S │
└───────────┘     └───────┴───┘       └──┴──────┴───┘
```

**提示词:**
```
Layout: bento grid, [N] blocks
Hero block: [MAIN], Medium: [SECONDARY], Small: [ICONS]
Gaps: uniform spacing
```

---

### 非对称网格

视觉平衡的动态构图。

**规则:**
- 从基础网格开始,然后有意识地打破
- 平衡重量: 左侧大元素 = 右侧若干小元素
- 三分法带来自然平衡
- 关键元素用大小与位置突出

**适用:** 创意演示、作品集、fashion、初创公司
**不适用:** 银行、政府门户、大数据 B2B、老年受众

**提示词:**
```
Layout: asymmetric composition
Left: [LARGE - 60%], Right: [2-3 SMALLER stacked]
Balance: visual weight distributed
Rule of thirds positioning
```

---

### 负空间

把空间当作聚焦工具。

**规则:**
- 用于结构化,而非为了美而留空
- 引导注意力,聚焦主角
- Gestalt: 分隔开的元素 = 独立,靠近的 = 关联

**适用:** 高端品牌、极简演示、hero 区块
**不适用:** 新闻门户、仪表盘、移动端

**提示词:**
```
Layout: generous whitespace
Focal point: [ELEMENT] with breathing room
Empty space: intentional, guides eye to [CTA]
```

---

### 分屏

双栏构图。

**比例:**
- 50/50 - 对等元素
- 60/40 - 侧重一侧
- 70/30 - 明显主角 + 辅助

**提示词:**
```
Layout: split-screen [RATIO]
Left: [CONTENT], Right: [CONTENT]
Divider: [sharp / gradient / none]
```

---

### 粗野主义

生猛美学、巨型字体、鲜艳颜色。

**规则:**
- 保持清晰导航与层级
- 可读性 > 表现力
- 选择性使用: 亮色**或**巨型字体

**适用:** 艺术家作品集、fashion、初创公司
**不适用:** 电商、企业、教育、金融科技

**提示词:**
```
Style: brutalist design
Typography: massive, raw
Colors: high contrast, bold
Hierarchy: clear despite unconventional styling
```

---

## 未来感 / SaaS 风格

Apple Keynote 极简 + 玻璃拟态 + 3D 物体。

### 视觉语言
```
Style: Apple Keynote + SaaS + glassmorphism
Mood: premium, immersive, clean, breathable
Lighting: volumetric, ray-traced reflections, ambient occlusion
Base: deep void black OR pure ceramic white
Accents: aurora gradients (neon purple, electric blue, coral, cyan)
```

### 玻璃拟态卡片
```
Material: frosted glass with blur
Edges: delicate white borders
Shadow: soft, diffused
Spacing: generous internal whitespace
```

### 3D 视觉锚点
```
Purpose: abstract 3D artifacts as focal points
Materials: polished metal, iridescent acrylic, transparent glass, soft silicone
Shapes: capsules, spheres, shields, Möbius strips, fluid waves
Quality: looks like expensive collectibles
```

### 按类型构图

**封面:** 中央巨大 3D 玻璃物体 + 粗体标题 + 极光背景
**内容页:** 便当格 + 小卡内 3D 图标 + 大卡内文字
**数据页:** 分屏 (左侧文字、右侧发光 3D 图表)

### 图表风格
```
3D donut charts, glowing
Capsule-shaped progress bars
Floating numbers with neon glow
Style: looks like glowing neon toys
```

### 示例提示词
```
Create a futuristic SaaS slide for product presentation.

Style: Apple Keynote + glassmorphism.
Mood: premium, immersive, clean.
Background: void black with aurora gradient (purple → cyan).

Layout: bento grid, 6 blocks.
Cards: frosted glass, blur, white edges, soft shadows.
Hero block: floating iridescent sphere.
Data blocks: glowing 3D donut chart, neon metrics.

Typography: clean sans-serif, high contrast white.
Format: 16:9
```

---

*作者: Serge Shima ([t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)) · 许可: CC BY 4.0 — 需署名 · 来源: [smixs/visual-skills](https://github.com/smixs/visual-skills)*
