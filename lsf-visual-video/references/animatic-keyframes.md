# 动画分镜关键帧（опорные кадры）

这是静帧面板层。分镜关键帧不是素材的截图——它是单张绘制图像，必须承载一个故事节拍，且**无运动、（通常）无脸**。动画分镜挂在这些面板上。一张只是好看的面板是壁纸；面板必须交代其故事功能、戏剧性，以及它无法表现的运动——全部冻结在此。

本文件把节拍表/阐述转化为**опорные кадры**（关键帧），再转成图像生成提示词。它建立在 `dramaturgy.md`（§2 细节法则、§10 三层法、§11 镜头卡、§12 节奏阶梯、§15 检查）与 `universal-rules.md`（U1 骨架、U11 最终画面）之上。取景/镜头/光线 token 与 `camera-lighting-vocabulary.md` 配对，功能分类法见 `role-modes.md` §4，空间清晰脊柱见 `patterns-and-genres.md`（动作类型、升级模式），每个锁定帧的动画化用 `seedance.md` / `kling.md` / `veo.md`。输出与分镜格式 C 兼容：`时间 | 镜头 | 功能 | 动作 | 运镜 | 光 | 声 | 情绪`。

贯穿以下示例的执行简报：直线竞速/漂移竞速广告，冷战斗色板（钢蓝、青、洋红、水银白；**红和绿仅作点缀**；琥珀色只作起跑树的异星脉冲或毒液溢光），面孔缺位或碎裂不堪。按任务需要更换主体——方法不变。

## 目录

1. 动画分镜关键帧必须做什么
2. 关键帧卡（镜头卡的静帧延伸）
3. 每个节拍多少关键帧（密度阶梯）
4. 构图出一幅读作"运动"的静帧
5. 静帧中无脸的情绪
6. 单面板的装载帧
7. 从关键帧到图像生成提示词
8. 30 秒竞速广告的关键帧板工作示例
9. 清单：这个关键帧是否配得上它的位置

---

## 1. 动画分镜关键帧必须做什么

动画分镜里**最小单元是面板，不是镜头。** 镜头有时长、运动和声音承载功能穿越时间。关键帧只有一张冻结图像，必须在一次扫视中承载同样的功能。所以每个面板在一张静帧里同时做四件事：

- **一个可读的故事节拍**——生成前用一句话命名。说不出来，面板未就绪（`dramaturgy.md` §1）。
- **一个功能标签**——Establish / Reveal / Power / Pressure / Detail / Reaction / Shift / Impact / Aftermath / Exit（`role-modes.md` §4）。标签即面板要回答的问题。无脸广告里 **Reaction** 从人脸改派给*机器的*脸——指针跳动、胎面皱纹、车头下沉。把仪表和橡胶当演员。
- **一个情绪**——经由金属、橡胶、光或解剖表达，绝不用名字（`dramaturgy.md` §2）。信号混杂 = 无信号。
- **一个隐含运动**——静帧无法做出的动作，冻结成它的物理残留（§4）。

携带节拍、功能、情绪和隐含运动的面板才配得上它的位置。缺四者之一的面板就是 *fantik*——没有糖的包装纸（`dramaturgy.md` §3）。整个文件的纪律是：**你不能把"运动"或"情绪"直接提示进静帧——你提示的是它们各自留下的物理后果。**

---

## 2. 关键帧卡

`dramaturgy.md` §11 的镜头卡描述移动镜头。关键帧需要一种*静帧*专用的卡：每个字段描述一张冻结图像，三个字段是新的（隐含运镜、情绪经由物件、运动渲染为静帧）。生成前填满每个字段。空字段暴露缺失的方向。

```text
KEYFRAME CARD
- Panel ID.            01, 02, 03
- Timecode.            on-screen life in the animatic (e.g. 0:10.5, HOLD 2s)
- Function tag.        Establish / Reveal / Power / Pressure / Detail /
                       Reaction / Shift / Impact / Aftermath / Exit
- Beat.                what changes in the story in this one still
- Framing + lens.      ECU / CU / MCU / wide / macro insert / POV + lens token
                       (24mm immersive ... 100mm macro — camera-lighting-vocabulary.md §3)
- Subject / anchor.    the ONE object or anatomy the eye lands on in 0.3s
- Depth layers.        FG job (frame / obstruct / put us inside)
                       MG job (the subject / the act)
                       BG job (stakes / context / rival)
- Implied camera.      the move this still is the first frame OF
                       (push-in, whip, bumper-POV, joust) — what it would do if it ran
- Light + palette.     one motivated source + direction + the surface it rims;
                       concrete colors, amber-ban repeated
- Emotion-via-object.  the feeling a face would show, mapped to an object's state (§5)
- Motion-as-still.     which frozen cue carries the missing movement (§4):
                       smear / partial blur / streak / vector / sharp-blur / held stillness
- Caption / label.     one word: setup / commitment / mistake / recovery /
                       proof-of-speed / result
- Sound.               what audio sits under the held frame, where the cut bites
                       (fill even though it is a still — dramaturgy.md §11)
- Production note.      prop, rig, continuity anchor
```

卡片直接映射到格式 C：`Function`、`Framing`、`Implied camera`、`Light`、`Sound`、`Emotion-via-object` 成为表格列。三个静帧专属字段——**implied camera（隐含运镜）、emotion-via-object（情绪经由物件）、motion-as-still（运动作为静帧）**——正是普通镜头卡不会逼你点名的那些，也恰恰是防止面板变平淡的字段。

---

## 3. 每个节拍多少关键帧——密度阶梯

**音频里的响度 = 板上的面板数。** 静默得到一张持守面板；一声爆响得到一次爆发。这是 `dramaturgy.md` §12（节奏阶梯）与 `role-modes.md` §3（剪辑密度：剧情 3-4 节拍/5 秒、叙事 4-7、快蒙太奇 6-9）的静帧版解读。完整 30 秒节拍图就是 §8 的工作板；按 `patterns-and-genres.md` §3 拆分（30 秒 = 6×5 秒）。

| 节拍 | 密度 | 面板 | 为什么 |
|---|---|---|---|
| **仪式/调度**（安静） | 1 张主角面板，持守 | 1 张面板存活 1.5-2.5 秒 | 静默节拍是整体性的。不要细分它——其威力在于世界屏息时万物不动。一张对称"呼吸"帧、最多负空间、最少运动。 |
| **压力攀升**（琥珀错落） | 递进单张 | 3 张面板，长度塌缩 | Sportsman 树相隔 0.5 秒连发三盏琥珀——三张可绘面板，一张比一张更紧，剪切长度向绿色塌缩。 |
| **起跑/冲击**（爆响） | 3 面板微爆发 → 最多 6-9 | 6-9 张面板，8 帧 → 4 帧 | 音频爆响渲染为面板*密度*，不是一张大图。嘻哈蒙太奇：保险杠 POV 拖影、侧面车轮打滑、转速表爆闪、离合手、车道线频闪。 |
| **对抗**（持续咆哮） | 交替 | 碎片簇 ↔ 一张持守细节 | 绝不允许两个爆响簇背靠背。每两次爆发之间，一张持守的安静面板——响亮只有在安静旁边才有效。 |
| **余波/退出**（切到静默） | 1 张主角面板，持守 | 1-2 张面板，约 2 秒持守 | 以后果收尾，而非解释。一张持守静帧：飘散的烟、松开的手、车头没入黑暗。 |

**分配法则。** 30 秒广告落在约 18-26 张面板。把板画成下降时长阶梯（≈2.5 秒 → 0.5 秒 → 4 帧），只被那一次起跑前停顿和那一次完赛后持守打断。即使静音，板也应该*读作*一个加速的转速表。只有当音频爆炸时才给节拍微爆发；其他任何地方，一张持守的面板强于三张散落的面板。

---

## 4. 构图出一幅读作"运动"的静帧

关键帧无法变速、剪切或甩镜。每个缺失的运动都结算为**六种冻结提示**之一。永远不要写"motion"——写运动留下的痕迹。在卡片的 *Motion-as-still* 字段写明提示，并在提示词的运镜/光条款里再写一遍；模型默认过度干净的稳定，不说明就会把速度打磨掉（§7）。

| 提示 | 在静帧中是什么 | 渲染的隐含动作 |
|---|---|---|
| **Directional motion-blur smear**（方向性运动模糊拖影） | 背景沿行进轴拖成条纹，主体锐利。护栏、车道线、树灯被拉成水平光棒。 | tracking pass（跟拍过场）、POV launch（POV 起跑）、whip-pan 余波 |
| **Frozen partial blur**（冻结部分模糊） | 一个运动元素模糊（胎侧壁、烟团、换挡手悬空）而锚点保持清晰——单帧被定格瞬间的证据。 | speed-ramp 峰值、起跑、换挡 |
| **Streak-frame (implied whip)**（条纹帧，隐含甩镜） | 整个面板被刮成运动条纹，只存活一个可读形状（轮弧、换挡杆）——"两镜之间"的模糊面板。 | whip pan、转场节拍 |
| **Posture / trajectory vector**（姿态/轨迹向量） | 身体或车锁定在只能向前结算的姿态——手腕在换挡杆上绷起、前轮抬起、重心甩到后轴。眼睛会替你完成动作。 | 蓄力姿态、定格帧、起跑 |
| **Sharp-subject / blurred-field separation**（锐主体/糊背景分离） | 浅景深微距：指节、指针、卡扣剃刀般锐利，其余全部溶掉。隔离 = 切细节的冻结。 | 插入链、急推到位、嘻哈特写 |
| **Freeze-frame stillness**（冻结帧静止） | 刻意*零*模糊、硬边缘、屏息——在周围模糊面板之间读作停摆的钟。 | 起跑前的持守节拍、上膛的弹簧 |

按技法套件（三要素 + 静帧应用）：

- **冻结运动模糊**——它作用于情绪：差分模糊读作被触感化的速度，世界从静止主体旁被撕过——出处：Dod Mantle 在《Rush》里对每次超车都用了 whip-pan，让背景溶解。——*关键帧中* [Shift/Impact]：主角车针尖般锐利，整个背景被刮成水平条纹，前景物体拉长成光棒。单面板最强大的速度技巧：**锐利主角 + 完全涂抹的世界。** 处处等量模糊 = 柔焦照片；差分模糊 = 速度。
- **胎面褶皱 / 部分模糊**——情绪：可感的物理，力量在其巅峰被定格——出处：Goodyear 刻意静音的胎侧壁折叠慢镜；Ritchie 的 speed-ramp 作为感叹号。——*关键帧中* [Detail/Reaction]：微距进后胎侧壁，褶皱被捕获在最大折叠处，接触斑处烟刚刚绽放，其余全部锐利。被定格的一万分之一秒。值得*持守*的主角细节。
- **烟/碎片/水雾形状**——情绪：力量获得可见的身体，恐惧升入空中——出处：NHRA 烧胎机位，"一堵烟墙"地面高度的逆光。——*关键帧中* [Pressure/Power]：逆光胎烟作为发光墙（正面光烟是死灰色虚无）；水盒水雾冻成镜面高光水滴星座，每颗在前缘描边。只有光线穿过它，氛围才可读（§5）。
- **姿态/倾斜向量**——情绪：只能向前resolve的静止；眼睛来完成起跑——出处：Vaughn 的蓄力姿态（《王牌特工》《夹心蛋糕》）——每一帧都装载着轨迹。——*关键帧中* [Power/Shift]：**没有中性面板。** 怠速的车 = 前轮微抬、重心甩到后轴。方向盘上的手 = 手指半握。把负空间构图在主体*前方*——它即将射入的方向。
- **引导线/光条**——情绪：给眼睛的轨道，同时编码方向与速度——出处：Papamichael 的沥青入画（《极速车王》），道路即速度表。——*关键帧中* [Power/Impact]：车道中线划向灭点，钠灯/汞灯实景灯拖成湿沥青上的长反射。保留纹理（箭头纹、焦油缝、胎痕），光条才有东西可拖。
- **失重荷兰式**——情绪：失衡、失抓地、威胁——出处：Raimi 的倾斜攻击帧（《鬼玩人 2》）。——*关键帧中* [Impact]：在唯一一次失抓地节拍用力倾斜地平线——轮胎挣脱、车侧滑。为单一不稳定节拍保留它，才保持响亮；作为壁纸的荷兰式读作糟糕构图。

**速度预算法则**（源自竞速真相流派）：当**五个提示至少三个共存于一帧**时，静帧才卖得出速度——(a) 相机在保险杠高度或更低，(b) 沥青拖过画面下方，(c) 近前景参考掠过边缘，(d) 锐利主角对运动模糊背景，(e) 机械振动提示（抖动的后视镜、重影指针、涂抹的轮缘）。一个提示 = 车照片。三个 = 速度。如果"快"面板凑不出三个，就放低构图、把相机拖到沥青上、往前景扔一个锥桶或护栏。

---

## 5. 静帧中无脸的情绪

脸做四份工：展示感受、展示看向哪、展示代价、展示决定。脸被封禁，重新分配：**决定 → 动作中的解剖；内在状态 → 跨越阈值的物件；观看/对抗 → 空间**（§6 与 `dramaturgy.md` §2）。每张面板分配一份工并打标签。情绪必须已经冻结*在物件内部*——静帧不能靠运动模糊替它做情绪工作。

两条承重规则：

- **解剖只出现在决定上。** 静止的手是填充物；*正在做决定*的手才是镜头。画任何手/脚面板之前，先命名动词——grip / latch / shift / preload / release。没有动词，就没有面板。渲染肌腱隆起、手套皮革起褶、一道硬侧光雕刻指节纹理、其余全在阴影（莱昂内的拔枪前的手；耐克《Take It to the Next Level》，第一人称，无主角脸）。
- **物件只在状态变化时才出现。** 静态挡杆只说明"车的东西"，然后平掉。画跨越阈值的**后**状态；前态是隐含的（本田《Cog》：每个物件都做一件不可逆的事）。转速表钉在红区，不是怠速。点火灯亮起发光，不是暗的。胎面被捕获在半折叠。

用替换表作为核心交付物——当剧本想要一种情绪而脸不可用时，用这个裁切渲染这个物件。全程冷色板。

| 情绪（脸会显示的） | 物件替身 | 裁切 | 渲染备注（静帧） | 标签/标记 |
|---|---|---|---|---|
| **恐惧/惊怖** | 指节上的汗珠；镜面反射中的震颤（不是眼睛） | macro / ECU | 汗珠上一记硬镜面高光、冷轮廓、四周深黑；镜缘双影暗示振动 | setup → Pressure |
| **决心/承诺** | 方向盘或挡杆上发白的指节；脚钉住油门 | CU / MCU | 肌腱隆起、手套皮革起褶、握力拉满；一记侧光、座舱在阴影中 | commitment → Shift |
| **专注/锁定** | 漆面/大灯玻璃上反射的起跑灯（不是人眼） | MCU | 舞台灯泡在漆面或镀铬上成冷点镜像；紧、居中、静 | setup → Detail |
| **紧绷（机器极限）** | 转速表指针钉在红弧；胎侧壁起皱；排气火焰 | ECU / CU | 指针死死顶着红线、运动静止但无疑是最大；侧壁在最深折叠 | proof-of-speed → Pressure |
| **失误/惊慌** | 轮胎抖动（侧壁"变方"）、方向盘回踢、转速过放 | CU | 侧壁变形错误、模糊方向与车道对抗；转速表飙过表带 | mistake → Impact |
| **胜利/释放** | 握力放松；降落伞绽放；一个车头过线；烟穿过大灯光束 | CU → WS | 手指从方向盘上展开；或胜利的远端干净几何，冷逆光穿过烟 | result → Aftermath / Exit |
| **期待（起跑前）** | 点火/线锁上方的指头；预赛灯亮起；持住的挡杆 | ECU / CU | 指头距按钮一毫，灯刚亮起冷光，一切冻结——"静默"面板 | setup → Pressure |

状态变化速查表（画活性状态；死态隐含）：点火暗 → 灯亮起；转速表怠速 → 指针钉红；胎面浑圆 → 深度折叠褶皱；水盒镜面静止 → 被起跑撕碎；前轮着地 → 抬起；底盘水平 → 下蹲；降落伞收紧 → 在终点网前绽放。

---

## 6. 单面板的装载帧

关键帧是一张观众在 0.3 秒解出、在 1 秒愉快重读的图。没有脸，几何与深度堆栈在表演。

> **装载面板的核心法则。** 一个焦点、一种情绪、三个可用深度层、零死物。第一眼回答一个问题；奖励第二眼。

**深度层职责（FG / MG / BG）。** 用三个显式深度从句写提示词，每句写明职责。这是"一眼可读、二眼有赏"的引擎（把 `dramaturgy.md` §10 延展进单张静帧）。若三个平面携带相同的模糊或尺度，你只有一个平面——强制锐利 MG 主体对柔和 FG 框与柔和 BG 筹码（浅景深是面板的层级工具，`camera-lighting-vocabulary.md` §3）。

| 平面 | 默认职责 | 直线竞速物体 | 服务功能 |
|---|---|---|---|
| **前景** | 框景/遮挡/把我们放进现场 | 防滚架横杆、后视镜缘、安全带、烟丝、湿玻璃 | Pressure, Power |
| **中景** | 主体/动作 | 换挡杆上的手、方向盘上的指节、踏板上的脚、转速表盘 | Detail, Shift, Impact |
| **背景** | 筹码/语境/对手 | 舞台灯泡、对手车道大灯、终点线、收窄的护栏 | Establish, Reveal, Pressure |

**一眼 + 有赏**——它作用于情绪：即时可读的帧建立信任；值得重读的帧建立密度与价值。没有脸可锚定，浑浊面板塌缩成虚无。——*关键帧中*：生成前点名唯一焦点（转速表指针/舞台灯泡/指节），把它放在强线上，把其余降为支撑。第二眼的奖励是一个倒影、一个桥接物件或一个状态指示——一个，不是一堆。

**中线脊柱，然后破对称**——情绪：一条主导轴线（车道线、圣诞树、分隔墙）给眼睛一条轨道，连混乱的帧都可读；在一辆车领先的瞬间打破它读作动量。——出处：Anderson 居中求即时可读；Bong 打破平衡调度显权力转移。——*关键帧中*：画一张正面头部对称"呼吸"面板——两车沿中线镜像、树正中、均等负空间（标签 **Establish/Pressure**，持守最久）。下一张面板破镜——主角领先一个车头、对手被轻推、中线滑离三分（标签 **Shift/Impact**）。这一对只在起跑用一次；过度用对称会杀死速度。

**功能性 vs 装饰性冗余物——证据测试。** 只有当物件至少满足其一才保留：(1) **状态指示器**（代替脸——转速表在红区、发白指节）、(2) **动作舞台**（推进节拍——前轮离起跑线 7 英寸 = 预赛）、(3) **接下一面板的桥**（setup match-cut 或伸手）。死细节——咖啡杯、后视镜骰子、仪表板贴纸——不出状态、不推进、不桥接。剪掉。"每件物品都是线索"（朴）；功能性冗余*装载*帧，装饰性冗余*削弱*它。

**角度编码节拍**（没有脸，所以角度*就是*情绪）：低/地面高度 = 力量、威胁、起跑力（**Power, Impact**）；平视横移 = 对等、明言的竞争（**Establish**）；高/俯视 = 审判、渺小、余波（**Aftermath, Exit**）。

---

## 7. 从关键帧到图像生成提示词

关键帧卡按照通用骨架（`universal-rules.md` U1）加开头权重（U2）变成静帧提示词。**开头放取景 + 镜头 + 光 + 色板 + 锚点物件**——这些是静帧的承重 token；模型把大部分注意力放在前 30-40% 的 token 上。

面板 → 提示词骨架：

```text
[Framing + lens]           e.g. "Low bumper-height macro, 24mm, shot past a blurred roll-cage bar"
[Anchor subject + state]   the ONE object at its threshold: "rear slick sidewall wrinkling at the contact patch"
[Depth clauses, 3 jobs]    FG frame / obstruct · MG subject / act · BG stake / rival
[Motion-as-still cue]      "sharp subject against horizontal motion-blurred background, foreground reference elongated into a light-streak, rear rim spokes smeared to a disc"
[Light + palette]          one motivated source + direction + surface it rims; concrete colors; amber-ban
[Texture]                  "fine film grain heaviest in shadow, halation on the practicals, one anamorphic flare, crushed blacks"
[Face rule]                "no face" — or "driver a featureless silhouette against blown rival headlights, only knuckle highlights legible"
[Aspect / no-speed-up note]  "no speed-ramp; build velocity into the static frame"
```

让静帧保持诚实的规则：

- **显式点名差分模糊。** 模型默认过度干净的稳定。写 "motion blur on background, fast-shutter look, sharp subject, rim spokes smeared to a disc." 等量/无模糊是最常被造假也最常失败的提示（防伪防火墙，§4 速度预算）。
- **把脸挡在画外或碎裂。** 把任何本应成脸的东西转成剪影 / 逆光加轮廓光和一点闪光。无特征。
- **把音频渲染为物理后果，绝不渲染为具名声音。** "Loud engine" 是被禁的填充（`dramaturgy.md` §2）——改提示 "heat-haze warp off the headers, exhaust flame, chassis squat, sidewall wrinkle"。
- **防无菌守卫。** 若面板可以被题注为"clean"、"beautiful lighting"或"high quality"，它就失败了——点名颗粒、光晕、压死黑、那一记镜面高光（`universal-rules.md` U12）。一个主导有动机光源；约 70% 的画框保持无光（`camera-lighting-vocabulary.md` §5-7）。

每个取景/镜头/光 token 都交叉链接到词汇文件。然后**关键帧就是锁定的首帧**；把它交给 `seedance.md` / `kling.md` / `veo.md`，带上唯一主导运镜（每 5 秒一个——`camera-lighting-vocabulary.md` §2）来动画化。用模型语法点名："low bumper-height camera, asphalt streaking, motion blur on background, sharp subject, no speed-up."

---

## 8. 30 秒竞速广告的关键帧板工作示例

Sportsman 树直线竞速，冷色板，无脸——用卡片约 13 张面板。这是用户填装的交付模板：每行是一张压缩关键帧卡，兼容格式 C（`时间 | 镜头 | 功能 | 动作 | 运镜 | 光 | 声 | 情绪`）。剪切长度向绿色塌缩、在褶皱上持守，然后加速到终点。

| Time | Shot (anchor) | Function | Action (state-change + motion-as-still) | Camera (implied move) | Light (cold) | Sound | Emotion-via-object |
|---|---|---|---|---|---|---|---|
| 0.0–2.5 | Slick into water box | Establish | Front tyre breaks mirror-still water; bulb reflected in the sheet | locked macro, low (held) | steel-blue, wet specular | idle lope, water trickle | coiled stillness |
| 2.5–5.0 | Burnout wall | Power | Rear erupts a smoke wall, car straining on line-lock; smoke backlit luminous | ground-level wide (burnout-cam) | cyan backlight through smoke, red tail bleed | lope → tyre scream | leashed force |
| 5.0–6.5 | Pre-stage bulb + front tyre | Pressure | Tyre creeps, top blue bulb lights, beam line as graphic spine | CU, static | blue glow on wet metal | lope thickens | held breath |
| 6.5–8.0 | Stage bulb + knuckles | Pressure | Second bulb lit, knuckles whiten on the trans-brake (depth: bulb BG, hand FG) | CU, depth layers, static | two blue bulbs, crushed black | idle DROPS to silence | point of no return |
| 8.0–9.5 | Amber stagger (1 of 3) | Pressure → Shift | First amber lights; foot pre-loading the pedal | tree-cam, snap-tight | amber pulse (sole warm, toxic) | vacuum of silence | trigger tension |
| 9.5–10.3 | Held breath frame | Pressure | Staged car dead-still, last amber, tach needle the only tremor | symmetric, locked (HOLD) | amber flare, steel rim | silence (the pause) | loaded spring |
| 10.3–11.6 | LAUNCH lunge | Impact | Both cars squat, front wheels lift, green flares, asphalt smears back | low bumper-POV, fisheye (smear) | green flash + hard flare | BANG, leads pic 3fr | release / violence |
| 11.6–13.5 | **Slick wrinkle** (HOLD) | Detail / Reaction | Sidewall folds and hooks at the contact patch; speed-ramp pause, partial blur | macro slick-cam (frozen ramp) | hard side light, smoke bloom | tyre bite (near-silent) | physics felt |
| 13.5–15.5 | Cabin shake | Pressure | Needle buried in red, mirror doubled by vibration, glass strobing | hard-mount interior (tremor) | strobing exterior, red needle accent | rising rev, gear stab | strain |
| 15.5–18.5 | Bumper POV | Pressure | Asphalt tears under the nose, lane stripes strobe to a vanishing point | low forward hood-cam, 24mm (radial smear) | streaked specular, mercury-white | doppler build | commitment |
| 18.5–22.5 | Joust / parallel pass | Power | Rival closes head-on, offset; cone huge-blurred on the opposite edge | chase tracking + joust (closing) | streaked roadside lights, red tail accent | engine duel, doppler swell | rivalry |
| 22.5–26.5 | Finish | Impact | Slicks blown-up and distorted, two cars inches apart across the line | slight high, finish-cam | cold-white finish pool | sound peak → cut | margin |
| 26.5–30.0 | Hand unclenches / chute | Aftermath / Exit | Fingers release the wheel; chute bloomed, smoke drifting through a beam | ECU then rear wide (settling) | single cold rim, residue haze | hard cut to silence, one breath | consequence / release |

板子的笔记：9.5–10.3 持守面板是持守最久的一张静帧——触发爆响的停顿。起跑*不是*一张主角帧；在更完整的片段里，把 10.3–11.6 展开成 6-9 面板微爆发（§3）——正是这个展开把 13 行压缩行带到 §3 约 18-26 面板的计数。褶皱是响亮段落里唯一让时间膨胀的地方。没有两个爆响簇相接；每次爆发都被一张持守的安静面板分隔。以后果收尾，持守约 2 秒——那片真空就是标点。

---

## 9. 清单：这个关键帧是否配得上它的位置

每张面板出厂前运行。失败就删。

- [ ] **功能标签已点名。** Establish / Reveal / Power / Pressure / Detail / Reaction / Shift / Impact / Aftermath / Exit 之一。无标签 → 删。
- [ ] **一个可读节拍**，一句话可说出。若无法题注（setup / commitment / mistake / recovery / proof-of-speed / result），它是 *fantik* ——删。
- [ ] **情绪经由物件**在场——脸会承载的那种感受，冻结在指节/指针/踏板/烟/汗珠里（§5）。无状态变化、无情绪 → 删。
- [ ] **速度或戏剧提示**在场——六种 motion-as-still 提示至少 1 个（smear / partial blur / streak / vector / sharp-blur / held stillness），或刻意的持守静止停顿。"快"面板要带五个速度提示中的 ≥3 个（§4）。
- [ ] **状态变化，而非静态癖好**——物件跨越阈值（怠速→爆闪、干净→冒烟、着地→抬起）。无怠速解剖、无停着的挡杆。
- [ ] **三个深度层**，各带明确职责（FG 框景/遮挡、MG 主体、BG 筹码）。一个焦点；其余每个物件是证据，不是装饰。
- [ ] **隐含运镜已点名**——这张静帧作为其首帧的那个动作，物理上可安装在车上（无上帝角度渲染）。
- [ ] **冷色板保持**——钢/青/洋红/水银白，红和绿仅作点缀，琥珀 ≤15% 且点光源（毒性的，绝不舒适）。一个有动机光源、约 70% 无光、一记硬镜面高光。质感点名（颗粒、光晕、一次 flare），不是"clean"。
- [ ] **无脸**，或脸碎裂到不可用（仅剪影/倒影）。
- [ ] **声音格已填**，尽管面板是静帧——持守帧之下是什么音频、剪切咬在哪（`dramaturgy.md` §11）。
- [ ] **配得上它的密度槽**——持守节拍一张面板，爆响一次爆发；板在静音下读作加速的转速表（§3）。

如果面板挺过全部十项，它就是 *опорный кадр*，不是壁纸。把它作为锁定的首帧交给 `seedance.md` / `kling.md` / `veo.md`。

---

*作者：Serge Shima（[t.me/aimastersme](https://t.me/aimastersme) · [sergeshima.com](https://sergeshima.com) · [aimasters.me](https://aimasters.me)）· 许可：CC BY 4.0 —— 需注明出处 · 来源：[smixs/visual-skills](https://github.com/smixs/visual-skills)*
