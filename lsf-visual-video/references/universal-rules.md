# 通用法则——适用于所有视频模型

以下法则适用于 Seedance、Kling、Veo 及任何其他 AI 视频生成器。它们存在的原因：当前所有视频模型共享同一种失败模式。它们奖励具体的实体导演指令，惩罚抽象、矛盾和关键词堆砌。无视这些规则，无论你瞄准哪个模型，都会产出浑浊的生成结果。

读完 `dramaturgy.md` 之后、读任何模型专属文件之前，先读本文件。模型专属语法建立在这些法则之上——它不取代它们。

## 目录

1. 不可协商之事。细节强化情绪（细节法则）
2. U1. 通用提示词骨架
3. U2. 开头权重
4. U3. Show don't tell（展示而非告知）
5. U4. 自然语言胜过标签堆砌
6. U5. 每个镜头一种主要运镜
7. U6. 精确的镜头语言
8. U7. 角色一致性锚点
9. U8. 不矛盾
10. U9. 具体实体细节胜过抽象概念
11. U10. 时长纪律
12. U11. 最终画面法则
13. U12. 三细节检查（发送前审计）
14. U13. 参考素材职责纪律
15. U14. 优先级声明

---

## 1. 不可协商之事。细节强化情绪。懒惰杀死提示词。

这是 AI 视频里最常被违反的法则，也是大多数多镜头提示词失败的唯一原因。戏构没问题——只是编剧在某个镜头上偷懒了，而那一个单薄的镜头把整段序列拖进糊里。

每个提示词里的每个镜头至少要拥有三个具体实体细节：

1. **一个环境压力。** 冰箱冷蓝光。沸水上的蒸汽。湿沥青。闪烁的荧光灯。滴水的水龙头。空调风里呼吸着的窗帘。（黑泽明：天气也是角色。见 `dramaturgy.md` §9。）
2. **一个身体微观动作。** 下颌锁紧。攥叉子的指节发白。嘴唇抿成一条线。他用力咽了一下。手指抵着门框蜷起。（Show, not tell——身体是情绪唯一能显影的地方。）
3. **一个声音锚点或视觉母题。** 2.3 秒处的腹鸣。暗色手机屏幕上的倒影。同一扇窗玻璃上的雨。每次剪切前那一次荧光灯闪烁。

如果一个镜头都没有这些——它就是填充物。删掉或重写。对"交代镜头""转场""主角产品"镜头没有例外——恰恰是这些镜头最先变懒。

不显影、且暴露编剧偷懒的词：

- "cinematic"、"professional"、"high quality"、"masterpiece"、"stunning"、"epic"、"amazing"
- "beautiful lighting"、"dynamic camera"、"intense moment"、"powerful scene"
- "he is sad"、"she is angry"、"he is afraid"——无身体承载地直接点名的情绪

把每个替换成具体实体事实。完整理论见 `dramaturgy.md` §2（第二法则）。

## 2. U1. 通用提示词骨架

每个提示词都按这些层构建，大致按此顺序：

```text
[Subject / Character]
[Action / Motion]
[Scene / Environment]
[Camera / Shot / Lens]
[Lighting / Atmosphere]
[Style / Mood / Palette]
[Sound / Audio]
[Duration / Aspect ratio / Resolution]
[Continuity rules]
[Negative constraints — only if the model supports them]
```

模型专属骨架见各自参考文件（`seedance.md`、`kling.md`、`veo.md`）。对剧情型/多镜头/角色锁定的 Seedance 工作，`seedance.md` §6 的生产级 11 块骨架取代本通用骨架。

## 3. U2. 开头权重

把最重要的主体、动作和本次修正放前面，减少重复描述。这是写作优先级，不是所有模型在前 30–40% token 上具有固定注意力权重的已证实机制。

## 4. U3. Show don't tell（展示而非告知）

模型无法渲染情绪。它渲染身体。把每个情绪翻译成物理动作。

- 差。"He is scared.（他很害怕）"
- 好。"His jaw locks. He stops breathing for one beat. His fingers curl against the doorframe.（他下颌锁紧。屏息了一拍。手指抵着门框蜷起。）"

校准：一次情绪转变，**2-4 个可观察线索**（眼球移动、眉部紧绷、嘴、呼吸、吞咽、手部）就够。少了让模型猜；多了像演技过猛。

## 5. U4. 自然语言胜过标签堆砌

视频模型不是图像模型。"masterpiece, 4k, cinematic, beautiful"这类标签堆砌会失败。用完整的电影化句子，就像在给真人摄影指导下brief一样写。

## 6. U5. 每个镜头一种主要运镜

不要在 5 秒片段里叠三种运镜。选一种主导运镜（dolly-in、pan、tracking、static）即可。若需要，叠一层细微次级调整（轻微手持晃动、柔和变焦移焦）。更多就是视觉混乱。

## 7. U6. 精确的镜头语言

写明焦段。"Shot on 50mm"在所有主流模型都有效。速查：

- 24mm。广角、沉浸、夸张的空间感
- 35mm。自然纪录片感
- 50mm。亲密、人的视角
- 85mm。肖像、压缩背景
- 100mm macro。质感、细节
- anamorphic 40mm。电影宽银幕

完整词汇见 `camera-lighting-vocabulary.md`。

## 8. U7. 角色一致性锚点

把身份锚在**每个提示词的开头**。多片段序列中，在每一条提示词里重复完整身份块。视频生成器在两次生成之间没有记忆。把每次生成当作在给一位失忆的天才实习生做brief。

身份块只写会影响一致性的可见特征。角色参考已清楚定义的外观不逐项复述；非人角色不套用人类鼻子、牙齿或嘴唇模板。局部修正只补充有歧义的结构与素材优先级。

角色锁定的模型专属语法：
- Seedance：`@img1` 参考 + 身份块（见 `seedance.md` §10）
- Kling 1.x – 2.x：Element Binding + 3-4 张参考图（见 `kling.md` §7）
- Kling 3.0：提示词内 `[Character A: <完整身份>]` 标签，可按需与元素库结合（见 `kling.md` §3）
- Veo：参考素材 ingredients / JSON 身份（见 `veo.md`）

## 9. U8. 不矛盾

模型服从最强信号。矛盾产生伪影。

- 差。"Still pond（静止水面）" + "flowing water（流动的水）"。
- 差。"Close-up（特写）" + "wide cinematic landscape（大广角电影风景）"。
- 差。"Quiet moment（安静时刻）" + "explosive action（爆炸动作）"。

## 10. U9. 具体实体细节胜过抽象概念

"Loneliness（孤独）"不显影。"A man sitting alone, shoulders collapsed, face lit by blue phone glow, empty bottles on the table"显影。

这与第 1 节的细节法则是同一法则，只是不同侧面。第 1 节是审计工具。这里是原则本身。

推论——**后果式提示词**。当前模型渲染真实物理，所以描述动作的后果而非仅描述动作：轮胎掀起水幕；手握罐子、盖子真的拧开；撞击把表面崩成蛛网状裂纹。每一步强制下一步的动作链还能当 QA 用——断裂的链条一眼就能暴露失败的生成。

## 11. U10. 时长纪律

先核实用户当前模型和界面支持的时长，再估算对白、动作与收尾的占用。不要按固定倍数默认拆分，也不要把故事所需时长写进提示词后当作设置已经生效。单次生成、单镜头和最终成片时长是不同概念。

若用户只要求多两三秒，不扩成多段长片。只有平台支持时才增加实际时长；受上限限制时提出最小可行调整，并说明哪些动作或台词需要取舍。详见 [局部修正与时长检查](iteration-repair.md)。

三个例外：
- Seedance——通过 "Cut to" 语法在一条 5-10 秒片段内放 2-3 个镜头（见 `seedance.md` §8）。
- Kling 3.0——一次生成内最多 6 个镜头，最长 15 秒，带原生音频与对白（见 `kling.md` §3）。
- Seedance 2.5——一次通过最长 30 秒。可用工作结构是连续阶段，每阶段一次主状态变化并明确可见的结束状态（见 `seedance-25.md` §6）。

## 12. U11. 最终画面法则

每个片段都需要清晰的最终帧。模型把结尾当作情绪目的地。

- "Ends on his face frozen in the blue refrigerator light"胜于"he stands there sadly。"

最终画面也是五大锚点之一（见 `dramaturgy.md` §13）。点名它不可妥协。

## 13. U12. 三细节检查（发送前审计）

在把最终提示词交给用户前，审计每个镜头。每个镜头必须至少带以下各一：

1. 环境压力（灯光、天气、表面、房间的声音）。
2. 身体上的物理微观动作（下颌、手、呼吸、眼睛、手势）。
3. 与情绪脊柱绑定的声音锚点或重复出现的视觉母题。

镜头为零，发之前修。只有一件，自问能否不加赘肉地加到两件。本技能工作例里最强的提示词总是三件齐全。

通不过本检查的空描述："establishing wide shot"、"beautiful lighting"、"dynamic camera move"、"cinematic look"、"intense moment"、"dramatic close-up"。把每个换成三个具体实体事实。

## 14. U13. 参考素材职责纪律

只要模型接受参考资产（Seedance `@Image/@Video/@Audio`、Kling Element Binding 与 Omni 参考、Veo ingredients），**每个资产都要在提示词里写明明确职责**：它定义了（外观、动作、声音、场景、运镜路径）什么、要忽略什么（"Do not use the image background"、"Do not use the people in the image"）。

- 逐主体绑定："<Character A> corresponds to @Image 1 — use only the appearance, hairstyle, and clothing."绝不写集体式"@Images 1 through 4 define four characters respectively"——它没说清哪个是哪个。
- 不要复述参考已定义的内容。若视频参考携带了动作，只点名要继承的属性；重新逐动作描述会与参考打架。
- 资产多不等于控制多。控制来自职责清晰；未分配职责的资产会漏进画面。

模型专属限制与模板在各模型文件里（`seedance-25.md` §5 的系统最完整）。

## 15. U14. 优先级声明

当提示词过载（10+ 场景、众多主体、空间花活）时，加更多描述只会更糟。改为声明优先级——模型无法知道什么最重要，除非你告诉它要保护什么、牺牲什么：

1. 必须在每个镜头存活的核心里程碑主体。
2. 必须出现的关键镜头。
3. 允许模型自由发挥的转场。
4. 强制性的最终帧。

这排在提示词长度纪律之上：带优先级声明的短提示词，胜过没有优先级声明的长提示词。

---

*作者：Serge Shima（[t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)）· 许可：CC BY 4.0 —— 需注明出处 · 来源：[smixs/visual-skills](https://github.com/smixs/visual-skills)*
