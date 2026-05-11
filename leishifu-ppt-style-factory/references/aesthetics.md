# 美学关键词 → 16 维度映射表

当用户用文字描述创建风格（方式 4）时，根据关键词匹配以下预设体系。

每行是一套完整的美学"基因"，覆盖 16 维度的核心取向。具体数值在生成时展开。

---

## 映射表

| 关键词 | D1 配色 | D2 强调 | D3 标题字体 | D8 背景 | D9 圆角 | D10 阴影 | D14 卡片 | D15 装饰 | D16 气质标签 |
|--------|---------|---------|------------|---------|---------|---------|---------|---------|-------------|
| 赛博朋克 / cyberpunk | 深紫#0a0014 / 浅青#e0f7fa | 霓虹青#00ffd5 + 品红#ff2d95 | 无衬线 display (Orbitron) | particle | 0px | none | glass | cross-matrix | 未来·科技·叛逆 |
| 日式侘寂 / wabi-sabi | 暖白#f5f0e8 / 墨色#2c2c2c | 陶土#c4a882 | 衬线 (Noto Serif JP) | solid | 0px | none | outlined | none | 极简·自然·不完美 |
| 包豪斯 / bauhaus | 纯白#ffffff / 黑#1a1a1a | 红#e63946 + 蓝#1d3557 + 黄#f4d03f | 几何无衬线 (DM Sans) | solid | 0px | none | filled | geometric | 功能·几何·理性 |
| 孟菲斯 / memphis | 粉#ffeef0 / 深灰#333 | 多色(薄荷+紫+橙) | 粗无衬线 (Space Grotesk Bold) | solid | 12px | subtle | filled | geometric | 玩味·波普·大胆 |
| 蒸汽波 / vaporwave | 粉紫渐变#e0aaff / 深蓝#1a1a40 | 热粉#ff6b9d + 青#00d2ff | 衬线 (Playfair Display) | fluid | 0px | medium | glass | lines | 怀旧·虚幻·梦境 |
| 极简北欧 / nordic minimal | 浅灰#f8f8f6 / 深灰#2d2d2d | 木色#c8956c | 无衬线 (Inter) | solid | 8px | subtle | outlined | none | 简洁·温暖·实用 |
| 暗黑科技 / dark tech | 纯黑#0a0a0a / 冷白#e8e8e8 | 冷蓝#0ea5e9 | 无衬线 (Inter) | grid-dots | 0px | none | outlined | dot-matrix | 科技·精密·专业 |
| 新中式 / neo-chinese | 宣纸#f4efe4 / 墨黑#1c1c1c | 朱砂#c23b22 | 衬线 (Noto Serif SC) | contour | 0px | none | outlined | none | 东方·雅致·文化 |
| 学术论文 / academic | 纯白#ffffff / 深蓝灰#1e293b | 深蓝#1e40af | 衬线 (Source Serif 4) | solid | 0px | none | outlined | none | 严谨·专业·可信 |
| 潮牌街头 / streetwear | 纯黑#0a0a0a / 纯白#ffffff | 荧光绿#b5ff00 | 粗体无衬线 (Bebas Neue) | particle | 0px | none | filled | cross-matrix | 张力·反叛·态度 |
| Material / 谷歌风 | 白#fafafa / 深灰#1c1c1e | 蓝#1a73e8 | 无衬线 (Roboto) | solid | 12px | medium | elevated | none | 规范·友好·系统 |
| 渐变玻璃 / glassmorphism | 深灰#1a1a2e / 白#ffffff | 紫蓝渐变#667eea→#764ba2 | 无衬线 (Inter) | fluid | 16px | subtle | glass | none | 通透·现代·精致 |
| 报纸杂志 / editorial | 米白#f5f1eb / 黑#1a1a1a | 红#d32f2f | 衬线 (Playfair Display) | solid | 0px | none | outlined | lines | 权威·经典·叙事 |
| 太空探索 / space | 深蓝黑#050520 / 白#e8e8f0 | 星蓝#4facfe + 橙#ff6b6b | 无衬线 (Exo 2) | particle | 4px | subtle | glass | dot-matrix | 探索·浩瀚·科幻 |
| Y2K / 千禧 | 银灰#d4d4d8 / 深紫#2d1b69 | 亮粉#ff69b4 + 银#c0c0c0 | display (Bungee) | fluid | 16px | medium | glass | geometric | 千禧·科技乐观·闪亮 |
| 自然生态 / organic | 暖米#f0ebe3 / 深绿#1a3c34 | 翠绿#22c55e | 衬线 (Lora) | contour | 8px | subtle | filled | none | 自然·生机·可持续 |

---

## 使用方法

1. 用户描述命中某个关键词时，取对应行作为基础
2. 其余未覆盖的维度（D4 正文字体、D5 字重、D6 字号、D7 间距、D11 动效、D12 图标、D13 图片处理）用通用默认值：
   - D4：body 跟随 D3 的 sans/serif 倾向，mono 用 JetBrains Mono
   - D5：heroWeight=200, headingWeight=300, bodyWeight=400
   - D6：标准响应式字号
   - D7：standard 密度
   - D11：standard 动效
   - D12：lucide stroke
   - D13：无滤镜，16:9，cover
3. 如果关键词不在表中，根据用户描述的情绪倾向，选最近的 1-2 行做参考，混合生成
4. 所有值都是起点，用户可以逐维度调整
