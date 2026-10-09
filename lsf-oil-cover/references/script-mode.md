# AI 教程：原版脚本模式

本入口仅支持原版 AI 教程风格。设计分享采用 Agent 自主模式；本脚本未接入多平台圆形头像版式。

## 制作前确认

先按主 `SKILL.md` 确认源内容与主标题，再确认平台、比例和 AI 教程风格，之后才运行生成脚本。以下参数默认值只说明脚本行为，不代替用户选择；没有确认时可分析和准备，不运行生成入口。

## 默认入口

将实际存在的生成脚本绝对路径记为 `OIL_COVER_SCRIPT`。默认运行以下命令；有字幕时额外添加 `--subtitle "<实际纯文本字幕路径>"`，没有字幕时省略该参数：

```bash
node "$SKILL_DIR/scripts/credential-ui/src/profile.ts" run default -- python3 "$OIL_COVER_SCRIPT" \
  --video "<视频路径>" \
  --title "<提炼后的封面主标题>" \
  --topic "<补充背景>"
```

如果用户提供的是截图或已选关键帧：

```bash
node "$SKILL_DIR/scripts/credential-ui/src/profile.ts" run default -- python3 "$OIL_COVER_SCRIPT" \
  --image "<截图或关键帧路径>" \
  --logo "<可选 Logo 路径>" \
  --title "<标题或主题>" \
  --topic "<补充背景>"
```

仅在用户已确认三画幅时不传 `--aspect`；脚本会并行生成小红书 `3:4` 竖屏版、通用/B 站首页主封面 `4:3` 横屏版和 B 站个人空间伴随版 `16:9` 横屏版。发布 B 站时默认上传 `_4x3.png`，平台再同步生成个人空间 `16:9` 版本。只重跑单个画幅时使用 `--aspect 3x4`、`--aspect 4x3` 或 `--aspect 16x9`。

## 进阶参数

- `--subtitle <脚本/字幕/转录文件>`：把上下文喂给 Gemini，帮助判断主题、标题措辞和证据选择。有完整文稿时优先加上。
- `--logo <Logo 路径>`：可多次传入多个产品 Logo 作为参考资产。
- 自动 Logo 匹配只把 `--title` 和 `--topic` 当作主产品依据。只要其中任一存在，就不再扫描字幕寻找 Logo，避免把口播里的次要产品错当成主产品。
- 主产品没有可信 Logo 资产时保持无外置 Logo，不拿字幕中的其他品牌代替，也不让生图模型发明近似标识；此时用准确产品名和真实界面建立识别。
- 如果标题、字幕、视频画面或截图能明确判断主产品有 Logo，但 `references/product-assets.md` 暂时没有对应资产，先联网寻找官方或可信来源的透明 PNG，归档到 `$SKILL_DIR/assets/product-logos/`；配置了 `product_asset_mirror` 时再同步到镜像目录。通过 `--logo` 传给脚本，高频复用的产品同步补充到 `product-assets.md` 和脚本的自动匹配表。
- 取帧策略是「本地预筛」：脚本用 ffmpeg 低分辨率扫描整段视频，对每帧算清晰度(拉普拉斯方差)、亮度、内容度，硬过滤掉黑屏/纯白/纯色/loading/模糊帧，再按时间分桶取每段最清晰的一帧，产出若干**真实高清候选**交给分析模型按语义挑最佳帧。全程不调模型选帧、不上传整段视频。这是唯一的自动取帧路径，没有旧的「视频选帧」/均匀盲采兜底——预筛若失败会直接报错，不会静默降级。
- `--frame-count <N>`：本地预筛产出多少个候选帧供分析模型挑选，默认 8。候选越多模型选择越好，但分析请求越大。
- `--scan-fps <N>`：本地预筛扫描的采样帧率，默认 0=自动（≤5 分钟视频用 2fps，更长用 1fps）。想抓更细的瞬间可调高。
- `--candidate-seconds 1,8,24.5`：手动指定取帧时间点，跳过本地预筛。已经知道哪几秒是关键画面时用。
- `--aspect all|both|3x4|4x3|16x9`：默认 `all` 并行生成三版；`both` 为兼容旧调用，只生成 `3:4` 和 `4:3`；单独重跑时只生成指定画幅。
- `--bilibili-size <尺寸>`：B 站个人空间 `16:9` 伴随版的 API 尺寸，默认 `1280x720`；B 站默认上传源仍是 `4:3` 主封面。
- 副标题默认放开。如需禁用副标题、让外层只剩主标题，传 `--no-allow-subtitle`。
- 创作者头像由本地代码在生图后合成，不作为 Gemini 或 `gpt-image-2` 的参考图上传。是否启用及素材路径来自用户配置；公开 Skill 默认关闭。默认布局参数为：3:4 宽约 55%、顶部约 58%、向右越界约 6%；4:3 宽约 38%、顶部约 40%、向右越界约 3%；16:9 宽约 32%、顶部约 40%、右侧内收约 2%。
- 用户明确要求无人物封面时传 `--no-default-creator-portrait`。配置启用头像时默认保留；未配置时保持无人物。

排查与验证：

- `--dry-run`：不调任何 API，只准备本地文件和 prompt，用于核对路径、规则文件和素材是否就位。
- `--skip-generate`：只跑 Gemini 分析和写 prompt，不调用图片 API。用来看 Gemini 选了哪一帧、标题怎么断行、prompt 写成什么样。
- `--generation-only`：用 `/images/generations` 而非 `/images/edits`，屏幕帧和 Logo 参考图不上传给图片 API；头像启用时始终只在本地合成。

## 脚本职责

- 脚本路径：优先 `$SKILL_DIR/scripts/generate_oil_cover.py`，否则使用用户配置 `script_path`
- 默认分析模型：`google/gemini-3.5-flash`
- 默认生图模型：`openai/gpt-image-2`
- 默认规则文件：`references/cover-rules.md`
- 默认输出位置：视频（或图片）所在目录。最终封面命名 `<视频名>_3x4.png`、`<视频名>_4x3.png`、`<视频名>_16x9.png`，直接落在影片旁边方便查找；分析、prompt、原始响应等中间产物收进 `<视频名>.oil-cover/` 子目录。传 `--output-root` 可改到别处。

脚本负责用 ffmpeg 本地扫描+评分预筛出若干高清候选帧（默认策略，无需调模型），把候选交给视觉模型分析、由模型按语义选出最佳封面帧并生成封面方案和提示词、保存 sidecar、并行调用所选图片服务、生成无人物底图。用户配置启用头像时，再用 Pillow 把透明头像按画幅参数合成到右下角；头像不会进入 视觉或图片 API 的参考图列表。底图保存在 `<视频名>.oil-cover/<画幅>.generated-base.png`，合成记录保存在 `portrait_composite.json`，最终封面写到影片目录。本地预筛的打分明细写在 `<视频名>.oil-cover/frame_selection_local.json`。
