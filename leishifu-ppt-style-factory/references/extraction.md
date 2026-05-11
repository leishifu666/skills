# 7 种提取策略 · 详细步骤

每种输入方式最终都要输出完整 16 维度。提取不到的用合理默认值补全，标记为"⚡推断"。

---

## 📸 方式 1：截图/图片提取

从静态图片中分析视觉特征。这是最直觉的方式，但也是推断最多的（动效、交互无法从图中获取）。

**逐维度提取路径：**

| 维度 | 提取方法 | 可靠度 |
|------|---------|--------|
| D1 配色 | 分析大面积背景色和文字色 | ✅ 高 |
| D2 强调色 | 识别按钮、高亮、图标的颜色 | ✅ 高 |
| D3 标题字体 | 判断衬线/非衬线/手写，匹配最接近的 Google Fonts | ⚠️ 中（无法精确识别字族） |
| D4 正文字体 | 同上，判断正文区域 | ⚠️ 中 |
| D5 字重 | 观察标题粗细对比 | ⚠️ 中 |
| D6 字号 | 估算标题与正文的大小比例 | ⚡ 推断 |
| D7 间距 | 判断留白密度（紧凑/标准/宽松） | ⚠️ 中 |
| D8 背景 | 识别是否有渐变、纹理、粒子效果 | ✅ 高 |
| D9 圆角边框 | 观察卡片和按钮的圆角 | ✅ 高 |
| D10 阴影 | 判断是否有投影和层次感 | ✅ 高 |
| D11 动效 | 无法从静态图提取 | ⚡ 推断（默认 standard） |
| D12 图标 | 识别图标风格（线性/填充） | ⚠️ 中 |
| D13 图片处理 | 观察图片是否有滤镜/圆角/蒙版 | ✅ 高 |
| D14 卡片 | 识别卡片样式（边框/填色/毛玻璃） | ✅ 高 |
| D15 装饰 | 识别是否有点阵/线条/几何装饰 | ✅ 高 |
| D16 气质 | 综合判断整体美学标签 | ✅ 高 |

**操作步骤：**
1. 仔细观察图片，记录第一印象的情绪关键词
2. 从大面积色块开始：背景色 → 文字色 → 强调色
3. 分析排版：字体类型 → 字重 → 间距感受
4. 分析细节：圆角 → 阴影 → 卡片 → 装饰
5. 列出 16 维度表，标注可靠度
6. 展示给用户确认

---

## 🧩 方式 2：HTML 代码提取

从 HTML/CSS 源码中精确解析。这是最准确的方式，大多数维度可以直接提取。

**解析优先级：**
1. `:root` 或 `html` 上的 CSS 变量 → D1, D2
2. `@import` / `<link>` 字体引用 → D3, D4
3. `font-weight` 声明（按选择器优先级排序）→ D5
4. `font-size` 包含 `clamp()` `min()` `vw` `vh` 的声明 → D6
5. `padding` `gap` `margin` 的主要值 → D7
6. `<canvas>` / WebGL / shader 相关代码 → D8
7. `border-radius` `border` 声明 → D9
8. `box-shadow` 声明 → D10
9. `transition` `animation` `@keyframes` → D11
10. 图标库引用（script src 中的 lucide/fontawesome 等）→ D12
11. `img` 相关的 `filter` `border-radius` `object-fit` → D13
12. `.card-*` 类名及其样式 → D14
13. SVG pattern / `::before` `::after` 背景装饰 → D15
14. 综合分析 → D16

---

## 🌐 方式 3：URL 网页提取

抓取页面后，走 HTML 提取的同一套流程。

**步骤：**
1. 用 WebFetch 获取页面内容
2. 提取 HTML 和内联 CSS
3. 按方式 2 的解析优先级逐项提取
4. 注意：外链 CSS 可能抓不到，对应维度标记为推断

---

## 💬 方式 4：文字描述创建

根据关键词匹配预设的美学体系（见 `aesthetics.md`），自动填充 16 维度。

**步骤：**
1. 解析用户描述中的关键词
2. 在 aesthetics.md 中查找匹配的美学体系
3. 用预设值填充 16 维度
4. 展示给用户，因为是全推断，每个维度都要让用户过目

---

## 🎨 方式 5：色板创建

用户给颜色值，自动补全其余维度。

**颜色角色分配：**
| 用户给了 | 分配策略 |
|---------|---------|
| 1 个色 | 作为 accent，根据明暗自动推算 ink/paper |
| 2 个色 | 深色→paper，浅色→ink，两色中间取 accent |
| 3 个色 | 按明暗排序分配到 ink/paper/accent |
| 4+ 个色 | ink/paper/accent/accent-alt/tint 依次分配 |

**补全逻辑：**
- paper-tint = paper 向 ink 方向偏移 10%
- ink-tint = ink 向 paper 方向偏移 60%
- 其余 14 维度根据色彩"温度"推断（暖色→衬线/人文，冷色→无衬线/科技）

---

## 🔀 方式 6：混搭已有风格

从风格库中选维度组合。

**步骤：**
1. 读取 `styles/index.json` 列出可用风格
2. 用户指定：X 的 D1-D2 + Y 的 D3-D5 + Z 的 D8...
3. 合并为新风格 JSON
4. 自动检查冲突：
   - 衬线标题 + cross-matrix 装饰 → 不协调，提示用户
   - 暗底 + 浅阴影 → 阴影不可见，自动调整
   - 圆角卡片 + 直角图片 → 风格不统一，提示用户
5. 让用户确认或修正

---

## 📄 方式 7：CSS/设计 Token 提取

从设计系统文件中映射到 16 维度。

**常见 Token 映射：**

| Token 名模式 | 映射维度 |
|-------------|---------|
| `--color-primary` / `--brand` / `--primary` | D2 accent |
| `--color-bg` / `--background` / `--surface` | D1 paper |
| `--color-text` / `--foreground` / `--on-surface` | D1 ink |
| `--color-secondary` / `--accent` | D2 accent-alt |
| `--font-heading` / `--font-display` / `--font-title` | D3 |
| `--font-body` / `--font-sans` / `--font-base` | D4 |
| `--font-mono` / `--font-code` | D4 mono |
| `--font-weight-*` | D5 |
| `--font-size-*` / `--text-*` | D6 |
| `--radius-*` / `--border-radius-*` | D9 |
| `--shadow-*` / `--elevation-*` | D10 |
| `--spacing-*` / `--space-*` | D7 |
| `--transition-*` / `--duration-*` | D11 |

**design-tokens.json 格式支持：**
- Style Dictionary 格式（`{ color: { primary: { value: "#xxx" } } }`）
- Figma Tokens 格式（`{ global: { colors: { ... } } }`）
- 扁平 key-value 格式（`{ "--color-primary": "#xxx" }`）
