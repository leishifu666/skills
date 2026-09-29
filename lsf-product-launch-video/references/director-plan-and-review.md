# LSF｜导演计划与审看

用于把拉片观察变成下一支片子的决策。配套 `assets/director-plan.example.json` 是“一杯奶茶变成产品海报”的新策划模板，不是已渲染成片。时间由这段内容需要决定，模板数值是原创起点，不是参考作者的参数。

## 先决定观众看什么

1. 为每镜写一句 `viewerTakeaway`：看完新知道什么。接着选 `role`（attention / claim / proof / payoff / context / brand）与 `presentation`（native-ui / artwork / typography / concept）。一镜一个主要任务即可，不要求六类齐全或规定 UI 占比
2. 按任务选技法卡，核对其 `selection` 的条件、素材和下一镜接口。模板允许成果先亮相，再回到原图和真实 Agent 创作；这不同于把生成完成声提前到提交之前
3. 指定焦点成立的区间 `readability.startFrame/endFrame`。`mode: read` 表示稳定读字/理解操作，`recognize` 表示只需识别主体或变化。解释停留理由；不把 Pen 的约 0.33 秒照搬给长中文输入。时长由两端相减，避免另存一个会失配的 hold 数值
4. 写相邻镜头 `continuity.kind/basis`。可用 object / action / composition / direction / semantic；只有 object 必须标识实际承接素材。直接切镜可令 startFrame = cutFrame = endFrame，不硬塞遮罩、飞行物或 whoosh
5. 定义视觉 `syncTargets`：`cut / land / reveal / contact / settle`，记录发生帧。音乐和采样围绕这些目标编排；镜头可以提前旅行，到位才是强调时刻。不是每个目标都必须响

真实 UI 段仍需展开原生事件、指针、输入分组和源代码证据；复用三段输入交接示例。抽象镜头不能代替产品能力证据。模板中的 Agent 会话回放不等于实际在线模型执行，新片须重新核对当前实现。

已有项目按 [UI 呈现选择](existing-project-mode.md) 为镜头记录原生复用、呈现优化或宣传重绘及选择理由。原生与仅改变外部包装的优化段使用 `presentation: native-ui`；重绘界面使用 `concept`，无需为其接入原生事件。把功能依据、组件/页面/录制素材来源、数据替换、重绘差异和验证范围写入既有 `evidence` 及导演文档。外观可以重做，功能证据仍来自当前项目；不增加校验器不支持的枚举或把概念画面称为实录。

## v2 字段与工具边界

- 设置 `schemaVersion: 2`；保留基础 fps、durationFrames、width、height、scenes、events、music。全部帧为主时间线绝对帧，主镜头和阅读区间左闭右开
- `assets` 登记素材 ID、用途和准备状态；`referenceLibrary` 登记具体区间及观看证据。每镜用 `assetIds / referenceIds` 指向登记项，不能用一个整片 URL 代替逐段观察
- 每镜保留 message、focus、action、evidence；action 可以是图形行为，不强制都是点击。增加上述 role、presentation、viewerTakeaway、readability、syncTargets
- 每对相邻镜头一条 transitions：from、to、reason、technique、startFrame、cutFrame、endFrame、continuity。cutFrame 对应二者边界；剪辑余量可覆盖两镜，不重复执行原生点击
- 每条音效 `syncTargetId` 指向视觉目标。`peakOffsetFrames` 是采样内拟对齐落点相对起音的偏移，尚未选音可为 null；不把文件起点当听觉重音。已知时要求 cue.frame + peakOffsetFrames = 目标帧。需要提前进入或延续时延长事件、调整采样入点，仍把主要强调对准所声明目标
- `music.bpm` 可为空，不强迫用算法值填空。`anchors` 记录 frame、evidenceLevel、evidence；分 audio-measured / beat-estimated / audition-confirmed。最后一种必须有 music.audition 的 reviewed、reviewer、evidence 记录。听审记录是声明，脚本不替人听
- `reviews` 分 nativeInteraction、visualContinuity、creative、audio，各含 status（pending / passed / needs-revision / not-applicable）和 evidence；完成审看写 reviewer，非适用写理由。传入 `passed` 只表示存在该声明，不证明事实
- `nativeInteraction` 只核对本片实际包含的原生交互。全片无原生操作可填 `not-applicable` 并说明；混合片按原生镜头记录范围与未完成项。重绘的状态编排在 visualContinuity / creative 中审看，不能代替原生测试

`scripts/validate_plan.py` 保留 `validate(plan) -> errors`，旧计划和旧调用方仍可用；CLI 另输出警告、审看声明和 `qualityVerdict: not_assessed_by_validator`。v2 校验镜头字段、区间、引用、相邻关系和声音目标；不会恢复缓动曲线、判断画面是否丝滑、访问在线来源、验证素材许可或代替听审。新增字段不会自动驱动现有渲染器，须在片子工程里接入。

## 正常速度审看

对实际导出而非计划填写记录；用成片路径、版本与时间码标明证据。记录没做时保持 pending，不能因校验通过一键改成 passed。

- **信息**：不看制作注释，能否说出产品帮谁完成什么；是否连续多镜都在点按钮，却没有新的信息；概念字卡是否由后面的真实操作支撑
- **节奏**：短镜头能辨认主角，输入和成果有阅读余地；运动旅行与停住之间有变化，而不是整片均速或每镜同一条推拉
- **连续性**：先原速看接缝是否自然，再逐帧定位视线、裁切、速度或动作相位问题。硬切可以通过；有同一对象也不自动通过
- **交互**：原生镜头检查鼠标抵达后的 hover，以及输入、引用、提交和 Agent 画布结果，画布不混入桌面 UI。重绘镜头检查焦点、指针、状态编排与真实任务是否一致；说明重设计范围。分别记录运行或渲染画面证据，不用组件文件名替代
- **声音**：实际听打字与接触轨，再听全混音；成果重音是否落在显现/到位，留白和尾音是否成立。当前工具不能听就保留 pending，可交用户试听，不能写音质已通过

发现问题回到对应镜头和邻接缝局部修改。结构通过、技术解码通过、原速视觉审看和听审是四种不同证据；最终交付分别说明，不合并成“全部验证完成”。
