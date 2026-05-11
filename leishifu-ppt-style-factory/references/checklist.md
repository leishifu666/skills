# 风格验证清单

生成风格后、交付用户前，逐项检查。

---

## 对比度安全（WCAG AA）

这是最硬的底线——不可读的配色没有任何美学价值。

| 检查项 | 标准 |
|--------|------|
| 正文 vs 背景 (ink vs paper) | ≥ 4.5:1 |
| 大标题 vs 背景 (ink vs paper) | ≥ 3:1 |
| 强调色 vs 背景 (accent vs paper) | ≥ 3:1 |
| 卡片内文字 vs 卡片背景 | ≥ 4.5:1 |
| dark 主题下的正文 vs 暗底 | ≥ 4.5:1 |
| light 主题下的正文 vs 亮底 | ≥ 4.5:1 |

不满足时主动调整颜色（通常加深或提亮 ink），告知用户改了什么。

---

## 字体检查

| 检查项 | 如何验证 |
|--------|---------|
| Google Fonts URL 可访问 | 浏览器打开 import URL 不 404 |
| 中文字体指定了 CJK 字族 | headingImport/bodyImport 包含 Noto Serif SC / Noto Sans SC 等 |
| 字体 fallback 链合理 | 最后有 serif / sans-serif / monospace 通用族 |
| 标题和正文字体有区分度 | 不能标题正文完全相同（除非极简风刻意为之） |

---

## 风格 JSON 完整性

| 检查项 | |
|--------|--|
| 16 个维度字段全部存在 | d01 到 d16 |
| name 以 "leishifu-" 开头 | |
| createdAt 日期格式正确 | YYYY-MM-DD |
| source.type 是 7 种之一 | screenshot/html/url/text/palette/remix/tokens |
| rgb 字段是纯数字格式 | "224,224,224" 不是 "rgb(224,224,224)" |

---

## 模板 HTML 检查

| 检查项 | |
|--------|--|
| `<title>` 不包含 [必填] 占位符 | |
| `:root` 变量与风格 JSON 一致 | |
| `@import` 字体 URL 与 JSON 一致 | |
| 横向翻页 JS 正常工作 | 键盘 ← →、滚轮、触屏 |
| WebGL canvas 正常渲染 | 背景效果可见（如果 enabled=true）|
| 四种主题变体都有定义 | .light / .dark / .hero.light / .hero.dark |
| 导航组件正常显示 | 底部页码/进度条 |

---

## 视觉节奏（用于示例 deck）

| 检查项 | |
|--------|--|
| 不连续 3 页同明暗主题 | light/dark 交替 |
| hero 页每 3-4 页出现一次 | |
| 封面和收束页气质统一 | |
| 图片不碰底部导航区域 | |

---

## index.json 更新

| 检查项 | |
|--------|--|
| 新风格已添加到 styles 数组 | |
| files.definition 路径正确 | |
| files.template 路径正确 | |
| tags 和 category 已填写 | |
