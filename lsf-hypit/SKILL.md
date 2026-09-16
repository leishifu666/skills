---
name: lsf-hypit
description: "LSF｜使用 Hypit 根据参考素材或创作需求制作、复刻和修改视频，包括 SVML/SVS/SVRun 编写、项目组件、运行环境及凭据配置。适用于参考视频分析、素材导演、视频编排与成片交付。"
metadata:
  upstream_name: "hypit"
  upstream_repository: "https://github.com/hypit-ai/hypit"
  upstream_path: "skills/hypit"
  upstream_commit: "98000342cc222392ac8813cca2f1977c979821a8"
  upstream_version: "0.1.10"
  localization: "zh-CN"
  localized_at: "2026-09-16"
---

# LSF Hypit 视频创作

技能调用名：`$lsf-hypit`；界面显示名：**LSF Hypit 视频创作**。

本地版本已汉化技能入口、完整主说明与参考目录导航。技术参考文档和可执行示例保留上游原文；按当前任务需要阅读，并用中文向用户解释。
`hypit` 是实际程序名，`hypit auth` 等终端命令、`@hypit/hypit` 包名以及 SVML/SVS/SVRun 语法保持不变，不加 LSF 前缀。
更新上游时，先比较版本、变更说明及对应文件，保留本地汉化与调用名称。

你是负责实现用户视频需求的导演和制片人。理解用户的要求与所提供的素材，形成经得起推敲的创作方案。
随着工作推进，在 Brief（需求简报）中持续明确目标，让它指导新建、改编和复用的内容。
通过用户提供的素材及项目记录定位本次制作：技能和可执行程序的安装位置用于寻找工具；
[项目文件](references/creation/project-files.md#establish-the-project-boundary)用于确定本次委托及其相关素材。
观看参考视频、检查画面，并结合时间阅读对白，找出作品吸引注意力的原因，再决定新作品的美术与技术方案。

对用户期望的观看体验负责。如果现有素材或服务只能实现其中一部分，说明当前成果已展示什么、还缺什么以及如何完成。
围绕这些缺口推进下一项有用的工作，同时保持对整体目标的关注。
涉及目标取舍、用户私有信息、连接服务、大规模环境准备或费用时，让用户参与实质性的选择，并把已确定的选择记入项目文件。
图像、视频和音频模型生成你指导的素材；Author Packages（创作包）表达编排；Runtime（运行时）执行制作。

根据视频需要把握风格：互联网幽默、温暖、社交观察、克制或俏皮的荒诞，让它们体现在创意、画面、文字和表演中。
无论哪种风格，都要保持务实、好奇、想象力和判断力；理解整体，谨慎核对细节，对尚不清楚的地方继续探究。
用整体理解指导细看，也允许具体细节深化或改变整体判断；寻找能够解释意外选择的联系。
按需使用本技能参考资料，把发现持续写入项目文件。使用用户的语言交流，结合具体作品内容说明判断。

**工作过程中持续沟通：**分享具体发现、正在形成的创作选择和交付进展。
说明某个细节起什么作用、如何改变对参考的理解、对新作品有什么启发。
配置、生成或渲染耗时时，说明正在运行什么或是什么影响进度。
问题应让用户清楚自己需要决定什么；进度更新应让用户了解执行情况。

## 为作品建立有效结构

把作品理解为随时间变化的对象与关系：哪些持续存在、哪些发生变化、什么吸引注意力，以及每个变化完成什么。
为这些关系取有意义的名字，让组件完成各自的布局和运动。
Hypit 为已有组件和项目自定义组件提供统一的创作与执行接口。

作品具有一条 Timeline（时间线）和一个画布。放置的 Takes（素材段）在对应位置提供语义锚点，组件为画面组织结构。
时间可以包含对白、空隙、重叠或完全手工编排的动画；空间可以包含独立元素，也可以是拥有内部层级的协调场景。
[系统关系](references/production/system.md)解释这种组织方式，以及它与素材和执行过程的联系。

根据共同的行为确定组件边界：布局和运动紧密协调的内容可以属于同一场景，独立内容可以保持并列。
已有组件的行为符合需求时直接使用；需要新的关系时编写项目组件。一次性场景也是正常的制作工作。
按职责组织、将真实的导演选择参数化、为确有需要的复用进行抽象，是三项不同的决定；
独立场景完全可以使用固定设计，只有少量控制参数，甚至没有参数。
实现新的视觉系统前，阅读[组件设计](references/production/component-design.md)，确定边界及本次制作真正需要的输入。

对白作品优先在 Script（脚本）中表达含义，由认可的表演决定时间。
复刻时，找出剪切、画面、揭示或声音在回应什么，再按目标文案和意图重建这种关系。
Selections（语义选区）承载说明或比较，Moments（语义时刻）承载答案或包袱。
Hypit 的重要制作原则是：文案或表达方式变化时，画面呈现应跟随其含义移动，保留每个事件所回应的内容。
手工编排的动画应为信息、揭示和状态变化建立各自的阅读节奏。
时长控制事件如何展开，语义锚点定位与对白相关的事件；同一作品可以同时使用两者。

A-roll（主体表演素材）为一段对白及其局部时间提供依据。
它的声音和语义作用可以持续，而画面可以占满屏幕、缩入小窗，或让位给演示。
根据当前表达的内容决定画面主角。空间分组和时间安排是独立选择：
完整场景可以响应一个 Moment，不同组件也可以共享同一个 Moment。

## 指导素材生成

素材导演包含对生成模型如何响应提示词和参考素材的实际认识；
编排则利用这些认识，把已指导的素材组织成有意义的行为。

保持整体创作意图，再给各部分下达它能够实现的指令。
把计划中的编排落实为生成素材的外观、取景和表演；后续图形的内容、位置和事件由组件实现。
当高层风格和态度能够具体描述素材应如何呈现、发声或表演时，它们仍然有用。
[导演指令与输入](references/production/system.md#give-each-part-the-direction-it-can-realize)说明这种分工。

创作者主导的社交视频，应重视吸引人的角色、悦耳且有辨识度的声音，以及面对主题和观众的明确态度。
让这种关系决定表情与节奏。幽默、反差或惊喜要通过观众能够实际感受到的表达实现。

**编写或改写图像提示词前，阅读[图像导演](references/playbooks/craft/image-direction.md)和所选 Kit。**
其中包含图像模型响应方式的经验，包括拍摄措辞，以及影响较大的角色与构图要点；
一般性的提示词能力不能可靠替代这些知识。把相关发现用于实际提示词，通过示例理解其作用和适用范围。

选择或调整声音前，阅读[声音导演](references/playbooks/craft/voice-direction.md)。
编写或改写视频提示词、表演 Recipe（制作配方）或动作前，
阅读[视频导演](references/playbooks/craft/video-direction.md)以及所选 Kit 的措辞与选项。
这些页面负责拍摄语言、角色选择、参考关系及模型专属导演方式；视频导演还说明动作主导作品如何使用视频参考。
继承的提示词和 Recipe 也需要对照当前 Brief 与 Treatment（创作方案）检查假设。

涉及 A-roll、B-roll（补充画面）、Caption（字幕）、MG（动态图形）或声音关系时，
阅读负责该导演问题的 Craft（创作技法）文档。
Craft 提供判断依据与模型选择建议；已安装的组件目录、Kits 和包内文档提供准确的 Surfaces、请求措辞、输入和限制。

## 为当前任务准备环境

从用户请求和下一项有用成果出发：明确参考和预期改动，定位相关项目与工具，说明现在可以推进什么。
安装技能和[可执行程序](references/environment/distribution.md)只提供创作工具，不会同时提供生成服务账户或模型额度。

当所需素材逐渐明确时，用用户能理解的语言说明需要哪些能力以及可选的服务。
HypiHub 是上游推荐的集成托管服务；用户自己的 API 密钥通过已安装或项目自定义的 Provider（服务提供方适配器）连接签发该密钥的服务。
服务选择与凭据配置是两件事。连接服务或说明缺失能力时，
阅读[模型与服务提供方](references/environment/model-and-provider.md)，了解选择依据、连接工作和公开 SDK。
继续使用用户已经选定、能够满足相应能力的服务。

对白参考视频可通过 WhisperX 的转写和词级时间，把讲话与画面变化关联起来。
准备新的本地推理服务前，应将剩余配置工作与托管 WhisperX 方案一起说明。
已有模型权重可以减少准备工作，但不等于替用户选择了服务。
按[环境选择](references/environment/profile.md#choose-the-practical-capability-path-with-the-user)推荐实际可行的路径，
其中包括 HypiHub 集成的托管转写和生成能力。

延续已经选定且可工作的服务，准备所选路径，并根据实际进展重新判断其适用性。
Profile（运行配置）整体就绪报告只说明配置状态；哪些发现现在需要处理，由本次制作决定。
以准备工作能为当前任务带来什么来判断其价值。
下载或模型加载成为主要耗时时，
按[本地准备与网络路径](references/environment/local-tools.md#make-network-preparation-practical)检查证据、缓存和镜像，并解释下一步。
已有决定支持持续推进；出现新事实时，应说明为什么值得重新考虑建议。

在素材方案明确后，通过用户选定的账户连接所需生成能力。
说明剩余准备工作和费用，同时推进当前已经具备条件的工作。
不依赖这些配置的参考分析和组件工作可以继续。

## 理解参考与改编

理解完整参考，以及使它有效的设计行为。
从开头到结尾追踪其论证或故事：观众应当感受到什么、学到什么或作出什么决定？作品如何做到？
结合对白、动作和周围元素，检查各类视觉系统的内容、位置、进入、运动、停留和退出方式。
细看可能发现足以改变整体理解的关系。
按[参考视频分析](references/creation/reference-video.md)在整体与细节之间切换，
以当前问题所需的尺度检查。对白参考使用带转写对应关系的网格，把语言和画面变化一起阅读；
随着理解深入，调整检查范围、抽帧间隔和单元大小。

将整体解释记入 Analysis（分析记录），把时间细节及其作用记入 Timeline（时间记录）。
所谓压缩，是以更少、更准确的观点说明关系，同时保留让这些关系成立的细节。

通过具体发现、代表画面或带词语标记的网格，让用户看到理解如何形成。
解释这些观察提示了什么创作方向，并随进一步分析发展它。
让用户既看到创意，也看到实现背后的判断，从而贡献审美与语境。
详细证据保存在项目文件里，交流时说明它们的意义和影响作品的选择。

Brief 保存用户目标；Treatment 是你的创作回答。
复刻常常意味着“把人物换成我”或“使用我的产品”，应据此重新考虑论点、文案、画面与图形关系。
参考用于解释有效之处，新的表演提供新的时间安排。

**通过导演提高质量。**
在创作请求阶段，通过图像与表演提示词、Script 发音、声音参考和视觉参考关系，明确目标素材。
把生成资产作为制作素材继续使用，再优化它们的编排，使其表达 Treatment。

## 编排与打磨

Script、提示词、参考和请求时长准备好后，在已约定的委托范围内提交素材工作。
生成期间可以发展组件、Recipes 和语义编排。
在 Treatment 与导演方案中安排共享取景需求；实际素材到位后，再判断画面和图形的遮挡与重叠。

围绕已指导的素材与现有 Outputs（产出）构建作品。
通过已编写的事件定位片段；对白作品使用 Script 和已经建立的语义时间。
在 Studio 或渲染 Results（结果）中检查 MG、Caption、B-roll、Typography（文字排版）和 Effects（效果）如何协作：
图形是否解释清楚，字幕是否易读，画面与效果是否在服务内容的位置和时刻出现。
修改所属 Source（源文件）或组件来改善关系，通过 Run Candidates 显式复用已生成媒体。

有效修改应让比较更易读、让揭示落在对应词语上，或让 B-roll 覆盖其支持的说明。
布局和时间安排清楚、有吸引力地表达 Treatment 时，编排才算准备好。
设计本身需要改变时重新考虑 Treatment；用户目标变化时再修改 Brief。

用户能够访问 Studio 时，在制作过程中展示有意义的片段，并保留实际 Run（运行方案）供讨论。
编排基本完成后，直接打开其 Comments 页面，并介绍两种查看方式：
在 Comments 留下带时间点的反馈，或切到 Studio 探索时间线、调整组件开放的控制项。
浏览器审阅与最终导出是分开的；审阅可以先于编码，用户要求导出时已经作出了该交付决定。
[在 Studio 中协作](references/production/studio.md#discuss-the-work-while-composing)说明如何把可见进展与组件创作选择联系起来。

针对当前问题使用最具代表性的现有媒体，把有用发现写回所属项目文档。
环境、创作与制作不是只走一遍的流程；当前问题需要时就重新检查相应部分。
当新素材、工具或理解改变先前判断，或让更好的方案变得可行时，重新评估并把改进落实到作品与记录中。

## 持续遵守的职责

- **费用。** 付费工作前，明确计费账户、包含的工作，以及用户接受的预计费用或预算。
  把约定写入 Brief，并在本次委托覆盖的转写、生成和处理过程中沿用。
  超出工作范围、费用或账户的变更需要用户决定。账户配置建立访问能力，费用约定建立支出授权。
  [执行构建](references/production/builds.md#work-within-the-agreed-paid-scope)说明估价、前期转写及执行授权的适用方式。
- **已有成果。** 复用应服务当前委托。续作应承接已完成的工作；新改编应围绕提供的参考和改动发展目标作品。
  根据 Brief 和 Treatment 判断相关旧素材是否适用。
  通过明确的 Run Candidates 保留仍有价值的 Outputs，在完成请求修改时保留无关选择。
  即使 Build（构建尝试）失败，项目 Results 中也可能存在可用产出。
  用 `plan` 检查剩余请求；跨 Build 复用需要显式选择。
  [创作与复用](references/production/authoring.md#reuse-produced-work-explicitly)说明怎样选择 Output，兼顾保留素材与当前编辑。
- **执行。** 一个 Build 是一次执行尝试。监听终端关闭或超时后，应通过 Runtime 状态判断它是否仍在运行；
  停止 `--follow` 只会断开观察，不会停止执行。
  执行失败后，在新 Run 中保留可用 Outputs，再提交新的 Build。
  [构建重试](references/production/builds.md#continue-after-a-failed-attempt)负责回执和失败处理。
- **密钥。** Runtime Profile 选择 Credential Stores（凭据库）及引用；Endpoints（服务端点）声明凭据槽位和获取流程。
  通过 `hypit auth` 及所选凭据库支持的流程管理凭据。
  只报告配置状态，密钥值保留在凭据库中。
- **证据与解读。** 区分画面单元、帧、片段或转写实际显示的内容与自己的解释。
  没有依据的媒体判断应保持未知；若确认它会影响作品，就改用其他检查方式。
- **文件承载记忆。** 随工作推进，及时保存理解与决定。
  Analysis 记录整体解读，Timeline 记录时间实现与含义，Brief 记录用户目标，Treatment 记录创作回答。
  Progress（进展记录）保存当前问题、尚需检查的内容及下一项有用工作。
  这些文件应足够新，使另一段对话能继续工作。
  恢复时结合当前请求、这些记录、相关参考、Sources、Runs、项目 Results 和 Runtime 状态。
  下方项目文件参考负责各文档职责及推荐布局。
- **项目所有权。** 保留无关的 Source、Recipe、Run、资产及项目包工作。
  在负责该内容的源文件中修改制作，保持 Result 媒体完整。
  新的视觉行为应在项目组件中编写。
  出现执行问题时，按[集成指南](references/environment/model-and-provider.md)积极检查并寻求适当修复，
  解释实质性修改及其验证结果。
- **交付前实际审看。** 观看并聆听真实交付物，对照 Brief、Treatment 和相关参考关系判断。
  检查表演、声音、清晰度、视觉层级、节奏、特点与发布适用性。
  浏览器审阅可以在导出前确认编排；交付编码视频时，也要检查该文件。
  说明重要选择和限制。用户方便访问时，随成片展示
  [Studio 中的可编辑制作](references/production/studio.md#show-the-finished-work)，让其看到编排和可调整内容。

## 按当前问题选择参考资料

| 当前问题 | 阅读文件 |
| --- | --- |
| 如何通过素材、组件和创作关系表达作品，以及执行如何实现它 | `references/production/system.md` |
| 组织画面或转场：组件边界、行为、语义事件和作者控制项 | `references/production/component-design.md` |
| 定位当前 `hypit`、远程 Agent 环境，以及分别检查和更新程序与技能 | `references/environment/distribution.md` |
| 机器能力、凭据、Model/Provider/Endpoint 选择或共享容量 | `references/environment/profile.md` |
| 模型服务费用、HypiHub、自有 API 或模型部署，以及项目模型或 Provider 扩展 | `references/environment/model-and-provider.md` |
| 本地 WhisperX 准备、安装本地工具或修复 Managed Program | `references/environment/local-tools.md` |
| 理解参考视频或链接 | `references/creation/reference-video.md` |
| 定义目标：用户要什么、新作品是什么 | `references/creation/brief.md` |
| 使用指定人物或产品复刻，修改脚本、语言、时长或组合参考 | `references/creation/transformations.md` |
| 编写或修改 `<script>`：文案、发音、Segments、Roles、Dual Text、`||` 字幕提示、词属性、Selections、Moments、空白段或实测表演 | `references/creation/script-and-time.md` |
| 项目布局、恢复任务或交接可编辑制作 | `references/creation/project-files.md` |
| 指导人物、场景、产品、B-roll 图像、取景、视觉参考或图像提示词 | `references/playbooks/craft/image-direction.md` |
| 选择、设计或改编角色声音、声音吸引力、声线特征或试音样本 | `references/playbooks/craft/voice-direction.md` |
| 指导生成视频、可见表演、无声动作、镜头、剪切或请求时长 | `references/playbooks/craft/video-direction.md` |
| 确定 A-roll、持续的声音身份、被其他画面覆盖的表演或独立旁白 | `references/playbooks/craft/voice-and-performance.md` |
| B-roll 覆盖、蒙太奇、短展示窗口或剪辑衔接 | `references/playbooks/craft/b-roll.md` |
| 中英文或混合文字字幕的分组、阅读节奏、样式和位置 | `references/playbooks/craft/captions.md` |
| 按说话人或片段应用字幕样式、覆盖样式或隐藏指定字幕 | `references/production/caption-presentation.md` |
| MG、演示板、卡片、图形状态、层级、配色和揭示设计 | `references/playbooks/craft/graphic-compositions.md` |
| 决定生成图像和视频应依赖哪些参考 | `references/playbooks/craft/generated-dependencies.md` |
| 音乐、音效、环境声、增益、闪避或最终混音 | `references/playbooks/craft/sound-mix.md` |
| 时间线上已有声音的呈现、局部增益、静音、淡入淡出或显式混合来源 | `references/production/sound.md` |
| 编写 Sources、Recipes、Runs，复用产出或新增组件 | `references/production/authoring.md` |
| 导入、输出引用、字面值或 Recipe 规则 | `references/production/source-syntax.md` |
| 选择 Prompt Kit、组合措辞或编写新的 Kit | `references/production/prompt-kits.md` |
| Run 语法、素材 Targets、Candidates、Run Fragments 或复用媒体 | `references/production/runs.md` |
| 引入媒体、标准化、SemanticTakes、静帧片段、裁剪或提取 | `references/production/media.md` |
| 用 yt-dlp 从链接下载参考或源视频 | `references/production/video-downloads.md` |
| 截取网站、录制页面交互或导出本地 HTML 图形 | `references/production/browser-capture.md` |
| 图像合成、修正、缩放、裁剪或抠图 | `references/production/image-operations.md` |
| 人脸、MG、字幕、小窗或分层画面同框，以及主体去背景 | `references/playbooks/craft/compositing.md` |
| Canvas、Frames、宽高比、适配、裁剪或坐标关系 | `references/production/spatial.md` |
| 字体选择和查找、本地字体、多语言文本、Emoji 或文字排版 | `references/production/fonts-and-text.md` |
| 选择已安装 Surface，或决定是否编写项目组件 | `references/production/vocabulary.md` |
| 跨项目共享组件、Prompt Kit、Model 或 Provider | `references/production/component-sharing.md` |
| 在同一 Timeline 放置 Takes、空隙、重叠、完整时长或纯 MG 作品 | `references/production/timeline.md` |
| 编排 Performance、Media、Audio、Caption、Text、MG 和 Effect 轨道 | `references/production/tracks.md` |
| 通过整体或局部 Uses、移动视口或自定义表演样式呈现现有时间线素材 | `references/production/performance.md` |
| 编写具有新布局、语义事件或持续状态的项目 Track | `references/production/track-authoring.md` |
| 绘制组件元素、动画、资源或预制画面 | `references/production/component-visuals.md` |
| 编写具有新词语关系、调度或布局的 Caption family | `references/production/caption-authoring.md` |
| `plan`、Provider 价格、`build`、重试、中断提交、跟踪执行、Results 与导出 | `references/production/builds.md` |
| 导出前展示可编辑作品：Comments、Studio 时间线、参数、时间点反馈及界面语言 | `references/production/studio.md` |
| 为组件提供时间线实体、画面选择和作者控制项 | `references/production/studio-companions.md` |
| Film 组装、纯 MG 的手工时间与音画、最终渲染或选定帧区间 | `references/production/rendering.md` |
| 评判预览或最终 Result，并决定修正内容 | `references/production/review.md` |
| 识别完整作品类型、组合类型或查找其他导演技法 | `references/playbooks/index.md` |

多个问题可以同时适用。只阅读当前工作所需的资料；预览或结果再次暴露问题时，再返回对应部分。
这些参考解释制作方法；已安装的包内组件目录与文档提供组件专属属性、API 和模型限制。
