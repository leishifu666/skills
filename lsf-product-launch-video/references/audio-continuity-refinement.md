# 声音选材与运动连续性精修

来源：坤坤魔法 V5 的 2026-09-19 反馈。用户认可视觉方向，要求改善配乐、音效与衔接，明确保持无旁白。此偏好不自动适用于其他用户。

## 不把下载当听审

- 标签、BPM、位深和网站口碑只用于初筛，不能证明音色适合。拿到 WAV 也不等于高质量选择已完成
- 音色候选放进同一段 10–12 秒画面做响度匹配对照；旧版也匹配响度。先完整比较，再单独听音乐与关键接触声
- 未能实际听审时在交付和事件 JSON 标明 `earAudited: false`，不能宣称已解决平淡、刺耳或质感问题
- 选音乐后再按实际乐句与重拍调整旅行段。不能把所有镜头强行缩到固定拍长，也不能用统一加速替代节奏设计
- 一条 whoosh 反复变速会同时改音高和质感，不能作为所有快镜头的默认解决方案。输入、点按、滑动、结果和品牌落点先选各自合适的素材，控制重复密度
- 当前用户要求不使用助手程序生成的音轨。专业录音或设计师制作的授权声音可选，剪辑、包络、声像及响度处理仍可用代码完成

## 可用素材入口与边界

- [SND](https://snd.dev/)：SND02 piano（Ayako Taniguchi，钢琴与实验演奏）、SND03 industrial（INDUSTRIAL JP，机械录音再编辑）。本地实测每套 27 个 WAV；来源允许免费商用，禁止未加工素材单独再分发或直接当声音商标。不要把这些 WAV 随 skill 发布；保留来源和许可记录，按需从官方下载
- [Incompetech](https://incompetech.com/music/royalty-free/licenses/)：免费路线需署名。District Four（176 BPM）、EDM Detection Mode（128 BPM）曾做对照样片，尚未听审定稿，不是所有产品的默认配乐。署名包含作者 Kevin MacLeod、来源、CC BY 4.0 链接和修改说明
- [Mixkit](https://mixkit.co/free-stock-music/tag/technology/)、[Pixabay](https://pixabay.com/music/corporate-digital-abstract-technology-248835/)：可继续初筛；本次下载 403，不能记作素材已入库
- [Sound Response](https://www.soundresponse.net/free-whoosh-sound-effects/)、[99Sounds](https://99sounds.org/cinematic-sounds/)、[Adobe](https://www.adobe.com/products/audition/offers/adobeauditiondlcsfx.html)：官方转场与音效库候选，逐项核对许可；本次未取得对应音频，不能声称已试听或可复用。Royalty-free 不代表没有使用、署名或再分发限制

## 三种必须实际检查的接缝

1. **同图换载体**：比较图片内部的可见矩形、眼睛等稳定特征位置、裁切、缩放和圆角。只对齐外壳不够。V5 在 11.25 秒从节点进入画廊时出现裁切跳变；以原帧率抽帧确认。运动中交接不能成为掩盖错误几何的借口
2. **速度归零**：逐段记录旅行的速度峰、停顿和下一段开始。V5 两次穿梭后存在 0.45 / 0.33 秒停住，再重启。旅行中保留余速；真正需要读屏时才停稳。避免每个 GSAP tween 都独立完整 ease-in-out
3. **换遮罩**：V5 在 16.875 秒直接把方图切成 Logo 后再放大缩小，形状没有变化过程。应在收拢运动中逐步揭示 Logo 负形，并保持同一图片的定位；遮罩与缩小重叠，避免额外一拍的弹跳

这些是该片诊断，不能机械禁止所有硬切或停顿。硬切在叙事和节拍需要时仍然有效。

## 阅读依据

- [School of Motion · Six Essential Motion Design Transitions](https://schoolofmotion.com/blog/six-essential-motion-design-transitions-tutorial)：已读正文，匹配剪辑、动作剪辑及形态变化；未声称完整观看课程
- [Sander van Dijk 访谈](https://schoolofmotion.com/blog/sander-van-dijk-podcast)：已读连续运动相关段落；每幅构图是运动中的时刻，不要求处处停顿；未声称听完播客
- [Flashmotion 作品集](https://flashmotion.io/portfolio)：Bolt Slides 已在上一轮观看与抽帧，7.75–10 秒是阵列转 UI 参考。研究视频与可用于我方成片的声音分开记录

验证留存：原帧率接缝抽帧、代码事件与速度停顿、同画面声音对照、许可、完整解码与播放器检查。技术验证和审美接受分别记录。
