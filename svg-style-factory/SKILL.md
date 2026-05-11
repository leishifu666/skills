---
name: svg-style-factory
description: >
  强大的 SVG 设计工厂。两种模式：
  1. 通过图片提取风格并保存为 XML (Image-to-Style)。
  2. 从风格库中选择风格并生成 SVG (Library-Selection)。
  支持生成可导入 Figma 的矢量文件。
entry_point: none (Agent-driven)
---

# SVG 风格工厂 (SVG Style Factory)

这是一个 Agent 驱动的高级设计技能，能够将视觉风格“数字化”为 XML，并复用该风格生成高质量 SVG 设计稿。

## 🎯 核心能力

1.  **👁️ 风格提取 (Extract)**: 像设计师一样通过“看图”分析配色、排版、间距和组件风格，并沉淀为结构化数据。
2.  **🎨 矢量生成 (Generate)**: 基于风格数据，自动设计并编写 SVG 代码，支持任意尺寸（16:9, 9:16, A4...）。
3.  **📚 风格库管理 (Library)**: 建立个人的设计资产库，随时通过名称调用。

## 🚀 使用流程

### 模式一：图片提取与生成 (Image-to-Style)

**当用户发送一张图片，并说“提取这个风格”或“用这个风格做个海报”时：**

1.  **读取指令**: 读取 `prompts/style_extractor.md` 中的系统提示词。
2.  **视觉分析**: 将**用户发送的图片**与**提示词**结合，进行多模态分析。
3.  **生成 XML**: 输出包含 `<StylePrompt>` 的完整 XML。
4.  **保存风格**: 
    - 询问用户：“这个风格叫什么名字？”（如果用户没说）。
    - 将 XML 内容保存到文件：`styles/[风格名].xml`。
    - **更新索引**: 读取 `styles/index.json`, 将新风格的 metadata (id, name, description) 追加到列表中并写回文件。
5.  **后续生成 (可选)**: 如果用户不仅是想提取，还想立即生成（例如“提取这个风格并做一个双十一海报”），则继续进入**步骤 4（调用 SVG 生成器）**。

### 模式二：库风格选择 (Library Selection)

**当用户直接说“我要生成一个 SVG”或“帮我设计个 PPT 封面”，但没有提供图片时：**

1.  **读取索引**: 
    - 读取 `styles/index.json` 文件以获取可用风格列表。
    - **注意**: 不要直接扫描 `styles/` 目录，以节省 Context Window。
    - 向用户展示风格名称和描述，供其选择。
2.  **用户选择**: 等待用户指定一个风格（例如 `acid-cyberpunk`, `minimalist-tech`）。
3.  **确认需求**:
    - **主题/文案**: 用户想做什么？（例如“关于 AI 的研报”）。
    - **比例 (Ratio)**: 16:9 (PPT/Web), 9:16 (手机海报), 1:1 (Ins) 等。
4.  **生成 SVG**:
    - 读取选中的风格文件：`styles/[选定风格].xml`。
    - 读取生成指令：`prompts/svg_generator.md`。
    - 结合 **XML + 生成指令 + 用户主题 + 比例**，调用模型生成 SVG 代码。
5.  **交付**: 将生成的 SVG 代码保存为 `.svg` 文件，并告知用户可直接拖入 Figma。

## 📂 文件结构

```
svg-style-factory/
├── prompts/
│   ├── style_extractor.md  # 风格分析师提示词
│   └── svg_generator.md    # SVG 编码师提示词
├── styles/
│   ├── acid-cyberpunk.xml  # [示例] 酸性赛博风格
│   ├── corporate-blue.xml  # [示例] 商务蓝风格
│   └── ...                 # 你的风格库
└── SKILL.md                # 本文件
```

## 💡 最佳实践

- **提取时**: 给出的参考图越清晰、典型，生成的 XML 质量越高。
- **生成时**: 如果生成的 SVG 版式错乱，可以尝试让 Agent “检查 XML 中的 `<layout-patterns>` 是否适合当前比例”，并在生成指令中强调使用该 Pattern。
- **关于 Figma**: 生成的 SVG 尽量使用标准标签，导入 Figma 后通常是可编辑的 Group 或 Frame。可以建议用户使用 "Ungroup" 进行深度编辑。
