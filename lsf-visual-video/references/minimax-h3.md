# MiniMax H3 路由与集成层

本文件把 LSF 的戏构、镜头与细节规则翻译到 MiniMax H3 官方提示词格式。H3 的字段、标签、说话人和时间表示以 MiniMax 官方 `h3-prompt-writing` skill 为准；LSF 负责先把故事、调度、运镜、表演和声音设计完整。

官方来源：[`MiniMax-AI/MiniMax-H3`](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/h3-prompt-writing)，同步自提交 `d21241f0a4b3acbb34c97dae47fa417b7065e438`。随附的官方参考文件受 MiniMax H3 Community License Agreement 约束，不归入本技能原有的 CC BY 4.0 内容。

## 强制路由

先判断输入模式，然后只读匹配的官方参考：

| 模式 | 适用情况 | 必须继续读 |
|---|---|---|
| T2VA | 纯文本生成完整音视频 | [minimax-h3-base-official.txt](minimax-h3-base-official.txt) |
| I2VA | 一张图片就是视频 0.00 秒的首帧 | [minimax-h3-base-official.txt](minimax-h3-base-official.txt) |
| FL2VA | 图片分别锁定首帧和尾帧 | [minimax-h3-base-official.txt](minimax-h3-base-official.txt) |
| L2VA | 一张图片只锁定视频尾帧 | [minimax-h3-base-official.txt](minimax-h3-base-official.txt) |
| Ref2VA | 图片、视频或音频提供角色、场景、动作、声音、风格等全能参考，而不是固定首尾帧 | [minimax-h3-ref-official.txt](minimax-h3-ref-official.txt)；涉及镜头、对白或运镜时还要读 [minimax-h3-base-official.txt](minimax-h3-base-official.txt) 的第 4 节 |

不要仅凭“上传了图片”就选择 I2VA。角色设定图、多视角角色图、服装图、场景图和风格图用于生成指导时属于 Ref2VA；只有用户明确把图片作为 0.00 秒首帧时才属于 I2VA。

## 官方格式不可替换项

### T2VA / I2VA / FL2VA / L2VA

保持以下三个字段及顺序：

```text
integrated_multimodal_description:

overall_soundscape:

non_diegetic_music:
```

I2VA、FL2VA、L2VA 还必须在第一行使用官方参考图对齐句，具体文本以 `minimax-h3-base-official.txt` 为准。

### Ref2VA

保持以下六个字段及顺序：

```text
subject_definitions:

summary:

retention_analysis:

detailed_description:

overall_soundscape:

non_diegetic_music:
```

引用标签在所有段落中保持同一含义：可复用的可见内容使用 `<Subject N>`；固定画面锚点使用 `<Picture N>`；整段视频结构使用 `<Video N>`；音频信号使用 `<Audio N>`。

## 写作规则

- 官方优化格式要求各结构段使用英文；对白、歌词和画面中真实可见的文字保留原语言。用户若明确要求中文结构，遵从用户，但说明这会偏离官方优化格式。
- 说话人按首次发声顺序固定为 `(S1)`、`(S2)`；同一角色跨镜头不得换号。
- 对白只写在 `<d>` 内，例如：`<Subject 2> (S1) says in a soft childlike voice, <d>[Chinese] 没有啊。</d>`。`<d>` 内不得混入表演、声线或镜头说明。
- `[Shot 1]` 不写时间戳；后续镜头在切点使用严格递增的 `[Shot N] At MM:SS.mmm, ...`。
- 运镜写成自然英文动作，必要时明确类型、幅度和速度，例如 `pushes in with small amplitude at slow speed`。
- `overall_soundscape` 只概括环境声、物理动作声与非语言声音，不重复对白。
- 没有观众侧背景音乐时，写 `non_diegetic_music: N/A`。
- 时长是平台设置，不是提示词能力。随附官方参考记录为 4–15 秒；版本变化先核对实际页面或当前官方文档。用户要单段 17–18 秒而已确认上限为 15 秒时，明确不可执行，不交付伪装可运行的超限成品。优先建议减少可选动作、保留结尾停顿；改变台词、拆段或换模型须符合用户选择。
- 六字段是随附 H3 优化指南的输出结构，不等同于所有界面强制要求的 API schema。用户要精简时可保留字段、每个分析字段压到一行；`detailed_description` 不受 350–500 词的硬下限约束。用户明确要求纯自然语言时可覆盖此约定，不把指南格式说成平台技术限制。
- `retention_analysis` 写各素材保留/迁移的职责，不写剧情卖点；`fully_preserved` 限于已定义的属性，不能既承诺首帧完全照搬又替换它的脸部结构。
- 图像同时定义角色、衣服和场景时分配属性优先级。修正角色图的嘴型优先于旧分镜的歧义嘴型；服装与构图仍按场景图。音频若仅作音色参考，不继承台词、停顿、笑声或完整音轨。
- 素材编号以用户实际上传顺序为准，正文保持同一映射。不要把“有音频素材”自动当作平台支持纯音色提取；若当前入口只有音频驱动口型/整轨复用，说明不能仅靠提示词可靠分离内容与音色。

## 与 LSF 规则的组合顺序

1. 先按 `dramaturgy.md` 确定欲望、障碍、空间、视线、节奏和最终画面。
2. 按 `universal-rules.md` 补齐角色锚点、环境压力、身体微动作和声音母题。
3. 按本文件选择 H3 模式并加载对应官方参考。
4. 把已经完成的导演设计翻译成 H3 官方字段，不再额外发明一套格式。
5. 发送前检查：时长匹配、标签闭合、说话人编号稳定、对白原文未改、切点递增、音乐层分类正确、所有引用都在 `subject_definitions` 中有定义。

若 LSF 的通用输出骨架与 H3 官方字段冲突，以 H3 官方字段为最终提示词格式；戏构、镜头职责、细节和连贯性检查仍由 LSF 规则约束。
