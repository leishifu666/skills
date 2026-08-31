# 文字渲染与信息图

通用风格、布局类型、示例。两种模型都适用,但渲染细节有差异:

- **Nano Banana:** 100+ 语言的 SOTA,单帧多语言,可点名具体字体(「Century Gothic 12px」、「Brush Script」)。见 [nano-banana.md](nano-banana.md)。
- **GPT Image 2:** EXACT TEXT 用 `"..."` 或 ALL CAPS,加「no extra words / no duplicate text」,小字用 `quality: high`。见 [gpt-image.md](gpt-image.md)。

## 提示词结构

```
Create an educational infographic about [TOPIC].
Target Audience: [GRADE/LEVEL]
Content: [SPECIFIC FACTS/SEQUENCE]
Title: "[TITLE TEXT]"
Visual Style: [STYLE]
Layout: [LAYOUT TYPE]
Format: [ASPECT RATIO]
```

## 视觉风格

**教育/亲和:**
- 剪纸贴画: 手工纸拼贴外观
- 黏土动画: 3D 触感,Wallace & Gromit 风格
- 卡哇伊/可爱矢量: 圆角、粉彩色
- 绘本水彩: 柔和手绘质感
- 黑板画: 绿/黑板上白色粉笔
- 像素画 (8-Bit): 复古游戏怀旧

**技术/专业:**
- 等距 3D: 游戏地图风格、流程
- 蓝图/示意图: 蓝图上的白线
- 达芬奇手稿: 文艺复兴素描、科学感
- UI/UX 线框图: 应用蓝图风格
- 仪表盘: 带数字的分析界面

**风格化:**
- 赛博朋克/霓虹: 暗色 + 亮霓虹点缀
- 图像小说/漫画: 粗轮廓、平涂色
- 复古科学海报: 柔和、泛黄纸张、细线
- 波普艺术 (安迪·沃霍尔): 高对比、粗犷、网点
- 企业孟菲斯/扁平插画: 科技公司风格

**专门:**
- 地铁/交通图: 旅程、换乘
- 宜家说明书: 无字分步
- Knolling (平铺俯拍): 物体呈 90° 角、俯视
- 折纸: 几何、干净

## 布局类型

**线性:**
- 横向时间轴: 历史、传记
- 分步流程: 菜谱、实验、流程
- 蜿蜒路线图: 穿越主题的旅程

**对比:**
- 分屏 (对比): 即时反差
- 对比矩阵: 多项目、同一标准
- 前后对比: 因果
- 韦恩图: 比较异同

**层级:**
- 金字塔: 从基础到顶端 (马斯洛、食物金字塔)
- 漏斗: 筛选过程 (法案→法律、销售)
- 冰山: 可见 vs 不可见 (上 10%、下 90%)

**放射/关联:**
- 中心辐射: 核心主题 + 属性
- 树状/分支图: 家谱、分类学
- 同心圆: 层级 (地球、邻近度)

**网格:**
- 便当格: 整齐方块、模块化
- 元素周期表网格: 按类型/族排列
- 漫画条: 分场景叙事
- 拼图: 碎片组成整体

**空间:**
- 等距地图: 3D 游戏世界风格
- 剖面 (剖切): 实心物体内部
- 解剖标注: 标注整体各部件
- 爆炸图: 部件悬浮、展示组装

## 示例

**科学 - 水循环:**
```
Create educational infographic for Elementary Science.
Topic: The Water Cycle.
Content: Evaporation, Condensation, Precipitation, Collection.
Visual Style: Bright, colorful, 3D claymation style.
Layout: Circular flow diagram with arrows clockwise.
```

**历史 - 时间轴:**
```
Create educational infographic for High School History.
Topic: Timeline of Ancient Egypt.
Content: Old Kingdom (Pyramids), Middle Kingdom (Arts), New Kingdom (Tutankhamun).
Visual Style: Papyrus texture, hieroglyphic icons, gold/sand palette.
Layout: S-curve roadmap flowing top to bottom.
```

**文学 - 冰山:**
```
Create educational infographic for Sociology class.
Topic: Surface Culture vs Deep Culture.
Content: Above water (Food, Flags, Festivals). Below water (Body Language, Beliefs, Etiquette).
Visual Style: Paper Cutout Style, textured construction paper.
Layout: Iceberg diagram, tip = 10%, submerged = 90%.
```

**对比 - 矩阵:**
```
Create educational infographic for Elementary Science.
Topic: Inner vs Outer Planets.
Content: Compare across Surface Type, Size, Rings.
Visual Style: Kawaii/Cute Vector, pastel colors.
Layout: Comparison Matrix grid.
```

## 文字优先 Hack

图内复杂文字,先**生成文字**,再要图:
1. 让模型先写/完善文字内容
2. 再要求生成带该精确文字的图

这比把一切塞进一个提示词得到更锐利、更准确的排版。

## 字体控制

描述排版风格或直接点名字体:
- "Bold, white, sans-serif font"
- "Century Gothic 12px font"
- "Flowing, elegant Brush Script"
- "Heavy, blocky Impact font"
- "Thin, minimalist Century Gothic"

## 多语言 / 本地化

支持 10+ 语言。两种方法:

**直接:** 用目标语言写提示词,文字即以该语言渲染。

**翻译:** 用一种语言写提示词,指定目标:
```
Create this product ad. Render all text in Korean.
```

**单图多语言:**
```
Line 1: "GLOW" in Brush Script
Line 2: "10% OFF" in Impact font
Line 3: "Your First Order" in Century Gothic
Then translate all text into Korean and Arabic.
```

## 技巧

**提供自己的内容:**
- 粘贴文章文本、视频字幕、你的笔记
- 比只依赖搜索更准确

**草图转图:**
- 在纸上画潦草布局草图
- 上传并附提示词: "Use layout from attached image"

**迭代编辑:**
- "Leave everything else exactly the same, but change [X]"
- 在下载的图上标注,再作为参考图上传

---

*作者: Serge Shima ([t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)) · 许可: CC BY 4.0 — 需署名 · 来源: [smixs/visual-skills](https://github.com/smixs/visual-skills)*
