# 阅读依据与转化范围

主书：Liz Blazer，*Animated Storytelling: Simple Steps for Creating Animation & Motion Graphics*，第 2 版，Peachpit，ISBN 9780135667859。出版社产品页发布日期为 2019-06-24，样章版权页标为 2020；不把二者混称为不同版次。

- [出版社书目](https://www.peachpit.com/store/animated-storytelling-9780135660386)
- [出版社 PDF 样章](https://ptgmedia.pearsoncmg.com/images/9780135667859/samplepages/9780135667859_Sample.pdf)
- [第4章网页正文](https://www.peachpit.com/articles/article.aspx?p=2979068)，含第 1–5 页。

2026-09-19 实际阅读：第 4 章 Storyboarding 的全部公开正文、配图、总结和作业；PDF 第 12–30 页，书内对应第 75–93 页（目录将章节入口列为 74）。没有阅读整本书。

逐节覆盖：

| 内容 | 书页 | 转化为视频制作动作 |
|---|---|---|
| Build the Storyboard，含 Thumbnailing 和两轮修订 | 77–80 | 先排可重排镜头卡，卡片写动作和结果；画面不成立时先改分镜 |
| Storyboarding Hints：Shot Composition / Framing / Staging | 80–87 | 每镜头明确观众该看什么，用景别和层级分配信息，删除无关装饰 |
| Transitions and Continuity | 87–89 | 检查空间、事件顺序和运动方向；每处转场写清保留的视觉线索 |
| Timing and Animatics；Time and Sound | 89–91 | 先设总长度，再排镜头时长和暂定声音，用动态分镜暴露节奏问题 |
| Storyboarding Recap / Assignment | 92–93 | 带时间限制跑一个新题材，记录修改与验证，而非只复述概念 |

选择理由：该章直接覆盖从粗分镜走向动画制作的决策，比只教软件按钮的资料更适合转成智能体流程；包含让声音在正式动画前进入时间线的方法。

阅读边界：第 7 章 Sound Ideas（目录 126–141）、第 10 章 Animate!（176–189）没有获得完整正文，未声称读过，也不根据二手书评重建它们。帧数预设、音量约定、Remotion 接入、合成音效和检查脚本都是为本任务原创的工程补充，不是作者原话或参数。

此文件是方法应用记录，不收录书的原文、插图或案例复刻。需要更深入声音理论时，可在取得合法正文后补读，保持来源边界。

## 2026-09-20 补读：动画制作工作流

Julian Shapiro，*Web Animation using JavaScript: Develop and Design*，Peachpit Press，2015，ISBN 9780134096667。

[出版社公开样章](https://www.peachpit.com/content/images/9780134096667/samplepages/9780134096667.pdf)。已完整阅读第 4 章 **Animation Workflow**：PDF 第 17–40 页，书页 **54–77**，含本章总结。PDF 共 52 页，SHA256 `a510b851a3066a3fdfb6f1ed1ac9b7235fb67ed0ac97adaadd141a70c591f5dd`。未读全书，第 3 章运动理论、第 7 章性能仅见目录，不能声称读过。

选它是因为当前失败发生在编排和调试，章节正文能合法完整取得。它采用旧版 Velocity；只迁移工作方法，工程实现用现有 GSAP，不照搬旧 API。

| 已读内容 | 书页 | 本任务的应用 |
|---|---|---|
| CSS animation workflow | 56–58 | 保留简单原生 hover，复杂镜头另排时间线 |
| Separate styling from logic | 59–64 | 外观 token 与镜头参数分开存放 |
| Organize sequenced animations | 65–68 | 用命名动作序列管理顺序及重叠 |
| Package your effects | 69–72 | 封装完整动作，明确初态、终态和复位 |
| Design techniques | 73–76 | 时长与延迟一起缩放，慢放找接缝，再回到原速判断 |
| 本章开头与总结 | 54–55、77 | 检查修改成本和反馈循环 |

下列是本任务原创工程补充，并非书中参数：共享坐标、事件命中检查、五次曲线、鼠标速度阈值、帧级采样、GSAP 接入和检验脚本。详见 [可执行步骤](interaction-continuity.md)。

另查 Ryan McLeod 的 *Animation Handbook*；旧公开 PDF 地址返回 403，新书目页可见介绍，未取得正文，未作为本次已读章节。
