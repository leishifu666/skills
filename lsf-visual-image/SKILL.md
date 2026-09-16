---
name: lsf-visual-image
title: LSF AI 图像导演
description: "为指定图像模型编写生成或编辑提示词，涵盖角色、产品、海报与参考图一致性；用于提示词交付。"
license: CC-BY-4.0 (attribution required — Serge Shima, github.com/smixs/visual-skills)
github_url: https://github.com/smixs/visual-skills
github_hash: ae26d624edd747e719fa21528d18d39e68c04a0e
upstream_path: image
version: 1.0.0-lsf.2
localization: zh-CN
---

# 图像提示词 — Nano Banana 与 GPT Image 2.5

本技能负责编写图像提示词,不生成图像。输出内容为:模型名 + 质量 / 尺寸 / 宽高比 + 提示词本身。

SKILL.md 正文有意保持精简,避免仅靠阅读正文就能冒充成果。真正的规则——模型奖励什么、惩罚什么、如何组织 5 段式模板、何时加 `quality: high`、何时使用图像接地——只存在于 reference 文件中。

## 先分流——这真的是图像提示词任务吗?

- **动态影像、短片、蒙太奇**(Seedance、Kling、Veo 及任意图生视频):使用同级技能 `lsf-visual-video`。本技能输出的分镜与关键帧可供其使用。
- **还没有想法或脚本**(用户想要的是概念或广告脚本,而非一张图):若已安装 `creative-director` 技能,从它开始——它负责为广告等场景孵化创意与脚本([github.com/smixs/creative-director-skill](https://github.com/smixs/creative-director-skill))。
- **需要一张具体图像**——本技能,继续往下。

---

# 强制阅读顺序 — 不读完不许写提示词

此前直接依据本技能正文写提示词的尝试,产出了偷懒、同质化的结果。每个模型有自己的"物理规则";脱离模型专属语法套用通用规则,最终会稀释成一团浆糊。产出任何提示词前,请按以下顺序阅读:

### 第 1 步 — 永远先读 → [models.md](references/models.md)

决定:Nano Banana (NB2 或 NBP) 还是 GPT Image 2.5。这一选择从根本上改变提示词语法——自然语言段落 vs. 带标签的 5 段式模板、质量设置、可用功能(图像接地仅 NB 支持,EXACT TEXT 纪律仅 GPT Image 有,等等)。

如果用户指定了模型——确认后继续。如果没有——用 `models.md` 中的表格选定,然后在输出头部注明你的选择。

### 第 2 步 — 阅读**一个**模型文件(你选中的那个)

- **Nano Banana** → [nano-banana.md](references/nano-banana.md)
  真实场景的图像接地。极限宽高比 (1:8、8:1、4:1)。思考模式。5+ 元素用 JSON。最多 14 张参考图。为什么绝对不能写 `50mm / f-stop / ISO` 数字。

- **GPT Image 2.5** → [gpt-image.md](references/gpt-image.md)
  5 段式模板(场景 Scene / 主体 Subject / 重要细节 Important Details / 用途 Use Case / 约束 Constraints)。anti-slop 禁用词清单。把 `quality: low / medium / high / xhigh / max` 当作刻意的保真度杠杆。尺寸约束(16 的倍数、最大 3:1、最高 3840×2160)。双栏编辑逻辑(修改 Change / 保留 Preserve / 约束 Constraints)。最多 16 张参考图且需明确角色。

模型文件不可跳过。跳过它是提示词孱弱的头号原因。

### 第 3 步 — 读完模型文件后永远接着读 → [golden-rules.md](references/golden-rules.md)

适用于两种模型的通用规则:以动词开头、正面表述、hex 颜色、文本加引号、改图不要重roll、一次只改一处、参考图。

### 第 4 步 — 按任务类型阅读(只加载与请求匹配的内容)

根据用户要求,选择零个或多个:

- 图内文字、信息图、图表、多语言渲染 → [text-rendering.md](references/text-rendering.md)
- 编辑已有图片(移除物体、换光、上色、修复、本地化) → [editing.md](references/editing.md)
- 多图/多面板间的角色一致性 → [characters.md](references/characters.md)
- **从零设计角色视觉身份**(人类、宠物、植物、虚构生物、随机角色、避免 AI 脸) → [character-identity-design.md](references/character-identity-design.md)。先生成身份档案与锁定锚点,再读取角色设定图模板;不要直接跳到画面提示词。
- 演示幻灯片 → [slides.md](references/slides.md)
- 顺序叙事(分镜、漫画、面板序列) → [storyboards.md](references/storyboards.md)
- 草图 → 成品、线框图、结构输入 → [structural.md](references/structural.md)
- 2D → 3D、户型图、等距风格 → [dimensional.md](references/dimensional.md)
- **视觉分析 / 图像转提示词 / 参考图风格迁移** → [vision-decomposer.md](references/vision-decomposer.md)。只要用户附图并要求重现、匹配、拆解或迁移其风格,就加载此文件。
- **多面板构图**(网格、拼贴、单图内的分镜表) → [multi-panel.md](references/multi-panel.md)。9 宫格 TVC 分镜、2x2 人像网格、3 面板 campaign 拼贴、4x3 无边框网格、6 帧电影序列、前后对比分割、12 面板分镜海报。
- **行业模式库** — 按垂直行业验证过的提示词模板,加载匹配的文件:
  - 电商产品拍摄 → [patterns/ecommerce.md](references/patterns/ecommerce.md)
  - 时尚编辑大片 → [patterns/fashion-editorial.md](references/patterns/fashion-editorial.md)
  - 食品与饮料广告 → [patterns/food-beverage.md](references/patterns/food-beverage.md)
  - 电影感人像 → [patterns/portrait-cinema.md](references/patterns/portrait-cinema.md)
  - 海报与插画 → [patterns/poster-illustration.md](references/patterns/poster-illustration.md)
  - 角色设定图(三视图、表情表、服装网格) → [patterns/character-design.md](references/patterns/character-design.md)。若角色尚未定型,先读 `character-identity-design.md`。
  - UI 模型与社媒格式 → [patterns/ui-social.md](references/patterns/ui-social.md)

### 第 5 步 — 生产级语言 → [creative-direction.md](references/creative-direction.md)

灯光设计、相机与硬件、调色与胶片、材质与质感的影棚级词汇。需要超出 `golden-rules.md` 范围的精确术语时阅读。

### 第 6 步 — 组织复杂提示词时阅读 → [prompt-framework.md](references/prompt-framework.md)

通用元素清单(主体、语境、动作、环境、相机、灯光、情绪、材质、调色板、格式)、细节模式(简洁 / 标准 / 详细 / 电影级详细)、参数化模板、含参数与排除项的输出结构。

---

# 输出格式

返回提示词时,按此结构组织:

```
Model: <nano-banana-2 | nano-banana-pro | gpt-image-2.5-flare | gpt-image-2.5-sunburst>
Quality: <low | medium | high | xhigh | max>          (only for gpt-image-2.5-flare)
Size / Ratio: <e.g. 1536×1024 or 16:9>

Prompt:
<the prompt text, ready to copy>

Notes:
- <anything you inferred or assumed because the user did not specify>
```

编辑类任务还需附上显式的保留清单(gpt-image-2.5-flare 必填,nano-banana 推荐):

```
Change: <one concrete thing>
Preserve: <face, pose, lighting, framing, geometry, ...>
Constraints: <no extra objects, no drift, ...>
```

---

# 最终回复风格

推荐:可直接复制的提示词、hex 颜色、具体材质、具名构图、模型专属语法(GPT Image 用 5 段式,Nano Banana 用自然行文)。

避免:标签堆砌("cool, modern, 4k")、空洞夸奖("stunning, epic, masterpiece" — 会实际损害 GPT Image 2.5 的效果)、负面表述("no people, no cars" — 要反转成正面)、外部类比("like Apple ad" — 改为描述视觉属性)、Nano Banana 提示词中的数字镜头参数(它会忽略)。

---

*作者: Serge Shima ([t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)) · 许可: CC BY 4.0 — 需署名 · 来源: [smixs/visual-skills](https://github.com/smixs/visual-skills)*
