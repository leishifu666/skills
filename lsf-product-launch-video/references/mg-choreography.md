# MG 编排研究与纠错

2026-09-19，根据坤坤魔法 v3 反馈、公开教学资料与参考片抽帧整理。属于制作经验与研究结论，不属于《Animated Storytelling》未读章节。

## 先判断哪里断了

- 一张张图片切换：检查是否仅按时间替换图片地址，没有共同主体、方向或容器
- 演示生成功能却静止：检查输入、点击、loading、结果是否真正走了组件状态；导入组件但一直传 idle 仍然是假静态展示
- 原有开场缺前奏：检查渲染是否从动画中途 seek；保留形成、展开、落位的因果，可重新分配时长
- 页面杂乱：只取讲述当前操作的真实局部 UI；本用户要求操作特写不出现顶部导航
- 音效机械：先换选音与节奏设计，不能靠提高音量或增加合成事件数量解决

## 实施顺序

1. 选一个主作品与一条创作流程，给出镜图片建立白名单；排除第三方广告、无关品牌和抢眼文字，不按文件顺序取图
2. 画主要静态构图与相邻两镜的交接对象，说明观众先看哪里、下一步看哪里
3. 分开产品原动画、场景编排、声音事件。产品组件的反馈与 shader 保留，新增镜头、对象运动和转场采用本用户要求的 GSAP timeline
4. 操作链至少包含指针到位、输入/接触、原反馈、状态变化、结果。安全演示回调可以替代后端，但必须驱动可见状态；不得触发真实扣费或伪造性能承诺
5. 相邻镜头明确对象、位置、尺度、方向、遮挡如何交接。优先匹配切、动作切、同容器展开；不要求所有镜头形变
6. 原有首页动画必须从出生阶段检查；把其中有意义的对象交给下一镜，不机械完整录屏，也不截去前奏
7. 图片可做编队、叠层抽取、扇形展开或容器内放大，按故事选择一种；保留一张主图的清晰阅读段，不把每幅作品平均全屏播放
8. 动效方向发生较大变化或上一版被否定时，先渲染最难的 8–10 秒连续段验证交互和交接，再扩展全片。不是每个常规修改都重新等待批准
9. 抽查首帧、状态切换、过渡 25%/50%/75%、稳定帧及尾帧；不能只看终态截图

以上时长是自定工作起点，不是参考作者的精确参数。

## 资料与适用边界

- [Ordinary Folk 制作流程](https://www.ordinaryfolk.co/process)：Message、Design、Animation、Audio 正文；信息和构图先于精修运动，声音在制作早期介入
- [School of Motion：Match Cuts](https://schoolofmotion.com/blog/match-cuts)：匹配对象位置与运动惯性；硬切也可以自然
- [六类转场](https://schoolofmotion.com/blog/six-essential-motion-design-transitions-tutorial)：按场景关系选方法，不以效果数量衡量质量
- [动作预期](https://schoolofmotion.com/blog/anticipation-principle-quick-tip)：动作前引导注意力；不因此给普通 UI 按钮增加违反产品规范的弹跳
- [BUCK：Comfy](https://www.buck.co/work/comfy-brand-refresh)：品牌形状、连接与空间语言。借鉴方法，不复制配色、Logo 或完整镜头
- [launchvideo.dev](https://www.launchvideo.dev/)：公开展示可用于研究；没有购买就不能宣称读过其技能包

本次看过 Nils 原片 8 fps 连续帧；官网功能示例与官方短循环概览 2–4 fps，选定转场 12 fps。Webflow 与 Spline 完整 Vimeo 获取失败，官方循环不冒充完整影片；没有实际耳听参考片。

## 免费采样优先，先听再混

- [Kenney Interface Sounds](https://kenney.nl/assets/interface-sounds)：本次实际下载 100 个 OGG，包内 CC0 明确可用于商业项目；偏 UI 音库，未经试听不能宣称适合精修
- [Mixkit Keyboard](https://mixkit.co/free-sound-effects/keyboard/) 与 [Transition](https://mixkit.co/free-sound-effects/transition/)：本次找到键盘、短空气转场候选，下载访问受限；不把搜索命中记成已获得素材
- [Freesound 许可说明](https://freesound.org/help/faq/#licenses)：逐素材核对 CC0 / CC BY；商业宣传排除 CC BY-NC、旧 Sampling+
- [Pixabay 许可摘要](https://pixabay.com/service/license-summary/)：结合具体素材和完整许可核对；不把免署名等同可独立分发
- [Sonniss GDC 许可](https://sonniss.com/gdc-bundle-license/)：免费包与商店试听不同，不默认下载庞大整包
- [Ableton 声音制作](https://www.ableton.com/en/blog/learn-how-to-make-high-impact-sounds-for-movies-and-trailers/)：学习分层、包络、声像与混音，不照搬电影预告片的重音密度

键盘按输入短组剪辑，点击声对准接触，空气声对准速度峰值，结果才给一次落点；音乐已强调的地方可少放音效。来源、许可、剪辑、信号检查、耳听结果分别记录。本用户已明确否定旧程序合成音效，不能以合成脚本默认交付精修音轨。
