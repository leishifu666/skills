# 黄金规则

通用原则。适用于**两大家族**模型(Nano Banana 与 GPT Image 2.5)。
模型专属细节见 [nano-banana.md](nano-banana.md)、[gpt-image.md](gpt-image.md)。

## 1. 以动词开头

告诉模型主要操作:"Create"(创建)、"Generate"(生成)、"Design"(设计)、"Transform"(转换)、"Convert"(转化)、"Edit"(编辑)。在细节之前先设定意图。

## 2. 正面表述

描述你**想要**什么,而不是你不想要的。模型对"存在"的理解优于对"不存在"的理解。

- ✅ "empty street" → ❌ "street with no cars"
- ✅ "clean background" → ❌ "no clutter"
- ✅ "solo portrait" → ❌ "no other people"

## 3. 改图,不要重新生成

图片完成度 80%?要求具体修改:
- "Change lighting to sunset"
- "Make text neon blue"
- "Move chart to right third"

## 4. 自然语言

❌ 差:"Cool car, neon, city, night, 8k"
✅ 好:"A cinematic wide shot of a futuristic sports car speeding through a rainy Tokyo street at night. Neon signs reflect off wet pavement and metallic chassis."

## 5. 具体化

| 要素 | 含糊 | 具体 |
|---------|-------|----------|
| 主体 | "a woman" | "sophisticated elderly woman in vintage Chanel-style suit" |
| 材质 | "shiny" | "brushed steel with matte finish" |
| 颜色 | "dark green" | "#0d3d2d deep emerald" |
| 位置 | "on the right" | "right third, bleeding off edge" |

## 6. 提供语境

语境帮助模型做出合乎逻辑的决策:
- "for Brazilian gourmet cookbook" → 推断专业摆盘、浅景深
- "for executive strategy presentation" → 推断企业美学
- "for children's educational app" → 推断友好、色彩丰富

## 7. 精确引用文本

任何需要渲染的文本都要加引号:
- "[HEADLINE TEXT]"
- 标签:"[Revenue Growth]"、"[Net Income]"
- 指定字重:bold(加粗)、thin(细体)、extra bold(特粗)
- 指定位置:"upper third"(上三分之一)、"centered"(居中)

## 提示词模板

```
Create a [TYPE] for [CONTEXT].

Background: [Description with hex colors]. [Atmospheric effects].

[HERO ELEMENT]:
[Detailed description - position, lighting, angle]

Typography:
Line 1: "[TEXT]" in [weight], [color], [size], [position]
Line 2: "[TEXT]" in [weight], [color], [size], [position]

[ADDITIONAL ELEMENTS]

Mood: [Emotional descriptor]
Format: [ASPECT RATIO]
```

> **思考模式** (仅 NB)、**`quality: low/medium/high/xhigh/max`** (仅 GPT Image 2.5) — 见对应 references。

## 成本优化(批量工作)

- **Nano Banana:** 先用 `0.5K` Flash 跑一批变体 → 精选 → 在 `2K`/`4K` 重生成优胜者。
- **GPT Image 2.5:** 先用 `quality: low` 跑 → 精选 → 在 `medium` 或 `high` 重生成。

两种情况都是:廉价侦察 → 昂贵定稿。

## 对话式微调

生成之后:
- "Change the headline color to #3b82f6"
- "Add subtle drop shadow to text"
- "Increase contrast, make it more dramatic"
- "Soften the background, add blur"

## 参考图

多图输入:**NB 最多 14 张**,**GPT Image 2.5 最多 16 张**。为每张图标注角色。

用于:

**嵌入已有设计:**
```
[Attach design/layout image]
Create content following this exact layout and style.
Replace [ELEMENT] with [NEW CONTENT].
Keep colors, typography, composition.
```

**面部/角色作为参考:**
```
[Attach portrait]
Use this person's face. Keep features exactly the same.
Change: [expression/pose/setting]
```

**产品/物体作为参考:**
```
[Attach product photo]
Place this product in [NEW CONTEXT].
Match lighting and perspective.
```

**风格作为参考:**
```
[Attach style reference]
Create [NEW CONTENT] in this exact visual style.
Match colors, textures, mood.
```

**多张参考图同时使用:**
```
[Attach Image 1 - face]
[Attach Image 2 - outfit]
[Attach Image 3 - background]
Combine: face from Image 1, outfit style from Image 2, setting from Image 3.
```

## 世界知识锚点

GPT Image 2.5 对文化、时代和视觉风格有深厚知识。与其描述每一个细节——不如给模型一个文化/时代/类型锚点,它会自动填充地道细节。

### 三种锚点类型

**时代锚点** — 时间与地理标记,唤起一整片视觉世界:
- "Bethel, NY, August 1969" → 无需描述扎染、泥泞、场景即可获得 Woodstock 美学
- "Berlin, November 1989" → 推倒柏林墙、人群、涂鸦、狂喜
- "Tokyo, 1982" → 霓虹新宿、模拟电子设备、早期赛博朋克

**文化锚点** — 把一个文化对象的视觉语言迁移到另一个语境:
- "{game_title} in {real_city}" → 自动把游戏视觉风格套用到真实地点(GTA style、Persona style 等)
- "Soviet constructivism poster about {modern_topic}" → 用罗德琴科/李西茨基风格呈现现代主题
- "Ukiyo-e print of {modern_scene}" → 浮世绘版画呈现现代内容

**类型锚点** — 导演/摄影师/流派作为镜头:
- "Peter Lindbergh influence" → 强力黑白、极少修图、raw editorial
- "Wes Anderson palette" → 对称构图、粉彩调色板、居中构图
- "Studio Ghibli mood" → 柔和水彩天空、绿色枝叶、温暖怀旧的光线
- "Roger Deakins lighting" → 自然光、深邃阴影、电影感体积

### 使用规则

1. **当作 HIGH-LEVEL 方向** — 锚点设定情绪与美学,而不是替代整个提示词
2. **与具体视觉细节组合** — 锚点建立世界,细节建立特定性
3. **不要堆叠多个 type 锚点** — 只选一个。"Peter Lindbergh + Wes Anderson" = 混乱
4. **时代/文化锚点在 GPT Image 2.5 上效果更好**(world knowledge)。Nano Banana 上的结果较不可预测——NB 更依赖显式描述

### 示例

**时代锚点 + 具体细节:**
```
Create an editorial portrait set in Havana, 1957.

Subject: jazz musician leaning against pastel-colored colonial building,
holding trumpet loosely at his side. Linen suit, open collar.
Lighting: harsh Caribbean afternoon sun, deep shadows under awning.
Format: 3:4
```
> "Havana, 1957" 唤起:背景中的老式美国车、斑驳灰泥、铁艺阳台、热带气息——无需逐一描述。

**文化锚点 + 新语境:**
```
Create a scene of a quiet Kyoto temple garden, rendered in the visual style
of Studio Ghibli. Morning mist over moss-covered stones, a single monk
sweeping fallen maple leaves. Soft watercolor textures, warm nostalgic palette.
Format: 16:9
```
> "Studio Ghibli" 设定水彩感、温暖、怀旧。细节(苔藓、枫叶、僧人)设定具体场景。

**类型锚点 + 具体化:**
```
Create a fashion editorial portrait with Peter Lindbergh influence.

Subject: model in oversized men's blazer, no makeup, wind-tousled hair.
Setting: empty winter beach, overcast sky.
Mood: raw, unpolished beauty
Format: 2:3
```
> "Peter Lindbergh influence" 带来:强力黑白(或低饱和)、无修图、raw emotional quality。细节(海滩、西装外套、风)使画面具体化。

---

*作者: Serge Shima ([t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)) · 许可: CC BY 4.0 — 需署名 · 来源: [smixs/visual-skills](https://github.com/smixs/visual-skills)*
