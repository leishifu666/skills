# AI 配图 Prompt 模板

用于 `scripts/generate_images.py` 调用 gpt-image-2 为 PPT 模板生成配图。先判断页面布局和图片落位，再选类型，最后拼接风格后缀。

## 通用规则

- 图片必须匹配当前风格的 D16 视觉气质（如"编辑/黑白"→ 纪实摄影风；"画廊/超现实"→ 艺术拼贴风）
- 图片要给标题或正文留出可叠加空间，不要满屏堆细节
- 同一 deck 内的所有配图必须使用统一的视觉缩放、边距密度、色调倾向
- 配图是嵌入 PPT 的素材，不是一张独立 slide：**不要**生成页眉、页脚、页码、标题栏、角标、署名、装饰边框或 slide chrome
- 命名规则：`{slug}/p{页号}-{语义}.png`，如 `surreal-gallery/p1-cover.png`

## 比例选择

根据页面布局选择图片尺寸（必须是 16 的倍数，最大边 3840px，宽高比 ≤ 3:1）：

| 页面布局 | 推荐尺寸 | 说明 |
|---------|---------|------|
| 全屏封面 / hero 背景 | 1920×1080 (16:9) | `.layout-cover-full` / `.layout-full-bleed` |
| 分屏图文 (50:50 / 60:40) | 960×1080 (8:9) 或 1152×1080 | `.layout-split` / `.split-photo` |
| 分屏图文 (40:60) | 768×1080 | `.layout-split-46` |
| 三栏网格 | 640×480 (4:3) | `.layout-3col` 内的图 |
| 2×2 网格 | 960×540 (16:9) | 多图网格，统一尺寸 |
| 声明页暗调背景 | 1920×1080 (16:9) | 暗调纹理或抽象背景 |

## Prompt 后缀模板

**每张图的 prompt 末尾必须追加约束后缀：**

### 标准后缀（单张图）
```
输出必须是横向构图，主体居中但保留边距，画面密度中等。只保留核心图形/画面本身，不要生成页眉、页脚、标题、页码、角标、署名、装饰边框、水印、超长条、竖图或不规则比例。
```

### 多图组后缀（同页多张图）
```
这是一组图片中的一张，请保持与同组图片相同的画面比例、元素大小、边距、色调和密度。输出必须是横向构图，主体居中但保留边距。不要生成页眉、页脚、标题、页码、角标、署名、装饰边框或水印。
```

## 风格后缀映射

根据 D16 视觉气质自动拼接到 prompt 末尾（在标准后缀之前）：

| D16 气质关键词 | 风格后缀 |
|--------------|---------|
| 编辑、黑白、杂志、纪实 | `Black and white editorial photography, high contrast, film grain, Fujifilm/Leica documentary style, natural lighting, restrained and humanistic.` |
| 画廊、超现实、艺术 | `Surrealist art composition, gallery exhibition quality, dreamlike atmosphere, rich color palette, artistic collage elements.` |
| 暗色、科技、专业 | `Dark tech aesthetic, subtle ambient glow, minimal composition, deep shadows, professional and sleek.` |
| 日式、侘寂、极简 | `Wabi-sabi aesthetic, muted earth tones, natural textures, imperfect beauty, zen minimalism, negative space.` |
| 赛博朋克、霓虹 | `Cyberpunk neon aesthetic, vibrant purple and cyan, rain-soaked streets, holographic elements, high contrast.` |
| 包豪斯、几何 | `Bauhaus geometric composition, primary colors, clean shapes, modernist design, grid-based layout.` |
| 波普、孟菲斯 | `Memphis design / Pop art style, bold colors, playful geometric patterns, energetic and expressive.` |
| 自然、有机 | `Organic natural photography, warm earth tones, soft natural lighting, botanical elements, calm and grounded.` |

如果 D16 标签不在上表中，根据标签语义自由组合风格描述。

## 5 种图片类型

### 类型 1：封面主视觉

用于 P1 封面页，需要留出标题叠加空间。

**Prompt 模板：**
```
生成一张横向主视觉配图，主题是：[页面主题]。
风格：[风格后缀]
构图要求：主体偏[左/右/中]，[上/下]方留出大面积空间供标题叠加。
画面氛围：[根据D16气质描述]，有冲击力但不抢文字。
[标准后缀]
```

### 类型 2：图文分屏配图

用于 `.split-photo` 区域，占页面 40%-60% 宽度。

**Prompt 模板：**
```
生成一张[竖向/横向]配图，主题是：[页面内容]。
风格：[风格后缀]
构图要求：主体可偏一侧，画面有纵深感，适合窄长容器。
色调：与整体deck的[D1配色描述]协调。
[标准后缀]
```

### 类型 3：数据页/声明页装饰背景

用于暗色声明页或数据页的背景图，不应抢注意力。

**Prompt 模板：**
```
生成一张抽象装饰背景图，氛围是：[页面情绪]。
风格：[风格后缀]
要求：低饱和度，暗调，纹理感，适合作为文字底层背景。
主体模糊或抽象化，不要有具体可辨识的物体抢夺注意力。
[标准后缀]
```

### 类型 4：内容相关实拍/艺术图

用于图文页中直接展示主题相关的照片或艺术品。

**Prompt 模板：**
```
生成一张与[具体主题]直接相关的[摄影/艺术/插画]配图。
风格：[风格后缀]
内容：[具体描述画面中应出现的元素]
色调：[根据D1/D2的配色倾向]
[标准后缀]
```

### 类型 5：网格多图（统一系列）

用于多图网格页，一组 2-4 张统一风格的图。

**Prompt 模板：**
```
生成一张系列配图（共[N]张中的第[M]张），主题是：[系列主题]。
本张聚焦：[本张具体内容]。
风格：[风格后缀]
要求：与同组其他图保持统一的色调、构图密度、边距和视觉缩放。
[多图组后缀]
```

## Claude 自动生成 Prompt 的流程

当 Step 5.5 触发时，Claude 按以下流程为每个图片位生成 prompt：

1. **识别图片位**：扫描模板 HTML 中的 `.split-photo` / `.cover-right` / `.cover-photo` / 网格容器等
2. **确定类型**：根据所在页面布局匹配上方 5 种类型
3. **确定尺寸**：根据比例选择表选择尺寸
4. **读取上下文**：
   - 页面标题（`data-title`）
   - 页面内的文字内容（`.h-hero` / `.h-xl` / `.body-text`）
   - 风格 JSON 的 D16 气质标签
   - D1 配色（暖/冷/黑白）
   - D13 图片处理（是否 grayscale、滤镜）
5. **拼装 prompt**：类型模板 + 页面语义 + 风格后缀 + 标准后缀
6. **调用脚本**：`python scripts/generate_images.py --prompt "..." --output "images/{slug}/p{N}-{name}.png" --size "WxH"`
7. **替换 HTML**：将占位 div 替换为 `<img src="images/{slug}/p{N}-{name}.png" class="img-art">`

## D13 图片后处理

生成的图片是原始满色图。如果风格定义了 D13 滤镜：
- `grayscale(1)` → CSS `filter: grayscale(1)` 在 `<img>` 上应用（不需要生成黑白图）
- `contrast(1.05)` → CSS `filter: contrast(1.05)`
- 其他滤镜同理

这样保留了原图色彩信息，用户可以随时通过修改 CSS 切换滤镜。
