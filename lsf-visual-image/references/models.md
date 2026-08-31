# 模型选择 — Nano Banana vs GPT Image 2

本技能为两大家族模型编写提示词。它们思考方式不同——模型选择会改变提示词结构。

## TL;DR

| 任务 | 模型 |
|--------|--------|
| 真实地点/物体(带图像接地) | **Nano Banana** (NB2/NBP) |
| 涉及物理/构图的复杂场景 | **Nano Banana Pro** |
| 超长横向/纵向格式 (1:8、8:1、4:1) | **Nano Banana** (仅 NB 支持极限比例) |
| 低成本批量生成 | **Nano Banana 2 Lite** 或 **gpt-image-1-mini** |
| 精细排版/UI 的写实风格 | **GPT Image 2** |
| 带保留要求的精确编辑 (try-on、换装、天气) | **GPT Image 2** (编辑时 identity-preservation 最佳) |
| 画面中的小号密集文字 | **GPT Image 2** (`quality: high`) |
| 品牌印刷品 / 需 EXACT TEXT 的海报 | **GPT Image 2** |
| 分镜、漫画(序列) | **Nano Banana** (extreme ratios + thinking) |
| 以排版为重点的分镜 | **GPT Image 2** |
| 不提参考图的风格迁移 | **GPT Image 2** (concrete visual targets) |
| 14+ 张参考图的渲染 | **Nano Banana Pro** (至 14)或 **GPT Image 2** (至 16) |

## 各自胜出的场景

### Nano Banana 胜出
- **图像接地 (Image grounding)。** NB2 生成前会在互联网上查找真实图像——特定寺庙、桥梁、广场的精确建筑;特定动物、植物品种。GPT Image 2 不做这个。
- **极限比例。** 1:8、8:1、1:4、4:1 — 横幅、长页、漫画条。GPT Image 2 最多 3:1。
- **「思考」模式。** 需要空间逻辑的复杂信息图。
- **价格/速度。** NB2 = $0.04/img。

### GPT Image 2 胜出
- **编辑时的身份保持。** 换衣服 / 天气 / 背景 — 面部、姿态、几何不漂移。双栏逻辑 (change / preserve) 像合同一样可靠。
- **画面中的精细文字。** 小字号标注、图例、footnotes、多字体排版。`quality: high` 下渲染更清晰。
- **UI 模型与产品截图。** 层级、真实界面元素、可读标签。
- **结构化的 5 段式提示词。** Scene/Subject/Details/Use case/Constraints 的清晰划分带来可预测性。
- **`quality` 杠杆。** low/medium/high — 对速度与精度的清醒权衡。

### 两者同样擅长的场景
- 写实人像。
- 中性背景的产品拍摄。
- 极简海报。
- 编辑类摄影。

## 提示词语法差异

| 方面 | Nano Banana | GPT Image 2 |
|--------|-------------|-------------|
| 提示词风格 | 自然语言,1-2 段 | 带小节标签的 5 段式 |
| 相机/镜头 | **不要指定**数字 (50mm、f/2.8) — NB 会忽略 | 可用「50mm feel」,但作为 high-level look |
| 「Stunning/epic/masterpiece」 | 忽略,不有害 | **Anti-slop**:有害,使结果变差 |
| 图内文字 | `"..."` 加引号,font + position | `"..."` 或 ALL CAPS +「no extra words / no duplicate text」 |
| 负面表述 | 使用正面表述 | 正面表述 + 显式 preserve list |
| 复杂场景 | 5+ 元素用 JSON | 分段落的 5-slot template |
| 编辑 |「Keep X same, change Y」 |「Change: X / Preserve: Y / Constraints: Z」— 每轮重复 preserve |
| 多参考图 | 至 14 张,编号 | 至 16 张,按角色编号(「Image 1: base」、「Image 2: jacket reference」) |

## 成本(参照价)

| 模型 | 价格 | 说明 |
|--------|------|---------|
| Nano Banana 2 Lite | ~$0.034/img | 仅 1K,约 4 秒。草稿与批量任务 |
| Nano Banana 2 (Flash) | ~$0.04/img | 大多数任务的默认选择 |
| Nano Banana Pro | ~$0.15/img | 复杂场景,至多 14 张参考图 |
| GPT Image 2 (`low`) | 便宜 | 延迟敏感、预览 |
| GPT Image 2 (`medium`) | 中等 | GPT Image 默认 |
| GPT Image 2 (`high`) | 较贵 | 小字、品牌敏感、写实 |
| gpt-image-1-mini | 便宜 | 高量探索性生成 |

> 本技能不自己启动生成 — 只产出提示词。模型/quality 作为元数据伴随提示词给出。

---

*作者: Serge Shima ([t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)) · 许可: CC BY 4.0 — 需署名 · 来源: [smixs/visual-skills](https://github.com/smixs/visual-skills)*
