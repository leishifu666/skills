---
name: leishifu-ppt-style-factory
description: PPT 风格模板工厂——从截图、HTML、网页 URL、文字描述、色板、已有风格混搭、CSS/设计 token 中提取或创建视觉风格，通过 16 维度分析生成完整 PPT 主题模板。当用户提到"提取风格"、"做个主题"、"这个网站风格不错"、"用这个配色做模板"、"style factory"、"风格工厂"，或给了参考图/截图/HTML/URL 并想变成 PPT 模板时，都应使用此 Skill。即使用户只说"这个好看"配上一张图，也要考虑触发。
---

# LeishiFu PPT Style Factory

从各种来源提取或创建 PPT 视觉风格，通过 **16 维度**完整定义，输出：
- 风格定义 JSON（16 维度）
- 完整横向翻页 HTML PPT 模板（单文件，全新构建）
- 完整 `:root` CSS 变量块

## 7 种输入方式

| # | 方式 | 触发词示例 | 输入 |
|---|------|-----------|------|
| 1 | 📸 截图/图片 | "这个截图的风格"、"参考这张图" | 图片文件 |
| 2 | 🧩 HTML 代码 | "从这个 HTML 提取风格" | .html 路径 |
| 3 | 🌐 URL 网页 | "这个网站风格不错" | URL |
| 4 | 💬 文字描述 | "赛博朋克风"、"日式侘寂" | 文字 |
| 5 | 🎨 色板 | "用 #1a1a2e 和 #e94560" | hex/rgb |
| 6 | 🔀 混搭已有 | "A 的配色 + B 的字体" | 风格库名称 |
| 7 | 📄 CSS/Token | "用公司设计规范" | .css / .json |

不确定用户想用哪种时，直接问。

## 16 维度概览

每个风格由 16 个维度完整定义，缺一不可。详细规格和 JSON schema 见 `references/dimensions.md`。

| 维度 | 一句话说明 |
|------|-----------|
| D1 配色体系 | ink(文字) + paper(背景) + tint(变体) |
| D2 强调色体系 | accent + accent-alt + 功能色 |
| D3 标题字体 | 字族 + 衬线/非衬线 + CJK 字体 |
| D4 正文字体 | 正文字族 + 等宽字体 |
| D5 字重体系 | hero/heading/body/emphasis 各级字重 |
| D6 字号比例 | 响应式字号 + 中文大标题分档 |
| D7 间距密度 | 紧凑/标准/宽松 + 各级间距值 |
| D8 背景风格 | WebGL 类型(流体/网格/粒子/纯色) |
| D9 圆角与边框 | 硬朗(0px) ↔ 柔和(16px) |
| D10 阴影体系 | 无/轻/中/重 |
| D11 动效倾向 | 入场方式 + 时长 + 缓动 |
| D12 图标风格 | 图标库 + 线性/填充 |
| D13 图片处理 | 滤镜 + 圆角 + 比例 |
| D14 卡片风格 | outlined/filled/glass/elevated |
| D15 装饰元素 | 点阵/线条/几何/无 |
| D16 视觉气质 | 美学标签 + 适用场景 |

---

## 工作流

### Step 1 · 识别输入方式

判断用户给的内容属于 7 种中的哪一种，然后读取 `references/extraction.md` 中对应方式的详细提取步骤。

如果是文字描述（方式 4），还要读取 `references/aesthetics.md` 查找关键词映射。

### Step 2 · 深度分析 & 提取 16 维度

**必须先读取 `references/style-analysis-metaprompt.md`**，按其中的 7 步分析法逐步提取：

1. 整体印象捕捉（情绪/重量/节奏）
2. 色彩系统深度分析（逐像素级 hex+rgb，不是"偏深""大概"）
3. 字体排版深度分析（衬线分类、Google Fonts 匹配、行高/字距）
4. 间距与密度分析（6 级间距 token）
5. 组件与细节分析（卡片/图片/装饰/分隔/WebGL）
6. 布局模式识别（CSS Grid/Flex 代码）
7. 明暗主题 & 节奏规划

每个维度必须给精确数值（hex/px/rem/vw），禁止模糊描述。标记可靠度：
- ✅ 直接提取 — 从源材料中明确获取
- ⚠️ 中等可靠 — 有依据但需确认
- ⚡ 推断 — 源材料无法提供，用合理默认值补全

`references/extraction.md` 提供各输入方式的具体策略作为补充参考。

### Step 3 · 展示分析 & 用户确认

按 `style-analysis-metaprompt.md` 中定义的报告格式输出完整 16 维度分析：

```
╔═══════════════════════════════════════╗
║ 风格名：{名称}                         ║
║ 来源：{方式}  气质：{3-5关键词}         ║
╠═══════════════════════════════════════╣
║ D1  配色  paper:#xxx → ink:#xxx    ✅  ║
║ D2  强调  accent:#xxx alt:#xxx     ✅  ║
║ D3  标题  {字族}·{衬线类型}·w{重}  ⚠️  ║
║ D4  正文  {字族}·mono:{等宽}       ✅  ║
║ D5  字重  hero:{} heading:{} ...   ⚡  ║
║ D6  字号  hero:{响应式值}          ⚡  ║
║ D7  间距  {密度级} slide-pad:{值}  ⚡  ║
║ D8  背景  {类型} {颜色} {透明度}   ✅  ║
║ D9  圆角  radius:{值} border:{值}  ✅  ║
║ D10 阴影  {级别}                   ✅  ║
║ D11 动效  {级别} {入场} {时长}     ⚡  ║
║ D12 图标  {库} {风格}              ⚡  ║
║ D13 图片  {滤镜} {圆角} {比例}     ✅  ║
║ D14 卡片  {类型} {hover}           ✅  ║
║ D15 装饰  {图案} {密度} {位置}     ✅  ║
║ D16 气质  {标签} 适合:{场景}       ✅  ║
╠═══════════════════════════════════════╣
║ ✅{N} 直接  ⚠️{N} 中等  ⚡{N} 推断   ║
╚═══════════════════════════════════════╝
```

随后输出完整 `:root` CSS 变量块和布局 CSS 代码（格式见 meta-prompt）。

用户可以修改任何维度。确认后进入生成。

### Step 4 · 生成风格 JSON

保存到 `styles/leishifu-{slug}.json`，16 维度完整数据。格式见 `references/dimensions.md` 底部的模板。

### Step 5 · 生成 HTML 模板

**完全基于 16 维度定义和 `style-analysis-metaprompt.md` 中的布局/CSS 代码全新构建。**

**模板骨架（横向翻页单文件 HTML）：**
- `<section class="slide">` 横向翻页骨架（flex + scroll-snap）
- 翻页 JS（键盘 ← →、滚轮、触屏、ESC 索引面板）
- 底部导航（页码 + 进度条）
- 所有 CSS 由 `:root` 变量驱动，变量值直接来自 16 维度定义

**CSS 全部由 16 维度驱动：**
- `:root` 变量 → D1~D2 颜色 + D6 字号 + D7 间距 + D9 圆角 + D10 阴影 + D11 动效
- 字体声明 → D3 标题字体（含衬线分类、CJK fallback）+ D4 正文 + D5 字重
- 排版规则 → 元提示词第三步定义的行高/字距/大小写/中文分档
- 图片样式 → D13 滤镜/圆角/比例/出血方式。**图片容器（`.img-art`、`.split-photo`、`.cover-right`）必须设 `min-height:0; min-width:0; overflow:hidden`，防止图片在 Grid/Flex 中撑破容器**
- 卡片样式 → D14 类型（outlined/filled/glass/elevated/none）
- 装饰图案 → D15
- 背景效果 → D8（fluid/grid-dots/particle/contour/solid）
- 布局模式 → 元提示词第六步识别的布局，直接使用其 CSS Grid/Flex 代码
- 明暗主题 → 元提示词第七步定义的节奏规则

保存到 `templates/template-leishifu-{slug}.html`

### Step 5.5 · AI 配图生成

为模板中的所有图片占位生成真实配图。

**前置检查：**
1. 读取 `config.json` → `image_api.enabled` 和 `api_key`
2. 若 API 不可用（key 为空或 enabled=false）→ 保持渐变色块占位，提示用户后续配置

**生成流程（API 可用时）：**

1. 读取 `references/image-prompts.md` 获取 prompt 模板和风格后缀映射
2. 扫描模板 HTML 中的图片位：
   - `.split-photo` / `.cover-right` / `.cover-photo` → 分屏配图
   - `.layout-cover-full` / `.layout-full-bleed` → 封面主视觉
   - 网格容器内的多图区域 → 网格多图
   - 声明页/引文页背景 → 装饰背景
3. 为每个图片位确定：
   - **类型**：5 种图片类型之一（封面/分屏/背景/内容/网格）
   - **尺寸**：**必须基于 1920×1080 视口精确计算容器的实际像素**，而不是使用通用比例。计算方法：
     - 读取 CSS Grid/Flex 的列宽百分比和行高（100vh = 1080px）
     - 如果是网格内多图，还要减去 gap 再除以行列数
     - 结果对齐到 16 的倍数（gpt-image-2 约束），直接传 `--size WxH`
     - 示例：`.layout-split-46` 右侧 60% = `1920×0.6=1152`，高 100vh=1080 → `--size 1152x1080`
   - **语义**：从页面 `data-title`、标题文本、正文内容提取
4. 拼装 prompt：
   - 类型模板 + 页面语义 + D16 风格后缀 + 标准/多图后缀
   - D1 配色倾向（暖/冷/黑白）影响色调描述
   - D13 滤镜信息留给 CSS 处理，prompt 生成满色原图
5. 逐张调用脚本（用精确计算的像素尺寸）：
   ```bash
   python scripts/generate_images.py \
     --prompt "<拼装好的prompt>" \
     --output "images/{slug}/p{页号}-{语义}.png" \
     --size "<精确像素WxH>"
   ```
6. 替换 HTML：将渐变占位 div 替换为 `<img>` 标签
   ```html
   <img src="images/{slug}/p{N}-{name}.png" class="img-art" alt="语义描述">
   ```
7. 若 D13 定义了滤镜（如 `grayscale(1)`），在 `<img>` 上添加对应 CSS filter

**降级模式（无 API）：**
保留原有渐变色块 + `<span class="meta-label">PHOTOGRAPH</span>` 占位，不影响模板其他功能。

### Step 6 · 预览验证

用模板生成 **5 页示例 deck**：
- P1 封面（hero 字体 + WebGL 背景）
- P2 数据页（卡片 + 强调色 + 数字）
- P3 图文页（图片处理 + 正文排版 + 装饰）
- P4 对比页（明暗切换）
- P5 收束页（整体氛围）

浏览器打开，对照 `references/checklist.md` 逐项验证。重点看：
- 对比度是否达标（WCAG AA）
- 字体是否加载成功
- WebGL 背景是否正常
- 整体气质是否符合预期

### Step 7 · 归档 & 更新索引

1. JSON → `styles/leishifu-{slug}.json`
2. HTML → `templates/template-leishifu-{slug}.html`
3. 更新 `styles/index.json`

---

## 风格库管理

| 用户说 | 操作 |
|--------|------|
| "看看风格库" | 读 `styles/index.json`，列出风格卡片 |
| "删掉 XX 风格" | 删 .json + .html，更新 index |
| "修改 XX 的配色" | 读 JSON → 改对应维度 → 重新生成模板 |
| "对比两个风格" | 并排展示 16 维度差异 |
| "导出 CSS 变量" | 输出完整 `:root` 变量块供外部使用 |

---

## 核心原则

1. **16 维度完整** — 提取不到的补默认值并标记，让用户知道
2. **用户确认优先** — 先展示分析，确认后才生成
3. **对比度安全** — 不生成不可读的配色（WCAG AA）
4. **全新构建模板** — 基于元提示词的分析结果独立构建，CSS 全部由 16 维度驱动
5. **CDN 字体** — Google Fonts 优先，不依赖本地字体
6. **归档到风格库** — 每次创建都更新 index.json
7. **风格名前缀** — slug 以 `leishifu-` 开头

---

## 参考文件

| 文件 | 何时读取 | 优先级 |
|------|---------|--------|
| `references/style-analysis-metaprompt.md` | **Step 2 必读** — 7 步深度分析法，像素级提取方法论 | 🔴 最高 |
| `references/dimensions.md` | 需要 16 维度的 JSON schema 和字段说明时 | 🟡 按需 |
| `references/extraction.md` | 各输入方式的具体策略（补充参考） | 🟡 按需 |
| `references/aesthetics.md` | 文字描述创建风格时（方式 4），查关键词映射 | 🟡 按需 |
| `references/checklist.md` | 生成完模板后，做验证自检时 | 🟠 必读 |
